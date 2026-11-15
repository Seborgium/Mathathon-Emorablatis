# handoff-2.md — from T4-Lean (m2) to T9 (red team)

- **from**: m2 (swarm `smwgrrpxy`, direction `d3`: scaffold + §1–2)
- **to**: T9 (red team), via `work/09-redteam/`
- **version**: 1, 2026-11-14 19:50, Lean 4.33.1 + shared pre-built Mathlib
- **depends-on**: `Mub6/{Basic,Hadamard,Seed,ThreeMUB}.lean`, `Mub6/AxiomCheck.lean`,
  `reports/{statements,status,DEPGRAPH}.md`
- **blocks**: any claim that §1–2 is "done"; the fidelity review of other members' statements
  (the carrier conventions below are binding on them)
- **artefacts**: same four modules plus `reports/status.md` (axiom footprints) and
  `reports/statements.md` (binder-by-binder table)
- **claims touched**: Lemma 1.2, Lemma 2.2, Lemma 2.3, Lemma 2.5; carriers for every other claim
- **open questions**: the eight attack items in §3

## 1. State of the code

Four modules compile with `LEAN_PATH=$PWD:$LEAN_PATH lean Mub6/<f>.lean`, exit 0, one file at a
time.  38 of 48 theorems are proved; 10 are statement-only and their `#print axioms` shows
`sorryAx` (verbatim output in `reports/status.md`).  **There are no user-declared axioms.**

The ten `sorry`s, in the order a red team should attack them:

1. `Hadamard.extendible_transposed` — the paper's own "only non-obvious case".
2. `Hadamard.extendible_iff_all` — **the most dangerous declaration in the tree**: it is a packaged
   *two-sided* claim, and it is **not** derived from the six one-directional clauses.  If it is
   cited as if it were, that is a false claim of composition.
3. `ThreeMUB.three_mub_exists` — the existence theorem of Lemma 1.2.
4. `ThreeMUB.FDF_entry` — the `F*DF` entry identity.
5. `Seed.gap_stability` — Lemma 2.5 with an arbitrary matching.
6. `Hadamard.extendible_rephaseCols` / `extendible_rephaseRows` / `extendible_permCols` /
   `extendible_permRows` / `extendible_conjMat` — the remaining Lemma 2.2 clauses.

## 2. Assumptions a reviewer should confirm are *not* hidden

* `IsPhaseHadamard` is one-sided (paper Def 2.1).  Mathlib's two-sided `Matrix.IsHadamard` is
  consulted for the survey only; the bridge `IsHadamard.of_mul_conjTranspose` is never invoked.
* `UnbiasedH H K := ∀ i j, normSq ((Hᴴ*K) i j) = 6`.  Derivation: with `H = √6 U`, `K = √6 V`,
  `(HᴴK)_{ij} = 6 (UᴴV)_{ij}` and `(UᴴV)_{ij} = ⟨v_j, u_i⟩` in the paper's convention, so the
  squared modulus is `36 · 1/6 = 6`.  **Check this index convention independently** — it is the
  single easiest place for a `1/6`-versus-`6` slip to hide, and every later statement inherits it.
* `Extendible H` does not include "unbiased to the standard basis" as a conjunct; that is implied by
  unit modulus.  If a reviewer disagrees, the paper's Def 2.1 reading (B8 in `statements.md`) is the
  place to argue, not the Lean file.
* `circularDist` is `min |s-t| (1-|s-t|)`, correct on `[0,1)` only; `gap_stability` carries the
  range hypotheses `x i < 1`, `y i < 1`.  A red-team finding that `circularDist` is not the circle
  metric off `[0,1)` is *correct but out of scope* — the hypotheses exclude it.

## 3. Eight things to try to break

1. **Normalisation.** Re-derive `UnbiasedH` and `UnbiasedBases` from Definition 2.1 without looking
   at our note.  A wrong factor of 6 in one of the two would make every §2–§6 statement vacuous or
   false while still compiling.
