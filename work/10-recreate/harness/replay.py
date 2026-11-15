#!/usr/bin/env python3
"""replay.py -- replay driver for the recorded MUB dimension-six run.

The published saved-run records 100 commands (`execution/commands.json`: argv, declared
inputs, declared outputs, return code, stage) over 249878 centres and ~82 MB of
artefacts (`execution/data/`).  This driver replays them and compares the result to
the recorded artefacts byte for byte.

Modes
  selftest   Replay the recorded artefacts against themselves: each command "produces"
             its declared outputs by copying the recorded file, then the *same*
             comparison code used in a real replay compares them to the pinned
             manifest.  Plus corpus checks C1..C9 over the recorded set.  A PASS here
             means the driver, the manifest and the recorded bookkeeping are coherent,
             so a later mismatch is the implementation's and not the harness's.
  replay     Execute the recorded argv against a build of the four programs
             (`--bin DIR` containing arun, brun, crun, covrun), chaining each command's
             own outputs into the next command's inputs, and compare.
  control    Seeded-corruption control: mutate a copy of the recorded set and require
             the checks to FAIL.  A harness that cannot fail has not checked anything.

Outputs (fixed schema, one file per command, see SCHEMA and docs below):
  logs/replay/R001.json .. R100.json   per-command record, index = commands.json key order
  logs/replay/summary.json             run summary + corpus-check table
  logs/replay-<UTCSTAMP>.json          copy of the summary for the gate ledger

Schema `mub-replay/1` per-command file:
  schema, mode, index, command, stage, argv, inputs, outputs,
  input_sources{name: "replayed"|"recorded"}, rc_expected, rc_got,
  artefacts[{path, bytes_expected, bytes_got, sha256_expected, sha256_got,
             byte_identical, declared}], checks{name: {status, detail}},
  elapsed_ms, verdict  ("PASS" | "FAIL")

Exit status: 0 all checks PASS, 1 anything else, 2 setup error (no manifest, no cache).

Nothing here decides mathematics; it decides whether the recorded run reproduces.
"""
import argparse
import datetime
import filecmp
import glob
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import time

SCHEMA = "mub-replay/1"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MANIFEST = os.path.join(HERE, "saved-run.manifest.json")
DEFAULT_CACHE = os.path.join(REPO_ROOT, "work", "10-recreate", "crew", "m3", "saved-run")
DEFAULT_LOGS = os.path.join(REPO_ROOT, "work", "10-recreate", "logs")
DATA = "execution/data"
MAXK = 10
# record layout, spec/interfaces.md 3.2: uint64 count, then per record
# int32 k, double p[36], double T[k][36], 8 doubles.  4 + 288 + 288k + 64 bytes.
REC_FIXED = 4 + 288 + 64
STAGE_RANK = {"cov": 0, "A": 1, "Bmid": 2, "Bfine": 3, "C.initial": 4,
              "C.fallback": 5, "C.final": 6}
BINARIES = ("arun", "brun", "crun", "covrun")


# ---------------------------------------------------------------- small helpers
def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                return h.hexdigest()
            h.update(b)


def utcstamp():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def result(status, detail=""):
    return {"status": status, "detail": detail}


class Setup(Exception):
    pass


def load_manifest(path=MANIFEST):
    if not os.path.exists(path):
        raise Setup("no manifest at %s (run fetch_saved_run.py first)" % path)
    return json.load(open(path))


def man_path(cache, rel):
    """Recorded file name (relative to execution/data) -> path in the cache."""
    return os.path.join(cache, DATA, rel)


def load_commands(cache):
    p = os.path.join(cache, "execution", "commands.json")
    if not os.path.exists(p):
        raise Setup("no commands.json at %s" % p)
    return json.load(open(p))["children"]


def recorded_text(cache, name):
    p = os.path.join(cache, "execution", "results", name + ".txt")
    return open(p, "r", errors="replace").read() if os.path.exists(p) else None


def walk_records(path, bounds=False):
    """Parse a record file exactly: count, every k, exact end of file.

    Returns (count, [k...], [radius...], [C...]).  Raises ValueError on any
    structural violation (short file, k out of range, trailing bytes).
    """
    with open(path, "rb") as f:
        data = f.read()
    if len(data) < 8:
        raise ValueError("%s: %d bytes, shorter than the 8-byte count" % (path, len(data)))
    n = struct.unpack_from("<Q", data, 0)[0]
    if n > 2000000:
        raise ValueError("%s: count %d above the 2e6 read cap" % (path, n))
    off = 8
    ks, radii, cs = [], [], []
    for i in range(n):
        if off + 4 > len(data):
            raise ValueError("%s: record %d starts past end of file" % (path, i))
        k = struct.unpack_from("<i", data, off)[0]
        if not 0 <= k <= MAXK:
            raise ValueError("%s: record %d has k=%d outside [0,%d]" % (path, i, k, MAXK))
        end = off + REC_FIXED + 288 * k
        if end > len(data):
            raise ValueError("%s: record %d runs past end of file" % (path, i))
        if bounds:
            eight = struct.unpack_from("<8d", data, end - 64)
            cs.append(eight[0])
            radii.append(eight[7])
        ks.append(k)
        off = end
    if off != len(data):
        raise ValueError("%s: %d trailing bytes after %d records"
                         % (path, len(data) - off, n))
    return n, ks, radii, cs


# ---------------------------------------------------------------- command model
def declared(cmd):
    return cmd.get("outputs") or []


