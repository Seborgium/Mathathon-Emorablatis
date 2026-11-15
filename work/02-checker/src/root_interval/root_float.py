"""Binary64 recomputation of the Root constants that depend only on (p, T).

Purpose: (i) validate our index/normalisation conventions against the stored
values produced by the authors' code (stored = float bound + bump), and
(ii) provide float *proposals* (never verdicts) for the interval checker.
"""
import numpy as np

PI = np.pi
EDGES = [(i, j) for i in range(6) for j in range(i)]        # (4.1) order
POS = (7, 8, 9, 10, 11, 13, 19, 25, 31)
PIJ = np.array([[((i // 6 == j // 6) - 1 / 6) * ((i % 6 == j % 6) - 1 / 6)
                 for j in range(36)] for i in range(36)])


def proj(M):
    """Pi x = x + mean/36 - (rowsum_i + colsum_j)/6 in the 6x6 matrix view."""
    M = np.asarray(M, float)
    A = M.reshape(M.shape[:-1] + (6, 6))
    g = A.sum(axis=(-2, -1)) / 36.0
    r = A.sum(axis=-1) / 6.0
    c = A.sum(axis=-2) / 6.0
    return (A + g[..., None, None] - r[..., :, None] - c[..., None, :]).reshape(M.shape)


def unit_matrix(p):
    return np.exp(2j * PI * np.asarray(p, float).reshape(6, 6))


def Fvec(p):
    """(4.1) as a real 30-vector, real part then imaginary part per edge."""
    u = unit_matrix(p)
    out = []
    for (i, j) in EDGES:
        s = np.sum(u[i] * np.conj(u[j]))
        out.append(s.imag / (2 * PI))
        out.append(-s.real / (2 * PI))
    return np.array(out)


def Lmat(p):
    """Full derivative (4.2) as a real 30x36 matrix (same row convention as Fvec)."""
    u = unit_matrix(p)
    out = np.zeros((30, 36))
    at = 0
    for (i, j) in EDGES:
        q = u[i] * np.conj(u[j])          # cos + i sin of the phase differences
        for g in range(6):
            out[at, 6 * i + g] = q[g].real      # d Im F / d x_ig
            out[at, 6 * j + g] = -q[g].real
            out[at + 1, 6 * i + g] = q[g].imag  # d (-Im ... ) see patchx fullL
            out[at + 1, 6 * j + g] = -q[g].imag
        at += 2
    return out


def root_float(p, T):
    T = np.asarray(T, float).reshape(-1, 36)
    k = T.shape[0]
    fv = Fvec(p)
    froot = np.linalg.norm(fv)
    G = T @ T.T
    ort = np.linalg.norm(G - np.eye(k)) if k else 0.0
    hor = np.linalg.norm(proj(T.copy()) - T) if k else 0.0
    return dict(froot=froot, ort=ort, hor=hor, F=fv, L=Lmat(p), T=T)


def best_M(p, T, eps=0.0):
    """Minimum-norm least-squares M for (4.15): rows solved independently."""
    T = np.asarray(T, float).reshape(-1, 36)
    k = T.shape[0]
    L = proj(Lmat(p))                       # LP Pi, 30x36
    Y = PIJ - (T.T @ T if k else 0.0)       # Pi - T T^*
    if eps:
        Y = Y.copy()
    pinv = np.linalg.pinv(L)                # 36x30
    M = Y @ pinv                            # 36x30
    R = Y - M @ L
    return M, R
