#!/usr/bin/env python3
"""Every margin in the closing table of Appendix A: established error, margin, ratio.

The table is copied as data (it is the paper's own statement of its error budgets); every ratio,
the ranking and the global resilience number are recomputed here.
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
# (path, [(name, error)], margin, unit)
T = [
 ("seed gap / direct support",            [("gap", 1e-14), ("support", 1e-11)], 1e-8,  ""),
 ("shared-coordinate numerator",          [("num", 3.5e-11)],                    1e-7,  ""),
 ("shared-coordinate endpoints",          [("end", 1e-7)],                      1e-5,  ""),
 ("seed dual support",                    [("dual", 1e-4)],                     .01,   ""),
 ("A flat norm",                          [("flat", 1e-6)],                    1e-5,  ""),
 ("A directional comparison",             [("dir", 4e-6)],                     .0001,  ""),
 ("Root identity Frobenius check",        [("id", 5e-8)],                     2e-6,  ""),
 ("Root orthogonal / horizontal checks",  [("orth", 1e-10), ("hor", 1e-11)],   1e-8,  ""),
 ("tensor transformed row bound",         [("tensor", 1e-6)],                  .0002, ""),
 ("Candidate direct support",             [("direct", 2e-6)],                  .0001, ""),
 ("Candidate external tangent error",     [("tangent", 0.00012)],              0.00015, "rad"),
 ("first / second G entry error",         [("G1", 1e-11), ("G2", 1e-9)],       1e-7,  ""),
 ("spectral row / fourth-norm bound",     [("row", 3e-13), ("fro4", 1e-10)],   [1e-10, 2e-7], ""),
 ("bootstrap update",                     [("boot", 1e-12)],                   1e-8,  ""),
 ("B projected normal / local update",    [("proj", 5e-11), ("loc", 1e-13)],   1e-8,  ""),
 ("B cross-Gram spectral perturbation",   [("cross", 2e-9)],                   1e-7,  ""),
 ("C direct / directional comparison",    [("Cd", 1e-9)],                      2e-7,  ""),
 ("C joint support",                      [("joint", 1e-8)],                   3e-7,  ""),
]

rows = []
for path, errs, margin, unit in T:
    for name, e in errs:
        mg = margin if not isinstance(margin, list) else margin[0 if name == "row" else 1]
        rows.append(dict(path=path, component=name, error=e, margin=mg,
                         error_over_margin=e / mg, margin_over_error=mg / e, unit=unit))
rows.sort(key=lambda r: r["margin_over_error"])
print("=" * 96)
print("Appendix A closing table, recomputed: margin / error, worst first")
print("=" * 96)
print(f"{'path':40s} {'comp':7s} {'error':>10s} {'margin':>10s} {'ratio':>10s}")
for r in rows:
    print(f"{r['path']:40s} {r['component']:7s} {r['error']:>10.3g} {r['margin']:>10.3g}"
          f" {r['margin_over_error']:>10.4g}")
print()
print(f"rows: {len(rows)}; margins below 2x the error: {[r['path'] for r in rows if r['margin_over_error']<2]}")
print(f"margins below 10x: {[(r['path'], round(r['margin_over_error'],2)) for r in rows if r['margin_over_error']<10]}")
print(f"margins above 1000x: {[(r['path'], round(r['margin_over_error'])) for r in rows if r['margin_over_error']>1000]}")
print()
print("global resilience (my conditioning number): a uniform inflation t of EVERY established")
print("error keeps the chain valid iff t < min ratio =", f"{rows[0]['margin_over_error']:.4g}",
      f"({rows[0]['path']})")
print("second and third:", f"{rows[1]['margin_over_error']:.3g} ({rows[1]['path']})",
      f"{rows[2]['margin_over_error']:.3g} ({rows[2]['path']})")
print()
print("scale check: 18 paths, 23 components; median ratio",
      f"{sorted(r['margin_over_error'] for r in rows)[len(rows)//2]:.4g}")

os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, "margins.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(f"\nwrote {os.path.join(DATA,'margins.csv')}")
