#!/usr/bin/env python3
"""F2: the Stage-C clustering cutoff (.042 - 1.11 w)^2, w = 1/M.

Sec. 6.3 / A.10: a bin may be assigned to a centre when the centre is within
(.042 - 1.11/M) of the bin midpoint, and Lemma 6.1 gives X_M = sqrt(29/6)/(2M)
for the bin halfwidth.   Run: python3 experiments/stagec.py
"""
from math import sqrt
import csv

C = 0.042          # 'proposed cluster radius' on the crun command line
A = 1.11           # stated bound on the coefficient of 1/M
K = sqrt(29/6)/2   # exact coefficient: X_M = K/M
print("coefficient of 1/M:   exact sqrt(29/6)/2 = %.6f   stated A = %.3f   A/exact = %.4f"
      % (K, A, A/K))

print("\nM    X_M       A/M      .042-A/M    |.| = effective radius   merge possible? (needs >= 1/M)")
rows = []
for M in (12, 24, 26, 27, 48, 51, 96, 192):
    X = K/M; ap = A/M; base = C - ap; eff = abs(base)
    ok = eff >= 1.0/M
    rows.append((M, X, ap, base, eff, 1.0/M, ok))
    print("%4d %8.5f %8.5f %10.5f %10.5f %20s %s" % (M, X, ap, base, eff, "%.5f" % (1.0/M), ok))

print("\nthe base is negative whenever A/M > .042, i.e. M <= %d (exactly 26.43)"
      % int(C/A and A/C))
print("and squaring hides that, so the 'cutoff' is an absolute value and is non-monotone:")
print("   M=12 -> .0505,  M=24 -> .0042,  M=48 -> .0189,  M=96 -> .0304  (as reported)")

print("\nneighbour test: two distinct bin midpoints differ by 1/M in one coordinate.")
print("a merge is geometrically possible only when the effective radius >= 1/M, i.e.")
print("   .042 - 1.11/M >= 1/M  <=>  M >= 2.11/.042 = %.3f  ->  M >= %d" % (2.11/C, int(2.11/C)+1))
print("(if centres may move off the lattice, the distance halves and M >= %.1f would do)"
      % (1.61/C))
print("=> on the recorded four C grids 12, 24, 48 the clustering stage merges NOTHING,")
print("   whatever the sign of the base.  Only M = 96 can compress, by up to")
print("   floor(2*.0304/.0104) = %d lattice steps." % int(2*0.0304/(1/96)))

print("\ncorrected cutoff max(0, .042 - X_M)^2 :")
print("M    X_M      .042-X_M   max(0,.)^2   monotone?")
prev = -1
mono = True
for M in (6, 12, 24, 26, 27, 48, 96, 192, 512):
    X = K/M; b = max(0.0, C - X)
    if b*b < prev: mono = False
    prev = b*b
    print("%4d %8.5f %9.5f %11.3e" % (M, X, b, b*b))
print("monotone non-decreasing:", mono)
print("still merges at M=96?  .042-X_M = %.5f >= 1/96 = %.5f -> %s"
      % (C-K/96, 1/96, (C-K/96) >= 1/96))
print("still merges at M=12?  no: %.5f < 1/12 = %.5f (correct: the bins are too coarse)"
      % (max(0.0, C-K/12), 1/12))

with open("data/m5-stagec-cutoff.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["M", "X_M", "A_over_M", "base_.042-A_over_M", "effective_radius",
                "bin_spacing_1_over_M", "merge_possible"])
    for r in rows:
        w.writerow(["%d" % r[0], "%.6f" % r[1], "%.6f" % r[2], "%.6f" % r[3],
                    "%.6f" % r[4], "%.6f" % r[5], r[6]])
print("\nwrote data/m5-stagec-cutoff.csv")
