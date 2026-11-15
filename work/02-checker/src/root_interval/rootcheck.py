"""Root-certificate checks (Def 4.1, (4.4), (4.15), remainder constant C)
run on the *stored* records, in exact rational arithmetic plus outward intervals.

What each check needs:
  (4.4)  T*T-I, (I-Pi)T, F(P)          <- stored p, T only
  (4.15) M, mnorm, id                   <- M is NOT stored; we reconstruct it by
                                           the paper's own recipe (Section 4.2 /
                                           patchx.cpp buildH::patch: eigen-split of
                                           the 25x25 horizontal Gram at .64) from p
                                           alone, then *verify* its two properties.
  C                                    <- pi*sqrt8*mnorm, or the (4.14)/(4.15) tensor
                                           candidate when the source took the min.

Every inequality is a one-sided implication; a comparison whose enclosure straddles
the decision point is reported as None = undecided, never as pass.
"""
import time
import numpy as np

import num
import rec
import root_float as rf
import sourceM as sm
from num import Dy, Iv, ONE, dy_to_fraction
from fractions import Fraction as Q

KMAX = 10
O32 = 32


# --------------------------------------------------------------------- helpers
def _iv(x):
    return Iv.dy(x) if isinstance(x, Dy) else Iv.frac(x)


def le_sq(x2, bound):
    """Verdict for sqrt(x2) <= bound, x2 an Iv (>=0) and bound a Dy: returns
    (verdict, slack) with slack = bound - sqrt(x2_hi) as a Fraction."""
    root = x2.sqrt()
    v = root.le(_iv(bound))
    return v, bound.as_fraction() - Q(root.hi, ONE)


def frob_sq(mat):
    """Exact sum of squares of rationals."""
    s = Q(0)
    for row in mat:
        for x in row:
            s += x * x
    return s


