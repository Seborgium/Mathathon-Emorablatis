#!/usr/bin/env python3
"""Counting audit of the seed cover (Sec. 2.2-2.4, Prop. 2.10): does the stated
enumeration explain the recorded pair count?

The paper states (Sec. 2.3) that seeds::build "visits every weakly increasing
five-bin X tuple and applies (2.7), the first inequality in (2.8), and sumok",
and that "[s]eparately, for every possible first bin it visits all weakly
increasing four-bin Y tails".  Table 1 reports 151,744,086 pairs.
Run: python3 experiments/seedcover.py
"""
from math import comb
import csv

N = 112
def gapmid(a, b, c, d, l):
    """eq. (2.8) midpoint gap of the X list, in units of 1/N"""
    return max(a + 0.5, b - a, c - b, d - c, l - d, N - l - 0.5)

def counts(N):
    tot = ori = ori_gap = 0
    for l in range(N):
        for d in range(l + 1):
            for a in range(d + 1):
                m = d - a
                nb = (m + 1)*(m + 2)//2          # number of (b,c) with a<=b<=c<=d
                tot += nb
                if a <= l - d + 1:               # eq. (2.7) orientation filter
                    ori += nb
    # with both (2.7) and the (2.8) X midpoint-gap filter, per (a,d,l)
    for l in range(N):
        for d in range(l + 1):
            for a in range(min(d, l - d + 1) + 1):
                ok = 0
                for b in range(a, d + 1):
                    for c in range(b, d + 1):
                        if gapmid(a, b, c, d, l) <= N - l + 1:
                            ok += 1
                ori_gap += ok
    return tot, ori, ori_gap

tot, ori, ori_gap = counts(N)
print("== the X side (Sec. 2.3)")
print("all weakly increasing 5-bin tuples, C(%d,5)          = %d" % (N+4, tot))
print("satisfying the orientation filter (2.7), a<=l-d+1   = %d  (%.1f%%)" % (ori, 100*ori/tot))
print("also satisfying the (2.8) X midpoint-gap filter     = %d  (%.1f%%)" % (ori_gap, 100*ori_gap/tot))
print("Table 1 'pairs'                                     = 151744086  (%.1f%% of C(116,5))"
      % (100*151744086/tot))
print("=> a filter list that includes (2.7) cannot leave 151,744,086 pairs:")
print("   the orientation filter alone leaves at most %d." % ori)

print("\n== the Y side (Sec. 2.3, last line of 7.3)")
print("tails for one fixed shared bin, C(%d,4) = %d" % (N+3, comb(N+3, 4)))
print("shared bins = N = %d, so the Y enumeration is N*C(N+3,4) = %d tail tests"
      % (N, N*comb(N+3, 4)))
print("ratio Y-side / X-side = %.3f ; Table 1 reports neither" % (N*comb(N+3, 4)/tot))

print("\n== what a 'pair' has to be")
print("X tuples offered to the filters      %d" % tot)
print("X tuples surviving (2.7)             %d" % ori)
print("Y tail tests                         %d" % (N*comb(N+3, 4)))
print("so 'pair' is either an X tuple (max %d) or a matched (X,Y) pair" % tot)
print("(>= the tail count when the matching is total).  151,744,086 fits neither.")

print("\n== the count the paper does justify")
print("C(116,5) = %d < 2^31 = %d : true, and the largest such N is 189."
      % (comb(116, 5), 2**31))
print("but Sec. 7.3 also stores bin differences in int8_t, which caps N at 128.")

with open("data/m5-seedcover-counts.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["quantity", "value"])
    for k, v in [("C(N+4,5) all X tuples", tot),
                 ("X tuples satisfying (2.7)", ori),
                 ("X tuples satisfying (2.7)+(2.8)", ori_gap),
                 ("Table 1 pairs", 151744086),
                 ("C(N+3,4) tails per shared bin", comb(N+3, 4)),
                 ("N*C(N+3,4) tail tests", N*comb(N+3, 4))]:
        w.writerow([k, v])
print("\nwrote data/m5-seedcover-counts.csv")
