// Streaming MPFR-128 certificate of Lemma 2.9(2.19) for the seed-cover witness.
// Parsing is constant-memory apart from the 22829 X tuples. Each accepted dual's
// v is exact binary64 input; all remaining quantities use outward enclosures.
#include <mpfr.h>
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>
constexpr int P=128;
struct Iv{
 mpfr_t lo,hi;
 Iv(){mpfr_init2(lo,P);mpfr_init2(hi,P);}
 ~Iv(){mpfr_clear(lo);mpfr_clear(hi);}
 Iv(const Iv&a){mpfr_init2(lo,P);mpfr_init2(hi,P);mpfr_set(lo,a.lo,MPFR_RNDD);mpfr_set(hi,a.hi,MPFR_RNDU);}
 Iv&operator=(const Iv&a){if(this!=&a){mpfr_set(lo,a.lo,MPFR_RNDD);mpfr_set(hi,a.hi,MPFR_RNDU);}return *this;}
};
void zero(Iv&z){mpfr_set_ui(z.lo,0,MPFR_RNDD);mpfr_set_ui(z.hi,0,MPFR_RNDU);}
void integer(Iv&z,int x){mpfr_set_si(z.lo,x,MPFR_RNDD);mpfr_set_si(z.hi,x,MPFR_RNDU);}
void add(Iv&z,const Iv&a,const Iv&b){mpfr_add(z.lo,a.lo,b.lo,MPFR_RNDD);mpfr_add(z.hi,a.hi,b.hi,MPFR_RNDU);}
void sub(Iv&z,const Iv&a,const Iv&b){mpfr_sub(z.lo,a.lo,b.hi,MPFR_RNDD);mpfr_sub(z.hi,a.hi,b.lo,MPFR_RNDU);}
void muli(Iv&z,const Iv&a,int k){
 if(k>=0){mpfr_mul_si(z.lo,a.lo,k,MPFR_RNDD);mpfr_mul_si(z.hi,a.hi,k,MPFR_RNDU);}
 else {mpfr_mul_si(z.lo,a.hi,k,MPFR_RNDD);mpfr_mul_si(z.hi,a.lo,k,MPFR_RNDU);}
}
void mul(Iv&z,const Iv&a,const Iv&b){
 mpfr_t l[4],u[4];for(int i=0;i<4;i++){mpfr_init2(l[i],P);mpfr_init2(u[i],P);}
 for(int i=0;i<4;i++){
  mpfr_srcptr x=(i&1)?a.hi:a.lo,y=(i&2)?b.hi:b.lo;
  mpfr_mul(l[i],x,y,MPFR_RNDD);mpfr_mul(u[i],x,y,MPFR_RNDU);
 }
 mpfr_set(z.lo,l[0],MPFR_RNDD);mpfr_set(z.hi,u[0],MPFR_RNDU);
 for(int i=1;i<4;i++){
  if(mpfr_cmp(l[i],z.lo)<0)mpfr_set(z.lo,l[i],MPFR_RNDD);
  if(mpfr_cmp(u[i],z.hi)>0)mpfr_set(z.hi,u[i],MPFR_RNDU);
 }
 for(int i=0;i<4;i++){mpfr_clear(l[i]);mpfr_clear(u[i]);}
}
void divpos(Iv&z,const Iv&a,const Iv&b){mpfr_div(z.lo,a.lo,b.hi,MPFR_RNDD);mpfr_div(z.hi,a.hi,b.lo,MPFR_RNDU);}
void absolute(Iv&z,const Iv&a){
 Iv t;
 if(mpfr_sgn(a.lo)>=0){t=a;z=t;return;}
 if(mpfr_sgn(a.hi)<=0){
  mpfr_neg(t.lo,a.hi,MPFR_RNDD);mpfr_neg(t.hi,a.lo,MPFR_RNDU);z=t;return;
 }
 mpfr_set_ui(t.lo,0,MPFR_RNDD);mpfr_neg(t.hi,a.lo,MPFR_RNDU);
 if(mpfr_cmp(a.hi,t.hi)>0)mpfr_set(t.hi,a.hi,MPFR_RNDU);
 z=t;
}
void sq(Iv&z,const Iv&a){
 if(mpfr_sgn(a.lo)>=0){mpfr_sqr(z.lo,a.lo,MPFR_RNDD);mpfr_sqr(z.hi,a.hi,MPFR_RNDU);}
 else if(mpfr_sgn(a.hi)<=0){mpfr_sqr(z.lo,a.hi,MPFR_RNDD);mpfr_sqr(z.hi,a.lo,MPFR_RNDU);}
 else{
  mpfr_set_ui(z.lo,0,MPFR_RNDD);mpfr_sqr(z.hi,a.hi,MPFR_RNDU);
  mpfr_t t;mpfr_init2(t,P);mpfr_sqr(t,a.lo,MPFR_RNDU);if(mpfr_cmp(t,z.hi)>0)mpfr_set(z.hi,t,MPFR_RNDU);mpfr_clear(t);
 }
}
void root(Iv&z,const Iv&a){mpfr_sqrt(z.lo,a.lo,MPFR_RNDD);mpfr_sqrt(z.hi,a.hi,MPFR_RNDU);}
void readn(FILE*f,void*p,size_t n){if(fread(p,1,n,f)!=n){fprintf(stderr,"unexpected EOF\n");abort();}}
uint32_t u4(const unsigned char*b){return b[0]|b[1]<<8|b[2]<<16|(uint32_t)b[3]<<24;}

