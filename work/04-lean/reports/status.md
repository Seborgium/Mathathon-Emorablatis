# reports/status.md — proof status (separate from source fidelity)

**This file reports only whether things compile, what remains, and what the result depends on.**
Whether a statement is a faithful transcription of the paper is a different question, answered in
`reports/statements.md`.  A row can be green here and red there, and the two are never merged.

## How everything here was checked

```
cd work/04-lean
LEAN_PATH=$PWD:$LEAN_PATH lean -o Mub6/Basic.olean   Mub6/Basic.lean      # exit 0
LEAN_PATH=$PWD:$LEAN_PATH lean -o Mub6/Hadamard.olean Mub6/Hadamard.lean   # exit 0
LEAN_PATH=$PWD:$LEAN_PATH lean -o Mub6/Seed.olean    Mub6/Seed.lean        # exit 0
LEAN_PATH=$PWD:$LEAN_PATH lean -o Mub6/ThreeMUB.olean Mub6/ThreeMUB.lean   # exit 0
LEAN_PATH=$PWD:$LEAN_PATH lean Mub6/AxiomCheck.lean                        # prints footprints
```

* Lean 4.33.1, `LEAN_PATH` preset to the pre-built shared Mathlib.  **No `lake build` was run**
  (`/opt/mathlib` is root-owned and shared); validation is direct `lean <file>`.
* The `-o` flag matters: `Mub6/Hadamard.lean` etc. `import Mub6.Basic`, which needs
  `Mub6/Basic.olean` beside the source and `$PWD` on `LEAN_PATH`.  Without both, `lean` fails with
  `unknown module prefix 'Mub6'` — not a proof problem, a path problem.
* Compiles were run one file at a time, as required.

## Aggregate

| module | paper content | declarations | proved | statement-only (`sorry`) |
|---|---|---|---|---|
| `Mub6/Basic.lean` | carriers, Def 2.1, (2.1), (2.2) | 10 theorems + 11 defs | 10 | 0 |
| `Mub6/Hadamard.lean` | Lemma 2.2, Lemma 2.3 | 19 theorems + 6 defs | 12 | 7 |
| `Mub6/Seed.lean` | Lemma 2.5 | 4 theorems + 3 defs | 3 | 1 |
| `Mub6/ThreeMUB.lean` | Lemma 1.2 | 15 theorems + 4 defs | 13 | 2 |
| **total** | | **48 theorems** | **38** | **10** |

Three **stub** modules complete the DAG (`Mub6/Completion.lean`, `Mub6/Refine.lean`,
`Mub6/Assembly.lean`).  They compile (`lean` exit 0) and contain no declarations at all, so they
contribute nothing to the counts above and nothing to the axiom footprint.  Their headers state what
belongs in them.

## Declaration-by-declaration

Axiom footprint `S` below abbreviates the three standard axioms `[propext, Classical.choice,
Quot.sound]`; `S+sorry` abbreviates `[propext, sorryAx, Classical.choice, Quot.sound]`.  These are
verbatim `#print axioms` output, not a claim.

### `Mub6/Basic.lean` — compiles, 10/10 proved

| declaration | compiles | remaining goals | axioms |
|---|---|---|---|
| `Dephase_apply` | yes | none | S |
| `Dephase_row_zero` | yes | none | S |
| `Dephase_col_zero` | yes | none | S |
| `Pi_rowSum` | yes | none | S |
| `Pi_colSum` | yes | none | S |
| `Pi_horizontal` | yes | none | S |
| `Pi_idem` | yes | none | S |
| `Pi_fixes_horizontal` | yes | none | S |
| `horizontal_iff_Pi_eq_self` | yes | none | S |
| `sub_Pi_eq_rowcol` | yes | none | S |

Method note (reusable by the rest of T4): every one of these is a polynomial identity in the 36
entries of a `6×6` real matrix.  `simp only [<def>, Fin.sum_univ_six]; ring` expands the explicit
six-term sums and lets `ring` close the goal.  This is why Lemma 2.3 needed no analysis.

### `Mub6/Hadamard.lean` — compiles, 12/19 proved

| declaration | compiles | remaining goals | axioms |
|---|---|---|---|
| `e_add`, `e_zero`, `e_neg` | yes | none | S |
| `e_int`, `e_add_int`, `expMat_int_shift` | yes | none | S |
| `expMat_rowcol_add` | yes | none | S |
| `sum_mul_rowcol_zero` | yes | none | S |
| `frobSqR_nonneg`, `frobSqR_add_of_cross_zero` | yes | none | S |
| `Pi_frobSqR_le` | yes | none | S |
| `expMat_Pi_rephasing` | yes | none | S |
| `extendible_permRows` | yes (with `sorry`) | `Extendible (permRows σ H)` | S+sorry |
| `extendible_permCols` | yes (with `sorry`) | `Extendible (permCols τ H)` | S+sorry |
| `extendible_rephaseRows` | yes (with `sorry`) | `Extendible (rephaseRows r H)` | S+sorry |
| `extendible_rephaseCols` | yes (with `sorry`) | `Extendible (rephaseCols c H)` | S+sorry |
| `extendible_conjMat` | yes (with `sorry`) | `Extendible (conjMat H)` | S+sorry |
| `extendible_transposed` | yes (with `sorry`) | `Extendible (transposed H)` | S+sorry |
| `extendible_iff_all` | yes (with `sorry`) | the packaged two-sided form | S+sorry |

