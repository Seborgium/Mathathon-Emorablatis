/-
  H2-ROOT, Lean fragment: the *consumer* obligations of a Root certificate.

  The analytic content of Definition 4.1 / Proposition 4.5 (that the stored constants imply
  (4.5)-(4.7) for every horizontal exact-solution displacement) is NOT formalised here.  What is
  formalised is what every consumer actually uses them for:

  * `root_radius_step` is Proposition 4.13's improvement formula (4.38): an upper bound `s` for the
    displacement, a tangent bound `t ≥ ||T^* δ||` and the normal bound (4.5) at `s` produce the
    smaller upper bound `sqrt (nP s ^ 2 + (1 + ort) t ^ 2)`.  Atlas coverage and Stage-B bootstrapping
    both rely on exactly this one-step implication, monotonicity of `n_P` included.
  * `absurd_if_radius_lt` is the strict-inequality form a checker emits (it is the shape an
    exclusion test takes: the ball radius is below the cell's target, strictly).

  No analysis, no floating point: pure ordered-field arithmetic in `ℝ`.
-/
import Mathlib

namespace Mub6.Root

/-- `n_P(s) = n0 + id*s + C*s^2` is nondecreasing on `[0, ∞)` when the coefficients are
nonnegative.  (4.3) plus the nonnegativity hypothesis of Definition 4.1. -/
theorem normal_bound_mono {n0 id C : ℝ} (_hn0 : 0 ≤ n0) (hid : 0 ≤ id) (hC : 0 ≤ C)
    {s s0 : ℝ} (hs : 0 ≤ s) (hs0 : s ≤ s0) :
    n0 + id * s + C * s ^ 2 ≤ n0 + id * s0 + C * s0 ^ 2 := by
  have hs0' : 0 ≤ s0 := le_trans hs hs0
  have h1 : id * s ≤ id * s0 := by nlinarith
  have h2 : s ^ 2 ≤ s0 ^ 2 := by nlinarith
  have h3 : C * s ^ 2 ≤ C * s0 ^ 2 := by nlinarith
  linarith

/-- Proposition 4.13 / (4.38), one step, with the (4.5) normal bound as hypothesis. -/
theorem root_radius_step {s t n n0 id C ort s0 : ℝ}
    (hn0 : 0 ≤ n0) (hid : 0 ≤ id) (hC : 0 ≤ C) (_hort : 0 ≤ ort)
    (hs : 0 ≤ s) (hn : 0 ≤ n) (hss : s ≤ s0)
    -- (4.5) at this `s`: the normal displacement is bounded by `n_P s`
    (hnormal : n ≤ n0 + id * s + C * s ^ 2)
    -- (4.6): the squared norm splits into tangent and normal parts
    (hsplit : s ^ 2 ≤ (1 + ort) * t ^ 2 + n ^ 2) :
    s ≤ Real.sqrt ((n0 + id * s0 + C * s0 ^ 2) ^ 2 + (1 + ort) * t ^ 2) := by
  have hpoly : n ≤ n0 + id * s0 + C * s0 ^ 2 :=
    le_trans hnormal (normal_bound_mono hn0 hid hC hs hss)
  have h1 : n ^ 2 ≤ (n0 + id * s0 + C * s0 ^ 2) ^ 2 := by nlinarith
  have hsq : s ^ 2 ≤ (n0 + id * s0 + C * s0 ^ 2) ^ 2 + (1 + ort) * t ^ 2 := by linarith
  calc s = Real.sqrt (s ^ 2) := (Real.sqrt_sq hs).symm
    _ ≤ Real.sqrt ((n0 + id * s0 + C * s0 ^ 2) ^ 2 + (1 + ort) * t ^ 2) :=
        Real.sqrt_le_sqrt hsq

/-- The exclusion shape a checker emits: a strict margin against the target radius. -/
theorem radius_below_target {r target : ℝ} (h : r < target) : ¬ (target ≤ r) := by linarith

end Mub6.Root
