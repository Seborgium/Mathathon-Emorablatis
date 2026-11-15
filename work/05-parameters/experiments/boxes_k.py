#!/usr/bin/env python3
"""The Stage-B box cap, the refinement widths, and the attainable Root depth k (F3).

Per-axis half-count  L = ceil(radius/w + 0.500001);
boxes per axis = 2L+1;  grid = (2L+1)**k;  cap 5*10**7;  depth <= 6.

Run: python3 experiments/boxes_k.py
"""
import csv
from math import ceil, log

CAP = 50_000_000
W_MIN, W_MAX = 0.0001, 0.05
TAU_MIN, TAU_MAX = 0.0001, 0.126
R_IN = 0.126

PASSES = [
    ("B mid",  0.013, 0.125, "atlas radius cap .125 (first input)"),
    ("B fine", 0.005, 0.070, "B mid target radius .07"),
    ("B fall", 0.0038, 0.016, "B fine target radius .016"),
]


def L_of(radius, w):
    return ceil(radius / w + 0.500001)


def kmax(L, cap=CAP):
    k = 0
    while (2 * L + 1) ** (k + 1) <= cap:
        k += 1
    return k


def main():
    rows = []
    print("=== Stage-B refinement passes: per-axis count, grid size, admissible k ===")
    print(f"{'pass':8s} {'w':>8s} {'input R':>8s} {'L':>5s} {'boxes/axis':>11s} {'kmax':>5s}"
          f" {'grid at kmax':>14s} {'grid at kmax+1':>16s}")
    for name, w, r, why in PASSES:
        L = L_of(r, w)
        boxes = 2 * L + 1
        k = kmax(L)
        g = boxes ** k
        g1 = boxes ** (k + 1)
        rows.append(dict(pass_name=name, w=w, input_radius=r, L=L, boxes_per_axis=boxes,
                         max_k=k, grid_at_kmax=g, grid_at_kmax_plus_1=g1,
                         cap_utilisation=g / CAP, radius_source=why))
        print(f"{name:8s} {w:8.4f} {r:8.3f} {L:5d} {boxes:11d} {k:5d} {g:14,} {g1:16,}")
    print()
    print("=== What the stated allowance 0 <= k <= 10 would need ===")
    for name, w, r, _ in PASSES:
        boxes = 2 * L_of(r, w) + 1
        need = boxes ** 10
        print(f"  {name:8s}: boxes/axis {boxes:3d}; (2L+1)^10 = {need:,.0f}"
              f" = {need / CAP:,.0f} x the cap")
    print()
    print("=== The cap needed to admit each depth, per pass ===")
    print(f"{'k':>3s}" + "".join(f"{n:>22s}" for n, _, _, _ in PASSES))
    for k in range(4, 9):
        line = f"{k:3d}"
        for name, w, r, _ in PASSES:
            boxes = 2 * L_of(r, w) + 1
            line += f"{boxes ** k:>22,}"
        print(line)
    print("  (the 50,000,000 cap admits k=5, k=5, k=7 respectively)")
    print()
    print("=== L <= 1262 claimed in section 7.3, from w >= 1e-4 and R <= .126 ===")
    Lmax = L_of(R_IN, W_MIN)
    print(f"  L = ceil({R_IN}/{W_MIN} + 0.500001) = {Lmax}  -> axis indices < {2 * Lmax + 1}"
          f"  (paper: L <= 1262, indices at most 2524)")
    print()
    print("=== The widths also have to be smaller than the child radius they refine ===")
    for (n1, w1, t1, _), (n2, w2, t2, _) in zip(PASSES, PASSES[1:]):
        print(f"  {n2}: w = {w2} vs the parent target radius {t1}: w/tau = {w2 / t1:.4f}"
              f"   (must be < 1: {w2 < t1})")
    print(f"  B mid: w = {PASSES[0][1]} vs atlas radius cap {PASSES[0][2]}: "
          f"ratio {PASSES[0][1] / PASSES[0][2]:.4f}")
    print()
    print("=== radius-shrink chain (each pass must shrink the stored radius) ===")
    chain = [0.125, 0.07, 0.016, 0.011]
    for a, b in zip(chain, chain[1:]):
        print(f"  {a} -> {b}: factor {a / b:.3f}")
    print(f"  depth 6 with the observed per-level shrink >= {0.016 / 0.011:.2f} is not the binding")
    print("  constraint; the binding one is the box cap above.")
    with open("work/05-parameters/data/boxes_k.csv", "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wtr.writeheader()
        wtr.writerows(rows)


if __name__ == "__main__":
    main()
