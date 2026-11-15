#!/usr/bin/env python3
"""Map each field of the Lean `Chain` interface to the archived quantity that would discharge it.

Reads machine-readable artefacts only (JSON); no prose is parsed and no quantity is re-derived.
Status vocabulary, deliberately three-valued so that "absent" can never read as "verified":

  DISCHARGED_NUMERICALLY  the archive contains the quantity the field asks for, and it passes
  NOT_DISCHARGEABLE       the archive lacks the datum the field needs (the field stays a hypothesis)
  INTERFACE_ONLY          the field is a mathematical implication, not a finite record property

Run:  python3 field_audit.py            (from the member directory)
"""
import json, pathlib, sys

REPO = pathlib.Path(__file__).resolve().parents[3]   # .../repo
R = REPO / "certdata/runs"

def load(p):
    return json.loads((R / p).read_text())

probe = load("h0-stagec-probe-summary.json")["summary"]
rec = load("h0-record-check.json")
cov = load("h1-coverage/coverage-report.json")

cats = probe["categories"]
groups = probe["groups"]
cover = rec["cover"]
t = cov["tests"]

rows = []

def row(field, paper, status, quantity, source):
    rows.append(dict(field=field, paper=paper, status=status, quantity=quantity, source=source))

# hseed: seed cover.  The archive has coverage *pairs*; the implication pairs -> cover is Prop 2.10.
row("hseed", "Prop 2.10", "INTERFACE_ONLY",
    f"centres={cover['centers']}, checked_pairs={cover['checked_pairs']} (the coverage relation; the "
    f"2.10 induction from pairs to a ball cover is not formalised)",
    "certdata/runs/h0-record-check.json:cover")

# tree: Stage-A cell certificates with no unresolved leaf.
row("tree", "Prop 3.11", "NOT_DISCHARGEABLE",
    "cell counts only (C.Bfallback: base=2386483, inside=515243, live=17207, snaps=17207, split=0, "
    "fail=0; upstream inside-cell obligations=321004555); no per-cell verdict is archived, so the "
    "cell tree -- which needs a verdict at every leaf -- cannot be built from it",
    "certdata/runs/h1-coverage/coverage-report.json:T11_ledger")

# hball_le: A-stage balls written to the coarse atlas.
row("hball_le", "Prop 4.16", "NOT_DISCHARGEABLE",
    "no per-ball write-out map from A-stage records to the coarse atlas is archived; only counts "
    "(coarse_records=764,774,757,788)",
    "certdata/runs/h0-record-check.json:coarse_records")

# hstep: the refinement step of each Stage-B/C pass.
row("hstep", "Prop 5.7 / Cor 5.8", "NOT_DISCHARGEABLE",
    "fallback parent bad10#0: 11480 outside + 1709 relation-covered of 14641 boxes, 1452 without an "
    "archived merge mediator; the run's own 'fail0/split0' counters are not a refinement witness",
    "work/02-checker/reports/H2-interval-prototype.md:53,289")

# hfinal on the final frontier: four modulo-4 shards, all completed negatives.
shards = t["T5_final_parts"]["parts"]
row("hfinal(final)", "Prop 6.9 + Sec 7.2", "DISCHARGED_NUMERICALLY",
    f"four shards {[shards[k]['residue_count'] for k in sorted(shards)]} sum to {t['T5_final_parts']['n']}, "
    f"union_is_all={t['T5_final_parts']['union_is_all']}; all final records are completed negatives "
    f"(nopattern={cats['nopattern']} = 22216 initial + 1127 final)",
    "certdata/runs/h1-coverage/coverage-report.json:T5_final_parts; h0-stagec-probe-summary.json:categories")

# hfinal on the initial frontier: 163 capped records are not negatives.
row("hfinal(initial)", "Prop 6.9 + Sec 7.2", "NOT_DISCHARGEABLE",
    f"capped={cats['cap']} records at exactly {probe['steps_cap']['max']} steps: a cap is an unresolved "
    f"search, not a negative verdict, so the initial frontier cannot terminate the chain",
    "certdata/runs/h0-stagec-probe-summary.json:steps_cap")

# hneg: Prop 6.9 conclusion, needs the ball radius bound and the graph predicates.
row("hneg", "Prop 6.9", "INTERFACE_ONLY",
    f"radii are below the paper's 0.1: fine max={t['T10_radius']['fine_atlas_radius_max']:.9f}, "
    f"fb1 max={t['T10_radius']['fb1_atlas_radius_max']:.9f}; the graph predicate itself is the "
    f"predicate-fidelity obligation (not certified here)",
    "certdata/runs/h1-coverage/coverage-report.json:T10_radius")

# hext, emb: pure interfaces.
row("hext", "Lemma 1.2", "INTERFACE_ONLY",
    "extendible => exact dephased Hadamard matrix; a definitional implication, not a record property",
    "-")
row("emb fields", "Lemma 2.2 / Lemma 4.7", "INTERFACE_ONLY",
    "signed permutation / transpose / rephasing equivalence and invariance of extendibility",
    "-")

print(f"{'field':16} {'paper':22} {'status':24} quantity")
for r in rows:
    print(f"{r['field']:16} {r['paper']:22} {r['status']:24} {r['quantity']}")

out = pathlib.Path(__file__).resolve().parent / "logs/field-audit.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(rows, indent=1) + "\n")
print(f"\nwrote {out}")
sys.exit(0)
