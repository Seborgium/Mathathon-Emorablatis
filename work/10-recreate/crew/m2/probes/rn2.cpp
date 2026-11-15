#include <cstdio>
#include <cmath>
#include <cstring>
#include <cstdint>
static uint64_t bits(double d){uint64_t b;memcpy(&b,&d,8);return b;}
int main(){
  int n=112; double R=.032; volatile double two=2.0;
  double x=R*n;
  double rn2_pow=std::pow((double)x,two)-.0001;   // covout.cpp:100
  double rn2_mul=x*x-.0001;
  double a_pow=std::pow(std::sqrt(rn2_pow)+1.5,two);   // covout.cpp:101
  double a_mul=(std::sqrt(rn2_mul)+1.5)*(std::sqrt(rn2_mul)+1.5);
  printf("x        = %a  (%.17g)\n",x,x);
  printf("pow(x,2) = %a   mul = %a   %s\n",std::pow((double)x,two),x*x, bits(std::pow((double)x,two))==bits(x*x)?"SAME":"DIFFER");
  printf("RN2      = %a / %a  %s\n",rn2_pow,rn2_mul,bits(rn2_pow)==bits(rn2_mul)?"SAME":"DIFFER");
  printf("T        = %a / %a  %s\n",a_pow,a_mul,bits(a_pow)==bits(a_mul)?"SAME":"DIFFER");
  printf("int(T)   = %d / %d ; (int)(RN2) = %d/%d\n",(int)a_pow,(int)a_mul,(int)rn2_pow,(int)rn2_mul);
  printf("sqrt(RN2) = %a  %s\n",std::sqrt(rn2_pow), bits(std::sqrt(rn2_pow))==bits(std::sqrt(rn2_mul))?"SAME":"DIFFER");
}
