/-
Mub6/AssemblyCover.lean

T4 Lean, group (B), direction m3/d1: the six assembly implications of the preprint as theorems over
the abstract interface of `Mub6.Interface`.  (Named `AssemblyCover` and not `Assembly` only
because `Mub6/Assembly.lean` belongs to the scaffold owner; that file points here.)

Every proposition is stated with the paper's conclusion and with the paper's own premises
explicit: the arithmetic/verification premise (**S**, "the routine does what the text says") and
the termination premise (**C**, "the traversal closed with no unresolved region") are *hypotheses*,
never proved facts, and each is identified in reports/statements.md section m3.

Design point the brief asked for: 2.10, 3.11, 4.16, 5.7 and the inner part of 6.9 are not five
inductions.  Each is `Cover.Cert.covered` at one particular decomposition, plus -- for 4.16 and
5.7 -- the single blocker induction `Cover.accumulate_covered`.  The geometric content of each
proposition lives in the instance files (`Exclude` for section 6; `Seed`, `Frames`, `Hadamard`,
`ThreeMUB` for sections 1-4).
-/
import Mathlib
import Mub6.Interface
import Mub6.Exclude

namespace Mub6
namespace AssemblyCover

open Cover

/-! ## Records and their solution sets -/

/-- A certified record: a centre with the radius at which it is certified.  In the paper a record
is a Root (Definition 4.1) together with a radius, and its solution set is (5.1),
`S(P,R) = { [e(P+δ)] : δ horizontal, ‖δ‖ ≤ R, F(P+δ) = 0 }`.  The assembly only uses it as a set
of points and the fact that radii may only grow, so both are abstract here. -/
structure Rec (C : Type*) where
  centre : C
  radius : ℝ

/-- The Euclidean distance on `ℝ^9`, the seed-coordinate carrier of section 2. -/
noncomputable def dist2 {n : ℕ} (x y : Fin n → ℝ) : ℝ := Real.sqrt (∑ j, (x j - y j) ^ 2)

/-! ## Proposition 2.10 (seed cover) -/

/-- The paper's constant: nine coordinates binned at width `1/112`, each midpoint within
`√9/(2·112) = 3/224` of its bin, and `3/224 < 0.032`. -/
theorem seed_radius : Real.sqrt 9 / (2 * 112) = 3 / 224 ∧ (3 / 224 : ℝ) < 0.032 := by
  constructor
  · rw [show Real.sqrt 9 = 3 by
      rw [show (9 : ℝ) = 3 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]]
    norm_num
  · norm_num

/-- **Proposition 2.10 (exhaustive seed cover).**  If every region of the traversal is either
excluded by a certified necessary filter or contained in one of the written balls (`hcert`, whose
`union` nodes are the bin tuples and whose `excl` leaves are the filters (2.11)-(2.19)), then
every seed coordinate of an exact Hadamard matrix lies in a written ball of radius `0.032`.

Premises made explicit: `hcert` is the **S + C** half -- the enumeration visits every bin tuple and
the run completed with no unresolved leaf.  The mathematical half (2.6, 2.7, 2.8, 2.9) justifies
the `excl` leaves and is not needed at assembly level. -/
theorem prop_2_10 {Ball : Type*} (mem : Ball → (Fin 9 → ℝ) → Prop) (𝔅 : Set Ball)
    (mid : Ball → (Fin 9 → ℝ)) (R : ℝ) (hR : R = 0.032)
    (hball : ∀ b ∈ 𝔅, ∀ x, mem b x → dist2 x (mid b) ≤ R)
    (seeds : Set (Fin 9 → ℝ)) (hcert : Cert mem 𝔅 seeds Set.univ) :
    ∀ x ∈ seeds, ∃ b ∈ 𝔅, dist2 x (mid b) ≤ 0.032 := by
  intro x hx
  obtain ⟨b, hb, hbm⟩ := hcert.covered (x := x) (And.intro hx (Set.mem_univ x))
  exact ⟨b, hb, by rw [← hR]; exact hball b hb x hbm⟩

/-! ## Proposition 3.11 (completion coverage) -/

