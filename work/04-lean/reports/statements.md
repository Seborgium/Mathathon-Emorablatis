# reports/statements.md — source-fidelity table

One row per Lean declaration that transcribes a paper claim, with **binder-by-binder** agreement:
quantifier order, carriers, shared witnesses, endpoints, and the strength of the conclusion.
Proof status is **not** here — it lives in `reports/status.md`, and the two are deliberately not
merged into one judgement.  (A statement can be a faithful transcription and unproved; it can also
be proved and unfaithful.  Those are different failures.)

## Conventions used in this table

* `M` = matches the paper exactly at the level of binders and conclusion.
* `M+` = same claim, hypotheses *stronger* than the paper's (so the Lean theorem is strictly weaker
  as a theorem — recorded because it is a weakening).
* `M-` = same claim, conclusion *weaker* than the paper's, or part of the paper's conclusion not
  packaged (recorded, never silently dropped).
* `M*` = the paper's words admit two readings and Lean forces one; the reading chosen is stated.
* `code` = the paper claim depends on the authors' code (status `S`/`C` in `results/proof-claims.md`).
  Such dependence is turned into an explicit binder or is absent.  §1–2 has no `code` dependence;
  Lemma 1.2 is pure mathematics, and Lemmas 2.2/2.3/2.5 are pure algebra.

Merge protocol: each member appends a section headed by its claim list; do not renumber another
member's rows.  Rows below are `B` (carriers), `12` (Lemma 1.2), `22` (Lemma 2.2), `23` (Lemma 2.3),
`25` (Lemma 2.5).

Owner of this section: m2 (direction `d3`, scaffold + §1–2).

---

## B. Carrier decisions (`Mub6/Basic.lean`)

These are not paper claims; they are the vocabulary every later row is judged against, so they get
rows of their own.

| id | Lean name | paper locator | paper's words | deliberate change | code |
|---|---|---|---|---|---|
| B1 | `Mat n := Matrix (Fin n) (Fin n) ℂ` | §2 preamble "Matrix indices run from 0 to 5" | matrices indexed `0..5` | none: `Fin 6` is `0..5` | — |
| B2 | `Vec n := Fin n → ℂ` | §2 preamble | vectors in `ℂ⁶` | none | — |
| B3 | `ip u v := ∑ j, u j * conj (v j)` | §2 preamble `⟨u,v⟩ = ∑_j u_j \overline{v_j}` | conjugate-linear in the **second** slot | none (the convention is fixed explicitly, not inherited) | — |
| B4 | `IsPhaseHadamard H := (∀ i j, normSq (H i j) = 1) ∧ H * Hᴴ = 6 • 1` | **Def 2.1** | "a complex Hadamard matrix here if every entry has modulus one and `HH* = 6I`" | **M** on the paper's one-sided form. Mathlib's `Matrix.IsHadamard` is the two-sided form (`H Hᴴ = n•1` **and** `Hᴴ H = n•1`); for square `H` over `ℂ` the two agree (a right inverse is a left inverse), and Mathlib's `IsHadamard.of_mul_conjTranspose` discharges the bridge — the bridge is **not** invoked anywhere below, so nothing depends on it. | no |
| B5 | `UnbiasedH H K := ∀ i j, normSq ((Hᴴ * K) i j) = 6` | §1 `|⟨b,c⟩|² = 1/d` | unbiased bases | **M**: `H = √6 U`, `K = √6 V` with `U,V` unitary, so `(HᴴK)_{ij} = 6 (UᴴV)_{ij}` and `normSq = 36·(1/6) = 6`; see the calculation note below | no |
| B6 | `IsBasisMat U := U * Uᴴ = 1` | §1 "orthonormal bases" | a matrix whose columns are orthonormal | none | — |
| B7 | `UnbiasedBases U V := ∀ i j, normSq ((Uᴴ*V) i j) = 1 / n` | §1 `|⟨b,c⟩|² = 1/d` | — | **M** in the unitary normalisation (`d = n`), used only for `n = 6` | no |
| B8 | `Extendible H := ∃ K L, IsPhaseHadamard K ∧ IsPhaseHadamard L ∧ UnbiasedH H K ∧ UnbiasedH H L ∧ UnbiasedH K L` | **Def 2.1** | "extendible if the standard basis and the columns of `H/√6` belong to a family of four mutually unbiased orthonormal bases" | **M\***: the family is `{standard basis, H/√6, K/√6, L/√6}`. Unbiasedness of each of the other three to the **standard basis** is not a conjunct: it is implied by unit modulus (`|⟨e_i, K_j/√6⟩| = |K_ij|/√6 = 1/√6`). The paper's four-basis family is thus exactly `{I, H/√6, K/√6, L/√6}` with the three pairwise conditions stated. | no |
| B9 | `Dephase P i j := P i j - P i 0 - P 0 j + P 0 0` | **(2.2)** | "unwrapped dephasing `D₀(P)_{ij} = P_{ij} - P_{i0} - P_{0j} + P_{00}`" | none | no |
| B10 | `Pi z i j := z i j - (1/6)∑_b z_ib - (1/6)∑_a z_aj + (1/36)∑_{a,b} z_ab` | **(2.1)** | double centring | none; `6` is the paper's dimension and is not generalised | no |
| B11 | `Horizontal z := (∀ i, ∑ j, z i j = 0) ∧ (∀ j, ∑ i, z i j = 0)` | §2.1 | "the horizontal subspace of matrices with every row sum and every column sum zero" | none | no |

