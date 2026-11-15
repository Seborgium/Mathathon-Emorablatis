"""Xi (F_3 rank of the relation matrix) at all anchors for one (2,3,3) and one (6,6,6)
member of m5's family: does the product identity get a genuine test?"""
import sympy as sp
from gen_delta import *
from zeta import ZERO, add, mul, conj, is_zero

def rankF3(X, Y):
    """F_3 rank of the relation matrix of the anchor whose other two bases (in its own
    coordinates) are the 6x6 matrices X, Y."""
    n = 6
    rels = set(); nz = 0
    edges = [(i,j) for i in range(n) for j in range(n) if i != j]
    for (i,j) in edges:
        for (k,l) in edges:
            s = ZERO
            for r in range(n):
                s = add(s, mul(mul(X[i][r], conj(X[j][r])), mul(conj(X[k][r]), X[l][r])))
                s = add(s, mul(mul(Y[i][r], conj(Y[j][r])), mul(conj(Y[k][r]), Y[l][r])))
            if not is_zero(s):
                nz += 1
                row = [0]*6
                row[i] += 1; row[j] -= 1; row[k] -= 1; row[l] += 1
                if any(row): rels.add(tuple(row[:5]))
    A = sp.Matrix([[v % 3 for v in r] for r in sorted(rels)])
    return A.rank(iszerofunc=lambda x: x % 3 == 0), nz

F, seen = family()
allmat = [it for v in seen.values() for it in v]
good = [it[0] for it in allmat if it[1]]
import random
Random = random.Random(5)
Id = [[ONE if i == j else ZERO for j in range(6)] for i in range(6)]
inst = []
for _ in range(40):
    a, b = Random.randrange(len(good)), Random.randrange(len(good))
    H0, H1 = good[a], good[b]
    K0 = rmul(H0, F); K1 = [[mul(I12, x) for x in row] for row in rmul(H1, F)]
    U = block(H0, H1); V = block(K0, K1)
    if not (mub(Id,U) and mub(Id,V) and mub(U,V)): continue
    pat = tuple(len(delta_general(A,B,C)) for A,B,C in [(Id,U,V),(U,Id,V),(V,Id,U)])
    inst.append((pat, U, V, H0, H1))
    if len({p for p, *_ in inst}) == 2 and len(inst) > 6: break
for pat, U, V, H0, H1 in inst:
    if pat != (2,3,3): continue
    print("pattern", pat)
    for name, (X, A, B, C) in [("I",(Id,Id,U,V)), ("U",(U,U,Id,V)), ("V",(V,V,Id,U))]:
        M1 = rmul(rconjT(A), B); M2 = rmul(rconjT(A), C)
        r3, nz = rankF3(M1, M2)
        print(f"   anchor {name}: rank_F3 = {r3}  (Xi {'=0' if r3<5 else '>0'})  nonzero P entries = {nz}", flush=True)
    break
