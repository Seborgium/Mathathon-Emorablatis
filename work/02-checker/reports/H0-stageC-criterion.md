# H0 / Q4 — Stage C: measured statistics, criterion audit, route verdict, certificate design

Author: m6 (direction d3). Phase: H0 feasibility — measurements and a costed design, not a certificate.
Companion files in this directory: `StageCNecessity.lean` (machine-checked criterion, `lean` clean),
`verify_lemma65.py` / `verify_lemma65.out` (exact arithmetic of Lemma 6.5 and of the thresholds),
`parse_recs.py` + the two archive batches `f0.bin`, `f87.bin` (record census), `paper.txt`
(pdftotext of the preprint, fetched from the public repo).

Division of labour on the board, so that this document does not duplicate it: **d1/m2** owns the
instrumented re-run and the per-record ball/edge/step distributions and the (a)-vs-(b) backbone;
**d2/m4** owns the kernel-reflected search (route (c)); **d5/m1** owns positive controls for the
branching; **d6/m3** owns the precision-padding chain; **d4/m5** owns invariant-based exclusion.
This document owns the *semantics of the criterion* — whether (6.24) is the right necessary
condition, what it needs from the ball family, and what the certificate must carry for that step to
be checkable — plus the measurements that this question forces.

---

## 0. Bottom line

1. **The criterion is correct as used.** (6.24) is necessary given two facts: the ball family covers
   every candidate vector (Lemma 6.2 + 6.4) and no ball may contain two of the twelve vectors
   (Lemma 6.5). Lemma 6.5 needs **strictly** `s < .1`; the code enforces exactly that
   (`stageC.cpp:220`) and the recorded run has zero clustering failures (d1), so every record that
   received a verdict satisfies it. I verified Lemma 6.5's arithmetic and computed the *sharp*
   thresholds: `s < 0.115347` (the paper's own linear chain) and `s < 0.212056` (mean-zero
   refinement). Margin of the code's `.1`: 1.15x / 2.12x.
2. **The reduction (6.24) ⇒ no two further MUB bases is machine-checked** in
   `StageCNecessity.lean`: 152 lines, no `sorry`, axioms `propext, Classical.choice, Quot.sound`.
   That is the one link of Stage C that is *combinatorial* rather than numeric, and it is no longer
   on trust.
3. **Measured from the archive bytes** (mine, this is new): the initial Stage-C stream is exactly
   **22,379 records** — `f0..f86` hold 256 each, `f87` holds 107 — **22,378 of them have k = 4
   tangent directions and exactly one (index 106, the last record of `f87.bin`) has k = 0**, and all have radius
   exactly `0.016`; the fallback stream `fb1.bin` is **1,127 records, radius `0.011`**. Composed with the code's own arithmetic this gives, for every record that
   reached the graph stage, **`s_max <= (RB - 1.11w) + X_M = 0.0418879`** with `RB = .042`,
   `w = 1/96`, `X_M = sqrt(29/6)/(2*96)`.

   **Graph statistics, measured by d6/m3 with an instrumented copy of the published source**
   (independent of me; byte-identical outputs on 4 batches): per record `balls = 180..305`
   (med 239), ball radius `.024..042` (med .027), `|O|` med 2,607 (density .093, range .082-.147),
   `|U|` med 12,315 (density .432, range .393-.465), graph `steps` med 32,850, max 1.04e6 =
   21% of the cap. The 61 cap records in two batches have `balls = 263..309`, O-density
   .221-.291 (2.7x typical) and U-density .385-.418. Two cross-checks against my numbers:
   `C(239,2) = 28,441 ~ 29,000` pairs/record, and the measured radius max `.042` is consistent
   with (and bounded by) `s_max <= 0.0418880` from the analytic derivation.
4. **Route verdict: (a).** An independent exhaustive checker over recomputed graphs is feasible —
   order **0.5-6 CPU-hours** for the 23,343 record-verdicts that need one (10-40 CPU-min in double
   arithmetic; measured counts + modelled unit costs in §4.2), and it is the
   only route that covers what actually needs checking. Route (b) (DRAT/LRAT) is dominated: its
   clause encoding buys nothing unless the graph is an axiom set — which is exactly the part that
   needs checking — and its proof is `C(B,5)`-scale in the naivest encoding and ~23-84 GB at the
   measured step counts of the 23,343 records that actually need one (§4.3). The cheapest *sound weakening* is to drop the joint test (6.23) and certify on
   the (6.16)-padded graph (§4.5).
