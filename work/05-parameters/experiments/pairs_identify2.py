#!/usr/bin/env python3
"""Identify the paper's 'pairs processed' = 151,744,086 by testing candidate rules.

hist_gap[c,G] counts ALL weakly increasing Y tails (no sumok) for shared bin c by
their largest midpoint gap G (units of 1/N).  hist_y[c,G] counts only sumok-passing
Y tails (experiments/seedcover_y.py).  X lists are the exact 22,829 of N=112.

Run: python3 experiments/pairs_identify2.py [N]
"""
import sys
from itertools import combinations_with_replacement

import numpy as np

OUT = "work/05-parameters/data"
PAPER = 151_744_086


def gap_hist_all(N, chunk=1_500_000):
    hist = np.zeros((N, N + 1), dtype=np.int64)
    tails = np.array(list(combinations_with_replacement(range(N), 4)), dtype=np.int16)
    nt = len(tails)
    for c in range(N):
        for lo in range(0, nt, chunk):
            t = tails[lo:lo + chunk]
            pts = np.sort(np.stack([np.full(len(t), c), t[:, 0], t[:, 1], t[:, 2], t[:, 3]], axis=1), axis=1)
            g = np.stack([pts[:, 0], pts[:, 1] - pts[:, 0], pts[:, 2] - pts[:, 1],
                          pts[:, 3] - pts[:, 2], pts[:, 4] - pts[:, 3], N - pts[:, 4]], axis=1)
            hist[c] += np.bincount(g.max(axis=1), minlength=N + 1)[:N + 1]
    return hist


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 112
    d = np.load(f"{OUT}/xlists_N{N}.npz")
    T, s = d["tuples"], d["s"]
    l = T[:, 4].astype(int)
    hg = gap_hist_all(N)
    np.save(f"{OUT}/yhist_gapall_N{N}.npy", hg)
    hy = np.load(f"{OUT}/yhist_N{N}.npy")
    print(f"N={N}: total tails per bin C(N+3,4) = {hg.sum(axis=1)[0]:,}")
    for name, h in (("all tails", hg), ("sumok tails", hy)):
        cum = np.concatenate([np.zeros((N, 1), dtype=np.int64), np.cumsum(h, axis=1)], axis=1)
        tot = int(sum(int(cum[c, N + 1]) for c in s))
        v = int(cum[s, np.clip(N - l - 2, 0, N)].sum())
        print(f"  Y side = {name:12s}: pairs with gap test (2.8) = {v:>14,}"
              f"   (ratio to paper {v / PAPER:.4f});  without gap test {tot:>14,}"
              f" (ratio {tot / PAPER:.4f})")


if __name__ == "__main__":
    main()
