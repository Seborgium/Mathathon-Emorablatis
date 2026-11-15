#!/usr/bin/env python3
"""Independent numerical-record checker for the MUB d=6 saved run.

Team V (verification), wave W1 / work unit 10.  Written from
  * work/10-recreate/spec/interfaces.md (frozen interface: argv, record layout,
    bounds, bad-file conventions, exit codes),
  * the published program sources (atlas.cpp saveRecords/readRecords, stageB.cpp
    main/validate, stageC.cpp main, covout.cpp),
  * VERIFY.md (recorded run schedule) and commands.json,
and it does NOT read, import, copy or consult check_records.py.

Usage:
    python3 check_records_indep.py <execution-dir> [--json out.json] [--verbose]

<execution-dir> holds data/, results/ and commands.json (recorded saved-run
layout).  Exit status 0 = PASS, 1 = FAIL, 2 = usage.

Every check carries a tier:
  A  forced by the frozen interface specification / published record format
  B  forced by the recorded run schedule (commands.json) plus that run's artefact
     and stdout counters
  C  empirical invariant of this data set (true of every recorded record,
     documented as such; not forced by the format)
A FAIL in any tier fails the run; the tier records what would have to be argued
if the check were removed.
"""

import argparse
import json
import os
import re
import struct
import sys

MAXK = 10                   # spec 4, enforced by readRecords
MAXCOUNT = 2000000          # spec 3.2, enforced by readRecords
MAXRADIUS = 0.126           # spec 3.2, enforced by validate
BOUNDS = {                  # name -> [lo, hi) as in stageB.cpp validate
    "C": (0.0, 20.0),
    "n0": (0.0, 1e-6),
    "froot": (0.0, 1e-6),
    "id": (0.0, 1e-4),
    "ort": (0.0, 1e-5),
    "hor": (0.0, 1e-5),
    "mnorm": (0.0, 2.0),
}
TAIL = ["C", "n0", "id", "ort", "hor", "mnorm", "froot", "radius"]
# Tier-C empirical bands: the recorded run keeps these three small quantities in
# a band ~1e-6 wide relative to their value (measured over all 49 731 records:
# id in 2e-6+[2.62e-14,1.32e-13], ort in 1e-8+[0,1.72e-14], hor in 1e-8+[0,3.82e-16]).
# Not forced by any format: they are the perturbation sizes the run uses.  Their
# use is that the bands are disjoint, so swapping two of the fields is visible.
BANDS = {"id": (2e-06, 2e-06 + 1e-12), "ort": (1e-08, 1e-08 + 1e-12),
         "hor": (1e-08, 1e-08 + 1e-12)}
REC_HEAD = 4 + 36 * 8 + 8 * 8


class RecordError(Exception):
    pass


class Report(object):
    def __init__(self):
        self.checks = []

    def check(self, cid, ok, detail, tier="A"):
        self.checks.append({"id": cid, "tier": tier, "ok": bool(ok), "detail": detail})
        return bool(ok)

    def failures(self):
        return [c for c in self.checks if not c["ok"]]

    @property
    def ok(self):
        return not self.failures()


def parse_record_file(path):
    """(count, records); records = [(k, p, T, tail, raw_bytes)].

    Layout (spec 3.2, atlas.cpp saveRecords):
        uint64 count, then count x {int32 k, double p[36], double T[k][36], double tail[8]}
    Raises RecordError on any deviation, including trailing bytes.
    """
    with open(path, "rb") as f:
        data = f.read()
    n = len(data)
    if n < 8:
        raise RecordError("file is %d bytes, shorter than the 8-byte count" % n)
    count = struct.unpack_from("<Q", data, 0)[0]
    if count > MAXCOUNT:
        raise RecordError("count %d exceeds the %d cap of readRecords" % (count, MAXCOUNT))
    off = 8
    recs = []
    for i in range(count):
        if off + 4 > n:
            raise RecordError("record %d: truncated inside the int32 k (byte %d of %d)" % (i, off, n))
        (k,) = struct.unpack_from("<i", data, off)
        if k < 0 or k > MAXK:
            raise RecordError("record %d: k=%d outside [0,%d]" % (i, k, MAXK))
        size = REC_HEAD + 288 * k
        if off + size > n:
            raise RecordError("record %d: truncated, needs %d bytes at offset %d, file has %d"
                              % (i, size, off, n))
        p = struct.unpack_from("<36d", data, off + 4)
        T = [struct.unpack_from("<36d", data, off + 4 + 288 + 288 * a) for a in range(k)]
        tail = struct.unpack_from("<8d", data, off + 4 + 288 + 288 * k)
        recs.append((k, p, T, tail, data[off:off + size]))
        off += size
    if off != n:
        raise RecordError("%d trailing byte(s) after %d records" % (n - off, count))
    return count, recs


