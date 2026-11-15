/-
Mub6/Ellipsoid.lean — §4: ellipsoid containment and the offset ellipsoid bound.

Paper locators: Lemma 4.11 ("Ellipsoid containment") and Lemma 4.12 ("Offset ellipsoid norm
bound", (4.34)), together with the uses (4.31)–(4.33), (4.35)–(4.36).

Rendering of `{G^{1/2} w : ‖w‖ ≤ 1}`.  The pin has no matrix square root (no `PosSemidef.sqrt`,
no continuous functional calculus for matrices — see reports/DEPGRAPH.md), so the ellipsoid is
carried in the *support-function form* that the paper itself proves equivalent in the last
paragraph of Lemma 4.11: `x` lies in the ellipsoid of `G` iff `(z·x)^2 ≤ z^*Gz` for every real test
vector `z`.  This is a definitional choice, not a weakening of the inequality that is proved: the
paper's proof of 4.11 consists exactly in establishing that support bound.  The equivalence with
`{G^{1/2} w}` is *not* formalised here and is recorded as an open bridge in reports/status.md.
-/
import Mub6.Basic

noncomputable section

namespace Mub6

open Matrix
open scoped Matrix BigOperators

/-! ### The ellipsoid, in the support-function form used by the paper's proof -/

/-- `x` belongs to the ellipsoid of `G` (support-function form): for every real test vector `z`,
`(z·x)^2 ≤ z ⬝ᵥ (G *ᵥ z)`.  For `G ⪰ 0` this is the paper's `{G^{1/2}w : ‖w‖ ≤ 1}`. -/
def InEllipsoid {k : ℕ} (G : Matrix (Fin k) (Fin k) ℝ) (x : Fin k → ℝ) : Prop :=
  ∀ z : Fin k → ℝ, (z ⬝ᵥ x) ^ 2 ≤ z ⬝ᵥ (G *ᵥ z)

/-! ### Lemma 4.11 — ellipsoid containment -/

/-- **Lemma 4.11 (ellipsoid containment).**  For real linear maps `A`, `B`, vectors `‖s‖ ≤ r`,
`‖v‖ ≤ q` and `β > 0`, the sum `A s + B v` belongs to the ellipsoid of `G` whenever

`G ⪰ (1+β) r^2 A A^* + (1 + 1/β) q^2 B B^*`.

The Loewner order is rendered pointwise, `(1+β)r²‖A^*z‖² + (1+1/β)q²‖B^*z‖² ≤ z^*Gz` for every
`z`, which is what the paper's support-function proof uses (and is equivalent to the Loewner
inequality when the difference is symmetric).  `‖s‖² = ∑ s_i²` and `‖v‖² = ∑ v_i²` are the
squared Euclidean norms, matching `‖·‖` in the paper.

The proof (paper): `z·(As+Bv) ≤ r‖A^*z‖ + q‖B^*z‖ ≤ ((1+β)r²‖A^*z‖² + (1+1/β)q²‖B^*z‖²)^{1/2}`,
the last step by completing a square.  Not formalised in this window; the two remaining goals are
`Real.sqrt` bookkeeping and the scalar AM–GM step (see reports/status.md). -/
theorem ellipsoid_containment {k m n : ℕ}
    (A : Matrix (Fin k) (Fin m) ℝ) (B : Matrix (Fin k) (Fin n) ℝ)
    (G : Matrix (Fin k) (Fin k) ℝ) {r q β : ℝ}
    (hβ : 0 < β) (hr : 0 ≤ r) (hq : 0 ≤ q)
    (hG : ∀ z : Fin k → ℝ,
      (1 + β) * r ^ 2 * (∑ i, (Aᵀ *ᵥ z) i ^ 2) + (1 + 1 / β) * q ^ 2 * (∑ i, (Bᵀ *ᵥ z) i ^ 2)
        ≤ z ⬝ᵥ (G *ᵥ z))
    {s : Fin m → ℝ} {v : Fin n → ℝ}
    (hs : ∑ i, s i ^ 2 ≤ r ^ 2) (hv : ∑ i, v i ^ 2 ≤ q ^ 2) :
    InEllipsoid G (A *ᵥ s + B *ᵥ v) := by
  sorry

/-- The scalar step of Lemma 4.11: `(r u + q v)^2 ≤ (1+β) r^2 u^2 + (1 + 1/β) q^2 v^2` for
`u, v, r, q ≥ 0` and `β > 0` ("the scalar inequality follows by completing a square"). -/
theorem sq_add_mul_le {r q u v β : ℝ} (hr : 0 ≤ r) (hq : 0 ≤ q) (hu : 0 ≤ u) (hv : 0 ≤ v)
    (hβ : 0 < β) :
    (r * u + q * v) ^ 2 ≤ (1 + β) * r ^ 2 * u ^ 2 + (1 + 1 / β) * q ^ 2 * v ^ 2 := by
  sorry