2. **`Extendible` faithfulness.** Is "two further Hadamards pairwise unbiased" *equivalent* to the
   paper's "the standard basis and the columns of `H/√6` belong to a family of four MUBs"?  We claim
   yes because `|H_ij| = 1` forces unbiasedness to the standard basis.  Check the corner: could a
   four-MUB family containing the standard basis have a member whose entries are *not* unit modulus
   after scaling?  (Answer should be no; if yes, our `Extendible` is the wrong predicate and every
   §2 equivalence is about the wrong object.)
3. **Lemma 2.3's norm bound.** `Pi_frobSqR_le` proves the *squared* Frobenius inequality via
   `frobSqR z = frobSqR (Πz) + frobSqR (z - Πz)`.  Check the cross term is genuinely zero:
   `sum_mul_rowcol_zero` needs *both* the row-sum and column-sum vanishing — if only one were used,
   the lemma would still compile (as a weaker true statement) but would not be the paper's.
4. **`sub_Pi_eq_rowcol` witnesses.** The explicit `r i = (1/6)∑_b z_ib - (1/36)∑_{a,b} z_ab`,
   `c j = (1/6)∑_a z_aj` must sum to `z - Π z`.  If they do not, the coefficient of the total sum
   is wrong and Lemma 2.3's rephasing sentence fails.
5. **Lemma 2.5's gap.** `seedGap` is the **largest** of the six arcs, with the wrap arc `1 - x 5`,
   and requires `Monotone`.  Attack: is the paper's gap the largest gap or the *minimum* gap?  §2.2
   says "largest circular gap"; Lemma 2.4 selects the pair by the *minimum*.  Confirm our reading
   (largest) against the paper's use in Lemma 2.6, where `g_{x,mid} ≤ 1 - (l-1)/N` and
   `g_y ≥ g_x`: that inequality only makes sense for the largest gap.
6. **Lemma 1.2's Gauss sums.** `gauss t = ∑_{x<3} ω^{x²+tx}` for `t ∈ {0,1,2}` gives `1+2ω`,
   `2+ω²`, `2+ω²`.  Check against `(F*DF)_{jk}` for all nine `(j,k)` including `k < j`, where the
   exponent in the paper is negative before reduction mod 3 (`ω^{-1} = ω²`).
7. **The vacuity check.** None of the statements in §1–2 should be vacuous: `three_mub_exists` is an
   existence claim (not vacuous by construction), and `IsPhaseHadamard` is satisfiable (`Fmat` is a
   candidate once `FDF_entry` is proved).  A useful cheap audit: exhibit one concrete
   `IsPhaseHadamard` matrix in Lean and check `normSq` on all 36 entries.  We did **not** do this;
   it is the cheapest independent check that the predicate is not empty.
8. **The composition gap.** `extendible_iff_all` and `FDF_entry` and `three_mub_exists` are all
   `sorry`; so the *chain* "Gauss sums ⇒ three MUBs" is not machine-checked at its last step.  If a
   downstream paper sentence says "Lemma 1.2 is formalised", this is the counterexample to that
   sentence.

## 4. What we did not do, stated plainly

* No proof of any §3–4 or §5–6 claim; no proof of Lemma 2.2; no proof of Lemma 1.2's existence
  statement.
* No identification of `Π` with a library orthogonal projection (Mathlib has no inner-product
  instance on `Matrix`; see `DEPGRAPH.md` §4).
* No `native_decide`, no `lake build`, no vendored Mathlib.
* No instantiation of m3's `Interface` coverage lemmas to the paper's specific region lists — the
  place where the brief says a mis-stated induction would be invisible.  `DEPGRAPH.md` §5 flags it.

---

## handoff-2 (section) — from m4 to T9 (red team)

- **from**: m4 (swarm `smwgrrpxy`, direction `d2`: §3–4)
- **to**: T9 (red team), via `work/09-redteam/`
- **version**: 1
- **depends-on**: `Mub6/{Basic,Frames,Exclusion,Ellipsoid}.lean`,
  `reports/{statements-S3-S4,status-S3-S4,DEPGRAPH-S3-S4}.md`
