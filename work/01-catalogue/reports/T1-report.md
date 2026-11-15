# T1 catalogue — report (gate G0)

Status: deliverables complete. `claims.yaml` (91 entries), `dependencies.dot` (91 nodes, 178 edges,
acyclic), `notation.tex` (compiles, 7 pp.), `style.md`, `reader-path.md` (≈3.3k words ≈ 6 pp.),
`changerequests/README.md` + protocol, `handoff-1.md`. This report states what changed relative to
`results/proof-claims.md`, gives a disposition for every statement whose subject is code, and lists
what I believe to be defects in the paper.

---

## 1. What changed relative to `results/proof-claims.md`

`results/proof-claims.md` is a *reading* of the paper: prose, in paper order, with a composite status
per claim. `claims.yaml` is an *inventory*: one entry per numbered claim (plus the load-bearing
displays), each with an id, a single status, a status decomposition, dependencies, an owner and an
open question. Substantively:

**1.1 Added — not in `proof-claims.md` as separate items.**
* All three definitions and the one remark: `def-2.1`, `def-4.1`, `def-4.14`, `rem-4.2`. They are
  numbered statements and T2/T3/T4 must cite them; `def-4.14` in particular fixes that a Record is a
  Root *plus* a radius, which the paper only says in passing.
* 18 numbered equations, including all 15 the mission names: `eq-2.6` `eq-2.7` `eq-2.12` `eq-2.14`
  `eq-3.19` `eq-3.24` `eq-3.26` `eq-3.29` `eq-4.17` `eq-4.20` `eq-4.38` `eq-5.17` `eq-5.26` `eq-6.7`
  `eq-6.11` `eq-6.12` `eq-6.23` `eq-6.24`. Of these, `eq-4.17` (integer lifts), `eq-5.17` (the
  semantics of the computed `D̂`) and `eq-6.24` (the forbidden two-clique pattern) are load-bearing
  statements that the paper never isolates as claims.
* The §7 machinery as four entries: `prem-arith` (§7.1 arithmetic and compiler premises),
  `flow-7.2` (control flow and the five terminal conditions), `bounds-7.3` (finite bounds and
  conservative stopping), `run-7.5` and `hashes-7.5` (Tables 1 and 2).
* `app-a4-a11` (the twenty pages of per-quantity budgets as one entry) and `margin-a.12` (the
  twenty-row margin table). `proof-claims.md` mentions the margin table in one sentence; it is the
  paper's real trust base and T5 needs it as an object.
* Dependencies (171 edges) and an owner for every entry. `proof-claims.md` has neither, so no team
  could tell what had to be discharged before what.

**1.2 Status changes — three, each deliberate.**
* `cor-1.3`: `proof-claims.md` says **M** modulo a citation. The paper's own statement begins
  "Under the arithmetic and compiler conditions of Appendix A, using the complete execution
  documented in Section 7.5 as in Theorem 1.1". A statement whose truth is inherited from Theorem 1.1
  is **C**. Tagged `C`, with the identity `tr((bb*-I/6)(cc*-I/6)) = |<b,c>|^2 - 1/6` recorded as the M
  part. Disagreement noted for T7/T8.
* `prop-4.6`: `proof-claims.md` says **S + C**. I use **S** only: the "successful call" is the
  routine's own guard, not a documented finite execution with provenance and terminal conditions. I
  reserve **C** for claims that depend on the §7.5 run. Same for `lem-6.8` (**S**, formerly S + M?).
* `prop-2.10`, `prop-3.11`, `prop-4.16`, `prop-5.7`, `cor-5.8`, `prop-6.9`, `thm-7.1`: `proof-claims.md`
  writes "M + S + C". They are tagged **C** (the weakest tag the statement as written depends on), with
  `status_parts` carrying the M/S/C decomposition. `bounds-7.3` is tagged **M** with S in the parts.
  This convention is documented in the file header and matters: a reader who filters on `status: M`
  gets the 58 statements that are mathematics only.

**1.3 Kept from `proof-claims.md` unchanged:** every M/M? judgement, the M? tag on `lem-2.4`,
`lem-3.7`, `eq-3.24`, and the identification of the four concentration points of risk
(`prop-4.6`, Stage-B traversal, Stage-C machinery, clique search).

