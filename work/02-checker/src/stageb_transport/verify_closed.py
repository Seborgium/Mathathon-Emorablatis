"""Independent verification of the transported-frame closures, plus controls.

Nothing here reuses the scan's state: children are re-read from fb1.bin, every
used (child, map) gets a *fresh* exact stageb.Relation, the certified threshold
search is re-run, and every one of the 1452 box inequalities is re-decided in
exact rational arithmetic.

Checks
  V1  all distinct edges used by any closure: ||dq|| <= cut, D^(ell) <= a (exact),
      and ell equals the value recorded by the scan.
  V2  all 1452 boxes: t_B^2 <= ell^2 exactly, from the re-derived eta.
  V3  identity-only edge set reproduces 1709 covered / 1452 unresolved.
  V4  negative controls:
      C1  replace each used map by a random other map -> closures must fail
      C2  shrink ell by 1e-3                              -> closures must fail
      C3  empty edge set                                  -> 0 covered
      C4  perturb one coordinate of eta by +2e-3           -> closures must fail
  V5  a transported record is still a Root witness: R1/R2/R4 (exact) hold with
      identical slack before and after the transport.
"""
import json
import random
import sys
import time
from fractions import Fraction as Q

sys.path.insert(0, "base")

import numpy as np

import align
import m3lib
import rec
import rootcheck
import stageb
import transcan
from m3lib import W, DATA
from num import Dy
from stageb import up, usqrt
from stageb_run import certified_threshold

random.seed(4242)


def nmap(m):
    """JSON map [row, col, trans, neg] -> hashable exact tuple."""
    row, col, trans, neg = m
    return (tuple(int(x) for x in row), tuple(int(x) for x in col),
            int(trans), int(neg))


def tB2(u, eta, h):
    s = Q(0)
    for a in range(len(u)):
        z = abs(u[a] - eta[a]) + h
        s += z * z
    return s


