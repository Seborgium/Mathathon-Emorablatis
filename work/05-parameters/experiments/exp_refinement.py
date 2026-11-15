#!/usr/bin/env python3
"""The three (tau,w) refinement passes, the grid extent L, the admissible root dimension k,
and the depth budget.  Everything is recomputed from A.9 and section 5.6/7.3:

  E   = (1+ort)*R_in + 1e-7 with ort < 1e-5   (A.9: stored grid radius)
  L   = ceil(E/w + 0.500001)                  (A.9: integer base range covers [-E,E])
  boxes per parent = (2L+1)^k <= 50,000,000    (section 5.6)  => bound on the Root dimension k
  L <= 1262 for w >= 1e-4                     (section 5.6 / A.9)
  depth: a parent box must be split until its halfwidth drops below tau, i.e.
         ceil(log2(tau/w)) levels, and the total depth cap is six (section 5.6)
"""
import csv, os
from math import ceil, log2

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
BOXCAP = 50_000_000
ORT = 1e-5
# pass, tau, w, input radius R_in (the previous stage's cap / A atlas cap)
PASSES = [("1 mid", 0.07, 0.013, 0.125),
          ("2 fine", 0.016, 0.005, 0.07),
          ("3 fallback", 0.011, 0.0038, 0.016)]

print("=" * 78)
print("1. L and the admissible k for each pass")
print("=" * 78)
rows = []
for name, tau, w, Rin in PASSES:
    E = (1 + ORT) * Rin + 1e-7
    L = ceil(E / w + 0.500001)
    axis = 2 * L + 1
    kmax = 0
    while (axis) ** (kmax + 1) <= BOXCAP:
        kmax += 1
    boxes_k5 = axis ** 5
    depth = ceil(log2(tau / w))
    rows.append(dict(pass_name=name, tau=tau, w=w, R_in=Rin, E=E, L=L, boxes_per_axis=axis,
                     boxes_k5=boxes_k5, k_max=kmax, tau_over_w=tau / w, depth_needed=depth,
                     L_at_wmin=ceil(((1 + ORT) * Rin + 1e-7) / 1e-4 + 0.500001)))
    print(f"{name:12s} tau={tau:<7} w={w:<7} R_in={Rin:<7} E={E:.7f} L={L:3d} "
          f"boxes/axis={axis:3d} (2L+1)^5={boxes_k5:>11,} = {100*boxes_k5/BOXCAP:5.1f}% of cap"
          f"  k_max={kmax}")
    print(f"{'':12s} tau/w = {tau/w:.4f} -> depth needed ceil(log2) = {depth};"
          f"  at w=1e-4 this pass would need L={rows[-1]['L_at_wmin']} (cap 1262)")
    print(f"{'':12s} (2L+1)^6 = {axis**6:,} {'> cap' if axis**6 > BOXCAP else '<= cap'};"
          f"  (2L+1)^7 = {axis**7:,} {'> cap' if axis**7 > BOXCAP else '<= cap'}")
print()
print("=> with the stated widths no record with k >= 6 (passes 1-2) or k >= 8 (pass 3) can be")
print("   processed at all: the parent fails on the grid cap.  The paper states 0 <= k <= 10.")
print(f"   the k = 10 allowance would need (2L+1)^10 <= 5e7, i.e. 2L+1 <= {int(BOXCAP**0.1)}, L <= {(int(BOXCAP**0.1)-1)//2}")
print(f"   i.e. w >= E/((2L+1-1)/2) ; for R_in=.125: w >= {((1+ORT)*0.125+1e-7)/((BOXCAP**0.1-1)/2):.4f}")

print()
print("=" * 78)
print("2. consistency of the (tau,w) chain")
print("=" * 78)
print(f"A atlas cap .125 -> validate .126 (slack {0.126-0.125:.3f})")
print(f"tau_1 .07 < .125 (input) : {0.07 < 0.125};  tau_2 .016 < .07 : {0.016 < 0.07};"
      f"  tau_3 .011 < .016 : {0.011 < 0.016}")
print(f"chain needs a strict decrease for refinement to shrink balls: .125 > .07 > .016 > .011")
print(f"  ratios: .07/.125={0.07/0.125:.3f}, .016/.07={0.016/0.07:.4f}, .011/.016={0.011/0.016:.4f}")
print(f"section 5.6 requires .0001 <= tau <= .126 and .0001 <= w <= .05: all three pass"
      f" (smallest tau .011 vs floor .0001 = {0.011/0.0001:.0f}x; largest w .013 vs ceiling .05 = {0.05/0.013:.2f}x)")
print(f"section 6.1 requires the C-relevant radius r <= .03: tau_2 = .016 ({0.03/0.016:.3f}x below),"
      f" tau_3 = .011 ({0.03/0.011:.3f}x below); tau_1 = .07 would violate it ({0.07/0.03:.2f}x above)")
print("  => the mid pass cannot feed C directly: the fine pass is forced by the r <= .03 hypothesis,")
print("     not by accuracy.  That is the decisive constraint on tau_2.")
print()
print("independent check: a ball of radius tau holds (tau/(3/(2N)))^9 bins of side 1/N")
for tau in (0.07, 0.016, 0.011):
    print(f"  tau={tau}: at N=112 a ball holds {(tau/(3/(2*112)))**9:12.4g} bins")

print()
print("=" * 78)
print("3. what half / double does")
print("=" * 78)
for name, tau, w, Rin in PASSES:
    for f in (0.5, 2.0):
        E = (1 + ORT) * Rin + 1e-7
        t2 = tau * f
        L2 = ceil(E / w + 0.500001)
        print(f"  {name}: tau x{f} -> {t2:.4f}; still < input {Rin}: {t2 < Rin};"
              f" tau/w = {t2/w:.3f} (depth {ceil(log2(t2/w))});"
              f" C-compatible (<=.03): {t2 <= 0.03}")
        w2 = w * f
        L3 = ceil(E / w2 + 0.500001)
        ax = 2 * L3 + 1
        kk = 0
        while ax ** (kk + 1) <= BOXCAP:
            kk += 1
        print(f"  {name}: w x{f} -> {w2:.5f}; L={L3}, boxes/axis={ax}, k_max={kk},"
              f" depth {ceil(log2(tau/w2))}; w within [1e-4,.05]: {1e-4 <= w2 <= 0.05}")

os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, "refinement.csv"), "w", newline="") as fh:
    w_ = csv.DictWriter(fh, fieldnames=list(rows[0])); w_.writeheader(); w_.writerows(rows)
print(f"\nwrote {os.path.join(DATA,'refinement.csv')}")