Calculation note for B5/B7 (the index convention matters and is easy to get wrong): with `Uᴴ` the
conjugate transpose, `(Uᴴ V)_{ij} = ∑_k conj(U_{ki}) V_{kj} = ∑_k (v_j)_k conj((u_i)_k) = ⟨v_j, u_i⟩`
in the paper's convention, so `|(UᴴV)_{ij}|²` is `|⟨u_i, v_j⟩|²` — the modulus of the inner product
between basis vector `i` of the first basis and vector `j` of the second.  This is why the
normalisation `1/n` in B7 and `6` in B5 is correct and not `n` versus `1/n` confusion.

---

## 12. Lemma 1.2 — three mutually unbiased bases in `ℂ⁶` (`Mub6/ThreeMUB.lean`)

Paper: **Lemma 1.2.** "There exist three pairwise mutually unbiased orthonormal bases in `ℂ⁶`."
Status in `results/proof-claims.md`: **M**.

| id | Lean name | paper locator | paper's statement (quoted) | deliberate change | code |
|---|---|---|---|---|---|
| 12.1 | `ω`, `sqrt3_sq`, `omega_sq`, `omega_add`, `omega_cube`, `omega_pow_four/six/eight`, `normSq_omega` | §1.3 proof | "`ω = e^{2πi/3}` … The identity `1 + ω + ω² = 0` shows that `F` is unitary" | **M**: `ω` is defined in closed form `⟨-1/2, √3/2⟩` rather than as `exp(2πi/3)` (no trigonometry in the proofs). Any claim about `e^{2πi/3}` is replaced by the two algebraic facts the paper actually uses, `ω² + ω + 1 = 0` and `ω³ = 1`. | no |
| 12.2 | `gauss_zero`, `gauss_one`, `gauss_two` | §1.3 proof, "For their cross product, `(F*DF)_{jk} = (1/3)∑_x ω^{x²+(k-j)x}`" | "the sum on the right is `1+2ω` for `t=0` and `2+ω²` for `t=1,2`" | **M**: `gauss t = ∑_{x<3} ω^{x²+tx}` for `t = 0,1,2` — exactly the three values of `t = k-j mod 3`, stated separately rather than with a `mod`-indexed `t`. The paper's `t` is read mod 3; the reduction is `omega_pow_*`. | no |
| 12.3 | `normSq_one_add_two_omega`, `normSq_two_add_omega_sq` | §1.3 proof | "Each has squared modulus `3`" | **M**: `|1+2ω|² = 3` and `|2+ω²|² = 3`, i.e. `1/(1/3)` — the entries of `F*DF` have squared modulus `1/3`. | no |
| 12.4 | `FDF_entry` | §1.3 | "`(F*DF)_{jk} = (1/3)∑_x ω^{x²+(k-j)x}`" | **M\***: stated as `(Fᴴ * D * F) j k = (1/3) * gauss ((k - j : Fin 3) : ℕ)`. Reading `k-j` in `Fin 3` is the paper's "`t = k-j` read modulo 3"; the passage between the two needs `ω³ = 1` for the terms with negative exponent, which is available. Assumption checked: `D = diag(1,ω,ω) = diag(ω^{x²})` because `2² ≡ 1 (mod 3)`, which is *why* the paper's exponent has the `x²` term. | no |
| 12.5 | `three_mub_exists : ∃ H K, IsPhaseHadamard H ∧ IsPhaseHadamard K ∧ UnbiasedH H K` | Lemma 1.2 | "There exist three pairwise mutually unbiased orthonormal bases in `ℂ⁶`" | **M\***: the conclusion is *three* MUBs but the statement exhibits *two* Hadamards plus the implicit standard basis (see B8). This is exactly the paper's own reduction: `U₀ = I₆` and the other two are `H/√6`, `K/√6`. Not packaged: the explicit pair `(H,K) = (A₁⊗B₁, A₂⊗B₂)` is not named in the statement — existence only, as in the paper. | no |
| 12.6 | (prose in file) the 2×2 cross product | §1.3 | "`A₁*A₂ = ½!![[1+i,1-i],[1-i,1+i]]` … squared modulus `1/2`" | **M-**: not restated as a Lean theorem in this window (it is discharged inside `three_mub_exists`); the closed form is recorded in the file as a comment so the red team can check it by hand. | no |

Binder-by-binder, 12.5:

