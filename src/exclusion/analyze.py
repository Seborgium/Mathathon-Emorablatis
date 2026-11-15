"""Directions, the exact optimal direction, and the second-order certificate.

Everything is float64 here; rigorous high-precision verification is in verify.py.
"""
import numpy as np
from cell import Cell

# ------------------------------------------------------------------ blocks
def block_ops(cell):
    """A_k as linear maps on the dual variables, acting on R^20."""
    ops = {}
    ops['s'] = (cell.Jall[:, :9], 'ball', cell.Rs)          # ||v_s|| <= Rs
    ops['t'] = (cell.Jall[:, 9:].copy(), 'box', cell.h)     # ||v_t||_inf <= h
    W = np.zeros((20, 16)); W[np.arange(16), np.arange(16)] = cell.Wabs
    ops['D'] = (W, 'ball', cell.Er)                         # ||v_D|| <= Er
    Z = np.zeros((20, 16)); Z[np.arange(16), np.arange(16)] = 1.0
    ops['z'] = (Z, 'neg', 0.5 * cell.z ** 2)                # v <= 0, ||v||_1 <= z^2/2
    X = np.zeros((20, 2)); X[16, 0] = X[17, 1] = 1.0
    ops['X'] = (X, 'ball', 0.5 * cell.Rs ** 2)
    Y = np.zeros((20, 2)); Y[18, 0] = Y[19, 1] = 1.0
    ops['Y'] = (Y, 'ball', 0.5 * cell.Rs ** 2)
    return ops

def proj(kind, r, rad):
    if kind == 'ball':
        n = np.linalg.norm(r)
        return r * (rad / n) if n > rad else r
    if kind == 'box':
        return np.clip(r, -rad, rad)
    if kind == 'neg':                     # {v<=0, sum|v| <= rad}
        v = np.maximum(r, 0.0)            # projection onto v<=0 direction reversed below
        # projection of r onto {v<=0, ||v||_1<=rad}: x = -proj of -r onto simplex-scaled set
        x = -_proj_simplex_ball(-r, rad)
        return x
    raise ValueError(kind)

def _proj_simplex_ball(z, rad):
    """project z onto {x >= 0, ||x||_1 <= rad}"""
    if z.sum() <= rad and z.min() >= 0:
        return np.maximum(z, 0)
    # euclidean projection onto {x>=0, sum x <= rad}: bisect on the shift
    lo, hi = z.min(), z.max() + 1.0
    for _ in range(200):
        mu = 0.5 * (lo + hi)
        x = np.maximum(z - mu, 0.0)
        if x.sum() > rad:
            lo = mu
        else:
            hi = mu
    return np.maximum(z - hi, 0.0)

def dual_optimal(cell, iters=3000, tol=1e-15):
    """min over dual variables of || c_all - sum_k A_k v_k ||_2.

    Strong duality: this equals max_{||y||<=1} (y.c_all - B1(y)) (Sion).
    """
    ops = block_ops(cell)
    keys = list(ops)
    v = {k: np.zeros(ops[k][0].shape[1]) for k in keys}
    def w_of(v):
        w = np.zeros(20)
        for k in keys:
            w += ops[k][0] @ v[k]
        return w
    # FISTA on the smooth convex objective 1/2||c - A v||^2
    L = 0.0
    for k in keys:
        L += np.linalg.norm(ops[k][0], 2) ** 2
    L = max(L, 1e-12)
    c = cell.c_all
    vold = {k: v[k].copy() for k in keys}
    zz = {k: v[k].copy() for k in keys}
    t = 1.0
    prev = np.inf
    for it in range(iters):
        w = w_of(zz)
        r = c - w
        for k in keys:
            A, kind, rad = ops[k]
            g = A.T @ r
            vnew = proj(kind, zz[k] + g / L, rad)
            v[k] = vnew
        tn = 0.5 * (1 + np.sqrt(1 + 4 * t * t))
        for k in keys:
            zz[k] = v[k] + ((t - 1) / tn) * (v[k] - vold[k])
        vold = {k: v[k].copy() for k in keys}
        t = tn
        if it % 50 == 0:
            w = w_of(v)
            if np.linalg.norm(c - w) < tol or it > 400 and abs(np.linalg.norm(c-w)-prev) < 1e-16*max(1.0,np.linalg.norm(c)):
                break
            prev = np.linalg.norm(c - w)
    w = w_of(v)
    y = c - w
    return y, v, np.linalg.norm(y)

