import Mathlib

namespace Mub6
namespace AssemblyScoped

/-- A closed axis-aligned box in `ℝ^n`: the paper's *cell*, a product of closed bin intervals. -/
structure Box (n : ℕ) where
  lo : Fin n → ℝ
  hi : Fin n → ℝ
  hle : ∀ j, lo j ≤ hi j

namespace Box

variable {n : ℕ}

/-- Membership in a closed box: coordinatewise closed intervals, so boundaries belong to both
neighbours and no point is lost at a shared face. -/
def mem (B : Box n) (x : Fin n → ℝ) : Prop := ∀ j, B.lo j ≤ x j ∧ x j ≤ B.hi j

/-- Midpoint of coordinate `j`, the subdivision face. -/
noncomputable def mid (B : Box n) (j : Fin n) : ℝ := (B.lo j + B.hi j) / 2

theorem lo_le_mid (B : Box n) (j : Fin n) : B.lo j ≤ B.mid j := by
  have := B.hle j; rw [mid]; linarith

theorem mid_le_hi (B : Box n) (j : Fin n) : B.mid j ≤ B.hi j := by
  have := B.hle j; rw [mid]; linarith

/-- The `2^n` children of a cell, each halving one coordinate: `k j = true` selects the upper
closed half `[mid j, hi j]`, `k j = false` the lower closed half `[lo j, mid j]`. -/
noncomputable def split (B : Box n) (k : Fin n → Bool) : Box n where
  lo := fun j => Bool.rec (B.lo j) (B.mid j) (k j)
  hi := fun j => Bool.rec (B.mid j) (B.hi j) (k j)
  hle := by
    intro j
    cases h : k j
    · exact B.lo_le_mid j
    · exact B.mid_le_hi j

theorem mem_split_of (B : Box n) {k : Fin n → Bool} {x : Fin n → ℝ}
    (h : ∀ j, (k j = true → B.mid j ≤ x j ∧ x j ≤ B.hi j) ∧
              (k j = false → B.lo j ≤ x j ∧ x j ≤ B.mid j)) : (B.split k).mem x := by
  intro j
  cases hk : k j
  · simpa only [split, hk] using (h j).2 hk
  · simpa only [split, hk] using (h j).1 hk

/-- **No gaps.**  The children cover the parent: every point of a closed box lies in at least one
child of every subdivision.  A shared face point lies in both neighbours, which is why the children
are closed intervals and why the cover is an inclusion and not a partition. -/
theorem mem_split (B : Box n) {x : Fin n → ℝ} (hx : B.mem x) :
    ∃ k : Fin n → Bool, (B.split k).mem x := by
  classical
  refine ⟨fun j => if B.mid j ≤ x j then true else false, mem_split_of B ?_⟩
  intro j
  by_cases h : B.mid j ≤ x j
  · have hk : (if B.mid j ≤ x j then (true : Bool) else false) = true := if_pos h
    rw [hk]
    exact ⟨fun _ => ⟨h, (hx j).2⟩, fun h' => absurd h' (by simp)⟩
  · have hk : (if B.mid j ≤ x j then (true : Bool) else false) = false := if_neg h
    rw [hk]
    exact ⟨fun h' => absurd h' (by simp), fun _ => ⟨(hx j).1, le_of_lt (lt_of_not_ge h)⟩⟩

end Box


open Box

/-! ## The arithmetic half of Proposition 2.10 -/

/-- **Seed-bin arithmetic.**  Nine coordinates, each within half a bin of width `1/112` of its
written midpoint, give Euclidean distance at most `3/224 = sqrt 9 / (2 * 112)`; that is strictly
below the certified seed radius `0.032`.