def implied_outputs(name, cmd, files):
    """Artefacts a command produces that commands.json does not declare.

    The one case in the recorded run is Bfine: `brun .016 .005 fine.bin finebad.bin
    batches/f mid.bin` writes batches/f0.bin .. f87.bin and batches/fdone.txt, which
    are inputs of the 88 C.batch commands and are 89 of the 107 recorded artefact
    names, but `outputs` lists only fine.bin and finebad.bin.  A driver that trusts
    `outputs` alone never compares the most important product of the run.
    """
    argv = cmd["argv"]
    base = os.path.basename(argv[0])
    out = []
    if base == "brun" and len(argv) > 5 and argv[5] != "-":
        prefix = argv[5]
        pat = re.compile(r"^" + re.escape(prefix) + r"\d+\.bin$")
        out = [p for p in files if pat.match(p)]
        done = prefix + "done.txt"
        if done in files:
            out.append(done)
    return sorted(out)


def all_outputs(name, cmd, files):
    return sorted(set(declared(cmd)) | set(implied_outputs(name, cmd, files)))


def order_commands(cmds, files):
    """Dependency order: a command runs after the commands that produce its inputs."""
    producer = {}
    for name, cmd in cmds.items():
        for p in all_outputs(name, cmd, files):
            producer.setdefault(p, []).append(name)
    placed, order = set(), []
    pending = list(cmds)
    while pending:
        progressed = False
        for name in list(pending):
            need = set()
            for i in cmds[name].get("inputs") or []:
                for p in producer.get(i, []):
                    if p != name:
                        need.add(p)
            if need <= placed:
                order.append(name)
                placed.add(name)
                pending.remove(name)
                progressed = True
        if not progressed:
            raise Setup("dependency cycle among: %s" % ", ".join(sorted(pending)))
    return order


