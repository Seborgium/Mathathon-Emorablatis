# Every constant in the dimension-six MUB proof: constraint, slack, cost, recommendation

Team T5 ("Parameters"). Every number below is produced by a script in
`work/05-parameters/experiments/`; the tables are in `work/05-parameters/data/`.
Where a number in `results/code-audit.md` or `results/plan.md` is wrong, the row says so
and names the script. Nothing here changes a threshold: the column "recommendation" is a
recommendation to T8 and the lead.

Status vocabulary:

* **justified** — the paper states an inequality that fixes the value, and the value satisfies
  it with a computable slack.
* **arbitrary-but-harmless** — no inequality constrains it; every failure mode it can cause is
  an *unresolved* outcome (more work), never a *negative* one (a wrong exclusion). Safe to
  leave, worth one sentence.
* **needs change** — the stated value, or the sentence that justifies it, is false or
  unreachable as written, and a reader checking it will find the contradiction.

Two global facts make most rows easy and are worth stating once.

**(G1) Nothing in this proof is a tolerance chain.** Each margin is compared against one
established error, not accumulated across stages, and a failed comparison produces
"unresolved", never "excluded" (Propositions 2.10, 3.11, 4.16, 5.7, 6.9 and Corollary 5.8 all
have that form). So the numerical safety of the proof is the *minimum* of the ratios in the
Appendix A table, not their product: it is **1.25** (the tangent margin `.00015` against
`.00012` rad) — see §7. That is the number the paper should print.

**(G2) The one cap that is actually binding is the graph-step cap.** Of the nine caps, eight
have at least 8× headroom in the recorded run; the graph cap was hit **163 times** and is
the entire reason the fallback stage exists. §6.

---

## 1. The seed-cover bin count N = 112

Full argument: `N112.md`. Summary row:

| constant | where | the inequality that constrains it | current value | slack | at half / at double | recommendation | status |
|---|---|---|---|---|---|---|---|
| bin count `N` | §2.2 (2.6), §2.4, A.3, §7.3 | **(C1)** `C(N+4,5) < 2^31` ⟹ `N ≤ 189`; **(C2)** `3/(2N) ≤ R = .032` ⟹ `N ≥ 47`; **(C3)** `N-1 ≤ 127` (int8 bin differences) ⟹ `N ≤ 128`; **(C4)** the coordinatewise reuse bound (2.18) needs `(NR)² > 4.25` ⟹ `N ≥ 65` (soft) | 112 | C1: 41% below the ceiling; C2: 2.39× (bin radius is 41.9% of R); C3: 16 units of int8 range spare, i.e. 87.5% of the ceiling; C4: `(NR)² = 12.845` against the `4.25` a nonzero offset needs, and 284,055 lattice points inside the reach `NR = 3.584` | 56: correct (C2 ratio 1.003 at 47), tuples ×0.034, but `(NR)² = 3.21 < 4.25`, so no nonzero offset can be certified and reuse collapses; 224: **breaks C1, C3 and the memory model** (C(228,5)=4.9e9, differences 223 ≫ int8) | state the window `[47,189]`, narrowed to `[47,128]` by the `int8` storage, and call 112 a cost choice; see `N112.md` §6 for the paragraph to paste | needs change (the *reason given* is wrong; the value is fine) |

## 2. The seed ball radius and its enlargement

