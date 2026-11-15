/-
Stage C, graph layer (L3) only: reflection of the (6.24) pattern search into Lean.

The combinatorial content of Stage C (`H0-stageC-criterion.md`, §1, H4) is:
  given two relations O, U on a finite vertex set (the balls of a record),
  there is NO pair of 6-sets `a`, `b` with
    a, b O-cliques, a and b disjoint, every cross pair in U.
If the search that establishes this is replaced by a Lean function, the verdict
"no pattern" becomes a kernel-checked fact about the same adjacency data.

This file contains:
  * `HasPattern`   : the declarative (6.24) statement;
  * `search`       : an executable complete enumeration (fuel index, no bitsets, no step cap);
  * `search_complete` : `HasPattern -> search = true`, hence
                        `search = false -> ¬ HasPattern` (the only direction a
                        certificate needs);
  * `no_pattern_of_search_false` : the certificate idiom used on real records.

Nothing here is about the numeric predicates (6.16)/(6.20)/(6.21)/(6.23): the
adjacency is an input.  See the report for what that leaves unverified.
-/
import Mathlib

namespace StageCGraph

/-- Pairwise adjacency on a list (irreflexivity is not assumed). -/
def PairwiseO (O : Nat → Nat → Bool) (l : List Nat) : Prop :=
  ∀ x ∈ l, ∀ y ∈ l, x ≠ y → O x y = true

/-- A clique: nodup list, pairwise adjacent. -/
def Clq (O : Nat → Nat → Bool) (l : List Nat) : Prop := l.Nodup ∧ PairwiseO O l

/-- **(6.24)**: two disjoint 6-cliques of `O` with all cross pairs in `U`. -/
def HasPattern (O U : Nat → Nat → Bool) : Prop :=
  ∃ a b : List Nat, Clq O a ∧ Clq O b ∧ a.length = 6 ∧ b.length = 6 ∧
    (∀ x ∈ a, ∀ y ∈ b, U x y = true) ∧ (∀ x ∈ a, x ∉ b)

/-- The set of vertices `U`-adjacent to every vertex of `A`, as a list. -/
def commonU (n : Nat) (U : Nat → Nat → Bool) (A : List Nat) : List Nat :=
  (List.range n).filter (fun w => A.all (fun a => U a w))

/-- Exists a `k`-clique inside the list `S`?  (Same recursion as `graph::clique`,
indexed by a fuel argument so that it is structurally recursive.) -/
def clqF (O : Nat → Nat → Bool) : Nat → List Nat → Nat → Bool
  | _, _, 0 => true
  | 0, _, _ + 1 => false
  | f + 1, S, k + 1 =>
      if S.length < k + 1 then false else
        match S with
        | [] => false
        | v :: rest => clqF O f (rest.filter (O v)) k || clqF O f rest (k + 1)

/-- Complete enumeration of the `k`-element extensions of `A` inside `cands`, then a
6-clique in the common `U`-neighbourhood.  (Same recursion as `graph::exist`, without
the step cap and without the `clique(pool,6)` prefilters.) -/
def searchF (n : Nat) (O U : Nat → Nat → Bool) : Nat → List Nat → List Nat → Nat → Bool
  | _, _, A, 0 => clqF O n (commonU n U A) 6
  | 0, _, _, _ + 1 => false
  | f + 1, cands, A, k + 1 =>
      if cands.length < k + 1 then false else
        match cands with
        | [] => false
        | v :: rest =>
            (if A.all (fun a => O a v) && decide (6 ≤ (commonU n U (A ++ [v])).length) then
              searchF n O U f (rest.filter (O v)) (A ++ [v]) k
             else false)
            || searchF n O U f rest A (k + 1)

/-- The executable search: a 6-clique `a` from `range n`, then a 6-clique in the
common `U`-neighbourhood of `a`.  Returns `true` iff a pattern was found. -/
def search (n : Nat) (O U : Nat → Nat → Bool) : Bool :=
  searchF n O U n (List.range n) [] 6

/-! ### basic invariance -/

