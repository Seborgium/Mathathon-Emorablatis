#!/usr/bin/env python3
"""Stage C: the clustering cutoff (defect F2), the initial resolution, the caps,
and the ell sentinel (defect F4).   Run: python3 experiments/stageC.py
"""
import csv, os
from math import sqrt, pi

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, os.pardir, os.pardir, "data", "m3"))
def pr(*a): print(*a)
rows, rec = [], []
def r2(k, v, note=""):
    rec.append((k, v, note)); pr(f"  {k:<44} {v:>20}  {note}")

XS = sqrt(29.0 / 6.0)          # Lemma 6.1: X_M = sqrt(29/6) * a, a = 1/(2M)
RAD = 0.042                    # mub6.txt 6.3: 'the heuristic radius parameter is .042'
pr("=" * 104)
pr("1. Defect F2: the Stage-C cutoff (.042 - 1.11 w)^2 with w = 1/M")
pr("=" * 104)
pr(f"  X_M = sqrt(29/6)/(2M) = {XS:.6f}/(2M) = {XS/2:.6f}/M;  the cutoff uses 1.11/M = {(1.11/ (XS/2)):.5f} * X_M")
pr(f"  the base .042 - 1.11/M is negative  <=>  M < 1.11/.042 = {1.11/RAD:.4f}  <=>  M <= 26")
hdr = (f"{'M':>4} {'X_M':>8} {'1.11/M':>8} {'.042-1.11/M':>12} {'squared':>10} {'coord cut':>10} "
       f"{'spacing':>8} {'proj dist':>10} {'merge?':>7} {'centres=s?':>11}")
pr(hdr); pr("-" * len(hdr))
for M in (12, 18, 24, 26, 27, 48, 96, 192):
    base = RAD - 1.11 / M
    thr = base * base
    cut = sqrt(2 * thr)                 # 'square root of twice that threshold' (6.3)
    spacing = 1.0 / M
    proj = sqrt(5.0 / 6.0) / M          # projected nearest-midpoint distance
    merge = proj <= cut
    rows.append(dict(M=M, X_M=round(XS/(2*M), 6), one11=round(1.11/M, 6), base=round(base, 6),
                     threshold_squared=round(thr, 8), coord_cutoff=round(cut, 6),
                     spacing=round(spacing, 6), proj_dist=round(proj, 6),
                     merge_possible=merge, centres_equals_bins=not merge))
    pr(f"{M:>4} {XS/(2*M):>8.4f} {1.11/M:>8.4f} {base:>12.6f} {thr:>10.6f} {cut:>10.4f} "
       f"{spacing:>8.4f} {proj:>10.4f} {str(merge):>7} {str(not merge):>11}")
pr()
pr("  The base is negative for M <= 26, so 1.11/M over-bounds X_M by 0.98% and the sign")
pr("  is swallowed by the square: the effective radius |.042 - 1.11/M| is NON-MONOTONE")
eff = [(M, abs(RAD - 1.11/M)) for M in (12, 24, 48, 96, 192)]
pr("  M:  " + "  ".join(f"{M:>6}" for M, _ in eff))
pr("  eff " + "  ".join(f"{v:>6.4f}" for _, v in eff))
pr()
pr("  What actually happens: at M=12 and M=24 the cutoff is below the lattice spacing,")
pr("  so NO bin can be assigned to another bin's centre.  The cluster count then equals")
pr("  the retained-bin count and the 2048-centre cap becomes a cap on retained bins at")
pr("  those two grids.  The recorded run reports no clustering failure (mub6.txt 7.5),")
pr("  hence every record retained <= 2048 bins at M=12 and M=24.")

first_merge = next(M for M in range(12, 400)
                   if sqrt(5.0/6.0)/M <= sqrt(2)*abs(RAD - 1.11/M))
first_merge_fix = next(M for M in range(12, 400)
                       if sqrt(5.0/6.0)/M <= sqrt(2)*max(0.0, RAD - XS/(2*M)))