| aspect | paper | Lean (`three_mub_exists`) | verdict |
|---|---|---|---|
| quantifiers | existential, no parameters | `∃ H K : Mat 6, …` | same |
| carrier | `ℂ⁶` bases / `6×6` matrices | `Mat 6 = Matrix (Fin 6) (Fin 6) ℂ` | same |
| basis normalisation | orthonormal bases (unit columns) | `H` is Definition 2.1, i.e. the columns of `H/√6` are the basis | same (via B8) |
| shared witnesses | one family of three bases | one pair `H, K` plus the fixed standard basis | same |
| endpoints | "there exist three" | existence only, no uniqueness, no count extremality | same |
| conclusion strength | `N(6) ≥ 3` | `N(6) ≥ 3` (no statement of `N(6)`) | same |

---

## 22. Lemma 2.2 — equivalences (`Mub6/Hadamard.lean`)

Paper: **Lemma 2.2.** "Extendibility is invariant under row or column permutations, multiplication
of rows or columns by unit scalars, complex conjugation, and transposition."
Status in `results/proof-claims.md`: **M**.

| id | Lean name | paper locator | paper's statement (quoted) | deliberate change | code |
|---|---|---|---|---|---|
| 22.1 | `permRows σ` / `extendible_permRows` | Lemma 2.2 (row permutations) | "invariant under row … permutations" | **M-**: the one-directional implication `Extendible H → Extendible (permRows σ H)` is stated for an arbitrary `σ : Equiv.Perm (Fin 6)`. The converse follows by re-applying the same theorem with `σ⁻¹`; that packaging is not formalised. | no |
| 22.2 | `permCols τ` / `extendible_permCols` | Lemma 2.2 (column permutations) | "… or column permutations" | as 22.1 | no |
| 22.3 | `rephaseRows r` / `extendible_rephaseRows` | Lemma 2.2 (row rephasings) | "multiplication of rows … by unit scalars" | **M**: "unit scalars" is the hypothesis `IsUnitScalarVec r := ∀ i, normSq (r i) = 1`, an explicit binder. One direction only, as 22.1. | no |
| 22.4 | `rephaseCols c` / `extendible_rephaseCols` | Lemma 2.2 (column rephasings) | "… or columns by unit scalars" | as 22.3 | no |
| 22.5 | `conjMat H / extendible_conjMat` | Lemma 2.2 (complex conjugation) | "complex conjugation" | **M**: `conjMat H = fun i j => star (H i j)` (entrywise conjugation, no transpose). One direction; `conjMat` is an involution. | no |
| 22.6 | `transposed H / extendible_transposed` | Lemma 2.2 (transposition) | "and transposition" | **M**: `transposed H = Hᵀ`, no conjugation. This is the clause the paper calls non-obvious; the paper's proof moves to the pair `(U*, I)` and conjugates coordinates, and *nothing in the Lean statement* encodes that route — the statement is the invariance alone, as it should be. | no |
| 22.7 | `extendible_iff_all` | Lemma 2.2, "invariant" (both directions) | invariance = "if and only if" | **M-**: packages the composition `rephaseRows ∘ rephaseCols ∘ permCols ∘ permRows` and the two involutions as `↔`, but this is the packaged *claim* of two-sidedness, not the derivation of it from 22.1–22.6 (that derivation needs the inverse-operation lemmas, not formalised). Flagged for the red team: 22.7 must not be cited as if it were proved from 22.1–22.6. | no |

Binder-by-binder, 22.1–22.6:

| aspect | paper | Lean | verdict |
|---|---|---|---|
| quantifiers | "extendibility is invariant under [operation]" | operation is a parameter (`σ`, `τ`, `r`, `c`), `H` is implicit, hypothesis `Extendible H` is explicit | same (one direction) |
| row permutation | reorder the 6 rows | `σ : Equiv.Perm (Fin 6)`, `(permRows σ H) i j = H (σ i) j` | same (bijective, so no loss) |
| unit scalar | unit complex number | `Complex.normSq (r i) = 1`, one per row | same |
| conjugation | entrywise | entrywise `star`, no transpose | same |
| transposition | `Hᵀ` | `Hᵀ` | same |
| conclusion | extendibility preserved | `Extendible (op H)` — full extendibility, not merely "the pair `(I,H)` stays unbiased" | same |
| converse | asserted by "invariant" | not derived | **M-** |

---

## 23. Lemma 2.3 — horizontal phase representatives (`Mub6/Basic.lean` + `Mub6/Hadamard.lean`)

Paper: **Lemma 2.3.** "The map `Π` is the orthogonal projection onto the horizontal subspace. In
particular, `‖Πz‖_F ≤ ‖z‖_F`. If two phase representatives have difference `z`, the second is
equivalent under row and column rephasings to the first plus `Πz`. This statement remains valid
after arbitrary entrywise integer changes of phase representatives."
Status in `results/proof-claims.md`: **M**.

