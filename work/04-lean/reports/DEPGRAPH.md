# reports/DEPGRAPH.md — module DAG, claim dependency, infrastructure vs assembly

Owner of the scaffold/DAG section: m2 (`d3`).  Other members' modules are described from their
import lines and headers as they stood at 19:40; if you change an import, update this file.

## 1. Module DAG (as built)

```
                     Mathlib (pre-built, on LEAN_PATH)
                        ▲        ▲         ▲         ▲
                        │        │         │         │
        ┌───────────────┘        │         │         └──────────────┐
        │                        │         │                        │
  Mub6/Basic.lean          Mub6/Interface.lean (m3)          (future modules)
  carriers, Def 2.1,       generic coverage/blocker
  Π, D₀, Horizontal        interface, no matrices
        ▲   ▲   ▲   ▲            ▲
        │   │   │   │            │
        │   │   │   └── Mub6/Exclude.lean (m3)
        │   │   │
        │   │   └────── Mub6/Frames.lean (m4)      ── imports Mub6.Basic
        │   │
        │   └────────── Mub6/ThreeMUB.lean (m2)    Lemma 1.2
        │
        ├────────────── Mub6/Seed.lean (m2)        Lemma 2.5
        │
        └────────────── Mub6/Hadamard.lean (m2)    Lemmas 2.2, 2.3

  Mub6/Completion.lean, Mub6/Refine.lean, Mub6/Assembly.lean (m2) — STUBS, no declarations.

  Mub6/AxiomCheck.lean (m2)  — reporting artifact only; imports Basic+Hadamard+Seed+ThreeMUB and
                               prints `#print axioms`.  Not part of the library; nothing imports it.
```

Rules this DAG is meant to enforce:

1. **One direction only.** `Basic` imports nothing from `Mub6`; `Hadamard`, `Seed`, `ThreeMUB` import
   `Basic` and nothing else from `Mub6`.  No module imports a module that imports it.
2. **Infrastructure before paper-specific claims.** The reusable layer is exactly `Basic` (carriers,
   the phase exponential, the Hadamard predicate, Π, D₀, Horizontal) plus the generic coverage
   interface `Interface` (m3).  Everything that mentions a paper lemma by number is downstream.
3. **Assembly only at the end.** `Exclude` (m3) sits on `Interface`.  The three remaining spine
   modules of the original brief exist as **stubs**: `Completion.lean` (Prop. 3.11 position, imports
   `Basic`), `Refine.lean` (Prop. 5.7 position, imports `Basic`), `Assembly.lean` (Thm. 7.1 position,
   imports `Basic` + `Interface`).  They compile, contain **no declarations and no claims**, and
   record in their headers exactly what belongs in them and which imports are forbidden.  The point
   is that the DAG has a fixed shape now, so a later filler cannot accidentally put `Frames` above
   `ThreeMUB`.
4. **AxiomCheck is not a library module.** It exists so that `reports/status.md` quotes machine
   output rather than a promise.

### Build order (only order that works)

```
Basic → Hadamard → Seed → ThreeMUB          (each with -o, $PWD on LEAN_PATH)
```

`lean Mub6/Hadamard.lean` without `LEAN_PATH=$PWD:$LEAN_PATH` and without `Mub6/Basic.olean` fails
with `unknown module prefix 'Mub6'`.  That is a path error, not a proof error; it cost one iteration
in this window and is recorded in `reports/status.md`.

## 2. Claim-dependency view (paper → module → in-scope claim)

Left column: the paper's chain as recorded in `results/proof-claims.md` §1.  Right: where the
formal counterpart lives, and whether it is in the scoped target list (A) cheap core or (B) assembly.

| paper claim | depends on | module | in scope | kind |
|---|---|---|---|---|
| Lemma 1.2 (3 MUBs in `ℂ⁶`) | — | `ThreeMUB` | (A) | infra/lower bound |
| Def 2.1, (2.1), (2.2) | — | `Basic` | (A) | infra |
| Lemma 2.2 (equivalences) | Def 2.1 | `Hadamard` | (A) | infra |
| Lemma 2.3 (Π is the projection) | (2.1) | `Basic` + `Hadamard` | (A) | infra |
| Lemma 2.4 (seed arrangement) | 2.2, 2.3 | — (nobody) | no | infra |
| Lemma 2.5 (gap stability) | — | `Seed` | (A) | infra |
| Lemma 2.6 (midpoint gap filters) | 2.4, 2.5 | — | no | infra |
| Lemmas 2.7–2.9 (vanishing sum, intervals, reuse) | 2.6 | — | no | infra |
| **Prop 2.10 (seed cover)** | 2.2, 2.6–2.9 | `Interface` (+ future `Seed`) | **(B)** | assembly |
| Lemma 3.1 (fixed frames) | 2.2 | `Frames` (m4) | (A) | infra |
| Lemmas 3.2–3.10 | 3.1 | `Frames`, (future) | no | infra |
| **Prop 3.11 (completion coverage)** | 3.2–3.10 | `Interface` | **(B)** | assembly |
| Def 4.1, Props 4.5/4.6, Lemmas 4.3/4.4 | 2.3, 3.x | — | no | infra |
| Lemma 4.11 (ellipsoid containment) | — | (m4) | (A) | infra (convex analysis) |
| Lemma 4.12 (offset ellipsoid) | — | (m4) | (A) | infra (convex analysis) |
| **Prop 4.16 (atlas covers)** | 4.1–4.15 | `Interface` | **(B)** | assembly |
| Lemma 5.1 (operator bounds) | Def 4.1 | (m3) | (A) | infra |
| Props 5.2–5.7, Cor 5.8 | 4.1, 5.1 | (m3) `Interface` | (B) 5.7 | assembly |
| Lemma 6.5 (two vectors in one ball) | — | (m3) | (A) | infra |
| Lemma 6.8, Prop 6.9 | 6.1–6.7 | (m3) `Exclude`/`Interface` | (B) 6.9 | assembly |
| **Thm 7.1 (finite-execution certificate)** | 1.2, 2.10, 4.16, 5.7, 6.9 | `Interface` (assembly spine) | **(B)** | assembly |

The dependency view's point: **every** (B) claim's mathematical content is a coverage implication
over region lists; the geometric predicates enter only through (A) claims.  That is why `Interface`
deliberately mentions no matrices, and why the compilation order above can put all of (A) before any
of (B).

## 3. Infrastructure vs assembly

| | modules | can be checked without any paper-specific constant | should be reusable by others |
|---|---|---|---|
| infrastructure | `Basic`, `Hadamard`, `Seed`, `Frames`, (m4's §4 modules) | yes | yes |
| assembly | `Interface`, `Exclude`, (future `Completion`, `Refine`, `Assembly`) | yes (they are parametric) | yes, but only once instantiated |

Design directive honoured for (B): the assembly is **not** a recitation of the algorithm.  m3's
`Interface` states `Cert.covered` (an exhaustive finite decomposition whose leaves are excluded or
contained) and `accumulate_covered` (the blocker induction with the "already-completed parent"
hypothesis explicit), and each paper proposition is an instance.  Cross-check for the red team: the
instantiation step (which is where a mis-stated induction would hide) is *not* yet done for 2.10,
3.11, 4.16, 5.7, 6.9 — the paper-specific hypotheses are still prose in the instance files.

## 4. Mathlib survey (what exists in the pin, and what does not)

Search was `grep -r <term>` under `/opt/mathlib/Mathlib`, plus `#check` against the live environment.

