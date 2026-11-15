# H0 / Q4 — Stage-C coverage and partition audit (direction d6)

Author: m2 (swarm smwgx104w). Scope: **coverage and partition only** — whether the archived
Stage-C run's record set is a complete, non-overlapping, uniquely identifiable cover of its
input, and what the *composition* (cover) layer costs to certify. The predicate arithmetic
(6.16)/(6.20)/(6.21)/(6.23) is d2's and d4's; the Lean reflection is d5's; the compact
search certificate is d3's; the byte schema is d1's. Every number below is produced by a
script in this directory or is a counter quoted from the archived run with its file named.

All work is on the archived tree
`.scratch/h0/dl/verification/saved-run/execution/` and on the lead's census
`certdata/runs/h0-stagec-probe.json`. Nothing in the archived tree was modified; the
re-executions ran in this directory on copies or on read-only inputs.

---

## 0. Bottom line

1. **The Stage-C record set is a verified partition of its input, byte for byte, with one
   systematic and conservative field rewrite.** `batches/f0..f87` are an order-preserving
   copy of `data/fine.bin`: 22,379 records, **0** differences in all fields except the final
   radius `double`, which is replaced by the pass target `0.016` in all 22,379 (the atlas
   radius stored in `fine.bin` is strictly smaller; worst-case slack `9.4188e-8`). `fb1.bin`
   is 1,127 records whose stored radii are all `< 0.011` (worst-case slack `1.8892e-7`).
2. **The 163 unresolved records are identified exactly**, not as a set difference: the 15
   non-empty `batches/bad<k>.bin` files are byte-identical to the batch records at the
   positions the replay reports as `cap`, the records are pairwise distinct (all 22,379
   signatures distinct in `fine.bin`), and the return codes agree on all 88 initial commands.
   `coverage-manifest.json` lists the 163 with `(batch, index, fine.bin byte offset, sha256)`
   and the 1,127 fallback records with `(fb1 index, byte offset, radius, sha256)`.
3. **The archived fallback stream reproduces exactly.** A fresh compile of the archived
   `stageB.cpp` run on the 15 bad files with `.011 .0038` produces `fb1.bin`
   **byte-identically** (sha256 `ef85ec73…`), with identical counters, in 4.93 s.
4. **The load-bearing gap is the cover map, and it is now measured.** The 163 capped records
   are excluded only through the 1,127 fallback balls, and the archive stores no parent→child
   relation. Instrumenting a copy of the refiner recovers it: 163 parents all fully refined
   (3,161 inside cells each = 515,243 total, matching the producer counter exactly), 1,127
   children created, but **11,838 covering incidences**, of which **90.5 % are inherited from
   children created for *earlier* parents** (median 71 children per parent, max 161; only
   4 of the 163 parents use no inherited child at all). A per-capped-record "its own
   children" list would be wrong for the other 159.
5. **The whole cover/composition layer is a 3.215e8-cell obligation, and nothing in the
   archive witnesses it.** Producer counters, all reproduced by my independent lattice model
   to the last cell: Bmid 1.7795e8 cells, Bfine 1.4305e8, fallback 5.152e5. Route (a) as
   currently specified (per-record Stage-C graphs) does not touch this layer. Re-deriving it
   at the measured rate costs ≈35–55 CPU-min; storing the maps at 2 B/incidence costs
   ≈0.2–2 MB. This is the largest item missing from "ball/graph data + independent complete
   checker", and it is spent before the Stage-C graph checker starts.

---

## 1. What the 92 commands must discharge

The criterion document (`work/02-checker/reports/H0-stageC-criterion.md` §1, §5 obligation 9)
splits the Stage-C argument into H1 cover, H2 diameter, H3 over-approximation of the graphs,
H4 no-pattern search, and then a *global* composition step: every record of a Stage-B output
is either `EXCLUDED` or covered by fallback records that are all `EXCLUDED`, with the
`(offset, parts)` partition covering each input record exactly once. The 92 commands
(88 `C.batch<k>` + 4 `C.final<p>`) are the only execution behind both H4 and the composition:

| layer | obligation | data the run leaves behind |
|---|---|---|
| partition of input | each record of `fine.bin` processed once, by one command | batch files + `parts` rule + counters |
| H4 per record | no (6.24) pattern in the recovered `(O,U)` | steps + tri-state (bad file membership) |
| cover (H1) | the balls cover the admissible region | **only aggregate counters** |
| composition | the 163 unresolved records are covered by the 1,127 fallback balls | **nothing per parent** |

