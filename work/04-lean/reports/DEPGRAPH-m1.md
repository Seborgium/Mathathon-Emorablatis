# DEPGRAPH — module DAG, claim dependencies, and what Mathlib already has

T4 phase 0, m1 (direction d4: fidelity/status audit + §2 gap layer).
Companion files: `reports/statements.md` (fidelity), `reports/status.md` (proof status),
`audit/spec.py` (hand-written fidelity data), `audit/audit.py` (generator).

---

## 1. Module DAG

Deliberate separation: **infrastructure** (reusable mathematics, no mention of the five stages)
below **paper-specific assembly** (the stages and their coverage implications). The rule enforced
by the layering is:

1. an infrastructure module never imports a stage module;
2. only `Mub6/Assembly.lean` may import the five stage modules, so the end-to-end statement lives
   in exactly one file and can be read on its own;
3. nothing imports `Assembly` — it is the top of the DAG;
4. `Mub6/Hypotheses.lean` (the `S`/`C` ledger) is imported by every stage module and by
   `Assembly`, and imports nothing but `Mathlib`. It is the only place a code-dependence can enter
   the development.

```
                         Mub6/Assembly.lean            (Thm 7.1, Thm 1.1 template)
                        /   |      |      |    \
                       /    |      |      |     \
        Mub6/Seed.lean  Mub6/Completion.lean  Mub6/Refine.lean  Mub6/Exclude.lean
        (Prop 2.10)      (Prop 3.11, L 3.1-3.10)   (Prop 5.7, L 5.1-5.6)   (Prop 6.9, L 6.1-6.8)
              \              |            |            /
               \             |            |           /
                Mub6/Hadamard.lean   (Def 2.1, L 2.2, L 2.3, D0, extendibility)
                        |
                Mub6/Hypotheses.lean (CodeClaims, RunReport, TerminalConditions) [in this tree]
                        |
                Mub6/Gap.lean        (circular multisets, Lemma 2.5)        [in this tree]
                        |
                Mub6/Basic.lean      (carrier: EuclideanSpace C (Fin 6), inner product
                                      normalisation, phase/exponential conventions,
                                      Frobenius norm, realification)
                        |
                     Mathlib
```

Edges actually present in this tree (m1):

```
Mub6.Gap        -> Mathlib
Mub6.Hypotheses -> Mathlib
Audit.Dump      -> Mub6.Gap, Mub6.Hypotheses        (generated, not a deliverable)
```

Pending edges owned by sibling directions: `Mub6.Basic -> Mathlib`; `Mub6.Hadamard -> Mub6.Basic,
Mub6.Gap`; `Mub6.Seed -> Mub6.Hadamard, Mub6.Hypotheses`; `Mub6.Completion -> Mub6.Basic,
Mub6.Hypotheses`; `Mub6.Refine -> Mub6.Basic, Mub6.Hypotheses`; `Mub6.Exclude -> Mub6.Basic,
Mub6.Hypotheses`; `Mub6.Assembly -> Mub6.Seed, Mub6.Completion, Mub6.Refine, Mub6.Exclude,
Mub6.Hypotheses`.

**Interface note (group B).** The assembly direction (d1) puts an abstract "region family"
interface between the stages and `Assembly`. That interface belongs in its own module
(`Mub6/Interface.lean`) *below* `Assembly` and *above* nothing else: the five stage modules must
not import it, otherwise the paper's specific constructions and the abstract coverage argument
become mutually dependent and the DAG stops showing which is which.

---

## 2. Claim dependency view

Solid edges are mathematical implications; the braces mark where an `S` or `C` hypothesis enters.

```
Lemma 1.2 ──────────────────────────────┐
                                        ├──> Theorem 1.1 (no four MUBs; N(6) = 3)
Prop 2.10 ──┐                           │
Prop 4.16 ──┤                           │
Prop 5.7 ───┼──> Theorem 7.1 ───────────┘
Prop 6.9 ───┘        │
                     └── (C) terminal conditions §7.2; (S) the seven programs; (S) App. A arithmetic

Lemma 2.2, 2.4, 2.6, 2.7, 2.8, 2.9 ──> Prop 2.10          [S: covout, seeds::mk, sumok,
                                                            extend, supdual]  [C]
Lemma 2.5 ──> Lemma 2.6 ──> Prop 2.10
Lemma 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10 ──> Prop 3.11
                                                            [S: buildH::gen, eq, trial::pass,
                                                             trial::certificate, Asearch]  [C]
Prop 3.11 + Def 4.1, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 4.10, 4.13, 4.15 ──> Prop 4.16
                                                            [S: buildH::patch, Candidate::prep]  [C]
Lemma 5.1, 5.2, 5.3, 5.4, 5.5, 5.6 ──> Prop 5.7 ──> Cor 5.8   [S: threshold protocol]  [C]
Lemma 6.1–6.8 ──> Prop 6.9                                  [S: graph::exist, clustering,
                                                             negative paths]  [C]
```

