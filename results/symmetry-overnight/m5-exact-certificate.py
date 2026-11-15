"""m5-exact-certificate.py -- exact certificate for the Delta=(2,3,3) MUB triple in C^6.

Exact arithmetic in Z[z], z = exp(2*pi*i/24), Phi_24 = x^8 - x^4 + 1  (= z^8 = z^4 - 1).
Every entry of every matrix below lies in  Q(z)  (indeed in (1/sqrt6) Z[z]), so the
zero / non-zero decision for the projection entries is an exact integer computation.

The triple {A = I6, B, C}:
    w = z^8,  F3 = (w^{ij})_{ij},  H0 = F3 diag(1,1,w),  H1 = F3 diag(1,1,w^2),
    K0 = H0 F3,  K1 = i H1 F3   (i = z^6),
    B = 2^{-1/2} [[H0,H0],[H1,-H1]] / sqrt3 ,   C = 2^{-1/2} [[K0,K0],[K1,-K1]] / 3 .
Storage: each flat basis M is stored as s*M with |s| = sqrt6, so all stored entries are
elements of Z[z]; only the zero set of the projection is used, and it is invariant under
multiplying a basis by a non-zero scalar as long as the two bases at an anchor carry
scalars of equal modulus (which is arranged below).

Run:  python3 m5-exact-certificate.py
"""


# ---------------------------------------------------------------- Z[z]/Phi_24
def rmul(a, b):
    c = [0] * 15
    for i in range(8):
        if a[i] == 0:
            continue
        for j in range(8):
            c[i + j] += a[i] * b[j]
    for k in range(14, 7, -1):          # z^k = z^{k-8}(z^4 - 1)
        v = c[k]
        if v:
            c[k - 8] -= v
            c[k - 4] += v
            c[k] = 0
    return tuple(c[:8])


def radd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def rneg(a):
    return tuple(-x for x in a)


def rscale(a, k):
    return tuple(k * x for x in a)


ZERO = (0,) * 8
ONE = (1,) + (0,) * 7
ZZ = (0, 1) + (0,) * 6


def rpow(k):
    r = ONE
    for _ in range(k % 24):
        r = rmul(r, ZZ)
    return r


def rconj(a):
    r = ZERO
    for k in range(8):
        if a[k]:
            r = radd(r, rscale(rpow((-k) % 24), a[k]))
    return r


def rsum(xs):
    r = ZERO
    for x in xs:
        r = radd(r, x)
    return r


def mmul(A, B):
    return [[rsum([rmul(A[i][t], B[t][j]) for t in range(len(B))]) for j in range(len(B[0]))]
            for i in range(len(A))]


def diagm(d):
    n = len(d)
    return [[d[i] if i == j else ZERO for j in range(n)] for i in range(n)]


# ---------------------------------------------------------------- the triple
w = rpow(8)              # exp(2 pi i /3)
i_unit = rpow(6)         # exp(i pi/2)
SQ3 = radd(rpow(2), rpow(22))     # 2 cos(pi/6) = sqrt3
SQ6 = rsum([rpow(1), rpow(23), rpow(5), rpow(19)])   # sqrt6
assert rmul(SQ6, SQ6) == rscale(ONE, 6), "sqrt6 wrong"
assert rmul(SQ3, SQ3) == rscale(ONE, 3), "sqrt3 wrong"

F3 = [[rpow((8 * j * k) % 24) for k in range(3)] for j in range(3)]      # w^{jk}, unnormalised
H0 = mmul(F3, diagm([ONE, ONE, w]))
H1 = mmul(F3, diagm([ONE, ONE, rmul(w, w)]))
K0 = mmul(H0, F3)
K1 = [[rmul(e, i_unit) for e in row] for row in mmul(H1, F3)]


def block(A, B, sgn=-1):
    n = len(A)
    M = [[ZERO] * (2 * n) for _ in range(2 * n)]
    for a in range(n):
        for b in range(n):
            M[a][b] = A[a][b]
            M[a][b + n] = A[a][b]
            M[a + n][b] = B[a][b]
            M[a + n][b + n] = B[a][b] if sgn == 1 else rneg(B[a][b])
    return M


#  sqrt6 * B = block(H0,H1)             (the H's carry the 1/sqrt3 factor)
#  sqrt6 * C = block(K0,K1) / sqrt3     (the K's carry 3 * 1/sqrt3)
#  store   B^ = 3 sqrt6 B = 3 block(H0,H1)   and   C^ = 3 sqrt6 C = sqrt3 block(K0,K1):
#  equal modulus |3 sqrt6| for the two scalar factors.
Bs = [[rscale(e, 3) for e in row] for row in block(H0, H1, -1)]
Cs = [[rmul(e, SQ3) for e in row] for row in block(K0, K1, -1)]

