#!/usr/bin/env python3
"""The U(2) cell grid: N_u = 16 base, subdivided 32, 64, ..., 512, with h = pi/N_u.
Constraints recomputed:
  * Lemma 3.3: bin counts (N_u/2, N_u/4, N_u, N_u)  =>  N_u^4/8 cells per seed;
  * Lemma 3.4: ||V-U||_F <= sqrt(6) h, Taylor remainder <= (sqrt(42)/2) h^2;
  * section 3.7 / 7.3: deeper-node cap 1,000,000 extra nodes; 64^4/8 cell tests at grid 64;
  * targets: local .103 (local::test), global .125 (A atlas radius cap), and the B validate
    range R <= .126 (A.9).
"""
import csv, os
from math import pi, sqrt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
NODE_CAP = 1_000_000
LOCAL, GLOBAL_, RVAL, RC = 0.103, 0.125, 0.126, 0.03   # RC: section 6.1 needs r <= .03
C6, C42 = sqrt(6.0), sqrt(42.0) / 2

print("=" * 78)
print("1. grid size, step and Taylor remainders")
print("=" * 78)
rows = []
for nu in (16, 32, 48, 64, 128, 256, 512):
    cells = nu ** 4 // 8
    h = pi / nu
    lin, quad = C6 * h, C42 * h * h
    rows.append(dict(Nu=nu, cells_per_seed=cells, h=h, linear_bound=lin, taylor_remainder=quad,
                     remainder_over_local=quad / LOCAL, remainder_over_global=quad / GLOBAL_,
                     under_node_cap=int(cells <= NODE_CAP), power_of_two=int((nu & (nu - 1)) == 0)))
    print(f"Nu={nu:4d}: cells/seed = {cells:>13,}  h = {h:.6f}  sqrt6 h = {lin:.6f}"
          f"  (sqrt42/2) h^2 = {quad:.6f}  = {100*quad/LOCAL:5.1f}% of .103"
          f"  <=1e6 nodes: {int(cells<=NODE_CAP)}")
print()
print("largest power-of-two grid with N_u^4/8 <= 1e6:", end=" ")
print(max(nu for nu in (16, 32, 64, 128, 256, 512) if nu ** 4 // 8 <= NODE_CAP))
print("largest N_u at all with N_u^4/8 <= 1e6: N_u <=", int((8 * NODE_CAP) ** 0.25))
print(f"predicted Nu at which the Taylor remainder falls below the local target .103: "
      f"{pi/sqrt(LOCAL/C42):.2f} (so Nu = 32, the first subdivision)")
print(f"same for the global target .125: {pi/sqrt(GLOBAL_/C42):.2f}")
print(f"at the base grid Nu=16 the remainder is {C42*(pi/16)**2:.6f}: above .103, below .125.")

print()
print("=" * 78)
print("2. the four targets and how they chain")
print("=" * 78)
print(f"local target  .103   (a cell is covered only if its certified Root radius fits this)")
print(f"atlas cap     .125   (A atlas grows a radius to r+d and aborts above this)")
print(f"B validate    .126   (A.9: every B input radius must satisfy 0 <= R <= .126)")
print(f"C requires    .03    (section 6.1 fixes a Record of radius 0 <= r <= .03)")
print()
print(f"  .125 - .103 = {GLOBAL_-LOCAL:.3f}: the atlas can absorb a merge distance d <= {GLOBAL_-LOCAL:.3f}"
      f" before aborting; ratio .125/.103 = {GLOBAL_/LOCAL:.4f}")
print(f"  .126 - .125 = {RVAL-GLOBAL_:.3f}: slack {100*(RVAL-GLOBAL_)/RVAL:.2f}% -- the tightest of the chain")
print(f"  A.9 needs total = R + 0.249002 + 1e-8 + 1e-12 < .377; at R = .126 total = "
      f"{RVAL+0.249002+2e-8:.6f}, slack {0.377-(RVAL+0.249002+2e-8):.6f}")
print(f"  section 6.1 needs r <= .03: fine pass tau = .016 is {0.03/0.016:.3f}x below it, "
      f"fallback .011 is {0.03/0.011:.3f}x below")
print(f"  what .03 buys: Lemma 6.5 (s < .1) has {0.1/0.03:.3f}x room; and 2s = {2*0.03:.2f} < .2")

print()
print("=" * 78)
print("3. sensitivity of the grid growth")
print("=" * 78)
for k in range(0, 6):
    nu = 16 * 2 ** k
    print(f"  Nu={nu:4d}: cells x{nu**4/16**4:8.1f} vs base, remainder x{1/2**(2*k):.4f},"
          f" h x{1/2**k:.4f}; cost per seed ~ cells")
print("doubling Nu multiplies cell work by 16 and divides the Taylor remainder by 4,")
print("so the cost of one more level is 16x and the accuracy gain is 2x: the base grid 16 -> 32")
print("is the only level at which the remainder crosses the .103 target.")
print(f"halving the target .103 -> .0515 would need Nu ~ {pi/sqrt(0.0515/C42):.1f} (i.e. 32 already ok)")
print(f"doubling .103 -> .206 is reached already at Nu=16 ({C42*(pi/16)**2:.4f} vs .206)")

os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, "u2_grid.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(f"\nwrote {os.path.join(DATA,'u2_grid.csv')}")
