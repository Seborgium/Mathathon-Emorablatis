#!/usr/bin/env python3
"""Every remaining constant: the inequality, the slack, the sensitivity.
Run: python3 experiments/margins.py
"""
from math import pi, sqrt, ceil, log2
import csv

def hr(t): print("\n== %s" % t)

# ------------------------------------------------------------------ R
hr("R = 0.032 and the enlarged 0.0320001 (Sec. 2.4, Prop. 2.10, A.3)")
R = 0.032
lo = 3/(2*112)
hi = 0.203/(2*pi)
print("lower: 3/(2N) = %.7f at N=112 -> R >= %.6f (slack %.2fx)" % (lo, lo, R/lo))
print("upper: Rs = 2*pi*(R+1e-7) < .203  ->  R <= %.8f (slack %.4f%%)"
      % (hi, 100*(hi/R-1)))
print("the enlargement .032 -> .0320001 (1e-7) is 1.0e+7 x the A.3 phase-error bound 1e-14")
print("and 1e-7/0.032 = %.2e relative.  Free, because nothing downstream is compared to R itself."
      % (1e-7/R))

# ------------------------------------------------- reuse threshold RN2
hr("reuse threshold RSQ = fl((fl(.032*112))^2) - 1e-4 (A.3, testBucket)")
t = (0.032*112)**2
print("(0.032*112)^2 = %.6f ; threshold = %.6f" % (t, t-1e-4))
print("1e-4 corresponds to a radius reduction of %.3e cycles" % (1e-4/(2*112*0.032)))
print("A.3 bounds the pre-subtraction error by 1e-12, so 1e-4 over-covers by %.0e x" % (1e-4/1e-12))
print("the .032 -> .0320001 inflation costs %.3e in the same squared units, i.e. %.0f%% of the 1e-4"
      % ((112*0.0320001)**2-(112*0.032)**2, 100*((112*0.0320001)**2-(112*0.032)**2)/1e-4))
print("caution: 1e-4 is not scale free.  At N=189 the same 1e-4 is %.3e cycles, still safe;"
      % (1e-4/(2*189*0.032)))

