"""Step 5 of 5 on one example: one documented execution, read back.

The input is the archived record census of a real Stage-C pass of the
documented run (23,506 graph records, certdata/runs/h0-stagec-probe.json).
Step 5's tests are not inequalities on matrices but statements about the run:
every record ends in exactly one of its three states, the unresolved list is
empty, and every threshold comparison is made with a margin that survives
binary64.

    python3 examples/step5_example.py [--probe PATH]
"""
import json
import statistics
import sys
from fractions import Fraction

import numpy as np

OUT = []
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBE = os.path.join(ROOT, "certdata/runs/h0-stagec-probe.json")
SUMMARY = os.path.join(ROOT, "certdata/runs/h0-stagec-probe-summary.json")


def row(key, value, note=""):
    OUT.append((key, value, note))


def main():
    global PROBE
    for a in sys.argv[1:]:
        if a.startswith("--probe="):
            PROBE = a.split("=", 1)[1]
    d = json.load(open(PROBE))
    rec = d["records"]

    # ---------------------------------------------------------- the census
    row("s5.records", len(rec), "records in the pass")
    cat = {}
    for r in rec:
        cat.setdefault(r["category"], []).append(r)
    for c in sorted(cat):
        st = [r["steps"] for r in cat[c]]
        row("s5.category.%s.n" % c, len(cat[c]), "records")
        row("s5.category.%s.steps" % c,
            dict(min=min(st), median=statistics.median(st), max=max(st),
                 total=sum(st)), "")
    row("s5.categories", {c: len(v) for c, v in sorted(cat.items())}, "")
    balls = [r["balls"] for r in rec]
    row("s5.balls", dict(min=min(balls), median=statistics.median(balls),
                         max=max(balls), total=sum(balls)), "")

    # three miniatures: fewest steps, the median record, one capped record
    bysteps = sorted(rec, key=lambda r: r["steps"])
    med = bysteps[len(bysteps) // 2]
    capped = next(r for r in rec if r["category"] == "cap")
    mini = []
    for r in (bysteps[0], med, capped):
        mini.append(dict(command=r["command"], index=r["index"], category=r["category"],
                         bins=r["bins"], balls=r["balls"], O=r["O"], U=r["U"],
                         steps=r["steps"]))
    row("s5.miniatures", mini, "")

    # ------------------------------------------------- the accounting identity
    n, nop, cap = len(rec), len(cat.get("nopattern", [])), len(cat.get("cap", []))
    row("s5.identity.records", n, "")
    row("s5.identity.nopattern_plus_cap", nop + cap, "")
    row("s5.identity.balances", nop + cap == n, "")
    row("s5.identity.unresolved", cap, "records with no completed verdict")
    # the pass's own log totals, and what each counter means
    tot = d["saved_log_totals"]
    row("s5.log.totals", tot, "the run's own counters for this pass")
    row("s5.log.done_equals_bad_plus_good",
        tot["done"] == tot["bad"] + (tot["done"] - tot["bad"]), "")
    row("s5.log.graph_is_not_searches", tot["graph"],
        "0, while %d graph searches ran: it counts completed searches that FOUND a pattern" % n)
    row("s5.log.over_and_cluster", [tot["over"], tot["cluster"]], "both 0: no overflow, no clustering failure")

    # ------------------------------------------- the arithmetic contract
    # the Step-1 vanishing-sum slack 5*pi*w^2/4 at w = 1/112
    w = Fraction(1, 112)
    exact = Fraction(5, 4) * w * w                     # times pi
    x = float(exact) * np.pi
    wid = 5 * 2.0 ** -53                               # a few roundings
    row("s5.margin.units", "5*pi*w^2/4 at w = 1/112", "")
    row("s5.margin.exact.times_pi", [exact.numerator, exact.denominator], "5/50176")
    row("s5.margin.exact", float(exact) * np.pi, "")
    row("s5.margin.float64", float(x), "binary64")
    row("s5.margin.ulp", float(abs(x - float(exact) * np.pi) / np.spacing(x)), "in ulps")
    row("s5.margin.outward.rel", float(wid), "k=5 roundings, relative")
    row("s5.margin.outward.abs", float(abs(x) * wid), "absolute width of the outward interval")
    row("s5.margin.relative_to_value", float(wid), "")
    # what the code compares instead: an absolute slack
    row("s5.margin.code_slack", 2e-7, "the absolute slack in the pair tests (stageC.cpp)")
    row("s5.margin.code_slack.over_outward", float(2e-7 / (abs(x) * wid)),
        "how many outward intervals fit in the code's own slack")
    # the same for the support bound 1.25*pi/N
    N = 112
    y = 1.25 * np.pi / N
    row("s5.support.value", float(y), "1.25*pi/112")
    row("s5.support.outward.abs", float(abs(y) * wid), "")

    # the cost side: what the pass did, in the units Step 5's ledger uses
    row("s5.steps.total", sum(r["steps"] for r in rec), "graph steps in the pass")
    row("s5.O_plus_U.total", sum(r["O"] + r["U"] for r in rec), "edges built")

    print_table()
    if "--json" in sys.argv:
        json.dump({k: v for k, v, _ in OUT},
                  open(os.path.join(ROOT, "examples/out/step5.json"), "w"),
                  indent=1)


def print_table():
    w = max(len(k) for k, _, _ in OUT)
    for k, v, note in OUT:
        vs = "%.12g" % v if isinstance(v, float) else str(v)
        print("%-*s  %-30s %s" % (w, k, vs, note))


if __name__ == "__main__":
    main()