This audit checks the first two exactly, the third and fourth up to what the archive contains,
and measures the missing part.

---

## 2. Method and artefacts

`recparse.py` — an independent parser of the record layout
(`atlas.cpp:191-215`: `uint64 count`, then `int32 k`, `36` doubles, `k×36` doubles, `8`
doubles = `356+288k` bytes), refusing trailing bytes. Every file parses to its exact length,
so all counts below are forced by the bytes, not inferred.

| file | role |
|---|---|
| `coverage_audit.py` → `coverage-report.json` | tests T1–T12; 9.4 s |
| `coverage_manifest.py` → `coverage-manifest.json` | the 163 + 1,127 records with provenance and hashes |
| `partition_probe.py` → `partition-probe-result.json`, `subset5.bin` | re-execution that fixes the four-way partition convention on 5 records |
| `instrB/` (copy of `stageB.cpp`, `atlas.cpp`, `patchx.cpp`, `ub.cpp`, `seed.cpp` + one output-only probe) → `build/brun-cov` | recovers the fallback cover map; output byte-identical to the archive |
| `pcov.log`, `pcov-summary.json`, `pcov-sample20.json`, `fb1-rerun.bin`, `fb1-cov.bin` | its raw results |
| `composition_cover_map.py` → `composition-cover-map.json` | the recovered map in embeddable form: 163 parent entries with their covering `fb1` indices, 1,127 child entries, metric parameters |
| `upstream-check_records.out` | the upstream tree's own checker, executed |
| `census_arithmetic.py` → `census-check.json` | independent recomputation of the census aggregates and of the fallback parent order |
| `coverage_audit_v1.py` | first (superseded) version of the audit; kept because the report's T1–T7 wording follows it |

Stream hashes (`coverage-manifest.json`): `fine.bin` `9b5b743b…`, `fb1.bin` `ef85ec73…`
(1,699,524 B), `fine.bin` 33,746,388 B, lead probe binary `crun-probe` `2500d0ac…`.

---

## 3. Partition audit — results

All twelve tests pass (`coverage-report.json:summary.all_ok = true`), and both added census
checks C13/C14 agree (`census-check.json`).

| # | claim | measured |
|---|---|---|
| T1 | every record file parses exactly; counts | 87 batches × 256 + 1 × 107 = 22,379; `fine.bin` = 8 + 22,378·1508 + 356 = 33,746,388 B; `fb1.bin` = 8 + 1,127·1508 |
| T2 | batches are an order-preserving copy of `fine.bin` | 22,379 records; **0** non-radius field differences; **0** radius equalities; batch radius = 0.016 in all |
| T3 | bad files = the 163 capped records | 15 non-empty bad files, 163 records, all byte-identical to `f<k>.bin` at the replay's cap positions; 163 unique |
| T4 | verdict ↔ return code | rc 1 ⇔ bad non-empty ⇔ cap>0 on all 15; rc 0 elsewhere; rc ∈ {0,1} only |
| T5 | the four `C.final` parts partition `fb1.bin` | residue classes of `i mod 4` = 282/282/282/281 = 1,127, disjoint, union complete |
| T6 | fallback input = the capped set | `C.Bfallback` argv reads exactly the 15 non-empty bad files; `fb1bad.bin` and all four `fb1cbad<p>.bin` have 0 records |
| T7 | producer's marker | `batches/fdone.txt` = `88 22379` = (batches, records) |
| T8 | replay counters = archived logs | 92/92 Stage-C commands identical in done/bad/graph/cap/over/cluster |
| T9 | no duplicate or shared records | 22,379 distinct signatures in `fine.bin`, 1,127 in `fb1.bin`, 0 overlap |
| T10 | radius accounting | see §4 |
| T11 | cover ledger | see §6 |
| T12 | one parameter set | all 92 commands: `12 4 1 .042 1 1 5000000`; initial `part=0 parts=1`; final `parts=4 part=0..3`; single binary `./build/crun` |
| C13 | census aggregates recomputed per record | steps 2,932,018,956; pairs 622,704,036; adjacency 350,022,800 B; `O+U` 357,191,053 — all four equal the probe summary; **0** records with `O+U > C(B,2)`; all 163 caps at exactly 5,000,001 steps |
| C14 | fallback parent order is determined | all 163 bad records have `k=4` and stored radius exactly `0.016`, so `stable_sort` (decreasing radius) preserves argv order; the 15 files are passed in ASCII order `bad10 < bad3 < … < bad84`, each in record order |

