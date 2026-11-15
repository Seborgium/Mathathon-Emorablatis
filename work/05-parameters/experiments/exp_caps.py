#!/usr/bin/env python3
"""Every resource cap: is it binding in the recorded run, and what is the largest value reached?

Evidence used: section 7.3 (the caps), section 7.5/Table 1 (the run), section 5.6 (grid, atlas,
file limits), section 6.3 (bins, centres), A.8/A.9 (local scale bounds).
Where the paper reports no counter (finding F6) the largest value is bounded from above by
"the cap was not hit" and, where possible, estimated from the measured wall time; estimates are
labelled EST and carry their assumption.
"""
import csv, os
from math import ceil, log2

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
# Table 1 (section 7.5)
SEEDS, PAIRS, CENTRES, XLISTS = 249_878, 151_744_086, 249_878, 22_829
A_REC = 3083; BMID, BFINE, CAPC, BFB = 600, 22_379, 163, 1127
COVER_S, A_S, CMID_S, CFINE_S, FB_S = 621.59, 2020.32, 1071.49, 407.45, 8.12
CINIT_S, CFINAL_S = 300.23, 36.27

rows = []
def row(cap, where, observed, evidence, binding, half, double):
    rows.append(dict(cap=cap, where=where, observed_max=observed, evidence=evidence,
                     binding=binding, at_half=half, at_double=double))

print("=" * 78)
print("1. caps with a reported counter")
print("=" * 78)
print(f"graph steps 5,000,000: {CAPC} of {BFINE} initial C records hit it "
      f"({100*CAPC/BFINE:.2f}%): THE ONLY CAP THAT BINDS.")
print(f"   after the fallback (tau .016 -> .011) all 163 resolved into {BFB} records.")
print(f"   cost of the whole fallback: {FB_S} s + {CFINAL_S} s = {FB_S+CFINAL_S:.2f} s "
      f"= {100*(FB_S+CFINAL_S)/4470.33:.2f}% of the 4470.33 s pipeline.")
row("5,000,000 graph steps", "section 6.6 / 7.2 crun", "5,000,000 (163 records)",
    "Table 1: 163 unresolved, all graph caps", "YES",
    "2.5e6: more cap hits, larger fallback; soundness unaffected (cap -> unresolved, never negative)",
    "1e7: probably resolves all 163 directly; saves 44.4 s of 4470 s = 1.0%")
row("256 records per batch file", "section 5.6", "256 (87 full batches + 107)",
    "87*256+107 = 22,379", "YES (by construction)",
    "128: 175 files instead of 88", "512: 44 files")
row("2,000,000 records per file", "section 5.6", f"{BFINE:,} (fine.bin)",
    f"87*256+107 = {BFINE:,}", "no", f"1e6: still {100*BFINE/1e6:.1f}% used", "4e6: no effect")
row("8,000,000 concatenated inputs", "section 5.6", f"{BFINE:,} (initial C input)",
    f"largest concatenation = {BFINE:,}; final C = {BFB:,}", "no",
    "4e6: 0.6% used", "1.6e7: no effect")
row("2,000,000 atlas Roots", "section 5.6 / 4.7", f"{A_REC:,} (764+774+757+788)",
    "Table 1 A0..A3 outputs", "no",
    f"1e6: {100*A_REC/1e6:.2f}% used", f"4e6: no effect")
row("2,000,000 C bins", "section 6.3 / 7.3", "not reported; < 2e6",
    "no initial bin overflow (7.5)", "no (but unmeasured)",
    "1e6: only matters if retained bins/record > 1e6", "4e6: no effect")
row("2048 clusters", "section 6.3 / 7.3", "not reported; <= 2048",
    "no clustering failures (7.5)", "unknown - plausibly near",
    "1024: would trip if a record has >1024 bins at M=24 (see exp_stagec_cutoff)",
    "4096: only helps if F2's degenerate cutoff is left in place")