- **claims touched**: Lemma 3.1, 3.8, 3.9, 4.11, 4.12

**Attack these, in this order — they are the places a transcription error would be invisible:**

1. **Lemma 3.1's endpoints and orientation.** The paper's `M(M*M)^{-1}` is `(M^+)*`, not `M^+`, and
   its printed formula `(4·1 − p S̄, 4p − 1 S)` is a *row of two column vectors*. Check
   `framePseudoInvFormula` entrywise: column 0 must be `(4 − p_i S̄)/c`, column 1 `(4p_i − S)/c`,
   `c = 16 − |S|²`. A transposition here would be silently consistent with the frames of (3.5) — so
   also check `G_B = B₀*(B₀B₀*)^{-1}` against it (`B₀ = (1 p)ᵀ`, so `G_B` is the *conjugate* of the
   3.1 formula, not the formula).
2. **Lemma 3.1 is vacuous at `|S| = 4`.** `‖S‖ = 4` forces `p` to be a unimodular multiple of **1**
   and `M` to have rank 1; the kernel claim then fails. Every row carries `hS : ‖S‖ < 4`. Ask
   whether the paper's §3.1 "acceptance checks" really exclude this case for every retained seed —
   nothing in the preprint's prose does.
3. **Lemma 3.9's shared witness.** The same `g = J_all* y` appears on *both* sides of the
   derivation (in the linear bound and in (3.29)). `gsθ` is one binder for that reason. If someone
   re-derives (3.29) with independent constants, the resulting inequality is *weaker* and the
   exclusion test may fire less often; check any recomputation for that.
4. **Lemma 3.9's quadratic term sign.** The `max(0, max(−y_D))` is there because `−½Σ y_D|Z|²` has no
   fixed sign. My rendering uses an arbitrary `M ≥ max(0, max(−y_D))` — if a recomputation takes
   `M = max(−y_D)` *without* the `0`, it is wrong exactly when all `y_D > 0`. Mutate that.
5. **Lemma 4.11's `β` bookkeeping.** `(1+β)` on `AA*` and `(1+1/β)` on `BB*`, not the other way
   round; the completing-the-square identity is
   `β((1+β)r²u² + (1+1/β)q²v² − (ru+qv)²) = (√β·ru − qv)²`. Swapping the two coefficients still
   gives a true inequality for a *different* `G`, which is how such an error survives review.
6. **Lemma 4.12's use of `‖U‖² + U*G(γI−G)^{-1}U = γU*(γI−G)^{-1}U`.** This needs `G` symmetric and
   commuting with `(γI−G)^{-1}`. If a re-derivation drops the commutation, the bound is invalid for
   non-symmetric `G` — and the paper's `G` is a *certified upper bound* on a sum of two PSD terms,
   typically chosen as a diagonal or scalar matrix, so the error can stay invisible in the run.
7. **The two "any certified upper bound" steps** (`E(G;{U_σ})`, and `Λ` in
   `normSq_le_of_inEllipsoid`): the paper's prose allows replacing `λ_max(G)` by any upper bound. Check
   that the *direction* is always `G' ⪰ G` and `γ ≥ λ_max(G')`; reversing either invalidates 4.12
   while leaving the inequality true for a different `w`-set.

---

## Section m3 — from m3 (`d1`: §5-6 + assembly interface) to T9

- **from**: m3; **artefacts**: `Mub6/{Interface,Exclude,Assembly}.lean`, `reports/statements.md` §m3,
  `reports/status-m3.md`, `reports/DEPGRAPH-m3.md`; **version**: 1, 2026-11-14.
- **blocks**: nothing; **depends-on**: nothing beyond Mathlib (my files do not import `Basic`).

**State.** `Interface` and `Assembly` compile with no `sorry`. `Exclude` has exactly one `sorry`
(`bin_displacement`, Lemma 6.1). Axiom footprints: only the Mathlib defaults
(`propext, Classical.choice, Quot.sound`); `sorryAx` appears only in `bin_displacement`.