Two dependencies that are easy to get wrong and are load-bearing:

* `Lemma 2.5 -> Lemma 2.6` is *one-directional in the radius*: an upper bound on `g_x` becomes an
  upper bound on `g_{y,mid}` with `+2w`. The Lean statement must therefore be
  `GapLE A t -> GapLE B (t + 2δ)` (`Mub6.gapLE_transfer`), not a difference of gaps at a point.
* `Prop 3.11 -> Prop 4.16` uses the *union* of A-stage Records, not each seed separately: the
  atlas merge (Lemma 4.15) is applied after the per-seed conclusion, so a Lean statement that
  quantifies per seed and forgets the merge misses the radius-τ bookkeeping.

### Infrastructure vs assembly (the split the brief asks for)

| class | claims | where |
|---|---|---|
| **infrastructure** | Def 2.1, 2.4's gap definition, Lemma 1.2, 2.2, 2.3, **2.5**, 3.1, 3.8, 3.9, 4.11, 4.12, 5.1, 6.5 | `Basic`, `Gap`, `Hadamard` (+ one module per lemma group) |
| **assembly** | Prop 2.10, 3.11, 4.16, 5.7, 6.9, Thm 7.1 | `Seed`, `Completion`, `Refine`, `Exclude`, `Assembly` |
| **hypothesis ledger** | every `S` and `C` tag | `Mub6/Hypotheses.lean` |

The reason for the split is exactly the brief's: a mis-stated induction is invisible in prose but
loud in a Lean assembly lemma, and assembly lemmas are only checkable if they do not have to fight
through the analytic estimates at the same time.

---

## 3. What Mathlib already has (searched before defining anything)

Searched `/opt/mathlib/Mathlib` with `rg --files` and `rg`. Findings, with the consequence for
this development.

