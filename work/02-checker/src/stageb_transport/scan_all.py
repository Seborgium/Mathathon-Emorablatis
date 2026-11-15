"""Exhaustive Stage-B transport closure attempt for parent bad10#0.

Pipeline (every verdict recomputed exactly; the float scan only *proposes*):
  1. reproduce the base-grid ledger (11480 outside / 1709 covered / 1452 unresolved)
  2. for each candidate child Q and all 2,073,600 transport maps Phi:
        || Pi(wrap(dp(Phi Q) - dp P)) || <= CUT_PROBE      (float, complete over maps)
  3. for every surviving (Q, Phi) build stageb.Relation exactly, run the certified
     threshold search: largest verified ell with D^(ell) <= a_Q
  4. test each of the 1452 unresolved boxes against the new edges:
        t_B^2 = sum_a (|u_a - eta_a| + w/2)^2 <= ell^2
  5. report, for every unresolved box, the best deficit over identity + transported
     edges; a box with no admissible edge keeps its exact t_B and the deficit.

Usage:  python3 scan_all.py [cluster|all] [nproc]
"""
import json
import os
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

CUT_PROBE = 0.06          # wider than the run's 0.027 admissibility cut, deliberately
CUT_RUN = 0.0270001       # min(.23, R + .011 + 1e-6) from stageb_run.ledger, R=.016

_G = {}


def _init(P, R, boxes):
    _G["P"] = P
    _G["R"] = R
    _G["Pmat"], _G["ZP"] = transcan.raw_matrix(P)
    _G["boxes"] = boxes


def tB2(u, eta, h):
    s = Q(0)
    for a in range(len(u)):
        z = abs(u[a] - eta[a]) + h
        s += z * z
    return s


def work(child_spec):
    """child_spec = (tag, index, record). Returns the certified transported edges."""
    tag, idx, Qi = child_spec
    P, R = _G["P"], _G["R"]
    Qmat, _ = transcan.raw_matrix(Qi)
    best, hits = transcan.scan_child(_G["Pmat"], _G["ZP"], Qmat, cut=CUT_PROBE)
    out = []
    # identity edge is measured exactly as the ledger does (no transform)
    cands = [((tuple(range(6)), tuple(range(6)), 0, 0), None)]
    cands += [(mp, d) for (d, mp) in hits
              if not (mp == (tuple(range(6)), tuple(range(6)), 0, 0))]
    for mp, dprobe in cands:
        Qt = Qi if mp == (tuple(range(6)), tuple(range(6)), 0, 0) else align.transform(Qi, mp)
        rel = stageb.Relation(P, R, Qt)
        sq = float(rel.sq.as_fraction())
        if sq > CUT_PROBE:                      # float proposal contradicted exactly
            out.append(dict(tag=tag, index=idx, map=mp, dq=sq, rejected="dq>probe"))
            continue
        ell, dhat = certified_threshold(rel, Qi.radius)
        rec_out = dict(tag=tag, index=idx, map=[list(mp[0]), list(mp[1]), mp[2], mp[3]],
                       dq=sq, nq=float(rel.nq.as_fraction()),
                       ell=float(ell), radius=float(Qi.radius),
                       dhat=float(dhat.as_fraction()),
                       slack=float(Q(Qi.radius) - dhat.as_fraction()),
                       eta=[float(x) for x in rel.eta],
                       lam=float(rel.lam.as_fraction()),
                       nu0=float(rel.nu0.as_fraction()),
                       sigma=float(rel.sigma.as_fraction()),
                       admissible=bool(sq <= CUT_RUN and ell > 0
                                       and Q(Qi.radius) >= dhat.as_fraction()))
        out.append(rec_out)
    return dict(tag=tag, index=idx, best_float=best, n_hits=len(hits), edges=out)