/-- **Proposition 3.11 (completion coverage).**  If every terminal cell of the finite recursion is
either excluded by a certified necessary test (`excl` leaves: Lemma 3.8's norm test or Lemma 3.9's
directional test) or covered by a certified phase ball (`ball` leaves), then those balls cover all
feasible completions of the seed.

The recursion terminating with zero unresolved cells is `hcert` itself: the tree is complete, every
cell being a leaf with a verdict.  An unresolved cell would be a leaf of neither kind, and no
`Cert` could be built. -/
theorem prop_3_11 {Ball Pt : Type*} (mem : Ball → Pt → Prop) (𝔅 : Set Ball)
    (feasible : Set Pt) (hcert : Cert mem 𝔅 feasible Set.univ) :
    ∀ x ∈ feasible, ∃ b ∈ 𝔅, mem b x :=
  fun x hx => hcert.covered (x := x) (And.intro hx (Set.mem_univ x))

/-! ## Proposition 4.16 (the atlas covers) -/

/-- **Proposition 4.16 (atlas covers).**  Let `seeds` be the processed seed list in program order,
`atlasOf l` the A-stage atlas after the prefix `l`.  If the atlas is append-only
(`hatlas_mono`), each processed seed's solutions are placed in the atlas at the moment that seed's
processing completes (`hstep`: Proposition 3.11 plus the coarse-record conversion), and the final
atlas is contained in the written `atlas` (`hfinal`), then the written A-stage records cover every
exact solution whose seed coordinates were exhausted by the seed cover (`hcover`, the conclusion of
Proposition 2.10).

This is `accumulate_covered` with no failed seed: "no failed and no unresolved seed" is exactly
`hstep` being available for every seed of the list. -/
theorem prop_4_16 {Pt S : Type*} (seedSol : S → Set Pt) (sol : Rec S → Set Pt)
    (seeds : List S) (atlas : List (Rec S)) (atlasOf : List S → Set (Rec S))
    (hatlas_mono : ∀ (l t : List S), atlasOf l ⊆ atlasOf (l ++ t))
    (hfinal : atlasOf seeds ⊆ {b | b ∈ atlas})
    (hstep : ∀ (l : List S) (p : S), Covered (fun b x => x ∈ sol b) (atlasOf (l ++ [p]))
      (seedSol p))
    (H : Set Pt) (hcover : ∀ x ∈ H, ∃ s ∈ seeds, x ∈ seedSol s) :
    ∀ x ∈ H, ∃ b ∈ atlas, x ∈ sol b := by
  intro x hx
  obtain ⟨s, hs, hxs⟩ := hcover x hx
  obtain ⟨b, hb, hbx⟩ := accumulate_covered (fun b (x : Pt) => x ∈ sol b) seedSol
    (fun _ => False) atlasOf hatlas_mono
    (fun l p _ => hstep l p) seeds x ⟨s, hs, (fun h => h), hxs⟩
  exact ⟨b, hfinal hb, hbx⟩

/-! ## Proposition 5.7 (Stage-B coverage inclusion) -/

/-- **Proposition 5.7 (Stage-B coverage inclusion).**  On a completed Stage-B run over the input
records, with `atlas` the final atlas of children and `bad` the input parents whose refinement
failed, `⋃_{input} S(P,R) ⊆ ⋃_{atlas} S(Q,r) ∪ ⋃_{bad} S(P,R)`   (5.26).