# ------------------------------------------------------- U(2) grid
hr("U(2) grid: Nu = 16 base, subdivided to 32, 64, ..., 512; h = pi/Nu")
for Nu in (16, 32, 64, 128, 512):
    print("  Nu=%3d  h=pi/Nu=%.6f rad  cells=Nu^4/8=%d  cell edge in cycles=%.4f"
          % (Nu, pi/Nu, Nu**4//8, 1.0/Nu))
print("cell bin counts Nu/2, Nu/4, Nu, Nu  (Lemma 3.3), so Nu^4/8 cells, requiring Nu divisible by 4")
print("Nu=16 -> cells within one base cell of radius h=%.4f rad; the local target .103 (cycles)" % (pi/16))
print("h in cycles = 1/16/2 = %.5f ; the .103 target is %.1f x a half cell" % (1/32, .103/(1/32)))

# ---------------------------------------------- local / global targets
hr("local target .103 and global (atlas) target .125")
print(".103 < .125: the local test certifies .103, atlas merges may grow a radius to .125")
print("merge headroom = .125-.103 = %.3f = %.1f%% of .103" % (.125-.103, 100*(.125-.103)/.103))
print("Stage C requires r <= .03 (Sec. 6.1) so .125 must be reduced by B: "
      ".07 -> .016 -> .011 all < .03: %s" % (.07, ))

# --------------------------------------------------------- (tau,w)
hr("three (tau,w) pairs and the constraints on them")
print("stated admissible ranges (Sec. 5.6): 1e-4 <= tau <= .126, 1e-4 <= w <= .05, 0 <= k <= 10")
# E is built from the INPUT radius the pass receives, not from tau:
# pass 1 gets A's atlas cap .125, pass 2 gets mid's tau .07, pass 3 gets fine's tau .016.
for (tau, w, Rin) in ((0.07, 0.013, 0.125), (0.016, 0.005, 0.07), (0.011, 0.0038, 0.016)):
    E = Rin + 1e-7
    L = ceil(E/w + 0.500001)
    print("  tau=%.4f w=%.4f Rin=%.3f  w/tau=%.4f  E/w=%.3f  L=%3d  boxes/axis=%3d  (L+1/2)w=%.5f >= E=%0.5f -> %s"
          % (tau, w, Rin, w/tau, E/w, L, 2*L+1, (L+0.5)*w, E, (L+0.5)*w >= E))
print("  the grid covers [-E,E] only if (L+1/2)w >= E:  all three hold with slack")
for (tau, w, Rin) in ((0.07, 0.013, 0.125), (0.016, 0.005, 0.07), (0.011, 0.0038, 0.016)):
    E = Rin + 1e-7; L = ceil(E/w + 0.500001)
    print("    tau=%.4f: (L+1/2)w = %.5f  vs E = %.7f  ratio %.4f ; w/tau = %.3f"
          % (tau, (L+0.5)*w, E, (L+0.5)*w/E, w/tau))
print("  why w must be below the child radius (Lemma 5.5): a child box of halfwidth w/2 in k")
print("  coordinates over-estimates the radius by at most sqrt(k)*w/2, so a pass with cap tau")
print("  only certifies children of radius <= tau - sqrt(k)*w/2:")
for (tau, w) in ((0.07, 0.013), (0.016, 0.005), (0.011, 0.0038)):
    for k in (5, 7):
        over = (k**0.5)*w/2
        print("    tau=%.4f w=%.4f k=%d: sqrt(k)w/2=%.5f  tau-over=%.5f  slack %.2fx"
              % (tau, w, k, over, tau-over, tau/over))
print("  corners: tau_max=.126 with w_min=1e-4 gives L=ceil(1260.500001)=%d, axis %d <= 2524 (Sec 7.3)"
      % (ceil(.126/1e-4+0.500001), 2*ceil(.126/1e-4+0.500001)+1))
print("  so 1e-4 and .126 are locked together by the 2524 axis bound: %s"
      % ((ceil(.126/1e-4+0.5)*1e-4*2+1e-4) >= .126))

# ------------------------------------------------ the small constants
hr("the undiscussed arithmetic constants")
print("K = 1.00001: bound on |T entries|.  omega < 1e-5 gives ||T||^2 <= 1+1e-5,")
print("   so 1.00001 covers sqrt(1+1e-5) = %.9f with slack %.2fx"
      % (sqrt(1+1e-5), 1.00001/sqrt(1+1e-5)))
print("q_d < 3.8: the arc bound uses 1/sqrt(1-q_d/4), which needs q_d < 4 (hard).")
print("   3.8 leaves 5%% and inflates the chord by at most 1/sqrt(1-3.8/4) = %.3f x" % (1/sqrt(1-3.8/4)))
print("beta = .45 and .8: Lemma 4.11 holds for every beta > 0; .45 gives 1+beta=1.45,"
      " 1+1/beta=%.3f; .8 gives 1.8, %.3f.  No inequality pins either value."
      % (1+1/0.45, 1+1/0.8))
print(".64 eigenvalue split: |eigenvalue|<.64 proposes a T column.  Spectral values of the")
print("   25x25 structural Jacobian are <=1 in the admissible range, so doubling to 1.28 gives k=0,")
print("   and Sec. 5.6 makes an unresolved cell with k=0 a parent FAILURE.  Halving only costs work.")
print("30 bootstrap updates: the guard is 0<=init<3, 0<=t<10, C<20, s<=3.00001, n0+ids+Cs^2<181.")
print("   A cap can only stop an improvement, and stopping keeps the previous valid upper (Sec. 4.6),")
print("   so 30 is a work bound, not a soundness bound.")
E = .126+1e-7
print("25 midpoint trials: the bracket is [0, 1.01a] with a <= .126, so 25 halvings leave")
print("   %.3e, while the acceptance test needs rho > 1e-7.  trials needed = ceil(log2(1.01*.126/1e-7)) = %d"
      % (1.01*.126/2**25, ceil(log2(1.01*.126/1e-7))))
print("1e-6 divisor skip in extend: skips |a|<1e-6, which only REMOVES a constraint,")
print("   so the interval is too large and the filter stays necessary (safe by construction).")
print("   at |a| just above 1e-6 the quotient is bounded by 112/1e-6 = 1.12e8 < 1.2e8 (A.3)")

# ------------------------------------------------- closing table
hr("Appendix A closing table: established error, margin, ratio")
T = [("seed gap / direct support", 1e-14, 1e-8),
     ("seed direct support", 1e-11, 1e-8),
     ("shared-coordinate numerator", 3.5e-11, 1e-7),
     ("shared-coordinate endpoints", 1e-7, 1e-5),
     ("seed dual support", 1e-4, .01),
     ("A flat norm", 1e-6, 1e-5),
     ("A directional comparison", 4e-6, .0001),
     ("Root identity Frobenius", 5e-8, 2e-6),
     ("Root orthogonal check", 1e-10, 1e-8),
     ("Root horizontal check", 1e-11, 1e-8),
     ("tensor transformed row bound", 1e-6, .0002),
     ("Candidate direct support", 2e-6, .0001),
     ("Candidate external tangent error", 1.2e-4, 1.5e-4),
     ("first G entry error", 1e-11, 1e-7),
     ("second G entry error", 1e-9, 1e-7),
     ("spectral row bound", 3e-13, 1e-10),
     ("spectral fourth-norm bound", 1e-10, 2e-7),
     ("bootstrap update", 1e-12, 1e-8),
     ("B projected normal", 5e-11, 1e-8),
     ("B local update", 1e-13, 1e-8),
     ("B cross-Gram spectral perturbation", 2e-9, 1e-7),
     ("C direct / directional comparison", 1e-9, 2e-7),
     ("C joint support", 1e-8, 3e-7)]
print("%-38s %12s %12s %10s" % ("path", "error", "margin", "ratio"))
rows = []
for (name, err, mar) in T:
    rows.append((name, err, mar, mar/err))
    print("%-38s %12.3g %12.3g %10.2f" % (name, err, mar, mar/err))
rr = sorted(rows, key=lambda r: r[3])
print("\ntightest three: " + "; ".join("%s %.2fx" % (r[0], r[3]) for r in rr[:3]))
print("loosest three:  " + "; ".join("%s %.0fx" % (r[0], r[3]) for r in rr[-3:]))
print("median ratio %.1f" % sorted(r[3] for r in rows)[len(rows)//2])

with open("data/m5-margins.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["path", "established_error", "margin", "ratio"])
    for (name, err, mar, rat) in rows:
        w.writerow([name, err, mar, "%.3f" % rat])
print("\nwrote data/m5-margins.csv")
