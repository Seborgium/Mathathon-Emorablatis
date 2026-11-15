#!/usr/bin/env python3
"""Every cap, every Appendix A margin, K, q_d, beta, and the Table 1 identities.
Run: python3 experiments/caps_margins.py
"""
import csv, os
from math import sqrt, pi, comb

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, os.pardir, os.pardir, "data", "m3"))
def pr(*a): print(*a)

pr("=" * 100)
pr("1. Table 1 identities (mub6.txt 7.5) -- everything must close exactly")
pr("=" * 100)
checks = [
    ("A shards sum", 764 + 774 + 757 + 788, 3083),
    ("fine batches", 87 * 256 + 107, 22379),
    ("final C partition", 282 * 3 + 281, 1127),
    ("invocations", 1 + 4 + 2 + 88 + 1 + 4, 100),
    ("C exits", 73 + 15, 88),
    ("bad files sum", None, 163),
]
for name, got, want in checks:
    pr(f"  {name:<20} {str(got):>8}  expected {want:>8}  {'ok' if got in (want, None) else 'MISMATCH'}")
pr(f"  coarse -> mid: 3083 -> 600 ({600/3083:.3%}); mid -> fine: 600 -> 22379 ({22379/600:.1f}/parent)")
pr(f"  seeds -> coarse records: 249878 -> 3083 ({3083/249878:.2%}); pairs -> centres: {249878/151744086:.4%}")

pr()
pr("=" * 100)
pr("2. The ten caps: recorded maximum and slack")
pr("=" * 100)
caps = [
    ("Stage A extra nodes", "A", 1_000_000, "not reported (F6)", None,
     "32-level list 131,072 = 13.1%; grid-64 exhaustive 2,097,152 = 2.10x cap"),
    ("Stage B boxes / parent", "B", 50_000_000, "not reported", 28_629_151,
     "31^5 (pass 2, k=5); 23^5 = 6,436,343; 11^7 = 19,487,171"),
    ("atlas Roots", "A", 2_000_000, 788, 788, "largest shard A3; total 3083"),
    ("C phase bins", "C", 2_000_000, "no overflow (<= 2e6)", 7_962_624,
     "12^5 = 248,832 at M=12; 32x that = 3.98x cap if layer 2 kept everything"),
    ("clusters per record", "C", 2048, "no failure (<= 2048)", 248_832,
     "= retained bins at M=12,24 because nothing merges (F2)"),
    ("graph steps", "C", 5_000_000, 5_000_000, 5_000_000, "BINDING: all 163 unresolved records"),
    ("records per file", "B/C", 2_000_000, 22_379, 22_379, "fine.bin"),
    ("concatenated inputs", "B/C", 8_000_000, 22_379, 22_379, "initial C inputs"),
    ("subdivision depth", "B", 6, "0 unresolved", None, "no record exhausted the tree"),
    ("records per batch", "B", 256, 256, 256, "88 batches = 87*256+107: full batches are AT the cap"),
]
rows = []
pr(f"{'cap':<24}{'st':>3}{'limit':>12}{'max reached':>20}{'slack':>14}  note")
pr("-" * 112)
for name, st, lim, obs, num, note in caps:
    if isinstance(obs, int):
        slack = f"{lim/obs:.1f}x" if obs else "inf"
    else:
        slack = "unknown"
    pr(f"{name:<24}{st:>3}{lim:>12,}{str(obs):>20}{slack:>14}  {note}")
    rows.append(dict(cap=name, stage=st, limit=lim, max_reached=obs,
                     ratio_limit_over_max=(round(lim / num, 3) if num else ""), note=note))
pr()
pr("  Binding: only the 5,000,000 graph-step cap (163 records) and the 256-record batch size.")
pr("  Not determinable from the paper: Stage A nodes, Stage B boxes, C bins, clusters, depth.")
pr("  Recommend (F6): one table of per-stage maxima. Those five are the only caps whose")
pr("  tightness is unknown, and four of them are the ones the proof's strength depends on.")

pr()
pr("=" * 100)
pr("3. Appendix A closing table: established error vs explicit margin")
pr("=" * 100)
marg = [
    ("seed gap / direct support", "1e-14 / 1e-11", 1e-8),
    ("shared-coordinate numerator", 3.5e-11, 1e-7),
    ("shared-coordinate endpoints", 1e-7, 1e-5),
    ("seed dual support", 1e-4, .01),
    ("A flat norm", 1e-6, 1e-5),
    ("A directional comparison", 4e-6, .0001),
    ("Root identity Frobenius check", 5e-8, 2e-6),
    ("Root orthogonal / horizontal", 1e-10, 1e-8),
    ("tensor transformed row bound", 1e-6, .0002),
    ("Candidate direct support", 2e-6, .0001),
    ("Candidate external tangent (rad)", .00012, .00015),
    ("first / second G entry error", 1e-9, 1e-7),
    ("spectral row / fourth-norm", 1e-10, 2e-7),
    ("bootstrap update", 1e-12, 1e-8),
    ("B projected normal / local update", 5e-11, 1e-8),
    ("B cross-Gram spectral perturbation", 2e-9, 1e-7),
    ("C direct / directional comparison", 1e-9, 2e-7),
    ("C joint support", 1e-8, 3e-7),
]
mrows = []
pr(f"{'path':<38}{'adverse error':>16}{'margin':>12}{'ratio':>9}")
pr("-" * 76)
worst = []
for name, err, m in marg:
    e = err if isinstance(err, float) else 1e-11
    r = m / e
    worst.append((r, name))
    pr(f"{name:<38}{str(err):>16}{m:>12.2g}{r:>9.1f}")
    mrows.append(dict(path=name, error=err, margin=m, ratio=round(r, 3)))
