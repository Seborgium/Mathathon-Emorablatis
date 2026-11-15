# Plan: an independently checkable certificate for N(6) = 3

Status: **proposal for the owner's approval.** No phase below has started. Each phase begins with a
human decision and ends with a gate the human (or the lead, under a recorded delegation) signs.
Supersedes the code arm of `results/plan.md` and absorbs `results/recreate-code-plan.md`
(its mode **C, hardened re-implementation**, is adopted for the *proposer* side only; its mode A
clean-room probe is retained as a two-hour measurement, not a work stream).

Subject: OpenAI preprint *The maximum number of mutually unbiased bases in dimension six*
(24 Sep 2026), sources and run record at
`openai/math/preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/verification/`.

---

## 0. Objective, and the sentence we want to be able to print

Today Theorem 1.1 hypothesises an **event**: a 100-process execution on one machine, under a
binary64/compiler/libm contract, of seven C++ files assumed to implement the paper's lemmas.

The project replaces that event with an **object**:

> **Target statement.** There is an explicit certificate file $C$ and a checker $Q$, written in
> exact/rational and outward-rounded interval arithmetic, such that: $Q(C)$ accepts, and the
> (human- and Lean-checked) assembly argument proves *if $Q$ accepts $C$ then no four pairwise
> mutually unbiased bases exist in $\mathbb C^6$*. Together with the three explicit bases this
> gives $N(6)=3$, with no floating-point, compiler, disassembly or evaluation-order premise.

Two properties are non-negotiable and come straight from the preprint's own architecture:

1. **Propose vs. certify.** The authors' programs (and ours) only ever *propose*. Every exclusion
   is a strict violation of a *necessary* condition, so it is a witness, not a search result.
   Anything not certified is `unresolved`, and **unresolved is never negative**. A certificate with
   a nonzero unresolved count is not a certificate of $N(6)=3$; it is a smaller theorem, reported
   as such.
2. **Small trusted base.** What a reader must trust at the end is: the necessity lemmas, the
   checker $Q$ (target $\le 2{,}000$ readable lines, one entry point), the assembly argument, and
   the arithmetic kernel. Not the search, not the run, not our instrumentation.

### Explicit non-goals
- Full Lean formalisation of the analytic middle (multi-person-year). Lean is scoped to the
  deterministic core plus the assembly implication, as in decision D2.
- A *new* mathematical proof of Zauner's conjecture by hand.
- Claiming the main theorem was formalised or independently proved before a gate says so.

### Definition of done (project level)
`certdata/<release>/` contains the certificate, the logs, and a manifest; `qcheck certdata/<release>`
exits 0; a synthetic valid certificate is accepted and $\ge 20/20$ seeded corruptions are rejected;
controls $d=2$ excludes while $d=3,4$ do **not**; the final unresolved ledger is zero; the report
reproduces every one of its numbers from the logs by script.

---

## 1. Artefact architecture

```
cert/spec/            frozen, versioned human+agent-written specifications
  statement.md        the target statement and exactly what is trusted
  arithmetic.md       the exact/interval kernel contract (outward rounding, e(x) bounds)
  cert-format.md      per-stage certificate schemas (binary + JSON header, versioned)
  inequalities.md     every certified inequality, with paper equation numbers
  ledger.md           the obligations model (what "unresolved = 0" means, per stage)
src/                  our code only
  kernel/             rational + interval arithmetic, rigorous exp/trig, tests
  emit/               witness emitters (separate translation units; see 2.2)
  proposer/           hardened modular re-implementation + amalgamation (recreate-plan mode C)
  qcheck/             the checker; one entry point per stage + one global
  sat/                Stage-C encoding + DRAT/LRAT emission and checking glue
  report/             log -> table/figure scripts (the only source of printed numbers)
certdata/             generated, never hand-edited
  upstream/           fetched sources, commands.json, records; sha256 manifest
  runs/<run-id>/      one directory per execution: argv, env, stdout/stderr, wall time,
                      outputs, hashes, emitter version, host facts (nproc, g++ --version)
  cert/<version>/     the certificate itself, per stage, plus manifest.json
  mutations/          seeded corruptions and the checker's verdict on each
  controls/           d = 2, 3, 4 and known-case runs
work/<team>/          per-team notes, derivations, handoffs (existing layout kept)
results/              plans, audits, the final report
```

