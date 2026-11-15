/-
Mub6/Gap.lean — circular multisets, their gaps, and paper Lemma 2.5
("Stability of circular gaps").

Paper locator: §2.2, Lemma 2.5, verbatim:
  "If each point of one circular multiset is matched to a point of another at circular
   distance at most δ, their gaps differ by at most 2δ."
Proof locator: §2.2, immediately after Lemma 2.5:
  "Take an empty open arc of length L in the first multiset. If L > 2δ, trim δ from each end.
   A point of the second multiset inside the remaining open arc would have its matched first
   point in the original empty arc, a contradiction. Hence the second gap is at least L − 2δ.
   If L ≤ 2δ, the same lower bound follows from nonnegativity. Apply this to a largest gap and
   then interchange the two multisets. No preservation of the sorted order is used."

Design notes (recorded in reports/statements.md):
* The paper defines (§2.2) "The gap of a finite circular multiset is its largest circular gap.
  Equivalently, it is the greatest length of an open arc containing no point of the multiset.
  Points are counted with multiplicity when sorted; a repeated point contributes a zero gap."
  We take the *arc* definition (`circGap` below), which is insensitive to multiplicity, and we
  therefore state the lemma for `Finset ℝ` (a finite set of real representatives of classes mod 1)
  rather than for a multiset.  This loses nothing: an empty open arc is empty whether or not a
  point is repeated, so the gap, its stability, and the use made of it in Lemma 2.6 only ever
  refer to the underlying set of classes.
* "matched ... at circular distance at most δ" is read as: every point of one multiset has a
  matched point of the other within circular distance δ.  The paper's proof uses only one
  direction of the matching at a time (`NearMap`), and the difference form `circGap_stability`
  keeps both directions as hypotheses, so the difference form is exactly the paper's statement.
  The transfer form `isEmptyArc_transfer` is *stronger* than the paper's step (it needs no
  matching of the other multiset at all); it is the form Lemma 2.6 actually consumes.
* "circular distance at most δ" is `CircDistLE x y δ`, i.e. some integer representative of
  `x - y` has modulus at most δ; no wrapping convention is imposed and no choice of lifts is
  needed.
-/
import Mathlib

namespace Mub6

/-- `CircDistLE x y δ`: the points `x y : ℝ` are at circular distance at most `δ` on `ℝ/ℤ`,
i.e. some integer translate of `x - y` has modulus at most `δ`. -/
def CircDistLE (x y δ : ℝ) : Prop := ∃ m : ℤ, |x - y - (m : ℝ)| ≤ δ

/-- `IsEmptyArc A a L`: the open arc `(a, a+L)` of the circle `ℝ/ℤ` contains no point of the
finite circular multiset `A` (given by real representatives mod 1).  Every point of the circle
has representatives `x - m`, `m : ℤ`, so the quantification over `m` is exactly membership of the
class of `x` in the arc. -/
def IsEmptyArc (A : Finset ℝ) (a L : ℝ) : Prop :=
  ∀ x ∈ A, ∀ m : ℤ, ¬ (a < x - (m : ℝ) ∧ x - (m : ℝ) < a + L)

/-- `NearMap A B δ`: every point of `B` is within circular distance `δ` of a point of `A`.
This is one half of the paper's "matched pointwise at circular distance at most δ"; the paper's
proof of Lemma 2.5 uses only this half in each application. -/
def NearMap (A B : Finset ℝ) (δ : ℝ) : Prop :=
  ∀ y ∈ B, ∃ x ∈ A, CircDistLE x y δ

