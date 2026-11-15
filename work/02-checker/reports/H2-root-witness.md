# H2-ROOT — the Root certificate, made checkable

Swarm member `m4`, direction **d4 (ROOT)**, swarm `smwgx2sv0`. Revision 2 (after review).
Subject: preprint *The maximum number of MUBs in dimension six* (24 Sep 2026), Section 4.1-4.2 and
A.5, and `patchx.cpp` (`Root`, `buildH::patch`).

**What this file is.** The complete list of check conditions for a Root certificate, with exact
index/matrix conventions, the direction of every inequality, a decision on which conditions are
decidable from the saved bytes and which need a missing witness, a runnable three-valued checker,
and measured slacks and costs on real saved records.

**What it is not.** No claim that the atlas, Stage A, Stage B or Stage C is certified; no claim that
N(6)=3 follows; no claim that any saved record is unsound; no erratum in the preprint. The saved
`.bin` records are not proof objects, and nothing below upgrades them into one.

Files: `records.py` (exact record parser), `kernel.py` (rational + outward-interval kernel),
`rootcheck.py` (the obligation checker), `derive.py` (canonical reconstruction of the source's
auxiliary map), `census.py` (slack census), `mutants.py` (corruption suite), `cost.py` (timing),
`tensor_branch.py` (which `C` branch a record's stored constants are consistent with),
`RootConsumer.lean` (the consumer step, machine-checked). Run the Python with
`OPENBLAS_NUM_THREADS=1` (BLAS threading otherwise makes a 30x30 `eigh` take ~30 ms on this VM).

---

## 0. Verdict semantics (load-bearing — read before the tables)

The checker is three-valued and the distinction is not cosmetic:

* **PASS** — the obligation is established for the stored record, given the transported witness when
  the obligation needs one.
* **FAIL** — reserved for a *refutation of stored bytes*. R1-R4 are statements about the record
  alone, so an exact/interval evaluation that strictly violates one refutes the record. For R5-R7
  the obligation quantifies over an auxiliary matrix `M` (and, for R7's tensor branch, over a
  congruence `U`); a checker that supplies its own `M`/`U` can only *fail to find* a witness. That is
  **UNDECIDED about the record**, never a refutation. If the witness is transported *inside* the
  certificate file (`witness_emitted=True`), a failure rejects that file — the pair is refuted.
* **UNDECIDED** — no witness, a derived witness that does not certify, or an enclosure that
  straddles the decision point. UNDECIDED is never a refutation and never a pass.

An upper enclosure of a norm that exceeds a bound does not refute the bound; only a *lower* bound
strictly above it would. `rootcheck.py` implements this split; `mutants.py` demonstrates it.

---

## 1. The certificate, stated as a checking problem

Fix the notation of Section 4. Real 6x6 matrices are identified with `R^36` in **row-major** order;
`Pi` is the orthogonal projection onto the horizontal space (rank 25); all matrix norms are
Frobenius; `F(P) in C^15` is (4.1) with the 15 edges ordered by increasing `i`, then increasing `j`
(`0 <= j < i <= 5`), each complex coordinate stored real part first.

> **Definition 4.1 (Root certificate).** A Root is `(P in R^36, T in R^{36 x k}, C, n0, id, ort,
> hor, mnorm, froot >= 0)`, `0 <= k <= 10`. It is certified if (4.4) holds and, for every horizontal
> `delta` with `F(P+delta) = 0`, with `eta = T^* delta`, `s = ||delta||`, (4.5), (4.6) and, for every
> horizontal `v` with `h' = delta - v`, (4.7) hold.

Proposition 4.5 reduces this *universally quantified, radius-free* statement to finitely many
inequalities by introducing one auxiliary matrix `M in R^{36 x 30}`:

**(4.4)** `||T^*T - I|| <= ort`, `||(I-Pi)T|| <= hor`, `||F(P)|| <= froot`;
**(4.15)** `||M|| <= mnorm`, `mnorm*froot <= n0`, `||Pi - T T^* - M L_P Pi|| <= id`;
plus **`C >= pi * b(M)`** where `b` is a constant of Lemma 4.3/4.4 for that same `M`.

That is the whole analytic content. Everything else in Section 4 (the ball radius (4.38), the
two-centre relation (5.2)-(5.12), Stage B's `nu0`, `lam`) is a *consumer* of these constants and
never looks at `P` or `T` again except through `(o_P, alpha_P, gamma_P, mu_P, eps_P, n0) =
(ort, id, C, mnorm, froot, n0)`.

### 1.1 The checker obligations (this is the witness schema)

| id | obligation | paper | arithmetic |
|----|------------|-------|------------|
| G1 | `k in [0,10]`; `|p_j| <= 4`; `|T[a][h]| <= 2`; 8 constants finite and `>= 0` | A.5 gates | exact |
| G2 | `id<1e-4`, `ort<1e-5`, `hor<1e-5`, `C<20`, `mnorm<2`, `n0<1e-6`, `froot<1e-6` | A.5, §7 range checks | exact |
| R1 | `(sum_{a,i} (T_a.T_i - delta_ai)^2)^{1/2} <= ort` (Gram of the k stored rows) | (4.4) | exact rational |
| R2 | `||(I-Pi)T||_F <= hor` | (4.4) | exact rational |
| R3 | `||F(P)|| <= froot` (30 real coordinates) | (4.4) | interval `e(x)` |
| R4 | `mnorm*froot <= n0` | (4.15) | exact rational |
| R5 | `||M||_2 <= mnorm` | (4.15) | exact rational **given the factors** |
| R6 | `||Pi - T T^* - M L_P Pi||_F <= id` | (4.15) | interval `e(x)` |
| R7 | `C >= pi * min(sqrt(8)*mnorm, sqrt(6*lambda_max(A)))`, `A` the 30x30 signed Gram (4.14) of the columns of `M` | Lem. 4.4 | exact rational + interval `pi` |

`R1-R4` need no witness: they are decidable from the stored bytes and a sound `e(x)` enclosure.
`R5-R7` need `M` (and for R7's tensor branch a congruence `U`), which the record does not contain.

`R6` is checked in the Frobenius form the source actually computes; Frobenius `>=` operator norm, so
a Frobenius *pass* implies (4.15). A Frobenius upper bound *above* `id` is UNDECIDED (§0).

### 1.2 Note on the printed constants — no erratum claimed

The checkable form used throughout is

```
C >= pi * sqrt(8) * mnorm          (Lemma 4.4, first constant)
C >= pi * sqrt(6 * ||S||^2)        (Lemma 4.4, second constant; ||S||^2 = lambda_max(SS*) )
```

which is exactly what `patchx.cpp:143` (`pi*sqrt(8.)*R.mnorm`) and `patchx.cpp:164`
(`pi*sqrt(6*(row+.0002)/(1-beta))`) compute, and what Lemma 4.4's proof gives. I make **no claim
about how the printed page renders these constants**: the text extraction I worked from drops
radicals inconsistently, so a printed `8` and a printed `sqrt(8)` are not distinguishable there. No
erratum is asserted, and none should be inferred from this file. Confirming the printed form requires
rendering the PDF page, which I did not do.

---

## 2. Conventions, tested against the source (not just read)

| object | convention | how it was tested |
|--------|-----------|-------------------|
| `Pi` | `Pi[i][j] = ((i/6==j/6) - 1/6)*((i%6==j%6) - 1/6)`, `Pi^2 = Pi`, rank 25 | `patchx.cpp:172`; reproduced to `1e-16` |
| basis of `ran Pi` | `Q[6i+j][5a+b] = q[i][a] q[j][b]`, `q[i][a] = 1/sqrt((a+1)(a+2))` for `i<=a`, `q[a+1][a] = -(a+1)/sqrt(...)` | `basis()` in `patchx.cpp` |
| `F` | `F_ij = (1/2 pi i) sum_g e(P_ig - P_jg)`; stored `(Re, Im)`; code writes `f = (Im/(2pi), -Re/(2pi))` | sign re-derived; matches (4.1) |
| `L_P` | `(L_P x)_ij = sum_g e(P_ig-P_jg)(x_ig - x_jg)`, no `2 pi i` factor | (4.2), `fullL` |
| `T` | 36 x k, stored as **k rows of 36** doubles; `T T^*` = Gram of those rows | record layout |
| tangent split | eigen-decomposition of `Gram = J^*J` (25x25, `J = L_P Q`), threshold **`lambda < .64`** for a `T` column, `k <= 10` | `patchx.cpp:100-118` |
| `M` | `M = sum_{lambda_i >= .64} h_i l_i^*`, `h_i = Q v_i`, `l_i = J v_i / lambda_i` -> 36x30, not serialized | `patchx.cpp:120-136` |
| `mnorm` | `sqrt((ah+1e-8)(al+1e-8)) + 1e-8`, `ah`,`al` = max absolute row sums of the Grams of `HV`,`LV` | A.5 (A.14) |
| `id, ort, hor, froot, n0, C` | `sqrt(.)+2e-6`, `+1e-8`, `+1e-8`, `sqrt(val)+1e-9`, `mnorm*froot+1e-9`, `min(pi sqrt8 mnorm + 1e-7, pi sqrt6 sqrt((row+.0002)/(1-beta)) + .00001)` | `patchx.cpp:143-181` |

**Tested, not assumed.** Rebuilding `M` from `P` with these conventions reproduces
(a) the stored subspace `span(T)` to `||P_T - P_Tstored||_F <= 3e-11` with `k` exactly
(`derive.py`), and (b) the stored `mnorm` to `|mnorm - (sqrt((ah+1e-8)(al+1e-8))+1e-8)| <= 6e-8`
relative over 2491 records in three files. A convention error in `Q`, in the edge order, or in `T`'s
row/column storage would destroy (a) and (b) immediately. Agreement at that level is evidence that
the conventions are right; it is not a proof that the reconstructed `M` is the run's `M` (§4.3).

---

## 3. A structural lemma: the `id` clause is identically zero in exact arithmetic

Let `Gram = J^*J = V Lambda V^*` with `V` orthogonal, split the columns into "small"
(`lambda < .64`, giving `T = Q V_s`) and "good" (`V_g`), and set `M = (Q V_g) Lambda_g^{-1} (J V_g)^*`
as the source does, with `J = L_P Q` and `Q^*Q = I_{25}`, `Q Q^* = Pi`.

Then, exactly,

```
Pi - T T^* - M L_P Pi
  = Q Q^* - Q V_s V_s^* Q^* - (Q V_g) Lambda_g^{-1} (J V_g)^* J Q^*
  = Q Q^* - Q V_s V_s^* Q^* - Q V_g Lambda_g^{-1} V_g^* (J^*J) Q^*
  = Q Q^* - Q V_s V_s^* Q^* - Q V_g V_g^* Q^*          [V_g^* J^*J V_g = Lambda_g]
  = Q (I - V_s V_s^* - V_g V_g^*) Q^*  =  0
```

(unitarity of `V` gives `V_s V_s^* + V_g V_g^* = I`). So (4.15)'s third clause carries no
mathematical content *for the canonical `M`*; `id` is a rounding allowance. Measured: the exact
residual is `<= 5e-14` on every record inspected, against the stored `id = 2.000e-6`.

Consequences: (i) a checker must never infer the identity's truth from `id` being small — for the
canonical `M` it is vacuous; (ii) `R6` can only be *informative* for a witness that is not canonical;
(iii) the substantive witness obligations are `R5` and `R7`.

---

## 4. What the saved bytes can and cannot certify

A saved record is `356 + 288k` bytes: `k`, `p[36]`, `T[k][36]`, `C, n0, id, ort, hor, mnorm, froot,
radius`. There is **no `M`**, no `HV`, `LV`, no `U`, and no cell/box/assignment data.

### 4.1 Decidability per obligation (mode `none` in `rootcheck.py`)

| obligation | from the stored record alone |
|---|---|
| G1, G2, R1, R2, R4 | **decidable and exact** (pure rational arithmetic on the stored floats) |
| R3 | decidable given a sound `e(x)` enclosure; no witness needed |
| R5, R6, R7 | **not decidable**: they quantify over `M` (and `U`), which is not stored |

`R5-R7` are existential in `M`; the record does not name one. Note the gauge: on the canary `L_P Pi`
is `30x36` of **rank 25** (`sigma_min = 1.3e-16`), so `M (L_P Pi) = Pi - T T^*` constrains `M` only
on a 25-dimensional subspace of `R^30` and leaves a **5-dimensional free component**. R6 does not see
that component; R5 and R7 do (measured on the canary: a shift of `1e-2` in Frobenius norm inside that
component moves `lambda_max(A)` by `1.3%` and `||M||_2` by `0.09%`). Consequently:

* a certificate must **declare the `M` (or `HV, LV`) it means**, and a checker that derives its own
  `M` certifies *a* witness, not necessarily the run's: sound, but possibly lossy;
* two admissible witnesses exist, and neither design is forced:

**(A) transport the witness.** Emit `HV` (36 x g) and `LV` (30 x g), `g = 25-k = 21` typically;
`11088 B/record`, 7.4x the current record (at `k=4`, 1508 -> 12596 bytes; plus `7200` for `U` when
the tensor constant is used). Then `R5` is exact and cheap: `||M|| <= ||HV|| ||LV|| <= sqrt(ah) sqrt(al)`
with `ah`, `al` the absolute-row-sum bounds — literally A.5's argument — and `R6` uses the exact
`M = HV LV^*`.

**(B) derive then verify.** The checker rebuilds `HV, LV, U` by the canonical construction (float64
proposal) and verifies R5, R6, R7 on the result. Zero extra bytes; the proposal step enters the
trusted base but cannot create a false PASS.

**`M` alone is a poor witness.** Emitting the 36x30 matrix (8640 B) leaves R5 as "compute `||M||_2`
to `4e-8` relative accuracy": measured, `mnorm/||M||_2 = 1+3.7e-8 ... 1+5.9e-8` over 2491 records, so
the cheap rational bounds (`||M||_F`, `sqrt(||M||_1 ||M||_inf)`) are 2-3x too large and do not
certify it; one would need exact Cholesky of `mnorm^2 I - M^*M` (30x30, ~20 s/record in Python
`Fraction` — measured) or a certified SVD. The factor pair avoids all of this because Gershgorin *is*
the source's own bound.

### 4.2 Which obligations bind, and how much headroom they have

Exact margins on a stratified sample (`census.py`, exact `mpq`; margin = stored constant minus the
certified upper bound it must dominate):

| obligation | margin (min over sample) | reading |
|---|---|---|
| R1 `ort - ||T^*T-I||_F` | `+1.000e-08` | defect `~1e-15`, the `+1e-8` bump dominates: slack `1e7` |
| R2 `hor - ||(I-Pi)T||_F` | `+1.000e-08` | same |
| R3 `froot - ||F(P)||` | `+1.000e-09` | `||F|| ~ 1e-11`: slack `~1e2` |
| R4 `n0 - mnorm*froot` | `+1.000e-09` | slack `~2x` |
| **R5** `mnorm - sqrt((ah+1e-8)(al+1e-8)) - 1e-8` | **`+3.63e-15`** (median `7e-15`) | **essentially zero: relative `1e-14`** |
| R6 `id - defect` | `+2.000e-06` | defect `~1e-14`: slack `1e8` |
| **R7** `C - pi*b(M)` | `+4.7e-03` (coarse0), **`+1.0e-12` (mid), `+5.5e-13` (fb1)** | **essentially zero on the refined files** |

Three consequences, stated as measurements and design facts, not as defects:

* **`R5` has almost no headroom.** The stored `mnorm` exceeds the requirement by `~5e-15`, which is
  *smaller* than A.5's own `1e-10` allowance for the row sums `ah`, `al`. Since a checker recomputes
  `ah`, `al` with its own accumulation order, `R5` can legitimately come out **UNDECIDED** on a
  record the source accepted — the bound is simply too tight to survive re-evaluation. This is a
  property of the constant, not evidence against the record. A design response is for the emitter to
  carry slack in the derived constants (`mnorm` with a larger additive bump, `n0` and `C` recomputed
  consistently), or for the checker to re-issue the derived constants from the transported witness;
  either way the *obligation* is unchanged.
* **`C >= pi*sqrt(8)*mnorm` does not certify most records.** On 13 of the 15 sampled records the
  stored `C` is *below* that expression (this is a direct comparison of stored bytes with an
  interval value of `pi`, needing no witness), so a checker must use the tensor branch
  (`beta = ||U^*U - I||_F + 1e-8 < .1`, `||A|| <= (row + .0002)/(1-beta)`, A.5), or another
  admissible route.
* **Inflating `C` is not obviously available.** `C` enters `n_P(s) = n0 + id s + C s^2` and hence
  (4.38); at the measured `s0 ~ 0.04` an increase from `4.5` to `14.5` changes `n_P(s0)` by
  `~2e-2`, which is the order of the Stage-B radius cap `1.1e-2`. Whether that breaks coverage
  depends on how `n_P` propagates through Stage B's radius recursion and grid tests, which I did
  **not** compute. Treat "C can/cannot be inflated" as an open engineering question, not a result.

### 4.3 Unresolved witness anomaly: 43 records

With a freshly derived `U` (`numpy.linalg.eigh` of the reconstructed `A`) the R7 bound exceeds the
stored `C` on **43 of 2491** records (`coarse0.bin` 19, `mid.bin` 24, `fb1.bin` 0), by `~0.03`
typically and `0.213` worst; on the other 1850 tensor-branch records the same route reproduces the
stored `C` to `<1e-7`. Under §0's semantics these 43 are **UNDECIDED**, not failures: a different
admissible `(M, U)` — in particular the run's own Jacobi output, which was never archived — may well
certify them, and I could not test the source's basis.

What is and is not excluded, stated exactly:

* *Not excluded*: that the source's own `U` certifies these `C` values (most likely explanation, and
  untestable without the run's `U`).
* *Not excluded*: that a different admissible witness `M` (a different point in the 5-dimensional
  gauge, or a different but equally legitimate eigenbasis inside a cluster) certifies them. My gauge
  probe (a `1e-2` gauge shift moves `lambda_max(A)` by `1.3%`) shows the gauge is *sensitive enough*
  to explain a deficit of this size; whether some gauge value closes it is not decided.
* *Not claimed*: any unsoundness of the stored `C`, any source/data mismatch, any defect in the
  preprint or the run.
* *Reproducible*: the 43 indices and the deficits come from `tensor_branch.py` and `census.py`.

**Cross-check against the other directions.** `m5`/d2 independently reports "stored `C` is not
reproducible from `(p,T)`" with a derived `U` overshooting by up to `4.4%`; `m6`/d1 reports
`C >= pi*min(sqrt8 ||M||_2, sqrt6 ||S||_2)` with ratio `1.47 .. 1.78` on all 27189 records. Both
cannot be right, and I do not adjudicate it here: my own reconstruction lands *on* the stored `C` to
`1e-12` on `mid.bin`/`fb1.bin`, which says my `A` is close to whatever the source used *there*, but
that is evidence about aggregate agreement, not a resolution of the 43 records or of d1's factor.
The decisive experiment is to extract and replay the source's own `Jacobi` output (`U`, `beta`,
`row`) for those records, or to serialise `U`. Until then the 43 stay on the unresolved list.

**One design conclusion survives all three readings**: the *witness* must be shipped and `C`
recomputed (or cross-checked) from it, because `C`'s admissibility depends on data the record does
not contain. That is a certifiability requirement, not an allegation.

---

## 5. Measured results

**Parser.** `records.py` parses every saved file and checks that the declared count reaches the exact
end of file: `coarse0/1/2/3.bin` 764/774/757/788, `mid.bin` 600, `fine.bin` **22379**, `fb1.bin`
1127 — **27189 records**.
Population facts: `k in {0,4}`, and **exactly one `k=0` record per atlas file** (6 of 27189;
`fb1.bin` has none) — a population that Stage A/atlas should explain; `C in [3.63,5.11]`,
`n0 ~ 1.4-1.6e-9`, `id = 2e-6 + O(1e-12)`, `ort = 1e-8 + O(1e-14)`, `hor = 1e-8 + O(1e-15)` (those
three bumps dominate), `mnorm in [0.408,0.577]`, `froot in [1.00,1.10e-9]`, `radius in [2.0e-5,
0.125]`.

**Checker.** `rootcheck.py` decides G1, G2, R1-R7 in the three-valued logic of §0 on a real record:
all nine obligations PASS on the canary `fb1.bin[0]`, and on all 15 sampled records (`census.py`),
with the margins of §4.2.

**Corruption suite** (`mutants.py`, canary `fb1.bin[0]`, single-field edits, default "derived
witness" mode):

| mutant | verdicts that move |
|---|---|
| unmutated | all nine PASS |
| `froot := 1e-13` | **R3 FAIL** (refutation from stored bytes) |
| `ort := 0` | **R1 FAIL** |
| `hor := 0` | **R2 FAIL** |
| `n0 := 0.5 mnorm froot` | **R4 FAIL** |
| `mnorm x (1-1e-6)` | R5 **UNDECIDED** (derived `M` fails; no witness certifies) |
| `id := 1e-15` | R6 **UNDECIDED** (upper enclosure exceeds `id`; exact defect not bounded below) |
| `C x 0.999` | R7 **UNDECIDED** (derived `U` fails; other `U`, `M` not excluded) |
| `C x 1.0001` | all PASS (a larger `C` is conservative — correct) |
| `T_0 x 1.001` | **R1 FAIL**, R6 UNDECIDED |
| `p_3 += 1e-5` | **R3 FAIL**, R5/R6/R7 UNDECIDED |
| `T` columns 0<->1 swapped | all PASS (the Root depends on `T` only through `T^*T`, `TT^*` — correct) |
| `k := 0`, `T` dropped | R6 UNDECIDED |
| `C := NaN` | **G1 FAIL**, rest UNDECIDED (a crashed checker is not a rejecting one — this path was a real bug, now closed) |
| same record, **witness withheld** | G1,G2,R1-R4 PASS; **R5,R6,R7 UNDECIDED** |

With `witness_emitted=True` (the certificate-file reading) the same mutants turn R5/R6/R7 into FAIL:
that rejects the *file*, which is the correct verdict for a transported witness that contradicts the
record.

**Cost** (`cost.py`, one record, pure Python + gmpy2 `mpq`, single core):

| phase | s |
|---|---|
| 36 `e(P_h)` enclosures (`cos/sin` at a rational midpoint, Machin `pi`) | 0.013 |
| `F(P)` and `||F||` (15 edges) | 0.270 |
| R1, R2 exact Gram defects | < 0.001 |
| R5 `ah`, `al` exact row sums (36x21 and 30x21 Grams) | 0.033 |
| `L_P Pi` rows, 30x36 with projection | 0.891 |
| **R6 36x36 interval defect** | **8.777** |
| `A` = signed Gram of `M` (30x30) | 0.036 |
| R7 exact congruence row sums (`U^*AU`, 30x30) | 0.078 |
| total | **10.1** |

So this implementation costs `~10 s/record` — `75 CPU-hours` for the 27189-record corpus. Where the
time goes is measured; what a compiled or vectorised implementation would cost is **not** measured
and I make no claim about it. The only structural remark that follows from the table is that `R6`'s
interval evaluation dominates and that its subject matter is the clause which §3 shows to be
vacuously satisfied for the canonical witness — so a certificate format that *transports* `HV, LV`
lets `R6` be replaced by the identity of §3 plus a much cheaper check of the non-canonical part.
That is a design consequence, not a certified fast path: the certified path stays exact rational for
R1, R2, R4, R5, R7 and outward-interval for R3, R6, as `cert/spec/arithmetic.md` requires.

---

## 6. Implementation plan this hands to the next team

1. **Freeze the record schema** as `k, p[36], T[k][36], C, n0, id, ort, hor, mnorm, froot, radius`
   plus a witness block `HV[36][g], LV[30][g]` (mandatory) and `U[30][30]` (mandatory iff the tensor
   constant is used), `g = 25-k`.
2. **Emit from `buildH::patch`** where `HV`, `LV`, `U` already exist (no recomputation), before
   `saveRecords`. Byte cost per record: `11444+288k`, plus `7200` with `U`.
3. **Checker order** (cheapest refutation first): G1 -> G2 -> R1 -> R2 -> R4 -> R5 -> R7 -> R3 -> R6.
4. **Witness discipline**: `R1-R4` may FAIL on a record; `R5-R7` may only FAIL on a *transported*
   witness, otherwise UNDECIDED. Every certificate must state which reading applies.
5. **Interface to the consumers** (unchanged): Stage B/atlas may use only `(ort, id, C, mnorm,
   froot, n0)` through (4.5)-(4.7); anything that uses `P` for a distance (atlas `find`, merge `d`,
   Stage B's `dq`) needs the rephasing/alignment clause, which is a different certificate (H2-ATLAS).
6. **Negative controls for CI**: the 15 mutants above, in both witness readings, plus mode `none`
   which must report exactly three UNDECIDED.

---

## 7. Explicitly unverified / not done here

* **Partial Lean only.** `RootConsumer.lean` (`lean RootConsumer.lean` exits 0 against the installed
  Mathlib) proves the *consumer* step: `normal_bound_mono` (`n_P` is nondecreasing on `[0, inf)`,
  where nonnegativity of `n0, id, C` is consumed) and `root_radius_step`, Proposition 4.13 / (4.38)
  as a one-step implication: from `n <= n_P(s)`, `s^2 <= (1+ort)t^2 + n^2`, `s <= s0` conclude
  `s <= sqrt (n_P(s0)^2 + (1+ort)t^2)`. Not formalised: the remainder lemmas (4.8)-(4.12), the
  residual identity of Proposition 4.5, and "R1-R7 => Definition 4.1".
* **`HV`, `LV`, `U` are not the run's bytes.** They are rebuilt from `P`. Every verdict is an exact
  certificate for `(P, T, HV_rebuilt, LV_rebuilt, U_rebuilt, constants)`. Whether the run's internal
  factors agree to A.5's `2.1e-11` is a claim about the run that is supported by the aggregate
  agreement in §2 but **not** checked record by record, and not at all for the 43 records of §4.3.
* **R6 is Frobenius, not operator.** The operator form of (4.15) is only *implied* by a Frobenius
  pass; a Frobenius failure leaves the operator form undecided, and is reported as such.
* **`pi`** is enclosed by Machin's series with 60 alternating terms (`width 7e-86`), spot-checked
  against `mpmath` at 160 digits on 804 points. Not a formally verified constant.
* **Sample sizes.** Slack census: 15 records (5 per file) exact; the derived-`U` sweep covers 2491
  records in binary64; `fine.bin` (22379) and `coarse1/2/3.bin` were parsed and population-censused
  only, not read through the exact checker.
* **The six `k=0` records** were not analysed individually; `R5` degenerates there because the
  canonical `M` is the full pseudo-inverse.
* **No claim about N(6)=3**; no Stage A/B/C obligation checked; no full-corpus exact run.