Two rules: **every number in the report comes from `src/report/` reading `certdata/`**, and every
run directory is self-describing enough to be re-executed by one command.

---

## 2. Technical design decisions (to be ratified at H0)

**2.1 Certificate = small hints + deterministic recomputation.** Per-pair logs for the
$1.5\cdot10^8$ seed bin pairs would be gigabytes of text and would only move trust onto the
emitter. Instead the checker re-enumerates cheap structure itself (bin pairs, cell trees, grids)
and the certificate supplies what is expensive to find: retained centres, dual vectors $v$,
separating directions $y$, root constants, adjacency bitsets, SAT refutations. This is the single
most important size/trust trade-off in the design.

**2.2 Instrumentation without semantic drift.** Upstream is one program textually split
(`stageC` ⊃ `stageB` ⊃ `atlas` ⊃ `patchx` ⊃ `ub` ⊃ `seed`). Emitters therefore live in *separate*
files, called behind a flag, writing to separate streams. Acceptance test, before any emitted data
is believed: with emission off, the 100 recorded commands reproduce the recorded counts and return
codes (85 rc 0, 15 rc 1 inside the fallback chain); with emission on, outputs are bit-identical and
only new files appear. Recorded evidence: the seed stage already reproduces `centers.txt`
byte-identically here (249,878 centres, 402 s).

**2.3 Arithmetic.** Rationals for bin indices/midpoints (phases are multiples of $1/(2N)$);
fixed-precision ($\ge 100$ bit) outward interval arithmetic for everything transcendental, with a
rigorously bounded $e(x)=e^{2\pi i x}$. All certified checks are one-sided with explicit slack; any
comparison that cannot be decided at the working precision is `unresolved`, never a pass and never
an exclusion. Precision is adaptive and *recorded*, since it is part of the witness.

**2.4 Where Appendix A goes.** Only the certify predicates are ported to the kernel. The binary64
error budgets, the platform probes and the saved-disassembly codegen check then become
*proposer-side* engineering notes; the target statement no longer mentions them. This is the
deletion of the paper's ~20-page weakest premise, and it is a by-product of the certificate, not a
separate project.

**2.5 The combinatorial core has two allowed resolutions.** Stage C needs: no two disjoint
six-cliques in $O$ with all 36 cross edges in $U$. Either (a) the retained graphs are small enough
that $Q$ exhaustively rechecks the pattern itself, with measured cost printed, or (b) the
instrumented least-vertex-branching search emits a DRAT/LRAT-style refutation, checked with an
existing (ideally formally verified) proof checker. Route (a) is preferred if the measurements
allow it: fewer moving parts, no encoding to trust. H0's feasibility measurement decides; route
(c) — "no compact witness, $Q$ re-runs the exponential search" — is explicitly *not* accepted as a
certificate.

**2.6 Assembly is a theorem, not a sentence.** The five covering propositions (2.10, 3.11, 4.16,
5.7/5.8, 6.9) plus 7.1 are restated as implications about *checked* objects, and combined in Lean
over an abstract region interface with the analytic lemmas as explicit hypotheses. The axiom
footprint is printed in the report. A failed assembly proof does not get papered over: its
obstruction is itself a finding about the paper's logic.

---

## 3. Teams and roles

The orchestrating chat agent is **O** (lead, integration desk, judge of all submissions). Teams are
directed single agents for mechanical work and **Ultramath swarms** for the two genuinely hard,
non-mechanical problems (Stage-C witnesses; Root/atlas rechecking). This VM has **4 CPUs and
15 GB RAM**; swarms share those cores with the compute they launch, so *at most one swarm plus one
heavy compute job at a time*, and Lean elaboration is never scheduled against a swarm. At most 16
background jobs exist project-wide; O keeps a queue and logs every launch in `work/00-lead/`.