# ---------------------------------------------------------------- corpus checks
def corpus_checks(cache, man, cmds):
    """C1..C9 on the recorded set.  Each returns name -> {status, detail}."""
    files = man["files"]
    data_names = sorted(p[len(DATA) + 1:] for p in files if p.startswith(DATA + "/"))
    data_set = set(data_names)
    C = {}

    # C1 manifest vs on-disk cache (all 308 published blobs incl. sources and results)
    bad = []
    for p, meta in files.items():
        fp = os.path.join(cache, p)
        if not os.path.exists(fp):
            bad.append(p + ":missing")
        elif os.path.getsize(fp) != meta["bytes"]:
            bad.append(p + ":size")
        elif sha256_file(fp) != meta["sha256"]:
            bad.append(p + ":sha256")
    C["C1_manifest_matches_published_bytes"] = result(
        "PASS" if not bad else "FAIL",
        "%d files, %d bytes, tree %s" % (len(files), sum(m["bytes"] for m in files.values()),
                                         man["source"]["tree_sha1"])
        if not bad else "%d mismatched: %s" % (len(bad), bad[:8]))

    # C2 commands.json facts: 100 commands, 85 zero / 15 one, all completed
    rcs = [c["returncode"] for c in cmds.values()]
    n0, n1 = rcs.count(0), rcs.count(1)
    ok = (len(cmds) == 100 and n0 == 85 and n1 == 15 and set(rcs) == {0, 1}
          and all(c.get("completed") for c in cmds.values()))
    C["C2_command_facts"] = result(
        "PASS" if ok else "FAIL",
        "%d commands, rc0=%d rc1=%d, all completed=%s"
        % (len(cmds), n0, n1, all(c.get("completed") for c in cmds.values())))

    # C3 coverage: declared inputs/outputs are recorded files; every recorded
    # *.bin / *.txt in data/ is produced by some command except the A bad*.txt
    # (zero-length, declared) and centers.txt (covrun's output).
    missing, declared_out = [], set()
    for name, cmd in cmds.items():
        for p in (cmd.get("inputs") or []) + declared(cmd):
            if p not in data_set:
                missing.append("%s:%s" % (name, p))
            if p in declared(cmd):
                declared_out.add(p)
        for p in all_outputs(name, cmd, files=data_set):
            declared_out.add(p)
    unproduced = sorted(data_set - declared_out)
    C["C3_artefact_coverage"] = result(
        "PASS" if not missing and not unproduced else "FAIL",
        "declared names all recorded; unproduced recorded names: %s"
        % (unproduced if unproduced else "none") if not missing else
        "declared but not recorded: %s" % missing[:8])

    # C4 record structure of every recorded binary: exact parse, k in [0,10],
    # cheap numeric bounds on radius and C.
    counts, problems = {}, []
    for rel in data_names:
        if not rel.endswith(".bin"):
            continue
        try:
            n, ks, radii, cs = walk_records(man_path(cache, rel), bounds=True)
            counts[rel] = n
            if any((not 0.0 <= r <= 0.126) for r in radii):
                problems.append(rel + ":radius out of [0,.126]")
            if any((not 0.0 <= c < 20.0) for c in cs):
                problems.append(rel + ":C out of [0,20)")
        except ValueError as e:
            problems.append(str(e).replace(cache + "/", ""))
    C["C4_record_structure"] = result(
        "PASS" if not problems else "FAIL",
        "%d record files parse exactly, k in [0,%d], radius/C bounds hold"
        % (len(counts), MAXK) if not problems else "; ".join(problems[:6]))

    # C5 rc polarity and the 15 unresolved batches
    initial = {n: c for n, c in cmds.items() if c["stage"] == "C.initial"}
    fallback = [n for n, c in cmds.items() if c["stage"] == "C.fallback"]
    perr = []
    for n, c in cmds.items():
        for p in declared(c):
            if not p.endswith(".bin"):
                continue
            k = p.rsplit("/", 1)[-1]
            if k.startswith("bad") and c["stage"].startswith("C."):
                cnt = counts.get(p, -1)
                want = 1 if c["returncode"] == 1 else 0
                if (cnt > 0) != (want == 1):
                    perr.append("%s rc=%d but %s count=%d" % (n, c["returncode"], p, cnt))
    rc1 = sorted(n for n, c in initial.items() if c["returncode"] == 1)
    C["C5a_rc_polarity_c_bad_files"] = result(
        "PASS" if not perr else "FAIL",
        "%d C commands: rc=1 iff the bad file is non-empty" % sum(
            1 for c in cmds.values() if c["stage"].startswith("C."))
        if not perr else "; ".join(perr[:6]))

    # C5b/c: exactly 15, and the fallback input list is exactly those 15, in ASCII order
    fb = []
    for n in fallback:
        fb = list(cmds[n].get("inputs") or [])
    unresolved = sorted({p for n in rc1 for p in declared(cmds[n])})
    same = set(unresolved) == set(fb)
    ascii_ok = fb == sorted(fb)
    order_ok = fb == [p for p in fb if p in set(unresolved)]
    C["C5b_15_unresolved_are_the_fallback_inputs"] = result(
        "PASS" if (len(rc1) == 15 and same and len(fb) == 15) else "FAIL",
        "%d C.initial rc=1 commands, %d fallback inputs, sets equal=%s, ascii-sorted=%s"
        % (len(rc1), len(fb), same, ascii_ok))
    C["C5c_fallback_input_order"] = result(
        "PASS" if ascii_ok and order_ok else "FAIL",
        "argv order %s" % ("= ASCII filename order" if ascii_ok else "!= ASCII filename order"))
    nonempty = {p: counts.get(p, -1) for p in fb}
    C["C5d_fallback_inputs_nonempty"] = result(
        "PASS" if all(v > 0 for v in nonempty.values()) else "FAIL",
        "counts %s" % sorted(nonempty.values()))

    # C6 the four final bad files are 8-byte count-zero records
    fin = []
    for n, c in cmds.items():
        if c["stage"] == "C.final":
            if c["returncode"] != 0:
                fin.append("%s rc=%d" % (n, c["returncode"]))
            for p in declared(c):
                fp = man_path(cache, p)
                with open(fp, "rb") as f:
                    b = f.read()
                if len(b) != 8 or struct.unpack("<Q", b)[0] != 0:
                    fin.append("%s: %s is %d bytes, count %s"
                               % (n, p, len(b),
                                  struct.unpack("<Q", b + b"\0" * (8 - len(b)))[0]))
    C["C6_final_bad_files_count_zero"] = result(
        "PASS" if not fin else "FAIL",
        "4 final C commands, rc 0, each output 8 bytes with uint64 count 0"
        if not fin else "; ".join(fin[:6]))

    # C7 arun bad*.txt are zero-length (spec 3.3: the only zero-length files)
    ar_bad = sorted(p for p in data_set if re.match(r"^bad\d+\.txt$", p))
    zero = {p: os.path.getsize(man_path(cache, p)) for p in ar_bad}
    C["C7_arun_bad_txt_zero_length"] = result(
        "PASS" if zero and all(v == 0 for v in zero.values()) else "FAIL",
        "%d files, sizes %s" % (len(zero), sorted(set(zero.values()))))

    # C8 the fine -> batch partition
    b8 = []
    fbats = sorted((p for p in data_set if re.match(r"^batches/f\d+\.bin$", p)),
                   key=lambda p: int(re.search(r"(\d+)\.bin$", p).group(1)))
    idx = [int(re.search(r"(\d+)\.bin$", p).group(1)) for p in fbats]
    if idx != list(range(len(fbats))):
        b8.append("batch numbering is not 0..%d" % (len(fbats) - 1))
    sizes = [counts.get(p, -1) for p in fbats]
    if any(s != 256 for s in sizes[:-1]):
        b8.append("a non-final batch is not 256 records: %s"
                  % [p for p, s in zip(fbats, sizes) if s != 256][:4])
    if sizes and not 0 < sizes[-1] <= 256:
        b8.append("final batch has %d records" % sizes[-1])
    done = os.path.join(cache, DATA, "batches/fdone.txt")
    txt = open(done).read().split() if os.path.exists(done) else []
    fbl = counts.get("fine.bin", -1)
    if sum(sizes) != fbl:
        b8.append("batches sum %d != fine.bin count %d" % (sum(sizes), fbl))
    if txt != [str(len(fbats)), str(sum(sizes))]:
        b8.append("fdone.txt says %s, batches give %s"
                  % (txt, [len(fbats), sum(sizes)]))
    C["C8_fine_to_batch_partition"] = result(
        "PASS" if not b8 else "FAIL",
        "%d batches, sizes %d..%d, sum %d = fine.bin count, fdone.txt %s"
        % (len(fbats), sizes[0] if sizes else -1, sizes[-1] if sizes else -1,
           sum(sizes), txt) if not b8 else "; ".join(b8))

    # C9 cross-command arithmetic against the recorded stdout counters
    c9 = []
    out = {}
    for n, c in cmds.items():
        t = recorded_text(cache, n)
        out[n] = t or ""
        if t is None:
            c9.append("%s: no recorded stdout" % n)
    def tok(name, key):
        m = re.search(key + r"\s*(\d+)", out[name].splitlines()[-1] if out[name] else "")
        return int(m.group(1)) if m else None
    a = [tok(n, "global") for n in ("A0", "A1", "A2", "A3")]
    coarse = sum(counts.get("coarse%d.bin" % i, -1) for i in range(4))
    if None in a or sum(a) != coarse:
        c9.append("A global counts %s vs coarse sum %d" % (a, coarse))
    if tok("Bmid", "parent") != coarse:
        c9.append("Bmid parent %s vs coarse sum %d" % (tok("Bmid", "parent"), coarse))
    if tok("Bmid", "result") != counts.get("mid.bin"):
        c9.append("Bmid result %s vs mid.bin count %d"
                  % (tok("Bmid", "result"), counts.get("mid.bin")))
    if tok("Bfine", "parent") != counts.get("mid.bin"):
        c9.append("Bfine parent %s vs mid.bin count %d"
                  % (tok("Bfine", "parent"), counts.get("mid.bin")))
    if tok("Bfine", "result") != counts.get("fine.bin"):
        c9.append("Bfine result %s vs fine.bin count %d"
                  % (tok("Bfine", "result"), counts.get("fine.bin")))
    fbn = "C.Bfallback"
    tot_bad = sum(counts.get(p, 0) for p in fb)
    if tok(fbn, "parent") != tot_bad:
        c9.append("fallback parent %s vs sum of 15 bad counts %d"
                  % (tok(fbn, "parent"), tot_bad))
    if tok(fbn, "result") != counts.get("fb1.bin"):
        c9.append("fallback result %s vs fb1.bin count %d"
                  % (tok(fbn, "result"), counts.get("fb1.bin")))
    for n, c in cmds.items():
        if c["stage"] == "C.initial":
            m = re.search(r"result done(\d+) bad(\d+)", out[n])
            if not m:
                c9.append("%s: no 'result done' line" % n)
                continue
            d, b = int(m.group(1)), int(m.group(2))
            if d != len(c["inputs"]) or True:
                pass
            if d != counts.get(c["inputs"][0], -1):
                c9.append("%s: done %d vs input count %d (modulo 1 part)"
                          % (n, d, counts.get(c["inputs"][0], -1)))
            if b != counts.get(declared(c)[0], -1):
                c9.append("%s: bad %d vs bad file count %d"
                          % (n, b, counts.get(declared(c)[0], -1)))
        if c["stage"] == "C.final":
            m = re.search(r"result done(\d+) bad(\d+)", out[n])
            if not m:
                c9.append("%s: no 'result done' line" % n)
                continue
            part, parts = int(c["argv"][8]), int(c["argv"][9])
            nfb = counts.get("fb1.bin", -1)
            want = len(range(part, nfb, parts))
            if int(m.group(1)) != want:
                c9.append("%s: done %s vs %d records with i%%%d==%d of fb1.bin"
                          % (n, m.group(1), want, parts, part))
            if int(m.group(2)) != 0:
                c9.append("%s: bad %s" % (n, m.group(2)))
    C["C9_cross_command_counts"] = result(
        "PASS" if not c9 else "FAIL",
        "coarse %d = 4x arun global; mid %d; fine %d; fallback parents %d -> %d records; "
        "C.batch done=input count, bad=bad-file count; final parts cover fb1.bin mod 4"
        % (coarse, counts.get("mid.bin", -1), counts.get("fine.bin", -1), tot_bad,
           counts.get("fb1.bin", -1)) if not c9 else "; ".join(c9[:8]))

    # C10 argv agrees with the declared inputs/outputs
    # commands.json stores the same file names twice: once in `argv` (what the driver
    # executes) and once in `inputs`/`outputs` (what a checker trusts).  They can drift
    # apart silently, so the driver checks that they describe the same command.
    c10 = []
    for n, c in cmds.items():
        argv = c["argv"][1:]
        def _is_file(a):
            return a in data_set or (a + "0.bin") in data_set
        fargs = [a for a in argv if _is_file(a)]
        decl_in = list(c.get("inputs") or [])
        decl_out = list(declared(c))
        prefixes = [a for a in fargs if (a + "0.bin") in data_set]
        inorder = [a for a in fargs if a in set(decl_in)]
        if inorder != decl_in:
            c10.append("%s: argv order %s != inputs %s" % (n, inorder[:4], decl_in[:4]))
        for o in decl_out:
            if o not in fargs and not any(o.startswith(p2) for p2 in prefixes):
                c10.append("%s: declared output %s absent from argv" % (n, o))
        known = set(decl_in) | set(decl_out) | set(prefixes)
        for a in fargs:
            if a not in known and not any(a.startswith(p2) for p2 in prefixes):
                c10.append("%s: argv names %s with no declared role" % (n, a))
    C["C10_argv_matches_declared"] = result(
        "PASS" if not c10 else "FAIL",
        "file arguments in argv equal the declared inputs in order, every declared "
        "output is named (Bfine's batch prefix included), no unexplained file argument"
        if not c10 else "; ".join(c10[:8]))

    return C



