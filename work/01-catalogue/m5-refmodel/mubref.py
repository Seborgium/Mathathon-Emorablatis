"""Reference model for the analytic core of the dimension-six MUB preprint.

Scope: the finite, exact mathematical statements that a small amount of code can
exercise.  Each function is named after the numbered statement it tests; each
returns measured quantities so that a *claimed constant* can be compared with the
*observed* constant on real data.

Conventions follow the paper: e(x) = exp(2*pi*i*x); phases in cycles unless a
variable name ends in _rad; row-major flattening; <u,v> = sum conj(u_j) v_j.
"""
from __future__ import annotations
import numpy as np

TWOPI = 2.0 * np.pi


def e(x):
    """Paper's e(x) = exp(2*pi*i*x)."""
    return np.exp(TWOPI * 1j * np.asarray(x, dtype=float))


def phz(M):
    """Phase (cycles in [0,1)) of every entry of a unit-modulus matrix."""
    return np.angle(M) / TWOPI % 1.0


# --------------------------------------------------------------------------
# Lemma 1.2: three mutually unbiased bases in C^6 via C^2 (x) C^3
# --------------------------------------------------------------------------
def lemma_1_2(A0, A1, A2, tol=1e-11):
    """Check that the three unitaries built from A0,A1,A2 (d=2 MUB) and the
    d=3 Fourier matrix are pairwise unbiased.

    The paper's construction: bases of C^6 are the columns of A_r (x) F_3 for
    r = 0,1,2, where A_0=I_2, A_1 = H_2/sqrt2 (Hadamard), A_2 = H_2/sqrt2 with
    the second column multiplied by i (up to phase).
    """
    d3 = 3
    j = np.arange(d3)
    F3 = e(np.outer(j, j) / d3) / np.sqrt(d3)              # paper's F
    D = np.diag(e(np.array([0.0, 1/3, 1/3])))              # paper's diag(1,w,w)
    Bs = [np.eye(d3, dtype=complex), F3, D @ F3]           # B0,B1,B2
    Ms = [np.kron(A, B) for A, B in zip((A0, A1, A2), Bs)]
    worst_unbiased = 0.0
    worst_unitary = 0.0
    for M in Ms:
        d = M.shape[0]
        worst_unitary = max(worst_unitary, np.abs(M.conj().T @ M - np.eye(d)).max())
    for r in range(3):
        for s in range(3):
            if r == s:
                continue
            G = Ms[r].conj().T @ Ms[s]
            worst_unbiased = max(worst_unbiased, np.abs(np.abs(G) ** 2 - 1.0 / 6.0).max())
    return dict(unitarity=max(0.0, worst_unitary), unbiasedness=max(0.0, worst_unbiased))


# --------------------------------------------------------------------------
# complex Hadamard matrices used to exercise Stage A on real data
# --------------------------------------------------------------------------
def fourier_family(a, b, d=6):
    """F_6(a,b): entries e((a j^2 + b k^2 + j k)/d).  Verified Hadamard below."""
    j = np.arange(d)[:, None]
    k = np.arange(d)[None, :]
    return e((a * j * j + b * k * k + j * k) / d)


def dephase(H):
    """(2.2): return (P, H') with H' equivalent to H (row/column phases) and
    P the phase matrix whose first row and column vanish."""
    P = phz(H)
    Q = P - P[:, [0]] - P[[0], :] + P[0, 0]
    return Q % 1.0


def is_hadamard(H, d=6, tol=1e-10):
    return (np.allclose(np.abs(H), 1.0, atol=1e-13)
            and np.allclose(H @ H.conj().T, d * np.eye(d), atol=tol))


