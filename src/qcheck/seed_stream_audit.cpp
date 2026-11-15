// Full streaming integrity + cheap-cover audit for src/emit/covout.cpp witnesses.
#include <array>
#include <cstdint>
#include <cstdio>
#include <unordered_set>
#include <string>
#include <vector>
#include <cmath>
#include <cstring>
using Key=std::array<unsigned char,10>;
struct H{size_t operator()(Key const&k)const{uint64_t h=1469598103934665603ULL;for(auto c:k){h^=c;h*=1099511628211ULL;}return h;}};
static void rd(FILE*f,void*p,size_t n){if(fread(p,1,n,f)!=n){fprintf(stderr,"unexpected EOF\n");abort();}}
static uint64_t u4(const unsigned char*b){return b[0]|(b[1]<<8)|(b[2]<<16)|((uint64_t)b[3]<<24);}
static Key key(unsigned char*x,unsigned char*y){return {x[0],x[1],x[2],x[3],x[4],x[5],y[0],y[1],y[2],y[3]};}
int main(int argc,char**argv){
 if(argc!=3 && argc!=4){fprintf(stderr,"usage: prefix.wit centres.txt [expected_prefix]\n");return 2;}
 FILE*f=fopen(argv[1],"rb");if(!f){perror(argv[1]);return 2;}
 char magic[8];rd(f,magic,8);if(std::string(magic,8)!="SEEDWIT1")abort();
 unsigned char b8[8];rd(f,b8,8);uint32_t n=u4(b8),nx=u4(b8+4);
 std::vector<std::array<unsigned char,6>> xs(nx);
 for(auto &x:xs){unsigned char tag;rd(f,&tag,1);if(tag!=0)abort();rd(f,x.data(),6);}
 FILE*fc=fopen(argv[2],"r");if(!fc){perror(argv[2]);return 2;}
 unsigned nc,nr;if(fscanf(fc,"%u%u",&nc,&nr)!=2)return 2;
 if(nc!=n)abort();std::unordered_set<Key,H> centres;centres.reserve(nr*2);
 for(size_t j=0;j<nr;j++){
  int z[10];for(int&i:z)if(fscanf(fc,"%d",&i)!=1)return 2;
  Key k;for(int i=0;i<10;i++){if(z[i]<0||z[i]>255)abort();k[i]=z[i];}
  if(!centres.insert(k).second){fprintf(stderr,"duplicate retained centre\n");return 1;}
 }
 fclose(fc);
 size_t prefix=centres.size();if(argc==4){prefix=strtoull(argv[3],nullptr,10);}
 uint64_t pairs=0,rr=0,cc=0,dd=0,cheapok=0,vbad=0;
 for(;;){
  unsigned char head[9];size_t got=fread(head,1,9,f);
  if(got==0){if(feof(f))break;perror("read");return 2;}
  if(got!=9 || head[0]!='P'){fprintf(stderr,"malformed pair at %llu\n",(unsigned long long)pairs);return 1;}
  uint32_t xi=u4(head+1);if(xi>=nx)return 1;
  unsigned char outcome[9];rd(f,outcome,9);
  char kind=outcome[0];uint32_t pi=u4(outcome+1);if(pi>xi||pi>=nx)return 1;
  unsigned char*y=head+5,*py=outcome+5;
  auto &a=xs[xi],&p=xs[pi];Key prev=key(p.data(),py);
  if(!centres.count(prev)){fprintf(stderr,"missing previous centre at %llu\n",(unsigned long long)pairs);return 1;}
  if(a[5]!=p[5]){fprintf(stderr,"selected-position mismatch at %llu\n",(unsigned long long)pairs);return 1;}
  if(kind=='R'){
   rr++;if(xi!=pi || memcmp(y,py,4)){fprintf(stderr,"bad fresh midpoint at %llu\n",(unsigned long long)pairs);return 1;}
  } else if(kind=='D'){
   dd++;double v[4];rd(f,v,32);for(double z:v)if(!std::isfinite(z)||std::abs(z)>10000)vbad++;
  } else if(kind=='C'){
   cc++;long long sq=0,ab=0;
   // Exact cheap witness (2.18), compared against exact 12.844956 = 802191/15625.
   // lhs = (4*(sum k^2 + sum |k|) + 9)/4 < 12.844956.
   for(int j=0;j<5;j++){long long k=int(a[j])-int(p[j]);sq+=k*k;ab+=std::llabs(k);}
   for(int j=0;j<4;j++){long long k=int(y[j])-int(py[j]);sq+=k*k;ab+=std::llabs(k);}
   if((4*sq+4*ab+9)*15625 >= 802191){fprintf(stderr,"cheap cover failed at %llu\n",(unsigned long long)pairs);return 1;}
   cheapok++;
  } else {fprintf(stderr,"unknown outcome at %llu\n",(unsigned long long)pairs);return 1;}
  pairs++;
 }
 fclose(f);
 printf("{\"N\":%u,\"Xtuples\":%zu,\"pairs\":%llu,\"R\":%llu,\"C\":%llu,\"D\":%llu,\"cheap_exact_pass\":%llu,\"nonfinite_dual_v\":%llu,\"fresh_centres_declared\":%zu,\"centres_in_source\":%zu,\"complete_parse\":true}\n",
   n,nx,(unsigned long long)pairs,(unsigned long long)rr,(unsigned long long)cc,(unsigned long long)dd,(unsigned long long)cheapok,(unsigned long long)vbad,prefix,centres.size());
 return (pairs && rr==prefix && !vbad)?0:1;
}
