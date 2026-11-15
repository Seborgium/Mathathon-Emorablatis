#!/usr/bin/env python3
"""Seed-cover cost curve: exact filter counts as a function of the bin count N.

For each N it reports the ladder of experiments/seedcover_x.py (tuple total,
orientation filter, gap filter, sumok) and the Y-side totals from
experiments/seedcover_y.py, then the pair count under the two readings
RP (the full sumok test set, which reproduces the paper's 22,829 for N=112) and
R (residual direction only).  w = 1/N is the paper's stored width throughout;
R = 0.032 is the ball radius.

Writes work/05-parameters/data/seedcover_sweep.csv.

Run: python3 experiments/n_sweep.py
"""
import csv
import sys

import numpy as np

sys.path.insert(0, "work/05-parameters/experiments")
from seedcover_x import x_lists, shared_bin          # noqa: E402
from seedcover_y import y_hist                        # noqa: E402

OUT = "work/05-parameters/data"
NS = [48, 56, 64, 80, 96, 112, 128]


def yr_counts(N):
    """Y lists per shared bin: full test set (RP) and residual-only (R)."""
    from itertools import combinations_with_replacement
    w = 1.0 / N
    mid = (np.arange(N) + 0.5) / N
    cs, sn = np.cos(2 * np.pi * mid), np.sin(2 * np.pi * mid)
    E = 5 * np.pi * w * w / 4.0
    pre = 2 * np.pi * (E + 2.5 * w)
    tails = np.array(list(combinations_with_replacement(range(N), 4)), dtype=np.int16)
    nt = len(tails)
    rp = np.zeros(N, dtype=np.int64)
    r1 = np.zeros(N, dtype=np.int64)
    chunk = 1_500_000
    for c in range(N):
        for lo in range(0, nt, chunk):
            t = tails[lo:lo + chunk]
            rs = 1.0 + cs[c] + cs[t[:, 0]] + cs[t[:, 1]] + cs[t[:, 2]] + cs[t[:, 3]]
            is_ = sn[c] + sn[t[:, 0]] + sn[t[:, 1]] + sn[t[:, 2]] + sn[t[:, 3]]
            kp = rs * rs + is_ * is_ <= pre * pre
            if not kp.any():
                continue
            t = t[kp]
            rs, is_ = rs[kp], is_[kp]
            k = len(t)
            cx, cy = is_ / (2 * np.pi), -rs / (2 * np.pi)
            Jx = np.stack([np.full(k, cs[c]), cs[t[:, 0]], cs[t[:, 1]], cs[t[:, 2]], cs[t[:, 3]]], axis=1)
            Jy = np.stack([np.full(k, sn[c]), sn[t[:, 0]], sn[t[:, 1]], sn[t[:, 2]], sn[t[:, 3]]], axis=1)
            nrm = np.hypot(cx, cy)
            with np.errstate(invalid="ignore", divide="ignore"):
                vx, vy = cx / nrm, cy / nrm
            rhs = E + 0.5 * w * np.sum(np.abs(vx[:, None] * Jx + vy[:, None] * Jy), axis=1)
            okR = np.where(nrm > 0, nrm <= rhs, True)
            okP = np.ones(k, dtype=bool)
            for j in range(5):
                vx, vy = -Jy[:, j], Jx[:, j]
                lhs = np.abs(vx * cx + vy * cy)
                rhs2 = E + 0.5 * w * np.sum(np.abs(vx[:, None] * Jx + vy[:, None] * Jy), axis=1)
                okP &= lhs <= rhs2
            r1[c] += int(okR.sum())
            rp[c] += int((okR & okP).sum())
    return rp, r1


def main():
    rows = []
    for N in NS:
        r = x_lists(N)
        T = r["tuples"]
        s = shared_bin(T, N)
        rp, r1 = yr_counts(N)
        pairs_rp = int(rp[s].sum())
        pairs_r = int(r1[s].sum())
        rows.append(dict(N=N, tuples=r["A"], after_orientation=r["B"], after_gap=r["C"],
                         x_lists=r["D"], y_lists=int(rp.sum()), y_per_bin_mean=float(rp.mean()),
                         y_resid=int(r1.sum()), pairs_full=pairs_rp, pairs_resid=pairs_r))
        print(f"N={N:4d}  tuples={r['A']:>13,}  x_lists={r['D']:>8,}  Y lists={int(rp.sum()):>10,}"
              f"  pairs(full test set)={pairs_rp:>13,}  pairs(residual only)={pairs_r:>13,}")
    with open(f"{OUT}/seedcover_sweep.csv", "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wtr.writeheader()
        wtr.writerows(rows)


if __name__ == "__main__":
    main()