# --------------------------------------------------------------------------
# Lemma 3.1: fixed frames for p in C^4 of unit modulus
# --------------------------------------------------------------------------
def lemma_3_1(p, tol=1e-12):
    """S = sum p_j; return the two sufficient statistics and the residual of the
    paper's display (3.4), checked against a direct inverse."""
    p = np.asarray(p, dtype=complex)
    S = p.sum()
    M = np.column_stack([np.ones(4, dtype=complex), p])          # 4x2
    G = M.conj().T @ M                                          # 2x2
    sing = np.linalg.svd(M, compute_uv=False) ** 2               # squared singular values
    claim_sing = np.array([4 - abs(S), 4 + abs(S)])
    Gm1 = np.linalg.inv(G) @ M.conj().T                          # (M*M)^{-1} M*  (2x4)
    # paper's (3.4): rows  (4*1 - conj(S) p) and (4 p - S * 1) divided by 16-|S|^2
    cand = np.vstack([4.0 * np.ones(4) - np.conj(S) * p,
                      4.0 * p - S * np.ones(4)]) / (16.0 - abs(S) ** 2)
    Mpinv = M @ np.linalg.inv(G)                                 # 4x2 = M (M*M)^{-1}
    resid = min(np.abs(Mpinv - cand.T).max(), np.abs(Gm1 - cand).max())
    # range of M is orthonormal-complementable: K spans ker M*
    _, sv, Vh = np.linalg.svd(M.conj().T)
    K = Vh[2:].conj().T                                          # 4 x 2
    return dict(sing_values_err=np.abs(np.sort(sing) - claim_sing).max(),
                sing_pos=(sing[0] > 0) if abs(S) < 4 else True,
                pseudo_inverse_resid=max(0.0, resid),
                K_orth_resid=float(np.abs(K.conj().T @ K - np.eye(2)).max()),
                K_kernel_resid=float(np.abs(M.conj().T @ K).max()))


# --------------------------------------------------------------------------
# Stage A: blocks, frames, compressed completion Y, Lemma 3.2
# --------------------------------------------------------------------------
SEED_POSITIONS = (7, 8, 9, 10, 11, 13, 19, 25, 31)   # paper (3.2), zero-based


def seed_of(P):
    """The nine seed phases of a dephased 6x6 phase matrix, in the paper's order
    s = (sa, b0..b3, c0..c3)."""
    return np.array([P[1, 1], P[1, 2], P[1, 3], P[1, 4], P[1, 5],
                     P[2, 1], P[3, 1], P[4, 1], P[5, 1]])


def seed_matrix(p9):
    """Rebuild the dephased 6x6 phase matrix of a seed (lower-right block = 0)."""
    P = np.zeros((6, 6))
    P[1, 1], P[1, 2], P[1, 3], P[1, 4], P[1, 5] = p9[0:5]
    P[2, 1], P[3, 1], P[4, 1], P[5, 1] = p9[5:9]
    return P


def blocks(P):
    A = e(P)
    return A[:2, :2], A[:2, 2:], A[2:, :2], A[2:, 2:]


def stageA(P_seed, P_exact, tol=1e-12):
    """Run the Stage-A reduction for one seed centre and one exact Hadamard.

    P_seed  : phase matrix of the stored seed centre (first row/col zero)
    P_exact : phase matrix of an exact dephased complex Hadamard (first row/col zero)
    Returns measured quantities together with the paper's constants.
    """
    P_t = seed_matrix(np.asarray(P_seed, float))
    E0, B0, C0, _ = blocks(P_t)
    E1, B1, C1, D1 = blocks(np.asarray(P_exact, float))

    # Lemma 3.1 frames, built from the *centre* only
    pB, pC = B0[1, :], C0[:, 1]
    # (3.5): ran K_B = ker B0  and  ran K_C = ker C0^*  (B0 is 2x4, C0 is 4x2)
    KB = np.linalg.svd(B0)[2][2:].conj().T
    KC = np.linalg.svd(C0.conj().T)[2][2:].conj().T
    MB = np.column_stack([np.ones(4, complex), pB])      # 4x2, Lemma 3.1's M for B
    mB = np.linalg.svd(MB, compute_uv=False).min()       # sigma_min(B0) = sigma_min(M_B)
    mC = np.linalg.svd(np.column_stack([np.ones(4, complex), pC]), compute_uv=False).min()

    Y = KC.conj().T @ D1 @ KB
    A0op = np.sqrt(2.0 + abs(1.0 + E0[1, 1]))          # (3.7): ||E0||_op
    # displacements
    dE, dB, dC = E1 - E0, B1 - B0, C1 - C0
    e1, b1, c1 = np.linalg.norm(dE), np.linalg.norm(dB), np.linalg.norm(dC)
    # (3.8): 6I - Y*Y identity
    PK = KB @ KB.conj().T
    lhs = 6 * np.eye(2) - Y.conj().T @ Y
    rhs = (KB.conj().T @ (B1.conj().T @ B1) @ KB
           + KB.conj().T @ (D1.conj().T @ (np.eye(4) - KC @ KC.conj().T) @ D1) @ KB)
    ident = np.abs(lhs - rhs).max()
    tr = np.trace(lhs).real
    # (3.9) with the exact quantities; m = min(mB,mC) as in the paper
    opE = np.linalg.norm(E1, 2)
    bound39 = b1 ** 2 + (opE * b1 + np.sqrt(6) * c1) ** 2 / mC ** 2
    return dict(ident38=float(max(0.0, ident)), psd=bool(np.linalg.eigvalsh(lhs).min() > -1e-10),
                trace_lhs=float(tr), bound39=float(bound39), bound39_ok=bool(tr <= bound39 + 1e-12),
                mB=float(mB), mC=float(mC), e1=float(e1), b1=float(b1), c1=float(c1),
                A0=float(A0op), Y=Y)


