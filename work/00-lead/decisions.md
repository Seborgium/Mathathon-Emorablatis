# Decision log

## D1 — 2026-11-14 — work without the authors' sources
The seven sources, the execution archive and the certificates are not available. Accuracy is
therefore pursued by (a) making the statements checkable, (b) an independent implementation whose
disagreements localise errors, (c) replacing the binary64-plus-margins model with interval
arithmetic. No team may describe the authors' code as audited.

## D2 — 2026-11-14 — formalisation scope
SCOPED (owner's decision). Targets: the cheap deterministic core (1.2, 2.2, 2.3, 2.5, 3.1, 3.8,
3.9, 4.11, 4.12, 5.1, 6.5) and, at highest value, the assembly implications (2.10, 3.11, 4.16,
5.7, 6.9, 7.1) as conditional implications over an abstract region interface. Full formalisation of
the analytic middle (2.4 in full, 3.2, 3.4-3.7, 4.3-4.9, 6.2-6.7) is out of scope; those are
reported as stated-only in the status table and printed as such.

## D3 — 2026-11-14 — destination
One preprint. Register: technical, honest about conditionality, no course-handout material in the
main file.

## D4 — 2026-11-14 — wave shape revised from results/plan.md §7
Originally W2 ran T2, T3 and T4 together. The VM has 4 CPUs and a Lean file importing Mathlib takes
~21 s to elaborate from disk, so the code arm (T2 checker, T3 reference) and the Lean arm (T4) get
separate waves. Revised: W1 T1+T5+T7+T4-phase0; G0; W2 T2+T3; G1-G2; W3 T4-phase1+T6; G3-G4; W4
T8; G5; W5 T9; G6.

## D5 — 2026-11-14 — build conventions
Validation is `lean <file>` with the preset LEAN_PATH. `/opt/mathlib` is root-owned and is never
rebuilt; a `lake build` against it is not a required check and its absence is not a defect. G4's
"lake build clean" is replaced by "every file in Mub6/ elaborates with `lean` and no declaration is
left with an unrecorded hole".

## D6 — 2026-11-14 — T5 first verdicts, and three corrections to the audit
m3's submission accepted: the constant table (45 rows), `N112.md`, `handoff-1.md`, six re-runnable
experiments. Independently verified the window (47 exact, 128 from int8), the reuse-reach threshold
at N = 110 and the offset counts 19/163/2869, the M >= 51 no-merge threshold, the 1.25x tangent
margin, and the two new seed-stage defects. m6 rejected: its restatement of m3's files introduced a
false "reuse ceiling" ((2NR/3)^9 compared against a compression ratio), a circular centre-count
model, and a mis-scoped k <= 10 claim; m6 continues under its own direction d4 (global conditioning),
which no other member covers.

Corrections applied to results/code-audit.md rather than left standing:
- F2: the sign threshold is M <= 26, and the stronger fact is that no merge is possible for M <= 50
  at all, so clustering is a no-op on three of the four Stage-C grids.
- §4: "every margin clears its error by 2-3 orders" was wrong. Median 200x, tightest 1.25x
  (Candidate external tangent, .00012 vs .00015 rad).
- New F11: N = 112 is defensible but not by the printed reason (window [47,128] from coverage and
  int8; the |k| = 2 reuse shell opens at 110; 112 = 16*ceil(3.5/(16R))).
- New F12: (2.8)'s first inequality cannot reject on well-formed tuples and the live filter has zero
  analytic slack; and A.3's RN^2 hard-codes 112, so changing N would silently certify 2R.

Consequence for the plan: T5 P5.2 is discharged for N, R, N_u, the (tau,w) pairs, the caps and the
margins. What remains open is the retained-centre curve as a function of N, which needs T3's
instrumented run, not more argument.

## D7 — 2026-11-14 — TWO PREMISES OVERTURNED. Read before any further work.
Verified at source, by me, this round:

1. **The authors' code is (at least partly) public.** `github.com/openai/math` exists, is public, and is
   owned by the `openai` account. That invalidates the premise on which the project was designed
   ("sources not available", recorded in D1 and in every swarm task). Two limits survive: I could not
   confirm the specific path claimed by a member (`saved-run/compiled-build/source/`) — the tree API
   is truncated and no `.cpp` appeared in the listing I could retrieve — and publication is not
   provenance, since the paper's VERIFY.md reportedly publishes no hash check, log or machine record.
   Consequence: T2/T3's task changes from "reimplement the specification" to "locate, hash-match
   against `extraction.json`, and audit the actual sources, with the independent implementation kept
   as a cross-check rather than as a substitute". No artefact may call the code audited until a file
   is fetched and matched.

