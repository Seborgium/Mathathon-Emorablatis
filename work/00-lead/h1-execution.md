# H1-H5 execution ledger (D12, eight-hour owner-authorised window)

Start: 2026-11-14 21:27 UTC. Owner approved H1-H5 and up to eight hours compute. This is not a
claim that all gates can close in that window.

## Active agent teams
| team | swarm | members | scope |
|---|---|---|---|
| H1 seed | smwgx3s1v | 6 | emitter, exact kernel/filter/reuse, enumeration, mutations, provenance audit |
| Q3 / H2 | smwgx2sv0 | 6 | Root, atlas, Stage A/B, interval pilot, adversarial interfaces |
| Q4 extension | smwgx104w | 6 | exact Stage-C pilot, schema, predicate fidelity, padding, Lean/alternatives |

All use deepseek/deepseek-v4.1-flash at max reasoning; Q3 100 steps / 300 min; H1 and Q4 120 / 300.
Lead integrates, re-runs, judges and writes specifications; no accepted output is final without lead
verification. Three teams and 4 CPUs means wall-clock benchmarks must be marked contended; heavy
jobs need coordination.

## Immediate lead responsibilities
- pin spec v0 arithmetic/statement and verification vocabulary across three independent proposals;
- source hash check (DONE: all seven expected sha256/byte sizes match);
- assemble evidence index, mutation rules and final report pipeline;
- review submissions as they arrive; avoid duplicate full covrun or full crun sweeps;
- reserve compute for end-to-end seed exact-checking once the emitter and checker integrate.

## Explicit current limitations
No exact exclusion certified yet; only binary64 full replay and microbenchmarks. Schemas v0. No
Root/Stage-A/B certificate has been generated. Lean proves one abstract Stage-C reduction, not the
full assembly. Q3/Q4/H1 have just started; no member submissions judged in this new window.

## Accepted H1 input — Stage-C fallback coverage (Q4/m2)
Report `work/02-checker/reports/H1-stageC-coverage-map.md`, data `certdata/runs/h1-coverage/`.
Lead reran partition/radius/census checks and the five-record residue probe; both regenerated
fallback streams are byte-identical to archive. The 163 unresolved records need 1,127 fallback
balls and 11,838 *covering* incidences (10,711 inherited across parents), not just creation lists.
Stage-B cover counters are 321,519,798 inside-cell obligations. Graph-only route (a) is therefore
necessary but not sufficient; schema v1 must include both radii and composition/cover maps.
The cover metric `relationB::init/eval` remains unproven and will be checked by Q3.

## Accepted H2 input — exact Root/Stage-B verdict prototype (Q3/m5)
`work/02-checker/reports/H2-interval-prototype.md`, code
`work/02-checker/src/root_interval/`, outputs `certdata/runs/h1-root-interval/`.
Lead reran 48 records: six basic Root facts 48/48; complete reconstructed-C verdicts 46 pass,
2 unresolved-by-missing-witness (printed FAIL for those two candidates, not a false Root).
Stage-B fallback parent ledger: 11480 outside, 1709 covered, 1452 unresolved. Independent
kernel tests: 150 outbound trigonometric enclosures, 1000 square-root enclosures and pi.
The proposed C0/C1(U) or serialised witness repair and full Stage-B cover remain work in progress.
The 16 CPU-hour production rewrite is explicitly an unmeasured estimate.

## Accepted H1 contributions and lead-built seed witness
- Seed arithmetic audit: `work/01-catalogue/H1-seed-arithmetic-audit.md` (accepted Q4/m6).
- Exact filter/enumeration: `work/01-catalogue/H1-filter-census.md` (accepted H1/m2). Lead reran
  both complete C++ censuses byte-for-byte; X=22,829, |Y|=829,306, 0 undecided cases.
- Lead emitter `src/emit/covout.cpp`: full witness `certdata/runs/h1-seed-emission/seed.wit` (5.7 GiB),
  exact archived centres. Structural parser confirms 151,744,086 pairs =
  249,878 fresh (R) + 45,648,766 exact cheap (C) + 105,845,442 dual (D).
- Prefix validation: 158 pairs, all covers proved, 13/13 duals verified independently with two
  number forms. Fixed-point division and matrix-row indexing bugs in the lead's prototypes were
  caught at prefix scale and not accepted silently; MPFR reproduces the Python smallest margin.
- Full MPFR verification of all duals is running as a separate background job. Do not call the
  seed covering proposition certified until it completes and an exact enumerator connects filters
  to pair IDs; rejected/undecided cases are retained, never silently dropped.

## Accepted scoped assembly (H2/H3 swarm mem 2)
`work/04-lean/Mub6/AssemblyScoped.lean` and `work/02-checker/reports/H2-scoped-assembly.md`.
Independently compiled via run.sh and after promotion: its refinement chase has no axioms, all other
checked theorems only standard axioms. This is a conditional proof skeleton with named interface
fields, not a record decoder, not the main theorem and not a claim that the archived run satisfies
Chain. Root witnesses, Stage-A cell verdicts, Stage-B missing mediator coverage and Stage-C
predicate fidelity remain separate analytic obligations. Negative controls for caps, missing
cover, missing refinement and missing terminal exclusion are compiled.