`hstep` is the per-parent certificate (a successful outside test, a successful direct assignment,
or a successful relation to a child or to an *already completed* blocker); `hfinal` records that
the atlas writes out what was accumulated.  The paper's "two finite inductions" are
`Cert.covered` (on the subdivision tree, inside `hstep`) and `accumulate_covered` (on the order of
completed parents). -/
theorem prop_5_7 {Pt : Type*} (sol : Rec ℕ → Set Pt) (input atlas bad : List (Rec ℕ))
    (atlasOf : List (Rec ℕ) → Set (Rec ℕ))
    (hatlas_mono : ∀ (l t : List (Rec ℕ)), atlasOf l ⊆ atlasOf (l ++ t))
    (hfinal : atlasOf input ⊆ {b | b ∈ atlas})
    (hstep : ∀ (l : List (Rec ℕ)) (p : Rec ℕ), p ∉ bad →
      Covered (fun b x => x ∈ sol b) (atlasOf (l ++ [p])) (sol p)) :
    ∀ x, (∃ a ∈ input, x ∈ sol a) → (∃ b ∈ atlas, x ∈ sol b) ∨ (∃ c ∈ bad, x ∈ sol c) := by
  intro x hx
  obtain ⟨a, ha, hxa⟩ := hx
  by_cases hbad : a ∈ bad
  · exact Or.inr ⟨a, hbad, hxa⟩
  · obtain ⟨b, hb, hbx⟩ := accumulate_covered (fun b (x : Pt) => x ∈ sol b) sol
      (fun p => p ∈ bad) atlasOf hatlas_mono
      (fun l p hp => hstep l p hp) input x ⟨a, ha, hbad, hxa⟩
    exact Or.inl ⟨b, hfinal hb, hbx⟩

/-- **Corollary 5.8.**  A completed batching invocation with no bad parents and every emitted batch
included replaces the input cover by the emitted records at the common cap `τ`. -/
theorem cor_5_8 {Pt : Type*} (sol : Rec ℕ → Set Pt) (input atlas : List (Rec ℕ))
    (atlasOf : List (Rec ℕ) → Set (Rec ℕ))
    (hatlas_mono : ∀ (l t : List (Rec ℕ)), atlasOf l ⊆ atlasOf (l ++ t))
    (hfinal : atlasOf input ⊆ {b | b ∈ atlas})
    (hstep : ∀ (l : List (Rec ℕ)) (p : Rec ℕ),
      Covered (fun b x => x ∈ sol b) (atlasOf (l ++ [p])) (sol p)) :
    ∀ x, (∃ a ∈ input, x ∈ sol a) → ∃ b ∈ atlas, x ∈ sol b := by
  intro x hx
  rcases prop_5_7 sol input atlas [] atlasOf hatlas_mono hfinal
      (fun l p _ => hstep l p) x hx with ⟨b, hb, hbx⟩ | ⟨c, hc, -⟩
  · exact ⟨b, hb, hbx⟩
  · simp at hc

/-! ## Proposition 6.9 (local exclusion certificate) -/

/-- **Proposition 6.9 (local exclusion certificate), in the form Theorem 7.1 consumes it.**  If the
Stage-C graph test for a record returns a negative result, then no exact Hadamard in the closed ball
of that record can be extended, together with the coordinate basis, by two further mutually
unbiased orthonormal bases.

