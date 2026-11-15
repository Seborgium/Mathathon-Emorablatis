#!/usr/bin/env python3
"""Direction d4: global conditioning of the proof's numeric chain.

For each quantitative input of the pipeline this script perturbs the input and propagates the
perturbation through the paper's own displayed formulas to the margin that consumes it, then
reports (i) the amplification, (ii) the tolerance at which that link fails, (iii) the first link
that fails when a whole class of quantities is inflated uniformly.

Every formula used is quoted from the paper in the comment above its use; nothing is fitted.
Section E is corroboration only (independent recomputation of numbers other members report) and
contains two explicit retractions of claims I made in an earlier submission.
"""
import csv, os
from math import comb, sqrt, ceil, log2, pi, gamma, log

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
rows = []
def add(link, inp, ampl, slack, tol, verdict):
    rows.append(dict(link=link, input=inp, amplification=ampl, slack=slack,
                     tolerance=tol, verdict=verdict))

print("=" * 92)
print("A. The chain as 23 comparisons: reserve = margin / established error")
print("=" * 92)
# (path, [(component, established error)], margin)
T = [("seed gap / direct support", [("gap",1e-14),("support",1e-11)], 1e-8),
     ("shared-coordinate numerator", [("num",3.5e-11)], 1e-7),
     ("shared-coordinate endpoints", [("end",1e-7)], 1e-5),
     ("seed dual support", [("dual",1e-4)], .01),
     ("A flat norm", [("flat",1e-6)], 1e-5),
     ("A directional comparison", [("dir",4e-6)], 1e-4),
     ("Root identity Frobenius", [("id",5e-8)], 2e-6),
     ("Root orthogonal", [("orth",1e-10)], 1e-8),
     ("Root horizontal", [("hor",1e-11)], 1e-8),
     ("tensor transformed row bound", [("tensor",1e-6)], 2e-4),
     ("Candidate direct support", [("direct",2e-6)], 1e-4),
     ("Candidate external tangent", [("tangent",1.2e-4)], 1.5e-4),
     ("G entry (first)", [("G1",1e-11)], 1e-7),
     ("G entry (second)", [("G2",1e-9)], 1e-7),
     ("spectral row bound", [("row",3e-13)], 1e-10),
     ("spectral fourth-norm", [("fro4",1e-10)], 2e-7),
     ("bootstrap update", [("boot",1e-12)], 1e-8),
     ("B projected normal", [("proj",5e-11)], 1e-8),
     ("B local update", [("loc",1e-13)], 1e-8),
     ("B cross-Gram spectral", [("cross",2e-9)], 1e-7),
     ("C direct / directional", [("Cd",1e-9)], 2e-7),
     ("C joint support", [("joint",1e-8)], 3e-7)]
comps = [(f"{p} [{c}]", e, m) for p, es, m in T for c, e in es]
comps.sort(key=lambda r: r[2] / r[1])
for name, e, m in comps:
    print(f"  {name:44s} error {e:9.2e}  margin {m:9.2e}  reserve {m/e:9.3g}")
lam = comps[0]
print()
print(f"  min reserve lambda* = {lam[2]/lam[1]:.4g}  ({lam[0]})")
print(f"  uniform inflation of EVERY established error is survived up to t = {lam[2]/lam[1]:.4g}")
print(f"  second: {comps[1][0]} at {comps[1][2]/comps[1][1]:.4g};"
      f" third: {comps[2][0]} at {comps[2][2]/comps[2][1]:.4g}")
print(f"  median reserve {sorted(m/e for _,e,m in comps)[len(comps)//2]:.3g} over {len(comps)} components")
add("uniform error inflation", "all established errors", 1.0, lam[2]/lam[1],
    f"{lam[2]/lam[1]:.4g}x", f"first failure at {lam[0]}")

print()
print("=" * 92)
print("B. Single-input tolerances: perturb one input through the stated formula")
print("=" * 92)
# (6.3): ||A/sqrt6||_op <= K = sqrt(1 + a f0), a = sqrt(2 pi^2/6), f0 < 1e-6, K = 1.00001
a = sqrt(2 * pi * pi / 6)
K = 1.00001
f0tol = (K * K - 1) / a
print(f"1. f0 -> K    K(f0) = sqrt(1 + {a:.4f} f0).  dK/df0 = a/(2K) = {a/(2*K):.4f}.")
print(f"   at f0 = 1e-6, K = {sqrt(1+a*1e-6):.9f}: reserve 1.00001/K = {K/sqrt(1+a*1e-6):.6f}")
print(f"   tolerance f0 <= {f0tol:.4e} = {f0tol/1e-6:.2f}x the stated 1e-6; elasticity dlnK/dlnf0 ="
      f" {a*1e-6/(2*(1+a*1e-6)):.2e} (K is essentially insensitive to f0)")