| id | Lean name | paper locator | paper's statement (quoted) | deliberate change | code |
|---|---|---|---|---|---|
| 23.1 | `Pi_rowSum`, `Pi_colSum`, `Pi_horizontal` | Lemma 2.3 (range) | "`Π` is the orthogonal projection onto the horizontal subspace" | **M**: the range half — `Π z` has zero row and column sums. | no |
| 23.2 | `Pi_idem`, `Pi_fixes_horizontal`, `horizontal_iff_Pi_eq_self` | Lemma 2.3 | idempotent projection with range = horizontal subspace | **M**: `Π∘Π = Π` and `Horizontal z ↔ Π z = z`, so the range is *exactly* the horizontal subspace. | no |
| 23.3 | `sum_mul_rowcol_zero`, `sub_Pi_eq_rowcol` | Lemma 2.3 proof | "`z - Πz` is a sum of a matrix constant on each row and a matrix constant on each column. Every such sum is orthogonal to the horizontal subspace" | **M**: `∃ r c, z - Πz = fun i j => r i + c j`, and horizontality gives orthogonality of the real Frobenius inner product. Explicit witnesses: `r i = (1/6)∑_b z_ib - (1/36)∑_{a,b} z_ab`, `c j = (1/6)∑_a z_aj`. | no |
| 23.4 | `Pi_frobSqR_le` | Lemma 2.3 | "In particular, `‖Πz‖_F ≤ ‖z‖_F`" | **M**: stated for the *squared* Frobenius norm, `frobSqR (Π z) ≤ frobSqR z`, from `frobSqR z = frobSqR (Πz) + frobSqR (z - Πz)`. The norm inequality is the square-root of this; the sqared form is the sharper statement and avoids square roots. | no |
| 23.5 | `expMat_rowcol_add` | Lemma 2.3 | "the second is equivalent under row and column rephasings to the first plus `Πz`" | **M-**: the two halves are separate facts: `z - Πz = r + c` (23.3) and `e(P + (r_i+c_j)) = e(r_i) e(c_j) e(P)` (23.5). The single sentence "`e(P + Πz)` differs from `e(Q)` by row and column phases" is **not** packaged as one theorem. | no |
| 23.6 | `expMat_int_shift` | Lemma 2.3, last sentence | "This statement remains valid after arbitrary entrywise integer changes of phase representatives" | **M**: `expMat (fun i j => P i j + m i j) = expMat P` for arbitrary integer-valued `m`, proved from `e (t + k) = e t` (`e_add_int`). | no |
| 23.7 | (not stated) | Lemma 2.3, "orthogonal projection" | `Π` *is* the orthogonal projection | **M-**: the projection is characterised by (range = horizontal, `z - Πz ⊥` horizontal) plus idempotence, not by an equality with Mathlib's `Submodule.orthogonalProjectionOnto`. Mathlib has no `InnerProductSpace` instance on `Matrix` (see DEPGRAPH), so the identification would need `Matrix` ↔ `EuclideanSpace` plumbing; the characterisation is equivalent and is what the paper uses. | no |

---

## 25. Lemma 2.5 — stability of circular gaps (`Mub6/Seed.lean`)

Paper: **Lemma 2.5.** "If each point of one circular multiset is matched to a point of another at
circular distance at most `δ`, their gaps differ by at most `2δ`."  (Gap = **largest** circular gap,
§2.2.)  Status in `results/proof-claims.md`: **M**.

| id | Lean name | paper locator | paper's statement (quoted) | deliberate change | code |
|---|---|---|---|---|---|
| 25.1 | `gap_stability` | Lemma 2.5 | as quoted | **M** with explicit representation hypotheses: both lists are sorted (`Monotone`), start at `0`, stay `< 1`, and the matching is an arbitrary permutation `σ : Equiv.Perm (Fin 6)` with `circularDist (x i) (y (σ i)) ≤ δ`. The paper's "circular multiset" is represented by its sorted six-point representative `(0, x₁, …, x₅)`; the paper's Lemma 2.4 arrangement is exactly what supplies such a representative. | no |
| 25.2 | `seedGap_lipschitz` | Lemma 2.5 (special case) | same, with the identity matching | **M+**: the matching is fixed to `σ = id` (hypothesis `∀ i, |x i - y i| ≤ δ`). This is the form Lemma 2.6 consumes (the two lists are compared index by index after sorting). Strictly weaker than 25.1 as a theorem; recorded so nobody cites it as Lemma 2.5. | no |
| 25.3 | `circularDist` | §2.2 | circular distance on `ℝ/ℤ` | **M\***: defined as `min |s-t| (1-|s-t|)`, which is the distance on the circle **only for `s, t ∈ [0,1)`**; the total function agrees there (and 25.1 assumes `x i, y i ∈ [0,1)`). Stated as a restriction, not as `AddCircle`. | no |
| 25.4 | `seedGap` | §2.2 "The gap of a finite circular multiset is its largest circular gap" | — | **M**: `seedGap x = max over the six arcs` where the last arc wraps from `x 5` to `1`; the six arcs are `x 1 - x 0, …, x 5 - x 4, 1 - x 5`. This is the paper's gap for a dephased sorted seed list. For an unsorted `x` the definition is the same formula but is not the gap of the multiset — that is why 25.1 carries `Monotone`. | no |

---

## What this section does **not** claim

