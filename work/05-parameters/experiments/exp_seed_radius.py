#!/usr/bin/env python3
"""R = 0.032, the enlargement 0.0320001, and the testBucket reuse threshold
RN2 = fl((fl(.032*112))**2) - 1e-4   (section 2.4, Appendix A.3).

Constraints recomputed here:
  (i)  coverage: a 9-d bin of side 1/N has half-diagonal 3/(2N) (Prop. 2.10), so R >= 3/(2N);
  (ii) reuse economy: one retained ball of radius R can hold at most (R/(3/(2N)))^9 bins,
       reach r = NR - 1.5 -- so R must exceed 3/(2N) by a decent factor.  (An earlier
       version of this line said 'ceiling rho^9 with rho = 2NR/3'; that bound was WRONG and is
       withdrawn -- see m6_conditioning.py section E2.)
  (iii) soundness of testBucket: success must imply ||q-u'|| < R, i.e. the comparison threshold
       must be fl((R*N)^2) minus a margin that dominates the evaluation error (< 1e-12, A.3);
  (iv) 0.0320001 absorbs the nine-phase binary64 midpoint error (< 1e-14, A.3);
  (v)  A.9 validates 0 <= R <= .126 for every B input.
"""
import csv, os, struct
from math import sqrt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
R, Rbig, Rval, N = 0.032, 0.0320001, 0.126, 112

print("=" * 78)
print("1. the two radii")
print("=" * 78)
print(f"R = {R!r}, enlarged R' = {Rbig!r}")
print(f"  enlargement: absolute {Rbig-R:.1e}, relative {(Rbig-R)/R:.3e}")
print(f"  A.3 bounds the nine-phase binary64 midpoint error by < 1e-14")
print(f"  ratio R'-R over that error: {(Rbig-R)/1e-14:.3e}   (needs >= 1)")
print(f"  bin half-diagonal at N=112: 3/(2N) = {3/(2*N):.9f} = {100*(3/(2*N))/R:.2f}% of R")
print(f"  so R/R_bin = {R/(3/(2*N)):.4f}; the number of previous-centre offsets (2.17) can"
      f" reach is 2869 offsets at N=112 (m6_conditioning.py, section E2)")

print()
print("=" * 78)
print("2. coverage window for R at each candidate N")
print("=" * 78)
rows = []
for n in (47, 56, 64, 96, 112, 128, 160, 189, 224):
    need = 3 / (2 * n)
    rho = R / need
    rows.append(dict(N=n, R_needed=need, rho=rho, reach=max(0.0, n * R - 1.5),
                     R_half_ok=int(R / 2 >= need), R_double=2 * R,
                     R_double_ok=int(2 * R <= Rval)))
    print(f"  N={n:4d}: needs R >= {need:.6f}; R={R} gives rho={rho:5.3f}, reach {max(0.0,n*R-1.5):8.4f};"
          f" R/2=0.016 ok: {int(R/2>=need)}; 2R=0.064 <= .126: {int(2*R<=Rval)}")

print()
print("=" * 78)
print("3. the testBucket threshold, computed in binary64 exactly as written")
print("=" * 78)
t = struct.unpack("d", struct.pack("d", (0.032 * 112)))
print(f"fl(.032*112) = {0.032*112!r}   (exactly representable? {0.032*112 == 3.584})")
sq = (0.032 * 112) ** 2
RN2 = sq - 1e-4
print(f"fl(fl(.032*112)^2) = {sq!r}")
print(f"RN2 = that - 1e-4  = {RN2!r}")
print(f"ideal (NR)^2 = {sq!r}; deficit = 1e-4 = {1e-4/sq:.3e} relative")
print(f"A.3: total error before the subtraction is below 1e-12")
print(f"  slack ratio 1e-4 / 1e-12 = {1e-4/1e-12:.3e}")
eff = sqrt(RN2) / N
print(f"effective certified radius sqrt(RN2)/N = {eff:.9f} = {eff/R:.9f} R")
print(f"  (so the 1e-4 costs {R-eff:.3e} in radius -- {100*(R-eff)/(3/(2*N)):.4f}% of the bin radius)")
print()
print("what the margin must dominate: the evaluation error of (2.17)-(2.19) on the RHS, < 1e-12")
for margin in (0.0, 1e-8, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2):
    thr = sq - margin
    print(f"  margin {margin:.0e}: threshold {thr:.9f}, certified radius "
          f"{sqrt(max(thr,0))/N:.9f} ({sqrt(max(thr,0))/N/R:.6f} R), "
          f"ratio to error {margin/1e-12:.1e}")

print()
print("=" * 78)
print("4. the hard-coded N: what happens to RN2 if N changes and the threshold does not")
print("=" * 78)
print("the source threshold is a function of N.  If N is changed and fl(.032*112) is kept:")
for n in (56, 64, 96, 112, 128, 160):
    rad = sqrt(RN2) / n
    print(f"  N={n:4d}: success would certify ||q-u'|| < sqrt(RN2)/N = {rad:.6f}"
          f" = {rad/R:6.3f} R   {'SOUND' if rad <= R+1e-12 else '*** UNSOUND: exceeds R ***'}")
print("  => the threshold must be written fl((R*N)^2) with R,N symbolic; at N <= 96 the literal")
print("     form would certify balls up to 2R and break Proposition 2.10.")
print("  Remedy: RN2 = fl((fl(R*N))^2) - c with c >= 1e-12; c = 1e-6 already gives 1e6x margin.")

os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, "seed_radius.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(f"\nwrote {os.path.join(DATA,'seed_radius.csv')}")
