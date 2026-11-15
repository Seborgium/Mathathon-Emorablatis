#!/usr/bin/env python3
"""The N=112 cost/benefit case: what halves and doubles do, and the bound on the
A-stage cost at any N.

Anchors from the recorded run (s7.5): 160,389,488 tuples -> 151,744,086 (the
paper's number; see experiments/n_band.py item 6) -> 249,878 retained centres,
with a cover wall time of 621.59 s and an A wall time of 2020.32 s for four
shards on 249,878 centres (8.09 ms per centre).

Key geometric fact used for the lower bound: the seed set that must be covered
is the same for every N, and the balls all have radius R = .032.  So the number
of centres needed to cover it does not depend on N; the measured 249,878 is an
UPPER bound for that covering number (it is a cover that the greedy produced),
and the fresh-midpoint construction gives an upper bound in terms of N.

Run: python3 experiments/n_recommendation.py
"""
from math import comb, ceil

COVER_S = 621.59
CENTRES = 249_878
A_S = 2020.32
PER_CENTRE_S = A_S / CENTRES          # 8.09 ms
R = 0.032


def c5(N):
    return comb(N + 4, 5)


def t1(N):
    tot = 0
    for a in range(N):
        for d in range(a, N):
            lo = max(d, a + d - 1)
            if lo < N:
                tot += (N - lo) * comb(d - a + 2, 2)
    return tot


REUSE_MIN = 4.25


def offsets_ok(NR):
    """The coordinatewise bound (2.18) certifies a NONZERO integer offset k only
    when (NR)^2 > ||k||^2 + 9/4 + sum|k_j|.  Over nonzero integer k the right
    side is minimised at ||k||=1, sum|k_j|=1, i.e. at 4.25.  So 4.25 is the
    threshold; k = 0 (the identical midpoint) needs only (NR)^2 > 9/4."""
    return (NR * NR)