def proj_rat(x):
    """Pi x for a 36-list of Fractions/ints (double centering), exact."""
    x = [Q(v) for v in x]
    g = sum(x) / 36
    r = [sum(x[6 * i:6 * i + 6]) for i in range(6)]
    c = [sum(x[6 * i + j] for i in range(6)) for j in range(6)]
    return [x[h] + g - (r[h // 6] + c[h % 6]) / 6 for h in range(36)]


def proj_iv(x):
    g = None
    x = list(x)
    for v in x:
        g = v if g is None else g + v
    g = g.div_int(36)
    r = []
    for i in range(6):
        s = x[6 * i]
        for j in range(1, 6):
            s = s + x[6 * i + j]
        r.append(s.div_int(6))
    c = []
    for j in range(6):
        s = x[j]
        for i in range(1, 6):
            s = s + x[6 * i + j]
        c.append(s.div_int(6))
    return [x[h] + g - r[h // 6] - c[h % 6] for h in range(36)]


# ---------------------------------------------------------------- exact blocks
def exact_part(r):
    """(4.4a) ||T*T-I|| <= ort, (4.4b) ||(I-Pi)T|| <= hor, mnorm*froot<=n0."""
    T = r.TQ()
    k = r.k
    out = {}
    # T*T - I
    s = Q(0)
    for a in range(k):
        for b in range(k):
            g = sum((T[a][h] * T[b][h] for h in range(36)), Q(0))
            d = g - (1 if a == b else 0)
            s += d * d
    v, slack = le_sq(Iv.frac(s), Dy.of(r.ort))
    out["ort"] = dict(verdict=v, value=s, stored=r.ort, slack=slack)
    # (I-Pi) T
    s = Q(0)
    for a in range(k):
        pT = proj_rat(T[a])
        for h in range(36):
            d = T[a][h] - pT[h]
            s += d * d
    v, slack = le_sq(Iv.frac(s), Dy.of(r.hor))
    out["hor"] = dict(verdict=v, value=s, stored=r.hor, slack=slack)
    # mnorm * froot <= n0   (4.15b)
    prod = Q(r.mnorm) * Q(r.froot)
    out["n0"] = dict(verdict=(prod <= Q(r.n0)), value=prod, stored=r.n0,
                     slack=Q(r.n0) - prod)
    return out


def froot_part(r, timing=None):
    """(4.4c) ||F(P)|| <= froot with an outward enclosure of e(2Pi i p)."""
    t0 = time.time()
    p = [Q(x) for x in r.p]
    s = Iv.exact_int(0)
    for (i, j) in rf.EDGES:
        re = Iv.exact_int(0)
        im = Iv.exact_int(0)
        for g in range(6):
            c, sn = num.e2pii(p[6 * i + g] - p[6 * j + g])
            re = re + c
            im = im + sn
        s = s + re.sq() + im.sq()
    four = Iv.exact_int(4) * (num.PI * num.PI)
    s = s * four.__class__(1) if False else s
    # ||F||^2 = sum |sum e|^2 / (2 pi)^2  =  (sum ...) / (4 pi^2)
    denom = (num.PI * num.PI).mul_int(4)
    s2 = _div_iv(s, denom)
    v, slack = le_sq(s2, Dy.of(r.froot))
    if timing is not None:
        timing["froot"] = time.time() - t0
    return dict(verdict=v, value=s2, stored=r.froot, slack=slack)


def _div_iv(a, b):
    """Interval division a/b for b an interval with b.lo > 0, outward."""
    assert b.lo > 0
    lo_f = Q(a.lo, b.hi) if False else Q(a.lo, ONE) / Q(b.hi, ONE)
    hi_f = Q(a.hi, ONE) / Q(b.lo, ONE)
    return Iv.frac(lo_f, ) if False else Iv(lo_f.numerator * ONE // lo_f.denominator,
                                            -((-hi_f.numerator * ONE) // hi_f.denominator))


# ------------------------------------------------- (4.15) with reconstructed M
def m_part(r, timing=None):
    """(4.15a) ||M||<=mnorm and (4.15c) ||Pi - T T* - M LP Pi||<=id.

    Witness choice.  M is not serialised by the source; the certificate check below
    reconstructs a *factorisation* M = HV LV^* from p alone (the paper's own recipe:
    eigen-split of the 25x25 horizontal Gram J^*J at .64), then certifies
        ||M|| <= sqrt(ah*al) <= mnorm,   ah/al the symmetric absolute row-sum bounds
    of HV^*HV and LV^*LV (Lemma 5.1 / Section 5.1 of the paper, used by the source).
    The same M (exactly, in dyadics) enters the residual check.  Nothing about the
    eigendecomposition is trusted: both properties are re-verified.
    """
    t0 = time.time()
    prop = sm.source_M(r.p)
    big = prop["big"]
    HVb = prop["HV"][:, big]
    LVb = prop["LV"][:, big]
    g = int(big.sum())
    k = r.k

    def rowsumbound(A):
        # max_i sum_j |<A_:,i, A_:,j>|  (exact)
        cols = len(A[0]) if len(A) else 0
        Qs = [[Dy.of(A[h][i]) for i in range(cols)] for h in range(len(A))]
        G = [[sum((Qs[h][i] * Qs[h][j] for h in range(len(A))), Dy(0, 0))
              for j in range(cols)] for i in range(cols)]
        return max(sum(abs(dy_to_fraction(G[i][j])) for j in range(cols))
                   for i in range(cols))

    ah = rowsumbound(HVb)
    al = rowsumbound(LVb)
    norm_bound = ah * al                      # ||M||^2 <= ah*al
    v_norm, slack_norm = le_sq(Iv.frac(norm_bound), Dy.of(r.mnorm))

    Mdy = num.dy_matmul([[Dy.of(x) for x in row] for row in HVb],
                        [[Dy.of(x) for x in col] for col in LVb.T])
    MQ = [[dy_to_fraction(x) for x in row] for row in Mdy]
    if timing is not None:
        timing["M_proposal"] = time.time() - t0

    t1 = time.time()
    Tm = np.asarray(r.T, float).reshape(-1, 36)
    TT = [[sum((Q(Tm[a][i]) * Q(Tm[a][j]) for a in range(k)), Q(0)) for j in range(36)]
          for i in range(36)]
    YQ = [[Q(rf.PIJ[i][j]) - TT[i][j] for j in range(36)] for i in range(36)]

    # rows of LP have support on the two grid rows of their edge (4.2)
    ei, ej = [], []
    for (i, j) in rf.EDGES:
        ei += [i, i]
        ej += [j, j]
    MLP = [[Iv.exact_int(0) for _ in range(36)] for _ in range(36)]
    for a in range(30):
        i, j = ei[a], ej[a]
        re = a % 2 == 0
        for gg in range(6):
            ph = Q(r.p[6 * i + gg]) - Q(r.p[6 * j + gg])
            c, sn = num.e2pii(ph)
            val = c if re else sn
            for col, sgn in ((6 * i + gg, 1), (6 * j + gg, -1)):
                for h in range(36):
                    cff = MQ[h][a] * sgn
                    if cff:
                        MLP[h][col] = MLP[h][col] + _scale(val, cff)
    s = Iv.exact_int(0)
    for h in range(36):
        row = proj_iv(MLP[h])
        for j in range(36):
            s = s + (_iv(YQ[h][j]) - row[j]).sq()
    v_res, slack_res = le_sq(s, Dy.of(r.id))
    if timing is not None:
        timing["residual"] = time.time() - t1
    return dict(norm=dict(verdict=v_norm, value=norm_bound, stored=r.mnorm, slack=slack_norm,
                          ah=ah, al=al),
                resid=dict(verdict=v_res, value=s, stored=r.id, slack=slack_res),
                M=[[float(x) for x in row] for row in MQ], prop=prop, g=g,
                k_agree=(25 - g == k))


def one_or_neg(MQ, h, a):
    return MQ[h][a]


def _scale(val, coeff):
    """coeff * interval (coeff an exact rational; outward on both ends)."""
    f = Q(coeff)
    n, d = f.numerator, f.denominator
    if n == 0:
        return Iv.exact_int(0)
    a, b = val.lo * n, val.hi * n
    lo, hi = (a, b) if n > 0 else (b, a)
    return Iv(lo // d, -((-hi) // d))


# ------------------------------------------------------- remainder constant C
def c_part(r, M):
    """C must bound pi*b in Lemma 4.3.  Two sufficient candidates from Lemma 4.4:
    pi*sqrt(8)*mnorm  (first choice) and the tensor candidate built from the row
    Gram (4.14) of the stored M (second choice).  The source stores the min, so a
    tensor-improved record can only be checked through the second candidate."""
    base = num.PI * Iv.frac(Q(8)).sqrt() * Iv.dy(Dy.of(r.mnorm))
    v1 = base.le(Iv.dy(Dy.of(r.C)))
    # tensor candidate
    MQ = [[Q(v) for v in row] for row in M]
    ei = []
    for (i, j) in rf.EDGES:
        ei += [i, j]
    Asign = np.zeros((30, 30))
    for a in range(30):
        ia, ja = ei[2 * (a // 2)], ei[2 * (a // 2) + 1]
        for b in range(30):
            ib, jb = ei[2 * (b // 2)], ei[2 * (b // 2) + 1]
            sg = (ia == ib) + (ja == jb) - (ia == jb) - (ja == ib)
            Asign[a][b] = sg
    AQ = [[sum((MQ[h][a] * MQ[h][b] for h in range(36)), Q(0)) * int(Asign[a][b])
           for b in range(30)] for a in range(30)]
    A = np.array([[float(x) for x in row] for row in AQ])
    w, V = np.linalg.eigh(A)
    beta2 = Q(0)
    for i in range(30):
        for j in range(30):
            g = sum((Q(V[h][i]) * Q(V[h][j]) for h in range(30)), Q(0)) - (1 if i == j else 0)
            beta2 += g * g
    beta = _sqrt_up(beta2) + Dy.of(1e-8)
    # X = A U ; row = max_i sum_j |(U^* X)_ij|
    XQ = [[sum((AQ[a][h] * Q(V[h][j]) for h in range(30)), Q(0)) for j in range(30)]
          for a in range(30)]
    row = Q(0)
    for i in range(30):
        s = Q(0)
        for j in range(30):
            s += abs(sum((Q(V[h][i]) * XQ[h][j] for h in range(30)), Q(0)))
        row = max(row, s)
    cand = None
    if beta < Q(1):
        inner = Q(6) * (row + Q(2, 10 ** 4)) / (1 - beta.as_fraction())
        inner_iv = Iv.frac(inner).sqrt()
        cand = num.PI * inner_iv + Iv.frac(Q(1, 10 ** 5))
        v2 = cand.le(Iv.dy(Dy.of(r.C)))
    else:
        v2 = False
    return dict(base=v1, tensor=v2, beta=beta, row=row,
                base_value=base, tensor_value=cand)


def _sqrt_up(f, shift=num.B):
    return num.dy_sqrt_up(Dy(f.numerator, (f.denominator).bit_length() - 1) if
                          (f.denominator & (f.denominator - 1)) == 0 else Dy.of(0), shift) \
        if False else Dy(_ceil_sqrt_frac(f, shift), shift)


def _ceil_sqrt_frac(f, shift=num.B):
    num_ = f.numerator << (2 * shift)
    den = f.denominator
    m = -((-num_) // den)
    n = _isqrt_ceil(m)
    while n * n * den < num_:
        n += 1
    return n


def _isqrt_ceil(m):
    from math import isqrt
    r = isqrt(m)
    return r if r * r == m else r + 1


# ------------------------------------------------------------------- driver
def check(r):
    timing = {}
    t0 = time.time()
    e = exact_part(r)
    f = froot_part(r, timing)
    m = m_part(r, timing)
    c = c_part(r, m["M"])
    timing["total"] = time.time() - t0
    verdicts = dict(ort=e["ort"]["verdict"], hor=e["hor"]["verdict"], froot=f["verdict"],
                    n0=e["n0"]["verdict"], mnorm=m["norm"]["verdict"],
                    id=m["resid"]["verdict"], C_base=c["base"], C_tensor=c["tensor"])
    ok = all(v is True for v in verdicts.values() if v is not False)
    anyfalse = any(v is False for v in verdicts.values())
    # a Root needs: (4.4) all three, (4.15) all three, and C bounded by ONE candidate
    need = [verdicts[x] for x in ("ort", "hor", "froot", "n0", "mnorm", "id")]
    c_ok = verdicts["C_base"] is True or verdicts["C_tensor"] is True
    root_verdict = ("pass" if all(v is True for v in need) and c_ok else
                    "FAIL" if any(v is False for v in need) or (verdicts["C_base"] is False
                                                               and verdicts["C_tensor"] is False)
                    else "undecided")
    nv = m["norm"]["value"]
    mnorm_ours = float(nv.as_fraction() if isinstance(nv, Dy) else Q(nv)) ** 0.5
    return dict(record=r, verdicts=verdicts, root=root_verdict, detail=dict(exact=e, froot=f, m=m, c=c),
                timing=timing,
                diag=dict(mnorm_rel=(mnorm_ours - r.mnorm) / r.mnorm if r.mnorm else 0.0,
                          k_agree=m["k_agree"],
                          resid=_fsqrt(m["resid"]["value"])))


def _fsqrt(iv):
    return (float(iv.lo) / num.ONE) ** 0.5 if iv.lo >= 0 else float("nan")


def _fmt(v):
    return {True: "pass", False: "FAIL", None: "undec"}[v]


def sample_of(recs, n):
    """Stratified: the k=0 records, the two smallest radii, n spread by radius."""
    small = [r for r in recs if r.k == 0]
    k4 = sorted((r for r in recs if r.k > 0), key=lambda r: r.radius)
    pick = list(small) + k4[:2]
    if k4:
        idxs = [len(k4) // 4, len(k4) // 2, 3 * len(k4) // 4, len(k4) - 1]
        pick += [k4[i] for i in idxs]
    seen, out = set(), []
    for r in pick:
        if (r.index, r.source) not in seen:
            seen.add((r.index, r.source))
            out.append(r)
    return out[:n] if n else out


def main(argv):
    import argparse, json
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--per-file", type=int, default=8)
    ap.add_argument("--json", default=None)
    a = ap.parse_args(argv)
    rows, worst = [], 0.0
    for path in a.files:
        recs = rec.read_records(path)
        name = path.split("/")[-1]
        for r in sample_of(recs, a.per_file):
            res = check(r)
            v, d = res["verdicts"], res["detail"]
            rows.append(dict(file=name, index=r.index, k=r.k, radius=r.radius, root=res["root"],
                             verdicts={k: (None if x is None else bool(x)) for k, x in v.items()},
                             mnorm_rel=res["diag"]["mnorm_rel"], k_agree=res["diag"]["k_agree"],
                             resid=res["diag"]["resid"],
                             beta=float(d["c"]["beta"]), row=float(d["c"]["row"]),
                             slack=dict(ort=float(d["exact"]["ort"]["slack"]),
                                        hor=float(d["exact"]["hor"]["slack"]),
                                        froot=float(d["froot"]["slack"]),
                                        n0=float(d["exact"]["n0"]["slack"]),
                                        mnorm=float(d["m"]["norm"]["slack"]),
                                        id=float(d["m"]["resid"]["slack"])),
                             timing=res["timing"]))
            print(f"{name:12s} #{r.index:<5d} k={r.k} r={r.radius:.3e} {res['root']:9s} "
                  + " ".join(f"{k}={_fmt(x)}" for k, x in v.items())
                  + f"  mnorm_rel={res['diag']['mnorm_rel']:+.1e} k_ok={res['diag']['k_agree']}"
                  + f"  t={res['timing']['total']:.2f}s")
    keys = ["ort", "hor", "froot", "n0", "mnorm", "id", "C_base", "C_tensor"]
    print("\nSummary over", len(rows), "records")
    for k in keys:
        cnt = {True: 0, False: 0, None: 0}
        for row in rows:
            cnt[row["verdicts"][k]] += 1
        print(f"  {k:9s} pass={cnt[True]:3d} FAIL={cnt[False]:3d} undecided={cnt[None]:3d}")
    ct = {v: sum(1 for row in rows if row["root"] == v) for v in ("pass", "FAIL", "undecided")}
    print("  Root verdicts:", ct)
    tk = [row["timing"]["total"] for row in rows]
    print(f"  per-record cost: mean {sum(tk) / len(tk):.3f}s  max {max(tk):.3f}s  n={len(tk)}")
    if a.json:
        json.dump(rows, open(a.json, "w"), indent=1, default=str)


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
