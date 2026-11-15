#!/usr/bin/env python3
"""The admissible band for the seed-cover bin count N, and its cost.

Everything here is exact integer arithmetic except where a float is flagged.

Constraints on N found in the paper (section, statement):
  (C1) C(N+4,5) < 2^31              s7.3 "The former bound is below the signed
                                    32-bit limit" (tuple counter is int32)
  (C2) 3/(2N) <= R = .032           s2.4 "Retaining u as a center would cover the
                                    entire bin with radius 3/(2N) < 0.032"
  (C3) N-1 <= 127                   s7.3 "All bin differences lie between -111 and
                                    111 ... the stored five-coordinate differences
                                    also fit the signed eight-bit type"
  (C4) (NR)^2 > 4.25 (soft)         the coordinatewise reuse bound (2.18) certifies a
                                    nonzero integer offset k only when
                                    (NR)^2 > ||k||^2 + 9/4 + sum|k_j|, minimised
                                    over nonzero integer k at 4.25.

Run: python3 experiments/n_band.py
"""
from math import comb
from itertools import combinations_with_replacement
import os

LIM32 = 2 ** 31
LIM8 = 127
R = 0.032


def c5(N):
    """Weakly increasing 5-tuples from [0,N): the X bin lists of s2.2."""
    return comb(N + 4, 5)


def c4(N):
    """Weakly increasing 4-tuples: the Y tails for one fixed shared bin."""
    return comb(N + 3, 4)


def t1(N):
    """#{a<=b<=c<=d<=l<N : a <= l-d+1}: the integral orientation filter (2.7).

    Derivation: fix (a,d).  The condition is a <= l-d+1 <=> l >= a+d-1, so l
    ranges over [max(d,a+d-1), N-1]; for each such l the pair (b,c) ranges over
    weakly increasing pairs in [a,d], i.e. comb(d-a+2,2) choices.  Sum.
    """
    tot = 0
    for a in range(N):
        for d in range(a, N):
            lo = max(d, a + d - 1)
            if lo < N:
                tot += (N - lo) * comb(d - a + 2, 2)
    return tot


def t1_closed(N):
    """Same count, l-first: fix (a,l), put D = min(l, l-a+1); the weakly
    increasing triple (b,c,d) in [a,D] has comb(D-a+3,3) choices."""
    tot = 0
    for a in range(N):
        for l in range(a, N):
            D = min(l, l - a + 1)
            if D >= a:
                tot += comb(D - a + 3, 3)
    return tot


def t1_brute(N):
    tot = 0
    for a, b, c, d, l in combinations_with_replacement(range(N), 5):
        if a <= l - d + 1:
            tot += 1
    return tot


def lattice_ball(r, dim=9, kmax=6):
    """#{k in Z^dim : |k_j| <= kmax, ||k|| <= r}: the integer offsets the reuse
    test can reach when the comparison radius is NR."""
    r2 = r * r
    vals = list(range(-kmax, kmax + 1))

    def rec(i, s):
        if i == dim:
            return 1
        n = 0
        for v in vals:
            s2 = s + v * v
            if s2 <= r2:
                n += rec(i + 1, s2)
        return n

    return rec(0, 0.0)


