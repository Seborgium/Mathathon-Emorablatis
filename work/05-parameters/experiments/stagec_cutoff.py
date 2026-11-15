#!/usr/bin/env python3
"""Stage-C clustering cutoff (section 6.3) and the sign of its base (audit finding F2).

The paper: w = 1/M, candidate threshold (.042 - 1.11w)^2, coordinate cutoff
sqrt(2 * threshold) + 1e-10.  X_M = sqrt(29/6)/(2M) is the bin-norm bound of
Lemma 6.1, and sqrt(29/6)/2 = 1.09924 < 1.11.

Also measures, on a synthetic 2-torus of retained bins, how many cluster centres
the assignment rule produces under (a) the printed formula and
(b) the sign-corrected formula max(0, .042 - 1.11w)^2.

Run: python3 experiments/stagec_cutoff.py
"""
import csv

import numpy as np

X_COEF = (29.0 / 6.0) ** 0.5 / 2.0        # X_M = X_COEF / M
GRID = [12, 24, 48, 96, 192]


def threshold(M, printed=True):
    base = 0.042 - 1.11 / M
    return base * base if printed else max(0.0, base) ** 2


def main():
    rows = []
    print("=== the base .042 - 1.11/M and the sign change at M = 26.5 ===")
    print(f"sqrt(29/6)/2 = {X_COEF:.6f}  so X_M = {X_COEF:.5f}/M and 1.11/M = 1.11/M")
    print(f"{'M':>4s} {'X_M':>9s} {'1.11/M':>9s} {'base':>10s} {'threshold':>12s}"
          f" {'coord cutoff':>13s} {'smallest nonzero':>17s} {'ratio':>7s}")
    for M in GRID:
        base = 0.042 - 1.11 / M
        th = threshold(M)
        cut = (2 * th) ** 0.5 + 1e-10
        # smallest nonzero coordinate of the projected midpoint displacement:
        # one coordinate differing by one bin gives deviations (5/6, -1/6,...,-1/6)/M
        minsep = (5.0 / 6.0) / M
        rows.append(dict(M=M, X_M=X_COEF / M, one_11_over_M=1.11 / M, base=base,
                         threshold=th, coord_cutoff=cut, min_nonzero_projected_sep=minsep,
                         ratio=cut / minsep))
        print(f"{M:4d} {X_COEF / M:9.5f} {1.11 / M:9.5f} {base:10.5f} {th:12.3e}"
              f" {cut:13.5f} {minsep:17.5f} {cut / minsep:7.3f}")
    print()
    print("  the base is negative for M < .042/1.11 = %.2f, i.e. M <= 26" % (1.11 / 0.042))
    print("  squaring hides the sign, so the effective radius is |.042 - 1.11/M|:"
          " non-monotone in M.")
    print()
    print("=== sign-corrected formula max(0, .042 - 1.11/M)^2 ===")
    for M in (12, 16, 24, 26, 27, 32, 48, 96):
        print(f"  M={M:3d}: printed cutoff {threshold(M):.5f}   corrected {threshold(M, False):.5f}"
              f"   ratio {threshold(M) / max(threshold(M, False), 1e-300):8.3f}")
    print()
    # --- synthetic clustering experiment -------------------------------------
    rng = np.random.default_rng(7)
    Q, _ = np.linalg.qr(rng.normal(size=(6, 6)))
    # a 2-dimensional torus inside the 5-dimensional mean-zero subspace
    B = Q[:, :2]
    B -= B.mean(axis=0)
    P = 400_000
    ab = rng.uniform(size=(P, 2))
    pts = (ab @ B.T) % 1.0
    print("=== synthetic test: 400k points on a random 2-torus in the 6-torus,")
    print("    binned at resolution M, then clustered with the paper's rule ===")
    print(f"{'M':>4s} {'bins':>8s} {'centres printed':>16s} {'centres corrected':>18s}"
          f" {'compression printed':>19s}")
    srows = []
    for M in (12, 24, 48, 96):
        idx = np.floor(pts * M).astype(np.int64) % M
        bins = np.unique(idx, axis=0)
        out = []
        for printed in (True, False):
            cut = (2 * threshold(M, printed)) ** 0.5 + 1e-10
            centres = np.zeros((0, 6))
            n = 0
            for b in bins:
                u = (b + 0.5) / M
                if n == 0:
                    centres = u[None, :]
                    n = 1
                    continue
                d = u[None, :] - centres
                d -= np.round(d)              # wrapped differences
                h = d - d.mean(axis=1, keepdims=True)
                ok = np.max(np.abs(h), axis=1) <= cut
                if ok.any():
                    continue                  # assigned, no new centre
                centres = np.vstack([centres, u[None, :]])
                n += 1
            out.append(n)
        srows.append(dict(M=M, bins=len(bins), centres_printed=out[0], centres_corrected=out[1],
                          compression_printed=len(bins) / out[0]))
        print(f"{M:4d} {len(bins):8d} {out[0]:16d} {out[1]:18d} {len(bins) / out[0]:19.3f}")
    with open("work/05-parameters/data/stagec_cutoff.csv", "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wtr.writeheader()
        wtr.writerows(rows)
    with open("work/05-parameters/data/stagec_clusters.csv", "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=list(srows[0].keys()))
        wtr.writeheader()
        wtr.writerows(srows)


if __name__ == "__main__":
    main()
