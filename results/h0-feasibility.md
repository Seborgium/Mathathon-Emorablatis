# H0 feasibility evidence (complete for G0; 2026-11-14 21:05 UTC)

Owner decisions: D8 approved `results/certificate-plan.md`; D9 set **H0 = one hour** from
20:15 UTC 2026-11-14 and authorised both six-member swarms (Q4 launched as `smwguhf32`, Q3 held
for H2). This file records only what was actually run. Nothing here is a certification of the
preprint; the instrumented build measures floating-point searches, it does not replace them by
exact proofs.

## 1. Upstream acquisition
- Git tree `949d86069dd23dcd2b543dd749e8d8889342da50` (the `verification/` tree) listed with
  `truncated: false`: 309 blobs. Listing: `certdata/upstream/tree.json`.
- All 309 files fetched from `raw.githubusercontent.com` (no API auth, no rate-limit event),
  82,506,791 bytes total, into `.scratch/h0/dl/verification/`; per-file sha256 and sizes:
  `certdata/upstream/manifest.json`. The preprint PDF (817,737 bytes) is beside that directory.
- The authors' consistency checker was run: **PASS within numerical consistency scope**
  (`certdata/runs/h0-record-check.json`, 2.6 s). Its own scope statement is repeated in that output:
  no source, binary or original-execution provenance verification. It is not the checker $Q$.

## 2. What the saved run actually did (read from its logs)
- `covrun`: `checked151744086 centers249878`, `completed_write`.
- Stage A: 62,470 + 62,470 + 62,469 + 62,469 = 249,878 centres, `failedBalls0` in all four shards;
  coarse records 764/774/757/788; mid 600; fine 22,379 in 88 batches.
- Initial C: done 22,379, bad 163, **graph 0**, cap 163 (15 batches), overflow 0, cluster failure 0.
  Fallback final C: done 1,127 over four modulo-4 parts, bad 0, graph 0, cap 0.
- Meaning of `graph`: in `negative()` the counter is `stats.positive`, incremented only when
  `g.candidate()` returns true and `gaveup` is false. It is **not** the number of graph searches.
  Therefore "graph 0" does not say graphs were absent; it says no completed search ended in
  "pattern possible". Categories must be measured per record, which is what §3 does.
- Proposition 6.9 has exactly two negative paths: an empty completed bin layer, or a completed
  negative graph search (Lemma 6.8, mode-1 `graph::exist`, cap 5,000,000 steps). A capped record is
  *unresolved*, not negative, and enters the fallback chain. Consequently the exclusions a
  certificate must justify never include a capped search: initial caps are replaced by refined
  records, and the final pass has zero caps.

## 3. Replay and instrumentation on this VM
- Stock build reused from `.scratch/gh/build/` (built from the fetched sources with upstream
  `build.sh`; gcc 16.2.0). Worst batch `f52` (256 records, 29 capped) replayed with the recorded
  argv `12 4 1 .042 1 1 5000000 0 1`: `result done256 bad29 (graph0 cap29 over0 cluster0)`,
  30.64 s wall, and `bad52.out.bin` is **byte-identical** to the shipped `batches/bad52.bin`.
- Output-only probe build: `.scratch/h0/instr/crun-probe` (same sources plus `recProbe` calls in
  `negative()`; no arithmetic or control-flow edits). On `f52` it reproduces stdout counters and
  the same bad file, and emits one line per record:
  `REC index category bins B balls B O n U m steps s`.
- Full probe sweep (88 batches + four final parts): `.scratch/h0/runs/probe-all/`, aggregated by
  `src/report/h0_stagec_stats.py` into `certdata/runs/h0-stagec-probe.json`.
- Per-command bad outputs are compared with the shipped files; see that JSON and
  `certdata/runs/h0-stagec-replay-report.md` (written after the sweep).

## 4. Arithmetic feasibility (micro-benchmark only)
`src/kernel/bench_h0.py` → `src/kernel/bench_h0.json`. Binary64 baseline 2.65 µs/pair for the
recorded 151,744,086 pairs; gmpy2 exact `mpq` gap arithmetic 0.68 µs/pair (~103 s if applied to
every pair, single core); 100-bit MPFR cosine 0.92 µs/eval; mpmath at 40 dps 14.9 µs/eval. These
are stand-in loops, not validated predicates, but they remove "exact arithmetic is obviously too
slow" as a blocker for the seed stage. Kernel correctness remains H1 work; no GMP/MPFR development
headers are installed, while Python 3.12 has gmpy2 2.3.1 and mpmath 1.3.0.

## 5. Draft specs and swarm
- `cert/spec/statement.md` v0 (target statement, trusted base, accept/reject/unresolved vocabulary).
- `cert/spec/arithmetic.md` v0 (rationals + ≥100-bit outward intervals, undecided-is-never-a-verdict).
- Q4 swarm `smwguhf32`, six members, six distinct directions: end-to-end measurement/route spec;
  Lean-reflection route; criterion-correctness audit; search-free graph-invariant certificates;
  positive controls for the branching search; precision/padding monotonicity. Its submissions are
  judged separately; no member result is asserted in this file until accepted.
- Shared lead note with paths and findings: `certdata/upstream/LEAD-H0.md`.