# ---------------------------------------------------------------- one command
def prepare(run, cache, name, cmd, mode, bindir, produced=()):
    """Lay out the working tree for one command; return {input: source}.

    An input is "replayed" when a command earlier in this run wrote it, and "recorded"
    when it is a symlink into the published saved-run.  The log says which, because a
    partial replay (--only) leans on recorded inputs and is a weaker test."""
    os.makedirs(run, exist_ok=True)
    srcs = {}
    for p in cmd.get("inputs") or []:
        dest = os.path.join(run, p)
        if p in produced:
            srcs[p] = "replayed"
            continue
        if os.path.exists(dest):
            srcs[p] = "recorded"
            continue
        os.makedirs(os.path.dirname(dest) or run, exist_ok=True)
        os.symlink(man_path(cache, p), dest)
        srcs[p] = "recorded"
    if mode == "real":
        bd = os.path.join(run, "build")
        os.makedirs(bd, exist_ok=True)
        for b in BINARIES:
            link = os.path.join(bd, b)
            if not os.path.exists(link):
                s = os.path.join(bindir, b)
                if not os.path.exists(s):
                    raise Setup("missing binary %s" % s)
                os.symlink(s, link)
    return srcs


def produce(run, cache, name, cmd, mode, bindir, files, timeout):
    """Run the command (or self-copy its recorded outputs).  Returns
    (rc_got, stdout, stderr, elapsed_ms, error)."""
    outs = all_outputs(name, cmd, files)
    for p in outs:
        d = os.path.dirname(os.path.join(run, p))
        os.makedirs(d or run, exist_ok=True)
        fp = os.path.join(run, p)
        if os.path.lexists(fp):
            os.unlink(fp)
    t0 = time.time()
    if mode == "self":
        for p in outs:
            shutil.copyfile(man_path(cache, p), os.path.join(run, p))
        txt = recorded_text(cache, name)
        return cmd["returncode"], txt, "", 0.0, None
    try:
        pr = subprocess.run(cmd["argv"], cwd=run, capture_output=True, timeout=timeout)
        return (pr.returncode, pr.stdout.decode("utf-8", "replace"),
                pr.stderr.decode("utf-8", "replace"), (time.time() - t0) * 1000.0, None)
    except subprocess.TimeoutExpired:
        return None, "", "", (time.time() - t0) * 1000.0, "timeout after %ss" % timeout
    except OSError as e:
        return None, "", "", (time.time() - t0) * 1000.0, "exec failed: %s" % e


