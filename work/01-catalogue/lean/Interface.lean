/-
  Assembly interface for "The maximum number of mutually unbiased bases in
  dimension six".  Companion to ../spine.md, Sections 1 and 3.

  This file contains NO analysis of the paper.  It isolates the top-level
  implication of Section 7.4 (Theorem 7.1 of the paper) and proves it from the
  six stage statements taken as hypotheses.  The hypotheses are the interface:
  instantiating them with the paper's Sections 2--6 is the analysis, and is the
  part that T4 owns.

  Reading of the abstract data (see spine.md Section 1):

    P            : the type of phase matrices,
    Reg          : the type of regions (seed balls, Records, batch records),
    mem R H      : the equivalence class of H meets the region R.  This is
                   deliberately *class* membership and not set membership: every
                   stage of the paper covers solution sets only up to the
                   equivalence of Lemma 2.2 / Lemma 4.7, and spine.md Lemma S.2
                   shows that equivalence preserves extendibility.  So `mem`
                   absorbs the "up to equivalence" clause of every stage at once.
    Exact H      : H is an exact complex Hadamard phase matrix (F(H) = 0),
    Ext H        : H is extendible, together with the coordinate basis, by two
                   further mutually unbiased orthonormal bases.

  Under that reading each stage statement has the same shape,
  `mem (source region) H -> mem (target region) H`, and the assembly is the
  chain of them.  No step below uses anything but the hypotheses.
-/

namespace Mub6Assembly

universe u

variable {P : Type u} {Reg : Type u}

/-! The three primitive notions of the interface. -/

-- `mem R H`: the equivalence class of the phase matrix `H` meets the region `R`.
variable (mem : Reg → P → Prop)

-- `Exact H`: `H` is an exact complex Hadamard phase matrix.
variable (Exact : P → Prop)

-- `Ext H`: `H` is extendible, with the coordinate basis, by two further MUBs.
variable (Ext : P → Prop)

/-- **Assembly, single branch.**

Hypotheses, in the order they are used:

* `h0`   -- Proposition 2.10 (seed cover): every extendible exact `H` has its
            class in one of the written seed balls.
* `hA`   -- Proposition 4.16 (Stage A): every exact `H` in a *processed* seed
            ball has its class in an A-stage Record.  "Processed with no failed
            or unresolved seed" is not a variable here: `hA` is only asserted
            for the seed regions of the completed run.
* `hBm`  -- Proposition 5.7 with Corollary 5.8 (B mid, tau = .07, no failed
            parents): A records are covered by mid records.
* `hBf`  -- the same for B fine (tau = .016).
* `hBat` -- Section 5.6 / X5 (batching): every fine record is emitted in a batch
            record at the same centre with radius tau_fine = .016.  The radius
            is RAISED, which can only enlarge the solution set, and the Root
            assertions of Definition 4.1 carry no radius restriction.
* `hC`   -- Proposition 6.9, used on the batch record and transported to classes
            by spine.md Lemma S.2 (extendibility is invariant under the
            equivalence).  This is the one hypothesis that consumes a lemma of
            spine.md; every other one is a paper statement verbatim.
-/
theorem assembly
    (seed recA recMid recFine recBat : Reg → Prop)
    (h0   : ∀ H, Exact H → Ext H → ∃ B, seed B ∧ mem B H)
    (hA   : ∀ B H, seed B → Exact H → mem B H → ∃ R, recA R ∧ mem R H)
    (hBm  : ∀ R H, recA R → Exact H → mem R H → ∃ M, recMid M ∧ mem M H)
    (hBf  : ∀ M H, recMid M → Exact H → mem M H → ∃ F, recFine F ∧ mem F H)
    (hBat : ∀ F H, recFine F → Exact H → mem F H → ∃ U, recBat U ∧ mem U H)
    (hC   : ∀ U, recBat U → ∀ H, mem U H → ¬ Ext H) :
    ¬ ∃ H, Exact H ∧ Ext H := by
  rintro ⟨H, hExact, hExt⟩
  obtain ⟨B, hB, hBH⟩ := h0 H hExact hExt
  obtain ⟨R, hR, hRH⟩ := hA B H hB hExact hBH
  obtain ⟨M, hM, hMH⟩ := hBm R H hR hExact hRH
  obtain ⟨F, hF, hFH⟩ := hBf M H hM hExact hMH
  obtain ⟨U, hU, hUH⟩ := hBat F H hF hExact hFH
  exact (hC U hU H hUH) hExt