add("f0 -> K", "f0 (Hadamard residual)", a/(2*K), f"{f0tol/1e-6:.2f}x", f"{f0tol:.3e}",
    "K is not where the chain is tight")

# (4.18)/(4.32): arc multiplier g(q) = 1/sqrt(1-q/4); q_d < 3.8
def g(q): return 1 / sqrt(1 - q / 4)
def dg(q): return (1/8) * (1 - q/4) ** -1.5
print(f"2. q_d -> arc   arc = sqrt(q_d) g(q_d), g = {g(3.8):.4f} at 3.8, g' = {dg(3.8):.3f}.")
print(f"   d arc / d q_d at 3.8 = (g/2 + 3.8 g')/sqrt(3.8) = {(g(3.8)/2 + 3.8*dg(3.8))/sqrt(3.8):.4f}")
print(f"   elasticity dln(arc)/dln(q_d) = {0.5 + 3.8*dg(3.8)/g(3.8):.3f}")
print(f"   tolerance q_d < 4 (structural): 3.8 -> 4 is {4/3.8-1:+.3%}; at 4 the multiplier diverges")
add("q_d -> arc bound", "q_d", 0.5 + 3.8*dg(3.8)/g(3.8), f"{4/3.8-1:.4%}", "q_d < 4 (3.8 chosen)",
    "most elastic constant in the paper: 1% in q_d -> 9.5% in the arc bound")

# Young split (4.32)/(4.33): (x+y)^2 <= (1+b)x^2 + (1+1/b)y^2
def young(beta, A, B): return (1 + beta) * A + (1 + 1 / beta) * B
print(f"3. beta -> tangent variance.  bound(beta)/bound(beta*) <= 1+beta, with beta* = sqrt(B/A).")
print(f"   beta=.45: optimal at B/A = {0.45**2:.4f}; beta=.8: at {0.8**2:.4f};")
print(f"   worst-case penalty 1+beta = 1.45 and 1.8: a mis-set beta is bounded, never singular")
add("beta -> tangent covariance", "beta", 1 + 0.45, "1.8x worst", "any beta>0", "bounded penalty")

# (4.38)/(4.6): nP(s) = n0 + id s + C s^2 ; update decreases s iff nP(s) < s
print(f"4. C -> bootstrap.  (4.38) replaces s by sqrt(nP(s)^2 + (1+ort)t0^2); it is accepted only")
print(f"   when it decreases, which needs nP(s) = n0 + id s + C s^2 < s, i.e.  C < 1/s - id - n0/s^2.")
for s in (1e-2, 1.6e-2, 3e-2, 5e-2, 7e-2, 1.03e-1, 1.25e-1):
    print(f"     s = {s:.4f}: needs C < {1/s - 1e-4 - 1e-6/s**2:8.3f}   (admitted C < 20: "
          f"{'ok' if 1/s - 1e-4 - 1e-6/s**2 > 20 else 'FAILS'})")
print(f"   so the admitted range C < 20 guarantees a decreasing bootstrap only for s < ~0.05, while")
print(f"   the local targets that actually occur are .103 and .125.  Above s = .05 the ellipsoid path")
print(f"   is inert: the update increases s, is rejected, and coverage falls back to the initial s0")
print(f"   (sound, but the 'finite improvement' of Prop. 4.13 does nothing there).  Not a soundness")
print(f"   failure -- a silent loss of the improvement mechanism in exactly the top of the radius range.")
add("C -> bootstrap improvement", "C (normal polynomial)", 0.0, "C<20 admitted vs C<1/s needed",
    "s < 0.05 for C = 20", "range and radii are mutually inconsistent above s=.05")

# R -> N (coverage), R -> validate
R, N = 0.032, 112
print(f"5. R -> coverage.  N >= 3/(2R): dN/dR = -3/(2R^2) = {-3/(2*R*R):.1f} per unit R; elasticity -1.")
print(f"   tolerance down R >= 3/(2N) = {3/(2*N):.6f} ({100*3/(2*N)/R:.2f}% of R), up R <= .126"
      f" ({.126/R:.2f}x R)")