* Nothing about `N(6) ≥ 4`, the atlas interface, or Stages A/B/C: those are other members'
  sections.
* No claim that the paper's proof of Lemma 2.2 (the `(U*,I)` trick) has been checked in Lean —
  only that the resulting invariance is stated.
* No `code`-dependent statement appears in this section. §1–2 is code-free; the first `S`/`C`
  claims in the paper are Prop. 2.10 onwards.

---

# Section m3 (direction `d1`): §5–6 statements and the group-(B) assembly interface

Owner: m3.  Files: `Mub6/Interface.lean`, `Mub6/Exclude.lean`, `Mub6/Assembly.lean`.
Row ids `I*` (interface), `C*` (§6 / Stage C), `A*` (assembly).  Proof status is in
`reports/status-m3.md`; nothing here should be read as a claim of proof.

## I. The abstract cover interface (`Mub6/Interface.lean`)

Not paper claims; they are the vocabulary that makes 2.10/3.11/4.16/5.7/6.9 one theorem each.

| id | Lean name | paper locator | paper's words | deliberate change | code |
|---|---|---|---|---|---|
| I1 | `Cover.Covered mem 𝔅 S` | (5.1), (5.26) | "`S(P,R) = {[e(P+δ)] : δ ∈ V, ‖δ‖ ≤ R, F(P+δ)=0}`" | the ball is an abstract `b : Ball` with its point-set `mem b`; no geometry | — |
| I2 | `Cover.Cert mem 𝔅 T S` | 3.7 (cell recursion), 5.3 (5.23), 6.3 (bin layers) | "the children's closed intervals cover the parent's" | the four constructors are *exactly* the four verdicts a region can receive: empty, excluded by a necessary test (`excl`, hypothesis `Disjoint T S`), contained in a ball (`ball`), decomposed (`union`). Finiteness of `union` is not required: only the covering inclusion is used, and every instantiation is finite | — |
| I3 | `Cover.Cert.covered` | the induction asserted inside 2.10, 3.11, 5.7, 6.9 | "The grid covers every possible tangent vector by (5.20)…" | **M**: conclusion is `T ∩ S ⊆ ⋃𝔅`, i.e. only target points are claimed to be covered — the paper's regions include non-solutions and never claims those | — |
| I4 | `Cover.accumulate_covered` | 4.16, 5.7 | "The induction invariant is that every previously successful parent sphere is covered by the current atlas" | **M** on the invariant. The hypothesis `hstep` is stated at the prefix `l ++ [p]` (certificate at the moment the parent *completes*), which is precisely the paper's "a blocker is only ever an already completed parent"; the final atlas is reached by prefix monotonicity `hatlas_mono` | — |
| I5 | `Cover.Cov emb S S'` | 7.4 "places an equivalent exact solution in a record of …" | — | `emb` is unanalysed: only reflexivity/transitivity/`ext`-invariance are ever used (Lemma 4.7) | — |
| I6 | `Cover.Cov.trans`, `Cover.Cov.excludes` | 7.4 | "Each coverage implication used here is justified by its geometric lemma" | **M**: the composition and the backwards transport of non-extendibility | — |

## C. §5.1 and §6 (`Mub6/Exclude.lean`)