| topic | found in Mathlib | consequence |
|---|---|---|
| complex Hadamard matrix | `Mathlib/LinearAlgebra/Matrix/HadamardMatrix.lean`: `structure Matrix.IsHadamard` (`mk_iff`, entries of modulus 1 and `A * Aᴴ = n • 1`), `IsHadamard.conjTranspose`, `isHadamard_conjTranspose_iff`, `isHadamard_transpose_iff`, `IsHadamard.reindex` (row/column permutations), `IsHadamard.kronecker`, `isHadamard_iff_mul_conjTranspose`, `IsHadamard.isStarNormal` | **use it**: Definition 2.1 is `H.IsHadamard ∧ Hᴴ * H = 6 • 1` (the second is free for square `H` via `isStarNormal`). Half of Lemma 2.2 (permutations, transposition, conjugation) is then `reindex`/`transpose_iff`/`conjTranspose`, and Lemma 1.2's tensor step is `IsHadamard.kronecker` at `2 × 3` |
| singular values | `Mathlib/Analysis/InnerProductSpace/SingularValues.lean`: `ContinuousLinearMap.singularValues : ℕ →₀ ℝ`, `singularValues_nonneg`, `singularValues_fin`, `singularValues_of_finrank_le` | Lemma 3.1's "squared singular values of `M` are `4 ± |S|`" is a statement about `T.singularValues ^ 2`; the eigenvalues of `Mᴴ M` are not exposed under that name, so state it as `T.singularValues 0 ^ 2 = 4 + |S| ∧ T.singularValues 1 ^ 2 = 4 - |S|` (order-free version: the multiset is `{4+|S|, 4-|S|}`) |
| polar decomposition | **not found**: `rg "polar decomposition"` under `Mathlib/` returns nothing; `--files \| rg -i polar` gives only `PolarCoord` and the locally-convex `Polar` (a different subject) | Lemma 3.2's polar factor `V = Y (Y*Y)^{-1/2}` must be constructed by hand from `Matrix.PosSemidef` + `CFC.sqrt` (see the `Analysis/Matrix/{PosDef,Order,Normed}.lean` files). This is the single largest gap between Mathlib and §3 |
| orthogonal projection | `Mathlib/Analysis/InnerProductSpace/Projection/{Basic,Submodule,FiniteDimensional,Minimal,Reflection}.lean`; `Algebra/Star/StarProjection.lean` | for Lemma 2.3 the paper's `Π` has an explicit formula, so proving idempotence + self-adjointness + range = horizontal by hand is cheaper and more faithful than identifying `Π` with `Submodule.starProjection`; record the identification as a remark, not as the statement |
| ellipsoid / `{G^{1/2} w : ‖w‖ ≤ 1}` | **not found**: `rg -i ellip` gives only `EllipticCurve`/`EllipticDivisibilitySequence` (unrelated) | Lemmas 4.11 and 4.12 have no Mathlib home. They must be built on `Matrix.PosSemidef`, `CFC.sqrt` (matrix `rpow 2⁻¹`) and the quadratic-form/support-function identity. Do **not** route them through a general convex-analysis file; the paper's proof is a two-line completing of the square |
| circular multiset, gap, arc | `Mathlib/Topology/Instances/AddCircle/{Defs,Real}.lean`, `Topology/Covering/AddCircle.lean` exist (the group `ℝ/ℤ`), but **no gap/arc/empty-interval API** | this is what `Mub6/Gap.lean` supplies: `CircDistLE`, `IsEmptyArc`, `NearMap`, `GapLE`, `circGap`, and Lemma 2.5 in transfer, upper-bound and difference forms. Stated over `Finset ℝ` (see `reports/statements.md` for why that loses nothing) |
| Hadamard in the MUB sense / mutually unbiased bases | **not found** (no MUB notion at all) | `Extendible` and `IsMUB` must be defined in `Mub6/Hadamard.lean`; state them for `OrthonormalBasis (Fin 6) ℂ` so `unitary`/orthonormality is free |

Nothing above is a *proof* obligation discharged: it is a map of what to reuse and what to build.
The two "not found" rows (polar factor, ellipsoid) are the places where the formalisation will
cost the most, and they sit in §3 and §4 — worth telling T8 and T9.

---

## 4. Build discipline (why there is no `lake build` here)

`/opt/mathlib` is root-owned and fully built; `LEAN_PATH` is preset to it. All validation in this
tree is `lean <file>` (or `lean -o <mod>.olean <file>` when a module must be imported), one file at
a time, because four CPUs are shared with three other teams.

`lakefile.lean` and `lean-toolchain` are provided **for documentation**: they state which toolchain
the sources are written against and what the module roots are, so that the merged tree can be built
by the lead in a writable location. They are not used in this window.

---

## 5. Conformance with the merged tree (checked against `work/04-lean`, not assumed)

The reports in this directory are generated over the **merged tree** (`Mub6/*.lean` of
`work/04-lean`, copied into this directory for auditing). At the time of writing, 35 of the 36 rows
in `reports/statements-m1.md` resolve to real declarations; the one exception is Lemma 5.1, whose
module (`Mub6/Refine.lean`) is still a stub.

Three consequences for the fidelity table, all of them working notes for the freeze:

1. **The assembly interface is `Mub6/Cover` in `Mub6/Interface.lean`** (`Cert`, `Covered`,
   `accumulate_covered`, `Cov`), and the six paper statements are instantiations in
   `Mub6/AssemblyCover.lean` (`prop_2_10`, `prop_3_11`, `prop_4_16`, `prop_5_7`, `prop_6_9`,
   `theorem_7_1`, `theorem_1_1`). The paper's *mathematical* half of each statement is a `Cert`
   whose leaves are `excl` (disjoint from the target set) or `ball`; the *S + C* half is the
   existence of that `Cert` together with the coverage links. This is the right shape and my
   `CodeClaims` fields are the names of the S-premises: the fidelity rows for 2.10, 3.11, 4.16,
   5.7, 6.9 now point at those interface theorems, and the "code-dependence" column names the
   `CodeClaims` field that supplies the premise.
