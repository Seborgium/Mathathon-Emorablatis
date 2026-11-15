#define main seed_cover_main_unused
#include "covout.cpp"
#undef main
int main(int argc,char**argv){
 environment(); seeds S;S.build(112);
 if(argc!=6)abort();
 int xi=atoi(argv[1]),prior=atoi(argv[2]);
 coverSeeds C;vector<SI>X;
 for(auto p:S.xs)X.push_back(extend(p,p.s));
 SI&A=X[xi],&P=X[prior];
 ar pt;F(j,4)pt[j]=atoi(argv[j+2]);
 // argv is xi,p0,y1,y2,y3,y4; prior is always 0 in this diagnostic.
 ar cur={A.p.b[A.p.s],atoi(argv[2]),atoi(argv[3]),atoi(argv[4]),0};
 // instead take the target tail from diagnostic p0=pt components below
 ar tailor={(ar::value_type)pt[0],(ar::value_type)pt[1],(ar::value_type)pt[2],(ar::value_type)pt[3]};
 // See invocation: xi,prior,y1,y2,y3,y4; recover previous tail from its first centre line manually.
 ar target={A.p.b[A.p.s],0,55,110,110};
 ar prev={P.p.b[P.p.s],0,55,57,110};
 ar oldtail={0,55,57,110};
 for(auto B:S.ys[A.p.b[A.p.s]]){
  if(B.b[1]==55 && B.b[2]==55 && B.b[3]==110 && B.b[4]==110){
   SI bb=extend(B,0);array<int,9>k={A.p.b[0]-P.p.b[0],A.p.b[1]-P.p.b[1],A.p.b[2]-P.p.b[2],A.p.b[3]-P.p.b[3],A.p.b[4]-P.p.b[4],
      B.b[1]-oldtail[0],B.b[2]-oldtail[1],B.b[3]-oldtail[2],B.b[4]-oldtail[3]};
   double best=C.supdual(k,A,bb,2);
   printf("best %.17g\n",best);for(double z:C.chosen)printf("v %.17g\n",z);
   return 0;
  }
 }
return 1;}
