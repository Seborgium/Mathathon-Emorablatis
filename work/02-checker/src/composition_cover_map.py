"""Export the recovered fallback cover map (direction d6, member m2).

Source: pcov.log, produced by build/brun-cov (copy of the archived stageB.cpp with an
output-only probe).  The instrumented build reproduces data/fb1.bin byte-identically, so the
map is a property of the archived run, not of a different execution.

Output: composition-cover-map.json
  metric     the refiner's cell lattice parameters (w, target, E per parent, naxis, inside)
  parents    one entry per capped record, in the order C.Bfallback processed them
             (ASCII order of the 15 bad-file names, record order inside each file):
               batch, batch_index, fine_index   provenance in the archived streams
               inside_cells                     cells that must be covered (3161)
               marks, created, used, inherited  producer/probe counters
               children                         fb1 indices covering its cells
  children   one entry per fb1 record: radius, and the number of parents it covers
Read with: json.load(open('composition-cover-map.json'))
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recparse as R

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = "/workspace/nucleus/work/projects/p-20d35e783d5d4092acb8bd94b19cf30b/repo"
EXEC = os.path.join(ROOT, ".scratch/h0/dl/verification/saved-run/execution")
CMDS = os.path.join(EXEC, "commands.json")
OUT = os.path.join(HERE, "composition-cover-map.json")


def main():
    cmds = json.load(open(CMDS))["children"]
    inputs = cmds["C.Bfallback"]["inputs"]           # order is the processing order
    # parent provenance: (batch, batch_index) in the order brun saw them
    parents_meta = []
    for name in inputs:
        i = int(re.search(r"bad(\d+)\.bin$", name).group(1))
        bad = R.parse_records(os.path.join(EXEC, "data", name))
        for j in range(bad["count"]):
            parents_meta.append({"batch": i, "batch_index": j, "fine_index": 256 * i + j})
    rows = []
    for line in open(os.path.join(HERE, "pcov.log")):
        if not line.startswith("PCOV"):
            continue
        head, idx = line.split("|")
        parts = head.split()
        d = {"ordinal": int(parts[1]), "ok": int(parts[2][2:])}
        for tok in parts[3:]:
            m = re.match(r"([a-zA-Z]+)(-?\d+)", tok)
            if m:
                d[m.group(1)] = int(m.group(2))
        d["children"] = [int(x) for x in idx.split()]
        rows.append(d)
    fb1 = R.parse_records(os.path.join(EXEC, "data/fb1.bin"))
    child_cover = {}
    for r in rows:
        for c in r["children"]:
            child_cover[c] = child_cover.get(c, 0) + 1
    parents = []
    for ord_, (meta, r) in enumerate(zip(parents_meta, rows)):
        assert r["ordinal"] == ord_
        parents.append({**meta, "inside_cells": r["inside"], "marks": r["marks"],
                        "created": r["created"], "used": r["used"],
                        "inherited": r["inherited"], "ok": r["ok"],
                        "children": r["children"]})
    children = []
    for j in range(fb1["count"]):
        k, pv, T, v, b = R.record_view(fb1, j)
        children.append({"fb1_index": j, "radius": v[7], "covers_parents": child_cover.get(j, 0)})
    out = {
        "what": "cover map of the 163 capped Stage-C records by the 1127 fallback balls",
        "how": "instrumented copy of the archived stageB.cpp; output byte-identical to data/fb1.bin",
        "metric": {"w": 0.0038, "target_child_radius": 0.011,
                   "E_formula": "sqrt(1+ort)*R + 1e-7, R = parent's stored radius (=0.016 here)",
                   "naxis": 11, "cells_total_per_parent": 14641, "inside_cells_per_parent": 3161,
                   "cover_criterion": "cell covered iff eval(corner(u,w/2)) <= target, "
                                      "relationB::init/eval in stageB.cpp"},
        "counts": {"parents": len(parents), "children": len(children),
                   "incidences": sum(p["used"] for p in parents),
                   "inherited": sum(p["inherited"] for p in parents)},
        "parents": parents, "children": children,
        "caveat": "the map is not in the archive; it is recovered here. Verify with "
                  "coverage/relationB arithmetic, not by trust; 7 of 515243 cells are closed "
                  "by the snap path rather than by a relation mark (see report section 5).",
    }
    json.dump(out, open(OUT, "w"), indent=1)
    print(json.dumps(out["counts"], indent=1))
    print("parents", len(parents), "children", len(children),
          "incidences", out["counts"]["incidences"])
    print("children never used:", sum(1 for c in children if c["covers_parents"] == 0))
    print("child covers_parents min/median/max:",
          min(c["covers_parents"] for c in children),
          sorted(c["covers_parents"] for c in children)[len(children)//2],
          max(c["covers_parents"] for c in children))


if __name__ == "__main__":
    main()
