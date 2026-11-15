"""Step 4 of 5 on one example: the O and U graphs of the Fourier pair in C^6.

The input is the most symmetric pair of bases in C^6: the standard basis and
the Fourier basis (columns of F/sqrt6).  Its candidate vectors -- those
unbiased to both -- are enumerated exactly on the 12th-root phase lattice
x_k = z^(a_k)/sqrt6, z = exp(i pi /6), and the two graphs of Step 4 are built
on them.  The six-clique pattern is then searched for.

Exactness: a sum of 12th roots of unity is reduced to A + B*sqrt3 with A, B
rational (see abs2), so every edge decision and every count below is exact;
binary64 is used only where the step itself uses it (the ball radii).

    python3 examples/step4_example.py
"""
import itertools
import json
import os
import sys
from fractions import Fraction

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = []


def row(key, value, note=""):
    OUT.append((key, value, note))


# ---------------------------------------------------------------- exact ring
# z = exp(i pi/6); z^6 = -1, z^4 = z^2 - 1.  A sum  sum_c n_c z^c  is stored as
# a list of 12 integer counts.  Its squared modulus is A + B sqrt3 with
# A = n0 - n6 + (n2+n10-n4-n8)/2  and  B = (n1+n11-n5-n7)/2, because
# Re z^c = cos(c pi/6) takes the values 1, sqrt3/2, 1/2, 0, -1/2, -sqrt3/2, -1.
COSTAB = [1, None, Fraction(1, 2), 0, Fraction(-1, 2), None, -1,
          None, Fraction(-1, 2), 0, Fraction(1, 2), None]   # None means +-sqrt3/2


def counts(exps):
    n = [0] * 12
    for a in exps:
        n[a % 12] += 1
    return n


def abs2(n):
    """|sum_c n_c z^c|^2 = A + B sqrt3, returned as (A, B) exactly.

    With N_t = sum_c n_c n_(c-t) (indices mod 12), |z|^2 = sum_t N_t z^t, whose
    real part is N_0 - N_6 + (N_2+N_10-N_4-N_8)/2 + sqrt3 (N_1+N_11-N_5-N_7)/2.
    """
    N = [sum(n[c] * n[(c - t) % 12] for c in range(12)) for t in range(12)]
    A = Fraction(N[0] - N[6]) + Fraction(N[2] + N[10] - N[4] - N[8], 2)
    B = Fraction(N[1] + N[11] - N[5] - N[7], 2)
    return A, B


def abs2_ok(n, target=6):
    A, B = abs2(n)
    return A == target and B == 0


# z = exp(i pi/6) has minimal polynomial x^4 - x^2 + 1, so a sum of 12th roots
# is zero iff its four coefficients in the basis 1, z, z^2, z^3 all vanish.
RED = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1),      # 1, z, z2, z3
       (-1, 0, 1, 0), (0, -1, 0, 1), (-1, 0, 0, 0), (0, -1, 0, 0),  # z4..z7
       (0, 0, -1, 0), (0, 0, 0, -1), (1, 0, -1, 0), (0, 1, 0, -1)]  # z8..z11


def reduce4(n):
    v = [0, 0, 0, 0]
    for c in range(12):
        if n[c]:
            for i in range(4):
                v[i] += n[c] * RED[c][i]
    return v


def inner(a, b):
    """<x,y> for x_k = z^a_k/sqrt6, y_k = z^b_k/sqrt6: a sum of 12th roots / 6."""
    return counts([a[k] - b[k] for k in range(6)])


F6 = np.array([[np.exp(2j * np.pi * j * k / 6) for k in range(6)] for j in range(6)])


