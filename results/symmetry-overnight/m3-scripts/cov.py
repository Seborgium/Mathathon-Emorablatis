"""Exact MUB analysis of the H(Z_6)-covariant bases of C^6 (Z[zeta_24] arithmetic)."""
from itertools import combinations
from math import gcd
from fractions import Fraction
from zeta import *
from wh import glaw, ginv, GROUP

MAXISO = {
 'inf':  [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5)],
 'm0':   [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0)],
 'm1':   [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)],
 'm2':   [(0,0),(1,2),(2,4),(3,0),(4,2),(5,4)],
 'm3':   [(0,0),(1,3),(2,0),(3,3),(4,0),(5,3)],
 'm4':   [(0,0),(1,4),(2,2),(3,0),(4,4),(5,2)],
 'm5':   [(0,0),(1,5),(2,4),(3,3),(4,2),(5,1)],
 'v0':   [(0,0),(0,3),(2,0),(2,3),(4,0),(4,3)],
 'v1':   [(0,0),(0,3),(2,2),(2,5),(4,1),(4,4)],
 'v2':   [(0,0),(0,3),(2,1),(2,4),(4,2),(4,5)],
 'w0':   [(0,0),(0,2),(0,4),(3,0),(3,2),(3,4)],
 'w1':   [(0,0),(0,2),(0,4),(3,1),(3,3),(3,5)],
}

def preimage(S):
    return frozenset((t,a,b) for t in range(6) for (a,b) in S)

MM = {k: preimage(set(v)) for k, v in MAXISO.items()}
CENT = frozenset((t,0,0) for t in range(6))

def intersect_mod_center(k1, k2):
    return (MM[k1] & MM[k2]) == CENT

def quotient_order(g):
    """order of g modulo the centre."""
    cur=(0,0,0); o=0
    while True:
        cur = glaw(cur,g); o += 1
        if cur[1]==0 and cur[2]==0: return o
        if o > 12: raise RuntimeError

def generator(k):
    """element (t,a,b) of M with (a,b) generating pi(M) (order 6 mod Z);
    prefer t=0 and a a unit, so that W(a,b) is a single 6-cycle."""
    M = MM[k]
    cands = sorted(M, key=lambda e: (e[0] != 0, gcd(e[1], 6) != 1, e))
    for (t,a,b) in cands:
        if (a,b) == (0,0): continue
        if quotient_order((t,a,b)) == 6:
            return (t,a,b)
    raise RuntimeError("no generator "+k)

def eigenbasis(a, b):
    """Eigenvectors (unnormalised, norm^2=6) of W(a,b)=X^a Z^b. Entries are monomials."""
    seen=set(); cols=[]
    for j0 in range(6):
        if j0 in seen: continue
        cyc=[j0]; seen.add(j0); j=(j0+a)%6
        while j!=j0:
            cyc.append(j); seen.add(j); j=(j+a)%6
        L=len(cyc); s=sum(cyc)
        lam_pow = POW[(4*b*s) % 24]
        lams=[k for k in range(24) if pow_ring(POW[k],L)==lam_pow]
        assert len(lams)==L, (L,lams)
        for k in lams:
            alpha={cyc[0]:0}   # exponents
            cur=0
            for i in range(L-1):
                cur = (cur + 4*b*cyc[i] - k) % 24
                alpha[cyc[i+1]] = cur
            cols.append([POW[alpha[t]] if t in alpha else ZERO for t in range(6)])
    # multiply each vector by lam-independent constant so that norms are 6?  already: entries unit
    return cols

def pow_ring(x,n):
    r=ONE
    for _ in range(n): r=mul(r,x)
    return r

def inner(u,v):
    s=ZERO
    for i in range(6): s=add(s,mul(u[i],conj(v[i])))
    return s

def is_flat(cols):
    return all(not is_zero(x) for vec in cols for x in vec)

def norm2(vec):
    """squared norm of an unnormalised eigenvector: number of non-zero entries
    (each entry is a monomial, hence of modulus 1)."""
    return sum(1 for x in vec if not is_zero(x))

def unbiased(c1,c2):
    """Exact test: |<u,v>|^2 = ||u||^2 ||v||^2 / 6  for all pairs."""
    for u in c1:
        for v in c2:
            ip = inner(u, v)
            if scal(6, mul(ip, conj(ip))) != scal(norm2(u)*norm2(v), ONE):
                return False
    return True

if __name__ == "__main__":
    bases={}
    for k in MAXISO:
        t,a,b = generator(k)
        cols = eigenbasis(a,b)
        assert len(cols)==6, (k,len(cols))
        bases[k]=cols
        print(f"{k:4s} gen {(t,a,b)}  flat: {is_flat(cols)}")
    keys=list(MAXISO)
    print("\nflatness/unbiasedness table (U = unbiased, . = not, = self)")
    for k1 in keys:
        row=[]
        for k2 in keys:
            row.append("=" if k1==k2 else ("U" if unbiased(bases[k1],bases[k2]) else "."))
        print(f"{k1:4s} "+" ".join(row))
    print("\ncriterion  M cap M' = Z  (U = expected unbiased):")
    for k1 in keys:
        row=[]
        for k2 in keys:
            row.append("=" if k1==k2 else ("U" if intersect_mod_center(k1,k2) else "."))
        print(f"{k1:4s} "+" ".join(row))
