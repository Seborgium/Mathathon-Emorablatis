"""Root-certificate checker: the obligations of Definition 4.1 / Proposition 4.5, decided in exact
rational arithmetic (Gram defects, matrix norms) and outward interval arithmetic (the only
transcendental input, e(x) = exp(2 pi i x)).

Verdict semantics (three-valued, and the distinction is load-bearing):

  PASS       the obligation is established for the stored record (given the transported witness
             when the obligation needs one).
  FAIL       reserved for a *refutation of stored bytes*: R1-R4 are statements about the record
             alone, so an exact/interval evaluation that strictly violates one refutes the record.
             For R5-R7, a failure of a checker-supplied ("derived") witness refutes nothing: a
             different admissible M or U may certify the same record, so the verdict is UNDECIDED.
             If the witness was transported inside the certificate file (`witness_emitted`), a
             failure rejects that file -- the *pair* is refuted, which is reported as FAIL.
  UNDECIDED  nothing is decided: a missing witness, a derived witness that does not certify, or an
             enclosure straddling the decision point.  UNDECIDED is never a refutation and never a
             pass.

Witness modes
  none   : only the stored record.  R1..R4 (4.4)+(4.15b) are still decidable; R5..R7 (the M
           clauses) become UNDECIDED -- this is the "what the saved bytes cannot do" mode.
  factors: the emitter adds HV (36 x g) and LV (30 x g) and, when the tensor constant was used,
           U (30 x 30).  Every check below is then exact given those bytes plus e(x) enclosures.
  derive : the same checks, but HV/LV/U are rebuilt here by the canonical construction, so the
           run's own bytes are not needed -- a proposal step whose output is still verified.

Obligations
  G1 field gates        k in [0,10], |p|<=4, |T|<=2, constants finite and >= 0
  G2 thresholds         id<1e-4, ort<1e-5, hor<1e-5, C<20, mnorm<2, n0<1e-6, froot<1e-6
  R1 (4.4a)  ||T*T - I_k||_F <= ort                       exact
  R2 (4.4b)  ||(I - Pi)T||_F <= hor                       exact
  R3 (4.4c)  ||F(P)|| <= froot                            interval
  R4 (4.15b) mnorm*froot <= n0                            exact
  R5 (4.15a) ||M|| <= mnorm                               exact, via Gershgorin on HV, LV
  R6 (4.15c) ||Pi - T T* - M L_P Pi||_F <= id             interval, M = HV LV*
  R7 remainder constant  C >= pi * min( sqrt(8) mnorm, sqrt(6 lam(A)) )   exact + interval
     with A the 30x30 signed Gram (4.14): lam(A) <= max row sum of |U* A U| / (1-beta),
     beta = ||U*U - I||_F + 1e-8 < .1  (A.5).  U empty => only the sqrt(8) mnorm branch.
"""
import math
import sys

import numpy as np

import kernel as K
import records as R
from derive import Qbasis, PI36, fullL

Q = K.Q
Iv = K.Iv
Qb = Qbasis()
PI_U = K.pi()
TWO_PI = Iv(PI_U.lo * 2, PI_U.hi * 2)

PASS, FAIL, UND = "PASS", "FAIL", "UNDECIDED"


# ------------------------------------------------------------------ exact record pieces
def Tmat(r):
    return [[Q(x) for x in row] for row in r.T]


def frob2_gram_defect(T, k):
    g = [[sum((T[a][h] * T[b][h] for h in range(36)), Q(0)) for b in range(k)] for a in range(k)]
    return sum(((g[a][b] - (1 if a == b else 0)) ** 2 for a in range(k) for b in range(k)), Q(0))


def pi_T_defect_sq(T, k):
    tot = Q(0)
    for a in range(k):
        x = T[a]
        rows = [sum(x[6 * i:6 * i + 6], Q(0)) for i in range(6)]
        cols = [sum((x[6 * i + j] for i in range(6)), Q(0)) for j in range(6)]
        g = sum(rows, Q(0))
        for i in range(6):
            for j in range(6):
                pr = x[6 * i + j] + g / 36 - (rows[i] + cols[j]) / 6
                tot += (pr - x[6 * i + j]) ** 2
    return tot


def sqrt_ub(d):
    return Q(0) if d == 0 else K.sqrt_bounds(d).hi


# ------------------------------------------------------------------ e(P), F(P), L_P Pi
def exp_table(p):
    return [K.cos_sin_2pi(Q(x)) for x in p]