**1.4 Corrections to the paper's own labels.** The mission's list calls 6.4 and 6.9 "Propositions";
the paper has *Lemma* 6.4 (p. 44) and *Proposition* 6.9 (p. 48). The inventory follows the paper:
`lem-6.4`, `prop-6.9`. It also calls 4.5/4.6/4.13 "Lemmas" in a range; they are Propositions. The
inventory uses paper labels so that a reader can find them.

---

## 2. Coverage and counts

| status | entries | which |
|---|---|---|
| M  | 63 | the mathematical core: all of §1-§3 except the three C entries, most of §4-§6 |
| M? | 3  | `lem-2.4`, `lem-3.7`, `eq-3.24` |
| S  | 8  | `prop-4.6`, `eq-5.17`, `lem-6.8`, `app-a4-a11`, `lem-a.1`, `lem-a.2`, `lem-a.3`, `margin-a.12` |
| C  | 10 | `thm-1.1`, `cor-1.3`, `prop-2.10`, `prop-3.11`, `prop-4.16`, `prop-5.7`, `eq-5.26`, `cor-5.8`, `prop-6.9`, `thm-7.1` |
| E  | 4  | `prem-arith`, `flow-7.2`, `run-7.5`, `hashes-7.5` |
| D  | 3  | `def-2.1`, `def-4.1`, `def-4.14` |

(91 entries. Five were added after an audit filed `changerequests/T1-audit.md` asked for ids on
(4.5), (4.6), (4.7), (4.15) and (6.2): `root-disp-n`, `root-disp-s`, `root-diff`, `root-suff`,
`stagec-iface`.)

Owners: T4 lean 48, T2 checker 20, T5 parameters 8, T8 paper 6, T3 reference 2, T7 quantum 1,
T6 figures 0 (T6's work is figure-level, not claim-level; `reader-path.md` §3 dictates F1's content).

`dependencies.dot`, checked mechanically at generation: **no cycles**, longest chain 14
(`thm-1.1 → thm-7.1 → prop-6.9 → lem-6.7 → lem-6.3 → lem-6.1`), 10 sources
(`lem-2.5`, `lem-4.3`→…, `lem-4.11`, `lem-4.12`, `lem-6.1`, `lem-6.6`, `prem-arith`, `eq-2.6`).
No cycle was silently broken: the two that existed in the first draft (`lem-2.8 ↔ eq-2.14`,
`prop-5.7 ↔ eq-5.26`) were my own mis-orientations of a lemma/display pair, and I re-oriented the
edge rather than dropping it.

---

## 3. Every S-statement, with a proposed disposition

Dispositions: **E** = evaluate in the checker (T2); **F** = formalise (T4); **H** = prove by hand
(T1/T4, cheap); **P** = promote into the printed theorem's hypothesis (T8); **R** = report as an
observation only. The routine list follows `results/code-audit.md` §2, which is the audit index.

### 3.1 Seed cover (§2) — serves `prop-2.10`

| routine claim | serves | audit | disposition | why |
|---|---|---|---|---|
| `seeds::build` visits every admissible five-bin x tuple and every matching y tail | `prop-2.10` | UNCHK | **E** + **F** | completeness is an arithmetic statement about integer tuples; a checker can verify `centers.txt` is exactly the filtered enumeration, and T4 can state "every tuple is visited" as a hypothesis on the list rather than on the code |
| `seeds::mk` picks the first minimiser of `|2b_s+1-N|` | `prop-2.10` | OK | **P** (one line) | validity is independent of which column is selected (Lemma 2.4 imposes no condition on ξ); print the rule as a definition, not a claim about code |
| `sumok` tests (2.11) in finitely many directions | `prop-2.10` | OK-U | **F** | the lemma needs (2.11) for all v; testing a subset only retains more, so the sound direction is universal and cheap |
| `extend` intersects the (2.14) intervals, skips divisors < 1e-6 | `prop-2.10` | OK-U | **F** | skipping a constraint enlarges the interval: a one-line monotonicity fact |
| `supdual` proposes v with entries ≤ 1e4, evaluates (2.19) with 1.251π/N | `lem-2.9` | OK | **E** | the inequality is valid for every v and the larger constant is conservative; store v and both sides |
| `testBucket` compares against (.032·112)² − 1e-4 | `prop-2.10` | OK | **E** | threshold is slightly *smaller* than nominal, i.e. conservative; the checker evaluates the comparison |