2. **An independent proof of N(6) = 3 exists.** arXiv:2611.06917, "Using topology to reveal all
   mutually unbiased bases in dimension six", Mateo Cárdenes Wuttig and Joseph Tindall, 4 Nov 2026
   (quant-ph). Route: a connectedness theorem for order-six complex Hadamard matrices modulo Tao's,
   reducing triples to finitely many overlapping four-dimensional phase balls, certified by interval
   arithmetic; it also classifies all MUB sets in dimension six. Its abstract credits this preprint as
   the prior report. Consequence: the paper under revision is no longer the only evidence, and every
   document must say so. T8's framing, T7's comparison section and T1's inventory entries change
   accordingly; "M(6) = 3 is still open" is now a defect wherever it appears.

3. **A prior Lean development for this problem exists** in the same repository:
   `lean/OAI/Analysis/MutuallyUnbiased/` defines `N6` as the supremum over attainable family sizes,
   and `lean/ComparatorChallenges/MUBSix.lean` contains Tao's matrix, Hadamard equivalence and the
   character construction. T4 must extend or explicitly reconcile with it; a parallel namespace is a
   defect in its own right. This also replaces an assumption in D2 about the formalisation landscape.

## D8 — 2026-11-14 — wave-1 verdicts
Accepted: T1's catalogue (91 entries, 178 acyclic edges, notation table, reader path) as the canonical
inventory, with two corrections (external status; repository existence and the Lean development);
T1's assembly spine (`Interface.lean` compiles with no imports, no axioms, no sorry; Thm 1.1 shown
*equivalent* to six stage statements plus seven terminal predicates, with "up to equivalence" absorbed
by class membership); T2's Lean arm (Lemma 5.1 proved in full from the Gram hypothesis, Gauss sums,
Lemma 6.5 arithmetic — all three files compile under `lean`); T2's reference model (30/30 checks, and
the finding that Table 1's "pairs" means 85,349,292 x-tuples x 1.78 y-tails = 151,744,086, plus the
`sqrt(42)/2` mis-render in the extracted text); T7's framing and comparison work (both premise findings,
verified at source).

Rejected: T4's member that claimed Lemma 5.1 is FALSE — it is true, and I derived it independently:
with `z = T*x`, `||x - T z||^2 = ||x||^2 - 2||z||^2 + ||T z||^2` and `||T z||^2 >= (1-o)||z||^2` give
exactly (4.6); the reported witness with `o_P = 0` forces `eps = 1` and is the equality case. Two
independent proofs (the Lean file and my derivation) refute it. And T1's second catalogue, on the
grounds that a parallel inventory is worse than one imperfect one, plus its false "still open" entry;
it was asked for a reconciliation diff instead.

Also corrected, in my own deliverable: the Stage-C no-merge threshold is M <= 50 (not 41, and not the
"no merge at M = 24" of the original audit).

## D6 — 2026-11-14 — the sources are public; the code arm is re-based on reproduction

Owner-approved after the sources were located. The seven C++ sources, the ABI/arithmetic probe,
`build.sh`, `check_records.py` and the whole saved run (a 100-command DAG and ~50 MB of artefacts) are
published under Apache-2.0 in `openai/math`, directory
`preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/verification/`
(last change 2026-10-26, commit `42907c9e`). The seven files hash-match
`verification/code/extraction.json`. **D1's premise is therefore void**, and this decision replaces it
for the code arm only:

1. The code arm is the recreation programme of `results/recreate-code-plan.md`, **mode C**: hardened
   re-implementation behind a frozen interface, with a `faithful` build (upstream TU shape and flags)
   held to byte-identity and a `portable` build held to structural equality and the checker.
2. T2 (`work/02-checker`) is absorbed by that programme's WU-10; T3's reference implementation is the
   programme itself. Neither runs separately.
3. The interval-arithmetic rationale in `results/plan.md` §2 no longer motivates the code arm. The
   accuracy goals of `results/plan.md` §1 stand unchanged.
4. Byte-identity against the recorded artefacts is the primary criterion. The structural fallback in
   `results/recreate-code-plan.md` §5 is fixed in advance; switching to it is a recorded finding, not
   a quiet adjustment.
5. Upstream is Apache-2.0: derivative work keeps the notices and records, in `docs/provenance.md`,
   which module derives from which upstream file, from which commit, and what changed.
6. Unchanged: D2 (scoped formalisation), D3 (one preprint), D4 (waves — the code arm and the Lean arm
   stay in separate waves for CPU reasons), D5 (Lean conventions).

