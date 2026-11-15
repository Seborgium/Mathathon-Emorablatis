#!/usr/bin/env python3
"""Global conditioning of the numeric chain (direction d4) and the derived constants
K, q_d, the Young split beta, the bootstrap count, the 25 midpoint trials, the divisor skip.

Everything printed here is computed from the paper's own displayed formulas:
  (6.3)  ||A/sqrt6||_op <= sqrt(1 + sqrt(2 pi^2/6) f0) < K = 1.00001
  (4.18) arc >= sqrt(q_d)/(1-q_d/4)^{1/2}, q_d < 3.8
  (4.32)/(4.33) Young split (x+y)^2 <= (1+beta)x^2 + (1+1/beta)y^2 with beta = .45, .8
  (4.38)/(A.8) bootstrap, at most 30 updates
  section 5.2  the rho search makes 25 midpoint trials
  section 2.3 / A.3  extend skips divisors |a| < 1e-6
"""
import csv, os
from math import sqrt, log2, pi, log

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
rows = []

print("=" * 78)
print("1. the radius chain, and its tightest link")
print("=" * 78)
chain = [("local target .103 vs atlas cap .125", 0.103, 0.125, "atlas must absorb merge distance"),
         ("atlas cap .125 vs validate .126", 0.125, 0.126, "B input range"),
         ("tau_mid .07 vs input .125", 0.07, 0.125, "child below parent"),
         ("tau_fine .016 vs input .07", 0.016, 0.07, "child below parent"),
         ("tau_fallback .011 vs input .016", 0.011, 0.016, "child below parent"),
         ("tau_fine .016 vs C hypothesis .03", 0.016, 0.03, "section 6.1 r <= .03"),
         ("tau_fallback .011 vs C hypothesis .03", 0.011, 0.03, "section 6.1 r <= .03"),
         ("C radius .03 vs Lemma 6.5 s < .1", 0.03, 0.1, "distinct-label lemma"),
         ("A.9 slack: R .126 + .249002 vs .377", 0.126 + 0.249002, 0.377, "A.23 scale")]
worst = None
for name, v, cap, why in chain:
    ratio = cap / v
    rows.append(dict(link=name, value=v, cap=cap, ratio=ratio, why=why))
    print(f"  {name:42s} {v:.6f} / cap {cap:.6f}: slack x{ratio:.4f}"
          f" ({100*(cap-v)/cap:5.2f}%)  [{why}]")
    if worst is None or ratio < worst[1]:
        worst = (name, ratio)
print(f"  => tightest link: {worst[0]} at x{worst[1]:.4f}; a 0.8% inflation of that radius breaks it.")

print()
print("=" * 78)
print("2. K = 1.00001 against f0 < 1e-6   (6.3)")
print("=" * 78)
a = sqrt(2 * pi * pi / 6)
print(f"K = sqrt(1 + a f0) with a = sqrt(2 pi^2/6) = {a:.6f}")
for f0 in (1e-6, 5e-6, 1e-5, 1.1e-5, 1.2e-5, 2e-5):
    print(f"  f0 = {f0:.1e}: K_needed = {sqrt(1+a*f0):.9f}  <= 1.00001 ? {sqrt(1+a*f0) <= 1.00001}")
print(f"  the stated f0 bound 1e-6 needs K >= {sqrt(1+a*1e-6):.9f}: K = 1.00001 leaves a factor")
print(f"  {((1.00001**2-1)/a)/1e-6:.1f}x slack in f0 (f0 may rise to {((1.00001**2-1)/a):.3e})")
print(f"  conversely K could be lowered to {sqrt(1+a*1e-6):.8f} (1.0000009) and still hold at f0=1e-6")

print()
print("=" * 78)
print("3. q_d < 3.8 against the structural bound q_d < 4   (4.18)")
print("=" * 78)
for q in (0.0, 1.9, 3.0, 3.5, 3.8, 3.9, 3.99, 3.999):
    fac = 1 / sqrt(1 - q / 4)
    print(f"  q_d = {q:6.3f}: arc multiplier 1/sqrt(1-q/4) = {fac:8.4f}")
