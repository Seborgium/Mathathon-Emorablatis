/-
Mub6/Interface.lean

T4 Lean, group (B): the abstract cover interface.

The six assembly implications of the preprint -- Proposition 2.10 (seed cover),
Proposition 3.11 (completion coverage), Proposition 4.16 (atlas covers), Proposition 5.7
(Stage-B coverage inclusion), Proposition 6.9 (local exclusion) and Theorem 7.1
(finite-execution certificate) -- are all instances of two combinatorial lemmas that this
file states and proves once:

* `Cert.covered`   : an exhaustive finite decomposition of a region in which every leaf is
                     either *excluded* (it contains no point of the target set) or
                     *contained in one certified ball* covers the region.
* `accumulate_covered` : the "blocker" induction. If the atlas only grows as the parents are
                     processed and each non-failed parent is covered at the moment its
                     processing completes, then the union of the non-failed parents'
                     solution sets is covered by the *final* atlas.
                     The paper's own remark -- that this is not circular because a blocker is
                     always an already-completed parent -- is exactly the shape of the
                     hypothesis `hstep`.
* `Cov.trans` / `Cov.excludes` : composition of coverage links along an extendibility-
                     preserving equivalence, which is how Theorem 7.1 chains the stages.

Nothing here refers to phases, matrices or the number six: the geometric content of each
proposition is isolated in the instance files (`Seed`, `Completion`, `Refine`, `Exclude`,
`Assembly`), and only the *assembly* is shared.
-/
import Mathlib

namespace Mub6

/-! ## Coverage of a region by a family of balls -/

namespace Cover

variable {Pt Ball : Type*} {mem : Ball → Pt → Prop}

/-- `Covered mem 𝔅 S`: every point of `S` lies in some ball of the family `𝔅`. -/
def Covered (mem : Ball → Pt → Prop) (𝔅 : Set Ball) (S : Set Pt) : Prop :=
  ∀ x ∈ S, ∃ b ∈ 𝔅, mem b x

theorem covered_empty (mem : Ball → Pt → Prop) (𝔅 : Set Ball) : Covered mem 𝔅 ∅ := by
  intro x hx
  exact absurd hx (Set.notMem_empty x)

theorem Covered.mono {𝔅 𝔅' : Set Ball} (h : 𝔅 ⊆ 𝔅') {S : Set Pt}
    (hc : Covered mem 𝔅 S) : Covered mem 𝔅' S :=
  fun x hx => let ⟨b, hb, hbx⟩ := hc x hx; ⟨b, h hb, hbx⟩

