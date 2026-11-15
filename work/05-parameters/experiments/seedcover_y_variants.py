#!/usr/bin/env python3
"""How strong is the Y-side sumok test?  Count Y lists per shared bin under four
test sets, and multiply by the exact 22,829 X lists to compare with the paper's
'151,744,086 pairs'.

  R  = residual direction only
  P  = the five directions perpendicular to J_0..J_4
  RP = both (the test set that reproduces the X-side count 22,829 exactly)
  -  = no test

Run: python3 experiments/seedcover_y_variants.py [N]
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
    counts = {k: np.zeros(N, dtype=np.int64) for k in ("R", "P", "RP", "-")}
    chunk = 1_500_000
    for c in range(N):
        for lo in range(0, nt, chunk):
            t = tails[lo:lo + chunk]
            k = len(t)
            rs = 1.0 + cs[c] + cs[t[:, 0]] + cs[t[:, 1]] + cs[t[:, 2]] + cs[t[:, 3]]
            is_ = sn[c] + sn[t[:, 0]] + sn[t[:, 1]] + sn[t[:, 2]] + sn[t[:, 3]]
            kp = rs * rs + is_ * is_ <= pre * pre
            counts["-"][c] += k
            if not kp.any():
                continue
            t2 = t[kp]
            rs, is_ = rs[kp], is_[kp]
            k = len(t2)
            # the residual-only test is also a necessary condition; apply to survivors
            cx, cy = is_ / (2 * np.pi), -rs / (2 * np.pi)
            Jx = np.stack([np.full(k, cs[c]), cs[t2[:, 0]], cs[t2[:, 1]], cs[t2[:, 2]], cs[t2[:, 3]]], axis=1)
            Jy = np.stack([np.full(k, sn[c]), sn[t2[:, 0]], sn[t2[:, 1]], sn[t2[:, 2]], sn[t2[:, 3]]], axis=1)
            nrm = np.hypot(cx, cy)
            with np.errstate(invalid="ignore", divide="ignore"):
                vx, vy = cx / nrm, cy / nrm
            rhs = E + 0.5 * w * np.sum(np.abs(vx[:, None] * Jx + vy[:, None] * Jy), axis=1)
            okR = np.where(nrm > 0, nrm <= rhs, True)
            okP = np.ones(k, dtype=bool)
            for j in range(5):
                vx, vy = -Jy[:, j], Jx[:, j]
                lhs = np.abs(vx * cx + vy * cy)
                rhs = E + 0.5 * w * np.sum(np.abs(vx[:, None] * Jx + vy[:, None] * Jy), axis=1)
                okP &= lhs <= rhs
            counts["R"][c] += int(okR.sum())
            counts["P"][c] += int(okP.sum())
            counts["RP"][c] += int((okR & okP).sum())
    d = np.load(f"{OUT}/xlists_N{N}.npz")
    s = d["s"]
    print(f"N = {N};  X lists = {len(s):,}")
    for k, v in counts.items():
        tot = int(v[s].sum())
        print(f"  Y test set {k:2s}: Y lists total {int(v.sum()):>12,}  weighted mean {v[s].mean():8.1f}"
              f"  -> pairs {tot:>14,}   ratio to paper {tot / PAPER:.4f}")


if __name__ == "__main__":
    main()
