#!/usr/bin/env python3
"""The remaining constants: sentinels (F4), grid and radius chain, free parameters,
and the closing table of Appendix A.

Every number printed here is either read off the paper or computed from it; the
inequality that constrains each constant is stated next to it.

Run: python3 experiments/constants_batch.py
"""
import csv
import math

rows = []


def row(name, where, inequality, value, slack, half, double, verdict, note=""):
    rows.append(dict(constant=name, where=where, inequality=inequality, value=value,
                     slack=slack, half=half, double=double, verdict=verdict, note=note))


def main():
    print("=== A. the U(2) grid: h = pi/Nu, constrained by (A.13) h < .197 ===")
    for nu in (8, 15, 16, 24, 32, 64, 128, 512):
        h = math.pi / nu
        # z from (3.19) with the (A.13) field bounds: Rs<.203, A<2, m>1.239, pol<.068
        uget = min(6 * h, 1.26) + 0.068 + 1e-9
        z = min(math.sqrt((0.203 * (math.sqrt(6) + 2) / 1.239) ** 2 + uget ** 2), 9)
        print(f"  Nu={nu:4d}  h={h:.5f}  uget=6h+pol={uget:.4f}  z(3.19)={z:.4f}"
              f"   h<.197: {h < 0.197}   z<1.5: {z < 1.5}")
    print(f"  smallest Nu with h<.197: pi/.197 = {math.pi / 0.197:.3f} -> Nu = 16")
    row("N_u base grid", "3.3, 7.3", "h = pi/N_u < .197 (A.13), and z(3.19) < 1.5", "16",
        f"h = {math.pi / 16:.5f} vs .197: 0.3% ; z = 1.44 vs 1.5: 4%", "N_u=8: h=.393 >> .197 fails",
        "N_u=32: h=.098, z=0.98, slack 35%", "justified", "the base grid is the smallest admissible")
    print()
    print("=== B. the local/global radius targets ===")
    chain = [0.0320001, 0.103, 0.125, 0.126]
    names = ["seed radius (A input)", "local target .103", "atlas radius cap .125",
             "B input radius cap .126"]
    for n, v in zip(names, chain):
        print(f"  {n:24s} {v}")
    print(f"  .103 < .125 < .126 : slack of .125 to the B cap = {0.126 - 0.125:.4f}"
          f" ({100 * (0.126 - 0.125) / 0.126:.2f}%)")
    print(f"  local target .103 vs atlas cap .125: slack {0.125 - 0.103:.3f} ({100 * (0.125 - 0.103) / 0.125:.1f}%)")
    row("local target .103", "4.6, 7.2", "covercompute bound < .103, else subdivide", ".103",
        f"atlas cap .125 is {100 * (0.125 - 0.103) / 0.125:.0f}% above", "finer subdivision, more cost",
        ".125 would equal the atlas cap, i.e. the atlas radius check binds", "arbitrary-but-harmless")
    row("global target / atlas cap .125", "4.7, 7.2", "R_A <= .125 < .126 = B input cap", ".125",
        "0.8% below the B input cap .126", "shrinks A records, more A records needed",
        "would break the B input range check", "justified (tight)")
    print()
    print("=== C. seed radius R = .032 and its enlargement .0320001 (2.4, A.3) ===")
    print(f"  R_s = 2*pi*.0320001 = {2 * math.pi * 0.0320001:.6f} < .203:"
          f" slack {0.203 - 2 * math.pi * 0.0320001:.6f} ({100 * (0.203 / (2 * math.pi * 0.0320001) - 1):.2f}%)")
    print(f"  so the A-stage frame bound allows R <= .203/(2pi) = {0.203 / (2 * math.pi):.7f}")
    print(f"  the fresh-centre inequality needs 3/(2N) <= R: at N=112, 3/224 = {3 / 224:.6f}"
          f" -> R/that = {0.032 / (3 / 224):.3f}x")
    print(f"  the enlargement 1e-7 vs the established seed-phase error 1e-14: ratio {1e-7 / 1e-14:.0f}")
    row("R = .032", "2.4, 2.10", "3/(2N) <= R <= .203/(2*pi) = .0323092", ".032",
        "2.39x above the lower end, 0.96% below the upper end", "N>=47 needed: at R=.016 no N works (3/(2N)<=.016 needs N>=94, still allowed)",
        "R=.064: 2*pi*.064=.402 > .203, breaks A.4's frame bound", "justified (upper end is tight)")
    row("R = .0320001", "2.4, A.3", "covers the 1e-14 phase-rounding error and stays under .0323092",
        ".0320001", "1e-7 vs 1e-14: 1e7x", "irrelevant", "2*pi*.0320002 = .2010627 < .203 still ok",
        "justified")
    rn2 = (0.032 * 112) ** 2
    print(f"  reuse threshold (fl(.032*112))^2 - 1e-4 = {rn2:.6f} - 1e-4 = {rn2 - 1e-4:.6f}")
    print(f"  effective radius sqrt(that)/112 = {math.sqrt(rn2 - 1e-4) / 112:.7f}"
          f"  ({100 * (math.sqrt(rn2 - 1e-4) / 112 / 0.032 - 1):.4f}% below R)")
    print(f"  1e-4 vs the established float error 1e-12: ratio {1e-4 / 1e-12:.0f}")
    row("reuse threshold (NR)^2 - 1e-4", "2.4, A.3", "success iff bound < (NR)^2 - 1e-4", "12.844956",
        "1e-4 vs 1e-12 float error: 1e8x; costs 0.0044% of the ball radius", "5e-5: still >> error",
        "2e-4: still >> error", "justified")
    print()
    print("=== D. the free parameters: beta in Lemma 4.11, the iteration caps ===")
    for b in (0.25, 0.45, 0.5, 0.8, 0.9):
        print(f"  beta={b}: seed factor 1+beta={1 + b:.3f}, error factor 1+1/beta={1 + 1 / b:.3f},"
              f" product of the two = {(1 + b) * (1 + 1 / b):.3f}")
    row("beta = .45 (direct bound)", "4.5, A.7", "Gl >= (1+b)R_s^2 AA* + (1+1/b)E^2 BB*, any b in (0,1)",
        ".45", "bound value 1.45 R_s^2 < .06, far from binding", "b=.225: 1+1/b = 5.44, weaker bound",
        "b=.9: 1.9 R_s^2 still small", "arbitrary-but-harmless (free parameter of an ellipsoid split)")
    row("beta = .8 (weighted bound)", "4.5", "same, no sine-error term", ".8",
        "1+1/.8 = 2.25, weakest of the two factors", "b=.4: 3.5x weaker on the error term",
        "b=1.6 not allowed (b<=1)", "arbitrary-but-harmless")
    row("30 bootstrap updates", "4.6, 4.13", "each update is an upper bound; the count is effort only",
        "30", "no convergence assertion is used", "15: more cells fail -> subdivision",
        "60: more work, same certificate", "arbitrary-but-harmless")
    row("25 midpoint trials", "5.2", "one stored successful trial is the certificate", "25",
        "no monotonicity of D-hat is needed", "12: more relations decline",
        "50: more work", "arbitrary-but-harmless")
    row("q_d < 3.8", "4.8", "q_d < 4 is needed for sqrt(1-q_d/4); amplification (1-q/4)^(-1/2)",
        "3.8", f"1-q/4 = {1 - 3.8 / 4:.3f} > .049 as stated; amplification {1 / math.sqrt(1 - 3.8 / 4):.2f}",
        "1.9: amplification 1.34, but rejects more cells (slower)",
        "7.6 > 4: the bound has no real square root -> unsound", "justified (pole at 4)")
    row("eigenvalue split .64", "4.2, Prop 4.6", "proposal threshold only; the certificate checks T*T-I <= ort",
        ".64", "accepted T columns have sigma >= 1-1e-5, so >= .36 above the threshold; no stated bound on the normal side",
        ".32: more T columns proposed, >10 causes failure -> subdivision",
        "1.28: no T columns at all, k=0, coverage fails -> subdivision", "arbitrary-but-harmless (performance only)")
    row("K = 1.00001", "6.1, (6.3), (A.17)", "K > ||T|| = sqrt(1+ort) with ort < 1e-5",
        "1.00001", "sqrt(1+1e-5) = 1.000005, so 5e-6 above the need (a factor 2)",
        "1.000005: exactly at the boundary, any rounding fails",
        "1.00002: 4x the excess, still harmless", "justified (tight to a factor 2)")
    row("divisor skip 1e-6 in extend", "2.3, A.3", "skipping a divisor only removes a constraint (conservative)",
        "1e-6", "accepted divisors > .999e-6 give endpoint error < 1e-7 vs the 1e-5 margin: 100x",
        "5e-7: still conservative", "2e-6: more constraints dropped, still conservative",
        "justified")
    print()
    print("=== E. the closing table of Appendix A: error, margin, ratio ===")
    table = [
        ("seed gap / direct support", 1e-14, 1e-8),
        ("seed direct support", 1e-11, 1e-8),
        ("shared-coordinate numerator", 3.5e-11, 1e-7),
        ("shared-coordinate endpoints", 1e-7, 1e-5),
        ("seed dual support", 1e-4, 0.01),
        ("A flat norm", 1e-6, 1e-5),
        ("A directional comparison", 4e-6, 1e-4),
        ("Root identity Frobenius", 5e-8, 2e-6),
        ("Root orthogonal check", 1e-10, 1e-8),
        ("Root horizontal check", 1e-11, 1e-8),
        ("tensor transformed row bound", 1e-6, 2e-4),
        ("Candidate direct support", 2e-6, 1e-4),
        ("Candidate external tangent (rad)", 1.2e-4, 1.5e-4),
        ("first G entry error", 1e-11, 1e-7),
        ("second G entry error", 1e-9, 1e-7),
        ("spectral row-sum bound", 3e-13, 1e-10),
        ("spectral fourth-norm bound", 1e-10, 2e-7),
        ("bootstrap update", 1e-12, 1e-8),
        ("B projected normal", 5e-11, 1e-8),
        ("B local update", 1e-13, 1e-8),
        ("B cross-Gram spectral", 2e-9, 1e-7),
        ("C direct comparison", 1e-9, 2e-7),
        ("C directional comparison", 1e-9, 2e-7),
        ("C joint support", 1e-8, 3e-7),
    ]
    mrows = []
    print(f"  {'path':36s} {'error':>10s} {'margin':>10s} {'ratio':>8s}  thinnest?")
    thin = min(table, key=lambda t: t[2] / t[1])
    for name, err, mar in table:
        mrows.append(dict(path=name, error=err, margin=mar, ratio=mar / err,
                          thinnest=(name == thin[0])))
        print(f"  {name:36s} {err:10.1e} {mar:10.1e} {mar / err:8.1f}"
              f"  {'<-- thinnest' if name == thin[0] else ''}")
    print(f"\n  thinnest margin in the table: {thin[0]}, ratio {thin[2] / thin[1]:.2f}")
    print("  (everything else is 1.5 to 1e6 times the error it covers)")
    with open("work/05-parameters/data/constants.csv", "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wtr.writeheader()
        wtr.writerows(rows)
    with open("work/05-parameters/data/margins.csv", "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=list(mrows[0].keys()))
        wtr.writeheader()
        wtr.writerows(mrows)


if __name__ == "__main__":
    main()