add("R -> coverage / validate", "R", -1.0, f"{100*(1-3/(2*N)/R):.1f}% down, {100*(1-R/0.126):.1f}% up",
    "R in [0.013393, 0.126]", "spans a factor 9.4; the value 0.032 is a choice inside it")

# w -> gap filter: exactly tight
print(f"6. w -> gap filter (2.8).  The filter's derivation is x5 <= (l+1)/N, gx >= 1-(l+1)/N,")
print(f"   gy >= gx, gy,mid >= gy - w: the spread between the exact bound and the threshold is")
print(f"   exactly w.  So the reserve on Lemma 2.5 is exactly 1 at every N: the proof spends its")
print(f"   whole perturbation allowance on this one comparison, with only the 1e-8 of A.3 behind it.")
add("w -> gap filter (2.8)", "w = 1/N", 1.0, "exactly 1 (zero analytic reserve)", "w + dw > w",
    "the tightest ANALYTIC link: any unrecognised perturbation breaks it")

# tau -> L -> boxes: (2L+1)^k
print(f"7. w -> box count.  L = ceil(E/w + .500001), boxes = (2L+1)^k, so dln(boxes)/dln(w) = -k.")
for k in (5, 7, 10):
    print(f"     k={k:2d}: 1% smaller w costs {k}% more boxes; 10% costs {10*k}%")
print(f"   elasticity -k, the largest cost amplification in the pipeline; with the 5e7 cap it is")
print(f"   also the reason w cannot be pushed below the values used (see the L/k table).")
add("w -> box count", "w", -5.0, "57% of the cap at pass 2", "w >= .005 at pass 2 (k=5)",
    "elasticity -k: the costliest amplification")

# M -> X_M -> clustering threshold (section 6.3)
print(f"8. M -> clustering.  X_M = sqrt(29/6)/(2M) = {sqrt(29/6):.6f}/(2M); threshold (.042-1.11/M)^2.")
print(f"   elasticity of X_M in M is -1; the reserve .042/X_M is .46 at M=12, .92 at M=24, 1.83 at")
print(f"   M=48, 3.67 at M=96.  The base is negative for M <= 26 (1.11/.042 = {1.11/.042:.4f}).")
add("M -> clustering cutoff", "M", -1.0, "reserve .042/X_M = .46 (M=12), .92 (M=24), 3.67 (M=96)",
    "M >= 27 for a positive base", "sign hidden by the square (F2)")

print()
print("=" * 92)
print("C. Classes of perturbation and the FIRST link that fails")
print("=" * 92)
print(f"  uniform inflation of established errors : {lam[0]}, at t = {lam[2]/lam[1]:.4g}x")
print(f"  uniform inflation of record radii       : atlas cap .125 vs validate .126, at t ="
      f" {.126/.125:.4f}x  (0.79%)")
print(f"  uniform inflation of the A.9 scale total: R + .249002 = .375002 vs .377, at t ="
      f" {.377/(.126+.249002):.4f}x  (0.53%)")
print(f"  uniform inflation of the tangent error  : .00012 -> .00015, at t = {1.5e-4/1.2e-4:.4g}x")
print(f"  f0: {f0tol/1e-6:.1f}x;  q_d: {4/3.8:.3f}x to the singular value 4;  R down:"
      f" {3/(2*N)/R:.3f}x;  N up: {128/112:.3f}x (int8), {189/112:.3f}x (32-bit)")
print("  => the chain does not break first on a numerical error at all: its tightest link is a")
print("     RADIUS proportion (0.8%) and its tightest analytic link is a zero-reserve filter.  The")
print("     1.25x tangent reserve is the third story, and it is the only one stated in radians.")

print()
print("=" * 92)
print("D. Precision: which comparisons binary32 could not carry")
print("=" * 92)
eps32, eps64 = 2.0 ** -23, 2.0 ** -52
below = [(n, m) for n, e, m in comps if m < eps32]
print(f"  binary32 eps = {eps32:.3e}; binary64 eps = {eps64:.3e}")
print(f"  tabulated margins below binary32 eps: {len(below)} of {len(comps)} ->")
print("   ", ", ".join(f"{n.split('[')[1][:-1]}={m:.0e}" for n, m in below))
print(f"  => binary64 is required by {len(below)} comparisons; {len(comps)-len(below)} would survive")
print(f"     in binary32.  The requirement is not uniform: it comes from the {len(below)} small ones.")
add("precision", "binary32 vs binary64", 0.0, f"{len(below)}/{len(comps)} margins < eps32",
    "binary64 only", f"{len(below)} comparisons rule out binary32")

