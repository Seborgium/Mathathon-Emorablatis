/-
Mub6/Basic.lean — carrier layer for the dimension-six MUB formalisation.

Everything in this file is *infrastructure*: it fixes the carriers and the paper's normalisations
once, so that the paper-specific modules (Hadamard, Seed, Completion, Refine, Exclude, Assembly)
never restate them.  It imports nothing from `Mub6`.

Normalisation decisions (all recorded binder-by-binder in reports/statements.md):

* `Mat 6` is `Matrix (Fin 6) (Fin 6) ℂ`; `RealMat 6` is the same over `ℝ`, used for phase lifts,
  displacements and the double-centring map `Π`.
* The Hermitian inner product is the paper's `⟨u,v⟩ = ∑_j u_j conj(v_j)`, conjugate-linear in the
  *second* argument; it is defined here rather than imported so that the convention is explicit.
* A complex Hadamard matrix is the paper's Definition 2.1: unit-modulus entries and `H H^* = 6 I`,
  one-sided.  Mathlib's `Matrix.IsHadamard` is the two-sided version and is *equivalent* for a
  square matrix; the bridge is in `Mub6/Hadamard.lean`.
* Because of that normalisation, "unbiased" for two Hadamards is `|(H^* K)_{ij}|^2 = 6`, while for
  two basis matrices (`U U^* = 1`) it is `|(U^* V)_{ij}|^2 = 1/6`.  Both are provided.
-/
import Mathlib

namespace Mub6

open scoped Matrix
open Finset

/-! ### Carriers -/

/-- Complex `n × n` matrices: the carrier for Hadamards and basis matrices. -/
abbrev Mat (n : ℕ) := Matrix (Fin n) (Fin n) ℂ

/-- Real `n × n` matrices: the carrier for phase lifts, displacements and `Π`. -/
abbrev RealMat (n : ℕ) := Matrix (Fin n) (Fin n) ℝ

/-- Complex column vectors. -/
abbrev Vec (n : ℕ) := Fin n → ℂ

/-! ### The phase exponential and the inner products -/

/-- Phases are in cycles: `e t = exp (2 π i t)` (paper, §2). -/
noncomputable def e (t : ℝ) : ℂ := Complex.exp ((2 * Real.pi * t : ℝ) * Complex.I)

/-- Entrywise application of `e` to a real matrix: the paper's `e(P)`. -/
noncomputable def expMat {m n : ℕ} (P : Matrix (Fin m) (Fin n) ℝ) : Matrix (Fin m) (Fin n) ℂ :=
  fun i j => e (P i j)

/-- The paper's Hermitian inner product `⟨u,v⟩ = ∑_j u_j conj(v_j)`. -/
noncomputable def ip {n : ℕ} (u v : Vec n) : ℂ := ∑ j, u j * starRingEnd ℂ (v j)

/-- Squared Euclidean norm of a complex vector. -/
noncomputable def vecNormSq {n : ℕ} (u : Vec n) : ℝ := ∑ j, Complex.normSq (u j)

/-- Hilbert–Schmidt (Frobenius) real inner product on complex matrices. -/
noncomputable def frob {m n : ℕ} (A B : Matrix (Fin m) (Fin n) ℂ) : ℝ :=
  ∑ i, ∑ j, (A i j * starRingEnd ℂ (B i j)).re

/-- Squared Frobenius norm on complex matrices. -/
noncomputable def frobSq {m n : ℕ} (A : Matrix (Fin m) (Fin n) ℂ) : ℝ :=
  ∑ i, ∑ j, Complex.normSq (A i j)

/-- Squared Frobenius norm on real matrices — the carrier for the `Π` norm bound. -/
noncomputable def frobSqR {m n : ℕ} (A : Matrix (Fin m) (Fin n) ℝ) : ℝ :=
  ∑ i, ∑ j, A i j ^ 2

/-! ### Unitary, Hadamard, unbiased -/

/-- A basis matrix: its columns are orthonormal, `U U^* = 1`. -/
def IsBasisMat {n : ℕ} (U : Mat n) : Prop := U * Uᴴ = 1

/-- Paper Definition 2.1, verbatim: every entry has modulus one and `H H^* = 6 I`.
(Only one factor is required; squareness supplies the other.  See `Hadamard.lean`.) -/
def IsPhaseHadamard (H : Mat 6) : Prop :=
  (∀ i j, Complex.normSq (H i j) = 1) ∧ H * Hᴴ = (6 : ℂ) • (1 : Mat 6)

/-- Unbiasedness of two basis matrices: every entry of `U^* V` has squared modulus `1/6`. -/
def UnbiasedBases {n : ℕ} (U V : Mat n) : Prop :=
  ∀ i j, Complex.normSq ((Uᴴ * V) i j) = 1 / (n : ℝ)

/-- Unbiasedness of two complex Hadamard matrices in Definition-2.1 normalisation:
every entry of `H^* K` has squared modulus `6`. -/
def UnbiasedH (H K : Mat 6) : Prop := ∀ i j, Complex.normSq ((Hᴴ * K) i j) = 6