| constant | where | the inequality that constrains it | current value | slack | at half / at double | recommendation | status |
|---|---|---|---|---|---|---|---|
| `R = .032` | §2.4, Prop 2.10, §7.2 (`.0320001`) | fresh midpoint covers its bin: `√9/(2N) = 3/(2N) ≤ R`; at `N=112`, `3/224 = .013393` | .032 | `R/(3/2N) = 2.389`; 58.1% of R unused | half (.016): forces `N ≥ 94` and multiplies the centre count by ~32 (est. 8.0 M centres, ~18 h of A); double (.064): bin argument trivial, centres ÷32 (est. 7.8 k), but every seed ball then needs more U(2) cells covered | keep .032; say that it is chosen *looser* than the bin needs by 2.39× | justified |
| `.0320001` | §2.4 last line, §7.2 (`seed radius .0320001`) | nine stored binary midpoint phases differ from the rational midpoints by `< 1e-14` in norm | .0320001 | `1e-7 / 1e-14 = 1e7` | half: 5e-8, still 5e6× the error; double: 2e-7, harmless | keep; state "1e-7 dominates 1e-14" | justified (1e7 over-conservative) |
| reuse threshold `(fl(.032·112))² − 1e-4` | §2.4 (`testBucket`), A.3 | `RN2 < (.032·112)²` with the comparison error before the subtraction `< 1e-12` | `12.844956` | `1e-4/1e-12 = 1e8`; effective radius `√RN2/112 = .031999875` (3.9e-6 below R) | 1e-8 instead of 1e-4: still `1e4` above the error and the effective radius is `.032` to 9 decimals; 1e-2: effective radius `.0317`, still sound, 0.4% fewer successful reuses | keep; the margin is 8 orders larger than needed and costs 4e-6 of relative radius, i.e. nothing — say so | justified (over-conservative) |
| `w = 1/N` in Lemma 2.5 and the gap filter (2.8) | §2.2, Lemma 2.6 | thresholds `1-(l-1)/N` and `1-(l+2)/N` differ by `3/N`; Lemma 2.5 bounds the perturbation by `w = 1/N` | `1/112` | the filter is exactly what Lemma 2.5 implies: **ratio 3 at every N**, zero slack by design and zero dependence on N | halving N doubles both sides; no constraint on N | nothing to change; state that (2.8) is tight, not slack | justified |
| divisor skip `1e-6` in `extend` | §2.3 | skipping a divisor *removes* a constraint, so the intersection only grows | 1e-6 | none needed for soundness; at the accepted `|a| > .999e-6` the quotients stay `≤ 1.2e8` and the endpoint error `1e-7/|a|` stays below `1e-5` | 1e-9: endpoint error budget rises to 100 — the `1e-5` endpoint margin no longer dominates | keep, and **report how many divisors were skipped**: the count measures how much weaker than advertised the filter is | arbitrary-but-harmless |
| `1.251 π/N` instead of `1.25 π/N` in `supdual` | §2.4, A.3 | the remainder coefficient must be an upper bound; `1.251 > 1.25` | 1.251 | 0.08% over the true coefficient; costs `2·(1.251-1.25)π/N · |v| ≈ 5e-4` of the support bound | 1.252 would also be sound and slightly weaker; 1.25 exactly would be unsound | keep; it is the smallest possible 3-digit overshoot | justified |
| `|v_a| ≤ 1e4` and the final support margin `.01` | §2.4, A.3 | `2 Σ|v_a|·3e-11 ≤ 2.4e-6 < 2.5e-6` (the sub-budget), then the margin must exceed the arithmetic error `< 1e-7 + 1e-4` | 1e4, .01 | the `1e4` cap is *derived*: at `2e4` the sub-budget would be `4.8e-6` and the proof's `2.5e-6` fails; `.01/.0001 = 100` | 5e3: halves the budget, tighter proposals, harmless; 2e4: breaks the stated sub-budget | keep 1e4; it is one of the few caps with a derivation — say so | justified |

## 3. The U(2) grid and the two targets

