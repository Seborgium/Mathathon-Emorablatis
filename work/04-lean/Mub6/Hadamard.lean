/-
Mub6/Hadamard.lean — §2.1: complex Hadamard matrices, the five equivalences (Lemma 2.2), and
double centring as the orthogonal projection (Lemma 2.3).

PROOF STATUS: mixed.  Everything about `Π` and about the phase exponential on this page is proved.
The five invariance clauses of Lemma 2.2 are transcribed as declarations and left unproved in this
window (`sorry`); they are listed with their axiom footprint in reports/status.md.  Nothing here
relies on the unproved clauses.

What is *not* claimed: the paper's Lemma 2.2 is about extendibility, and each clause is asserted in
both directions.  Both directions are stated separately below (`extendible_*` and its converse
`extendible_*_iff`), so a reader can see exactly which direction carries the content (only
transposition is not immediate).
-/
import Mub6.Basic

namespace Mub6

open scoped Matrix
open Finset

/-! ### The phase exponential is a character of the additive group -/

theorem e_add (a b : ℝ) : e (a + b) = e a * e b := by
  unfold e
  rw [← Complex.exp_add]
  congr 1
  push_cast
  ring

theorem e_zero : e 0 = 1 := by
  unfold e
  simp

theorem e_neg (a : ℝ) : e (-a) = (e a)⁻¹ := by
  unfold e
  rw [← Complex.exp_neg]
  congr 1
  push_cast
  ring

/-! ### Lemma 2.3, the rephasing half

Two phase lifts differing by `z` give, after replacing the second by `P + Π z`, matrices whose
exponentials differ only by a row phase and a column phase — the content of the second sentence of
Lemma 2.3, given `sub_Pi_eq_rowcol`. -/

/-- `e` applied to a row-plus-column addition factors into a row phase times a column phase. -/
theorem expMat_rowcol_add (P : RealMat 6) (r c : Fin 6 → ℝ) :
    expMat (fun i j => P i j + (r i + c j)) = fun i j => e (r i) * e (c j) * expMat P i j := by
  ext i j
  simp only [expMat, e_add]
  ring

/-- `e` of an integer is one. -/
theorem e_int (k : ℤ) : e (k : ℝ) = 1 := by
  unfold e
  rw [show ((2 * Real.pi * (k : ℝ) : ℝ) : ℂ) * Complex.I
        = (k : ℂ) * (2 * (Real.pi : ℂ) * Complex.I) by push_cast; ring]
  exact Complex.exp_int_mul_two_pi_mul_I k

/-- Entrywise integer shifts are invisible to `e(P)`: `e(t + k) = e t` for integer `k`. -/
theorem e_add_int (t : ℝ) (k : ℤ) : e (t + k) = e t := by
  rw [e_add, e_int, mul_one]

/-- Lemma 2.3, integer-shift clause: adding integer multiples of `2π` to the phases does not
change the matrix. -/
theorem expMat_int_shift (P : RealMat 6) (m : Fin 6 → Fin 6 → ℤ) :
    expMat (fun i j => P i j + (m i j : ℝ)) = expMat P := by
  ext i j
  simp only [expMat, e_add_int]

/-! ### Lemma 2.3, the norm bound

`Π z` is horizontal, `z - Π z` is a sum of a row-constant and a column-constant matrix, and the two
are orthogonal in the Frobenius inner product: hence `‖Π z‖_F ≤ ‖z‖_F`.  This is proved, not
assumed; the projection statement itself (that `Π` is *the* orthogonal projection, i.e. its range is
exactly the horizontal subspace) follows from `horizontal_iff_Pi_eq_self`. -/

