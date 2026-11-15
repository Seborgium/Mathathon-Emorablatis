# Plan: make the dimension-six MUB proof accessible and accurate

Status: proposal. Nothing has been launched. Skeleton directories exist under `work/` with
per-team READMEs that state the file contract (`work/*/README.md`).

Scope note that shapes everything below: **the authors' sources are not in the packet** (checked:
the PDF embeds no files; no repository is connected here). So accuracy cannot be improved by
auditing their code. It is improved by (a) making the *statements* checkable, (b) producing an
independent implementation whose disagreements localise errors, and (c) replacing the fragile
arithmetic model with one that does not depend on a compiler. Every team below is designed against
that constraint.

---

## 1. What "better" means, numerically

| dimension | today | target |
|---|---|---|
| trust base of the main claim | 7 sources + 100-process run + 20 pp of binary64 budgets | one certificate file + one checker of ≤1500 lines |
| claims whose evidence is prose about code (my **S** tag) | ~30 | 0 unmarked: each either proved, formalised, or explicitly assumed in a stated hypothesis |
| Appendix A length | ~20 pp | ≤4 pp |
| paper length | 76 pp | ≤45 pp, with a 1-page summary and a 6-page 18.701-level path |
| figures | 2 | 12, each tied to a named paragraph |
| constants justified by an inequality + slack + cost curve | a handful | all (N=112, R=.032, N_u, .103/.125, the three (τ,w), all caps, k≤10, the .64 eigenvalue split, every margin) |
| controls showing the pipeline can fail | none | d=2 positive, d=3/d=4 negative, plus two known cases |
| code | ~4k lines, unauditable | ≤2k lines reference implementation + 1.5k-line checker |

The single sentence of intent: *a reader should be able to check the conclusion with one program and
one data file, and understand the argument from twelve pictures and six pages of narrative.*

---

## 2. Design principles (binding on every team)

1. **One source of truth for claims.** `work/01-catalogue/claims.yaml` is frozen at gate G0. Every
   other artefact cites claim ids; no artefact may assert a claim that is not in the inventory.
2. **Propose ≠ certify.** The new code keeps the paper's discipline: generators propose, and only a
   one-sided inequality check certifies. No team may "fix" a certificate by tightening a comparison.
3. **Nothing unmarked.** A statement about code is either replaced by a statement about sets, or
   carried as an explicit hypothesis in the theorem's statement. Silence is not allowed.
4. **One reader path.** The final file has exactly one intended route: summary → narrative →
   assembly of the five stages → verification appendix. Everything else hangs off it.

---

## 3. Teams

Nine workstreams plus the integration desk. Swarm configuration reflects the work: wide where there
are many independent directions, narrow where coherence matters. Members see only the `task` string
I pass, so each task will contain the team's mission, its file contract and its gate criteria
verbatim.

### T0 — Integration desk (me, not a swarm)

Holds sole write access to `work/00-lead/`; the only agent that starts, stops and judges swarms.
Processes: freeze `claims.yaml`; arbitrate change requests and defects; pass or fail each gate; run
the merge into `paper/`; sign off the end state. Also the only writer of `results/`.

### T1 — Catalogue: organisation, simplification, notation

*Mission*: turn the prose into a machine-readable claim graph and fix the vocabulary.
*Processes*: P1.1 assign ids and status tags to every numbered claim (seed: `results/proof-claims.md`);
P1.2 dependency edges (which claim needs which), emitted as `dependencies.dot`; P1.3 restate each
lemma in ≤2 lines with hypotheses explicitly quantified over (this is the "simplification" pass at
statement level); P1.4 notation table with the three renamings unified (`C/γ/Γ`, `id/α/ι`,
`mnorm/µ`, `ort/o/ω`, `froot/ε`), and one page of "what each symbol is, in words"; P1.5 flag every
claim that is currently **S** and propose for each: prove, formalise, or promote to a hypothesis;
P1.6 a 6-page 18.701-level narrative skeleton (the reader path, no proofs).
*Reads*: the PDF, `results/proof-claims.md`, `results/code-audit.md`.
*Writes*: `work/01-catalogue/{claims.yaml, dependencies.dot, notation.tex, style.md, reader-path.md, changerequests/}`.
*Swarm*: 6 members, 90 min. Seed directions: (1) claim graph and ids; (2) statement rewriting;
(3) notation unification; (4) S-claim triage; (5) dependency cycles and hidden circularity hunt;
(6) reader path.
*Gate*: G0.