lemma PairwiseO.perm {O : Nat → Nat → Bool} {l l' : List Nat} (h : l.Perm l')
    (hp : PairwiseO O l) : PairwiseO O l' := by
  intro x hx y hy hxy
  exact hp x (h.mem_iff.mpr hx) y (h.mem_iff.mpr hy) hxy

lemma commonU_perm (n : Nat) (U : Nat → Nat → Bool) {A A' : List Nat} (h : A.Perm A') :
    commonU n U A = commonU n U A' := by
  unfold commonU
  have key : ∀ w, A.all (fun a => U a w) = A'.all (fun a => U a w) := by
    intro w
    rw [Bool.eq_iff_iff]
    simp only [List.all_eq_true]
    constructor <;> intro hh a ha
    · exact hh a (h.mem_iff.mpr ha)
    · exact hh a (h.mem_iff.mp ha)
  simp only [key]

lemma commonU_length (n : Nat) (U : Nat → Nat → Bool) (A : List Nat) :
    (commonU n U A).length ≤ n := by
  unfold commonU
  have := List.length_filter_le (fun w => A.all (fun a => U a w)) (List.range n)
  simpa using this

lemma exists_mem_of_length_pos {l : List Nat} (h : 0 < l.length) : ∃ a, a ∈ l := by
  cases l with
  | nil => simp at h
  | cons a t => exact ⟨a, by simp⟩

lemma length_le_of_subset : ∀ {T S : List Nat}, T.Nodup → (∀ x ∈ T, x ∈ S) → T.length ≤ S.length
  | [], _, _, _ => by simp
  | a :: t, S, hnd, h => by
      have ha : a ∈ S := h a (by simp)
      have ht : ∀ x ∈ t, x ∈ S.erase a := by
        intro x hx
        have hxS : x ∈ S := h x (by simp [hx])
        have hxa : x ≠ a := by
          intro hh
          exact (List.nodup_cons.mp hnd).1 (hh ▸ hx)
        exact (List.mem_erase_of_ne hxa).mpr hxS
      have hpos : 0 < S.length := List.length_pos_of_mem ha
      have hrec := length_le_of_subset (List.nodup_cons.mp hnd).2 ht
      rw [List.length_erase_of_mem ha] at hrec
      simp only [List.length_cons]
      omega

lemma commonU_anti (n : Nat) (U : Nat → Nat → Bool) {A B : List Nat}
    (h : ∀ x ∈ A, x ∈ B) : ∀ y ∈ commonU n U B, y ∈ commonU n U A := by
  intro y hy
  simp only [commonU, List.mem_filter, List.all_eq_true] at hy ⊢
  exact ⟨hy.1, fun a ha => hy.2 a (h a ha)⟩

/-! ### `clqF` is complete -/