/-- Orthogonality of the horizontal subspace to row-plus-column matrices. -/
theorem sum_mul_rowcol_zero (h : RealMat 6) (hh : Horizontal h) (r c : Fin 6 → ℝ) :
    ∑ i, ∑ j, h i j * (r i + c j) = 0 := by
  have h1 : ∑ i, ∑ j, h i j * r i = 0 := by
    refine Finset.sum_eq_zero (fun i _ => ?_)
    rw [← Finset.sum_mul, hh.1 i, zero_mul]
  have h2 : ∑ i, ∑ j, h i j * c j = 0 := by
    rw [Finset.sum_comm]
    refine Finset.sum_eq_zero (fun j _ => ?_)
    rw [← Finset.sum_mul, hh.2 j, zero_mul]
  simp only [mul_add, Finset.sum_add_distrib, h1, h2, add_zero]

theorem frobSqR_nonneg (A : RealMat 6) : 0 ≤ frobSqR A := by
  refine Finset.sum_nonneg (fun i _ => Finset.sum_nonneg (fun j _ => ?_))
  exact sq_nonneg _

/-- Pythagoras for matrices with vanishing Frobenius cross term. -/
theorem frobSqR_add_of_cross_zero (A B : RealMat 6)
    (h : ∑ i, ∑ j, A i j * B i j = 0) :
    frobSqR (A + B) = frobSqR A + frobSqR B := by
  have hBA : ∑ i, ∑ j, B i j * A i j = 0 := by
    rw [← h]
    exact Finset.sum_congr rfl (fun i _ => Finset.sum_congr rfl (fun j _ => by ring))
  have hexp : ∀ i j : Fin 6, (A i j + B i j) ^ 2
      = A i j ^ 2 + B i j ^ 2 + (A i j * B i j + B i j * A i j) := fun i j => by ring
  simp only [frobSqR, Matrix.add_apply, hexp, Finset.sum_add_distrib, h, hBA, add_zero]

/-- **Lemma 2.3, norm bound.** `‖Π z‖_F ≤ ‖z‖_F`. -/
theorem Pi_frobSqR_le (z : RealMat 6) : frobSqR (Pi z) ≤ frobSqR z := by
  obtain ⟨r, c, hrc⟩ := sub_Pi_eq_rowcol z
  have hcross : ∑ i, ∑ j, Pi z i j * (z - Pi z) i j = 0 := by
    have hz : ∑ i, ∑ j, Pi z i j * (fun i j => r i + c j) i j = 0 :=
      sum_mul_rowcol_zero (Pi z) (Pi_horizontal z) r c
    rwa [hrc]
  have hz : z = Pi z + (z - Pi z) := by
    ext i j; simp
  calc frobSqR (Pi z)
      ≤ frobSqR (Pi z) + frobSqR (z - Pi z) := by
        have := frobSqR_nonneg (z - Pi z); linarith
    _ = frobSqR (Pi z + (z - Pi z)) := (frobSqR_add_of_cross_zero _ _ hcross).symm
    _ = frobSqR z := by rw [← hz]

/-- **Lemma 2.3, rephasing sentence (packaged).**  If two phase lifts `P` and `Q` differ by `z`,
then `e(P + Π z)` and `e(Q)` differ only by a row phase and a column phase, and those phases are
exponentials of real angles (hence of modulus one) — exactly the paper's "the second is equivalent
under row and column rephasings to the first plus `Π z`". -/
theorem expMat_Pi_rephasing (P Q : RealMat 6) :
    ∃ a b : Fin 6 → ℝ, expMat (P + Pi (Q - P))
      = fun i j => e (-(a i)) * e (-(b j)) * expMat Q i j := by
  obtain ⟨a, b, hab⟩ := sub_Pi_eq_rowcol (Q - P)
  refine ⟨a, b, ?_⟩
  have hPQ : ∀ i j, (P + Pi (Q - P)) i j = Q i j + (-(a i) + -(b j)) := by
    intro i j
    have h1 : (Q - P) i j - Pi (Q - P) i j = a i + b j := by
      simpa only [Matrix.sub_apply] using congrFun (congrFun hab i) j
    have h2 : Pi (Q - P) i j = (Q - P) i j - (a i + b j) := by linarith
    simp only [Matrix.add_apply, Matrix.sub_apply] at h2 ⊢
    rw [h2]
    ring
  ext i j
  simp only [expMat, hPQ i j, e_add]
  ring

