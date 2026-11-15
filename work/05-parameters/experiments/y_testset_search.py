#!/usr/bin/env python3
"""Which subset of the sumok test directions, applied to the Y list, reproduces the
paper's 151,744,086 'pairs processed'?

For each Y list we record which of six tests of (2.11) it passes:
  bit 0  : the residual direction
  bits 1-5: the direction perpendicular to J_0, J_1, ..., J_4
Then for every one of the 64 subsets we compute
  pairs(subset) = sum over the 22,829 X lists of #{Y lists in its shared bin}
and compare with 151,744,086.

Run: python3 experiments/y_testset_search.py [N]
"""
import sys
from itertools import combinations_with_replacement

import numpy as np

OUT = "work/05-parameters/data"
PAPER = 151_744_086


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 112
    w = 1.0 / N
    mid = (np.arange(N) + 0.5) / N
    cs, sn = np.cos(2 * np.pi * mid), np.sin(2 * np.pi * mid)
    E = 5 * np.pi * w * w / 4.0
    pre = 2 * np.pi * (E + 2.5 * w)
    tails = np.array(list(combinations_with_replacement(range(N), 4)), dtype=np.int16)
    nt = len(tails)
    counts = np.zeros((N, 64), dtype=np.int64)   # per shared bin, per subset
    chunk = 1_500_000
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
            bits = np.zeros(k, dtype=np.int64)
            nrm = np.hypot(cx, cy)
            with np.errstate(invalid="ignore", divide="ignore"):
                vx, vy = cx / nrm, cy / nrm
            rhs = E + 0.5 * w * np.sum(np.abs(vx[:, None] * Jx + vy[:, None] * Jy), axis=1)
            bits |= np.where(nrm > 0, nrm <= rhs, True).astype(np.int64)
            for j in range(5):
                vx, vy = -Jy[:, j], Jx[:, j]
                lhs = np.abs(vx * cx + vy * cy)
                rhs = E + 0.5 * w * np.sum(np.abs(vx[:, None] * Jx + vy[:, None] * Jy), axis=1)
                bits |= (lhs <= rhs).astype(np.int64) << (j + 1)
            counts[c] += np.bincount(bits, minlength=64)[:64]
    np.save(f"{OUT}/ybits_N{N}.npy", counts)
    d = np.load(f"{OUT}/xlists_N{N}.npz")
    s = d["s"]
    print("subset of tests -> pairs (X lists = %d)" % len(s))
    hits = []
    for mask in range(64):
        # a Y list is retained if it passes every test in the mask
        keep = np.zeros(64, dtype=bool)
        for b in range(64):
            keep[b] = (b & mask) == mask
        tot = int((counts[:, keep].sum(axis=1))[s].sum())
        if abs(tot - PAPER) / PAPER < 0.06:
            hits.append((mask, tot))
    for mask, tot in sorted(hits, key=lambda x: abs(x[1] - PAPER)):
        names = ["R"] + [f"P{j}" for j in range(5)]
        sel = [names[i] for i in range(6) if mask >> i & 1]
        print(f"  {'+'.join(sel):24s} pairs = {tot:>14,}   ratio {tot / PAPER:.4f}")
    print(f"\n  paper: {PAPER:,}")
    print("  (RP = R+P0+P1+P2+P3+P4 is the set that reproduces the X-side count 22,829)")


if __name__ == "__main__":
    main()