def judge(run, cache, name, cmd, mode, outs, rc_got, stdout, stderr, man):
    checks, arts = {}, []
    for p in outs:
        exp = man_path(cache, p)
        got = os.path.join(run, p)
        is_decl = p in declared(cmd)
        e = {"path": p, "declared": is_decl}
        e["bytes_expected"] = os.path.getsize(exp)
        e["sha256_expected"] = man["files"]["%s/%s" % (DATA, p)]["sha256"]
        if os.path.exists(got):
            e["bytes_got"] = os.path.getsize(got)
            e["sha256_got"] = sha256_file(got)
            e["byte_identical"] = filecmp.cmp(exp, got, shallow=False)
        else:
            e["bytes_got"] = None
            e["sha256_got"] = None
            e["byte_identical"] = False
        arts.append(e)
    missing = [a["path"] for a in arts if a["bytes_got"] is None]
    differ = [a["path"] for a in arts if a["bytes_got"] is not None and not a["byte_identical"]]
    checks["artefacts_present"] = result("PASS" if not missing else "FAIL",
                                         "all %d produced" % len(arts) if not missing
                                         else "missing: %s" % missing[:8])
    checks["artefacts_byte_identical"] = result(
        "PASS" if not differ else "FAIL",
        "%d files, %d bytes compared byte for byte"
        % (len(arts), sum(a["bytes_expected"] for a in arts)) if not differ
        else "differ: %s" % differ[:8])
    checks["return_code"] = result(
        "PASS" if rc_got == cmd["returncode"] else "FAIL",
        "expected %d, got %s" % (cmd["returncode"], rc_got))
    if mode == "self":
        checks["stderr_empty"] = result("SKIP", "no process executed in selftest")
    else:
        checks["stderr_empty"] = result(
            "PASS" if stderr == "" else "FAIL",
            "stderr empty" if stderr == "" else "stderr: " + stderr[:400].replace("\n", " | "))
    # stdout is informational, not gated: spec/interfaces.md 2 says so for covrun, and
    # the published execution/results/*.txt are a sanitised projection of stdout, not
    # stdout (they drop `time %.2f`, `avg bins%.0f balls%.0f` and the ` t%d/...` progress
    # lines, and rewrite printf("xs%zu build%.2f") as "xs 22829").  Comparing stdout to
    # them byte-wise yields a false failure, so the recorded counters are compared as a
    # digit subsequence and the result never gates the verdict.
    want_d = re.findall(r"\d+", recorded_text(cache, name) or "")
    got_d = re.findall(r"\d+", stdout or "")
    it = iter(got_d)
    sub = all(any(d == g for g in it) for d in want_d)
    checks["stdout_informational"] = result(
        "SKIP",
        "not gated (spec 2). results/%s.txt digit sequence is a subsequence of stdout: %s"
        % (name, "yes" if sub else "NO"))
    fails = [k for k, v in checks.items() if v["status"] == "FAIL"]
    return checks, arts, ("PASS" if not fails else "FAIL")