lemma clq_complete (O : Nat → Nat → Bool) :
    ∀ (fuel : Nat) (S : List Nat), S.length ≤ fuel →
      ∀ (T : List Nat) (k : Nat), (∀ x ∈ T, x ∈ S) → T.Nodup → T.length = k →
        PairwiseO O T → clqF O fuel S k = true := by
  intro fuel
  induction fuel with
  | zero =>
      intro S hS T k hsub hnd hlen hpw
      have hS' : S = [] := List.eq_nil_of_length_eq_zero (by omega)
      subst hS'
      have hT : T = [] := by
        cases T with
        | nil => rfl
        | cons a l => exact absurd (hsub a (by simp)) (by simp)
      subst hT
      have hk : k = 0 := by simpa using hlen.symm
      subst hk
      simp [clqF]
  | succ m ih =>
      intro S hS T k hsub hnd hlen hpw
      by_cases hk0 : k = 0
      · subst hk0
        simp [clqF]
      · obtain ⟨k', rfl⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
        cases S with
        | nil =>
            have hT : T = [] := by
              cases T with
              | nil => rfl
              | cons a l => exact absurd (hsub a (by simp)) (by simp)
            subst hT
            simp at hlen
        | cons v rest =>
            by_cases hv : v ∈ T
            · have hnd_ne : ∀ x ∈ T.erase v, x ≠ v := fun x hx =>
                ((List.Nodup.mem_erase_iff hnd).mp hx).1
              have hmem_erase : ∀ x ∈ T.erase v, x ∈ rest := by
                intro x hx
                have hxT : x ∈ T := List.mem_of_mem_erase hx
                have hxne : x ≠ v := hnd_ne x hx
                have hcases : x = v ∨ x ∈ rest := List.mem_cons.mp (hsub x hxT)
                rcases hcases with h | h
                · exact absurd h hxne
                · exact h
              have hsub_f : ∀ x ∈ T.erase v, x ∈ rest.filter (O v) := by
                intro x hx
                refine List.mem_filter.mpr ⟨hmem_erase x hx, ?_⟩
                exact hpw v hv x (List.mem_of_mem_erase hx) (Ne.symm (hnd_ne x hx))
              have hlen' : (T.erase v).length = k' := by
                rw [List.length_erase_of_mem hv, hlen]; omega
              have hrec := ih (rest.filter (O v))
                (by have h := List.length_filter_le (O v) rest
                    simp only [List.length_cons] at hS
                    omega)
                (T.erase v) k' hsub_f (hnd.erase v) hlen'
                (fun x hx y hy hxy =>
                  hpw x (List.mem_of_mem_erase hx) y (List.mem_of_mem_erase hy) hxy)
              have hge : ¬ ((v :: rest).length < k' + 1) := by
                have hle := length_le_of_subset hnd hsub
                omega
              simp only [clqF]
              rw [if_neg hge]
              rw [hrec]
              rfl
            · have hsub' : ∀ x ∈ T, x ∈ rest := by
                intro x hx
                have hcases : x = v ∨ x ∈ rest := List.mem_cons.mp (hsub x hx)
                rcases hcases with h | h
                · exact absurd (h ▸ hx) hv
                · exact h
              have hrec := ih rest (by simp only [List.length_cons] at hS; omega)
                T (k' + 1) hsub' hnd hlen hpw
              have hge : ¬ ((v :: rest).length < k' + 1) := by
                have hle := length_le_of_subset hnd (fun x hx => List.mem_cons_of_mem v (hsub' x hx))
                omega
              simp only [clqF]
              rw [if_neg hge]
              rw [hrec]
              simp

/-! ### `searchF` is complete -/

lemma searchF_complete (n : Nat) (O U : Nat → Nat → Bool) :
    ∀ (fuel : Nat) (cands : List Nat), cands.length ≤ fuel →
      ∀ (A A' : List Nat) (k : Nat) (B : List Nat),
        (∀ x ∈ A', x ∈ cands) →
        (A ++ A').Nodup → A'.length = k → (A ++ A').length = 6 →
        PairwiseO O (A ++ A') →
        B.Nodup → B.length = 6 → PairwiseO O B →
        (∀ y ∈ B, y ∈ commonU n U (A ++ A')) →
        searchF n O U fuel cands A k = true := by
  intro fuel
  induction fuel with
  | zero =>
      intro cands hcands A A' k B hsub hnd hlenA hlen6 hpw hBnd hBlen hBpw hBU
      have hcands' : cands = [] := List.eq_nil_of_length_eq_zero (by omega)
      subst hcands'
      have hA' : A' = [] := by
        cases A' with
        | nil => rfl
        | cons a l => exact absurd (hsub a (by simp)) (by simp)
      subst hA'
      have hk : k = 0 := by simpa using hlenA.symm
      subst hk
      have hmem : ∀ y ∈ B, y ∈ commonU n U A := by
        intro y hy
        simpa using hBU y hy
      have hclq := clq_complete O n (commonU n U A) (commonU_length n U A) B 6
        (fun y hy => hmem y hy) hBnd hBlen hBpw
      simpa [searchF] using hclq
  | succ m ih =>
      intro cands hcands A A' k B hsub hnd hlenA hlen6 hpw hBnd hBlen hBpw hBU
      by_cases hk0 : k = 0
      · subst hk0
        have hA' : A' = [] := List.eq_nil_of_length_eq_zero (by omega)
        subst hA'
        have hmem : ∀ y ∈ B, y ∈ commonU n U A := by
          intro y hy
          simpa using hBU y hy
        have hclq := clq_complete O n (commonU n U A) (commonU_length n U A) B 6
          (fun y hy => hmem y hy) hBnd hBlen hBpw
        simpa [searchF] using hclq
      · obtain ⟨k', rfl⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
        cases cands with
        | nil =>
            have hA' : A' = [] := by
              cases A' with
              | nil => rfl
              | cons a l => exact absurd (hsub a (by simp)) (by simp)
            subst hA'
            simp at hlenA
        | cons v rest =>
            have hndA' : A'.Nodup := (List.nodup_append.mp hnd).2.1
            have hdisj : ∀ a ∈ A, ∀ b ∈ A', a ≠ b := (List.nodup_append.mp hnd).2.2
            by_cases hv : v ∈ A'
            · have hperm : A'.Perm (v :: A'.erase v) := List.perm_cons_erase hv
              have hperm2 : (A ++ A').Perm ((A ++ [v]) ++ A'.erase v) := by
                simpa only [List.append_assoc, List.singleton_append] using hperm.append_left A
              have hall : A.all (fun a => O a v) = true := by
                rw [List.all_eq_true]
                intro a ha
                exact hpw a (List.mem_append_left _ ha) v (List.mem_append_right _ hv)
                  (hdisj a ha v hv)
              have hsub2 : ∀ x ∈ A'.erase v, x ∈ rest.filter (O v) := by
                intro x hx
                have hx' : x ∈ A' := List.mem_of_mem_erase hx
                have hxne : x ≠ v := ((List.Nodup.mem_erase_iff hndA').mp hx).1
                refine List.mem_filter.mpr ⟨?_, ?_⟩
                · have hcases : x = v ∨ x ∈ rest := List.mem_cons.mp (hsub x hx')
                  rcases hcases with h | h
                  · exact absurd h hxne
                  · exact h
                · exact hpw v (List.mem_append_right _ hv) x (List.mem_append_right _ hx')
                    (fun h => hxne h.symm)
              have hlen' : (A'.erase v).length = k' := by
                rw [List.length_erase_of_mem hv, hlenA]; omega
              have hnd2 : ((A ++ [v]) ++ A'.erase v).Nodup := hperm2.nodup_iff.mp hnd
              have hlen2 : ((A ++ [v]) ++ A'.erase v).length = 6 := by
                rw [← hperm2.length_eq]; exact hlen6
              have hpw2 : PairwiseO O ((A ++ [v]) ++ A'.erase v) :=
                PairwiseO.perm hperm2 hpw
              have hBU2 : ∀ y ∈ B, y ∈ commonU n U ((A ++ [v]) ++ A'.erase v) := by
                intro y hy
                rw [← commonU_perm n U hperm2]
                exact hBU y hy
              have hrec := ih (rest.filter (O v))
                (by have h := List.length_filter_le (O v) rest
                    simp only [List.length_cons] at hcands
                    omega)
                (A ++ [v]) (A'.erase v) k' B hsub2 hnd2 hlen' hlen2 hpw2
                hBnd hBlen hBpw hBU2
              have hge : ¬ ((v :: rest).length < k' + 1) := by
                have hle := length_le_of_subset hndA' hsub
                omega
              have hBAsub : ∀ x ∈ A ++ [v], x ∈ A ++ A' := by
                intro x hx
                rcases List.mem_append.mp hx with h | h
                · exact List.mem_append_left _ h
                · rw [List.mem_singleton.mp h]
                  exact List.mem_append_right _ hv
              have hBA : ∀ y ∈ B, y ∈ commonU n U (A ++ [v]) := by
                intro y hy
                exact commonU_anti n U hBAsub y (hBU y hy)
              have hpool : decide (6 ≤ (commonU n U (A ++ [v])).length) = true := by
                rw [decide_eq_true_eq]
                calc 6 = B.length := hBlen.symm
                  _ ≤ (commonU n U (A ++ [v])).length := length_le_of_subset hBnd hBA
              have hcond : (A.all (fun a => O a v) &&
                  decide (6 ≤ (commonU n U (A ++ [v])).length)) = true := by
                rw [Bool.and_eq_true]
                exact ⟨hall, hpool⟩
              simp only [searchF]
              rw [if_neg hge]
              rw [if_pos hcond, hrec]
              rfl
            · have hsub' : ∀ x ∈ A', x ∈ rest := by
                intro x hx
                have hcases : x = v ∨ x ∈ rest := List.mem_cons.mp (hsub x hx)
                rcases hcases with h | h
                · exact absurd (h ▸ hx) hv
                · exact h
              have hrec := ih rest (by simp only [List.length_cons] at hcands; omega)
                A A' (k' + 1) B hsub' hnd hlenA hlen6 hpw hBnd hBlen hBpw hBU
              have hge : ¬ ((v :: rest).length < k' + 1) := by
                have hle := length_le_of_subset hndA'
                  (fun x hx => List.mem_cons_of_mem v (hsub' x hx))
                omega
              simp only [searchF]
              rw [if_neg hge, hrec]
              simp

/-! ### the certificate statement -/

/-- **Completeness of the reflected search**: a (6.24) pattern forces `search = true`.
`hOut` says vertices outside `range n` are isolated in `O`. -/
theorem search_complete (n : Nat) (O U : Nat → Nat → Bool)
    (hOut : ∀ x y, (n ≤ x ∨ n ≤ y) → O x y = false)
    (h : HasPattern O U) : search n O U = true := by
  obtain ⟨a, b, ⟨hand, hpwa⟩, ⟨hbnd, hbpw⟩, halen, hblen, hcross, hdisj⟩ := h
  have hmem_a : ∀ x ∈ a, x < n := by
    intro x hx
    by_contra hge
    push_neg at hge
    obtain ⟨y, hy⟩ : ∃ y, y ∈ a.erase x := by
      have hpos : 0 < (a.erase x).length := by
        rw [List.length_erase_of_mem hx, halen]; omega
      exact exists_mem_of_length_pos hpos
    have hyx : y ≠ x := ((List.Nodup.mem_erase_iff hand).mp hy).1
    have hya : y ∈ a := List.mem_of_mem_erase hy
    have h1 : O x y = false := hOut x y (Or.inl hge)
    have h2 : O x y = true := hpwa x hx y hya (Ne.symm hyx)
    rw [h1] at h2
    exact Bool.noConfusion h2
  have hmem_b : ∀ y ∈ b, y < n := by
    intro y hy
    by_contra hge
    push_neg at hge
    obtain ⟨x, hx⟩ : ∃ x, x ∈ b.erase y := by
      have hpos : 0 < (b.erase y).length := by
        rw [List.length_erase_of_mem hy, hblen]; omega
      exact exists_mem_of_length_pos hpos
    have hxy : x ≠ y := ((List.Nodup.mem_erase_iff hbnd).mp hx).1
    have hxb : x ∈ b := List.mem_of_mem_erase hx
    have h1 : O x y = false := hOut x y (Or.inr hge)
    have h2 : O x y = true := hbpw x hxb y hy hxy
    rw [h1] at h2
    exact Bool.noConfusion h2
  have hsub0 : ∀ x ∈ a, x ∈ List.range n := fun x hx => List.mem_range.mpr (hmem_a x hx)
  have hnd0 : ([] ++ a).Nodup := by simpa using hand
  have hlen60 : ([] ++ a).length = 6 := by simpa using halen
  have hpw0 : PairwiseO O ([] ++ a) := by simpa using hpwa
  have hBU0 : ∀ y ∈ b, y ∈ commonU n U ([] ++ a) := by
    intro y hy
    refine List.mem_filter.mpr ⟨List.mem_range.mpr (hmem_b y hy), ?_⟩
    exact List.all_eq_true.mpr (fun x hx => hcross x hx y hy)
  exact searchF_complete n O U n (List.range n) (by simp) [] a 6 b
    hsub0 hnd0 halen hlen60 hpw0 hbnd hblen hbpw hBU0

/-- **The certificate statement**: if `search` evaluates to `false` on the record's
adjacency, no (6.24) pattern exists. -/
theorem no_pattern_of_search_false (n : Nat) (O U : Nat → Nat → Bool)
    (hOut : ∀ x y, (n ≤ x ∨ n ≤ y) → O x y = false)
    (h : search n O U = false) : ¬ HasPattern O U := by
  intro hp
  rw [search_complete n O U hOut hp] at h
  exact Bool.noConfusion h

end StageCGraph
