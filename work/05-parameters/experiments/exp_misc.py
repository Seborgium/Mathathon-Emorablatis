#!/usr/bin/env python3
"""The arithmetic constants that carry no discussion: .64, 1e4, 1e10, 1e8, .249/.23, 1e-7.

Each line states the inequality that constrains the constant (where the paper gives one), the
slack, and what half/double does.  No new mathematics -- only arithmetic on the paper's text.
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
rows = []
def row(c, where, ineq, val, slack, half, double, verdict):
    rows.append(dict(constant=c, where=where, inequality=ineq, value=val, slack=slack,
                     at_half=half, at_double=double, verdict=verdict))

print("=" * 78)
print("1. .64: the eigenvalue split that proposes T columns (Prop. 4.6)")
print("=" * 78)
print("  the 25-coordinate horizontal Jacobian is split at .64; eigenvalues below propose T,")
print("  at most 10 T columns are allowed, more than 10 causes failure, and k <= 10 is the")
print("  stated range.  .64 = 0.8^2; the paper gives no spectrum, so .64 is a gap guess.")
print(f"  effective k observed (F3): <= 5 in passes 1-2, <= 7 in pass 3 -> the run never used")
print(f"  more than 5 of the 10 allowed columns.  A split at .32 would add columns (risk k>10),")
print(f"  at 1.28 would drop columns (risk uncovered directions).  Both failures are losses of")
print(f"  coverage, never soundness: the Gram/identity checks are one-sided.")
print(f"  ratio to the 25-coordinate cap: 10/25 = .40 of the directions may be tangent.")
row(".64 eigenvalue split", "Prop. 4.6 (buildH::patch)",
    "at most 10 of 25 eigenvalues may be < .64, else failure", 0.64,
    "no stated spectrum; k<=5 observed vs k<=10 allowed", ".32: more T columns, k>10 -> failure",
    "1.28: fewer T columns, missed directions -> coverage loss", "arbitrary-but-harmless")

print()
print("=" * 78)
print("2. 1e4: the magnitude cap on supdual proposals (2.19), A.3")
print("=" * 78)
print("  A.3: 2 * sum_{a=1..4} |v_a| * 3e-11 <= 2 * 4 * v_max * 3e-11 < 2.5e-6")
for vmax in (1e3, 1e4, 2e4, 1e5):
    e = 2 * 4 * vmax * 3e-11
    print(f"    v_max={vmax:.0e}: bound {e:.3e} vs 2.5e-6 budget: {'ok' if e < 2.5e-6 else 'exceeds'};"
          f" vs the .01 final addition: {'ok' if e < .01 else 'exceeds'}")
print(f"  solving 2*4*v*3e-11 = 2.5e-6 gives v = {2.5e-6/(2*4*3e-11):.0f}: 1e4 is the budget itself,")
print(f"  so it is a *derived* constant with 4% slack.  Doubling to 2e4 doubles the sub-budget")
print(f"  (4.8e-6 > 2.5e-6) but stays 2000x below the .01 addition actually used.")
row("1e4 supdual entry cap", "section 2.4 / A.3", "2*4*v_max*3e-11 < 2.5e-6", 1e4,
    f"{2.5e-6/(2*4*1e4*3e-11):.2f}x (derived, not free)", "5e3: half the budget, tighter proposals",
    "2e4: 4.8e-6 > the stated 2.5e-6 sub-budget", "justified")

print()
print("=" * 78)
print("3. 1e10: the initial support bound in testBucket (A.3)")
print("=" * 78)
trivial = 9 * 111          # (2.18): sum |k_j| <= 9 * 111
print(f"  the initial bound 1e10 is replaced only by a successful (2.18)/(2.19) proposal.")
print(f"  (2.18) alone gives at most sum|k_j| <= 9*111 = {trivial} for the k term of (2.17),")
print(f"  i.e. the honest trivial value is ~{trivial}, so 1e10 is {1e10/trivial:.1e}x larger than")
print(f"  anything it could bound.  It only has to exceed the comparison threshold (NR)^2 = "
      f"{0.032*112**1*3.584:.3f}")
print(f"  so that an unimproved bound fails the test: 1e10 >> 12.8 holds by {1e10/12.845:.1e}x.")
row("1e10 initial support", "section 2.4 / A.3", "must exceed (NR)^2 = 12.845", "1e10",
    "7.8e8x larger than the trivial 999; 7.8e8x the threshold", "5e9: no change",
    "2e10: no change", "arbitrary-but-harmless")

print()
print("=" * 78)
print("4. .249 and .23: the clipped alignment cuts in relationB::init (5.1)")
print("=" * 78)
print("  the cut only declines a relation; it never excludes a parent solution.  Its job is to keep")
print("  the projected difference d_q inside the ball where the local estimates hold.")
print(f"  .249 vs the strict requirement ||d_q|| < .25 (a quarter of the unit cell): slack "
      f"{.25-.249:.3f} = {100*(.25-.249)/.25:.2f}%")
print(f"  with the 1e-6 allowance the stored check gives ||d_q|| < .249002 (A.9), which feeds")
print(f"  total = R + ||d_q|| + 1e-8 + 1e-12 < .377 at R <= .126: slack {.377-(.126+.249002+2e-8):.6f}")
row(".249 / .23 alignment cuts", "section 5.1 / 5.6",
    "cut < .25 (quarter cell); total = R + d_q < .377", ".249 / .23",
    f"{.25-.249:.3f} absolute; .377-total = {.377-.375002:.6f}",
    ".1245: more relations declined (more work)", ".5: total > .377, local estimates invalid",
    "justified (upper one) / arbitrary-but-harmless (.23)")

print()
print("=" * 78)
print("5. 1e-7 and 2e-8: the atlas distance and cap margins (4.7)")
print("=" * 78)
print("  Atlas::find adds 1e-7 to the computed dephased-projected norm; A.6 bounds the")
print("  dephasing/projection error below 1e-11 -> ratio 1e4.")
print("  Atlas::add compares r + d + 1e-8 <= .125 - 2e-8: the 2e-8 margin covers the addition")
print("  and the comparison roundings, which are ~1e-16 at these scales -> ratio 1e8.")
for e, m, name in ((1e-11, 1e-7, "atlas find"), (1e-16, 2e-8, "atlas cap compare"),
                   (1e-12, 1e-8, "assign radius growth"), (1e-13, 1e-9, "z = 1 + o t + 1e-9")):
    print(f"    {name:22s} error {e:.0e}, margin {m:.0e}, ratio {m/e:.1e}")
row("1e-7 atlas find margin", "section 4.7 / A.6", "projection error < 1e-11", "1e-7",
    "1e4x", "5e-8: still 5000x", "2e-7: 2e4x", "arbitrary-but-harmless")
row("2e-8 atlas cap margin", "section 4.7", "addition/comparison rounding ~1e-16", "2e-8",
    "1e8x", "1e-8: 1e8x", "4e-8: 4e8x", "arbitrary-but-harmless")

os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, "misc_constants.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(f"\nwrote {os.path.join(DATA,'misc_constants.csv')}")