# ---------------------------------------------------------------- drivers
def run_commands(args, cmds, man, cache, mode):
    files = {p[len(DATA) + 1:] for p in man["files"] if p.startswith(DATA + "/")}
    order = order_commands(cmds, files)
    if args.only:
        rx = re.compile(args.only)
        order = [n for n in order if rx.search(n)]
        if not order:
            raise Setup("--only %r selected no command" % args.only)
    index = {n: i + 1 for i, n in enumerate(sorted(cmds))}
    run = os.path.abspath(args.rundir or os.path.join(REPO_ROOT, ".ultramath", "smwgt1mdy", "m3", "run-" + mode))
    if os.path.exists(run):
        shutil.rmtree(run)
    os.makedirs(run)
    logsub = {"self": "selftest", "real": "replay"}[mode]
    logdir = os.path.join(args.logs, logsub)
    os.makedirs(logdir, exist_ok=True)
    for old in glob.glob(os.path.join(logdir, "R*.json")):   # logs are per run
        os.unlink(old)
    per, t_all, produced = [], time.time(), set()
    for pos, name in enumerate(order, 1):
        cmd = cmds[name]
        outs = all_outputs(name, cmd, files)
        srcs = prepare(run, cache, name, cmd, mode, args.bin, produced)
        rc, so, se, ms, err = produce(run, cache, name, cmd, mode, args.bin, files,
                                      args.timeout)
        produced.update(outs)
        checks, arts, verdict = judge(run, cache, name, cmd, mode, outs, rc, so, se, man)
        if err:
            checks["execution"] = result("FAIL", err)
            verdict = "FAIL"
        rec = {"schema": SCHEMA, "mode": logsub, "index": index[name], "command": name,
               "stage": cmd.get("stage"), "run_order": pos, "argv": cmd["argv"],
               "inputs": cmd.get("inputs") or [], "outputs": outs,
               "declared_outputs": declared(cmd),
               "input_sources": srcs, "rc_expected": cmd["returncode"], "rc_got": rc,
               "artefacts": arts, "checks": checks, "elapsed_ms": round(ms, 1),
               "stdout_sha256": hashlib.sha256((so or "").encode()).hexdigest(),
               "stderr_bytes": len(se or ""),
               "verdict": verdict}
        p = os.path.join(logdir, "R%03d.json" % index[name])
        with open(p + ".part", "w") as f:
            json.dump(rec, f, indent=1, sort_keys=False)
            f.write("\n")
        os.replace(p + ".part", p)
        per.append(rec)
        print("[%3d/%3d] %-14s rc=%s %s %s"
              % (pos, len(order), name, rc, verdict,
                 "%.1fs" % (ms / 1000.0) if ms else ""), flush=True)
    return per, round((time.time() - t_all) * 1000.0, 1), logdir


def summarise(args, mode, per, corpus, elapsed_ms, cmds, man, cache, logdir):
    fails = [r["command"] for r in per if r["verdict"] != "PASS"]
    cfails = [k for k, v in corpus.items() if v["status"] == "FAIL"]
    by_check = {}
    for r in per:
        for k, v in r["checks"].items():
            if v["status"] == "FAIL":
                by_check.setdefault(k, []).append(r["command"])
    for k, v in corpus.items():
        if v["status"] == "FAIL":
            by_check.setdefault(k, []).append("corpus")
    arts = sum(len(r["artefacts"]) for r in per)
    nbyte = sum(a["bytes_expected"] for r in per for a in r["artefacts"])
    noneq = [a["path"] for r in per for a in r["artefacts"] if not a["byte_identical"]]
    bins = {}
    if mode == "replay" and args.bin:
        for b in BINARIES:
            p = os.path.join(args.bin, b)
            if os.path.exists(p):
                bins[b] = {"path": p, "bytes": os.path.getsize(p), "sha256": sha256_file(p)}
    summary = {
        "schema": SCHEMA, "mode": mode, "utc": utcstamp(),
        "verdict": "PASS" if (not fails and not cfails) else "FAIL",
        "cache": cache, "manifest": MANIFEST,
        "manifest_tree_sha1": man["source"]["tree_sha1"],
        "manifest_files": len(man["files"]),
        "manifest_bytes": sum(m["bytes"] for m in man["files"].values()),
        "binaries": bins,
        "selection": args.only,
        "commands": len(per), "commands_passed": len(per) - len(fails),
        "commands_failed": fails,
        "rc_zero": sum(1 for r in per if r["rc_expected"] == 0),
        "rc_one": sum(1 for r in per if r["rc_expected"] == 1),
        "rc_one_names": sorted(r["command"] for r in per if r["rc_expected"] == 1),
        "artefacts_compared": arts, "artefacts_bytes": nbyte,
        "artefacts_not_identical": noneq,
        "corpus_checks": corpus,
        "failed_checks": by_check,
        "elapsed_ms": elapsed_ms,
        "per_command_logs": os.path.join(logdir, "R%03d.json"),
        "notes": ("Per-command logs are R001..R100 in commands.json key order. "
                  "'artefacts' includes the outputs commands.json does not declare "
                  "(Bfine's 88 batch files + fdone.txt)."),
    }
    sp = os.path.join(logdir, "summary.json")
    with open(sp + ".part", "w") as f:
        json.dump(summary, f, indent=1, sort_keys=False)
        f.write("\n")
    os.replace(sp + ".part", sp)
    dated = os.path.join(args.logs, "replay-%s-%s.json" % (mode, utcstamp()))
    shutil.copyfile(sp, dated)
    return summary, sp


