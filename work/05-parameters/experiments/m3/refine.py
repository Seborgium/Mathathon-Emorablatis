#!/usr/bin/env python3
"""Stage B: the three (tau,w) passes, the box/k/depth caps, the 25 midpoint trials,
the 30 bootstrap updates, the 1e-6 divisor skip.
Run: python3 experiments/refine.py
"""
import csv, os
from math import sqrt, ceil, log2, pi

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, os.pardir, os.pardir, "data", "m3"))
def pr(*a): print(*a)
rows, rec = [], []
def r2(k, v, note=""):
    rec.append((k, v, note)); pr(f"  {k:<40} {v:>20}  {note}")

BOX_CAP, DEPTH, W_FLOOR = 50_000_000, 6, 1e-4
oP = 1e-5                                  # A.9: 0 <= ort < 1e-5
passes = [(1, 0.126, 0.07, 0.013), (2, 0.070, 0.016, 0.005), (3, 0.016, 0.011, 0.0038)]

pr("=" * 100)
pr("1. L = ceil(E/w + 0.500001), n = 2L+1, boxes = n^k, with E = sqrt(1+oP) R + 1e-7")
pr("=" * 100)
hdr = f"{'pass':>4} {'R_in':>7} {'tau':>6} {'w':>7} {'E':>10} {'L':>4} {'n=2L+1':>7} {'23^5..n^k at k=5':>17} {'k_max(cap)':>11} {'k_max(diam)':>12} {'depth ok':>9}"
pr(hdr); pr("-" * len(hdr))
for i, Rin, tau, w in passes:
    E = sqrt(1 + oP) * Rin + 1e-7
    L = ceil(E / w + 0.500001)
    n = 2 * L + 1
    kcap = max(k for k in range(0, 40) if n**k <= BOX_CAP)
    kdiam = max(k for k in range(0, 400) if sqrt(k) * w <= 2 * tau)
    dok = max(d for d in range(0, 20) if w / 2**d >= W_FLOOR)
    rows.append(dict(pass_no=i, R_in=Rin, tau=tau, w=w, E=round(E, 8), L=L, n=n,
                     boxes_k5=n**5, boxes_k7=n**7, boxes_k10=n**10,
                     k_max_box_cap=kcap, k_max_diameter=kdiam, depth_ok=dok))
    pr(f"{i:>4} {Rin:>7.3f} {tau:>6.3f} {w:>7.4f} {E:>10.7f} {L:>4} {n:>7} {n**5:>17,} {kcap:>11} {kdiam:>12} {dok:>9}")
pr()
pr("  C(116,5) / boxes: pass 1 axes 23, pass 2 axes 31, pass 3 axes 11 -- reproduces audit F3.")
pr("  k_max(cap) = 5, 5, 7: the stated allowance 0 <= k <= 10 is unreachable in passes 1-2")
pr(f"  and 3 short in pass 3.  n^6 pass1 = {23**6:,} > 5e7; n^6 pass2 = {31**6:,} > 5e7;")
pr(f"  n^8 pass3 = {11**8:,} > 5e7.  So a k=6 record in mid.bin could not be refined at all.")
pr()
dl = [int((2*tau/w)**2) for (_, _, tau, w) in passes]
pr(f"  k_max(diameter): a k-box of side 2w must fit in a child sphere of radius tau, so")
pr(f"  sqrt(k) w <= 2 tau is necessary.  It gives k <= {dl[0]} / {dl[1]} / {dl[2]} -- never binding.")
pr("  Hence 'w smaller than the child radius' is true but far from necessary: the real")
pr("  binding constraint on w is the BOX CAP from below (see section 2) and the")
pr("  child radius from above (w <= 2 tau/sqrt(k)).")

pr()
pr("=" * 100)
pr("2. w_min(k) = E/(L_max(k)-0.500001) with (2 L_max+1)^k <= 5e7  -- box cap, lower bound on w")
pr("=" * 100)
for i, Rin, tau, w in passes:
    E = sqrt(1 + oP) * Rin + 1e-7
    for k in (5, 6, 7, 10):
        nmax = int(BOX_CAP ** (1.0 / k))
        while nmax ** k > BOX_CAP:
            nmax -= 1
        Lmax = (nmax - 1) // 2
        # ceil(E/w + 0.500001) <= Lmax  <=>  E/w <= Lmax - 0.500001
        wmin = E / (Lmax - 0.500001)
        pr(f"  pass {i}: k={k:2d}  n_max = {nmax:3d}  L_max = {Lmax:3d}  w_min = {wmin:.5f}   w = {w:.4f}  "
           f"w/w_min = {w/wmin:6.2f}  {'ok' if w >= wmin else 'FAILS'}")