def main():
    print("=== 0. the two counts the paper quotes (s7.3) ===")
    assert c5(112) == 160_389_488, c5(112)
    assert c4(112) == 6_913_340, c4(112)
    print(f"  C(116,5) = {c5(112):,}   C(115,4) = {c4(112):,}   both reproduce")

    print("\n=== 1. (C1) signed 32-bit window: largest N with C(N+4,5) < 2^31 ===")
    n1 = max(N for N in range(1, 400) if c5(N) < LIM32)
    print(f"  N = {n1}: C({n1 + 4},5) = {c5(n1):,}  < 2^31 = {LIM32:,}")
    print(f"  N = {n1 + 1}: C({n1 + 5},5) = {c5(n1 + 1):,}  exceeds it by "
          f"{c5(n1 + 1) - LIM32:,}")
    print(f"  so (C1) alone gives N <= {n1}")

    print("\n=== 2. (C2) fresh-centre window: 3/(2N) <= R ===")
    nmin = 1.5 / R
    print(f"  3/(2R) = {nmin:.6f}  ->  N >= {int(nmin) + 1}")
    print(f"  at N = {int(nmin)}: 3/(2N) = {1.5 / int(nmin):.6f} > .032  (violates)")
    print(f"  at N = {int(nmin) + 1}: 3/(2N) = {1.5 / (int(nmin) + 1):.6f} <= .032")

    print("\n=== 3. (C3) signed eight-bit window: N-1 <= 127 ===")
    print(f"  N <= {LIM8 + 1}; at N=112 the largest bin difference is 111")
    print(f"  headroom 127-111 = {LIM8 - 111} bin units = "
          f"{(LIM8 - 111) / 111:.3f} of the observed range")

    print("\n=== 4. (C4) reuse geometry: reachable integer offsets ||k|| <= NR ===")
    print("   N      NR      #{k in Z^9: ||k||<=NR}     (NR)^2")
    for N in (47, 56, 64, 80, 96, 112, 128, 160, 189):
        nr = N * R
        nl = lattice_ball(nr) if nr <= 6 else None
        print(f"  {N:4d} {nr:8.4f}   {('%-22d' % nl) if nl is not None else '>1e6':<22} {nr * nr:9.4f}")
    print("  (the column counts lattice points inside the reach; the coordinatewise")
    print("   bound (2.18) additionally needs ||k||^2 + sum|k_j| <= (NR)^2 - 9/4, whose")
    print("   minimum over nonzero k is 2, so it can fire at all only when (NR)^2 > 4.25,")
    print("   i.e. N >= 65.  Below that every bin is retained as a fresh centre.)")

    print("\n=== 5. cost curve (exact) ===")
    print("  %4s %14s %12s %20s %20s %10s"
          % ("N", "C(N+4,5)", "C(N+3,4)", "T1(N) 2.7-survivors",
             "N*C(N+3,4) tail cap", "ratio/112"))
    base = c5(112)
    for N in (47, 56, 64, 80, 96, 112, 128, 160, 189):
        print("  %4d %14d %12d %20d %20d %10.4f"
              % (N, c5(N), c4(N), t1(N), N * c4(N), c5(N) / base))

    print("\n=== 6. the orientation filter (2.7) and Table 1 of s7.5 ===")
    for N in range(3, 10):
        assert t1(N) == t1_closed(N) == t1_brute(N), N
    print("  the two formulas agree with brute force for N = 3..9")
    T112 = t1(112)
    print(f"  T1(112) = {T112:,}  =  {100 * T112 / base:.2f}% of C(116,5)")
    print(f"  Table 1 of s7.5 reports 151,744,086 'pairs processed'.")
    print(f"  151,744,086 - T1(112) = {151_744_086 - T112:,}; the ratio is "
          f"{151_744_086 / T112:.4f}.")
    print("  No count stated in s2.2-s2.3 reproduces 151,744,086: it is not")
    print("  C(116,5), not T1(112), not 112*C(115,4) and not a multiple of any of")
    print("  them.  It is 94.63% of C(116,5), so it cannot be the orientation")
    print("  filter alone, which removes 46.79%.  OPEN ITEM for T8/T9.")
    print(f"  the vanishing-sum filter leaves 22,829 X lists "
          f"({100 * 22_829 / T112:.5f}% of the (2.7) survivors).")

    print("\n=== 7. retained centres: the measured point and its scaling ===")
    print("  recorded: 160,389,488 tuples -> 151,744,086 filter survivors")
    print("            -> 22,829 X lists -> 249,878 centres")
    print(f"  bins per retained centre     : {base / 249_878:.2f}")
    print(f"  centres per surviving X list : {249_878 / 22_829:.2f}")
    print(f"  A-stage cost per centre      : {2020.32 / 249_878 * 1e3:.2f} ms")
    print(f"  if every bin needed its own centre at N=112: "
          f"{base / 249_878:.0f}x more A work = "
          f"{2020.32 * base / 249_878 / 3600:.1f} h")

    print("\n=== 8. cost of moving N by one grid step ===")
    for a, b in ((48, 64), (64, 80), (80, 96), (96, 112), (112, 128), (112, 160)):
        print(f"  C({b + 4},5)/C({a + 4},5) = {c5(b) / c5(a):7.3f}"
              f"   (N {a} -> {b})")

    os.makedirs("data", exist_ok=True)
    with open("data/n_band.csv", "w") as f:
        f.write("N,C_Nplus4_5,C_Nplus3_4,T1_N,N_times_C_Nplus3_4,NR,"
                "ratio_to_112,lattice_pts_within_NR\n")
        for N in (47, 56, 64, 80, 96, 112, 128, 160, 189):
            nr = N * R
            nl = lattice_ball(nr) if nr <= 6 else ""
            f.write(f"{N},{c5(N)},{c4(N)},{t1(N)},{N * c4(N)},{nr:.6f},"
                    f"{c5(N) / base:.6f},{nl}\n")
    print("\nwrote data/n_band.csv")


if __name__ == "__main__":
    main()
