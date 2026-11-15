"""Is the transported-frame closure a generic mechanism, or specific to bad10#0?

A. Characterise the 5 maps that do all the work: are they approximate symmetries
   of the parent itself?  Measure  ||Pi(wrap(dp(Phi P) - dp(P)))||  and the
   distance ||Phi p_P - p_P|| for each.
B. Are the 5 transported children distinct records, or the same point repeated?
C. How many of the 1127 fallback records are within the run's admissibility cut
   of bad10#0 if one does NOT stop at the first gap (the prototype's `cluster`
   breaks at the first failure)?
D. Repeat the whole closure pipeline for other fallback parents.
"""
import itertools
import json
import sys
import time
from fractions import Fraction as Q

sys.path.insert(0, "base")

import numpy as np

import align
import m3lib
import rec
import stageb
import transcan
from m3lib import W, DATA
from num import Dy
from stageb import up, usqrt
from stageb_run import certified_threshold

CUT_RUN = Q(0.0270001)


def nmap(m):
    row, col, trans, neg = m
    return (tuple(int(x) for x in row), tuple(int(x) for x in col), int(trans), int(neg))


def tB2(u, eta, h):
    s = Q(0)
    for a in range(len(u)):
        z = abs(u[a] - eta[a]) + h
        s += z * z
    return s


def dist_orbit(Pmat, ZP, Xmat, mp):
    """||Pi(wrap(dp(Phi X) - dp(P)))|| for one map, float (validated in selftest T2)."""
    row, col, trans, neg = mp
    s = -1 if neg else 1
    B = Xmat.T if trans else Xmat
    a, b = row[0], col[0]
    M = B - B[:, b][:, None] - B[a, :][None, :] + B[a, b]
    Wm = s * transcan.wrapf(M)
    D = transcan.wrapf(Wm[np.ix_(list(row), list(col))] - ZP)
    return float(np.sqrt(transcan.pi_proj_norm_sq(D)))


def ledger_boxes(P, R, children, verbose=False):
    k = P.k
    E, L, n = m3lib.grid(P, R, W)
    h = Q(W) / 2
    edges = m3lib.edges_for(P, R, children, verbose=False)
    rep = m3lib.box_report(E, L, W, edges, k)
    if verbose:
        print(f"     grid {n**k} boxes: outside {rep['outside']} covered "
              f"{rep['covered']} unresolved {len(rep['unresolved'])}")
    return E, L, h, edges, rep


def closure(parent_rec, children, E, L, h, unresolved, cut_probe=0.06):
    """Scan all maps of `children`, and test the unresolved boxes; returns counts."""
    P = parent_rec
    R = Q(P.radius)
    Pmat, ZP = transcan.raw_matrix(P)
    adm = []
    t0 = time.time()
    for Qi in children:
        Qmat, _ = transcan.raw_matrix(Qi)
        best, hits = transcan.scan_child(Pmat, ZP, Qmat, cut=cut_probe)
        mp0 = (tuple(range(6)), tuple(range(6)), 0, 0)
        cands = [(mp0, None)] + [(mp, d) for (d, mp) in hits if mp != mp0]
        for mp, dprobe in cands:
            Qt = Qi if mp == mp0 else align.transform(Qi, mp)
            rel = stageb.Relation(P, R, Qt)
            sq = rel.sq.as_fraction()
            if sq > CUT_RUN:
                continue
            ell, dhat = certified_threshold(rel, Qi.radius)
            if not (ell > 0 and Q(Qi.radius) >= dhat.as_fraction()):
                continue
            adm.append(dict(child=Qi.index, map=mp, dq=float(sq), ell=ell, radius=Q(Qi.radius),
                            eta=[Q(x) for x in rel.eta]))
    closed = 0
    for bx in unresolved:
        u = [Q(int(x)) * Q(W) for x in bx["idx"]]
        if any(tB2(u, e["eta"], h) <= e["ell"] ** 2 for e in adm):
            closed += 1
    return dict(children=len(children), edges=len(adm), closed=closed,
                unresolved=len(unresolved), t=time.time() - t0)


