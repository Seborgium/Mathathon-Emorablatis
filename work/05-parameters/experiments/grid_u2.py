#!/usr/bin/env python3
"""The U(2) grid N_u in {16,32,...,512}, h = pi/N_u, the targets .103 and .125.

Sources: Lemma 3.3 (four bin counts N_u/2, N_u/4, N_u, N_u), Lemma 3.4 (Taylor
bounds sqrt(6)h and (sqrt(42)/2)h^2), s3.7 ('base grid is Nu = 16 ... subdivision
through Nu = 512'), s5.1/s7.3 (1,000,000-node cap, 64^4/8 = 2,097,152 cells).

Run: python3 experiments/grid_u2.py
"""
import math

S6 = math.sqrt(6)
S42_2 = math.sqrt(42) / 2


def cells(nu):
    """Number of closed cells per seed: (nu/2)*(nu/4)*nu*nu = nu^4/8."""
    return nu ** 4 // 8


def main():
    print("=== 1. the grid chain and the Taylor bounds of Lemma 3.4 ===")
    print("   N_u    h=pi/N_u   sqrt(6)h   (sqrt42/2)h^2   cells=N^4/8   vs 1e6 cap")
    for nu in (16, 32, 64, 128, 256, 512):
        h = math.pi / nu
        print(f"  {nu:4d}  {h:9.6f}  {S6 * h:9.6f}   {S42_2 * h * h:12.8f}"
              f"   {cells(nu):12,d}   {cells(nu) / 1e6:9.3f}")
    print("   the four bin counts must be integers, so 4 | N_u; the chain")
    print("   16 -> 512 is exactly five doublings (six grids), see item 4.")

    print("\n=== 2. .125 IS the level-1 Taylor remainder ===")
    h16 = math.pi / 16
    t2 = S42_2 * h16 * h16
    print(f"   (sqrt(42)/2)*(pi/16)^2 = {t2:.9f}")
    print(f"   .125 - that            = {0.125 - t2:.3e}")
    print(f"   so .125 is the first-order Taylor bound rounded UP to 3 decimals:")
    print(f"   ceil(1000*{t2:.6f})/1000 = {math.ceil(1000 * t2) / 1000:.3f}")
    print("   This is the one target in the paper with a derivable value: the")
    print("   global atlas target must exceed the error of the COARSEST cell, and")
    print("   the coarsest cell is N_u=16 with second-order remainder .124928.")
    print("   Halving it (.0625) would be below the N_u=16 remainder -> unsound.")
    print("   Doubling it (.25) is safe and would cost: the atlas cap .125 and the")
    print("   child cap tau <= .126 both come from it, so doubling forces every")
    print("   Stage B output radius up (see experiments/stage_b_widths.py).")

    print("\n=== 3. what could .103 be?  no closed form reproduces it ===")
    cands = {
        "level-1 Taylor at N_u=16            ": t2,
        "level-1 Taylor at N_u=32            ": S42_2 * (math.pi / 32) ** 2,
        "level-2 Taylor at N_u=16            ": S6 * h16,
        ".125 - 2*pi*.032*? (see below)      ": float("nan"),
        ".125*(1-1/6)                        ": 0.125 * 5 / 6,
        "sqrt(.125^2-.032^2)                 ": math.hypot(0.125, 0.032),
        "2*pi*.0320001/2                     ": 2 * math.pi * 0.0320001 / 2,
        ".125 - (sqrt42/2)(pi/64)^2          ": 0.125 - S42_2 * (math.pi / 64) ** 2,
    }
    for k, v in cands.items():
        print(f"   {k} = {v:.6f}   |v-.103| = {abs(v - 0.103):.4f}")
    print("   none of these is .103 to 3 decimals.  .103 is therefore a MEASURED")
    print("   threshold (the largest local radius the run had to cover), not a")
    print("   derived one; s4.6 only says success requires the bound to fit it.")
    print("   Constraint: max achievable local radius <= .103 <= .125 = global.")
    print("   Recommendation: print the observed max local radius.  If it is .06,")
    print("   .103 carries 1.7x slack; if it is .102, the whole atlas is within 1%")
    print("   of its target and any change to R or to the (tau,w) passes is unsafe.")

    print("\n=== 4. depth six IS the 512 ceiling ===")
    lv = [16]
    while lv[-1] < 512:
        lv.append(2 * lv[-1])
    print(f"   grids: {lv}  = {len(lv)} levels = {len(lv) - 1} doublings")
    print("   'subdivision depth at most six' with base 16 reaches 16*2^6 = 1024,")
    print("   while 'deepest grid 512' stops at 16*2^5.  The two limits differ by")
    print("   one level, so the depth cap is not the binding one for Stage A; the")
    print("   node cap and the 512 ceiling are.")
    print("   Cost of one more level from 64: 16x the cells per retained cell.")
    print(f"   cells at 512 alone = {cells(512):,} per seed = "
          f"{cells(512) / 2e6:.0f}x the 2,000,000 C-bin cap, so a live cell at 512")
    print("   can only be closed by a certified phase ball, never by enumeration.")

    print("\n=== 5. the cap that actually bites: 1,000,000 nodes ===")
    print(f"   64^4/8 = {cells(64):,} > 1e6: from grid 64 downward Stage A cannot")
    print("   enumerate a seed, so success must come from the phase-ball cover.")
    print(f"   at 32: {cells(32):,} cells = {cells(32) / 1e6:.2f} of the cap")
    print(f"   at 16: {cells(16):,} cells = {cells(16) / 1e6:.4f} of the cap")


if __name__ == "__main__":
    main()
