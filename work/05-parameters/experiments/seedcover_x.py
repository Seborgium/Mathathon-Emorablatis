#!/usr/bin/env python3
"""Replay of the X side of the seed cover (paper sections 2.2-2.3).

For N bins this counts, exactly and in the paper's order of filtering:
  A  weakly increasing 5-bin tuples (a,b,c,d,l), 0 <= a <= b <= c <= d <= l < N
  B  survivors of the integral orientation filter (2.7):  a <= l-d+1
  C  survivors of the midpoint gap filter (2.8) first inequality
  D  survivors of the vanishing-sum filter sumok (2.11), tested in the residual
     direction and in the five directions perpendicular to the unit-exponential
     columns J_j -- the test set the paper describes after (2.11).
  D is exactly the paper's "five-bin x lists" of table 1 (caption, section 7.5).

The shared bin is s = first minimiser of |2 b_s + 1 - N| over the five bins; the
surviving tuples are written to .scratch-free files under work/05-parameters/data/.

Run: python3 experiments/seedcover_x.py [N ...]
"""
import sys
from itertools import combinations_with_replacement

import numpy as np

OUT = "work/05-parameters/data"


def x_lists(N):
    """Return a dict with the count ladder and the surviving tuples (arrays)."""
    w = 1.0 / N
    mid = (np.arange(N) + 0.5) / N
    cs, sn = np.cos(2 * np.pi * mid), np.sin(2 * np.pi * mid)
    E = 5 * np.pi * w * w / 4.0
    pre = 2 * np.pi * (E + 2.5 * w)          # necessary for every test in (2.11)

    nA = nB = nC = nD = 0
    keep_tuples = []
    for d in range(N):
        tri = np.array(list(combinations_with_replacement(range(d + 1), 3)), dtype=np.int16)
        a_, b_, c_ = tri[:, 0], tri[:, 1], tri[:, 2]
        ori = {}
        for l in range(d, N):
            nA += len(a_)
            o = a_ <= l - d + 1
            nB += int(o.sum())
            M = N - l + 1                     # integer form of the threshold 1-(l-1)/N
            m = o & (a_ * 2 + 1 <= 2 * M) & (b_ - a_ <= M) & (c_ - b_ <= M) & (d - c_ <= M) & (l - d <= M)
            nC += int(m.sum())
            if not m.any():
                continue
            ia, ib, ic = a_[m], b_[m], c_[m]
            rs = 1.0 + cs[ia] + cs[ib] + cs[ic] + cs[d] + cs[l]
            is_ = sn[ia] + sn[ib] + sn[ic] + sn[d] + sn[l]
            kp = rs * rs + is_ * is_ <= pre * pre
            if not kp.any():
                continue
            sel = np.nonzero(kp)[0]
            ia, ib, ic = ia[sel], ib[sel], ic[sel]
            k = len(sel)
            cx, cy = is_[sel] / (2 * np.pi), -rs[sel] / (2 * np.pi)
            Jx = np.stack([cs[ia], cs[ib], cs[ic], np.full(k, cs[d]), np.full(k, cs[l])], axis=1)
            Jy = np.stack([sn[ia], sn[ib], sn[ic], np.full(k, sn[d]), np.full(k, sn[l])], axis=1)
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
            nD += int(ok.sum())
            if ok.any():
                s = np.nonzero(ok)[0]
                keep_tuples.append(np.stack([ia[s], ib[s], ic[s],
                                             np.full(len(s), d, dtype=np.int16),
                                             np.full(len(s), l, dtype=np.int16)], axis=1))
    T = np.concatenate(keep_tuples) if keep_tuples else np.zeros((0, 5), dtype=np.int16)
    return dict(N=N, A=nA, B=nB, C=nC, D=nD, tuples=T)


def shared_bin(t, N):
    """s = first minimiser of |2 b_s + 1 - N| over the five bins (seeds::mk)."""
    dist = np.abs(2 * t + 1 - N)
    return np.argmin(dist, axis=1)


if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] or [112]
    for N in ns:
        r = x_lists(N)
        s = shared_bin(r["tuples"], N) if len(r["tuples"]) else np.zeros(0, dtype=int)
        np.savez(f"{OUT}/xlists_N{N}.npz", tuples=r["tuples"], s=s, l=r["tuples"][:, 4] if len(r["tuples"]) else [])
        print(f"N={N:4d}  A={r['A']:>13,}  B={r['B']:>13,}  C={r['C']:>12,}"
              f"  D(sumok)={r['D']:>8,}")
