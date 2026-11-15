/-
Mub6/Exclude.lean

T4 Lean, group (B): the Stage-C exclusion geometric core (Section 6 of the preprint).

Carriers.  The paper works with phase vectors `e(β) ∈ (S¹)^6`; `e(t) = exp(2πit)`.  A vector is
unbiased to the coordinate basis iff it has the form `e(β)/√6`, and the global phase and the
integer lifts of the phases are irrelevant to orthogonality and unbiasedness.  We therefore carry
a *phase point* `u : Fin 6 → ℝ` (a point of the six-torus covered by ℝ^6) and define the two
relations on the unscaled inner-product sum

  `∑ j, e (u j - u' j)`  of modulus `0` for orthogonal vectors and `√6` for unbiased ones.

This file contains
* Lemma 6.5 (distinct labels), fully proved: two vectors in one closed vector ball `Bvec v s`
  with `s < .1` are neither orthogonal nor unbiased.  The arithmetic is the paper's
  `6 - 2π√6‖z‖ > 6 - 22/7 > √6`; Mathlib's `Real.pi_lt_d2` (`π < 3.15`) replaces `π < 22/7`,
  giving `6 - 63/20 > √6`, the same conclusion with slightly less slack (recorded in
  reports/statements-m3.md).
* Lemma 6.1 (bin displacement bounds), stated.
* Lemma 6.4 (certified clustering), stated with its hypothesis explicit.
* Lemma 6.8 (complete graph search), stated as an explicit hypothesis of Proposition 6.9:
  it is a specification claim about the routine `graph::exist`, so it can only be a binder.
* Proposition 6.9 (local exclusion certificate), proved from the above.
-/
import Mathlib
import Mub6.Interface

namespace Mub6
namespace StageC

open scoped BigOperators

/-! ## 1. Phases, phase points, and the two relations -/

/-- The paper's phase function `e(t) = exp(2πit)`. -/
noncomputable def e (t : ℝ) : ℂ := Complex.exp ((2 * Real.pi * t) * Complex.I)

lemma e_add (a b : ℝ) : e (a + b) = e a * e b := by
  simp only [e, ← Complex.exp_add]
  congr 1
  push_cast
  ring

lemma e_int (m : ℤ) : e (m : ℝ) = 1 := by
  simp only [e]
  rw [show (2 * Real.pi * (m : ℝ) * Complex.I) = (m : ℂ) * (2 * Real.pi * Complex.I) by
    push_cast; ring]
  exact Complex.exp_int_mul_two_pi_mul_I m

lemma norm_e (t : ℝ) : ‖e t‖ = 1 := by
  simp only [e]
  rw [Complex.norm_exp]
  simp

/-- The unscaled inner product sum of two phase points; `e(u)/√6` and `e(u')/√6` are orthogonal
iff this vanishes, and unbiased iff its modulus is `√6`. -/
noncomputable def ip (u u' : Fin 6 → ℝ) : ℂ := ∑ j, e (u j - u' j)