/-- The paper's notion: `H` is *extendible* if the standard basis and the columns of `H/√6`
belong to a family of four mutually unbiased orthonormal bases.  Equivalently (with §2.1's
reduction) there are two further complex Hadamard matrices, pairwise unbiased with each other and
with `H`.  Unbiasedness to the standard basis is *automatic* from unit modulus and therefore not a
separate conjunct — recorded in reports/statements.md. -/
def Extendible (H : Mat 6) : Prop :=
  ∃ K L : Mat 6, IsPhaseHadamard K ∧ IsPhaseHadamard L ∧
    UnbiasedH H K ∧ UnbiasedH H L ∧ UnbiasedH K L

/-! ### Dephasing and double centring -/

/-- Paper (2.2): unwrapped dephasing, `D₀(P)_{ij} = P_{ij} - P_{i0} - P_{0j} + P_{00}`. -/
def Dephase (P : RealMat 6) : RealMat 6 := fun i j => P i j - P i 0 - P 0 j + P 0 0

/-- Paper (2.1): double centring `Π` on real `6 × 6` matrices. -/
noncomputable def Pi (z : RealMat 6) : RealMat 6 :=
  fun i j => z i j - (1 / 6) * (∑ b, z i b) - (1 / 6) * (∑ a, z a j)
    + (1 / 36) * (∑ a, ∑ b, z a b)

/-- The horizontal subspace: zero row sums and zero column sums. -/
def Horizontal (z : RealMat 6) : Prop :=
  (∀ i, ∑ j, z i j = 0) ∧ (∀ j, ∑ i, z i j = 0)

/-! ### Dephasing lemmas (paper §2.1, `D₀` fixes the first row and column) -/

@[simp] theorem Dephase_apply (P : RealMat 6) (i j : Fin 6) :
    Dephase P i j = P i j - P i 0 - P 0 j + P 0 0 := rfl

theorem Dephase_row_zero (P : RealMat 6) (j : Fin 6) : Dephase P 0 j = 0 := by
  simp only [Dephase]; ring

theorem Dephase_col_zero (P : RealMat 6) (i : Fin 6) : Dephase P i 0 = 0 := by
  simp only [Dephase]; ring

/-! ### The two structural facts about `Π` (paper Lemma 2.3)

`Π` is proved to land in the horizontal subspace and to be idempotent.  Both are polynomial
identities in the 36 entries of `z`, so they are settled by expanding the (six-term, explicit)
`Fin 6` sums and `ring`.  The projection/orthogonality content is in `Mub6/Hadamard.lean`. -/

theorem Pi_rowSum (z : RealMat 6) (i : Fin 6) : ∑ j, Pi z i j = 0 := by
  simp only [Pi, Fin.sum_univ_six]
  ring

theorem Pi_colSum (z : RealMat 6) (j : Fin 6) : ∑ i, Pi z i j = 0 := by
  simp only [Pi, Fin.sum_univ_six]
  ring

theorem Pi_horizontal (z : RealMat 6) : Horizontal (Pi z) :=
  ⟨Pi_rowSum z, Pi_colSum z⟩

theorem Pi_idem (z : RealMat 6) : Pi (Pi z) = Pi z := by
  ext i j
  simp only [Pi, Fin.sum_univ_six]
  ring

theorem Pi_fixes_horizontal {z : RealMat 6} (h : Horizontal z) : Pi z = z := by
  obtain ⟨hr, hc⟩ := h
  ext i j
  simp only [Pi]
  rw [hr i, hc j]
  have htot : ∑ a, ∑ b, z a b = 0 := by
    rw [Finset.sum_eq_zero (fun a _ => hr a)]
  rw [htot]
  ring

theorem horizontal_iff_Pi_eq_self (z : RealMat 6) : Horizontal z ↔ Pi z = z :=
  ⟨Pi_fixes_horizontal, fun h => h ▸ Pi_horizontal z⟩

/-- Paper Lemma 2.3, second half: `z - Πz` is a sum of a row-constant and a column-constant
matrix.  This is exactly the statement that two phase representatives differing by `z` are
equivalent under row and column rephasings once the first is replaced by `P + Π z`. -/
theorem sub_Pi_eq_rowcol (z : RealMat 6) :
    ∃ r c : Fin 6 → ℝ, z - Pi z = fun i j => r i + c j := by
  refine ⟨fun i => (1 / 6) * (∑ b, z i b) - (1 / 36) * (∑ a, ∑ b, z a b),
    fun j => (1 / 6) * (∑ a, z a j), ?_⟩
  ext i j
  simp only [Pi, Matrix.sub_apply]
  ring

/-! ### API probes kept as documentation of the imported names (removed before release) -/

#check @Matrix.IsHadamard
#check @Matrix.IsHadamard.of_mul_conjTranspose
#check @Fin.sum_univ_six
#check @Complex.normSq
#check @Complex.normSq_apply

end Mub6