/-- **Paper Lemma 2.5, transfer form** (the content of the paper's first two sentences).

If every point of `B` is within circular distance `δ` of a point of `A`, then an empty arc of
`A` of length `L` produces an empty arc of `B` of length `L - 2δ` (the paper's "trim δ from each
end"; negative lengths mean the trimmed arc is empty for trivial reasons, which is the paper's
"If L ≤ 2δ, the same lower bound follows from nonnegativity"). -/
theorem isEmptyArc_transfer {A B : Finset ℝ} {δ : ℝ} (h : NearMap A B δ)
    {a L : ℝ} (hA : IsEmptyArc A a L) : IsEmptyArc B (a + δ) (L - 2 * δ) := by
  intro y hy m hmem
  obtain ⟨x, hx, k, hk⟩ := h y hy
  have hk1 : -δ ≤ x - y - (k : ℝ) := (abs_le.mp hk).1
  have hk2 : x - y - (k : ℝ) ≤ δ := (abs_le.mp hk).2
  have hkey : x - ((m + k : ℤ) : ℝ) = (x - y - (k : ℝ)) + (y - (m : ℝ)) := by
    push_cast
    ring
  have h1 : a < x - ((m + k : ℤ) : ℝ) := by
    rw [hkey]
    linarith [hmem.1, hk1]
  have h2 : x - ((m + k : ℤ) : ℝ) < a + L := by
    rw [hkey]
    linarith [hmem.2, hk2]
  exact hA x hx (m + k) ⟨h1, h2⟩

/-- `GapLE A t`: `t` is an upper bound for the gap of `A`, i.e. every empty open arc of `A` has
length at most `t`.  The least such `t` is `circGap A`. -/
def GapLE (A : Finset ℝ) (t : ℝ) : Prop := ∀ a L, IsEmptyArc A a L → L ≤ t

/-- **Paper Lemma 2.5, one-sided form, as used by Lemma 2.6**: if the points of `A` are matched
by points of `B` at circular distance `δ` (`NearMap B A δ`), then an upper bound `t` for the gap
of `A` becomes the upper bound `t + 2δ` for the gap of `B`. -/
theorem gapLE_transfer {A B : Finset ℝ} {δ : ℝ} (h : NearMap B A δ) {t : ℝ}
    (ht : GapLE A t) : GapLE B (t + 2 * δ) := by
  intro a L hL
  have h' : L - 2 * δ ≤ t := ht (a + δ) (L - 2 * δ) (isEmptyArc_transfer h hL)
  linarith

/-- Any empty arc of a nonempty circular multiset has length at most `1`: every open arc of
length strictly greater than one contains a representative of any given point. -/
theorem IsEmptyArc.le_one {A : Finset ℝ} (hA : A.Nonempty) {a L : ℝ} (h : IsEmptyArc A a L) :
    L ≤ 1 := by
  by_contra hle
  have hlt : 1 < L := not_le.mp hle
  obtain ⟨x, hx⟩ := hA
  have h1 : ((⌊x - a⌋ : ℤ) : ℝ) ≤ x - a := Int.floor_le (x - a)
  have h2 : x - a < ((⌊x - a⌋ : ℤ) : ℝ) + 1 := Int.lt_floor_add_one (x - a)
  rcases lt_or_eq_of_le h1 with hlt | heq
  · refine h x hx ⌊x - a⌋ ⟨?_, ?_⟩
    · linarith
    · linarith
  · refine h x hx (⌊x - a⌋ - 1) ⟨?_, ?_⟩
    · push_cast
      linarith
    · push_cast
      linarith

/-- The set of lengths of empty arcs of a nonempty circular multiset is bounded above. -/
theorem bddAbove_gapSet {A : Finset ℝ} (hA : A.Nonempty) :
    BddAbove {L : ℝ | ∃ a, IsEmptyArc A a L} :=
  ⟨1, by rintro L ⟨a, ha⟩; exact IsEmptyArc.le_one hA ha⟩

/-- The set of lengths of empty arcs is nonempty (the empty arc of length `0`). -/
theorem gapSet_nonempty (A : Finset ℝ) : {L : ℝ | ∃ a, IsEmptyArc A a L}.Nonempty :=
  ⟨0, 0, by
    intro x _ m hmem
    linarith [hmem.1, hmem.2]⟩

/-- `circGap A`: the paper's gap of a finite circular multiset, "the greatest length of an open
arc containing no point of the multiset". -/
noncomputable def circGap (A : Finset ℝ) : ℝ := sSup {L : ℝ | ∃ a, IsEmptyArc A a L}

/-- The gap of `A` is an upper bound for the lengths of empty arcs of `A`. -/
theorem le_circGap {A : Finset ℝ} (hA : A.Nonempty) {a L : ℝ} (h : IsEmptyArc A a L) :
    L ≤ circGap A :=
  le_csSup (bddAbove_gapSet hA) ⟨a, h⟩

/-- Any upper bound for the lengths of empty arcs bounds the gap. -/
theorem circGap_le {A : Finset ℝ} {t : ℝ} (h : GapLE A t) : circGap A ≤ t :=
  csSup_le (gapSet_nonempty A) (by rintro L ⟨a, ha⟩; exact h a L ha)

/-- **Paper Lemma 2.5** ("Stability of circular gaps"), literal difference form.

If the points of `A` and `B` are matched pointwise at circular distance at most `δ` — both
directions of the matching are kept here, as in the paper's "interchange the two multisets" —
then the gaps of `A` and `B` differ by at most `2δ`. -/
theorem circGap_stability {A B : Finset ℝ} {δ : ℝ} (hA : A.Nonempty) (hB : B.Nonempty)
    (h : NearMap A B δ) (h' : NearMap B A δ) :
    |circGap A - circGap B| ≤ 2 * δ := by
  have hBA : circGap B ≤ circGap A + 2 * δ :=
    circGap_le (gapLE_transfer h' (fun a L hL => le_circGap hA hL))
  have hAB : circGap A ≤ circGap B + 2 * δ :=
    circGap_le (gapLE_transfer h (fun a L hL => le_circGap hB hL))
  rw [abs_le]
  constructor <;> linarith

/-- Sanity check: the gap of a nonempty circular multiset is at most `1`. -/
theorem circGap_le_one {A : Finset ℝ} (hA : A.Nonempty) : circGap A ≤ 1 :=
  circGap_le (fun _ _ hL => IsEmptyArc.le_one hA hL)

end Mub6
