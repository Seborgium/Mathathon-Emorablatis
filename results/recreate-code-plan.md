# Plan: six agent teams to recreate the dimension-six verification code

Status: **proposal for the owner's decision.** Nothing launched. Supersedes the code arm of
`results/plan.md` (§T2/T3) if approved; see §11 for exactly what it changes.

---

## 0. What changed, and why a recreation is now possible

`results/plan.md` and decision D1 were written on a premise that no longer holds: *"the seven
sources, the execution archive and the certificates are not available."* They are available. Under
`preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/verification/`
in the `openai/math` repository:

| file | lines | bytes | sha256 (first 12) | role |
|---|---|---|---|---|
| `saved-run/compiled-build/source/seed.cpp` | 119 | 3 514 | `3c6c7a709223` | 112-bin triples, `sumok`, `seeds::build/list` |
| `…/ub.cpp` | 386 | 11 557 | `bb0312823400` | complex arithmetic, LDLᵗ, blocks, `Usearch` |
| `…/patchx.cpp` | 473 | 16 137 | `a78a1ab171d8` | `Root`, `buildH`, `Asearch`, spectral bound |
| `…/atlas.cpp` | 241 | 8 821 | `dcbf2dbe1054` | `Atlas`, `CenterList`, binary record I/O, `arun` |
| `…/stageB.cpp` | 336 | 12 030 | `7e609a2f282d` | `refiner`, batching, `brun` |
| `…/stageC.cpp` | 567 | 17 471 | `60a1b1009185` | clique-graph exclusion, `crun` |
| `…/covout.cpp` | 143 | 5 286 | `2a7e6bf5ca48` | `coverSeeds`, writes `centers.txt` |
| `…/abi-fp-probe.cpp` | 51 | 2 496 | (not in manifest) | binary64 + ABI contract probe |
| `compiled-build/build.sh` | 29 | 1 303 | — | build recipe |
| `execution/check_records.py` | 373 | 18 229 | — | the shipped record checker |

The seven mathematical files (2 265 lines) all match the hashes in `verification/code/extraction.json`
— I checked, so "recreate" has an unambiguous object. A copy of the ten files, the 100-command
record and `centers.txt` is cached at `.scratch/gh/` for this session; the programme should re-fetch
from the repository rather than trust that cache.

Three facts about that code shape everything below.

1. **It is one program, textually split.** `stageC.cpp` includes `stageB.cpp` includes `atlas.cpp`
   includes `patchx.cpp` includes `ub.cpp` includes `seed.cpp`; `covout.cpp` includes `seed.cpp` on
   its own. Each file defines the next file's guard (`#define ATLAS_HEADER` at the top of
   `stageB.cpp`) and hides its own `main` behind its own guard. There are four binaries — `covrun`,
   `arun`, `brun`, `crun` — and no shared headers, no separate compilation. Editing "one file" edits
   everything downstream of it.
2. **The record is the interface.** `saveRecords`/`readRecords` in `atlas.cpp` fix the on-disk
   format: `uint64 count`, then per record `int k`, `double p[36]`, `double T[k][36]`, and eight
   doubles `C n0 id ort hor mnorm froot radius`. `readRecords` recomputes `dp` via `finish()`, so the
   file carries `p` and not `dp`. `centers.txt` is ASCII: `112 249878` then one line per centre.
3. **The run is a 100-command DAG, recorded.** `saved-run/execution/commands.json` gives every
   argv, its inputs, outputs and return code: 1 `covrun`, 4 `arun` (parts mod 4), 1 `brun .07 .013`,
   1 `brun .016 .005` (batched at 256), 88 `crun` on batches, 1 `brun .011 .0038` on the 15 bad
   batches, 4 `crun` parts mod 4. 85 commands returned 0, 15 returned 1 — the unresolved ones, all
   inside the fallback chain, none in the final pass.

So a recreation is not a port. It is: **re-derive the seven files so that the 100 recorded commands
produce the 50 MB of recorded artefacts again.**

---

## 1. The decision this plan needs from you first

"Recreate the code files" admits three standards that cost very different amounts and prove
different things. Everything else in this document is written so that the choice is one line.

| mode | what the teams do | what it proves | cost |
|---|---|---|---|
| **A. Clean room** | write from the paper + §0's interface spec, never open the sources | that the prose is sufficient to rebuild the code — the strongest rebuke to "trust our 4 k lines" | highest, and likely to fail |
| **B. Transcription** | read each file, rewrite it in different words | nothing; it is a photocopier with extra steps | low, worthless |
| **C. Hardened re-implementation** | read the sources, re-derive the algorithms behind a frozen interface, keep a *faithful* build for equivalence and a *portable* build for maintenance; hold both to the recorded run | that the recorded run is reproducible, and that the binary64 contract is or is not load-bearing | medium |

