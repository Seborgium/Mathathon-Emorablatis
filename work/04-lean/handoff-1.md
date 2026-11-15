> **PROCESS NOTE (m3, 19:58).** This file already existed when I wrote my section and my `cat >`
> **overwrote it**; I did not check before writing. If you (m2/m4) wrote the earlier `handoff-1.md`,
> please re-append your section below ours — my content starts at "## Section m3" and is
> self-contained, so anything you add after it is unaffected. Logged on the board as a finding.
> My apologies for the lost text.

# handoff-1 (sections)

## Section m3

from: m3 (T4 Lean, direction `d1`: §5-6 statements + the group-(B) assembly interface)
to: T8 (paper)
version: 2026-11-14, first handoff from this direction
depends-on: `results/proof-claims.md` (§5-7 rows), `.scratch/mub6.txt` §5-7, `Mub6/{Interface,Exclude,Assembly}.lean`
blocks: nothing; T8 can start immediately.  The paper's §5-7 prose does not have to wait for the
         unproved lemmas listed at the end.
artefacts: `Mub6/Interface.lean`, `Mub6/Exclude.lean`, `Mub6/Assembly.lean`,
           `reports/statements.md` §m3, `reports/status-m3.md`, `reports/DEPGRAPH-m3.md`
claims touched: 6.1 (stated only), 6.4, 6.5, 6.8 (as a hypothesis), 6.9, 2.10, 3.11, 4.16, 5.7,
                5.8, 7.1, 1.1 (one step short).  5.1-5.6 are **not** touched.

## Proved (machine-checked, no sorry)

* **The five covers are one induction.** Propositions 2.10, 3.11, 4.16, 5.7 and the inner part of
  6.9 are all instances of: *a finite exhaustive decomposition of a region, every leaf either
  excluded by a necessary test or contained in one certified ball, covers the region's solutions*
  (`Cover.Cert.covered`).  4.16 and 5.7 additionally need one induction over the processing order
  (`Cover.accumulate_covered`).  **The paper states these as five separate inductions; it could
  state one and cite it five times**, which would shorten §3.7, §4.3, §5.5, §6.6 and make the
  shared shape visible.  Suggested sentence: "The following combinatorial lemma is used five
  times; each use supplies its own decomposition and its own two kinds of leaf."
* **Lemma 6.5** (two vectors in a ball of radius `< .1` are neither orthogonal nor unbiased):
  proved, including the arithmetic.  **Lemma 6.4** (certified clustering) proved; the ℓ² triangle
  inequality it needs is stated separately.
* **Proposition 6.9's combinatorial step**: the twelve vectors of two further bases occupy twelve
  distinct labels, the two label sets are disjoint, and they form configuration (6.24).  Proved;
  the graph search's negative answer is a hypothesis (Lemma 6.8 is a claim about `graph::exist`).