def main():
    scope = sys.argv[1] if len(sys.argv) > 1 else "cluster"
    nproc = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    t00 = time.time()

    P, R, fb, cluster, dists, cut = m3lib.load_parent_and_children()
    k = P.k
    E, L, n = m3lib.grid(P, R, W)
    h = Q(W) / 2

    # ---- 1. base ledger
    edges = m3lib.edges_for(P, R, cluster)
    rep = m3lib.box_report(E, L, W, edges, k)
    print(f"[1] ledger: outside={rep['outside']} covered={rep['covered']} "
          f"unresolved={len(rep['unresolved'])} "
          f"(published 11480/1709/1452)")
    un = rep["unresolved"]
    ub = [[Q(x) for x in bx["u"]] for bx in un]

    # ---- 2/3. transported edges
    if scope == "cluster":
        specs = [("cluster", Qi.index, Qi) for Qi in cluster]
    else:
        specs = [("fb1", Qi.index, Qi) for Qi in fb]
    print(f"[2] scanning {len(specs)} children x 2,073,600 maps "
          f"({nproc} processes, probe cut {CUT_PROBE})", flush=True)

    import multiprocessing as mp
    t0 = time.time()
    results = []
    with mp.Pool(nproc, initializer=_init, initargs=(P, R, ub)) as pool:
        for i, r in enumerate(pool.imap_unordered(work, specs, chunksize=1)):
            results.append(r)
            if (i + 1) % 25 == 0 or i + 1 == len(specs):
                el = time.time() - t0
                print(f"    {i+1}/{len(specs)} children  {el:.0f}s "
                      f"({el/(i+1):.2f}s/child)", flush=True)
    t_scan = time.time() - t0

    all_edges = [e for r in results for e in r["edges"] if "map" in e]
    adm = [e for e in all_edges if e["admissible"]]
    ident = [e for e in adm if e["map"] == [list(range(6)), list(range(6)), 0, 0]]
    trans_e = [e for e in adm if e not in ident]
    print(f"[3] edges probed {len(all_edges)}; admissible {len(adm)} "
          f"(identity {len(ident)}, transported {len(trans_e)}); "
          f"rejected-by-exactness {sum(1 for e in all_edges if 'rejected' in e)}")
    if trans_e:
        print("    best transported edges by dq:")
        for e in sorted(trans_e, key=lambda z: z["dq"])[:10]:
            print(f"      {e['tag']}#{e['index']:<4d} dq={e['dq']:.6f} "
                  f"ell={e['ell']:.6f} slack={e['slack']:.2e} map={e['map']}")

    # ---- 4. box coverage with the enlarged edge set
    ext = [dict(child=e["index"], eta=[Q(x) for x in e["eta"]],
                ell=Q(e["ell"]), radius=Q(e["radius"])) for e in adm]
    print(f"[4] testing {len(un)} unresolved boxes against {len(ext)} admissible edges",
          flush=True)
    t0 = time.time()
    closed, still = [], []
    for bi, u in enumerate(ub):
        best = None
        for j, e in enumerate(ext):
            s = tB2(u, e["eta"], h)
            defc = s - e["ell"] * e["ell"]
            if best is None or defc < best[0]:
                best = (defc, j, s)
            if defc <= 0:
                break
        if best[0] <= 0:
            closed.append(dict(box=list(un[bi]["idx"]), tB=float(usqrt(best[2]).as_fraction()),
                               edge=ext[best[1]]["child"], map=adm[best[1]]["map"],
                               ell=float(ext[best[1]]["ell"]),
                               radius=float(ext[best[1]]["radius"]),
                               dq=adm[best[1]]["dq"],
                               deficit_sqrt=float(usqrt(best[2]).as_fraction()
                                                  - ext[best[1]]["ell"])))
        else:
            still.append(dict(box=list(un[bi]["idx"]),
                              tB=float(usqrt(best[2]).as_fraction()),
                              deficit_sqrt=float(usqrt(best[2]).as_fraction()
                                                 - ext[best[1]]["ell"]),
                              edge=ext[best[1]]["child"]))
    print(f"    closed {len(closed)} / {len(un)}; still unresolved {len(still)} "
          f"({time.time()-t0:.0f}s)")
    if closed:
        for c in sorted(closed, key=lambda z: -z["deficit_sqrt"])[:15]:
            print(f"      CLOSED box {c['box']} t_B={c['tB']:.6f} <= ell={c['ell']:.6f} "
                  f"(child {c['edge']}, dq={c['dq']:.5f})")
    if still:
        ds = sorted(x["deficit_sqrt"] for x in still)
        print(f"    remaining sqrt-deficit min {ds[0]:.2e} median {ds[len(ds)//2]:.2e}")

    json.dump(dict(scope=scope, parent="bad10#0", cut_probe=CUT_PROBE, cut_run=CUT_RUN,
                   children_scanned=len(specs), t_scan_s=t_scan,
                   ud=dict(je=dict(**{
                       "out_dir": "out"})),
                   base=dict(outside=rep["outside"], covered=rep["covered"],
                             unresolved=len(un)),
                   admissible=adm, edges_probed=all_edges,
                   closed=closed, still=still),
              open(f"out/scan_{scope}.json", "w"), indent=1)
    print(f"wrote out/scan_{scope}.json   wall {time.time()-t00:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
