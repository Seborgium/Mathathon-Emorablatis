# Proof status — §3.1, §3.6, §4.11–4.12 (member m4, direction d2)

**Status is about machines, fidelity is about the paper.** Fidelity for these rows is in
`reports/statements-S3-S4.md`; a row can be `compiles / stated only` and still be *faithful*, and a
row can be `proved` and still be a *deliberate weakening* (the `M`-replacement in Lemma 3.9).

Validation method: `lean <file>` with the preset `LEAN_PATH`, one file at a time, oleans emitted with
`lean -o` so that the modules can be imported. No `lake build` against `/opt/mathlib` was attempted
(root-owned). Axiom footprints below are the output of `#print axioms` on each declaration; the three
Lean axioms `propext`, `Classical.choice`, `Quot.sound` are present throughout and are not listed.

| declaration | file | compiles | `sorryAx` | remaining goals |
|---|---|---|---|---|
| `UnitModulus`, `frameMat`, `seedSum`, `gramMat`, `gramInv`, `framePseudoInv`, `framePseudoInvFormula`, `seedGB`, `seedGC`, `PK`, `PB`, `PC`, `pairNorm`, `InEllipsoid` | Frames, Ellipsoid | yes | no | — (definitions) |
| `conj_mul_self` | Frames | yes | **no** | — |
| `star_mul_self` | Frames | yes | **no** | — |
| `seedSum_mul_conj` | Frames | yes | **no** | — |
| `frameMat_conjTranspose_mul` | Frames | yes | yes | 2×2 entry evaluation. The mathematics is a two-line computation; the cost is Lean `Fin 2`/`!![]` index reduction. Statement transcribed with the paper's orientation (S at (0,1)) |
| `frameMat_charpoly` | Frames | yes | yes | needs the trace/det reductions `trace = 8`, `det = 16 − |S|²` from the previous row |
| `frameMat_sq_singular_pair` | Frames | yes | yes | polynomial bookkeeping `(X−a)(X−b) = X² − 8X + (16−|S|²)` |
| `gram_mul_gramInv` | Frames | yes | yes | scalar `c·(16−|S|²) = 1` and `S·S̄ = |S|²` inside a `2×2` product |
| `frameMat_mul_gramInv` | Frames | yes | yes | follows from the previous row by `Matrix.inv_eq_right_inv` plus a 4×2 product |
| `kerFrame_exists` | Frames | yes | yes | existence of the Gram–Schmidt frame; needs a kernel-dimension argument (`finrank ker M* = 2`) plus orthonormalisation |
| `frame_projection_identities` | Frames | yes | yes | (3.6) from (3.4) and `ran K_B = ker B₀` |
| `SeedSingularBounds.m_pos` | Frames | yes | **no** | — |
| `norm_exclusion` | Exclusion | yes | **no** | — |
| `norm_exclusion_z` | Exclusion | yes | **no** | — |
| `directional_exclusion` | Exclusion | yes | yes | four sub-goals, in the paper's own order: (i) the flat identity `(|D+Z|²−1)/2 = c + Re(D̄J) + Re(D̄(Z−J)) + |Z|²/2`; (ii) Cauchy–Schwarz `Σ y_D Re(D̄ R) ≤ E_r‖D∘y_D‖_F`; (iii) the sign step `−½Σ y_D|Z|² ≤ ½ M‖Z‖²`; (iv) `Σ⟪y_X,ρ_S⟫ ≤ ½R_s²(‖y_X‖+‖y_Y‖)`. (i) is the crux and is a real-imaginary `ring` identity |
| `ellipsoid_containment` | Ellipsoid | yes | yes | (i) `z·(As+Bv) = (Aᵀz)·s + (Bᵀz)·v`; (ii) two Cauchy–Schwarz steps with `‖s‖ ≤ r`, `‖v‖ ≤ q`; (iii) `sq_add_mul_le` |
| `sq_add_mul_le` | Ellipsoid | yes | yes | `β·((1+β)r²u² + (1+1/β)q²v² − (ru+qv)²) = (√β·ru − qv)²` |
| `normSq_le_of_inEllipsoid` | Ellipsoid | yes | **no** | — |
| `offset_ellipsoid_bound` | Ellipsoid | yes | yes | `‖U+Rw‖² = ‖U‖² + 2(RU)·w + w*Gw`; `w*Gw = γ‖w‖² − w*Aw`; the AM–GM step `2(Aw)·p' ≤ w*Aw + p'·Ap'` for `p' = Rp` (a perfect square in `A`); then `‖U‖² + U*Gp = γU·p` |
| `offset_hull_bound` | Ellipsoid | yes | yes | triangle inequality + convexity of `U ↦ ‖U+y‖` |

Summary: **7 declarations Lean-checked** (no `sorryAx`), **12 transcribed with `sorryAx`**, 0 files
with an undeclared hole, 0 `admit`s. Every `sorry` has a row above.

## Open bridges (the things a future window must build, in dependency order)

* **B1** — `{G^{1/2}w : ‖w‖ ≤ 1} = {x : ∀z, (z·x)² ≤ z*Gz}`. Needs the spectral theorem for real
  symmetric matrices and a matrix square root. Blocks the *set-theoretic* reading of Lemma 4.11 and
  of `E(G;{U_σ})` in §4.5–4.6. Consequence for this window: `InEllipsoid` is the support form.
* **B2** — existence of `R` with `R*R = G` for `G ⪰ 0` (same spectral input). Blocks removing
  `hRsq` from `offset_ellipsoid_bound`.
* **B3** — invertibility of `γI − G` from `γ > λ_max(G)`, and `‖G^{1/2}v‖² = v*Gv`. Blocks removing
  `hp`/`hcomm`.
* **B4** — `Matrix.IsHadamard` (pin, `LinearAlgebra/Matrix/HadamardMatrix.lean`) to the paper's
  one-sided Definition 2.1: **not mine**, belongs to the §2 module; noted here because the §3 frames
  are used to analyse Hadamards whose block is `D'`.

## What was *not* attempted

* No proof of the five Stage-A/B assembly implications (other direction).
* No numerical constants (§3.2–3.5 `q`, `p`, `z`, `E_r`, `L`, `A₀`). They are the authors' code's
  output and are absent from the preprint's text in closed form; the statements here take them as
  binders precisely so that the transcriptions stay faithful.
* No `lakefile.lean` / `lean-toolchain` — that is the scaffold direction; my modules import
  `Mub6.Basic` and nothing else, so the DAG inserts below whatever the scaffold provides.
