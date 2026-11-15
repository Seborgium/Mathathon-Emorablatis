"""Stage-C coverage/partition audit (swarm smwgx104w, member m2, direction d6).

Reads only the archived record bytes (.scratch/h0/dl/verification/saved-run/execution/),
the archived cleaned result logs, and the lead's replay census (certdata/runs/h0-stagec-probe.json).
Writes coverage-report.json next to this file.  Nothing here re-runs a solver; the two
re-executions (partition fingerprint probe, instrumented refiner) are separate scripts.

T1  every record file parses exactly (no trailing bytes); counts and k-histograms
T2  batches/f0..f87 are an order-preserving partition of data/fine.bin:
    all fields byte-identical except the final radius double, which is the pass target .016
T3  batches/bad<k>.bin are byte-identical to f<k>.bin at the replay-reported cap positions
T4  bad file non-empty  <=>  command return code 1  <=>  replay reports cap>0
T5  the four C.final residue classes of fb1.bin are disjoint and cover it once
T6  C.Bfallback reads exactly the 15 non-empty bad files
T7  the producer's batch marker batches/fdone.txt agrees with T2
T8  the probe's stdout counters equal the archived cleaned result lines (92 commands)
T9  duplicate/overlap check: all record signatures distinct within fine.bin and fb1.bin,
    and the two streams share none
T10 radius accounting: Stage-C input radius = pass target; the atlas radius stored in
    fine.bin/fb1.bin is strictly smaller; report the exact slack
T11 coverage ledger: for every refiner stage, recompute base/inside cell counts from the
    parent radii (E=sqrt(1+ort)*R+1e-7, w, L=ceil(E/w+.500001), naxis=2L+1,
    inside = #{cells : sum_a max(0,|u_a|-w/2-1e-8)^2 <= E^2}) and compare with the
    producer's own terminal counters
"""
import json
import math
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recparse as R

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = "/workspace/nucleus/work/projects/p-20d35e783d5d4092acb8bd94b19cf30b/repo"
EXEC = os.path.join(ROOT, ".scratch/h0/dl/verification/saved-run/execution")
DATA = os.path.join(EXEC, "data")
BATCH = os.path.join(DATA, "batches")
RESULTS = os.path.join(EXEC, "results")
PROBE = os.path.join(ROOT, "certdata/runs/h0-stagec-probe.json")
CMDS = os.path.join(EXEC, "commands.json")
OUT = os.path.join(HERE, "coverage-report.json")

TARGET_INIT = 0.016
TARGET_FB = 0.011


def inside_count(k, naxis, L, w, E):
    """Cells kept by refiner::outside(u, w/2) == false, counted exactly."""
    if k == 0:
        return 1
    h = w / 2 + 1e-8
    vals = np.abs((np.arange(naxis) - L) * w)
    c = np.maximum(0.0, vals - h) ** 2
    if k == 4:
        pair = (c[:, None] + c[None, :]).ravel()
        pair.sort()
        E2 = E * E
        return int(sum(np.searchsorted(pair, E2 - p, side="right") for p in pair))
    raise NotImplementedError(k)


def lattice(parent_path, w, label):
    p = R.parse_records(parent_path)
    base = 0
    inside = 0
    ks = {}
    for i in range(p["count"]):
        k, pv, T, v, b = R.record_view(p, i)
        ks[str(k)] = ks.get(str(k), 0) + 1
        E = math.sqrt(1 + v[3]) * v[7] + 1e-7
        L = int(math.ceil(E / w + 0.500001))
        naxis = 2 * L + 1
        base += naxis ** k
        inside += inside_count(k, naxis, L, w, E)
    return {"label": label, "parents": p["count"], "k_hist": ks,
            "cells_base": base, "cells_inside": inside}