/-! ### The `λ_max` half of Lemma 4.12, in support form

The paper's simpler bound is `‖U + G^{1/2}w‖ ≤ ‖U‖ + √λ_max(G)`.  What that needs is that a point
of the ellipsoid has norm at most `√λ_max(G)`; here `λ_max(G)` is replaced by an explicit `Λ` with
`z^*Gz ≤ Λ‖z‖²` for all `z` — the paper's own convention elsewhere (`E(G;{U_σ})` is *any* certified
upper bound), and it avoids introducing eigenvalues of `G`.  This one is Lean-checked. -/
theorem normSq_le_of_inEllipsoid {k : ℕ} {G : Matrix (Fin k) (Fin k) ℝ} {y : Fin k → ℝ} {Λ : ℝ}
    (h : InEllipsoid G y) (hΛ : ∀ z : Fin k → ℝ, z ⬝ᵥ (G *ᵥ z) ≤ Λ * (z ⬝ᵥ z)) (hΛ0 : 0 ≤ Λ) :
    ∑ i, y i ^ 2 ≤ Λ := by
  have h1 : (y ⬝ᵥ y) ^ 2 ≤ Λ * (y ⬝ᵥ y) := by
    calc (y ⬝ᵥ y) ^ 2 ≤ y ⬝ᵥ (G *ᵥ y) := h y
      _ ≤ Λ * (y ⬝ᵥ y) := hΛ y
  have h2 : 0 ≤ y ⬝ᵥ y := by
    rw [dotProduct]
    exact Finset.sum_nonneg fun i _ => mul_self_nonneg _
  have hs : y ⬝ᵥ y ≤ Λ := by
    rcases eq_or_lt_of_le h2 with h0 | hpos
    · rw [← h0]; exact hΛ0
    · nlinarith [h1, hpos]
  rw [dotProduct] at hs
  simpa [sq] using hs

/-! ### Lemma 4.12 — offset ellipsoid norm bound (4.34)

The paper writes `‖U + G^{1/2}w‖² ≤ γ(1 + U^*(γI-G)^{-1}U)`.  Because the pin has no matrix
square root, the square root is carried as an explicit `R` with `R*R = G` (such an `R` exists for
`G ⪰ 0` by the spectral theorem; that existence is not formalised), and the inverse `(γI-G)^{-1}U`
is carried as a vector `p` with `(γI-G)p = U`.  The commutation `R(γI-G) = (γI-G)R` follows from
`R*R = G` and symmetry of `R`; it is taken as an explicit hypothesis to avoid matrix-algebra
plumbing in this window.  `γ > λ_max(G)` is rendered as `(γI-G) ⪰ 0` plus the existence of `p`. -/
theorem offset_ellipsoid_bound {k : ℕ}
    (G R : Matrix (Fin k) (Fin k) ℝ) (U w p : Fin k → ℝ) {γ : ℝ}
    (hRsq : R * R = G)
    (hcomm : (γ • (1 : Matrix (Fin k) (Fin k) ℝ) - G) * R = R * (γ • (1 : Matrix (Fin k) (Fin k) ℝ) - G))
    (hp : (γ • (1 : Matrix (Fin k) (Fin k) ℝ) - G) *ᵥ p = U)
    (hpsd : ∀ u : Fin k → ℝ, 0 ≤ u ⬝ᵥ ((γ • (1 : Matrix (Fin k) (Fin k) ℝ) - G) *ᵥ u))
    (hγ : 0 ≤ γ) (hw : ∑ i, w i ^ 2 ≤ 1) :
    ∑ i, (U i + (R *ᵥ w) i) ^ 2 ≤ γ * (1 + U ⬝ᵥ p) := by
  sorry

/-- **Lemma 4.12, last sentence.**  If the offsets range over the convex hull of finitely many
`U_σ`, it suffices to take the largest of the bounds at those offsets: `U ↦ ‖U + y‖` is convex, so
its maximum over a polytope is attained at a vertex.  (Convexity of the bound, stated only.) -/
theorem offset_hull_bound {k : ℕ} {n : ℕ} (y : Fin k → ℝ) (U : Fin n → Fin k → ℝ)
    (t : Fin n → ℝ) {E : ℝ}
    (ht : ∀ σ, 0 ≤ t σ) (ht1 : ∑ σ, t σ = 1) (hE : 0 ≤ E)
    (h : ∀ σ, Real.sqrt (∑ i, (U σ i + y i) ^ 2) ≤ E) :
    Real.sqrt (∑ i, (∑ σ, t σ * U σ i + y i) ^ 2) ≤ E := by
  sorry

end Mub6