# ------------------------------------------------- second-order certificate
def quad_form(cell, Yp):
    """Q (13x13) with ||sqrt(Yp) o J(u)||^2 = u^T Q u, and the linear map Jbar."""
    Q = np.zeros((13, 13))
    for i in range(4):
        for j in range(4):
            w = Yp[i, j]
            if w == 0.0:
                continue
            a = cell.Jc[i, j, :].real
            b = cell.Jc[i, j, :].imag
            Q += 2.0 * w * (np.outer(a, a) + np.outer(b, b))
    return 0.5 * Q            # so that 0.5*u^T Q u = 0.5*sum Yp|J|^2

def _tr(g, Q, rho):
    """min over ||u|| <= rho of g.u + 0.5 u^T Q u   (Q symmetric PSD), exact by 1-D secular equation."""
    if rho <= 0:
        return 0.0
    n = len(g)
    lam_min = np.linalg.eigvalsh(Q)[0]
    def sol(lam):
        M = Q + lam * np.eye(n)
        return -np.linalg.solve(M, g)
    u = sol(0.0)
    if np.linalg.norm(u) <= rho:
        return g @ u + 0.5 * u @ Q @ u
    lo = max(0.0, -lam_min)
    u = sol(lo * (1 + 1e-12) + 1e-300)
    hi = max(1.0, np.linalg.norm(g) / rho)
    while np.linalg.norm(sol(hi)) > rho:
        hi *= 2.0
        if hi > 1e20:
            break
    for _ in range(120):
        mid = 0.5 * (lo + hi)
        if np.linalg.norm(sol(mid)) > rho:
            lo = mid
        else:
            hi = mid
    u = sol(hi)
    u = u * min(1.0, rho / max(np.linalg.norm(u), 1e-300))
    return g @ u + 0.5 * u @ Q @ u

def min_K_quad(cell, g, Q, x0=None):
    """min over K = {||s||<=Rs, |theta_j|<=h} of  g.u + 0.5 u^T Q u  (Q PSD).

    Convex QP in 13 variables; solved by SLSQP, then checked against the KKT system
    (which is sufficient for a global minimum of a convex program).  Returns
    (value, u, kkt_residual).
    """
    from scipy.optimize import minimize
    Rs, h = cell.Rs, cell.h
    cons = [{'type': 'ineq', 'fun': lambda u: Rs ** 2 - u[:9] @ u[:9],
             'jac': lambda u: np.concatenate([-2 * u[:9], np.zeros(4)])}]
    bnds = [(None, None)] * 9 + [(-h, h)] * 4
    f = lambda u: g @ u + 0.5 * u @ Q @ u
    jac = lambda u: g + Q @ u
    best = None
    starts = [np.zeros(13)]
    u1 = np.zeros(13)
    u1[:9] = Rs * g[:9] / max(np.linalg.norm(g[:9]), 1e-300)
    u1[9:] = h * np.sign(g[9:])
    starts.append(u1)
    if x0 is not None:
        starts.append(x0)
    for st in starts:
        r = minimize(f, st, jac=jac, bounds=bnds, constraints=cons, method='SLSQP',
                     options=dict(ftol=1e-16, maxiter=500))
        if r.success or r.fun < (best.fun if best is not None else np.inf):
            if best is None or r.fun < best.fun:
                best = r
    u = best.x
    val = f(u)
    # KKT: grad = Q u + g = -lam * (2 s, 0) + (0, mu) with lam>=0, mu_i sign-consistent
    grad = Q @ u + g
    lam = max(0.0, -grad[:9] @ u[:9] / (2 * max(u[:9] @ u[:9], 1e-300)))
    res = np.abs(grad[:9] + 2 * lam * u[:9]).max()
    for k in range(4):
        i_ = 9 + k
        if abs(abs(u[i_]) - h) < 1e-12:
            res = max(res, 0.0)
            if u[i_] * grad[i_] < 0:      # multiplier sign wrong
                res = max(res, abs(grad[i_]))
        else:
            res = max(res, abs(grad[i_]))
    res = max(res, max(0.0, u[:9] @ u[:9] - Rs ** 2))
    return val, u, res