theorem Covered.union {𝔅 : Set Ball} {S S' : Set Pt}
    (h : Covered mem 𝔅 S) (h' : Covered mem 𝔅 S') : Covered mem 𝔅 (S ∪ S') := by
  intro x hx
  rcases hx with hx | hx
  · exact h x hx
  · exact h' x hx

theorem Covered.iUnion {ι : Type*} {𝔅 : Set Ball} {S : ι → Set Pt}
    (h : ∀ i, Covered mem 𝔅 (S i)) : Covered mem 𝔅 (⋃ i, S i) := by
  intro x hx
  obtain ⟨i, hi⟩ := Set.mem_iUnion.1 hx
  exact h i x hi

/-- A finite cover certificate for one region.

* `empty`  : the region is empty;
* `excl`   : the region contains no point of the target set `T` (a certified necessary test
             failed there -- Lemmas 3.8, 3.9, 6.2, 6.3, 6.6, 6.7 in the paper);
* `ball`   : the region is contained in one ball of `𝔅` (a certified phase ball, a
             cluster ball, a seeded radius-`R` ball);
* `union`  : a finite exhaustive decomposition into sub-regions, each certified
             (a subdivision (5.23), the cell recursion of 3.11, the bin layers of 6.9).

The `union` constructor is where the paper's "children's closed intervals cover the
parent's" is recorded; it is a hypothesis of the constructor, never a proof obligation of
the assembly. -/
inductive Cert (mem : Ball → Pt → Prop) (𝔅 : Set Ball) (T : Set Pt) : Set Pt → Prop where
  | empty : Cert mem 𝔅 T ∅
  | excl (S : Set Pt) (h : Disjoint T S) : Cert mem 𝔅 T S
  | ball (S : Set Pt) (b : Ball) (hb : b ∈ 𝔅) (h : S ⊆ {x | mem b x}) : Cert mem 𝔅 T S
  | union (S : Set Pt) (U : Set (Set Pt)) (hcov : S ⊆ ⋃₀ U)
      (hU : ∀ R ∈ U, Cert mem 𝔅 T R) : Cert mem 𝔅 T S

/-- The single induction behind Propositions 2.10, 3.11, 5.7 (inner part) and 6.9: a certified
region contains no target point outside the covered family. -/
theorem Cert.covered {𝔅 : Set Ball} {T : Set Pt} {S : Set Pt}
    (h : Cert mem 𝔅 T S) : Covered mem 𝔅 (T ∩ S) := by
  induction h with
  | empty => simpa using covered_empty mem 𝔅
  | excl S hd =>
      intro x hx
      exact absurd hx.2 (Set.disjoint_left.1 hd hx.1)
  | ball S b hb hsub =>
      intro x hx
      exact Exists.intro b (And.intro hb (hsub hx.2))
  | union S U hcov hU ih =>
      intro x hx
      obtain ⟨R, hR, hxR⟩ := Set.mem_sUnion.1 (hcov hx.2)
      exact ih R hR x (And.intro hx.1 hxR)

theorem Cert.mono {𝔅 𝔅' : Set Ball} (hsub : 𝔅 ⊆ 𝔅') {T S : Set Pt}
    (h : Cert mem 𝔅 T S) : Cert mem 𝔅' T S := by
  induction h with
  | empty => exact Cert.empty
  | excl S hd => exact Cert.excl S hd
  | ball S b hb hS => exact Cert.ball S b (hsub hb) hS
  | union S U hcov hU ih => exact Cert.union S U hcov ih

/-! ## The blocker induction -/

/-- `atlas l` is the atlas after the parents in the list `l` have been processed, in the
program's order.  The conclusion is the paper's (5.26) restricted to the non-failed parents.

The hypotheses are precisely the paper's: the atlas is append-only and radii only grow
(`hatlas_mono`), and a parent is entered into the successful list only after its whole sphere
has been shown covered at the *then current* atlas (`hstep`). -/
theorem accumulate_covered {P : Type*}
    (mem : Ball → Pt → Prop) (sols : P → Set Pt) (failed : P → Prop)
    (atlas : List P → Set Ball)
    (hatlas_mono : ∀ (l t : List P), atlas l ⊆ atlas (l ++ t))
    (hstep : ∀ (l : List P) (p : P), ¬ failed p → Covered mem (atlas (l ++ [p])) (sols p)) :
    ∀ (l : List P) (x : Pt), (∃ p ∈ l, ¬ failed p ∧ x ∈ sols p) → ∃ b ∈ atlas l, mem b x := by
  intro l
  induction l using List.reverseRecOn with
  | nil =>
      intro x hx
      obtain ⟨p, hp, -⟩ := hx
      exact absurd hp (by simp)
  | append_singleton l a ih =>
      intro x hx
      obtain ⟨p, hp, hnf, hxs⟩ := hx
      rcases List.mem_append.1 hp with hp | hp
      · obtain ⟨b, hb, hbm⟩ := ih x ⟨p, hp, hnf, hxs⟩
        exact ⟨b, hatlas_mono l [a] hb, hbm⟩
      · obtain rfl : p = a := by simpa using hp
        exact hstep l p hnf x hxs

/-! ## Composition of coverage links (Theorem 7.1) -/

/-- `Cov emb S S'`: every point of `S` is equivalent, under the paper's permitted
equivalences (`emb`), to a point of `S'`.  This is the shape of each stage's conclusion:
"places an equivalent exact solution in a record of ...". -/
def Cov (emb : Pt → Pt → Prop) (S S' : Set Pt) : Prop := ∀ x ∈ S, ∃ y ∈ S', emb x y

theorem Cov.refl {emb : Pt → Pt → Prop} (hrefl : ∀ x, emb x x) (S : Set Pt) : Cov emb S S :=
  fun x hx => ⟨x, hx, hrefl x⟩

theorem Cov.trans {emb : Pt → Pt → Prop}
    (htrans : ∀ x y z, emb x y → emb y z → emb x z) {S S' S'' : Set Pt}
    (h₁ : Cov emb S S') (h₂ : Cov emb S' S'') : Cov emb S S'' := by
  intro x hx
  obtain ⟨y, hy, hxy⟩ := h₁ x hx
  obtain ⟨z, hz, hyz⟩ := h₂ y hy
  exact ⟨z, hz, htrans x y z hxy hyz⟩

/-- The final step of Theorem 7.1: coverage transports non-extendibility backwards. -/
theorem Cov.excludes {emb : Pt → Pt → Prop} {S S' : Set Pt} (h : Cov emb S S')
    (ext : Pt → Prop) (hinv : ∀ x y, emb x y → (ext x ↔ ext y))
    (hbad : ∀ y ∈ S', ¬ ext y) : ∀ x ∈ S, ¬ ext x := by
  intro x hx hext
  obtain ⟨y, hy, hxy⟩ := h x hx
  exact hbad y hy ((hinv x y hxy).1 hext)

end Cover

end Mub6
