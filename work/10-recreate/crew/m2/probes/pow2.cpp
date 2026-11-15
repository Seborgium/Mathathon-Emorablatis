// Does libm pow(x,2) equal the separately rounded x*x on this host?
// Compiled with the faithful flags: g++ -O3 -march=native -ffp-contract=off
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <cmath>
static double from_bits(uint64_t b){double d;memcpy(&d,&b,8);return d;}
static uint64_t bits(double d){uint64_t b;memcpy(&b,&d,8);return b;}
int main(){
  volatile double two=2.0;
  long n=0,bad=0; double w1=0,w2=0; uint64_t wb=0;
  auto chk=[&](double x){
    if(!std::isfinite(x))return;
    volatile double vx=x;
    double p=std::pow(vx,two);     // real libm call (errno visible to the compiler)
    double m=x*x;                  // one mulsd
    n++;
    if(bits(p)!=bits(m)){bad++; if(bad==1){w1=p;w2=m;wb=bits(x);} }
  };
  chk(0.0); chk(-0.0); chk(1.0); chk(-1.0); chk(1.5); chk(0.1);
  chk(std::ldexp(1.0,-537)); chk(std::ldexp(1.0,-538)); chk(0x1p-600); chk(0x1p-1074);
  chk(1e-160); chk(1e-162); chk(0x1p511); chk(1.7976931348623157e308);
  chk(std::nextafter(1.0,2.0)); chk(1.0+0x1p-52);
  uint64_t s=0x243F6A8885A308D3ULL;
  for(long i=0;i<4000000;i++){
    s^=s<<13; s^=s>>7; s^=s<<17;
    chk(from_bits(s));
  }
  printf("samples %ld mismatches %ld\n",n,bad);
  if(bad)printf("first: x=%a pow=%a mul=%a\n",from_bits(wb),w1,w2);
  return bad?1:0;
}