The seven statement-only clauses are **exactly** Lemma 2.2's six invariance clauses and their
packaged form.  What a proof needs, for the next window: `(permRows σ H)ᴴ * (permRows σ J) i j =
(Hᴴ * J) (σ i) (σ j)` (via `Equiv.sum_comp`), the analogous column identity, `IsPhaseHadamard` /
`UnbiasedH` preservation under each operation, and for transposition the paper's two-step trick.
The transposition clause is the only one with real content.

### `Mub6/Seed.lean` — compiles, 3/4 proved

| declaration | compiles | remaining goals | axioms |
|---|---|---|---|
| `abs_sup'_sub_sup'_le` | yes | none | S |
| `arcVal_diff` | yes | none | S |
| `seedGap_lipschitz` | yes | none | S |
| `gap_stability` | yes (with `sorry`) | `|seedGap x - seedGap y| ≤ 2δ` under an arbitrary matching `σ` | S+sorry |

`seedGap_lipschitz` (index-aligned matching) is proved from scratch: the max of six arcs moves by at
most `2δ` when each endpoint moves by at most `δ`.  `gap_stability` (arbitrary matching) is the
paper's actual statement and remains open; it needs the sortedness/matching reduction, not new
analysis.

### `Mub6/ThreeMUB.lean` — compiles, 13/15 proved

| declaration | compiles | remaining goals | axioms |
|---|---|---|---|
| `sqrt3_sq`, `omega_sq`, `omega_add`, `omega_cube` | yes | none | S |
| `omega_pow_four`, `omega_pow_six`, `omega_pow_eight` | yes | none | S |
| `normSq_omega` | yes | none | S |
| `normSq_one_add_two_omega` | yes | none | S |
| `normSq_two_add_omega_sq` | yes | none | S |
| `gauss_zero`, `gauss_one`, `gauss_two` | yes | none | S |
| `FDF_entry` | yes (with `sorry`) | `(Fᴴ*D*F) j k = (1/3)·gauss ((k-j) mod 3)` | S+sorry |
| `three_mub_exists` | yes (with `sorry`) | existence of two mutually unbiased complex Hadamards | S+sorry |

This is the paper's "only cross product that is not immediate" done: `ω²+ω+1 = 0`, `ω³ = 1`, all
three Gauss-sum evaluations and both modulus-squared values `3` are proved.  What remains in
`three_mub_exists` is expansion of the tensor products `A_r ⊗ B_r` — mechanical but long; it also
subsumes the 2×2 cross-product check.

## What the footprint does and does not mean

* There are **no user-declared axioms** in this project: `sorryAx` is the only non-standard name, and
  it appears only in the ten declarations listed above.  So "S" rows are genuinely proved from
  Mathlib, and "S+sorry" rows are stated, not proved.
* `Classical.choice` appears because Mathlib's analysis library uses it; it is not a hidden
  assumption about the six-dimensional problem.
* A green row says nothing about whether the statement matches the paper.  In particular
  `extendible_iff_all` compiles and is **not proved** (see `statements.md` row 22.7).

## Not attempted in this window (deliberate)

* No proofs of the §3–4 or §5–6 claims (other members' sections).
* No `sorry`-free claim about `N(6)`: nothing here proves that four MUBs in `ℂ⁶` do not exist.
* No `lake build`, no vendored Mathlib copy, no `native_decide` on 6×6 complex matrices (the
  arithmetic is exact but `native_decide` would hide the constants the paper needs).

---

# §3.1, §3.6, §4.11–4.12 — from m4 (direction `d2`)

Full table with remaining goals and the axiom footprints: **`reports/status-S3-S4.md`**.
Validation: `lean <file>` (one at a time) with oleans emitted via `lean -o`; `#print axioms` on every
declaration.

| declaration | compiles | `sorryAx` | note |
|---|---|---|---|
| `conj_mul_self`, `star_mul_self`, `seedSum_mul_conj`, `SeedSingularBounds.m_pos` | yes | **no** | infrastructure, Lean-checked |
| `norm_exclusion`, `norm_exclusion_z` (L3.8) | yes | **no** | the paper's one-line reverse-triangle proof, checked |
| `normSq_le_of_inEllipsoid` (L4.12 ingredient) | yes | **no** | checked |
| `frameMat_conjTranspose_mul`, `frameMat_charpoly`, `frameMat_sq_singular_pair`, `gram_mul_gramInv`, `frameMat_mul_gramInv` (L3.1) | yes | yes | 2×2 index/`field_simp` plumbing, not mathematics |
| `kerFrame_exists`, `frame_projection_identities` (L3.1, (3.6)) | yes | yes | needs a `finrank ker = 2` argument |
| `directional_exclusion` (L3.9) | yes | yes | 4 named sub-goals: flat identity, two Cauchy–Schwarz steps, seed-remainder step |
| `ellipsoid_containment`, `sq_add_mul_le` (L4.11) | yes | yes | 3 named sub-goals; `sq_add_mul_le` is `(√β·ru − qv)² ≥ 0` |
| `offset_ellipsoid_bound`, `offset_hull_bound` (L4.12) | yes | yes | the `(Aw)·p'` AM–GM step is a perfect square in `A` |

Totals for this slice: 3 files, all compile; **7 declarations sorry-free**, **12 stated only**,
0 undeclared holes.

Open bridges blocking the removal of the re-renderings: **B1** the support-function/`G^{1/2}`-ball
equivalence, **B2** existence of a symmetric `R` with `R*R = G`, **B3** `γI − G` invertibility from
`γ > λ_max(G)`. All three need the spectral theorem for real symmetric matrices, which the pin has
for endomorphisms but not packaged as a matrix square root.
