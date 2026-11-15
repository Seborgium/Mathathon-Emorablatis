# Fidelity table — §3.1, §3.6, §4.11–4.12 (member m4, direction d2)

Scope of this file: the declarations in `Mub6/Frames.lean`, `Mub6/Exclusion.lean`,
`Mub6/Ellipsoid.lean`. Rows for §1–2 / §5–6 / assembly belong to the other members and are not
touched here. **Fidelity is judged separately from proof status** (`reports/status-S3-S4.md`).

Source of truth: `attachments/read-this-proof-condense-v9a3/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026.pdf`,
text at `.scratch/mub6.txt` (line numbers below refer to that file).

Columns: Lean name | paper locator | paper's statement (quoted) | deliberate change | code-dependence.

---

## A. Lemma 3.1 (fixed frames), mub6.txt:675–699 — file `Mub6/Frames.lean`

Paper: *"Lemma 3.1 (Fixed frames). Let p ∈ C4 have unit-modulus entries, let S = ∑_j p_j, and set
M = (1 p). The squared singular values of M are 4 ± |S|. If |S| < 4, then
M(M*M)^{-1} = 1/(16−|S|²) (4·1 − p S̄, 4p − 1 S). Under the same condition |S| < 4, there is an
orthonormal 4-by-2 matrix K with range ker M*. It may be constructed by completing 1/√2 and the
normalized residual of p by projected coordinate vectors with nonzero residuals."*