/-- Orthogonality of two (unbiased-to-the-coordinate-basis) vectors, on phase points. -/
def Ortho (u u' : Fin 6 → ℝ) : Prop := ip u u' = 0

/-- Unbiasedness of two such vectors, on phase points. -/
def Unbiased (u u' : Fin 6 → ℝ) : Prop := ‖ip u u'‖ = Real.sqrt 6

/-- Squared Euclidean norm on `ℝ^6`.  (Mathlib's `‖·‖` on a function type is the sup norm, so
the ℓ² quantity is written out.) -/
def sq (z : Fin 6 → ℝ) : ℝ := ∑ j, z j ^ 2

lemma sq_nonneg' (z : Fin 6 → ℝ) : 0 ≤ sq z :=
  Finset.sum_nonneg (fun j _ => sq_nonneg (z j))

lemma sq_sub_le (a b : Fin 6 → ℝ) : sq (fun j => a j - b j) ≤ 2 * (sq a + sq b) := by
  have h : ∀ j : Fin 6, (a j - b j) ^ 2 ≤ 2 * (a j ^ 2 + b j ^ 2) := by
    intro j
    nlinarith [sq_nonneg (a j + b j)]
  calc sq (fun j => a j - b j) = ∑ j, (a j - b j) ^ 2 := rfl
    _ ≤ ∑ j, 2 * (a j ^ 2 + b j ^ 2) := Finset.sum_le_sum (fun j _ => h j)
    _ = 2 * (sq a + sq b) := by
        rw [← Finset.mul_sum, Finset.sum_add_distrib]
        rfl

/-- Cauchy–Schwarz in the form used by the paper. -/
lemma sum_abs_le (z : Fin 6 → ℝ) : ∑ j, |z j| ≤ Real.sqrt 6 * Real.sqrt (sq z) := by
  have h := Finset.sum_mul_sq_le_sq_mul_sq (s := Finset.univ)
    (f := fun _ : Fin 6 => (1 : ℝ)) (g := fun j : Fin 6 => |z j|)
  simp only [one_mul, one_pow, sq_abs, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
    nsmul_eq_mul] at h
  have h' : Real.sqrt ((∑ j, |z j|) ^ 2) ≤ Real.sqrt (6 * sq z) :=
    Real.sqrt_le_sqrt (by simpa [sq] using h)
  rw [Real.sqrt_sq (Finset.sum_nonneg (fun j _ => abs_nonneg (z j))),
    Real.sqrt_mul (by norm_num : (0:ℝ) ≤ 6)] at h'
  exact h'

/-- The numeric core of Lemma 6.5: if the mean-zero displacement between two phase points has
squared norm at most `(1/5)^2` (i.e. `‖z‖ ≤ 2s` with `s < .1`), the unscaled inner product sum
has modulus strictly larger than `√6`. -/
theorem ip_norm_gt (z : Fin 6 → ℝ) (hz : sq z ≤ (1 / 5) ^ 2) :
    Real.sqrt 6 < ‖ip z 0‖ := by
  have hstep : ∀ j : Fin 6, ‖e (z j) - 1‖ ≤ 2 * Real.pi * |z j| := by
    intro j
    have h := Real.norm_exp_I_mul_ofReal_sub_one_le (x := 2 * Real.pi * z j)
    have harg : e (z j) = Complex.exp (Complex.I * ((2 * Real.pi * z j : ℝ) : ℂ)) := by
      simp only [e]
      congr 1
      push_cast
      ring
    have hnorm : ‖2 * Real.pi * z j‖ = 2 * Real.pi * |z j| := by
      rw [Real.norm_eq_abs, abs_mul, abs_of_pos (by positivity : (0:ℝ) < 2 * Real.pi)]
    rw [harg]
    exact h.trans (le_of_eq hnorm)
  have hsum : ‖ip z 0‖ ≥ 6 - 2 * Real.pi * (∑ j, |z j|) := by
    have hrew : ip z 0 = (6 : ℂ) + ∑ j, (e (z j) - 1) := by
      have hone : (∑ j : Fin 6, e (z j)) = ∑ j, ((1 : ℂ) + (e (z j) - 1)) := by
        apply Finset.sum_congr rfl
        intro j _
        ring
      simp only [ip, Pi.zero_apply, sub_zero]
      rw [hone, Finset.sum_add_distrib]
      try simp
    have h1 : ‖(6 : ℂ) + ∑ j, (e (z j) - 1)‖ ≥ 6 - ‖∑ j, (e (z j) - 1)‖ := by
      set S := ∑ j, (e (z j) - 1) with hS
      have h := norm_sub_norm_le (6 : ℂ) (-S)
      have h2 : ((6 : ℂ) - -S) = 6 + S := by ring
      rw [h2] at h
      simpa using h
    have h2 : ‖∑ j, (e (z j) - 1)‖ ≤ ∑ j, ‖e (z j) - 1‖ := norm_sum_le _ _
    have h3 : ∑ j, ‖e (z j) - 1‖ ≤ 2 * Real.pi * ∑ j, |z j| := by
      rw [Finset.mul_sum]
      exact Finset.sum_le_sum (fun j _ => hstep j)
    rw [hrew]
    linarith
  have hz' : ∑ j, |z j| ≤ Real.sqrt 6 / 5 := by
    have h := sum_abs_le z
    have hsq : Real.sqrt (sq z) ≤ 1 / 5 := by
      calc Real.sqrt (sq z) ≤ Real.sqrt ((1 / 5) ^ 2) := Real.sqrt_le_sqrt hz
        _ = 1 / 5 := by
            rw [Real.sqrt_sq (by norm_num)]
    nlinarith [Real.sqrt_nonneg 6]
  have hmain : Real.sqrt 6 < 6 - 2 * Real.pi * (Real.sqrt 6 / 5) := by
    have hp : Real.pi < 3.15 := Real.pi_lt_d2
    have hs : Real.sqrt 6 < 5 / 2 := by
      rw [Real.sqrt_lt' (by norm_num)]
      norm_num
    nlinarith [Real.pi_pos, Real.sqrt_nonneg 6]
  have hfin : 2 * Real.pi * (∑ j, |z j|) ≤ 2 * Real.pi * (Real.sqrt 6 / 5) := by
    have := Real.pi_pos
    nlinarith [Finset.sum_nonneg (fun j (_ : j ∈ Finset.univ) => abs_nonneg (z j))]
  linarith

/-! ## 2. Lemma 6.5 (distinct labels) -/

/-- Membership in the closed vector ball `Bvec v s` of (6.14), up to global phase and integer
phase lifts: `u = v + x + θ·1 + m` with `∑ x = 0`, `‖x‖ ≤ s`, `θ` a global phase and `m ∈ ℤ^6`. -/
def InBall (v : Fin 6 → ℝ) (s : ℝ) (u : Fin 6 → ℝ) : Prop :=
  ∃ x : Fin 6 → ℝ, (∑ j, x j = 0) ∧ sq x ≤ s ^ 2 ∧
    ∃ θ : ℝ, ∃ m : Fin 6 → ℤ, ∀ j, u j = v j + x j + θ + (m j : ℝ)

/-- **Lemma 6.5 (Distinct labels).**  Two vectors in one ball `Bvec v s` with `s < .1` are neither
orthogonal nor mutually unbiased. -/
theorem distinct_labels {v : Fin 6 → ℝ} {s : ℝ} (hs0 : 0 ≤ s) (hs : s < 1 / 10)
    {u u' : Fin 6 → ℝ}
    (hu : InBall v s u) (hu' : InBall v s u') : ¬ Ortho u u' ∧ ¬ Unbiased u u' := by
  obtain ⟨x, hx0, hxs, θ, m, hm⟩ := hu
  obtain ⟨x', hx0', hxs', θ', m', hm'⟩ := hu'
  -- the displacement `u - u'` splits as a small mean-zero part plus a global phase and integers
  have hterm : ∀ j : Fin 6, e (u j - u' j) = e (θ - θ') * e (x j - x' j) := by
    intro j
    have hsplit : u j - u' j = (θ - θ') + (x j - x' j) + ((m j - m' j : ℤ) : ℝ) := by
      have h1 := hm j
      have h2 := hm' j
      push_cast
      linarith
    rw [hsplit, e_add, e_add, e_int, mul_one]
  have hfac : ip u u' = e (θ - θ') * ip x x' := by
    simp only [ip, hterm, ← Finset.mul_sum]
  have hnorm : ‖ip u u'‖ = ‖ip x x'‖ := by
    rw [hfac, norm_mul, norm_e, one_mul]
  have hsq : sq (fun j => x j - x' j) ≤ (1 / 5) ^ 2 := by
    have h1 : sq (fun j => x j - x' j) ≤ 2 * (sq x + sq x') := sq_sub_le x x'
    have hs2 : s ^ 2 ≤ (1 / 10) ^ 2 := by nlinarith
    nlinarith [hxs, hxs']
  have hbig : Real.sqrt 6 < ‖ip (fun j => x j - x' j) (fun _ => 0)‖ := ip_norm_gt _ hsq
  simp only [ip, sub_zero] at hbig
  have hbig' : Real.sqrt 6 < ‖ip x x'‖ := hbig
  constructor
  · intro h
    have : ‖ip u u'‖ = 0 := by rw [h]; simp
    rw [hnorm] at this
    have := Real.sqrt_pos.2 (by norm_num : (0:ℝ) < 6)
    linarith
  · intro h
    have h' : ‖ip u u'‖ = Real.sqrt 6 := h
    rw [hnorm] at h'
    linarith

/-! ## 3. Lemma 6.1 (bin displacement bounds), stated -/

/-- **Lemma 6.1 (Bin displacement bounds).**  For a phase bin of resolution `M` with halfwidth
`a = 1/(2M)`, the centred displacement `x` of `d ∈ [-a,a]^5` (with `d 0 = 0`) satisfies
`∑ x = 0`, `‖x‖ ≤ √(29/6) a`, `‖x‖₁ ≤ 5a`, `‖x‖_∞ ≤ 3a/2`.

Stated only: the proof is a convexity/vertex argument in five real variables, which we did not
mechanise in this window (status: stated). -/
theorem bin_displacement (M : ℕ) (hM : 0 < M) (d : Fin 6 → ℝ)
    (hd0 : d 0 = 0) (hdb : ∀ j, |d j| ≤ 1 / (2 * M))
    (x : Fin 6 → ℝ) (hx : ∀ j, x j = d j - (∑ i, d i) / 6) :
    (∑ j, x j = 0) ∧ sq x ≤ (29 / 6) * (1 / (2 * M)) ^ 2 ∧
      (∑ j, |x j|) ≤ 5 * (1 / (2 * M)) ∧ ∀ j, |x j| ≤ 3 / 2 * (1 / (2 * M)) := by
  sorry

/-! ## 4. The `ℓ²` triangle inequality, and Lemma 6.4 (certified clustering) -/

/-- Cauchy–Schwarz, cross-term form, for `ℝ^6`. -/
lemma cross_le (a b : Fin 6 → ℝ) :
    (∑ j, a j * b j) ≤ Real.sqrt (sq a) * Real.sqrt (sq b) := by
  have hcs : (∑ j, a j * b j) ^ 2 ≤ sq a * sq b := by
    have h := Finset.sum_mul_sq_le_sq_mul_sq (s := Finset.univ) (f := a) (g := b)
    simpa [sq] using h
  have h2 : |∑ j, a j * b j| ≤ Real.sqrt (sq a * sq b) := by
    rw [← Real.sqrt_sq_eq_abs]
    exact Real.sqrt_le_sqrt hcs
  rw [Real.sqrt_mul (sq_nonneg' a)] at h2
  linarith [le_abs_self (∑ j, a j * b j)]

lemma sq_add_le (a b : Fin 6 → ℝ) :
    sq (fun j => a j + b j) ≤ (Real.sqrt (sq a) + Real.sqrt (sq b)) ^ 2 := by
  have hexp : sq (fun j => a j + b j) = sq a + 2 * (∑ j, a j * b j) + sq b := by
    have hterm : ∀ j : Fin 6, (a j + b j) ^ 2 = a j ^ 2 + 2 * (a j * b j) + b j ^ 2 := by
      intro j; ring
    simp only [sq, hterm, Finset.sum_add_distrib, ← Finset.mul_sum]
    try ring
  rw [hexp]
  have hsa : (Real.sqrt (sq a)) ^ 2 = sq a := Real.sq_sqrt (sq_nonneg' a)
  have hsb : (Real.sqrt (sq b)) ^ 2 = sq b := Real.sq_sqrt (sq_nonneg' b)
  nlinarith [cross_le a b, Real.sqrt_nonneg (sq a), Real.sqrt_nonneg (sq b)]

/-- **Lemma 6.4 (Certified clustering).**  Suppose a bin with midpoint `u` has been assigned to
the centre `v`, the integer lift `m` and the radius `s`, the centred wrap `h` of `u - v - m`
satisfies `∑ h = 0`, and the assigned radius is at least `‖h‖ + X` (the paper's rule
`radius ≥ ‖h‖ + X_M`).  Then every vector of the bin (phase displacement `x` with `∑ x = 0`,
`‖x‖ ≤ X`) lies in `Bvec v s` up to global phase.

The two code-dependent hypotheses are `hdef` (the integer wrap is a coordinatewise wrap of
`u - v`) and `hrad` (the final radius recomputation is an outward upper bound); they are exactly
what the routine's final radius update guarantees. -/
theorem certified_clustering {v : Fin 6 → ℝ} {s X : ℝ} (hX0 : 0 ≤ X)
    {u : Fin 6 → ℝ} {m : Fin 6 → ℤ} {h : Fin 6 → ℝ}
    (hmean : ∑ j, h j = 0) (hdef : ∀ j, u j - v j = h j + (m j : ℝ))
    (hrad : (Real.sqrt (sq h) + X) ^ 2 ≤ s ^ 2)
    {x : Fin 6 → ℝ} (hx : ∑ j, x j = 0) (hxX : sq x ≤ X ^ 2) :
    InBall v s (fun j => u j + x j) := by
  refine ⟨fun j => h j + x j, ?_, ?_, 0, m, ?_⟩
  · rw [Finset.sum_add_distrib, hmean, hx, add_zero]
  · calc sq (fun j => h j + x j) ≤ (Real.sqrt (sq h) + Real.sqrt (sq x)) ^ 2 := sq_add_le h x
      _ ≤ (Real.sqrt (sq h) + X) ^ 2 := by
          have h1 : Real.sqrt (sq x) ≤ X := by
            calc Real.sqrt (sq x) ≤ Real.sqrt (X ^ 2) := Real.sqrt_le_sqrt hxX
              _ = X := Real.sqrt_sq hX0
          have hsum : Real.sqrt (sq h) + Real.sqrt (sq x) ≤ Real.sqrt (sq h) + X := by
            linarith [Real.sqrt_nonneg (sq h)]
          have hnn : 0 ≤ Real.sqrt (sq h) + Real.sqrt (sq x) := by
            linarith [Real.sqrt_nonneg (sq h), Real.sqrt_nonneg (sq x)]
          exact pow_le_pow_left₀ hnn hsum 2
      _ ≤ s ^ 2 := hrad
  · intro j
    have h1 := hdef j
    show u j + x j = v j + (h j + x j) + 0 + (m j : ℝ)
    linarith

/-! ## 5. The graph on retained labels and the forbidden configuration -/

/-- The graph on retained ball labels: `O` = orthogonality edge retained, `U` = unbiasedness
edge retained.  An edge is *retained* unless the necessary tests of Lemmas 6.6 and 6.7 excluded
the pair, so the graphs are permissive supersets of the realised relations. -/
structure Graph (V : Type*) where
  O : V → V → Prop
  U : V → V → Prop

/-- The forbidden configuration (6.24): two disjoint six-element sets, each an `O`-clique, with
all thirty-six cross pairs `U`-adjacent. -/
def Config {V : Type*} (G : Graph V) : Prop :=
  ∃ A B : Finset V, A.card = 6 ∧ B.card = 6 ∧ Disjoint A B ∧
    (∀ a ∈ A, ∀ a' ∈ A, a ≠ a' → G.O a a') ∧
    (∀ b ∈ B, ∀ b' ∈ B, b ≠ b' → G.O b b') ∧
    (∀ a ∈ A, ∀ b ∈ B, G.U a b)

/-! ## 6. Proposition 6.9 (local exclusion certificate) -/

/-- **Proposition 6.9 (Local exclusion certificate).**  Suppose

* every admissible vector (unbiased to the coordinate basis and to the given Hadamard basis) lies
  in its labelled closed vector ball of radius `< .1` (`hlab`; Lemma 6.4 supplies this from a
  successful clustering, the covering property being independent of the heuristic);
* `O`/`U` edges are retained for every orthogonal/unbiased pair (`hO`, `hU`; Lemmas 6.6 and 6.7);
* the finite graph search returned a negative result, i.e. `G` contains no configuration (6.24)
  (`hgraph`; Lemma 6.8, a specification claim about `graph::exist`, hence a binder).

Then two further mutually unbiased orthonormal bases, both unbiased to the coordinate basis and
to the second basis, do not exist. -/
theorem prop_6_9 {V : Type*} (G : Graph V) (v : V → Fin 6 → ℝ) (s : V → ℝ)
    (hs0 : ∀ b, 0 ≤ s b) (hs : ∀ b, s b < 1 / 10)
    (lab : (Fin 6 → ℝ) → V) (hlab : ∀ u, InBall (v (lab u)) (s (lab u)) u)
    (hgraph : ¬ Config G)
    (hO : ∀ u u', Ortho u u' → G.O (lab u) (lab u'))
    (hU : ∀ u u', Unbiased u u' → G.U (lab u) (lab u'))
    (u0 u1 : Fin 6 → Fin 6 → ℝ)
    (hortho0 : ∀ i j, i ≠ j → Ortho (u0 i) (u0 j))
    (hortho1 : ∀ i j, i ≠ j → Ortho (u1 i) (u1 j))
    (hunb : ∀ i j, Unbiased (u0 i) (u1 j)) :
    False := by
  classical
  let f0 : Fin 6 → V := fun i => lab (u0 i)
  let f1 : Fin 6 → V := fun i => lab (u1 i)
  have h0 : ∀ i, InBall (v (f0 i)) (s (f0 i)) (u0 i) := fun i => hlab _
  have h1 : ∀ i, InBall (v (f1 i)) (s (f1 i)) (u1 i) := fun i => hlab _
  have hinj0 : Function.Injective f0 := by
    intro i j hij
    by_contra hne
    have h2 : InBall (v (f0 i)) (s (f0 i)) (u0 j) := by
      rw [hij]
      exact h0 j
    exact (distinct_labels (hs0 _) (hs _) (h0 i) h2).1 (hortho0 i j hne)
  have hinj1 : Function.Injective f1 := by
    intro i j hij
    by_contra hne
    have h2 : InBall (v (f1 i)) (s (f1 i)) (u1 j) := by
      rw [hij]
      exact h1 j
    exact (distinct_labels (hs0 _) (hs _) (h1 i) h2).1 (hortho1 i j hne)
  refine hgraph ⟨Finset.univ.image f0, Finset.univ.image f1, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · rw [Finset.card_image_of_injective _ hinj0, Finset.card_univ, Fintype.card_fin]
  · rw [Finset.card_image_of_injective _ hinj1, Finset.card_univ, Fintype.card_fin]
  · rw [Finset.disjoint_left]
    intro b hb hb'
    simp only [Finset.mem_image, Finset.mem_univ, true_and] at hb hb'
    obtain ⟨i, rfl⟩ := hb
    obtain ⟨j, hj⟩ := hb'
    have h2 : InBall (v (f0 i)) (s (f0 i)) (u1 j) := by
      rw [← hj]
      exact h1 j
    exact (distinct_labels (hs0 _) (hs _) (h0 i) h2).2 (hunb i j)
  · intro a ha a' ha' hne
    simp only [Finset.mem_image, Finset.mem_univ, true_and] at ha ha'
    obtain ⟨i, rfl⟩ := ha
    obtain ⟨j, rfl⟩ := ha'
    exact hO _ _ (hortho0 i j (fun h => hne (by rw [h])))
  · intro b hb b' hb' hne
    simp only [Finset.mem_image, Finset.mem_univ, true_and] at hb hb'
    obtain ⟨i, rfl⟩ := hb
    obtain ⟨j, rfl⟩ := hb'
    exact hO _ _ (hortho1 i j (fun h => hne (by rw [h])))
  · intro a ha b hb
    simp only [Finset.mem_image, Finset.mem_univ, true_and] at ha hb
    obtain ⟨i, rfl⟩ := ha
    obtain ⟨j, rfl⟩ := hb
    exact hU _ _ (hunb i j)

end StageC
end Mub6
