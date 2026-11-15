# Verification manifest — `mub6-verification.tex`

Companion to `mub6-verification.tex` / `.pdf` (10 pp.). Written 2026-11-15 during the
one-hour verification window. Every row names the program that produced the claim and the
artefact that holds its output, so a reader can rerun or refute a single line without the rest.

This file records **what was executed**. It is not a proof of the source paper, and no row by
itself proves $N(6)=3$.

## Status vocabulary

| status | meaning |
|---|---|
| `RERUN` | the checker was executed in this window on stored bytes; output archived under `results/preprint-verification/` |
| `QUOTED` | taken from an archived report, **not** executed in this window; the report is named |
| `REFUSED` | the evidence audit declined the claim; the disposition is stated |
| `OPEN` | no checker exists yet; this is the missing premise |

No row has person approval. Nothing here has been peer reviewed.

## A. Seed-cover certificate (§4)

| item | value |
|---|---|
| witness | `certdata/runs/h1-seed-emission/seed.wit`, 6,118,607,511 B, sha256 `de0d07909b8fb46500d383279923db68a5f94c644bb39f14e16253242c06ae87` |
| centres | `certdata/runs/h1-seed-emission/centers.txt`, 249,878 lines, sha256 `c48bc9a2be1eb2cdeea82ea1b030d7cb9f00a6c9563b63f0248dd115748a5789` |
| checker | `src/report/h1_render.py` (report), `src/qcheck/seed_stream_audit.cpp`, `src/qcheck/seed_dual_mpfr.cpp` (duals) |
| output | `certdata/runs/h1-seed-emission/{dual-full,filter-full,structural-audit}.json`; `report.md` regenerated in this window ("H1 report verified and written") |
| status | `RERUN` for the digests, the report regeneration and the summary re-extraction; `QUOTED` for the pair and dual tallies below |

```
pairs_processed 151,744,086 = 249,878 R + 45,648,766 C + 105,845,442 D
mandatory_eligible_pairs 151,742,926 ; rigorously_disjoint 1,160
missing_mandatory 0 ; duplicate_pairs 0 ; invalid_Y 0 ; gap_violations 0
independent_X_membership true ; complete_stream true
duals 105,845,442 proved, failed 0, undecided 0 ; largest_upper_excess -1.1131595859164135e-08 ; MPFR 4.2.2
N 112 ; X tuples 22,829
```

What was **not** recomputed here: the 151,744,086-pair stream and the 105,845,442-comparison
MPFR dual run. Their summary files are dated 00:34–01:08 on the same day, before this window
(`dual-full.json` 00:51, `filter-full.json` 01:08); this window re-read them and checked them
against the regenerated report. Recomputing either is an hours-to-days job, not a one-hour one,
and no number above should be read as having been re-derived in the hour.

Mutations: 62/62 refused in the archived suite (`certdata/runs/h1-seed-emission/mutations.json`,
sha256 `2aaa08ca…`, 21,289 B, 01:14) — `QUOTED`, not rerun here. The 47/47 schema mutations of
§B were rerun.
Prefix cross-check: `prefix2.wit` sha256 `21581207…`, `prefix2-centers.txt` sha256 `a18521e2…`.

**Not covered by this row:** the arrangement and normal-form lemmas of the source, and the
binary-midpoint enlargement to radius `0.0320001`. The claim is for radius `0.032` only.

## B. Composition block and schema (§5.1)

| item | value |
|---|---|
| checker | `work/02-checker/src/make_composition_fixed.py` |
| rebuilt | `.scratch/preprint-comp.bin` |
| archived | `certdata/runs/h1-coverage/composition-v1.bin`, 57,104 B, sha256 `fd61d25749c9ba55cd3082af7023b1b52b09c4715b64fdc2dbcac54616e0f819` |
| comparison | `cmp` identical (both digests `fd61d257…`) |
| status | `RERUN` |

```
parents 163 ; children 1,127 ; links 11,838 ; inherited 10,711
bytes 57,104 = header 28 + 5,216 (parents) + 4,508 (children) + 47,352 (links)
relation_marks 515,236 + snap_closed_cells 7 = 515,243 inside cells (identity holds)
schema mutations 47/47 refused
```

Companion digests: `composition-cover-map.json` sha256 `83516ece860722cad3307181b91a22ac26bbf3cc65630ccef807c15467bc0150`;
`composition-v1.patch.json` sha256 `01d5c836…`; `coverage-manifest.json` sha256 `a59f338c…`.

The archived block differs from the producer's original by an identifier-only patch; that
difference is intended and is itself checked (`comp.prod_identity` below).

## C. Stage-C basic predicates (§5.2)

