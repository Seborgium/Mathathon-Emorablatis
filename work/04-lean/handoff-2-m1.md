# handoff-2 — T4 (Lean) to T9 (red team)

from: T4 / m1 (direction d4: fidelity & status audit, §2 gap layer)
to: T9 / work/09-redteam
version: 1 (phase 0)
depends-on: `results/proof-claims.md`, the preprint (text `.scratch/mub6.txt`)
blocks: nothing; supplies attack targets and a checklist
artefacts: `work/04-lean/reports/statements.md` (binders, generated + hand-audited),
  `work/04-lean/reports/status.md` (axiom footprints), `work/04-lean/Mub6/Gap.lean`,
  `work/04-lean/Mub6/Hypotheses.lean`, `work/04-lean/audit/{spec.py,audit.py}`
claims touched: all 17 in-scope statements; §7.2; §7.5 Table 1

## What is proved, so attack it directly

*Lemma 2.5* is machine-checked in `Mub6/Gap.lean`, no `sorry`, standard axioms only. If you think
it is false, the counterexample must defeat `Mub6.circGap_stability`. Note the formal statement is
for `Finset ℝ` with `CircDistLE`-matching — a counterexample using **multiplicities** (two points at
the same phase) does not apply, and that is the deliberate change recorded in
`reports/statements.md`. A counterexample using a *one-sided* matching also does not apply: the
difference form takes both directions; the one-sided form `isEmptyArc_transfer` is a strictly
stronger statement and is the one Lemma 2.6 consumes.

`Mub6.table1_consistent` checks §7.5's arithmetic. If the paper's counts are internally
inconsistent, that theorem would not compile — so attack the *interpretation* of the counts, not
their sums.

## Where a statement is most likely mis-transcribed (attack in this order)

1. **Lemma 5.1 — retracted attack; do not repeat it.** I earlier claimed the third inequality
   needs a hypothesis absent from Definition 4.1. It does not: (4.4) is the two-sided Gram bound
   `‖T*T − I‖ ≤ ort`, so both `‖T‖² ≤ 1 + o_P` and `T*T ⪰ (1 − o_P) I` hold, and expanding
   `‖Ax‖²` gives the inequality for every `x`, horizontal or not. Anything that attacks 5.1 must
   attack the *use* of `o_P` elsewhere (e.g. whether every Root really certifies (4.4) with the
   same constant that appears in `n_P`), not the lemma. A useful question for the authors: in
   §5.2 `β = √((1+o_P)(1+o_P)(1+o_Q))` uses `o_P` twice for bounds of different type — one is the
   Gram defect, the other a norm bound; check that no `o_P` is reused for a quantity that is not
   the Gram defect.
2. **Quantifier order in Prop. 2.10.** `∀H ∃(equivalence, centre)` vs `∃equivalence ∀H`. Also the
   two radii: `0.032` (exact, Nine-dimensional bin midpoint bound `3/224`) and `0.0320001` (after
   binary conversion). Replacing the first by the second is a *weakening* that silently drops the
   `10⁻¹⁴` conversion budget; check the paper does not do it in the proof of Theorem 7.1.
3. **Prop. 5.7's right-hand side.** The failed-parent term must be `S(P,R)` at the **input** radius,
   not `S(P,τ)`. If the paper's Cor. 5.8 then assumes "no bad parents" the distinction is invisible
   — which is exactly why it should be attacked before the corollary.
4. **Prop. 4.16's carrier.** "Every exact second-basis Hadamard matrix required for the four-basis
   problem" = extendible ones. Quantifying over all exact `H` is stronger, and since the A-stage
   exclusions are per-seed, a reader may not notice the difference.
5. **Prop. 6.9's outcome algebra.** "Negative" has exactly two producers (empty completed bin layer;
   completed negative graph search). Unresolved outcomes are not negative. Any Bool-valued
   formalisation (or any paper sentence of the form "otherwise, exclusion") is a soundness bug.
6. **Lemma 3.1's endpoint.** `|S| < 4` is used for `(M*M)^{-1}`; the `K` existence clause does not
   need it. Check the paper never uses `K` at `|S| = 4`, where `(3.4)` is undefined but `K` exists.
7. **Lemma 4.11 with singular `G`.** The containment `{G^{1/2}w : ‖w‖ ≤ 1}` is an *existential over
   `w`*; for singular `G` it is **not** equivalent to the quadratic-form inequality
   `x*G^†x ≤ 1` unless one restricts to `ran G`. The paper's support-function proof is right; a
   red-team re-derivation that uses `G^{-1}` is wrong.
8. **Lemma 6.5's carrier.** The two vectors are phase classes modulo global phase; the ball is a
   ball in phase space. Re-derive the constant: `‖z‖ ≤ 2s < 0.2` gives
   `|Σ_j e(z_j)| ≥ 6 - 2π√6·0.2 = 6 - 0.4π√6 ≈ 2.921 > √6 ≈ 2.449`, hence
   `|⟨p,q⟩| = |Σ|/6 > 1/√6·(2.921/2.449)` — bounded away from both `0` and `1/√6`. Check the
   printed display, whose OCR is garbled.
9. **Lemma 2.3's "is the orthogonal projection".** A linear map is an orthogonal projection iff it
   is idempotent, self-adjoint, and has the stated range. Any two of the three are not enough; a
   red-team complaint that the paper only proves `‖Πz‖ ≤ ‖z‖` is fair unless all three are shown.

## What my artifacts do NOT certify (do not treat them as evidence)

* No analytic estimate of §3–§6 is formalised here (owned by d2/d1); the `PENDING` rows in
  `reports/status.md` are statements of *intent*, not of fact.
* `Mub6/Hypotheses.lean` does not verify any code claim. `CodeClaims` has 18 `Prop` fields on
  purpose: typing them concretely would invent a specification of programs not in the packet, which
  the project forbids. If a `CodeClaims` field is *false* as described, that is a defect in the
  paper's prose, and it is exactly the kind of thing T9 should report.
* `TerminalConditions` does not say that the run happened. It is the shape of the claim.

## The checklist I would use

For each of the 17 in-scope statements, ask the four questions in `reports/statements.md`:
(1) is the quantifier order right, (2) is the carrier right (matrix vs basis vs phase class vs
solution set), (3) are the endpoints right (closed ball, strict `<`, `≤ r`, `|S| < 4`), (4) is the
conclusion the strong one (necessary vs sufficient; squared norm vs norm; iff vs implication).
Every one of the nine items above is a violation of exactly one of those four.
