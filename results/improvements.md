# What is lacking in the paper, and what action fixes each gap

Companion to `results/proof-summary.md`. Each item states the defect precisely, why it blocks a
reader, and the concrete artefact that would remove it. Effort estimates are mine, not the
authors'.

---

## A. The theorem hypothesizes an event, not a checkable object

**Lacking.** Theorem 1.1 reads: *under the arithmetic and compiler conditions of Appendix A, the
fresh complete execution documented in Section 7.5 certifies that there are no four MUBs.* The
hypothesis is therefore (i) a 100-process run on one machine on 4 Oct 2026, whose evidence is an
archive, plus (ii) the unstated premise that seven C++ files implement the specification of
§§2–6. Neither is checkable by a referee. The paper's own §7.5 says the archive "documents the
finite execution, not an automatic verification of the geometric or arithmetic lemmas" — so the
gap is acknowledged and left open.

Consequence: the proof is currently as strong as *the reviewers' reading of 4,000 lines of code
they cannot see*. One sign error — in the negative part $\max(0,\max_{i,j}(-y_{D,ij}))$ of (3.29),
in `markRec`'s $(ρ-5\cdot10^{-8})^2$ comparison, in the root deletion of Lemma 6.8 — yields a
silent false exclusion, and no reported quantity would move.

**Actions.**

1. **Separate generation from verification.** Make the seven programs *heuristic generators* of
   records, and make the theorem rest on a checker: "if $Q$ accepts certificate $C$ then
   $N(6)=3$". The proof architecture already permits this: every exclusion is a strict violation of
   a *necessary* condition, so it is a witness, not a search result.
2. **Define the certificate format as a proof object**, not a computation log (§7.1's binary record
   already carries a Root and a radius; extend it stage by stage):
   * seed stage: retained center, its rational bin indices, and for every *discarded* bin pair the
     one filter that killed it and the evaluated bounds;
   * Stage A: per seed, the list of cells together with, for each excluded cell, the direction $y$
     and the evaluated two sides of (3.26) or (3.29); for each retained cell, the Root constants;
   * Stage B: per emitted record, the center, the frame $T$, the eight constants, the radius $τ$,
     and the parent index;
   * Stage C: per record, the ball centers and radii, and **the $O$ and $U$ adjacency sets**.
3. **Write the checker in exact arithmetic** (rational or interval at ≥100 bits), covering:
   Root constants against (4.4)/(4.15); cell exclusion inequalities; ball covering radii
   (Lemma 6.4); edge tests (6.16)/(6.20)/(6.21)/(6.23); atlas merge distances (Lemma 4.15).
   Target size: the checker should be small enough for one person to read — a few thousand lines.
4. **Solve the clique-exclusion certificate problem — this is the genuine obstruction to (3).**
   "No two disjoint six-cliques with all 36 cross edges" has no obvious compact witness, so a
   checker either re-runs an exponential search (not a certificate) or trusts the 5,000,000-step
   engine. Two acceptable resolutions: emit a resolution-style refutation over the retained graph
   (the search of Lemma 6.8 enumerates least-vertex branches, which is close to a DPLL trace —
   emit it as a DRAT-style proof and let a standard checker verify); or prove *a priori* that the
   retained graphs are sparse enough that exhaustive verification of the pattern is polynomial in
   practice, and report the observed cost. Until one is done, the Stage-C conclusions remain
   unverifiable in principle, not merely in practice.
5. **Audit the bookkeeping separately from the mathematics.** The completeness half — every bin
   visited, every child covered, atlas radii only growing, unresolved counted — is what §7.2–7.3
   specifies in prose. Turn that into a machine-checked trace property (each stage emits a count of
   regions entered/excluded/unresolved, and the checker recomputes the sums in Table 1).
6. **Ship a second implementation of the seed cover.** It is the one stage that is nearly
   self-checking: each of the 151,744,086 bin pairs is either killed by a local filter or covered by
   a local comparison with one retained center, so an independent program over `centers.txt`
   should reproduce the 249,878 centers. Disagreement localises a bug to one stage.

**Cost.** Checker + formats: substantial but mechanical; the clique witness (action 4) is the
research-flavoured piece and should be scoped first. Benefit: the paper becomes a proof with a
short trust base instead of a computation with a long one.

---

## B. The arithmetic model is asserted, not eliminated

**Lacking.** The theorem depends on binary64 semantics of a specific build. The paper states the
premises (§7.1, A.1), probes the platform (FLT_EVAL_METHOD=0, MXCSR 0x1f80, sqrt and
gradual-underflow samples), and then concedes: "these probes provide limited evidence for the
stated platform conditions, not a proof of all primitive-operation or compiler semantics. Those
semantics remain assumptions." A further *code-generation* condition is needed and is discharged by
inspecting a saved disassembly for the two `pow(·,2)` calls at hex addresses `6035, 6039, 603d,
605c, 606d, 608b` — a check on one binary, void for any rebuild (the paper says so).

