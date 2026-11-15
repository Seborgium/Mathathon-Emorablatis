#!/usr/bin/env python3
"""The ten resource caps: limit, the largest value the recorded run can have reached,
whether the cap binds, and the arithmetic of the bound.

Run: python3 experiments/caps_table.py
"""
import csv
import math

# recorded run, paper table 1 (section 7.5)
SEEDS_TOTAL = 249_878
A_RECORDS = 764 + 774 + 757 + 788
SEEDS_PER_SHARD = [62_470, 62_470, 62_469, 62_469]
B_MID_IN = 3083
B_MID_OUT = 600
B_FINE_OUT = 22_379
C_INIT_IN = 22_379
C_INIT_CAP_HITS = 163
B_FALL_IN = 163
B_FALL_OUT = 1127
TOTAL_INVOCATIONS = 100


def main():
    rows = []

    def add(cap, stage, limit, largest, binding, note):
        rows.append(dict(cap=cap, stage=stage, limit=limit, largest_possible_or_reached=largest,
                         binding=binding, note=note))

    # 1. Stage A extra nodes
    grid64 = 64 ** 4 // 8
    add("extra nodes", "A", 1_000_000, "unreported; <= %d cells at grid 64 per seed" % grid64,
        "no (no unresolved seed)",
        "the base grid at Nu=64 has 2,097,152 cells > the cap, so coverage must fire there")
    # 2. Stage B boxes
    boxes = {23: 23 ** 5, 31: 31 ** 5, 11: 11 ** 7}
    add("boxes per parent", "B", 50_000_000, "%d (pass 2, k=5)" % boxes[31],
        "no", "57.3% of the cap; k=6 in pass 1 would need 148,035,889 > cap")
    # 3. atlas Roots
    add("atlas Roots", "A", 2_000_000, f"{A_RECORDS:,} records", "no", f"0.15% of cap, slack {2e6 / A_RECORDS:.0f}x")
    # 4. C bins
    add("retained C bins", "C", 2_000_000, "unreported (first grid 248,832 = 12.4% of cap)",
        "no (no bin overflow stated)", "32 children per retained bin, so >62,500 parents could bind")
    # 5. clusters
    add("cluster centres", "C", 2048, "unreported; synthetic M=24 model reaches 1626",
        "no (no clustering failure stated)", "79% of cap in the synthetic model -> the thinnest cap")
    # 6. graph steps
    add("graph steps", "C", 5_000_000, f"{C_INIT_CAP_HITS} records hit it exactly", "YES (163 records)",
        "0.73% of the 22,379 initial C records; resolved by B fallback + final C")
    # 7. records per file
    add("records per file", "A/B/C", 2_000_000, f"{max(B_FINE_OUT, A_RECORDS, SEEDS_TOTAL):,}", "no",
        f"largest file is fine.bin at 22,379 records: {100 * B_FINE_OUT / 2e6:.2f}% of cap")
    # 8. concatenated inputs
    add("concatenated inputs", "B/C", 8_000_000, f"{max(C_INIT_CAP_HITS, B_FINE_OUT, SEEDS_TOTAL):,}", "no",
        "the largest concatenation is fine.bin (22,379) or ALL_NON_EMPTY_C_BAD_FILES (163)")
    # 9. depth
    add("subdivision depth", "B", 6, "unreported; no unresolved box", "no",
        "radius chain .125 -> .07 -> .016 -> .011 shrinks by >= 1.45 per pass")
    # 10. Root dimension
    add("Root dimension k", "A/B", 10, "<= 5 in passes 1-2, <= 7 in pass 3 (box cap)", "YES (box cap)",
        "see boxes_k.py: the stated allowance is unreachable")

    print(f"{'cap':22s} {'stage':6s} {'limit':>12s} {'largest':>52s} {'binding':>10s}")
    for r in rows:
        print(f"{r['cap']:22s} {r['stage']:6s} {r['limit']:>12,}"
              f" {r['largest_possible_or_reached']:>52s} {r['binding']:>10s}")
    print()
    print("=== cross-checks of the recorded counts (paper table 1) ===")
    print(f"  seeds {SEEDS_PER_SHARD} sum to {sum(SEEDS_PER_SHARD):,} = recorded {SEEDS_TOTAL:,}:"
          f" {sum(SEEDS_PER_SHARD) == SEEDS_TOTAL}")
    print(f"  A records 764+774+757+788 = {A_RECORDS} (paper: 3083)")
    print(f"  fine.bin batches 87*256+107 = {87 * 256 + 107:,} = recorded {B_FINE_OUT:,}")
    print(f"  final C partition 282*3+281 = {282 * 3 + 281:,} = recorded 1127")
    print(f"  initial C failures 163 = sum of the fifteen bad files (paper)")
    print(f"  invocations 1 + 4 + 2 + 88 + 1 + 4 = {1 + 4 + 2 + 88 + 1 + 4} = recorded {TOTAL_INVOCATIONS}")
    print()
    print("=== wall-clock shares of the recorded run (section 7.5) ===")
    times = [("seed cover", 621.59), ("A (4 parallel shards)", 2020.32), ("B mid", 1071.49),
             ("B fine", 407.45), ("initial C", 300.23), ("B fallback", 8.12), ("final C", 36.27)]
    tot = 4470.33
    s = 0.0
    for n, t in times:
        s += t
        print(f"  {n:24s} {t:9.2f} s  {100 * t / tot:5.1f}%")
    print(f"  sum of stages {s:.2f} s vs the supervisor's {tot:.2f} s (polling/validation overhead"
          f" {tot - s:.2f} s)")
    with open("work/05-parameters/data/caps.csv", "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wtr.writeheader()
        wtr.writerows(rows)


if __name__ == "__main__":
    main()
