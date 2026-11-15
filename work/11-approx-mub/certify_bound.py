"""Rigorous upper bound on eps*_6 for a stored quadruple of 6x6 unitaries.

Method.  Let U_1..U_4 be the float64 matrices in the given .npy file (shape (4,6,6)).
Their entries are dyadic rationals, hence exact.  Write v^a_i for the i-th column of U_a.

 (1) Exact arithmetic: G_a = U_a^* U_a and the cross-Grams X^{ab}_{ij} = <v^a_i, v^b_j>
     are computed in Q(i) exactly (fractions.Fraction).  Hence q^{ab}_{ij} = |X^{ab}_{ij}|^2
     is an exact non-negative rational.
 (2) Unitarity defect: eta_a = ||G_a - I||_2 <= ||G_a - I||_F =: e_a, computed exactly.
     If e_a < 1 then V_a := U_a (G_a)^{-1/2} is exactly unitary (polar correction) and
        ||V_a - U_a||_2 <= sqrt(1+e_a) * ((1-e_a)^{-1/2} - 1) <= 2 e_a      (for e_a <= 1/2).
     We bound 2*max e_a by a rational DELTA computed below (no floating point in the chain).
 (3) Perturbation: with ||v - v'|| <= DELTA and ||v||=||v'||=1, ||u||,||u'|| <= 1+DELTA,
        | <u,u'> - <v,v'> | <= DELTA + (1+DELTA) DELTA = 2 DELTA + DELTA^2 =: C.
 (4) Therefore for every entry
        |<v,v'>|^2 <= ( sqrt(q) + C )^2   and   |<v,v'>|^2 >= ( max(0, sqrt(q) - C) )^2,
     with sqrt(q) bounded from below and above by exact rational bounds.  Taking the max over
     the 6 pairs and 36 entries and subtracting 1/6 gives a rational upper bound for eps*_6.

Everything is exact rational arithmetic except the final decimal printing.  Runtime ~seconds.
Usage:  python3 certify_bound.py [file.npy]
"""
import sys, math
import numpy as np
from fractions import Fraction as F

def sqrt_bounds(q, bits=80):
    """exact rational lo<=sqrt(q)<=hi for q>=0 rational."""
    assert q >= 0
    num, den = q.numerator, q.denominator
    sh = 2*bits
    n = num << sh
    r = math.isqrt(n // den)          # r <= sqrt(q)*2^bits
    lo = F(r, 1 << bits)
    hi = F(r + 2, 1 << bits)          # guard: r is floor of a floor-quotient; +2 is safe
    return lo, hi

def certify(path, verbose=True):
    U = np.load(path)
    nb = U.shape[0]; d = U.shape[1]
    # exact complex vectors: vec[a][i] = (list re, list im)
    vec = [[([F(*float(U[a,k,i].real).as_integer_ratio()) for k in range(d)],
             [F(*float(U[a,k,i].imag).as_integer_ratio()) for k in range(d)]) for i in range(d)] for a in range(nb)]

    def gram(u, v):     # sum_k conj(u_k) v_k  -> (re, im)
        re = F(0); im = F(0)
        for k in range(d):
            a1,b1 = u[0][k], u[1][k]; a2,b2 = v[0][k], v[1][k]
            re += a1*a2 + b1*b2
            im += a1*b2 - b1*a2
        return re, im

    # (2) unitarity defects, exact Frobenius
    emax = F(0)
    for a in range(nb):
        s = F(0)
        for i in range(d):
            for j in range(d):
                re, im = gram(vec[a][i], vec[a][j])
                t = abs(re - (1 if i == j else 0)) + abs(im)
                s += t*t
        emax = max(emax, s)
    _, sq_hi = sqrt_bounds(emax, 60)
    DELTA = 4*sq_hi            # >= 2*sqrt(emax) >= 2*||G-I||_2 (factor 2 safety margin)
    assert emax < F(1, 100), "matrices are far from unitary"
    C = 2*DELTA + DELTA*DELTA

    # (4) exact max deviation
    worst_bound = F(-1); worst_exact = F(-1); arg = None
    for a in range(nb):
        for b in range(a+1, nb):
            for i in range(d):
                for j in range(d):
                    re, im = gram(vec[a][i], vec[b][j])
                    q = re*re + im*im                    # exact |<u,u'>|^2
                    ex = abs(q - F(1, d))
                    worst_exact = max(worst_exact, ex)
                    lo, hi = sqrt_bounds(q)
                    hi2 = (hi + C)**2
                    lo2 = (max(F(0), lo - C))**2
                    bd = max(abs(hi2 - F(1, d)), abs(F(1, d) - lo2))
                    if bd > worst_bound:
                        worst_bound = bd; arg = (a, b, i, j)
    if verbose:
        print(f"file {path}: {nb} bases, d={d}")
        print(f"unitarity: ||G-I||_F^2 <= {float(emax):.3e},  DELTA = {float(DELTA):.3e}, C = {float(C):.3e}")
        print(f"exact max |P_ij - 1/d| (treating the given matrices as exact) = {worst_exact}")
        print(f"   = {float(worst_exact):.15f}")
        print(f"CERTIFIED eps*_6 <= {worst_bound}  = {float(worst_bound):.15f}")
        print(f"   (attained at pair {arg})")
    return worst_bound, worst_exact

if __name__ == "__main__":
    for p in (sys.argv[1:] or ["tetra_u.npy"]):
        certify(p); print()
