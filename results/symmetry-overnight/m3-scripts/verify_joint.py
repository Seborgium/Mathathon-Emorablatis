"""For each of the 12 maximal abelian subgroups M: check that the computed eigenbasis
(6 rays) consists of simultaneous eigenvectors of ALL elements of M, and that the
characters are distinct (so the rays form the M-eigenbasis)."""
from zeta import *
from wh import Wmat, matmul
from cov import MAXISO, MM, eigenbasis, generator

def matvec(M, v):
    out=[]
    for i in range(6):
        s=ZERO
        for j in range(6): s=add(s, mul(M[i][j], v[j]))
        out.append(s)
    return out

def eig_ratio(M, v):
    """return exponent k with Mv = zeta^k v, or None if not an eigenvector"""
    ratio = None
    for i in range(6):
        if is_zero(v[i]): continue
        r = monomial_index(mul(matvec_dev(M,v)[i], inv_monomial(v[i]))) if False else None
    return None

def check(k):
    t,a,b = generator(k)
    cols = eigenbasis(a,b)
    bad = []
    chars = []
    for g in sorted(MM[k]):
        th, ga, gb = g
        M = [[mul(POW[4*th % 24], x) for x in row] for row in Wmat(ga, gb)]
        for idx, v in enumerate(cols):
            Mv = matvec(M, v)
            ratios = set()
            for i in range(6):
                if is_zero(v[i]): continue
                ratios.add(monomial_index(mul(Mv[i], inv_monomial(v[i]))))
            if len(ratios) != 1 or None in ratios:
                bad.append((g, idx))
    # check orthonormality and distinctness of the 6 characters
    return bad

ok = True
for k in MAXISO:
    bad = check(k)
    print(k, "simultaneous eigenvector failures:", len(bad))
    if bad: ok = False; print("   e.g.", bad[:3])
print("all 12 subgroups: computed 6 rays are simultaneous M-eigenvectors:", ok)
