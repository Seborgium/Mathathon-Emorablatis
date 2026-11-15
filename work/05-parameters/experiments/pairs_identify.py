#!/usr/bin/env python3
"""What is the paper's '151,744,086 pairs' of the seed cover (Table 1, section 7.5)?

Candidate readings of the enumeration count for N=112 bins:
  A  all weakly increasing 5-bin X tuples                     C(116,5)
  B  the integral orientation filter (2.7): a <= l-d+1
  C  the midpoint gap filter (2.8) first inequality:
        max{(a+1/2)/N, (b-a)/N, (c-b)/N, (d-c)/N, (l-d)/N, 1-(l+1/2)/N} <= 1-(l-1)/N
  D  B and C together
Counts are exact integer sums; C is evaluated with integer arithmetic
(M = N-l+1 = floor(N*(1-(l-1)/N))).

Run: python3 experiments/pairs_identify.py
"""
from math import comb

PAPER = 151_744_086


def count_all(n):
    return comb(n + 4, 5)


def count_orientation(n):
    """a <= l-d+1."""
    total = 0
    for l in range(n):
        for d in range(l + 1):
            amax = min(d, l - d + 1)
            for a in range(amax + 1):
                total += comb(d - a + 2, 2)
    return total


def count_gapfilter(n):
    """Six-gap test with integer threshold M = n-l+1.

    Constraints (all gaps <= M/n, gaps scaled by n):
        a+1/2 <= M, b-a <= M, c-b <= M, d-c <= M, l-d <= M, n-(l+1/2) <= M.
    The last is automatic.  a+1/2 <= M  <=>  a <= M-1 for integer a.
    """
    total = 0
    for l in range(n):
        M = n - l + 1
        for d in range(l + 1):
            if l - d > M:
                continue
            # number of a in [0, M-1] with a <= b and b-a <= M, summed over b<=c<=d
            for c in range(d + 1):
                if d - c > M:
                    continue
                for b in range(c + 1):
                    if c - b > M:
                        continue
                    lo = max(0, b - M)
                    hi = min(b, M - 1, d)
                    if hi >= lo:
                        total += hi - lo + 1
    return total


def count_both(n):
    total = 0
    for l in range(n):
        M = n - l + 1
        for d in range(l + 1):
            if l - d > M:
                continue
            for c in range(d + 1):
                if d - c > M:
                    continue
                for b in range(c + 1):
                    if c - b > M:
                        continue
                    lo = max(0, b - M)
                    hi = min(b, M - 1, d, l - d + 1 + 0)  # orientation: a <= l-d+1
                    hi = min(hi, l - d + 1)
                    if hi >= lo:
                        total += hi - lo + 1
    return total


def brute_gap(n):
    from itertools import combinations_with_replacement
    c = 0
    for (a, b, cc, d, l) in combinations_with_replacement(range(n), 5):
        g = max((a + 0.5) / n, (b - a) / n, (cc - b) / n, (d - cc) / n,
                (l - d) / n, 1 - (l + 0.5) / n)
        if g <= 1 - (l - 1) / n + 1e-12:
            c += 1
    return c


def main():
    n = 112
    for small in (4, 5, 6, 7):
        assert count_gapfilter(small) == brute_gap(small), small
    print("count_gapfilter agrees with a float brute force for N = 4..7")
    print()
    A = count_all(n)
    B = count_orientation(n)
    C = count_gapfilter(n)
    D = count_both(n)
    print(f"N = {n}")
    print(f"  A all tuples                         {A:>13,}")
    print(f"  B orientation filter (2.7) only      {B:>13,}")
    print(f"  C midpoint gap filter (2.8) only     {C:>13,}")
    print(f"  D both filters                       {D:>13,}")
    print(f"  paper Table 1 'pairs processed'      {PAPER:>13,}")
    print()
    for name, v in (("A", A), ("B", B), ("C", C), ("D", D)):
        print(f"  {name}: difference from paper = {v - PAPER:+,}")
    print()
    print("For comparison, the same four counts at other N:")
    print("   N        A           B           C           D")
    for nn in (16, 24, 32, 47, 56, 64, 80, 96, 112):
        print(f"  {nn:3d} {count_all(nn):>12,} {count_orientation(nn):>12,}"
              f" {count_gapfilter(nn):>12,} {count_both(nn):>12,}")


if __name__ == "__main__":
    main()