So ~20 pages of Appendix A convert assumptions into bounds. Two structural problems: (i) every
budget is tied to a particular evaluation order, so refactoring code invalidates the proof; (ii) the
argument is not robust to a *different but equally correct* rounding outcome — the paper repeatedly
has to prove that "a different valid rounding outcome may increase unresolved work without
invalidating a certificate", which is true but is proved case by case.

**Actions.**

1. **Migrate all certificate evaluations to outward-rounded interval arithmetic** (MPFR with
   directed rounding, or rational endpoints where the values are dyadic). Then "the stored number
   is an upper bound" is a theorem of the library, uniform in evaluation order.
2. Delete, as a consequence: the `-march=native` dependence, the disassembly check, the platform
   probes, and A.1–A.12 down to a short premises section (expair accuracy, π, the interval
   library's own correctness). Estimated reduction: 20 pages → 3–4.
3. Keep the crude constants but recompute them in interval arithmetic; several (e.g. $z<1.5$ where
   the truth is far smaller, the $\pi b$ remainders) can then be tightened for free, which will cut
   subdivision depth and the 163 graph-cap failures.
4. Report the cost. The whole run is 4,470 s of wall time; even a 10× slowdown from interval
   arithmetic is affordable.

**Cost.** The propose/certify split means only the *certify* predicates need porting; that is the
place to spend engineering effort. This is the highest ratio of risk removed to work done.

---

## C. There are no controls, and the risk locus is unreported

**Lacking.** The pipeline's entire force is "nothing survived". There is no evidence that the
pipeline *can* fail to exclude when it should, and no report of how close any accepted certificate
came to its threshold. Meanwhile the run itself points at a risk locus: 163 of 22,379 Stage-C
records hit the 5,000,000-step graph cap, and those are precisely the records where the automatic
argument was weakest; the whole burden then rests on a B fallback and a second C run using the same
cap.

**Actions.**

1. **Run the pipeline in $d=2,3,4$.** These are decisive and cheap:
   * $d=2$: $N(2)=3$, so coordinate basis + Hadamard + two further bases would be four — it must
     be **excluded**. A positive control: the code paths run end to end.
   * $d=3$: $N(3)=4$, so that configuration **exists**; the analogue pipeline must terminate
     unresolved, never negative. A negative result here is a soundness bug, full stop.
   * $d=4$: $N(4)=5$, same expectation as $d=3$.
   These three runs cost minutes and are the cheapest bug-catcher for the exclusion logic in the
   paper.
2. **Reproduce the rigorous antecedents for the stated reason.** Grassl's case (standard + Fourier
   pair) and the Fourier-family result of Jaming–Matolcsi–Móra–Szöllősi–Weiner must be excluded by
   Stage C with a *cleared* certificate, not by cap exhaustion. Report which test did it.
3. **Publish slack distributions.** For each test class, the minimum over the run of
   (established error margin) and the argmin record; the observed range of $z$, $q$, $ρ$, cell
   count per seed, nodes per seed, graph steps per record, vertices per graph. A single histogram
   per stage answers "is this knife-edge?" — currently unanswerable.
4. **Characterise the 163 hard records.** Sizes, vertex counts, densities, which test nearly fired,
   and what the fallback changed (radius $.016\to.011$). If the exclusion in that region depends on
   one margin, say so.
5. **Mutation tests.** Perturb one certificate threshold by $+10^{-9}$ (or one bound in the
   generator by a relative $10^{-6}$) and confirm the pipeline reports *unresolved* rather than
   success. A proof whose checks are too loose to notice perturbations is not checking what it
   claims.
6. **Independent sample recomputation.** Re-verify a random 100 records (Root constants, ball cover,
   graph verdict) at 200-digit precision with separate code. This is the cheapest partial answer to
   the trust gap if the full checker (item A) is not built.

---

## D. The human-checkable mathematics is not formalised, and it is the formalisable part

**Lacking.** The paper separates mathematical lemmas from floating-point budgets, but nothing
separates *correct* lemmas from *plausible* ones. ~50 lemmas are asserted with proofs of one to
fifteen lines; a reader must trust all of them.

**Actions.**

1. **Formalise in Lean 4 / Mathlib the lemmas that need no floating point.** In rough order of
   cost, cheapest first: 1.2 (Gauss sums, elementary), 2.2, 2.3, 2.5, 2.6, 2.7, 2.8, 6.1, 6.5,
   5.1, 3.1, 3.8, 3.9, 4.11, 4.12. Then the fiddly ones: 2.4 (combinatorial gap arrangement),
   2.9, 3.4 (trig Taylor bounds), 3.2 (polar decomposition plus trace defect), 4.3/4.4 (remainder
   constants), 6.2/6.3/6.6/6.7 (Taylor remainders with the 2π normalisations).
2. **Formalise the composition, not the search**: Propositions 2.10, 3.11, 4.16, 5.7, 6.9 and
   Theorem 7.1 are conditional implications ("if the region list has property P then coverage"), and
   they are the part where an error would be most damaging and least visible.