### 3.2 Stage A (§3) — serves `prop-3.11`, `prop-4.16`

| routine claim | serves | audit | disposition | why |
|---|---|---|---|---|
| `block::setup`, `makeD`, `makeJ` assemble (3.1)-(3.7), (3.23) | `lem-3.5`-`lem-3.9` | UNCHK | **E** | §3.7 prints the coefficient formulas; the checker can recompute J and D from the centre and compare |
| frame check: m = sqrt(4-|S|), fails if m ≤ 1.25 | `lem-3.1` | OK | **E** | the only thing needed is m_B, m_C > 0 and the certified 1/m in every bound; store them |
| `uc::init`, `uc::initDeriv` supply the four angular derivatives | `lem-3.4` | OK | **F** | the derivatives are printed in prose (p. 15); the constant 42 depends on them |
| `eq` stacks exactly the twenty equations (3.28) | `lem-3.9` | OK | **E** | the checker recomputes the 20-vector from the centre |
| `trial::pass` proposes directions; `trial::certificate` checks finiteness, divides by max, uses the negative part of the flat weights | `cor-3.10` | OK | **E** | this is the one place the paper's prose is exactly the guarantee the lemma needs; the stored y and both sides of (3.29) are the certificate |
| `Asearch::testA` is the used path; `Usearch::test` and scalar routines give no exclusions | `prop-3.11` | UNCHK / DEAD | **E** + **R** | dead code needs one sentence in the final paper, not a claim |

### 3.3 Roots and atlas (§4) — serves `prop-4.6`, `prop-4.16`

| routine claim | serves | audit | disposition | why |
|---|---|---|---|---|
| `buildH::gen` supplies F, L_P; rejects |p_j| > 4 or nonfinite | `lem-4.3` | OK | **E** | F and L_P are explicit formulas; the checker recomputes them |
| **`buildH::patch` certifies (4.4), (4.15) and C** | `prop-4.6` | UNCHK, **F1 high** | **P** + **E** | no later stage can detect a false Root. Print it as a hypothesis *and* have the checker verify (4.4)/(4.15) from a stored Root; that converts the paper's weakest link into a checkable record |
| optional tensor step: checks β < .1, certifies ‖S‖² ≤ r/(1-β) | `lem-4.4` | OK-U | **E** | a congruence bound, not an eigenvalue assertion |
| `Candidate::prep`: mag_j > .15, chord < 1e-7, slack, q_d < 3.8 | `lem-4.8`, `lem-4.9`, `eq-4.20` | OK | **E** | q_d is a *hypothesis* of Lemma 4.8; the record must store enough to recompute it (see I11) |
| `Candidate::delta` rounds to integer lifts | `eq-4.17` | OK-U | **F** | (4.17) is true for every integral N; the choice is free |
| `covercompute::value` computes (4.27)-(4.28) with +1e-4 before dividing by π | `lem-4.10` | OK | **E** | margin 1e-4 vs error 2e-6; store S_1, S_2 |
| `ell` returns a certified inverse quadratic form | `lem-4.12` | OK-U | **E** | the solve only proposes; the residual certificate is checked. Note the sentinel 100 lies inside the legitimate range (F4) |
| `spectralUpper` | `lem-a.3` | OK | **E** | min of row-sum and fourth-norm bounds; the checker can recompute both |
| `bootstrap` does ≤ 30 updates of (4.38), inflates t and r | `prop-4.13` | OK | **F** | Prop 4.13 needs no iteration count; the final s is the certificate |
| `local::test` succeeds only after a certified `covercompute` bound fits .103 | `prop-3.11`, `prop-4.16` | OK-U | **E** | snapping must re-pass patch and the same covering computation; store the final bound |
| `mapH`, `variants`, `canonicalMap` choose signed maps | `lem-4.7`, `lem-4.15` | OK-U | **F** (+**E**) | Lemma 4.15 needs *some* allowed Φ; the certificate must record which (F7) |
| `Atlas::find`, `Atlas::add` merge with r+d and a 2e-8 cap check | `lem-4.15` | OK | **E** | store Φ, N, d |

