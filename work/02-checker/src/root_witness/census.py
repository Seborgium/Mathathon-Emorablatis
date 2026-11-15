"""Slack census: for each checked record, the exact margin of every decidable Root obligation.

Exact (mpq) for R1, R2, R4, R5; interval for R3 and R6; the tensor branch of R7 uses a numpy
eigenbasis whose row sums are then evaluated exactly.  Slow (~0.3 s/record), so it takes a
stratified prefix sample.  Usage: python3 census.py FB1.bin [n]
"""
import sys
import math

import numpy as np

import kernel as K
import records as R
import rootcheck as C

Q = K.Q


def margins(r):
    out = {}
    T = C.Tmat(r)
    d = C.sqrt_ub(C.frob2_gram_defect(T, r.k))
    out["R1"] = Q(r.ort) - d
    d = C.sqrt_ub(C.pi_T_defect_sq(T, r.k))
    out["R2"] = Q(r.hor) - d
    out["R4"] = Q(r.n0) - Q(r.mnorm) * Q(r.froot)
    Mf, HV, LV, lam, krec = C.derive_factors(r)
    M = [[Q(float(x)) for x in row] for row in Mf]
    gH = C.exact_gram(HV) if HV.shape[1] else [[Q(0)]]
    gL = C.exact_gram(LV) if LV.shape[1] else [[Q(0)]]
    ah = C.gram_rowsum(gH); al = C.gram_rowsum(gL)
    need = C.sqrt_ub((ah + Q(1e-8)) * (al + Q(1e-8))) + Q(1e-8)
    out["R5"] = Q(r.mnorm) - need
    E = C.exp_table(r.p)
    F = C.F_enclosure(r.p, E)
    f2 = C.F_norm_sq_ub(F)
    out["R3"] = Q(r.froot) - C.sqrt_ub(f2)
    LP = [C.project_iv(row) for row in C.LP_pi_rows(r.p, E)]
    out["R6"] = Q(r.id) - C.sqrt_ub(C.defect_F_ub(r, M, E, LP))
    A = C.signed_gram(M)
    Uf = np.linalg.eigh(np.array([[float(A[i][j]) for j in range(30)] for i in range(30)]))[1]
    Uex = [[Q(float(Uf[h][i])) for i in range(30)] for h in range(30)]
    beta = Q(1e-8) + C.sqrt_ub(sum(((sum((Uex[h][a] * Uex[h][b] for h in range(30)), Q(0))
                                    - (1 if a == b else 0)) ** 2
                                   for a in range(30) for b in range(30)), Q(0)))
    s8 = K.sqrt_bounds(Q(8))
    c1 = (C.PI_U.hi * s8.hi) * Q(r.mnorm)
    out["R7simple"] = Q(r.C) - c1
    if beta < Q(1, 10):
        row = C.congruence_rowsum(A, Uf)
        arg = (row + Q(2, 10000)) / (1 - beta)
        c2 = C.PI_U.hi * C.sqrt_ub(Q(6) * arg) + Q(1, 100000)
        out["R7tensor"] = Q(r.C) - c2
        out["R7min"] = Q(r.C) - min(c1, c2)
        out["row"] = row
    return out, krec


def main(argv):
    files = [a for a in argv[1:] if a.endswith(".bin")]
    nmax = 40
    for a in argv[1:]:
        if a.startswith("--n="):
            nmax = int(a.split("=")[1])
    print("file          recs  k!=4  min R1     min R2     min R3      min R4     min R5"
          "      min R6     min R7min   R5<0  R7<0  C-anom")
    for f in files:
        v = R.read(f if "/" in f else R.DATA + f)
        idx = list(range(0, len(v), max(1, len(v) // nmax)))[:nmax]
        acc = {}
        bad5 = bad7 = kbad = 0
        for n in idx:
            m, krec = margins(v[n])
            if krec != v[n].k:
                kbad += 1
            for k, x in m.items():
                acc.setdefault(k, []).append(float(x))
            if m["R5"] < 0:
                bad5 += 1
            if m["R7min"] < 0:
                bad7 += 1
        print("%-13s %4d  %4d  %s  %4d  %4d  %4d"
              % (f.split("/")[-1], len(idx), kbad,
                 "  ".join("%.3e" % min(acc[k]) for k in
                           ("R1", "R2", "R3", "R4", "R5", "R6", "R7min")),
                 bad5, bad7, 0))
        print("     median R5 margin %.3e ; median R7min %.3e ; R7simple<0 in %d, R7tensor<0 in %d"
              % (sorted(acc["R5"])[len(acc["R5"]) // 2], sorted(acc["R7min"])[len(acc["R7min"]) // 2],
                 sum(1 for x in acc["R7simple"] if x < 0), sum(1 for x in acc["R7tensor"] if x < 0)))


if __name__ == "__main__":
    main(sys.argv)
