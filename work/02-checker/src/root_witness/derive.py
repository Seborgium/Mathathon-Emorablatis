"""Reproduce the source's auxiliary map M from a stored record, and measure the slack.

Reconstruction (patchx.cpp:buildH::patch, read literally):
  q[i][a] = 1/sqrt((a+1)(a+2)) for i<=a ;  q[a+1][a] = -(a+1)/sqrt((a+1)(a+2))
  Q[6i+j][5a+b] = q[i][a] q[j][b]           (orthonormal basis of ran Pi, 36x25)
  J = L_P Q  (30x25),  Gram = J^T J (25x25),  eigendecomposition
  eig < .64  -> column of T (lifted hvec = Q v)
  eig >= .64 -> HV column = Q v, LV column = J v / eig ;  M = HV LV^T
Then ||M||_2 is compared with the stored mnorm (the source's certified upper bound) and the
residual Pi - T T* - M L_P Pi with the stored id.
"""
import math
import numpy as np
import records as R


def Qbasis():
    q = np.zeros((6, 5))
    for a in range(5):
        u = 1.0 / math.sqrt((a + 1.0) * (a + 2.0))
        for i in range(a + 1):
            q[i, a] = u
        q[a + 1, a] = -(a + 1.0) * u
    Q = np.zeros((36, 25))
    for i in range(6):
        for j in range(6):
            for a in range(5):
                for b in range(5):
                    Q[6 * i + j, 5 * a + b] = q[i, a] * q[j, b]
    return Q


Q = Qbasis()


def PI():
    P = np.zeros((36, 36))
    for i in range(36):
        for j in range(36):
            P[i, j] = ((i // 6 == j // 6) - 1 / 6) * ((i % 6 == j % 6) - 1 / 6)
    return P


PI36 = PI()


def fullL(p):
    A = np.exp(2j * math.pi * np.array(p).reshape(6, 6))
    L = np.zeros((30, 36))
    at = 0
    for i in range(6):
        for j in range(i):
            qq = A[i, :] * np.conj(A[j, :])
            for g in range(6):
                L[at, 6 * i + g] = qq[g].real
                L[at, 6 * j + g] = -qq[g].real
                L[at + 1, 6 * i + g] = qq[g].imag
                L[at + 1, 6 * j + g] = -qq[g].imag
            at += 2
    return L


def derive(r):
    """Return dict with T_rec, M, subspace mismatch, residual."""
    J = fullL(r.p) @ Q
    Gram = J.T @ J
    lam, V = np.linalg.eigh(Gram)
    small = lam < 0.64
    Ts = Q @ V[:, small]                # 36 x k
    Hg = Q @ V[:, ~small]               # 36 x (25-k)
    Lg = (J @ V[:, ~small]) / lam[~small]
    M = Hg @ Lg.T
    Tst = np.array(r.T).reshape(r.k, 36).T if r.k else np.zeros((36, 0))
    # subspace mismatch: ||P_Ts - P_Tst||_F  (sign/order free)
    P1 = Ts @ Ts.T
    P2 = Tst @ Tst.T if r.k else np.zeros((36, 36))
    return dict(M=M, lam=lam, sub=np.linalg.norm(P1 - P2), k_rec=int(small.sum()),
                resid=np.linalg.norm(PI36 - Tst @ Tst.T - M @ (fullL(r.p) @ PI36)),
                Mnorm=np.linalg.svd(M, compute_uv=False)[0])


def report(path, idxs):
    v = R.read(path)
    print("== %s" % path.split("/")[-1])
    print("  idx   k  k_rec  sub      ||M||_2   mnorm     mnorm/||M||  mnorm-||M||  resid     id")
    for n in idxs:
        r = v[n]
        d = derive(r)
        print("  %4d  %d   %2d   %.2e  %.9f  %.9f  %.9f   %+.2e  %.2e  %.2e"
              % (n, r.k, d["k_rec"], d["sub"], d["Mnorm"], r.mnorm, r.mnorm / d["Mnorm"],
                 r.mnorm - d["Mnorm"], d["resid"], r.id))
    ratios = []
    kk = {}
    for n in range(len(v)):
        r = v[n]
        d = derive(r)
        ratios.append(r.mnorm / d["Mnorm"])
        kk[d["k_rec"]] = kk.get(d["k_rec"], 0) + 1
    ratios = np.array(ratios)
    print("  over %d records: mnorm/||M||_2  min %.9f  median %.9f  max %.9f ; min ratio-1 = %.3e"
          % (len(v), ratios.min(), np.median(ratios), ratios.max(), ratios.min() - 1))
    print("  reconstructed k histogram:", kk)


if __name__ == "__main__":
    report(R.DATA + "coarse0.bin", [0, 1, 2, 3, 382, 700])
    report(R.DATA + "fb1.bin", [0, 1, 2, 563])
