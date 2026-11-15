"""Mutation suite for the Root checker: every mutant is applied to one real record
(fb1.bin record 0) and the checker's per-obligation verdicts are printed.

Purpose: show that (a) a claim refutable from the stored bytes is refuted (R1-R4), (b) a claim
that needs a witness which the checker cannot supply comes out UNDECIDED, and (c) absent evidence
is never a PASS.  Verdicts are printed in the default ("derived witness") mode, in which R5-R7
failures are UNDECIDED by construction: a derived M/U is only a proposal.
"""
import copy
import sys
import time

import records as R
import rootcheck as C

PASS, FAIL, UND = C.PASS, C.FAIL, C.UND


def clone(r):
    return R.Root(r.k, list(r.p), [list(x) for x in r.T],
                  [r.C, r.n0, r.id, r.ort, r.hor, r.mnorm, r.froot, r.radius])


def run(name, r, mode="factors"):
    t = time.time()
    out, det = C.check(r, mode=mode)
    dt = time.time() - t
    cells = {nm: vd for nm, vd, mg, nt in out}
    order = ["G1 fields", "G2 thresholds", "R1 |T*T-I|_F", "R2 |(I-Pi)T|_F", "R3 |F(P)|<=froot",
             "R4 n0>=mnorm*froot", "R5 |M|<=mnorm", "R6 defect<=id", "R7 C>=pi*b(M)"]
    print("%-26s %s   (%.2fs)" % (name, " ".join("%s:%s" % (o.split()[0], cells[o]) for o in order), dt))
    return cells


def main():
    v = R.read(R.DATA + "fb1.bin")
    base = v[0]
    print("canary: fb1.bin record 0, k=%d, radius=%.6g" % (base.k, base.radius))
    run("unmutated", base)

    r = clone(base); r.froot = 1e-13
    run("froot := 1e-13", r)
    r = clone(base); r.ort = 0.0
    run("ort := 0", r)
    r = clone(base); r.hor = 0.0
    run("hor := 0", r)
    r = clone(base); r.n0 = base.mnorm * base.froot * 0.5
    run("n0 := 0.5 mnorm*froot", r)
    r = clone(base); r.mnorm = base.mnorm * (1 - 1e-6)
    run("mnorm x (1-1e-6)", r)
    r = clone(base); r.id = 1e-15
    run("id := 1e-15", r)
    r = clone(base); r.C = base.C * 0.999
    run("C x 0.999", r)
    r = clone(base); r.C = base.C * 1.0001
    run("C x 1.0001 (harmless?)", r)
    r = clone(base)
    r.T[0] = [x * 1.001 for x in r.T[0]]
    run("T column 0 x 1.001", r)
    r = clone(base)
    r.p[3] = r.p[3] + 1e-5
    run("p[3] += 1e-5", r)
    r = clone(base)
    r.T = [r.T[1], r.T[0], r.T[2], r.T[3]]
    run("T columns 0<->1 swapped", r)
    r = clone(base)
    r.k = 0; r.T = []
    run("k := 0, T dropped", r)
    r = clone(base)
    r.C = float("nan")
    run("C := NaN", r)
    run("same record, no witness", base, mode="none")


if __name__ == "__main__":
    main()