def F_enclosure(p, E=None):
    if E is None:
        E = exp_table(p)
    inv = Iv(Q(1) / TWO_PI.hi, Q(1) / TWO_PI.lo)
    out = []
    for i in range(6):
        for j in range(i):
            re = Iv(Q(0)); im = Iv(Q(0))
            for g in range(6):
                ci, si = E[6 * i + g]
                cj, sj = E[6 * j + g]
                re = re + ci * cj + si * sj
                im = im + si * cj - ci * sj
            out.append((im * inv, -(re * inv)))
    return out


def F_norm_sq_ub(F):
    return sum((re.sq().hi + im.sq().hi for (re, im) in F), Q(0))


def LP_pi_rows(p, E=None):
    if E is None:
        E = exp_table(p)
    rows = []
    for i in range(6):
        for j in range(i):
            q = []
            for g in range(6):
                ci, si = E[6 * i + g]
                cj, sj = E[6 * j + g]
                q.append((ci * cj + si * sj, si * cj - ci * sj))
            for part in (0, 1):
                row = [Iv(Q(0))] * 36
                for g in range(6):
                    v = q[g][part]
                    row[6 * i + g] = v
                    row[6 * j + g] = -v
                rows.append(row)
    return rows


def project_iv(row):
    """Pi applied to a 36-vector of intervals: x_ij - rowmean_i - colmean_j + grandmean."""
    rows = [Iv(Q(0))] * 6
    cols = [Iv(Q(0))] * 6
    for i in range(6):
        rows[i] = sum((row[6 * i + j] for j in range(6)), Iv(Q(0)))
    for j in range(6):
        cols[j] = sum((row[6 * i + j] for i in range(6)), Iv(Q(0)))
    g = sum(rows, Iv(Q(0)))
    out = [Iv(Q(0))] * 36
    for i in range(6):
        for j in range(6):
            out[6 * i + j] = row[6 * i + j] - rows[i] / Iv(Q(6)) - cols[j] / Iv(Q(6)) + g / Iv(Q(36))
    return out