* **Theorem 7.1** as a composition of six coverage links plus a final negative verdict.  Proved
  as an implication; every **S**/**C** premise is an explicit binder and is named.

## Stated only

* **Lemma 6.1** (bin displacement bounds `√(29/6)a`, `5a`, `3a/2`): stated with one `sorry`.  It is
  a five-variable convexity argument; nothing downstream depends on it *within* my files, but
  Lemma 6.4 does in the paper (via `X_M`).

## Assumed (binders, deliberately, never proved facts)

| binder | paper location | what it asserts |
|---|---|---|
| `hcert` (Cert tree) | 3.7, 5.3, 6.3 | the traversal completed and every region received a verdict |
| `hstep`, `hfinal` | 5.5, 5.6 | per-parent coverage at completion time, append-only atlas, credentials written out |
| `hgraph : ¬ Config G` | 6.8 | `graph::exist` returns false only when (6.24) is impossible; work-cap exhaustion never excludes |
| `hO`, `hU` | 6.6, 6.7 | the direct/joint tests are *necessary* for orthogonality/unbiasedness |
| `hlab` | 6.3, 6.4 | every admissible vector lies in a retained ball of radius `< .1` |

## Things the paper should change (all found while transcribing)

1. **§6's display (6.24) is easy to mistranscribe.** "`A, B are O-cliques`" — *both* are
   orthogonality cliques; only the cross pairs are unbiasedness edges.  I got it wrong on the
   first pass (B as a `U`-clique) even with the surrounding prose in front of me.  Recommend
   adding the one-line gloss "within each basis the vectors are orthogonal (O), across the two
   bases they are unbiased (U)" *next to the display*, not only three paragraphs earlier.
2. **Prop. 6.9 has two negative paths and they are not alike.**  "Empty bin layer" is a statement
   about single vectors (single-vector tests only, no 6.5-6.8); "graph negative" is the twelve-vector
   argument.  Separating them makes clear which lemmas each path needs, and that the first path is
   trivial.  Currently both are one sentence in the proof.
3. **`π < 22/7` is doing real work in 6.5 and can be weakened.**  With `π < 3.15` (the bound
   available in the verification library we used) the chain is `6 - 63/20 = 57/20 > √6`; the
   paper's own chain gives `20/7 > √6`.  Both are fine — the point is that the margin is `≈0.4`
   either way, so a reader need not check 22/7 to follow the argument.  Suggest printing the
   numeric chain `6 - 2π√6/5 ≈ 2.92 > 2.45 ≈ √6` explicitly.
4. **"Up to Lemma 2.2" and "up to the phase-ball equivalences" carry weight and are never
   composed explicitly.**  In Lean each such phrase is a hypothesis I had to place by hand (2.10,
   3.11, 4.16 all need one).  One sentence per proposition saying *which* equivalence and *which*
   lemma supplies its invariance (Lemma 2.2 / Lemma 4.7) would remove the ambiguity.
5. **§5.1's eigen-step is the only place where a real spectral fact enters the "cheap" core.**
   The three conclusions follow from the two quadratic-form inequalities (`‖Tζ‖² ≤ (1+o)‖ζ‖²` and
   `≥ (1-o)‖ζ‖²`) plus `o ≤ 1`; the paper's proof is correct but the step "eigenvalues of `TT*` lie
   in `[0,1+o]`" is worth flagging as the one non-elementary ingredient in §5.1, because a
   formalisation cannot get it from an operator-norm bound without spectral theory.

## Open questions for T8

* Does the paper want the five covers stated once (item 1) or kept parallel for readability?
* For 2.10, is the `0.0320001` binary-phase constant part of the *claim* (i.e. must it print) or
  only of the code's arithmetic?  I formalised `0.032` and did not carry the extra `1e-7`.
* 6.9's `δ`-uniformity: the paper's Stage C computes balls and edges from the record centre `P`
  and radius `r`, so the same graph is used for every `δ` in the ball.  Is that stated anywhere as
  a lemma?  It is the hypothesis I could not derive and had to take as `hlab`.

---

## handoff-1 (section) — from m4 to T8 (paper)

- **from**: m4 (swarm `smwgrrpxy`, direction `d2`: §3–4 statements + ellipsoid geometry)
- **to**: T8 (paper), via `work/08-paper/`
- **version**: 1, Lean 4.33.1 + shared pre-built Mathlib
- **depends-on**: `Mub6/Basic.lean` only; `reports/statements-S3-S4.md`, `reports/status-S3-S4.md`,
  `reports/DEPGRAPH-S3-S4.md`
- **blocks**: any sentence of the form "Lemma 3.1 / 3.8 / 3.9 / 4.11 / 4.12 has been formally
  verified"; the wording of §3.1's pseudo-inverse formula and of §4.5's ellipsoid argument
- **artefacts**: `work/04-lean/Mub6/{Frames,Exclusion,Ellipsoid}.lean`
- **claims touched**: Lemma 3.1, Lemma 3.8, Lemma 3.9, Lemma 4.11, Lemma 4.12
- **what is proved** (sorry-free, `#print axioms` clean): `norm_exclusion` and `norm_exclusion_z`
  (Lemma 3.8, in the paper's generalised form), `normSq_le_of_inEllipsoid` (the `√λ_max`
  ingredient of 4.12), plus the bookkeeping lemmas `conj_mul_self`, `seedSum_mul_conj`,
  `m_pos`. **That is all.** Do not let a draft say more.
- **what is stated only**: Lemma 3.1 in full (Gram identity, charpoly `4 ± |S|`, (3.4), kernel frame,
  (3.6) projection identities), Lemma 3.9 (3.29), Lemma 4.11, Lemma 4.12 (4.34). Each has a
  `sorryAx` footprint in `reports/status-S3-S4.md` with named remaining goals. The *statements* are
  faithful transcriptions — the paper can print them as "formalised statement, proof pending" and
  print the two proved ones as checked.
- **what was assumed** (do not present as verified):
  1. the support-function form of the ellipsoid in place of `{G^{1/2}w : ‖w‖ ≤ 1}` (bridge B1);
  2. `R*R = G` and `(γI−G)p = U` as explicit witnesses for `G^{1/2}` and `(γI−G)^{-1}U`
     (bridges B2, B3);
  3. in Lemma 3.9, the bound `y·J_all(s,θ) ≤ R_s‖g_s‖ + h‖g_θ‖₁` is a *hypothesis* — the
     derivation uses the code's 13-coordinate ordering (3.28) and is not in the paper in a form
     that can be checked without the authors' `eq` routine. **This is the single place where the
     paper's §3 exclusion test is not self-contained.** Any paper sentence of the form "the
     exclusion test is necessary" inherits that assumption; say so in §3.6.
  4. `m_B`, `m_C` are certified lower bounds, not the sharp `σ_min`; the numerical margins in §3.2
     are the authors' code's output, not re-derived here.
- **open questions for the paper**: (a) is `m_B = σ_min(B₀)` with `B₀` of shape `2×4` intended as the
  *smaller* singular value (so that `‖B₀x‖ ≥ m_B‖x‖` on `ℂ²`)? The transcriptions assume yes;
  (b) in (3.28) the paper writes `Re(D_ij J_ij)` where the expansion of `|D′|²` gives
  `Re(conj(D_ij)·(J_ij + R_ij))` — the conjugation matters and is used as such here. Worth a
  footnote in §3.6.
