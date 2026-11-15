"""Exact toolkit for the diagonal-symmetry detector of a MUB triple in C^6.

Representation: a flat (unitary, all entries modulus 1/sqrt(d)) matrix M is stored as an
integer exponent matrix E mod N with M = zeta_N^E / sqrt(d).

Projection entries:  36*P_{ij,kl} = sum_r z^{B_ir - B_jr - B_kr + B_lr} + (same for C)
which is an element of Z[z_N]; it is zero iff the reduced coefficient vector vanishes.
"""
import itertools, numpy as np
import sympy as sp
from sympy import Poly, Symbol, rem
from sympy.matrices.normalforms import smith_normal_form
from sympy import ZZ

def phi_poly(N):
    x = Symbol("x")
    return Poly(sp.cyclotomic_poly(N, x), x)

class Ring:
    def __init__(self, N=24):
        self.N=N; self.phi=phi_poly(N); self.deg=sp.degree(self.phi)
        self.pows=[self.reduce(k) for k in range(N)]
    def reduce(self,k):
        k%=self.N
        if k==0: v=np.zeros(self.deg,dtype=np.int64); v[0]=1; return v
        x=Symbol("x")
        p=rem(Poly(x**k,x),self.phi)
        v=np.zeros(self.deg,dtype=np.int64)
        for j in range(self.deg): v[j]=int(p.nth(j))
        return v
    def sumexp(self, exps):
        v=np.zeros(self.deg,dtype=np.int64)
        for k in exps: v+=self.pows[int(k)%self.N]
        return v
    def iszero(self,v): return not np.any(v)

def flat_to_complex(E, N=24):
    return np.exp(2j*np.pi*np.asarray(E)/N)/np.sqrt(E.shape[0])

# ---------------- generic (numeric) helpers, used to cross-check ----------------
def proj_entries_numeric(B,C):
    d=B.shape[0]
    P=np.zeros((d*d,d*d),dtype=complex)
    for i in range(d):
        for j in range(d):
            if i==j: continue
            for k in range(d):
                for l in range(d):
                    if k==l: continue
                    val=sum(B[i,r]*np.conj(B[j,r])*np.conj(B[k,r])*B[l,r] for r in range(d))
                    val+=sum(C[i,r]*np.conj(C[j,r])*np.conj(C[k,r])*C[l,r] for r in range(d))
                    P[i*d+j,k*d+l]=val
    return P

def proj_support_numeric(B,C,tol=1e-9):
    d=B.shape[0]; S=set()
    for i in range(d):
        for j in range(d):
            if i==j: continue
            for k in range(d):
                for l in range(d):
                    if k==l: continue
                    val=sum(B[i,r]*np.conj(B[j,r])*np.conj(B[k,r])*B[l,r] for r in range(d))
                    val+=sum(C[i,r]*np.conj(C[j,r])*np.conj(C[k,r])*C[l,r] for r in range(d))
                    if abs(val)>tol: S.add((i,j,k,l))
    return S

# ---------------- exact support / lattice ----------------
def proj_support_exact(Bexp,Cexp,ring):
    d=Bexp.shape[0]; S=[]
    for i in range(d):
        for j in range(d):
            if i==j: continue
            for k in range(d):
                for l in range(d):
                    if k==l: continue
                    v=ring.sumexp(list(Bexp[i]-Bexp[j]-Bexp[k]+Bexp[l])) \
                     +ring.sumexp(list(Cexp[i]-Cexp[j]-Cexp[k]+Cexp[l]))
                    if not ring.iszero(v): S.append((i,j,k,l))
    return S

def relation_row(i,j,k,l,d=6):
    r=np.zeros(d,dtype=np.int64); r[i]+=1; r[j]-=1; r[k]-=1; r[l]+=1
    return r

def relation_matrix(S,d=6):
    rows=set()
    for (i,j,k,l) in S:
        r=relation_row(i,j,k,l,d)
        if np.any(r): rows.add(tuple(int(t) for t in r[:d-1]))
    return sorted(rows)

def f3_rank(rows):
    if not rows: return 0
    M=[[int(x)%3 for x in r] for r in rows]
    return _rank_mod(M,p=3)

def _rank_mod(M,p):
    M=[list(map(lambda x: x%p,row)) for row in M]
    n=len(M); m=len(M[0]); r=0
    for c in range(m):
        piv=None
        for i in range(r,n):
            if M[i][c]%p: piv=i; break
        if piv is None: continue
        M[r],M[piv]=M[piv],M[r]
        inv=pow(M[r][c],-1,p)
        M[r]=[(x*inv)%p for x in M[r]]
        for i in range(n):
            if i!=r and M[i][c]%p:
                f=M[i][c]
                M[i]=[(a-f*b)%p for a,b in zip(M[i],M[r])]
        r+=1
        if r==n: break
    return r

def index_of_lattice(rows):
    """[Z^5 : lattice spanned by rows] (0 if rank deficient)."""
    if not rows: return 0
    M=sp.Matrix([list(r) for r in rows])
    s=smith_normal_form(M,domain=ZZ)
    dg=[abs(int(s[i,i])) for i in range(min(s.shape))]
    if len(dg)<M.cols or any(d==0 for d in dg): return 0
    p=1
    for d in dg: p*=d
    return p

def delta_anchor(Bexp,Cexp,ring):
    S=proj_support_exact(Bexp,Cexp,ring)
    rows=relation_matrix(S)
    return dict(nsupp=len(S), nrel=len(rows), f3=f3_rank(rows), index=index_of_lattice(rows))
