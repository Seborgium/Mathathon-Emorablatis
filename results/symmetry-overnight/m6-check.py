#!/usr/bin/env python3
"""m6 (swarm smwhnslql): exact diagonal-symmetry data for MUB triples in C^6.

Representation.  zeta = exp(2*pi*i/24), Phi_24(x) = x^8-x^4+1, sqrt6 = zeta+zeta^23+zeta^5+zeta^19.
A *flat* 6x6 matrix (all entries of modulus 1/sqrt6) is stored as an integer exponent array E,
entry e meaning zeta^e/sqrt6.  Flat products are handled exactly through Z[zeta_24].

Outputs, for a given exact triple {A=I_6, B, C}:
  * exact MUB verification;
  * |G_A|, |G_B|, |G_C| (exhaustive: 720 permutations per basis, per anchor);
  * the order and eigenvalue multiplicity pattern of every element of each G;
  * Smith normal form / index of the support lattice L_A, to test the source's eq. (5)
    (Delta_A = [Lambda_0 : L_A]).
"""
import itertools
import numpy as np
import sympy as sp
from sympy import Poly, Symbol, rem, ZZ
from sympy.matrices.normalforms import smith_normal_form

x = Symbol("x")
PHI = Poly(x**8 - x**4 + 1, x)          # Phi_24
SQRT6 = (1, 23, 5, 19)                  # sqrt6 = sum zeta^e


def red(expr):
    return rem(Poly(sp.expand(expr), x), PHI)


def isz(expr):
    return red(expr).is_zero


def zsum(exps):
    return red(sum(x**e for e in exps)).as_expr()


def ip2(X, j, Y, k):
    """36 * |<X[:,j], Y[:,k]>|^2, exactly (should be 6 for unbiased flat columns)."""
    t = {}
    for i in range(6):
        e = (X[i][j] - Y[i][k]) % 24
        t[e] = t.get(e, 0) + 1
    s = sum(c * x**e for e, c in t.items())
    sbar = sum(c * x ** ((-e) % 24) for e, c in t.items())
    return red(s * sbar).as_expr()


def check_flat_unitary(X, name, verbose=True):
    for j in range(6):
        for k in range(6):
            assert isz(ip2(X, j, X, k) - (36 if j == k else 0)), (name, j, k)
    if verbose:
        print(f"  {name}: exactly orthonormal")


def entries_of_product(EY, EX):
    """entries of the flat unitary  X^* Y  ( = sqrt6 * <X_j,Y_k> /6 )  as 24th-root exponents.

    We compute s = sum_r zeta^{EY[r][k]-EX[r][j]} = 6 <X_j,Y_k> = sqrt6 * eta, and certify
    exactly that s = sqrt6 * zeta^e for a 24th root of unity, returning e.
    """
    d = EX.shape[0]
    E = np.zeros((d, d), dtype=int)
    for j in range(d):
        for k in range(d):
            s = zsum([(EY[r][k] - EX[r][j]) % 24 for r in range(d)])
            found = None
            for e in range(24):
                cand = red(sum(x**(ee % 24) for ee in SQRT6) * x**e).as_expr()
                if red(s - cand).is_zero:
                    found = e
                    break
            assert found is not None, ("not a 24th root times sqrt6", j, k, s)
            E[j][k] = found
    return E


def adj(X):
    return np.array([[(-X[j][i]) % 24 for j in range(6)] for i in range(6)], dtype=int)


def kron2x3(A2, B3):
    """6x6 exponent array of the product basis A2 (x) B3, index (a,r) -> 3a+r."""
    out = np.zeros((6, 6), dtype=int)
    for a in range(2):
        for r in range(3):
            for b in range(2):
                for s in range(3):
                    out[3 * a + r][3 * b + s] = (A2[a][b] + B3[r][s]) % 24
    return out