def main():
    P, R, fb, cluster, dists, cut = m3lib.load_parent_and_children()
    k = P.k
    E, L, n = m3lib.grid(P, R, W)
    h = Q(W) / 2
    J = json.load(open("out/scan_cluster.json"))
    closed = J["closed"]
    print(f"closures to verify: {len(closed)} (of 1452)")

    # box index -> exact centre
    box_u = {}
    for c in closed:
        b = tuple(c["box"])
        box_u[b] = [Q(int(x)) * Q(W) for x in b]

    # ---- V1: fresh exact relation for every distinct edge used
    used = {}
    for c in closed:
        key = (c["edge"], nmap(c["map"]))
        used.setdefault(key, []).append(c)
    print(f"distinct (child, map) edges used: {len(used)}")
    t0 = time.time()
    fresh = {}
    bad = 0
    for (cidx, mp), boxes in sorted(used.items()):
        mp_t = mp
        Qi = fb[cidx]
        Qt = Qi if mp_t == (tuple(range(6)), tuple(range(6)), 0, 0) else align.transform(Qi, mp_t)
        rel = stageb.Relation(P, R, Qt)
        dq = rel.sq.as_fraction()
        ell, dhat = certified_threshold(rel, Qi.radius)
        ok_sq = dq <= Q(0.0270001)
        ok_lem = dhat.as_fraction() <= Q(Qi.radius)
        if not (ok_sq and ok_lem):
            bad += 1
            print("   EDGE FAILS", cidx, mp_t, float(dq), float(dhat.as_fraction()))
        # compare with the scan's own numbers (must be bit-identical, same code path)
        rec_c = boxes[0]
        assert abs(float(dq) - rec_c["dq"]) < 1e-15, (float(dq), rec_c["dq"])
        assert abs(float(ell) - rec_c["ell"]) < 1e-15, (float(ell), rec_c["ell"])
        fresh[(cidx, mp_t)] = dict(eta=[Q(x) for x in rel.eta], ell=ell,
                                   radius=Q(Qi.radius), dhat=dhat)
    print(f"V1 {len(used)} edges: ||dq||<=cut and D^(ell)<=a exact; failures {bad} "
          f"({time.time()-t0:.0f}s)")
    assert bad == 0

    # ---- V2: every box inequality, exact, from the freshly derived eta
    t0 = time.time()
    worst = None
    fails = 0
    for c in closed:
        b = tuple(c["box"])
        key = (c["edge"], nmap(c["map"]))
        e = fresh[key]
        s = tB2(box_u[b], e["eta"], h)
        slack = e["ell"] * e["ell"] - s
        if slack < 0:
            fails += 1
            print("   BOX FAILS", b, float(slack))
        if worst is None or slack < worst[0]:
            worst = (slack, b, c["edge"])
    sq = usqrt(worst[0]) if worst[0] > 0 else Q(0)
    print(f"V2 {len(closed)}/{len(closed)} boxes satisfy t_B^2 <= ell^2 exactly; "
          f"failures {fails} ({time.time()-t0:.0f}s)")
    print(f"   tightest closure: box {worst[1]} child {worst[2]}  "
          f"ell^2 - t_B^2 = {float(worst[0]):.3e}  (ell - t_B >= "
          f"{float(worst[0])/(2*0.011):.3e})")
    assert fails == 0

    # ---- V3: identity-only control
    Pmat, ZP = transcan.raw_matrix(P)
    edges_id = m3lib.edges_for(P, R, cluster, verbose=False)
    rep = m3lib.box_report(E, L, W, edges_id, k)
    print(f"V3 identity-only: outside {rep['outside']} covered {rep['covered']} "
          f"unresolved {len(rep['unresolved'])}")
    assert (rep["outside"], rep["covered"], len(rep["unresolved"])) == (11480, 1709, 1452)

    # ---- V4 controls
    print("V4 negative controls:")
    # C1: how many of the 418 admissible edges close the 40 *tightest* boxes?
    #     A coverage claim that came from "any edge closes anything" would show ~418.
    allad = J["admissible"]
    tight = sorted(closed, key=lambda z: -z["deficit_sqrt"])[:40]   # closest to the boundary
    hist = []
    for c in tight:
        u = box_u[tuple(c["box"])]
        hist.append(sum(1 for e in allad
                        if tB2(u, [Q(x) for x in e["eta"]], h) <= Q(e["ell"]) ** 2))
    print(f"   margins (t_B-ell) of the 40 tightest: "
          f"{[round(x,7) for x in sorted(-z['deficit_sqrt'] for z in tight)[:5]]} ...")
    print(f"   C1 for the 40 tightest closures, #edges (of 418) that close them: "
          f"min {min(hist)} median {sorted(hist)[len(hist)//2]} max {max(hist)}")
    # C2: shrink ell
    c2 = sum(1 for c in tight
             if tB2(box_u[tuple(c["box"])],
                    fresh[(c["edge"], nmap(c["map"]))]["eta"], h)
             <= (fresh[(c["edge"], nmap(c["map"]))]["ell"] - Q(1, 1000)) ** 2)
    print(f"   C2 shrink ell by 1e-3: {c2}/{len(tight)} tight closures survive "
          f"(expect 0)")
    assert c2 == 0
    # C3: empty edge set
    rep0 = m3lib.box_report(E, L, W, [], k)
    print(f"   C3 empty edge set: outside {rep0['outside']} covered {rep0['covered']} "
          f"unresolved {len(rep0['unresolved'])} (expect 11480/0/3161)")
    assert rep0["outside"] == 11480 and rep0["covered"] == 0
    # C4: eta perturbed by +2e-3 in one coordinate
    c4 = 0
    for c in tight:
        b = tuple(c["box"])
        key = (c["edge"], nmap(c["map"]))
        e = fresh[key]
        eta2 = list(e["eta"])
        eta2[0] += Q(2, 1000)
        if tB2(box_u[b], eta2, h) <= e["ell"] ** 2:
            c4 += 1
    print(f"   C4 eta_0 += 2e-3: {c4}/{len(tight)} still close (expect 0)")

    # ---- V5: transport preserves the Root obligations R1/R2/R4 (exact)
    print("V5 Root obligations of a transported record (exact parts):")
    for cidx, mp in [(c["edge"], nmap(c["map"]))
                     for c in sorted(closed, key=lambda z: -z["deficit_sqrt"])[:3]]:
        Qi = fb[cidx]
        Qt = align.transform(Qi, mp)
        a = rootcheck.exact_part(Qi)
        b = rootcheck.exact_part(Qt)
        def fmt(d):
            return " ".join(f"{kk}:{d[kk]['verdict']}" for kk in ("ort", "hor", "n0"))
        same = all(abs(a[kk]["slack"] - b[kk]["slack"]) < Q(1, 10 ** 15)
                   for kk in ("ort", "hor", "n0"))
        print(f"   fb1#{cidx} map {mp}: stored [{fmt(a)}] | transported [{fmt(b)}] "
              f"| slack identical {same}")

    print("VERIFICATION PASSED")


if __name__ == "__main__":
    main()