def check_one_file(report, rel, recs, max_radius, cid_prefix, expect_radius=None):
    """Per-record invariants of spec 3.2 (validate) plus the tier-C constants."""
    bad_bounds = bad_p = bad_T = nonfinite = bad_const = bad_target = 0
    first = {}
    for i, (k, p, T, tail, _raw) in enumerate(recs):
        vals = dict(zip(TAIL, tail))
        for name, (lo, hi) in BOUNDS.items():
            v = vals[name]
            if not (v >= lo and v < hi):
                bad_bounds += 1
                first.setdefault("bounds", "record %d: %s=%r not in [%g,%g)" % (i, name, v, lo, hi))
        r = vals["radius"]
        if r != r or r in (float("inf"), float("-inf")):
            nonfinite += 1
            first.setdefault("finite", "record %d: radius=%r" % (i, r))
        elif not (0.0 <= r <= max_radius):
            bad_bounds += 1
            first.setdefault("bounds", "record %d: radius=%r not in [0,%g]" % (i, r, max_radius))
        for h, v in enumerate(p):
            if v != v or v in (float("inf"), float("-inf")):
                nonfinite += 1
                first.setdefault("finite", "record %d: p[%d]=%r" % (i, h, v))
            elif abs(v) > 4.0:
                bad_p += 1
                first.setdefault("p", "record %d: |p[%d]|=%r > 4" % (i, h, abs(v)))
        for a in range(k):
            for h, v in enumerate(T[a]):
                if v != v or v in (float("inf"), float("-inf")):
                    nonfinite += 1
                    first.setdefault("finite", "record %d: T[%d][%d]=%r" % (i, a, h, v))
                elif abs(v) > 1.01:
                    bad_T += 1
                    first.setdefault("T", "record %d: |T[%d][%d]|=%r > 1.01" % (i, a, h, abs(v)))
        for name, (lo, hi) in BANDS.items():
            v = vals[name]
            if not (lo <= v <= hi):
                bad_const += 1
                first.setdefault("const", "record %d: %s=%r outside the recorded band [%r,%r]"
                                 % (i, name, v, lo, hi))
        if expect_radius is not None and r != expect_radius:
            bad_target += 1
            first.setdefault("target", "record %d: radius=%r, brun emit() forces the batch target %r"
                             % (i, r, expect_radius))
    tailmsg = "".join("; " + first[k] for k in ("bounds", "p", "T") if k in first)
    report.check(cid_prefix + ".bounds", bad_bounds == 0 and bad_p == 0 and bad_T == 0,
                 "%s: %d records; %d tail, %d |p|>4, %d |T|>1.01 violations%s"
                 % (rel, len(recs), bad_bounds, bad_p, bad_T, tailmsg), "A")
    report.check(cid_prefix + ".finite", nonfinite == 0,
                 "%s: %d non-finite doubles%s"
                 % (rel, nonfinite, "; " + first["finite"] if "finite" in first else ""), "A")
    report.check(cid_prefix + ".constants", bad_const == 0,
                 "%s: %d records deviate from the recorded id/ort/hor constants%s"
                 % (rel, bad_const, "; " + first["const"] if "const" in first else ""), "C")
    if expect_radius is not None:
        report.check(cid_prefix + ".radius_is_target", bad_target == 0,
                     "%s: %d records with radius != brun target %r%s"
                     % (rel, bad_target, expect_radius, "; " + first["target"] if "target" in first else ""), "B")


