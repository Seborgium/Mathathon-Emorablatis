# H0 Stage-C, direction 3 — Lean reflection of the graph predicate (L3): measured go/no-go

Author: m3, swarm smwgx104w, direction d5. Scope: the **graph predicate only** (layer L3 of
`work/02-checker/reports/H0-stageC-criterion.md` §1: "no (6.24) pattern"), not the numeric
predicates (6.16)/(6.20)/(6.21)/(6.23) and not Stage-B/A.

## 0. Verdict

**Kernel reflection is real but does not scale to the run; it is usable as a sampled cross-check.**
A complete Lean development is here: the (6.24) search is executable, its *completeness* is proved
(`HasPattern → search = true`, hence `search = false → ¬HasPattern`), and it compiles with the
standard axioms only. On real records:

| record | balls | C steps | Lean native (compiled) | Lean kernel (`decide`) | C, whole record |
|---|---|---|---|---|---|
| C_min | 49 | 157 | finishes (<0.5 s) | **passes**, ≈4.5 s over the import baseline | 0.02 s |
| D_first | 212 | 19,762 | finishes (~1–2 s) | **> 200 s** (killed) | 0.14 s |
| A_med (median steps) | 190 | 38,453 | ≈1.8 s per search | not attempted | 0.12 s |
| E_fb (fallback) | 180 | 567,598 | **> 200 s** (killed) | not attempted | 0.10 s |
| B_heavy (max steps) | 285 | 4,986,110 | **> 120 s** (killed) | not attempted | 0.26 s |

* **Kernel route:** at the measured factor (a 49-ball / 157-step record costs ≈4.5 s of kernel
  reduction, i.e. ≈29 ms per search step) the 2.932e9 steps of the 23,343 completed negatives cost
  ~2.4e7 CPU-s ≈ 275 CPU-days. **Not viable**, not even for the heavy tail.
* **Native route:** the faithful port is ≈50 µs/step where C is ≈0.26 µs/step, and the gap grows on
  the dense records (E_fb, B_heavy do not finish in minutes although C needs 0.1–0.26 s). At the
  measured A_med rate the run would be ≈40 CPU-h *if* it scaled, which it does not; measured cases
  exceed that. **Not competitive with route (a)'s 0.5–6 CPU-h** (criterion report §4.2).
* **What it does buy:** a kernel-checked, axiom-clean certificate of L3 for small records
  (C_min class), i.e. the "route (c)" sample that criterion report §4.4 proposed as a companion.
  The proof is the reusable part: it removes the search algorithm itself from the trusted base,
  leaving the adjacency input.

## 1. Artefacts (all under `.ultramath/smwgx104w/m3/`)

| file | content |
|---|---|
| `lean/StageCGraph.lean` | definitions + `search_complete` + `no_pattern_of_search_false`; compiles, no `sorry`, axioms `[propext, Classical.choice, Quot.sound]` |
| `lean/RecData_<rec>.lean` | adjacency of 5 real records as `Nat` bit matrices (`bit x*n+y` = relation x→y) + `cSteps` |
| `lean/Check_C_min.lean` | the certificate idiom on a real record: `¬ HasPattern C_min.O C_min.U`, kernel `decide` |
| `lean/Check_{D_first,A_med,E_fb,B_heavy}.lean` | same script for the other records |
| `lean/Native_*.lean`, `lean/Timing*.lean`, `lean/Count*.lean` | compiled-timing and node-count harness |
| `lean/Sanity.lean` | controls: synthetic 12-vertex graph with a (6.24) pattern ⇒ `search = true`; same graph with one cross-U edge deleted ⇒ `search = false` and `¬HasPattern` |
| `instr/` | my own copy of `.scratch/h0/instr/*.cpp`, patched to dump ball adjacency (`DUMP_PATH`), built as `instr/crun-dump` |
| `data/extract.py`, `data/graph_*.txt`, `data/*.bin` | single-record extraction from the upstream archives and the dumps |
| `gen_data.py` | dump → Lean literal |

Reproduce (from `lean/`, `export LEAN_PATH=.:$LEAN_PATH`):

```
lean -o StageCGraph.olean StageCGraph.lean          # ~10 s
lean -o RecData_C_min.olean RecData_C_min.lean
lean Check_C_min.lean                                # kernel-checked certificate
lean Native_A_med.lean                               # compiled evaluation
lean Sanity.lean                                     # positive/negative controls
```

## 2. What is proved

```lean
def HasPattern (O U : Nat → Nat → Bool) : Prop :=
  ∃ a b : List Nat, Clq O a ∧ Clq O b ∧ a.length = 6 ∧ b.length = 6 ∧
    (∀ x ∈ a, ∀ y ∈ b, U x y = true) ∧ (∀ x ∈ a, x ∉ b)          -- a, b nodup 6-cliques of O, U-complete across

theorem search_complete (n : Nat) (O U) (hOut : ∀ x y, (n ≤ x ∨ n ≤ y) → O x y = false)
    (h : HasPattern O U) : search n O U = true
theorem no_pattern_of_search_false ... (h : search n O U = false) : ¬ HasPattern O U
```

`search` mirrors `graph::exist` (`stageC.cpp:433-470`): enumerate a 6-clique `a` of `O` in increasing
index order, keep the U-pool `commonU a`, then ask `clq` (mirror of `graph::clique`) for a 6-clique of
`O` inside the pool. Two of C's prunes are ported and proved neutral for the completeness direction:
`|cands| < k → false`, and `|commonU (A++[v])| < 6 → false` (the `pool.count()<6 continue` of
`stageC.cpp:437`). Disjointness of `a` and `b` is *not* assumed in the program: it follows from
`U x x = false` (no U self-loops), which is why the spec keeps the explicit conjunct and the proof
does not need it (`hUirr` was dropped from the final statement — the `clq` search is over the pool
alone; the spec conjunct is what the paper requires).
Axioms: `propext`, `Classical.choice`, `Quot.sound` — `#print axioms` output in `lean/Axioms.lean`.
**`native_decide` is not used anywhere**, so `Lean.ofReduceBool` is not in any proof; the compiled
evaluations in §4 are measurements, not proofs.

