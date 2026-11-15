import sys, numpy as np
import mpmath as mp
mp.mp.dps=60
src=open('/workspace/nucleus/work/projects/p-20d35e783d5d4092acb8bd94b19cf30b/repo/.scratch/mub6/fouriercheck2.py').read()
exec(src.split('def dephase_unimodular')[0])
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

def conjT(M):
    d=M.rows; e=M.cols; out=mp.zeros(e,d)
    for i in range(e):
        for j in range(d):
            out[i,j]=mp.conj(M[j,i])
    return out
def mmul(X,Y):
    d=X.rows; m=Y.cols; out=mp.zeros(d,m)
    for i in range(d):
        for j in range(m):
            out[i,j]=mp.fsum([X[i,k]*Y[k,j] for k in range(X.cols)])
    return out

def delta(M, N_, thr=mp.mpf('1e-30')):
    """M,N: the two other bases in the anchor's coordinates (mpmath, entries 1/sqrt6)."""
    d=6; vals={}
    for i in range(d):
        for j in range(d):
            if i==j: continue
            for k in range(d):
                for l in range(d):
                    if k==l: continue
                    v=mp.fsum([M[i,r]*mp.conj(M[j,r])*mp.conj(M[k,r])*M[l,r] for r in range(d)]) \
                     +mp.fsum([N_[i,r]*mp.conj(N_[j,r])*mp.conj(N_[k,r])*N_[l,r] for r in range(d)])
                    vals[(i,j,k,l)]=abs(v)
    nz=[v for v in vals.values() if v>thr]; z=[v for v in vals.values() if v<=thr]
    rows=set()
    for (i,j,k,l),v in vals.items():
        if v>thr:
            r=[0]*6; r[i]+=1; r[j]-=1; r[k]-=1; r[l]+=1
            if any(r): rows.add(tuple(r[:5]))
    rows=sorted(rows)
    sm=[abs(int(smith_normal_form(Matrix([list(r) for r in rows]),domain=ZZ)[i,i])) for i in range(5)] if rows else [0]
    return dict(nsupp=len(nz), nrel=len(rows), smith=sm,
                min_nz=min(nz) if nz else None, max_z=max(z) if z else mp.mpf(0))

def three_deltas(A,B,C,**kw):
    Ai=conjT(A); Bi=conjT(B); Ci=conjT(C)
    out={}
    out['A']=delta(mmul(Ai,B), mmul(Ai,C), **kw)
    out['B']=delta(mmul(Bi,A), mmul(Bi,C), **kw)
    out['C']=delta(mmul(Ci,A), mmul(Ci,B), **kw)
    return out

if __name__=="__main__":
    print("=== JMSSW family {I, F(0,b(t)), C(t)}   (mpmath dps=60, threshold 1e-30) ===")
    for t in ['0.5','0.6','0.7','0.8','0.9','1.0','1.1']:
        Ct,b=Cmat(mp.mpf(t))
        U2=Fmat(0,b)
        A=mp.eye(6); B=U2; C=Ct
        dev=max(mp.norm(mp.matrix(6,6,lambda i,j: mp.conj(B[j,i]))) , 0)
        mus=[]
        for X,Y in ((A,B),(A,C),(B,C)):
            Z=mmul(conjT(X),Y); mus.append(max(abs(abs(Z[i,j])-1/mp.sqrt(6)) for i in range(6) for j in range(6)))
        print(f"t={t} b={mp.nstr(b,8)}  MUB deviation={mp.nstr(max(mus),3)}")
        for k,v in three_deltas(A,B,C).items():
            print(f"   anchor {k}: supp={v['nsupp']:3d} rel={v['nrel']:3d} smith={v['smith']} "
                  f"min|P|={mp.nstr(v['min_nz'],4) if v['min_nz'] else None} max|P_zero|={mp.nstr(v['max_z'],3)}")