/-! ### Lemma 2.2: the five equivalences

The paper's operations, as maps on the Hadamard matrix `H` whose columns (divided by `√6`) are the
second basis.  Each is followed by the extendibility-invariance clause.  These five clauses are
STATEMENT-ONLY in this window. -/

/-- Row permutation. -/
def permRows (σ : Equiv.Perm (Fin 6)) (H : Mat 6) : Mat 6 := fun i j => H (σ i) j

/-- Column permutation. -/
def permCols (τ : Equiv.Perm (Fin 6)) (H : Mat 6) : Mat 6 := fun i j => H i (τ j)

/-- Multiplication of row `i` by the scalar `r i`. -/
def rephaseRows (r : Fin 6 → ℂ) (H : Mat 6) : Mat 6 := fun i j => r i * H i j

/-- Multiplication of column `j` by the scalar `c j`. -/
def rephaseCols (c : Fin 6 → ℂ) (H : Mat 6) : Mat 6 := fun i j => H i j * c j

/-- Complex conjugation. -/
def conjMat (H : Mat 6) : Mat 6 := fun i j => starRingEnd ℂ (H i j)

/-- Transposition. -/
def transposed (H : Mat 6) : Mat 6 := Hᵀ

/-- A scalar vector all of whose entries have modulus one. -/
def IsUnitScalarVec {n : ℕ} (r : Fin n → ℂ) : Prop := ∀ i, Complex.normSq (r i) = 1

/-- **Lemma 2.2 (row permutations).** -/
theorem extendible_permRows (σ : Equiv.Perm (Fin 6)) {H : Mat 6} (h : Extendible H) :
    Extendible (permRows σ H) := by
  sorry

/-- **Lemma 2.2 (column permutations).** -/
theorem extendible_permCols (τ : Equiv.Perm (Fin 6)) {H : Mat 6} (h : Extendible H) :
    Extendible (permCols τ H) := by
  sorry

/-- **Lemma 2.2 (row rephasings).** -/
theorem extendible_rephaseRows {r : Fin 6 → ℂ} (hr : IsUnitScalarVec r) {H : Mat 6}
    (h : Extendible H) : Extendible (rephaseRows r H) := by
  sorry

/-- **Lemma 2.2 (column rephasings).** -/
theorem extendible_rephaseCols {c : Fin 6 → ℂ} (hc : IsUnitScalarVec c) {H : Mat 6}
    (h : Extendible H) : Extendible (rephaseCols c H) := by
  sorry

/-- **Lemma 2.2 (complex conjugation).** -/
theorem extendible_conjMat {H : Mat 6} (h : Extendible H) : Extendible (conjMat H) := by
  sorry

/-- **Lemma 2.2 (transposition).** The only clause whose proof is not immediate. -/
theorem extendible_transposed {H : Mat 6} (h : Extendible H) : Extendible (transposed H) := by
  sorry

/-- Lemma 2.2 in the paper's form: extendibility is *invariant*, so each clause holds in both
directions.  `Equiv.Perm` and `IsUnitScalarVec` are involutive/closed under inverse, which is why
the one-directional clauses above give the equivalence.  STATEMENT-ONLY (it is the conjunction of
the six clauses above plus the inverse constructions). -/
theorem extendible_iff_all (H : Mat 6) :
    (∀ (σ τ : Equiv.Perm (Fin 6)) (r c : Fin 6 → ℂ), IsUnitScalarVec r → IsUnitScalarVec c →
        (Extendible H ↔ Extendible (permRows σ (permCols τ (rephaseRows r (rephaseCols c H))))))
      ∧ (Extendible H ↔ Extendible (conjMat H))
      ∧ (Extendible H ↔ Extendible (transposed H)) := by
  sorry

#check @Complex.exp_int_mul_two_pi_mul_I
#check @Complex.exp_two_pi_mul_I

end Mub6
