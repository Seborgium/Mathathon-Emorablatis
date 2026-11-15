"""Independent outward evaluation of Lemma 2.9 (2.19) on emitted seed duals.
The emitted v is only a proposal. Inputs are exact bin pairs and binary64 components;
pi and every midpoint exp(2*pi*i*x) are enclosed by root_interval's tested kernel.
"""
import argparse,sys
from fractions import Fraction
from pathlib import Path
numdir=Path(__file__).resolve().parents[2]/'work'/'02-checker'/'src'/'root_interval'
sys.path.insert(0,str(numdir))
import num
from seed_witness import records

NORM=Fraction(112)*Fraction(0.032)
RN2=NORM*NORM-Fraction(1,10000)
SCALE=128

def iexp(b):
    return num.e2pii(Fraction(2*b+1,224))

def interval_AB(x,tail=None):
    bins,s=x
    if tail is not None:
        bins=[bins[s]]+list(tail)
    E=[iexp(b) for b in bins]
    c0=num.Iv.exact_int(0);c1=num.Iv.exact_int(0)
    for co,si in E:
        c0=c0+si;c1=c1+co
    twopi=num.PI*2
    one=num.Iv.exact_int(1)
    # (2.9); p*=-112c. Hence rhs=(-N Sim/(2pi), N(1+Sre)/(2pi))
    rhs=[(c0*(-112))._divpos(twopi),((c1+one)*112)._divpos(twopi)]
    return rhs

def _divpos(self,b):
    assert b.lo>0
    return num.Iv((self.lo << num.B) // b.hi, -((-(self.hi << num.B)) // b.lo))
num.Iv._divpos=_divpos

def support(cur,tail,prev,ptail,v,bins_current,bins_previous):
    bc,sc=bins_current;bp,sp=bins_previous
    assert sc==sp
    # Lemma 2.9 is evaluated in the original sorted X order; the shared coordinate
    # remains at position s. Moving it to zero is only the later isometric permutation.
    perm=list(range(5))
    k=[bc[sc]-bp[sc]]+[bc[j]-bp[j] for j in perm[1:]]+[tail[j]-ptail[j] for j in range(4)]
    J1=[iexp(bc[j]) for j in perm]
    J2=[iexp(bc[sc])]+[iexp(t) for t in tail]
    rows=[[entry[0],entry[1],num.Iv.exact_int(0),num.Iv.exact_int(0)] for entry in J1]
    rows += [[num.Iv.exact_int(0) for _ in range(4)] for _ in range(4)]
    for j in range(5):
        h=sc if j==0 else 4+j
        rows[h]=rows[h][:2]+list(J2[j])
    def dot(col):
        z=num.Iv.exact_int(0)
        for a in range(4): z=z+col[a]*num.Iv.dy(num.Dy.of(v[a]))
        return z
    zabs=num.Iv.exact_int(0)
    for j in range(9):
        zend=dot(rows[j])
        zabs=zabs+(num.Iv.dy(num.Dy.of(k[j]))-zend).abs()
    rhs=interval_AB(bins_current)+interval_AB(bins_current,tail)
    out=num.Iv.exact_int(0)
    for a,r in enumerate(rhs): out=out+r.mul_int(2)*num.Iv.dy(num.Dy.of(v[a]))
    nX=(num.Iv.dy(num.Dy.of(v[0])).sq()+num.Iv.dy(num.Dy.of(v[1])).sq()).sqrt()
    nY=(num.Iv.dy(num.Dy.of(v[2])).sq()+num.Iv.dy(num.Dy.of(v[3])).sq()).sqrt()
    E=num.PI*num.Iv.frac(Fraction(1251,1000*112))
    bound=zabs+out+(nX+nY)*E*2+num.Iv.frac(Fraction(1,100))
    k2=sum(a*a for a in k)
    full=bound+num.Iv.frac(Fraction(k2))+num.Iv.frac(Fraction(9,4))
    return full,num.Iv.frac(RN2)

def check(path,limit=None):
    N,xs,ev=records(path);rows=[]
    for i,(xi,tail,kind,prior,ptail,v) in enumerate(ev):
        if kind!=b'D':continue
        _,cur,pr=xs[xi][0],xs[xi],xs[prior]
        lhs,rhs=support((cur,tail),tail,(pr[0],ptail),ptail,v,cur,pr)
        decision=lhs.le(rhs)
        # A rejected case proves lhs>rhs; straddling is unresolved, never cheap acceptance.
        negative=rhs.le(-lhs)  # not expected; used only to distinguish refutation
        rows.append(dict(pair=i,xi=xi,tail=tail,prior=prior,verdict=decision,
                         upper_minus_RN2=lhs.hi-rhs.lo,lower_minus_RN2=lhs.lo-rhs.hi))
    print('duals',len(rows),'proved',sum(r['verdict'] is True for r in rows),
          'refuted',sum(r['verdict'] is False for r in rows),'undecided',sum(r['verdict'] is None for r in rows))
    if rows:
        print('largest certified excess',max(r['upper_minus_RN2'] for r in rows)/num.ONE)
    for r in rows:
        if r['verdict'] is not True:print(r)
    return rows

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('witness');a=ap.parse_args();check(a.witness)