**Recommendation: C, with A as a two-hour probe on `seed.cpp` only.** A is cheap to test on the
smallest file and its result — how much of `sumok`/`seeds::mk` can be recovered from the manuscript
alone — is itself a fact worth having, because it measures how much of the proof's trust base is
carried by prose. B is listed to be refused explicitly.

I recommend against full A: the manuscript describes the *mathematics* of each stage, not the
enumeration order, the tolerance constants, the sort keys or the reservoir sampling, and a faithful
run depends on all of them.

---

## 2. Architecture: one source tree, two builds

The single decision that determines whether six teams can work at all, given §0 fact 1:

- **Modular sources** — `src/seed.{h,cpp}`, `src/ub.{h,cpp}`, … with real headers, separate
  compilation, no textual include chain. This is what the coding teams edit, and the only thing
  documentation and critics read.
- **`amalgamate.sh`** — generates `build/faithful/all.cpp` by concatenating the module sources in
  upstream's dependency order into one translation unit per binary.
- **Two targets, both built every wave:**
  - `faithful`: amalgamated single TU, `g++ -O3 -march=native -ffp-contract=off` (+ `-std=gnu++17`
    for the three later binaries, exactly as `build.sh` does). **Only this target is held to
    byte-identity.**
  - `portable`: modular, `-O2`, no `-march=native`, `g++` and `clang++`, x86-64 and (best effort)
    aarch64. Held to structural equality and to passing the checker.

**Measured, and it falsified the guess this paragraph first made.** I expected the modular build to be
unable to reproduce the bytes, because codegen follows translation-unit shape. It can: two
independent modular builds with the published flags reproduced `centers.txt` exactly, counters and
all (W1, units 03/04).

I then wrote that the split costs 1.9× — 759.6 s against 401.8 s — and that was wrong too. Those runs
were made while thirteen agents shared four CPUs. The integrated two-TU build, run on an idle
machine, takes **400.8 s against the published build's 401.8 s** (`logs/R2.json`). The TU-split
penalty is therefore unestablished and may be nil for this code, whose hot loops are already
self-contained. Keep the two targets for a different reason: the faithful build reproduces upstream's
exact TU shape and flags, which is the strongest available guarantee of identity, and it costs one
build. Do not claim a performance justification for it — there is none in the measurements.

A critic's standing objection to this design — that the amalgamation is one more thing that can drift
from the modules — is accepted, and answered by a gate item: the amalgamation is generated, never
edited, and `faithful`/`portable` must agree on every rung of §5 below the byte level.

---

## 3. The six teams

Each team gets a directory, a write scope, a deliverable form and a gate item. No team writes outside
its scope; cross-scope requests go to O as a numbered change request (CR).

### C — Coding (implementation)
- **Writes:** `work/10-recreate/src/` only.
- **Reads:** `spec/interfaces.md`, the manuscript section for its unit, and (mode C) the
  corresponding upstream file.
- **Deliverable per work unit:** the module, plus `src/<unit>/NOTES.md` recording every choice the
  spec did not fix (order of enumeration, tie-breaks, seeds, tolerances) with the line of the
  manuscript or the upstream file that decided it.
- **Refuses to:** change a constant, a comparison direction or a tolerance to make a test pass. That
  is a CR against the spec, not a code edit.

### V — Verification (the harness)
- **Writes:** `work/10-recreate/harness/`, `work/10-recreate/logs/`.
- **Owns:** the build recipes, the replay driver over `commands.json`, the differential comparators,
  the record-parser cross-check, the cost measurements.
- **Deliverable:** one command — `harness/verify.sh --rung R3` — that emits a machine-readable
  pass/fail table with log paths. Prose is not a deliverable of V.
- **Independence rule:** V does not write algorithm code. If V finds a bug it files a CR.

### K — Critics (read-only, adversarial)
- **Writes:** `work/10-recreate/findings/<team>-<n>.md`. Nothing else.
- **Attacks, in order of value:** (i) the harness — see §6, "test the test"; (ii) the spec — an
  interface that under-determines behaviour is a defect in the spec, not in the coder; (iii) the
  code — a defect report must name a command that would expose it; (iv) the documents — a claim
  without an evidence pointer is a finding.