pr()
pr("=" * 100)
pr("3. Subdivision depth vs the stated width range 1e-4 <= w <= .05")
pr("=" * 100)
for i, Rin, tau, w in passes:
    d = max(dd for dd in range(0, 20) if w / 2**dd >= W_FLOOR)
    pr(f"  pass {i}: w = {w:.4f}; w/2^d >= 1e-4 for d <= {d}; at d=6 the width is {w/64:.3e} "
       f"({'inside' if w/64 >= 1e-4 else 'BELOW'} the stated floor)")
pr("  So at passes 2 and 3 the sixth subdivision level exits the printed range")
pr("  .0001 <= w <= .05.  Either the range governs the invocation parameter only")
pr("  (almost certainly what is meant) or the depth cap is effectively 5 there.")
pr("  Recommend the paper say which: 'w' is the invocation width; the effective")
pr("  subdivision floor is w_min = w/2^6 = 7.8e-5 (pass 2), 5.9e-5 (pass 3).")

pr()
pr("=" * 100)
pr("4. The 25 midpoint trials of the rho search (5.2, 5.18-5.19)")
pr("=" * 100)
for a in (0.03, 0.07, 0.126):
    width = 1.01 * a
    res = width / 2**25
    need = ceil(log2(width / 1e-7))
    pr(f"  a = {a:.3f}: interval 1.01a = {width:.5f}; after 25 halvings the resolution is "
       f"{res:.2e}; bits needed to resolve 1e-7 = {need}; slack {25-need} bits (x{2**(25-need):.0f})")
pr("  So 25 is 4-7 bits more than needed: it is a generous, harmless cap, and the search")
pr("  never needed more than 21 trials at any radius in the run.")
pr()
pr("=" * 100)
pr("5. The 30 bootstrap updates (4.6) and the 30 relation improvements (5.2)")
pr("=" * 100)
pr("  Each iterate is an upper bound and the sequence is non-increasing (Lemmas 4.13, 5.3),")
pr("  so stopping after ANY finite number is sound. 30 is therefore a pure work cap:")
pr("  there is no inequality it must satisfy, and no reported statistic tests whether it")
pr("  binds.  Recommend: report the number of records for which the 30th iterate still")
pr("  improved (and the same for the 30 relation improvements).")

pr()
pr("=" * 100)
pr("6. The 1e-6 divisor skip in extend (2.14), (A.11)")
pr("=" * 100)
N = 112
r2("numerator N*v.c bound", f"{N*1.01:.2f}", "A.3: residual magnitude below 112 (norm<1.01 dir)")
r2("support bound before division", "3", "A.3: 'the support before division is below three'")
r2("skipped |a| > .999e-6", "9.99e-7", "at an accepted divisor")
r2("largest quotient 3/|a|", f"{3/9.99e-7:.3e}", "A.3: below 3e6")
r2("largest midpoint quotient", f"{112/9.99e-7:.3e}", "A.3: below 1.2e8")
r2("division rounding at that scale", f"2.22e-16*1.12e8={2.22e-16*1.12e8:.2e}", "")
r2("endpoint inflation", "1e-5", "A.3")
r2("slack ratio", f"{1e-5/(2.22e-16*1.12e8):.0f}", "")
pr("  The skip is sound for ANY positive threshold: skipping removes a constraint, so the")
pr("  interval only grows (the paper says exactly this).  Its only cost is lost filtering;")
pr("  doubling or halving it changes no certificate.  Recommending: state it as a")
pr("  performance knob, not a tolerance.")

pr()
pr("=" * 100)
pr("7. L <= 1261, not 1262 (7.3, and the audit's cross-check)")
pr("=" * 100)
E = sqrt(1 + oP) * 0.126 + 1e-7
L = ceil(E / 1e-4 + 0.500001)
r2("E at R=.126, w=1e-4", f"{E:.8f}", "")
r2("L = ceil(E/1e-4 + .500001)", L, "paper prints L <= 1262")
r2("axis indices 2L+1", 2 * L + 1, "paper prints 2524")
r2("verdict", "harmless over-estimate", "of one axis index; not worth a change, worth a footnote")

with open(os.path.join(DATA, "refine_passes.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
with open(os.path.join(DATA, "refine_scalars.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["quantity", "value", "note"]); w.writerows(rec)
pr()
pr(f"  wrote {DATA}/refine_passes.csv and refine_scalars.csv")