Consequences that matter for a certificate:

* The tri-state is not recoverable from the archived records alone — it is `bad`-file
  membership — but it *is* pinned to specific records by T3+T9, so a certificate can be built
  from the archive with no re-run.
* The replay census stores a **per-command positional index** (`recIndex++` in
  `stageC.cpp`), not the global record index. For the initial pass (parts = 1) position is
  order, which T3 confirms on 163 records; for the four final parts the convention is the
  source rule `(offset+i) % parts == part`, which T5 confirms only at the level of counts.
  `partition_probe.py` closes that: for each part, the cheapest record whose
  `(bins, balls, O, U, steps)` fingerprint is unique in all 23,506 census rows, plus the
  heaviest fallback record, were extracted and re-run with `parts=1`. All five fingerprints
  reproduce the predicted `(part, local)` census line — including global 739 ↔ `final3`
  local 185 at 3,200,276 steps. (`subset5.bin`, `partition-probe-result.json`.)
* Exit status is a weak signal: `main` returns `bad.empty()?0:1`, and `validate` **aborts**
  rather than returning a verdict, so a crash would also be nonzero. No command has a
  return code outside {0,1} and every one is `completed: true`, so nothing was lost here —
  but a certificate must not let an aborted batch read as "no bad records".

The upstream tree's own consistency checker (`execution/check_records.py`, which the earlier
report lists as *not executed*) runs clean on the archived tree in 2.8 s, with the same
partition facts: `batches: 88`, `initial_C {done 22379, bad 163, cap 163}`,
`fallback_records 1127`, `final_C 282/282/282/281 bad 0`
(`upstream-check_records.out`). Its batch test is exactly T2's rule
(`record[:-8] == original[:-8] and record[-8:] == pack(.016)`), and its Stage-B test accepts
the refiner's own `parent` counter as the parent-coverage claim — which is the gap in §5.

C13 re-derives, from the per-record census rows alone, the four aggregates that the swarm's
cost arguments quote (route (a)'s 350,022,800 B adjacency and 2.932e9 steps, d3's baseline):
all four agree with `h0-stagec-probe-summary.json`, and `O+U <= C(balls,2)` holds record by
record. C14 matters for reproducibility of the cover map: because every capped record carries
exactly the pass radius, the refiner's `stable_sort` by decreasing radius is a no-op on ties,
so parent order = `C.Bfallback` argv order = ASCII order of the fifteen file names. That is
what makes the measured map in §5 reproducible at all.

---

## 4. The radius field: two radii in circulation, and which one a cover recheck needs

`emit()` in `stageB.cpp` copies each atlas entry into a batch file and overwrites
`z.radius := target` before writing; the atlas stream (`fine.bin`, `fb1.bin`) keeps the
radius the refiner computed. Measured (T10):

| stream | stored radius min | stored radius max | target | worst-case slack | records at target |
|---|---|---|---|---|---|
| `fine.bin` (22,379) | 7.773430893866114e-08 | 0.015999905811574015 | 0.016 | 9.418842598571397e-08 | 0 |
| `fb1.bin` (1,127) | 0.0038419284681657086 | 0.010999811083611326 | 0.011 | 1.8891638867320204e-07 | 0 |

All 22,379 (resp. 1,127) radii are distinct. The rewrite is *conservative* for Stage C: a
larger record radius widens the (6.7) thresholds and `rH`, which retains more bins and more
edges, never fewer.

It is **not** conservative, and not valid, to use `0.016` when re-checking the refiner's own
cover. The refiner's cell lattice uses `E = sqrt(1+ort)*R + 1e-7` with `R` the parent's
*stored* radius; my lattice model reproduces the producer's `base`/`inside` counters to the
last cell only when the stored (atlas) radii are used (§6). A checker that took the batch
radius would be checking a different, larger region than the one the refiner covered. The
certificate therefore needs **both** radii per record (`atlas_radius`, `pass_radius`) and a
statement of which layer uses which.