- **Deliverable:** numbered findings, each with severity (blocker / major / minor), the artefact and
  line, and the test that would settle it. A finding without a test is downgraded to "question".

### D — Commenting / Documentation
- **Writes:** `work/10-recreate/docs/`.
- **Deliverable:** per-module doc (purpose, contract, invariants, what a maintainer may and may not
  change), a CLI reference for the four binaries (argument ranges as *enforced*, e.g. `crun` aborts
  if `M ∉ [6,24]`, `layers ∉ [1,6]`, `RB ∉ [.012,.09]`, `capSteps ∉ [100,10⁹]`), the record-format
  spec with a worked hex example, the reproduction guide, and a provenance map
  paper-§ ↔ module ↔ recorded artefact.
- **Forbidden:** restating code in prose. A doc line that a reader could have got from reading the
  function signature is a defect. Docs explain *why* and *what breaks if*.

### S — Summarization
- **Writes:** `work/10-recreate/state/`.
- **Deliverable:** after each wave, `state/wave-<n>.md` — what passed, what failed, what changed,
  what is now assumed — every sentence carrying a pointer (`harness/logs/…`, `findings/…:12`,
  `src/…:88`). Plus `state/discrepancies.md`: the running list of places where our output and the
  recorded output differ, with the smallest input that shows each.
- **Rule:** a summary may compress, never introduce. Any statement not traceable to a log or a file
  is deleted at the gate, not softened.

### O — Organization (the desk; one agent, me, not a swarm)
- **Writes:** `work/10-recreate/{INDEX.md,gates.md,ownership.md,adr/}`, and `results/`.
- **Owns:** the interface freeze, the CR queue, the gate ledger, the merge order, the verdicts on
  swarm reports. Sole authority to declare a gate passed.
- **Deliverable:** at any moment, a reader can answer from `INDEX.md` — what exists, who owns it,
  what passed, what is open — without reading a log.

**Interaction, one sentence:** C produces, V measures, K attacks (concurrently, read-only), D
documents only what V has passed, S digests at the wave boundary, O arbitrates and freezes.

---

## 4. Work units

Sized for one agent-run each (~90 min), not for one file each — the dependency chain is real and
splitting it finer buys nothing.

| WU | unit | owner | depends on | done when |
|---|---|---|---|---|
| 01 | interface freeze: record format, four CLI tables, exit codes, constants, RNG seeds, sort keys | O+K | — | `spec/interfaces.md` frozen; every constant has an owner row |
| 02 | build harness: `faithful` + `portable`, probe integrated, flags/CPU/compiler logged | V | 01 | both targets build; probe passes; `logs/build-*.json` |
| 03 | `seed`: 112-bin triples, `sumok` interval test, `mk`, `build`, `list` (mt19937_64 seed 42) | C | 01–02 | A-probe result recorded; unit tests on `n=12,16,24` |
| 04 | `covout`: `coverSeeds`, `centers.txt` writer (`112 249878`) | C | 03 | rung R2 |
| 05 | `ub`: `Z`, LDLᵗ, `frame`, `block`, `uc`, `dataU`, `scalar`, `derr`, `trial`, `Usearch` | C | 01 | unit tests on synthetic frames |
| 06 | `patchx`: `Root`/`dephase`, `buildH` + Jacobian, `jacobi`, `spectralUpper`, `chol`, `ell`, `bootstrap`, `covercompute`, `Asearch` | C | 05 | `Asearch` converges on the recorded centres sample |
| 07 | `atlas`: `mapH`, `pivot`, `variants`, `Atlas`, `CenterList`, record I/O, `arun` | C | 06 | R3 |
| 08 | `stageB`: `inverseTransform`, `refiner`, batching/rename/`done.txt`, `brun` | C | 07 | R4, R5 |
| 09 | `stageC`: `Layer`, `cluster`, `graph`, `negative`, exit-code semantics, `crun` | C | 08 | R6 |
| 10 | independent re-derivation of the probe and of `check_records.py` | V | 01 | our checker accepts the recorded data and rejects 20 seeded corruptions |
| 11 | replay driver + differential comparators + report schema | V | 02 | `verify.sh --rung Rn` works on the recorded artefacts alone |
| 12 | mutation controls (§6) | K+V | 11 | 8/8 mutations fail the harness |
| 13 | docs: module docs, CLI reference, record format, reproduction guide, provenance map | D | 03–09 | every module documented; one-command rerun works from a clean tree |
| 14 | wave summaries, discrepancy ledger, final report | S | continuous | `state/final.md`, no untraceable sentence |