def ascii_sorted(names):
    """ASCII (byte) filename order: bad10 < bad3, as C.Bfallback records it."""
    return sorted(names, key=lambda s: s.encode())


def emit(report, args, extra):
    out = {
        "result": "PASS" if report.ok else "FAIL",
        "checks": len(report.checks),
        "failed": len(report.failures()),
        "failures": report.failures(),
        "summary": extra,
        "scope": ("Derived numerical consistency only: record layout, bounds, shard/partition/"
                  "subsequence/coverage relations and artefact-vs-stdout counters. Not an "
                  "authentication of the archive, not a check of the C++ implementation."),
    }
    text = json.dumps(out, indent=1)
    print(text)
    if args.json:
        with open(args.json, "w") as f:
            f.write(text + "\n")
    if args.verbose:
        for c in report.checks:
            print("%s %-30s %s" % ("ok  " if c["ok"] else "FAIL", c["id"], c["detail"]),
                  file=sys.stderr)
    return 0 if report.ok else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("execution_directory")
    ap.add_argument("--json", default=None)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)

    root = args.execution_directory
    data = os.path.join(root, "data")
    results = os.path.join(root, "results")
    cmdpath = os.path.join(root, "commands.json")
    report = Report()

    if not os.path.isdir(data):
        report.check("structure", False, "no data/ directory under %r" % root, "A")
        return emit(report, args, {})
    if not os.path.isfile(cmdpath):
        report.check("structure", False, "no commands.json under %r" % root, "A")
        return emit(report, args, {})
    try:
        with open(cmdpath, "rb") as f:
            cmds = json.load(f)["children"]
        if not isinstance(cmds, dict):
            raise ValueError("'children' is not an object")
    except Exception as exc:                                    # noqa: BLE001
        report.check("structure", False, "commands.json unusable: %s" % exc, "A")
        return emit(report, args, {})

    # ------------------------------------------------------------------ parsing
    present = []
    for dirpath, _dn, filenames in os.walk(data):
        for fn in filenames:
            present.append(os.path.relpath(os.path.join(dirpath, fn), data).replace(os.sep, "/"))
    present.sort()
    parsed = {}
    parse_errors = {}
    for rel in present:
        if not rel.endswith(".bin"):
            continue
        try:
            parsed[rel] = parse_record_file(os.path.join(data, rel))
        except RecordError as exc:
            parse_errors[rel] = str(exc)
        except OSError as exc:
            parse_errors[rel] = "unreadable: %s" % exc
    report.check("recordfiles.parse", not parse_errors,
                 "%d record files parsed, %d failed%s"
                 % (len(parsed), len(parse_errors),
                    "".join("; %s: %s" % kv for kv in sorted(parse_errors.items()))), "A")

    declared = set()
    implicit = []
    for name, c in cmds.items():
        for key in ("inputs", "outputs"):
            for p in c.get(key) or []:
                declared.add(p.replace(os.sep, "/"))
        av = c.get("argv") or []
        if len(av) >= 6 and av[0].endswith("brun") and av[5] != "-":
            # stageB.cpp main writes <prefix>done.txt whenever batching is on; the
            # recorded commands.json lists <prefix><n>.bin outputs but not this file.
            implicit.append(av[5] + "done.txt")
            declared.add(av[5] + "done.txt")
    declared.add("commands.json")
    missing = sorted(p for p in declared if p != "commands.json" and p not in present)
    undeclared = sorted(p for p in present if p not in declared)
    report.check("files.declared", not missing and not undeclared,
                 "declared-but-absent: %s; present-but-undeclared: %s"
                 % (missing or "none", undeclared or "none"), "B")
    report.check("commands.count", len(cmds) == 100,
                 "%d recorded commands (the published run has 100)" % len(cmds), "B")

    def argv(name):
        return cmds[name].get("argv") or []

    def rc(name):
        return cmds[name].get("returncode")

    def recs(rel):
        return parsed[rel][1] if rel in parsed else []

    def count(rel):
        return len(parsed[rel][1]) if rel in parsed else None

    def res_line(name, prefix):
        p = os.path.join(results, name + ".txt")
        if not os.path.isfile(p):
            return None
        with open(p, "r", errors="replace") as f:
            for line in reversed(f.read().splitlines()):
                if line.startswith(prefix):
                    return line
        return None

    # --------------------------------------------------------------- centers.txt
    centers_n = None
    cpath = os.path.join(data, "centers.txt")
    if not os.path.isfile(cpath):
        report.check("centers.format", False, "data/centers.txt absent", "A")
    else:
        with open(cpath, "r", errors="replace") as f:
            ctext = f.read()
        lines = ctext.split("\n")
        if lines and lines[-1] == "":
            lines.pop()
        hdr = lines[0].split() if lines else []
        ok_hdr = len(hdr) == 2 and hdr[0] == "112" and hdr[1].isdigit() and int(hdr[1]) > 0
        centers_n = int(hdr[1]) if ok_hdr else None
        body = lines[1:]
        bad = 0
        first = None
        for i, line in enumerate(body):
            parts = line.split(" ")
            if len(parts) != 11 or parts[-1] != "":
                bad += 1
                first = first or ("line %d: %r is not ten space-terminated integers" % (i + 2, line[:48]))
                continue
            try:
                v = [int(x) for x in parts[:10]]
            except ValueError:
                bad += 1
                first = first or ("line %d: non-integer field" % (i + 2))
                continue
            if any(not (0 <= x < 112) for x in v[:5]) or any(not (0 <= x < 112) for x in v[6:]) \
                    or not (0 <= v[5] < 5):
                bad += 1
                first = first or ("line %d: bin outside [0,112) or s outside [0,5): %r" % (i + 2, v))
        report.check("centers.format", ok_hdr and bad == 0 and centers_n == len(body),
                     "header=%r, %d centre lines, %d malformed%s"
                     % (" ".join(hdr), len(body), bad, ("; " + first) if first else ""), "A")
        cov = res_line("covrun", "N112")
        if cov is None:
            report.check("centers.counter", False, "results/covrun.txt has no N112 line", "B")
        else:
            toks = {}
            for tok in cov.split():
                for key in ("checked", "centers", "dual"):
                    if tok.startswith(key):
                        toks[key] = tok[len(key):]
            report.check("centers.counter",
                         toks.get("centers") == str(centers_n) and toks.get("dual") == "2"
                         and toks.get("checked", "").isdigit(),
                         "results/covrun.txt %r vs header count %r" % (cov, centers_n), "B")

    stage = {}
    for name, c in cmds.items():
        stage.setdefault(c.get("stage"), []).append(name)
    for k in stage:
        stage[k].sort(key=lambda s: s.encode())

    report.check("cov.present", len(stage.get("cov", [])) == 1,
                 "stage 'cov' commands: %r" % (stage.get("cov"),), "B")

    # -------------------------------------------------------------------- stage A
    a_names = stage.get("A", [])
    a_parts = []
    a_records = 0
    for name in a_names:
        av = argv(name)
        if len(av) != 6:
            report.check("A.argv[%s]" % name, False, "argv=%r, expected 6 arguments" % (av,), "B")
            continue
        try:
            part, parts = int(av[2]), int(av[3])
        except ValueError:
            report.check("A.argv[%s]" % name, False, "part/parts not numeric: %r" % (av,), "B")
            continue
        a_parts.append((part, parts))
        out, badf = av[4], av[5]
        n = count(out)
        if n is not None:
            a_records += n
        line = res_line(name, "total ")
        g = f = None
        for tok in (line.split() if line else []):
            if tok.startswith("global"):
                g = tok[len("global"):]
            elif tok.startswith("failedBalls"):
                f = tok[len("failedBalls"):]
        report.check("A.count[%s]" % name, n is not None and g == str(n),
                     "results/%s.txt global=%r vs %r records in %s" % (name, g, n, out), "B")
        report.check("A.failedBalls[%s]" % name, f == "0" and rc(name) == 0,
                     "failedBalls=%r, returncode=%r" % (f, rc(name)), "B")
        bp = os.path.join(data, badf)
        sz = os.path.getsize(bp) if os.path.isfile(bp) else None
        report.check("A.badfile[%s]" % name, sz == 0,
                     "%s is %r bytes; spec 3.3: zero-length, written only when nothing fails"
                     % (badf, sz), "A")
        if out in parsed:
            check_one_file(report, out, recs(out), MAXRADIUS, "A.rec[" + name + "]")
    report.check("A.partition",
                 len(a_parts) == 4 and sorted(p for p, _q in a_parts) == [0, 1, 2, 3]
                 and all(q == 4 for _p, q in a_parts),
                 "A (part,parts) pairs %r; the shards must cover 0..3 mod 4 exactly once"
                 % (a_parts,), "B")

    # -------------------------------------------------------------------- stage B
    def brun_info(name):
        av = argv(name)
        if len(av) < 7:
            return None, "argv=%r, expected >= 7 arguments" % (av,)
        try:
            target = float(av[1])
            float(av[2])
        except ValueError:
            return None, "target/width not numeric: %r" % (av,)
        return {"target": target, "out": av[3], "bad": av[4], "prefix": av[5], "inputs": av[6:]}, None

    b_info = {}
    for tag, want in (("Bmid", "Bmid"), ("Bfine", "Bfine"), ("C.fallback", "C.fallback")):
        names = stage.get(want, [])
        if len(names) != 1:
            report.check("B.present[%s]" % tag, False, "stage %r has commands %r" % (want, names), "B")
            continue
        info, err = brun_info(names[0])
        if info is None:
            report.check("B.argv[%s]" % tag, False, err, "B")
            continue
        b_info[tag] = (names[0], info)

    def b_counts(tag, want_parents):
        if tag not in b_info:
            return
        name, info = b_info[tag]
        line = res_line(name, "result ")
        out_n, bad_n = count(info["out"]), count(info["bad"])
        out_log = bad_log = parents = None
        if line:
            tok = line.split()
            if len(tok) > 3:
                try:
                    out_log, bad_log = int(tok[1]), int(tok[3])
                except ValueError:
                    pass
            for t in tok:
                if t.startswith("parent"):
                    parents = t[len("parent"):]
        report.check("B.outputs[%s]" % tag, out_log is not None and out_log == out_n,
                     "results/%s.txt %r vs %r records in %s" % (name, line, out_n, info["out"]), "B")
        report.check("B.bad[%s]" % tag, bad_n == 0 and rc(name) == 0 and bad_log == 0,
                     "%s count=%r, returncode=%r, log bad=%r; brun returns 1 iff bad is non-empty"
                     % (info["bad"], bad_n, rc(name), bad_log), "B")
        if want_parents is not None:
            report.check("B.parents[%s]" % tag, parents == str(want_parents),
                         "results/%s.txt parent=%r, computed from the inputs %d"
                         % (name, parents, want_parents), "B")

    b_counts("Bmid", a_records if a_names else None)
    if "Bmid" in b_info:
        name, info = b_info["Bmid"]
        coarse_order = [argv(n)[4] for n in a_names if len(argv(n)) == 6]
        report.check("B.mid_inputs", info["inputs"] == coarse_order,
                     "Bmid inputs %r, A outputs %r" % (info["inputs"], coarse_order), "B")
        if info["out"] in parsed:
            check_one_file(report, info["out"], recs(info["out"]), info["target"], "B.rec[Bmid]")

    mid_n = count(b_info["Bmid"][1]["out"]) if "Bmid" in b_info else None
    b_counts("Bfine", mid_n)
    if "Bfine" in b_info:
        name, info = b_info["Bfine"]
        report.check("B.fine_inputs",
                     "Bmid" in b_info and info["inputs"] == [b_info["Bmid"][1]["out"]],
                     "Bfine inputs %r, mid output %r"
                     % (info["inputs"], b_info["Bmid"][1]["out"] if "Bmid" in b_info else None), "B")
        if info["out"] in parsed:
            check_one_file(report, info["out"], recs(info["out"]), info["target"], "B.rec[Bfine]")
        done_rel = info["prefix"] + "done.txt"
        done_full = os.path.join(data, done_rel)
        if not os.path.isfile(done_full):
            report.check("B.batches[done]", False,
                         "%s absent although batching was on (prefix=%r)" % (done_rel, info["prefix"]), "A")
        else:
            with open(done_full, "r", errors="replace") as f:
                dtxt = f.read()
            toks = dtxt.split()
            ok_done = len(toks) == 2 and all(t.isdigit() for t in toks) and dtxt.endswith("\n")
            nb = int(toks[0]) if ok_done else 0
            ne = int(toks[1]) if ok_done else None
            batch_names = [info["prefix"] + str(i) + ".bin" for i in range(nb)]
            have = [b for b in batch_names if b in parsed]
            report.check("B.batches[files]", ok_done and nb > 0 and len(have) == len(batch_names),
                         "%s = %r; %d/%d batch files present"
                         % (done_rel, dtxt.strip(), len(have), len(batch_names)), "A")
            if info["out"] in parsed and len(have) == len(batch_names) and batch_names:
                # emit() rewrites every batched record's radius to `target`, so the
                # partition is over the records minus their final 8-byte radius slot.
                payload = [r[4][:-8] for b in batch_names for r in recs(b)]
                want = [r[4][:-8] for r in recs(info["out"])]
                report.check("B.batches[partition]", payload == want,
                             "%d batch records against the %d records of %s: %s"
                             % (len(payload), len(want), info["out"],
                                "identical outside the radius slot" if payload == want else "DIFFERENT"), "B")

                sizes = [count(b) for b in batch_names]
                report.check("B.batches[size]",
                             all(s == 256 for s in sizes[:-1]) and 1 <= sizes[-1] <= 256,
                             "batch sizes: %d x 256, last %d" % (len(sizes) - 1, sizes[-1]), "A")
                report.check("B.batches[emitted]", ne == sum(sizes),
                             "%s emitted=%r, batches hold %d records" % (done_rel, ne, sum(sizes)), "B")
            # per-record invariants of every batch, with radius forced to `target`
            for i, b in enumerate(batch_names):
                if b in parsed:
                    check_one_file(report, b, recs(b), info["target"], "B.rec[batch%d]" % i,
                                   expect_radius=info["target"])

    # -------------------------------------------------------------------- stage C
    fail_files = []
    for name in stage.get("C.initial", []):
        av = argv(name)
        if len(av) < 12:
            report.check("C.argv[%s]" % name, False, "argv=%r, expected >= 12 arguments" % (av,), "B")
            continue
        try:
            part, parts = int(av[8]), int(av[9])
        except ValueError:
            report.check("C.argv[%s]" % name, False, "part/parts not numeric: %r" % (av,), "B")
            continue
        out, inputs = av[10], av[11:]
        bad_n = count(out)
        line = res_line(name, "result ")
        m = re.search(r"done(\d+) bad(\d+)", line or "")
        done, bad_log = (int(m.group(1)), int(m.group(2))) if m else (None, None)
        in_n = count(inputs[0]) if len(inputs) == 1 else None
        report.check("C.index[%s]" % name,
                     done is not None and in_n is not None and done == in_n and part == 0 and parts == 1,
                     "results/%s.txt done=%r, input %r holds %r records, part/parts=%d/%d"
                     % (name, done, inputs[0] if inputs else None, in_n, part, parts), "B")
        report.check("C.bad[%s]" % name,
                     bad_n is not None and bad_log == bad_n and rc(name) == (1 if (bad_n or 0) else 0),
                     "%s holds %r records, log bad=%r, returncode=%r"
                     % (out, bad_n, bad_log, rc(name)), "B")
        if bad_n:
            fail_files.append((name, out, inputs[0] if inputs else None, bad_n))

    fine_target = b_info["Bfine"][1]["target"] if "Bfine" in b_info else None
    for name, out, inp, bad_n in fail_files:
        if out not in parsed or inp not in parsed:
            report.check("C.subseq[%s]" % name, False, "%r or %r did not parse" % (out, inp), "B")
            continue
        want, have = recs(out), recs(inp)
        j = 0
        for r in have:
            if j < len(want) and r[4] == want[j][4]:
                j += 1
        report.check("C.subseq[%s]" % name, j == len(want),
                     "%d unresolved records of %s occur in order in %s (%d matched)"
                     % (len(want), out, inp, j), "B")
        check_one_file(report, out, want, MAXRADIUS, "C.rec[" + name + "]", expect_radius=fine_target)

    if "C.fallback" in b_info:
        fbname, fbinfo = b_info["C.fallback"]
        nonempty = ascii_sorted([rel for _n, rel, _i, bn in fail_files if bn])
        report.check("C.fallback_inputs",
                     fbinfo["inputs"] == nonempty and len(fbinfo["inputs"]) == len(fail_files),
                     "C.%s inputs %r; non-empty initial C failure files in ASCII order %r"
                     % (fbname, fbinfo["inputs"], nonempty), "B")
        b_counts("C.fallback", sum(bn for _n, _o, _i, bn in fail_files))
        if fbinfo["out"] in parsed:
            check_one_file(report, fbinfo["out"], recs(fbinfo["out"]), fbinfo["target"], "B.rec[C.fallback]")

    fb_out = b_info["C.fallback"][1]["out"] if "C.fallback" in b_info else None
    fb_n = count(fb_out) if fb_out else None
    finals = []
    for name in stage.get("C.final", []):
        av = argv(name)
        if len(av) < 12:
            report.check("C.argv[%s]" % name, False, "argv=%r, expected >= 12 arguments" % (av,), "B")
            continue
        try:
            part, parts = int(av[8]), int(av[9])
        except ValueError:
            report.check("C.argv[%s]" % name, False, "part/parts not numeric: %r" % (av,), "B")
            continue
        out = av[10]
        finals.append((part, parts, out, name))
        bad_n = count(out)
        line = res_line(name, "result ")
        m = re.search(r"done(\d+) bad(\d+)", line or "")
        done, bad_log = (int(m.group(1)), int(m.group(2))) if m else (None, None)
        report.check("C.final_bad[%s]" % name, bad_n == 0 and bad_log == 0 and rc(name) == 0,
                     "%s holds %r records, log bad=%r, returncode=%r; a final unresolved record "
                     "is not a negative certificate" % (out, bad_n, bad_log, rc(name)), "B")
        full = os.path.join(data, out)
        sz = os.path.getsize(full) if os.path.isfile(full) else None
        report.check("C.final_bytes[%s]" % name, sz == 8,
                     "%s is %r bytes; spec 3.3: an empty record file is the 8-byte count zero "
                     "(only bad0..3.txt are zero-length)" % (out, sz), "A")
        report.check("C.final_inputs[%s]" % name,
                     fb_out is not None and av[11:] == [fb_out] and parts == 4 and 0 <= part < 4,
                     "inputs=%r part/parts=%d/%d, fallback output %r"
                     % (av[11:], part, parts, fb_out), "B")
        if fb_n is not None and parts == 4 and done is not None:
            want_done = fb_n // 4 + (1 if part < fb_n % 4 else 0)
            report.check("C.final_coverage[%s]" % name, done == want_done,
                         "results/%s.txt done=%d; %d records of %s have index %% 4 == %d, so %d are processed"
                         % (name, done, fb_n, fb_out, part, want_done), "B")
    report.check("C.final_partition",
                 len(finals) == 4 and sorted(f[0] for f in finals) == [0, 1, 2, 3]
                 and all(f[1] == 4 for f in finals),
                 "C.final (part,parts) %r; the four parts must cover 0..3 mod 4 exactly once"
                 % ([(f[3], f[0], f[1]) for f in finals],), "B")
    if fb_n is not None and finals:
        tot = 0
        for _p, _q, _o, name in finals:
            m = re.search(r"done(\d+)", res_line(name, "result ") or "")
            if m:
                tot += int(m.group(1))
        report.check("C.final_total", tot == fb_n,
                     "final done counters sum to %d; the fallback output holds %d records" % (tot, fb_n), "B")

    return emit(report, args, {"centers": centers_n,
                               "record_files": len(parsed),
                               "records": sum(len(v[1]) for v in parsed.values())})


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
