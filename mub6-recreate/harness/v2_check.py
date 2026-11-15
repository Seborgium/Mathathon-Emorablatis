#!/usr/bin/env python3
"""Driver for work unit 10: run the independent checker on the recorded set and
on every seeded corruption, and run the published checker on the same cases.

Usage:
  python3 v2_check.py --execution <pristine execution dir> \
                      --sandbox <scratch dir> [--published <check_records.py>] \
                      [--logdir work/10-recreate/logs] [--reuse]

Writes logs/v2-<UTC date>.json (machine readable, fixed schema) and
logs/v2-<date>.md, prints a PASS/FAIL table, exits 0 only if
  * the independent checker accepts the recorded set,
  * the independent checker rejects every case with its expected check id, and
  * both checkers and both counts are reported (a published miss is recorded,
    not treated as a failure of this script).
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def run(cmd, cwd=None, timeout=900):
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return {"rc": p.returncode, "out": p.stdout, "err": p.stderr,
                "elapsed_s": round(time.time() - t0, 3), "timeout": False}
    except subprocess.TimeoutExpired:
        return {"rc": None, "out": "", "err": "timed out after %ds" % timeout,
                "elapsed_s": round(time.time() - t0, 3), "timeout": True}


def parse_json(text):
    try:
        return json.loads(text)
    except Exception:                                            # noqa: BLE001
        i = text.find("{")
        if i < 0:
            return None
        try:
            return json.loads(text[i:])
        except Exception:                                        # noqa: BLE001
            return None


def last_meaningful(err):
    for line in reversed([l.strip() for l in err.splitlines() if l.strip()]):
        if not line.startswith(("File ", "^", "Traceback")):
            return line[:300]
    return ""


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--execution", required=True)
    ap.add_argument("--sandbox", required=True)
    ap.add_argument("--published", default=None,
                    help="published check_records.py, used as a black-box oracle")
    ap.add_argument("--logdir", default=os.path.join(HERE, os.pardir, "logs"))
    ap.add_argument("--reuse", action="store_true", help="reuse an existing sandbox manifest")
    args = ap.parse_args(argv)

    execution = os.path.abspath(args.execution)
    sandbox = os.path.abspath(args.sandbox)
    mine = os.path.join(HERE, "check_records_indep.py")
    now = datetime.datetime.now(datetime.timezone.utc)
    stamp = now.strftime("%Y-%m-%dT%H%M%SZ")
    os.makedirs(args.logdir, exist_ok=True)

    doc = {
        "unit": "W1 / work unit 10 (independent record checker)",
        "date_utc": stamp,
        "execution_dir": execution,
        "checker": os.path.relpath(mine),
        "published_checker": os.path.abspath(args.published) if args.published else None,
        "pristine": {},
        "cases": [],
    }

    # ------------------------------------------------------------ pristine data
    r = run([sys.executable, mine, execution])
    doc["pristine"]["independent"] = {"rc": r["rc"], "elapsed_s": r["elapsed_s"],
                                      "result": (parse_json(r["out"]) or {}).get("result"),
                                      "checks": (parse_json(r["out"]) or {}).get("checks"),
                                      "summary": (parse_json(r["out"]) or {}).get("summary"),
                                      "stderr": last_meaningful(r["err"])}
    if args.published:
        p = run([sys.executable, args.published, execution])
        doc["pristine"]["published"] = {"rc": p["rc"], "elapsed_s": p["elapsed_s"],
                                        "out_head": p["out"].strip().splitlines()[:2],
                                        "stderr": last_meaningful(p["err"])}
    print("pristine: independent rc=%r (%ss) published rc=%r"
          % (doc["pristine"]["independent"]["rc"], doc["pristine"]["independent"]["elapsed_s"],
             doc["pristine"].get("published", {}).get("rc")))

    # ---------------------------------------------------------------- corruptions
    manifest_path = os.path.join(sandbox, "manifest.json")
    if not (args.reuse and os.path.isfile(manifest_path)):
        if os.path.isdir(sandbox):
            shutil.rmtree(sandbox)
        b = run([sys.executable, os.path.join(HERE, "mkcorruptions.py"), execution, sandbox], timeout=1200)
        if b["rc"] != 0:
            print(b["out"] + b["err"], file=sys.stderr)
            raise SystemExit("building the corruption suite failed")
    with open(manifest_path) as f:
        manifest = json.load(f)

    n_indep = n_pub = n_expected = n_miss = n_miss_confirmed = 0
    for case in manifest["cases"]:
        cdir = case["dir"]
        m = run([sys.executable, mine, cdir])
        mj = parse_json(m["out"]) or {}
        fails = [c for c in mj.get("failures") or []]
        fired = [c["id"] for c in fails]
        caught = m["rc"] != 0 and bool(fails)
        expect = case.get("expect_check") or []
        expect_miss = bool(case.get("expect_miss")) or not expect
        expected_ok = (not caught) if expect_miss else (caught and any(e in fired for e in expect))
        entry = {"id": case["id"], "description": case["description"],
                 "mutation": case["mutation"], "expect_check": expect,
                 "expect_miss": expect_miss,
                 "independent": {"rc": m["rc"], "caught": caught, "expected_check_fired": expected_ok,
                                 "checks_failed": len(fails), "fired": fired[:6],
                                 "elapsed_s": m["elapsed_s"]},
                 "published": {}}
        if args.published:
            p = run([sys.executable, args.published, cdir])
            pj = parse_json(p["out"]) or {}
            # the oracle "catches" a corruption iff it does not report PASS
            caught_pub = (p["rc"] != 0) or pj.get("result") not in (None,
                                                                    "PASS within numerical consistency scope")
            entry["published"] = {"rc": p["rc"], "caught": bool(caught_pub),
                                 "note": (pj.get("result") or last_meaningful(p["err"]) or
                                          last_meaningful(p["out"]))[:200],
                                 "elapsed_s": p["elapsed_s"]}
            n_pub += 1 if caught_pub else 0
        n_indep += 1 if caught else 0
        n_expected += 1 if expected_ok else 0
        if expect_miss:
            n_miss += 1
            n_miss_confirmed += 1 if (not caught and
                                      (not args.published or not entry["published"].get("caught"))) else 0
        doc["cases"].append(entry)
        print("%-24s mine=%-6s expected=%-6s published=%s"
              % (case["id"], "reject" if caught else "ACCEPT",
                 ("accept" if expect_miss else "reject") + ("" if expected_ok else "(NO)"),
                 ("reject" if entry["published"].get("caught") else "ACCEPT")
                 if args.published else "-"))

    total = len(manifest["cases"])
    doc["totals"] = {
        "cases": total,
        "independent_caught": n_indep,
        "independent_expected_check_fired": n_expected,
        "published_checked": n_pub,
        "published_caught": sum(1 for c in doc["cases"] if c["published"].get("caught")) if args.published else None,
        "published_missed": [c["id"] for c in doc["cases"]
                             if args.published and not c["published"].get("caught")],
        "pristine_files": manifest.get("pristine_files"),
        "expected_misses": n_miss,
        "expected_misses_confirmed": n_miss_confirmed,
    }
    # Every case must behave as predicted: a real corruption rejected with its
    # named check, a predicted-undetectable one accepted.  A published miss is
    # reported, never counted as a failure of this script.
    ok = (doc["pristine"]["independent"]["rc"] == 0 and n_expected == total
          and (not args.published or doc["pristine"]["published"]["rc"] == 0))
    doc["verdict"] = "PASS" if ok else "FAIL"

    json_path = os.path.join(args.logdir, "v2-%s.json" % stamp)
    with open(json_path, "w") as f:
        json.dump(doc, f, indent=1)

    md_path = os.path.join(args.logdir, "v2-%s.md" % stamp)
    with open(md_path, "w") as f:
        f.write("# W1/10 — independent checker v2, run %s\n\n" % stamp)
        f.write("pristine set: independent rc=%r, published rc=%r\n\n"
                % (doc["pristine"]["independent"]["rc"],
                   doc["pristine"].get("published", {}).get("rc")))
        f.write("| case | mutation | my checker | expected check fired | published checker |\n")
        f.write("|---|---|---|---|---|\n")
        for c in doc["cases"]:
            f.write("| %s | %s | %s | %s | %s |\n"
                    % (c["id"], c["mutation"].replace("|", "\\|"),
                       "reject" if c["independent"]["caught"] else "**accept**",
                       ("none fired: accepted as predicted" if c["expect_miss"]
                        else "yes: " + ", ".join(c["independent"]["fired"][:2]))
                       if c["independent"]["expected_check_fired"] else "**unexpected**",

                       ("reject" if c["published"].get("caught") else "**accept (miss)**")
                       if args.published else "-"))
        f.write("\nverdict: %s; independent rejected %d/%d, behaved as predicted %d/%d, "
                "predicted-undetectable confirmed %d/%d"
                % (doc["verdict"], n_indep, total, n_expected, total,
                   n_miss_confirmed, n_miss))
        if args.published:
            f.write("; published caught %d/%d, missed: %s"
                    % (doc["totals"]["published_caught"], total,
                       ", ".join(doc["totals"]["published_missed"]) or "none"))
        f.write("\n")

    print("\nverdict %s: independent rejected %d/%d, as predicted %d/%d, "
          "undetectable-confirmed %d/%d%s"
          % (doc["verdict"], n_indep, total, n_expected, total, n_miss_confirmed, n_miss,
             "" if not args.published else
             "; published %d/%d, missed %s" % (doc["totals"]["published_caught"], total,
                                               doc["totals"]["published_missed"])))
    print("logs: %s" % json_path)
    print("logs: %s" % md_path)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