| Lean name | locator | change | code-dependence |
|---|---|---|---|
| `UnitModulus` (def) | "p ∈ C⁴ have unit-modulus entries" | none: `∀ j, ‖p j‖ = 1`, on the *entries* | none |
| `frameMat` (def) | "M = (1 p)" | none: `Matrix (Fin 4) (Fin 2) ℂ`, column 0 = **1**, column 1 = p. Note `1` is the all-ones *vector* | none |
| `seedSum` (def) | "S = ∑_j p_j" | none | none |
| `conj_mul_self`, `star_mul_self` | proof of Lemma 3.1 ("direct multiplication") | infrastructure only, not a claim | none |
| `frameMat_conjTranspose_mul` | proof: "M*M = [[4,S],[S̄,4]]" | **presentational**: the paper's `!![4,S;S̄,4]` is realised as `gramMat p`, a `Matrix.of` with `val`-tests on the two indices, so that Lean reduces entries. Definitionally the same matrix; **orientation checked**: S at (0,1), S̄ at (1,0) | none |
| `seedSum_mul_conj` | proof: eigenvalues of M*M | infrastructure: `S·S̄ = |S|²` (used by the charpoly row) | none |
| `frameMat_charpoly` | "The squared singular values of M are 4 ± |S|" | **precise rendering, not a weakening**: `charpoly (M*M) = (X − C(4+|S|))·(X − C(4−|S|))`, i.e. the eigenvalues of M*M are exactly `4±|S|` **with multiplicity**. The paper's phrase "squared singular values" is the multiset of eigenvalues of M*M; the bridge "singular values of M = square roots of eigenvalues of M*M" is the pin's definition (`Analysis/InnerProductSpace/SingularValues.lean`), not restated | none |
| `frameMat_sq_singular_pair` | same | companion form `X² − C 8·X + C(16−|S|²)`; kept because it is the shape in which `4 ± |S|` is read off | none |
| `gramInv` (def) | "(16−|S|²)^{-1}(−)" in (3.4) | the candidate right inverse `c • !![4, −S; −S̄, 4]`, `c = ((16−‖S‖²:ℝ):ℂ)⁻¹` | none |
| `framePseudoInv` (def) | LHS `M(M*M)^{-1}` of (3.4) | `M * gramInv p` — the identification `gramInv = (M*M)^{-1}` is the *content* of the next row, so it is not assumed by the definition | none |
| `framePseudoInvFormula` (def) | RHS of (3.4) | the paper prints the two columns as a **row** `(4·1 − p S̄, 4p − 1 S)`; here they are the two **columns** of a 4×2 matrix with the same entries. Presentational only; column 0 = `4 − p_i S̄`, column 1 = `4 p_i − S`, both scaled by `c` | none |
| `gram_mul_gramInv` | "If |S| < 4" | `(M*M)·gramInv p = 1` under `‖S‖ < 4`; the hypothesis is the paper's, and the nonvanishing `16−|S|² > 0` is derived from it | none |
| `frameMat_mul_gramInv` | (3.4) | `framePseudoInv p = framePseudoInvFormula p`, obtained from the previous row by `Matrix.inv_eq_right_inv`. **Two-step rendering recorded**: (i) `gramInv` is a right inverse of `M*M`; (ii) hence it is `(M*M)^{-1}`. No weakening | none |
| `kerFrame_exists` | "there is an orthonormal 4-by-2 matrix K with range ker M*" | `∃ K, KᴴK = 1 ∧ M*K = 0 ∧ ∀ x, M*x = 0 → ∃ t, K t = x`. **Both** inclusions of "range = kernel" are stated (the paper's phrase fixes the direction: `ran K = ker M*`, dim 2); the existence is under the paper's `‖S‖ < 4` | the paper's *construction* ("completing 1/√2 and the normalized residual of p by projected coordinate vectors") is **not formalised**; only the existence assertion is transcribed. The construction is what makes the frame canonical for a given Gram–Schmidt choice — a real assumption for reproducing the authors' numbers |
| `seedGB`, `seedGC` (defs) | (3.5): `G_B = B₀*(B₀B₀*)^{-1}`, `G_C = C₀(C₀*C₀)^{-1}` | verbatim; `B₀ = (frameMat b)ᵀ` (2×4), `C₀ = frameMat c` (4×2) | none |
| `SeedFrames` (structure) | (3.5): "ran K_B = ker B₀, ran K_C = ker C₀*", `K_B*K_B = K_C*K_C = I₂` | **the existential of Lemma 3.1 becomes data**: the structure's fields are exactly `KB_orthonormal`, `KC_orthonormal`, `KB_in_kernel`, `KC_in_kernel`, `KB_span`, `KC_span`. Consequence: downstream modules never re-derive Gram–Schmidt, and nothing downstream can claim *more* than Lemma 3.1 gives | **yes** — the paper's frame construction is numerical ("the numerical construction chooses particular coordinate vectors; the ideal frames in this argument use those same choices", mub6.txt:712). Rendering: the *choice* is a parameter (the structure), and only the *properties* are used |
| `PK`, `PB`, `PC` (defs) | (3.6): `P_K = K_B K_B*`, `P_B = I − P_K`, `P_C = I − K_C K_C*` | verbatim | none |
| `frame_projection_identities` | (3.6): `P_B = I − P_K = G_B B₀`, `P_C = I − K_C K_C* = G_C C₀*` | statement only; the second conjunct is the paper's `P_C = G_C C₀*` | uses `seedGB`/`seedGC`, which the authors compute numerically |
| `SeedSingularBounds` (structure) | `m_B = σ_min(B₀)`, `m_C = σ_min(C₀)`, `m = min(m_B,m_C) > 0` | **deliberate weakening of the constants**: `mB` is *any* positive lower bound with `mB‖x‖ ≤ ‖B₀x‖` (domain `ℂ²`), not the sharp `σ_min`. Every use in §3 is `‖G_B‖_op = 1/m_B`, for which any certified lower bound suffices; recorded because the paper's numerical margins depend on the sharp value | `σ_min` is computed numerically by the authors' code; here it is an explicit binder |

**Reading of the lemma's endpoints.** The paper's `M(M*M)^{-1}` is `(M^+)*` (the conjugate transpose
of the Moore–Penrose pseudo-inverse), *not* `M^+`. The formula is transcribed as printed, not
silently transposed; this is the single most likely place for a transcription error and the reason
the two columns are spelled out above.

---

## B. Lemma 3.8 (norm exclusion), mub6.txt:1037–1047 — file `Mub6/Exclusion.lean`

Paper: *"Lemma 3.8 (Norm exclusion). A feasible completion associated to a cell must satisfy
∑_{i,j=0}^{3} (|D_ij| − 1)² ≤ z²."* Proof: *"Each D′_ij has modulus one, and the reverse triangle
inequality gives ||D_ij| − 1| ≤ |D′_ij − D_ij|. Sum the squares and use (3.19)."*

| Lean name | locator | change | code-dependence |
|---|---|---|---|
| `norm_exclusion` | (3.26) | **harmless generalisation**: the 4×4 index set becomes arbitrary finite `ι, κ`; the paper's case is `ι = κ = Fin 4`. The paper's `z` is dropped: the conclusion is `∑∑(|D_ij|−1)² ≤ ‖Z‖_F²`, i.e. (3.26) with the *exact* value instead of the bound | none |
| `norm_exclusion_z` | (3.26) verbatim | adds the paper's hypothesis `‖Z‖_F ≤ z` as `∑∑ normSq Z ≤ z²`, derived from (3.19) elsewhere. No weakening: if `z < 0` the hypothesis is unsatisfiable | none |

**Binder-by-binder.** Paper: "a feasible completion associated to a cell" (a *shared witness*: one
completion, giving `D′` and `Z = D′ − D`). Lean: `D`, `Z` free, and feasibility enters as
`hunit : ∀ i j, ‖D i j + Z i j‖ = 1`. The paper's implicit relation `D′ = D + Z` is therefore
*materialised* in `hunit` rather than left to a definition — deliberate, and the only difference in
the carrier. Quantifier order: `D, Z` then `hunit`, then the conclusion — no witness is shared
across an alternation, so no quantifier-strength change. Endpoints: `|D_ij|` (stored), not `|D′_ij|`;
both sides squared, no `sqrt` introduced.

---

## C. Lemma 3.9 (directional exclusion), mub6.txt:1071–1105 — file `Mub6/Exclusion.lean`

Paper: *"Lemma 3.9 (Directional exclusion). Let y ∈ R20 be arbitrary, split as two pairs y_X, y_Y ∈
R² and a flat part y_D ∈ R¹⁶, and write g = J_all* y = (g_s, g_θ) ∈ R⁹ × R⁴. Every feasible
completion associated to the cell satisfies
y·c_all ≤ R_s‖g_s‖ + h‖g_θ‖₁ + E_r‖D ∘ y_D‖_F + ½ z² max(0, max_{i,j}(−y_{D,ij})) + ½ R_s²(‖y_X‖ + ‖y_Y‖)."*

| Lean name | locator | change | code-dependence |
|---|---|---|---|
| `pairNorm` (def) | `‖y_X‖`, `‖y_Y‖` | Euclidean 2-norm **named explicitly**: Lean's default `‖·‖` on `ℝ × ℝ` is the *sup* norm. Using the default would have made the right-hand side larger, i.e. the lemma weaker; the paper's norm is Euclidean | none |
| `directional_exclusion` | (3.29) | see the five items below | **yes**, see item (d) |

Binder-by-binder, in the paper's order:

1. **`y` arbitrary.** Paper: "Let y ∈ R20 be arbitrary". Lean: `yD : ι → ℝ` and `yX : Fin 2 → Fin 2 → ℝ`
   are *free binders*, i.e. universally quantified in front of the statement — same position as the
   paper's "let … be arbitrary". The 20 coordinates are split 16 + 2×2 exactly as the paper does.
2. **"every feasible completion of the cell".** Lean: the completion's data `D, J, Z, cS, JS, ρS`
   are free binders with feasibility `hunit : ∀ i, ‖D i + Z i‖ = 1`. This is *equivalent*: nothing in
   the conclusion names a completion, so a statement uniform in the data is uniform over completions.
   (Recorded because a reader might expect an explicit `∀ completion`.)
3. **Shared witness `g`.** Paper: the same `g = J_all* y` produces both the linear bound
   `R_s‖g_s‖ + h‖g_θ‖₁` and the same term on the right of (3.29). Lean: one binder `gsθ` used in
   `hlinear` and in the conclusion, so the sharing is *preserved*, not duplicated. This is the
   quantifier-audit item that a careless transcription loses.
4. **`max(0, max_ij(−y_{D,ij}))`.** Lean: replaced by an arbitrary `M` with `0 ≤ M` and `−y_D i ≤ M`.
   **Deliberate weakening of the conclusion** (any admissible `M` may be used; the paper's value is
   the least one). Reason: `Finset.sup`/`iSup` bookkeeping over an abstract index type; the
   mathematical content is `−½ Σ y_D,ij |Z_ij|² ≤ ½ M ‖Z‖²`, which the proof does with `M` directly.
5. **The 13-coordinate layout and (3.28).** Lean: `hlinear` (the bound
   `y·J_all(s,θ) ≤ R_s‖g_s‖ + h‖g_θ‖₁`) is an **explicit hypothesis**. In the paper it is *derived*
   from the seed ball `‖s‖ ≤ R_s`, the angle box `|θ_a| ≤ h` and `g = J_all* y`, and that derivation
   uses the concrete ordering (3.2)/(3.28) of the 20 equations and 13 variables. **Code-dependence:**
   the ordering is produced by the authors' `eq` routine, is not available, and is therefore a
   hypothesis here — exactly the discipline required for code-dependent statements.
6. **The flat equations (3.28) are derived, not assumed.** Lean takes `hunit` plus `Z` and `J` and
   obtains `(|D′_i|²−1)/2 = c_i + Re(D̄_i J_i) + Re(D̄_i (Z−J)_i) + |Z_i|²/2`. Recorded because it
   changes the *hypothesis count* vs. a literal reading of the paper's proof (which starts from the
   twenty equations).