| id | Lean name | paper locator | paper's statement (quoted) | deliberate change | code |
|---|---|---|---|---|---|
| C0 | `StageC.e`, `ip`, `Ortho`, `Unbiased` | §6.2 (6.5) | "the necessary unbiasedness equations are `|S'_i| = 1`"; `A = e(P)` | carrier: a *phase point* `u : Fin 6 → ℝ`; `ip u u' = ∑_j e(u_j - u'_j)`. `Ortho` := `ip = 0`, `Unbiased` := `‖ip‖ = √6`. Unscaled inner product: `⟨e(u),e(u')⟩ = ip/6`, so `|⟨·,·⟩|² = 1/6` iff `‖ip‖² = 6` | — |
| C1 | `StageC.sq`, `InBall` | (6.14) | "`Bvec(v,s) = {λe(v+x)/√6 : |λ|=1, x ∈ ℝ⁶, ∑x_j = 0, ‖x‖ ≤ s}`" | **M** with `‖x‖ ≤ s` written as `sq x ≤ s²` (ℓ² on `ℝ⁶`, no `Pi` sup-norm), plus an explicit global phase `θ` and integer lift `m ∈ ℤ⁶`. Both are the paper's own identifications ("up to global phase", phases lifted to `[0,1]`) | — |
| C2 | `StageC.ip_norm_gt` | Lemma 6.5 proof | "`|∑_j e(z_j)| ≥ 6 - ∑_j|e(z_j)-1| ≥ 6 - 2π√6‖z‖ > 6 - π√6 > 20/7 > √6`" | hypothesis `sq z ≤ (1/5)²` is exactly `‖z‖ ≤ 2s < .2`. **Numeric deviation**: the paper closes with `π < 22/7`; Mathlib at this pin has `Real.pi_lt_d2` (`π < 3.15`) and no `π < 22/7`, giving `6 - 2·3.15·(5/2)/5 = 6 - 63/20 = 57/20 > √6` instead of `20/7 > √6`. Same conclusion, slightly less slack; the deviation is in one intermediate constant only | no |
| C3 | `StageC.distinct_labels` | **Lemma 6.5** | "Two vectors in the same ball `Bvec(v,s)` with `s < .1` are neither orthogonal nor mutually unbiased." | **M** modulo: (i) `0 ≤ s` added (needed: `s < 1/10` alone does not bound `s²`; all paper balls have `s ≥ 0`); (ii) the numeric step as C2. The "hence the twelve vectors occupy twelve distinct balls" half is not in this row; it is proved where used (C9) | no |
| C4 | `StageC.bin_displacement` | **Lemma 6.1** | "`∑x_j = 0`, `‖x‖ ≤ X_M := √(29/6)a`, `‖x‖₁ ≤ L_M := 5a`, `‖x‖_∞ ≤ I_M := 3a/2`" | `‖x‖ ≤ X_M` restated as `sq x ≤ (29/6)a²`; `a = 1/(2M)`; `|d_j| ≤ a` is imposed also at `j = 0` where `d_0 = 0` anyway (harmless, noted). Conclusion unchanged | no |
| C5 | `StageC.cross_le`, `sq_add_le` | not in the paper | — | infrastructure: Cauchy–Schwarz on `ℝ⁶` and the ℓ² triangle inequality, used to pass from `‖h‖ + X` to `‖h + x‖` in C6 | — |
| C6 | `StageC.certified_clustering` | **Lemma 6.4** | "If the assigned radius is at least `‖h‖ + X_M`, then `Bvec(v,s)` covers the whole bin up to global phase." | **M**: `hmean`/`hdef` encode `h = u - v - m - (1/6)Σ(u_j-v_j-m_j)1`; `hrad` is `(‖h‖+X)² ≤ s²`; conclusion `InBall v s (u+x)` for every bin displacement `x`. `X` abstract (linked to `X_M` by C4) | yes: the two binders `hdef`, `hrad` are what the final radius recomputation of `cluster` guarantees |
| C7 | `StageC.Graph`, `StageC.Config` | (6.24) | "`|A| = |B| = 6, A,B are O-cliques, A×B ⊆ E(U)`" | **M**. Note we *first* mis-stated this as "`B` is a `U`-clique" and corrected it against (6.24) and the surrounding text ("within either group the vectors are pairwise orthogonal"): `B` is an **O**-clique. This is exactly the class of slip the fidelity pass is for | — |
| C8 | `StageC.prop_6_9` | **Prop. 6.9** | "If Stage C returns a negative result for the Record, then no exact Hadamard `e(P+δ)` in its closed horizontal radius-r ball can be extended, together with the coordinate basis, by two further mutually unbiased orthonormal bases." | **M\***: (i) the record's `δ` does not appear — the theorem is stated for a fixed Hadamard, with the twelve phase points given outright; (ii) the ball cover `hlab` is assumed for *every* phase point, stronger than "every vector unbiased to both bases", so the theorem excludes a larger class of configurations than the paper's — harmless downstream, recorded; (iii) only the **graph-negative** certificate path is formalised; the paper's other negative path ("a completed empty bin layer") is the trivial case (no admissible vector at all) and is not packaged; (iv) Lemma 6.8 (`graph::exist`) is a binder `hgraph : ¬ Config G` | yes: `hgraph` (6.8), `hO`/`hU` (6.6, 6.7 necessary tests) |
| C9 | `StageC.prop_6_9` (proof) | 6.9 proof + 6.5 last sentence | "Two additional bases would give twelve distinct ball labels" | **M**: label injectivity within a basis and disjointness across the two bases, then the configuration; the two facts are `distinct_labels` applied to the shared ball, so "distinct labels" is not assumed | no |

## A. The assembly (`Mub6/Assembly.lean`)