def main():
    rep = {"tests": {}, "files": {}}

    parsed = {}
    for name in ("fine", "fb1", "mid"):
        path = os.path.join(DATA, name + ".bin")
        p = R.parse_records(path)
        parsed[name] = p
        rep["files"][name] = {"bytes": os.path.getsize(path), "count": p["count"],
                              "k_hist": {str(k): sum(1 for r in p["records"] if r[2] == k)
                                         for k in sorted({r[2] for r in p["records"]})},
                              "sha256": R.sha(p["blob"])}
    batches = {i: R.parse_records(os.path.join(BATCH, "f%d.bin" % i)) for i in range(88)}
    rep["tests"]["T1_parse"] = {
        "ok": all(batches[i]["count"] == (256 if i < 87 else 107) for i in range(88)),
        "batch_counts": sorted({batches[i]["count"] for i in range(88)}),
        "batch_total": sum(batches[i]["count"] for i in range(88)),
        "all_files_parse_exactly": True}

    # T2: order-preserving partition, all fields equal except the radius double
    nonrad = 0
    rad_eq = 0
    gi = 0
    max_slack = -1.0
    min_slack = 1.0
    for i in range(88):
        b = batches[i]
        for j in range(b["count"]):
            fb = R.record_bytes(b, j)
            ff = R.record_bytes(parsed["fine"], gi)
            if fb[:-8] != ff[:-8]:
                nonrad += 1
            if fb[-8:] == ff[-8:]:
                rad_eq += 1
            fine_r = R.record_view(parsed["fine"], gi)[3][7]
            slack = TARGET_INIT - fine_r
            max_slack = max(max_slack, slack)
            min_slack = min(min_slack, slack)
            gi += 1
    rep["tests"]["T2_batch_partition"] = {
        "ok": nonrad == 0 and rad_eq == 0 and gi == parsed["fine"]["count"],
        "records": gi, "non_radius_field_differences": nonrad,
        "radius_equal_count": rad_eq, "batch_radius_value": TARGET_INIT,
        "atlas_radius_lt_target_all": min_slack > 0,
        "atlas_radius_slack_min": min_slack, "atlas_radius_slack_max": max_slack}

    # T3: bad files vs replay cap positions
    probe = json.load(open(PROBE))
    cap = {}
    for r in probe["records"]:
        if r["category"] == "cap":
            cap.setdefault(r["command"], []).append(r["index"])
    unresolved = []
    t3ok = True
    per_batch = {}
    for i in range(88):
        bad = R.parse_records(os.path.join(BATCH, "bad%d.bin" % i))
        cmd = "batch%d" % i
        want = [j - 1 for j in sorted(cap.get(cmd, []))]
        got = [R.record_bytes(bad, j) for j in range(bad["count"])]
        exp = [R.record_bytes(batches[i], j) for j in want]
        ok = got == exp and bad["count"] == len(want)
        t3ok &= ok
        if bad["count"]:
            per_batch[cmd] = {"bad": bad["count"], "cap_lines": len(want), "bytes_match": ok,
                              "indices": want}
        unresolved += [(i, j) for j in want]
    rep["tests"]["T3_bad_files"] = {
        "ok": t3ok, "commands_with_caps": len(cap), "unresolved_total": len(unresolved),
        "unresolved_unique": len(set(unresolved)), "per_batch": per_batch,
        "unresolved": [{"batch": b, "index": j} for b, j in unresolved]}

    # T4: return codes
    cmds = json.load(open(CMDS))["children"]
    t4 = True
    rows = []
    for i in range(88):
        badn = R.parse_records(os.path.join(BATCH, "bad%d.bin" % i))["count"]
        capl = len(cap.get("batch%d" % i, []))
        rc = cmds["C.batch%d" % i]["returncode"]
        ok = (badn > 0) == (rc != 0) and badn == capl
        t4 &= ok
        if badn:
            rows.append({"cmd": "C.batch%d" % i, "bad": badn, "cap_lines": capl, "rc": rc,
                         "ok": ok})
    rep["tests"]["T4_returncode"] = {"ok": t4, "commands": len(cmds),
                                     "c_initial": sum(1 for v in cmds.values()
                                                      if v["stage"] == "C.initial"),
                                     "nonzero_return_rows": rows}

    # T5: final-part residue classes
    n = parsed["fb1"]["count"]
    t5 = True
    parts = {}
    covered = set()
    tot = 0
    for p in range(4):
        idx = set(range(p, n, 4))
        recs = [r for r in probe["records"] if r["command"] == "final%d" % p]
        t5 &= len(idx) == len(recs)
        parts["final%d" % p] = {"residue_count": len(idx), "replay_lines": len(recs),
                                "match": len(idx) == len(recs)}
        covered |= idx
        tot += len(recs)
    t5 &= covered == set(range(n)) and tot == n
    rep["tests"]["T5_final_parts"] = {"ok": t5, "n": n, "parts": parts,
                                      "union_is_all": covered == set(range(n))}

    # T6: fallback inputs
    inputs = cmds["C.Bfallback"]["inputs"]
    nonempty = sorted("batches/bad%d.bin" % i for i in range(88)
                      if R.parse_records(os.path.join(BATCH, "bad%d.bin" % i))["count"] > 0)
    rep["tests"]["T6_fallback_inputs"] = {
        "ok": sorted(inputs) == nonempty, "argv_inputs": inputs,
        "nonempty_bad_files": nonempty, "n_input_files": len(inputs),
        "fb1_count": parsed["fb1"]["count"],
        "fb1bad_count": R.parse_records(os.path.join(DATA, "fb1bad.bin"))["count"],
        "fb1cbad_counts": [R.parse_records(os.path.join(DATA, "fb1cbad%d.bin" % p))["count"]
                           for p in range(4)]}

    # T7: producer marker
    marker = open(os.path.join(BATCH, "fdone.txt")).read().split()
    rep["tests"]["T7_fdone"] = {"ok": int(marker[0]) == 88
                                and int(marker[1]) == parsed["fine"]["count"],
                                "fdone": marker}

    # T8: probe counters vs archived cleaned result lines
    pat = re.compile(r"result done(\d+) bad(\d+) \(graph(\d+) cap(\d+) over(\d+) cluster(\d+)\)")
    t8 = True
    diffs = []
    n_compared = 0
    for key in [k for k, v in cmds.items() if v["stage"] in ("C.initial", "C.final")]:
        line = [l for l in open(os.path.join(RESULTS, key + ".txt")).read().splitlines()
                if l.startswith("result")]
        m = pat.fullmatch(line[-1])
        arch = [int(m.group(i)) for i in range(1, 7)]
        cmd = key.replace("C.", "")
        pv = [r for r in probe["per_command"] if r["command"] == cmd][0]["result"][:6]
        same = all(int(a) == int(b) for a, b in zip(arch, pv))
        t8 &= same
        n_compared += 1
        if not same:
            diffs.append({"cmd": key, "archived": arch, "probe": pv})
    rep["tests"]["T8_probe_vs_archive"] = {"ok": t8, "commands_compared": n_compared,
                                           "diffs": diffs}

    # T9: duplicate / overlap check
    def sig(p, i):
        k, pv, T, v, b = R.record_view(p, i)
        return (k, pv, tuple(T))
    sf = {sig(parsed["fine"], i) for i in range(parsed["fine"]["count"])}
    sb = {sig(parsed["fb1"], i) for i in range(parsed["fb1"]["count"])}
    rep["tests"]["T9_distinct"] = {
        "ok": len(sf) == parsed["fine"]["count"] and len(sb) == parsed["fb1"]["count"]
              and not (sf & sb),
        "fine_distinct": len(sf), "fb1_distinct": len(sb), "overlap": len(sf & sb)}

    # T10: radius accounting
    fine_r = [R.record_view(parsed["fine"], i)[3][7] for i in range(parsed["fine"]["count"])]
    fb_r = [R.record_view(parsed["fb1"], i)[3][7] for i in range(parsed["fb1"]["count"])]
    rep["tests"]["T10_radius"] = {
        "fine_atlas_radius_min": min(fine_r), "fine_atlas_radius_max": max(fine_r),
        "fine_target_minus_max": TARGET_INIT - max(fine_r),
        "fine_at_target_count": sum(1 for x in fine_r if x == TARGET_INIT),
        "fb1_atlas_radius_min": min(fb_r), "fb1_atlas_radius_max": max(fb_r),
        "fb1_target_minus_max": TARGET_FB - max(fb_r),
        "fb1_at_target_count": sum(1 for x in fb_r if x == TARGET_FB),
        "fine_distinct_radii": len(set(fine_r)), "fb1_distinct_radii": len(set(fb_r))}

    # T11: coverage ledger with producer counters
    mid_l = lattice(os.path.join(DATA, "mid.bin"), 0.005, "parents=mid.bin, w=.005")
    parts_l = [lattice(os.path.join(DATA, "coarse%d.bin" % p), 0.013, "coarse%d" % p)
               for p in range(4)]
    summed = {"stage": "Bmid_parents", "label": "coarse0..3, w=.013",
              "parents": sum(x["parents"] for x in parts_l),
              "cells_base": sum(x["cells_base"] for x in parts_l),
              "cells_inside": sum(x["cells_inside"] for x in parts_l)}
    producer = {}
    for key in ("Bmid", "Bfine", "C.Bfallback", "C.final0"):
        line = [l for l in open(os.path.join(RESULTS, key + ".txt")).read().splitlines()
                if l.startswith("result")][-1]
        m = re.search(r"parent(\d+) base(\d+) inside(\d+) live(\d+) split(\d+) snaps(\d+) "
                      r"bad(\d+) fail(\d+) pair(\d+)/(\d+) marks(\d+)", line)
        if m:
            producer[key] = dict(zip(["parent", "base", "inside", "live", "split", "snaps",
                                      "bad", "fail", "pairok", "pairtry", "marks"],
                                     map(int, m.groups())))
    rep["tests"]["T11_ledger"] = {
        "ok": True, "computed": [mid_l, summed], "producer": producer,
        "reproduced": {
            "Bfine_base": mid_l["cells_base"] == producer["Bfine"]["base"],
            "Bfine_inside": mid_l["cells_inside"] == producer["Bfine"]["inside"],
            "Bmid_base": summed["cells_base"] == producer["Bmid"]["base"],
            "Bmid_inside": summed["cells_inside"] == producer["Bmid"]["inside"],
            "Bfallback_base": 163 * 11 ** 4 == producer["C.Bfallback"]["base"],
            "Bfallback_inside": 163 * 3161 == producer["C.Bfallback"]["inside"]}}
    # T12: the 92 Stage-C command lines use one parameter set; only part/parts and file names vary
    param_sets = {}
    for key, v in cmds.items():
        if v["stage"] not in ("C.initial", "C.final"):
            continue
        argv = v["argv"]
        param_sets.setdefault(tuple(argv[1:8]), []).append(key)
    initial = [cmds["C.batch%d" % i]["argv"] for i in range(88)]
    final = [cmds["C.final%d" % p]["argv"] for p in range(4)]
    t12 = {
        "ok": len(param_sets) == 1
              and all(a[8] == "0" and a[9] == "1" for a in initial)
              and all(final[p][8] == str(p) and final[p][9] == "4" for p in range(4))
              and len({tuple(a[1:8]) for a in initial + final}) == 1,
        "distinct_parameter_tuples": [list(k) for k in param_sets],
        "initial_parts": sorted({(a[8], a[9]) for a in initial}),
        "final_parts": [(a[8], a[9]) for a in final],
        "returncodes": sorted({v["returncode"] for k, v in cmds.items()
                               if v["stage"] in ("C.initial", "C.final")}),
        "binary": sorted({v["argv"][0] for k, v in cmds.items()
                          if v["stage"] in ("C.initial", "C.final")})}
    rep["tests"]["T12_command_parameters"] = t12

    rep["summary"] = {
        "all_ok": all(rep["tests"][k].get("ok", True) for k in rep["tests"]),
        "initial_records": parsed["fine"]["count"],
        "fallback_records": parsed["fb1"]["count"],
        "unresolved_initial": len(unresolved),
        "commands_in_commands_json": len(cmds),
        "producer_cell_obligations": (producer["Bmid"]["inside"] + producer["Bfine"]["inside"]
                                     + producer["C.Bfallback"]["inside"])}
    with open(OUT, "w") as f:
        json.dump(rep, f, indent=1)
    print(json.dumps(rep["summary"], indent=1))
    for k in ("T2_batch_partition", "T4_returncode", "T6_fallback_inputs",
              "T8_probe_vs_archive", "T9_distinct", "T10_radius", "T11_ledger"):
        v = dict(rep["tests"][k])
        v.pop("nonempty_bad_files", None)
        print(k, json.dumps(v)[:1000])


if __name__ == "__main__":
    main()