### 3.4 Stage B (§5) — serves `prop-5.7`, `cor-5.8`

| routine claim | serves | audit | disposition | why |
|---|---|---|---|---|
| `relationB::init` cuts the wrapped difference at .249/.23, inward only | `prop-5.2` | OK | **E** | a wrong cut loses an opportunity, never coverage; the checker evaluates the final bound |
| `relationB::eval` does ≤ 30 improvements, guard 0 ≤ t ≤ 2, sentinel 10 | `lem-5.3`, `eq-5.17` | OK | **F** + **E** | the induction is Lemma 5.3; the *stored* evaluation is the certificate. This is `eq-5.17`, the single most important S-statement in the paper |
| ρ-search: 25 midpoint trials, ρ = max(0, ℓ-1e-8), usable iff ρ > 1e-7 | `lem-5.4` | OK | **E** | a single stored trial is the certificate; no monotonicity of D̂ needed |
| `outside` lower test with 1e-8 inside each part | `lem-5.5` | OK | **E** | A.9: rounding 4e-17 vs separation 9.9e-15 |
| `corner`, `markRec` accumulate per-coordinate inflated radii | `lem-5.5` | OK | **E** | whole-box marking only; a subbox success does not mark the base box |
| `assign`: merge if r+ℓ+2e-8 < τ, else insert ΦQ with radius r | `lem-5.6` | OK | **E** | store ℓ and Φ |
| batch writer: ≤ 256 records, radius → τ, atomic rename, count marker | `cor-5.8` | OK | **E** | the count marker alone is not a certificate; the batch records must be included and checked |

### 3.5 Stage C (§6) — serves `prop-6.9`

| routine claim | serves | audit | disposition | why |
|---|---|---|---|---|
| `Layer::test` applies (6.7), then (6.12), then (6.11) | `lem-6.2`, `lem-6.3`, `eq-6.7`, `eq-6.11`, `eq-6.12` | OK | **E** | three one-sided inequalities; store y and both sides |
| `single::support` starts the coefficient array at zero | `lem-6.3` | OK | **E** | the ordering detail is essential (A.11) |
| `cluster`: ≤ 2 Lloyd passes, radii recomputed from the assignments | `lem-6.4` | OK-U/OK | **F** | the lemma is universally quantified over the assignment, so the heuristic is irrelevant; the recomputed radius is the claim |
| `graph::joint` accumulates both -(B^t)*y_t before the norm, ≤ 14 rows | `lem-6.7` | OK | **E** | the shared η is the only coupling; store the two vectors and y_e |
| **`graph::exist` mode 1 is a complete two-clique search; a cap is not a negative** | `lem-6.8` | UNCHK, **F9 medium** | **P** + **E** | two options per F9: a mathematical criterion for (6.24)-infeasibility checkable on the adjacency sets (preferred: it makes the claim a theorem about graphs), or an emitted trace checked externally. Until one exists, print the exhaustiveness as a hypothesis |
| `negative` has exactly two negative paths; caps and failures never negative | `prop-6.9` | OK | **F** | this is the "pipeline can say I don't know" property; it must survive into the new code |
| `expair` guarded range checked | `lem-a.2` | OK | **E** | |P| ≤ 4, |v| ≤ 2, differences ≤ 6 bound every argument |

### 3.6 Appendix A — serves everything

