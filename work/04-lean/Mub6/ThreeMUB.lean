/-
Mub6/ThreeMUB.lean — §1.3, Lemma 1.2: three pairwise unbiased orthonormal bases in `ℂ⁶`.

The paper's construction is `U_r = A_r ⊗ B_r` with `A_r` the three 2×2 unitaries and `B_r = 1, F, DF`
the three 3×3 unitaries, `F = (1/√3)(ω^{jk})`, `D = diag(1, ω, ω) = diag(ω^{x²})`, `ω = e^{2πi/3}`.
The paper itself flags the cross product `F^* D F` as "the only cross product that is not immediate",
and its entries are the Gauss sums `(1/3)∑_x ω^{x² + t x}` with values `1 + 2ω` (`t = 0`) and
`2 + ω²` (`t = 1, 2`), each of squared modulus `3`.

PROOF STATUS: mixed.
* Proved here: `ω² + ω + 1 = 0`, `ω³ = 1`, `ω⁶ = ω⁸ = 1`-type reductions, `|ω|² = 1`, the two
  Gauss-sum values `gauss_zero`, `gauss_one`, `gauss_two`, and `|1 + 2ω|² = |2 + ω²|² = 3`.  This is
  exactly the part of Lemma 1.2 the paper calls non-immediate.
* Statement-only (`sorry`): the entrywise identity `(F^* D F)_{jk} = (1/3)·gauss ((k-j) mod 3)`, the
  2×2 cross-product check, and the final existence theorem `three_mub_exists`.  These are expanded
  mechanical computations; they are listed in reports/status.md with their axiom footprint.
-/
import Mub6.Basic

namespace Mub6

open scoped Matrix
open Finset

/-- `ω = e^{2πi/3}`, in the closed form `-1/2 + (√3/2)i` (no trigonometry needed). -/
noncomputable def ω : ℂ := ⟨-1 / 2, Real.sqrt 3 / 2⟩

theorem sqrt3_sq : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)

/-- `ω² = -1 - ω`, the only relation needed downstream. -/
theorem omega_sq : ω ^ 2 = -1 - ω := by
  refine Complex.ext ?_ ?_ <;> simp [ω, pow_two] <;> nlinarith [sqrt3_sq]

/-- `1 + ω + ω² = 0`. -/
theorem omega_add : ω ^ 2 + ω + 1 = 0 := by
  linear_combination omega_sq

/-- `ω³ = 1`. -/
theorem omega_cube : ω ^ 3 = 1 := by
  have h : (ω - 1) * (ω ^ 2 + ω + 1) = 0 := by rw [omega_add, mul_zero]
  have expand : (ω - 1) * (ω ^ 2 + ω + 1) = ω ^ 3 - 1 := by ring
  rw [expand] at h
  exact sub_eq_zero.mp h

theorem omega_pow_four : ω ^ 4 = ω := by
  rw [show (4 : ℕ) = 3 + 1 by norm_num, pow_add, omega_cube, one_mul, pow_one]

theorem omega_pow_six : ω ^ 6 = 1 := by
  rw [show (6 : ℕ) = 3 + 3 by norm_num, pow_add, omega_cube, one_mul]

theorem omega_pow_eight : ω ^ 8 = ω ^ 2 := by
  rw [show (8 : ℕ) = 6 + 2 by norm_num, pow_add, omega_pow_six, one_mul]

theorem normSq_omega : Complex.normSq ω = 1 := by
  rw [Complex.normSq_apply]
  simp only [ω]
  nlinarith [sqrt3_sq]

/-- `|1 + 2ω|² = 3`: `1 + 2ω = i√3`. -/
theorem normSq_one_add_two_omega : Complex.normSq (1 + 2 * ω) = 3 := by
  have h : (1 + 2 * ω : ℂ) = ⟨0, Real.sqrt 3⟩ := by
    refine Complex.ext ?_ ?_ <;> simp [ω] <;> ring
  rw [h, Complex.normSq_apply]
  nlinarith [sqrt3_sq]