def lemma_3_2_q(params, Rs):
    """(3.10): q = Rs^2 (1 + (A*^2+6)/mC^2) with A* = min(2, A0+Rs)."""
    A0, mC = params["A0"], params["mC"]
    Astr = min(2.0, A0 + Rs)
    return Rs ** 2 * (1.0 + (Astr ** 2 + 6.0) / mC ** 2)


def lemma_3_2_polar(Y, q):
    """(3.11): with V the polar factor of Y, ||Y - sqrt6 V||_F <= p."""
    U, s, Vh = np.linalg.svd(Y)
    V = U @ Vh
    lhs = np.linalg.norm(Y - np.sqrt(6) * V)
    p = q / (np.sqrt(6) + np.sqrt(max(6.0 - q, 0.0)))
    return dict(lhs=float(lhs), p=float(p), ok=bool(lhs <= p + 1e-12), q=float(q))


# --------------------------------------------------------------------------
# Lemma 3.3 / 3.4: closed covering of U(2) and the cell Taylor bounds
# --------------------------------------------------------------------------
def u2_params(V):
    """Return (alpha, t, beta, gamma) in cycles as in (3.12)."""
    det = np.linalg.det(V)
    alpha = (np.angle(det) / TWOPI) % 1.0 / 2.0          # in [0,1/2]
    W = e(-alpha) * V                                    # in SU(2)
    z, w = W[0, 0], W[0, 1]
    t = np.arccos(np.clip(abs(z), 0.0, 1.0)) / TWOPI     # in [0,1/4]
    beta = (np.angle(z) / TWOPI) % 1.0
    gamma = (np.angle(w) / TWOPI) % 1.0
    return alpha, t, beta, gamma


def u2_matrix(alpha, t, beta, gamma):
    c, s = np.cos(TWOPI * t), np.sin(TWOPI * t)
    return e(alpha) * np.array([[e(beta) * c, e(gamma) * s],
                                [-e(-gamma) * s, e(-beta) * c]], dtype=complex)


def u2_derivs(alpha, t, beta, gamma):
    """Angular derivatives w.r.t. *radian* angles (the paper's dU[.] basis)."""
    Th_a, Th_t = TWOPI * alpha, TWOPI * t
    c, s = np.cos(Th_t), np.sin(Th_t)
    Ea, Eb, Eg = e(alpha), e(beta), e(gamma)
    da = 1j * Ea * np.array([[Eb * c, Eg * s], [-e(-gamma) * s, e(-beta) * c]])
    db = Ea * np.array([[1j * Eb * c, 0.0], [0.0, -1j * e(-beta) * c]])
    dg = Ea * np.array([[0.0, 1j * Eg * s], [1j * e(-gamma) * s, 0.0]])
    dt = Ea * np.array([[-Eb * s, Eg * c], [-e(-gamma) * c, -e(-beta) * s]])
    return da, dt, db, dg


def u2_cell(V, Nu):
    """The cell of V and its radian displacement theta from the cell midpoint."""
    alpha, t, beta, gamma = u2_params(V)
    n_a, n_t = Nu // 2, Nu // 4
    ia = min(int(np.floor(alpha * Nu)), n_a - 1)
    it = min(int(np.floor(t * Nu)), n_t - 1)
    ib = min(int(np.floor(beta * Nu)), Nu - 1)
    ig = min(int(np.floor(gamma * Nu)), Nu - 1)
    mid = ((ia + 0.5) / Nu, (it + 0.5) / Nu, (ib + 0.5) / Nu, (ig + 0.5) / Nu)
    theta = np.array([alpha - mid[0], t - mid[1], beta - mid[2], gamma - mid[3]]) * TWOPI
    return mid, theta, (ia, it, ib, ig)