## 6. Route analysis and gate input (complete, 21:05 UTC)

### Verified full-run measurements
`certdata/runs/h0-stagec-replay-report.md` is the short report; the full data is
`certdata/runs/h0-stagec-probe.json`. All 92 commands reproduced their recorded counters and exit
statuses; **all 92 bad-record outputs are byte-identical**, with no differences. There are exactly
23,343 completed negative graph searches and 163 cap outcomes; no empty-layer exclusions, positives,
overflows or cluster failures. Completed searches total 2,932,018,956 steps (median 38,453, maximum
4,986,110). Their graphs need 350,022,800 bytes for raw O+U adjacency alone.

### Recommended Stage-C route: (a)
Use **per-record ball/graph data plus an independent complete checker** as the default. Evidence:
a complete floating-point replay is order 40 CPU-min (contended run; not a clean CPU benchmark), the
certificate's raw adjacency is ~350 MB, and both accepted swarm reports recommend this route after
independent checks. Do not adopt DRAT as the default: at 30–60 bytes per completed-search node it is
an estimated 88–176 GB before encoding/checking overhead, while saying nothing about the geometric
predicates. A trace or proof log remains an optional independent recheck for selected hard records.

The exact-arithmetic cost is **not settled**. Accepted kernel extrapolations range from order 1 to
30 CPU-hours; the lead's rerun of one loaded benchmark moved its headline estimate from 23 to 29
CPU-hours. G0 should therefore approve an end-to-end exact Stage-C pilot on a small stratified sample
before promising full-run time. This is a cost risk, not a demonstrated soundness obstruction.

Keep the archived fallback path as the baseline certificate composition. The separately measured
higher-cap direct exclusion of all 163 parents is useful redundancy and may simplify a later version,
but it is a different execution and cannot silently replace the recorded chain.

### What G0 can honestly approve
- **GO for H1**: seed-stage end-to-end certificate, integrated per-stage schemas, mutation harness and
  a small exact Stage-C pilot; the feasibility obstruction feared in the plan was not found.
- Stage-C direction: route (a), with optional proof/trace checking only as auxiliary assurance.
- Draft trust model and arithmetic contract: `cert/spec/statement.md`, `cert/spec/arithmetic.md`.

### What G0 must NOT claim
- No exact checker has been implemented; no numerical exclusion has been re-certified in exact
  arithmetic. All replay verdicts are floating-point measurements of the upstream algorithm.
- Schemas are **v0 drafts, not frozen**. Two detailed Stage-C proposals exist and must be reconciled;
  other stages' schemas are not yet written.
- Predicate fidelity to (6.16)/(6.20)/(6.21)/(6.23), Lemma 6.7, Stage A/B, and the global assembly
  remain open. The accepted Lean theorem covers only the abstract combinatorial reduction.
- Four swarm directions (end-to-end spec, Lean reflection, invariant certificates, precision padding)
  are still running and are not assumed here. Their findings may refine, but are not prerequisites
  for, the recommendation above.

### Suggested human gate decision
Approve H1 with (i) route (a) as the design default, (ii) an exact Stage-C pilot capped at a named
compute budget before full deployment, and (iii) a requirement to freeze integrated schemas v1 at the
H1 gate. Q3's authorised six-member Root/atlas swarm remains held until H2, as originally scoped.

## 5b. Accepted swarm contribution (Q4/m6, direction d3)
`work/02-checker/reports/H0-stageC-criterion.md` and
`work/04-lean/Mub6/StageCNecessity.lean`. Independently compiled by the lead both in the swarm
directory and after adoption (Lean 4.33.1, direct `lean`, exit 0); axioms only
`propext, Classical.choice, Quot.sound`. It machine-checks the abstract reduction: diameter-separated
ball labels + over-approximating O/U graphs + no (6.24) pattern => no two further bases. The numeric
conversion `s < .1` to the diameter hypothesis is numerical, not formalised. Earlier review rejected
two reporting errors; the revised version fixes the one-record `k=0` exception and charges DRAT costs
only to the 23,343 completed negative searches, not to capped/unresolved records. Accepted with
route costs explicitly labelled estimates; numeric filters, Lemma 6.7 and Stages A/B remain open.

## 5c. Second accepted swarm contribution (Q4/m1, direction d5)
`work/02-checker/reports/H0-stageC-search-controls.md`; harness and recorded output copied to
`work/02-checker/tests/stageC/`. Lead reran the controls and the four definitional Python checks, and
parsed both hard-record logs: all 163 initial cap records complete negatively with cap 2e8,
1,925,134,199 total steps, maximum 39,968,282, no give-up. 400/400 small random cases and 54/54
planted production-scale controls pass. A constructed U self-loop makes the search accept a
non-disjoint pseudo-pattern, so loop-free adjacency is a required certificate invariant, not an
optional assertion. The binary64 route-(a) measurement (~46 CPU-min) and interval-kernel
extrapolations (~23 CPU-h in the member's run, ~29 CPU-h in the lead's loaded rerun) are distinct;
the latter is not an end-to-end exact-checker measurement and is not a validated interval kernel.
Two accepted reports independently favour route (a): graph data plus independent complete checking,
rather than DRAT as the default.