# ---------------------------------------------------------------- mutation control
def _clone(cache, dest):
    """Symlink farm of the cache so a mutant costs no bytes."""
    for root, dirs, fs in os.walk(cache):
        rel = os.path.relpath(root, cache)
        tgt = os.path.join(dest, rel) if rel != "." else dest
        os.makedirs(tgt, exist_ok=True)
        for f in fs:
            os.symlink(os.path.join(root, f), os.path.join(tgt, f))


def _replace(dest, rel, data):
    p = os.path.join(dest, rel)
    if os.path.lexists(p):
        os.unlink(p)
    os.makedirs(os.path.dirname(p) or dest, exist_ok=True)
    with open(p, "wb") as f:
        f.write(data)


def _repin(man, dest, rel, data):
    """Rewrite a manifest entry to match mutated bytes (defeats the C1 detector)."""
    new = json.loads(json.dumps(man))
    new["files"][rel] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                         "blob_sha1": "repinned-by-control"}
    return new


def _mutations(man):
    """(id, what, rel path, mutation(body, man) -> (new bytes, repin?), expected checks)."""
    def flip(rel):
        def f(b):
            b = bytearray(b)
            b[-1] ^= 0xFF
            return bytes(b)
        return {"rel": rel, "body": f}

    def swap_doubles(rel):
        def f(b):
            b = bytearray(b)
            b[12:20], b[20:28] = b[20:28], b[12:20]     # record 0 p[0] <-> p[1]
            return bytes(b)
        return {"rel": rel, "body": f}

    def set_count(rel, n):
        def f(b):
            return struct.pack("<Q", n) + b[8:]
        return {"rel": rel, "body": f}

    def truncate(rel, n):
        return {"rel": rel, "body": lambda b: b[:n]}

    def drop_last_record(rel):
        def f(b, ):
            cnt, ks, _, _ = walk_records_buf(b)
            last = 8 + sum(REC_FIXED + 288 * k for k in ks[:-1])
            return struct.pack("<Q", cnt - 1) + b[8:last]
        return {"rel": rel, "body": f}

    def radius_bomb(rel):
        def f(b):
            cnt, ks, _, _ = walk_records_buf(b)
            b = bytearray(b)
            off = 8 + 4 + 288 + 288 * ks[0] + 7 * 8      # record 0, last field = radius
            struct.pack_into("<d", b, off, 1e9)
            return bytes(b)
        return {"rel": rel, "body": f}

    def swap_lines(rel, a, b):
        def f(d):
            s = d.decode()
            return s.replace(a, "\0TMP").replace(b, a).replace("\0TMP", b).encode()
        return {"rel": rel, "body": f}

    return [
        ("M01_manifest_catches_data_byte_flip", "one byte flipped in mid.bin",
         flip(DATA + "/mid.bin"), False, ["C1_manifest_matches_published_bytes"]),
        ("M02_manifest_catches_appended_byte", "one byte appended to batches/f10.bin",
         {"rel": DATA + "/batches/f10.bin", "body": lambda b: b + b"\0"}, False,
         ["C1_manifest_matches_published_bytes"]),
        ("M03_manifest_catches_truncation", "fb1cbad0.bin truncated to 0 bytes",
         truncate(DATA + "/fb1cbad0.bin", 0), False,
         ["C1_manifest_matches_published_bytes"]),
        ("M04_manifest_catches_swapped_double", "record 0 p[0] and p[1] swapped in coarse0.bin",
         swap_doubles(DATA + "/coarse0.bin"), False,
         ["C1_manifest_matches_published_bytes"]),
        ("M05_rc_field_one", "commands.json returncode of C.batch3 set 1 -> 0, manifest repinned",
         {"rel": "execution/commands.json", "body": None}, True,
         ["C2_command_facts", "C5b_15_unresolved_are_the_fallback_inputs"]),
        ("M06_batch_dropped_record",
         "batches/f5.bin loses its last record (count and bytes), manifest repinned",
         drop_last_record(DATA + "/batches/f5.bin"), True,
         ["C8_fine_to_batch_partition", "C9_cross_command_counts"]),
        ("M07_count_field_wrong", "batches/bad3.bin count set 2 -> 3, manifest repinned",
         set_count(DATA + "/batches/bad3.bin", 3), True,
         ["C4_record_structure", "C9_cross_command_counts"]),
        ("M08_radius_out_of_range", "record 0 of fine.bin given radius 1e9, manifest repinned",
         radius_bomb(DATA + "/fine.bin"), True, ["C4_record_structure"]),
        ("M09_done_txt_wrong", "batches/fdone.txt record total 22379 -> 22378, manifest repinned",
         {"rel": DATA + "/batches/fdone.txt",
          "body": lambda b: b.replace(b"88 22379", b"88 22378")}, True,
         ["C8_fine_to_batch_partition"]),
        ("M10_arun_bad_nonempty", "bad0.txt appended a centre index, manifest repinned",
         {"rel": DATA + "/bad0.txt", "body": lambda b: b + b"17\n"}, True,
         ["C7_arun_bad_txt_zero_length"]),
        ("M11_fallback_order_swapped",
         "C.Bfallback swaps its first two inputs, manifest repinned",
         {"rel": "execution/commands.json",
          "body": lambda b: b.replace(b'"batches/bad10.bin",\n        "batches/bad3.bin"',
                                      b'"batches/bad3.bin",\n        "batches/bad10.bin"', 1)},
         True, ["C10_argv_matches_declared"]),
        ("M12_final_bad_count_one", "fb1cbad1.bin count 0 -> 1 with no record, manifest repinned",
         set_count(DATA + "/fb1cbad1.bin", 1), True,
         ["C4_record_structure", "C6_final_bad_files_count_zero"]),
    ]


