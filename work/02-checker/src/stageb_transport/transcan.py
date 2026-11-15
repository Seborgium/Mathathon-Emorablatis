"""Exhaustive transport-map relation scan for one Stage-B parent.

Mechanism sought (H2 report section 4.4 item 2, "transported-frame relations"):
the base-grid ledger of `bad10#0` tests only the identity map for each child, so
1452 boxes are reported UNRESOLVED.  A Stage-B edge is (child Q, map Phi, ell) with

    dq = Pi( wrap( dp(Phi Q) - dp(P) ) ),   ||dq|| <= cut,
    D^(ell) <= a_Q                                          (Lemma 5.5)

and it discharges every base box with  t_B(u)^2 = sum_a (|u_a - eta_a| + w/2)^2 <= ell^2,
eta = T_P^* dq.  Different Phi give different dq, hence different (eta, ell), hence a
different covered set.  The H2 prototype scanned only Phi = identity.

EXACT REDUCTION USED HERE (proved in the report; also asserted numerically in
`selftest.py` against align.transform + stageb.dephase):

  write Pmat, Qmat for the stored 6x6 phase arrays (units: cycles, |p| <= 4) and
      Z(u,v) = Pmat[u,v] - Pmat[u,0] - Pmat[0,v] + Pmat[0,0]          (P's raw double diff)
  for a map Phi = (row r, col c, trans t, neg s) with anchor (a,b) = (r[0], c[0]),
  B = Qmat or Qmat^T, and
      M(u,v) = B[u,v] - B[u,b] - B[a,v] + B[a,b],
  one has  dp(Phi Q)(i,j) = s * wrap(M(r_i, c_j))  and therefore

      wrap( dp(Phi Q)(i,j) - dp(P)(i,j) )  =  wrap( s*M(r_i,c_j) - Z(i,j) )   (*)

  independent of the integer-lift conventions.  (*) is what the scan evaluates.
"""
import itertools
import sys
from fractions import Fraction as Q

sys.path.insert(0, "base")

import numpy as np

PERMS6 = list(itertools.permutations(range(6)))          # 720, lexicographic
PIDX = np.array(PERMS6, dtype=np.int64)
BY_ANCHOR = {a: np.array([i for i, p in enumerate(PERMS6) if p[0] == a],
                         dtype=np.int64) for a in range(6)}


def raw_matrix(record):
    """Stored 6x6 phase array (cycles), float, and its dephased form Z."""
    Pm = np.array([float(x) for x in record.p], dtype=np.float64).reshape(6, 6)
    Z = Pm - Pm[:, 0][:, None] - Pm[0, :][None, :] + Pm[0, 0]
    return Pm, Z


def wrapf(X):
    return X - np.rint(X)


def pi_proj_norm_sq(D):
    """||Pi D||^2 for a stack of 36-vectors D of shape (..., 6, 6)."""
    g = D.sum(axis=(-1, -2)) / 36.0
    r = D.sum(axis=-1) / 6.0                    # (...,6)
    c = D.sum(axis=-2) / 6.0                    # (...,6)
    E = D + g[..., None, None] - r[..., :, None] - c[..., None, :]
    return (E ** 2).sum(axis=(-1, -2))


def scan_child(Pmat, ZP, Qmat, cut=0.05, block=40):
    """All (map, ||dq||) with ||dq|| <= cut, plus the global minimum.

    Complete over the 2*2*720*720 = 2,073,600 maps: for each anchor (a,b) the
    120x120 permutation pairs with r[0]=a, c[0]=b are scanned exactly once, and
    every map has exactly one anchor.
    """
    hits = []
    best = (float("inf"), None)
    for trans in (0, 1):
        B = Qmat.T if trans else Qmat
        for a in range(6):
            for b in range(6):
                M = B - B[:, b][:, None] - B[a, :][None, :] + B[a, b]
                W = wrapf(M)
                ir = BY_ANCHOR[a]
                ic = BY_ANCHOR[b]
                AR = PIDX[ir]                                    # 120 x 6
                IC = PIDX[ic]                                    # 120 x 6
                for s in (1, -1):
                    A = (s * W)[AR]                                  # 120 x 6 x 6
                    for lo in range(0, 120, block):
                        Ablk = A[lo:lo + block]                      # B x 6 x 6
                        Blk = Ablk[:, :, IC]                         # B x 6 x 120 x 6
                        Blk = Blk.transpose(0, 2, 1, 3)              # B x 120 x 6 x 6
                        D = Blk - ZP[None, None, :, :]
                        D -= np.rint(D)
                        d2 = pi_proj_norm_sq(D)
                        d = np.sqrt(d2)
                        j = int(np.argmin(d))
                        bi, ci = divmod(j, 120)
                        neg = 0 if s == 1 else 1
                        if d[bi, ci] < best[0]:
                            best = (float(d[bi, ci]),
                                    (tuple(int(x) for x in PIDX[ir[lo + bi]]),
                                     tuple(int(x) for x in PIDX[ic[ci]]), trans, neg))
                        ii, jj = np.nonzero(d <= cut)
                        for p, q in zip(ii, jj):
                            hits.append((float(d[p, q]),
                                         (tuple(int(x) for x in PIDX[ir[lo + p]]),
                                          tuple(int(x) for x in PIDX[ic[q]]), trans,
                                          0 if s == 1 else 1)))
    return best, hits
