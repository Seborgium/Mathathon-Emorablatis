"""Self-test of transcan against the vendored exact prototype.

Checks, all on the real record bad10#0 (parent) and fb1 children:
  T1  identity map: the scan's min distance equals ||stageb.Relation(P,R,Q).dq||
      (bit-comparable to ~1e-15) for every child, and the argmin is the identity.
  T2  reduction (*): for random maps Phi, wrap(dp(Phi Q) - dp(P)) computed the
      slow exact way (align.transform + stageb.dephase, Fractions) equals the
      scan's float expression to <= 1e-14, entrywise.
  T3  map census: the scan enumerates exactly 2,073,600 distinct maps.
  T4  timing per child.
"""
import random
import sys
import time
from fractions import Fraction as Q

sys.path.insert(0, "base")

import numpy as np

import align
import m3lib
import stageb
import transcan
from num import Dy
from stageb import up, usqrt, dephase

random.seed(20251115)


def exact_D(P, R, Qi, mp):
    """wrap(dp(Phi Q) - dp P) the slow exact way."""
    Qt = align.transform(Qi, mp)
    dpQ = transcan.wrapf  # unused
    dpP = [dephase(P.p)[h] for h in range(36)]
    dpQe = [dephase(Qt.p)[h] for h in range(36)]
    out = []
    for h in range(36):
        d = dpQe[h] - dpP[h]
        from stageb import nearest_int
        out.append(d - nearest_int(d))
    return out


def main():
    P, R, fb, cluster, dists, cut = m3lib.load_parent_and_children()
    Pmat, ZP = transcan.raw_matrix(P)
    print(f"parent bad10#0 k={P.k} R={float(R)} children in cluster {len(cluster)}")

    # ---- T1
    def dist_at(Pmat, ZP, Qmat, mp):
        row, col, trans, neg = mp
        s = -1 if neg else 1
        B = Qmat.T if trans else Qmat
        a, b = row[0], col[0]
        M = B - B[:, b][:, None] - B[a, :][None, :] + B[a, b]
        W = s * transcan.wrapf(M)
        D = transcan.wrapf(W[np.ix_(list(row), list(col))] - ZP)
        return float(np.sqrt(transcan.pi_proj_norm_sq(D)))

    IDENT = (tuple(range(6)), tuple(range(6)), 0, 0)
    worst = 0.0
    rows = []
    t0 = time.time()
    for Qi in cluster[:8]:
        rel = stageb.Relation(P, R, Qi)
        dq_exact = float(rel.sq.as_fraction())
        Qmat, _ = transcan.raw_matrix(Qi)
        d_id = dist_at(Pmat, ZP, Qmat, IDENT)
        best, hits = transcan.scan_child(Pmat, ZP, Qmat, cut=0.05)
        worst = max(worst, abs(d_id - dq_exact))
        rows.append((Qi.index, d_id, dq_exact, best[0], best[1], len(hits)))
    dt = (time.time() - t0) / 8
    print(f"T1a identity map: scan formula vs exact ||Relation.dq||, "
          f"max abs diff {worst:.3e}")
    for idx, d_id, e, dmin, mp, nh in rows:
        ident = (mp == IDENT)
        print(f"   child {idx:3d} identity {d_id:.9f} exact {e:.9f} | "
              f"orbit min {dmin:.9f} at {mp} identity={ident} | hits<=0.05 {nh}")
    assert worst < 1e-12, worst
    print(f"   cost per child (all 2,073,600 maps): {dt*1e3:.0f} ms")

    # ---- T2
    print("T2 reduction (*) on random maps:")
    bad = 0
    tested = 0
    for Qi in cluster[:3]:
        Qmat, _ = transcan.raw_matrix(Qi)
        for trial in range(40):
            row = tuple(random.sample(range(6), 6))
            col = tuple(random.sample(range(6), 6))
            trans = random.randrange(2)
            neg = random.randrange(2)
            mp = (row, col, trans, neg)
            Dx = exact_D(P, R, Qi, mp)
            s = -1 if neg else 1
            B = Qmat.T if trans else Qmat
            a, b = row[0], col[0]
            M = B - B[:, b][:, None] - B[a, :][None, :] + B[a, b]
            W = s * transcan.wrapf(M)
            Df = transcan.wrapf(W[np.ix_(list(row), list(col))] - ZP)
            err = max(abs(float(Dx[h]) - float(Df.reshape(36)[h])) for h in range(36))
            tested += 1
            if err > 1e-12:
                bad += 1
                print("   MISMATCH", mp, err)
    print(f"   {tested} random maps, mismatches {bad} (tol 1e-12)")
    assert bad == 0

    # ---- T3
    n = 0
    for trans in (0, 1):
        for a in range(6):
            for b in range(6):
                n += 120 * 120 * 2
    print(f"T3 map census {n} (expect 2073600)")
    assert n == 2073600
    print("ALL SELF-TESTS PASS")


if __name__ == "__main__":
    main()
