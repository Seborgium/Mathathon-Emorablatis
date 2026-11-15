#!/usr/bin/env python3
"""Stage A: the U(2) grid N_u = 16 -> 512, h = pi/N_u, the cell counts, the node cap,
and the local/global targets.  Run: python3 experiments/stageA.py
"""
import csv, os
from math import pi, sqrt, ceil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, os.pardir, os.pardir, "data", "m3"))
def pr(*a): print(*a)
rows = []

pr("=" * 92)
pr("1. The U(2) grid (Lemma 3.3): bins (Nu/2, Nu/4, Nu, Nu), so Nu^4/8 closed cells")
pr("=" * 92)
hdr = f"{'Nu':>5} {'h=pi/Nu':>9} {'sqrt6*h':>9} {'sqrt42/2*h^2':>12} {'cells=Nu^4/8':>14} {'vs 1e6 cap':>11} {'rem/.647':>9}"
pr(hdr); pr("-" * len(hdr))
NODE_CAP = 1_000_000
for Nu in (16, 32, 64, 128, 256, 512):
    h = pi / Nu
    cells = Nu**4 // 8
    rem = sqrt(42) / 2 * h * h
    rows.append((Nu, h, cells, rem, cells / NODE_CAP))
    pr(f"{Nu:>5} {h:>9.5f} {sqrt(6)*h:>9.5f} {rem:>12.6f} {cells:>14,} {cells/NODE_CAP:>10.2f}x {rem/.647:>9.5f}")
pr()
pr("  cells = Nu^4/8 reproduces the paper's 64^4/8 =", 64**4 // 8, "(7.3).")
pr("  sqrt42/2*h^2 is the Lemma 3.4 linearisation remainder (radians); .647 rad = 2*pi*.103.")
pr("  At the base grid Nu=16 the Taylor remainder is already 5.2x inside the local target,")
pr("  so the target does not force subdivision: coverage/cost does.")
pr()
pr("  The node cap: at Nu=64 exhaustive enumeration needs 2,097,152 cells > 1,000,000.")
pr("  32 levels are retained in full (131,072 cells = 13.1% of the cap); at Nu=64 the")
pr("  exhaustive list is abandoned and the search is capped at 1e6 extra nodes =")
pr(f"  {131072 + NODE_CAP:,} of {2097152:,} cells = {(131072+NODE_CAP)/2097152:.1%} of the grid.")
pr("  So from Nu=64 on, Stage A completeness rests on the phase-ball cover, not enumeration.")

pr()
pr("=" * 92)
pr("2. Cost: observed A wall time vs the base-grid cell count")
pr("=" * 92)
seeds, tA = 249878, 2020.32
per_seed = tA / seeds
pr(f"  recorded {seeds:,} seeds, {tA} s -> {per_seed*1e3:.3f} ms/seed")
pr(f"  base grid 8,192 cells/seed -> {per_seed/8192*1e9:.0f} ns/cell (the dominant loop is consistent)")
pr(f"  one extra grid level (x4 cells) costs ~{3*tA/60:.0f} min more in total; 4 levels ~{15*tA/60:.0f} min")
pr(f"  deepest grid 512 = 8.6e9 cells/seed if ever enumerated -> impossible; never is.")

pr()
pr("=" * 92)
pr("3. h = pi/Nu: what it must be small against, and what it must not exceed")
pr("=" * 92)
pr("  (i) Taylor: all four angular displacements satisfy |theta| <= h (3.13).")
pr("  (ii) the seed ball angular radius is  Rs = 2*pi*.0320001 = .20106 rad.")
pr(f"       At Nu=16, h = {pi/16:.5f} and Rs/h = {2*pi*0.0320001/(pi/16):.4f}: the seed ball is")
pr("       one base cell across to 2.4%.  If R were doubled, Rs/h = 2.05 and the seed ball")
pr("       would straddle ~4 base cells instead of ~1 (a cost factor, not a failure).")
pr("  (iii) h enters A.4 as h < .197 (proved headroom .2%); at Nu=16 h = .19635, i.e. 0.3%")
pr(f"       below the .197 threshold; at Nu=15 h = {pi/15:.5f} > .197 would fail the field bound.")
pr("       So Nu >= 16 is forced by the A.4 chain, not only by resolution.")

with open(os.path.join(DATA, "stageA_grid.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["Nu", "h_rad", "cells_per_seed", "taylor_remainder_rad", "cells_over_1e6"]); w.writerows(rows)
pr()
pr(f"  wrote {DATA}/stageA_grid.csv")
