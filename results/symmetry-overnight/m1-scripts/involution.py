"""The Delta=2 anchor of the (2,3,3) triple: the involutive diagonal symmetry S, the source's
SS4 block normal form (6) and the (7) dichotomy.  Exact, Z[zeta_24]."""
from fractions import Fraction
import cyc
from cyc import add, mul, conj, zpow, canon, ZERO
import mubtools as T
import delta2_test as D

reps = [D.A, D.B6, D.C6]
Phi = {}
for i in range(3):
    for j in range(3):
        if i != j:
            Phi[(i, j)] = T.pair_phase(reps[i], reps[j])[0]

M = T.projections(Phi[(0, 1)], Phi[(0, 2)])
supp = T.support(M)
rows = T.relations(M, supp)
k, B = T.index_of(rows)
sols = T.annihilator(B, k)
nontriv = [a for a in sols if any(x % 1 != 0 for x in a)]
a = nontriv[0]
t = list(a) + [Fraction(0)]
print("Delta_A = |Ann_A| =", len(sols), "; S has phases (turns) t =", t)
print("S = diag(-1,-1,-1,+1,+1,+1) up to order:", sorted(t) == [Fraction(0)] * 3 + [Fraction(1, 2)] * 3)
print("S on B's rays:", T.ray_perm(Phi[(0, 1)], t), " C's rays:", T.ray_perm(Phi[(0, 2)], t))

plus = [i for i in range(6) if t[i] == 0]
minus = [i for i in range(6) if t[i] != 0]
order = plus + minus                      # S = diag(I3,-I3) in this order
def reorder(Mat):
    return [[Mat[i][j] for j in range(6)] for i in order]

U0 = reorder(D.B)      # coefficient matrices of B, C in A coordinates (modulus 1/sqrt6)
V0 = reorder(D.C)
def S_col(Mat, j):
    return [cyc.scale(Mat[i][j], 1 if i < 3 else -1) for i in range(6)]   # S = diag(I3,-I3)
# rephase the columns so that column j+3 is exactly S*(column j): a column rephasing of a basis
# does not change its ray set, so the triple is unchanged.
U = [[None] * 6 for _ in range(6)]
V = [[None] * 6 for _ in range(6)]
for j in range(3):
    for i in range(6):
        U[i][j] = U0[i][j]
        V[i][j] = V0[i][j]
    for i in range(6):
        U[i][j + 3] = S_col(U0, j)[i]
        V[i][j + 3] = S_col(V0, j)[i]
# consistency: the new columns must lie in the same rays as the old ones
def same_ray(colA, colB):
    rs = {canon(mul(x, conj(y))) for x, y in zip(colA, colB) if x and y}
    return len(rs) == 1
print("column rephasing preserves the ray sets of B and C:",
      all(same_ray([U[i][j] for i in range(6)], [U0[i][j] for i in range(6)]) for j in range(6)),
      all(same_ray([V[i][j] for i in range(6)], [V0[i][j] for i in range(6)]) for j in range(6)))

def sub(Mat, rs, cs):
    return [[Mat[i][j] for j in cs] for i in rs]
def adj(Mx):
    return [[conj(Mx[j][i]) for j in range(3)] for i in range(3)]
