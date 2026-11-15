// Verify membership, exact gap rules and rigorous shared-displacement intersections
// for every P record in a seed-cover witness stream. No coverage decision is made
// solely by this file: it connects the archived identities to the independent
// complete rigorous X/Y enumerations and to R/C/D outcome checks elsewhere.
#define main dual_checker_main_unused
#include "seed_dual_mpfr.cpp"
#undef main
#include <fstream>
#include <unordered_map>
#include <unordered_set>
void divrange(Iv&z,const Iv&a,const Iv&b){
 mpfr_t l[4],u[4];for(int i=0;i<4;i++){mpfr_init2(l[i],P);mpfr_init2(u[i],P);}
 for(int i=0;i<4;i++){
  mpfr_srcptr x=(i&1)?a.hi:a.lo,y=(i&2)?b.hi:b.lo;
  mpfr_div(l[i],x,y,MPFR_RNDD);mpfr_div(u[i],x,y,MPFR_RNDU);
 }
 mpfr_set(z.lo,l[0],MPFR_RNDD);mpfr_set(z.hi,u[0],MPFR_RNDU);
 for(int i=1;i<4;i++){if(mpfr_cmp(l[i],z.lo)<0)mpfr_set(z.lo,l[i],MPFR_RNDD);if(mpfr_cmp(u[i],z.hi)>0)mpfr_set(z.hi,u[i],MPFR_RNDU);}
 for(int i=0;i<4;i++){mpfr_clear(l[i]);mpfr_clear(u[i]);}
}
std::array<Iv,2> extend(const unsigned char*b,int shared,Data&d,const std::array<Iv,2>&c){
 Iv lo,hi;integer(lo,-1);integer(hi,1);mpfr_div_si(lo.lo,lo.lo,2,MPFR_RNDD);mpfr_div_si(hi.lo,hi.lo,2,MPFR_RNDD);mpfr_div_si(hi.hi,hi.hi,2,MPFR_RNDU);
 Iv E;mpfr_const_pi(E.lo,MPFR_RNDD);mpfr_mul_si(E.lo,E.lo,5,MPFR_RNDD);mpfr_div_si(E.lo,E.lo,448,MPFR_RNDD);
 mpfr_const_pi(E.hi,MPFR_RNDU);mpfr_mul_si(E.hi,E.hi,5,MPFR_RNDU);mpfr_div_si(E.hi,E.hi,448,MPFR_RNDU);
 for(int kind=0;kind<5;kind++){
  int j=kind==0?shared:(kind<=shared?kind-1:kind);
  if(kind>0&&j==shared)continue;
  Iv a,bx,dot,r;zero(a);zero(r);
  // Shared direction is J_shared; perpendicular direction is R90(J_j)=(-sin,cos).
  auto project=[&](const Iv&co,const Iv&si,int part)->Iv{
   Iv out;
   if(kind==0) mpfr_set(out.lo,(part?si:co).lo,MPFR_RNDD),mpfr_set(out.hi,(part?si:co).hi,MPFR_RNDU);
   else if(part==0){mpfr_neg(out.lo,si.hi,MPFR_RNDD);mpfr_neg(out.hi,si.lo,MPFR_RNDU);}
   else {out=co;}
   return out;
  };
  Iv v0=project(d.tab[b[j]][0],d.tab[b[j]][1],0),v1=project(d.tab[b[j]][0],d.tab[b[j]][1],1);
  mul(a,v0,d.tab[b[shared]][0]);Iv a2;mul(a2,v1,d.tab[b[shared]][1]);add(a,a,a2);
  if(mpfr_sgn(a.lo)<=0&&mpfr_sgn(a.hi)>=0){
   if(getenv("EXTEND_DEBUG"))fprintf(stderr,"skip kind%d j%d a=[%.17g,%.17g]\n",kind,j,mpfr_get_d(a.lo,MPFR_RNDD),mpfr_get_d(a.hi,MPFR_RNDU));
   continue;
  }
  if(getenv("EXTEND_DEBUG"))fprintf(stderr,"do kind%d j%d\n",kind,j); // inconclusive direction: remove only this constraint
  Iv lhs;mul(lhs,v0,c[0]);Iv rhs;mul(rhs,v1,c[1]);add(lhs,lhs,rhs);
  mul(a2,v0,v0);mul(rhs,v1,v1);add(a2,a2,rhs);root(a2,a2);mul(r,E,a2);
  for(int j2=0;j2<5;j2++){
   if(j2==shared)continue;
   mul(a2,v0,d.tab[b[j2]][0]);mul(rhs,v1,d.tab[b[j2]][1]);add(a2,a2,rhs);absolute(a2,a2);
   mpfr_div_si(a2.lo,a2.lo,2,MPFR_RNDD);mpfr_div_si(a2.hi,a2.hi,2,MPFR_RNDU);add(r,r,a2);
  }
  if(getenv("EXTEND_DEBUG"))fprintf(stderr,"  lhs=%.17g a=['%.17g','%.17g']\n",mpfr_get_d(lhs.hi,MPFR_RNDU),mpfr_get_d(a.lo,MPFR_RNDD),mpfr_get_d(a.hi,MPFR_RNDU));
  Iv nv=lhs;
  Iv mid;divrange(mid,nv,a);absolute(a2,a);divrange(rhs,r,a2);
  Iv newlo,newhi;sub(newlo,mid,rhs);add(newhi,mid,rhs);
   if(getenv("EXTEND_DEBUG"))fprintf(stderr,"kind%d a=%.17g mid=%.17g rad=%.17g nest=%.17g %.17g\n",kind,mpfr_get_d(a.hi,MPFR_RNDU),mpfr_get_d(mid.hi,MPFR_RNDU),mpfr_get_d(rhs.hi,MPFR_RNDU),mpfr_get_d(newlo.lo,MPFR_RNDD),mpfr_get_d(newhi.hi,MPFR_RNDU));
  if(mpfr_cmp(newlo.lo,lo.lo)>0)mpfr_set(lo.lo,newlo.lo,MPFR_RNDD);
  if(mpfr_cmp(newhi.hi,hi.hi)<0)mpfr_set(hi.hi,newhi.hi,MPFR_RNDU);
 }
 return {lo,hi};
}
int gap(const unsigned char*b){
 unsigned q[5];for(int j=0;j<5;j++)q[j]=b[j];std::sort(q,q+5);
 int g=std::max(2*q[0]+1,224-2*q[4]-1);for(int j=0;j<4;j++)g=std::max(g,2*int(q[j+1]-q[j]));return g;
}
int main(int argc,char**argv){
 if(argc!=5){fprintf(stderr,"usage: seed.wit census_x census_y limit(0=all)\n");return 2;}
 uint64_t lim=strtoull(argv[4],nullptr,10);Data d;
 std::unordered_map<uint64_t,uint32_t> yid;yid.reserve(1000000);
 std::vector<std::array<unsigned char,5>> ydata;
 std::vector<std::array<Iv,2>> yclip;
 std::array<std::vector<uint32_t>,112> ygroup;
 std::vector<uint32_t> yordinal;
 auto code=[](const unsigned char*b){uint64_t z=0;for(int j=0;j<5;j++)z=z*112+b[j];return z;};
 auto load=[&](const char*p,bool isX,std::vector<std::array<unsigned char,6>>&out){
  std::ifstream f(p);std::string tag,margin;int bad=0;
  while(f>>tag){unsigned char b[5];unsigned v[5];int flag;
   if(!(f>>v[0]>>v[1]>>v[2]>>v[3]>>v[4]>>flag))return -1;
   for(int j=0;j<5;j++)b[j]=v[j];std::getline(f,margin);if(flag!=0)return -1;
   if(isX){int s=0;for(int j=1;j<5;j++)if(labs(2*b[j]+1-112)<labs(2*b[s]+1-112))s=j;
    out.push_back({b[0],b[1],b[2],b[3],b[4],(unsigned char)s});
   } else {
    uint64_t q=code(b);if(yid.count(q)){bad++;continue;}
    std::array<unsigned char,5> record={b[0],b[1],b[2],b[3],b[4]};
    yid[q]=ydata.size();ydata.push_back(record);
    yordinal.push_back(ygroup[b[0]].size());ygroup[b[0]].push_back(ydata.size()-1);
    auto cone=d.rhs(b);yclip.push_back(extend(b,0,d,cone));
   }
  }return bad;
 };
 std::vector<std::array<unsigned char,6>> xx;
 if(load(argv[2],true,xx)<0||load(argv[3],false,xx)){fprintf(stderr,"failed to load accepted censuses\n");return 2;}
 if(xx.size()!=22829||ydata.size()!=829306){fprintf(stderr,"wrong accepted census cardinality %zu/%zu\n",xx.size(),ydata.size());return 2;}
 FILE*f=fopen(argv[1],"rb");char magic[8];readn(f,magic,8);if(std::string(magic,8)!="SEEDWIT1")abort();unsigned char bb[8];readn(f,bb,8);
 uint32_t n=u4(bb),nx=u4(bb+4);std::vector<std::array<unsigned char,6>> xs(nx);
 for(auto&x:xs){unsigned char tag;readn(f,&tag,1);if(tag)abort();readn(f,x.data(),6);}
 if(xs!=xx){fprintf(stderr,"X traversal mismatch\n");return 2;}
 for(auto&a:xs){int s=0;for(int j=1;j<5;j++)if(abs(2*a[j]+1-n)<abs(2*a[s]+1-n))s=j;if(s!=a[5]){fprintf(stderr,"selected position wrong\n");return 2;}}
 std::vector<std::array<Iv,2>> xr(nx),xc(nx);
 for(size_t i=0;i<nx;i++){xr[i]=d.rhs(xs[i].data());xc[i]=extend(xs[i].data(),xs[i][5],d,xr[i]);}
 std::vector<std::vector<uint8_t>> seen(nx);for(size_t i=0;i<nx;i++)seen[i].assign(ygroup[xs[i][xs[i][5]]].size(),0);
 uint64_t pairs=0,bad=0,gapbad=0,disjoint=0,duplicates=0,notY=0;
 while(!lim||pairs<lim){unsigned char h[9];size_t got=fread(h,1,9,f);if(!got)break;if(got!=9||h[0]!='P')abort();
  unsigned char out[9];readn(f,out,9);double v[4];if(out[0]=='D')readn(f,v,32); // independently checked by seed_dual_mpfr
  uint32_t xi=u4(h+1);auto&A=xs[xi];unsigned char*y=h+5,Y[5]={A[A[5]],y[0],y[1],y[2],y[3]};uint64_t q=code(Y);
  if(!yid.count(q)){notY++;bad++;pairs++;continue;}
  uint32_t iy=yid[q],j=yordinal[iy];
  if(seen[xi][j])duplicates++;else seen[xi][j]=1;
  if(A[0]>A[4]-A[3]+1||gap(A.data())>2*n-2*A[4]+2){gapbad++;bad++;}
  if(gap(Y)<2*n-2*A[4]-4){gapbad++;bad++;}
  auto&aiv=xc[xi],&biv=yclip[iy];
  if(mpfr_cmp(aiv[1].hi,biv[0].lo)<0||mpfr_cmp(biv[1].hi,aiv[0].lo)<0)disjoint++;
  pairs++;
 }
 uint64_t mandatory=0,missing=0;
 if(!lim){
  for(size_t i=0;i<nx;i++){
   auto&A=xs[i];
   for(size_t j=0;j<ygroup[A[A[5]]].size();j++){
    uint32_t iy=ygroup[A[A[5]]][j];
    if(gap(ydata[iy].data())<2*n-2*A[4]-4)continue;
    auto&aiv=xc[i],&biv=yclip[iy];
    if(mpfr_cmp(aiv[1].hi,biv[0].lo)<0||mpfr_cmp(biv[1].hi,aiv[0].lo)<0)continue;
    mandatory++;if(!seen[i][j])missing++;
   }
  }
 }
 bool complete=!lim&&feof(f);
 printf("{\"pairs_processed\":%llu,\"independent_X_membership\":true,\"invalid_Y\":%llu,\"gap_violations\":%llu,\"rigorously_disjoint\":%llu,\"duplicate_pairs\":%llu,\"mandatory_eligible_pairs\":%llu,\"missing_mandatory\":%llu,\"complete_stream\":%s}\n",
  (unsigned long long)pairs,(unsigned long long)notY,(unsigned long long)gapbad,(unsigned long long)disjoint,(unsigned long long)duplicates,(unsigned long long)mandatory,(unsigned long long)missing,complete?"true":"false");
 if(complete&&(bad||missing||duplicates||mandatory+disjoint!=pairs)){
  fprintf(stderr,"coverage mismatch: bad=%llu missing=%llu duplicates=%llu mandatory=%llu\n",(unsigned long long)bad,(unsigned long long)missing,(unsigned long long)duplicates,(unsigned long long)mandatory);
  for(size_t i=0;i<xx.size();i++)for(size_t j=0;j<seen[i].size();j++){
   if(bad||duplicates||!missing)break;
   uint32_t iy=ygroup[xs[i][5]][j];auto&A=xs[i];
   if(gap(ydata[iy].data())<2*n-2*A[4]-4)continue;
   auto&aiv=xc[i],&biv=yclip[iy];
   if(mpfr_cmp(aiv[1].hi,biv[0].lo)<0||mpfr_cmp(biv[1].hi,aiv[0].lo)<0)continue;
   if(!seen[i][j]){fprintf(stderr,"first missing xi=%zu y=%u,%u,%u,%u,%u\\n",i,ydata[iy][0],ydata[iy][1],ydata[iy][2],ydata[iy][3],ydata[iy][4]);
    fprintf(stderr,"Xiv %.17g %.17g Yiv %.17g %.17g\n",mpfr_get_d(aiv[0].lo,MPFR_RNDD),mpfr_get_d(aiv[1].hi,MPFR_RNDU),mpfr_get_d(biv[0].lo,MPFR_RNDD),mpfr_get_d(biv[1].hi,MPFR_RNDU));goto done;}
  }
 done:return 1;
 }
 return 0;
}