| id | Lean name | paper locator | paper's statement (quoted) | deliberate change | code |
|---|---|---|---|---|---|
| A0 | `Assembly.Rec` | Def 4.14 | "A Record is a Root plus a radius" | centre/radius abstract; `S(P,R)` is a parameter `sol` | — |
| A1 | `Assembly.seed_radius` | Prop 2.10 proof | "`√9/(2·112) = 3/224 < 0.032`" | **M**, proved | no |
| A2 | `Assembly.prop_2_10` | **Prop. 2.10** | "the written rational midpoints … cover the nine seed coordinates of every exact H up to Lemma 2.2, by closed balls of radius 0.032; after conversion to binary phases, 0.0320001 suffices" | **M-** on two counts: (i) the binary-phase conversion term (`0.0320001`) is not carried — we conclude `0.032`; (ii) "up to Lemma 2.2" is not composed: `seeds` is the set of seed coordinates of one representative, and the equivalence would have to be folded into the hypothesis, which we did not state. The enumeration/completion premise (**S + C**) is the binder `hcert` | yes: `hcert` |
| A3 | `Assembly.prop_3_11` | **Prop. 3.11** | "If every terminal cell … is either excluded by a certified necessary test or covered by a certified phase ball, then those balls cover all feasible completions of the seed, up to the phase-ball equivalences." | **M-** : "up to the phase-ball equivalences" is not composed (the conclusion is the raw inclusion). The terminating-with-no-unresolved-cells premise (**S + C**) is `hcert` | yes: `hcert` |
| A4 | `Assembly.prop_4_16` | **Prop. 4.16** | "If the seed cover is valid and the completion search processes all seeds with no failed and no unresolved seed, the A-stage Records cover every exact second-basis Hadamard matrix up to extendibility-preserving equivalence." | **M** on the shape; the equivalence is folded into `hstep` (each seed's solutions "placed in the atlas" — the coarse-record conversion is not formalised here) and the seed cover is `hcover` (A2's conclusion). "No failed seed" = `failed := fun _ => False` | yes: `hstep`, `hfinal` |
| A5 | `Assembly.prop_5_7` | **Prop. 5.7** | "`⋃_{input} S(P,R) ⊆ ⋃_{atlas} S(Q,r) ∪ ⋃_{bad} S(P,R)`" (5.26) | **M** verbatim, with two absorptions recorded: (i) "with valid Root certificates" and "under the arithmetic assumptions and error bounds of Section A" are *not* binders of the assembly theorem — they are needed to justify `hstep`, so they are absorbed there; (ii) `S(P,R)` is abstract (no horizontal/`F` structure) | yes: `hstep` (per-parent certificate), `hfinal` (atlas written out) |
| A6 | `Assembly.cor_5_8` | **Cor. 5.8** | "…no bad parents and every emitted batch is included. Then the input solution sets are covered … by the emitted records with their stored target radius τ." | **M-** : the radius change `S(Q_i,r_i) ⊆ S(Q_i,τ)` (5.27) is not formalised (radii are abstract), and the batching/insertion-order bookkeeping is in `hfinal` | yes |
| A7 | `Assembly.prop_6_9` | **Prop. 6.9** | as C8 | the "no two further bases" form: `¬ ∃ u0 u1, (ortho within each) ∧ (unbiased across)`; equals `¬ ext` at the record, which is what 7.1 consumes | yes: `hgraph` |
| A8 | `Assembly.theorem_7_1` | **Thm. 7.1** | "Use the seven specified source files and the arithmetic conditions of Appendix A. Suppose the invocations in §7.2 meet all of its terminal conditions, with the record provenance and batch checks stated there. Then four mutually unbiased orthonormal bases in ℂ⁶ do not exist." | **M\***: the seven sources and Appendix A are not binders — they are absorbed into the six links, each of which is the corresponding proposition's **S + C** content; the terminal conditions of §7.2 appear as the four bookkeeping links (`hinitC`, `hfallback`, `hfinal`) plus `hCneg`. Conclusion is stated as "no extendible point of `H`", i.e. one step short of "no four MUBs": that step is A9 | yes: all links |
| A9 | `Assembly.theorem_1_1` | Thm. 1.1 | "No four pairwise MUBs exist in ℂ⁶; hence N(6) = 3 with Lemma 1.2." | **M-**: the passage "four MUBs ⟹ an extendible point of `H`" (Lemma 2.2 normalisation + Lemma 1.2 for the converse) is the hypothesis `hfour`; Lemma 1.2's existence half is m2's `ThreeMUB` | — |

## Row-by-row notes on quantifier order and shared witnesses

* **2.10.** Paper: `∀ exact H, ∃ ball`. Lean `A2`: `∀ x ∈ seeds, ∃ b ∈ 𝔅` — same order. The witness `b` may depend on `x`; the paper's cover is also non-uniform in `H`. ✓
* **5.7.** Paper's inclusion is a `∀ x, (∃ parent, x ∈ S(P,R)) → (∃ child …) ∨ (∃ bad …)`. Lean `A5` has exactly this quantifier order, including that the *disjunction* is decided per point. ✓
* **7.1.** Paper chains six implications and ends with "every final record has a negative C result, contradicting extendibility". Lean `A8` composes with `Cov.trans` (associativity fixed explicitly by the nesting) and finishes with `Cov.excludes`; the *shared witness* of the chain is the sequence of equivalent points, which is existentially quantified at each link — the paper's "that very record" correspondence is what makes the chain follow one solution, and in Lean this is exactly `Cov.trans`'s composition of witnesses. ✓
* **6.9.** Paper: "no exact Hadamard in the ball can be extended". Lean `C8` quantifies over the twelve vectors with the ort/unbiased relations, concluding `False`; the `δ`-uniformity is in `hlab`. Recorded.

## Findings from this pass (things a reader of the paper should be told)