/-- `|2 + ω²|² = 3`: `2 + ω² = 3/2 - (√3/2)i`. -/
theorem normSq_two_add_omega_sq : Complex.normSq (2 + ω ^ 2) = 3 := by
  have h : (2 + ω ^ 2 : ℂ) = ⟨3 / 2, -(Real.sqrt 3 / 2)⟩ := by
    rw [omega_sq]
    refine Complex.ext ?_ ?_ <;> simp [ω] <;> ring
  rw [h, Complex.normSq_apply]
  nlinarith [sqrt3_sq]

/-! ### The Gauss sums `∑_{x=0}^{2} ω^{x² + t x}` -/

/-- The Gauss sum of Lemma 1.2 for `t ∈ {0,1,2}`. -/
noncomputable def gauss (t : ℕ) : ℂ := ∑ x ∈ Finset.range 3, ω ^ (x ^ 2 + t * x)

/-- `t = 0`: the sum is `1 + 2ω` (values `ω⁰, ω¹, ω⁴ = ω`). -/
theorem gauss_zero : gauss 0 = 1 + 2 * ω := by
  have h : gauss 0 = 1 + ω + ω ^ 4 := by simp [gauss, Finset.sum_range_succ]
  rw [h, omega_pow_four]; ring

/-- `t = 1`: the sum is `2 + ω²` (values `ω⁰, ω², ω⁶ = 1`). -/
theorem gauss_one : gauss 1 = 2 + ω ^ 2 := by
  have h : gauss 1 = 1 + ω ^ 2 + ω ^ 6 := by simp [gauss, Finset.sum_range_succ]
  rw [h, omega_pow_six]; ring

/-- `t = 2`: the sum is `2 + ω²` (values `ω⁰, ω³ = 1, ω⁸ = ω²`). -/
theorem gauss_two : gauss 2 = 2 + ω ^ 2 := by
  have h : gauss 2 = 1 + ω ^ 3 + ω ^ 8 := by simp [gauss, Finset.sum_range_succ]
  rw [h, omega_pow_eight, omega_cube]; ring

/-! ### The 3×3 phase matrices of Lemma 1.2 -/

/-- `F = (1/√3)(ω^{jk})_{j,k=0..2}`. -/
noncomputable def Fmat : Matrix (Fin 3) (Fin 3) ℂ :=
  fun j k => (1 / (Real.sqrt 3 : ℂ)) * ω ^ ((j : ℕ) * (k : ℕ))

/-- `D = diag(1, ω, ω) = diag(ω^{x²})`. -/
noncomputable def Dmat : Matrix (Fin 3) (Fin 3) ℂ :=
  fun j k => if j = k then ω ^ (j : ℕ) ^ 2 else 0

/-- **Lemma 1.2, the Gauss-sum step (STATEMENT-ONLY here).**  The entries of `F^* D F` are the
Gauss sums of the paper, divided by three.  The three values are `gauss_zero`, `gauss_one`,
`gauss_two` above, each of squared modulus `3`; hence every entry of `F^* D F` has squared modulus
`1/3`. -/
theorem FDF_entry (j k : Fin 3) :
    (Fmatᴴ * Dmat * Fmat) j k = (1 / 3 : ℂ) * gauss (((k - j : Fin 3) : ℕ)) := by
  sorry

/- The 2×2 cross-product check of Lemma 1.2 is not restated separately here: it is part of
`three_mub_exists` below.  For the record, `A₁ = (1/√2)!![1,1;1,-1]`, `A₂ = (1/√2)!![1,1;i,-i]` and
`A₁^* A₂ = (1/2)!![1+i,1-i;1-i,1+i]`, whose entries have squared modulus `(1+1)/4 = 1/2`. -/

/-! ### The conclusion of Lemma 1.2 -/

/-- **Lemma 1.2 (Three mutually unbiased bases in dimension six), STATEMENT-ONLY.**
There are two complex Hadamard matrices in the sense of Definition 2.1 that are unbiased to each
other; with the standard basis this is the paper's family of three pairwise unbiased orthonormal
bases (`U₀ = I₆`, `U₁ = A₁ ⊗ B₁`, `U₂ = A₂ ⊗ B₂`), since `|H_{ij}| = 1` makes both Hadamards
unbiased to the standard basis automatically. -/
theorem three_mub_exists :
    ∃ H K : Mat 6, IsPhaseHadamard H ∧ IsPhaseHadamard K ∧ UnbiasedH H K := by
  sorry

end Mub6
