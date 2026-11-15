"""Widened fallback ledger: every fb1 record within the run's cut is a child, with
transported-frame edges, for several parents.

Differences from stageb_run.cluster (a real defect, see report):
  * `cluster` walks the fb1 list and BREAKS at the first child outside the cut, so
    for bad10#0 it keeps 66 of the 158 records that are actually within the cut;
  * it tests only the identity map, so a child whose non-identity image is aligned
    is discarded even though the run's own `variants` mechanism would find it.

Usage: python3 ledger_all.py [nproc]
"""
import json
import sys
import time
from fractions import Fraction as Q

sys.path.insert(0, "base")

import numpy as np

import align
import m3lib
import stageb
import transcan
from m3lib import W, DATA
from stageb import up, usqrt
from stageb_run import certified_threshold

CUT_RUN = Q(0.0270001)
CUT_PROBE = 0.06
IDENT = (tuple(range(6)), tuple(range(6)), 0, 0)

_G = {}


def tB2(u, eta, h):
    s = Q(0)
    for a in range(len(u)):
        z = abs(u[a] - eta[a]) + h
        s += z * z
    return s


def orbit_dist(Pmat, ZP, Xmat, mp=IDENT):
    row, col, trans, neg = mp
    s = -1 if neg else 1
    B = Xmat.T if trans else Xmat
    a, b = row[0], col[0]
    M = B - B[:, b][:, None] - B[a, :][None, :] + B[a, b]
    Wm = s * transcan.wrapf(M)
    D = transcan.wrapf(Wm[np.ix_(list(row), list(col))] - ZP)
    return float(np.sqrt(transcan.pi_proj_norm_sq(D)))


def _init(fb):
    _G["fb"] = fb


def run_parent(pi):
    """Full ledger for parent index pi with all within-cut fb children."""
    fb = _G["fb"]
    parents, _ = m3lib.load_fallback(DATA)
    P = parents[pi]
    R = Q(P.radius)
    k = P.k
    Pmat, ZP = transcan.raw_matrix(P)
    try:
        kids = [Qi for Qi in fb if orbit_dist(Pmat, ZP, transcan.raw_matrix(Qi)[0]) <= 0.0270001]
        # contiguous prefix kept by the prototype, for comparison
        pre, run = [], []
        for Qi in fb:
            d = orbit_dist(Pmat, ZP, transcan.raw_matrix(Qi)[0])
            run.append(d)
            if d <= 0.0270001:
                pre.append(Qi)
            elif pre:
                break
        E, L, n = m3lib.grid(P, R, W)
        h = Q(W) / 2
        edges_id = m3lib.edges_for(P, R, kids, verbose=False)
        rep = m3lib.box_report(E, L, W, edges_id, k)
        un = rep["unresolved"]
        out = dict(parent=pi, k=k, R=float(R), boxes=n ** k, children=len(kids),
                   prefix_children=len(pre), outside=rep["outside"],
                   covered_identity=rep["covered"], unresolved_identity=len(un),
                   edges_identity=len(edges_id))
        if not un:
            out["closed"] = 0
            return out
        # transported scan
        adm = []
        t0 = time.time()
        for Qi in kids:
            Qmat, _ = transcan.raw_matrix(Qi)
            best, hits = transcan.scan_child(Pmat, ZP, Qmat, cut=CUT_PROBE)
            cands = [(IDENT, None)] + [(mp, d) for (d, mp) in hits if mp != IDENT]
            for mp, _d in cands:
                Qt = Qi if mp == IDENT else align.transform(Qi, mp)
                rel = stageb.Relation(P, R, Qt)
                sq = rel.sq.as_fraction()
                if sq > CUT_RUN:
                    continue
                ell, dhat = certified_threshold(rel, Qi.radius)
                if not (ell > 0 and Q(Qi.radius) >= dhat.as_fraction()):
                    continue
                adm.append(dict(child=Qi.index, map=mp, dq=float(sq), ell=ell,
                                radius=Q(Qi.radius), eta=[Q(x) for x in rel.eta]))
        closed, still, marg = [], [], []
        for bx in un:
            u = [Q(int(x)) * Q(W) for x in bx["idx"]]
            bestd = None
            for e in adm:
                s = tB2(u, e["eta"], h)
                dfc = s - e["ell"] * e["ell"]
                if bestd is None or dfc < bestd[0]:
                    bestd = (dfc, e)
                if dfc <= 0:
                    break
            if bestd[0] <= 0:
                closed.append(bx["idx"])
                marg.append(float(usqrt(-bestd[0]).as_fraction()))   # sqrt(ell^2-t_B^2)
            else:
                still.append(dict(idx=list(bx["idx"]),
                                  deficit=float(usqrt(bestd[0]).as_fraction())))    # sqrt(t_B^2-ell^2)
        out.update(edges_transported=len(adm), closed=len(closed),
                   still=len(still), t_scan=time.time() - t0,
                   tightest_margin=min(marg) if marg else None,
                   worst_still=sorted((x["deficit"] for x in still), reverse=True)[:5])
        return out
    except Exception as exc:                     # never lose the whole run
        import traceback
        traceback.print_exc()
        return dict(parent=pi, error=repr(exc))


def main():
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    P, R, fb, cluster, dists, cut = m3lib.load_parent_and_children()
    todo = [int(x) for x in (sys.argv[2].split(",") if len(sys.argv) > 2
                             else "0,1,2,3".split(","))]
    print(f"parents {todo}, {len(fb)} fb records available as children, {nproc} procs",
          flush=True)
    import multiprocessing as mp
    res = []
    t0 = time.time()
    with mp.Pool(nproc, initializer=_init, initargs=(fb,)) as pool:
        for r in pool.imap_unordered(run_parent, todo):
            res.append(r)
            print(json.dumps({kk: vv for kk, vv in r.items() if kk != "worst_still"}),
                  flush=True)
            if r.get("worst_still"):
                print("   worst still-unresolved deficits:", r["worst_still"], flush=True)
    res.sort(key=lambda z: z["parent"])
    json.dump(res, open("out/ledger_all.json", "w"), indent=1)
    print(f"wrote out/ledger_all.json  wall {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
