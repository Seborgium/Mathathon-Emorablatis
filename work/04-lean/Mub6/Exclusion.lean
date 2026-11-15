/-
Mub6/Exclusion.lean — §3.6: the two necessary (excluding) inequalities of Stage A.

Paper locators: Lemma 3.8 ("Norm exclusion", (3.26)), Lemma 3.9 ("Directional exclusion", (3.29)),
with (3.27) and (3.28) as the seed-remainder and flatness data.

Both lemmas are *necessary* conditions: they hold for every feasible completion in the cell, so
their failure certifies that the cell contains none (Corollary 3.10).  Formalising them as an
implication is therefore the whole content: the "certificate" reading never needs the converse.

Status: `norm_exclusion` is Lean-checked; `directional_exclusion` is transcribed with its binding
structure explicit and marked `stated only` — the remaining goals are listed in reports/status.md.
-/
import Mub6.Basic
import Mub6.Frames

noncomputable section

namespace Mub6

open Matrix
open scoped Matrix BigOperators

/-! ### Lemma 3.8 — norm exclusion (3.26) -/

/-- **Lemma 3.8 (norm exclusion).**  If a feasible completion has block `D' = D + Z` with every
entry of modulus one, then the deviation of the stored block `D` from the unit torus is bounded by
the total displacement: `∑_ij (|D_ij| - 1)^2 ≤ ‖Z‖_F^2`.

The paper's `z` is the certified upper bound `‖Z‖_F ≤ z`; `norm_exclusion_z` below is (3.26)
verbatim.  Nothing here uses the 4×4 shape: the proof is entrywise (reverse triangle inequality),
exactly as the paper's one-line proof says. -/
theorem norm_exclusion {ι κ : Type*} [Fintype ι] [Fintype κ]
    (D Z : ι → κ → ℂ) (hunit : ∀ i j, ‖D i j + Z i j‖ = 1) :
    (∑ i, ∑ j, (‖D i j‖ - 1) ^ 2) ≤ ∑ i, ∑ j, Complex.normSq (Z i j) := by
  refine Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j _ => ?_
  -- `| |D_ij| - 1 | ≤ |Z_ij|`, both directions from the triangle inequality
  have h1 : |‖D i j‖ - 1| ≤ ‖Z i j‖ := by
    rw [abs_le]
    constructor
    · -- `1 - ‖D‖ ≤ ‖Z‖` from `‖D + Z‖ ≤ ‖D‖ + ‖Z‖`
      have h := norm_add_le (D i j) (Z i j)
      rw [hunit i j] at h
      linarith
    · -- `‖D‖ - 1 ≤ ‖Z‖` from `‖D‖ = ‖(D + Z) - Z‖ ≤ ‖D + Z‖ + ‖Z‖`
      have h2 : ‖D i j‖ = ‖(D i j + Z i j) - Z i j‖ := by ring_nf
      have h3 : ‖(D i j + Z i j) - Z i j‖ ≤ 1 + ‖Z i j‖ := by
        calc ‖(D i j + Z i j) - Z i j‖ ≤ ‖D i j + Z i j‖ + ‖Z i j‖ := norm_sub_le _ _
          _ = 1 + ‖Z i j‖ := by rw [hunit i j]
      linarith
  calc (‖D i j‖ - 1) ^ 2 = |‖D i j‖ - 1| ^ 2 := (sq_abs _).symm
    _ ≤ ‖Z i j‖ ^ 2 := by
        have h0 := abs_nonneg (‖D i j‖ - 1)
        nlinarith [h1, h0, norm_nonneg (Z i j)]
    _ = Complex.normSq (Z i j) := Complex.sq_norm _

/-- **Lemma 3.8, as printed (3.26).**  If in addition `‖Z‖_F ≤ z` then
`∑_ij (|D_ij| - 1)^2 ≤ z^2`. -/
theorem norm_exclusion_z {ι κ : Type*} [Fintype ι] [Fintype κ]
    (D Z : ι → κ → ℂ) (hunit : ∀ i j, ‖D i j + Z i j‖ = 1) {z : ℝ}
    (hz : ∑ i, ∑ j, Complex.normSq (Z i j) ≤ z ^ 2) :
    (∑ i, ∑ j, (‖D i j‖ - 1) ^ 2) ≤ z ^ 2 :=
  le_trans (norm_exclusion D Z hunit) hz

/-! ### Lemma 3.9 — directional exclusion (3.29)