The chain 03→09 is genuinely sequential. **Parallelism therefore comes from duplication and from the
satellites, not from splitting the chain:** two implementations of `seed` (03, mode A probe) and of
`covout` (04) run side by side; 10–14 run concurrently with 03–09; critics run per unit as it lands.

---

## 5. Verification ladder

Each rung is a command with a pass criterion. A rung is never "mostly passing": it is pass, fail, or
not-run, and the discrepancy goes to S's ledger.

| rung | what | pass criterion |
|---|---|---|
| **R0** | contract | `abi-fp-probe` passes on the build host; compiler, CPU model, glibc recorded |
| **R1** | unit tests | per-module tests written by C, reviewed by K; no test may compare against a value our own code produced |
| **R2** | `centers.txt` | our `covrun` reproduces the recorded `centers.txt` (7 339 546 B, sha256 `c48bc9a2…`) **byte for byte** |
| **R3** | `coarse0..3.bin` | our `arun` on the recorded `centers.txt`, parts 0–3, reproduces all four files; `bad0..3.txt` empty |
| **R4** | `mid.bin` | our `brun .07 .013` on the recorded coarse files reproduces `mid.bin` |
| **R5** | `fine.bin` + 88 batches | our `brun .016 .005` reproduces `fine.bin`, every `batches/f*.bin`, `batches/done.txt`, in the recorded order |
| **R6** | full DAG | all 100 commands replay; return codes match `commands.json` exactly (85×0, 15×1); final-pass bad files empty (8 B header, count 0); the shipped checker passes when given **our `data/`** with the recorded `results/` and `commands.json` (its transcript assertions then test our counts against the recorded console facts), and our independent checker passes on our data |

Rung-by-rung is deliberate: R2 is one command and about one binary, and it settles in minutes what
R6 would settle in hours. **R2 is also the experiment that decides whether byte-identity is a usable
standard at all** — if the *upstream* binary compiled here reproduces the recorded `centers.txt`
exactly, byte-identity is real; if it does not, the ladder must start at structural equality (§7).

**That experiment has been run.** On 2026-11-14 I built the upstream `build.sh` output on this VM
(gcc 16.2.0, `-O3 -march=native -ffp-contract=off`, four CPUs, probe passing) and ran `covrun` on
nothing but the recorded inputs. It reproduced `centers.txt` **exactly**: sha256 `c48bc9a2…`,
7 339 546 B, in 402 s (`xs22829 build19.30`, 249 878 centres). Two consequences: byte-identity is a
real gate and not an aspiration, at least through stage A; and the first stage's cost is known, so
the R3→R6 budget is extrapolable before anyone is staffed. It also means the binary64 contract
survives a CPU that is not the one the record was made on — a fact about this stage, not a proof
about the others, and worth a sentence in the paper's §7.5 discussion if the rest holds.

**Measured budget so far** (same VM, one core each):

| stage | measurement | projected for the full run |
|---|---|---|
| `covrun` | 402 s for `centers.txt` | 402 s (one command, no split) |
| `arun` part 0 | the first 200 recorded centres in 4.30 s = 21.5 ms/centre, `failedBalls 0` | 62 470 centres per part ≈ 22 min; four parts on four cores ≈ 25 min wall |

Stage A is therefore cheap enough that R3 belongs in the same wave as the rebuild it tests. Whether
R4–R6 fit depends on B and C, which are unmeasured: `fine.bin` is 33.7 MB of records, so refinement
dominates and must be timed on one batch before W3 is scheduled.

**One layout hazard, before any rung runs.** The recorded argv is `covrun centers.txt`, and A0–A3
then read that same path. A replay that seeds a working directory with the recorded `centers.txt`
and runs our `covrun` inside it truncates the reference and afterwards compares our output with
itself. The driver must keep the reference outside the working tree or read-only, write our output
to a fresh path, and record the reference's sha256 before and after every run. Related: the eight
count-0 artefacts (four 0-byte `bad*.txt`, four 8-byte `fb1cbad*.bin`) make `[ ! -s file ]` a false
pass for a *missing* file, so existence is asserted separately from emptiness; and a replay loop
must not run under `set -e`, since 15 of the 100 recorded commands legitimately return 1.

Structural fallback (declared now, not after a failure): identical record counts, identical `k`
histograms, identical bad-file membership and order, identical exit codes, and `|Δ| ≤ 1e-12` on each
of the eight doubles with the *decision* fields (`radius`, `k`) exact. A failure under this fallback
is a finding about the binary64 contract, and belongs in the paper's §7.5 discussion — that is a
result, not a disappointment.