| constant | where | the inequality that constrains it | current value | slack | at half / at double | recommendation | status |
|---|---|---|---|---|---|---|---|
| `N_u = 16` base grid | §3.3, §3.7 | `4 \| N_u` (bin counts `N_u/2, N_u/4, N_u, N_u` must be integers); level-1 Taylor remainder must be coverable by the global target (§ next row) | 16 | cells per seed `16^4/8 = 8,192` = 0.8% of the 1e6 node cap | 8: `N_u/4 = 2` still integral, remainder falls to `.0312`, but the base grid no longer resolves the phases the fixed frames need; 32: base remainder `.0312`, cells ×16 — the paper would simply start one level deeper and lose the cheap first pass | keep 16 | justified (by `4 \| N_u` and by cost) |
| `h = π/N_u` | §3.3 (3.13) | Lemma 3.4: `‖V-U‖_F ≤ √6 h`, `‖V-U-dU[θ]‖_F ≤ (√42/2) h²` | `π/16` at level 1 | see the `.125` row | — | keep | justified |
| global target `.125` | §4.7 (atlas radius cap), §7.2 | a ball must dominate the second-order Taylor remainder of the cell it covers: `(√42/2)(π/16)² = .1249265 ≤ .125` | .125 | **ratio 1.00059** — the tightest inequality in the paper outside Appendix A's tangent margin | half (.0625): no longer dominates a level-1 cell (`.1249`), still dominates a level-2 cell (`.0312`); double (.25): safe, and inflates the atlas cap, the child cap `.126`, and every Stage-B radius | keep .125, but **say which level it is sized for**. If it is "one ball per level-1 cell", the slack is 0.06% and the paper must say so; if it is "level 2 and deeper", it is 4.0× and `.0313` would do | needs change (the number is right, the reason is missing) |
| local target `.103` | §4.6, §7.2 | every certified `covercompute` bound for a Root must fit it; it must be `≤ .125` (atlas cap) so the merge can grow the radius | .103 | `.125/.103 = 1.214`; against the level-2 remainder, `.103/.0312 = 3.30` | half (.0515): below the level-2 remainder plus the seed radius, so Records would fail coverage and cells would subdivide; double (.206): exceeds the atlas cap `.125`, so no Record could ever be merged | **print the observed maximum local radius**. If it is `.06`, `.103` carries 1.7× and is a cost choice; if it is `.101`, the whole atlas is within 2% of its target and no other constant may move | needs change (no closed form reproduces .103; see `experiments/grid_u2.py` §3) |
| subdivision depth 6 / deepest grid 512 | §3.7, §5.1 | `16·2^5 = 512` is five doublings; depth 6 reaches 1024 | 6 | one level spare for Stage A; for B the six box halvings are exactly the cap | 5: forbids the 512 grid (the paper's stated deepest); 7: reachable only by spending 16× per level | keep 6, and say that the *binding* ceiling is 512, not the depth | justified |
| `1,000,000` extra nodes | §3.7, F5 | `64^4/8 = 2,097,152 > 1e6`, so from grid 64 enumeration is impossible and the phase-ball cover must fire | 1e6 | 0 unresolved seeds; at grid 32 the cell count is `.131` of the cap | 5e5: forces coverage already at 32 (cells 131,072 × 16 children = 2.1 M > 5e5); 2e6: permits exhaustive enumeration at 64 and changes the character of the run | keep; state that the cap forbids enumeration from grid 64, so completeness at depth ≥ 4 rests on coverage (this is F5's point) | justified |
| `.64` eigenvalue split | Prop 4.6 | none: the certificate is the direct check. The only quantitative requirement is on the *count* kept: `≤ 10` (Def 4.1/§5.1/§6.1) and in fact `≤ 5` for the mid pass (see §5) | .64 | unknown: the 25-coordinate spectrum is not reported | .32: more `T` columns — if `> 10` the Root is rejected (work, not unsoundness); 1.28: fewer columns, the norm exclusion test misses directions (work again) | print the five smallest eigenvalues and the adjacent gap; then `.64` is justified by the gap instead of by habit | arbitrary-but-harmless |

## 4. Roots, atlas and the ellipsoid

| constant | where | the inequality that constrains it | current value | slack | at half / at double | recommendation | status |
|---|---|---|---|---|---|---|---|
| `q_d < 3.8` | Lemma 4.8, A.7 | `(1-q_d/4)^{-1/2}` needs `q_d < 4`; the paper's own sentence "no individual chord reaches √2" needs `q_d < 2` | 3.8 | 0.2 below 4 (5% of denominator), but **1.8 above what the sentence claims** | 1.9: the sentence becomes true, and only records with `q_d ∈ [1.9,3.8)` change behaviour (more subdivision, never less coverage); 7.6: `(1-q/4)^{-1/2}` imaginary — unsound | restate as `q_d < 2`, or delete the sentence. `q_d` is never reported, so the cost is unknown but bounded by the 22,379 fine records | needs change |
| `β = .45` and `β = .8` | Lemma 4.11, (4.32)/(4.33) | `G ⪰ (1+β) r²AA* + (1+1/β) q²BB*` holds for **every** `β > 0` | .45, .8 | none needed for soundness; the two values encode assumed ratios `v/u = β²` of the D-contribution to the seed-contribution (.2025 and .64) | .225: inflates the D coefficient to 5.44; 1.6: inflates it to 1.625 but the seed coefficient to 2.6 | print `u = r²‖A‖²`, `v = q²‖B‖²` and use `β = √(v/u)`; the current values are defensible only as "we knew v/u" | arbitrary-but-harmless (safe for any β) |
| "at most 30 bootstrap updates" | §4.6, Prop 4.13 | each accepted update strictly decreases `s`, and any finite number preserves coverage — 30 is a work cap, not a convergence claim | 30 | unknown; fraction of records needing > 1 update is not reported | 15: more Records keep their initial radius (bigger, worse for B); 60: strictly more work, no soundness change | keep 30; report the update-count histogram | arbitrary-but-harmless |
| `10^8` trial-solve cap, `gap ≥ 1e-6`, `1e-10`-scale additions in `ell` | §4.5, A.8 | the `z` of (4.37) is only a *proposer*; the returned quadratic form is checked, so `‖z‖` may be anything finite | as stated | the residual expression carries an explicit `1/gap` factor, and `gap ≥ 1e-6` bounds it | `gap ≥ 5e-7`: `1/gap` doubles, the added `1e-10` no longer dominates the quotient | keep; these are the correct one-sided guards | justified |
| `2·10^-6` centre correction and the `.00015` rad tangent margin | Lemma 4.9 (4.20)–(4.21), §4.5, A.7 | `‖ε‖ ≤ 2e-6` cycles; external tangent error `< .00012` rad, so the margin must exceed it | `2e-6`, `.00015` | `2e-6` is the *established* error, not a margin; `.00015/.00012 = 1.25` | `.0001`: below the established `.00012` — unsound; `.0003`: every Record radius grows by `~2.4e-5` and Stage B does more work | keep; **this is the tightest number in the proof** (§7) and deserves a sentence saying so | justified (but the weakest link) |
| `100` as `ell`'s failure sentinel | §4.6 ("`ell` return 100"), A.8 (`gu ≤ 100.1`) | the sentinel must be distinguishable from every certified value; `100 ∈ [0, 100.1]` | 100 | none in the value; safety comes from converting to cycles (`100/2π = 15.92`) against the `t < 10` guard — a factor **1.59**, and nothing more | 50: still `7.96` cycles, still caught; 5: `0.796` cycles, accepted as a certified bound — silent unsoundness | use NaN with a checked `isnan`, or a separate status flag (F4) | needs change |
| `10` as `bootstrap`'s and `relationB::eval`'s failure sentinel | §4.6, §5.6 | every legitimate value there is a radius `≤ .126` or a tangent distance `≤ 2`; A.9 bounds all stored distances by `.378` | 10 | `10/.378 = 26×` above every legitimate value | 5: still 13× above `.378`; 0.3: below a legitimate radius — catastrophic | keep, but give them the same treatment as 100 (a flag), and record in one place that `10` is `26×` the largest legitimate value | arbitrary-but-harmless (one retune from unsound) |

## 5. Stage B: the three (τ,w) pairs

Table `data/stage_b.csv`; script `experiments/stage_b_widths.py`.

| constant | where | the inequality that constrains it | current value | slack | at half / at double | recommendation | status |
|---|---|---|---|---|---|---|---|
| `(τ,w) = (.07,.013)` (mid) | §5.1, §7.2 | `τ ≥` the radius the children must reach; `√k·w < τ` (a box's diameter must fit the child target); `(2L+1)^k ≤ 5e7` with `L = ⌈E/w + .500001⌉`, `E = √(1+ort)R + 1e-7`, `R ≤ .126` | .07, .013 | `√k·w = .0291`, `τ/(√k w) = 2.41`; `L = 11`, `23^k` with `k ≤ 5` | w halved: `L = 20`, `41^4 = 2.8 M` boxes — *fewer* than at `w`, because the axis doubles and the admissible `k` falls by one; w doubled: `.026`, `√k w = .058 > τ` so no box can be closed whole and the split recursion must run | keep; note that this pass costs 24% of the whole run (1071 s of 4470 s) | justified |
| `(τ,w) = (.016,.005)` (fine) | §5.1, §7.2 | as above, with the input radius **`.016`**, not `.07`: §7.2 replaces every batch radius by `.016` before B fine reads it | .016, .005 | `L = 4`, `9^k` with `k ≤ 8`; `√k w = .01414`, `τ/(√k w) = 1.13` | w halved: `L = 7`, `15^7 = 1.7e8` > 5e7 so `k ≤ 6`, fewer boxes at admissible `k`; w doubled: `.01·√8 = .0283 > τ` — boxes can no longer be closed | keep; the ratio 1.13 is the tightest of the three and is the real reason `w` must scale with `τ` | justified |
| `(τ,w) = (.011,.0038)` (fallback) | §5.1, §7.2 | as above, input radius `.016` | .011, .0038 | `L = 5`, `11^k` with `k ≤ 7`; `τ/(√k w) = 1.09` — the tightest in the run | w halved: `L = 9`, `19^7 = 8.9e8`, so `k ≤ 5` and only `19^5 = 2.5 M`; w doubled: `.0076·√5 = .017 > τ` | keep; it exists only because of the graph cap (§6) | justified |
| the *statement* `0 ≤ k ≤ 10` | Def 4.1, §5.1, §6.1, A.9 | `(2L+1)^k ≤ 5·10^7` | 10 | **unreachable**: the mid pass allows `k ≤ 5`, the fallback pass `k ≤ 7`, the fine pass `k ≤ 8` (see the correction below) | the allowance has no operating point | restate as `k ≤ 5` for the mid pass (the pass every coarse record must survive) or report the observed `k` histogram; do not keep a bound nothing can reach | needs change |
| `50,000,000` boxes | §5.1, §7.3 | `(2L+1)^k ≤ 5e7`; at the largest admissible `k` the count is `23^5 = 6.4 M` (mid), `9^8 = 43.0 M` (fine), `11^7 = 19.5 M` (fallback) | 5e7 | not hit; 12.9% used at the mid pass, **86% used at the fine pass** | halved (2.5e7): the fine pass falls to `k ≤ 7`, the mid pass unchanged; doubled: no pass gains a level (23^6 = 148 M still exceeds 1e8) | keep; and note that its real role is to *define* `k_max`, so the paper cannot state both `k ≤ 10` and this cap | needs change (as a pair with the row above) |
| `2,000,000` records per file, `8,000,000` concatenated | §5.1, §7.3 | file sizes must stay representable and batchable | 2e6 / 8e6 | recorded maxima 22,379 (1.1%) and 3,083 (0.04%) | halved: still 44× above `fine.bin`; doubled: no effect | keep; these are safety rails, and the paper should say so in one clause | arbitrary-but-harmless |
| "25 midpoint trials" | §5.6 (ρ-search) | bisection on `[0,1.01a]`, `a ≤ .126`, with acceptance tolerance `2e-7` (5.18); resolution after `k` trials is `1.01·.126/2^k` | 25 | resolution `3.8e-9`, i.e. **32×** below the tolerance; the smallest sufficient `k` is 20 | 12: resolution `3.1e-5`, coarser than the tolerance, so `ρ` would be left short by up to `3e-5` (still sound: the certificate uses the stored trial value); 50: no change | keep; 25 is justified by the resolution and not merely a habit — one of the few iteration caps that is | justified |
| "at most 30 attempted improvements" in `relationB::eval` | §5.6 | Lemma 5.3 holds after **any** finite number of steps; the certified object is the stored iterate | 30 | none needed | 15: larger upper bounds, more boxes marked; 60: more work | keep | arbitrary-but-harmless |
| raw-distance cuts `.249` / `.23` | §5.1, §6.4 (`relationB::init`) | a wrong cut can only *decline* a relation, never exclude a parent | .249, .23 | none needed | tighter cut: fewer relations tried, more subdivision; looser: more tries | keep; state in one line that they are opportunities, not filters | justified |
| batch radius replacement `→ .016` | §7.2 | `every original fine radius ≤ .016`, so the replacement *enlarges* the represented set | .016 | depends on mid.bin's actual radii, which are not reported; the claim is exactly "max mid radius ≤ .016" | — | **report the max radius in mid.bin**: the soundness of the batch concatenation rests on it, and it is one number | needs change (evidence, not arithmetic) |

**Correction to `results/code-audit.md` F3.** The audit's pass-2 row uses input radius `.07` and
gets `L = 15`, 31 boxes per axis, `k ≤ 5`. `.07` is the *mid pass's child cap* `τ`, not an input
radius: §7.2 replaces every batch radius by `.016` before B fine reads it. With `R_in = .016`:
`E = .0160002`, `E/w = 3.200036`, `L = 4`, **9 boxes per axis**, `k ≤ 8`. Both readings agree that
`k = 9, 10` are unreachable; they disagree on whether `k = 6` is admissible, which decides whether
the observed `k` histogram may contain a 6. Script: `experiments/stage_b_widths.py` §3.

## 6. The nine caps, against the recorded run

Table `data/caps.csv`; script `experiments/caps_margins.py`.

| cap | limit | largest value the recorded run reached | utilisation | recommendation | status |
|---|---|---|---|---|---|
| Stage A extra nodes | 1,000,000 | 0 unresolved seeds | 0% | the cap is *structural*: `64^4/8 = 2.1 M > 1e6`, so from grid 64 enumeration is forbidden and coverage must fire | justified |
| Stage B grid boxes | 50,000,000 | `23^5 = 6,436,343` (mid pass, largest admissible) | 12.9% | cannot bind; it defines `k_max` instead | needs change (as a pair with `k ≤ 10`) |
| atlas Roots | 2,000,000 | 788 (largest shard) | 0.04% | keep | arbitrary-but-harmless |
| Stage C phase bins | 2,000,000 | not reported; no bin overflow in 22,379 records | ≤ 25% for any record (else the first split would overflow) | report the max retained-bin count | needs change (evidence) |
| clusters per record | 2,048 | not reported; no clustering failure | unknown; needs a 976:1 compression at the bin cap | report the max cluster count and the bin:cluster ratio | needs change (evidence) |
| graph steps | 5,000,000 | **5,000,000 — hit 163 times** | 100% | the only binding cap; it created the fallback stage, which cost 44.4 s = 1.0% of the run. Doubling it would have saved that 1% and is otherwise harmless | justified (binding) |
| records per file | 2,000,000 | 22,379 (`fine.bin`) | 1.1% | keep | arbitrary-but-harmless |
| concatenated inputs | 8,000,000 | 3,083 (coarse → B mid) | 0.04% | keep | arbitrary-but-harmless |
| subdivision depth | 6 | 6 | 100% by construction | keep; the binding ceiling is the 512 grid, which is five doublings | justified |

## 7. The closing table of Appendix A, with ratios

Table `data/margins.csv`; script `experiments/caps_margins.py`. "Ratio" is margin / established
error; the paper prints the two columns and never the ratio, which is the number that decides
where the numerical risk is.

| certificate path | established adverse error | explicit margin | ratio |
|---|---|---|---|
| Candidate external tangent error | `.00012` rad | `.00015` rad | **1.25** |
| A flat norm | `1e-6` | `1e-5` | 10 |
| A directional comparison | `4e-6` | `1e-4` | 25 |
| C joint support | `1e-8` | `3e-7` | 30 |
| Root identity Frobenius check | `5e-8` | `2e-6` | 40 |
| B cross-Gram spectral perturbation | `2e-9` | `1e-7` | 50 |
| Candidate direct support | `2e-6` | `1e-4` | 50 |
| G entry error, second choice | `1e-9` | `1e-7` | 100 |
| seed dual support | `1e-4` | `.01` | 100 |
| Root orthogonal check | `1e-10` | `1e-8` | 100 |
| shared-coordinate endpoints | `1e-7` | `1e-5` | 100 |
| C direct / directional comparison | `1e-9` | `2e-7` | 200 |
| B projected normal / local update | `5e-11` | `1e-8` | 200 |
| tensor transformed row bound | `1e-6` | `2e-4` | 200 |
| spectral row-sum bound | `3e-13` | `1e-10` | 333 |
| seed direct support | `1e-11` | `1e-8` | 1000 |
| Root horizontal check | `1e-11` | `1e-8` | 1000 |
| spectral fourth-norm bound | `1e-10` | `2e-7` | 2000 |
| shared-coordinate numerator | `3.5e-11` | `1e-7` | 2857 |
| G entry error, first choice | `1e-11` | `1e-7` | 10000 |
| bootstrap update | `1e-12` | `1e-8` | 10000 |
| B local update (A.9) | `1e-13` | `1e-8` | 100000 |
| seed gap / direct support | `1e-14` | `1e-8` | 1000000 |

Median ratio 200; minimum **1.25**. A single sentence T8 can print: *the numerical risk of this
proof is concentrated in one inequality, `.00012 < .00015` rad on the external tangent error;
every other comparison has at least 8× and most have 10²–10⁶. Were that error underestimated by
20%, the argument would fail at the bootstrap, not at the seed cover.*

## 8. What the team should change, in priority order

1. **N = 112**: replace the 32-bit sentence with the window `[47,189]` (narrowed to `[47,128]` by the paper's own `int8` storage) and a cost table
   (`N112.md` §6 has the paragraph to paste).
2. **`k ≤ 10`**: restate as `k ≤ 5` (mid pass) or print the observed histogram. It cannot be
   satisfied simultaneously with the 50 M box cap.
3. **F2 clustering cutoff**: rewrite `(.042 − 1.11w)²` as `max(0, .042 − 1.11w)²`. The paper's
   own §6.3 sentence ("these constants affect only the choice of assignments") supports the
   harmless reading, but the formula as printed is non-monotone in the grid: `.0505, .0042,
   .0189, .0304` at `M = 12,24,48,96`, with no merge *possible* at all at `M = 12` or `24`.
4. **F4 sentinel**: `100` lies inside the certified range (`gu ≤ 100.1`), and the only thing that
   catches it is a `t < 10` guard at 1.59× — use a flag.
5. **`.103` and `.125`**: print which level each is sized for. `.125` is within 0.06% of the
   level-1 Taylor remainder; `.103` has no closed form.
6. **`q_d < 3.8`**: restate as `< 2`, or delete the sentence it contradicts.
7. **Evidence, four numbers the paper should print**: max retained bins per C record, max clusters
   per record, max local radius, max radius in `mid.bin`. Each is one line of the existing logs
   and each closes a "not reported" in §6.

## 9. Reproducing

```
cd work/05-parameters
for f in experiments/*.py; do python3 "$f"; done
```

Each script is self-contained (`math` only), prints every number quoted above, and writes its
table into `data/`. `experiments/n_band.py`, `seed_ball.py`, `grid_u2.py`, `stage_b_widths.py`,
`cluster_F2.py`, `caps_margins.py`, `consts.py` are this team member's; `n_window.py` and
`pairs_identify.py` are another member's and are *not* relied on — where they overlap, both
scripts print the same value (`C(116,5)`, `T1(112) = 85,349,292`), which is the intended
cross-check.
