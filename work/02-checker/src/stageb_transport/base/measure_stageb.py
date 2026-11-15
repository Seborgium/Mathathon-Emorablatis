"""Produce the Stage-B measurement table for H2-INTERVAL-PROTOTYPE.md."""
import glob
import itertools
import json
import time
from fractions import Fraction as Q

import numpy as np

import align
import num
import rec
import stageb
import stageb_run as S
from num import Dy

DATA = ("/workspace/nucleus/work/projects/p-20d35e783d5d4092acb8bd94b19cf30b/repo/.scratch/"
        "h0/dl/verification/saved-run/execution/data")
W = 0.0038
TAU = 0.011


def main():
    parents, fb = S.load_fallback(DATA)
    out = {}
    out["parents"] = len(parents)
    out["parent_k"] = sorted({p.k for p in parents})
    out["parent_radii"] = sorted({p.radius for p in parents})
    out["fb_records"] = len(fb)
    # grid census: every parent has the same k, R, so the same box count
    P = parents[0]
    R = Q(P.radius)
    oP = Q(P.ort)
    E = S.usqrt((1 + oP) * R * R)
    E = S.up(E.as_fraction() + Q(1, 10 ** 7))
    L = int(np.ceil(float(E.as_fraction()) / W + 0.500001))
    h = Q(W) / 2
    n = 2 * L + 1
    inside = 0
    for b in itertools.product(range(-L, L + 1), repeat=4):
        u = [Q(b[a] * W) for a in range(4)]
        d2 = sum((max(Q(0), abs(u[a]) - h) ** 2) for a in range(4))
        if d2 <= E.as_fraction() ** 2:
            inside += 1
    out["grid"] = dict(L=L, n=n, boxes=n ** 4, inside_per_parent=inside,
                       run_inside=515243, predicted_total=len(parents) * inside)
    print("grid:", out["grid"])
    # cluster + ledger for parent 0
    cut = min(.23, float(R) + TAU + 1e-6)
    t0 = time.time()
    ch = S.cluster(P, fb, cut)
    out["cluster_scan_s"] = time.time() - t0
    out["cluster_size"] = len(ch)
    res = S.ledger(P, R, ch, W)
    out["ledger_parent0"] = {k: res[k] for k in ("total", "outside", "covered", "unresolved",
                                                 "t_rel", "t_box")}
    print("ledger:", out["ledger_parent0"])
    # exhaustive transport search on the first children (completeness of the map set)
    dpP = align.dp_matrix(P)
    checks = []
    t0 = time.time()
    for Qi in ch[:6]:
        d, mp = align.best_map(dpP, align.dp_matrix(Qi))
        checks.append(dict(child=Qi.index, best_distance=d, map=list(map(lambda x: list(x) if isinstance(x, tuple) else x, mp)),
                           identity=(mp == align.IDENT if hasattr(align, 'IDENT') else
                                     mp == ((0, 1, 2, 3, 4, 5), (0, 1, 2, 3, 4, 5), 0, 0))))
    out["exhaustive_map_checks"] = checks
    out["exhaustive_cost_s_per_pair"] = (time.time() - t0) / 6
    print("map search:", out["exhaustive_cost_s_per_pair"], "s/pair;",
          [(c["child"], round(c["best_distance"], 5), c["identity"]) for c in checks])
    # per-relation detail of the first three
    det = []
    for Qi in ch[:3]:
        rel = stageb.Relation(P, R, Qi)
        ell, dh = S.certified_threshold(rel, Qi.radius)
        det.append(dict(child=Qi.index, dq=float(rel.sq.as_fraction()),
                        eta=[float(x) for x in rel.eta], nq=float(rel.nq.as_fraction()),
                        nu0=float(rel.nu0.as_fraction()), lam=float(rel.lam.as_fraction()),
                        e0=float(rel.e.as_fraction()), sigma=float(rel.sigma.as_fraction()),
                        beta=float(rel.beta.as_fraction()), radius=Qi.radius,
                        ell=float(ell), D_at_ell=float(dh.as_fraction()),
                        slack=Qi.radius - float(dh.as_fraction())))
    out["relations"] = det
    for d in det:
        print("rel:", {k: (round(v, 6) if isinstance(v, float) else v) for k, v in d.items()
                       if k != "eta"})
    json.dump(out, open("out/stageb_parent0.json", "w"), indent=1, default=str)
    print("wrote out/stageb_parent0.json")


if __name__ == "__main__":
    main()
