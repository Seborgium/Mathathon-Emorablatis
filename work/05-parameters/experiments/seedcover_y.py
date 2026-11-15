#!/usr/bin/env python3
"""Replay of the Y side of the seed cover and of the covout pair count.

For each possible shared bin c the program visits every weakly increasing four-bin
tail (section 2.3) and applies sumok (2.11) to the five varying phases
(c, t1, t2, t3, t4).  covout then applies the second gap inequality of (2.8),

        gy,mid >= 1 - (l+2)/N ,

where l is the X tuple's last bin, and intersects the shared-displacement
intervals.  We compute exact pair counts for the first two tests:

    pairs(N,l) = sum over X lists of #{ Y lists in its shared bin : G <= N-l-2 }

with G the largest of the six circular gaps of the midpoint set {0} u {midpoints},
in units of 1/N.  This is the paper's "pairs processed" of Table 1 minus whatever
covout's interval intersection removes.

Run: python3 experiments/seedcover_y.py [N ...]
"""
import sys
from itertools import combinations_with_replacement

import numpy as np

OUT = "work/05-parameters/data"


def y_hist(N, chunk=1_500_000):
    """hist[c, G] = number of sumok-passing Y lists for shared bin c with max gap G."""
    w = 1.0 / N
    mid = (np.arange(N) + 0.5) / N
    cs, sn = np.cos(2 * np.pi * mid), np.sin(2 * np.pi * mid)
    E = 5 * np.pi * w * w / 4.0
    pre = 2 * np.pi * (E + 2.5 * w)
    tails = np.array(list(combinations_with_replacement(range(N), 4)), dtype=np.int16)
    nt = len(tails)
    hist = np.zeros((N, N + 1), dtype=np.int64)
    ycount = np.zeros(N, dtype=np.int64)
    for c in range(N):
        for lo in range(0, nt, chunk):
            t = tails[lo:lo + chunk]
            k = len(t)
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
            ok = np.ones(k, dtype=bool)
            nrm = np.hypot(cx, cy)
            with np.errstate(invalid="ignore", divide="ignore"):
                vx, vy = cx / nrm, cy / nrm
            rhs = E + 0.5 * w * np.sum(np.abs(vx[:, None] * Jx + vy[:, None] * Jy), axis=1)
            ok &= np.where(nrm > 0, nrm <= rhs, True)
            for j in range(5):
                vx, vy = -Jy[:, j], Jx[:, j]
                lhs = np.abs(vx * cx + vy * cy)
                rhs = E + 0.5 * w * np.sum(np.abs(vx[:, None] * Jx + vy[:, None] * Jy), axis=1)
                ok &= lhs <= rhs
            if not ok.any():
                continue
            t = t[ok]
            # six circular gaps of {0} u {c, t1..t4}, in units of 1/N
            pts = np.sort(np.stack([np.full(len(t), c), t[:, 0], t[:, 1], t[:, 2], t[:, 3]], axis=1), axis=1)
            g = np.stack([
                pts[:, 0],                       # 0 -> p0  (p0 + 1/2)
                pts[:, 1] - pts[:, 0],
                pts[:, 2] - pts[:, 1],
                pts[:, 3] - pts[:, 2],
                pts[:, 4] - pts[:, 3],
                N - pts[:, 4],                   # p4 -> 1  (N - p4 - 1/2, rounded up)
            ], axis=1)
            G = g.max(axis=1)
            ycount[c] += len(t)
            hist[c] += np.bincount(G, minlength=N + 1)[:N + 1]
    return hist, ycount, nt


def main():
    ns = [int(x) for x in sys.argv[1:]] or [112]
    for N in ns:
        hist, ycount, nt = y_hist(N)
        np.save(f"{OUT}/yhist_N{N}.npy", hist)
        d = np.load(f"{OUT}/xlists_N{N}.npz")
        T, s = d["tuples"], d["s"]
        l = T[:, 4]
        # pairs passing sumok(both sides) + both gap filters
        pairs = 0
        for i in range(len(T)):
            pairs += int(hist[s[i], :N - l[i] - 1].sum())
        print(f"N={N:4d}  Y tails enumerated={N * nt:,}  Y lists passing sumok={int(ycount.sum()):,}"
              f"  (mean per shared bin {ycount.mean():.1f})")
        print(f"          X lists={len(T):,}   pairs after both sumok tests and both gap filters={pairs:,}")
        print(f"          paper Table 1: 'Seed cover  151,744,086 pairs'")
        print(f"          ratio mine/paper = {pairs / 151_744_086:.4f}")


if __name__ == "__main__":
    main()