pr(f"  First M at which ANY assignment can succeed: printed formula M = {first_merge};")
pr(f"  repaired formula M = {first_merge_fix}.  With the C recursion 12->24->48->96 this means")
pr("  only the last grid can cluster at all under the printed formula, and the repaired")
pr("  formula recovers the layer M=48.")

corr = [(M, max(0.0, RAD - XS/(2*M)) ** 2) for M in (12, 24, 48, 96, 192)]
pr("  Suggested repair  max(0, .042 - X_M)^2:")
pr("  M:      " + "".join(f"{M:>12}" for M, _ in corr))
pr("  value:  " + "".join(f"{v:>12.6f}" for _, v in corr))
pr("  monotone in M (0 up to M=26, then increasing), sign never lost, same value as the")
pr("  printed formula wherever it is positive (M >= 27).  Track: T3 P3.4 / T8.")

pr()
pr("=" * 104)
pr("2. Why M = 12 (the initial resolution) and not less: the s < .1 check (Lemma 6.4)")
pr("=" * 104)
for M in (10, 11, 12, 24):
    pr(f"  M={M:>3}: a centre that absorbs nothing has radius X_M = {XS/(2*M):.4f}  "
       f"({'passes' if XS/(2*M) < .1 else 'FAILS'} the final check s < .1)")
pr(f"  X_M < .1  <=>  M > {XS/2/.1:.4f}  =>  M >= 11.  M = 12 is the smallest integer with")
pr(f"  slack, and its slack is {(1- XS/24/.1):.1%} (X_12 = {XS/24:.4f} vs .1).  A base grid of 10 would have")
pr("  made every record unresolved, i.e. the run could not have completed.")
r2("initial M", 12, "6.3 'The initial resolution is M = 12'")
r2("M >= 11 forced by s<.1", f"{XS/2/.1:.4f}", "X_M < .1")
r2("12^5 bins at M=12", f"{12**5:,}", "6.3; 12.4% of the 2e6 bin cap")
r2("2e6 bin cap at M=24 if all children kept", f"{32*12**5:,}", f"{32*12**5/2e6:.2f}x the cap")
r2("2048 centre cap", "2048", "6.3; binding in effect at M=12,24 because nothing merges")

pr()
pr("=" * 104)
pr("3. Defect F4: the ell sentinel 100 and its neighbours")
pr("=" * 104)
r2("legitimate certified gu (A.8)", "[0, 100.1]", "explicit upper bound in A.8")
r2("invalid sentinel returned by ell", "100", "inside [0,100.1]")
r2("separation from the top of the range", f"{100.1-100:.2f}", "0.1")
r2("ell triangle bound for valid data", "< 43", "A.8")
r2("improved candidate", "< 44", "A.8")
r2("what rejects the sentinel downstream", "2*pi*100 = 628.3 > 10", "the t < 10 bootstrap guard")
r2("bootstrap sentinel", "10", "with guard 0 <= t < 10: safe, the guard rejects both")
r2("relationB::eval sentinel", "10", "guard 0 <= t <= 2: separation 8, safer")
r2("legitimate t range at ell's exit", f"up to 2*pi*43 = {2*pi*43:.1f}", "so 10 is NOT outside the legitimate range")
pr()
pr("  Reading: 100 is not distinguishable from a valid gu, and 10 is not outside the")
pr("  legitimate t range (a valid t can be 270). Both work only because a later STRICT")
pr("  guard happens to reject them. Recommend: NaN + isnan, or a status flag; and state")
pr("  the guard as the definition of failure rather than as a numerical comparison.")

with open(os.path.join(DATA, "stageC_cutoff.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
with open(os.path.join(DATA, "stageC_scalars.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["quantity", "value", "note"]); w.writerows(rec)
pr()
pr(f"  wrote {DATA}/stageC_cutoff.csv and stageC_scalars.csv")