| wanted abstraction | found in Mathlib? | where / what | consequence for us |
|---|---|---|---|
| complex Hadamard matrix (entries unit modulus, `HH* = n·1`) | **yes** | `Matrix.IsHadamard`, `Mathlib/LinearAlgebra/Matrix/HadamardMatrix.lean`: `structure IsHadamard (A : Matrix n n R)` with `apply_mem : A i j ∈ unitary R`, `mul_conjTranspose : A * Aᴴ = card n • 1`, `conjTranspose_mul : Aᴴ * A = card n • 1` | reused conceptually.  The paper's Def 2.1 is **one-sided**, so `Basic.IsPhaseHadamard` states the paper's form and the two-sided Mathlib predicate is not assumed.  `Matrix.IsHadamard.of_mul_conjTranspose` is the bridge (needs `IsRegular (card n)`), not invoked. |
| mutually unbiased bases | **no** | nothing under `Mathlib` matching `mutually unbiased`, `IsMUB`, "unbiased basis" | `IsPhaseHadamard`, `UnbiasedH`, `UnbiasedBases`, `Extendible` are ours. |
| orthogonal projection onto a subspace | **yes** | `Submodule.orthogonalProjectionOnto`, `Mathlib/Analysis/InnerProductSpace/Projection/{Basic,FiniteDimensional}.lean`; `orthogonalProjectionOnto_mem_subspace_eq_self`, `..._apply_of_mem_orthogonal` | not applied: it needs an `InnerProductSpace` structure on the carrier.  See the next row. |
| Frobenius inner product space on `Matrix` | **partially** | `Matrix.frobeniusNormedAddCommGroup`, `Matrix.frobeniusNormedSpace`, `Matrix.frobenius_norm_def` in `Mathlib/Analysis/Matrix/Normed.lean`.  These are **defs, not global instances** ("Not declared as an instance because there are several natural choices"), and there is **no `InnerProductSpace ℝ (Matrix m n ℝ)` instance** in the pin | Lemma 2.3 is therefore proved by sums: `frobSqR`, `sum_mul_rowcol_zero`, `frobSqR_add_of_cross_zero`.  A future window could `attribute [local instance]` the Frobenius instances and *state* `Π = Submodule.orthogonalProjectionOnto`; this is the cleanest upgrade path and is recorded in `statements.md` row 23.7. |
| polar decomposition | **no** | nothing named `polarDecomp`, and no occurrence of "polar decomposition" in `Mathlib` | Lemma 3.2's polar factor `V = Y(Y^*Y)^{-1/2}` must be built from functional calculus (`cfc`) or stated with its own hypotheses.  Relevant to m4/m3, not to §1–2. |
| ellipsoid / ellipsoidal containment | **no** | no occurrence of "ellipsoid" in `Mathlib` | Lemmas 4.11/4.12 (m4) are proved from `Matrix.PosSemidef` and support functions, not imported. |
| phase exponential `e(t) = exp(2πit)` | **partially** | `Complex.exp_two_pi_mul_I`, `Complex.exp_int_mul_two_pi_mul_I` (used in `e_int`), `Complex.normSq` (monoid hom) | `Basic.e` is ours (cycles, not radians); integer periodicity is proved, not assumed. |
| `6×6` explicit-sum computation | **yes** | `Fin.sum_univ_six : ∑ i : Fin 6, f i = f 0 + f 1 + f 2 + f 3 + f 4 + f 5` | the workhorse of Lemma 2.3: expand the explicit six-term sums and `ring`. |
| roots of unity | yes for the general theory (`IsPrimitiveRoot`), not used | `Mathlib/RingTheory/RootsOfUnity/*` | Lemma 1.2 needs only `ω² + ω + 1 = 0` and `ω³ = 1`, so `ω` is the explicit closed form `-1/2 + √3/2 i` and no root-of-unity API is touched.  Deliberate: it keeps every step `ring`-checkable. |

