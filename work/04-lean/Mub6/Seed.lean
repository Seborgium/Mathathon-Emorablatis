/-
Mub6/Seed.lean — §2.2: the gap of a finite circular multiset and its stability (Lemma 2.5).

In this phase the file carries exactly one paper claim, Lemma 2.5, in two forms:

* `gap_stability` — the paper's statement: two circular multisets matched pointwise at circular
  distance at most `δ` have gaps differing by at most `2δ`, with an ARBITRARY matching.  It is
  transcribed and left unproved (`sorry`, listed in reports/status.md).
* `seedGap_lipschitz` — the special case in which the matching is the identity on the index set.
  This one is proved, and it is the form actually consumed by Lemma 2.6 (the two lists are compared
  after sorting, index by index).  The hypothesis is *stronger* than the paper's, so this is a
  strictly weaker theorem and is recorded as such in reports/statements.md.

The carrier `SeedList` is the paper's nine-phase / five-varying-phase seed list: six circular points
`(0, x₁, …, x₅)`.  `seedGap` is the paper's gap: the largest of the six arcs, where the arc from the
last point wraps to `1` (equivalently to `0` on the circle).

PROOF STATUS: mixed — `seedGap_lipschitz` and everything it uses are proved; `gap_stability` is
statement-only.
-/
import Mub6.Basic

namespace Mub6

open Finset

/-- The paper's dephased seed list: the fixed zero plus five varying phases, in cycles. -/
abbrev SeedList := Fin 6 → ℝ

/-- Circular distance on phases in cycles.  For `s, t ∈ [0,1)` this is the distance on `ℝ/ℤ`;
the definition is total but only the restricted case is used. -/
noncomputable def circularDist (s t : ℝ) : ℝ :=
  let d := |s - t|
  min d (1 - d)

/-- The `j`-th arc of the seed list: from `x j` to the next point, where the last arc wraps from
`x 5` to `1` (`=` `0` on the circle). -/
noncomputable def arcVal (x : SeedList) (j : Fin 6) : ℝ :=
  if h : (j : ℕ) + 1 < 6 then x ⟨(j : ℕ) + 1, h⟩ - x j else 1 - x j

/-- The paper's gap: the largest circular gap of the six-point multiset `(0, x₁, …, x₅)`. -/
noncomputable def seedGap (x : SeedList) : ℝ :=
  (Finset.univ : Finset (Fin 6)).sup' ⟨0, Finset.mem_univ 0⟩ (arcVal x)

/-! ### A tool: the maximum of a finite family is Lipschitz for the sup distance -/

theorem abs_sup'_sub_sup'_le {ι : Type*} (s : Finset ι) (hs : s.Nonempty) (f g : ι → ℝ)
    {δ : ℝ} (h : ∀ i ∈ s, |f i - g i| ≤ δ) (hδ : 0 ≤ δ) :
    |s.sup' hs f - s.sup' hs g| ≤ δ := by
  have h1 : s.sup' hs f ≤ s.sup' hs g + δ := by
    refine Finset.sup'_le hs f (fun i hi => ?_)
    have h2 : f i - g i ≤ δ := (abs_le.mp (h i hi)).2
    have h3 : g i ≤ s.sup' hs g := Finset.le_sup' g hi
    linarith
  have h2 : s.sup' hs g ≤ s.sup' hs f + δ := by
    refine Finset.sup'_le hs g (fun i hi => ?_)
    have h3 : g i - f i ≤ δ := by
      have := (abs_le.mp (h i hi)).1
      linarith
    have h4 : f i ≤ s.sup' hs f := Finset.le_sup' f hi
    linarith
  rw [abs_sub_le_iff]
  constructor <;> linarith

/-! ### Lemma 2.5, proved in the index-aligned form -/

theorem arcVal_diff {x y : SeedList} {δ : ℝ} (h : ∀ i, |x i - y i| ≤ δ) (j : Fin 6) :
    |arcVal x j - arcVal y j| ≤ 2 * δ := by
  have hδ : 0 ≤ δ := le_trans (abs_nonneg _) (h 0)
  by_cases hj : (j : ℕ) + 1 < 6
  · have hsub : arcVal x j - arcVal y j
        = (x ⟨(j : ℕ) + 1, hj⟩ - y ⟨(j : ℕ) + 1, hj⟩) - (x j - y j) := by
      simp only [arcVal, dif_pos hj]; ring
    rw [hsub, abs_le]
    have ha := abs_le.mp (h ⟨(j : ℕ) + 1, hj⟩)
    have hb := abs_le.mp (h j)
    constructor <;> linarith [ha.1, ha.2, hb.1, hb.2]
  · have hsub : arcVal x j - arcVal y j = -(x j - y j) := by
      simp only [arcVal, dif_neg hj]; ring
    rw [hsub, abs_neg]
    linarith [h j, hδ]

/-- **Lemma 2.5, index-aligned form (proved).**  If two seed lists agree pointwise to within `δ`,
their largest circular gaps differ by at most `2δ`. -/
theorem seedGap_lipschitz {x y : SeedList} {δ : ℝ} (h : ∀ i, |x i - y i| ≤ δ) :
    |seedGap x - seedGap y| ≤ 2 * δ := by
  have hδ : 0 ≤ δ := le_trans (abs_nonneg _) (h 0)
  exact abs_sup'_sub_sup'_le _ ⟨0, Finset.mem_univ 0⟩ (arcVal x) (arcVal y)
    (fun j _ => arcVal_diff h j) (by linarith)

/-- **Lemma 2.5, the paper's form (STATEMENT-ONLY).**  If each point of one circular multiset is
matched to a point of another at circular distance at most `δ`, their gaps differ by at most `2δ`.

The hypotheses `hx`, `hy` record that `x` and `y` are the sorted representatives of their circular
multisets, so that `seedGap` really is the gap of the multiset (the paper's Lemma 2.4 arrangement
supplies exactly such representatives: a fixed zero and an ordered complementary arc). -/
theorem gap_stability (x y : SeedList) {δ : ℝ}
    (hx : Monotone x) (hy : Monotone y) (hx0 : x 0 = 0) (hy0 : y 0 = 0)
    (hx1 : ∀ i, x i < 1) (hy1 : ∀ i, y i < 1)
    (σ : Equiv.Perm (Fin 6))
    (h : ∀ i, circularDist (x i) (y (σ i)) ≤ δ) :
    |seedGap x - seedGap y| ≤ 2 * δ := by
  sorry

#check @Finset.sup'_le
#check @Finset.le_sup'
#check @abs_sub_le_iff

end Mub6
