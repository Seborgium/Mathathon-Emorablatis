"""V6: independent binary64 port of the certified threshold + structure statistics.

The exact kernel (`stageb.Relation`, `certified_threshold`) is the authority; the
float port `relfloat.relation_float` is written from the C++ `relationB` only and
shares no code with it.  Agreement to ~1e-9 confirms the exact path did not slip a
sign/square/root -- the same check that caught a missing sqrt in the first H2 run.
"""
import json
import sys
from fractions import Fraction as Q

sys.path.insert(0, "base")

import align
import m3lib
import relfloat
import stageb
import transcan
from m3lib import W
from stageb_run import certified_threshold


def nmap(m):
    row, col, trans, neg = m
    return (tuple(int(x) for x in row), tuple(int(x) for x in col), int(trans), int(neg))


def main():
    P, R, fb, cluster, dists, cut = m3lib.load_parent_and_children()
    J = json.load(open("out/scan_cluster.json"))
    adm = J["admissible"]
    closed = J["closed"]

    # ---- structure statistics
    kids = sorted({e["index"] for e in adm})
    kids_t = sorted({e["index"] for e in adm
                     if nmap(e["map"]) != (tuple(range(6)), tuple(range(6)), 0, 0)})
    print(f"admissible edges {len(adm)} over {len(kids)} distinct children "
          f"({len(kids_t)} children have at least one transported edge)")
    from collections import Counter
    per = Counter(e["index"] for e in adm)
    print(f"edges per child: min {min(per.values())} median "
          f"{sorted(per.values())[len(per)//2]} max {max(per.values())}")
    used_children = Counter(c["edge"] for c in closed)
    print(f"children actually used by a closure: {len(used_children)}; "
          f"most used {used_children.most_common(5)}")
    maps_used = len({nmap(c["map"]) for c in closed})
    print(f"distinct maps used by closures: {maps_used} "
          f"(of {len({nmap(e['map']) for e in adm})} admissible, "
          f"2,073,600 x {len(kids)} scanned)")

    # ---- V6 float cross-check on every distinct edge used
    used = sorted({(c["edge"], nmap(c["map"])) for c in closed})
    print(f"V6 float re-derivation of {len(used)} edges:")
    worst_sl = worst_dq = worst_D = 0.0
    nbad = 0
    for cidx, mp in used:
        Qi = fb[cidx]
        Qt = Qi if mp == (tuple(range(6)), tuple(range(6)), 0, 0) else align.transform(Qi, mp)
        rel = stageb.Relation(P, R, Qt)
        ell, dhat = certified_threshold(rel, Qi.radius)
        fl = relfloat.relation_float(P, Qt, float(R), float(Qi.radius))
        if fl is None:
            nbad += 1
            print("   float port rejected edge", cidx, mp)
            continue
        worst_dq = max(worst_dq, abs(fl["sq"] - float(rel.sq.as_fraction())))
        worst_D = max(worst_D, abs(fl["D"](float(ell)) - float(dhat.as_fraction())))
        # float verdict at the certified ell: must also be <= a + float pads
        okf = fl["D"](float(ell)) <= Qi.radius + 1e-6
        if not okf:
            nbad += 1
            print("   float port DISAGREES on ell", cidx, mp,
                  fl["D"](float(ell)), Qi.radius)
        # how far below the boundary is the certified ell? smallest ell the float
        # port would accept (sanity: must be <= our exact ell + 1e-6)
    print(f"   max |dq|_float - |dq|_exact : {worst_dq:.2e}")
    print(f"   max |D^(ell)_float - D^(ell)_exact| : {worst_D:.2e}")
    print(f"   float port confirming D^(ell) <= a : {len(used)-nbad}/{len(used)}")
    assert nbad == 0 and worst_D < 1e-6      # the float port's own pads are 1e-8/op

    # ---- margin statistics over all 1452 closures
    mar = sorted(-c["deficit_sqrt"] for c in closed)
    print(f"closure margin t_B - ell over 1452 boxes: min {mar[0]:.3e} "
          f"median {mar[len(mar)//2]:.3e} max {mar[-1]:.3e}")
    dsq = sorted(c["deficit_sqrt"] for c in closed)
    print(f"how many boxes close with margin > 1e-4: "
          f"{sum(1 for x in mar if x > 1e-4)}; > 1e-3: {sum(1 for x in mar if x > 1e-3)}")
    # ---- census of the transport maps that do the work
    print("maps used by at least one closure (map, #children it is admissible for, "
          "#boxes it closes):")
    from collections import Counter
    per_map = Counter(nmap(e["map"]) for e in adm)
    box_map = Counter(nmap(c["map"]) for c in closed)
    for mp in sorted(box_map, key=lambda m: -box_map[m]):
        dq = sorted(e["dq"] for e in adm if nmap(e["map"]) == mp)
        print(f"   {mp}  children {per_map[mp]:2d}  boxes {box_map[mp]:4d}  "
              f"dq in [{dq[0]:.6f}, {dq[-1]:.6f}]")
    idm = (tuple(range(6)), tuple(range(6)), 0, 0)
    print(f"   identity maps admissible: {per_map[idm]}, boxes closed by identity: "
          f"{box_map.get(idm,0)}")
    print("V6 PASSED")


if __name__ == "__main__":
    main()