### T2 — Checker: make the conclusion checkable

*Mission*: a small program that reads a certificate and either accepts it or names the failing
inequality.
*Processes*: P2.1 define `cert-format.md` — a stage-indexed, self-describing format carrying, for
each region, the witness of its exclusion or coverage (seed pairs: the killing filter and its
evaluated bounds; Stage A cells: the direction `y` and both sides of (3.26)/(3.29); Roots: the seven
constants plus `T`; Stage C: ball centres/radii and the `O/U` adjacency sets); P2.2 define
`inequalities.md` — every inequality the checker evaluates, stated once, with exact constants;
P2.3 implement in exact/interval arithmetic; P2.4 a **clique witness**: either a DRAT-style
refutation emitted by the search, or a mathematical characterisation of (6.24)-infeasibility
checkable on the adjacency sets — this is the one genuinely hard sub-problem and gets two members;
P2.5 mutation harness: seeded corruptions (flip a sign, inflate a radius, drop an edge) must be
rejected; P2.6 runtime budget and a `--sample N` mode.
*Reads*: `claims.yaml`, `notation.tex`, the PDF (Def 4.1, §§3.6, 4.5, 6.2–6.7, A.7–A.11).
*Writes*: `work/02-checker/{spec,src,tests,reports}`.
*Swarm*: 10 members, 240 min. Seed directions: Root constants; cell exclusion; seed-cover coverage;
single-vector filters; pair/joint tests; clustering coverage; atlas merge distances; clique witness
(DRAT); clique witness (structural); format/provenance/mutation harness.
*Gate*: G2.

### T3 — Reference implementation and controls

*Mission*: a short, readable implementation of the specification, plus the controls the paper lacks.
*Processes*: P3.1 implement the reductions (seed cover, `U(2)` cover, Root construction, refinement,
vector cover and graph) at ≤2000 lines with interval arithmetic, single entry point, `--check` mode
emitting T2's format; P3.2 **controls**: the same pipeline with `d=2` (must exclude: N(2)=3),
`d=3` (must not: N(3)=4), `d=4` (must not: N(4)=5) — a negative verdict in d=3/d=4 is a soundness
bug and stops the project; P3.3 known cases: standard+Fourier (Grassl) and the Fourier family
excluded *with a cleared certificate*, naming the test that fired; P3.4 slack instrumentation —
per-test minimum margin and argmin, emitted as CSV for T5 and T6; P3.5 cap instrumentation — nodes,
boxes, clusters, graph steps near their caps.
*Reads*: `claims.yaml`, `notation.tex`, `02-checker/spec/*`.
*Writes*: `work/03-reference/{src,controls,reports}`.
*Swarm*: 10 members, 240 min. Seed directions: seed cover; blocks and frames; `U(2)` cover and
Taylor; Root construction; refinement relations; vector cover; graph tests; d=2/3/4 controls;
known-case reproduction; instrumentation.
*Gate*: G1 (controls) then G5-input.

### T4 — Formalisation

*Mission*: machine-check the part that is mathematics.
*Processes*: P4.1 formalise the cheap core: 1.2, 2.2, 2.3, 2.5, 6.5, 5.1, 3.1, 3.8, 3.9, 4.11, 4.12;
P4.2 the fiddly middle: 2.4, 2.6, 2.7, 2.8, 3.4, 3.6, 4.3, 4.4, 6.1, 6.2, 6.3, 6.6, 6.7, 4.8;
P4.3 **the assembly implications** — 2.10, 3.11, 4.16, 5.7, 6.9, 7.1 as implications over
abstract region lists (this is the highest-value part: an error here is invisible in prose);
P4.4 state the end-to-end theorem with the checker's acceptance as an explicit hypothesis, so the
formal statement is honest and finite; P4.5 a status table (proved / stated / skipped) that the paper
prints.
*Reads*: `claims.yaml`, `notation.tex`, paper sections as they appear.
*Writes*: `work/04-lean/{lakefile.lean, lean-toolchain, Mub6/*.lean, reports/status.md}`.
*Swarm*: 14 members, 360 min (this is the stream most likely to need a second wave). Seed
directions: one per lemma cluster of P4.1, two for 2.4, two for the assembly implications, one for
the interval/checker interface.
*Gate*: G4.

