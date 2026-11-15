#!/usr/bin/env python3
"""The nine resource caps against the recorded run, and every margin in the
closing table of Appendix A.

Recorded run (s7.5 Table 1 and s7.3): 160,389,488 tuples before filtering;
249,878 retained seed centres out of 22,829 surviving X lists; A 4x62,470 = 249,878
inputs -> 764+774+757+788 = 3,083 records, 0 unresolved; B mid 3,083 -> 600;
B fine 600 -> 22,379 in 88 batches of <=256; initial C 22,379 -> 163 failures,
all of them graph caps, no bin overflow, no clustering failure; B fallback
163 -> 1,127; final C 1,127 -> 0.  Wall times: cover 621.59 s, A 2020.32 s,
B mid 1071.49 s, B fine 407.45 s, C initial 300.23 s, fallback 8.12 s,
final C 36.27 s, total 4470.33 s.

Run: python3 experiments/caps_margins.py
"""
import math

CAPS = [
    # name, cap, largest value the recorded run can have reached, source
    ("Stage A extra nodes", 1_000_000, 0, "no unresolved seed in any shard (s7.5)"),
    ("Stage B grid boxes", 50_000_000, 6_436_343, "largest admissible box count, mid pass"),
    ("atlas Roots", 2_000_000, 788, "largest single A shard output (788)"),
    ("Stage C phase bins", 2_000_000, None, "no bin overflow in 22,379 records"),
    ("clusters per record", 2_048, None, "no clustering failure in 22,379 records"),
    ("graph steps", 5_000_000, 5_000_000, "163 cap hits, all initial C failures"),
    ("records per file", 2_000_000, 22_379, "fine.bin; batches are 256"),
    ("concatenated inputs", 8_000_000, 3_083, "coarse0-3 -> B mid"),
    ("subdivision depth", 6, 6, "2^6 children; no unresolved box reported"),
]

MARGINS = [
    ("seed gap / direct support", 1e-14, 1e-8),
    ("seed direct support", 1e-11, 1e-8),
    ("shared-coordinate numerator", 3.5e-11, 1e-7),
    ("shared-coordinate endpoints", 1e-7, 1e-5),
    ("seed dual support", 1e-4, 0.01),
    ("A flat norm", 1e-6, 1e-5),
    ("A directional comparison", 4e-6, 1e-4),
    ("Root identity Frobenius check", 5e-8, 2e-6),
    ("Root orthogonal check", 1e-10, 1e-8),
    ("Root horizontal check", 1e-11, 1e-8),
    ("tensor transformed row bound", 1e-6, 2e-4),
    ("Candidate direct support", 2e-6, 1e-4),
    ("Candidate external tangent error (rad)", 1.2e-4, 1.5e-4),
    ("G entry error, first choice", 1e-11, 1e-7),
    ("G entry error, second choice", 1e-9, 1e-7),
    ("spectral row-sum bound", 3e-13, 1e-10),
    ("spectral fourth-norm bound", 1e-10, 2e-7),
    ("bootstrap update", 1e-12, 1e-8),
    ("B projected normal / local update", 5e-11, 1e-8),
    ("B local update (A.9)", 1e-13, 1e-8),
    ("B cross-Gram spectral perturbation", 2e-9, 1e-7),
    ("C direct / directional comparison", 1e-9, 2e-7),
    ("C joint support", 1e-8, 3e-7),
]


