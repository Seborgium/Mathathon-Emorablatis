"""Independent audit of the Delta = (2,3,3) triple (m5's certificate) with the m1 machinery.

m5's construction (his m5-exact-certificate.py, read on the board):
  w = zeta_24^8 (cube root), F3 = (w^{ij}), H0 = F3 diag(1,1,w), H1 = F3 diag(1,1,w^2),
  K0 = H0 F3, K1 = i H1 F3,  B = 2^-1/2 [[H0,H0],[H1,-H1]]/sqrt3,
  C = 2^-1/2 [[K0,K0],[K1,-K1]]/3,  A = I6.
We rescale each basis by 6 (phases unchanged) so that every entry has modulus^2 an integer.
"""
from fractions import Fraction
import cyc
from cyc import add, mul, conj, zpow, canon, ZERO
import mubtools as T

def mm(A, B):
    return T.mm(A, B)

def scl(A, c):
    return [[cyc.scale(x, c) if x else {} for x in row] for row in A]

# 3x3 pieces (F3 rows indexed by i, columns by j, exponent 8ij)
F3 = [[zpow(8 * i * j) for j in range(3)] for i in range(3)]
d_w = [zpow(0), zpow(0), zpow(8)]     # diag(1,1,w)
d_w2 = [zpow(0), zpow(0), zpow(16)]   # diag(1,1,w^2)
def rmul_diag(M, d):
    return [[mul(M[i][j], d[j]) for j in range(3)] for i in range(3)]
H0 = rmul_diag(F3, d_w)
H1 = rmul_diag(F3, d_w2)
K0 = mm(H0, F3)
K1 = scl(mm(H1, F3), 1)          # multiply by i at the end (phase only): i = zeta^6
K1 = [[mul(x, zpow(6)) for x in row] for row in K1]

def block(P, Q):
    """[[P,P],[Q,-Q]] with index 3a+r"""
    M = [[None] * 6 for _ in range(6)]
    for a in range(2):
        for r in range(3):
            for b in range(2):
                for s in range(3):
                    base = (P if a == 0 else Q)[r][s]
                    sgn = -1 if (a == 1 and b == 1) else 1
                    M[3 * a + r][3 * b + s] = cyc.scale(base, sgn) if base else {}
    return M

B = block(H0, H1)
C = block(K0, K1)
A = T.ident(6)
# rescale B, C by 6 so that |entry|^2 is an integer (phases unchanged)
B6, C6 = scl(B, 6), scl(C, 6)

print("A basis:", T.is_basis_rep(A, 6))
print("B basis:", T.is_basis_rep(B6, 6), " C basis:", T.is_basis_rep(C6, 6))
print("A-B unbiased:", T.is_unbiased_rep(A, B6, 6),
      " A-C unbiased:", T.is_unbiased_rep(A, C6, 6),
      " B-C unbiased:", T.is_unbiased_rep(B6, C6, 6))

res = T.analyze_triple(A, B6, C6)
print()
print(f"{'anchor':6s} {'support':>8s} {'|Ann|=index':>12s} {'HNF diag':>18s} {'rankF3':>7s} {'ord3':>5s} {'pres':>5s} {'swap':>5s} {'idem':>6s}")
for k in 'ABC':
    r = res[k]
    print(f"{k:6s} {r['nsup']:8d} {r['nann']:12d} {str(r['hnfdiag']):>18s} {r['rank_f3']:7d} "
          f"{r['ord3']:5d} {r['pres']:5d} {r['swap']:5d} {str(r['idem']):>6s}")

# ---- Smith normal forms (to compare with the source's claimed (1,1,1,1,3),(1,1,1,1,3),(1,1,1,1,2))
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
reps = [A, B6, C6]
Ph = {}
for i in range(3):
    for j in range(3):
        if i != j:
            Ph[(i, j)] = T.pair_phase(reps[i], reps[j])[0]
for x in range(3):
    o = [y for y in range(3) if y != x]
    M = T.projections(Ph[(x, o[0])], Ph[(x, o[1])])
    supp = T.support(M)
    rows = T.relations(M, supp)
    S = smith_normal_form(sp.Matrix(rows), domain=sp.ZZ)
    print("anchor", 'ABC'[x], "Smith diag", [abs(int(S[i, i])) for i in range(5)])