def defect_F_ub(r, M, E=None, LP=None):
    """Upper bound for ||Pi - T T* - M L_P Pi||_F; M exact 36x30; L_P Pi enclosures."""
    T = Tmat(r); k = r.k
    if E is None:
        E = exp_table(r.p)
    if LP is None:
        LP = [project_iv(row) for row in LP_pi_rows(r.p, E)]
    ML = []
    for i in range(36):
        acc = [Iv(Q(0))] * 36
        Mi = M[i]
        for a in range(30):
            m = Mi[a]
            if m == 0:
                continue
            LPa = LP[a]
            acc = [acc[j] + m * LPa[j] for j in range(36)]
        ML.append(acc)
    tot = Q(0)
    for i in range(36):
        for j in range(36):
            tt = sum((T[a][i] * T[a][j] for a in range(k)), Q(0))
            pij = (((i // 6 == j // 6) and Q(1) or Q(0)) - Q(1, 6)) * \
                  (((i % 6 == j % 6) and Q(1) or Q(0)) - Q(1, 6))
            tot += (Iv(pij) - Iv(tt) - ML[i][j]).sq().hi
    return tot


# ------------------------------------------------------------------ the canonical construction
def derive_factors(r):
    """patchx.cpp's construction, read literally (a proposal; every use below is verified)."""
    J = fullL(r.p) @ Qb
    Gram = J.T @ J
    lam, V = np.linalg.eigh(Gram)
    small = lam < 0.64
    HV = Qb @ V[:, ~small]
    LV = (J @ V[:, ~small]) / lam[~small] if (~small).any() else np.zeros((30, 0))
    M = HV @ LV.T
    return M, HV, LV, lam, int(small.sum())


def gram_rowsum(A):
    return max(sum(abs(A[i][j]) for j in range(len(A))) for i in range(len(A)))


def exact_gram(F):
    """G = F* F for an (m x g) float matrix, exact rationals."""
    m, g = len(F), len(F[0]) if len(F) else 0
    Fi = [[Q(float(x)) for x in row] for row in F]
    return [[sum((Fi[h][a] * Fi[h][b] for h in range(m)), Q(0)) for b in range(g)] for a in range(g)]


def signed_gram(M):
    ei, ej = [], []
    for i in range(6):
        for j in range(i):
            ei += [i, i]; ej += [j, j]
    n = 30
    dots = [[sum((M[h][a] * M[h][b] for h in range(36)), Q(0)) for b in range(n)] for a in range(n)]
    A = [[Q(0)] * n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            sg = ((ei[a] == ei[b]) + (ej[a] == ej[b]) - (ei[a] == ej[b]) - (ej[a] == ei[b]))
            if sg:
                A[a][b] = dots[a][b] * sg
    return A


def float_signed_gram(Mf):
    ei, ej = [], []
    for i in range(6):
        for j in range(i):
            ei += [i, i]; ej += [j, j]
    n = 30
    dots = Mf.T @ Mf
    A = np.zeros((n, n))
    for a in range(n):
        for b in range(n):
            sg = ((ei[a] == ei[b]) + (ej[a] == ej[b]) - (ei[a] == ej[b]) - (ej[a] == ei[b]))
            if sg:
                A[a][b] = dots[a][b] * sg
    return A


def congruence_rowsum(A, U):
    """max_i sum_j |(U* A U)_ij| with U an exact rational 30x30 (dyadic from float)."""
    n = len(A)
    Ui = [[Q(float(U[h][i])) for i in range(n)] for h in range(n)]
    AU = [[sum((A[h][l] * Ui[l][j] for l in range(n)), Q(0))
           for j in range(n)] for h in range(n)]
    tot = [[sum((Ui[h][i] * AU[h][j] for h in range(n)), Q(0)) for j in range(n)] for i in range(n)]
    return max(sum(abs(tot[i][j]) for j in range(n)) for i in range(n))


# ------------------------------------------------------------------ the checking routine
_ROWCACHE = {}


def check(r, mode="factors", want_detail=False, exact_row=True, tensor=True,
          witness_emitted=False):
    out = []
    det = {}

    def put(name, verdict, margin, note=""):
        out.append((name, verdict, margin, note))

    def dec(ok, note=""):
        """Verdict for a witness-dependent obligation."""
        if ok:
            return PASS
        return FAIL if witness_emitted else UND

    # -------- G1 gates
    bad = []
    if not (0 <= r.k <= 10):
        bad.append("k range")
    if any((not math.isfinite(x)) or abs(x) > 4.0 for x in r.p):
        bad.append("|p|<=4")
    if any((not math.isfinite(x)) or abs(x) > 2.0 for row in r.T for x in row):
        bad.append("|T|<=2")
    vals = dict(C=r.C, n0=r.n0, id=r.id, ort=r.ort, hor=r.hor, mnorm=r.mnorm, froot=r.froot)
    if any((not math.isfinite(v)) or v < 0 for v in vals.values()):
        bad.append("constants >= 0")
    put("G1 fields", PASS if not bad else FAIL, None, "; ".join(bad) or "ok")
    if bad:
        for nm in ("G2 thresholds", "R1 |T*T-I|_F", "R2 |(I-Pi)T|_F", "R3 |F(P)|<=froot",
                   "R4 n0>=mnorm*froot", "R5 |M|<=mnorm", "R6 defect<=id", "R7 C>=pi*b(M)"):
            put(nm, UND, None, "not evaluated: field gate failed")
        return out, det
    gates = [("id", 1e-4), ("ort", 1e-5), ("hor", 1e-5), ("C", 20.0), ("mnorm", 2.0),
             ("n0", 1e-6), ("froot", 1e-6)]
    bad = ["%s<%g" % (n, t) for n, t in gates if not (vals[n] < t)]
    put("G2 thresholds", PASS if not bad else FAIL, None, "; ".join(bad) or "all 7")

    # -------- R1, R2, R4 exact
    T = Tmat(r)
    ub = sqrt_ub(frob2_gram_defect(T, r.k))
    put("R1 |T*T-I|_F", PASS if ub <= Q(r.ort) else FAIL, Q(r.ort) - ub)
    ub = sqrt_ub(pi_T_defect_sq(T, r.k))
    put("R2 |(I-Pi)T|_F", PASS if ub <= Q(r.hor) else FAIL, Q(r.hor) - ub)
    m = Q(r.n0) - Q(r.mnorm) * Q(r.froot)
    put("R4 n0>=mnorm*froot", PASS if m >= 0 else FAIL, m)

    # -------- R3 interval
    E = exp_table(r.p)
    F = F_enclosure(r.p, E)
    f2 = F_norm_sq_ub(F)
    fub = sqrt_ub(f2)
    flb = K.sqrt_bounds(f2).lo
    if fub <= Q(r.froot):
        put("R3 |F(P)|<=froot", PASS, Q(r.froot) - fub)
    elif flb > Q(r.froot):
        put("R3 |F(P)|<=froot", FAIL, flb - Q(r.froot))
    else:
        put("R3 |F(P)|<=froot", UND, None, "enclosure straddles")

    if mode == "none":
        for nm in ("R5 |M|<=mnorm", "R6 defect<=id", "R7 C>=pi*b(M)"):
            put(nm, UND, None, "witness M missing from the record")
        return out, det

    # -------- witness
    Mf, HV, LV, lam, krec = derive_factors(r)
    M = [[Q(float(x)) for x in row] for row in Mf]

    # R5: ||M|| <= ||HV|| ||LV|| <= sqrt(ah) sqrt(al), Gershgorin on the two Grams
    gH = exact_gram(HV) if HV.shape[1] else [[Q(0)]]
    gL = exact_gram(LV) if LV.shape[1] else [[Q(0)]]
    ah = gram_rowsum(gH); al = gram_rowsum(gL)
    prod = (ah + Q(1e-8)) * (al + Q(1e-8))
    need = sqrt_ub(prod) + Q(1e-8)              # mnorm must dominate this
    ok5 = Q(r.mnorm) >= need
    put("R5 |M|<=mnorm", dec(ok5, "no certified witness"),
        Q(r.mnorm) - need,
        "" if ok5 else "derived witness fails; other guards not excluded")
    det["ah"] = ah; det["al"] = al

    # R6
    ub = sqrt_ub(defect_F_ub(r, M, E))
    ok6 = ub <= Q(r.id)
    put("R6 defect<=id", dec(ok6), Q(r.id) - ub,
        "" if ok6 else "upper enclosure exceeds id; exact defect not bounded below")

    # R7
    s8 = K.sqrt_bounds(Q(8))
    c1 = Iv(PI_U.lo, PI_U.hi) * Iv(s8.lo, s8.hi) * Iv(Q(r.mnorm))          # pi sqrt8 mnorm
    if not tensor:
        put("R7 C>=pi*b(M)", UND, None, "tensor branch skipped (cheap run)")
        return out, det
    if exact_row:
        A = signed_gram(M)
        Uf = np.linalg.eigh(np.array([[float(A[i][j]) for j in range(30)] for i in range(30)]))[1]
    else:
        Mf2 = np.array([[float(M[h][a]) for a in range(30)] for h in range(36)])
        A = float_signed_gram(Mf2)
        Uf = np.linalg.eigh(A)[1]
    Uex = [[Q(float(Uf[h][i])) for i in range(30)] for h in range(30)]
    beta_q = Q(1e-8) + sqrt_ub(sum(((sum((Uex[h][a] * Uex[h][b] for h in range(30)), Q(0))
                                     - (1 if a == b else 0)) ** 2
                                    for a in range(30) for b in range(30)), Q(0)))
    if beta_q < Q(1, 10):
        if exact_row:
            key = tuple(round(float(x), 12) for x in r.p) + (round(float(r.T[0][0]), 12) if r.k else 0.0,)
            if key in _ROWCACHE:
                row = _ROWCACHE[key]
            else:
                row = congruence_rowsum(A, Uf)
                _ROWCACHE[key] = row
        else:
            Af = np.array([[float(A[i][j]) for j in range(30)] for i in range(30)])
            row = Q(float(np.abs(Uf.T @ (Af @ Uf)).sum(axis=1).max())) + Q(1, 10**9)
        arg = (row + Q(2, 10000)) / (1 - beta_q)
        c2 = Iv(PI_U.lo, PI_U.hi) * Iv(sqrt_ub(Q(6) * arg), sqrt_ub(Q(6) * arg)) + Iv(Q(1, 100000))
        cmin = min(c1.hi, c2.hi)
        det["C_simple"] = c1.hi; det["C_tensor"] = c2.hi; det["beta"] = beta_q; det["row"] = row
        ok7 = Q(r.C) >= cmin
        put("R7 C>=pi*b(M)", dec(ok7), Q(r.C) - cmin,
            "min(simple %.6f, tensor %.6f)%s" % (float(c1.hi), float(c2.hi),
                                                 "" if ok7 else "; derived U fails, others not excluded"))
    else:
        det["C_simple"] = c1.hi
        put("R7 C>=pi*b(M)", dec(Q(r.C) >= c1.hi), Q(r.C) - c1.hi,
            "simple branch only (derived U has beta >= .1)")
    return out, det


def main(argv):
    mode = "factors"
    nmax = 2
    files = []
    for a in argv[1:]:
        if a.startswith("--mode="):
            mode = a.split("=")[1]
        elif a.startswith("--n="):
            nmax = int(a.split("=")[1])
        else:
            files.append(a)
    for f in files:
        v = R.read(f if "/" in f else R.DATA + f)
        pick = list(range(min(nmax, len(v))))
        extra = [len(v) // 2, len(v) - 1]
        pick += [i for i in extra if i not in pick]
        print("== %s (%d records)" % (f, len(v)))
        for n in pick:
            out, det = check(v[n], mode=mode)
            print("  rec %5d k=%d radius=%.6g" % (n, v[n].k, v[n].radius))
            for nm, vd, mg, note in out:
                ms = "" if mg is None else "  margin %+.3e" % float(mg)
                print("     %-20s %-9s%s %s" % (nm, vd, ms, note))
            for k, x in det.items():
                print("     [%s = %.9g]" % (k, float(x)))


if __name__ == "__main__":
    main(sys.argv)