3. **Leave the interval evaluations to the checker of item A**, and state the interface as an
   assumption: "the checker's certificate inequalities hold". Then the formal statement is honest
   and finite.

**Cost.** This is a multi-person-year project, so it should be scoped: a formalisation of Lemmas
1.2, 2.2, 2.3, 2.5, 5.1, 6.5 plus Propositions 2.10/5.7 as implications is a realistic first target
and would already catch the class of error that matters (a mis-stated induction or a wrong
quantifier).

---

## E. The statement should be finite; the provenance is confusing

**Lacking.** (i) The theorem quantifies over "the fresh complete execution documented in Section
7.5" — a hypothesis by reference to an event. (ii) The manuscript is dated 24 Sep 2026, the run it
relies on is 4 Oct 2026, and §1.2/§7.5 repeatedly disown a 7 Sep 2026 run ("the complete evidence
packet ... was not recovered"; "this agreement does not authenticate the earlier execution"). A
reader cannot tell what the 24 Sep version asserted, or why a disowned run is discussed at length.
(iii) The abstract says "resolving Zauner's dimension-six MUB conjecture" without flagging that the
novel half is the *upper* bound and that the claim's force is the computation.

**Actions.**

1. **Restate as two statements.** (a) A finite, checkable theorem: *let $C$ be the certificate with
   the digests of Table 2; if the checker of §X accepts $C$, then no four MUBs exist in
   $\mathbb{C}^6$.* (b) A separate empirical statement: *$C$ exists, was produced by the documented
   run, and is archived at ...*. Then a reader knows exactly what to distrust.
2. **Give a change log** from the 7 Sep run and the 24 Sep draft: what was re-run, which constants
   or sources changed, which claims were withdrawn. If the earlier run is irrelevant, delete the
   discussion; if it is relevant, say how.
3. **Reword the abstract** as "proves the upper bound $N(6)\le3$, hence $N(6)=3$ given the explicit
   three-basis construction", and state the conditional status in the abstract itself, not only in
   Theorem 1.1.
4. **Say what a reader can reproduce in a day**: the checker on the archive, or the $d=2,3,4$
   controls. Add a container/`make` target that reproduces Table 1 on a specified machine class.

---

## F. Presentation: three layers interleaved, code behaviour in prose

**Lacking.** Each of §§3–6 mixes (i) ideal mathematics, (ii) assertions about what a named routine
does — `extend` "begins with $[-1/2,1/2]$ and intersects these constraints", `spectralUpper` "uses
their minimum with margins", `markRec` "keeps a branch only while ..." — and (iii) numerical
budgets. Layer (ii) is unverifiable from the document, and a lemma's validity often depends on it.
Notation is overloaded: $D$ (comparison block) vs $\hat D(t)$ (Stage-B iteration); $n_P$ (normal
polynomial, then normal displacement); $m$ (pair of lower singular bounds) vs $m_j=|D_j|$;
$\epsilon$ (center correction) vs $\varepsilon_{\exp}$; "ball/cell/bin/box/sphere/Record/Root".

**Actions.**

1. **Split the document** into: a mathematics paper (statements with code-free hypotheses, proofs,
   and the five stage conclusions in one place); a **specification** of each routine as
   pre/post-conditions written as inequalities; a verification report (Appendix A's content, in
   interval form); and a code appendix with the checker-sized fragments.
2. **Add three maps**: lemma → routine(s) → Appendix subsection certifying its margins; a dependency
   graph of the five conditionality chains; a notation table.
3. **Collect the spine** — 2.10, 3.11, 4.16, 5.7, 6.9, 7.1 — as a numbered "assembly" section, so
   the composition can be read in five pages without the machinery.
4. **State the global convention once**: all sets closed, covers may overlap, unresolved is never a
   negative.

---

## G. Smaller, still worth doing

* **Corollary 1.3** (Cartan subalgebras) adds nothing to the MUB claim and rests on a 2005 preprint
  for the correspondence. Either prove the correspondence or drop the corollary.
* **Stage A's $U(2)$ cover over-counts by roughly $8\times$** (each completion lies in many cells),
  which inflates the cell tree, the record count, and the number of Stage-C cap hits. A reduced
  parametrisation (or a canonical cell choice) would shrink the pipeline and make the run easier to
  reproduce.
* **Crude constants propagate into cost.** $z<1.5$, $q<.32$, the $\pi b$ remainders: tightening them
  (cheap once interval arithmetic is in place) reduces subdivision depth and record counts.
* **Report archive size and checker cost.** A certificate proof is judged partly on whether the
  certificate is small enough to be checked by someone else. The paper never says how many bytes
  the evidence is, or how long re-verification takes.
* **State failure modes as a table**: for each stage, what a *single* bad region would do (seed:
  unresolved → whole run fails; A: failed seed → no conclusion; B: bad parent stays on the RHS of
  (5.26); C: cap → saved bad record). Most of this is in the text, scattered; one table would show
  the proof's robustness profile.