/-- **Assembly, fallback branch.**  The shape actually used in the paper's proof
of Theorem 7.1 and in spine.md Section 3.2, Step 5.

`hC` now says what initial Stage C really produces for a batch record: either a
negative result, or the record is saved as a failure and hence (X6) becomes an
input of B fallback and afterwards of the final C shards, which are all
negative (`hFb`).  Both branches are contradictory.
-/
theorem assembly_fallback
    (seed recA recMid recFine recBat recFb : Reg → Prop)
    (h0   : ∀ H, Exact H → Ext H → ∃ B, seed B ∧ mem B H)
    (hA   : ∀ B H, seed B → Exact H → mem B H → ∃ R, recA R ∧ mem R H)
    (hBm  : ∀ R H, recA R → Exact H → mem R H → ∃ M, recMid M ∧ mem M H)
    (hBf  : ∀ M H, recMid M → Exact H → mem M H → ∃ F, recFine F ∧ mem F H)
    (hBat : ∀ F H, recFine F → Exact H → mem F H → ∃ U, recBat U ∧ mem U H)
    (hC   : ∀ U, recBat U → ∀ H, mem U H → ¬ Ext H ∨ ∃ V, recFb V ∧ mem V H)
    (hFb  : ∀ V, recFb V → ∀ H, mem V H → ¬ Ext H) :
    ¬ ∃ H, Exact H ∧ Ext H := by
  rintro ⟨H, hExact, hExt⟩
  obtain ⟨B, hB, hBH⟩ := h0 H hExact hExt
  obtain ⟨R, hR, hRH⟩ := hA B H hB hExact hBH
  obtain ⟨M, hM, hMH⟩ := hBm R H hR hExact hRH
  obtain ⟨F, hF, hFH⟩ := hBf M H hM hExact hMH
  obtain ⟨U, hU, hUH⟩ := hBat F H hF hExact hFH
  rcases hC U hU H hUH with hneg | ⟨V, hV, hVH⟩
  · exact hneg hExt
  · exact (hFb V hV H hVH) hExt

/-! ## What a refinement pass can and cannot do

The two facts below are the abstract content of Proposition 5.7 / Corollary 5.8
and of the "unresolved is never an exclusion" rule.  They are included because
they are the only properties of the stage relation the assembly relies on, and
they are cheap to state exactly. -/

/-- A refinement relation between region families: every extendible exact matrix
in a source region is in some target region.  This is spine.md's `⊒`. -/
def Refines (src tgt : Reg → Prop) : Prop :=
  ∀ R H, src R → Exact H → mem R H → ∃ S, tgt S ∧ mem S H

/-- Refinement is transitive.  This is what lets two B passes be composed. -/
theorem refines_trans {src mid tgt : Reg → Prop}
    (h1 : Refines mem Exact src mid) (h2 : Refines mem Exact mid tgt) :
    Refines mem Exact src tgt := by
  intro R H hR hE hRH
  obtain ⟨M, hM, hMH⟩ := h1 R H hR hE hRH
  exact h2 M H hM hE hMH

/-- A family with no extendible member excludes.  Stated to make explicit that
nothing but `Ext`-free-ness is exported by Stage C. -/
def Excludes (fam : Reg → Prop) : Prop :=
  ∀ R, fam R → ∀ H, mem R H → ¬ Ext H

/-- If a family refines into an excluding family then no exact matrix in it is
extendible.  (Exactness of the candidate must be supplied: a non-exact matrix
has no reason to be covered by anything, which is exactly the paper's insistence
that every stage acts on exact solutions only.) -/
theorem excludes_of_refines {src tgt : Reg → Prop}
    (h1 : Refines mem Exact src tgt) (h2 : Excludes mem Ext tgt) :
    ∀ R H, src R → Exact H → mem R H → ¬ Ext H := by
  intro R H hR hE hRH hExt
  obtain ⟨S, hS, hSH⟩ := h1 R H hR hE hRH
  exact (h2 S hS H hSH) hExt

end Mub6Assembly