print()
print("=" * 78)
print("2. caps with no reported counter: bounded from the run")
print("=" * 78)
# Stage A nodes: throughput argument
core_seconds = A_S * 4
print(f"1,000,000 extra nodes (Stage A): zero unresolved A records => never reached.")
print(f"   {SEEDS:,} seeds in {A_S} s over 4 shards = {core_seconds:.0f} core-s")
print(f"   => {core_seconds/SEEDS*1e6:.1f} microseconds of Stage A per seed.")
for cost_us in (1000, 100, 10, 1):
    est = core_seconds / (cost_us * 1e-6) / SEEDS
    print(f"   EST if one node costs {cost_us:>4} us: {est:10,.0f} nodes/seed "
          f"({100*est/1e6:5.2f}% of cap)")
print("   => the node cap is not binding at any plausible node cost; it is 2-3 orders of magnitude")
print("      away.  Halving it to 5e5 changes nothing; doubling it to 2e6 gains nothing either,")
print("      because the grid at Nu=64 already needs 2,097,152 cell tests.")
row("1,000,000 extra nodes (A)", "section 3.7 / 7.3", "not reported; << 1e6 (EST 1e3-3e4/seed)",
    "zero unresolved A; throughput bound", "no",
    "5e5: no change (EST)", "2e6: no change -- grid 64 still needs 2,097,152 cell tests")
row("50,000,000 boxes (B)", "section 5.6", "at most 28,629,151 (pass 2, k=5)",
    "L=23/31/11 with k<=5 => 23^5, 31^5=57.3% of cap", "no, but within 1.75x",
    "2.5e7: pass-2 k=5 (31^5=28,629,151) FAILS => bad parents", "1e8: no k gain (31^6=8.9e8)")
row("depth 6", "section 5.6", "<= 5 (no depth-limit parent failures)",
    "a depth-limit hit fails the parent; zero bad parents", "no",
    "3: tau_1 needs 3 levels (tau/w = 5.38) => borderline", "12: pointless; needed levels are 3,2,2")

print()
print("=" * 78)
print("3. largest grid the caps and widths permit")
print("=" * 78)
for i, (L, w_, tau) in enumerate([(11, .013, .07), (15, .005, .016), (5, .0038, .011)]):
    ax = 2 * L + 1
    print(f"  pass {i+1}: 2L+1={ax:2d}, k<=5 gives {ax**5:>11,}; k=6 gives {ax**6:>13,}"
          f" ({'FAIL' if ax**6>5e7 else 'ok'}), k=10 gives {ax**10:>19,} "
          f"({'FAIL' if ax**10>5e7 else 'ok'})")
print("  so at the three widths used the allowance is k <= 5, 5, 7.  CORRECTION: it is NOT true that")
print("  k <= 10 is unreachable at every admissible width -- with w = .05 and a small-radius record")
print("  (E ~ .016) one gets L = 1 and 3^10 = 59,049 <= 5e7, so k = 10 is admissible.  The narrow")
print("  statement (the three specified widths) is the correct one.")

print()
print("=" * 78)
print("4. B-stage counter arithmetic")
print("=" * 78)
print(f"  B mid: {A_REC} parents -> {BMID} records; B fine: {BMID} -> {BFINE}"
      f" ({BFINE/BMID:.1f} children per parent)")
print(f"  fallback: {CAPC} parents -> {BFB} records ({BFB/CAPC:.2f} per parent)")
print(f"  final C partition {282*3+281} = {282*3+281} (paper 1127)")
print(f"  A shards: 62,470+62,470+62,469+62,469 = {62470*2+62469*2:,} (paper) vs {CENTRES:,} centres")
print(f"  total pipeline 4470.33 s; A is {100*A_S/4470.33:.1f}%, B {100*(CMID_S+CFINE_S)/4470.33:.1f}%,"
      f" C {100*(CINIT_S+FB_S+CFINAL_S)/4470.33:.1f}%, cover {100*COVER_S/4470.33:.1f}%")

os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, "caps.csv"), "w", newline="") as fh:
    w_ = csv.DictWriter(fh, fieldnames=list(rows[0])); w_.writeheader(); w_.writerows(rows)
print(f"\nwrote {os.path.join(DATA,'caps.csv')}")