### T5 — Parameters: justification and sensitivity

*Mission*: every constant earns its place or is replaced.
*Processes*: P5.1 build the table *constant → the inequality that constrains it → current slack →
cost as a function of the constant → recommended value*; P5.2 **N=112**: the paper's stated reason
("$\binom{116}{5}$ is below the signed 32-bit limit") does not single out 112 — the largest
admissible N under that bound is **189** (but the binding ceiling is the `int8_t` bin difference, **N <= 128**), and the fresh-centre distance $\tfrac{3}{2N}\le R=0.032$
only forces $N\ge47$. So N sits in a window $[47,\mathbf{128}]$ — the 32-bit bound at 189 is dominated by the paper's own `int8_t` storage claim — and the printed code's hardwired constant makes the *printed-consistent* window $[112,128]$. Deliver: the cost
curve (tuple count grows as $N^5/120$: 10.4M at 64, 160.4M at 112, 309.3M at 128, 930M at 160) and,
if T3's instrumented run is available, *retained centre count vs N* — the quantity that actually
matters; P5.3 the same treatment for $R=.032$, $N_u=16\to512$, the local/global targets $.103/.125$,
the three $(\tau,w)$ pairs, every cap (1e6 nodes, 5e6 graph steps, 2048 clusters, 2e6 records,
5e7 boxes), $k\le10$ (see below), the $.64$ eigenvalue split, $K=1.00001$, $q_d<3.8$, and every
margin in the closing table; P5.4 the two audit findings: the **k≤10 vs box cap** tension (the
operative bound is $k\le5$ in passes 1–2 and $k\le7$ at $w=.0038$, so half the stated allowance is
unreachable) and the **Stage-C cutoff** $(.042-1.11w)^2$ whose base is negative for $M<26$, giving a
non-monotone effective merge radius $.0505\to.0042\to.0189\to.0304$; P5.5 a "why not simpler" note
for each: what breaks if the value is halved or doubled.
*Reads*: the PDF (A.3, §5.6, §6.3, §7.3), `claims.yaml`, `03-reference/data/*.csv`.
*Writes*: `work/05-parameters/{justification.md, experiments/, data/}`.
*Swarm*: 8 members, 150 min. Seed directions: seed-stage constants; Stage A/`U(2)`; Root/tangent;
Stage B; Stage C; caps; margins; N=112 cost experiment.
*Gate*: G3.

### T6 — Figures

*Mission*: replace prose with twelve pictures.
*Processes*: F1 five-stage nested cover; F2 certificate data flow with the unresolved branches;
F3 the nine seed phases on a circle with the min-gap choice and the orientation swap; F4 the 2+4
block split, the two rank-2 kernels, the compression to `U(2)`; F5 the `U(2)` cell cover with the
angle ranges and one cell's Taylor neighbourhood; F6 $Z$ decomposed into three Frobenius-orthogonal
pieces; F7 Root geometry: ball, tangent frame, normal cone, two centres; F8 the ellipsoid sum and
the offset bound; F9 Stage B: parent/child/blocker triangle over the box grid; F10 Stage C:
bins → balls → twelve labels → the forbidden two-clique pattern; F11 a margin number line showing
each established error against its margin; F12 the d=6 landscape (prime powers, what is known,
where this sits).
*Writes*: `work/06-figures/{src,out,captions.md}`. Each caption names the paragraph that cites it;
unreferenced figures are deleted.
*Swarm*: 6 members, 120 min. Seed directions: F1/F2; F3/F4; F5/F6; F7/F8; F9/F10; F11/F12.
*Gate*: G5-input.

### T7 — Quantum framing and application

