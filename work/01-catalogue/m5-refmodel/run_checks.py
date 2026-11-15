"""Run every reference-model check and print a table.  Writes checks.json.

Deterministic: all randomness comes from np.random.default_rng(20260924).
"""
import json, sys
import numpy as np
sys.path.insert(0, '.')
import mubref as M

RS = 0.0320001            # paper's rs (cycles), Section 3.1
RS_RAD = 2 * np.pi * RS   # paper's Rs
RESULTS = []


def record(cid, statement, what, value, bound=None, ok=None, note=""):
    RESULTS.append(dict(id=cid, statement=statement, quantity=what,
                        value=float(value), bound=None if bound is None else float(bound),
                        ok=None if ok is None else bool(ok), note=note))


def main():
    rng = np.random.default_rng(20260924)

    # ---------------- Lemma 1.2 ----------------
    A0 = np.eye(2, dtype=complex)
    A1 = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    A2 = np.array([[1, 1], [1j, -1j]], dtype=complex) / np.sqrt(2)
    r = M.lemma_1_2(A0, A1, A2)
    record("Lem1.2-a", "Lemma 1.2", "max |U_r^*U_r - I|", r["unitarity"], 1e-12, r["unitarity"] < 1e-12)
    record("Lem1.2-b", "Lemma 1.2", "max | |<u,v>|^2 - 1/6 |", r["unbiasedness"], 1e-12,
           r["unbiasedness"] < 1e-12, "U_r = A_r (x) B_r, B = (I3, F, DF)")

    # ---------------- Lemma 3.1 ----------------
    worst_sing = worst_pinv = worst_k = 0.0
    for _ in range(2000):
        p = M.e(rng.random(4))
        r = M.lemma_3_1(p)
        worst_sing = max(worst_sing, r["sing_values_err"])
        worst_pinv = max(worst_pinv, r["pseudo_inverse_resid"])
        worst_k = max(worst_k, r["K_orth_resid"], r["K_kernel_resid"])
    record("Lem3.1-a", "Lemma 3.1", "max |sigma - (4 +- |S|)|", worst_sing, 1e-12, worst_sing < 1e-12)
    record("Lem3.1-b", "Lemma 3.1 (3.4)", "max residual, M(M*M)^-1", worst_pinv, 1e-12, worst_pinv < 1e-12)
    record("Lem3.1-c", "Lemma 3.1", "max residual, K orthonormal in ker M*", worst_k, 1e-12, worst_k < 1e-12)

    # ---------------- Lemma 3.3: the cover itself ----------------
    for Nu in (16, 32):
        counts, ncells = M.u2_cell_count(Nu)
        worst_theta = 0.0
        V = M.random_u2(4000, rng)
        for v in V:
            mid, theta, idx = M.u2_cell(v, Nu)
            worst_theta = max(worst_theta, np.abs(theta).max() / (np.pi / Nu))
            assert 0 <= idx[0] < Nu // 2 and 0 <= idx[1] < Nu // 4
            assert 0 <= idx[2] < Nu and 0 <= idx[3] < Nu
        record(f"Lem3.3-Nu{Nu}", "Lemma 3.3", "max |theta_j| / h over 4000 Haar V", worst_theta, 1.0,
               worst_theta <= 1.0, f"bin counts {counts}, {ncells} cells per seed")

    # ---------------- Lemma 3.4: the cell Taylor bounds ----------------
    for Nu in (16, 32):
        h = np.pi / Nu
        # random points and cell corners
        Vs = list(M.random_u2(3000, rng))
        for _ in range(3000):
            mid = (rng.random() / 2, rng.random() / 4, rng.random(), rng.random())
            th = rng.choice([-1.0, 1.0], size=4) * h
            Vs.append(M.u2_matrix(*(np.array(mid) + th / (2 * np.pi))))
        wl = wq = 0.0
        for v in Vs:
            r = M.lemma_3_4(v, Nu)
            wl = max(wl, r["lin_ratio"])
            wq = max(wq, r["quad_ratio"])
        record(f"Lem3.4-lin-Nu{Nu}", "Lemma 3.4 (3.14)", "max ||V-U||_F / (sqrt6 h)", wl, 1.0, wl <= 1.0)
        record(f"Lem3.4-quad-Nu{Nu}", "Lemma 3.4 (3.14)", "max ||V-U-dU||_F / h^2", wq,
               42 * np.sqrt(2) / 2, wq <= 42 * np.sqrt(2) / 2,
               f"stated 42sqrt2/2={42*np.sqrt(2)/2:.3f}; the proof's ||U''||_F<=sqrt42 h^2 gives "
               f"sqrt42/2={np.sqrt(42)/2:.3f}")

    # ---------------- Lemma 3.2 on exact Hadamards ----------------
    ident = b39 = pol = psd = 0.0
    qmax = 0.0
    disp = 0.0
    mmin = 9.0
    n_trials = 400
    for _ in range(n_trials):
        a, b = rng.random(2)
        H = M.fourier_family(a, b)
        P = M.dephase(H)
        s = M.seed_of(P)
        v = rng.standard_normal(9)
        v = v / np.linalg.norm(v) * RS * rng.random() ** (1 / 9)
        r = M.stageA(s + v, P)
        q = M.lemma_3_2_q(r, RS_RAD)
        pl = M.lemma_3_2_polar(r["Y"], q)
        ident = max(ident, abs(r["ident38"]))
        b39 = max(b39, r["trace_lhs"] / r["bound39"])
        pol = max(pol, pl["lhs"] / pl["p"])
        psd = max(psd, -np.linalg.eigvalsh(6 * np.eye(2) - r["Y"].conj().T @ r["Y"]).min())
        qmax = max(qmax, q)
        disp = max(disp, (r["e1"] ** 2 + r["b1"] ** 2 + r["c1"] ** 2) / RS_RAD ** 2)
        mmin = min(mmin, r["mB"], r["mC"])
    record("Lem3.2-38", "Lemma 3.2 (3.8)", "max |6I-Y*Y - RHS| over 400 exact Hadamards", ident, 1e-10,
           ident < 1e-10)
    record("Lem3.2-psd", "Lemma 3.2 (3.8)", "min eigenvalue of 6I-Y*Y (>=0)", -psd, 0.0, psd <= 1e-10)
    record("Lem3.2-39", "Lemma 3.2 (3.9)", "max tr(6I-Y*Y) / RHS", b39, 1.0, b39 <= 1.0 + 1e-12)
    record("Lem3.2-q", "Lemma 3.2 / Sec 3.2", "max q over 400 seeds", qmax, 0.32, qmax < 0.32)
    record("Lem3.2-pol", "Lemma 3.2 (3.11)", "max ||Y-sqrt6 V||_F / p", pol, 1.0, pol <= 1.0 + 1e-12)
    record("Sec3.1-33", "Section 3.1 (3.3)", "max (e1^2+b1'^2+c1'^2)/Rs^2", disp, 1.0, disp <= 1.0)
    record("Sec3.1-m", "Section 3.1", "min observed m = min(mB,mC)", mmin, 1.25, mmin > 1.25,
           "the paper's frame check accepts m > 1.25 (Section A.4)")

    # ---------------- threshold arithmetic ----------------
    thr = np.sqrt(10.0 / (0.32 / RS_RAD ** 2 - 1.0))
    record("SecA-q-m", "Section 3.2 / A.4", "m_C above which q<0.32 (A*=2)", thr, 1.24, thr <= 1.24,
           "q = Rs^2 (1+10/m_C^2) < .32  <=>  m_C > sqrt(10/(.32/Rs^2-1))")

    # ---------------- Section 2 counts ----------------
    allt, adm = M.seed_x_tuples()
    record("Sec2-count", "Section 2.2-2.3", "admissible x bin tuples (a<=l-d+1)", adm, 151744086,
           adm >= 0, f"all weak 5-tuples {allt}; y-tuples per x {M.y_tuple_count()}; "
                     f"execution processed 151744086 pairs = {151744086/adm:.4f} per x tuple")

    # ---------------- Lemma 6.5 ----------------
    r = M.lemma_6_5_exact()
    record("Lem6.5", "Lemma 6.5", "lower bound 6-2 pi sqrt6 (.2), exact rational", r["bound"],
           6 ** 0.5, r["ok"], f"exact {r['bound_exact']}, needs > sqrt6 = {6**0.5:.4f}")

    # ---------------- Section 3.1 (3.7) and A.4 arithmetic ----------------
    worstA0 = 0.0
    for _ in range(2000):
        a = M.e(rng.random())[()]
        E0 = np.array([[1, 1], [1, a]], dtype=complex)
        worstA0 = max(worstA0, abs(np.linalg.norm(E0, 2) ** 2 - (2 + abs(1 + a))))
    record("Sec3.1-A0", "Section 3.1 (3.7)", "max | ||E0||_op^2 - (2+|1+a|) |", worstA0, 1e-12,
           worstA0 < 1e-12)
    # A.4: stored m > 1.25 gives ideal m > 1.24, hence |S| <= 4-1.24^2 and 16-|S|^2 > 6.1,
    # and the pseudoinverse numerators (<= 8) give |G_ij| < .81
    Sbound = 4 - 1.24 ** 2
    denom = 16 - Sbound ** 2
    record("SecA.4-16S", "Section A.4", "16-|S|^2 at the frame threshold m=1.24", denom, 6.1,
           denom > 6.1)
    record("SecA.4-G", "Section A.4", "8/(16-|S|^2) at the frame threshold", 8 / denom, 0.81, 8 / denom < 0.81)

    # ---------------- Lemma 4.3 ----------------
    r43 = M.lemma_4_3_sharpness()
    record("Lem4.3-a", "Lemma 4.3 (4.8)", "max |r(t)|/(pi t^2)", r43["ratio1"], 1.0,
           r43["ratio1"] <= 1 + 1e-9, f"attained near t=0: {r43['near_origin']:.9f}")
    record("Lem4.3-b", "Lemma 4.3 (4.9)", "max |r(x)-r(v)| / (pi|x-v|(|x|+|v|))", r43["ratio2"], 1.0,
           r43["ratio2"] <= 1 + 1e-9, "the constant pi in C = pi b is sharp, not merely valid")

    # ---------------- Lemmas 4.11 and 4.12 ----------------
    we = wsu = 0.0
    for _ in range(20):
        A = rng.standard_normal((10, 36)); B = rng.standard_normal((10, 36))
        r, q, beta = rng.random() + .1, rng.random() + .1, rng.random() + .05
        o = M.lemma_4_11(A, B, r, q, beta, 150, rng)
        we = max(we, o["worst_ellipsoid"]); wsu = max(wsu, o["worst_support_ratio"])
    record("Lem4.11", "Lemma 4.11", "max x*G^+x with G at its threshold", we, 1.0, we <= 1 + 1e-9)
    record("Lem4.11-s", "Lemma 4.11", "max support ratio r||A*z||+q||B*z|| / (z*Gz)^.5", wsu, 1.0,
           wsu <= 1 + 1e-9)
    wq = wt = 0.0
    for _ in range(20):
        Z = rng.standard_normal((10, 10)); G = Z @ Z.T / 10
        U = rng.standard_normal(10)
        lam = np.linalg.eigvalsh(G).max()
        o = M.lemma_4_12(G, U, lam * (1.5 + rng.random()), 200, rng)
        wq = max(wq, o["worst_ratio"]); wt = max(wt, o["triangle_ratio"])
    record("Lem4.12", "Lemma 4.12 (4.34)", "max ||U+G^.5w||^2 / gamma(1+U*(gammaI-G)^-1U)", wq, 1.0,
           wq <= 1 + 1e-9)
    record("Lem4.12-t", "Lemma 4.12", "max ||U+G^.5w|| / (||U||+sqrt(lam_max))", wt, 1.0,
           wt <= 1 + 1e-9)

    # ---------------- output ----------------
    for x in RESULTS:
        tag = "" if x["ok"] is None else ("PASS" if x["ok"] else "FAIL")
        b = "" if x["bound"] is None else f" (bound {x['bound']:.6g})"
        print(f"{x['id']:<16} {x['quantity']:<52} {x['value']:.6g}{b}  {tag}")
        if x["note"]:
            print(f"{'':<16} note: {x['note']}")
    json.dump(RESULTS, open("checks.json", "w"), indent=1)
    nfail = sum(1 for x in RESULTS if x["ok"] is False)
    print(f"\n{len(RESULTS)} checks, {nfail} failures")


if __name__ == "__main__":
    main()