---

## 5. The cover map: what is missing, and what it measures

The 163 capped records are not excluded by their own graphs; they are excluded because
`C.Bfallback` refines their boxes into 1,127 balls at radius `.011`, and each of those balls
was excluded by `C.final`. The certificate must show that the 1,127 balls cover the 163
boxes. The archive contains no such relation, and it is not recoverable from record content:

* all 1,127 fallback records have **distinct** tangent bases `T`, and **none** of them equals
  any capped record's `T` even up to a global sign (0 of 1,127): children are re-snapped by
  `buildH::snap`/`patch`, so the parent's `T` is not carried over. (I did not test `T` under
  the 6×6 row/column permutation of `mapH`; the source builds `T` afresh from the new
  Hadamard, and the distance test below fails independently.)
* the nearest-parent distance in the wrapped 36-phase metric is not separating: median
  0.0237, 292 of 1,127 children lie further than 0.1 from every capped centre, and 31
  capped records are not the nearest parent of any child. Content matching fails.

Instrumenting a **copy** of the refiner (output-only probe in `instrB/stageB.cpp`, no
arithmetic change; the instrumented binary reproduces `fb1.bin` byte-identically) on the same
15 inputs (`pcov.log`, summary in `pcov-summary.json`):

| quantity | measured |
|---|---|
| parents | 163, all `ok` (fully refined), `fail 0`, `split 0` |
| inside cells per parent | 3,161 (identical for all 163), total **515,243** = producer `inside` |
| cells closed by the snap path rather than a relation mark | 7 (all 163 parents: 515,236 marks vs 515,243 inside; 7 parents with one such cell each) |
| children created | 1,127 = the atlas size (no pre-existing entries) |
| **parent→child covering incidences** | **11,838** (min 2, median 71, mean 72.6, max 161 per parent) |
| inherited incidences (child created by an earlier parent) | **10,711 = 90.5 %** |
| parents covered only by their own children | 4 of 163 |
| map size at 2 B per incidence | 23,676 B |

So "the capped record's own refined balls cover it" is false in general; the atlas is global
and 90 % of a parent's cover comes from other parents' balls. A certificate must carry the
*covering* map, not the creation map. The map is exported ready to embed in
`composition-cover-map.json` (163 parent entries with their `fb1` index lists, 1,127 child
entries, and the metric parameters). Its reverse side: every one of the 1,127 children covers
at least one parent, median 8, maximum 41 — no child is redundant, and a certificate that
listed only "a few balls per capped record" would be wrong in both directions.

The same measurement on the two larger stages is out of the time budget for a full run, so a
20-parent sample of the fine stage was run instead (`pcov-sample20.json`; first 20 records of
`mid.bin`, `w=.005`, target `.016`, 40.8 s CPU): 8,107 children created, 43,824 covering
incidences, 35,717 inherited (81.5 %), 240,497 inside cells per parent, median 2,681 children
used per parent. The sample is in file order, not the run's `stable_sort` order, so it
*under*-states the inheritance available in the 600-parent run; the full fine-stage map is
therefore larger than 43,824 incidences and at most of order 10^6 (≈2 MB at 2 B/incidence).
Only the fallback map (23.7 KB) is measured exactly.

---

## 6. The cover ledger, and what it costs to make checkable

Producer terminal counters (cleaned logs in `execution/results/`), with my independent
reproduction of `base`/`inside` from the parent radii and the refiner's lattice
(`E = sqrt(1+ort)*R+1e-7`, `w` per stage, `L = ceil(E/w+.500001)`, `naxis = 2L+1`,
`inside = #{cells : Σ_a max(0,|u_a|-w/2-1e-8)² ≤ E²}`):

| stage | parents | base cells | inside cells | snaps | fail | output | my reproduction |
|---|---|---|---|---|---|---|---|
| A (`covrun`) | 112 cells | — | 151,744,086 pairs checked | — | 0 | 249,878 centres | not recomputed |
| A (`arun` ×4) | 249,878 | — | — | — | 0 | coarse 764+774+757+788 = 3,083 | `failedBalls0`, done 62,470/62,470/62,469/62,469 |
| Bmid | 3,083 | 857,190,043 | 177,954,483 | 1,197,104 | 0 | `mid.bin` 600 | base ✔ inside ✔ |
| Bfine | 600 | 550,650,008 | 143,050,072 | 716,765 | 0 | `fine.bin` 22,379 | base ✔ inside ✔ |
| C.initial | 22,379 | — | — | — | — | 22,216 excluded, 163 cap | T3/T4/T8 |
| C.fallback | 163 | 2,386,483 | 515,243 | 17,207 | 0 | `fb1.bin` 1,127 | base ✔ inside ✔ |
| C.final | 1,127 | — | — | — | 0 | all excluded | T5/T8 |