7. **Seed remainder (3.27).** Lean: `cS a + JS a + ρS a = 0` and `‖ρS a‖ ≤ R_s²/2`, i.e. the paper's
   `|ρ_X|, |ρ_Y| ≤ ½R_s²`.
8. **Endpoint norms.** `E_r‖D ∘ y_D‖_F` is rendered as `Er * sqrt(∑_i normSq(D i) * (yD i)²)`, the
   entrywise product taken over the abstract index type; for `ι = Fin 4 × Fin 4` this is exactly the
   Frobenius norm of the entrywise product ("the sixteen flat coordinates arranged as a 4-by-4
   matrix", mub6.txt:1093).

---

## D. Lemma 4.11 (ellipsoid containment), mub6.txt:1587–1610 — file `Mub6/Ellipsoid.lean`

Paper: *"Lemma 4.11 (Ellipsoid containment). For real linear maps A, B, vectors ‖s‖ ≤ r, ‖v‖ ≤ q,
and β > 0, the sum As + Bv belongs to the ellipsoid {G^{1/2} w : ‖w‖ ≤ 1} whenever
G ⪰ (1 + β)r²AA* + (1 + 1/β)q²BB*."*

| Lean name | locator | change | code-dependence |
|---|---|---|---|
| `InEllipsoid` (def) | the set `{G^{1/2} w : ‖w‖ ≤ 1}` | **deliberate re-rendering**: `∀ z, (z·x)² ≤ z ⬝ᵥ (G *ᵥ z)`, the support-function characterisation that the paper proves equivalent in the last paragraph of 4.11 ("the vectors satisfying |z·x| ≤ (z*Gz)^{1/2} for every z are exactly G^{1/2} times the unit ball"). Reason: the pin has **no matrix square root** (no `PosSemidef.sqrt`, no matrix CFC — see `DEPGRAPH-S3-S4.md`). The equivalence itself is **not** formalised: open bridge **B1**. | none |
| `ellipsoid_containment` | 4.11 | `G ⪰ …` is rendered **pointwise**: `(1+β)r²‖A*z‖² + (1+1/β)q²‖B*z‖² ≤ z*Gz` for every `z` — what the proof uses, and equivalent to the Loewner inequality when the difference is symmetric. Two extra binders `0 ≤ r`, `0 ≤ q`: they exclude only the **vacuous** cases `r < 0` (where `‖s‖ ≤ r` is unsatisfiable); no non-vacuous instance is lost. `A*z` is `Aᵀ *ᵥ z` (real transpose) | none |
| `sq_add_mul_le` | "The scalar inequality follows by completing a square" | the scalar core `(ru+qv)² ≤ (1+β)r²u² + (1+1/β)q²v²` for `u,v,r,q ≥ 0`, `β>0`, isolated as its own lemma | none |

**Binder order check.** Paper: `A, B` (maps), then `s, v` with the ball hypotheses, then `β > 0`
mentioned last but used in the hypothesis on `G`. Lean: `A B G` then `r q β` then `hβ hr hq` then
`hG` then `s v` then `hs hv`. `β` occurs in `hG`, on which the *conclusion* does not depend — no
dependency inversion. The conclusion names `A s + B v` and `G` only, matching the paper.

## E. Lemma 4.12 (offset ellipsoid norm bound), mub6.txt:1625–1637 — file `Mub6/Ellipsoid.lean`

Paper: *"Lemma 4.12 (Offset ellipsoid norm bound). Let G ⪰ 0 and U ∈ R^k. For every γ > λ_max(G) and
‖w‖ ≤ 1, ‖U + G^{1/2}w‖² ≤ γ(1 + U*(γI − G)^{-1}U). The simpler upper bound ‖U‖ + √λ_max(G) for the
norm is also valid. If offsets range over a convex hull of finitely many U_σ, it suffices to take the
largest of the bounds at those offsets."*

| Lean name | locator | change | code-dependence |
|---|---|---|---|
| `normSq_le_of_inEllipsoid` | "the simpler bound ‖U‖ + √λ_max(G)" | the ingredient: a point of the ellipsoid has `‖y‖² ≤ Λ` whenever `z*Gz ≤ Λ‖z‖²` for all `z`. **λ_max(G) replaced by an explicit `Λ`** — the paper's own convention (`E(G;{U_σ})` is "any certified upper bound obtained from Lemma 4.12"). Not a weakening: it is the universally quantified form | none |
| `offset_ellipsoid_bound` | (4.34) | **four explicit replacements**, each because the corresponding object is not in the pin: (i) `G^{1/2}` becomes a matrix `R` with `R*R = G` (exists for `G ⪰ 0` by the spectral theorem; existence **not** formalised — bridge **B2**); (ii) `(γI−G)^{-1}U` becomes a vector `p` with `(γI−G)p = U` (invertibility follows from `γ > λ_max`; **not derived**, assumed — bridge **B3**); (iii) `R(γI−G) = (γI−G)R` is a hypothesis `hcomm` (it follows from `R*R = G` and symmetry of `R`); (iv) `γ > λ_max(G)` becomes `(γI−G) ⪰ 0` **and** `0 ≤ γ`. Conclusion `∑(U_i + (R w)_i)² ≤ γ(1 + U·p)` is (4.34) with `U·p = U*(γI−G)^{-1}U` | the constants `γ, E(G;{U_σ})` are computed numerically by the authors' code; here they are binders |
| `offset_hull_bound` | "It suffices to take the largest of the bounds at those offsets" | convex-combination form: if every vertex `U_σ` satisfies `‖U_σ + y‖ ≤ E` then so does every convex combination. The paper's proof is "for fixed w, convexity of norm"; this is the `U`-convexity restated for a general `y` (here `y = G^{1/2}w`) | none |

---

## F. Deliberate omissions (recorded, not hidden)

* Lemma 3.1's **construction** of `K` (Gram–Schmidt choice) — existence only.
* The **derivation** of `y·J_all ≤ R_s‖g_s‖ + h‖g_θ‖₁` from the 13-coordinate layout — hypothesis.
* `{G^{1/2}w}` as a set of vectors — replaced by the support-function form (bridge B1).
* Eigenvalue/square-root bookkeeping of singular values — charpoly form used instead.
* Nothing was weakened silently: every `⊆`/hypothesis addition above is a *binder* in the Lean
  statement, and every conclusion-strength change is listed with its direction.