The paper's data: a cell of the seed box and angle box; a feasible completion determines
`Z = D' - D` (total block displacement), a linearisation `J(s,θ)`, a remainder `R = Z - J(s,θ)`,
constants `c_all ∈ ℝ^20` and a matrix `J_all ∈ ℝ^{20×13}`; `y ∈ ℝ^20` is an arbitrary test
direction and `g = J_all^* y = (g_s, g_θ)`.

Formalisation choices, recorded binder-by-binder in `reports/statements.md`:

* the 16 flat coordinates are indexed by an abstract finite type `ι`; the paper's `Σ_{ij}` over the
  4×4 block and its `max_{ij}` are the `ι`-indexed versions;
* the flat exact equations (3.28) are *derived* here from feasibility `|D'_i| = 1` with `D' = D + Z`
  and `Z = J + (Z - J)`, not assumed (the derivation is the identity `|D'|^2 = |D|^2 +
  2 Re(conj D · Z) + |Z|^2` with `Z = J + (Z-J)`);
* the two complex seed-sum equations of §3.6 are carried as `cS a + JS a + ρS a = 0` with the
  remainder bound `‖ρS a‖ ≤ R_s^2/2` — this is (3.27);
* the *bound* `y·J_all(s,θ) ≤ R_s‖g_s‖ + h‖g_θ‖₁` is the hypothesis `hlinear`: the paper derives it
  from the seed ball `‖s‖ ≤ R_s`, the angle box `|θ_a| ≤ h` and `g = J_all^* y`, and that
  derivation uses the concrete 13-coordinate layout of (3.28), which is a code-dependent ordering
  and is therefore *not* fixed here;
* `max(0, max_ij(-y_{D,ij}))` is replaced by an arbitrary `M` with `0 ≤ M` and `-y_D i ≤ M`: a
  deliberate weakening of the conclusion (any admissible `M` may be used; the paper's least such
  value is the sharpest). -/

/-- Euclidean norm of a pair of real weights, `‖y_X‖` in the paper (the standard `‖·‖` on `ℝ × ℝ`
is the sup norm, so the Euclidean version is named explicitly). -/
def pairNorm (y : Fin 2 → ℝ) : ℝ := Real.sqrt (∑ l, y l ^ 2)

/-- **Lemma 3.9 (directional exclusion), equation (3.29).**  For any real test vector `y` and every
feasible completion of the cell,

`y·c_all ≤ R_s‖g_s‖ + h‖g_θ‖₁ + E_r‖D ∘ y_D‖_F + (z^2/2) max(0, max_ij(-y_D,ij))
            + (R_s^2/2)(‖y_X‖ + ‖y_Y‖)`.

The right-hand side's first group `R_s‖g_s‖+h‖g_θ‖₁` is the hypothesis `hlinear` (see the module
docstring); everything else is derived. -/
theorem directional_exclusion
    {ι : Type*} [Fintype ι]
    (D J Z : ι → ℂ) (yD : ι → ℝ) (hunit : ∀ i, ‖D i + Z i‖ = 1)
    {z Er Rs gsθ M : ℝ}
    (hZ : ∑ i, Complex.normSq (Z i) ≤ z ^ 2)
    (hR : ∑ i, Complex.normSq (Z i - J i) ≤ Er ^ 2)
    (cS JS ρS : Fin 2 → ℂ) (yX : Fin 2 → Fin 2 → ℝ)
    (hseed : ∀ a, cS a + JS a + ρS a = 0)
    (hρ : ∀ a, ‖ρS a‖ ≤ Rs ^ 2 / 2)
    (hlinear : (∑ i, yD i * (starRingEnd ℂ (D i) * J i).re) +
        ∑ a, (yX a 0 * (JS a).re + yX a 1 * (JS a).im) ≤ gsθ)
    (hM0 : 0 ≤ M) (hM : ∀ i, -yD i ≤ M)
    (hRs : 0 ≤ Rs) (hEr : 0 ≤ Er) :
    (∑ i, yD i * ((Complex.normSq (D i) - 1) / 2)) +
        ∑ a, (yX a 0 * (cS a).re + yX a 1 * (cS a).im)
      ≤ gsθ + Er * Real.sqrt (∑ i, Complex.normSq (D i) * (yD i) ^ 2)
        + z ^ 2 / 2 * M + Rs ^ 2 / 2 * (pairNorm (yX 0) + pairNorm (yX 1)) := by
  sorry

end Mub6
