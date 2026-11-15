"""Step 2 of 5 on one example: the frames, the constant q, and the defect bound.

Input: the 6x6 Hadamard matrix H' of mub-step1-example.tex (the dephased
gauged Fourier matrix in Step 1's canonical order).  Step 2 receives a seed
ball around a centre -- here the centre is the exact seed of H' itself, which
is the point the cover has to contain.

Every number printed here is computed in exact arithmetic in Q(w) where the
matrix allows it (see mubexact.py) and in binary64 where it does not
(norms, frames, the perturbation experiment).  The printed table is the
source of every number in mub-step2-example.tex.

    python3 examples/step2_example.py            # human readable
    python3 examples/step2_example.py --json     # machine readable
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mubexact import (Qw, ZERO, ONE, wp, fmt, blocks, Hprime, mmul, madd,
                      dagger, nullspace, gram, to_cplx, maxabs)

RS_CYCLES = 0.032                # Step 1's seed radius, in cycles
R_S = 2 * np.pi * RS_CYCLES      # the same, in radians
SIX = 6.0

OUT = []
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def row(key, value, note=""):
    OUT.append((key, value, note))


# ---------------------------------------------------------------- 1. frames
def orthonormalise(V):
    """Orthonormal basis of the span of exact vectors V, returned as floats."""
    G = gram(V)
    n = len(V)
    U = []
    for j in range(n):
        w = [np.array([x.complex() for x in V[j]])]
        for u in U:                                  # subtract projections
            c = np.vdot(u, w[0])
            w[0] = w[0] - c * u
        nrm = np.linalg.norm(w[0])
        if nrm < 1e-9:
            raise ValueError("dependent vectors")
        U.append(w[0] / nrm)
    return np.array(U).T                             # columns are the basis


def _ker(M):
    """Orthonormal basis (as columns) of {x : Mx = 0}, by SVD."""
    _, s, vh = np.linalg.svd(M)
    k = int(np.sum(s > 1e-9 * max(s[0], 1.0)))
    return vh[k:].conj().T


def frames():
    E, B, C, D = blocks()
    KB = orthonormalise(nullspace(B))
    KC = orthonormalise(nullspace(dagger(C)))
    return E, B, C, D, KB, KC


def svals_exact(M):
    """The two singular values of a 2 x n or n x 2 matrix over Q(w), exactly.

    Uses the 2x2 Gram matrix of the shorter side; both eigenvalues are real
    because that Gram matrix is Hermitian positive semidefinite of size 2.
    """
    G = mmul(M, dagger(M)) if len(M) <= len(M[0]) else mmul(dagger(M), M)
    tr = G[0][0].complex().real + G[1][1].complex().real
    det = (G[0][0] * G[1][1] - G[0][1] * G[1][0]).complex().real
    disc = max(tr * tr - 4 * det, 0.0)
    lam = [(tr - np.sqrt(disc)) / 2, (tr + np.sqrt(disc)) / 2]
    return [float(x) for x in sorted(np.sqrt([max(l, 0.0) for l in lam]))]


def main():
    E, B, C, D, KB, KC = frames()
    Ec, Bc, Cc, Dc = to_cplx(E), to_cplx(B), to_cplx(C), to_cplx(D)

    # (a) the frames exist at all: the two blocks must have a 2-dim kernel
    row("s2.kernel.dimB", 4 - np.linalg.matrix_rank(Bc), "")
    row("s2.kernel.dimC", 4 - np.linalg.matrix_rank(Cc), "")
    row("s2.frame.KB.err", float(np.max(np.abs(KB.conj().T @ KB - np.eye(2)))),
        "||K_B^*K_B - I||_max")
    row("s2.frame.KC.err", float(np.max(np.abs(KC.conj().T @ KC - np.eye(2)))),
        "||K_C^*K_C - I||_max")

    # (b) the two stretching constants, exact
    sB = svals_exact(B)          # B' is 2x4: both singular values are nonzero
    sC = svals_exact(C)          # C' is 4x2
    row("s2.mB", float(sB[0]), "smallest nonzero singular value of B'")
    row("s2.mC", float(sC[0]), "smallest nonzero singular value of C'^*")
    # exact statement: B'B'* = |S|^2 route.  S = sum b_j
    S = wp(1) + wp(2) + wp(4) + wp(5)
    row("s2.S", fmt(S), "S = sum_j b_j; singular values of B are sqrt(4 +- |S|)")
    row("s2.S.abs", float(abs(S)), "")
    # exact eigenvalues of B'B'* = [[4, conj S],[S, 4]] -> 4 +- |S|
    row("s2.BB.svals.exact", sB, "sqrt(4 -+ |S|), exact")
    # exact C'C'* block form: eigenvalues
    row("s2.CC.svals.exact", sC, "the two nonzero singular values of C', exact")

    # (c) A_0 = operator norm of E_0 = E'
    A0 = float(np.linalg.svd(Ec, compute_uv=False)[0])
    Astar = min(2.0, A0 + R_S)
    row("s2.A0", A0, "operator norm of E' = sqrt(2)")
    row("s2.Astar", Astar, "min(2, A_0 + R_s)")

    # (d) the budget
    q = R_S ** 2 * (1 + (Astar ** 2 + 6) / float(sC[0]) ** 2)
    p = q / (np.sqrt(6) + np.sqrt(6 - q))
    row("s2.Rs", float(R_S), "2*pi*0.032")
    row("s2.q", float(q), "R_s^2 (1 + (A_*^2+6)/m_C^2)")
    row("s2.p", float(p), "q/(sqrt6 + sqrt(6-q))")
    row("s2.p.limit", 0.067, "the value Step 3's grid is built for")
    row("s2.q.limit", 0.32, "the value the paper quotes as the operating range")

    # critical seed radii: solve q(R_s) = target with A_* = min(2, sqrt2 + R_s)
    def q_of(rs):
        a = min(2.0, np.sqrt(2) + rs)
        return rs ** 2 * (1 + (a ** 2 + 6) / float(sC[0]) ** 2)

    def solve(target, hi=0.6):
        lo = 1e-9
        for _ in range(200):
            mid = (lo + hi) / 2
            if q_of(mid) < target:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    q32 = solve(0.32)
    q6 = solve(6.0, hi=1.4) if q_of(1.4) > 6 else float("nan")
    row("s2.Rs.crit.q032", float(q32), "R_s at which q = 0.32")
    row("s2.Rs.crit.q032.cycles", float(q32 / (2 * np.pi)), "")
    row("s2.Rs.crit.q6", float(q6), "R_s at which q = 6")
    row("s2.headroom", float(q32 / R_S), "how much larger the seed radius could be")

    # ------------------------------------------------------- 3. the defect
    Y = KC.conj().T @ Dc @ KB
    row("s2.Y.YY.err", float(np.max(np.abs(Y.conj().T @ Y - 6 * np.eye(2)))),
        "||Y^*Y - 6I||_max at the exact seed")
    # exact: Y^*Y = 6I follows from the two block identities, checked exactly
    six2 = [[Qw(6) if i == j else ZERO for j in range(2)] for i in range(2)]
    idB = madd(mmul(dagger(B), B), mmul(dagger(D), D))
    row("s2.exact.BstarB+DstarD", maxabs([[x - (Qw(6) if i == j else ZERO) for j, x in enumerate(r)]
                                         for i, r in enumerate(idB)]), "exact 0")
    idC = madd(mmul(dagger(E), B), mmul(dagger(C), D))
    row("s2.exact.EstarB+CstarD", maxabs(idC), "exact 0")
    # the identity 6I - Y*Y = M1*M1 + M2*M2
    KCM = KC @ KC.conj().T
    PC = np.eye(4) - KCM
    M1 = Bc @ KB
    M2 = PC @ Dc @ KB
    lhs = 6 * np.eye(2) - Y.conj().T @ Y
    rhs = M1.conj().T @ M1 + M2.conj().T @ M2
    row("s2.defect.identity.err", float(np.max(np.abs(lhs - rhs))), "")
    row("s2.defect.trace", float(np.trace(lhs).real), "tr(6I - Y*Y) at the exact seed")
    row("s2.defect.terms", [float(np.linalg.norm(M1) ** 2), float(np.linalg.norm(M2) ** 2)], "")

    # ------------------------------------------- 4. the perturbation check
    # The nine seed phases: a; b_0..b_3; c_0..c_3, in cycles.
    def seed_matrices(x):
        a = x[0]
        b = x[1:5]
        c = x[5:9]
        E = np.array([[1, 1], [1, np.exp(2j * np.pi * a)]], dtype=complex)
        Bp = np.array([[1, 1, 1, 1],
                       [np.exp(2j * np.pi * t) for t in b]], dtype=complex)
        Cp = np.array([[1, np.exp(2j * np.pi * t)] for t in c], dtype=complex)
        return E, Bp, Cp

    x0 = np.array([0.5, 1 / 6, 1 / 3, 2 / 3, 5 / 6, 0.0, 0.0, 0.5, 0.5])
    rng = np.random.default_rng(20261114)
    ntr = 40000
    trmax, fail = -1.0, 0
    bmax = cmax = 0.0
    worst = (0.0, 0.0)
    for i in range(ntr):
        v = rng.normal(size=9)
        v /= np.linalg.norm(v)
        d = v * RS_CYCLES                 # the centre is this far from the seed
        E0, B0, C0 = seed_matrices(x0 + d)
        KB0 = _ker(B0)                    # Step 2's frames, at the centre
        KC0 = _ker(np.conj(C0.T))
        M1 = Bc @ KB0
        M2 = (np.eye(4) - KC0 @ KC0.conj().T) @ Dc @ KB0
        tr = np.linalg.norm(M1) ** 2 + np.linalg.norm(M2) ** 2
        b1 = np.linalg.norm(Bc - B0)
        c1 = np.linalg.norm(Cc - C0)
        bmax, cmax = max(bmax, b1), max(cmax, c1)
        if tr > q:
            fail += 1
        if tr > trmax:
            trmax = tr
            worst = (np.sum(d[:5] ** 2), np.sum(d[5:] ** 2))
    row("s2.perturb.trials", ntr, "random centres at distance R_s from the seed")
    row("s2.perturb.failures", fail, "centres with tr(6I-Y*Y) > q")
    row("s2.perturb.trmax", float(trmax), "largest observed tr(6I-Y*Y)")
    row("s2.perturb.trmax.over.q", float(trmax / q), "")
    row("s2.perturb.split", [float(worst[0] / RS_CYCLES ** 2), float(worst[1] / RS_CYCLES ** 2)],
        "squared error share in the five x-phases / four y-phases at the maximum")
    row("s2.perturb.b1max", float(bmax), "largest ||Delta B||_F seen")
    row("s2.perturb.c1max", float(cmax), "largest ||Delta C||_F seen")
    # the analytic sharp value of the paper's own estimate:
    # tr <= b1^2 + ((A_* b1 + sqrt6 c1)/m_C)^2 with b1^2 + c1^2 <= R_s^2
    m = float(sC[0])
    Mm = np.array([[1 + Astar ** 2 / m ** 2, Astar * np.sqrt(6) / m ** 2],
                   [Astar * np.sqrt(6) / m ** 2, 6.0 / m ** 2]])
    lam = float(np.linalg.eigvalsh(Mm)[-1])
    row("s2.estimate.sharp", float(lam * R_S ** 2),
        "max of the paper's estimate over the chord ball")

    # ------------------------------------------------ 5. the degenerate case
    E2, B2, C2 = seed_matrices(np.array([0.5, .25, .25, .25, .25, 0.0, 0.0, 0.5, 0.5]))
    sv = np.linalg.svd(B2, compute_uv=False)
    row("s2.degenerate.B.svals", [float(sv[0]), float(sv[1])], "b_0=..=b_3=1/4")
    row("s2.degenerate.B.rank", int(np.linalg.matrix_rank(B2)), "")
    row("s2.degenerate.B.kerneldim", 4 - int(np.linalg.matrix_rank(B2)),
        "no 2-dimensional frame exists -> seed unresolved")
    # also: what R_s makes the check fail is not the point; the point is the
    # kernel is 3-dimensional, so K_B does not exist and the seed is unresolved.

    print_table()
    if "--json" in sys.argv:
        json.dump({k: v for k, v, _ in OUT},
                  open(os.path.join(ROOT, "examples/out/step2.json"), "w"),
                  indent=1)


def print_table():
    w = max(len(k) for k, _, _ in OUT)
    for k, v, note in OUT:
        if isinstance(v, float):
            vs = "%.10g" % v
        else:
            vs = str(v)
        print("%-*s  %-28s %s" % (w, k, vs, note))


if __name__ == "__main__":
    main()