---

## 6. Test the test

The failure mode of a differential programme is a harness that cannot fail. A control counts only
where it has been *shown* to fail a named rung. The first version of this list was measured by a
critic and half of it was inert; this is the version that bites, with the rung each mutation aims at.

| # | mutation | rung it must break | measured behaviour |
|---|---|---|---|
| 1 | rounding mode, set **after** `environment()` / `checkcpu()` | R3 | R2 is identical either way; at R3 `FE_UPWARD` stalls cells (3 cells > 90 s against 0.14 s), so per-command timeouts and the empty-bad-file test are load-bearing. A pre-`main` mutation is undone, because `environment()` sets `FE_TONEAREST` at start. |
| 2 | one constant nudged, **per stage** | R2 for `covout`'s literal `R = .032`; R3 for `atlas.cpp`'s `.0320001` and `.103` | R2 is blind to the atlas constants, and R3 is blind to `covout`'s. At R3, all 27 records of a 200-centre run differ from byte 1509. |
| 3 | `-ffp-contract=fast` | R3 | R2 identical; at R3 `candidates` moves 283 228 → 283 230 and `coarse*.bin` differs at byte 13. |
| 4 | `-ffast-math` | build | the probe's `#error` refuses to compile. That is a build guard, not a sensitivity test — it is not evidence that the harness can fail. |
| 5 | one inequality reversed | R2 (`seed.cpp:46`: xs 197 → 387) and R3 (`ub.cpp:207`) | two controls, not one. |
| 6 | two records swapped inside `batches/f0.bin` | R5 and the checker | the sort-key mutation (`radius` → `id`) is *semantic*, not order-only — Atlas merges and `ref.blockers` change — so any comparator catches it and it proves nothing about order sensitivity. |
| 7 | Atlas bins 8 → 9, or `<` → `<=` in `Atlas::find` | R3 | replaces the reservoir-seed control, which is unreachable: `list()` is called only from the three unbuilt mains, and seed's own main passes `samples = 0`, so the `mt19937_64(42)` draw never happens in any binary the build produces. |
| 8 | one byte appended, and a truncated file | checker | both caught; a clean tree costs 4.9 s, so none of this is expensive. |

A rung with no mutation that fails it is not evidence — and a control that cannot be reached is
worse than none, because it manufactures confidence.

---

## 7. Risks, and what each is answered by

| risk | answer |
|---|---|
| recreation degrades into transcription (mode B by accident) | C reads only the interface and the manuscript section at implementation time; upstream is available to V and K, not to C, except in one enumerated `read-source` phase per unit, recorded in `NOTES.md` |
| byte-identity unattainable (`-march=native`, libm, compiler) | already measured: upstream reproduces stage A on this VM (§5); the remaining stages are still open, so the structural fallback stays fixed in advance |
| the four-CPU VM starves parallel runs | one heavy stage at a time; C's runs are unit tests only; V schedules; all long runs as background jobs with logs |
| `clang` cannot build the faithful target | expected — the probe refuses non-GCC; portable target uses clang with the probe's checks relaxed and is *not* held to identity |
| agents report success without evidence | V re-runs from logs; a report whose claim has no command is rejected at the gate |
| `check_records.py` is too weak (it checks consistency, not correctness) | WU-10 re-derives it independently; mutation 8 tests it |
| scope creep: rewriting the paper, re-proving the theorem | out of scope by D3; this programme produces code and evidence, not claims |
| time: full replay could be hours | measured at R3 (per-centre cost × 249 878/4) before R4 is scheduled |

---

## 8. Waves and gates

Gates are pass/fail at the desk; `work/10-recreate/gates.md` is the ledger.

| wave | teams | gate | criterion |
|---|---|---|---|
| **W0** (½ h) | O | **G-R0** spec frozen | `spec/interfaces.md` covers every CLI argument, every constant, the record layout, exit codes; K signs that it under-determines nothing that affects output |
| **W1** (2 h) | C(03, 04·A-probe), V(02, 10, 11), K | **G-R1** reproduction base | R0, R1 pass and R2 passes *for our `covrun`* — the upstream side of R2 is already confirmed (§5), so this gate measures only our re-derivation |
| **W2** (3 h) | C(05, 06), V, K, D(module docs) | **G-R2** core | R3 passes; `ub`/`patchx` unit tests reviewed; mutation controls 1–3 fail the harness |
| **W3** (3 h) | C(07, 08), V, K, D | **G-R3** refinement | R4, R5 pass; ordering mutations 6–7 behave as specified |
| **W4** (3 h) | C(09), V, K, D | **G-R4** exclusion and full replay | R6 passes or the gap is localised to named records with a minimal reproducer |
| **W5** (2 h) | D, S, K | **G-R5** handover | one-command clean-tree rerun; `docs/` complete; `state/final.md` traceable; no open blocker |