print()
print("=" * 92)
print("E. Corroboration (independent recomputation) and two retractions")
print("=" * 92)
print("E1 corroborated exactly, by this script:")
print(f"   C(116,5) = {comb(116,5):,}   C(115,4) = {comb(115,4):,}")
n32 = max(n for n in range(1, 400) if comb(n+4,5) < 2**31)
print(f"   largest N with C(N+4,5) < 2^31: N = {n32}, C(193,5) = {comb(193,5):,}")
for n in (56, 112, 224):
    print(f"   N={n:3d}: 3/(2N) = {3/(2*n):.6f} = {100*(3/(2*n))/R:.2f}% of R;"
          f"  C(N+4,5) = {comb(n+4,5):,}")

def lattice(S, d=9):
    dp = [[0]*(S+1) for _ in range(d+1)]
    dp[0][0] = 1
    steps = [(0, 1)] + [(v*v, 2) for v in range(1, int(sqrt(S))+1)]
    for i in range(d):
        for s in range(S+1):
            c = dp[i][s]
            if c:
                for sq, w in steps:
                    if s + sq <= S:
                        dp[i+1][s+sq] += c*w
    return sum(dp[d])
print()
print("E2 the reuse reach, exactly (this replaces my earlier (2NR/3)^9 ceiling, which was WRONG):")
print("   A previous centre can be tried only for a bin whose grid offset k = N(u-u') satisfies")
print("   ||k + h|| <= NR with |h_j| <= 1/2 (2.17), so the offsets that can ever be reached are")
print("   #{k in Z^9 : ||k|| <= NR - 1.5}.  Exact counts:")
for n in (47, 56, 64, 96, 112, 128, 160, 189, 224):
    reach = max(0.0, n * R - 1.5)
    print(f"     N={n:4d}: NR-1.5 = {reach:6.3f} -> {lattice(int(reach*reach)):>10,} offsets k")
print(f"   at N=112 this is {lattice(4)} = 2869, which matches the reach another member reported.")
print(f"   at N=56 it is 1 (only k=0): reuse degenerates to exact-coincidence. That is the")
print(f"   defensible form of 'halving N kills reuse'.")
print()
print("   The number of unit bins a radius-R ball can contain at all is the same count with")
print(f"   r = NR: at N=112, #{{||k|| <= 3.584}} = {lattice(int((112*R)**2)):,} (volume estimate"
      f" {3.2985*(112*R)**9:,.0f}).")
print(f"   The run's 607 = pairs/centres is a compression ratio that mixes FILTERING with reuse")
print(f"   and is 607 << 284055, so it says nothing about how full the balls were.  My earlier")
print(f"   comparison '607 is 23.9% of a ceiling of 2538' was a category error: RETRACTED.")
print(f"   My earlier centre-count extrapolations (4.6e6 at N=56, 1.58e4 at N=224) fitted one")
print(f"   constant to one datum and are also RETRACTED.  What the record does determine: pairs")
print(f"   processed 151,744,086 in 621.59 s (4.10 us/pair), 22,829 x-lists retained, 249,878")
print(f"   centres; nothing separates filtering from reuse without instrumentation.")
print()
print("E3 scope correction for the k finding (F3): at the three specified (E,w) pairs the")
print("   per-axis counts are 23, 31, 11 and the 5e7 cap admits 23^5, 31^5, 11^7 but not the next")
print("   powers, so records in the run have k <= 5 (passes 1-2) and k <= 7 (pass 3).  The claim")
print("   'k<=10 is unreachable at every admitted w' is FALSE: with w=.05 and a small-radius")
print("   record E~.016, L = ceil(.016/.05+.5) = 1, 3^10 = 59049 <= 5e7, so k=10 is admissible.")
print(f"   correct statement kept: k<=10 is unreachable at the three widths used, not in general.")

os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, "m6_conditioning.csv"), "w", newline="") as fh:
    w_ = csv.DictWriter(fh, fieldnames=["link", "input", "amplification", "slack", "tolerance", "verdict"])
    w_.writeheader(); w_.writerows(rows)
print(f"\nwrote {os.path.join(DATA,'m6_conditioning.csv')}")
