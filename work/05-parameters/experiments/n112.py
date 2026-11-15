#!/usr/bin/env python3
"""N = 112: every constraint on the seed-cover bin count, and its cost curve.

All arithmetic is exact (integers / Fractions) except the cost model, which is
flagged.  Run: python3 experiments/n112.py
"""
from math import comb, log, sqrt, ceil

def hr(t): print("\n== %s" % t)

# ---------------------------------------------------------------- basics
hr("binomial counts (eq. 2.6, 2.10)")
for N in (47, 56, 64, 96, 112, 128, 160, 189, 224):
    print("N=%3d  C(N+4,5)=%14d  C(N+3,4)=%10d  N*C(N+3,4)=%14d"
          % (N, comb(N+4, 5), comb(N+3, 4), N*comb(N+3, 4)))

# --------------------------------------------------- constraint 1: covering
# Prop 2.10: a retained midpoint covers its bin, whose circumradius in the
# nine seed coordinates q=(x1..x5,y2..y5) is sqrt(9)/(2N) = 3/(2N).
hr("C1 covering radius: 3/(2N) <= R")
R = 0.032
print("3/(2N) <= %.6g  <=>  N >= 3/(2R) = %.6f  -> N >= %d"
      % (R, 3/(2*R), ceil(3/(2*R))))
for N in (46, 47, 56, 112, 128, 189):
    print("  N=%3d  3/(2N)=%.6f  ratio to R=%.4f" % (N, 3/(2*N), (3/(2*N))/R))

# ------------------------------------------------- constraint 2: 32-bit array
hr("C2 signed-32-bit array: C(N+4,5) < 2**31 = %d" % 2**31)
M = 1
while comb(M+1+4, 5) < 2**31:
    M += 1
print("largest N with C(N+4,5)<2^31: N=%d (C(%d,5)=%d < 2^31); N=%d gives C(%d,5)=%d >= 2^31"
      % (M, M+4, comb(M+4, 5), M+1, M+5, comb(M+5, 5)))
print("so the 32-bit argument alone permits N <= %d; the int8 claim of Sec 7.3 permits N <= 128" % M)

# ------------------------------------------------------ constraint 3: int8
hr("C3 int8 storage of bin differences (Sec 7.3: '[-111,111] ... int8_t')")
for N in (112, 128, 129, 160, 189, 224):
    d = N-1
    print("  N=%3d  max |bin difference|=%3d  fits int8[-128,127]? %s  9*d^2=%d fits int32? %s"
          % (N, d, d <= 127, 9*d*d, 9*d*d < 2**31))

# ------------------------------------------------ constraint 4: gap filter
hr("C4 gap filter (2.8): thresholds 1-(l-1)/N and 1-(l+2)/N, Lemma 2.5 bound w=1/N")
print("  separation of thresholds = 3/N ; perturbation bound w = 1/N ; ratio = 3 for every N")

# --------------------------------------- constraint 5: reuse threshold RN2
hr("C5 reuse threshold RN2 = fl((fl(.032*N))^2) - 1e-4  (A.3)")
for N in (112, 128, 189):
    t = (0.032*N)**2 - 1e-4
    r = sqrt(t)/N
    print("  N=%3d  (NR)^2=%.6f  RN2=%.6f  equivalent radius=%.9f cycles"
          % (N, (0.032*N)**2, t, r))
print("  1e-4 in (Nr)^2 units = a radius reduction of 1e-4/(2*112*0.032) = %.3e cycles"
      % (1e-4/(2*112*0.032)))
print("  radius inflation .032 -> .0320001 costs 1e-7 cycles, i.e. %.3e in (Nr)^2 units at N=112"
      % ((112*0.0320001)**2 - (112*0.032)**2))
print("  A.3 states the pre-subtraction error is < 1e-12, so 1e-4 over-covers it by %.1e x"
      % (1e-4/1e-12))

# ------------------------------------------------------- constraint 6: R cap
hr("C6 upper bound on R from Sec. 3 (A.4/A.7 budgets: Rs=2*pi*R < .203)")
print("  Rs = 2*pi*(R+1e-7) < .203  <=>  R < %.8f" % (.203/(2*3.141592653589793)))
print("  at R=.032: Rs=%.6f, headroom %.4f%%" % (2*3.141592653589793*0.0320001,
      100*(0.203/(2*3.141592653589793*0.0320001)-1)))