def tensor_triple():
    """A = I_2 (x) I_3;  B = H (x) F_3;  C = H' (x) F'_3,  H,H' the qubit Fourier pair,
    F_3 the qutrit DFT and F'_3 the eigenbasis of XZ (all entries 24th roots / sqrt6)."""
    # qubit: H = (1/sqrt2)[[1,1],[1,-1]] ; H' = (1/sqrt2)[[1,1],[i,-i]]
    H = [[0, 0], [0, 12]]              # zeta^0, zeta^0, zeta^0, zeta^12 = -1  (24th roots)
    Hp = [[0, 0], [6, 18]]             # 1, 1, zeta^6 = i, zeta^18 = -i
    # qutrit DFT: F_3[r][s] = omega^{rs}, omega = zeta^8
    F3 = [[(8 * r * s) % 24 for s in range(3)] for r in range(3)]
    # F'_3 : eigenbasis of XZ in d=3, entries omega^{r(r-1)/2 - m r}, omega = zeta^8
    Fp3 = [[(8 * ((r * (r - 1) // 2 - m * r) % 3)) % 24 for m in range(3)] for r in range(3)]
    return kron2x3(H, F3), kron2x3(Hp, Fp3)


# --------------------------------------------------------------- symmetry group
def mono_phases(ex, sigma):
    """a (a_0 = 0) with lambda_i ex[i][sigma(j)] = delta_j ex[i][j] for a diagonal lambda."""
    d = ex.shape[0]
    M = [[(ex[i][j] - ex[i][sigma[j]]) % 24 for j in range(d)] for i in range(d)]
    for i in range(d):
        for ip in range(d):
            for j in range(d):
                for jp in range(d):
                    if (M[i][j] + M[ip][jp] - M[i][jp] - M[ip][j]) % 24:
                        return None
    return tuple((M[i][0] - M[0][0]) % 24 for i in range(d))


def mono_group(ex):
    out = {}
    for sigma in itertools.permutations(range(ex.shape[0])):
        a = mono_phases(ex, sigma)
        if a is not None:
            out.setdefault(a, []).append(sigma)
    return out


def symmetry_group(exX, exY):
    gX, gY = mono_group(exX), mono_group(exY)
    return {a: (gX[a], gY[a]) for a in set(gX) & set(gY)}


def order_of(a):
    for k in range(1, 25):
        if all((k * ai) % 24 == 0 for ai in a):
            return k
    return None


def pattern(a):
    c = {}
    for ai in a:
        c[ai] = c.get(ai, 0) + 1
    return sorted(c.values(), reverse=True)


# --------------------------------------------------------- support lattice
def support_full(exH, exK):
    """Scan all 30x30 = 900 positions (i!=j, k!=l) of the anchored projection P_X.

    Returns (n_nonzero, n_trivial_relation, n_nontrivial, rows) where
      * n_nonzero counts positions with (P_X)_{ij,kl} != 0,
      * n_trivial_relation counts those whose relation vector e_i-e_j-e_k+e_l is zero
        (these must be exactly the 30 positions (i,j,i,j), with value 1/3),
      * rows are the nonzero relation vectors in Z^5 (sixth coordinate dropped).
    """
    d = 6
    n_nonzero = n_trivial = 0
    rows = []
    for i in range(d):
        for j in range(d):
            if i == j:
                continue
            for k in range(d):
                for l in range(d):
                    if k == l:
                        continue
                    s1 = zsum([(exH[i][r] - exH[j][r] - exH[k][r] + exH[l][r]) % 24
                               for r in range(d)])
                    s2 = zsum([(exK[i][r] - exK[j][r] - exK[k][r] + exK[l][r]) % 24
                               for r in range(d)])
                    val = sp.expand(s1 + s2)          # = 36 * (P_X)_{ij,kl}
                    if isz(val):
                        continue
                    n_nonzero += 1
                    if (k, l) == (i, j):
                        # relation vector is zero; the source's normalisation says 1/3
                        assert isz(val - 12), ("diagonal entry not 1/3", i, j)
                        n_trivial += 1
                        continue
                    v = [0] * 5
                    for idx, c in ((i, 1), (j, -1), (k, -1), (l, 1)):
                        if idx < 5:
                            v[idx] += c
                    rows.append(v)
    return n_nonzero, n_trivial, len(rows), rows


def lattice_index(rows):
    """Smith invariants of the lattice spanned by the given relation vectors in Z^5."""
    M = sp.Matrix.vstack(*[sp.Matrix([r]) for r in rows])
    snf = smith_normal_form(M, domain=ZZ)
    diag = [abs(int(snf[i, i])) for i in range(5)]
    idx = 1
    for d in diag:
        idx *= d
    return diag, idx


def cycle_type(sigma):
    d = len(sigma)
    seen = set()
    t = []
    for i in range(d):
        if i in seen:
            continue
        l = 0
        j = i
        while j not in seen:
            seen.add(j)
            j = sigma[j]
            l += 1
        t.append(l)
    return tuple(sorted(t, reverse=True))


if __name__ == "__main__":
    B, C = tensor_triple()
    print("== exact tensor/Heisenberg triple in C^6, arithmetic in Z[zeta_24]")
    check_flat_unitary(B, "B = H (x) F_3")
    check_flat_unitary(C, "C = H' (x) F'_3")
    BC = entries_of_product(adj(B), C)
    check_flat_unitary(BC, "B^* C (entries certified as zeta_24^e/sqrt6)")
    print()
    anchors = {
        "A": (B, C),
        "B": (adj(B), BC),
        "C": (adj(C), adj(BC)),
    }
    for name, (X, Y) in anchors.items():
        G = symmetry_group(X, Y)
        print(f"anchor {name}: |G_{name}| = {len(G)}")
        for a in sorted(G):
            aa = tuple(int(t) for t in a)
            sx, sy = G[a]
            print(f"    lambda = zeta^{aa}: order {order_of(a)}, "
                  f"eigenvalue multiplicities {pattern(a)}, "
                  f"cycle types on the other two bases "
                  f"{sorted({cycle_type(sig) for sig in sx})} and "
                  f"{sorted({cycle_type(sig) for sig in sy})}")
        nnz, ntriv, nnt, rows = support_full(X, Y)
        diag, idx = lattice_index(rows)
        print(f"    P_{name}: {nnz} nonzero entries; {ntriv} of them have zero relation "
              f"vector (the 30 positions (i,j,i,j), value 1/3); {nnt} nonzero relation "
              f"vectors; Smith {diag}, index {idx}")