## 5. Known overlaps and risks (for the next member)

1. **Two unit-modulus predicates.** `Basic.IsUnitScalarVec r := ∀ i, normSq (r i) = 1` and
   `Frames`' own `UnitModulus p`.  They are the same predicate on different carriers (`Fin 6` vs
   `Fin 4`).  Unifying them is a two-line change in `Frames` (`fun i => IsUnitScalarVec p` needs a
   coercion of index type); nobody should add a third copy.
2. **Two carrier styles.** `Basic` uses `Matrix (Fin n) (Fin n) ℂ` and function-type vectors;
   a member working with `EuclideanSpace ℂ (Fin 6)` would produce statements that do not unify with
   §1–2.  The §3–4 and §5–6 modules as they stand both go through `Basic`, so this has not happened
   yet.
3. **`Interface` imports only `Mathlib`.** That is correct for a parametric coverage interface, but
   it means the *instantiation* files must import `Basic`; if an instantiation file imports only
   `Interface`, the paper's geometric predicates will be re-declared a second time.
4. **The (B) instantiation is the weak point**, exactly as the brief predicted: the interface lemmas
   are proved, but no file yet contains the paper's specific hypothesis list as an instance of
   `Cert.covered`/`accumulate_covered`.  An error there — a missing "every leaf" clause, a wrong
   quantifier over completed parents — is invisible in prose and would not be caught by the current
   files.

---

# §3–§4 slice — from m4 (direction `d2`)

Full version, including the claim-dependency view and the pin survey table:
**`reports/DEPGRAPH-S3-S4.md`**.

```
Mub6/Basic.lean                     (scaffold: Mat/Vec/e/ip/frobSq/IsPhaseHadamard/Pi)
   ├── Mub6/Frames.lean             §3.1  seed block, Gram, 4±|S|, pseudo-inverse, G_B,G_C,K_B,K_C,P_K,P_B,P_C
   │      └── Mub6/Exclusion.lean   §3.6  L3.8 (proved), L3.9 (stated)
   └── Mub6/Ellipsoid.lean          §4.11–4.12  ellipsoid containment, offset bound   [leaf]
```

`Ellipsoid` is a leaf and imports only `Basic`, so §4's refinement (`Mub6/Refine.lean`) can use it
without pulling Stage A in. `Exclusion` genuinely needs `Frames` (it speaks about the stored block
`D` and its displacement).

**Pin survey (grep under `/opt/mathlib/Mathlib`), headlines:**

* `Matrix.IsHadamard` **exists** (`LinearAlgebra/Matrix/HadamardMatrix.lean`) but is the *two-sided*
  version with entries in `unitary R`; the paper's one-sided Definition 2.1 still needs a bridge
  (§2's job, not mine).
* singular values: **exist** (`Analysis/InnerProductSpace/SingularValues.lean`).
* orthogonal projection: **exists** as a submodule API; not needed — (3.6)'s projections are the
  explicit matrices `K K*`.
* **absent**: matrix polar decomposition; matrix square root / matrix CFC; any ellipsoid or
  ellipsoidal-calculus notion; double centring; circular gaps. The first two are *obligations*, not
  conveniences: they are why Lemma 3.2 (`Y(Y*Y)^{-1/2} ∈ U(2)`) and Lemma 4.11/4.12 are stated with
  explicit witnesses (`R*R = G`, `p` solving `(γI−G)p = U`).
* present and load-bearing for a future proof: `Real.sum_mul_le_sqrt_mul_sqrt`,
  `Real.sum_sqrt_mul_sqrt_le`, `Finset.sum_mul_sq_le_sq_mul_sq`, `Matrix.charpoly_fin_two`,
  `Matrix.inv_eq_right_inv`.