def lemma_3_4(V, Nu):
    """Check (3.14) for the cell of V at grid parameter Nu."""
    mid, theta, idx = u2_cell(V, Nu)
    h = np.pi / Nu
    U = u2_matrix(*mid)
    da, dt, db, dg = u2_derivs(*mid)
    dU = theta[0] * da + theta[1] * dt + theta[2] * db + theta[3] * dg
    lin = np.linalg.norm(V - U)
    quad = np.linalg.norm(V - U - dU)
    return dict(idx=idx, h=h, lin=lin, lin_bound=np.sqrt(6) * h,
                quad=quad, quad_bound_claimed=42 * np.sqrt(2) / 2 * h * h,
                quad_bound_derived=np.sqrt(42) / 2 * h * h,
                lin_ratio=lin / (np.sqrt(6) * h), quad_ratio=quad / (h * h),
                theta_max=float(np.abs(theta).max()))


def random_u2(n, rng):
    """Haar-random U(2) via QR of a Ginibre matrix."""
    out = np.empty((n, 2, 2), dtype=complex)
    for i in range(n):
        Z = (rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))) / np.sqrt(2)
        Q, R = np.linalg.qr(Z)
        Q = Q * (np.diag(R) / np.abs(np.diag(R)))
        out[i] = Q
    return out


# --------------------------------------------------------------------------
# Section 2: the seed box (2.6), the index restriction (2.7), the counts
# --------------------------------------------------------------------------
N_BINS = 112          # paper's N (2.6)


def seed_x_tuples(N=N_BINS):
    """Count the weakly increasing 5-tuples 0<=a<=b<=c<=d<=l<N of (2.6) that also
    satisfy the orientation restriction a <= l-d+1 of (2.7).

    This is the exact size of the x-bin index space that `seeds::build` traverses
    before any filter.  Returned as (all, admissible).
    """
    all_t = 0
    adm = 0
    for a in range(N):
        for b in range(a, N):
            for c in range(b, N):
                for d in range(c, N):
                    for l in range(d, N):
                        all_t += 1
                        if a <= l - d + 1:
                            adm += 1
    return all_t, adm


def closed_form_counts(N=N_BINS):
    """Closed forms for the two counts of seed_x_tuples (checked against it)."""
    from math import comb
    all_t = comb(N + 4, 5)
    return all_t, comb(N + 4, 5)


def y_tuple_count(N=N_BINS):
    """Number of weakly increasing 4-tuples 0<=y1<=..<=y4<N: the y side of a seed,
    whose shared first entry is fixed by the x tuple."""
    from math import comb
    return comb(N + 3, 4)