Totals over the refiner stages: **1,410,226,534** base cell slots, **321,519,798** inside-cell
obligations, 1,931,076 snaps, 27,760,370 successful relation inits — each of these an
operation a cover checker must perform or store.

Cost of re-deriving the witnesses (labels: measured rate, then extrapolation):

* measured: the fallback stage (2,386,483 base cells, 515,243 inside, 69,714 pair inits,
  17,207 snaps) runs in **5.49 s CPU** (`brun-cov`, `time` user; the un-probed build 4.93 s
  wall);
* measured: 20 of the 600 fine parents in **40.8 s CPU** (`pcov-sample20.json`);
* extrapolated from those rates: fine ≈ 20 min, mid ≈ 30–33 min, **total ≈ 35–55 CPU-min**
  for all 321.5M cell checks — the same order as route (a)'s whole Stage-C checker
  (10–40 CPU-min in double arithmetic per the criterion report), and it is work route (a)
  does not include.

Storage alternative: keep the covering maps instead of re-deriving. Fallback 23,676 B at
2 B/incidence (measured); fine and mid are not measured but bounded by the sample and by the
child counts — order 10^5–10^6 and 10^4–10^5 incidences respectively, i.e. well under 2 MB
together. Either way the checker needs the refiner's relation algebra (`relationB::init/eval`,
`corner`) — ~50 lines of arithmetic, and the only piece of Stage B that a Stage-C certificate
currently leaves on trust.

For comparison, the other candidate route to H1 — per-ball bin membership lists, the
Lemma 6.4 check of criterion §5 step 5 — needs the last-layer bin index of every bin in every
ball: the census reports 485,599,722 final-layer bins over the 23,506 records, i.e. ~1–2 GB at
2–4 B per index. The cell route (0.5e6–1e6 stored incidences) is the cheaper of the two.

---

## 7. Reproducibility runs