| item | value |
|---|---|
| checker | `.ultramath/smwh7pmn0/m6/src/recheck_basic.py`, `src/check_witness.py`, interval layer `src/iv.py` |
| command | `python3 src/recheck_basic.py runs/f0r0.emitted.txt runs/census`; `python3 src/check_witness.py runs/witness.json` |
| output | `results/preprint-verification/seed-and-basic.log` (05:50); per-record `runs/census*`, `runs/witness.json` |
| status | `RERUN` for f0#0 in this window; the four-record census in `runs/census-r1..r3` carries the earlier judging-phase timestamps 02:40–02:45 |

```
f0#0 populations 16o 22,366 | 16u 22,366 | 20 3,760 | 21 13,112
     exclusions  16o 18,606 | 16u  9,254 | 20 1,032 | 21  1,619
     code_fired == certified on all four rules; unknown_interval empty; edge_violations empty
12 witness claims, 0 failures
tightest certified 16o 8.494366e-07 (137,84) | 16u 8.774554e-06 (153,47)
                   20  2.873108e-05 (173,29) | 21  3.596107e-07 (187,44)
closest retained 3.573221e-07 (20, pair 153,62)
```

Per-record populations for f0#1–3 are in `runs/census-r1..r3`; the paper's totals
(81,226 / 40,923 / 4,656 / 7,139) are sums of the four measured rows, not a separate measurement.

## D. Stage-C joint predicate (§5.3)

| item | value |
|---|---|
| checker | `.ultramath/smwh95wl3/m3/src/{jointcheck.py,certify_all.py,ratcheck.py}` |
| command | `python3 src/certify_all.py data/f0r0.bin runs/f0r0.emitted.txt runs/f0r0.joint.txt runs/certify-all-f0r0.json` (also r1–r3) |
| output | `.ultramath/smwh95wl3/m3/runs/certify-all-f0r{0,1,2,3}.json`, `runs/xcheck-f0r*.json` (written 03:17–03:24) |
| status | `QUOTED` — the joint certification was **not** re-executed in this window; the files are the judging-phase run, and the numbers below are read from them |

```
61,832 joint rows (14,221 / 17,184 / 16,274 / 14,153)
10,293 rejections certified (3,503 O + 6,790 U) ; 0 of 51,539 retained certified
tightest 7.786e-07 at f0#1 (188,46)
headline f0#0 (188,173): |c.y| = 0.15323322954992958305, RHS = 0.08806125884794263342
gate bits vs independent verdict: 0 mismatches on 61,832 rows
T*T - I = 4.94e-15 <= 1.0e-8
```

## E. Stage-B transported-frame cover (§6.1)

| item | value |
|---|---|
| checker | `work/02-checker/src/stageb_transport/source_transport.py`; graph search in the same tree |
| output | `certdata/runs/h2-stageb/parent-bad10-0-source-transport.json`, 268,131 B, sha256 `f487a4bfe6684bc0b1acd4d96123c2346998de81b78571c98612561955f562fb`; log `results/preprint-verification/stageb-graph.log` |
| status | `RERUN` |

```
normalized_edges 902 ; edges_referenced_by_boxes 303 ; distinct_parent_maps 12
14,641 = 11,480 outside + 3,161 covered + 0 open
smallest_selected_closure_margin 1.0513979010476847e-09
wrong direction: agrees on 620 involutive edges, fails on 282; 135 of the 282 still pass the radius test
(6.24) exact checks: f0 v1/g0 no O-six-clique; g30/g37/g38 omega(O)=6 with 1,997/326/1,344 six-cliques and <= 1 common partner
graph self-tests: planted_full, near_miss, five_wide, empty -- all_ok
```

**Not covered:** a two-level chain. 0 of 1,896 transported-child/parent pairs match, so no
parent → child → Stage-C instance exists (obligation N3).

## F. Stage-A (§6.2)

| item | value |
|---|---|
| tree checker | `.ultramath/smwh7pmn0/m5/reproduce.sh` (driver `instr/treex.cpp`, checks `checker/treecheck.py`, `checker/controls.py`, `checker/fidelity.py`) |
| dual checker | `.ultramath/smwh95wl3/m2/reproduce.sh` |
| output | `results/preprint-verification/stage-a-root.log` (clean rerun 06:01Z, exit 0: trees, then duals with controls and output digests); Root 43 in `stage-a-root-complete.log`; two tensor-C in `root-two.log` |
| status | `RERUN` |

A superseded copy, `stage-a-root.superseded.log`, is kept: it printed the same tree and dual
output and then died in a `FileNotFoundError` because `verify_all.py` was given a relative
output path from inside a subshell. Its Root section is not evidence; the clean copy separates
the Root run into `stage-a-root-complete.log`.