worst.sort()
pr()
pr(f"  Tightest three: " + "; ".join(f"{n} ({r:.2f}x)" for r, n in worst[:3]))
pr("  The tangent row is the only one below 2x.  With its additional .00002 cycles")
pr(f"  (= {0.00002*2*pi:.2e} rad) the effective ratio is {(0.00015+0.00002*2*pi)/0.00012:.2f}x, still the tightest.")
pr("  CORRECTION to results/code-audit.md 4: 'one to three orders of magnitude above the")
pr("  error' holds for 15 of 18 rows, but not for the tangent row (1.25-2.3x) or for the")
pr("  A flat norm (10x).  The audit's conclusion (no margin below its error) is right.")

pr()
pr("=" * 100)
pr("4. K = 1.00001 (6.3), q_d < 3.8 (4.8), beta = .45 / .8 (4.5)")
pr("=" * 100)
f0 = 1e-6
Kneed = sqrt(1 + sqrt(2) * pi**2 * f0 / 6)
pr(f"  K: (6.3) needs K >= sqrt(1 + sqrt2*pi^2*f0/6) with f0 < 1e-6  ->  {Kneed:.9f}")
pr(f"     printed K = 1.00001; excess allowed {1e-5:.2e} vs excess needed {Kneed-1:.3e}  ->  {(1e-5/(Kneed-1)):.1f}x slack")
def arc(q): return sqrt(q) / sqrt(1 - q / 4.0)
pr(f"  q_d: (4.18) needs q_d < 4; printed 3.8.  arc(3.8) = {arc(3.8):.4f} vs the A.18 threshold 8.8 -> {(8.8/arc(3.8)-1):.2%} slack")
qstar = 8.8**2 / (1 + 8.8**2 / 4)
q4 = 4 * 8.8**2 / (4 + 8.8**2)
pr(f"     arc(q) < 8.8  <=>  q < {q4:.5f};  printed 3.8 is {(q4-3.8)/q4:.3%} below it. This is the binding chain.")
pr(f"     weighted at q_d=3.8, min modulus 1: sqrt(3.8)/sqrt(1-3.8/4) = {arc(3.8):.3f} < 10 ({(10/arc(3.8)-1):.1%} slack)")
Rs = 2 * pi * 0.0320001
pr(f"  beta=.45: coefficients are (1+beta) = 1.45 and (1+1/beta) = {1+1/.45:.4f}.")
pr(f"     1.45*Rs^2 = {1.45*Rs**2:.5f} < .06 (A.7: 'its multiplier 1.45Rs^2 is below .06') -> {(0.06/(1.45*Rs**2)-1):.2%} slack")
pr(f"     the inequality (1+beta)Rs^2 < .06 gives beta < {0.06/Rs**2-1:.4f}; .45 is {((0.06/Rs**2-1)-.45)/(0.06/Rs**2-1):.1%} below that.")
pr(f"  beta=.8: coefficients (1+.8) = 1.8 and (1+1/.8) = {1+1/.8:.4f}.")
pr(f"     The A.7 bound is 2.25*weighted^2 < 225, i.e. weighted < {sqrt(225/2.25):.1f} = the A.18 threshold.")
pr(f"     So beta=.8 is calibrated so that its coefficient times the A.18 weighted bound is round (225).")

pr()
pr("=" * 100)
pr("5. One cross-check of the seed-stage constants (2.12), supdual")
pr("=" * 100)
N = 112
E = 5 * pi / (4 * N)
pr(f"  E = 5*pi/(4N) at N=112 = {E:.6f};  1.25*pi/N = {1.25*pi/N:.6f} (identical: 5/4 = 1.25)")
pr(f"  supdual evaluates with 1.251*pi/N = {1.251*pi/N:.6f}: a {(1.251/1.25-1):.2%} upward substitution, as stated.")

with open(os.path.join(DATA, "caps.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
with open(os.path.join(DATA, "appendixA_margins.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(mrows[0].keys())); w.writeheader(); w.writerows(mrows)
pr()
pr(f"  wrote {DATA}/caps.csv and appendixA_margins.csv")
