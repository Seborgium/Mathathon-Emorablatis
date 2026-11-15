"""Step 0: reproduce the bad10#0 base-grid ledger of work/02-checker (H2 interval
prototype) from scratch, and dump the *unresolved box set* with per-box deficits.

Run:  python3 repro.py            (writes out/ledger_bad10_0.json, logs/repro.log)
"""
import itertools
import json
import sys
import time
from fractions import Fraction as Q

sys.path.insert(0, "base")

import numpy as np

import m3lib
from m3lib import load_parent_and_children, edges_for, W, DATA
from num import Dy
from stageb import up, usqrt


def main():
    t0 = time.time()
    P, R, fb, cluster, dists, cut = load_parent_and_children()
    k = P.k
    print(f"parent bad10#{P.index} k={k} R={float(R):.6f} C={P.C:.6g} "
          f"mnorm={P.mnorm:.6g} froot={P.froot:.3g}")
    print(f"fb records {len(fb)}; identity cluster {len(cluster)} (cut {cut:.4f})")
    print("identity distances of the scanned prefix:",
          [round(x, 4) for x in dists])

    E, L, n = m3lib.grid(P, R, W)
    total = n ** k
    print(f"E={float(E.as_fraction()):.8g} w={W} L={L} n={n} boxes={total}")

    t = time.time()
    edges = edges_for(P, R, cluster)
    t_rel = time.time() - t

    t = time.time()
    rep = m3lib.box_report(E, L, W, edges, k)
    t_box = time.time() - t

    print(f"outside={rep['outside']} relation-covered={rep['covered']} "
          f"UNRESOLVED={len(rep['unresolved'])}")
    print(f"t_rel={t_rel:.2f}s t_box={t_box:.2f}s")
    assert rep["outside"] + rep["covered"] + len(rep["unresolved"]) == total
    ok = (rep["outside"] == 11480 and rep["covered"] == 1709
          and len(rep["unresolved"]) == 1452)
    print("MATCHES published 11480/1709/1452:", ok)

    u = rep["unresolved"]
    if u:
        ds = sorted(x["deficit_sqrt"] for x in u)
        tb = sorted(x["tB"] for x in u)
        print(f"unresolved t_B  min {tb[0]:.6f} median {tb[len(tb)//2]:.6f} "
              f"max {tb[-1]:.6f}   (best ell over all edges "
              f"{float(max(e['ell'] for e in edges)):.6f})")
        print(f"unresolved sqrt-deficit  min {ds[0]:.6f} median {ds[len(ds)//2]:.6f} "
              f"max {ds[-1]:.6f}")
        print("closest 5 unresolved boxes (index, t_B, ell, t_B-ell):")
        for x in sorted(u, key=lambda z: z["deficit_sqrt"])[:5]:
            print("  ", x["idx"], f"{x['tB']:.6f}", f"{x['ell']:.6f}",
                  f"{x['deficit_sqrt']:+.6f}")
        print("farthest 3:", [(x["idx"], round(x["tB"], 5)) for x in
                              sorted(u, key=lambda z: -z["deficit_sqrt"])[:3]])

    json.dump(dict(parent="bad10#0", k=k, R=float(R), w=W, L=L, n=n, boxes=total,
                   outside=rep["outside"], covered=rep["covered"],
                   unresolved=len(u), matches_published=ok,
                   edges=[dict(child=e["child"], ell=float(e["ell"]),
                                radius=float(e["radius"]),
                                eta=[float(x) for x in e["eta"]],
                                dq=float(e["rel"].sq.as_fraction())) for e in edges],
                   unresolved_boxes=[dict(idx=list(x["idx"]), tB=x["tB"],
                                          deficit_sqrt=x["deficit_sqrt"],
                                          nearest_child=x["nearest_child"])
                                     for x in u]),
              open("out/ledger_bad10_0.json", "w"), indent=1)
    print(f"wrote out/ledger_bad10_0.json  total {time.time()-t0:.1f}s")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