```
trees: 113 nodes = 7 PASS + 14 covered + 72 norm + 20 dual + 1 Root
       145 nodes ; 1-node degenerate control
treecheck: 26 checks pass on all three trees
controls: 9 mutations per tree, 0 uncaught, base_ok
fidelity: restricted tree == corresponding subtree of the unrestricted run, same_keys, 0 verdict differences
duals: 20/20 PASS, min margin 0.020637412556 at node 90 (206.4x the 1e-4 pad), max 0.293710235 at node 34 (2937.1x)
       chain (bins -> block -> dataU -> bound -> certificate) PASS 20/20 ; max bound rounding 2.06 ulp
```

Build flags: the m2 replay is compiled `g++ -O2 -std=c++17`, not the record's
`-O3 -march=native`, so its payload dump is an independent build; agreement with the stored
`sum`/`b.z` on 113/113 nodes is therefore a bit-identity result across two builds.

**Known artefact, stated in the paper.** The Stage-A replay driver reuses the upstream
arithmetic but does not implement the covering test, so it labels the 14 covered leaves `PASS`
where the tree says `COVERED`; `sum` and `b.z` agree on 113/113 nodes regardless
(`.ultramath/smwh95wl3/m2/runs/s0c7/replay.csv`, columns `repsum_eq_m5`, `repZ_eq_m5`).
The paper's claim is about sums and `b.z`, not about labels. The count matches the covering
test exactly: the replay reports `mismatch 14` for the 113-node tree, whose covered leaves are
14, and the 145-node tree has 22 covered leaves — no other field disagrees.

**Not covered:** the (3.26) implication and the `block::get` majorisation — 20 certificates
exist, the analytic step to "cell empty" is transcribed, not proved (obligation N2).

## G. Root witnesses (§6.3)

| item | value |
|---|---|
| checker | `.ultramath/smwh7pmn0/m1/src/verify_all.py` (interface), `.ultramath/smwh95wl3/m1/run_all.sh` (two tensor-C records) |
| output | `results/preprint-verification/root43.json` (sha256 `fb2b41b9bb59c7f0f1be1a151cc3d23b54ea586749a1988f847f564334960b98`), `root-two.log` |
| status | `RERUN` |

```
43 different-U witnesses: PASS 34, FAIL 9, UNDECIDED 0
   all 9 failures are R7-only (R5, R6 pass): coarse0 indices 8, 11, 19, 24, 94 ; mid indices 4, 10, 13, 500
coarse0#678, coarse3#33: stored representation root=body_pass_C_undecided
   at exact image q with rescaled M (eps 1e-7): root=pass, C_tensor margin ~4.7e-7
coarse0#547 (k=0 control): root=pass, C_base slack ~1e-7
```

Independent transport check (lead-written, `.scratch/verify_two_root_transfers.py`), kept
separate from the member's own report because their numbers disagree:

```
certdata/runs/h1-root-interval/two-tensor-transport-check.json
  sha256 63944ad5d84edbf4febb14b236277f450b0ba0d4446969d871099e3bb727afb5
  coarse0#678  TT* projector delta <= 7.386179670356769e-14
  coarse3#33   TT* projector delta <= 6.35280385589379e-14     (residual budget id = 2e-6)
```

The member's report claimed 2.5e-15 for the same quantity; the lead's measurement is the one
quoted. Root verdicts are existential: they do not recover the source's `M` or its original
pre-canonical centre.

## H. Lean skeleton (§7)

| item | value |
|---|---|
| checker | `lean` on the preset `LEAN_PATH` (Lean 4.33.1, Mathlib built) |
| files | `work/04-lean/Mub6/AssemblyScoped.lean` sha256 `be5f8445…`, `StageCGraph.lean` sha256 `f1d671a3…`, `StageCNecessity.lean` sha256 `6030a78a…` |
| output | `results/preprint-verification/lean.log` |
| status | `RERUN` |

```
all three modules elaborate (warnings only: unused variables, deprecation, unnecessary simpa)
'Mub6.AssemblyScoped.chain_excluded' does not depend on any axioms
'Mub6.AssemblyScoped.chain_excluded_emb' does not depend on any axioms
```

No axioms means no `sorryAx` in those two theorems. It does **not** mean the hypotheses are
instantiated: `Cov` facts and terminal conditions are assumed arguments (obligation N6).

## I. Quoted, not rerun

| item | source | status |
|---|---|---|
| 92-command Stage-C replay: 92/92 bad-record outputs byte-identical, 23,343 completed negatives + 163 capped at exactly 5,000,001 steps | `certdata/runs/h0-stagec-replay-report.md`; numbers in `certdata/runs/h0-stagec-probe{,-summary}.json` | `QUOTED` |

Byte identity is a provenance property, not a proof of any predicate. The paper says so in §9.