*Mission*: say precisely what the result means for quantum information, and what it does not.
*Processes*: P7.1 the physical reading of unbiasedness (complementary measurements, state
tomography, the $d+1$ bound, why composite dimension is hard); P7.2 the honest status paragraph:
what "computer-assisted, conditional on an execution" means for a conjecture claim, and the relation
to recent work on triples and to order-six Hadamard classification; P7.3 what a certificate-based
bound would be *usable* for (a checkable negative result, reuse for other Hadamard families, the
$d=10$ question); P7.4 a short, cited literature note that does not overclaim.
*Reads*: PDF §1 and bibliography, `claims.yaml`.
*Writes*: `work/07-quantum/{application.md, references.addition.bib}`.
*Swarm*: 4 members, 90 min. Seed directions: physical reading; status/honesty; usability; literature.
*Gate*: G5-input.

### T8 — The single final file

*Mission*: one self-contained document, one reader path.
*Processes*: P8.1 skeleton and section plan with page budget; P8.2 the accessibility layer — 1-page
summary, 6-page narrative, "what to read if you only read one section"; P8.3 the mathematics from
`claims.yaml` with the five assembly propositions collected in one place; P8.4 the verification
report replacing Appendix A (interval arithmetic means the budgets collapse); P8.5 the parameter
justification chapter from T5; P8.6 figure placement and captions from T6; P8.7 build via
`latexmk -outdir` into `.scratch/build`.
*Reads*: everything. *Writes*: `work/08-paper/` only.
*Swarm*: 4 members, 180 min (coherence matters more than parallelism here; most of the assembly is
mine between waves).
*Gate*: G5.

### T9 — Red team

*Mission*: try to break it.
*Processes*: P9.1 hunt false lemmas: re-derive each of the fifteen load-bearing statements
independently, no peeking at the paper's proof; P9.2 quantifier audit: every "for every", "there
exists", "closed", "up to equivalence" — check the direction; P9.3 arithmetic audit of the new
margins, not the old ones; P9.4 code audit of T2/T3 with fresh eyes: signed comparisons, sentinels,
off-by-one on bins and boundaries, integer overflow in the grid products; P9.5 the "too strong"
test: does the pipeline exclude a configuration that provably exists (the d=3/d=4 controls are the
standing test); P9.6 write defects with severity and a reproduction.
*Reads*: everything, read-only. *Writes*: `work/09-redteam/`.
*Swarm*: 6 members, 150 min, run *after* a draft exists and again after revision.
*Gate*: G6.

---

## 4. Your list, mapped

| you asked for | who |
|---|---|
| organisation | T1 |
| simplification | T1 P1.3 (statements), T5 P5.5 (constants), T8 P8.2 (narrative), T2/T3 (20 pp of budgets → interval arithmetic) |
| verification | T2 (checker), T3 (controls), T9 (adversarial) |
| formalization | T4 |
| coding | T3 (reference), T2 (checker) |
| visualization | T6 |
| quantum application | T7 |
| one-file write-up | T8 |
| N=112 justification | T5 P5.2 |

---

## 5. Files, ownership, and who reads what

```
work/00-lead/        T0 only          plan, gates.md, decisions.md, freeze/
work/01-catalogue/   T1 writes        claims.yaml, dependencies.dot, notation.tex, style.md,
                                       reader-path.md, changerequests/<team>.md
work/02-checker/     T2 writes        spec/cert-format.md, spec/inequalities.md, src/check.py,
                                       tests/, reports/
work/03-reference/   T3 writes        src/, controls/, reports/, data/*.csv
work/04-lean/        T4 writes        lakefile.lean, lean-toolchain, Mub6/*.lean, reports/status.md
work/05-parameters/  T5 writes        justification.md, experiments/, data/
work/06-figures/     T6 writes        src/, out/*.pdf + *.png, captions.md
work/07-quantum/     T7 writes        application.md, references.addition.bib
work/08-paper/       T8 writes        mub6.tex, sections/, Makefile
work/09-redteam/     T9 writes        findings.md, defects/<team>-<n>.md
results/             T0 only          digests, plan, audit (read-only to all teams)
scratch              nobody           .scratch/build, .scratch/venv — never a deliverable
```

Read sets (who must read what before writing):