print(f"  the multiplier is the only cost, and it diverges at q_d = 4: the constraint is q_d < 4,")
print(f"  3.8 buys a multiplier of 4.472 instead of infinity (5% margin in q_d, 4.472 vs .inf).")
print(f"  the search constant 3.8 is therefore a *shape* choice (accept at most 4.5x chord inflation)")

print()
print("=" * 78)
print("4. the Young split beta = .45 and .8   (4.32)/(4.33)")
print("=" * 78)
def bound(beta, A, B):
    return (1 + beta) * A + (1 + 1 / beta) * B
print("  (x+y)^2 <= (1+beta) x^2 + (1+1/beta) y^2 is optimal at beta* = sqrt(B/A)")
print(f"  beta=.45 => optimal when B/A = {0.45**2:.4f}; beta=.8 => B/A = {0.8**2:.4f}")
for rho in (0.0, 0.05, 0.2025, 0.4, 0.64, 1.0, 2.0, 4.0):
    A = 1.0
    B = rho
    opt = A + B + 2 * sqrt(A * B)
    for beta in (0.45, 0.8):
        f = bound(beta, A, B) / opt
        rows.append(dict(link=f"Young beta={beta}", value=rho, cap=f, ratio=1 / f,
                         why="B/A ratio vs penalty"))
        print(f"  B/A = {rho:6.4f}: beta={beta}: bound/optimal = {f:.4f}"
              f"  (penalty {100*(f-1):5.1f}%)")
    print()
print("  worst case over all ratios of the penalty at beta: 1+beta (when B=0), i.e. 1.45 and 1.8.")
print("  so a mis-set beta costs at most 45% / 80% in the tangent bound: bounded, never unbounded.")
print("  recommendation: state beta* = sqrt(B/A) and the actual ratio; or drop beta to .45 only")

print()
print("=" * 78)
print("5. the counts: 30 bootstrap updates, 25 midpoint trials, the 1e-6 divisor skip")
print("=" * 78)
print("  bootstrap: Prop. 4.13 accepts ANY finite number of improving steps (each preserves the")
print("  upper).  So 30 is a time cap, not a correctness constant.  If the per-step contraction")
print("  factor is lam, 30 steps close the gap by a factor lam^30:")
for lam in (0.5, 0.8, 0.9, 0.95, 0.99, 0.999):
    print(f"    lam={lam:5.3f}: lam^30 = {lam**30:.3e}; steps to reach 1e-6: "
          f"{log(1e-6)/log(lam):.1f}")
print("  => 30 steps polish the radius only when lam <= .63 (lam^30 <= 1e-6).  For lam >= .9 the")
print("     count is decorative: the bound is whatever the first few updates give.")
print()
print("  rho search: 25 midpoint trials on the tangent distance, over the scale .377 (A.23),")
print("  can resolve at best (bisection) 2^-25 of the range:")
print(f"    .377/2^25 = {0.377/2**25:.3e}, versus the 1e-8 additions used after every update")
print(f"    ceil(log2(.377/1e-8)) = {log2(0.377/1e-8):.2f} -> 26 trials would be complete; 25 gives"
      f" {0.377/2**25:.2e} > 1e-8.")
print("  => 25 is exactly one trial short of resolving the whole range to the 1e-8 scale, which is")
print("     consistent (the search must not resolve below its own additive margin).")
print()
print("  divisor skip |a| < 1e-6 in extend: the radius quotient is at most 3/|a|, each division")
print("  moves an endpoint by about eps*quotient; the endpoint margin is 1e-5:")
eps = 2.220446049250313e-16
for amin in (1e-12, 1e-11, 1e-10, 1e-8, 1e-6, 1e-4):
    q = 3 / amin
    print(f"    a_min={amin:.0e}: quotient <= {q:.1e}, endpoint movement ~{eps*q:.2e},"
          f" margin 1e-5 ok: {eps*q <= 1e-5}")
print(f"  => soundness needs a_min >= 3*eps/1e-5 = {3*eps/1e-5:.1e}; the chosen 1e-6 is "
      f"{(1e-6)/(3*eps/1e-5):.1e}x larger than that.  Raising it to 1e-4 only drops constraints.")

os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, "conditioning.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["link", "value", "cap", "ratio", "why"])
    w.writeheader(); w.writerows(rows)
print(f"\nwrote {os.path.join(DATA,'conditioning.csv')}")