**Where an error would be invisible, and therefore where to attack.** Each item below is a binder
I turned the paper's prose into. If the binder is *false* of the code, the corresponding
proposition fails while every lemma it cites still holds.

1. **`Cover.accumulate_covered`'s `hstep` (Prop. 5.7).** The certificate for parent `p` must hold
   at the atlas state `l ++ [p]`, i.e. *after* `p` completes. If `stageB` ever inserts a parent into
   the blocker list *before* its refinement completes, the induction is circular and 5.7 is false.
   The paper claims the distinction explicitly ("a blocker is only ever an already completed
   parent"); verify it in the code's insertion site, not in the paper.
2. **`hfinal` (5.7) and (5.27).** Centres, tangent columns and Root constants are immutable after
   insertion; only `r_i` may grow, and it is written out at the cap `τ`. If any batch record were
   written with a radius smaller than the final achieved radius, `hfinal` fails. Attack: compare
   `fine.bin` radii against the in-memory final radii for the 22,379 records.
3. **`hgraph : ¬ Config G` (Prop. 6.9 via Lemma 6.8).** A negative result requires an exhausted
   search *with the give-up flag unset*. Attack: (a) is the flag set on work-cap exhaustion and on
   *every* early return; (b) is it preserved (persistent) as the code says; (c) is the root-deletion
   convention (`min(A ∪ B) ∈ A`) applied only at the root, as the proof needs; (d) mode 1 with cap
   5,000,000 — is the cap counted in the same unit the proof counts steps?
4. **`hO`/`hU` (6.6, 6.7).** These assert that the tests are *necessary*: no genuine orthogonal or
   unbiased pair is ever removed. The dangerous spot is the sign of the quadratic term in the
   directional test (3.29) and the `max(0, max_{ij}(-y_{D,ij}))` in 3.9, and in Stage C the
   `2·10⁻⁷` comparison allowances. A test that is merely *sufficient* (over-strict) silently
   removes genuine configurations and every downstream lemma still holds — this is the single
   most plausible way for the whole proof to be wrong while all of §§2-6 remain correct.
5. **`hlab` (6.4/6.9): the `δ`-uniformity and the boundaries.** `hlab` says every admissible vector
   — for *every* `δ` in the record's closed ball, and including vectors whose phases sit on bin or
   torus boundaries — lies in the labelled ball. Two failure modes: (i) Stage C builds its bins and
   balls from the centre `P` only, and the joint test (6.7) is the only place the shared tangent
   displacement enters, so a \(\delta\)-independent test must still be *necessary* for every `δ`
   with `‖δ‖ ≤ r`; (ii) boundary vectors: bins are closed and the torus is wrapped, so a vector
   exactly on a bin edge must appear in at least one retained bin path. Attack: construct a vector
   on a bin boundary and check the code's bin indexing includes both children.
6. **`Config` (6.24) itself.** My first transcription had `B` as a `U`-clique; the paper means both
   `A` and `B` are **O**-cliques with `A × B ⊆ E(U)`. If the *code* implements the other reading,
   the graph search is testing a weaker condition than the mathematics requires — check the
   auxiliary six-clique prune operates on the unbiasedness graph for the *cross* condition only.
7. **Lemma 6.5's radius hypothesis `s < .1`.** Distinctness of the twelve labels needs *every*
   ball radius below `.1` at the time the graph is built. If the clustering's final radius update
   ran after edge construction, or if the `|v_j| ≤ 2` check is applied to a stale `v`, the
   `< .1` hypothesis is not established. (The paper says the checks are on the final assignment.)
8. **Two negative paths, one of which I did not formalise.** Prop. 6.9 also allows "empty bin
   layer" as a negative certificate. That path needs only the single-vector tests and no graph;
   it is not in my Lean. If a record's negative result came from *both* paths the paper counts it
   once — check the exit-status bookkeeping does not conflate "no bins" with "graph negative" when
   reporting the 163 saved failures.