| team | role | writes | shape |
|---|---|---|---|
| O | integration, gates, judging, change requests, data releases | `work/00-lead/` | lead agent |
| S | specification: `cert/spec/*`, claims-to-evidence traceability | `cert/spec/`, `work/01-catalogue/` | 1–2 agents |
| K | exact/interval arithmetic kernel + its own test suite | `src/kernel/` | 1 agent + 1 reviewer |
| P | proposer: hardened re-implementation, two builds, replay harness | `src/proposer/`, `src/emit/` | 2 agents (mode C) |
| Q1 | seed-stage checker (Prop 2.10) | `src/qcheck/seed*` | 1 agent |
| Q2 | Stage-A cell-tree checker (Prop 3.11) | `src/qcheck/stageA*` | 1 agent |
| Q3 | Root/atlas + Stage-B ledger checker (Prop 4.16, 5.7–5.8) | `src/qcheck/{atlas,stageB}*` | **swarm**, then 1 agent |
| Q4 | Stage-C graph/edge checker + clique witness route | `src/qcheck/stageC*`, `src/sat/` | **swarm**, then 1 agent |
| R | red team: mutation corpus, adversarial review, independent re-derivations | `certdata/mutations/`, `work/09-redteam/` | 2 agents, never the authors of $Q$ |
| C | controls ($d=2,3,4$; known cases) and exaggeration tests | `certdata/controls/`, `work/03-reference/` | 1 agent |
| L | scoped Lean: core sorries, assembly implication, axiom report | `work/04-lean/` | 1 agent, separate waves |
| E | editor: report pipeline, figures, final condensation | `src/report/`, `work/08-paper/` | 1 agent + O |

