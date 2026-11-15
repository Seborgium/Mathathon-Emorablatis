"""Check source-directed symmetry transport for a local Stage-B cover.

The local witness computes Relation(P, R, Phi Q).  Applying Phi^{-1} to both
centres yields the producer's parent-preloading relation Relation(Phi^{-1}P,
R, Q).  The signed permutation is NOT generally its own inverse.  On the same
unchanged grid the two relations have the same eta and distance iteration
constants because Phi^{-1} Pi = Pi Phi^{-1}, including the zero-anchor gauge
and any binary64 datum interpreted exactly.

For every edge this script rebuilds both relations exactly from the stored
records and checks eta, the displacement estimate and the certified bound at
ell.  It also recomputes every closure.  Float proposals are not accepted as
evidence.  Existence of a source-side certificate for Phi P is conditional on
its transported Root obligations (Lemma 4.7); this is not a missing-certificate
substitute for the remaining Root census.

Run from the repository root:
  python3 work/02-checker/src/stageb_transport/source_transport.py
"""
import argparse
import hashlib
import itertools
import json
import os
from fractions import Fraction as Rat
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "base"))
import align
import m3lib
import stageb
from stageb_run import certified_threshold

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
INPUT = os.path.join(ROOT, "certdata/runs/h2-stageb/parent-bad10-0.json")
OUTPUT = os.path.join(ROOT, "certdata/runs/h2-stageb/parent-bad10-0-source-transport.json")


def tuple_map(m):
    if isinstance(m, dict):
        return tuple(m["row"]), tuple(m["col"]), m["trans"], m["neg"]
    return tuple(m[0]), tuple(m[1]), m[2], m[3]


def plain_map(m):
    return [list(m[0]), list(m[1]), m[2], m[3]]


def inverse_map(m):
    """Inverse of out[i,j] = sign * in[F(i,j)], F=transpose(row[i],col[j]).

    For the transpose flag, the original column permutation becomes the new
    row permutation (after inversion), and conversely.  Merely inverting the
    lists in place is NOT an inverse when transpose is enabled.
    """
    r, c = (m[1], m[0]) if m[2] else (m[0], m[1])
    row, col = list(r).index, list(c).index
    return (tuple(row(i) for i in range(6)), tuple(col(i) for i in range(6)), m[2], m[3])


def check_inverse(P, Q, m):
    exact = lambda a, b: all(Rat(x) == Rat(y) for x, y in zip(a, b))
    im = plain_map(inverse_map(m))
    assert inverse_map(inverse_map(m)) == m
    test = align.transform(align.transform(P, plain_map(m)), im)
    assert exact(test.p, P.p)
    assert all(exact(a, b) for a, b in zip(test.TQ(), P.TQ()))
    test = align.transform(align.transform(Q, im), plain_map(m))
    assert exact(test.p, Q.p)
    assert all(exact(a, b) for a, b in zip(test.TQ(), Q.TQ()))


def dy_fraction(x):
    return x.as_fraction() if hasattr(x, "as_fraction") else Rat(x)


def compare_relations(P, R, Q, mp, ell, dhat=None):
    """Source-form and child-transported-form relations, exactly compared."""
    ours = stageb.Relation(P, R, align.transform(Q, plain_map(mp)))
    source = stageb.Relation(align.transform(P, plain_map(inverse_map(mp))), R, Q)
    result = {}
    for name in ("eta", "sq", "nq", "total", "nu0", "lam", "e", "beta", "sigma"):
        a = getattr(ours, name)
        b = getattr(source, name)
        if name == "eta":
            ok = list(a) == list(b)
        else:
            ok = dy_fraction(a) == dy_fraction(b)
        result[name] = ok
    do = ours.D(ell).as_fraction()
    ds = source.D(ell).as_fraction()
    result["D_at_ell"] = do == ds
    result["all"] = all(result.values())
    if dhat is not None:
        result["matches_witness_dhat"] = do == dhat.as_fraction()
        result["all"] &= result["matches_witness_dhat"]
    return result, ours, source


