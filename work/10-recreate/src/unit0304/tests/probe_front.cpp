// probe_front.cpp -- test-only driver (not part of the frozen interface).
// Prints the front end of the pipeline: pi, w, the tab table digest, xs (count + full dump),
// each ys[a] (count + digest + dump at verbosity 2), and the cover constants RN2, T, K, m
// as hex floats + bits, so an R2 failure can be bisected without a 7-minute run.
#include "../include/cover.hpp"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>

static uint64_t fnv(const std::string&s,uint64_t h=1469598103934665603ULL){
  for(unsigned char c:s){h^=c;h*=1099511628211ULL;} return h;
}
static std::string canon(const xy&p){
  char buf[256];
  snprintf(buf,sizeof buf,"%d %d %d %d %d %d %a\n",p.b[0],p.b[1],p.b[2],p.b[3],p.b[4],p.s,p.g);
  return buf;
}
static void bits(const char*name,double x){
  uint64_t u; memcpy(&u,&x,8);
  printf("%s %a %016llx\n",name,x,(unsigned long long)u);
}
int main(int argc,char**argv){
  environment();
  int nn = argc>1? atoi(argv[1]) : 112;
  int verb = argc>2? atoi(argv[2]) : 0;   // 0 summary, 1 xs dump, 2 xs+ys dump
  seeds S; S.build(nn);
  printf("n %d\n",n); bits("w",w); bits("pi",pi);
  std::string T; for(int i=0;i<n;i++){ T+=canon(xy{ar{i,i,i,i,i},0,0.,{0.,0.}}); }
  printf("tab_digest %016llx\n",(unsigned long long)fnv(T));
  printf("xs %zu\n",S.xs.size());
  std::string X; uint64_t hx=1469598103934665603ULL;
  for(size_t t=0;t<S.xs.size();t++){ auto s=canon(S.xs[t]); hx=fnv(s,hx); X+=s; }
  printf("xs_digest %016llx\n",(unsigned long long)hx);
  if(verb>=1) fputs(X.data(),stdout);
  for(int a=0;a<n;a++){
    std::string Y; uint64_t hy=1469598103934665603ULL;
    for(auto&p:S.ys[a]){ auto s=canon(p); hy=fnv(s,hy); Y+=s; }
    printf("ys %d %zu %016llx\n",a,S.ys[a].size(),(unsigned long long)hy);
    if(verb>=2) fputs(Y.data(),stdout);
  }
  // cover constants, recomputed exactly as coverSeeds::run does
  coverSeeds C; C.R=.032; C.dual=2;
  C.RN2=sq(1)*std::pow(C.R*n,2)-.0001;
  C.T=std::pow(std::sqrt(C.RN2)+1.5,2);
  C.K=int(C.R*n+.51); C.K=std::max(1,C.K); C.m=(n+C.K-1)/C.K;
  bits("RN2",C.RN2); bits("T",C.T);
  printf("intT %d K %d m %d\n",int(C.T),C.K,C.m);
  // the pow(x,2) question: is pow(x,2) bit-identical to x*x here?
  double a=C.R*n, b=a*a; uint64_t u1,u2; double p1=std::pow(a,2); memcpy(&u1,&b,8); memcpy(&u2,&p1,8);
  printf("pow_square_identical %d %016llx %016llx\n",(int)(u1==u2),(unsigned long long)u1,(unsigned long long)u2);
  return 0;
}
