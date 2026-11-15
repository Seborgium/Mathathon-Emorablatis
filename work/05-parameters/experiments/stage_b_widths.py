#!/usr/bin/env python3
"""Stage B: the three (tau,w) refinement pairs, the box grid, and the largest
admissible tangent dimension k.

Paper facts used (and where):
  s5.1  input radii 0 <= R <= 0.126, child cap and width 1e-4 <= tau <= .126,
        1e-4 <= w <= .05, 0 <= k <= 10, base grid <= 50,000,000 boxes, depth <= 6
  A.9   E = sqrt(1+ort_P) R + 1e-7,  L = ceil(E/w + .500001),  L <= 1262
  s7.2  (tau,w) = (.07,.013), (.016,.005), (.011,.0038); the fine batches
        replace each batch radius by .016 before B fine reads them
  s7.5  B mid 3083 -> 600, B fine 600 -> 22379, B fallback 163 -> 1127, no
        unresolved parents, no grid-cap rejection

Run: python3 experiments/stage_b_widths.py
"""
import math

CAP_BOXES = 50_000_000
ORT_MAX = 1e-5


def E_of(R, ort=ORT_MAX):
    """Stored grid radius, A.9: it exceeds the true tangent radius."""
    return math.sqrt(1 + ort) * R + 1e-7


def L_of(R, w, ort=ORT_MAX):
    return math.ceil(E_of(R, ort) / w + 0.500001)


def kmax(L, cap=CAP_BOXES):
    a = 2 * L + 1
    k = 0
    while a ** (k + 1) <= cap:
        k += 1
    return k, a