1. **The fallback stream.** `build/brun .011 .0038 fb1-rerun.bin fb1bad-rerun.bin - <15 bad
   files>` (compiled from the archived source with `g++ -std=gnu++17 -O3 -march=native
   -ffp-contract=off`, this VM's gcc 16.2.0) → `fb1-rerun.bin` is byte-identical to
   `data/fb1.bin` (sha256 `ef85ec73…`), `fb1bad-rerun.bin` empty, terminal counters identical
   (`parent163 base2386483 inside515243 live17207 split0 snaps17207 bad0 fail0
   pair69714/3039760 marks515236`), 4.93 s wall.
2. **The four-way partition.** Five records extracted by fingerprint uniqueness and re-run
   with `parts=1` reproduce the census fingerprints at the predicted `(part, local)` positions
   (§3; `partition-probe-result.json:ok = true`). A deliberately wrong pick (a capped initial
   record instead of the heaviest fallback record) was rejected by the same test before it was
   fixed, so the test has teeth.
3. **The upstream checker.** `python3 check_records.py .` → `PASS within numerical consistency
   scope` in 2.8 s (`upstream-check_records.out`).

---

## 8. Answers to the G0 feasibility questions in this direction

* **Is the Stage-C record census a complete, non-overlapping cover of its input?** Yes at
  byte level, with the radius rewrite of §4, and up to the `parts` convention which is
  verified by construction (initial) and by fingerprint re-execution (final).
* **Can the unresolved set be identified without re-running the solver?** Yes. 163 records,
  enumerated in `coverage-manifest.json`, each tied to a batch, an index, a byte offset in
  `fine.bin` and a SHA-256; uniquely because every `fine.bin` signature is distinct.
* **Is the fallback chain checkable from the archive?** No — only at counter level
  (163 parents processed, 0 failures, 1,127 children all excluded). The per-parent cover is
  absent and is not recoverable from record content; it is recoverable by an instrumented
  re-run (§5), and its exact size is 11,838 incidences.
* **What does the composition layer cost?** 321,519,798 inside-cell obligations; ≈35–55
  CPU-min to re-derive, or <2 MB to store as covering maps; both need the refiner's relation
  arithmetic in the checker.
* **Does the archived data reproduce?** For the fallback stream, byte-identically, in 4.93 s.

---

## 9. What was NOT verified

* **No Stage-C predicate.** I did not re-evaluate (6.16)/(6.20)/(6.21)/(6.23), the clustering
  radii, or the search; the 23,343 completed negatives are taken as the census states them.
  Nothing here bears on the fidelity question (d2, d4) or on the search's completeness (d3, d5).
* **The refiner's inequality.** My instrumented run *is* the producer's arithmetic; it
  establishes the cover map and reproduces the producer's `fail 0`, not that `relationB::eval`
  is a correct cover bound. That remains an unverified 50-line numeric core.
* **Stage A.** `covrun`'s 151,744,086 pair tests and the 249,878-centre cover were not
  re-derived; only the archived counters are quoted.
* **The Bmid/Bfine cover maps** are not measured, only bounded by a 20-parent sample and
  extrapolation.
* **Provenance.** I did not re-fetch the upstream tree or check hashes against the public
  repository; I used the local archive as given. The probe's equality with the archived run is
  established by the lead's byte-compare and cross-checked here only at counter level (T8).
* **Compiler identity.** The re-executions use this VM's `g++ 16.2.0` with `-march=native`;
  the archived binaries' compiler is unknown. Byte-identical output is strong evidence, not a
  proof of build identity, and the `-march=native` binary is VM-specific.
* **The 7-cell bookkeeping residue** (`marks` 515,236 vs `inside` 515,243) is reported, not
  explained: consistent with cells closed by the snap path after a corner-tolerance
  mismatch, but I did not trace them. It is 1.4e-5 of the cells and does not affect
  `remaining == 0`.

---

## 10. Recommendations for schema v1 (interface with d1)

1. Every verdict carries `(stream, global_index, byte_offset)` or `(batch, index)`. The
   recorded census index is per-command and positional; without this, a tri-state verdict
   cannot be attached to a record without re-deriving the `parts` rule.
2. Every record carries **both** radii: `atlas_radius` (what the refiner's cover was computed
   at) and `pass_radius` (`.016` / `.011`, the Stage-C envelope). Measured envelope slack:
   ≥ `9.418842598571397e-08` and ≥ `1.8891638867320204e-07`.
3. A `composition` section per capped record: the list of *covering* fallback record indices
   (11,838 incidences for this run; 23,676 B at 2 B) and the cover metric
   `(w, E, cell lattice)`; not the creation list.
4. A `cover_counters` section per parent-record: `base`, `inside`, `snaps`, `fail`, so a
   checker can compare its own lattice arithmetic against the producer's before trusting it —
   exactly the check that reproduced 857,190,043 / 177,954,483, 550,650,008 / 143,050,072 and
   2,386,483 / 515,243 here.
5. State the verdict semantics of exit status: `1 = bad non-empty`, and a crash is also
   nonzero; `EXCLUDED` must require a complete search and `cap_hit = false` (criterion §7.1),
   which the archive supports only through the bad-file membership plus the `steps` census.

---

## 11. Reproduce

```
python3 coverage_audit.py          # T1-T12 -> coverage-report.json (9.4 s)
python3 coverage_manifest.py       # 163 + 1127 records -> coverage-manifest.json
python3 census_arithmetic.py       # C13/C14 -> census-check.json (0.1 s)
python3 composition_cover_map.py   # pcov.log -> composition-cover-map.json (0.2 s)
python3 partition_probe.py         # 5-record partition re-execution (0.2 s + crun-probe)
g++ -std=gnu++17 -O3 -march=native -ffp-contract=off instrB/stageB.cpp -o build/brun-cov
./build/brun-cov .011 .0038 fb1-cov.bin fb1bad-cov.bin - \
  <execution>/data/batches/bad{10,3,4,5,52,53,55,56,6,7,78,79,8,80,84}.bin 2> pcov.log
( cd <execution> && python3 check_records.py . )
```

`<execution>` = `.scratch/h0/dl/verification/saved-run/execution` (read-only use).