| team | must read | may read |
|---|---|---|
| T1 | PDF, `results/proof-claims.md`, `results/code-audit.md` | — |
| T2 | `01-catalogue/claims.yaml`, `notation.tex`, PDF §§3.6,4.1–4.5,6.2–6.7,A.7–A.11 | T3 `src/` |
| T3 | `claims.yaml`, `notation.tex`, `02-checker/spec/cert-format.md` | T2 `src/` |
| T4 | `claims.yaml`, `notation.tex`, `08-paper/sections/` | T2 spec |
| T5 | PDF App. A + §7.3, `claims.yaml`, `03-reference/data/` | — |
| T6 | `claims.yaml`, `notation.tex`, `08-paper/sections/`, `05-parameters/justification.md` | T3 reports |
| T7 | PDF §1, bibliography, `claims.yaml` | — |
| T8 | everything | — |
| T9 | everything (read-only) | — |

---

## 6. Command and communication

```
                    you (chat)
                        │  orders, decisions
                 ┌──────▼───────┐
                 │  T0  lead    │  starts/stops/judges swarms; freezes files; passes gates
                 └──┬───┬───┬───┘
        ┌───────────┤   │   ├───────────┐
     ┌──▼──┐     ┌──▼─┐ ┌▼───┐      ┌──▼──┐        … T5 T6 T7 T8 T9
     │ T1  │     │ T2 │ │ T3 │      │ T4  │
     └─────┘     └────┘ └────┘      └─────┘
```

It is a star, not a hierarchy, and that is a fact about the tooling: only the lead can start a
swarm, stop it, or judge a submission. Members inside a swarm talk to each other through the
swarm's board (they must register distinct directions, so duplicate work is refused at the board);
they cannot talk to another swarm. Teams therefore communicate in exactly three ways:

1. **Files.** Each team owns its directory. Cross-team information is a file; there is no side channel.
2. **Handoffs.** `work/<team>/handoff-<n>.md` with a fixed header: `from: / to: / version: /
   depends-on: / blocks: / artefacts: / claims touched: / open questions:`.
3. **Change requests and defects.** If a team believes a claim in `claims.yaml` is wrong, it writes
   `work/01-catalogue/changerequests/<team>.md`. If it believes another team's artefact is wrong it
   writes a defect file; T9 writes them read-only-externally. **No team ever edits another team's
   file**, and no team edits `claims.yaml` after G0.
4. **Arbitration.** The lead reads change requests and defects at each gate and answers in
   `work/00-lead/decisions.md`, one entry per item, with the reasoning. A defect blocks the gate
   until it is fixed, contradicted with evidence, or recorded as a limitation.

Escalation rule: a member that finds a contradiction between two artefacts stops its direction and
reports it, rather than choosing one. The lead resolves it; a swarm member never has authority to
declare another team wrong.

---

## 7. Waves (the VM is small; three swarms at a time at most)

| wave | swarms | why this order | wall time |
|---|---|---|---|
| W0 | none — lead only | freeze the claim inventory, create skeletons, write swarm task strings | today |
| W1 | T1 (6), T5 (8), T7 (4) | all three can start from the PDF alone; T1's output is everyone else's interface | ~2 h |
| **G0** | — | `claims.yaml` + notation frozen | — |
| W2 | T2 (10), T3 (10), T4 (14) | the accuracy arm; each needs G0 | ~4–6 h |
| **G1–G4** | — | controls, checker, parameters, formalisation reviewed | — |
| W3 | T6 (6), T8 (4) | figures and the single file, from frozen claims + reports | ~3 h |
| **G5** | — | draft compiles, has the reader path, all figures cited | — |
| W4 | T9 (6) | red team on the draft | ~2.5 h |
| W5 | T8 (4) + lead | revision, sign-off | ~2 h |

Members run at maximum reasoning effort and share the VM's CPUs, so a 14-member swarm is slow; the
wave plan trades latency for coherence. Every swarm returns immediately and I am woken when a member
submits; a swarm that produces nothing usable still costs its full window, so each wave has a
kill criterion (below).

---

## 8. Gates