This is the only *numerical* statement in the assembly that is fully checkable here: it is the
paper's "`sqrt 9 /(2N) = 3/224 < 0.032`", proved rather than quoted.  The remaining `0.0320001`
of Proposition 2.10 is the Section A bound on the nine binary midpoint phases (joint error below
`10^-14`), and is *not* formalised here. -/
theorem seed_bin_dist_le {x m : Fin 9 → ℝ} (h : ∀ j, |x j - m j| ≤ 1 / (2 * 112)) :
    Real.sqrt (∑ j, (x j - m j) ^ 2) ≤ 3 / 224 := by
  have hterm : ∀ j, (x j - m j) ^ 2 ≤ (1 / 224) ^ 2 := by
    intro j
    have h1 : |x j - m j| ≤ 1 / 224 := by
      have := h j; norm_num at this ⊢; linarith
    have h2 : |x j - m j| ^ 2 ≤ (1 / 224) ^ 2 := by nlinarith [abs_nonneg (x j - m j)]
    simpa [sq_abs] using h2
  have hsum : (∑ j, (x j - m j) ^ 2) ≤ 9 * (1 / 224) ^ 2 := by
    calc (∑ j, (x j - m j) ^ 2) ≤ ∑ _j : Fin 9, (1 / 224) ^ 2 := Finset.sum_le_sum (fun j _ => hterm j)
      _ = 9 * (1 / 224) ^ 2 := by simp [Finset.sum_const, Finset.card_univ]
  calc Real.sqrt (∑ j, (x j - m j) ^ 2) ≤ Real.sqrt (9 * (1 / 224) ^ 2) := Real.sqrt_le_sqrt hsum
    _ = 3 / 224 := by
        rw [show (9 : ℝ) * (1 / 224) ^ 2 = (3 / 224) ^ 2 by norm_num,
          Real.sqrt_sq (by norm_num)]

/-- `3/224 < 0.032`: the seed radius of Proposition 2.10 really is an upper bound for the bin
radius, with room to spare. -/
theorem seed_bin_lt_radius : (3 / 224 : ℝ) < 0.032 := by norm_num

/-- **Stage A: one cell-tree certificate over a seed ball.**

`S : Pt → ℝ^9` assigns to a point its nine seed phase coordinates; `ext` is "extendible by two
further mutually unbiased bases" (the property Stage C refutes); `mem b x` says the point lies in
the closed ball of record `b`; `𝔅` is the family of records written by the run.

The three constructors are the paper's three terminal verdicts for a cell, and there is no fourth:
a cell that hits the depth cap, fails a frame construction or fails coverage is *unresolved*, and
an unresolved cell is not a certificate (so it has no constructor here).  This is the formal
content of "zero unresolved cells". -/
inductive CellTree {Pt Ball : Type*} (n : ℕ) (S : Pt → (Fin n → ℝ))
    (ext : Pt → Prop) (mem : Ball → Pt → Prop) (𝔅 : Set Ball) : Box n → Type _ where
  /-- A certified necessary-condition test failed on this cell (paper: Lemma 3.8 norm test or
  Lemma 3.9 directional test): no extendible point has seed coordinates in the cell. -/
  | excl {B : Box n} (h : ∀ x, B.mem (S x) → ¬ ext x) : CellTree n S ext mem 𝔅 B
  /-- A certified phase ball covers the cell: every extendible point with seed coordinates in the
  cell lies in the ball of record `b`. -/
  | ball {B : Box n} (b : Ball) (hb : b ∈ 𝔅) (h : ∀ x, B.mem (S x) → ext x → mem b x) :
      CellTree n S ext mem 𝔅 B
  /-- A subdivision: all `2^n` closed children are certified. -/
  | node {B : Box n} (c : (k : Fin n → Bool) → CellTree n S ext mem 𝔅 (B.split k)) :
      CellTree n S ext mem 𝔅 B

/-- **The branch-following argument of Proposition 3.11.**  A complete cell tree over a box covers
every extendible point whose seed coordinates lie in that box.