# --------------------------------------------- hard reuse crossover
hr("C7 hard reuse crossover: a bin can be assimilated only if delta(N) >= 1/N")
print("delta(N) = R - 3/(2N) >= 1/N  <=>  R >= 5/(2N)  <=>  N >= 5/(2R) = %.3f" % (5/(2*R)))
for N in (70, 78, 79, 80, 112):
    print("  N=%3d  delta=%.6f  1/N=%.6f  reuse possible? %s"
          % (N, R-3/(2*N), 1.0/N, R-3/(2*N) >= 1.0/N))
print("  so for N <= 78 every admissible bin pair becomes a Stage-A seed: no compression at all.")

# ------------------------------------------------------ cost model
hr("cost model calibrated on the recorded run (Table 1, Sec 7.5)")
PAIRS = 151744086          # Table 1
CENTRES = 249878           # Table 1
COVER_S, A_S = 621.59, 2020.32
a = COVER_S/PAIRS
b = A_S/CENTRES
print("a = %.4e s per enumerated pair (621.59 s / 151,744,086)" % a)
print("b = %.4e s per retained centre (2020.32 s / 249,878)" % b)

# retained-centre model: greedy maximal delta-separated set on the 5-dim seed
# manifold, delta = R - 3/(2N).  Count(delta) = C0 * delta^-5, fitted at N=112.
DIM = 5
d112 = R - 3/(2*112)
print("effective separation delta(N) = R - 3/(2N); delta(112) = %.6f" % d112)
C0 = CENTRES * d112**DIM
print("fitted C0 = %.4e so that the model reproduces 249,878 at N=112" % C0)

def pairs(N):   # enumerated X-side bin pairs: all C(N+4,5) tuples before filters
    return comb(N+4, 5)
def model_centres(N):
    d = R - 3/(2*N)
    if d <= 1e-6:
        return pairs(N)
    return min(pairs(N), C0*d**(-DIM))
def cost(N):
    return a*pairs(N) + b*model_centres(N)

hr("cost curve")
print("%4s %16s %14s %13s %12s %10s" % ("N", "tuples", "delta", "centres", "seconds", "vs 112"))
base = cost(112)
rows = []
for N in (47, 50, 56, 64, 80, 96, 104, 112, 120, 128, 144, 160, 189, 224):
    rows.append((N, pairs(N), R-3/(2*N), model_centres(N), cost(N), cost(N)/base))
    print("%4d %16d %14.6f %13.0f %12.0f %10.3f" % rows[-1])

hr("what breaks at half (56) and double (224)")
for N in (56, 224):
    print("N=%d: 3/(2N)=%.4f (C1 %s); C(N+4,5)=%d (C2 %s); max diff=%d (C3 %s); predicted centres %.3g"
          % (N, 3/(2*N), "OK" if 3/(2*N) <= R else "FAILS",
             comb(N+4, 5), "OK" if comb(N+4, 5) < 2**31 else "FAILS",
             N-1, "OK" if N-1 <= 127 else "FAILS", model_centres(N)))

hr("sensitivity of the optimum to the packing exponent d")
print("%3s %10s %10s %12s %12s" % ("d", "argmin N", "cost ratio", "centres(56)", "centres(128)"))
for DIM in (4, 5, 6):
    C0d = CENTRES*d112**DIM
    def cen(N, C0d=C0d, DIM=DIM):
        d = R - 3/(2*N)
        return min(pairs(N), C0d*d**(-DIM)) if d > 1e-6 else pairs(N)
    def cst(N, cen=cen):
        return a*pairs(N) + b*cen(N)
    cand = [N for N in range(47, 190)]
    best = min(cand, key=cst)
    print("%3d %10d %10.3f %12.3g %12.3g"
          % (DIM, best, cst(best)/cst(112), cen(56), cen(128)))

# ------------------------------------------------------------------ CSV
import csv
with open("data/m5-cost-curve-N.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["N", "tuples_C(N+4,5)", "tail_count_C(N+3,4)", "fresh_centre_dist_3_over_2N",
                "delta_eff_R_minus_3_over_2N", "modelled_retained_centres",
                "modelled_seconds", "ratio_to_N112", "int8_ok", "int32_ok"])
    for (N, t, d, c, s, r) in rows:
        w.writerow([N, t, comb(N+3, 4), "%.6f" % (3/(2*N)), "%.6f" % d,
                    int(round(c)), int(round(s)), "%.3f" % r,
                    N-1 <= 127, comb(N+4, 5) < 2**31])
print("\nwrote data/m5-cost-curve-N.csv")
