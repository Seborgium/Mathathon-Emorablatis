#!/usr/bin/env python3
"""Which pairing rule reproduces the paper's 151,744,086 'pairs processed'?

Uses the exact X lists (experiments/seedcover_x.py) and the exact per-shared-bin
histogram of sumok-passing Y lists binned by their largest midpoint gap G
(experiments/seedcover_y.py).  Variants differ only in the gap threshold applied
to the Y list, where the X tuple enters through its last bin l.

Run: python3 experiments/pairs_variants.py [N]
"""
import sys

import numpy as np

OUT = "work/05-parameters/data"
PAPER = 151_744_086


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 112
    hist = np.load(f"{OUT}/yhist_N{N}.npy")
    d = np.load(f"{OUT}/xlists_N{N}.npz")
    T, s = d["tuples"], d["s"]
    l = T[:, 4].astype(int)
    cum = np.concatenate([np.zeros((N, 1), dtype=np.int64), np.cumsum(hist, axis=1)], axis=1)
    tot = int(sum(int(cum[c, N + 1]) for c in s))
    print(f"N = {N}: X lists = {len(T):,}   Y lists (sumok) per bin: mean "
          f"{hist.sum(axis=1).mean():.1f}  min {hist.sum(axis=1).min()}  max {hist.sum(axis=1).max()}")
    print(f"  variant 0: no gap threshold (all sumok pairs)          {tot:>13,}  "
          f"ratio to paper {tot / PAPER:.3f}")
    for k, name in ((0, "G <= N-l-2  (paper (2.8): 1-(l+2)/N)"),
                    (1, "G <= N-l-1  (1-(l+1)/N)"),
                    (2, "G <= N-l    (1-l/N)"),
                    (3, "G <= N-l+1"),
                    (4, "G <= N-l+2")):
        idx = np.clip(N - l - 2 + k, 0, N)
        v = int(cum[s, idx].sum())
        print(f"  variant {k+1}: {name:<46} {v:>13,}  ratio {v / PAPER:.3f}")
    # gap counted with the exact endpoint (last gap = N - p4 - 1/2): the integer
    # comparison G' <= t  with G' the rounded-up largest gap is identical to variant 0/1
    print()
    print("  paper Table 1: 'Seed cover   151,744,086 pairs'")


if __name__ == "__main__":
    main()