Baseline measured before any team was staffed, on this VM: upstream builds; both probe builds pass;
upstream `covrun` reproduces the recorded `centers.txt` byte for byte (`c48bc9a2…`, 7 339 546 B,
402 s); upstream `arun` part 0 costs 21.5 ms/centre.

## D9 — 2026-11-14 — second wave of verdicts; four verified errata in the paper
Seven submissions judged, all accepted. T5 and T7 ended solved.

**RETRACTED 2026-11-14 — the four "errata" below are all wrong. Do not print them.**
I checked each against `pdftotext` output instead of the rendered page, and pdftotext drops the
radicals that LaTeX draws on the line *above* a fraction. The rendered pages (verified by
`pdftoppm` + inspection) show the paper is correct in all four places:
- Lemma 4.4 prints `b = sqrt8 ||M||` and `b = sqrt6 ||S||` (the radicals sit on the preceding line),
  agreeing with A.5's `C = pi*sqrt8*mnorm` and with `C < 20`. No missing square root.
- (3.24) prints `sqrt(6 * 42)/2 * h^2`, whose square is `63 h^4`. Exactly right; the paper's own
  prose says so ("p + sqrt(6*42) h^2/2"). My 2646 came from reading `6 * 42` without the radical.
- (4.29) prints `S_Delta/pi` *inside* the radical, as the code requires. I misread the bracket.
- (6.3) prints `sqrt(1 + (2 pi sqrt2 / 6) f0)`, i.e. coefficient `sqrt2 pi/3` — the value the member
  derived as "correct" and then reported as a defect. The paper already has it.
What survives of that audit: the (6.8) observation is real but may equally be an extraction artefact
(bars are a separate glyph); state the requirement, never call it a misprint. The (6.5)/(6.15) clash
of two different `S` is a notation defect for the table. The implicit-edge list and the S-claim
triage stand, and those are the parts of that submission worth keeping.

**Binding rule from now on:** no claim about a displayed formula may be made from `pdftotext`,
`-layout` or `-raw`. Radicals, overlines, superscript placement and bracket extents must be checked
on the rendered page (`pdftoppm -r 150 -png` then inspect). Two members flagged this trap before I
fell into it; T9 gets it as a standing red-team item, and T8 must not print any formula-level claim
that has not been checked this way.

**N = 112 is now settled three ways:** coverage gives N >= 47; the `int8_t` bin difference gives
N <= 128; the reuse reach gives N >= 110, and 112 is the smallest multiple of 16 above it. And the
sharpest: `testBucket`'s threshold hardwires 112, so the *printed* pipeline is sound only for
N >= 112 — 112 is the left endpoint of the window it is itself consistent with.

**Table 1's "pairs" number** is not derivable from the filters as described: one replay reproduces
the paper's 22,829 X-lists exactly, and then the Y side admits at most 112,160,350 pairs, not
151,744,086. It is a run count of undefined scope, and the paper should say which product it is.

**Formalisation status:** the assembly implications (2.10, 3.11, 4.16, 5.7, 5.8, 6.9, 7.1, 1.1) are
proved as implications with every S/C premise a named binder; Lemma 2.5 and Lemma 5.1 are proved;
Lemma 6.1's bin displacement is the single remaining hole, shared by two members. Section 5.1-5.6
(Stage B relations) is *not* stated, and T8's status table must say so.

## D7 — 2026-11-14 — certificate programme proposed, not started
`results/certificate-plan.md` is the owner's next decision. It supersedes the code arm of
`results/plan.md` and absorbs `results/recreate-code-plan.md` (mode C for the proposer side only),
and reorganises gates G0-G6 into human-initiated phases H0-H5. D1 is stale: upstream sources and
the run record are public (cached at `.scratch/gh/upstream/`). No phase is launched; the next human
input is H0 (approve scope, choose what to measure for the Stage-C witness route, set the compute
budget). Until then, nothing in the plan is an agreed output.

## D8 — 2026-11-14 — plan APPROVED; H0 open
Owner approved `results/certificate-plan.md`, set the H0 compute budget to **one week**
(2026-11-14 → 2026-11-21) and authorised **both** swarms at six members (Q4 Stage-C witnesses,
Q3 Root/atlas re-derivation). Scheduling rule of §3 stands: one swarm + one heavy compute job at a
time, Lean never against a swarm. Q4 launches at H0 (feasibility decides the Stage-C route); Q3 is
held for H2. H0 gate G0 is a human decision: go/no-go, Stage-C route, schemas v1.