Times are wall clock for one swarm per team per wave on the shared four-CPU VM. Waves 2–4 are the
expensive ones; the estimate assumes R2 passes and C does not have to re-derive an algorithm from
scratch twice.

---

## 9. Swarm configuration

Ultramath, `deepseek/deepseek-v4.1-flash`, maximum reasoning effort, as the owner set for this
project. Members see only the `task` string, so each task carries: the unit's contract verbatim, the
file it may write, the rung it must reach, and the exact command whose output counts as done.

| team | members | window | why this width |
|---|---|---|---|
| C | 6 | 120 min | one member per unit in flight plus a spare for the amalgamation |
| V | 3 | 120 min | harness, checker re-derivation, replay driver — three separable jobs |
| K | 4 | 90 min | read-only; breadth is the point |
| D | 2 | 90 min | module docs + reproduction guide |
| S | 1 | 45 min | one voice; summaries do not parallelise |

I judge every report. A report is accepted only if I can reproduce its stated command from the log it
cites. Two rejections close a direction.

---

## 10. Definition of done

1. `src/` builds two targets from a clean tree with one command each.
2. `harness/verify.sh` reports every rung with a log path; R0–R1 pass, R2–R6 pass under the criteria
   fixed at G-R1 (byte-identity or the declared structural fallback).
3. 8/8 mutation controls fail the harness.
4. The shipped `check_records.py`, run with our `data/` and the recorded `results/`, and our independent
   checker on our data, both pass. (The `results/*.txt` are a curated transcript of the console, not
   stdout — spec §3.5 — so "the checker accepts our output" means our records agree with the recorded
   console facts, not that our stdout is byte-identical to those files.)
5. `docs/` lets someone who has not read the C++ rerun the recorded experiment and interpret a
   failure.
6. `state/final.md` states what was reproduced, what was not, and what that does and does not say
   about the paper's claim. In particular: reproducing the run does not audit the mathematics, and
   it does not authenticate the October 4 record — it re-derives it.

---

## 11. What this changes in the existing plan

- **D1 is void.** Its premise (sources unavailable) is false as of this repository. I propose a
  **D6** in `work/00-lead/decisions.md` recording: sources and the execution archive are public; the
  recreation programme of this document replaces the interval-arithmetic rationale of
  `results/plan.md` §2 for the *code* arm only; the accuracy goals in §1 there stand.
- **T2 is absorbed.** `work/02-checker/` is empty; WU-10 delivers the same thing (an independent
  checker) with a stronger acceptance test (it must reproduce the recorded coverage, and it must
  reject 20 seeded corruptions), so there is no reason to run both.
- **T3's reference implementation is this programme**, not a separate one.
- **G2's criterion should be restated** to: "our checker accepts the recorded data and our
  reproduction, rejects ≥ 20/20 seeded corruptions including a one-byte append, and runs the full
  record set in under 10 minutes."
- **Unchanged:** D2 (scoped formalisation), D3 (one preprint), D5 (Lean conventions), and the Lean
  arm's separation from the code arm for CPU reasons (D4). The Lean arm can run in the same weeks as
  this programme only if the heavy stage runs are scheduled, not concurrent — I would keep them in
  separate waves as D4 says.

---

## 12. Licensing (affects mode C)

`openai/math` is Apache-2.0. Mode C produces a derivative work: keep the upstream notices, attribute
the source repository and commit (`42907c9e`, 2026-10-26, the last change under this preprint's
directory), and record in `docs/provenance.md` which module derives from which upstream file and what
was changed. Mode A (clean room from the manuscript) does not raise this, which is a small argument
in its favour that does not outweigh the cost.

## 13. Three questions for you

1. **Mode:** C with an A-probe on `seed.cpp` (my recommendation), full A, or B?
2. **Byte-identity:** if our faithful build cannot reproduce the recorded artefacts exactly on this
   VM, do you want the structural fallback pursued to R6, or the programme stopped at the finding?
3. **D6:** may I record it in `work/00-lead/decisions.md`, and restate G2 as in §11?