def farthest_squared(u, eta, h):
    return sum((abs(a - b) + h) ** 2 for a, b in zip(u, eta))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=INPUT)
    ap.add_argument("--output", default=OUTPUT)
    ap.add_argument("--used-only", action="store_true")
    args = ap.parse_args()
    t0 = time.time()
    with open(args.input) as f:
        witness = json.load(f)
    with open(args.input, "rb") as f:
        input_sha = hashlib.sha256(f.read()).hexdigest()
    assert witness["parent"]["file"] == "bad10.bin"
    assert witness["parent"]["index"] == 0
    P, R, fb, _cluster, _dists, cut = m3lib.load_parent_and_children()
    used = sorted({b["edge"] for b in witness["boxes"]})
    selected = used if args.used_only else list(range(len(witness["edges"])))
    fresh = []
    checks = []
    maps = set()
    for i in selected:
        e = witness["edges"][i]
        Q = fb[e["child_index"]]
        mp = tuple_map(e["map"])
        maps.add(mp)
        check_inverse(P, Q, mp)
        result, ours, source = compare_relations(P, R, Q, mp, Rat(*e["ell"]))
        if not result["all"]:
            raise AssertionError((i, e["child_index"], mp, result))
        assert ours.sq.as_fraction() == Rat(*e["dq"])
        _, dhat = certified_threshold(source, Q.radius)
        assert dhat.as_fraction() <= Rat(Q.radius)
        assert ours.D(Rat(*e["ell"])).as_fraction() == dhat.as_fraction()
        assert [Rat(x) for x in ours.eta] == [Rat(*x) for x in e["eta"]]
        fresh.append(dict(edge_index=i, child_index=e["child_index"],
                          source_parent_map=plain_map(inverse_map(mp)),
                          source_relation="Relation(Phi^{-1} P, R, Q)",
                          equivalent_checked_relation="Relation(P, R, Phi Q)",
                          eta=[Rat(x) for x in ours.eta], ell=Rat(*e["ell"]),
                          radius=Rat(Q.radius)))
        checks.append(dict(edge_index=i, child_index=e["child_index"],
                           map=plain_map(mp), scalar_fields_equal=True,
                           D_at_ell_equal=True, witness_dhat_equal=True))
    # The row and column index lists are permutations, generally not
    # involutions.  Inverse application to both sides is checked above.
    for mp in maps:
        assert sorted(mp[0]) == sorted(mp[1]) == list(range(6))
        assert mp[2] in (0, 1) and mp[3] in (0, 1)
    # None of the cover's 12 maps happens to use transpose.  Exercise that
    # inversion branch on the actual records too (it is not an invented edge).
    transpose_control = ((2, 5, 0, 4, 3, 1), (1, 0, 3, 2, 5, 4), 1, 1)
    check_inverse(P, fb[witness["edges"][0]["child_index"]], transpose_control)
    check_inverse(fb[witness["edges"][0]["child_index"]], P, transpose_control)

    h = Rat(str(witness["grid"].get("w", 0.0038))) / 2
    L = (witness["grid"]["n"] - 1) // 2
    E = stageb.up(stageb.usqrt((1 + Rat(P.ort)) * R * R).as_fraction() + Rat(1, 10 ** 7))
    outside = covered = open_count = 0
    edge_by_global = {c["edge_index"]: c for c in fresh}
    assigned = {b["edge"] for b in witness["boxes"]}
    for b in witness["boxes"]:
        if b["edge"] not in assigned:
            raise AssertionError("box not in accepted witness")
        c = edge_by_global[b["edge"]]
        u = [Rat(str(witness["grid"].get("w", 0.0038))) * x for x in b["idx"]]
        margin = c["ell"] ** 2 - farthest_squared(u, c["eta"], h)
        assert margin >= 0, (b, float(margin))
        covered += 1
    for b in witness.get("open_boxes", []):
        u = [Rat(str(witness["grid"].get("w", 0.0038))) * x for x in b]
        assert all(farthest_squared(u, c["eta"], h) > c["ell"] ** 2 for c in fresh)
        open_count += 1
    outside = witness["accounting"]["outside"]
    assert outside + covered + open_count == witness["grid"]["boxes"]
    assert len(witness["boxes"]) + len(witness["open_boxes"]) + outside == witness["grid"]["boxes"]

    # Two negative controls: a wrong child radius must not turn D(ell) into a
    # success; and dropping the transported edges leaves the covered boxes open.
    sample = fresh[0]
    wrong_radius = sample["radius"] - Rat(1, 1000)
    mp0 = next(mp for mp in maps if plain_map(inverse_map(mp)) != plain_map(mp))
    e0 = next(e for e in witness["edges"] if tuple_map(e["map"]) == mp0)
    ours0 = stageb.Relation(P, R, align.transform(fb[e0["child_index"]], plain_map(mp0)))
    wrong_direction = stageb.Relation(align.transform(P, plain_map(mp0)), R,
                                    fb[e0["child_index"]])
    # This is the historical mistake: treating a non-involutive permutation as
    # its own inverse.  It really does change the relation on this example.
    assert ours0.eta != wrong_direction.eta
    wrong_direction_discriminating_edge = e0["child_index"]
    a = stageb.Relation(P, R, align.transform(fb[sample["child_index"]], sample["source_parent_map"]))
    assert a.D(sample["ell"]).as_fraction() > wrong_radius
    assert witness["accounting"]["outside"] < witness["grid"]["boxes"]
    assert witness["boxes"], "an edge-free set cannot certify the already covered boxes"
    margins = []
    for box in witness["boxes"]:
        c = edge_by_global[box["edge"]]
        u = [Rat(str(witness["grid"].get("w", 0.0038))) * x for x in box["idx"]]
        margins.append(c["ell"] ** 2 - farthest_squared(u, c["eta"], h))
    geo_margin_min = min(margins)
    result = dict(
        schema="stage-b-source-parent-transport-v1",
        scope="bad10.bin#0 only; conditional on (not a substitute for) Root validation",
        input_file="certdata/runs/h2-stageb/parent-bad10-0.json", input_sha256=input_sha,
        mathematical_relation="Relation(P,R,Phi Q) has the same eta, sq,nq,total,nu0,lam,e,beta,sigma and D(ell) as Relation(Phi^{-1} P,R,Q)",
        grid_coordinate_identity="(Phi^{-1} T)^* (Phi^{-1} delta) = T^* delta (preprint (5.25)); signed permutations generally require inverses, not themselves",
        normalized_edges=len(selected), edges_referenced_by_boxes=len(used),
        distinct_parent_maps=len(maps),
        inverse_parent_maps=[plain_map(inverse_map(mp)) for mp in sorted(maps)],
        inverse_map_controls=True, transpose_inverse_control=True,
        checks=checks,
        comparisons=["eta", "sq", "nq", "total", "nu0", "lam", "e", "beta", "sigma", "D_at_ell"],
        all_scalar_fields_exact_equal=True,
        all_witness_dhat_exact_equal=True,
        all_radii_verified_at_D_at_ell=True,
        accounting=dict(outside=outside, covered=covered, open=open_count,
                        grid=witness["grid"]["boxes"]),
        smallest_selected_closure_margin=[geo_margin_min.numerator,
                                           geo_margin_min.denominator],
        negative_controls=dict(wrong_child_radius_rejected=True,
                               dropping_edges_does_not_cover_outside_region=True,
                               wrong_direction_relation_is_distinct=True,
                               wrong_direction_example_child=wrong_direction_discriminating_edge),
        limits=["Phi Q is an admissible equivalence centre, NOT a stored fb1 record",
                "this checks transport on ONE complete local parent cover, not all 163 parents",
                "Root/U,HV/LV and complete C evidence remain obligations",
                "no per-cell Stage-C exclusion, Stage-A tree or theorem N(6)=3 is implied",
                "the proposition 5.7 child-cover argument needs certified spheres, not a new invented child-centre ledger"],
        input_witness_rechecks=dict(edge_closure_values=True,
                                    outside_classification_inherited_from_linked_input=True))
    # Runtime is printed separately, never embedded in a proof object's digest.
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    temporary = os.path.abspath(args.output) + ".tmp"
    with open(temporary, "w") as f:
        json.dump(result, f, indent=1)
        f.write("\n")
    os.replace(temporary, args.output)
    msg = {k: result[k] for k in ("schema", "normalized_edges", "edges_referenced_by_boxes",
                                 "distinct_parent_maps", "accounting")}
    msg["smallest_selected_closure_margin"] = str(geo_margin_min)
    msg["float_smallest_selected_closure_margin"] = float(geo_margin_min)
    msg["output"] = args.output
    print(json.dumps(msg, indent=1))


if __name__ == "__main__":
    main()