struct Data{
 Iv piLo,piHi,twoPi,E,RN;
 Iv tab[112][2];
 std::array<Iv,2> rhs(const unsigned char*b){
  Iv re,im;zero(re);zero(im);
  for(int j=0;j<5;j++){add(re,re,tab[b[j]][0]);add(im,im,tab[b[j]][1]);}
  std::array<Iv,2> out;muli(out[0],im,-112);divpos(out[0],out[0],twoPi);
  Iv r;integer(r,1);add(r,re,r);muli(r,r,112);divpos(out[1],r,twoPi);return out;
 }
 Data(){
  mpfr_const_pi(piLo.lo,MPFR_RNDD);mpfr_const_pi(piLo.hi,MPFR_RNDD);
  mpfr_const_pi(piHi.lo,MPFR_RNDU);mpfr_const_pi(piHi.hi,MPFR_RNDU);
  mpfr_add(twoPi.lo,piLo.lo,piLo.lo,MPFR_RNDD);mpfr_add(twoPi.hi,piHi.hi,piHi.hi,MPFR_RNDU);
  for(int b=0;b<112;b++){
   Iv l,h;muli(l,piLo,2*b+1);muli(l,l,2);mpfr_div_si(l.lo,l.lo,224,MPFR_RNDD);mpfr_div_si(l.hi,l.hi,224,MPFR_RNDD);
   muli(h,piHi,2*b+1);muli(h,h,2);mpfr_div_si(h.lo,h.lo,224,MPFR_RNDU);mpfr_div_si(h.hi,h.hi,224,MPFR_RNDU);
   for(int kind=0;kind<2;kind++){
    mpfr_t a[4];for(auto&x:a)mpfr_init2(x,P);
    auto fn=kind?mpfr_sin:mpfr_cos;
    fn(a[0],l.lo,MPFR_RNDD);fn(a[1],l.hi,MPFR_RNDU);fn(a[2],h.lo,MPFR_RNDD);fn(a[3],h.hi,MPFR_RNDU);
    mpfr_set(tab[b][kind].lo,a[0],MPFR_RNDD);mpfr_set(tab[b][kind].hi,a[0],MPFR_RNDU);
    for(auto&x:a){if(mpfr_cmp(x,tab[b][kind].lo)<0)mpfr_set(tab[b][kind].lo,x,MPFR_RNDD);if(mpfr_cmp(x,tab[b][kind].hi)>0)mpfr_set(tab[b][kind].hi,x,MPFR_RNDU);}
    for(auto&x:a)mpfr_clear(x);
   }
  }
  mpfr_const_pi(E.lo,MPFR_RNDD);mpfr_mul_si(E.lo,E.lo,1251,MPFR_RNDD);mpfr_div_si(E.lo,E.lo,112000,MPFR_RNDD);
  mpfr_const_pi(E.hi,MPFR_RNDU);mpfr_mul_si(E.hi,E.hi,1251,MPFR_RNDU);mpfr_div_si(E.hi,E.hi,112000,MPFR_RNDU);
  mpfr_set_str(RN.lo,"12.844956",10,MPFR_RNDD);mpfr_set_str(RN.hi,"12.844956",10,MPFR_RNDU);
 }
};
int main(int argc,char**argv){
 if(argc<2||argc>3){fprintf(stderr,"usage: seed.wit [max_pairs]\n");return 2;}
 uint64_t limit=argc==3?strtoull(argv[2],nullptr,10):~0ull;
 FILE*f=fopen(argv[1],"rb");if(!f){perror(argv[1]);return 2;}
 char magic[8];readn(f,magic,8);if(std::string(magic,8)!="SEEDWIT1")abort();unsigned char bb[8];readn(f,bb,8);
 uint32_t n=u4(bb),nx=u4(bb+4);std::vector<std::array<unsigned char,6>> xs(nx);
 for(auto&x:xs){unsigned char tag;readn(f,&tag,1);if(tag)abort();readn(f,x.data(),6);}
 Data d;
 std::vector<std::array<Iv,2>> xr(nx);for(size_t i=0;i<nx;i++)xr[i]=d.rhs(xs[i].data());
 uint64_t pairs=0,duals=0,proved=0,und=0,failed=0;double worst=-1e100;uint64_t records=0;
 while(pairs<limit){
  unsigned char h[9];size_t got=fread(h,1,9,f);if(!got)break;if(got!=9||h[0]!='P')abort();records++;
  unsigned char out[9];readn(f,out,9);if(out[0]!='D')continue;
  double vv[4];readn(f,vv,32);duals++;
  uint32_t xi=u4(h+1),pi=u4(out+1);auto&A=xs[xi],&P=xs[pi];unsigned char*y=h+5,*py=out+5;int sc=A[5];
  unsigned char Y[5]={A[sc],y[0],y[1],y[2],y[3]};auto yr=d.rhs(Y);
  Iv bound,zabs,rdot;zero(bound);zero(zabs);zero(rdot);long long squared=0;
  for(int a=0;a<4;a++){
   Iv vi;mpfr_set_d(vi.lo,vv[a],MPFR_RNDD);mpfr_set_d(vi.hi,vv[a],MPFR_RNDU);
   Iv tmp;muli(tmp,a<2?xr[xi][a]:yr[a-2],2);mul(tmp,tmp,vi);add(rdot,rdot,tmp);
  }
  for(int j=0;j<9;j++){
   int k=j<5?int(A[j])-int(P[j]):int(y[j-5])-int(py[j-5]);squared+=k*k;
   Iv dot,vi;zero(dot);
   for(int a=0;a<4;a++){
    const Iv*q=nullptr;
    if(j<5&&a<2)q=&d.tab[A[j]][a];
    if(j>=5&&a>=2)q=&d.tab[Y[j-4]][a-2];
    if(j==sc&&a>=2)q=&d.tab[Y[0]][a-2];
    if(!q)continue;
    if(q<&d.tab[0][0] || q>&d.tab[111][1]){fprintf(stderr,"bad q: j%d a%d sc%d Yidx%d Aidx%d q=%p low=%p high=%p\n",j,a,sc,j>=5?Y[j-4]:-1,j<5?A[j]:-1,(void*)q,(void*)&d.tab[0][0],(void*)&d.tab[111][1]);abort();}
    mpfr_set_d(vi.lo,vv[a],MPFR_RNDD);mpfr_set_d(vi.hi,vv[a],MPFR_RNDU);
    Iv term;mul(term,*q,vi);add(dot,dot,term);
   }
   Iv ki,z;integer(ki,k);sub(z,ki,dot);
    absolute(z,z);
    add(zabs,zabs,z);
  }
  Iv norms[2];
  for(int a=0;a<2;a++){
   Iv va,vb;mpfr_set_d(va.lo,vv[2*a],MPFR_RNDD);mpfr_set_d(va.hi,vv[2*a],MPFR_RNDU);mpfr_set_d(vb.lo,vv[2*a+1],MPFR_RNDD);mpfr_set_d(vb.hi,vv[2*a+1],MPFR_RNDU);
   Iv qa,qb;sq(qa,va);sq(qb,vb);add(qa,qa,qb);root(norms[a],qa);
  }
  add(bound,zabs,rdot);Iv ens;add(ens,norms[0],norms[1]);mul(ens,ens,d.E);muli(ens,ens,2);add(bound,bound,ens);
  Iv full,margin;integer(margin,squared);add(full,bound,margin);integer(margin,225);mpfr_div_si(margin.lo,margin.lo,100,MPFR_RNDD);mpfr_div_si(margin.hi,margin.hi,100,MPFR_RNDU);add(full,full,margin);
  integer(margin,1);mpfr_div_si(margin.lo,margin.lo,100,MPFR_RNDD);mpfr_div_si(margin.hi,margin.hi,100,MPFR_RNDU);add(full,full,margin);
  sub(margin,full,d.RN);double excess=mpfr_get_d(margin.hi,MPFR_RNDU);worst=std::max(worst,excess);
  if(mpfr_cmp(full.hi,d.RN.lo)<0)proved++;
  else {if(mpfr_cmp(full.lo,d.RN.hi)>0)failed++;else und++;if(failed+und<5)fprintf(stderr,"unresolved/fail pair %llu xi %u\n",(unsigned long long)pairs,xi);}
  pairs++;
 }
 bool complete=pairs==limit||!feof(f)?false:true;
 printf("{\"duals_processed\":%llu,\"total_records_scanned\":%llu,\"duals\":%llu,\"proved\":%llu,\"failed\":%llu,\"undecided\":%llu,\"largest_upper_excess\":%.17g,\"complete_stream\":%s,\"mpfr\":\"%s\"}\n",
   (unsigned long long)pairs,(unsigned long long)records,(unsigned long long)duals,(unsigned long long)proved,(unsigned long long)failed,(unsigned long long)und,worst,complete?"true":"false",mpfr_get_version());
 fclose(f);return 0;
}
