"""Exact diagonal-symmetry indices Delta_A, Delta_B, Delta_C for MUB triples whose
bases have entries in Z[zeta_24] (monomials times 1/sqrt6), plus the lattice index
of the source's support lattice."""
from itertools import permutations
from fractions import Fraction
import sympy as sp
from zeta import *
from cov import MAXISO, eigenbasis, unbiased, generator, norm2
from wh import Wmat

def monomial_matrix(a, b):
    """basis of eigenvectors of W(a,b) as a 6x6 matrix of exponents (mod 24) with
    normalisation 1/sqrt(L) per column (L = column support).  Returns (exp or None)."""
    cols = eigenbasis(a, b)
    E = [[None]*6 for _ in range(6)]
    for j, v in enumerate(cols):
        L = norm2(v)
        assert all(L == norm2(v) for v in cols), "columns with different supports"
        for i in range(6):
            if not is_zero(v[i]):
                k = monomial_index(v[i])
                assert k is not None
                E[i][j] = k
    return E, norm2(cols[0])

SIX = [('m%d' % m) for m in range(6)]
def all_flat_bases():
    out = {}
    for k in SIX:
        t,a,b = generator(k)
        E, L = monomial_matrix(a, b)
        out[k] = (E, L)
    return out

def delta_monomial_pair(E1, E2):
    """Delta for anchor = standard basis: diagonal unitaries preserving the ray sets of
    the two monomial bases E1, E2 (each column normalised by 1/sqrt(L)).  Returns the
    set of exponent vectors lambda mod global shift."""
    n = 6
    def perm_ok(E, sigma, lam):
        for j in range(n):
            vals = {(lam[i] + E[i][j] - E[i][sigma[j]]) % 24 for i in range(n)}
            if len(vals) != 1:
                return False
        return True
    lam_list = []
    for sigma in permutations(range(n)):
        lam = tuple((E1[i][sigma[0]] - E1[i][0]) % 24 for i in range(n))
        if not perm_ok(E1, sigma, lam):
            continue
        ok = False
        for tau in permutations(range(n)):
            if perm_ok(E2, tau, lam):
                ok = True; break
        if ok:
            lam_list.append(lam)
    # mod global shift: normalise lam[0] = 0
    norm = set()
    for lam in lam_list:
        c = lam[0]
        norm.add(tuple((x - c) % 24 for x in lam))
    return norm

def delta_at_flat_anchor(Bexp, Aexp, Cgen):
    """anchor = basis B (monomial exponents Bexp).  Other bases in B coordinates:
    A is monomial (conjugate transpose), C is general (conjugate transpose times matrix)."""
    n = 6
    # A in B coordinates: (B^* A)_{ij} = conj(B_{j i}) (A = standard), monomial
    # Aexp[i][j] = exponent of row i, column j  =>  conj(B_{j,i}) has exponent -Bexp[j][i]
    MA = [[(-Bexp[j][i]) % 24 for j in range(n)] for i in range(n)]
    # columns of MA[j] are A-vectors; the column space is what matters
    # general matrix C in B coords: (B^* C)_{ij} = sum_k conj(B_{k i}) C_{k j}
    MC = [[ZERO]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = ZERO
            for k in range(n):
                # conj(B[k][i]) = zeta^{-Bexp[k][i]} / sqrt6 ; C[k][j] = zeta^{Cexp[k][j]}/sqrt6
                e = (-Bexp[k][i] + Cexp[k][j]) % 24
                s = add(s, POW[e])
            MC[i][j] = s      # overall factor (1/6) is a positive real, irrelevant
    def perm_ok_mono(sigma, lam):
        for j in range(n):
            vals = {(lam[i] + MA[i][j] - MA[i][sigma[j]]) % 24 for i in range(n)}
            if len(vals) != 1: return False
        return True
    def prop_to_col(lam, c, cprime):
        # is (lam_i c_i)_i proportional to cprime ?
        nz = [k for k in range(n) if not is_zero(cprime[k])]
        if not nz: return False
        k0 = nz[0] if not is_zero(c[k0] if False else c[nz[0]]) else None
        # test all pairs j,l : lam_j c_j c'_l = lam_l c_l c'_j
        for j in range(n):
            for l in range(n):
                lhs = mul(POW[lam[j]], mul(c[j], cprime[l]))
                rhs = mul(POW[lam[l]], mul(c[l], cprime[j]))
                if lhs != rhs: return False
        return True
    def perm_ok_general(lam, tau):
        for j in range(n):
            c = [MC[i][j] for i in range(n)]
            cp = [MC[i][tau[j]] for i in range(n)]
            if not prop_to_col(lam, c, cp): return False
        return True
    lam_list = []
    for sigma in permutations(range(n)):
        lam = tuple((MA[i][sigma[0]] - MA[i][0]) % 24 for i in range(n))
        if not perm_ok_mono(sigma, lam): continue
        for tau in permutations(range(n)):
            if perm_ok_general(lam, tau):
                lam_list.append(lam); break
    norm = set()
    for lam in lam_list:
        c = lam[0]
        norm.add(tuple((x - c) % 24 for x in lam))
    return norm

def lattice_index(Bexp, Cexp):
    """[Lambda_0 : L_A] for anchor = standard basis, bases given by exponent matrices
    (entries zeta^{exp}/sqrt6).  Uses the source's formula for P_A and exact support."""
    n = 6
    rels = set()
    edges = [(i,j) for i in range(n) for j in range(n) if i != j]
    P = {}
    for (i,j) in edges:
        for (k,l) in edges:
            # (P_A)_{ij,kl} = sum_r conj(U_jr) U_ir conj(U_kr) U_lr + (same with V)
            s = ZERO
            for r in range(n):
                e = (0 - Bexp[j][r] + Bexp[i][r] - Bexp[k][r] + Bexp[l][r]) % 24
                s = add(s, POW[e])
                e2 = (0 - Cexp[j][r] + Cexp[i][r] - Cexp[k][r] + Cexp[l][r]) % 24
                s = add(s, POW[e2])
            if not is_zero(s):
                P[(i,j,k,l)] = s
                row = [0]*6
                row[i] += 1; row[j] -= 1; row[k] -= 1; row[l] += 1
                if any(row):
                    rels.add(tuple(row[:5]))
    M = sp.Matrix(sorted(rels))
    if M.rows == 0:
        return 1, len(P)
    from sympy.matrices.normalforms import smith_normal_form
    sm = smith_normal_form(M, domain=sp.ZZ)
    diag = [abs(int(sm[i,i])) for i in range(min(sm.rows, sm.cols))]
    idx = 1
    for d in diag: idx *= d
    return idx, len(P)

if __name__ == "__main__":
    fb = all_flat_bases()
    for k in SIX:
        E, L = fb[k]
        print(k, "column support", L, "exponents row0", E[0])
    print()
    # lattice index and Delta at the standard anchor for a few pairs
    for (k1, k2) in [('m0','m1'), ('m0','m2'), ('m1','m2')]:
        E1,_ = fb[k1]; E2,_ = fb[k2]
        D = delta_monomial_pair(E1, E2)
        idx, nz = lattice_index(E1, E2)
        print(f"anchor std, bases {k1},{k2}: |Delta| = {len(D)}  lattice index = {idx}  nonzero P entries = {nz}  unbiased={unbiased(eigenbasis(*generator(k1)[1:]), eigenbasis(*generator(k2)[1:]))}")
