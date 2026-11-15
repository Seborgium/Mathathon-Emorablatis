"""Alignment search between two stored centers (Lemma 4.7 transport + (5.5)).

A stored atlas center is a *canonical representative* of an equivalence class
(signed row/column permutations, transpose, global sign, integer phases).  To state
a Stage-B relation from a parent P to a child Q we need the map Phi with
    dq = Pi( wrap( dp(Phi Q) - dp(P) ) )
small.  The map is a discrete witness (4 bits + two permutations of six indices);
the search below only *proposes* it -- every verdict is recomputed exactly from the
record data with that explicit map.
"""
import itertools
import numpy as np

from fractions import Fraction as Q
import num
from stageb import dephase, nearest_int

PERMS6 = list(itertools.permutations(range(6)))
PERM_IDX = np.array(PERMS6, dtype=np.int64)          # 720 x 6


def dp_matrix(record):
    return np.array([float(x) for x in dephase(record.p)]).reshape(6, 6)


def _interior(v6x6):
    return v6x6[1:, 1:]


def fingerprint(record):
    """Sorted row patterns of the dephased interior: invariant under row/column
    permutations and integer lifts, up to sign and transpose."""
    A = _interior(dp_matrix(record))
    rows = sorted(tuple(sorted(A[i])) for i in range(5))
    cols = sorted(tuple(sorted(A[:, j])) for j in range(5))
    fp = np.array(rows + cols, dtype=float)
    return fp, -fp[::-1]


def fp_distance(fa, fb):
    return float(np.max(np.abs(fa - fb)))


def best_map(dpP, dpQ, block=48):
    """Exhaustive search over the 2*2*720*720 = 2,073,600 signed
    permutation/transpose maps for the one minimising ||Pi(wrap(Phi Q - P))||.
    Complete: no admissible transport map is missed.  Returns (distance, map)."""
    best = (float("inf"), None)
    for neg in (0, 1):
        sgn = -1.0 if neg else 1.0
        for trans in (0, 1):
            base = (sgn * dpQ.T) if trans else (sgn * dpQ)
            for lo in range(0, 720, block):
                rows = PERM_IDX[lo:lo + block]
                A = base[rows]                                  # b x 6 x 6
                B = A[:, :, PERM_IDX]                           # b x 6 x 720 x 6
                B = B.transpose(0, 2, 1, 3)                     # b x 720 x 6 x 6
                D = B - dpP[None, None, :, :]
                D = D - np.rint(D)
                g = D.sum(axis=(2, 3)) / 36.0
                r = D.sum(axis=3) / 6.0
                c = D.sum(axis=2) / 6.0
                E = D + g[:, :, None, None] - r[:, :, :, None] - c[:, :, None, :]
                d = np.sqrt((E ** 2).sum(axis=(2, 3)))
                j = int(np.argmin(d))
                bi, ci = divmod(j, 720)
                if d[bi, ci] < best[0]:
                    best = (float(d[bi, ci]),
                            (tuple(int(x) for x in rows[bi]),
                             tuple(int(x) for x in PERM_IDX[ci]), trans, neg))
    return best


def transform(record, mp):
    """Exact (row, col, trans, neg) action on phases and tangent columns (Lemma 4.7)."""
    row, col, trans, neg = mp
    sg = -1 if neg else 1
    p = [Q(x) for x in record.p]
    T = record.TQ()
    k = record.k
    idx = (lambda i, j: 6 * col[j] + row[i]) if trans else (lambda i, j: 6 * row[i] + col[j])
    pout = [0] * 36
    Tout = [[0] * 36 for _ in range(k)]
    for i in range(6):
        for j in range(6):
            h = 6 * i + j
            g = idx(i, j)
            pout[h] = sg * p[g]
            for a in range(k):
                Tout[a][h] = sg * T[a][g]
    import rec as recmod
    return recmod.Record(k, pout, Tout,
                         [record.C, record.n0, record.id, record.ort, record.hor,
                          record.mnorm, record.froot, record.radius],
                         record.index, record.source)


def map_size(mp):
    return 2 + 2 + 4 * len(PERMS6)          # informational
