#!/usr/bin/env python3
"""The seed-ball radius R = .032, the A-stage enlargement .0320001, and the
reuse threshold (fl(fl(.032*112))^2) - 1e-4 of s2.4 / A.3.

Run: python3 experiments/seed_ball.py
"""
from fractions import Fraction as F

N = 112
R = F(32, 1000)                 # 0.032 exactly, as a rational
R_BIG = F(320001, 10000000)     # 0.0320001


def main():
    print("=== 1. the inequality that fixes R: a fresh midpoint covers its bin ===")
    print("   ||h||_2 <= sqrt(9)/(2N) = 3/(2N)   (h in [-1/2,1/2]^9, s2.4)")
    for n in (46, 47, 64, 96, 112, 128, 189):
        v = F(3, 2 * n)
        print(f"   N={n:4d}: 3/(2N) = {float(v):.6f}  R/that = {float(R / v):6.3f}"
              f"  {'OK' if v <= R else 'VIOLATES'}")
    v112 = F(3, 224)
    print(f"   at N=112: 3/(2N) = {float(v112):.6f}, slack R - 3/(2N) = "
          f"{float(R - v112):.6f} ({100 * float((R - v112) / R):.2f}% of R)")
    print("   so the bin argument uses only "
          f"{100 * float(v112 / R):.2f}% of the radius; R is not tuned to N=112.")
    print("   R = .032 is exactly 32/1000, a 3-digit decimal; 2*R = .064 = 64/1000,")
    print("   and .032 = 1/31.25 is not a dyadic rational.")
    print(f"   note: 1.5/R = {1.5 / 0.032:.5f}; the next integer 47 is the hard floor.")

    print("\n=== 2. the enlargement to .0320001 ===")
    d = R_BIG - R
    print(f"   .0320001 - .032 = {float(d):.7f} = 1e-7")
    print("   established error: the nine stored binary midpoint phases differ from")
    print("   their rational midpoints in norm by less than 1e-14 (s2.4 proof, A.3).")
    print(f"   margin / error = 1e-7 / 1e-14 = {1e-7 / 1e-14:.0f}")
    print("   so the enlargement is 1e7 times the error it must dominate.")
    for cand in (1e-8, 1e-9, 1e-15):
        print(f"   a smaller enlargement {cand:g} would still dominate 1e-14: "
              f"{cand > 1e-14}")
    print("   halving to .03200005: still 5e-8 >> 1e-14, no effect on anything.")
    print("   removing it (R=.032 exactly): UNSOUND, the seed phases are rounded.")
    print(f"   2*pi*.0320001 = {2 * 3.141592653589793 * 0.0320001:.5f} < .203 (A.4 "
          "uses .203 for R_s)")

    print("\n=== 3. the reuse threshold RN2 = fl((fl(.032*112))^2) - .0001 (A.3) ===")
    a = 0.032 * N
    b = a * a
    rn2 = b - 1e-4
    exact = float(R * N) ** 2
    print(f"   fl(.032*112) = {a!r}")
    print(f"   fl(that^2)   = {b!r}    exact (.032*112)^2 = {exact!r}")
    print(f"   RN2          = {rn2!r}")
    print(f"   RN2 / (NR)^2 = {rn2 / exact:.12f}   ({(1 - rn2 / exact):.3e} lost)")
    print(f"   effective radius sqrt(RN2)/112 = {(rn2 ** 0.5) / N:.9f}"
          f"  vs R = .032")
    print(f"   the threshold is (NR)^2 - 1e-4 with NR = {a:.4f}")
    print("   error budget: 'the total possible error before the subtraction is")
    print("   below 1e-12' (A.3) -> margin/error = 1e-4/1e-12 = 1e8.")
    for eps in (1e-6, 1e-8, 1e-10, 0.0):
        r = (b - eps) ** 0.5 / N
        print(f"   eps={eps:<8g} -> effective radius {r:.9f} "
              f"({(1 - r / 0.032) * 100:.6f}% below .032)")
    print("   1e-8 would still be 1e4 above the established error; the .0001 choice")
    print("   costs 3.9e-6 of relative radius, i.e. nothing.  Verdict: justified,")
    print("   eight orders over-conservative.")

    print("\n=== 4. cost of R: covering count scales as R^-5 ===")
    print("   the seed set is 5-dimensional (9 phase coordinates - 4 real equations)")
    print("   and the measured run retained 249,878 centres at R=.032.")
    for f in (0.5, 1.0, 2.0):
        rr = 0.032 * f
        n = 249_878 * (1 / f) ** 5
        print(f"   R -> {rr:.4f} ({f:g}x): estimated centres {n:,.0f},"
              f" A time {2020.32 * n / 249_878 / 60:.1f} min (measured 33.7 min at R=.032)")
    print("   halving R also forces N >= 3/(2*.016) = 94 for the bin argument,")
    print("   and doubling R makes the bin argument trivial (N >= 24) but the seed")
    print("   balls coarser, so Stage A must cover more U(2) cells per seed.")


if __name__ == "__main__":
    main()
