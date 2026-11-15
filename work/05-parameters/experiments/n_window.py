#!/usr/bin/env python3
"""Counts that the seed cover of the paper (sections 2.2-2.3, 7.3) depends on.

Independent verification of:
  * C(n,5) style pre-filter tuple counts quoted in section 7.3;
  * the signed-32-bit window for the bin count N;
  * the fresh-centre window for N from the paper's own sentence
    "Retaining u as a center would cover the entire bin with radius 3/(2N) < 0.032";
  * T1(N) = #{weakly increasing 5-bin X tuples satisfying the integral orientation
    filter (2.7), i.e. a <= l-d+1} -- compared with the paper's
    "Seed cover ... 151,744,086 pairs" in Table 1 of section 7.5.

Run: python3 experiments/n_window.py
"""
from math import comb

LIM32 = 2 ** 31


def weakly_inc_5(n):
    """Number of weakly increasing 5-tuples with entries in [0,n)."""
    return comb(n + 4, 5)


def weakly_inc_4(n):
    return comb(n + 3, 4)


def t1_formula(n):
    """#{a<=b<=c<=d<=l<n : a <= l-d+1} by exact summation.

    For fixed (a,d,l) the number of (b,c) with a<=b<=c<=d is comb(d-a+2,2).
    """
    total = 0
    for l in range(n):
        for d in range(l + 1):
            amax = min(d, l - d + 1)
            for a in range(amax + 1):
                m = d - a + 2
                total += comb(m, 2)
    return total


def t1_bruteforce(n):
    from itertools import combinations_with_replacement
    total = 0
    for t in combinations_with_replacement(range(n), 5):
        a, b, c, d, l = t
        if a <= l - d + 1:
            total += 1
    return total


def main():
    print("=== 1. pre-filter tuple counts quoted in section 7.3 ===")
    print(f"C(116,5) = {comb(116,5):,}   (paper: 160,389,488)")
    print(f"C(115,4) = {comb(115,4):,}   (paper:   6,913,340)")
    print(f"112*C(115,4) = {112 * comb(115,4):,}  (Y-tail enumeration per full pass)")
    print()

    print("=== 2. the signed-32-bit window on N (C(N+4,5) < 2**31) ===")
    nmax32 = max(n for n in range(1, 400) if weakly_inc_5(n) < LIM32)
    print(f"largest N with C(N+4,5) < 2^31 : N = {nmax32}, C(N+4,5) = {weakly_inc_5(nmax32):,}")
    n1 = nmax32 + 1
    print(f"first failing N              : N = {n1}, C(N+4,5) = {weakly_inc_5(n1):,}")
    print(f"signed 32-bit limit          : {LIM32:,}")
    print()

    print("=== 3. tuple-count growth C(N+4,5) (the enumeration cost) ===")
    for n in (32, 46, 47, 48, 56, 64, 80, 96, 112, 128, 160, 189, 224):
        v = weakly_inc_5(n)
        print(f"  N={n:4d}  C(N+4,5)={v:>15,}   C(N+3,4)={weakly_inc_4(n):>12,}"
              f"   ratio to N=112: {v / weakly_inc_5(112):7.3f}")
    print()

    print("=== 4. the fresh-centre window on N (3/(2N) <= R) ===")
    for R in (0.032, 0.0320001):
        nmin = 1.5 / R
        print(f"  R = {R}: need N >= 3/(2R) = {nmin:.6f}  -> N >= {int(nmin) + 1} (integer)")
        for n in (46, 47, 56, 112, 189, 224):
            print(f"     N={n:4d}: fresh-centre radius 3/(2N) = {1.5 / n:.6f}"
                  f"   ratio to R = {1.5 / n / R:.4f}")
        print()
    print("  the two windows combined from 32-bit arithmetic: 47 <= N <= %d" % nmax32)
    print()
    print("=== 4b. the signed-8-bit (int8_t) window: section 7.3 and A.3 ===")
    print("  section 7.3: 'All bin differences lie between -111 and 111; ... The stored")
    print("  five-coordinate differences also fit the signed eight-bit type used by the cover.'")
    print("  Bin differences a-b with a,b in [0,N-1] range over [-(N-1), N-1].")
    print("  int8_t holds [-128, 127], so N-1 <= 127, i.e. N <= 128.")
    for n in (112, 127, 128, 129, 189):
        print(f"    N={n:4d}: max difference {n-1:3d}  fits int8: {n-1 <= 127}"
              f"   headroom to 127: {127-(n-1)}")
    print("  N = 128 is the largest admissible N; the 32-bit bound (189) is dominated by it.")
    print("  the combined window from the paper's own types: 47 <= N <= 128")
    print()

    print("=== 5. the 'pairs processed' count of Table 1 (151,744,086) ===")
    for n in range(3, 10):
        f, b = t1_formula(n), t1_bruteforce(n)
        assert f == b, (n, f, b)
    print("  t1_formula agrees with brute force for N = 3..9")
    v112 = t1_formula(112)
    print(f"  T1(112) = {v112:,}   paper Table 1: 151,744,086   match = {v112 == 151_744_086}")
    print(f"  T1(112)/C(116,5) = {v112 / comb(116,5):.6f}"
          f"  (orientation filter alone removes {100 * (1 - v112 / comb(116,5)):.2f}% of tuples)")
    print()

    print("=== 6. T1(N) and the tuple total as functions of N ===")
    print("   N     T1(N)          C(N+4,5)       T1/C")
    for n in (32, 47, 56, 64, 80, 96, 112, 128, 160, 189):
        t = t1_formula(n)
        c = weakly_inc_5(n)
        print(f"  {n:4d}  {t:>13,}  {c:>13,}   {t / c:.6f}")
    print()

    print("=== 7. gap-filter arithmetic (2.8): thresholds 1-(l-1)/N and 1-(l+2)/N ===")
    for n in (47, 64, 112, 189):
        print(f"  N={n:4d}: threshold separation = 3/N = {3 / n:.6f}"
              f"   vs Lemma 2.5 perturbation w = 1/N = {1 / n:.6f}"
              f"   ratio = {(3 / n) / (1 / n):.1f}")


if __name__ == "__main__":
    main()