This is the paper's sentence: "the branch followed by a feasible completion cannot end in exclusion,
and therefore ends in coverage".  The only geometric input is `Box.mem_split`, i.e. that the `2^n`
closed children cover the parent without gaps.  The induction is over the processed cell tree and
terminates because every `node`'s children are strict subterms: a `CellTree` is a finite term by
construction, so no depth counter or cap is needed in the proof (and an infinite regress would not be
a term of this type, which is exactly what "the traversal closed" means). -/
theorem CellTree.covers {Pt Ball : Type*} {n : ℕ} {S : Pt → (Fin n → ℝ)}
    {ext : Pt → Prop} {mem : Ball → Pt → Prop} {𝔅 : Set Ball} {B : Box n}
    (t : CellTree n S ext mem 𝔅 B) :
    ∀ x, B.mem (S x) → ext x → ∃ b ∈ 𝔅, mem b x :=
  CellTree.rec
    (motive := fun B _ => ∀ x, B.mem (S x) → ext x → ∃ b ∈ 𝔅, mem b x)
    (fun {_} h x hx hxe => absurd hxe (h x hx))
    (fun {_} b hb h x hx hxe => ⟨b, hb, h x hx hxe⟩)
    (fun {B} c ih x hx hxe =>
      let ⟨k, hk⟩ := Box.mem_split (B := B) hx
      ih k x hk hxe)
    t

/-! ## The finite refinement chase (Stage B, Stage C) -/

/-- **One pass of the refinement chase.**  `frontier i` is the list of records still live after
pass `i`.  Every record on a live frontier must be *refined*: each exact point in its ball lies in
the ball of a record on the next frontier.  A parent that failed its outside test, hit a grid cap,
or whose merge mediator / transport was never archived has no such refinement and cannot be handed
on -- it must reappear on a later frontier, or the chain breaks.  This is the precise sense in which
the 1452 unexploded boxes of `bad10#0` are *not* coverage. -/
theorem chain_excluded {Pt Ball : Type*} {mem : Ball → Pt → Prop} {exact ext : Pt → Prop}
    {Neg : Ball → Prop}
    (hneg : ∀ b, Neg b → ∀ x, mem b x → ¬ ext x)
    (hext : ∀ x, ext x → exact x)
    (k : ℕ) (frontier : ℕ → List Ball)
    (hstep : ∀ i, i < k → ∀ b ∈ frontier i, ∀ x, mem b x → exact x →
      ∃ b' ∈ frontier (i + 1), mem b' x)
    (hfinal : ∀ b ∈ frontier k, Neg b) :
    ∀ b ∈ frontier 0, ∀ x, mem b x → ¬ ext x := by
  intro b hb x hx hxe
  have hex : exact x := hext x hxe
  have key : ∀ i, i ≤ k → ∃ b' ∈ frontier i, mem b' x := by
    intro i hi
    induction i with
    | zero => exact ⟨b, hb, hx⟩
    | succ i ih =>
        obtain ⟨b', hb', hb'x⟩ := ih (Nat.le_of_succ_le hi)
        exact hstep i (Nat.lt_of_succ_le hi) b' hb' x hb'x hex
  obtain ⟨b', hb', hb'x⟩ := key k le_rfl
  exact hneg b' (hfinal b' hb') x hb'x hxe

/-- **The chase with the paper's equivalences.**  Every coverage link of the preprint holds only up
to the signed-permutation, transpose and rephasing equivalences of Lemma 2.2, and extendibility is
invariant under them.  So a refinement step carries a *different* representative on each pass, and
the chase must transport along `emb`.

