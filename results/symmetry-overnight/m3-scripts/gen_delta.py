"""Independent cross-check of m5's (Delta_A,Delta_B,Delta_C) = (2,3,3) family.

Construction (m5, d2; source sec.4 'uniform case'):
  H0, H1 3x3 complex Hadamards with H_i F flat;  K0 = H0 F, K1 = i H1 F;
  U = [[H0,H0],[H1,-H1]],  V = [[K0,K0],[K1,-K1]];   triple = (I_6, U, V).
Matrices are carried *unnormalised* over Z[zeta_24] with a known constant modulus per
basis (u_I = 1, u_U = 1, u_V = 3); Delta is scale-free and is computed from the
definition by brute force over all 6! permutations with exact proportionality tests.
"""
from itertools import permutations, product
from fractions import Fraction
from zeta import *

n = 6
OM3 = POW[8]
SQ3 = add(POW[2], POW[22])
SQ2 = add(POW[3], POW[21])
I12 = POW[6]

def rmul(A, B):
    m, k, n2 = len(A), len(B), len(B[0])
    return [[_sum(mul(A[i][t], B[t][j]) for t in range(k)) for j in range(n2)] for i in range(m)]

def _sum(xs):
    s = ZERO
    for x in xs: s = add(s, x)
    return s

def rconjT(A):
    return [[conj(A[j][i]) for j in range(len(A))] for i in range(len(A[0]))]

def abs2(x):
    y = mul(x, conj(x))
    assert all(v == 0 for v in y[1:]), y
    return Fraction(y[0])

def is_mod(M, val):
    return all(abs2(x) == Fraction(val) for row in M for x in row)

def F3un():
    return [[POW[(8*i*j) % 24] for j in range(3)] for i in range(3)]

def diag3(ph):
    return [[ph[i] if i == j else ZERO for j in range(3)] for i in range(3)]

def perm3(p):
    return [[ONE if p[j] == i else ZERO for j in range(3)] for i in range(3)]

def canonical_basis(M):
    cols = []
    for j in range(len(M[0])):
        col = [M[i][j] for i in range(len(M))]
        k0 = next(i for i in range(len(col)) if not is_zero(col[i]))
        inv = inv_field(col[k0])
        cols.append(tuple(mul(x, inv) for x in col))
    return tuple(sorted(cols))

def mult_table(a):
    T = [[0]*8 for _ in range(8)]
    for j in range(8):
        e = [0]*8; e[j] = 1
        c = mul(a, tuple(e))
        for i in range(8): T[i][j] = c[i]
    return T

def inv_field(a):
    T = mult_table(a)
    A = [[Fraction(T[i][j]) for j in range(8)] + [Fraction(1 if i == 0 else 0)] for i in range(8)]
    for c in range(8):
        piv = next(r for r in range(c, 8) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        pv = A[c][c]
        A[c] = [x/pv for x in A[c]]
        for r in range(8):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f*y for x, y in zip(A[r], A[c])]
    sol = [A[i][8] for i in range(8)]
    return tuple(sol)          # Fractions in general: 1/x lives in Q(zeta_24)

def colnorms(A):
    return [sum(abs2(A[i][j]) for i in range(n)) for j in range(n)]

def mub(A, B):
    """exact MUB test: |<u,v>|^2 = ||u||^2 ||v||^2 / 6 for all pairs."""
    na, nb = colnorms(A), colnorms(B)
    for j in range(n):
        for k in range(n):
            ip = _sum(mul(conj(A[i][j]), B[i][k]) for i in range(n))
            if abs2(ip) != na[j]*nb[k]/6:
                return False
    return True