## D9 — 2026-11-14 — H0 budget corrected to ONE HOUR
Owner's second message supersedes D8's one-week H0 budget: **H0 = one hour** from the launch of the
Stage-C swarm (20:15 UTC 2026-11-14, so G0 material is due ~21:15 UTC). Both swarms remain
authorised at six members; Q3 stays held for H2. H0 is rescoped to fit: upstream manifest + saved
run fetch, specs drafted at v0 (not frozen), seed-stage arithmetic micro-benchmark, Stage-C
feasibility verdict from swarm smwguhf32. Everything else in the original H0 (schema freeze at v1,
full replay baseline, controls) moves to H1. A route verdict plus measured counts is the gate input;
"schemas frozen" is explicitly NOT claimed at G0.

## D10 — 2026-11-14 — preprint draft of the formalisation results
`work/08-paper/mub6-formal.tex` (+ PDF, 11 pp, compiles clean, no undefined references).
Scope: the formalisation results only, not the source's proof. Structure: the source's trust
structure; the assembly as an equivalence; the driver gap (Thm 7.1 needs a bookkeeping hypothesis it
does not state); the disputed Lemma 5.1 settled; what is proved / stated / absent; the hole
inventory (16 modules, 23 holes over 7 of them, 3 stubs); five specification defects; threats to
fidelity, including the withdrawn formula-level claims and the rendered-page rule.

Deliberately excluded, pending the owner's framing decision (D3): the reproduction programme's
byte-exact `centers.txt`, the parameter justification in full, and the comparison with the
independent proof beyond one paragraph. Those belong in whichever shape the paper takes next.

Counts verified against the tree before typesetting: 16 modules in `work/04-lean/Mub6/`, 23 declared
holes, 7 modules carrying them. Two prose counting errors were caught and fixed during the build.

## D10 — 2026-11-14 — H0 evidence complete; G0 recommendation only
Full Stage-C probe replay: 92/92 commands, 92/92 bad outputs byte-identical; 23,343 completed
negative graph searches and 163 capped/unresolved records, zero other categories. Two Q4 submissions
accepted after review (criterion/Lean reduction; branching positive controls). G0 recommendation:
route (a), proceed to H1 with schemas v1 deferred to that gate and an exact Stage-C pilot first. No
human G0 decision has yet been recorded and H1 is not launched.

## D11 — 2026-11-14 — H0 reopened with a NINE-HOUR budget
Owner again approved the plan and authorises both six-member swarms, superseding D9's one-hour H0
budget with **nine hours of deeper H0 feasibility work**. H0 had already produced a complete G0
recommendation (D10). The lead interprets this literally as reopening/extending H0, **not as human
initiation of H1**. Q4 receives a six-member continuation on the unresolved Stage-C feasibility
questions, reading the accepted reports and full replay statistics rather than repeating them. Q3
remains authorised at six members but held for H2 under the approved phase structure. Schemas are
still v0 and no exact exclusion is claimed certified.

## D12 — 2026-11-14 — H1–H5 APPROVED; EIGHT-HOUR execution window
Owner explicitly approves H1-H5 and authorises **8h compute**, superseding the lead's conservative
reading of D11 (H0-only continuation). Work therefore proceeds beyond feasibility into implementation
and verification: H1 seed/checker/schemas/controls, H2 Stage A/atlas with the authorised six-member
Q3 swarm, and Stage B/C/assembly/report as far as measured progress permits within the window. The
existing Q4 continuation `smwgx104w` is adopted into the Stage-C work rather than duplicated. H5 must
condense actual artefacts and must not imply the full target statement was established if exact
checking remains incomplete. This eight-hour window does not erase the full programme's longer
schedule or the requirement for an honest final gate/limitations report.

## D13 — 2026-11-15 — H1 evidence achieved under D12, awaiting human gate
Lead seed evidence and independent exact checker completed; see certdata/runs/h1-seed-emission/.
No human review or approval of the written report has been given. Stage A/atlas and full Stage B/C
remain unproven, and the alternate high-cap Stage-C simplification remains a proposed new execution.
Historical inputs are reused only through hash-identified new witnesses, not by assuming that the
authors' execution was independently certified.

## D14 — 2026-11-15 — Stage-C continuation closed with three accepted directions
Q4 swarm smwgx104w ended solved: accepted coverage, Lean reflection, and cap policy. Its three
remaining directions (fidelity, padding, compact search witnesses) ended without solutions and
are open. Correct schema composition is 57,104 B with 515,236 relation marks + 7 snap-closed
cells = 515,243 inside cells; 47/47 mutations reproduce. Saved reports in work/02-checker/ and
data in certdata/runs/h1-coverage. Baseline remains archived fallback. High-cap one-pass is only
a conditional alternative, not a completed certificate or a deletion of upstream Stage-B cover.

