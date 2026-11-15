"""Step 3 of 5 on one example: the cell cover of U(2).

Input: the compressed block V = Y/sqrt(6) of Step 2 (an exact point of U(2)),
written in Step 3's four-angle chart, and a grid of N_u cells per coordinate.
The two Taylor bounds of Step 3 are then checked on the cell that contains V
and on random points of that cell.

Angles here are in radians:  V = e^{iA} [[e^{iB} cos T, e^{iC} sin T],
                                        [-e^{-iC} sin T, e^{-iB} cos T]]
with 0 <= A <= pi, 0 <= B, C <= 2 pi, 0 <= T <= pi/2.  Cutting each coordinate
into N_u equal cells gives N_u^4 cells, each of angular half-width
    dA <= pi/(2 N_u),  dB = dC <= pi/N_u,  dT <= pi/(4 N_u),
so the uniform statement |theta_j| <= h with h = pi/N_u holds.

    python3 examples/step3_example.py
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mubexact import blocks, to_cplx
import step2_example as s2


def chart(A, B, C, T):
    e = np.exp
    return e(1j * A) * np.array(
        [[e(1j * B) * np.cos(T), e(1j * C) * np.sin(T)],
         [-e(-1j * C) * np.sin(T), e(-1j * B) * np.cos(T)]], dtype=complex)


def dchart(A, B, C, T, th):
    """The derivative of the chart at (A,B,C,T) in the direction th=(dA,dB,dC,dT)."""
    dA, dB, dC, dT = th
    e = np.exp
    pre = e(1j * A)
    z, w = e(1j * B) * np.cos(T), e(1j * C) * np.sin(T)
    V = pre * np.array([[z, w], [-w.conjugate(), z.conjugate()]])
    d = 1j * dA * V                                     # d/dA = i V
    d += pre * 1j * dB * np.array([[z, 0], [0, -z.conjugate()]])
    d += pre * 1j * dC * np.array([[0, w], [w.conjugate(), 0]])
    d += pre * np.array([[-e(1j * B) * np.sin(T), e(1j * C) * np.cos(T)],
                         [-e(-1j * C) * np.cos(T), -e(-1j * B) * np.sin(T)]]) * dT
    return d


def coords(V):
    """The chart coordinates (A,B,C,T) of V in U(2), in radians."""
    det = np.linalg.det(V)
    A = np.angle(det) / 2.0 % np.pi                     # det = e^{2iA}
    V0 = np.exp(-1j * A) * V                            # now in SU(2)
    z, w = V0[0, 0], V0[0, 1]
    T = np.arctan2(abs(w), abs(z))
    B = np.angle(z) % (2 * np.pi)
    C = np.angle(w) % (2 * np.pi)
    return np.array([A, B, C, T])


def cell_centre(x, N):
    """Midpoint of the cell of the grid (N cells per coordinate) holding x."""
    ranges = np.array([np.pi, 2 * np.pi, 2 * np.pi, np.pi / 2])
    k = np.floor(x / ranges * N).astype(int)
    k = np.clip(k, 0, N - 1)
    return (k + 0.5) * ranges / N


OUT = []
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def row(key, value, note=""):
    OUT.append((key, value, note))


def main():
    E, B, C, D, KB, KC = s2.frames()
    Y = KC.conj().T @ to_cplx(D) @ KB
    V = Y / np.sqrt(6)
    row("s3.V.unitary", float(np.max(np.abs(V.conj().T @ V - np.eye(2)))), "||V^*V - I||_max")
    row("s3.V.det", float(abs(np.linalg.det(V))), "|det V|")

    x = coords(V)
    A, Bb, Cc, T = x
    row("s3.chart.A", float(A), "radians")
    row("s3.chart.B", float(Bb), "")
    row("s3.chart.C", float(Cc), "")
    row("s3.chart.T", float(T), "")
    row("s3.chart.cycles", [float(v / (2 * np.pi)) for v in x], "same, in cycles")
    row("s3.chart.reconstruct", float(np.max(np.abs(chart(*x) - V))), "")

    # (b) the two Taylor bounds on the cell containing V
    print("  N_u      h        theta(max)  ||V-U||   sqrt6*h   ratio    "
          "||rem||   (sqrt42/2)h^2  ratio   worst ||V-U||  worst ||rem||")
    for N in (8, 16, 32, 64, 128, 256):
        xc = cell_centre(x, N)
        th = x - xc
        h = np.pi / N
        dU = dchart(*xc, th=th)
        lin = np.linalg.norm(V - chart(*xc))
        rem = np.linalg.norm(V - chart(*xc) - dU)
        # worst case over the cell: sample random points inside it
        rng = np.random.default_rng(N)
        wl = wr = 0.0
        for _ in range(4000):
            p = xc + (rng.random(4) * 2 - 1) * np.array(
                [np.pi / (2 * N), np.pi / N, np.pi / N, np.pi / (4 * N)])
            Vp = chart(*p)
            dp = dchart(*xc, th=p - xc)
            wl = max(wl, np.linalg.norm(Vp - chart(*xc)))
            wr = max(wr, np.linalg.norm(Vp - chart(*xc) - dp))
        row("s3.N%d.h" % N, float(h), "")
        row("s3.N%d.theta_max" % N, float(np.max(np.abs(th))), "")
        row("s3.N%d.lin" % N, float(lin), "")
        row("s3.N%d.lin_bound" % N, float(np.sqrt(6) * h), "sqrt(6) h")
        row("s3.N%d.rem" % N, float(rem), "")
        row("s3.N%d.rem_bound" % N, float(np.sqrt(42) / 2 * h * h), "(sqrt42/2) h^2")
        row("s3.N%d.worst_lin" % N, float(wl), "max over 4000 points of the cell")
        row("s3.N%d.worst_rem" % N, float(wr), "")
        print("%5d %8.5f %9.2e %9.2e %9.2e %7.3f %9.2e %9.2e %7.3f %9.2e %9.2e"
              % (N, h, np.max(np.abs(th)), lin, np.sqrt(6) * h, lin / (np.sqrt(6) * h),
                 rem, np.sqrt(42) / 2 * h * h, rem / (np.sqrt(42) / 2 * h * h), wl, wr))

    # measured constants: sup of ||V-U||/h and of ||rem||/h^2 over each cell
    c1 = c2 = 0.0
    rng = np.random.default_rng(7)
    ranges = np.array([np.pi, 2 * np.pi, 2 * np.pi, np.pi / 2])
    for N in (8, 16, 32, 64, 128):
        h = np.pi / N
        for _ in range(400):                      # 400 random cells per grid
            xr = rng.random(4) * ranges
            xc = cell_centre(xr, N)
            for _ in range(5):                    # 5 random points per cell
                p = xc + (rng.random(4) * 2 - 1) * np.array(
                    [np.pi / (2 * N), np.pi / N, np.pi / N, np.pi / (4 * N)])
                Vp = chart(*p)
                dp = dchart(*xc, th=p - xc)
                c1 = max(c1, np.linalg.norm(Vp - chart(*xc)) / h)
                c2 = max(c2, np.linalg.norm(Vp - chart(*xc) - dp) / h ** 2)
    row("s3.const.c1", float(c1), "measured sup ||V-U||_F / h")
    row("s3.const.c1.quoted", float(np.sqrt(6)), "the paper's constant sqrt(6)")
    row("s3.const.c2", float(c2), "measured sup ||V-U-dU||_F / h^2")
    row("s3.const.c2.quoted", float(np.sqrt(42) / 2), "the paper's constant sqrt(42)/2")

    # (c) how fine the grid must be
    for target in (0.03, 1e-3, 1e-6):
        Nstar = int(np.ceil(np.pi / (target / np.sqrt(6))))
        p2 = int(np.ceil(np.pi / np.sqrt(target / (np.sqrt(42) / 2))))
        row("s3.Nstar.lin.%g" % target, Nstar, "smallest N with sqrt6 h <= %g" % target)
        row("s3.Nstar.quad.%g" % target, p2, "smallest N with (sqrt42/2)h^2 <= %g" % target)

    # (d) the inflation rule: a test at the centre with margin mu is uniform on
    # the cell when mu > c2 h^2 + (the movement of the test's own value)
    for mu in (1e-2, 1e-3, 1e-4):
        hstar = np.sqrt(mu / c2)
        row("s3.inflate.mu%g" % mu, int(np.ceil(np.pi / hstar)),
            "smallest N with c2 h^2 < %g (c2 = measured)" % mu)

    print_table()
    if "--json" in sys.argv:
        json.dump({k: v for k, v, _ in OUT},
                  open(os.path.join(ROOT, "examples/out/step3.json"), "w"),
                  indent=1)


def print_table():
    w = max(len(k) for k, _, _ in OUT)
    for k, v, note in OUT:
        vs = "%.10g" % v if isinstance(v, float) else str(v)
        print("%-*s  %-30s %s" % (w, k, vs, note))


if __name__ == "__main__":
    main()