def delta_general(A, B, C):
    """Delta at anchor A (A's columns orthonormal basis; scale irrelevant)."""
    AB = rmul(rconjT(A), B)
    AC = rmul(rconjT(A), C)
    out = set()
    def test(X, i, ip, j, jp, sigma):
        return (mul(mul(X[i][sigma[j]], X[ip][sigma[jp]]), mul(X[i][jp], X[ip][j]))
                == mul(mul(X[i][sigma[jp]], X[ip][sigma[j]]), mul(X[i][j], X[ip][jp])))
    pre = [(0,1,0,1),(0,2,0,2),(1,2,1,2),(0,1,1,2),(2,3,0,1)]
    def rank1(X, sigma):
        for (i,ip,j,jp) in pre:
            if not test(X, i, ip, j, jp, sigma): return False
        for i in range(n-1):
            for ip in range(i+1, n):
                for j in range(n-1):
                    for jp in range(j+1, n):
                        if not test(X, i, ip, j, jp, sigma): return False
        return True
    def lam_from(X, sigma):
        lam = [mul(X[i][sigma[0]], inv_field(X[i][0])) for i in range(n)]
        inv0 = inv_field(lam[0])
        return [mul(x, inv0) for x in lam]
    def preserves(X, lam, sigma):
        for j in range(n):
            base = mul(lam[0], mul(X[0][j], inv_field(X[0][sigma[j]])))
            for i in range(1, n):
                if mul(lam[i], mul(X[i][j], inv_field(X[i][sigma[j]]))) != base:
                    return False
        return True
    for sigma in permutations(range(n)):
        if not rank1_ok_pre(AB, sigma): continue
        lam = lam_from(AB, sigma)
        for tau in permutations(range(n)):
            if preserves(AC, lam, tau):
                out.add(tuple(lam))
                break
    return out

def rank1_ok_pre(X, sigma):
    pre = [(0,1,0,1),(0,2,0,2),(1,2,1,2),(0,1,1,2),(2,3,0,1)]
    def test(i, ip, j, jp):
        return (mul(mul(X[i][sigma[j]], X[ip][sigma[jp]]), mul(X[i][jp], X[ip][j]))
                == mul(mul(X[i][sigma[jp]], X[ip][sigma[j]]), mul(X[i][j], X[ip][jp])))
    for (i,ip,j,jp) in pre:
        if not test(i, ip, j, jp): return False
    for i in range(n-1):
        for ip in range(i+1, n):
            for j in range(n-1):
                for jp in range(j+1, n):
                    if not test(i, ip, j, jp): return False
    return True

def block(A, B):
    M = [[ZERO]*6 for _ in range(6)]
    for i in range(3):
        for j in range(3):
            M[i][j] = A[i][j]; M[i][j+3] = A[i][j]
            M[i+3][j] = B[i][j]; M[i+3][j+3] = neg(B[i][j])
    return M

def family():
    F = F3un()
    seen = {}
    for a in product(range(3), repeat=3):
        D = diag3([POW[(8*a[i]) % 24] for i in range(3)])
        for p in permutations(range(3)):
            H = rmul(rmul(F, D), perm3(p))
            HF = rmul(H, F)
            seen.setdefault(canonical_basis(H), []).append((H, is_mod(HF, 3)))
    return F, seen

if __name__ == "__main__":
    F, seen = family()
    allmat = [it for v in seen.values() for it in v]
    good = [it[0] for it in allmat if it[1]]
    print("H = F D Pi matrices:", len(allmat), " distinct basis keys:", len(seen), " with |H F|^2 = 3:", len(good))
    Id = [[ONE if i == j else ZERO for j in range(6)] for i in range(6)]
    import random
    random.seed(7)
    pairs = [(0,1),(0,2),(1,2)] + [(random.randrange(len(good)), random.randrange(len(good))) for _ in range(3)]
    for (a,b) in pairs:
        H0 = good[a]; H1 = good[b]
        K0 = rmul(H0, F); K1 = [[mul(I12, x) for x in row] for row in rmul(H1, F)]
        U = block(H0, H1); V = block(K0, K1)
        ok = mub(Id,U) and mub(Id,V) and mub(U,V)
        pat = []
        for X, Y, Z in [(Id, U, V), (U, Id, V), (V, Id, U)]:
            pat.append(len(delta_general(X, Y, Z)))
        print(f"pair ({a},{b}) MUB={ok}  Delta pattern = {tuple(pat)}", flush=True)
