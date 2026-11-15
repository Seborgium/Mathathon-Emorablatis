# Module DAG and claim dependency — the §3.1/§3.6/§4 slice (member m4)

## 1. Modules I added, and their place in the DAG

```
Mub6/Basic.lean        (another member: carriers Mat/Vec, e, ip, frobSq, IsPhaseHadamard, Pi, ...)
   ├── Mub6/Frames.lean      §3.1  — seed block, Gram matrix, singular values, pseudo-inverse,
   │                                 the fixed frames G_B,G_C,K_B,K_C and projections P_K,P_B,P_C
   │      └── Mub6/Exclusion.lean  §3.6 — Lemma 3.8 (proved), Lemma 3.9 (stated)
   └── Mub6/Ellipsoid.lean   §4.11–4.12 — ellipsoid containment, offset bound (independent of §3)
```

* `Frames` → `Exclusion` is a *real* dependency: the exclusion inequalities speak about the 4×4
  block `D` against the stored centre, whose meaning (`D = D₀(P) + ...`) is fixed in `Frames`/`Basic`.
* `Ellipsoid` is a *leaf*: §4.5's tangent bounds use it, but nothing in §3 does. It imports only
  `Basic`, so a future `Mub6/Refine.lean` can pick it up without pulling Stage A in.
* All three are **infrastructure for the paper's §3–§4**, not assembly. The assembly interface
  (`Mub6/Interface.lean`, other direction) does not depend on them; it depends on the *statements*
  of 3.11/4.16, which take these lemmas as hypotheses.

## 2. Claim-dependency view (which claim needs which)

```
Lemma 3.1 (a) M*M = [[4,S],[S̄,4]] ──► (b) squared singular values 4 ± |S|      [same lemma]
       └── (c) pseudo-inverse (3.4) ──► (3.6) P_B = G_B B₀, P_C = G_C C₀*      [frame_projection_identities]
                                  └──► existence of K_B, K_C (via rank/kernel) ──► (3.5) frames fixed
Lemma 3.8 (norm exclusion) ──► Cor 3.10 (cell excluded when (3.26) fails) ──► Prop 3.11 (coverage)
Lemma 3.9 (directional exclusion) ──► Cor 3.10 ──► Prop 3.11
Lemma 4.11 (ellipsoid containment) ──► (4.32)/(4.33) G_lin, G_dir ──► Lemma 4.10/4.9 (displacement)
Lemma 4.12 (offset bound) ──► E(G;{U_σ}) ──► (4.35)/(4.36) tangent bounds ──► Prop 4.13 (bootstrap)
                             └──► Prop 4.16 (atlas covers) via the Root data
```

Two dependency facts worth flagging to the paper team:

* **3.1(c) is load-bearing for 3.11.** If `‖S‖ = 4` the kernel claim fails (then `p` is a unimodular
  multiple of **1** and `M` has rank 1). The paper's "if |S| < 4" is therefore not decoration: the
  coverage proposition is only available on seeds whose residual does not degenerate, and the
  §3.1 acceptance checks ("the acceptance checks on rank and residual norms certify that this
  construction is defined") are exactly what excludes that case. Rendered as the explicit hypothesis
  `hS : ‖S‖ < 4` on every row of the 3.1 family.
* **4.11 → 4.12 composition is a chain of *upper bounds*, not a containment chain.** The paper uses
  4.11 to get a shape matrix `G` with `T*u ∈ ellipsoid(G)` and then 4.12 to bound `‖T*δ‖`. Since
  `E(G;{U_σ})` is "any certified upper bound", any `G' ⪰ G` and any larger `γ` remain valid. My
  `normSq_le_of_inEllipsoid` is stated with an explicit `Λ ≥ λ_max(G)` for that reason.

## 3. Pin survey (`grep -r` under `/opt/mathlib/Mathlib`) — what exists, what does not

| object | pin status | file | consequence for us |
|---|---|---|---|
| complex Hadamard predicate | **exists**: `Matrix.IsHadamard A := (∀ i j, A i j ∈ unitary R) ∧ A * Aᴴ = n•1 ∧ Aᴴ * A = n•1` | `LinearAlgebra/Matrix/HadamardMatrix.lean` | the paper's Definition 2.1 is the *one-sided* version `H H* = 6I` + unit entries; the two-sided/two-factor bridge is a real (§2) obligation, not an import |
| singular values of a linear map | **exists**: `T.singularValues : ℕ →₀ ℝ` with `hasEigenvalue_adjoint_comp_self_sq_singularValues` | `Analysis/InnerProductSpace/SingularValues.lean` | usable for "squared singular values are 4±|S|", but the matrix statement is cheaper via `charpoly_fin_two`; used the latter |
| orthogonal projection | **exists** (submodule projection API) | `Analysis/InnerProductSpace/Projection/*.lean` | not used: (3.6)'s projections are given by explicit matrices `K K*`, no subspace API needed |
| polar decomposition | **absent** (hits for "polar" are the polarisation identity, polar cones, polar coordinates — not matrix polar decomposition) | — | Lemma 3.2's polar factor `V = Y(Y*Y)^{-1/2} ∈ U(2)` has **no** pin support. Not my rows, but a §3.2 obligation |
| matrix square root / CFC on matrices | **absent**: no `PosSemidef.sqrt`, no `Matrix.cfc` | — | this is why 4.11/4.12 are stated in support/`R*R = G` form; bridges B1–B3 |
| `Matrix.PosSemidef`, `Matrix.PosDef` | **exists** with `posSemidef_iff_dotProduct_mulVec`, `dotProduct_mulVec_nonneg` | `LinearAlgebra/Matrix/PosDef.lean` | the Loewner hypotheses of 4.11/4.12 can be expressed through these later; the current statements use the pointwise form, which is what the proofs consume |
| ellipsoid / ellipsoidal calculus | **absent** (no hits) | — | `InEllipsoid` is new; its name is chosen to be the only new notion so a later `Mub6/Ellipsoid.lean` extension is local |
| double centring `Π` | **absent** | — | provided in `Mub6/Basic.lean` by the scaffold direction |
| circular gaps / min-gap | **absent** | — | §2.5 obligation, not mine |
| Cauchy–Schwarz, AM–GM | **exists**: `Real.sum_mul_le_sqrt_mul_sqrt`, `Real.sum_sqrt_mul_sqrt_le`, `Finset.sum_mul_sq_le_sq_mul_sq` | `Analysis/Real/Sqrt.lean`, `Algebra/Order/BigOperators/Ring/Finset.lean` | these are the intended workhorses for 3.9/4.11; no new analysis needed |
| 2×2 matrix algebra | **exists**: `Matrix.det_fin_two`, `Matrix.trace_fin_two`, `Matrix.charpoly_fin_two`, `Matrix.adjugate_fin_two_of`, `Matrix.inv_eq_right_inv` | `LinearAlgebra/Matrix/*` | enough for Lemma 3.1; remaining cost is `Fin 2` index reduction |

Nothing in the pin covers the paper's five stages; there is no risk of a hidden duplicate of the
assembly interface.