| gate | pass criterion |
|---|---|
| G0 | every numbered claim has an id, a status tag, a dependency list and an owner team; notation table exists and is used in `reader-path.md` |
| G1 | d=3 and d=4 analogues return "not excluded" with a stated reason; d=2 returns "excluded"; the two known cases are excluded by a cleared certificate naming the test |
| G2 | checker accepts a synthetic valid certificate and rejects ≥20/20 seeded corruptions; runs a 1000-record sample in <10 min; clique-witness route chosen and documented |
| G3 | every constant has constraint, slack, cost curve, recommendation; N=112 resolved with a measured centre-count curve, not a guess |
| G4 | `lake build` clean; zero `sorry` in the declared set; statements match `claims.yaml` after translation; status table printed by the paper |
| G5 | single file compiles; ≤45 pp; 1-page summary + ≤6-page narrative; 12 figures, each cited; Appendix A ≤4 pp; no claim in the file that is absent from `claims.yaml` |
| G6 | no open defect above "minor"; every remaining defect appears in the paper as a stated limitation |

Kill criteria (checked at each gate): a stream whose artefact cannot be reviewed in 30 minutes by
the lead is too big and is split; a stream that has not produced a file after its window is stopped
and re-scoped rather than extended.

---

## 9. Accuracy work with named targets

1. **The two audit findings.** k≤10 vs the box cap (T5 P5.4, fixed either by raising the cap,
   lowering the stated allowance to $k\le7$, or reporting the observed $k$ histogram); the Stage-C
   cutoff degeneracy (T5 P5.4 + T3 P3.4, fixed by rewriting the cutoff as
   $\max(0,\, .042-X_M)^2$ or by deleting the merge and letting radii speak).
2. **Every S-claim gets a disposition.** T1 P1.5 assigns each to: proved by hand (T1), formalised
   (T4), replaced by a checker-evaluated inequality (T2), or promoted into the theorem's hypothesis
   (T8). After this pass the paper has no statement whose only support is "the code does this".
3. **The N=112 discussion** becomes a subsection with a table: candidate N, tuple count, retained
   centres (measured), Stage-A cost, total wall time, and the chosen value's slack in each
   constraint. The honest finding to report is that the 32-bit bound permits up to 189 and the
   fresh-centre bound forces only ≥47, so 112 is a cost choice — which is fine once it is argued
   rather than implied.
4. **A negative result is now possible.** The controls are designed so that a broken pipeline says
   so loudly. If T3's d=3/d=4 controls exclude anything, the project stops and reports that the
   specification as printed cannot be right — that outcome is worth more than a polished paper.

---

## 10. Risks

| risk | likelihood | mitigation |
|---|---|---|
| authors' sources never arrive | high | T2/T3 build an independent pipeline and a new certificate format; the paper's claim becomes checkable *for the new pipeline*, and the old run is reported as unverified (already the status) |
| formalisation balloons past its window | high | scope to P4.1 + P4.3; the status table is a deliverable, incompleteness is reported |
| swarm members invent Lean that does not compile | medium | I run `lake build` myself at the gate; no `sorry`, no `admit`, statements diffed against `claims.yaml` |
| checker and reference implementation disagree | medium | that is the *point*: disagreements are localised by stage and reported as defects. Two implementations agreeing on 1000 records is the strongest evidence available without the authors' code |
| figures become decoration | medium | every figure must be cited by a named paragraph; T8 deletes uncited ones at G5 |
| scope creep into "proving it ourselves" | medium | the plan never claims to re-verify the authors' run; it produces an independent, checkable version of the argument |
| VM saturation | medium | ≤3 swarms per wave, member counts sized to work, kill criteria at gates |

---

## 11. Decisions I need from you

1. **Do you want to request the authors' seven sources and one worked record?** If they arrive, T2/T3
   gain a direct comparison and G2 gets much stronger; if not, the plan still stands.
2. **Formalisation budget**: full P4.1–P4.3 (multi-week, several waves) or the scoped version
   (P4.1 + P4.3, one wave, status table printed)? My recommendation: scoped.
3. **Where the result goes**: internal note, arXiv-style preprint, or course material. This changes
   T7 and T8's register, not the work.
4. **Launch**: I have not started any swarm. Say the word and I launch W1 (T1, T5, T7) and report
   back at G0.

End-state artefacts, one line each: `work/08-paper/mub6.tex` (the single file),
`work/02-checker/src/check.py` + `spec/cert-format.md`, `work/03-reference/src/` + `controls/`,
`work/04-lean/Mub6/` + `reports/status.md`, `work/05-parameters/justification.md`,
`work/06-figures/out/*.pdf` (12), `work/07-quantum/application.md`, `work/09-redteam/findings.md`.
