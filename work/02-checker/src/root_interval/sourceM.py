"""Reconstruction of the auxiliary map M of Section 4.2 from p alone.

The source (patchx.cpp buildH::patch) never serialises M: it is built from an
approximate eigendecomposition of the 25x25 horizontal Jacobi Gram J^T J,
splitting at eigenvalue .64 (below -> column of T, at/above -> factor of M).
We reconstruct the same object numerically:
    M = sum_{eig >= .64} h_i l_i^T ,  h_i = Q v_i ,  l_i = J v_i / eig_i .
This is a *proposal*; every property we rely on is re-checked by the interval
code.  It also lets us test whether the stored mnorm / C / id are reproducible
from the stored (p, T) alone, i.e. whether M must be serialised.
"""
import numpy as np
import root_float as rf

def basis_q():
    q = np.zeros((6, 5))
    for j in range(5):
        u = 1.0 / np.sqrt((j + 1.0) * (j + 2.0))
        for i in range(j + 1):
            q[i, j] = u
        q[j + 1, j] = -(j + 1.0) * u
    return q

Q0 = basis_q()
Q = np.zeros((36, 25))
for i in range(6):
    for j in range(6):
        for a in range(5):
            for b in range(5):
                Q[6 * i + j, 5 * a + b] = Q0[i, a] * Q0[j, b]


def source_M(p, split=0.64):
    """Return dict with J, Gram, eigenvalues, M, ah, al, mnorm, C, and T-proposal."""
    L = rf.Lmat(p)                 # 30x36
    J = L @ Q                      # 30x25
    G = J.T @ J                    # 25x25
    w, V = np.linalg.eigh(G)
    HV = Q @ V                     # 36x25
    LV = np.zeros((30, 25))
    for i in range(25):
        LV[:, i] = (J @ V[:, i]) / w[i] if w[i] > 0 else 0.0
    small = w < split
    big = ~small
    M = (HV[:, big] * 1.0) @ LV[:, big].T      # 36x30
    def rowsumbound(A):
        # max_i sum_j |<A_:,i, A_:,j>|
        Gm = A.T @ A
        return np.max(np.sum(np.abs(Gm), axis=1))
    ah = rowsumbound(HV[:, big])
    al = rowsumbound(LV[:, big])
    mnorm = np.sqrt((ah + 1e-8) * (al + 1e-8)) + 1e-8
    C = np.pi * np.sqrt(8.0) * mnorm + 1e-7
    return dict(J=J, G=G, w=w, V=V, M=M, HV=HV, LV=LV, small=small, big=big,
                ah=ah, al=al, mnorm=mnorm, C=C, k=int(small.sum()),
                Tprop=HV[:, small].T, scale=np.max(np.abs(J)) if J.size else 0.0)
