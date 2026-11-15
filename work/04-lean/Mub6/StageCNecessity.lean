import Mathlib

/-!
# Stage-C necessity lemma: label distinctness needs a ball-diameter bound
-/

noncomputable section

open scoped InnerProductSpace ComplexInnerProductSpace

namespace StageC

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

/-- `γ = √(2 - 2/√6)`. -/
def gamma : ℝ := Real.sqrt (2 - 2 / Real.sqrt 6)

lemma sqrt6_pos : (0 : ℝ) < Real.sqrt 6 := Real.sqrt_pos.mpr (by norm_num)

lemma one_le_sqrt6 : (1 : ℝ) ≤ Real.sqrt 6 := Real.one_le_sqrt.mpr (by norm_num)

lemma one_lt_sqrt6 : (1 : ℝ) < Real.sqrt 6 := by
  have h : (0:ℝ) < Real.sqrt 6 := sqrt6_pos
  nlinarith [Real.sq_sqrt (show (0:ℝ) ≤ 6 by norm_num), Real.sqrt_nonneg 6]

/-- Expansion of `‖x - y‖ ^ 2` over `ℂ` (field argument made explicit). -/
lemma nsq (x y : E) : ‖x - y‖ ^ 2 = ‖x‖ ^ 2 - 2 * RCLike.re (inner ℂ x y) + ‖y‖ ^ 2 :=
  norm_sub_sq (𝕜 := ℂ) x y

lemma gamma_arg_nonneg : (0 : ℝ) ≤ 2 - 2 / Real.sqrt 6 := by
  have h : 2 / Real.sqrt 6 ≤ 2 := by
    rw [div_le_iff₀ sqrt6_pos]; nlinarith [one_le_sqrt6]
  linarith

lemma gamma_sq : gamma ^ 2 = 2 - 2 / Real.sqrt 6 := by
  rw [gamma, Real.sq_sqrt gamma_arg_nonneg]

lemma gamma_pos : 0 < gamma := by
  rw [gamma, Real.sqrt_pos]
  have h : 2 / Real.sqrt 6 < 2 := by
    rw [div_lt_iff₀ sqrt6_pos]; nlinarith [one_lt_sqrt6]
  linarith

lemma gamma_lt_sqrt_two : gamma < Real.sqrt 2 := by
  have h2 : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hlt : gamma ^ 2 < (Real.sqrt 2) ^ 2 := by
    rw [gamma_sq, h2]
    have : 0 < 2 / Real.sqrt 6 := by positivity
    linarith
  nlinarith [gamma_pos.le, Real.sqrt_nonneg 2]

/-- Two unit vectors mutually unbiased in dimension `6` are at distance `≥ γ`. -/
theorem gamma_le_norm_sub_mub {x y : E} (hx : ‖x‖ = 1) (hy : ‖y‖ = 1)
    (h : ‖⟪x, y⟫_ℂ‖ = 1 / Real.sqrt 6) : gamma ≤ ‖x - y‖ := by
  have hre : RCLike.re (inner ℂ x y) ≤ 1 / Real.sqrt 6 := by
    calc RCLike.re (inner ℂ x y) ≤ ‖inner ℂ x y‖ := RCLike.re_le_norm _
      _ = 1 / Real.sqrt 6 := h
  have hsq : gamma ^ 2 ≤ ‖x - y‖ ^ 2 := by
    have hd : 2 / Real.sqrt 6 = 2 * (1 / Real.sqrt 6) := by ring
    rw [nsq, hx, hy, gamma_sq, hd]
    linarith
  nlinarith [gamma_pos.le, norm_nonneg (x - y)]

/-- Two orthogonal unit vectors are at distance `≥ γ` (indeed `√2 ≥ γ`). -/
theorem gamma_le_norm_sub_ortho {x y : E} (hx : ‖x‖ = 1) (hy : ‖y‖ = 1)
    (h : ⟪x, y⟫_ℂ = 0) : gamma ≤ ‖x - y‖ := by
  have hsq : gamma ^ 2 ≤ ‖x - y‖ ^ 2 := by
    rw [nsq, hx, hy, h, map_zero, gamma_sq]
    have hpos : 0 < 2 / Real.sqrt 6 := by positivity
    linarith
  nlinarith [gamma_pos.le, norm_nonneg (x - y)]

/-- The twelve vectors of two bases are pairwise at distance `≥ γ`. -/
theorem gamma_le_norm_sub_pair {B₁ B₂ : Fin 6 → E}
    (hn₁ : ∀ i, ‖B₁ i‖ = 1) (hn₂ : ∀ i, ‖B₂ i‖ = 1)
    (ho₁ : ∀ i j, i ≠ j → ⟪B₁ i, B₁ j⟫_ℂ = 0)
    (ho₂ : ∀ i j, i ≠ j → ⟪B₂ i, B₂ j⟫_ℂ = 0)
    (hu : ∀ i j, ‖⟪B₁ i, B₂ j⟫_ℂ‖ = 1 / Real.sqrt 6)
    {k k' : Fin 6 ⊕ Fin 6} (h : k ≠ k') :
    gamma ≤ ‖Sum.elim B₁ B₂ k - Sum.elim B₁ B₂ k'‖ := by
  rcases k with i | i <;> rcases k' with j | j <;>
    simp only [Sum.elim_inl, Sum.elim_inr]
  · exact gamma_le_norm_sub_ortho (hn₁ i) (hn₁ j) (ho₁ i j (by rintro rfl; exact h rfl))
  · exact gamma_le_norm_sub_mub (hn₁ i) (hn₂ j) (hu i j)
  · exact gamma_le_norm_sub_mub (hn₂ i) (hn₁ j) (by rw [norm_inner_symm]; exact hu j i)
  · exact gamma_le_norm_sub_ortho (hn₂ i) (hn₂ j) (ho₂ i j (by rintro rfl; exact h rfl))