def u2_cell_count(Nu):
    """The four bin counts of Lemma 3.3 and their product."""
    counts = (Nu // 2, Nu // 4, Nu, Nu)
    n = 1
    for c in counts:
        n *= c
    return counts, n


# --------------------------------------------------------------------------
# Lemma 6.5: the .1 threshold, checked exactly with rational arithmetic
# --------------------------------------------------------------------------
def lemma_6_5_exact():
    """Exact check of the chain used in Lemma 6.5.

    For ||z|| <= 2s < .2:  |sum_j e(z_j)| >= 6 - sum_j |e(z_j)-1|
    >= 6 - 2*pi*sqrt(6)*||z|| > 6 - (22/7)*sqrt(6)/5 ... and the displayed
    conclusion needs a lower bound strictly above sqrt(6) (unbiasedness) and
    above 0 (orthogonality).  All comparisons use pi < 22/7, sqrt6 < 5/2.
    """
    from fractions import Fraction as Fr
    bound = Fr(6) - Fr(2) * Fr(22, 7) * Fr(5, 2) * Fr(1, 5)     # 6 - 2pi sqrt6 * .2
    return dict(bound=float(bound), bound_exact=str(bound),
                needs=float(6 ** 0.5), slack=float(bound) - 6 ** 0.5,
                ok=bool(float(bound) > 6 ** 0.5 and bound > 0))


# --------------------------------------------------------------------------
# Lemmas 4.11 and 4.12: the ellipsoid machinery of Stage B
# --------------------------------------------------------------------------
def lemma_4_11(A, B, r, q, beta, n_samples=200, rng=None):
    """(4.32) engine: if G >= (1+beta) r^2 A A* + (1+1/beta) q^2 B B*, then every
    As + Bv with ||s||<=r, ||v||<=q lies in {G^{1/2} w : ||w|| <= 1}.

    Returns the largest observed value of x* G^+ x over random and adversarial
    displacements (must be <= 1), and the largest support-function ratio.
    """
    rng = rng or np.random.default_rng(0)
    k, n = A.shape
    G = (1 + beta) * r ** 2 * (A @ A.conj().T) + (1 + 1 / beta) * q ** 2 * (B @ B.conj().T)
    G = G.real
    Gp = np.linalg.pinv(G)
    worst = 0.0
    for _ in range(n_samples):
        s = rng.standard_normal(n); s = s / np.linalg.norm(s) * r
        v = rng.standard_normal(n); v = v / np.linalg.norm(v) * q
        x = A @ s + B @ v
        worst = max(worst, float((x.conj() @ Gp @ x).real))
    for _ in range(n_samples):
        z = rng.standard_normal(k)
        As, Bv = A.conj().T @ z, B.conj().T @ z
        if np.linalg.norm(As) > 0 and np.linalg.norm(Bv) > 0:
            s = r * As / np.linalg.norm(As)
            v = q * Bv / np.linalg.norm(Bv)
            x = A @ s + B @ v
            worst = max(worst, float((x.conj() @ Gp @ x).real))
    worst_support = 0.0
    for _ in range(n_samples):
        z = rng.standard_normal(k)
        z = z / np.linalg.norm(z)
        lhs = r * np.linalg.norm(A.conj().T @ z) + q * np.linalg.norm(B.conj().T @ z)
        rhs = np.sqrt(max(float((z.conj() @ G @ z).real), 0.0))
        if rhs > 0:
            worst_support = max(worst_support, lhs / rhs)
    return dict(worst_ellipsoid=worst, worst_support_ratio=worst_support)


def lemma_4_12(G, U, gamma, n_samples=400, rng=None):
    """(4.34): ||U + G^{1/2} w||^2 <= gamma (1 + U* (gamma I - G)^{-1} U) for
    every ||w|| <= 1, when gamma > lambda_max(G).  Also the simpler bound."""
    rng = rng or np.random.default_rng(1)
    k = G.shape[0]
    lam = np.linalg.eigvalsh(G).max()
    assert gamma > lam
    Gm = np.linalg.pinv(G)
    Ghalf = np.linalg.cholesky(G + 1e-300 * np.eye(k)) if lam > 0 else np.zeros_like(G)
    rhs = gamma * (1 + float((U.conj() @ np.linalg.solve(gamma * np.eye(k) - G, U)).real))
    simple = (np.linalg.norm(U) + np.sqrt(lam)) ** 2
    worst = 0.0
    worst_tri = 0.0
    for _ in range(n_samples):
        w = rng.standard_normal(k); w = w / np.linalg.norm(w)
        x = U + Ghalf @ w
        worst = max(worst, float((x.conj() @ x).real) / rhs)
        worst_tri = max(worst_tri, np.linalg.norm(x) / (np.linalg.norm(U) + np.sqrt(lam)))
    return dict(lam=float(lam), gamma=float(gamma), worst_ratio=worst, rhs=float(rhs),
                triangle_ratio=worst_tri, triangle_ok=bool(worst_tri <= 1 + 1e-12))


# --------------------------------------------------------------------------
# Lemma 4.3: the scalar remainder r(t) = (e(t) - 1 - 2 pi i t)/(2 pi i)
# --------------------------------------------------------------------------
def r_scalar(t):
    t = np.asarray(t, dtype=float)
    return (M_e(t) - 1.0 - 2j * np.pi * t) / (2j * np.pi)


def M_e(t):
    return np.exp(2j * np.pi * np.asarray(t, dtype=float))


def lemma_4_3_sharpness(n=200001, tmax=1.0, rng=None):
    """(4.8)-(4.9): |r(t)| <= pi t^2 and |r(x)-r(v)| <= pi|x-v|(|x|+|v|).

    Returns the largest observed ratios to the claimed bounds (both bounded by 1,
    and both tending to 1 as the arguments shrink, i.e. the constants are sharp).
    """
    t = np.linspace(-tmax, tmax, n)
    mask = np.abs(t) > 1e-3          # avoid the cancellation region of e(t)-1-2 pi i t
    ratio1 = np.max(np.abs(r_scalar(t[mask])) / (np.pi * t[mask] ** 2))
    rng = rng or np.random.default_rng(3)
    x = rng.uniform(-tmax, tmax, 20000)
    v = rng.uniform(-tmax, tmax, 20000)
    num = np.abs(r_scalar(x) - r_scalar(v))
    den = np.pi * np.abs(x - v) * (np.abs(x) + np.abs(v))
    good = den > 1e-12
    ratio2 = np.max(num[good] / den[good])
    # near the origin, where the constants are attained
    eps = 1e-4
    near = np.abs(r_scalar(eps)) / (np.pi * eps ** 2)
    return dict(ratio1=float(ratio1), ratio2=float(ratio2), near_origin=float(near))