## 3. Data fidelity (checked)

Each sample record was cut from the upstream archive (`data/extract.py`, layout of
`atlas.cpp:191-215`), run through my instrumented dump build of the published source with the same
parameters as the lead probe (`12 4 1 .042 1 1 5000000 0 1`), and the dumped ball count, `|O|`, `|U|`
and step counter were compared with `certdata/runs/h0-stagec-probe.json`:

| label | archive record | balls | O/U | steps | probe JSON entry | match |
|---|---|---|---|---|---|---|
| C_min | `fb1.bin` #461 | 49 | 151/378 | 157 | final0 #116 | exact |
| D_first | `batches/f0.bin` #1 | 212 | 1,944/9,931 | 19,762 | batch0 #1 | exact |
| A_med | `batches/f23.bin` #67 | 190 | 2,184/8,184 | 38,453 | batch23 #67 | exact |
| E_fb | `fb1.bin` #1 | 180 | 3,620/5,452 | 567,598 | final0 #1 | exact |
| B_heavy | `batches/f56.bin` #103 | 285 | 9,530/16,453 | 4,986,110 | batch56 #103 | exact |

So the Lean `search` is evaluated on exactly the adjacency the C run used, and it returns `false` on
all five (agreeing with the recorded `cand 0` / "nopattern"). The first extraction attempt for C_min
took the wrong index (`fb1.bin` #116 instead of #461, because the probe index counts only the shard's
records) and did not match; that mismatch is what identified the correct index, and it is a useful
reminder that probe indices are per-shard, per-process.

## 4. Cost measurements and their basis

* **Baseline noise.** The VM is shared; `import Mathlib` alone took 7–20 s per process during these
  runs. All Lean wall times below include that. `IO.monoNanosNow` proved unusable here (it reported
  390 units for a 1e7-iteration loop), so times are wall-clock of one process minus the measured
  import baseline, or differences between an N-times and a 1-time run.
* **Kernel.** `Check_C_min.lean`: 14.47 s wall, import baseline 9.95 s ⇒ ≈4.5 s for the whole
  kernel-checked certificate of a 157-step record. `Check_D_first.lean` (19,762 steps) hit a 200 s
  timeout after `maxRecDepth` was raised; that is ≈1e4× the C search cost and grows with the record.
* **Native (compiled `#eval`).** C_min 5.41 s and D_first 6.91 s wall, both within the import
  baseline + compilation noise; A_med 13.92 s for one run and 17.55 s for three ⇒ ≈1.8 s per search;
  E_fb > 200 s; B_heavy > 120 s. C, on the *same* records and doing all Stage-B/bin/ball work as
  well, needs 0.02–0.26 s (`/usr/bin/time` on `instr/crun-dump`).
* **Node counts** (`lean/Count.lean`, count of candidate visits, same recursion): C_min 329,
  D_first 2,437, A_med 35,302 versus C's step counters 157 / 19,762 / 38,453. The visit counts are
  the same order as C's, so the slowdown is per-step cost and not (for these records) a different
  tree. E_fb and B_heavy are the exceptions: their trees are much larger than C's, because the port
  does not reproduce C's *early* `clique(pool,6)` prefilter at every level (`stageC.cpp:440`), only
  the two prunes listed in §2.

## 5. What this does NOT establish

1. **Not a Stage-C certificate.** `HasPattern`/`search` say nothing about (6.16)/(6.20)/(6.21)/(6.23);
   the adjacency `O,U` is an *input*. The certificate for a record is conditional on the graphs being
   over-approximations (H3), which is exactly the part this direction does not touch.
2. **Not the run.** Only 5 of 23,343 completed negatives were checked; the extrapolations in §0 are
   labelled as such.
3. **Not a competitive implementation.** The port is list-based; C uses 64-bit masks with O(1)
   intersections and a step cap. A mask-based Lean port could plausibly reach ~1 µs/step (still
   ~4× C) but the proofs would have to be redone for the new data structures, and nothing here
   measures that.
4. **Two records fail.** E_fb and B_heavy do not finish, so the port's *completeness in practice*
   is untested on them; the theorem says the answer is correct if it returns, not that it returns
   quickly.
5. **The kernel-checked instance is tiny.** C_min has 49 balls and 157 steps — a real record, but
   not representative; a "sampled" kernel check of, say, 100 records of that class would cost hours.
6. **No timing of a mask-based `decide`.** The kernel numbers apply to this list implementation only.
7. **Fidelity of the prunes to C.** The two prunes are proved neutral *for the specification*, but
   the port is not a line-by-line transliteration of `graph::exist`: ordering and pool bookkeeping
   differ. Agreement on the five records is test agreement, not a proof of equivalence with the C
   program.

## 6. Implication for route (a)

Route (a) remains the only affordable complete L3 checker. Lean reflection should be scoped exactly
as criterion report §4.4 proposed: route (a) for all 23,343 verdicts, plus Lean (this development)
on a small sample — and, if a trust anchor for the search algorithm is wanted, on the 163
cap-affected records only after they are re-searched and excluded by the fallback pass, since those
are the ones whose C run needed 5e6 steps and whose independence matters most. The kernel cost makes
even that a deliberate choice: at ≈29 ms per search step, a 5000-step record costs ≈2.5 CPU-min of
kernel time, so the sample must be chosen by step count, not at random.