def main():
    P, R, fb, cluster, dists, cut = m3lib.load_parent_and_children()
    Pmat, ZP = transcan.raw_matrix(P)
    J = json.load(open("out/scan_cluster.json"))
    closed = J["closed"]
    maps = sorted({nmap(c["map"]) for c in closed})
    print("A. the 5 transport maps that close boxes, measured on the PARENT itself:")
    print("   map                                              ||dq(P,Phi P)||   max|Phi p - p|")
    for mp in maps:
        dq = dist_orbit(Pmat, ZP, Pmat, mp)
        Qt = align.transform(P, mp)
        dev = max(abs(Q(Qt.p[h]) - Q(P.p[h])) for h in range(36))
        print(f"   {str(mp):48s}  {dq:.6f}          {float(dev):.6f}")
    Qt = align.transform(P, (tuple(range(6)), tuple(range(6)), 0, 0))
    print(f"   (identity for scale: max|dp(P)| = "
          f"{float(max(abs(Q(x)) for x in stageb.dephase(P.p))):.4f})")

    print("B. are the 5 transported images of one child distinct records?")
    Q0 = fb[closed[0]["edge"]]
    seen = {}
    for mp in maps:
        Qt = align.transform(Q0, mp)
        key = tuple(round(float(x), 12) for x in Qt.p)
        seen.setdefault(key, []).append(mp)
        dev = max(abs(Q(Qt.p[h]) - Q(Q0.p[h])) for h in range(36))
        print(f"   {str(mp):48s} max|Phi p_Q - p_Q| = {float(dev):.6f}")
    print(f"   distinct transported centres among the 5 maps: {len(seen)}")

    print("C. fb1 records within the cut of bad10#0 if the prefix gap is not fatal:")
    n_in = 0
    for Qi in fb:
        if dist_orbit(Pmat, ZP, transcan.raw_matrix(Qi)[0], (tuple(range(6)),
                                                            tuple(range(6)), 0, 0)) <= 0.0270001:
            n_in += 1
    print(f"   {n_in} of {len(fb)} (the prototype's contiguous-prefix cluster has 66)")

    print("D. other fallback parents, same pipeline:")
    parents, _ = m3lib.load_fallback(DATA)
    rows = []
    for pi in (1, 2, 3, 7, 20, 41):
        if pi >= len(parents):
            continue
        Pi = parents[pi]
        Ri = Q(Pi.radius)
        pmat, zP = transcan.raw_matrix(Pi)
        kids = [Qi for Qi in fb
                if dist_orbit(pmat, zP, transcan.raw_matrix(Qi)[0],
                              (tuple(range(6)), tuple(range(6)), 0, 0)) <= 0.0270001]
        E, L, h, edges, rep = ledger_boxes(Pi, Ri, kids)
        un = rep["unresolved"]
        print(f"   parent bad{10+pi//8}#{pi%8} (k={Pi.k} R={float(Ri):.4f}) "
              f"children {len(kids)}: outside {rep['outside']} covered {rep['covered']} "
              f"unresolved {len(un)}", flush=True)
        if not un:
            rows.append(dict(parent=pi, children=len(kids), unresolved=0, closed=0))
            continue
        r = closure(Pi, kids, E, L, h, un)
        print(f"      transported closure: {r['closed']}/{r['unresolved']} boxes, "
              f"{r['edges']} admissible edges, {r['t']:.0f}s", flush=True)
        rows.append(dict(parent=pi, children=len(kids),
                         unresolved=len(un), **{k: v for k, v in r.items() if k != "t"}))
    json.dump(rows, open("out/generality.json", "w"), indent=1)
    print("wrote out/generality.json")


if __name__ == "__main__":
    main()