The proof is `StageC.prop_6_9`; the geometric hypotheses are that theorem's (ball cover `hlab`,
radii `< .1`, retained edges `hO`/`hU`, and the negative graph search `hgraph`, which is Lemma 6.8 --
a specification claim about `graph::exist` and therefore a binder). -/
theorem prop_6_9 {V : Type*} (G : StageC.Graph V) (v : V → Fin 6 → ℝ) (s : V → ℝ)
    (hs0 : ∀ b, 0 ≤ s b) (hs : ∀ b, s b < 1 / 10)
    (lab : (Fin 6 → ℝ) → V) (hlab : ∀ u, StageC.InBall (v (lab u)) (s (lab u)) u)
    (hgraph : ¬ StageC.Config G)
    (hO : ∀ u u', StageC.Ortho u u' → G.O (lab u) (lab u'))
    (hU : ∀ u u', StageC.Unbiased u u' → G.U (lab u) (lab u')) :
    ¬ ∃ (u0 u1 : Fin 6 → Fin 6 → ℝ),
      (∀ i j, i ≠ j → StageC.Ortho (u0 i) (u0 j)) ∧
      (∀ i j, i ≠ j → StageC.Ortho (u1 i) (u1 j)) ∧
      (∀ i j, StageC.Unbiased (u0 i) (u1 j)) := by
  rintro ⟨u0, u1, h0, h1, hc⟩
  exact StageC.prop_6_9 G v s hs0 hs lab hlab hgraph hO hU u0 u1 h0 h1 hc

/-! ## Theorem 7.1 (finite-execution certificate) -/

/-- **Theorem 7.1 (finite-execution certificate).**  A chain of coverage links, each one
proposition of sections 2-6, whose last set carries a negative Stage-C verdict for every record, has
no extendible point.  The links are

| set | supplied by |
|---|---|
| `H -> Sseed` | Proposition 2.10 |
| `Sseed -> Scoarse` | Proposition 4.16 |
| `Scoarse -> Smid`, `Smid -> Sfine` | Proposition 5.7, Corollary 5.8 |
| `Sfine -> Sinit` | batch/marker bookkeeping (5.6, 7.2) |
| `Sinit -> Sfallback` | the subsequence and fallback-input checks (7.2) |
| `Sfallback -> Sfinal` | the four modulo-4 final shards partition (7.2) |
| `Sfinal` excluded | Proposition 6.9 at every final record |

Every link is an **S + C** implication; `emb` is the permitted signed permutation/transpose action
and `hinv` is Lemma 4.7's invariance of extendibility.  The paper's remark that "counts and hashes
establish the identity and completeness of the finite chain, not those inequalities in isolation"
is exactly why the bookkeeping steps appear as coverage links rather than as arithmetic. -/
theorem theorem_7_1 {Pt : Type*} (emb : Pt → Pt → Prop)
    (htrans : ∀ x y z, emb x y → emb y z → emb x z)
    (ext : Pt → Prop) (hinv : ∀ x y, emb x y → (ext x ↔ ext y))
    (H Sseed Scoarse Smid Sfine Sinit Sfallback Sfinal : Set Pt)
    (h2_10 : Cov emb H Sseed)
    (hA : Cov emb Sseed Scoarse)
    (hBmid : Cov emb Scoarse Smid)
    (hBfine : Cov emb Smid Sfine)
    (hinitC : Cov emb Sfine Sinit)
    (hfallback : Cov emb Sinit Sfallback)
    (hfinal : Cov emb Sfallback Sfinal)
    (hCneg : ∀ y ∈ Sfinal, ¬ ext y) :
    ∀ x ∈ H, ¬ ext x := by
  have hc : Cov emb H Sfinal :=
    Cov.trans htrans (Cov.trans htrans (Cov.trans htrans (Cov.trans htrans
      (Cov.trans htrans (Cov.trans htrans h2_10 hA) hBmid) hBfine) hinitC) hfallback) hfinal
  exact Cov.excludes hc ext hinv hCneg

/-- **Theorem 1.1 from Theorem 7.1.**  If four mutually unbiased orthonormal bases in `ℂ^6` give an
extendible point of the initial set `H`, Theorem 7.1's conclusion refutes it. -/
theorem theorem_1_1 {Pt : Type*} (emb : Pt → Pt → Prop)
    (htrans : ∀ x y z, emb x y → emb y z → emb x z)
    (ext : Pt → Prop) (hinv : ∀ x y, emb x y → (ext x ↔ ext y))
    (H Sseed Scoarse Smid Sfine Sinit Sfallback Sfinal : Set Pt)
    (h2_10 : Cov emb H Sseed)
    (hA : Cov emb Sseed Scoarse)
    (hBmid : Cov emb Scoarse Smid)
    (hBfine : Cov emb Smid Sfine)
    (hinitC : Cov emb Sfine Sinit)
    (hfallback : Cov emb Sinit Sfallback)
    (hfinal : Cov emb Sfallback Sfinal)
    (hCneg : ∀ y ∈ Sfinal, ¬ ext y)
    (hfour : ∃ x ∈ H, ext x) : False := by
  obtain ⟨x, hx, hxext⟩ := hfour
  exact theorem_7_1 emb htrans ext hinv H Sseed Scoarse Smid Sfine Sinit Sfallback Sfinal
    h2_10 hA hBmid hBfine hinitC hfallback hfinal hCneg x hx hxext

end AssemblyCover
end Mub6
