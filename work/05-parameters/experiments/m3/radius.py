#!/usr/bin/env python3
"""R = 0.032, the enlarged 0.0320001, the reuse threshold, and the .103/.125 targets.
Run: python3 experiments/radius.py
"""
import csv, os
from math import pi, sqrt, ceil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, os.pardir, os.pardir, "data", "m3"))
def pr(*a): print(*a)
out = []
def rec(k, v, note=""):
    out.append((k, v, note)); pr(f"  {k:<34} {v:>22}   {note}")

pr("=" * 90)
pr("1. The seed radius R = 0.032: three constraints (A.3, A.4, Prop 2.10)")
pr("=" * 90)
R, Re, N = 0.032, 0.0320001, 112
Rs  = 2 * pi * R
Rse = 2 * pi * Re
rec("R", R)
rec("2*pi*R (radians)", f"{Rs:.6f}", "A.4 threshold: Rs < .203")
rec("2*pi*0.0320001", f"{Rse:.6f}", "still < .203")
rec("slack of Rs < .203", f"{.203/Rse:.5f}", f"{(.203/Rse-1):.3%} headroom")
Rmax203 = .203 / (2 * pi) - 1e-7
rec("R upper bound from Rs<.203", f"{Rmax203:.6f}", "R < .203/(2*pi)")
# q = Rs^2 (1 + (A*^2+6)/mC^2) with A* = 2, mC = 1.239 (A.4)
mC, Aast = 1.239, 2.0
fac = 1 + (Aast**2 + 6) / mC**2
q = Rs**2 * fac
rec("q at R=.032", f"{q:.5f}", "A.4 threshold q < .32")
rec("slack of q < .32", f"{.32/q:.4f}", f"{(.32/q-1):.2%} headroom")
Rmaxq = sqrt(.32 / fac) / (2 * pi) - 1e-7
rec("R upper bound from q<.32", f"{Rmaxq:.6f}", "")
Rlo = 1.5 / N
rec("R lower bound 1.5/N at N=112", f"{Rlo:.6f}", "Prop 2.10 packing; R must exceed it")
rec("R / (1.5/N)", f"{R/Rlo:.4f}", "downward slack 2.39x")
rec("(1.5/N) / R", f"{Rlo/R:.4f}", "the fresh-centre radius as a fraction of R")
rec("R window at N=112", f"[{Rlo:.6f}, {min(Rmax203,Rmaxq):.6f})", "")
# doubling / halving
for Rt in (R/2, 2*R):
    s = 2*pi*Rt; qt = s**2*fac
    pr(f"  R={Rt:.4f}:  Rs={s:.5f} ({'<' if s < .203 else '>'} .203),  q={qt:.5f} "
       f"({'<' if qt < .32 else '>'} .32), 1.5/N < R ? {1.5/N < Rt}")
pr()
pr("  Doubling R to .064 breaks the A.4 field chain (Rs = .402 > .203, q = 1.21 > .32)")
pr("  before it ever reaches Stage A: the 'invalid-q branch' is entered.")
pr("  Halving R to .016 keeps every inequality but doubles the seed-ball covering number")
pr("  per dimension-5 volume law: centres x 2^5 = 32.")
rec("R=1/32 exact?", f"{1/32:.7f}", "2*pi/32 = .196350 = pi/16 = h at Nu=16 (2.4% below .032)")

pr()
pr("=" * 90)
pr("2. The enlarged 0.0320001 (Prop 2.10 last line)")
pr("=" * 90)
rec("excess of .0320001 over .032", f"{1e-7:.1e}", "must absorb the 9-phase binary conversion")
rec("conversion error bound (A.3)", f"{1e-14:.0e}", "nine rounding-rounded phases")
rec("slack ratio", f"{1e-7/1e-14:.0e}", "harmless, 7 orders of magnitude of slack")

pr()
pr("=" * 90)
pr("3. The reuse threshold RN^2 = fl(fl(.032*112)^2) - 1e-4   (A.3, testBucket)")
pr("=" * 90)
a = round(R * N, 12); b = round(a * a, 12); RN2 = b - 1e-4
rec(".032 * 112", f"{a:.6f}")
rec("(.032*112)^2", f"{b:.9f}")
rec("RN^2 = that - 1e-4", f"{RN2:.9f}")
rec("sqrt(RN^2)", f"{sqrt(RN2):.9f}", "= largest certified distance in grid units")
rec("implied phase radius", f"{sqrt(RN2)/N:.9f}", "vs R = .032")
rec("radius given up to the 1e-4", f"{R - sqrt(RN2)/N:.3e}", f"relative {(R-sqrt(RN2)/N)/R:.2e}")
rec("needed to be safe (binary64)", f"{1e-12:.0e}", "A.3: total possible error before subtraction")
rec("slack of the 1e-4", f"{1e-4/1e-12:.0e}", "8 orders: any 1e-4 >= 1e-12 works")
rec("cost of the conservatism", "0.99996 of a lattice step", "reuse lost only if NR-1.5 lands within 1.4e-5 of an integer")
pr("  The threshold is conservative in the right direction: a failed reuse inserts a fresh")
pr("  midpoint of radius 1.5/112 = .0134 < .032, so no coverage is lost.")

pr()
pr("=" * 90)
pr("4. The A targets: local .103, atlas/global cap .125, B validate cap .126")
pr("=" * 90)
loc, glob, val = .103, .125, .126
rec("local target .103 < atlas cap .125", f"{glob-loc:.4f}", f"headroom {(glob-loc)/glob:.1%}")
rec("atlas cap .125 < B validate .126", f"{val-glob:.4f}", f"headroom {(val-glob)/val:.2%}")
rec("window for the atlas cap", f"({loc}, {val})", ".103 < cap < .126")
rec("observed A output records", "3083", "Table 1: all radii <= .125 by the cap")
rec("local .103 at half (.0515)", "Roots x2^5 = 32 per cell", "A wall time x32 = 18 h; 3083 -> 98,656 records (< 2e6 cap)")
rec("local .103 at double (.206)", "> .125", "Atlas::add cannot insert: every A record aborts -> A fails")
rec("atlas .125 at half (.0625)", "< .103", "no local record fits the cap -> A fails at once")
rec("atlas .125 at double (.25)", "> .126", "B validate rejects every input -> B fails")
# crude cell phase extent from A.4: E < 1 radian
rec("crude cell phase extent (A.4)", f"{1/(2*pi):.4f} cycles", "E < 1 rad; exceeds .103 -> .103 is empirical, not derived")
rec("seed-cell angular match", f"{Rs/(pi/16):.4f}", "2*pi*R vs h = pi/16 at Nu = 16")

with open(os.path.join(DATA, "radius.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["constant_or_quantity", "value", "note"]); w.writerows(out)
pr()
pr(f"  wrote {DATA}/radius.csv")