def B2(cell, y, kap=None):
    """Second-order right-hand side (see report): strictly below B1 on Y>=0."""
    y = np.asarray(y, float)
    Yd = y[:16].reshape(4, 4)
    Yp = np.maximum(Yd, 0.0); Yn = max(0.0, -Yd.min())
    g = cell.Jall.T @ y
    Q = quad_form(cell, Yp)
    u_part, ustar, kkt = min_K_quad(cell, g, Q)
    if kap is None:
        kap = sigma_J(cell) * np.sqrt(cell.Rs ** 2 + 4 * cell.h ** 2)
    delta = np.sqrt(max(0.0, Yp.max())) * cell.Er * kap
    return (-u_part + cell.Er * np.linalg.norm(cell.Wabs * y[:16])
            + 0.5 * cell.z ** 2 * Yn
            + 0.5 * cell.Rs ** 2 * (np.linalg.norm(y[16:18]) + np.linalg.norm(y[18:20]))
            + delta), delta

def sigma_J(cell):
    """sigma_max of the real 32x13 map u -> vec(J(u))."""
    M = np.zeros((32, 13))
    for k in range(13):
        Jk = cell.Jc[:, :, k]
        M[:16, k] = np.real(Jk).reshape(-1)
        M[16:, k] = np.imag(Jk).reshape(-1)
    return np.linalg.norm(M, 2)

def margin2(cell, y):
    b2, d = B2(cell, y)
    return (y @ cell.c_all - b2) / np.linalg.norm(y), d

# ---------------------------------------------------------------- merged certificate
def gain_rev(cell, y):
    """(1/2) sum_ij (y_D,ij)_+ (|D_ij|-1)^2 : the reverse-triangle gain (rigorous)."""
    Yp = np.maximum(np.asarray(y, float)[:16].reshape(4, 4), 0.0)
    return 0.5 * float(np.sum(Yp * (np.abs(cell.D) - 1.0) ** 2))

def margin3(cell, y):
    """margin of the merged certificate  y.c <= B(y) - gain_rev."""
    return y @ cell.c_all - cell.B1(y) + gain_rev(cell, y)

# ---------------------------------------------------------------- heuristic analogue
def heuristic(cell, iters=60, reg0=0.2, floor=0.03):
    """Analogue of the authors' proposer.

    The source routine `coverSeeds::supdual` (covout.cpp, lines 40-72) solves its small
    problem by regularised normal equations (M[a][a] += reg) followed by weight updates
    ww[j] = 1/max(|z_j|, .03) and reg[e] = 2*err/max(.02, q).  This is that scheme
    lifted to the 20 equations of (3.29): we maximise the quadratic surrogate
        y.c_all - sum_k w_k ||A_k^T y||^2
    by a regularised solve, then update the weights from the current residuals.
    It is a documented analogue, not the authors' code.
    """
    ops = block_ops(cell)
    keys = list(ops)
    n = 20
    w = {k: 1.0 for k in keys}
    reg = 0.2
    best = None
    y = cell.c_all / max(np.linalg.norm(cell.c_all), 1e-300)
    for it in range(iters):
        M = reg * np.eye(n)
        for k in keys:
            A = ops[k][0]
            M += w[k] * (A @ A.T)
        y = np.linalg.solve(M, cell.c_all)
        ny = np.linalg.norm(y)
        if ny < 1e-14:
            break
        y = y / ny
        m = cell.margin(y)
        if best is None or m > best[0]:
            best = (m, y.copy())
        for k in keys:
            A = ops[k][0]
            z = A.T @ y
            nz = np.linalg.norm(z)
            w[k] = 1.0 / max(nz, floor)
        reg = max(0.02, 2 * reg * 0.5)
    if best is None:
        return cell.margin(y), y
    return best