## D15 — 2026-11-15 — composition identifier correction (lead)
The previous composition-v1 block's parent address convention was wrong (14/163 correct). Repaired
by joining actual capped batch indices with local bad-file ordinals, producing 163/163 correct
addresses with unchanged counters and links. New SHA-256 fd61d25749c9ba55cd3082af7023b1b52b09c4715b64fdc2dbcac54616e0f819.
See results/composition-repair-note.md. The old object is retained only as an audit example.
Header order corrected to pass_id,n_parents,n_children,n_links with no reserved word. This is an
identifier/notation fix, not a geometric-cover certificate. Root mnorm slack semantics documented;
g0 serialisation/index-order finding remains under review rather than accepted as a fidelity refutation.

## D16 — 2026-11-15 — evidence repairs and bounded transport/search
The lead rebuilt and byte-compared composition-v1 (fd61d257…), verified the
repaired map (83516ece…), recorded the deliberate patch, and reran the schema
mutations (47/47). The m4 d5 submission was rejected: g0 has eight valid ball
permutations, not a unique one. Its lead-corrected auditor passes 55 claims
(42 CERTIFIED/4 CONTRADICTED/9 UNSUPPORTED) and 26 controls; all structural and
analytic limits remain visible.

The bad10#0 witness now also has an exact source-direction transport bridge:
Relation(P,R,Phi Q) = Relation(Phi^{-1}P,R,Q) on all compared fields and at ell
for all 902 edges; 303 used edges and 3161 cover inequalities pass. The source's
Proposition 5.7 uses certified child spheres up to equivalence; a separately
invented Phi-Q ledger is not a new theorem obligation. All root/analytic/global
obligations remain.

Targeted swarm smwh5efk8 ended solved with four accepted scoped contributions:
conditional assembly, local Stage-B cover, bounded exact clique decisions (four
distinct real record graphs), and finite seed-symmetry/census checks plus the
refutation of the proposed orbit sum. These are not accepted as a full theorem,
an all-matrix seed invariance proof, or an all-record graph/predicate certificate.

## D17 — 2026-11-15 — first analytic specimens under D12
smwh7pmn0 has ended solved with four accepted, explicitly scoped specimens:
1. real instrumented Stage-A cell trees with exact subdivision and Root-link
   arithmetic (113, 145 and 1 nodes; 26 checks and nine controls each). Neither
   norm nor dual exclusions, nor the actual Root radius proof, is thereby certified;
2. outward MPFR basic Stage-C pair predicates on four records: 269,403
   evaluations, 133,944 certified exclusions, zero interval-undecided and zero
   graph-edge violations. Joint (6.23), the ball layer and remaining records open;
3. a Root/derived-C witness interface (M, UA, UM rational; MPFR residual) and
   34 existential witnesses for the three derived clauses. Nine remain undecided;
   declaration is not use of the original run's M, nor validation of every Root field;
4. Stage-B composition algebra: 12-map nonabelian group, all specified action
   populations and negative controls, but no actual two-level parent/child match.

The failed directions for Stage-A dual test and Stage-C joint test were not
silently closed. The still-unassigned original two-record Root matrix-emission
case is also open. No human gate or full Stage A/B/C certificate is inferred.

## D18 — 2026-11-15 — analytic witnesses and two former Root/C failures
The focused swarm smwh95wl3 is solved with two accepted bounded results:
- 20 real Stage-A dual INEQUALITY certificates, including exact-rooted frame and
  dataU chains plus 360 controls; the implication to empty cells and analytic
  majorisation lemmas remain explicitly conditional;
- joint (6.23) pair-predicate proofs on four records: 61,832 joint comparisons,
  10,293 rejections all outward-verified, zero retained-pair violations and exact
  gate/row consistency. Basic and joint pair work does NOT establish ball cover,
  all Root bounds, graph search or the record NEG verdict.

An abandoned worker's original-tensor-C report was reviewed independently rather
than accepted by inference. Two original `root != pass` rows (coarse0#678,
coarse3#33) now have explicit rescaled witnesses at exact symmetry images, and
lead computed the actual frame-projector difference bounds 7.386e-14 and 6.353e-14
(larger than the helper's 2.5e-15 claim, yet negligible versus id=2e-6).
Both witnesses pass the other basic Root/C clauses and mutations. This establishes
an EXISTENTIAL witness under Lemmas 4.4/4.7, not recovery of their original M,
original pre-canonical phases, or corpus-wide Root validity. Details:
work/02-checker/reports/H2-root-tensor-two-records.md and
certdata/runs/h1-root-interval/two-tensor-transport-check.json. No human gate
or N(6) theorem claim is made.
