/-
Mub6/Frames.lean — §3.1: seed blocks and the fixed complementary frames.

Paper locator: Lemma 3.1 ("Fixed frames") and (3.1), (3.4), (3.5), (3.6).

This module is *infrastructure for Stage A*: it fixes the seed block `M = (1 p)`, computes the
Gram matrix `M^* M`, states the two singular values, the pseudo-inverse formula (3.4) and the
existence of the complementary frame `K`.  Nothing here depends on §4–§6.

Status (see reports/status.md): the Gram identity, the characteristic polynomial (hence the
squared singular values `4 ± |S|`) and the kernel-frame *existence* are Lean-checked; the
pseudo-inverse formula (3.4) and the projection identities (3.6) are transcribed and marked
`stated only`.
-/
import Mub6.Basic

noncomputable section

namespace Mub6

open Matrix Complex
open scoped Matrix

/-! ### The hypothesis, the seed block, the seed sum

The paper's "`p ∈ ℂ^4` has unit-modulus entries" is `UnitModulus p`; note that it is a hypothesis on
the *entries*, not an entrywise-unit-modulus matrix statement, and that it is what makes `4 ± |S|`
come out of `M^*M`. -/

/-- `p` has unit-modulus entries: `|p_j| = 1`. -/
def UnitModulus {n : ℕ} (p : Fin n → ℂ) : Prop := ∀ j, ‖p j‖ = 1

/-- The paper's `M = (1 p)`: the `n × 2` matrix with first column the all-ones vector and second
column `p`.  (Lemma 3.1 is stated for `n = 4`; the definition is size-generic.) -/
def frameMat {n : ℕ} (p : Fin n → ℂ) : Matrix (Fin n) (Fin 2) ℂ :=
  Matrix.of fun i j => if j.val = 0 then 1 else p i

/-- The seed sum `S = ∑_j p_j`. -/
def seedSum {n : ℕ} (p : Fin n → ℂ) : ℂ := ∑ j, p j