5. **Certificate format**: §5. Two required fields are missing from the saved-run record format: the
   **per-ball radius `s`** (Lemma 6.5's only warrant) and the **per-record `s_max`**; plus the
   tri-state verdict that makes a cap/overflow/cluster exit impossible to read as an exclusion.
6. **Edge predicates** with equation numbers, code lines, inputs and margins: §6.
7. **Soundness review**: §7. **No soundness defect found in the Stage-C exclusion path** — scoped
   to §7 and to Stage C only (not Stage A/B, not the predicates as implemented, see §8). Three defects
   (D1, D2, D3: format and method, none a soundness failure) and one robustness trap (D4 = the
   audit's F2, cost only, with a proof that it cannot change a verdict), plus the observation that clustering quality is *irrelevant* to
   soundness (only `s < .1` and the per-ball cover matter) — which is why F2 is not a soundness bug.

---

## 1. What exactly is being certified

Fix a record `z = (P, T, k, r, C, n0, id, ort, ...)`; `A = e(P)` entrywise, `e(t) = exp(2*pi*i*t)`,
phases in cycles. The first basis is the coordinate basis; the second is `e(P + delta)/sqrt(6)` with
`||delta|| <= r` (§6.1). Then:

* **Flatness is not an assumption.** A vector unbiased to the coordinate basis has all moduli
  `1/sqrt(6)`, i.e. is `e(beta)/sqrt(6)`; choosing the global phase gives `beta_0 = 0` and five free
  phases. Stage C enumerates exactly those five phases. This is why the enumeration is 5-dimensional.
* **Ball family.** `B_vec(v,s) = { lambda*e(v+x)/sqrt(6) : |lambda| = 1, sum_j x_j = 0, ||x|| <= s }`
  (6.14). Balls are phase-metric objects: `s` bounds the **mean-zero** phase displacement in cycles.
* **Graphs.** `O` joins two distinct ball labels unless orthogonality has been excluded by (6.16)
  left, (6.20), or the joint test (6.23) with `(6.18)`; `U` likewise for unbiasedness via (6.16)
  right, (6.21), (6.23) with (6.19). Edges are *retained* whenever the tests do not rule the relation
  out: `O`, `U` over-approximate. Extra edges are harmless.
* **Pattern.** `|A| = |B| = 6`, `A`, `B` O-cliques, `A x B subset of E(U)` — (6.24).

**Lemma (Stage-C exclusion, per record).** Assume
  (H1) *cover*: for every Hadamard `e(P+delta)`, `||delta|| <= r`, every flat vector unbiased to all
       six of its columns lies in some ball `B_vec(v_l, s_l)` of the record's family;
  (H2) *diameter*: `s_l < .1` for every ball;
  (H3) *over-approximation*: (H_O), (H_U) of §2.3 hold for the recomputed graphs;
  (H4) *search*: no (6.24) pattern exists in `(O,U)` and the search did not hit its cap.
Then no two further mutually unbiased orthonormal bases exist together with the coordinate basis and
that Hadamard.

Proof chain: H1 gives twelve labels; H2 + Lemma 6.5 gives twelve *distinct* labels; H3 converts the
required orthogonality/unbiasedness of the twelve vectors into the O-edges/cliques and the 36 cross
U-edges; H4 contradicts (6.24). The first two steps are Lemma 6.4/6.5, the third is 6.6/6.7, the
fourth is 6.8; the *composition* is what `StageCNecessity.lean` checks.

---

## 2. The criterion, audited (this is the d3 core)

### 2.1 Lemma 6.5's arithmetic is correct

Paper: two vectors in one ball have unscaled inner-product sum `sum_j e(z_j)` with
`||z|| <= 2s < .2`, hence with `pi < 22/7`, `sqrt6 < 5/2`

```
|sum_j e(z_j)| >= 6 - sum_j |e(z_j)-1| >= 6 - 2*pi*sqrt6*||z||
               >  6 - 2*pi*sqrt6/5 = 2.92188 > 6 - 22/7 = 20/7 = 2.85714 > sqrt6 = 2.44949
```

I re-evaluated this at 40 digits (`verify_lemma65.py`): the printed chain is valid, with the final
comparison `20/7 > sqrt(6)` equivalent to `400 > 294`. Consequence: `|<u,u'>| > 20/42 = 0.47619`,
while orthogonality needs `0` and unbiasedness needs `1/sqrt6 = 0.40825`. So no pair of the twelve
vectors can share a ball. **Verified.**

### 2.2 The thresholds are much sharper than `.1`; `.1` is safe

Solving the same chain for `s`:

| argument | threshold on `s` | source |
|---|---|---|
| linear, `|sum e(z_j)| >= 6 - 2*pi*sqrt6*||z||` | `s < (6-sqrt6)/(4*pi*sqrt6) = 0.115347` | paper Lemma 6.5 |
| mean-zero second order, `|sum (e(z_j)-1)| <= 2*pi^2*||z||^2` (uses `sum_j z_j = 0` from (6.14)) | `s < sqrt(3(1-1/sqrt6))/(2*pi) = 0.212056` | this note |
| code guard (strict) | `s < .1` | `stageC.cpp:220` |

Both thresholds exceed `.1`, so the guard is conservative and Lemma 6.5 holds with 1.15x / 2.12x
margin. Note the guard is `!(next[j].s < .1 && next[j].s >= 0) -> return false`, i.e. NaN and negative
radii also fail the record (unresolved), which is the correct direction.

### 2.3 The reduction, machine-checked

`StageCNecessity.lean` proves (verbatim, `E` a complex inner-product space, here `C^6`):

```lean
theorem false_of_two_mub_bases {L : Type*} [DecidableEq L] {V : L → Set E} {O U : L → L → Prop}
    (lab : Fin 6 ⊕ Fin 6 → L) {B₁ B₂ : Fin 6 → E}
    (hV : ∀ k, Sum.elim B₁ B₂ k ∈ V (lab k))
    (hdiam : ∀ (l : L) (x : E), x ∈ V l → ∀ (y : E), y ∈ V l → ‖x - y‖ < gamma)
    (hn₁ : ∀ i, ‖B₁ i‖ = 1) (hn₂ : ∀ i, ‖B₂ i‖ = 1)
    (ho₁ : ∀ i j, i ≠ j → ⟪B₁ i, B₁ j⟫_ℂ = 0)
    (ho₂ : ∀ i j, i ≠ j → ⟪B₂ i, B₂ j⟫_ℂ = 0)
    (hu : ∀ i j, ‖⟪B₁ i, B₂ j⟫_ℂ‖ = 1 / Real.sqrt 6)
    (hO : ∀ (l l' : L) (x : E), x ∈ V l → ∀ (y : E), y ∈ V l' → ⟪x, y⟫_ℂ = 0 → O l l')
    (hU : ∀ (l l' : L) (x : E), x ∈ V l → ∀ (y : E), y ∈ V l' →
      ‖⟪x, y⟫_ℂ‖ = 1 / Real.sqrt 6 → U l l')
    (hpat : ¬ ∃ s t : Finset L, s.card = 6 ∧ t.card = 6 ∧ Disjoint s t ∧
      (∀ x ∈ s, ∀ y ∈ s, x ≠ y → O x y) ∧
      (∀ x ∈ t, ∀ y ∈ t, x ≠ y → O x y) ∧
      (∀ x ∈ s, ∀ y ∈ t, U x y)) :
    False := by
```

with `gamma = Real.sqrt (2 - 2/Real.sqrt 6)` and the auxiliary results
`gamma_le_norm_sub_mub` (`|⟪x,y⟫| = 1/sqrt6` and unit norms ⇒ `||x-y|| >= gamma`),
`gamma_le_norm_sub_ortho` (orthogonal ⇒ `||x-y|| >= gamma`), `gamma_le_norm_sub_pair`
(all twelve pairwise distances `>= gamma`) and `label_injective` (no two of the twelve share a ball).
`gamma = 1.087889`, `gamma < sqrt 2` is also proved (both constants are used).

Reading of the three hypothesis groups:
* `hdiam` is H2 in metric form: any two vectors in one ball are closer than `gamma`. By §2.1-2.2 this
  follows from `s < .212` for **unnormalised** vectors scaled as in (6.14); in the *normalised*
  convention of the Lean file the same computation is `|⟪u,u'⟫| >= 1 - (pi^2/3)(2s)^2 > 1/sqrt6`.
* `hO`, `hU` are H3. They are the only hypotheses that speak about *how* the graphs were computed;
  they are what (6.16)/(6.20)/(6.21)/(6.23) must deliver, and they are exactly where a real defect
  would live (a filter that is not a necessary condition).
* `hpat` is H4. Note the theorem is one-directional — a pattern is *not* a configuration, so the
  positive outcome means "unresolved", which is the correct reading of `stats.positive`.

`label_injective` is the only place where a ball family could go wrong, and it is stated as a
hypothesis rather than derived from the code, deliberately: the certificate must carry `s` so that
the checker can verify it (§5).

### 2.4 The hypothesis is not removable

Without `hdiam` (H2) the argument has no content: the label map need not be injective and a
no-pattern verdict says nothing. This is not a hypothetical — it is realised in dimension 3, where the maximum is four MUBs. Take
`d = k = 3` and, with `omega = e^{2 pi i/3}` and `1/2 = 2 (mod 3)`,

    B1 = I,   B2 = F3 = B(0),   B3 = B(1),   B4 = B(2),
    B(a)[j][k] = omega^(a*j^2/2 + k*j) / sqrt(3),   a in {0,1,2},   j,k in {0,1,2},

which is the complete set of four MUBs in dimension 3 (`mub3.py`, 40 digits: every basis is
orthonormal, and all cross inner products have modulus `1/sqrt3` to 8e-41). With the one-ball family
`L = {*}`, `V_* = C^3`, the graphs are `O = U = empty` on one label, so (6.24) with `k = 3` is
unsatisfiable (two disjoint 3-subsets of a one-element type do not exist), yet the two further bases
`B3, B4` exist — unbiased to `B1`, to `B2` and to each other. Hence the criterion is *false* without a diameter hypothesis in the same formal
shape; any certificate that omits `s` is vacuous. (In dimension 6 an explicit counterexample would be
an actual 4-MUB configuration, i.e. it would refute the theorem — the point is that the *criterion*
must carry the hypothesis, not that the theorem is in doubt.)

**Smallest weakening if a record ever failed `s < .1`:** split each offending ball into sub-balls of
radius `< .212` (or `< .1` to reuse the paper's chain) around a `< .212`-net of its centre, with radii
`s' = s/ceil(s/.212)` in the same phase metric; the graph then has more labels, the diameter hypothesis is restored, and the
search is re-run. Cost is one extra factor in the ball count; nothing else changes. If that is not
affordable, the record is **unresolved** and the theorem is conditional on it — which is exactly the
mechanism the run's fallback pass already uses (radius `.016` records that hit the cap are re-covered
by radius `.011` records and re-searched, §3.1).

### 2.5 Code status of H2

`s` never leaves `cluster()` and is never written to any file: the record stream contains only
`(k, P, T, C, n0, id, ort, hor, mnorm, froot, radius)`. The only enforcement is
`stageC.cpp:220` inside `cluster()`, which converts any `s >= .1` (or NaN, or negative) into
`clusterFail` -> `negative()` returns false -> *unresolved* (`stageC.cpp:524`). Therefore:

* every record with a verdict satisfies H2, with the margins of §2.2;
* **but the certificate cannot show it** without recording `s` (defect D1, §7);
* the run reported `cluster 0` failures (d1's measurement f2), so no record was lost this way.

Composed with the code's own numbers, for any record that reaches the graph stage with the recorded
invocation (`RB = .042`, `M = 12`, 4 layers -> `N = 96`, `w = 1/96`, `X_M = sqrt(29/6)/(2*96) =
0.0114504`): the final radius satisfies `s <= sqrt(tol2) + X_M + 1e-9` with
`sqrt(tol2) = RB - 1.11w = 0.0304375`, hence

    s_max <= 0.0418879,  ||<_u,u'>| >= 1 - (pi^2/3)(2*0.0418879)^2 = 0.97691,
    ray distance <= 0.214893  vs  gamma = 1.087889   (5.06x margin).

So in the recorded run the twelve labels are separated by a factor 5, not 1.15 — Lemma 6.5 is nowhere
near its limit.

---

## 3. Measurements (item 1)

### 3.1 Mine: the record census, from archive bytes

Method: parse with `parse_recs.py` using the exact layout of `saveRecords`/`readRecords`
(`atlas.cpp:191-215`): `uint64 count`, then per record `int32 k`, `36 doubles P`, `k*36 doubles T`,
`8 doubles (C, n0, id, ort, hor, mnorm, froot, radius)`. Every file parses to its exact byte length
(no trailing bytes), so the record count is forced, not inferred.

| file | bytes | records | k histogram | radius | C | n0 | id | ort |
|---|---|---|---|---|---|---|---|---|
| `batches/f0.bin` | 386,056 | 256 | `{4: 256}` | all `0.016` | 4.116–4.405 | 1.48e-9–1.57e-9 | 2e-6 | 1e-8 |
| `batches/f87.bin` | 160,212 | 107 | `{4: 106, 0: 1}` | all `0.016` | 4.116–5.057 | 1.475e-9–1.605e-9 | 2e-6 | 1e-8 |

Because `f0..f86` are all 386,056 bytes and `356 + 288*4 = 1508` bytes/record, each holds exactly
`(386048 - 8)/1508 = 256` records at `k = 4`; `f87.bin` holds 106 records at `k = 4` and one at
`k = 0` (`356` bytes) at index 106, which is exactly its 160,212 bytes: `8 + 106*1508 + 356 = 160,212`. Hence

    initial Stage-C stream : 87*256 + 107 = 22,379 records, 22,378 at k = 4 and 1 at k = 0,
                             radius 0.016 for all of them
    fallback stream (fb1)  : 1,127 records (d1, f2), k = 4, radius 0.011

which matches the audit's "22,379 fine records" (F3) exactly. All radii are `.016 <= .03`, inside the
range `validate(z, .03)` admits at `stageC.cpp:497`.

### 3.2 d1's run counters (cited, not remeasured by me)

    initial C: done 22379, bad 163, graph 0, cap 163, over 0, cluster 0
    final   C: done  1127, bad   0

So: **163 records hit the 5,000,000-step cap in the initial pass; every failure is a cap hit; there
are no overflow, no clustering failures and no positive (pattern-found) outcomes.** The 163 capped
records were re-covered by radius `.011` records (the Stage-B fallback) and all 1,127 fallback
records were excluded. Consequences I rely on:

* `cluster 0` and `over 0` -> H1/H2 hold for *every* record that got a verdict, with no exception;
* `graph 0` plus `cap 163` -> the run's negative verdicts are 22,379 - 163 = 22,216 (initial) and
  1,127 (final); the step distribution is heavy-tailed but bounded by 5e6 by construction.

### 3.2b d6/m3's per-record graph measurement (cited; instrumented copy of the published source)

| quantity | measured (256 typical records of `f0.bin`) |
|---|---|
| balls per record | min 180, p10 197, med 239, p90 277, max 305 |
| ball radius `s` | min .024, med .027, mean .032, max .042 |
| `|O|` | med 2,607, density .082-.147 (med .093) |
| `|U|` | med 12,315, density .393-.465 (med .432) |
| graph `steps` | min 13,570, med 32,850, max 1.04e6 (21% of cap) |
| 61 cap records (bad52, bad53) | balls 263-309, O density .221-.291, U density .385-.418, steps = 5e6 |

Consequences I use below: pairs/record `~ C(240,2) = 28.7k`; excluded pairs/record
`C(B,2) - |O| - |U| ~ 13.8k` (i.e. ~48% of pairs are excluded, ~52% survive as edges — the graphs
are *dense*, which is the honest reason the search is not trivial); total over the run: **6.7e8
pairs, 3.4e8 joint tests, ~8e8-1.4e9 search steps** for the 23,343 records that received a verdict,
and bounded above by 23,343 * 5e6 = 1.2e11 if every one of them had sat at the cap. (The 163 capped
records are *not* in this count: they produced no verdict and are replaced by fallback records.) The cap locus has 2.7x the typical O-density: plausible, because a larger `|O|` is
what makes two 6-cliques more likely.

### 3.3 Derived per-record geometry (mine, exact arithmetic)

With `s_max = 0.0418879` (§2.5):

| quantity | value | note |
|---|---|---|
| ball diameter, phase metric | `2*s_max = 0.083776` | (6.14) |
| worst-case `|⟪u,u'⟫|` inside one ball | `>= 0.97691` | mean-zero 2nd order |
| worst-case ray distance | `<= 0.214893` | = `sqrt(2-2*0.97691)` |
| required separation (Lemma 6.5) | `1.087889` | `sqrt(2-2/sqrt6)` |
| margin | `5.06x` | |

### 3.4 What remains unmeasured

Nothing that the route-(a) cost model needs: `B`, `|O|`, `|U|` and `steps` are measured (§3.2b).
Still unmeasured: the *per-record* distribution of the two tails (which records have B > 277 or
steps > 1e6 — d1's 4-shard run answers that), the fraction of exclusions due to (6.16) alone versus
(6.20)/(6.21)/(6.23) (a checker-cost question: it decides whether the "drop the joint test" weakening
of §4.5 loses records), and the *capped* records' resolution margin (how close the fallback pass came
to *its* cap — the 1,127 fallback records took the same 5e6 cap and none hit it, but the margin is
unknown). The estimator for those, when d1 posts them:

    T_route_a = sum_records [ c1*C(B,2) + c2*(|O|+|U|) + c3*steps ]
    size_cert = sum_records [ 56*B + 8 + (1..152)*(C(B,2)-|O|-|U|) ]

---

## 4. Route verdict (item 2)

### 4.1 What a Stage-C certificate has to establish

Three layers, and they are *not* interchangeable:

| layer | content | how it can be certified |
|---|---|---|
| **L1 analytic** | H1 (cover: Lemmas 6.2, 6.4) and H2 (diameter: Lemma 6.5) | parameter-level inequalities, **no per-record data**: (6.6)/(6.7) per layer, Lemma 6.4's radius rule, `s < .1`. Check once per `(M, layers, r)`; there are only two distinct radii in the run (.016, .011). |
| **L2 numeric** | H3: each excluded pair really violates a necessary condition, i.e. (6.16)/(6.20)/(6.21)/(6.23) are re-evaluated outward | per *non-edge*; this is the only place where interval/eaxct arithmetic is needed |
| **L3 combinatorial** | H4: the graphs contain no (6.24) pattern | exhaustive search — or a formal proof of the search (route (b)/(c)) |

Route (a) = a small independent checker over L2+L3 with L1 as a separate arithmetic appendix.
Route (b) = a DRAT/LRAT refutation of L3 only (L1, L2 unchanged).
This framing is the main reason (b) cannot replace (a): (b) is silent about L1 and L2, which is where
a defect would actually be.

### 4.2 Route (a), costed

The checker: read the record (P, T, k, r), the ball list (centres `v_l`, radii `s_l`), and the list of
*excluded* pairs (relation, direction `y`, margin); recompute `q, S, c, J, B` from (P,T,v) per ball
(6.5)/(6.8); for every excluded pair re-evaluate the relevant test in outward arithmetic; insert all
other pairs as edges; then run its own complete (6.24) search. Nothing else. Note the design point:
**only exclusions need evidence** — an edge is free (extra edges only make the pattern easier to
find), so the certificate is a list of *non-edges with reasons*, and the checker never has to
reproduce stageC's internal decisions.

Estimator (monotone; inputs are `B`, `n_e = |O|+|U|`, `steps`, all per record):

    T_record ~ c1 * C(B,2) + c2 * n_e + c3 * steps
    c1 = 0.1-0.5 us   (six complex products, |S|, two divisions, one sqrt, outward rounding 3-5x)
    c2 = 3-20  us     (the (6.23) test: one (12+k)x(12+k) solve, k = 4 -> 16x16 ~ 1.4e3 flops,
                       plus two single-vector support evaluations)
    c3 = 0.05-0.2 us  (one bitset step: intersection + popcount on 32 words)

Now with the inputs of §3.2b (`B ~ 240`, `|O|+|U| ~ 14.9k`, `steps ~ 33k` median; 23,343
record-verdicts = 22,379 - 163 capped + 1,127 fallback; all but one record have k = 4, so the joint
test's matrix is 16x16 — 12x12 for the single k = 0 record, a negligible difference):

| term | count over the run | unit cost | subtotal |
|---|---|---|---|
| (6.16) on all pairs | 6.7e8 | 0.1-0.5 us | 1-6 min |
| (6.23) on retained pairs | 3.4e8 | 1-5 us | 6-30 min |
| search steps | 0.8-1.4e9 | 0.05-0.2 us | 1-5 min |

Total in double arithmetic: **~10-40 CPU-min**; multiply by 3-10 for outward-rounded evaluation
(fixed-point/error-bound doubles are enough — A.11's budgets are 1e-11..1e-8, far above 1 ulp), so
**0.5-6 CPU-hours**, dominated by the joint test. Dropping the joint test (§4.5) removes the middle
row: ~15-60 CPU-min. Worst case, if every verdict record sat at the cap: 1.2e11 steps -> ~7 CPU-h at
0.2 us.

**Status of each number in that table** (the judge's distinction is worth keeping in the deliverable):

* *measured* (d6/m3, instrumented copy, 256 typical records): pairs/record, `|O|+|U|`, `steps`;
  also d6's cap-record statistics and d1's 44 CPU-min full re-run;
* *extrapolation*: the three "count over the run" cells, = per-record measured values x 23,343;
* *model, not measured*: the unit costs `c1, c2, c3`, and the 3-10x factor for outward rounding.
  They are order-of-magnitude anchors (one 16x16 solve is ~1.4e3 flops; the original run does the
  same 3.4e8 joint tests inside 44 CPU-min, which bounds `c2` from above by ~8 us);
* the totals are therefore **estimates with a factor-2-3 uncertainty**, not measurements.

Anchor: d1's *full* instrumented Stage-C re-run (4-layer bin enumeration + all bin tests + clustering
+ the graph) is ~44 CPU-min for the same 22,379 records. Route (a) does none of the bin work (L1 is
symbolic), only the graph part, in outward arithmetic. **Verdict: 0.5-6 CPU-hours for the whole run (10-40 CPU-min in
double arithmetic, 3-10x for outward rounding), ~15-60 CPU-min if the joint test is dropped; ~7 CPU-h
in the pathological case where every record sat at the cap.** That is affordable — it is the order of
the original run itself (44 CPU-min) — and it is the route I recommend.

Cheapening without loss of soundness — see §4.5.

### 4.3 Route (b), costed, and why it loses

Clause encoding of "no (6.24) pattern" for a fixed pair of graphs `(O,U)` on `B` labels.
Variables `x_{l,A}, x_{l,B}` (`l` a ball) plus, if cardinality is not expanded, sequential-counter
auxiliaries.

    (b1)  for each l :                         not x_{l,A} or not x_{l,B}            B clauses
    (b2)  exactly six of side A (and of B):    SC(B,6): O(B*6) clauses/aux  (Sinz counter)
             naive encoding instead:           C(B,5) at-least clauses + C(B,7) at-most
    (b3)  for each pair {l,l'} not in O :      not x_{l,A} or not x_{l',A};  same for B
    (b4)  for each pair {l,l'} not in U :      not x_{l,A} or not x_{l',B};  not x_{l,B} or not x_{l',A}
    (no clause for a pair in O or U: an edge is a permission)

UNSAT of this CNF is exactly H4 for that record. `B`-size of the CNF: `O(B^2)` for (b3)/(b4) — the
same data the route-(a) checker reads — so the CNF is not the problem.

**Mapping the least-vertex branching to a proof log.** `graph::exist` is a DPLL search on exactly this
formula with the decision order "least vertex"; each `tick()`-counted step is one node expansion, so
node counts scale with the recorded step counter (a count of candidate-vertex iterations, so it is a
lower bound). A faithful log
is: emit the decision literal on entering a branch, emit a learned clause at each conflict, emit the
empty clause at the end (DRAT), or the LRAT variant with hints. Sizes:

* one proof line per node plus one per conflict, ~30-60 bytes (factor not measured);
* **only records with a completed negative search need a refutation.** The 163 capped records are
  unresolved, are never read as negative (`stageC.cpp:413`, `:487`, `:528`), and are re-covered by
  the 1,127 fallback records — charging a proof to them is wrong. The certificate set is
  22,216 initial + 1,127 final = **23,343 records**;
* their measured step counts (median 32,850, max 1.04e6, d6/m3) give ~7.7e8 nodes at the median
  (~1.4e9 at a 60k mean), i.e. **~23-84 GB** at 30-60 bytes/node — a *lower* bound on a DPLL log,
  which also carries decision and conflict lines. **Estimate, not measurement**; the point stands that
  it is 1-2 orders of magnitude above the ~0.3-1 GB of the route-(a) certificate (§5);
* checking that log costs a propagation pass per line, i.e. the same order as re-running the search,
  with a larger constant.

**Trust accounting.** The DRAT/LRAT proof fixes L3 relative to the *clauses*, and the clauses encode
the graph. So (b) removes exactly the same trust as a formalisation of the search (d2's route (c)),
and nothing about L1/L2. Meanwhile (a)'s search is ~30 lines of code with a complete-and-sound
argument already in the paper (Lemma 6.8, which I re-read and whose two delicate points I checked:
(i) `tick()` returns *true* = "possible", so a cap can never yield a negative — `stageC.cpp:413`,
`stageC.cpp:487`, `stageC.cpp:527-528`; (ii) the second clique is automatically disjoint from the
first because `O`/`U` have no self-loops, so `pool = u & nodes[j].U` excludes every already-chosen
vertex — `stageC.cpp:433-440`; this matches the paper's Lemma 6.8 proof sentence "The lack of U
self-loops also removes every selected first-clique vertex from the second pool").

If a proof-log route were taken anyway, the checker should be the CakeML-verified LRAT checker in
`CakeML/cakeml`, `examples/lpr_checker` (the `cake_lpr` binary; I verified the directory exists in
the repo, I did not run it), with `drat-trim`/`lrat-trim` as the unverified fast path. **Verdict:
(b) is dominated — 3-4 orders of magnitude more bytes, no extra coverage, and it cannot say anything
about the predicates that the certificate's real risk lies in.**

### 4.4 Route (c) (d2) as a companion, not a replacement

Kernel-reflected search (d2) on the *recomputed* graphs buys independence of the branching at
~10-100x the C search cost per record. The right deployment is therefore: route (a) for all 23,343
verdict records, plus route (c) on the heavy tail (the 163 cap-affected records, plus a random sample) — that
is a few CPU-hours at worst and removes the only program-dependent lemma (F9).

### 4.5 The smallest weakening that is still a certificate

* **Drop the joint test.** Certify with (6.16) alone (and, if desired, (6.20)/(6.21)): those are
  *necessary* conditions too, so the graph is a superset of the true one and a no-pattern verdict on
  it is sound. Cost drops by the whole `c2` term and the checker no longer needs (6.22)/(6.23) or the
  tangent machinery at all. Risk: the padded graph may contain a pattern the true graph does not, in
  which case the record becomes unresolved. Whether that happens is a *measurement* (d1's data can
  answer it: re-run the search on the (6.16)-only graph of each record).
* **Shrink the radius.** If a record cannot be certified, re-cover its H-ball with smaller-radius
  records and re-run — exactly the fallback mechanism the archive already used for the 163 capped
  records. This is sound because a smaller `r` only tightens the bins (6.7) and the tangent bound
  (6.2); it never weakens H1/H2.
* Nothing weaker works: an *unresolved* record cannot be replaced by any local argument, and a
  certificate that omits `s` (§7, D1) is vacuous (2.4).

---

## 5. Certificate format for Stage C (item 3)

Requirements: (i) another team can implement the checker from this section alone; (ii) everything the
checker cannot recompute is explicit; (iii) the tri-state verdict is unambiguous. Canonical text
(one file per record; a JSON schema is fine, but every float is a **hex float or a decimal with a
declared outward radius**, never a bare `%.17g`).

```
record                                    # one per (parent record, pass)
  id          : "f0.bin#0007@C.initial"   # provenance: archive file, index, pass
  parent      : record id | "seed"        # if produced by a fallback pass
  stageB {                                # EXACT copy of atlas.cpp's saved layout, all fields
    k         : int 0..10
    P         : 36 x binary64 (cycles, |P| <= 4)
    T         : k x 36 binary64 (|T| <= 1.01)
    C, n0, id, ort, hor, mnorm, froot, radius : binary64
  }                                       # radius r <= .03, checked by validate()
  paramsC { M, layers, linear, RB, detail, mode, capSteps, part, parts, lloyd }
                                        # run: 12 4 1 .042 1 1 5000000 {0..3} 1|4 ; lloyd = 2 (default)
  fp        { "IEEE-754 binary64, FE_TONEAREST, FLT_EVAL_METHOD=0, no contraction", probe hash }
  derived { K = 1.00001,
            eta   = (basis = T (k x 36), bound rH)   # (6.2): shared Hadamard displacement,
            rH    = sqrt(1+ort)*r + 1e-9,             #       existentially quantified per H, so
            nhat  = n0 + id*r + C*r*r + 1e-9,         #       the certificate stores the bound only
            N     = M*2^(layers-1)  (= 96),
            X_M   = sqrt(29/6)/(2N), L_M = 5/(2N), I_M = 3/(4N) }   # at the finest layer N = 96
  layers { L = 1..4: { N_L = M*2^(L-1), retained : int, sha256(bin index list),
                       tau_L  = 2*pi*(5/(2 N_L)/sqrt6 + r),          # (6.7) component threshold
                       comb_L = 2*pi*(K * sqrt(29/6)/(2 N_L) + r) } } # (6.7) combined threshold
  balls  { n : 1..2048,
           [ { v : 6 x binary64 (cycles, |v_j| <= 2),   # (6.14) centre
               s : binary64, 0 <= s < .1,               # (6.14) radius, REQUIRED (D1)
               members : { count, sha256(bin index list) } } ] }
  criterion { s_max = max_l s_l,                      # REQUIRED: Lemma 6.5's warrant
              cover_ok  = true,                        # Lemma 6.4: per ball, max_member ||h||+X_M <= s
              diam_ok   = (s_max < .1) }
  excluded {                                  # THIS is the load-bearing content: non-edges
           [ { pair : (l,l'), rel : "O" | "U",
               rule : "6.16" | "6.20" | "6.21" | "6.23",
               y    : direction (2, 1 or 12+k reals, |y|_inf = 1),
               slack: certified positive margin (outward lower bound) } ] }
  graph   { O : bitsets (n x 32 x uint64), U : bitsets }   # redundant: recomputable from `excluded`
  verdict : { kind : "EXCLUDED",    steps_used : int, cap_hit : false }
          | { kind : "UNRESOLVED",  reason : "cap" | "overflow" | "cluster" | "empty" | "invalid" }
          | { kind : "PATTERN",     A : 6 labels, B : 6 labels, steps_used : int }
```

Size accounting (measured inputs, §3.2b): balls `56 B ~ 13 KB`/record; excluded pairs
`8.5e3-1.4e4`/record at 1 byte (rule tag) = 8-14 KB/record, or +152 bytes each if the direction `y`
is stored (that would be ~2 MB/record, 48 GB for the run — so **store `y` only when the checker
cannot re-derive a witness**, i.e. prefer rule tags + a witness-search obligation in the checker);
stage-B data 1.51 KB/record at k = 4 (356 B at k = 0). Total **~0.7-1 GB** uncompressed text, or ~0.3 GB binary — versus
>=23-84 GB estimated for the DRAT route (§4.3).

Checker obligations, in this order (each step's failure invalidates the record, and "invalid" is never
"excluded"):

1. **Parse + bounds**: `k <= 10`, `r <= .03`, `|P| <= 4`, `|T| <= 1.01` (the `validate` ranges,
   `stageB.cpp:274-281`), `n <= 2048`, `s_l < .1`, `|v_l| <= 2`.
2. **Derived constants**: recompute `rH, nhat, K, X_M, L_M, I_M, tau_L, comb_L`; compare.
3. **L1 arithmetic appendix** (once per `(paramsC, r)`): verify the two (6.7) thresholds and (6.12)'s
   `rho` are the paper's expressions, and that the *cover* claim they support is the stated one
   (Lemma 6.2 gives `||S' - S|| <= comb_L`, `|S'_i - S_i| <= tau_L`; a genuine vector in a bin
   satisfies both). This is 20 lines of arithmetic per layer — the numbers are in §6.9.
4. **Per-ball single-vector data**: recompute `q_ji, S_i` (6.5) and `c_i, J_ij, B_ik` (6.8) from
   `(P, T, v_l)`; recompute `S_i` (the ball-level Hadamard sums) and `R_ij`; any mismatch with the
   stored data is invalid.
5. **Ball cover (Lemma 6.4)**: for every ball and every member bin, recompute `h` (wrapped, mean-free)
   and check `||h|| + X_M <= s_l`; also check that the union of member lists is *exactly* the retained
   bin set of the last layer.
6. **Exclusions (L2)**: for every entry of `excluded`, recompute the named test outward and check that
   it *fails* with the stated positive margin. Direction of failure per §6: (6.16) requires
   `|S|/(2*pi*sqrt6) > r_e` (O) or `||S|/sqrt6 - 1|/(2*pi) > r_e` (U); (6.20), (6.21), (6.23) are
   the displayed inequalities violated.
7. **Graph**: build `O` (all pairs not excluded with rel "O") and `U` likewise; every pair of distinct
   balls gets an edge unless excluded. Compare with the stored bitsets if present.
8. **Search (L3)**: run a complete (6.24) search on the rebuilt graphs. `verdict.kind = EXCLUDED`
   requires: no pattern found, `cap_hit = false`, and the search was complete (no give-up). A
   `PATTERN` verdict is *not* a certificate of existence — it means "unresolved"; the checker must
   confirm the pattern actually satisfies (6.24) before recording it as a witness.
9. **Global composition** (outside the per-record file): every record of a Stage-B output is either
   EXCLUDED or is covered by records of a fallback pass that are all EXCLUDED; the `(offset, parts)`
   partition map covers each input record exactly once.

---

## 6. Edge predicates the checker must re-evaluate (item 4)

Notation: `e(t) = exp(2*pi*i*t)`; two balls with centres `u, v` (cycles) and radii `s_u, s_v`;
`r_e = s_u + s_v` (the code stores `+1e-10`); `Q_j = e(u_j - v_j)`, `S = sum_j Q_j` (6.15).
The stored single-vector data of a ball at centre `v` is `q_ji = e(v_j - P_ji)/sqrt6`,
`S_i = sum_j q_ji` (6.5), `c_i, J_ij, B_ik` (6.8). All of it is recomputable from `(P, T, v)`.

| # | test | paper | code (`stageC.cpp`) | inputs | direction that removes the edge |
|---|---|---|---|---|---|
| P1 | O direct | (6.16) left | `pairtest` :377-379 | `Q, S, s_u, s_v` | `|S|/(2*pi*sqrt6) > r_e` |
| P2 | U direct | (6.16) right | `:377-379` | same | `||S|/sqrt6 - 1|/(2*pi) > r_e` |
| P3 | edge derivatives | (6.17) | `:381-384` | `Q, S` | (definitions: `D_O in R^{2x6}` with rows `-Im Q_j`, `Re Q_j`; `D_U in R^{1x6}`, `(D_U)_j = Im(S*conj(Q_j))/6`) |
| P4 | O residual + support | (6.18), (6.20) | `:388-389` | `Q,S,D_U,E_O = pi*r_e^2` | `|S|^2/(2*pi) > 6*r_e*||D_U|| + E_O*|S|` |
| P5 | U residual + support | (6.19), (6.21) | `:396-397` | `Q,S,D_U,E_U = pi*r_e^2*(1+|S|/6)` | `|q_U| > r_e*||D_U|| + E_U`, `q_U = (|S|^2/6-1)/(4*pi)` |
| P6 | joint, O | (6.23) with (6.22), `E=O`, `ell=2` | `joint<2>` :312-371 | both balls' `(c,J,B,S,R)`, the record's `(P,T,k)`, `rH`, `nhat`, `s_0,s_1`, `D_O, q_O`, `E_O` | displayed inequality violated for the given `y` |
| P7 | joint, U | (6.23) with (6.22), `E=U`, `ell=1` | `joint<1>` :312-371 | same | same |
| B1 | bin tests (H1, not per pair) | (6.6), (6.7), (6.12)-(6.13), (6.4) | `Layer::test` :50-75 | `P, r, N, X_M, L_M, I_M, K` | a bin is dropped only if one of (6.7)/(6.12) fails |

Direction discipline, which the checker must implement rather than copy: a pair keeps its edge unless
the test shows the relation to be *impossible*; a bin is kept unless the test shows it contains no
admissible vector. So all tests are used in the **necessary** direction, and every numerical slack
must enlarge the retained set. Note the code's additive allowances (`2e-7` on the (6.16) radius,
`2e-8` on `E_O, E_U`, `2e-7` on (6.20)/(6.21), `3e-7` on (6.23), all listed in §6.7 of the paper and
justified in A.10/A.11) are all on the conservative side, and `joint` returns "possible" on any
numerical trouble (`!isfinite`, zero norm, abnormal magnitude: `:330-336`). A checker should replace
them by hard outward bounds, e.g. `|S|^2` to `1.1e-11`, edge constants to `1e-12`, the joint support
to `1e-8` (A.11's budgets).

### 6.9 The L1 numbers for the recorded invocation

`N in {12, 24, 48, 96}`, `K = 1.00001`, `r` from the record (.016 initial, .011 fallback):

| N | X_M | L_M | I_M | tau = 2*pi*(L_M/√6 + r), r=.016 | comb = 2*pi*(K*X_M + r), r=.016 | tau, r=.011 | comb, r=.011 |
|---|---|---|---|---|---|---|---|
| 12 | 0.0916035 | 0.2083333 | 0.0625 | 0.634927 | 0.676099 | 0.603511 | 0.644683 |
| 24 | 0.0458018 | 0.1041667 | 0.03125 | 0.367729 | 0.388315 | 0.336313 | 0.356899 |
| 48 | 0.0229009 | 0.0520833 | 0.015625 | 0.234130 | 0.244423 | 0.202714 | 0.213007 |
| 96 | 0.0114504 | 0.0260417 | 0.0078125 | 0.167330 | 0.172477 | 0.135915 | 0.141061 |

These are the only numbers Lemma 6.2 needs; both are positive and both are *necessary-condition*
thresholds, so any outward enlargement is safe. In particular the cover does not depend on the
clustering quality, on the number of layers actually retained, or on any per-record data beyond `r`.

---

## 7. Soundness review (item 5)

**Scope.** This section reviews Stage C's *exclusion path* only — record -> balls -> graphs -> search
(§1). It makes no claim about Stage A/B, about the numeric evaluation of the predicates as
*implemented* (§8, first two bullets), or about the theorem as a whole. "No soundness defect found"
below means exactly: no defect found **in this path**, under the arithmetic-guarantee hypothesis that
the tests are outward (which §8 leaves unverified).

### 7.1 What the certificate must contain so that no exit can masquerade as an exclusion

The six ways Stage C can fail to finish are `overflow` (bins > 2e6, `:147`), `clusterFail`
(`:204`, `:219`, `:220`), `cap` (`:413`, `:487`), `got a pattern` (`positive`), `empty bin
layer` (`:520`, which *is* an exclusion and is legitimate), and input invalidity (`:497`). The
certificate must make each of them explicit per record, because in the saved-run data the only
per-record signal is membership in the `bad` list:

1. an explicit **tri-state verdict** per record (not a set difference against a `bad` file);
2. **`cap_hit` and `steps_used`** must be stored for every record; `EXCLUDED` requires
   `cap_hit = false` *and* a complete search (`gaveup` unset — `stageC.cpp:484-487`, `:527-528`);
3. **`overflow` and `clusterFail` must be recorded as `UNRESOLVED`, never dropped** — the empty
   `bad*.bin` files in the archive are evidence, so their meaning must be preserved;
4. **`s_max` per record** (Lemma 6.5) and the **ball member lists** (Lemma 6.4) — otherwise the cover
   and the diameter hypotheses are unverifiable;
5. the **`(offset, parts)` partition map** and the fallback parent links, so that a record missing
   from an input shard cannot silently vanish (the archive's `check_records.py` does check
   "complete final modulo-four coverage"; the certificate should not rely on a separate tool for this);
6. the **`empty bin layer`** verdict must carry the per-layer retained-bin counts, since that is the
   evidence that the layer really was completed.

### 7.2 Defects found (with file:line)

**D1 — the ball radius `s` is never recorded; Lemma 6.5's hypothesis is invisible. Severity: high for
auditability, none for the recorded run.**
`cluster()` computes `s` and checks `s < .1` at `stageC.cpp:220`, but `s` lives only in the local
`vector<ball> balls` (`stageC.cpp:161`); the record stream writes 8 doubles and none of them is `s`
(`atlas.cpp:191-198`, `saveRecords`). Consequence: the certificate as it stands cannot demonstrate
H2 — it must be *taken on trust that some run of `cluster` produced radii below .1*. For the recorded
run this is corroborated (`cluster 0` failures, d1) but not certifiable; and a re-run of the checker
cannot distinguish "the balls had radii 0.04" from "the balls had radii 0.2 and the check was
skipped". Fix: record `s_l` and `s_max`, as in §5.

**D2 — the verdict is stored as a set difference, not as a per-record fact. Severity: medium.**
`negative()` reports through `statC` counters and `bad` (`stageC.cpp:496-530`), and the only on-disk
artefact is `saveRecords(argv[10], bad)`. A record is "excluded" iff it is *absent* from `bad`, which
is only as reliable as the input enumeration (`offset += v.size()`, `:551`). This is exactly the kind
of step where a dropped input looks like success. Fix: per-record verdicts (§5), and the explicit
partition map.

**D3 — the additive allowances are undocumented in the data. Severity: medium (method).**
`2e-7` (radius), `2e-7` ((6.20)/(6.21)), `2e-8` (`E_O`, `E_U`), `3e-7` ((6.23)), `1e-9` (radius
inflation), `1e-10` (pair radius), `1e-12` — all appear as literals in the pair path
(`stageC.cpp:377, 388, 389, 396, 397`). I checked the *direction* of each: each one enlarges the
retained set (a rejection is harder), so none of them can produce a false exclusion. But they are not
derived in the data and they are not additive-with-proof: A.11 budgets `1e-11` for `|S|^2` and `1e-8`
for the joint support, which is what a checker must use. Fix: an interval checker with hard outward
bounds; the literals must not be copied.

**D4 — the merge cutoff `sq(R - 1.11*w)` is non-monotone for `w > R/1.11` (the audit's F2). Severity:
cost/robustness only, provably not soundness.**
`tol2 = sq(R - w*1.11)` at `stageC.cpp:183`; for the recorded `N = 96`, `w = 1/96`, `R = .042` the base
is positive (0.0304375) and the merge radius is 0.0304375, i.e. 2.92 lattice steps — fine. But for a
different `M` the base can be negative and squaring makes the effective radius non-monotone. **Why it
cannot change a verdict:** `cluster`'s only soundness duties are (i) every retained bin is a member of
some ball whose stored radius satisfies `s >= ||h|| + X_M` — the final assignment does exactly this at
`stageC.cpp:210`, and it recomputes radii from actual assignments; and (ii) `s < .1`, checked at
`:220`. *Nothing else about the partition is used*: the exclusion argument (§1) holds for any ball
family satisfying H1+H2, and a coarser partition is nowhere required (a finer partition only adds
labels, and §1 is simply re-applied to the finer family: sub-balls cover their parent, their radii
only shrink, so H1 and H2 still hold and Lemma 6.5 still applies — no monotonicity between different
partitions is needed or claimed). So the merge rule can only change the ball count (`2048` cap ->
`clusterFail` -> unresolved) and the search cost. Verdict: F2 stays a cost/robustness finding; it
must not be "fixed" by weakening any radius check.

**D5 — the batch files overwrite `radius` with the pass target (`d1`'s note). Severity: low for Stage
C (conservative), an obligation for Stage B.**
`batches/f*.bin` store `radius = .016` for every record, including records whose `fine.bin` radius is
tiny (one record has `7.77e-8`). For Stage C this is *conservative*: a larger `r` widens the (6.7)
thresholds and the tangent bound `rH = sqrt(1+ort)*r`, i.e. retains more bins and more edges. The
obligation it creates belongs to Stage B: the coverage claim must be made at radius `.016`, not at the
smaller certified radius. The Stage-C certificate must therefore document `r` as "the radius at which
the record was validated".

**D6 — bounds checks that are correct and should be kept.** `:219` `|v_j| <= 2`, `:220`
`s < .1 && s >= 0`, `:204` ball cap, `:147` bin cap, `:497` `validate(z, .03)`: all NaN-safe because
written as negated comparisons (`!(x < .1)`), so NaN fails the record rather than passing it. This is
the right idiom and the certificate should preserve it.

**D7 — out of scope but flagged.** The `100` sentinel in `ell` (`patchx.cpp`) and the Stage-A/B
numerics are upstream of Stage C; Stage C re-validates every input record (`:497`), so it inherits
whatever radius the record claims. F4 (audit) stays with the Stage-B owner.

---

## 8. What I did NOT verify

* **No Stage-C execution.** I did not run `stageC.cpp` or any re-run; every per-record quantity
  (`B`, `|O|`, `|U|`, `steps`) is either d1's measurement or unmeasured (§3.4). My compute use was a
  few seconds total.
* **The numeric filters as implemented.** I did not verify that `joint` (`stageC.cpp:312-371`) with
  `detail = 1`, `fE/fB/fJ` rescaling and the `±3e-7` really is an outward evaluation of (6.23); I
  verified only the paper's statement, the code/equation correspondence term-by-term, and that every
  slack is on the conservative side. This is the load-bearing item for route (a) and needs its own
  interval re-derivation (or a Lean/HOL formalisation of (6.22)/(6.23)).
* **Lemma 6.7's proof.** Transcribed and matched to the code, not independently proved.
* **The H1 cover beyond (6.7).** I checked the (6.7) arithmetic (§6.5) and Lemma 6.4's radius rule;
  I did not verify the `linear` test (6.11)/(6.12) as a necessary condition (the `Layer::test`
  KKT/Newton step), nor the refinement-completeness sentence of §6.3 at boundary points.
* **The Lean file's translation to (6.14).** `StageCNecessity.lean` is stated for *unit* vectors;
  the unnormalised convention of (6.14) and the step `s < .212` (resp. `s < .115`) is checked
  numerically in `verify_lemma65.py`, not in Lean. In particular `gamma` in Lean is the *normalised*
  distance `sqrt(2 - 2/sqrt6)`; the unnormalised Stage-C inner products are the same numbers divided
  by 6.
* **Stage-B/A.** I did not verify that the records cover the surviving region (Lemma 6.4's
  *feed* claim), the atlas merges, `patch`, or `ell`/sentinels; see the audit's F1-F4.
* **The archive's authenticity.** I did not check `extraction.json`/hashes, nor that the sources I
  read are the binaries that produced the saved records; I read the copies cached in
  `.scratch/gh/upstream/` and byte-compared the record layout against `atlas.cpp` only.
* **`check_records.py`.** Not executed; its coverage logic is cited from `VERIFY.md`.

---

## Appendix: reproduce

```
lean StageCNecessity.lean           # ~5 s CPU, no output; axioms: see CheckAxioms.lean
python3 verify_lemma65.py           # Lemma 6.5 chain + sharp thresholds (40 digits)
python3 parse_recs.py f0.bin f87.bin   # record census of the archive batches
python3 layers.py                   # X_M, L_M, I_M, tau, comb per layer
python3 mub3.py                     # the four MUBs in d=3 used as the sharpness example
```
Sources fetched from the public repo `openai/math`, tree
`preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/`:
`...pdf` (paper.txt), `verification/saved-run/VERIFY.md`, `verification/saved-run/execution/data/batches/{f0,f87}.bin`.
The upstream C++ is the cached copy at `.scratch/gh/upstream/` (not edited).