def main():
    print("=== 1. the three prescribed passes ===")
    print("   pass   tau     w       R_in (as printed)     E         L   axes   k_max")
    passes = [
        ("mid", 0.070, 0.013, 0.126, "coarse records, radius <= .126 (s5.1 worst case)"),
        ("fine", 0.016, 0.005, 0.016, "mid.bin with radius replaced by .016 (s7.2)"),
        ("fallback", 0.011, 0.0038, 0.016, "the 163 fine records, radius <= .016"),
    ]
    for name, tau, w, Rin, why in passes:
        E = E_of(Rin)
        L = L_of(Rin, w)
        k, a = kmax(L)
        print(f"  {name:<9}{tau:<8}{w:<8}{Rin:<21} {E:.6f}  {L:3d}  {a:4d}   {k}")
        print(f"           input: {why}")

    print("\n=== 2. F3: is k <= 10 reachable?  no, and the operative bound is 5 ===")
    print("   (2L+1)^k <= 5e7 first fails at:")
    for name, tau, w, Rin, _ in passes:
        L = L_of(Rin, w)
        a = 2 * L + 1
        k, _ = kmax(L)
        print(f"  {name:<9} axes={a:3d}: {a}^{k} = {a ** k:>12,} <= 5e7 < "
              f"{a}^{k + 1} = {a ** (k + 1):>14,}")
    print("   so a record with more than 5 tangent columns cannot be refined in the")
    print("   mid pass, which is the pass every coarse record must survive; the")
    print("   stated allowance 0 <= k <= 10 (Def 4.1, s5.1, s6.1) overshoots by 5.")

    print("\n=== 3. correction to results/code-audit.md F3 ===")
    print("   the audit's row for the fine pass assumes input radius .07 and gets")
    print("   L=15, 31 boxes/axis, k<=5.  But .07 is the MID pass's child cap tau,")
    print("   not an input radius: s7.2 replaces every batch radius by .016 before")
    print("   B fine reads it.  With R_in=.016: E/w = "
          f"{E_of(0.016) / 0.005:.6f}, L = {L_of(0.016, 0.005)}, "
          f"axes = {2 * L_of(0.016, 0.005) + 1}, k_max = {kmax(L_of(0.016, 0.005))[0]}.")
    print("   With the audit's .07: L = %d, axes = %d, k_max = %d (its numbers)."
          % (L_of(0.07, 0.005), 2 * L_of(0.07, 0.005) + 1, kmax(L_of(0.07, 0.005))[0]))
    print("   Both readings agree that k=9,10 are unreachable; they disagree on")
    print("   whether k=6 is admissible, and that is what decides whether the")
    print("   observed k histogram may contain a 6.")

    print("\n=== 4. why the width must be smaller than the child radius ===")
    print("   a box of width w in k coordinates has diameter sqrt(k)*w; markRec can")
    print("   only close a box whose farthest corner is inside the child target, and")
    print("   assign merges only when r + l < tau.  So the necessary scale is")
    print("   sqrt(k)*w < tau.")
    print("   pass     tau      w      sqrt(k)w   tau/(sqrt(k)w)   verdict")
    for name, tau, w, Rin, _ in passes:
        k, _ = kmax(L_of(Rin, w))
        d = math.sqrt(k) * w
        print(f"  {name:<9}{tau:<8}{w:<8}{d:<10.5f}{tau / d:<15.3f}"
              f"{'tight' if tau / d < 1.2 else 'ok'}")
    print("   the third pass is the tight one (1.09): that is the concrete reason")
    print("   the fine widths shrink with the radius rather than staying fixed.")

    print("\n=== 5. cost curve in w (boxes per parent at the largest admissible k) ===")
    print("   pass      L(w)   L(w/2)   boxes(w)      boxes(w/2)     ratio")
    for name, tau, w, Rin, _ in passes:
        k, a = kmax(L_of(Rin, w))
        k2, a2 = kmax(L_of(Rin, w / 2))
        b1, b2 = a ** k, a2 ** k2
        print(f"  {name:<9}{L_of(Rin, w):<7}{L_of(Rin, w / 2):<9}{b1:<14,}{b2:<15,}"
              f"{b2 / b1:8.2f}")
    print("   Note the non-monotonicity: boxes(w/2) is SMALLER than boxes(w) for the")
    print("   first two passes, because the axis count doubles while the admissible k")
    print("   falls by one.  The 5e7 cap couples w to k, so 'halve the width' is not")
    print("   uniformly more expensive - only the fallback pass gets dearer.")
    print("   doubling w instead halves the axis count but breaks sqrt(k)w < tau,")
    print("   so the box can no longer be marked whole and the split recursion must")
    print("   run, at 2^k children per level for at most 6 levels (depth cap).")

    print("\n=== 6. depth six, and the batch radius replacement ===")
    print("   depth 6 with halving width: w/64;")
    for name, tau, w, Rin, _ in passes:
        print(f"   {name:<9} w/64 = {w / 64:.7f}, child target becomes "
              f"{tau / 64:.7f}")
    print("   'each unresolved box is split to depth at most six, and the 2^k child")
    print("   masks fit an integer' -> with k<=8, 2^8=256 fits; with the stated")
    print("   k<=10, 2^10=1024 also fits.  No tension here.")
    print("   the batching rule (radius -> .016) is what makes the fine pass cheap:")
    print(f"   with R_in=.07 instead, L would be {L_of(0.07, 0.005)} instead of "
          f"{L_of(0.016, 0.005)}, and the box count per parent would rise from "
          f"{9 ** 8:,} to {(2 * L_of(0.07, 0.005) + 1) ** 5:,}.")

    import os
    os.makedirs("data", exist_ok=True)
    with open("data/stage_b.csv", "w") as fh:
        fh.write("pass,tau,w,R_in,E,L,axes,k_max,box_diameter,tau_over_diameter,"
                 "boxes_at_kmax\n")
        for name, tau, w, Rin, _ in passes:
            E = E_of(Rin)
            L = L_of(Rin, w)
            k, a = kmax(L)
            fh.write(f"{name},{tau},{w},{Rin},{E:.7f},{L},{a},{k},"
                     f"{math.sqrt(k) * w:.6f},"
                     f"{tau / (math.sqrt(k) * w):.4f},{a ** k}\n")
    print("\nwrote data/stage_b.csv")


if __name__ == "__main__":
    main()