def mm3(A, Bm):
    out = [[ZERO] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            s = ZERO
            for kk in range(3):
                s = add(s, mul(A[i][kk], Bm[kk][j]))
            out[i][j] = s
    return out
def is_hadamard_norm(H):
    for i in range(3):
        for j in range(3):
            s = ZERO
            for kk in range(3):
                s = add(s, mul(H[i][kk], conj(H[j][kk])))
            if not cyc.eq_int(s, 1 if i == j else 0):
                return False
    return True

# phase normalisation: every entry of the coefficient matrices has modulus sqrt6 (m5's storage
# convention), so dividing by a fixed entry gives a unimodular phase matrix; the 3x3 pieces are
# then  (phase)/sqrt3 , i.e. normalised 3x3 Hadamards.
def phase_mat(Mat):
    """entries have modulus^2 6; returns the exponent matrix of the phases."""
    k00 = Mat[0][0]
    out = [[None] * 6 for _ in range(6)]
    for i in range(6):
        for j in range(6):
            c = cyc.canon(mul(Mat[i][j], conj(k00)))       # = m * zeta^e
            e = None
            for m in (1, 3, 6):
                for cand in range(24):
                    if c == tuple(m * p for p in cyc.POW[cand]):
                        e = cand
                        break
                if e is not None:
                    break
            assert e is not None, (i, j, c)
            out[i][j] = cyc.zpow(e)
    return out
Up, Vp = phase_mat(U), phase_mat(V)
def sub(Mat, rs, cs):
    return [[Mat[i][j] for j in cs] for i in rs]
def adj(Mx):
    return [[conj(Mx[j][i]) for j in range(3)] for i in range(3)]
def mm3(A, Bm):
    out = [[ZERO] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            s = ZERO
            for kk in range(3):
                s = add(s, mul(A[i][kk], Bm[kk][j]))
            out[i][j] = s
    return out
def had3(H):
    for i in range(3):
        for j in range(3):
            s = ZERO
            for kk in range(3):
                s = add(s, mul(H[i][kk], conj(H[j][kk])))
            if not cyc.eq_int(s, 3 if i == j else 0):
                return False
    return True
H0, H0b = sub(Up, range(3), range(3)), sub(Up, range(3), range(3, 6))
H1, H1b = sub(Up, range(3, 6), range(3)), sub(Up, range(3, 6), range(3, 6))
K0, K0b = sub(Vp, range(3), range(3)), sub(Vp, range(3), range(3, 6))
K1, K1b = sub(Vp, range(3, 6), range(3)), sub(Vp, range(3, 6), range(3, 6))
eq = lambda P, Q, sgn: all(canon(add(P[i][j], cyc.scale(Q[i][j], -sgn))) == (0,) * 8
                           for i in range(3) for j in range(3))
print("U = 2^-1/2 [[H0,H0],[H1,-H1]] (source (6)), exact:", eq(H0, H0b, 1) and eq(H1, H1b, -1))
print("V = 2^-1/2 [[K0,K0],[K1,-K1]], exact:", eq(K0, K0b, 1) and eq(K1, K1b, -1))
print("H0,H1,K0,K1 are 3x3 Hadamards (HH^* = 3I, unimodular):", [had3(x) for x in (H0, H1, K0, K1)])

# h = H/sqrt3 ; X = h0^* k0 = (H0^* K0)/3 ; 9|X_ij|^2 = |(H0^*K0)_ij|^2
X = mm3(adj(H0), K0)
Y = mm3(adj(H1), K1)
print("(7)  |X_ij|^2 + |Y_ij|^2 = 2/3  and  Re(X_ij conj(Y_ij)) = 0, exact:")
ok7 = True; unif = True; tab = []
for i in range(3):
    for j in range(3):
        def rit(t):
            return t[0] if t[1:] == (0,) * 7 and t[0] >= 0 else None
        nx = rit(cyc.norm2(X[i][j]))
        ny = rit(cyc.norm2(Y[i][j]))
        cross = mul(X[i][j], conj(Y[i][j]))
        re_zero = canon(add(cross, conj(cross))) == (0,) * 8
        tab.append((nx, ny, nx + ny, re_zero))
        ok7 = ok7 and (nx + ny == 6) and re_zero
        unif = unif and (nx == 3)
print("   9|X_ij|^2 (row-major):", [x for x, y, s, r in tab])
print("   9|Y_ij|^2 (row-major):", [y for x, y, s, r in tab])
print("   all (7) conditions hold:", ok7)
print("   UNIFORM case, |X_ij|^2 = 1/3 everywhere:", unif)