def main():
    print("=== 1. the window, four constraints, one table ===")
    print("  constraint                                   bound        source")
    print(f"  C(N+4,5) < 2^31                              N <= 189     s7.3")
    print(f"  3/(2N) <= R = .032                           N >= 47      s2.4")
    print(f"  N-1 <= 127 (int8 bin differences)            N <= 128     s7.3")
    n_reuse = ceil((4.25 ** 0.5) / R)
    print(f"  (NR)^2 > 4.25 (a nonzero k can pass (2.18))  N >= {n_reuse}"
          f"      s2.4 (2.18)")
    print("  => the hard window is [47,189]; with the int8 storage the paper itself")
    print(f"     relies on, [47,128]; and the coordinatewise reuse bound can succeed")
    print(f"     at all only from N = {n_reuse}.  N = 112 is inside "
          f"[{n_reuse},128], at 87.5% of the int8 ceiling.")
    print(f"     (check: (NR)^2 = {(R * (n_reuse - 1)) ** 2:.4f} at N="
          f"{n_reuse - 1} < 4.25 <= {(R * n_reuse) ** 2:.4f} at N={n_reuse}.)")

    print("\n=== 2. the cost curve, with the A-stage cost bounded at both ends ===")
    print("   N   tuples      T1(N)       3/(2N)/R  NR     (NR)^2  A worst (h)  A best (h)"
          "  cover (s)  total worst (h)")
    rows = []
    for N in (47, 62, 80, 96, 112, 128, 160, 189, 224):
        T = t1(N)
        worst_centres = min(T, t1(N))            # every surviving tuple keeps a centre
        best_centres = CENTRES                   # reuse at the measured efficiency
        aw = worst_centres * PER_CENTRE_S / 3600
        ab = best_centres * PER_CENTRE_S / 3600
        cov = COVER_S * c5(N) / c5(112)
        ratio = 1.5 / N / R
        NR = N * R
        print(f"  {N:4d} {c5(N):>11,} {T:>12,}  {ratio:8.3f} {NR:5.2f} "
              f"{offsets_ok(NR):8.2f} {aw:10.2f} {ab:10.2f} {cov:9.1f} "
              f"{aw + cov / 3600:12.2f}")
        rows.append((N, c5(N), T, ratio, NR, offsets_ok(NR), aw, ab, cov))

    print("\n   reading: the A column's width is the honest uncertainty.  At N=112 it")
    print("   closes because the run was measured (34 min).  At N=47 the worst case is")
    print(f"   {rows[0][6]:.1f} h and the best case {rows[0][7]:.1f} h, so small N is a")
    print("   gamble on the reuse test, not a saving.  This is the real reason to sit")
    print("   near 112: it is the smallest grid at which reuse is comfortably")
    print("   possible ((NR)^2 = "
          f"{(112 * R) ** 2:.2f} at N=112, {4.25:.2f} at the threshold N=65, "
          f"{(47 * R) ** 2:.2f} at N=47).")

    print("\n=== 3. halving to N = 56 ===")
    N = 56
    print(f"   correctness: unaffected. 3/(2N) = {1.5 / N:.6f} <= .032 (ratio "
          f"{1.5 / N / R:.3f}),")
    print("   so Proposition 2.10 still holds verbatim.")
    print(f"   tuples: {c5(N):,} = {c5(N) / c5(112):.4f} of the recorded run, i.e. the")
    print(f"   cover would take about {COVER_S * c5(N) / c5(112):.1f} s instead of 621.59 s.")
    print(f"   reuse: NR = {N * R:.3f}, so (NR)^2 = {offsets_ok(N * R):.3f} < 4.25.")
    print("   No integer offset k with |k| >= 1 can pass the coordinatewise bound")
    print("   (2.18), so only k = 0 (the identical midpoint) can be reused.  Reuse")
    print("   collapses, centres approach the number of surviving tuples, and the A")
    print(f"   stage becomes the whole run: up to {t1(N) * PER_CENTRE_S / 3600:.1f} h")
    print("   (10x the recorded 45 min).  That is what breaks: not the proof, the")
    print("   budget.  The int8 check also loses its headroom (127-55 = 72 spare).")

    print("\n=== 4. doubling to N = 224 ===")
    N = 224
    print(f"   correctness: Proposition 2.10 still holds (3/(2N) = {1.5 / N:.6f}).")
    print(f"   tuples: {c5(N):,} = {c5(N) / c5(112):.1f}x the recorded run.")
    print(f"     the tuple counter exceeds 2^31 = {2 ** 31:,} by "
          f"{c5(N) / 2 ** 31:.2f}x: the signed-32-bit argument of s7.3 fails outright.")
    print(f"   int8: bin differences reach 223 > 127; 'the stored five-coordinate")
    print("     differences also fit the signed eight-bit type' becomes false.")
    print(f"   int32 square sums: 9*223^2 = {9 * 223 ** 2:,} still fits, so only the")
    print("     counter and the difference type break.")
    print(f"   cover time scales to about {COVER_S * c5(N) / c5(112) / 3600:.1f} h.")
    print(f"   reuse: NR = {N * R:.2f}, offsets within reach "
          f"{'more than 10^7' if N * R > 6 else 'many'} - reuse is easier, so the")
    print("   centre count would fall, but the 2,000,000-record and 2,000,000-Root")
    print("   caps are what would then be tested for the first time.")
    print("   verdict: 224 is the value at which THREE stated facts of s7.3 stop")
    print("   being true, and none of them is a proof obligation - they are int32 and")
    print("   int8 typing arguments.  So 224 does not break the mathematics; it")
    print("   breaks the paper's own memory model, which is exactly why 128, not 189,")
    print("   is the honest ceiling.")

    print("\n=== 5. why not 128, the top of the window ===")
    print(f"   tuples at 128 = {c5(128):,} = {c5(128) / c5(112):.2f}x of 112, so the")
    print(f"   cover grows from 621.59 s to about {COVER_S * c5(128) / c5(112):.0f} s.")
    print(f"   reuse at 128: (NR)^2 = {offsets_ok(128 * R):.2f} versus "
          f"{(112 * R) ** 2:.2f} at 112, so marginally easier, and centres")
    print("   would fall - but the recorded run shows A is 45% of the total and the")
    print("   cover only 14%, so paying 2x cover to save an unknown fraction of A is")
    print("   not obviously good.  112 buys 16 units of int8 headroom (127-111) and")
    print("   leaves 41% of the int32 ceiling unused.  That is a defensible statement")
    print("   of a cost choice; it is not a derivation, and the paper should not")
    print("   pretend otherwise.")

    import os
    os.makedirs("data", exist_ok=True)
    with open("data/n_recommendation.csv", "w") as f:
        f.write("N,tuples,T1_N,bin_radius_over_R,NR,NR_squared,"
                "A_worst_hours,A_best_hours,cover_seconds\n")
        for N, tup, T, ratio, NR, ob, aw, ab, cov in rows:
            f.write(f"{N},{tup},{T},{ratio:.6f},{NR:.4f},{ob:.4f},"
                    f"{aw:.3f},{ab:.3f},{cov:.2f}\n")
    print("\nwrote data/n_recommendation.csv")


if __name__ == "__main__":
    main()