Working agreements (each team's prompt states them):
- Write only inside your scope; cross-scope needs go to O as a numbered **CR**; O logs the decision.
- Every deliverable arrives with `handoff-<n>.md`: what was done, what was run, exact commands,
  exit statuses, file paths, and what was **not** verified.
- Never change a constant, comparison direction, tolerance or schema to make a check pass. That is a
  CR against the spec, and it is reported, not silently fixed.
- No team describes the authors' code as "audited" unless it actually read the specific lines, with
  file/line citations; no team claims a stage "certified" while its unresolved count is nonzero.
- Swarm submissions are accepted by O only after O re-runs the check itself. Plausible-but-unproved
  is a rejection with the gap named.

Suggested swarm configurations (as used successfully earlier in this project):
`deepseek/deepseek-v4.1-flash`, maximum reasoning effort, 100 member steps; Q4: 6 members, 150 min;
Q3: 6 members, 150 min; red-team reviews: 3 members, 90 min. Directions must be disjoint and are
registered before work; the board is the shared memory, the handoffs are the deliverables.

---

## 4. Phases

Every phase is **initiated by a human** with a short decision (listed as "H<n> input"), followed by
a long autonomous agentic stretch, followed by a gate. O prepares each H-input as a one-screen
brief: options, measured costs, recommendation. Nothing starts the next phase on its own.

### H0 — Kick-off and feasibility (human: approve this plan, pick 2.5's route to *measure*, set budget)
*Agent work (1–2 days autonomous).* S freezes `statement.md` and schema v0. P fetches upstream into
`certdata/upstream/` with hashes and replays `covrun` to confirm the recorded 402 s / 249,878-centre
baseline. Q4 **measures, before designing anything**: per-record graph sizes, $O/U$ densities, cap
and overflow counts from the `crun` summaries; estimates the cost of exhaustive rechecking vs. the
size of a SAT refutation. K prototypes the kernel and measures the exact-arithmetic slowdown on the
seed filters (the 10–100× planning factor is replaced by a measurement). C drafts the controls. E
sets up the log-to-table pipeline skeleton.
*Gate G0 (human):* feasibility memo with measured sizes and times; chosen Stage-C route;
certificate size and total-runtime estimates; schemas frozen at v1; go/no-go on the whole project.
**If Stage C is infeasible by both routes, the project does not pretend otherwise: it retargets to
"everything except the combinatorial core, independently certified", which is still a large
improvement, and the human decides whether that is worth the remaining phases.**

### H1 — Seed stage end-to-end (human: approve G0's schemas and the compute budget)
*Agent work (2–4 days autonomous, mostly compute in background).* P adds seed emitters and proves
semantic non-interference. Q1 writes the seed checker on K's kernel: re-enumerate bin pairs, apply
(2.6)–(2.8) in interval arithmetic, verify each surviving pair's exclusion or absorption into a
retained centre's radius-$0.032$ ball via (2.9); check $N=112$ coverage and slack directly, so the
certificate is valid for the *stated* constants, not for a story about them. R builds the mutation
harness and corrupts the seed certificate (off-by-one bin, inflated radius, wrong dual vector,
dropped centre, flipped comparison). C runs the $d=2,3,4$ analogues.
*Gate G1 (human):* Proposition 2.10 independently machine-checked; unresolved = 0 at the seed
stage; mutations rejected $\ge 20/20$; the true enumerated-pair count reported (resolving the audit
finding that $151{,}744{,}086$ is unreproducible); measured runtime and certificate size; one-page
demo sheet a non-specialist can follow.

### H2 — Instrumentation everywhere, Stage A and the atlas (human: approve scaling up)
*Agent work (1–3 weeks autonomous; long background runs, batches of the recorded 100-command DAG).*
P completes emission for `arun`/`brun`/`crun` and maintains the replay harness (counts and return
codes match the recorded run, divergences are findings, not bugs to hide). Q2 checks cell trees:
children tile parents, every terminal node carries a valid exclusion witness $y$ with evaluated
sides of (3.26)/(3.29) or a retained cell with Root constants. Q3's swarm re-derives the
Root/atlas inequalities (4.4), transport, merge distances (4.15), and the Stage-B relation (5.2)
and iteration (5.3) as *checkable* statements — this is the analytic core and gets the swarm,
because the paper's compressed presentation is where transcription errors will live. L works the
deterministic core sorries in a separate, compute-quiet wave.
*Gate G2 (human):* Props 3.11 and 4.16 checked on all emitted records; unresolved = 0 for A/atlas;
per-stage runtimes and sizes; red team's independent re-derivation of two Root inequalities agrees
or the discrepancy is a recorded defect.

### H3 — Stage B's ledger and Stage C's core (human: approve the heaviest compute)
*Agent work (1–3 weeks autonomous).* Q3 turns Stage B into an explicit **obligations ledger**: per
parent, children + tangent-grid boxes + outside tests + blocker links; failed parents stay on the
right-hand side until discharged at $(\tau,w)=(0.011,0.0038)$; the final balance must be zero, and
coverage is a checked trace property, not prose. Q4 executes the chosen Stage-C route at scale and
checks edge predicates (6.16), (6.20), (6.21), (6.23) with non-edges certified. R attacks the whole
certificate now, with a dedicated hunt at the six audit targets (pair count, merge no-op for
$M\le50$, $\mathrm{RN}^2$ hard-coding $N=112$, stated $k\le10$ vs. the box cap, sentinel 100,
the $1.25\times$ tangent margin).
*Gate G3 (human):* the terminal statement "no unresolved record" is now machine-checked, or the
precise obstruction is documented; every red-team finding has a verdict (harmless + proof, or
defect + impact). **A demonstrated false exclusion at this gate is a major result and pivots the
report to the defect; the plan does not assume the paper is right.**

### H4 — Assembly, full replay, Lean, independent acceptance (human: approve the release candidate)
*Agent work (1 week autonomous).* O runs one clean end-to-end replay from `certdata/upstream/`
through emission to `qcheck` acceptance, on a fresh certificate version. C finishes controls and
known cases. L proves the assembly implication over the abstract region interface and prints the
axiom footprint. R performs a release audit: can anyone accept a doctored certificate? Are the
trusted files exactly the ones the statement lists? E freezes the evidence index.
*Gate G4 (human):* the target statement of §0 is true *as written*, with its trusted base listed
file by file; or it is not, and the remaining conditions are printed verbatim in the report.

### H5 — Condensation (human: choose audience and length; sign the release)
*Agent work (3–5 days autonomous).* This is the "lots of code and runtime data $\to$ one report"
step, and it is mechanical by design:
1. `src/report/` regenerates **every** table and figure from `certdata/`: stage counts, runtimes,
   certificate sizes, slack distributions, mutation results, control outcomes, unresolved ledgers,
   the axiom footprint.
2. A claims-to-evidence matrix: each printed claim $\to$ the certificate object, the checker's
   function, the log file, and the gate that signed it. No claim without a row (existing gate G5).
3. Report skeleton: 1-page summary; $\le 6$-page narrative of the argument (the outline's five
   steps); the certificate format as a specification others can implement; the verification
   appendix ($\le 4$ pp.); limitations and provenance, including everything still conditional.
4. Two derivative artefacts: the certificate + checker release with a README that reproduces the
   accept verdict in one command, and a short "what would make this proof fully human?" section
   (where the difficulty actually concentrates, from the measured data).
*Gate G5 (human):* report compiles, numbers regenerate, red-team findings above "minor" are either
fixed or printed as limitations, and the release is signed.

---

## 5. Schedule, cost and honest expectations

| phase | autonomous span | dominant cost | demo-able outcome |
|---|---|---|---|
| H0 | 1–2 days | measurement, spec | feasibility memo, frozen schemas |
| H1 | 2–4 days | exact-arithmetic seed recheck (hours of background compute) | Prop 2.10 machine-checked |
| H2 | 1–3 weeks | Stage A/atlas emission + checking; swarm derivations | Props 3.11, 4.16 checked |
| H3 | 1–3 weeks | Stage B/C compute, SAT proofs | unresolved = 0, or a named obstruction |
| H4 | 1 week | clean replay, Lean assembly | the target statement, verified |
| H5 | 3–5 days | report generation | the release |

Total: **roughly 5–9 weeks of phased work**, of which the humans' part is six short gate meetings.
A mathathon-sized slice is H0+H1 with H3's Stage-C measurement moved forward: it produces a real,
checkable artefact and a defensible sentence ("the seed covering proposition is independently
machine-checked; here is the format and the costed path for the rest"), without overclaiming.

Known unknowns, stated up front: exact-arithmetic slowdown beyond the seed stage; Stage-C graph
sizes (measured at H0); whether Stage B's prose specifies enough to check coverage without
re-deriving the search; whether the recorded run's 15 return-code-1 commands are fully discharged
by the fallback chain as the paper asserts. Any of these can lengthen H2/H3; none is a reason to
weaken the definition of done.

## 6. Failure modes and how the plan responds

- **A real defect is found.** Report it, localise it with the bit-identical replay, quantify the
  affected records, and if possible repair and re-certify. This is a success outcome, not a failure.
- **Stage C has no compact witness and is too big to recheck.** Ship stages 0–B certified; state
  the remaining trust precisely; do not relabel a re-run as a certificate.
- **Exact arithmetic is too slow.** Raise precision adaptively, cache interval evaluations, shard
  the independent per-record checks; never resolve an undecided comparison by guessing.
- **Checker bug asymmetry.** The dangerous direction is *accepting* a bad certificate, hence the
  mutation corpus, the independent re-derivations, and controls that must *not* exclude.
- **Agent overclaiming.** Every gate has evidence paths and re-runnable commands; O re-runs before
  signing; handoffs must name what was not verified.

## 7. Relationship to existing decisions and gates

D1 (work without the authors' sources) is superseded: sources and run records are public and
cached. D2 (scoped Lean), D3 (one preprint), D5 (`lean <file>` with preset `LEAN_PATH`, no
`lake build` against `/opt/mathlib`) stand. D4's wave separation (Lean vs. heavy code work) is
kept as a scheduling rule in §3. Existing gates G0–G6 are reorganised as H0–H5 above; the criteria
themselves (controls G1, checker mutations G2, parameter justification G3, formalisation fidelity
G4, draft G5, red team G6) are carried into the corresponding new gates rather than dropped.
The T5 parameter table remains the reference for every constant the checker relies on, and the six
audit targets in `results/improvements.md` are the red team's initial corpus.