2. **§7.2 is NOT a hypothesis of `theorem_7_1`.** The interface absorbs "the run completed, with no
   unresolved region" into the existence of each `Cert`, and the record-identity bookkeeping into
   the chain of `Cov` links between the named sets `H, Sseed, Scoarse, Smid, Sfine, Sinit,
   Sfallback, Sfinal`. That is a defensible abstraction, but it means the paper's §7.2 terminal
   conditions are nowhere *stated*. `Mub6.TerminalConditions` + the field
   `CodeClaims.driver_bookkeeping_identifies_records` are exactly the missing premise, and the
   fidelity table records this as the gap between the paper's Theorem 7.1 and
   `Mub6.AssemblyCover.theorem_7_1`. Closing it means proving that terminal conditions + the six
   stage statements produce the seven `Cov` links; that is a statement about *record identities*,
   which is why it cannot be done without modelling the file formats.
3. **Lemma 2.5 exists twice.** `Mub6/Seed.lean` states `Mub6.gap_stability` in the sorted-list
   carrier (six hypotheses: `Monotone`, first entry zero, entries below one, a permutation, and the
   pointwise circular-distance matching) and leaves it `sorry`; `Mub6/Gap.lean` proves the same
   lemma in the arc carrier appearing only in `Mub6/Gap.lean`, with no sortedness and no
   permutation (the paper's own remark: "No preservation of the sorted order is used"). The two
   are related by the missing bridge `seedGap x = circGap (image x univ)` for sorted
   representatives in `[0,1)`. Until that bridge is proved, the tree contains one proved and one
   statement-only copy of the same paper lemma — a defect of the merge, not of either file. This
   is the concrete next step; it removes a `sorry` and reconciles the carriers.

## 6. The public Lean development (`github.com/openai/math`)

There is now a public formalisation of this problem:
`lean/OAI/Analysis/MutuallyUnbiased/` in `github.com/openai/math` (verified: the directory exists
and, per the repository's contents API, contains `Bases`, `Certificate`, `Completion`, `Cubic`,
`Fourier`, `GramAssembly`, `GramData`, `GramEntries`, `GramFunctions`, `GramKeys`, `GramRows`,
`Matrix`, `MixedData`, `MixedMerge`, `MixedMoments`, `MixedSemantics`, `MixedSources`,
`MixedTargets`, `Model.lean`, `Main.lean`, `Moments`, `PairData`, `PairMerge`, `PairMoments`,
`PairPolynomial`, `PairSemantics`, `PairSources`, `PairTargets`, `Results`, `Tao`,
`TaoCertificate`), together with `lean/ComparatorChallenges/MUBSix.lean` (Tao's matrix, Hadamard
equivalence, characters).

Relationship to this tree, stated honestly:

* This development is **standalone and parallel**. It defines its own carrier in
  `Mub6/Basic.lean` (its `e`, `ip`, `IsBasisMat`, `UnbiasedBases`, `Extendible`) and its own
  namespace `Mub6`; it does not import `OAI.Analysis.MutuallyUnbiased`. Nothing in this directory
  depends on that repository, and nothing there depends on this.
* It should not stay parallel. Two concrete options, in order of preference:
  1. **Rehome**: move this development under the public namespace as
     `OAI.Analysis.MutuallyUnbiased.*` and replace `Mub6/Basic.lean`'s carrier with theirs
     (`N6` as the supremum of attainable family sizes, their `Hadamard` equivalence and their
     character API). The statements of §1–2 (Lemma 1.2's Gauss sums, Lemma 2.2's equivalences,
     Lemma 2.3's double centring) are then restatements of facts the public development already
     has, and should be dropped in favour of citing it.
  2. **If the parallel tree is kept** (because the paper's proof structure — five stages with
     certified region lists — is what is being formalised, and the public development organises the
     same mathematics differently), then it must be *justified in the status report* as a
     deliberately different development, and every duplicated statement must be listed with the
     public name it duplicates. `reports/statements-m1.md` is the table that would carry that
     column; it does not yet, because the public sources are not in the packet.
* Either way, **Lemma 2.5 and the gap layer** (`Mub6/Gap.lean`) is the one piece with no obvious
  counterpart in the public directory listing: the public development has `Bases`, `Cubic`,
  `Fourier`, `Tao`, `Moments`, `Gram*`, `Pair*`, `Mixed*` — an analysis of Gram/moment data, not
  the *combinatorial seed* argument of §2.2 with its circular gaps and bin midpoint filters. If
  that is right, the gap layer is where this development adds something the public one does not
  have, and it should be offered upstream rather than kept beside it.
