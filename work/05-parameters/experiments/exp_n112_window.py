#!/usr/bin/env python3
"""N = 112: recompute every constraint on the seed-cover bin count, plus the cost curve.

CORRECTION (m6, second submission).  An earlier version of this script printed a reuse "ceiling"
(2NR/3)^9 and a centre-count model built on it.  Both were WRONG and are withdrawn: (2NR/3)^9 is not
a bound on the number of bins a ball can absorb -- that is the lattice count
#{k in Z^9 : ||k|| <= NR} = 284,055 at N=112 -- and 607 = pairs/centres mixes filtering with reuse, so
it cannot be compared with either.  The defensible quantity is the REACH
#{k in Z^9 : ||k|| <= NR - 1.5}, whose exact counts are printed by m6_conditioning.py (2869 at N=112,
1 at N=56).  Everything printed below is a count or a ratio of counts and is unaffected.

Sources (paper): bins [b/N,(b+1)/N] (2.6); nine seed coordinates q (2.15) with bin half-diagonal
sqrt(9)/(2N) (Prop. 2.10); gap filters (2.8) with w = 1/N and Lemma 2.5; tuple counts and the
"signed 32-bit limit" of 7.3; int8 five-coordinate differences and int32 nine-coordinate squares
(A.3, 7.3).  Run data (Table 1, 7.5) is used only for the measured unit cost.
"""
import csv, os
from math import comb, ceil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
R, INT32, INT8_MAX = 0.032, 2**31, 127
OBS = dict(pairs=151_744_086, centres=249_878, xlists=22_829, cover_seconds=621.59)
tuples = lambda N: comb(N + 4, 5)
tails = lambda N: comb(N + 3, 4)

print("=" * 78); print("1. tuple counts and the 32-bit window"); print("=" * 78)
print(f"C(116,5) = {tuples(112):,} (paper 160,389,488); C(115,4) = {tails(112):,} (paper 6,913,340)")
n32 = max(N for N in range(1, 400) if tuples(N) < INT32)
print(f"largest N with C(N+4,5) < 2^31: N = {n32}, C(193,5) = {tuples(n32):,}")
print(f"  next: N = {n32+1}, C({n32+5},5) = {tuples(n32+1):,} (> 2^31 by {tuples(n32+1)-INT32:,})")

print(); print("=" * 78); print("2. lower bound on N from coverage (Prop. 2.10)"); print("=" * 78)
print(f"3/(2N) <= R = {R}  <=>  N >= {3/(2*R)}  =>  N >= {ceil(3/(2*R))}")
for N in (47, 56, 112, 128, 189, 224):
    print(f"  N={N:4d}: 3/(2N) = {3/(2*N):.6f} = {100*3/(2*N)/R:6.2f}% of R;"
          f"  reach r = NR-1.5 = {max(0.0,N*R-1.5):7.4f}")

print(); print("=" * 78); print("3. the other storage limits"); print("=" * 78)
print(f"int8 five-coordinate differences: N-1 <= 127  =>  N <= {INT8_MAX+1}")
print(f"int32 nine-coordinate squares: 9(N-1)^2 <= 2^31-1  =>  "
      f"N <= {max(n for n in range(1,4000) if 9*(n-1)**2 <= INT32-1)}")
print(f"at N=112: 9*111^2 = {9*111**2:,}; at N=128: 9*127^2 = {9*127**2:,}")

print(); print("=" * 78); print("4. gap filters (2.8) against Lemma 2.5"); print("=" * 78)
print("as printed: gx,mid <= 1-(l-1)/N, gy,mid >= 1-(l+2)/N -- thresholds differ by 3/N.")
print("but gx,mid = 1-(l+1/2)/N identically, so the first inequality holds with 1.5/N to spare for")
print("EVERY bin and every N: it can never reject.  The live filter follows from x5 <= (l+1)/N:")
print("  gx >= 1-(l+1)/N, gy >= gx, gy,mid >= gy - w  =>  gy,mid >= 1-(l+2)/N,")
print("and its spread against the exact bound is exactly w: zero analytic reserve at every N.")
for N in (47, 112, 189):
    print(f"  N={N:4d}: printed spread 3/N = {3/N:.6f}; live spread 1/N = {1/N:.6f}")

print(); print("=" * 78); print("5. cost curve (measured unit cost 4.10 us/pair)"); print("=" * 78)
print(f"run: {OBS['pairs']:,} pairs -> {OBS['centres']:,} centres in {OBS['cover_seconds']} s"
      f" ({OBS['cover_seconds']*1e6/OBS['pairs']:.2f} us/pair); {OBS['xlists']:,} x-lists retained")
print("the counters mix filtering with reuse: no reuse rate can be read off them.")
rows = []
for N in (47, 56, 64, 80, 96, 112, 128, 144, 160, 176, 189, 224):
    T = tuples(N)
    r = dict(N=N, tuples=T, bits=T.bit_length(), fits_int32=int(T < INT32),
             fits_int8=int(N - 1 <= INT8_MAX), tails=tails(N), bin_radius=3/(2*N),
             ratio_to_R=(3/(2*N))/R, reach_radius=max(0.0, N*R-1.5),
             cover_seconds=OBS["cover_seconds"]*T/tuples(112))
    rows.append(r)
    print(f"N={N:4d} C(N+4,5)={T:>13,} ({T.bit_length():2d} bits) int32={r['fits_int32']} "
          f"int8={r['fits_int8']} C(N+3,4)={r['tails']:>12,} 3/(2N)={r['bin_radius']:.6f}"
          f" reach={r['reach_radius']:6.3f} cover={r['cover_seconds']:9,.0f}s")

print(); print("=" * 78); print("6. sensitivity"); print("=" * 78)
for f in (0.5, 0.9, 1.1, 2.0):
    N = int(round(112*f))
    print(f"  N={N:4d} ({f:4.2f}x): tuples x{tuples(N)/tuples(112):7.3f}, cover"
          f" {OBS['cover_seconds']*tuples(N)/tuples(112):8,.0f}s, bin radius x{112/N:4.2f},"
          f" reach r={max(0.0,N*R-1.5):.3f}")
print(f"N=224: C(228,5) = {tuples(224):,} > 2^31; int8 differences up to 223 > 127;"
      f" cost x{tuples(224)/tuples(112):.2f}")
print(f"N=56: reach falls from 2869 offsets to 1; R cannot shrink with N (needs >= {3/(2*56):.5f}).")
n8 = INT8_MAX + 1
print(f"WINDOW: [47, {n8}] under the paper's storage limits, [47, {n32}] under the 32-bit count alone.")

os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, "n112_window.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(f"\nwrote {os.path.join(DATA,'n112_window.csv')}")
