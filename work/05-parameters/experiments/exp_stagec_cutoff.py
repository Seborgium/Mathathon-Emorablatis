#!/usr/bin/env python3
"""F2: the Stage-C clustering cutoff (.042 - 1.11 w)^2 at w = 1/M.

Recomputed from Lemma 6.1 (X_M = sqrt(29/6) a, a = 1/(2M)) and section 6.3:
  "with w = 1/M the candidate threshold is (.042 - 1.11 w)^2, and the coordinate cutoff is the
   square root of twice that threshold plus 1e-10".
The heuristic intends: a bin may join a centre only if its projected midpoint distance plus the
bin's own displacement bound X_M still fits the .042 radius, i.e. d + X_M <= .042.
Squaring (.042 - 1.11/M) hides the sign, so for X_M > .042 the condition is silently replaced
by d <= |.042 - 1.11/M|, which is the wrong direction (it accepts merges the radius cannot
cover, and rejects nothing).  Correction: max(0, .042 - X_M)^2 -- or delete the merge.
"""
import csv, os
from math import sqrt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
C = sqrt(29.0 / 6.0)
RAD, COEF = 0.042, 1.11
GRIDS = [12, 24, 48, 96]

print("=" * 78)
print("1. the table the audit calls non-monotone")
print("=" * 78)
rows = []
print(f"X_M = sqrt(29/6)/(2M) = {C:.6f}/(2M);  code uses 1.11/M = {COEF}/M "
      f"(ratio 1.11/{C/2:.6f} = {COEF/(C/2):.5f} >= 1, conservative)")
for M in (12, 24, 25, 26, 27, 32, 48, 64, 96, 192):
    X = C / (2 * M)
    w = 1.0 / M
    base = RAD - COEF * w
    thr = base * base
    eff = abs(base)
    coord = sqrt(2 * thr) + 1e-10
    spacing = 1.0 / M
    correct = max(0.0, RAD - X) ** 2
    rows.append(dict(M=M, X_M=X, one_11_over_M=COEF * w, base=base, sign=int(base > 0),
                     threshold=thr, effective_radius=eff, coord_cutoff=coord,
                     midpoint_spacing=spacing, coord_over_spacing=coord / spacing,
                     merge_possible=int(coord > spacing),
                     correct_threshold=correct,
                     correct_radius=sqrt(correct)))
    print(f"M={M:4d}: X_M={X:.5f} 1.11/M={COEF*w:.5f} base={base:+.5f} "
          f"thr={thr:.3e} R_eff={eff:.5f} coord={coord:.5f} spacing={spacing:.5f} "
          f"coord/space={coord/spacing:5.3f} merge? {int(coord>spacing)} "
          f"| correct: thr={correct:.3e} R={sqrt(correct):.5f}")

print()
print("=" * 78)
print("2. where the sign flips, and the audit's boundary")
print("=" * 78)
print(f"code: base >= 0 iff 1.11/M <= .042 iff M >= 1.11/.042 = {COEF/RAD:.4f} -> M >= 27")
print("so the base is negative for M <= 26, not only for M < 26 as the audit states:")
for M in (25, 26, 27):
    print(f"  M={M}: base = {RAD - COEF/M:+.6f}  ({'NEGATIVE' if RAD-COEF/M < 0 else 'positive'})")
print("(with the exact X_M the flip is at M >= %.4f, i.e. also M >= 27)" % (C/(2*RAD)))

print()
print("=" * 78)
print("3. is the effective radius monotone in M, and can a bin merge?")
print("=" * 78)
prev = None
for M in GRIDS:
    eff = abs(RAD - COEF / M)
    print(f"  M={M:3d}: effective radius {eff:.5f}" + ("" if prev is None else
          f"  ({'UP' if eff > prev else 'DOWN'} from {prev:.5f}, factor {eff/prev:.3f})"))
    prev = eff
print("  => non-monotone: .0505 (M=12) -> .0042 (M=24) -> .0189 (M=48) -> .0304 (M=96).")
print()
print("  minimum midpoint separation in the projected metric is about (5/6)/M (one coordinate")
print("  moves by 1/M, then the mean is removed):")
for M in GRIDS:
    coord = sqrt(2 * (RAD - COEF / M) ** 2)
    print(f"  M={M:3d}: bin separation ~{5/(6*M):.5f}, coordinate cutoff {coord:.5f},"
          f" ratio {coord/(5/(6*M)):.3f} -> merges {'possible' if coord > 5/(6*M) else 'IMPOSSIBLE'}")
print("  at M=24 the cutoff .0060 is 7x below the .0347 separation: one centre per bin.")
print("  That is also the state the heuristic is in for M <= 26 anyway.")

print()
print("=" * 78)
print("4. cost and soundness")
print("=" * 78)
print("  soundness: unchanged.  Lemma 6.4's proof is the final radius update; the cutoff only")
print("  chooses assignments (section 6.3 says so explicitly).  A bad assignment costs radius,")
print("  and a radius >= .1 is caught by the final check |v_j| <= 2, s < .1 -> unresolved.")
print("  cost: centres = bins whenever the cutoff is below the bin separation.  With the 2048")
print("  centre cap, a record survives only if it retains <= 2048 bins at that grid.  The run")
print("  reports zero clustering failures, so retained bins at M=24 must have been <= 2048.")
print("  with the corrected max(0,.042-X_M)^2 the M=24 behaviour is the same (X_M > .042),")
print("  so the correction is cosmetic there; what changes is M<=26 no longer pretends to merge.")
print("  the only real fix is to keep the constant ratio .042/(1/M) fixed: .042 is 4.7 bins")
print("  at M=12, 1.0 bins at M=24, 2.0 at M=48, 4.0 at M=96 -- i.e. .042 is not a grid-")
print("  independent radius at all.  Scaling the radius with the grid (.042*M/96) would make")
print("  the merge behaviour M-independent.")
print()
print("which reading the paper supports: section 6.3 states the threshold affects only the choice")
print("of assignments and 'the proof is the final radius update in Lemma 6.4'.  So deleting the")
print("merge heuristic altogether is supported by the paper's own argument; max(0,.)^2 is the")
print("minimal repair; leaving (.042-1.11w)^2 is also sound but its behaviour at M <= 26 is")
print("opposite to its intent.")

os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, "stagec_cutoff.csv"), "w", newline="") as fh:
    w_ = csv.DictWriter(fh, fieldnames=list(rows[0])); w_.writeheader(); w_.writerows(rows)
print(f"\nwrote {os.path.join(DATA,'stagec_cutoff.csv')}")