/-- **Label distinctness.**  No two of the twelve vectors lie in the same ball. -/
theorem label_injective {L : Type*} [DecidableEq L] {V : L → Set E} (lab : Fin 6 ⊕ Fin 6 → L)
    {B₁ B₂ : Fin 6 → E}
    (hV : ∀ k, Sum.elim B₁ B₂ k ∈ V (lab k))
    (hdiam : ∀ (l : L) (x : E), x ∈ V l → ∀ (y : E), y ∈ V l → ‖x - y‖ < gamma)
    (hn₁ : ∀ i, ‖B₁ i‖ = 1) (hn₂ : ∀ i, ‖B₂ i‖ = 1)
    (ho₁ : ∀ i j, i ≠ j → ⟪B₁ i, B₁ j⟫_ℂ = 0)
    (ho₂ : ∀ i j, i ≠ j → ⟪B₂ i, B₂ j⟫_ℂ = 0)
    (hu : ∀ i j, ‖⟪B₁ i, B₂ j⟫_ℂ‖ = 1 / Real.sqrt 6) :
    Function.Injective lab := by
  intro k k' hkk
  by_contra hne
  have hlt : ‖Sum.elim B₁ B₂ k - Sum.elim B₁ B₂ k'‖ < gamma :=
    hdiam (lab k) _ (hV k) _ (by rw [hkk]; exact hV k')
  have hge := gamma_le_norm_sub_pair hn₁ hn₂ ho₁ ho₂ hu hne
  linarith

/-- **Stage-C necessity lemma.** -/
theorem false_of_two_mub_bases {L : Type*} [DecidableEq L] {V : L → Set E} {O U : L → L → Prop}
    (lab : Fin 6 ⊕ Fin 6 → L) {B₁ B₂ : Fin 6 → E}
    (hV : ∀ k, Sum.elim B₁ B₂ k ∈ V (lab k))
    (hdiam : ∀ (l : L) (x : E), x ∈ V l → ∀ (y : E), y ∈ V l → ‖x - y‖ < gamma)
    (hn₁ : ∀ i, ‖B₁ i‖ = 1) (hn₂ : ∀ i, ‖B₂ i‖ = 1)
    (ho₁ : ∀ i j, i ≠ j → ⟪B₁ i, B₁ j⟫_ℂ = 0)
    (ho₂ : ∀ i j, i ≠ j → ⟪B₂ i, B₂ j⟫_ℂ = 0)
    (hu : ∀ i j, ‖⟪B₁ i, B₂ j⟫_ℂ‖ = 1 / Real.sqrt 6)
    (hO : ∀ (l l' : L) (x : E), x ∈ V l → ∀ (y : E), y ∈ V l' → ⟪x, y⟫_ℂ = 0 → O l l')
    (hU : ∀ (l l' : L) (x : E), x ∈ V l → ∀ (y : E), y ∈ V l' →
      ‖⟪x, y⟫_ℂ‖ = 1 / Real.sqrt 6 → U l l')
    (hpat : ¬ ∃ s t : Finset L, s.card = 6 ∧ t.card = 6 ∧ Disjoint s t ∧
      (∀ x ∈ s, ∀ y ∈ s, x ≠ y → O x y) ∧
      (∀ x ∈ t, ∀ y ∈ t, x ≠ y → O x y) ∧
      (∀ x ∈ s, ∀ y ∈ t, U x y)) :
    False := by
  have hinj := label_injective lab hV hdiam hn₁ hn₂ ho₁ ho₂ hu
  have hinl : Function.Injective (fun i => lab (Sum.inl i)) := hinj.comp Sum.inl_injective
  have hinr : Function.Injective (fun j => lab (Sum.inr j)) := hinj.comp Sum.inr_injective
  apply hpat
  refine ⟨Finset.univ.image (fun i => lab (Sum.inl i)),
          Finset.univ.image (fun j => lab (Sum.inr j)), ?_, ?_, ?_, ?_, ?_, ?_⟩
  · rw [Finset.card_image_of_injective _ hinl, Finset.card_univ, Fintype.card_fin]
  · rw [Finset.card_image_of_injective _ hinr, Finset.card_univ, Fintype.card_fin]
  · rw [Finset.disjoint_left]
    intro l hl hl'
    simp only [Finset.mem_image, Finset.mem_univ, true_and] at hl hl'
    obtain ⟨i, rfl⟩ := hl
    obtain ⟨j, hj⟩ := hl'
    exact Sum.inl_ne_inr (hinj hj.symm)
  · intro x hx y hy hxy
    simp only [Finset.mem_image, Finset.mem_univ, true_and] at hx hy
    obtain ⟨i, rfl⟩ := hx
    obtain ⟨j, rfl⟩ := hy
    exact hO _ _ _ (hV _) _ (hV _) (ho₁ i j (by rintro rfl; exact hxy rfl))
  · intro x hx y hy hxy
    simp only [Finset.mem_image, Finset.mem_univ, true_and] at hx hy
    obtain ⟨i, rfl⟩ := hx
    obtain ⟨j, rfl⟩ := hy
    exact hO _ _ _ (hV _) _ (hV _) (ho₂ i j (by rintro rfl; exact hxy rfl))
  · intro x hx y hy
    simp only [Finset.mem_image, Finset.mem_univ, true_and] at hx hy
    obtain ⟨i, rfl⟩ := hx
    obtain ⟨j, rfl⟩ := hy
    exact hU _ _ _ (hV _) _ (hV _) (hu i j)

end StageC
