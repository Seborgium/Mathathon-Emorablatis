"""F_3 rank of the relation matrix at every anchor of the covariant triples
(equivalently: whether the source's detector Xi vanishes there)."""
from itertools import combinations
import sympy as sp
from zeta import *
from cov import MAXISO, intersect_mod_center
from delta import all_flat_bases
from index3 import matrices_in_anchor, general_matrix_std
keys = list(MAXISO)
n = 6
fb = all_flat_bases()

def relations_and_rank(M1, M2):
    edges = [(i,j) for i in range(n) for j in range(n) if i != j]
    rels = set(); nz = 0
    for (i,j) in edges:
        for (k,l) in edges:
            s = ZERO
            for r in range(n):
                s = add(s, mul(mul(M1[i][r], conj(M1[j][r])), mul(conj(M1[k][r]), M1[l][r])))
                s = add(s, mul(mul(M2[i][r], conj(M2[j][r])), mul(conj(M2[k][r]), M2[l][r])))
            if not is_zero(s):
                nz += 1
                row = [0]*6
                row[i] += 1; row[j] -= 1; row[k] -= 1; row[l] += 1
                if any(row): rels.add(tuple(row[:5]))
    if not rels:
        return 0, nz
    M = sp.Matrix(sorted(rels))
    r3 = len(M.T.rref(iszerofunc=lambda x: x % 3 == 0, simplify=lambda x: x % 3)[1]) if False else None
    # rank over F_3 by reducing mod 3
    A = sp.Matrix([[v % 3 for v in r] for r in M.tolist()])
    rank3 = A.rank(iszerofunc=lambda x: x % 3 == 0)
    return rank3, nz

FLAT = {'inf','m0','m1','m2','m3','m4','m5'}
triples = [s for s in combinations(keys, 3)
           if set(s) <= FLAT and all(intersect_mod_center(x,y) for x,y in combinations(s,2))]
for T in triples:
    out = []
    for anchor in T:
        others = [u for u in T if u != anchor]
        if anchor == 'inf':
            mats = [general_matrix_std(u) for u in others]
        else:
            mats = matrices_in_anchor(anchor, others)
        r3, nz = relations_and_rank(mats[0], mats[1])
        out.append(f"{anchor}: rank_F3={r3}, Xi=0:{r3<5}")
    print(T, "; ".join(out))