`hstep` is the record-level obligation: each exact point of a live record is equivalent to an exact
point of a record on the next frontier.  `hinv` is Lemma 4.7's invariance of extendibility, and is
what allows the terminal negative verdict to be pulled back. -/
theorem chain_excluded_emb {Pt Ball : Type*} {mem : Ball → Pt → Prop} {exact ext : Pt → Prop}
    {Neg : Ball → Prop} {emb : Pt → Pt → Prop}
    (hneg : ∀ b, Neg b → ∀ x, mem b x → ¬ ext x)
    (hext : ∀ x, ext x → exact x)
    (hinv : ∀ x y, emb x y → (ext x ↔ ext y))
    (hrefl : ∀ x, emb x x)
    (htrans : ∀ x y z, emb x y → emb y z → emb x z)
    (k : ℕ) (frontier : ℕ → List Ball)
    (hstep : ∀ i, i < k → ∀ b ∈ frontier i, ∀ x, mem b x → exact x →
      ∃ b' ∈ frontier (i + 1), ∃ y, emb x y ∧ mem b' y)
    (hfinal : ∀ b ∈ frontier k, Neg b) :
    ∀ b ∈ frontier 0, ∀ x, mem b x → ¬ ext x := by
  intro b hb x hx hxe
  have key : ∀ i, i ≤ k → ∃ (b' : Ball) (y : Pt), b' ∈ frontier i ∧ mem b' y ∧ emb x y ∧ ext y := by
    intro i hi
    induction i with
    | zero => exact ⟨b, x, hb, hx, hrefl x, hxe⟩
    | succ i ih =>
        obtain ⟨b', y, hb', hb'y, hxy, hye⟩ := ih (Nat.le_of_succ_le hi)
        obtain ⟨b'', hb'', z, hyz, hb''z⟩ :=
          hstep i (Nat.lt_of_succ_le hi) b' hb' y hb'y (hext y hye)
        exact ⟨b'', z, hb'', hb''z, htrans x y z hxy hyz, (hinv y z hyz).1 hye⟩
  obtain ⟨b', y, hb', hb'y, hxy, hye⟩ := key k le_rfl
  exact hneg b' (hfinal b' hb') y hb'y hye

/-! ## The scoped assembly, as a bundle of named interfaces -/

/-- **The assembly interfaces.**  Every field is a separately falsifiable proposition about explicit
data; none of them is proved in this file.  The two that are arithmetic-level (checkable against
records by a program) are `hball_le` and `hstep`; `hseed`, `hneg` and `hext` contain the analytic
content of the paper (Propositions 2.10 and 6.9, and exactness of extendible points).

* `mem`, `ext`, `exact`: the geometric carrier.  `ext x` is "x is extendible by two further
  mutually unbiased bases"; `exact x` is "x is an exact complex Hadamard matrix"; `mem b x` is
  "x lies in the closed ball of record `b`".
* `seeds`, `S`, `hseed`: **Proposition 2.10**.  Every extendible point is `emb`-equivalent to a point
  whose nine seed coordinates lie in one of the written seed balls.  Unproved here: it is the output
  of the covout traversal.
* `𝔅`, `tree`: **Stage A**, `Proposition 3.11`.  A complete cell tree over each seed ball, every
  leaf a certified exclusion or a certified phase ball, no unresolved leaf.
* `𝔅 ⊆ coarse`: the atlas write-out of **Proposition 4.16** (the coarse records include every ball
  written by the A stage).
* `frontier`, `hstep`: **Stage B**, `Proposition 5.7` and `Corollary 5.8`, iterated over the
  mid / fine / initial / fallback / final passes of Section 7.2.
* `Neg`, `hfinal`, `hneg`: **Stage C**, `Proposition 6.9`.  Every record of the last frontier carries
  a completed negative graph search, and a negative verdict excludes extendibility in that ball.
* `hext`: 4-MUB extendibility implies exactness (definitional in the paper, an interface here). -/
structure Chain (Pt Ball : Type*) where
  /-- Closed-ball containment of a record. -/
  mem : Ball → Pt → Prop
  /-- `x` is an exact complex Hadamard matrix (dephased, first row/column one). -/
  exact : Pt → Prop
  /-- `x` is extendible by two further mutually unbiased orthonormal bases. -/
  ext : Pt → Prop
  /-- The completed negative Stage-C verdict of a record. -/
  Neg : Ball → Prop
  /-- The paper's permitted equivalence on configurations: signed permutations, transposition,
  rephasing (Lemma 2.2). -/
  emb : Pt → Pt → Prop
  /-- `emb` is reflexive. -/
  hemb_refl : ∀ x, emb x x
  /-- `emb` is transitive. -/
  hemb_trans : ∀ x y z, emb x y → emb y z → emb x z
  /-- Extendibility is invariant under `emb` (Lemma 4.7). -/
  hinv : ∀ x y, emb x y → (ext x ↔ ext y)
  /-- The nine seed phase coordinates of a point. -/
  S : Pt → (Fin 9 → ℝ)
  /-- The written seed balls. -/
  seeds : List (Box 9)
  /-- The seed cover: Proposition 2.10, unproved here.  Up to `emb`, as the paper states it. -/
  hseed : ∀ x, ext x → ∃ B ∈ seeds, ∃ y, emb x y ∧ B.mem (S y)
  /-- The balls written by the A stage. -/
  𝔅 : Set Ball
  /-- The Stage-A cell tree of each seed, with no unresolved leaf. -/
  tree : ∀ B, B ∈ seeds → CellTree 9 S ext mem 𝔅 B
  /-- The first Stage-B frontier (the coarse atlas). -/
  coarse : List Ball
  /-- Every A-stage ball is in the coarse atlas (Proposition 4.16's write-out). -/
  hball_le : ∀ b ∈ 𝔅, b ∈ coarse
  /-- Number of refinement passes actually completed. -/
  k : ℕ
  /-- The live records after each pass. -/
  frontier : ℕ → List Ball
  /-- The coarse atlas is the frontier before the first pass. -/
  h0 : frontier 0 = coarse
  /-- The refinement step of each pass: no live record is dropped.

  Two behaviours are allowed, and both are instances of this one field.  A record can be *refined*
  (its points land in the balls of records on the next frontier, up to `emb`), or it can be *failed*:
  the run re-emits it unchanged into the next bad list, so it reappears in `frontier (i+1)` as the
  same record and the field holds with `b' = b`, `y = x` and `hemb_refl`.  What the field forbids is
  dropping a record, or replacing its ball by a different record with no witness -- which is what
  "handing off an unexploded box" means. -/
  hstep : ∀ i, i < k → ∀ b ∈ frontier i, ∀ x, mem b x → exact x →
    ∃ b' ∈ frontier (i + 1), ∃ y, emb x y ∧ mem b' y
  /-- Every record of the last frontier has a completed negative verdict. -/
  hfinal : ∀ b ∈ frontier k, Neg b
  /-- A negative verdict excludes extendibility in the whole closed ball (Proposition 6.9). -/
  hneg : ∀ b, Neg b → ∀ x, mem b x → ¬ ext x
  /-- Extendible points are exact Hadamard matrices. -/
  hext : ∀ x, ext x → exact x

/-- **The scoped assembly.**  If the interfaces of `Chain` hold, no point is extendible.

This is *not* a statement that four MUBs do not exist: every field of `Chain` is an assumption.  It
is the logical skeleton of Theorem 7.1 with its analytic premises exposed as binders, proved once so
that the record-level checks only have to establish the fields. -/
theorem Chain.no_extendible {Pt Ball : Type*} (C : Chain Pt Ball) : ∀ x, ¬ C.ext x := by
  intro x hxe
  obtain ⟨B, hB, y, hxy, hyB⟩ := C.hseed x hxe
  have hye : C.ext y := (C.hinv x y hxy).1 hxe
  obtain ⟨b, hb𝔅, hby⟩ := (C.tree B hB).covers y hyB hye
  have hb0 : b ∈ C.frontier 0 := by rw [C.h0]; exact C.hball_le b hb𝔅
  exact chain_excluded_emb C.hneg C.hext C.hinv C.hemb_refl C.hemb_trans C.k C.frontier
    C.hstep C.hfinal b hb0 y hby hye

/-- **Conditional form.**  If in addition some extendible point exists, contradiction.  The paper's
Theorem 1.1 is this implication applied to the four-MUB configuration, with `hfour` supplied by
Lemma 1.2 and `hseed` by Proposition 2.10. -/
theorem Chain.false_of_four {Pt Ball : Type*} (C : Chain Pt Ball)
    (hfour : ∃ x, C.ext x) : False := by
  obtain ⟨x, hx⟩ := hfour
  exact C.no_extendible x hx

/-! ## Negative controls: no premise of the assembly is decorative -/

/-- **The cap-hit control.**  `CellTreeLive` is `CellTree` with one extra leaf that carries
nothing: a cell that hit the depth cap, a give-up flag, a failed frame construction or a failed
coverage test.  This is exactly what a run emits for an unresolved cell. -/
inductive CellTreeLive {Pt Ball : Type*} (n : ℕ) (S : Pt → (Fin n → ℝ))
    (ext : Pt → Prop) (mem : Ball → Pt → Prop) (𝔅 : Set Ball) : Box n → Type _ where
  | excl {B : Box n} (h : ∀ x, B.mem (S x) → ¬ ext x) : CellTreeLive n S ext mem 𝔅 B
  | ball {B : Box n} (b : Ball) (hb : b ∈ 𝔅) (h : ∀ x, B.mem (S x) → ext x → mem b x) :
      CellTreeLive n S ext mem 𝔅 B
  | node {B : Box n} (c : (k : Fin n → Bool) → CellTreeLive n S ext mem 𝔅 (B.split k)) :
      CellTreeLive n S ext mem 𝔅 B
  | live {B : Box n} : CellTreeLive n S ext mem 𝔅 B

/-- The unit interval `[0,1]`, the smallest Stage-A cell that exercises the cover. -/
noncomputable def segBox : Box 1 := ⟨fun _ => 0, fun _ => 1, fun _ => by norm_num⟩

/-- **The cap-hit control is a real control.**  `CellTreeLive` admits a live root, and for that tree
the analogue of `CellTree.covers` is *false*: an extendible point sits in the cell, the family of
written balls is empty, and nothing follows.  So the missing fourth constructor in `CellTree` --
"the run closed with zero unresolved cells" -- is a premise, not bookkeeping. -/
theorem live_defeats_covers :
    ¬ ∀ t : CellTreeLive 1 (fun x : ℝ => fun _ => x) (fun x => x = 1 / 2)
        (fun (_ : Unit) (x : ℝ) => x = 1 / 2) (∅ : Set Unit) segBox,
      ∀ x, segBox.mem (fun _ => x) → x = 1 / 2 →
        ∃ b ∈ (∅ : Set Unit), (fun (_ : Unit) (x : ℝ) => x = 1 / 2) b x := by
  intro h
  have hx : segBox.mem (fun _ => (1 / 2 : ℝ)) := by
    intro j; simp [segBox]; norm_num
  obtain ⟨b, hb, -⟩ := h CellTreeLive.live (1 / 2) hx rfl
  simpa using hb

/-- Executable spot check of the subdivision: in one dimension the point `1/2` lies in **both**
children of `[0,1]` (the shared closed face), while `1/4` lies only in the lower child.  This is the
boundary case that makes `Box.mem_split` true for closed cells and false for half-open ones. -/
theorem split_boundary_check :
    (segBox.split (fun _ => true)).mem (fun _ => (1 / 2 : ℝ)) ∧
    (segBox.split (fun _ => false)).mem (fun _ => (1 / 2 : ℝ)) ∧
    (segBox.split (fun _ => false)).mem (fun _ => (1 / 4 : ℝ)) ∧
    ¬ (segBox.split (fun _ => true)).mem (fun _ => (1 / 4 : ℝ)) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro j; norm_num [Box.split, Box.mid, segBox]
  · intro j; norm_num [Box.split, Box.mid, segBox]
  · intro j; norm_num [Box.split, Box.mid, segBox]
  · intro h
    have h0 := h 0
    norm_num [Box.split, Box.mid, segBox] at h0

/-! ### Load-bearing checks

Each theorem below exhibits data on which every *data* interface of `Chain` except one holds and the
conclusion of `Chain.no_extendible` fails.  `emb` is taken to be equality, so its three structural
fields (`hemb_refl`, `hemb_trans`, `hinv`) are satisfied automatically; they exist for transport
fidelity and are not empirical claims about the run.  What is being shown is that `hseed`, `hstep`
and `hfinal` are each indispensable: with one of them false the remaining interfaces are consistent
with an extendible point, so no chain of records can replace it.
-/

/-- The unit cube `[0,1]^9`, used for the concrete seed in the checks below. -/
noncomputable def unitCube9 : Box 9 := ⟨fun _ => 0, fun _ => 1, fun _ => by norm_num⟩

/-- **`hseed` is load-bearing.**  With an empty seed list, a single record covering everything and
no terminal verdict, every other interface holds and an extendible point survives.  So the assembly
proves nothing without Proposition 2.10. -/
theorem hseed_needed :
    ∃ (mem : Unit → ℝ → Prop) (Neg : Unit → Prop) (S : ℝ → Fin 9 → ℝ)
      (seeds : List (Box 9)) (𝔅 : Set Unit) (coarse : List Unit) (k : ℕ)
      (frontier : ℕ → List Unit),
      (∀ b ∈ 𝔅, b ∈ coarse) ∧
      (frontier 0 = coarse) ∧
      (∀ i, i < k → ∀ b ∈ frontier i, ∀ x, mem b x → True → ∃ b' ∈ frontier (i + 1), mem b' x) ∧
      (∀ b ∈ frontier k, Neg b) ∧
      (∀ b, Neg b → ∀ x, mem b x → ¬ x = 0) ∧
      (Nonempty (∀ B, B ∈ seeds → CellTree 9 S (fun x => x = 0) mem 𝔅 B)) ∧
      (∃ x : ℝ, x = 0) ∧
      ¬ (∀ x, x = 0 → ∃ B ∈ seeds, B.mem (S x)) := by
  refine ⟨fun _ _ => True, fun _ => False, fun _ _ => 0, [], ∅, [], 0, fun _ => [], ?_, rfl, ?_,
    ?_, ?_, ?_, ⟨0, rfl⟩, ?_⟩
  · simp
  · simp
  · simp
  · simp
  · exact ⟨fun B hB => absurd hB (by simp)⟩
  · intro h
    have := h 0 rfl
    simpa using this

/-- **`hstep` is load-bearing.**  A single record that is neither refined nor re-injected stops the
chase, even with a complete seed cover, a complete Stage-A tree and a terminal verdict on every
frontier record: the record that must be exploded is on the first frontier and nowhere else. -/
theorem hstep_needed :
    ∃ (mem : Unit → ℝ → Prop) (Neg : Unit → Prop) (S : ℝ → Fin 9 → ℝ)
      (seeds : List (Box 9)) (𝔅 : Set Unit) (coarse : List Unit) (k : ℕ)
      (frontier : ℕ → List Unit),
      (∀ b ∈ 𝔅, b ∈ coarse) ∧
      (frontier 0 = coarse) ∧
      (∀ b ∈ frontier k, Neg b) ∧
      (∀ b, Neg b → ∀ x, mem b x → ¬ x = 0) ∧
      (∀ x, x = 0 → ∃ B ∈ seeds, B.mem (S x)) ∧
      (Nonempty (∀ B, B ∈ seeds → CellTree 9 S (fun x => x = 0) mem 𝔅 B)) ∧
      (∃ x : ℝ, x = 0) ∧
      ¬ (∀ i, i < k → ∀ b ∈ frontier i, ∀ x, mem b x → True → ∃ b' ∈ frontier (i + 1), mem b' x) := by
  refine ⟨fun _ _ => True, fun _ => False, fun _ _ => 0, [unitCube9], {()}, [()], 1,
    fun i => if i = 0 then [()] else [], ?_, ?_, ?_, ?_, ?_, ?_, ⟨0, rfl⟩, ?_⟩
  · simp
  · simp
  · simp
  · simp
  · intro x hx
    refine ⟨unitCube9, by simp, ?_⟩
    subst hx
    intro j
    simp [unitCube9]
  · exact ⟨fun B hB => by
      rw [List.mem_singleton] at hB
      subst hB
      exact CellTree.ball () (by simp) (fun x _ _ => trivial)⟩
  · intro h
    have := h 0 (by norm_num) () (by simp) 0 trivial
    simpa using this

/-- **`hfinal` is load-bearing.**  Every interface holds including the refinement step, but with no
terminal negative verdict on the last frontier the extendible point survives.  So Stage C cannot be
replaced by "the record was processed". -/
theorem hfinal_needed :
    ∃ (mem : Unit → ℝ → Prop) (Neg : Unit → Prop) (S : ℝ → Fin 9 → ℝ)
      (seeds : List (Box 9)) (𝔅 : Set Unit) (coarse : List Unit) (k : ℕ)
      (frontier : ℕ → List Unit),
      (∀ b ∈ 𝔅, b ∈ coarse) ∧
      (frontier 0 = coarse) ∧
      (∀ i, i < k → ∀ b ∈ frontier i, ∀ x, mem b x → True → ∃ b' ∈ frontier (i + 1), mem b' x) ∧
      (∀ b, Neg b → ∀ x, mem b x → ¬ x = 0) ∧
      (∀ x, x = 0 → ∃ B ∈ seeds, B.mem (S x)) ∧
      (Nonempty (∀ B, B ∈ seeds → CellTree 9 S (fun x => x = 0) mem 𝔅 B)) ∧
      (∃ x : ℝ, x = 0) ∧
      ¬ (∀ b ∈ frontier k, Neg b) := by
  refine ⟨fun _ _ => True, fun _ => False, fun _ _ => 0, [unitCube9], {()}, [()], 1,
    fun _ => [()], ?_, ?_, ?_, ?_, ?_, ?_, ⟨0, rfl⟩, ?_⟩
  · simp
  · simp
  · intro i hi b hb x hx hex
    exact ⟨(), by simp, trivial⟩
  · simp
  · intro x hx
    refine ⟨unitCube9, by simp, ?_⟩
    subst hx
    intro j
    simp [unitCube9]
  · exact ⟨fun B hB => by
      rw [List.mem_singleton] at hB
      subst hB
      exact CellTree.ball () (by simp) (fun x _ _ => trivial)⟩
  · intro h
    have := h () (by simp)
    simpa using this

/-- **Consistency of the interfaces.**  `Chain` is inhabited by non-degenerate data: a real seed cube, a
real Stage-A ball leaf, a one-pass frontier, a real refinement step and a terminal verdict.  The
only field that is empty is `ext` itself, which is forced by `Chain.no_extendible`: any inhabited
`Chain` has no extendible point.  So the conjunction of interface fields is satisfiable and
`Chain.no_extendible` is not an implication over an empty class of inputs. -/
noncomputable def consistentChain : Chain ℝ Unit where
  mem := fun _ _ => True
  exact := fun _ => True
  ext := fun _ => False
  Neg := fun _ => True
  emb := fun _ _ => True
  hemb_refl := fun _ => trivial
  hemb_trans := fun _ _ _ _ _ => trivial
  hinv := fun _ _ _ => ⟨fun h => h, fun h => h⟩
  S := fun _ _ => 0
  seeds := [unitCube9]
  hseed := fun x hx => absurd hx (by simp)
  𝔅 := {()}
  tree := fun B hB => by
    rw [List.mem_singleton] at hB
    subst hB
    exact CellTree.ball () (by simp) (fun x _ _ => trivial)
  coarse := [()]
  hball_le := by intro b hb; simp
  k := 1
  frontier := fun _ => [()]
  h0 := rfl
  hstep := fun i hi b hb x hx hex => ⟨(), by simp, x, trivial, trivial⟩
  hfinal := fun _ _ => trivial
  hneg := fun _ _ _ _ h => h
  hext := fun x hx => trivial

/-- The consistency witness really does satisfy the assembly's conclusion. -/
theorem consistentChain_no_extendible : ∀ x : ℝ, ¬ consistentChain.ext x :=
  consistentChain.no_extendible

end AssemblyScoped
end Mub6