1. **`Config` mis-stated at first pass.** (6.24) requires `B` to be an **O**-clique, not a `U`-clique; the prose in §6 ("within either group the vectors are pairwise orthogonal; across the groups every pair is unbiased") is unambiguous, but the displayed condition `A, B are O-cliques, A × B ⊆ E(U)` is easy to mistranscribe as "A orthogonal, B unbiased" because the *tests* split that way. Corrected in C7.
2. **6.5's numeric step.** `π < 22/7` is not in Mathlib; `π < 3.15` suffices and leaves `57/20 > √6` (slack `≈ 0.10` instead of `≈ 0.41`). The paper's own margin is thin here: `6 - 2π√6·(1/5) ≈ 2.92` vs `√6 ≈ 2.449`, so any weaker bound on `π` below `≈ 3.2` still works — no fragility.
3. **§6's "distinct labels" is used twice.** Once inside the graph construction (labels injective *within* each basis) and once as the argument that the two bases occupy *disjoint* label sets. The paper states it once; both uses are needed and both are proved (C9).
4. **The empty-bin negative path is not a graph argument.** Proposition 6.9's proof says "if the retained set becomes empty, no such vector exists" — that path needs only "a vector unbiased to both bases lies in some retained bin", i.e. the single-vector tests, and is independent of 6.5–6.8. Worth separating in the paper; not formalised here (trivial).

---

# §3.1, §3.6, §4.11–4.12 rows — from m4 (direction `d2`)

Full binder-by-binder table: **`reports/statements-S3-S4.md`** (159 lines, one row per
declaration, with the paper's sentence quoted and every change classified). Summary of the rows and
of the *deliberate* changes, so that the merged table stays auditable:

| Lean name | locator | deliberate change | direction of the change |
|---|---|---|---|
| `frameMat_conjTranspose_mul` | L3.1 | `!![4,S;S̄,4]` written as a reducible `Matrix.of` (`gramMat`) | presentational only; orientation (S at (0,1)) checked |
| `frameMat_charpoly`, `frameMat_sq_singular_pair` | L3.1 "squared singular values 4 ± |S|" | rendered as the **charpoly** of `M*M` | same content, more precise (multiplicity); the "singular values = √eigenvalues" bridge is left to the pin's definition |
| `frameMat_mul_gramInv` | L3.1 (3.4) | two-step: `gramInv` is a right inverse, hence `(M*M)^{-1}` | none |
| `kerFrame_exists` | L3.1 sentence 3 | existence + both inclusions of `ran K = ker M*` | construction (Gram–Schmidt choice) **not** formalised |
| `SeedFrames` | L3.1 + (3.5) | the existential becomes **data** (fields = the lemma's conclusions) | makes the numerical frame *choice* a parameter |
| `frame_projection_identities` | (3.6) | none | — |
| `SeedSingularBounds` | `m_B = σ_min(B₀)`, `m_C` | `mB` is **any** certified lower bound, not the sharp `σ_min` | weakening of the constant (all §3 uses need only `‖G_B‖ ≤ 1/m_B`) |
| `norm_exclusion`, `norm_exclusion_z` | L3.8 (3.26) | arbitrary finite index types instead of `Fin 4 × Fin 4`; `D′ = D + Z` materialised in the hypothesis | harmless generalisation |
| `directional_exclusion` | L3.9 (3.29) | (i) `max(0,max(−y_D))` → an arbitrary `M ≥` that max; (ii) `y·J_all ≤ R_s‖g_s‖+h‖g_θ‖₁` is a **hypothesis** `hlinear`; (iii) flat equations (3.28) are **derived**, not assumed; (iv) `‖y_X‖` is the Euclidean norm, named `pairNorm` (Lean's default on `ℝ×ℝ` is the sup norm) | (i) **weakens the conclusion**, (ii) code-dependent layout → hypothesis, (iii) strengthens the hypothesis context, (iv) restores the paper's norm |
| `InEllipsoid` | L4.11 `{G^{1/2}w}` | support-function form `∀z, (z·x)² ≤ z*Gz` | **deliberate re-rendering** (pin has no matrix square root); equivalence is open bridge **B1** |
| `ellipsoid_containment` | L4.11 | `G ⪰ …` pointwise; extra `0 ≤ r`, `0 ≤ q` | pointwise form is what the proof uses; the extra binders exclude only vacuous cases |
| `offset_ellipsoid_bound` | L4.12 (4.34) | `G^{1/2}` → `R` with `R*R = G`; `(γI−G)^{-1}U` → `p` with `(γI−G)p = U`; `γ > λ_max` → `(γI−G) ⪰ 0`; commutation as a hypothesis | four replacements, all because the objects are absent from the pin; bridges **B2**, **B3** |
| `normSq_le_of_inEllipsoid` | L4.12 "‖U‖ + √λ_max(G)" | `λ_max(G)` → an explicit `Λ ≥ λ_max(G)` | the paper's own "any certified upper bound" convention |
| `offset_hull_bound` | L4.12 last sentence | convex combinations instead of "largest at the vertices" | equivalent restatement |

> **Rename (m3).** Rows `A0`-`A9` live in `Mub6/AssemblyCover.lean`, not `Mub6/Assembly.lean`:
> the scaffold owner claimed `Assembly.lean` as a stub while this section was being written, so the
> proved module was renamed rather than fight over the path. `Assembly.lean` now carries a pointer.
