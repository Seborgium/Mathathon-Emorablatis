#!/usr/bin/env python3
"""Defect F2: the Stage-C clustering cutoff (.042 - 1.11 w)^2 has a negative
base for M <= 26, so squaring hides it and the effective merge radius is
non-monotone in the grid.

Paper facts: s6.3 'the heuristic radius parameter is .042 and there are two
assignment iterations.  With w = 1/M the candidate threshold is
(.042 - 1.11w)^2, and the coordinate cutoff is the square root of twice that
threshold plus 1e-10'; Lemma 6.1 X_M = sqrt(29/6) a with a = 1/(2M); Lemma 6.4
the final radius update is what certifies coverage; grids 12,24,48,96 (s7.2);
caps 2,000,000 bins and 2048 centres.

Run: python3 experiments/cluster_F2.py
"""
import math

X_COEF = math.sqrt(29 / 6) / 2      # X_M = X_COEF / M
CAP_CLUSTERS = 2048
CAP_BINS = 2_000_000
GRIDS = (12, 24, 48, 96)


def X(M):
    return X_COEF / M


def base(M, r=0.042, c=1.11):
    return r - c / M


def main():
    print("=== 1. the base of the square, and where it changes sign ===")
    print(f"   X_M = sqrt(29/6)/(2M) = {X_COEF:.6f}/M ; 1.11w = 1.11/M")
    print(f"   1.11 > {X_COEF:.6f}, so 1.11w is a {100 * (1.11 / X_COEF - 1):.2f}% "
          "over-estimate of X_M: a valid upper bound.")
    print("   .042 - 1.11/M < 0  <=>  M < 1.11/.042 = "
          f"{1.11 / 0.042:.3f}  <=>  M <= 26")
    print("   M    X_M      1.11/M    base      effective radius |base|"
          "   coordinate cutoff sqrt(2)|base|   bin spacing 1/M")
    for M in (6, 12, 24, 26, 27, 32, 48, 96):
        b = base(M)
        print(f"  {M:4d} {X(M):8.5f} {1.11 / M:9.5f} {b:9.5f}   {abs(b):22.5f}"
              f"   {math.sqrt(2) * abs(b):30.5f}   {1 / M:14.5f}")

    print("\n=== 2. non-monotonicity over the run's four grids ===")
    prev = None
    for M in GRIDS:
        b = base(M)
        eff = abs(b)
        cut = math.sqrt(2) * eff + 1e-10
        ratio = cut / (1 / M)
        dirn = "" if prev is None else ("DOWN" if eff < prev else "up")
        print(f"   M={M:3d}: threshold={b * b:.6f}  effective radius={eff:.5f}"
              f"  coordinate cutoff={cut:.5f}  cutoff/spacing={ratio:.4f}  {dirn}")
        prev = eff
    print("   .0505 -> .0042 -> .0189 -> .0304: the effective merge radius falls by")
    print("   12x from grid 12 to grid 24 and then rises 7x: it is NOT monotone in M.")
    print("   the paper's intent (1.11w is an upper bound for X_M, so .042 - 1.11w")
    print("   is the margin left after paying the bin norm) is only realised for")
    print("   M >= 27.")

    print("\n=== 3. why M=24 is the worst case: the cutoff is below the spacing ===")
    for M in (12, 24, 48, 96):
        cut = math.sqrt(2) * abs(base(M))
        print(f"   M={M:3d}: a neighbouring midpoint is at distance 1/M = {1 / M:.5f}"
              f" per coordinate; the cutoff is {cut:.5f}"
              f" -> {'CANNOT merge' if cut < 1 / M else 'can merge'}"
              f"  (ratio {cut * M:.4f})")
    print("   at M=24 no bin can merge into an existing centre, so clustering")
    print("   degenerates to one centre per retained bin, the most expensive and")
    print("   weakest regime, and the one that would trip the 2048-centre cap.")
    print(f"   the ratio bins/centres needed to stay under the cap is "
          f"{CAP_BINS}/{CAP_CLUSTERS} = {CAP_BINS // CAP_CLUSTERS}:1; at M=24 the")
    print("   achieved ratio is 1:1.")

    print("\n=== 4. the two candidate fixes ===")
    print("   M    |.042-1.11w| (current)   max(0,.042-1.11w)   .042-X_M")
    for M in (12, 24, 26, 48, 96, 192):
        cur = abs(base(M))
        fix = max(0.0, base(M))
        alt = max(0.0, 0.042 - X(M))
        print(f"  {M:4d} {cur:22.5f} {fix:22.5f} {alt:12.5f}")
    print("   max(0,.042-X_M)^2 is monotone non-decreasing in M for M > 0")
    print("   (it is 0 for M <= 26 and rises thereafter), it is the faithful")
    print("   reading of '1.11w bounds X_M', and it changes nothing for M >= 48.")
    print("   Deleting the merge test entirely also restores monotonicity (to the")
    print("   constant 0) and loses nothing: Lemma 6.4's radius update is the")
    print("   certificate, and s6.3 says so explicitly.")

    print("\n=== 5. is it a soundness defect?  no ===")
    print("   Lemma 6.4 sets the assigned radius to max(projected distance + X_M,")
    print("   1e-9), whatever the assignment was; a too-large cutoff only changes")
    print("   which centre a bin is assigned to, and the radius follows.  So the")
    print("   defect costs work, never coverage.  s6.3's own sentence - 'these")
    print("   constants affect only the choice of assignments; the proof is the")
    print("   final radius update in Lemma 6.4' - is the paper supporting the")
    print("   harmless reading.  Recorded run: no clustering failures reported, so")
    print("   the cap was not hit at any grid.")

    print("\n=== 6. the real constraint on the .042 parameter ===")
    print("   for the merge test to be able to fire at all at resolution M we need")
    print("   sqrt(2)|.042-1.11/M| >= 1/M, i.e. .042 >= (1/sqrt2 + 1.11)/M, i.e.")
    need = (1 / math.sqrt(2) + 1.11)
    print(f"   M >= {need / 0.042:.3f} for a merge to be geometrically possible.")
    print("   So .042 and the grid set {12,24,48,96} are jointly constrained: with")
    print("   .042 and grids below 45 the clustering stage cannot cluster.")
    for r in (0.042, 0.05, 0.06, 0.08):
        print(f"   r={r:.3f}: merges possible from M >= {need / r:.1f}")

    import os
    os.makedirs("data", exist_ok=True)
    with open("data/cluster_F2.csv", "w") as fh:
        fh.write("M,X_M,one_11_over_M,base,effective_radius,coord_cutoff,spacing,"
                 "cutoff_over_spacing,monotone_fix\n")
        for M in list(range(6, 200, 6)) + [12, 24, 48, 96]:
            b = base(M)
            cut = math.sqrt(2) * abs(b)
            fh.write(f"{M},{X(M):.6f},{1.11 / M:.6f},{b:.6f},{abs(b):.6f},"
                     f"{cut:.6f},{1 / M:.6f},{cut * M:.6f},{max(0.0, b):.6f}\n")
    print("\nwrote data/cluster_F2.csv")


if __name__ == "__main__":
    main()
