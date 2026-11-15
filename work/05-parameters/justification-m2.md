# Every constant: constraint, slack, sensitivity, recommendation (member m2)

T5 / Parameters. Scripts: `experiments/n_window.py`, `seedcover_x.py`, `seedcover_y.py`,
`n_sweep.py`, `cost_model.py`, `boxes_k.py`, `stagec_cutoff.py`, `constants_batch.py`,
`caps_table.py`, `pairs_variants.py`, `y_testset_search.py`. Tables: `data/*.csv`
(`seedcover_sweep.csv`, `boxes_k.csv`, `stagec_cutoff.csv`, `stagec_clusters.csv`,
`constants.csv`, `margins.csv`, `cost_model.csv`, `caps.csv`).

Status vocabulary: **justified** = the paper proves, or the scripts verify, an inequality
that pins the value within a factor 2; **arbitrary-but-harmless** = any value in a wide
range is sound, so no change is needed but the choice should be labelled a choice;
**needs change** = the stated justification is wrong, a type contract is violated, or a
value is unreachable.

## 1. Seed cover (§2.2–2.4, A.3)

| constant | where | constraining inequality | current | slack | at half / at double | recommendation | status |
|---|---|---|---|---|---|---|---|
| N (bin count) | 2.2, 7.3 | int8_t on stored differences: N−1 ≤ 127; and 3/(2N) ≤ R=.032 | 112 | max diff 111 of 127 (16 headroom); fresh-centre 41.9% of R | 56: fine, 15% faster, fresh margin 1.19× / 224: int8 **and** 2³¹ both fail | keep; justify by int8, not by 2³¹ | needs change (justification) |
| w = 1/N (stored width) | 2.2, A.3 | A.3 error budget 10⁻¹⁴ against a 10⁻⁸ comparison slack; §5.6 range w ≤ 0.05 | 0.008929 | 10⁶× on error; 5.6× under the range | 1/224 = .00446 still in range / 1/56 = .0179 | none | justified |
| R (ball radius) | 2.4, 2.10 | 3/(2N) ≤ R ≤ .203/(2π) = .032309 (A.13) | .032 | 2.39× above the floor; **0.96% below the ceiling** | .016: needs N ≥ 94, still inside the window / .064: R_s = .402 > .203, A.4's frame bound fails | keep; note the upper end is tight | justified (tight above) |
| R = .0320001 | 2.4, A.3 | covers the 10⁻¹⁴ seed-phase rounding, stays under .032309 | .0320001 | 10⁷× on the error | n/a / .0640002 fails | keep | justified |
| reuse threshold (NR)²−10⁻⁴ | 2.4, A.3 | success iff (2.17) bound < (NR)²−10⁻⁴; float error < 10⁻¹² | 12.844956 | 10⁸× on the error; costs 0.0004% of the radius | ½·10⁻⁴ / 2·10⁻⁴ both harmless | keep | justified |
| gap thresholds 1−(l−1)/N, 1−(l+2)/N | 2.2, (2.8) | Lemma 2.5: the two thresholds differ by 3/N, the perturbation is w = 1/N | — | ratio 3 for every N | invariant / invariant | none: this is a clean 3× margin | justified |
| divisor skip 10⁻⁶ | 2.3 (`extend`) | skipping a divisor only *removes* a constraint | 10⁻⁶ | accepted divisors > .999·10⁻⁶ give endpoint error < 10⁻⁷ vs a 10⁻⁵ margin (100×) | 5·10⁻⁷: conservative / 2·10⁻⁶: conservative | keep | justified |
| 151,744,086 "pairs" | 7.3, 7.5 | must be ≤ Σ_Xlist (#Y lists in its shared bin) | 151,744,086 | see §2 of N112-m2.md: the stated tests give 112,160,350, so the printed number is 35% **above** the allowed maximum | — | print the per-side counts, or explain the traversal | needs change |
| 22,829 X lists; 249,878 centres | 7.5 | completeness of the traversal | — | reproduced exactly (X lists); centres modelled | — | keep; state the filters that produce them | justified |

## 2. Stage A and the U(2) cover (§3, §4, A.4)

| constant | where | constraining inequality | current | slack | at half / at double | recommendation | status |
|---|---|---|---|---|---|---|---|
| N_u = 16 (base grid) | 3.3, 7.3 | h = π/N_u < .197 (A.13), which needs N_u ≥ π/.197 = 15.95 | 16 | h = .19635, **0.33%** under .197; z(3.19) = 1.44 < 1.5 (4%) | 8: h = .393, z = 1.51 > 1.5 fails / 32: z = 0.98, 35% slack | keep; add the one-line derivation | justified (tight) |
| h = π/N_u | 3.3 | same as N_u | .19635 | see above | see above | none | justified |
| refinement 16→32→64…→512 | 3.3, 7.3 | enumeration cap 10⁶: grid 64 has 64⁴/8 = 2,097,152 cells per seed, so depth ≥ 4 rests on coverage, not enumeration | 512 deepest | 8.6·10⁹ cells at 512 is unreachable by enumeration | 256: fewer coverage chances / 1024: more cost | say explicitly that depth ≥ 4 rests on the ball cover (F5) | arbitrary-but-harmless (label it) |
| local target .103 | 4.6, 7.2 | certified cover bound < .103, else subdivide | .103 | 17.6% below the atlas cap .125 | .0515: more subdivision / .206 > .125 conflicts with the atlas cap | keep | arbitrary-but-harmless |
| atlas cap .125 (global target) | 4.7, 7.2 | R_A ≤ .125 < .126 (Stage-B input cap) | .125 | **0.79%** below .126 | .0625: more records / .25 > .126 fails B's range check | keep; the tightest radius chain in the paper | justified (tight) |
| seed radius at A .0320001 | 7.2 | ≤ .032309 | .0320001 | 0.96% | see R | none | justified |
| extra-node cap 10⁶ | 3.3, 7.3 | per seed; node counts unreported | 10⁶ | never hit (no unresolved seed), but grid 64 has 2,097,152 cells > cap, so it *can* bind | 5·10⁵: more unresolved / 2·10⁶: none | report the per-seed node histogram (F6) | needs change (evidence) |
| atlas cap 2·10⁶ Roots | 4.7, 7.3 | A output must fit | 2·10⁶ | recorded 3,083 records = **0.15%**; 649× slack | 10⁶: still 300× / 4·10⁶: none | none | arbitrary-but-harmless |
| Root dimension k ≤ 10 | Def 4.1, 5.6 | box cap 5·10⁷ with L = ⌈R/w + .500001⌉: k ≤ 5 (passes 1–2), k ≤ 7 (pass 3) | 10 | unreachable: (2L+1)¹⁰ would need 8.3·10⁵× (pass 1), 1.6·10⁷× (pass 2), 519× (pass 3) the cap | k ≤ 5 unchanged / k ≤ 10 needs a cap of 8.2·10¹⁴ | restate as k ≤ 7 (or ≤ 5 for the B inputs) and print the observed histogram | needs change (F3) |
| eigenvalue split .64 | 4.2 | none: proposal threshold; the certificate checks ‖T*T−I‖ ≤ ort | .64 | accepted columns have σ ≥ 1−10⁻⁵, i.e. .36 above the threshold; no stated bound on the normal side | .32: more T columns, >10 causes failure / 1.28: no T columns, k = 0, coverage fails | keep; call it a proposal heuristic | arbitrary-but-harmless |
| β = .45, β = .8 | 4.5, Lemma 4.11 | Gl ⪰ (1+β)r²AA* + (1+1/β)q²BB*, any β ∈ (0,1) | .45, .8 | factors 1.45/3.22 and 1.8/2.25; the earlier bound's own value 1.45R_s² < .06 | .225: error factor 5.44, weaker / .9: 1.9, still valid | keep; state that β is free | arbitrary-but-harmless |
| 30 bootstrap updates | 4.6, 4.13 | each update is an upper bound; no convergence is assumed | 30 | effort only | 15: more subdivision / 60: more work | keep | arbitrary-but-harmless |
| K = 1.00001 | (6.3), (A.17) | K > ‖T‖ = √(1+ort) with ort < 10⁻⁵, i.e. K > 1.000005 | 1.00001 | **a factor 2 in the excess** (5·10⁻⁶) | 1.000005: at the boundary, any rounding fails / 1.00002: harmless | keep; cross-reference the ort < 10⁻⁵ threshold | justified (tight) |
| q_d < 3.8 | 4.8, A.7 | the bound needs √(1−q/4), so q < 4; amplification (1−q/4)^{−1/2} | 3.8 | 1−q/4 = .05 > .049; amplification ≤ 4.52 | 1.9: amplification 1.34, more cells rejected / 7.6 > 4: **no real square root, unsound** | keep | justified |
| 25 midpoint trials | 5.2 | a single stored successful trial is the certificate | 25 | effort only | 12: more relations decline / 50: more work | keep | arbitrary-but-harmless |
| ell sentinel 100 | 4.6, A.8 | must be outside the legitimate range, but A.8 proves the certified bound ≤ 100.1 | 100 | **negative**: not distinguishable from a valid bound | — | use NaN with a checked isnan, or a status flag | needs change (F4) |
| sentinels 10 (bootstrap, relationB) and the "t<10" guard | 4.6, 5.1 | the guard must not be reachable by a valid t | 10 | same class as above; works only because the local target is .103 | — | one sentinel representation, checked | needs change (F4) |
| acceptance thresholds id < 10⁻⁴, ort,hor < 10⁻⁵, C < 20, mnorm < 2, γ_P < 20, n0,ε_P < 10⁻⁶, α_P < 10⁻⁴, o_P,hor_P < 10⁻⁵, µ_P < 2 | A.5, 5.6 | each must exceed its A.5 error budget (2.1·10⁻¹¹ factor product, 10⁻⁹ per identity entry, 2·10⁻⁶ for id) | as listed | 10²–10⁶× | halving: still above the budgets / doubling: harmless | none | justified |

## 3. Stage B: refinement passes and caps (§5.6, A.9)

| constant | where | constraining inequality | current | slack | at half / at double | recommendation | status |
|---|---|---|---|---|---|---|---|
| (τ,w) = (.07,.013) | 5.6 | w < τ (the boxes must be finer than the child they refine); L = ⌈.125/.013 + .5⌉ = 11, 23 boxes/axis, k ≤ 5, grid ≤ 28.6·10⁶ | .013 | w/τ = .186 for the input radius .125; grid 6.44·10⁶ at k=5 = 12.9% of the cap | .0065: L = 20, 41/axis, k ≤ 4 / .026: L = 5, 11/axis | keep | justified |
| (τ,w) = (.016,.005) | 5.6 | same, input radius .07: L = 15, 31/axis; grid 28,629,151 at k=5 | .005 | **57.3% of the 5·10⁷ cap** (1.75× slack) | .0025: L = 29, 59/axis, k ≤ 4 / .01: L = 8, 17/axis | keep; the k=5 grid here is the largest object in Stage B | justified (tightest B constant) |
| (τ,w) = (.011,.0038) | 5.6 | input radius .016: L = 5, 11/axis, k ≤ 7 | .0038 | grid 19,487,171 at k=7 = 39% of the cap | .0019: L = 9, 19/axis, k ≤ 5 / .0076: L = 3, 7/axis, k ≤ 8 | keep | justified |
| w < τ (why the fine pass needs it) | 5.2, Lemma 5.5 | the box half-width must be below the child radius, else one box *is* the child and the relation test cannot shrink | ratios 5.4×, 3.2×, 2.9× | all pass | w = τ: coverage degenerates to a single box, no progress | keep; state the ratio | justified |
| radius chain .125 → .07 → .016 → .011 | 5.6, 7.2 | each pass must shrink; depth ≤ 6 | 4 passes | factors 1.79, 4.38, 1.45 | — | none | justified |
| box cap 5·10⁷ | 5.6, 7.3 | (2L+1)^k ≤ 5·10⁷ per parent | 5·10⁷ | largest actual 28,629,151 (57%); 1.75× | 2.5·10⁷: fails k=5 in pass 2 → pass 2 unresolved / 10⁸: admits k=6 at pass 1 (148·10⁶ still over) | keep; it is what makes F3 matter | justified |
| graph-step cap 5·10⁶ | 6.6, 7.3 | a cap hit is *unresolved*, never negative | 5·10⁶ | **binding**: 163 of 22,379 initial C records (0.73%) hit it; all resolved by B fallback + final C | 2.5·10⁶: more fallback work / 10⁷: fewer cap hits | keep; report the 163 as a class with their step counts | justified (binding, harmless) |
| cluster cap 2048 | 6.3, 7.3 | exceeding it is unresolved | 2048 | unreported; a synthetic 2-torus model reaches **1,626 centres at M=24** (79% of the cap) | 1024: plausibly exhausted at M=24 / 4096: none | report the per-level cluster counts; the cap is the thinnest in Stage C | needs change (evidence) |
| C bin cap 2·10⁶ | 6.3, 7.3 | retained bins; overflow is unresolved | 2·10⁶ | first grid 248,832 (12.4%); ≤ 32 children per retained bin | 10⁶: still 4× the first grid / 4·10⁶: none | none | arbitrary-but-harmless |
| records per file 2·10⁶ | 7.2 | file integrity | 2·10⁶ | largest file 22,379 records (1.1%); batches ≤ 256 | 10⁶: fine / 4·10⁶: fine | none | arbitrary-but-harmless |
| concatenated inputs 8·10⁶ | 7.2, 7.3 | concatenation bound | 8·10⁶ | largest concatenation 22,379 (0.28%) | fine / fine | none | arbitrary-but-harmless |
| depth 6 | 5.6, 7.3 | subdivision depth per box | 6 | never reached; the radius shrinks ≥ 1.45 per pass | 3: more unresolved / 12: no extra power | none | arbitrary-but-harmless |

## 4. Stage C: the clustering cutoff (F2)

The paper (§6.3): "w = 1/M, the candidate threshold is (.042 − 1.11w)², and the
coordinate cutoff is the square root of twice that threshold plus 10⁻¹⁰." With
X_M = √(29/6)/(2M) = 1.09924/M < 1.11/M (Lemma 6.1), the base is negative for M ≤ 26,
and squaring hides it, so the effective radius is |.042 − 1.11/M| — non-monotone
(`stagec_cutoff.py`, `data/stagec_cutoff.csv`):

| M | X_M | 1.11/M | base | threshold | coordinate cutoff | smallest nonzero *projected* separation | cutoff/sep |
|---|---|---|---|---|---|---|---|
| 12 | .09160 | .09250 | −.05050 | 2.550·10⁻³ | **.07142** | .06944 | 1.03 |
| 24 | .04580 | .04625 | −.00425 | 1.806·10⁻⁵ | **.00601** | .03472 | 0.17 |
| 48 | .02290 | .02313 | +.01887 | 3.563·10⁻⁴ | .02669 | .01736 | 1.54 |
| 96 | .01145 | .01156 | +.03044 | 9.264·10⁻⁴ | .04305 | .00868 | 4.96 |

Consequences, measured on a synthetic 2-torus of bins clustered with the paper's rule
(`data/stagec_clusters.csv`):

| M | bins | centres (printed formula) | centres (max(0,·)²) | compression |
|---|---|---|---|---|
| 12 | 432 | 81 | 432 | 5.33 / 1.00 |
| 24 | 1,626 | **1,626** | 1,626 | **1.00 / 1.00** |
| 48 | 6,028 | 465 | 465 | 12.96 / 12.96 |
| 96 | 21,507 | 205 | 205 | 104.9 / 104.9 |

* The F2 arithmetic is right, and the mechanism is worse than a wasted heuristic: at
  M = 24 the coordinate cutoff is 6.0·10⁻³ against a smallest nonzero projected
  separation of (5/6)/24 = 3.47·10⁻², so no two distinct bins can merge and clustering
  degenerates to one centre per bin — while M = 12 compresses 5.3× and M = 96
  compresses 105×. Across the refinement chain the centre count is
  **81 → 1,626 → 465 → 205**: the intermediate level is by far the most expensive, and
  1,626 is within 26% of the 2048 cap.
* **The recommended fix `max(0, .042 − 1.11w)²` does not work.** Its base is 0 for every
  M ≤ 26, so the cutoff is 0 and nothing merges — at M = 12 it turns a 5.3× compression
  into 1.00. The sign bug is real, but clamping is not the repair. Sound options, in
  order of preference: (i) delete the distance cutoff and let the final radius update
  carry the covering (Lemma 6.4 already certifies it; the cutoff only chooses
  assignments); (ii) keep the printed expression but document it as |.042 − 1.11/M| and
  say that clustering is heuristic; (iii) use .042 + 1.11/M, which is monotone
  decreasing in M and never zero. The paper's own reading supports (i): "These constants
  affect only the choice of assignments; the proof is the final radius update in
  Lemma 6.4."

Status: **needs change** (F2). Severity stays as the audit has it — soundness is
untouched — but the remedy the plan proposes must be replaced.

## 5. Appendix A's closing table: error, margin, ratio

`constants_batch.py` §E reproduces all 24 rows; `data/margins.csv`. Ratios run from
**1.25** to 10⁵. The single thin row is *Candidate external tangent error* 1.2·10⁻⁴ rad
against a margin of 1.5·10⁻⁴ rad — 1.25×, not the "one to three orders of magnitude"
that `results/code-audit.md` §4 reports for the table as a whole. Everything else is
≥ 10×; the median is 200×. Recommendation: print the ratios (a column), and say in the
text that the tangent arc is the thin one, so a retune there is the first thing to check.

## 6. Answer to the four questions, in one line each

1. **Inequality.** Every constant above now has one; the notable discoveries are that
   N is pinned *above* by int8_t (128) rather than by 32-bit arithmetic (189), that
   R is pinned within 1% from above by R_s < .203, that N_u = 16 is the exact minimum
   admissible under h < .197, and that K = 1.00001 sits a factor 2 above its need.
2. **Slack.** Three constants are tight (R 0.96%, atlas cap .125 0.79%, N_u 0.33%, K a
   factor 2); one is binding in the recorded run (graph steps, 163 records); one is
   degenerate (the Stage-C cutoff at M = 24); one is unreachable (k ≤ 10); one is
   unverifiable as printed (151,744,086 pairs).
3. **Cost curve.** The measured cost curve for N is flat within 15% over [47,128] and
   rises as N^4.15 beyond; the binding resource is stage A + B + C at 15.4 ms per
   retained centre, not the cover.
4. **Recommendation.** Keep N = 112, R = .032, N_u = 16, the three (τ,w) pairs and the
   caps; change the *justification* of N, the *statement* of k, the *sentinel*
   representation, the *pair count* of Table 1, and the Stage-C *cutoff*.