| claim | disposition | why |
|---|---|---|
| `lem-a.1` (accumulation) | **E** (replaced) | if T2 uses interval arithmetic the lemma disappears; if it re-uses binary64 it must be re-derived for T2's own operation order |
| `lem-a.2` (expair, ε_exp, π) | **E** for the exponential, **H**/**F** for the π part | the π bound is three checkable lines and should stay in the final paper |
| `lem-a.3` (spectralUpper) | **E** | recompute both bounds |
| `app-a4-a11` (twenty pages of budgets) | **P** until replaced, then delete | T1's recommendation: do not re-derive 20 pages to serve ~30 S-statements; replace them by T2's interval arithmetic and keep only the margin table as a summary |
| `margin-a.12` (the twenty margins) | **E** | each margin is an inequality the checker evaluates on stored data; T5 turns the table into the constant → inequality → slack → cost table |

**Net effect if the dispositions are followed:** the final paper has no statement whose only support
is "the code does this". `prop-4.6`, `eq-5.17` and `lem-6.8` become explicit hypotheses (three, all
named); everything else becomes a stored inequality (T2) or a proved statement about sets (T4).

---

## 4. What I believe is wrong, missing or inconsistent in the paper

Severity: **H**igh = a reader cannot check the claim as printed; **M**edium = a gap or a defect in the
specification that costs a team work; **L**ow = comprehension or a harmless slip.

**I1 (H, comprehension). Three naming systems for the same seven constants.** Def 4.1
`(C,n0,id,ort,hor,mnorm,froot)`; §5.1 `(γ,α,o,hor,μ,ε)`; §6.1 `(Γ,ι,ω,-,-,f0)`. §7.1's record format
stores the first set. A reader tracking one constant through A→B→C translates twice, and `ε` collides
with the centre correction of Lemma 4.9 and with `ε_exp` of A.2. **Fixed** by `notation.tex` Table 1
and its rule "always Definition 4.1 form". Owner: T8.

**I2 (H, logic). §6.1's admitted ranges are an unclosed hypothesis.** §6.1 assumes
`‖F(P)‖ ≤ f0 < 1e-6`, `0 ≤ ω < 1e-5`, `0 ≤ n0 < 1e-6`, `0 ≤ ι < 1e-4`, `0 ≤ Γ < 20`, `r ≤ .03`, and
A.10 says "the C stage validates its Root and 0 ≤ r ≤ .03". *None of these is part of Definition 4.1*;
`prop-4.6` does not claim the constants it certifies satisfy them; `prop-5.7`/`cor-5.8` emit Records
with "valid Root certificates" and nothing more. So `prop-6.9`'s hypothesis is not known to be met by
the records Stage B emits. A.12 §5 mentions that B and C "enforce the stated numeric ranges in
`validate`" — which would make the ranges a *check*, but then the check is not one of §7.2's five
terminal conditions, so a record failing validation would have to appear as unresolved, and the run
reports none. Either way there is a missing link. **Fix:** state the ranges as hypotheses of Prop 6.9
(they are), prove that B's output satisfies them *or* add "all records pass `validate`" as terminal
condition 6 and emit the validation counts. Owner: T8 + T2, checked by T5.

**I3 (M, specification). `k ≤ 10` cannot be exercised at the stated refinement widths.** The base grid
has `(2L+1)^k` boxes with a 5·10⁷ cap; at `w = .013` and `w = .005` this forces `k ≤ 5`, at
`w = .0038` `k ≤ 7`. A record with `k = 6` in `mid.bin` fails its parent outright, and the run reports
zero bad parents, so every observed `k` is ≤ 5. §4.1's allowance and §7.3's cap are mutually
unreachable. Not a soundness issue. **Fix:** state `k ≤ 7` (or report the histogram of `k`). Owner: T5
(`results/code-audit.md` F3).

**I4 (M, specification). The Stage-C clustering cutoff is degenerate at the two coarsest grids.** The
candidate threshold `(.042 - 1.11w)²` has a negative base for `M < 26`, so squaring turns it into an
absolute value and the effective merge radius is non-monotone: `.0505 → .0042 → .0189 → .0304`. At
`M = 24` no bin can merge (neighbouring midpoints are .0417 apart, the coordinate cutoff is .0060), so
clustering degenerates to one centre per bin — the most expensive regime, and the one where the
2048-centre cap trips. A clustering failure is unresolved, never negative, so soundness survives.
**Fix:** write the cutoff as `max(0, .042 - X_M)²`, or delete the merge. Owner: T5 + T3
(`results/code-audit.md` F2).

**I5 (L, arithmetic). A printed intermediate does not follow.** §A.10 reads
`‖e(P)/√6‖ ≤ √(1 + (2π²/6)·10⁻⁶) < 1.00000075 < K` as typeset (PDF p. 70; (6.3) at PDF p. 41 is the
same inequality). At `f0 = 10⁻⁶` the square root is `1.0000016`, and the linear expression is
`1.0000033`; neither is `1.00000075`. Both are below `K = 1.00001`, so nothing breaks, but one of the
three numbers is wrong. Owner: T5 (re-derive the line; keep K).

**I6 (L, notation). `ε`, `D`, `N`, `k`, `m`, `S`, `s`, `d`, `z` each carry two or three meanings.**
`notation.tex` Table 2 fixes all of them. The two that matter most for a checker are `D` (comparison
block / scalar distance bound / `D̂(t)`, the computed Stage-B function) and `m` (the pair of singular
bounds / `m_j = |D_j|` / the integer lift `m ∈ Z⁶` in Lemma 6.4). Owner: T8 + T2.

**I7 (L, notation). "Sphere" and "ball" are used for the same object**, and `Def 4.14` says so in
passing. A sphere includes its interior; the object is closed and bounded, and it is a set of phase
matrices up to equivalence. `notation.tex` Table 3 bans "sphere". Owner: T8.

**I8 (M, formal). `S(P,R)` is a set of equivalence classes, and (5.26) takes unions of such sets.**
`Def 4.14` defines the solution set of a Record as a set of classes `[e(P+δ)]`, "up to the
extendibility-preserving equivalences of Lemma 4.7", and explicitly allows the chosen equivalence to
differ per assignment. `prop-5.7` then unions `S(P,R)` over parents and atlas children. A union of
classes under different equivalences is not well defined as a set of classes; the statement is
literally true only if the ambient group is fixed. **Fix:** state coverage per exact matrix ("for every
exact δ in the parent there is a child and an allowed Φ with Φδ in the child"), and let the classes be
notation. Owner: T4 (and T9 should attack it).

**I9 (M, statement strength). (5.26) is trivially satisfiable.** Its right side retains every parent
whose refinement failed, so the inclusion alone never shrinks a cover. The stage's content is
"completed with an **empty** bad list", which is what `cor-5.8` uses. The paper's prose is aware of
this, but the display reads as a refinement step. **Fix:** print the empty-bad-list corollary as the
refinement step and (5.26) as the safety net. Owner: T8.

**I10 (L, evidence). Table 2 binds an archive that is not in the packet.** The eight SHA-256 digests
are unverifiable and 356+288k-byte records are never exhibited. §7.5's honest paragraph does not say
this; the audit does (`results/code-audit.md` §0). **Fix:** say it once, in the verification section.
Owner: T8.

**I11 (L, certificate content). The Record stores eight doubles (seven constants + radius) and 36k for
the frame — and nothing else.** Lemma 4.8's `q_d` and `slack`, Lemma 4.15's `Φ` and `N`, and the
Stage-B `ℓ` are not in that layout. Each is needed to check the corresponding lemma. Owner: T2
(`results/code-audit.md` F7).

**I12 (L, presentation). Theorem 1.1's "Consequently N(6) = 3" leans on Lemma 1.2 (§1.3), while
Theorem 7.1 states only non-existence.** Not an error, but the join should be printed where the theorem
is. Owner: T8.

**What I checked and found consistent** (so that it is not re-done): the count arithmetic of Table 1
and §7.3 (binomials, shard splits, 87·256+107, 282·3+281, 73+15 = 88, 163 = sum of the fifteen bad
files); `R_s = 2π·0.0320001 = .20106`; the Lemma 6.5 chain `2π√6·.2 < 22/7`; `K = 1.00001` dominating
`√(1+(2π²/6)·10⁻⁶)`; `q_d < 3.8` keeping `1 - q_d/4` positive; the union in (5.26); and the status of
every claim in `results/proof-claims.md` against the paper's own statement. I did **not** re-derive the
Appendix A budgets, the §3 Taylor ledgers, or anything that requires the sources.

---

## 5. Where the argument could be circular (for T9)

1. **Stage B's blocker induction.** `prop-5.7` is proved by induction on completed parents, with a
   blocker allowed only if it was already completed. If either implementation or the new reference
   implementation allowed a not-yet-completed parent as a blocker, the induction would be circular and
   the paper's statement would not notice. This is the only place in the paper where the order of
   processing is load-bearing. `prop-5.7`, `lem-5.6`.
2. **Stage A's "covered by a certified phase ball" versus "excluded".** `prop-3.11` assumes every
   terminal cell is one of the two. A cell that is both (an exclusion *and* a cover) is harmless; a cell
   that is neither is unresolved, and the paper says so. Check that the implementation cannot label a
   cell as "covered" using the same computation that failed to exclude it at a coarser grid.
3. **Root from a centre that is not a solution.** `prop-4.6` is the only link that turns a numerical
   object into a certificate. If it is false, every later stage is vacuous but silent. This is why I
   recommend **P** + **E** for it rather than trusting A.5.
4. **The clique search.** `lem-6.8`'s proof is a description of an algorithm; a cap is correctly
   declared not to be a certificate, but an *incomplete* enumeration that terminates normally would be
   indistinguishable in the record. Needs the mathematical criterion (F9).

---

## 6. Limits of this report

* I read `.scratch/mub6.txt` in full for §§1-7 and A.1-A.3, A.10, A.12, and used `pdftotext -layout`
  for page anchoring and for the lines I quote in I5. I did **not** read A.4-A.9, A.11 line by line:
  their content enters `claims.yaml` only through `app-a4-a11` and the margin table.
* I did not verify any S statement against source (not in the packet), and I did not run any of the
  paper's computations.
* `claims.yaml` is frozen. Anything I got wrong is fixed by a change request, not by an edit.

---

## 7. Change requests received before G0

`work/01-catalogue/changerequests/T1-audit.md` (from m3, direction d2) landed after my first draft of
`claims.yaml`. I checked each item against the PDF with `pdftotext -layout` and accepted four, noted
four, and one is a documentation fix:

| CR | verdict | what changed |
|---|---|---|
| CR-T1A-1 `b = 8‖M‖, 6‖S‖` | **accepted** | the radicals sit on the line above the display; the entries now read `sqrt(8)`, `sqrt(6)`, and §A.5's `C = π√8·mnorm + 1e-7` confirms it |
| CR-T1A-2 `E_r²` coefficient | **accepted** | the coefficient of `h⁴` is `((√6·√42)/2)² = 63`, not `(√6·42/2)²`; §A.4's `E_3 = (1/2)√252 h²` matches |
| CR-T1A-3 `S_Δ/π` inside the radical | **accepted** | confirmed independently on dimensional grounds (`S_Δ` is a squared length) and by `covercompute::value` |
| CR-T1A-4 missing ids | **accepted** | five entries added: `root-disp-n` (4.5), `root-disp-s` (4.6), `root-diff` (4.7), `root-suff` (4.15), `stagec-iface` (6.2) |
| CR-T1A-5 `(6.8)` sign of `J` | **noted** | recorded in `lem-6.3`'s open questions with the audit's proposed `conj(S_i)`. I could not settle the intent from the prose; T3/T4 must |
| CR-T1A-6 page convention | **accepted as a caveat** | the header no longer asserts a single offset; section and equation numbers are declared authoritative |
| CR-T1A-7 `u, Δ ∈ R^5` | **noted** | recorded in `lem-2.7`'s open questions; the index range must be read off the PDF before formalising. The inequality is unaffected |
| CR-T1A-8 `(2.18)` tautology | **accepted** | the entry now reads `2k·h ≤ Σ_j |k_j|` |

Lesson worth recording for the next gate: the layout-extraction in `.scratch/mub6.txt` drops radicals
onto the preceding line, so **every constant in the inventory that came from a display with a radical
must be re-read with `pdftotext -layout`**. The four accepted items are all of that kind. Anyone
citing a constant from `claims.yaml` should apply the same check once.