def main():
    print("=== 1. the nine caps: is each binding, and how close did we get? ===")
    print("  %-24s %12s %14s %10s  %s" % ("cap", "limit", "max reached", "use", "note"))
    for name, cap, got, note in CAPS:
        if got is None:
            print(f"  {name:<24}{cap:>12,} {'not reported':>14} {'?':>10}  {note}")
        elif got == 0:
            print(f"  {name:<24}{cap:>12,} {0:>14,} {0.0:>9.2%}  {note}")
        else:
            print(f"  {name:<24}{cap:>12,} {got:>14,} {got / cap:>9.4%}  {note}")

    print("\n  verdicts:")
    print("   * graph steps: the ONLY cap the recorded run actually hit - 163 times,")
    print("     every one of the 163 initial-C failures.  Raising it would remove the")
    print("     fallback stage (8.12 s + 36.27 s = 1.0% of the 4470 s run); lowering")
    print("     it multiplies unresolved records.  It is doing real work.")
    print("   * Stage A nodes: not hit as a failure, but 64^4/8 = 2,097,152 cells per")
    print("     seed exceeds 1e6, so from grid 64 the cap forbids enumeration and the")
    print("     phase-ball cover must fire.  The cap is structural, not incidental.")
    print("   * Stage B boxes: not hit, and cannot be: 23^5 = 6,436,343 is only 12.9%")
    print("     of 5e7.  The cap does not bind; it is what DEFINES k_max = 5.")
    print("   * 2048 clusters: needs a 121.5:1 compression of the 248,832 first-grid")
    print("     bins (2,000,000/2048 = 976:1 at the 2e6 bin cap).  No failure means")
    print("     the achieved ratio was enough, but the ratio is not reported.")
    print("   * 2e6 and 8e6 (records, concatenation) are 3 to 4 orders of magnitude")
    print("     above anything the run needed: they are safety rails, not design.")
    print("   * depth 6: exactly the level at which the 16 -> 512 grid chain stops")
    print("     (five doublings) plus one for the B box split.")

    print("\n=== 2. every margin in the closing table of Appendix A, ranked ===")
    rank = sorted(MARGINS, key=lambda t: t[2] / t[1])
    print("  %-42s %10s %10s %10s" % ("path", "error", "margin", "ratio"))
    for name, err, mar in rank:
        print(f"  {name:<42}{err:>10.1e} {mar:>10.1e} {mar / err:>10.1f}")
    print("\n  the three tightest, and what each would take to break:")
    for name, err, mar in rank[:3]:
        print(f"   * {name}: ratio {mar / err:.2f}; an error under-estimate of "
              f"{100 * (1 - err / mar):.0f}% breaks the chain.")
    print("  the tangent margin .00015 vs .00012 radians is the binding numerical")
    print("  inequality of the whole proof: it is the only ratio below 3, and it")
    print("  sits inside the bootstrap (4.38) that sets every Record radius.")
    lo = rank[0]
    print(f"  for scale: the median ratio is "
          f"{sorted(m / e for _, e, m in MARGINS)[len(MARGINS) // 2]:.0f} and the")
    print("  largest is 1e6.  A single number for the paper's numerical risk is")
    print(f"  therefore {lo[2] / lo[1]:.2f}, not 1e6.")

    print("\n=== 3. what a 'safety factor' claim would need ===")
    print("  a chain's total safety factor is the product of its ratios only if the")
    print("  errors add; they do not, they are each dominated independently.  The")
    print("  correct summary is the minimum, and the minimum is the tangent margin.")
    for f in (0.5, 1.0, 2.0):
        print(f"  scaling every margin by {f:g}: the tightest ratio becomes "
              f"{lo[2] / lo[1] * f:.2f}"
              f" ({'breaks' if f < lo[1] / lo[2] else 'holds'})")

    print("\n=== 4. wall-time cost of the caps actually in play ===")
    tot = 4470.33
    stages = [("seed cover", 621.59), ("A (4 shards)", 2020.32),
              ("B mid", 1071.49), ("B fine", 407.45), ("C initial", 300.23),
              ("B fallback", 8.12), ("C final", 36.27)]
    for n, t in stages:
        print(f"   {n:<14}{t:>9.2f} s  {100 * t / tot:6.2f}%")
    print(f"   {'total':<14}{tot:>9.2f} s")
    print("   the two passes that exist only because of the graph cap cost 44.4 s,")
    print("   i.e. 1.0%; the cap is cheap.  Doubling it would have saved ~1% and")
    print("   removed the only stage in the run that needed a second attempt.")
    print("   B mid alone is 24% of the run: that is the tau=.07 / w=.013 pass, so")
    print("   the coarse pass, not the fine one, is where the time goes.")

    import os
    os.makedirs("data", exist_ok=True)
    with open("data/caps.csv", "w") as fh:
        fh.write("cap,limit,max_reached_in_recorded_run,utilisation,note\n")
        for name, cap, got, note in CAPS:
            u = "" if got is None else (f"{got / cap:.6f}" if got else "0")
            fh.write(f"\"{name}\",{cap},{'' if got is None else got},{u},"
                     f"\"{note}\"\n")
    with open("data/margins.csv", "w") as fh:
        fh.write("path,established_error,margin,ratio\n")
        for name, err, mar in sorted(MARGINS, key=lambda t: t[2] / t[1]):
            fh.write(f"\"{name}\",{err:.3e},{mar:.3e},{mar / err:.4f}\n")
    print("\nwrote data/caps.csv and data/margins.csv")


if __name__ == "__main__":
    main()