# --- sanity check against floating point
import numpy as np


def zc(e):
    return sum(c * np.exp(2j * np.pi * k / 24) for k, c in enumerate(e))


def toC(M):
    return np.array([[zc(e) for e in row] for row in M])


_wn = np.exp(2j * np.pi / 3)
_Fn = np.array([[_wn**(j * k) for k in range(3)] for j in range(3)]) / np.sqrt(3)
_H0 = _Fn @ np.diag([1, 1, _wn]); _H1 = _Fn @ np.diag([1, 1, _wn**2])
_U = np.block([[_H0, _H0], [_H1, -_H1]]) / np.sqrt(2)
_V = np.block([[_H0 @ _Fn, _H0 @ _Fn], [1j * _H1 @ _Fn, -1j * _H1 @ _Fn]]) / np.sqrt(2)
s = 3 * np.sqrt(6)
assert np.abs(toC(Bs) / s - _U).max() < 1e-12, "B mismatch"
assert np.abs(toC(Cs) / s - _V).max() < 1e-12, "C mismatch"
print("storage check: the stored matrices equal (3 sqrt6) x the numerical triple")


# ---------------------------------------------------------------- projections
def proj_support(U, V):
    n = len(U)
    nz = []
    for a in range(n):
        for b in range(n):
            if a == b:
                continue
            for c in range(n):
                for d in range(n):
                    if c == d:
                        continue
                    tot = ZERO
                    for r in range(n):
                        for M in (U, V):
                            tot = radd(tot, rmul(rmul(M[a][r], rconj(M[b][r])),
                                                 rmul(rconj(M[c][r]), M[d][r])))
                    if tot != ZERO:
                        nz.append((a, b, c, d))
    return nz


def relations(nz):
    rows = set()
    for (a, b, c, d) in nz:
        r = [0] * 6
        r[a] += 1; r[b] -= 1; r[c] -= 1; r[d] += 1
        rows.add(tuple(r[:5]))
    return sorted(rows)


import sympy as sp
from sympy.matrices.normalforms import smith_normal_form


def delta_of(U, V, name):
    nz = proj_support(U, V)
    rows = relations(nz)
    S = smith_normal_form(sp.Matrix(rows), domain=sp.ZZ)
    diag = [abs(int(S[k, k])) for k in range(5)]
    idx = 1
    for dd in diag:
        idx *= dd
    print("  anchor %s: %4d nonzero entries, %3d relation rows, Smith %s, Delta = %d"
          % (name, len(nz), len(rows), diag, idx))
    return idx, len(nz), tuple(diag)


def adj(M):
    return [[rconj(M[j][k]) for j in range(len(M))] for k in range(len(M[0]))]


def inner_mat(A, B):
    n = len(A)
    return [[rsum([rmul(rconj(A[k][a]), B[k][b]) for k in range(n)]) for b in range(len(B[0]))]
            for a in range(len(A[0]))]


print("\nprojection support and lattice index at the three anchors, exactly:")
dA = delta_of(Bs, Cs, "A=I6")
# anchor B: the other two bases are B^H and B^H C.  With Bs = s B, Cs = s C (s = 3 sqrt6 real),
# adj(Bs) = s B^H, inner_mat(Bs,Cs) = s^2 B^H C.  Multiplying the first by s makes both
# carry the scalar s^2, so the two stored matrices have equal scalar modulus.
BH = [[rmul(e, rscale(SQ6, 3)) for e in row] for row in adj(Bs)]
CB = inner_mat(Bs, Cs)
dB = delta_of(BH, CB, "B")
CH = [[rmul(e, rscale(SQ6, 3)) for e in row] for row in adj(Cs)]
BC = inner_mat(Cs, Bs)
dC = delta_of(CH, BC, "C")
print("\nDelta tuple (A,B,C) =", (dA[0], dB[0], dC[0]), " supports", (dA[1], dB[1], dC[1]))
assert (dA[0], dB[0], dC[0]) == (2, 3, 3), "unexpected Delta tuple"
assert dA[2] == (1, 1, 1, 1, 2) and dB[2] == (1, 1, 1, 1, 3) and dC[2] == (1, 1, 1, 1, 3)
print("Smith normal forms match the source's exact (3,3,2) example as a multiset -- OK")