## J. Claims the evidence audit refused

`results/matrix.json` (sha256 `16095453f7aaa67a3ebed5c545c1564654b380599bc0ec9857362a0f8bcce69e`),
55 claims: 42 `CERTIFIED`, 4 `CONTRADICTED`, 9 `UNSUPPORTED`, 26/26 controls, no baseline mismatch.

| id | claim | disposition |
|---|---|---|
| `comp.spec_layout_old` | counts at 12/16/20 with a reserved word at 24 | `REFUSED` — the retired layout; the repaired spec is what the block implements |
| `comp.prod_identity` | archived block byte-identical to the producer's | `REFUSED` — differs by the audited identifier-only patch; difference is intended |
| `rec.g0_bytes` | record adjacency byte-identical to `g0.txt` | `REFUSED` — equivalent after big-endian decode and a non-unique ball permutation, not byte-identical |
| `cap.delta_naive` | `delta_bytes` = raised − today | `REFUSED` — arithmetic in the claim is wrong |
| `seed.semantic` | all 151,742,926 mandatory pairs covered by a proof object | `REFUSED` — per-pair cover objects are not stored; the certificate is the inequality stream |
| `stageb.clearance_1709`, `stageb.slack_stats` | positive clearance / slack statistics for 1,709 boxes | `REFUSED` — not measured; the 3,161 covered boxes are covered by relation or snap, not by a measured margin |
| `comp.percell`, `comp.remaining_measured` | each of 515,243 inside cells closed; 321,004,555 remaining obligations measured | `REFUSED` — per-cell closure is not verified (this is the N1 gap) |
| `cap.capped_covered` | 163 capped records covered by the fallback layer | `REFUSED` — the fallback chain is not transported end-to-end (N4) |
| `root.slack_typing`, `root.semantic` | stored `mnorm` slack bounds the relative error; 48 sampled Root verifications hold | `REFUSED` — typing not established; the sample was superseded by the 43-witness rerun in §G |
| `rec.soundness` | 32,857 stored exclusions are sound | `REFUSED` — counters are not an implication |

The paper's status table (`tab:status`) is built from these dispositions.

## K. Open obligations (the paper's N1--N7)

Numbering matches `\subsection{Priorities}` of the article; the "blocking" column says what
cannot be claimed until the item is closed.

| # | obligation | blocking what | status |
|---|---|---|---|
| N1 | certify the ball/cluster cover: every admissible bin lies within its assigned ball radius | Proposition 5.6, the local Stage-C exclusion | `OPEN` — largest missing premise; needs an outward membership test on the four-record pilot |
| N2 | complete Stage-A locally: the (3.26) implication, the `block::get` majorisation, and one fully retained small tree | "cell empty" from the 20 dual certificates | `OPEN` — 113/145-node trees certify subdivision and duals; the analytic implication is transcribed, not proved |
| N3 | transport Stage-B as a chain: one parent whose own ledger, transformed child ledger and Stage-C record are all present | the 163 capped records | `OPEN` — 0/1,896 transported-child/parent matches |
| N4 | resolve the nine undecided Root witnesses: coarse0[8, 11, 19, 24, 94], mid[4, 10, 13, 500] | Root-layer completeness | `OPEN` — find an exact `M` at the standard of the 34, or a rigorous obstruction; a failed search is not one |
| N5 | repeat the basic/joint predicates over every completed-negative and fallback record | any global Stage-C claim | `OPEN` — four records done; the two `omega(O)=3` records stay marked vacuous |
| N6 | instantiate the Lean `Cov` premises and terminal conditions against decoded certificates | the assembly theorem | `OPEN` — `chain_excluded` is axiom-free but its hypotheses are assumed arguments |
| N7 | commission an independent human review | publication | `OPEN` — no human gate exists; no result here is approved |

## L. Reproduction

Working directory is the repository root. Binaries are rebuilt by the `reproduce.sh` scripts
named above; no script writes into the upstream tree.

```
python3 src/report/verify_upstream_hashes.py            # 7 upstream sources, all_match
.ultramath/smwh7pmn0/m5/reproduce.sh                    # Stage-A trees (run from its directory)
.ultramath/smwh95wl3/m2/reproduce.sh                    # Stage-A dual certificates
.ultramath/smwh95wl3/m1/run_all.sh                      # two tensor-C records
python3 work/02-checker/src/stageb_transport/source_transport.py
cd work/04-lean && lean Mub6/AssemblyScoped.lean        # Lean 4.33.1, built Mathlib
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=.scratch/build mub6-verification.tex
```

`verify_all.py` must be given an absolute output path; a relative one inside a subshell writes
to the wrong directory. Use `-outdir=DIR` (with `=`) for `latexmk`.