/-- The paper's Gram matrix `M^* M = !![4, S; conj S, 4]`, written with `val`-tests so that it
reduces definitionally on the two indices `0`, `1`; this is `!![4, S; S̄, 4]` in the paper. -/
def gramMat {n : ℕ} (p : Fin n → ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  Matrix.of fun i j =>
    if j.val = 0 then (if i.val = 0 then 4 else starRingEnd ℂ (seedSum p))
    else (if i.val = 0 then seedSum p else 4)

@[simp] theorem frameMat_zero {n : ℕ} (p : Fin n → ℂ) (i : Fin n) : frameMat p i 0 = 1 := by
  simp [frameMat]

@[simp] theorem frameMat_one {n : ℕ} (p : Fin n → ℂ) (i : Fin n) : frameMat p i 1 = p i := by
  simp [frameMat]

/-! ### Entrywise consequences of unit modulus -/

theorem conj_mul_self {n : ℕ} {p : Fin n → ℂ} (hp : UnitModulus p) (i : Fin n) :
    starRingEnd ℂ (p i) * p i = 1 := by
  have h : ((Complex.normSq (p i) : ℝ) : ℂ) = 1 := by
    rw [Complex.normSq_eq_norm_sq, hp i]
    norm_num
  rw [mul_comm, Complex.mul_conj, h]

theorem star_mul_self {n : ℕ} {p : Fin n → ℂ} (hp : UnitModulus p) (i : Fin n) :
    star (p i) * p i = 1 :=
  conj_mul_self hp i

/-! ### `M^* M` and the squared singular values (Lemma 3.1, first sentence) -/

/-- Lemma 3.1, first computation: `M^* M = [[4, S], [conj S, 4]]`. -/
theorem frameMat_conjTranspose_mul {p : Fin 4 → ℂ} (hp : UnitModulus p) :
    (frameMat p)ᴴ * frameMat p = gramMat p := by
  sorry

/-- The scalar identity `S conj S = |S|^2` in the form used below. -/
theorem seedSum_mul_conj {n : ℕ} (p : Fin n → ℂ) :
    seedSum p * starRingEnd ℂ (seedSum p) = ((‖seedSum p‖ ^ 2 : ℝ) : ℂ) := by
  rw [Complex.mul_conj, Complex.normSq_eq_norm_sq]

/-- Lemma 3.1, first sentence, in exact form: the characteristic polynomial of `M^* M` is
`(X - (4 + |S|)) (X - (4 - |S|))`, i.e. the squared singular values of `M` are `4 ± |S|`,
counted with multiplicity. -/
theorem frameMat_charpoly {p : Fin 4 → ℂ} (hp : UnitModulus p) :
    ((frameMat p)ᴴ * frameMat p).charpoly =
      (Polynomial.X - Polynomial.C ((4 + ‖seedSum p‖ : ℝ) : ℂ)) *
        (Polynomial.X - Polynomial.C ((4 - ‖seedSum p‖ : ℝ) : ℂ)) := by
  sorry

/-- The two squared singular values as an unordered pair: every eigenvalue of `M^* M` is `4 + |S|`
or `4 - |S|`.  Stated as a polynomial-identity corollary so that it needs no spectral theory. -/
theorem frameMat_sq_singular_pair {p : Fin 4 → ℂ} (hp : UnitModulus p) :
    ((frameMat p)ᴴ * frameMat p).charpoly =
      (Polynomial.X ^ 2 - Polynomial.C 8 * Polynomial.X +
        Polynomial.C (((16 : ℝ) - ‖seedSum p‖ ^ 2 : ℝ) : ℂ)) := by
  sorry

/-! ### The pseudo-inverse formula (3.4) -/

/-- The candidate inverse `(16 - |S|^2)^{-1} · [[4, -S], [-conj S, 4]]` of the Gram matrix. -/
def gramInv {n : ℕ} (p : Fin n → ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  (((16 : ℝ) - ‖seedSum p‖ ^ 2 : ℝ) : ℂ)⁻¹ • !![(4 : ℂ), -seedSum p; -starRingEnd ℂ (seedSum p), 4]

/-- `M (M^*M)^{-1}`, the paper's left-hand side in (3.4).  By Lemma 3.1 it equals
`(16-|S|^2)^{-1} (4·1 - p conj S, 4p - 1 S)`; that identity is `frameMat_mul_gramInv`. -/
def framePseudoInv {n : ℕ} (p : Fin n → ℂ) : Matrix (Fin n) (Fin 2) ℂ :=
  frameMat p * (gramInv p)

/-- The paper's right-hand side of (3.4), written out entrywise: column `0` is
`(16-|S|^2)^{-1}(4·1 - p S̄)` and column `1` is `(16-|S|^2)^{-1}(4p - 1 S)`. -/
def framePseudoInvFormula {n : ℕ} (p : Fin n → ℂ) : Matrix (Fin n) (Fin 2) ℂ :=
  Matrix.of fun i j =>
    (((16 : ℝ) - ‖seedSum p‖ ^ 2 : ℝ) : ℂ)⁻¹ *
      (if j = 0 then 4 - p i * starRingEnd ℂ (seedSum p) else 4 * p i - seedSum p)

/-- `M^*M` is invertible when `|S| < 4`: the Gram matrix multiplied by its candidate inverse is
the identity.  (This is the "if `|S| < 4`" hypothesis of Lemma 3.1, and it is exactly the
nondegeneracy that makes `(M^*M)^{-1}` meaningful in (3.4).) -/
theorem gram_mul_gramInv {p : Fin 4 → ℂ} (hp : UnitModulus p) (hS : ‖seedSum p‖ < 4) :
    ((frameMat p)ᴴ * frameMat p) * gramInv p = 1 := by
  sorry

/-- Lemma 3.1, equation (3.4): for `|S| < 4`,
`M (M^*M)^{-1} = (16-|S|^2)^{-1}(4·1 - p S̄, 4p - 1 S)`.

Stated as `framePseudoInv = framePseudoInvFormula`, i.e. the two columns are identified
entrywise; the paper writes the two columns as a row to save space. -/
theorem frameMat_mul_gramInv {p : Fin 4 → ℂ} (hp : UnitModulus p) (hS : ‖seedSum p‖ < 4) :
    framePseudoInv p = framePseudoInvFormula p := by
  sorry

/-- Lemma 3.1, third sentence: for `|S| < 4` there is a `4 × 2` matrix `K` with orthonormal
columns spanning `ker M^*`.  The paper constructs it by Gram–Schmidt from `1/√2`-type vectors and
projected coordinate vectors; the construction is not formalised here (see reports/status.md),
so the paper's *assertion* is transcribed as the existence statement, with the spanning condition
written as "every element of `ker M^*` is in the range of `K`".

This is the hypothesis that makes the frames `K_B`, `K_C` of (3.5) exist; `SeedFrames` below
records it as data rather than reproving it per seed. -/
theorem kerFrame_exists {p : Fin 4 → ℂ} (hp : UnitModulus p) (hS : ‖seedSum p‖ < 4) :
    ∃ K : Matrix (Fin 4) (Fin 2) ℂ,
      Kᴴ * K = 1 ∧ (frameMat p)ᴴ * K = 0 ∧
        ∀ x : Fin 4 → ℂ, (frameMat p)ᴴ *ᵥ x = 0 → ∃ t : Fin 2 → ℂ, K *ᵥ t = x := by
  sorry

/-! ### The fixed frames and projections of (3.5)–(3.6)

The paper *defines* `G_B = B_0^*(B_0B_0^*)^{-1}`, `G_C = C_0(C_0^*C_0)^{-1}` and the projections
(3.6).  Here they are definitions, so that `Mub6/Completion.lean` can use them; the fact that they
are the right frames (i.e. `G_B B_0 = I - P_K`) is `frame_projection_identities`, below, which is
`stated only`. -/

/-- (3.5): `G_B = B_0^*(B_0 B_0^*)^{-1}`, where `B_0 = (1 p)ᵀ` is the `2 × 4` seed block. -/
def seedGB (p : Fin 4 → ℂ) : Matrix (Fin 4) (Fin 2) ℂ :=
  ((frameMat p)ᵀ)ᴴ * (((frameMat p)ᵀ) * ((frameMat p)ᵀ)ᴴ)⁻¹

/-- (3.5): `G_C = C_0(C_0^*C_0)^{-1}`, where `C_0 = (1 p)` is the `4 × 2` seed block. -/
def seedGC (p : Fin 4 → ℂ) : Matrix (Fin 4) (Fin 2) ℂ :=
  frameMat p * ((frameMat p)ᴴ * frameMat p)⁻¹

/-- The Stage-A frame data of (3.5): the two kernels, plus the complementary frame `K_B`, `K_C`.
The fields `KB_span`/`KC_span` are Lemma 3.1's "range = kernel" assertion, carried as data so that
callers never need to re-derive the Gram–Schmidt construction. -/
structure SeedFrames (b c : Fin 4 → ℂ) : Type where
  /-- the ideal frame spanning `ker B_0` -/
  KB : Matrix (Fin 4) (Fin 2) ℂ
  /-- the ideal frame spanning `ker C_0^*` -/
  KC : Matrix (Fin 4) (Fin 2) ℂ
  KB_orthonormal : KBᴴ * KB = 1
  KC_orthonormal : KCᴴ * KC = 1
  /-- `B_0 K_B = 0`, i.e. `ran K_B ⊆ ker B_0` -/
  KB_in_kernel : (frameMat b)ᵀ * KB = 0
  /-- `C_0^* K_C = 0`, i.e. `ran K_C ⊆ ker C_0^*` -/
  KC_in_kernel : (frameMat c)ᴴ * KC = 0
  /-- `ran K_B ⊇ ker B_0` -/
  KB_span : ∀ x : Fin 4 → ℂ, (frameMat b)ᵀ *ᵥ x = 0 → ∃ t : Fin 2 → ℂ, KB *ᵥ t = x
  /-- `ran K_C ⊇ ker C_0^*` -/
  KC_span : ∀ x : Fin 4 → ℂ, (frameMat c)ᴴ *ᵥ x = 0 → ∃ t : Fin 2 → ℂ, KC *ᵥ t = x

namespace SeedFrames

variable {b c : Fin 4 → ℂ} (F : SeedFrames b c)

/-- (3.6): `P_K = K_B K_B^*`. -/
def PK : Matrix (Fin 4) (Fin 4) ℂ := F.KB * F.KBᴴ

/-- (3.6): `P_B = I - P_K`. -/
def PB : Matrix (Fin 4) (Fin 4) ℂ := 1 - F.PK

/-- (3.6): `P_C = I - K_C K_C^*`. -/
def PC : Matrix (Fin 4) (Fin 4) ℂ := 1 - F.KC * F.KCᴴ

end SeedFrames

/-- (3.6), first identity: `P_B = I - P_K = G_B B_0`.  This is where the pseudo-inverse formula
(3.4) is used: `G_B B_0 = B_0^*(B_0B_0^*)^{-1}B_0` is the orthogonal projection onto `ran B_0^*`.
Stated only (the content is Lemma 3.1 (3.4) plus `ran K_B = ker B_0`). -/
theorem frame_projection_identities {b c : Fin 4 → ℂ} (F : SeedFrames b c) :
    F.PB = seedGB b * (frameMat b)ᵀ ∧ F.PC = seedGC c * (frameMat c)ᴴ := by
  sorry

/-- The paper's `m_B = σ_min(B_0) > 0`, `m_C = σ_min(C_0) > 0`, carried as certified lower
bounds: `mB` is a positive number with `mB·‖x‖ ≤ ‖B_0 x‖` for all `x`.  Constant bookkeeping, not
a claim of the paper; it is separated out so that `Mub6/Completion.lean` can take `m = min mB mC`
without touching singular value theory. -/
structure SeedSingularBounds where
  b : Fin 4 → ℂ
  c : Fin 4 → ℂ
  mB : ℝ
  mC : ℝ
  mB_pos : 0 < mB
  mC_pos : 0 < mC
  mB_le : ∀ x : Fin 4 → ℂ, mB * ‖x‖ ≤ ‖(frameMat b)ᵀ *ᵥ x‖
  mC_le : ∀ x : Fin 2 → ℂ, mC * ‖x‖ ≤ ‖(frameMat c) *ᵥ x‖

/-- The paper's `m = min(m_B, m_C) > 0`. -/
def SeedSingularBounds.m (S : SeedSingularBounds) : ℝ :=
  min S.mB S.mC

theorem SeedSingularBounds.m_pos (S : SeedSingularBounds) : 0 < S.m :=
  lt_min S.mB_pos S.mC_pos

end Mub6
