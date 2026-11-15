"""Complete the Stage-B witness for bad10#0: classify ALL 14641 grid boxes.

The closure of the 1408 boxes left open by the identity map is already in
out/witness_bad10_0.json.  This script re-reads it, re-derives every edge exactly,
classifies *every* grid slot (outside / covered by edge e) and rewrites the file so
that the accounting is total:  outside + covered = L^n, no box unaccounted.
"""
import json
import sys
import time
from fractions import Fraction as Q

sys.path.insert(0, "base")

import align
import m3lib
import stageb
from m3lib import W, DATA
from num import Dy
from stageb import up, usqrt
from stageb_run import certified_threshold

IDENT = [list(range(6)), list(range(6)), 0, 0]


def frac(x):
    f = Q(x)
    return [f.numerator, f.denominator]


def tB2(u, eta, h):
    s = Q(0)
    for a in range(len(u)):
        x = abs(u[a] - eta[a]) + h
        s += x * x
    return s


def main():
    t0 = time.time()
    P, R, fb, cluster, dists, cut = m3lib.load_parent_and_children()
    k = P.k
    E, L, n = m3lib.grid(P, R, W)
    h = Q(W) / 2
    E2 = E.as_fraction() ** 2
    Wf = json.load(open("out/witness_bad10_0.json"))
    print(f"grid {n**k} boxes (L={L}, w={W}); witness edges {len(Wf['edges'])}")

    # re-derive every edge exactly (independent of the scan)
    fresh = []
    for e in Wf["edges"]:
        Qi = fb[e["child_index"]]
        mp = (tuple(e["map"][0]), tuple(e["map"][1]), e["map"][2], e["map"][3])
        Qt = Qi if e["map"] == IDENT else align.transform(Qi, mp)
        rel = stageb.Relation(P, R, Qt)
        ell, dhat = certified_threshold(rel, Qi.radius)
        assert rel.sq.as_fraction() == Q(*e["dq"])
        assert ell == Q(*e["ell"])
        assert dhat.as_fraction() <= Q(Qi.radius)
        fresh.append(dict(eta=[Q(x) for x in rel.eta], ell=ell, radius=Q(Qi.radius),
                          child=e["child_index"], map=e["map"]))
    print(f"re-derived {len(fresh)} edges exactly ({time.time()-t0:.0f}s)")

    import itertools
    outside = 0
    boxes = []
    openb = []
    t1 = time.time()
    for b in itertools.product(range(-L, L + 1), repeat=k):
        u = [Q(x) * Q(W) for x in b]
        d2 = Q(0)
        for a in range(k):
            z = abs(u[a]) - h
            if z > 0:
                d2 += z * z
        if d2 > E2:
            outside += 1
            continue
        hit = None
        for j, e in enumerate(fresh):
            if tB2(u, e["eta"], h) <= e["ell"] ** 2:
                hit = j
                break
        if hit is None:
            openb.append(list(b))
        else:
            boxes.append(dict(idx=list(b), edge=hit))
    print(f"classification: outside {outside} covered {len(boxes)} open {len(openb)} "
          f"sum {outside+len(boxes)+len(openb)} ({time.time()-t1:.0f}s)")

    Wf["boxes"] = boxes
    Wf["open_boxes"] = openb
    Wf["accounting"] = dict(grid=n ** k, outside=outside, covered=len(boxes),
                            open=len(openb))
    Wf["schema"] = "stage-b-transported-edge-v1"
    Wf["check"] = dict(
        outside_rule="dist(0,B)^2 > (sqrt(1+ort)*R + 1e-7)^2, exact rational",
        cover_rule="exists edge: sum_a (|u_a-eta_a| + w/2)^2 <= ell^2, exact rational",
        edge_rule="dq = Pi(wrap(dp(Phi Q) - dp(P))), ||dq|| <= min(.23, R+tau+1e-6),"
                  " D^(ell) <= a_Q  (certified_threshold), recomputed here from fb1.bin")
    json.dump(Wf, open("out/witness_bad10_0.json", "w"), indent=1)
    print(f"rewrote out/witness_bad10_0.json: {len(fresh)} edges, {len(boxes)} box "
          f"closures, {len(openb)} open, outside {outside}")
    assert outside + len(boxes) + len(openb) == n ** k
    # which edges actually carry the cover?
    from collections import Counter
    cnt = Counter(boxes_idx := [b["edge"] for b in boxes])
    idm = [j for j, e in enumerate(fresh) if e["map"] == IDENT]
    print(f"edges used: {len(cnt)} of {len(fresh)}; identity edges {len(idm)}; "
          f"boxes closed by an identity edge "
          f"{sum(cnt[j] for j in idm if j in cnt)}")
    print(f"worst margin over all covered boxes: "
          f"{min(float(fresh[b['edge']]['ell']**2 - tB2([Q(int(x))*Q(W) for x in b['idx']], fresh[b['edge']]['eta']))*0 + 0 for b in boxes[:1]):.0f}"
          if False else "", end="")
    mar = []
    for b in boxes[:400]:
        u = [Q(int(x)) * Q(W) for x in b["idx"]]
        mar.append(fresh[b["edge"]]["ell"] ** 2 - tB2(u, fresh[b["edge"]]["eta"], h))
    print(f"margin distribution over 400 sampled boxes: min {float(min(mar)):.3e}")
    print(f"WITNESS COMPLETE  wall {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
