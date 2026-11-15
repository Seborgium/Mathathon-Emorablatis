#!/usr/bin/env python3
"""The nine resource caps: is each binding, and what is the largest value it can
have reached in the recorded run?  Constants from Sec. 3.7, 6, 7.2, 7.3 and
Table 1 of Sec. 7.5.   Run: python3 experiments/caps.py
"""
from math import comb, ceil
import csv

print("== A. Stage A: 1,000,000 extra nodes, deeper-node cap")
for Nu in (16, 32, 64, 128, 256, 512):
    cells = Nu**4//8                       # bin counts Nu/2 * Nu/4 * Nu * Nu
    print("  Nu=%3d  cells/seed=Nu^4/8=%12d  over 1e6? %s" % (Nu, cells, cells > 10**6))
print("  -> the cap binds for every seed that needs enumeration at Nu>=64 (F5).")
print("     Recorded: A shards processed 62,470/62,470/62,469/62,469 centres with")
print("     0 unresolved, so no seed hit the cap; the per-seed maximum is NOT reported (F6).")

print("\n== B. Stage B: 50,000,000 boxes, depth 6")
for (name, w, Rin) in (("mid", 0.013, 0.125), ("fine", 0.005, 0.07), ("fallback", 0.0038, 0.016)):
    E = Rin + 1e-7
    L = ceil(E/w + 0.500001)
    n = 2*L+1
    kmax = 1
    while n**(kmax+1) <= 5*10**7:
        kmax += 1
    print("  %-8s w=%.4f Rin=%.3f  E/w=%.3f  L=%4d  boxes/axis=%4d  max k with n^k<=5e7: %d"
          % (name, w, Rin, E/w, L, n, kmax))
    print("           largest admissible box count n^k = %d (%.1f%% of the cap); k+1 would be %d (%.1fx over)"
          % (n**kmax, 100*n**kmax/5e7, n**(kmax+1), n**(kmax+1)/5e7))
print("  depth 6: total nodes of a fully split tree = sum_{j<=6} 2^(jk)")
for k in range(0, 7):
    t = sum(2**(j*k) for j in range(7))
    print("    k=%d: %15d boxes  under 5e7? %s" % (k, t, t <= 5e7))

print("\n== C. Atlas Roots 2,000,000 per seed")
print("  recorded: 249,878 seed centres -> 3083 coarse records (Table 1)")
print("  per-seed atlas size is not reported (F6); 0 unresolved/0 failed seeds implies < 2e6.")

print("\n== D/E. C: 2,000,000 bins, 8,000,000 concatenated inputs, 2048 clusters")
print("  first C grid 12^5 = %d (%.1f%% of the 2e6 bin cap)" % (12**5, 100*12**5/2e6))
print("  each retained bin is split into 2^5 = 32 children")
print("  32 * 12^5 = %d <= 8e6 = %d  (headroom %.2f%%)"
      % (32*12**5, 8*10**6, 100*(1-32*12**5/8e6)))
print("  if the 8e6 input cap is applied to those children, retained bins <= 8e6/32 = %d,"
      % (8*10**6//32))
print("  which is 1/8 of the stated 2,000,000 bin cap: the two caps cannot both be reached.")
print("  2048 clusters: needs a compression of bins/2048; at 12^5 that is %.0f:1" % (12**5/2048))

print("\n== F. 5,000,000 graph steps")
print("  recorded: 163 of 22,379 initial C records hit the cap; all 15 bad files")
print("  accounted for; final C had 0.  Largest value reached = 5,000,000 exactly, 163 times.")
print("  fraction of records capped: %.3f%%" % (100*163/22379))

print("\n== G. 2,000,000 records per file")
print("  batch writer: 87*256+107 = %d (= 22,379), so the largest file holds 256 records."
      % (87*256+107))
print("  the 2e6 cap is 2e6/256 = %.0f times the batch size: unreachable for batch files." % (2e6/256))

print("\n== H. 8,000,000 concatenated inputs")
print("  B mid: 3083 coarse records; B fine: 600; fallback: 163; C: batches of <=256.")
print("  largest actual concatenation = 3083 (0.04%% of the cap).")

print("\n== I. depth 6")
print("  a box splits into 2^k children, so depth 6 needs 2^(6k) leaves; see the table under B.")

rows = [("Stage A extra nodes", 10**6, "per seed", "no (0 unresolved)", "not reported"),
        ("Stage B boxes", 5*10**7, "per parent", "no (0 bad parents)", "<= 28,629,151 at k=5, pass 2"),
        ("Atlas Roots", 2*10**6, "per seed", "no (0 failed seeds)", "not reported"),
        ("C bins", 2*10**6, "per record", "no", "<= 250,000 by the 8e6 cap"),
        ("clusters", 2048, "per record", "no (no clustering failures)", "not reported"),
        ("graph steps", 5*10**6, "per record", "YES (163 records)", "5,000,000 x163"),
        ("records per file", 2*10**6, "per file", "no", "256 (batch writer)"),
        ("concatenated inputs", 8*10**6, "per invocation", "no", "3083 (B mid)"),
        ("depth", 6, "per box", "no", "not reported")]
with open("data/m5-caps.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["cap", "value", "scope", "binding_in_recorded_run", "largest_reached"])
    w.writerows(rows)
print("\nwrote data/m5-caps.csv")
