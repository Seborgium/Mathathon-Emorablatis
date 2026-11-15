# Module DAG and claim dependency — section m3 (direction `d1`)

## 1. Module DAG of my files

```
Mathlib
  ├── Mub6/Interface.lean        (Cover: Covered, Cert, Cert.covered, accumulate_covered, Cov)
  │        ▲
  │        │
  ├── Mub6/Exclude.lean          (StageC: e, ip, Ortho, Unbiased, InBall, Lemma 6.5,
  │        ▲                      Lemma 6.1 (stated), Lemma 6.4, Graph/Config, Prop. 6.9)
  │        │
  └── Mub6/Assembly.lean         (Rec, prop_2_10, prop_3_11, prop_4_16, prop_5_7, cor_5_8,
                                  prop_6_9, theorem_7_1, theorem_1_1)
```

`Exclude` imports `Interface` (it uses nothing from it yet — the dependency is declared so that
`Assembly` sees one interface), `Assembly` imports both.  Build order is the topological order
above; each olean is built with
`LEAN_PATH="$LEAN_PATH:." lean -o Mub6/<M>.olean Mub6/<M>.lean`.

**Integration note (for m2/m4).** My three files import `Mathlib` only, not
`Mub6/Basic.lean`, deliberately: `Basic.lean` was being rewritten while I worked, and a broken
`Basic` must not block the assembly.  When `Basic` settles, the rebasing is mechanical:
* `StageC.e` → `Basic`'s phase function (same definition, `exp (2πit)`);
* `StageC.sq` → the ℓ² squared norm on `Fin 6 → ℝ` (keep the ℓ² form: Mathlib's `‖·‖` on a
  function type is the **sup** norm, which is wrong here and a silent trap);
* `StageC.Ortho`/`Unbiased` → `Basic`'s `ip`/`UnbiasedH` specialised to phase points
  (`H = √6 · e(u)`): the interface is `ip u u' = 6·⟨e(u)/√6, e(u')/√6⟩`;
* `Assembly.prop_6_9`'s `¬ ∃ u0 u1, …` → `Basic.Extendible`-shaped `¬ ext`.

## 2. Claim dependency view (group (B))

```
Lemma 1.2 (m2) ──────────────────────────────┐
                                             ▼
Prop 2.10 (A2) ──► Prop 4.16 (A4) ──► Prop 5.7 (A5) ──► Cor 5.8 (A6) ──► Thm 7.1 (A8) ──► Thm 1.1 (A9)
   ▲                  ▲                  ▲                                ▲
   │                  │                  │                                │
 I2/I3 (Cert)      I4 (accumulate)    I4 (accumulate)             Prop 6.9 (C8)
                                                                       ▲
Prop 3.11 (A3) ◄── Lemma 3.8, 3.9 (m4)                                 │
                                    Lemma 6.1 (C4, stated) ──► Lemma 6.4 (C6) ──► Lemma 6.5 (C3)
                                                                                   ▲
                                                     Lemmas 6.2, 6.3, 6.6, 6.7 (not mine) ──┘
                                                     Lemma 6.8 = binder `hgraph`
```

Assembly nodes: **A2, A3, A4, A5, A6, A8, A9, C8** (their whole content is a composition; the
geometric content is elsewhere).  Infrastructure nodes: **I3, I4, I5/I6, C1, C2, C5** (proved;
reusable by §2–§4 work).  Geometric instance nodes: **C3 (6.5), C4 (6.1), C6 (6.4)**.

Every edge labelled by a proposition is proved as an *implication* whose hypotheses are that
proposition's **S** and **C** premises.  The only edges that are not implications are
`Lemma 6.8 → Prop 6.9` (a binder `hgraph`, because `graph::exist`'s behaviour is a specification
claim) and `Lemma 6.1 → Lemma 6.4` (my `sorry`).

## 3. What the Mathlib pin already provides (searched before defining anything)

`rg` under `/opt/mathlib/Mathlib` (pin shipped with Lean 4.33.1):

| wanted | found | where | used? |
|---|---|---|---|
| Cauchy–Schwarz, squared finset form | **yes** `Finset.sum_mul_sq_le_sq_mul_sq` | `Algebra/Order/BigOperators/Ring/Finset.lean` | yes (`cross_le`, `sum_abs_le`) — **do not** use `sq_sum_le_card_mul_sum_sq`, it needs monotone data |
| `\|e^{iθ} − 1\| ≤ \|θ\|` | **yes** `Real.norm_exp_I_mul_ofReal_sub_one_le` | `Analysis/SpecialFunctions/Trigonometric/Bounds.lean` | yes (`ip_norm_gt`).  Note `Complex.norm_exp_sub_one_le` is *weaker* (`2‖x‖`, and needs `‖x‖ ≤ 1`, which fails at `‖x‖ = 2π/5`) |
| `e^{2πin} = 1` for `n ∈ ℤ` | **yes** `Complex.exp_int_mul_two_pi_mul_I` | `Analysis/SpecialFunctions/Trigonometric/Basic.lean` | yes (`e_int`) |
| `π < 22/7` | **no** | nearest: `Real.pi_lt_d2` (`π < 3.15`), `Real.pi_lt_d4`, `Real.pi_lt_d20` in `Analysis/Real/Pi/Bounds.lean` | yes, `pi_lt_d2` substituted (recorded) |
| Hadamard **matrix** theory | yes but **wrong notion**: `Matrix.IsHadamard` is `HHᴴ = n•1` for matrices (entries arbitrary, Mathlib uses it for `±1`) | `LinearAlgebra/Matrix/HadamardMatrix.lean` | no |
| phase-Hadamard / MUB / unbiased bases | **no** — `rg -i "mutually unbiased\|unbiased"` returns nothing | — | defined in `Exclude`/`Basic` |
| orthogonal projection onto row/column-sum-zero | **no** matrix-level lemma | `Submodule.orthogonalProjection` exists (`LinearAlgebra/Projection.lean`, `Analysis/InnerProductSpace/Projection.lean`) but for submodules of an inner-product space, not for (2.1) | not used: `Basic` defines `Pi` explicitly |
| polar decomposition (Lemma 3.2) | **no** (the `polar` hits are polar *forms* / root systems) | — | not used; relevant for m4 |
| matrix operator norm / spectral order | partial: `Matrix.l2_opNorm` in `Analysis/CStarAlgebra/Matrix.lean` (C*-algebra norm); `Matrix.PosSemidef` + `PosSemidef.dotProduct_mulVec_nonneg` (`LinearAlgebra/Matrix/PosDef.lean`) | — | not used by me; `Lemma 5.1` should be built on these |
| ellipsoid / support-function containment | **no** (`rg -i ellipsoid` empty) | `Analysis/Convex/*` has `gauge`, `ConvexBody` | m4's problem; 4.11/4.12 need a new statement, not a search hit |
| list induction from the right | **yes** `List.reverseRecOn` (case name `append_singleton`) | `Init`/`Mathlib` | yes (`accumulate_covered`) |
| finite sets, cardinality of images | yes `Finset.card_image_of_injective`, `Finset.disjoint_left` | — | yes (`prop_6_9`) |
