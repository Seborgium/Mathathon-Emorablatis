"""Cross-check of the source's formula Delta_A = [Lambda_0 : L_A] at every anchor
of the six flat H(Z_6)-covariant MUB triples of C^6."""
from itertools import combinations
from zeta import *
from cov import eigenbasis, generator, norm2, unbiased, MAXISO
from delta import all_flat_bases
from delta3 import delta_std_anchor, delta_general_anchor, standard_in_B, general_matrix
from latin import intersect_mod_center, keys
from delta import lattice_index
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

n = 6
fb = all_flat_bases()

def general_matrix_std(u):
    E = fb[u][0]
    return [[POW[E[i][j]] if E[i][j] is not None else ZERO for j in range(n)] for i in range(n)]

def matrices_in_anchor(anchor, others):
    """return the two other bases as 6x6 matrices of ring elements in anchor coordinates"""
    if anchor == 'inf':
        return [[POW[fb[u][0][i][j]] if fb[u][0][i][j] is not None else ZERO for i in range(n)] for j in range(n)] , None
    Bexp = fb[anchor][0]
    out = []
    for u in others:
        if u == 'inf':
            out.append(standard_in_B(Bexp))
        else:
            out.append(general_matrix(Bexp, fb[u][0]))
    return out

def index_at_anchor(M1, M2):
    """[Lambda_0 : L_A] from the exact support of P_A, where M1, M2 are the two other
    bases as 6x6 matrices of ring elements in the anchor's coordinates."""
    edges = [(i,j) for i in range(n) for j in range(n) if i != j]
    rels = set(); nz = 0
    for (i,j) in edges:
        for (k,l) in edges:
            s = ZERO
            for r in range(n):
                # U_{ir} conj(U_{jr}) conj(U_{kr}) U_{lr}
                s = add(s, mul(mul(M1[i][r], conj(M1[j][r])), mul(conj(M1[k][r]), M1[l][r])))
                s = add(s, mul(mul(M2[i][r], conj(M2[j][r])), mul(conj(M2[k][r]), M2[l][r])))
            if not is_zero(s):
                nz += 1
                row = [0]*6
                row[i] += 1; row[j] -= 1; row[k] -= 1; row[l] += 1
                if any(row): rels.add(tuple(row[:5]))
    M = sp.Matrix(sorted(rels))
    sm = smith_normal_form(M, domain=sp.ZZ)
    diag = [abs(int(sm[i,i])) for i in range(min(sm.rows, sm.cols))]
    idx = 1
    for d in diag: idx *= d
    return idx, nz

if __name__ == "__main__":
    FLAT = {'inf','m0','m1','m2','m3','m4','m5'}
    triples = [s for s in combinations(keys, 3)
               if set(s) <= FLAT and all(intersect_mod_center(x,y) for x,y in combinations(s,2))]
    print("triples:", len(triples))
    allok = True
    for T in triples:
        for anchor in T:
            others = [u for u in T if u != anchor]
            if anchor == 'inf':
                D = delta_std_anchor(fb[others[0]][0], fb[others[1]][0])
                mats = [general_matrix_std(u) for u in others]
            else:
                mats = matrices_in_anchor(anchor, others)
                D = delta_general_anchor(fb[anchor][0], mats)
            idx, nz = index_at_anchor(mats[0], mats[1])
            print(f"  triple {T} anchor {anchor:4s}: |Delta| = {len(D):2d}   [Lambda_0:L_A] = {idx:2d}   nonzero P entries = {nz}")
            if len(D) != idx: allok = False
    print("formula Delta_A = [Lambda_0:L_A] holds at every checked anchor:", allok)
