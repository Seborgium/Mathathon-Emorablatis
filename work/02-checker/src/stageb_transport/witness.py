"""Emit the Stage-B transported-edge witness file for bad10#0 and verify it cold.

Parent bad10#0, children = ALL fb1 records within the run's admissibility cut
(158, not the prototype's contiguous prefix of 66), maps = all 2,073,600.

The written file is exactly the certificate-shaped object the H2 report asks for
(section 4.5, extended with the transport map on each edge).  It is then re-read
from disk and every edge and every box is re-decided with fresh exact Relations,
so the file is checked the way an external checker would check it.

Usage: python3 witness.py [nproc]
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
from num import Dy
from stageb import up, usqrt
from stageb_run import certified_threshold
import scan_all

IDENT = [list(range(6)), list(range(6)), 0, 0]


def tB2(u, eta, h):
    s = Q(0)
    for a in range(len(u)):
        z = abs(u[a]) - 0
        x = abs(u[a] - eta[a]) + h
        s += x * x
    return s


def frac(x):
    f = Q(x)
    return [f.numerator, f.denominator]


def orbit_dist(Pmat, ZP, Qmat):
    """identity-map distance ||Pi(wrap(dp_Q - dp_P))|| (dp = double difference)."""
    a, b = 0, 0
    M = Qmat - Qmat[:, b][:, None] - Qmat[a, :][None, :] + Qmat[a, b]
    D = transcan.wrapf(transcan.wrapf(M) - ZP)
    return float(np.sqrt(transcan.pi_proj_norm_sq(D)))


def main():
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    t00 = time.time()
    P, R, fb, cluster, dists, cut = m3lib.load_parent_and_children()
    k = P.k
    E, L, n = m3lib.grid(P, R, W)
    h = Q(W) / 2
    Pmat, ZP = transcan.raw_matrix(P)
    kids = [Qi for Qi in fb if orbit_dist(Pmat, ZP, transcan.raw_matrix(Qi)[0]) <= 0.0270001]
    print(f"parent bad10#0 k={k} R={float(R)} w={W}; children within cut: {len(kids)} "
          f"(contiguous prefix {len(cluster)})")
    edges_id = m3lib.edges_for(P, R, kids, verbose=False)
    rep = m3lib.box_report(E, L, W, edges_id, k)
    un = rep["unresolved"]
    print(f"identity-only ledger: outside {rep['outside']} covered {rep['covered']} "
          f"unresolved {len(un)}  (prototype with 66 children: 11480/1709/1452)")
    ub = [[Q(int(x)) * Q(W) for x in bx["idx"]] for bx in un]

    specs = [("fb1", Qi.index, Qi) for Qi in kids]
    import multiprocessing as mp
    t0 = time.time()
    results = []
    with mp.Pool(nproc, initializer=scan_all._init, initargs=(P, R, ub)) as pool:
        for r in pool.imap_unordered(scan_all.work, specs, chunksize=1):
            results.append(r)
    adm = [e for r in results for e in r["edges"]
           if "map" in e and e["admissible"]]
    adm.sort(key=lambda e: (e["index"], e["map"]))
    print(f"scan {len(kids)} children x 2,073,600 maps in {time.time()-t0:.0f}s; "
          f"admissible edges {len(adm)}")
    # rebuild every admissible edge EXACTLY and keep the rationals in the witness
    t0 = time.time()
    for e in adm:
        mp = (tuple(e["map"][0]), tuple(e["map"][1]), e["map"][2], e["map"][3])
        Qi = fb[e["index"]]
        Qt = Qi if e["map"] == IDENT else align.transform(Qi, mp)
        rel = stageb.Relation(P, R, Qt)
        ell_f, dhat_f = certified_threshold(rel, Qi.radius)
        assert ell_f > 0 and dhat_f.as_fraction() <= Q(Qi.radius)
        e["ellQ"] = ell_f
        e["dhatQ"] = dhat_f
        e["etaQ"] = [Q(x) for x in rel.eta]
        e["dqQ"] = rel.sq.as_fraction()
        e["radiusQ"] = Q(Qi.radius)
        assert abs(float(e["ellQ"]) - e["ell"]) < 1e-15
        assert max(abs(float(x) - y) for x, y in zip(e["etaQ"], e["eta"])) < 1e-15
    print(f"exact rebuild of {len(adm)} edges in {time.time()-t0:.0f}s")

    # box -> covering edge
    closes = []
    for bi, u in enumerate(ub):
        hit = None
        for j, e in enumerate(adm):
            if tB2(u, e["etaQ"], h) <= e["ellQ"] ** 2:
                hit = j
                break
        closes.append(hit)
    left = [i for i, j in enumerate(closes) if j is None]
    print(f"boxes closed {len(closes)-len(left)} / {len(ub)}; still open {len(left)}")

    wf = dict(
        schema="stage-b-transported-edge-v1",
        parent=dict(file="bad10.bin", index=0, k=k, R=frac(R), w=W, tau=0.011,
                    C=P.C, n0=P.n0, id=P.id, ort=P.ort, hor=P.hor,
                    mnorm=P.mnorm, froot=P.froot),
        grid=dict(L=L, n=n, boxes=n ** k,
                  rule="u=b*w, h=w/2, outside iff sum_a max(|u_a|-h,0)^2 > (sqrt(1+ort)*R+1e-7)^2"),
        edges=[dict(child_file="fb1.bin", child_index=e["index"],
                    map=e["map"],
                    ell=frac(e["ellQ"]), radius=frac(e["radiusQ"]),
                    dq=frac(e["dqQ"]),
                    eta=[frac(x) for x in e["etaQ"]], dhat=frac(e["dhatQ"].as_fraction()))
               for e in adm],
        boxes=[dict(idx=list(un[i]["idx"]), edge=closes[i])
               for i in range(len(un)) if closes[i] is not None],
        open_boxes=[list(un[i]["idx"]) for i in left],
    )
    json.dump(wf, open("out/witness_bad10_0.json", "w"), indent=1)
    print(f"wrote out/witness_bad10_0.json "
          f"({len(wf['edges'])} edges, {len(wf['boxes'])} box closures)")

    # ---------------- cold verification from the file
    t0 = time.time()
    Wf = json.load(open("out/witness_bad10_0.json"))
    pad = Wf["parent"]
    assert (pad["file"], pad["index"]) == ("bad10.bin", 0)
    parents, _ = m3lib.load_fallback(DATA)
    P2 = parents[0]
    R2 = Q(pad["R"][0], pad["R"][1])
    assert R2 == Q(P2.radius)
    hf = Q(1, 2) * Q(pad["w"])
    fresh = []
    for e in Wf["edges"]:
        Qi = fb[e["child_index"]]
        mp = (tuple(e["map"][0]), tuple(e["map"][1]), e["map"][2], e["map"][3])
        Qt = Qi if e["map"] == IDENT else align.transform(Qi, mp)
        rel = stageb.Relation(P2, R2, Qt)
        ell_f, dhat_f = certified_threshold(rel, Qi.radius)
        assert rel.sq.as_fraction() == Q(*e["dq"]), "dq mismatch"
        assert ell_f == Q(*e["ell"]), "ell mismatch"
        assert Q(Qi.radius) == Q(*e["radius"])
        assert [Q(x) for x in rel.eta] == [Q(*x) for x in e["eta"]], "eta mismatch"
        assert dhat_f.as_fraction() <= Q(Qi.radius), "D(ell) > a"
        fresh.append(dict(eta=[Q(x) for x in rel.eta], ell=ell_f,
                          radius=Q(Qi.radius)))
    print(f"cold verify: {len(fresh)} edges rebuilt exactly from fb1.bin, "
          f"dq/ell/eta identical, D(ell)<=a for all")
    nbad = 0
    margins = []
    for b in Wf["boxes"]:
        u = [Q(int(x)) * Q(pad["w"]) for x in b["idx"]]
        e = fresh[b["edge"]]
        m = e["ell"] ** 2 - tB2(u, e["eta"], hf)
        if m < 0:
            nbad += 1
        margins.append(m)
    print(f"cold verify: {len(Wf['boxes'])} box closures, exact t_B^2 <= ell^2, "
          f"failures {nbad}; open boxes {len(Wf['open_boxes'])}")
    print(f"   margin ell^2-t_B^2: min {float(min(margins)):.3e} "
          f"median {float(sorted(margins)[len(margins)//2]):.3e} "
          f"max {float(max(margins)):.3e}")
    print(f"   accounting of the 1452->1408 target set: outside {rep['outside']} + "
          f"identity-covered {rep['covered']} + transported-covered {len(Wf['boxes'])} "
          f"+ open {len(Wf['open_boxes'])} = "
          f"{rep['outside']+rep['covered']+len(Wf['boxes'])+len(Wf['open_boxes'])} "
          f"(grid {n**k})")
    print("   note: Wf['boxes'] lists only the boxes the identity map missed; "
          "complete_witness.py extends it to all 3161 covered boxes")
    assert nbad == 0
    assert rep['outside'] + rep['covered'] + len(Wf['boxes']) + len(Wf['open_boxes']) == n ** k
    print(f"WITNESS VERIFIED  wall {time.time()-t00:.0f}s")


if __name__ == "__main__":
    main()