def main():
    # ---------------------------------------------------------- the candidates
    # Fast pass in binary64 over all 12^5 = 248832 tuples, then an exact pass
    # over the survivors.  The filter is safe: |S|^2 - 6 is A + B sqrt3 - 6 with
    # A, B rational of denominator 2 and |B| <= 36, so a nonzero value has
    # modulus > 1/200 (Liouville), far above the 1e-6 cut used here.
    tab = np.exp(1j * np.pi * np.arange(12) / 6)
    tails = np.stack(np.meshgrid(*[np.arange(12)] * 5, indexing="ij"), -1).reshape(-1, 5)
    E = np.concatenate([np.zeros((len(tails), 1), dtype=int), tails], axis=1)
    ok = np.ones(len(E), dtype=bool)
    for j in range(6):
        S = np.zeros(len(E), dtype=complex)
        for k in range(6):
            S += tab[(E[:, k] - 2 * j * k) % 12]
        ok &= np.abs(np.abs(S) ** 2 - 6) < 1e-6
    cand = [tuple(int(x) for x in E[i]) for i in np.nonzero(ok)[0]]
    # exact confirmation of every survivor
    for a in cand:
        for j in range(6):
            assert abs2_ok(counts([a[k] - 2 * j * k for k in range(6)])), a
    n = len(cand)
    row("s4.candidates", n, "rays unbiased to the standard and Fourier bases")
    row("s4.candidates.vectors", 12 * n, "counting all 12 global phases")
    row("s4.candidates.tuples", [list(a) for a in cand], "exponents a_0..a_5, a_0 = 0")

    # every candidate really is unbiased to both bases, checked exactly
    worst = 0
    for a in cand:
        for j in range(6):
            A, B = abs2(counts([a[k] - 2 * j * k for k in range(6)]))
            worst = max(worst, abs(A - 6) + abs(B))
    row("s4.candidates.exact_residual", worst, "max |A-6| + |B| over all checks (exact ints)")

    # -------------------------------------------------------------- the graphs
    O = np.zeros((n, n), dtype=bool)
    U = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            nn = inner(cand[i], cand[j])
            if all(x == 0 for x in reduce4(nn)):
                O[i, j] = True
            if abs2_ok(nn):
                U[i, j] = True
    row("s4.O.edges", int(np.sum(np.triu(O, 1))), "pairs exactly orthogonal")
    row("s4.O.degree.hist", {int(d): int(np.sum(np.sum(O, 1) == d)) for d in set(np.sum(O, 1))}, "")
    row("s4.U.edges", int(np.sum(np.triu(U, 1))), "pairs exactly unbiased (|<x,y>| = 1/sqrt6)")
    row("s4.pairs", n * (n - 1) // 2, "pairs of candidates")

    # ------------------------------------------------------------- the cliques
    def cliques(adj, size=6):
        adj = [set(np.nonzero(adj[i])[0]) for i in range(len(adj))]
        res = []

        def ext(R, P):
            if len(R) == size:
                res.append(tuple(sorted(int(x) for x in R)))
                return
            P = list(P)
            while P:
                if len(R) + len(P) < size:
                    return
                v = P.pop()
                ext(R + [v], set(P) & adj[v])

        ext([], set(range(len(adj))))
        return res

    cl = cliques(O, 6)
    row("s4.O.sixcliques", len(cl), "orthonormal bases among the candidates")
    row("s4.O.sixcliques.sets", cl, "as candidate indices")
    # is every 6-clique maximal (no 7-clique)?
    row("s4.O.sevencliques", len(cliques(O, 7)), "")
    # disjoint pairs with all 36 cross edges: the Step-4 pattern
    pat = 0
    cross = []
    for i in range(len(cl)):
        for j in range(i + 1, len(cl)):
            if set(cl[i]) & set(cl[j]):
                continue
            k = sum(1 for u in cl[i] for v in cl[j] if U[u, v])
            cross.append(k)
            if k == 36:
                pat += 1
    row("s4.cross_unbiased.counts", cross, "of 36 cross pairs, per pair of bases")
    row("s4.mub_pairs", pat, "pairs of bases that are mutually unbiased")
    row("s4.pattern", pat > 0, "two disjoint six-cliques with all 36 cross edges?")
    row("s4.bases", len(cl), "")

    # ------------------------------------------------- the ball edge tests
    def vec(a):
        return np.array([np.exp(1j * np.pi * x / 6) for x in a]) / np.sqrt(6)

    def edge(a, b, sa=0.0, sb=0.0):
        t = abs(np.vdot(vec(b), vec(a)))
        r = sa + sb + 1e-10
        dO = np.sqrt(6) * t / (2 * np.pi)
        dU = abs(np.sqrt(6) * t - 1) / (2 * np.pi)
        return dict(t=t, disto=dO, distu=dU, r=r,
                    O=bool(dO <= r + 2e-7), U=bool(dU <= r + 2e-7))

    # a pair inside one basis (orthogonal) and the closest cross pair
    same = edge(cand[cl[0][0]], cand[cl[0][1]])
    best = None
    for u in cl[0]:
        for v in cl[1]:
            e = edge(cand[u], cand[v])
            if best is None or e["distu"] < best[1]["distu"]:
                best = (u, e)
    row("s4.pair.same_basis", {k: (float(x) if isinstance(x, (float, np.floating)) else x)
                               for k, x in same.items()}, "two vectors of one basis")
    row("s4.pair.closest_cross", {k: (float(x) if isinstance(x, (float, np.floating)) else x)
                                  for k, x in best[1].items()},
        "closest pair between two of the bases (best of 36)")

    # ---------------------------------------------------- what a radius does
    # rotate one entry of the second vector of an orthogonal pair and watch the
    # O edge die: the entrywise change is what the ball radius has to cover
    a = vec(cand[cl[0][0]])
    b = vec(cand[cl[0][1]])
    for delta in (1e-7, 1e-6, 1e-5, 1e-4):
        b2 = b.copy()
        b2[0] *= np.exp(2j * np.pi * delta)
        e = edge(cand[cl[0][0]], cand[cl[0][1]])
        t = abs(np.vdot(b2, a))
        dO = np.sqrt(6) * t / (2 * np.pi)
        row("s4.kill.%g.disto" % delta, float(dO), "one entry rotated by %g cycles" % delta)
        row("s4.kill.%g.O" % delta, bool(dO <= 1e-10 + 2e-7), "O edge at radius 0")
        row("s4.kill.%g.radius" % delta, float(max(dO - 2e-7 - 1e-10, 0.0)),
            "per-ball radius needed to keep the O edge anyway (false positive)")
        row("s4.kill.%g.displacement" % delta, float(np.linalg.norm(b2 - b)),
            "Euclidean displacement of the centre")

    if "--slow" in sys.argv:
        offlattice()

    print_table()
    if "--json" in sys.argv:
        json.dump({k: v for k, v, _ in OUT},
                  open(os.path.join(ROOT, "examples/out/step4.json"), "w"),
                  indent=1)


# ---------------------------------------------- the candidates off the lattice
def offlattice(starts=4000):
    """Multistart Newton search for candidates with arbitrary phases.

    Not an enumeration: it finds solutions, it does not prove there are none
    others.  The condition is |u_j| = 1 and |(F u)_k|^2 = 6 for all k, on the
    six phases of u; the global phase is fixed by rotating the first entry to 1.
    """
    from scipy.optimize import least_squares

    def res(th):
        u = np.exp(1j * th)
        return np.concatenate([np.abs(u) ** 2 - 1, np.abs(F6 @ u) ** 2 - 6])

    rng = np.random.default_rng(1)
    sols = []
    for _ in range(starts):
        r = least_squares(res, rng.uniform(0, 2 * np.pi, 6),
                          xtol=1e-14, ftol=1e-14, gtol=1e-14)
        if np.max(np.abs(r.fun)) > 1e-10:
            continue
        th = (r.x - r.x[0]) % (2 * np.pi)
        if any(np.max(np.abs(((th - s + np.pi) % (2 * np.pi)) - np.pi)) < 1e-6
               for s in sols):
            continue
        sols.append(th)
    U = np.array([np.exp(1j * t) for t in sols])
    G = np.abs(U @ U.conj().T)
    O = (G < 1e-8)
    np.fill_diagonal(O, False)
    Ue = (np.abs(G * np.sqrt(6) - 1) < 1e-8)
    np.fill_diagonal(Ue, False)
    adj = [set(np.nonzero(O[i])[0]) for i in range(len(U))]
    six = []

    def ext(R, P):
        if len(R) == 6:
            six.append(tuple(R))
            return
        P = list(P)
        while P:
            if len(R) + len(P) < 6:
                return
            v = P.pop()
            ext(R + [v], set(P) & adj[v])

    ext([], set(range(len(U))))
    pat = 0
    for i in range(len(six)):
        for j in range(i + 1, len(six)):
            if not set(six[i]) & set(six[j]):
                pat += sum(1 for a in six[i] for b in six[j] if Ue[a, b]) == 36
    # which of them sit on a 6th, 12th, 24th or 48th root of unity lattice?
    onl = {M: 0 for M in (6, 12, 24, 48)}
    for t in sols:
        for M in onl:
            if np.max(np.abs((M * t / (2 * np.pi) + 0.5) % 1.0 - 0.5)) < 1e-9:
                onl[M] += 1
    row("s4.offlattice.candidates", len(sols), "multistart search, up to global phase")
    row("s4.offlattice.O_edges", int(O.sum() // 2), "")
    row("s4.offlattice.O_degree_hist",
        {int(d): int(np.sum(np.sum(O, 1) == d)) for d in set(np.sum(O, 1))}, "")
    row("s4.offlattice.sixcliques", len(six), "")
    row("s4.offlattice.U_edges", int(Ue.sum() // 2), "")
    row("s4.offlattice.patterns", int(pat), "disjoint clique pairs with all 36 cross edges")
    row("s4.offlattice.on_lattice", onl, "number of solutions on each M-th root lattice")


def print_table():
    w = max(len(k) for k, _, _ in OUT)
    for k, v, note in OUT:
        vs = "%.10g" % v if isinstance(v, float) else str(v)
        print("%-*s  %-34s %s" % (w, k, vs, note))


if __name__ == "__main__":
    main()