def walk_records_buf(data):
    n = struct.unpack_from("<Q", data, 0)[0]
    off, ks = 8, []
    for i in range(n):
        k = struct.unpack_from("<i", data, off)[0]
        ks.append(k)
        off += REC_FIXED + 288 * k
    return n, ks, [], []


def control(args, man, cache):
    rows, t0 = [], time.time()
    tmp = os.path.join(REPO_ROOT, ".ultramath", "smwgt1mdy", "m3", "control")
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.makedirs(tmp)
    for i, (mid, what, spec, repin, expect) in enumerate(_mutations(man)):
        if mid.startswith("M05"):        # rc flip: patch the JSON key, not a byte string
            body = json.load(open(os.path.join(cache, "execution", "commands.json")))
            body["children"]["C.batch3"]["returncode"] = 0
            data = json.dumps(body, indent=2).encode()
            man2 = _repin(man, cache, "execution/commands.json", data)
        else:
            rel = spec["rel"]
            data = spec["body"](open(os.path.join(cache, rel), "rb").read())
            man2 = _repin(man, cache, rel, data) if repin else man
        rel = "execution/commands.json" if mid.startswith("M05") else spec["rel"]
        dest = os.path.join(tmp, "%02d" % i)
        _clone(cache, dest)
        _replace(dest, rel, data)
        mpath = os.path.join(tmp, "man%02d.json" % i)
        with open(mpath, "w") as f:
            json.dump(man2, f)
        try:
            cmds = load_commands(dest)
            C = corpus_checks(dest, json.load(open(mpath)), cmds)
            caught = sorted(k for k, v in C.items() if v["status"] == "FAIL")
        except Exception as e:                        # a mutation may make parsing fatal
            caught = ["fatal: %s" % e]
        ok = any(any(c.startswith(e) for c in caught) for e in expect) if expect else False
        rows.append({"id": mid, "mutation": what, "manifest_repinned": repin,
                     "expected_caught_by": expect, "caught_by": caught,
                     "verdict": "PASS" if ok else "FAIL"})
        print("[%2d/%2d] %-38s %s  caught by %s"
              % (i + 1, len(_mutations(man)), mid, rows[-1]["verdict"], caught or "nothing"),
              flush=True)
        shutil.rmtree(dest)
    shutil.rmtree(tmp, ignore_errors=True)
    summary = {"schema": SCHEMA, "mode": "control", "utc": utcstamp(),
               "verdict": "PASS" if all(r["verdict"] == "PASS" for r in rows) else "FAIL",
               "mutations": rows,
               "note": ("Each mutation is a seeded corruption of a copy of the recorded "
                        "artefact set. A PASS means the named checks failed, i.e. the "
                        "harness bit; a FAIL means the corruption went undetected."),
               "elapsed_ms": round((time.time() - t0) * 1000.0, 1)}
    os.makedirs(args.logs, exist_ok=True)
    sp = os.path.join(args.logs, "control", "summary.json")
    os.makedirs(os.path.dirname(sp), exist_ok=True)
    with open(sp + ".part", "w") as f:
        json.dump(summary, f, indent=1)
        f.write("\n")
    os.replace(sp + ".part", sp)
    shutil.copyfile(sp, os.path.join(args.logs, "control-%s.json" % utcstamp()))
    return summary, sp


# ---------------------------------------------------------------- CLI
def main(argv):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["selftest", "replay", "control"])
    ap.add_argument("--cache", default=DEFAULT_CACHE)
    ap.add_argument("--logs", default=DEFAULT_LOGS)
    ap.add_argument("--manifest", default=MANIFEST)
    ap.add_argument("--bin", default=None, help="replay: directory with arun brun crun covrun")
    ap.add_argument("--only", default=None, help="regex on command names")
    ap.add_argument("--timeout", type=float, default=3600.0)
    ap.add_argument("--rundir", default=None)
    args = ap.parse_args(argv)
    try:
        man = load_manifest(args.manifest)
        cache = os.path.abspath(args.cache)
        if not os.path.isdir(cache):
            raise Setup("no cache at %s (run fetch_saved_run.py)" % cache)
        os.makedirs(args.logs, exist_ok=True)
        if args.mode == "control":
            summary, sp = control(args, man, cache)
        else:
            if args.mode == "replay":
                if not args.bin:
                    raise Setup("replay needs --bin DIR")
                args.bin = os.path.abspath(args.bin)
            cmds = load_commands(cache)
            C = corpus_checks(cache, man, cmds)
            runmode = "self" if args.mode == "selftest" else "real"
            per, ms, logdir = run_commands(args, cmds, man, cache, runmode)
            summary, sp = summarise(args, args.mode, per, C, ms, cmds, man, cache, logdir)
    except Setup as e:
        print(json.dumps({"schema": SCHEMA, "verdict": "SETUP_ERROR", "error": str(e)}))
        return 2
    print(json.dumps({"schema": SCHEMA, "mode": summary["mode"],
                      "verdict": summary["verdict"],
                      "commands": summary.get("commands"),
                      "commands_failed": summary.get("commands_failed"),
                      "failed_checks": summary.get("failed_checks"),
                      "log": sp}, sort_keys=False))
    return 0 if summary["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
