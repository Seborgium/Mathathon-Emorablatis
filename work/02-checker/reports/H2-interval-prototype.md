# H2 — INTERVAL PROTOTYPE (direction 5): outward arithmetic as the verdict layer for Root and Stage B

Status: **prototype, measured on saved records; no full-proof claim.**
Owner: member m5 of swarm `smwgx2sv0`. Every number below is produced by the scripts in this
directory from the saved run data
(`.scratch/h0/dl/verification/saved-run/execution/data/`).

Deliverables in `.ultramath/smwgx2sv0/m5/` (all runnable, `python3`, no third-party numerical
dependency on a verdict path):

| file | what it is |
|---|---|
| `num.py` | exact dyadics `Dy` + outward intervals `Iv` (2^-128 fixed point), rigorous `π`, `sin`/`cos` (Machin + Taylor with explicit tail bound), `sqrt` by `isqrt` |
| `rec.py` | exact parser for the upstream `Record` format (`atlas.cpp saveRecords`), byte-checked |
| `root_float.py` | binary64 recomputation of (4.1)/(4.2)/(4.4) — *proposals and convention tests only* |
| `sourceM.py` | reconstruction of the paper's auxiliary map `M` (§4.2, `buildH::patch`) from `p` alone |
| `rootcheck.py` | the Root checks `(4.4)/(4.15)/C`, exact + interval, with verdicts and slacks |
| `stageb.py` | the Stage-B relation (`Lemma 5.1`, `Prop 5.2`, `(5.14)–(5.16)`, `Lemma 5.5`) in **exact rational arithmetic** |
| `relfloat.py` | independent binary64 port of `relationB::init/eval` — cross-check only |
| `align.py` | exhaustive transport search (2,073,600 signed permutation/transpose maps) — a *proposal* step |
| `stageb_run.py` | complete base-grid ledger for one real fallback parent |
| `measure_stageb.py` | the measurement table, writes `out/stageb_parent0.json` |
| `out/root_sample.json`, `out/stageb_parent0.json`, `out/stageb_slack.json` | recorded measurements |

Reproduce (from that directory):

```
D=/workspace/nucleus/work/projects/p-20d35e783d5d4092acb8bd94b19cf30b/repo/.scratch/h0/dl/verification/saved-run/execution/data
python3 rootcheck.py $D/coarse0.bin $D/coarse1.bin $D/coarse2.bin $D/coarse3.bin $D/mid.bin $D/fine.bin $D/fb1.bin --json out/root_sample.json
python3 measure_stageb.py          # ~40 s
```

---

## 0. Headline

1. **The six basic Root checks are decidable from the stored `(p, T)` alone: 48/48 pass, 0
   undecided.** The auxiliary map `M` of (4.15) need not be serialised: the paper's own construction
   (eigen-split of the 25×25 horizontal Gram at 0.64) is reproducible to `1e-14` relative and both of
   its required properties are re-verified one-sidedly; the certified residual is `≤ 5·10^-11` against
   a stored `id ≈ 2·10^-6`.
2. **Complete Root verdicts (the six basic checks *plus* the sufficiency condition on `C`) are
   46 pass / 2 FAIL** on the same 48-record sample. The two failures are an **interface / witness
   mismatch on `C`**, not a false Root and not a defect in the stored record: where the source took
   the tensor minimum, an independently chosen (equally valid) change of basis `U` reproduces the
   stored `C` only to the percent level (`+4.4 %` worst case), so `C` is not re-certifiable from
   `(p,T)` without either `U` or a re-issued `C`. Two fixes are costed in §3.
3. **Stage B contains no transcendental function at all.** Every quantity of `(5.5)–(5.16)` is a
   rational function of stored binary64 entries plus square roots and one spectral-norm bound, so the
   whole Stage-B ledger is decidable in exact dyadic arithmetic with integer square roots — a much
   smaller trusted base than Root. Measured: every comparison decided, smallest margin `8.5·10^-8`.
4. **A complete base-grid ledger for one real fallback parent**: 11480 of 14641 base grid slots outside,
   1709 covered by certified relations, **1452 unresolved**, and the unresolved set is not a defect of
   the paper — it is exactly the evidence the saved run did not archive (§4.4 names the three missing
   witness classes, with byte costs).
5. **A convention check stronger than "it parses"**: recomputing `(5.20)–(5.22)` gives
   `163 × 14641 = 2 386 483` base grid slots and `163 × 3161 = 515 243` non-outside slots, which equal
   the run's own recorded `base 2386483` and `inside 515243` for the fallback pass **exactly**.
6. **Feasibility, measured for the prototype**: `45 ms` per certified relation edge and `0.19 ms` per
   base grid slot in Python/`Fraction` arithmetic. The recorded runs contain `2.8·10^7` certified
   relation edges (`pair`) and `1.41·10^9` base grid *slots*, i.e. **≈420 CPU-hours in this
   prototype**. These are slot counts, not relation evaluations: a certificate supplies the edges, so
   a checker never repeats the run's `pairTry` attempt counts, which are 100–300× larger. Projecting a
   fixed-point rewrite (20× on relations, 100× on the slot predicate) gives **≈16 CPU-hours, but that
   is an architecture estimate — no such implementation was built or measured here.** Even as an
   estimate it changes the story from "infeasible" to "a 1–2 day shard", dominated by the `2.3·10^7`
   mid-pass edges rather than by the slots (§5).

---

## 1. Arithmetic kernel (`num.py`) — and what it does not trust

* `Dy`: exact dyadic `n·2^-s`. Every stored entry, every scalar constant, and every product/sum of
  them is exact; no rounding happens anywhere in the Stage-B algebra.
* `Iv`: closed interval `[lo,hi]·2^-128`. `+`, `−`, `×` outward by `floor`/`ceil` of integer products;
  `sqrt` by `isqrt` (exact directed rounding); `x²` special-cased so an interval straddling 0 gives
  `[0, max]` (the naive product rule reports a negative left end — a real bug found and fixed here).
* `π`: Machin `16·atan(1/5) − 4·atan(1/239)` with the alternating-series remainder bound, in
  `Fraction`; the enclosure is `2.9·10^-39` wide and contains the 40-digit value of `π`;
  self-consistency tested across 120/300/900-term truncations.
* `sin`/`cos`: reduction `t = k·π/2 + r`, with `k` proposed on the midpoint and the reduction
  *verified* (`|r| ≤ π/4`), then interval Taylor (26+26 terms) with the first omitted term as tail
  bound. No `libm` and no `numpy` transcendental is on any verdict path. Measured enclosure width
  `1·10^-37`; `cos²+sin²−1` inside `[−80,80]·2^-128`; `e(1/3)`, `e(1/2)`, `e(1/4)` verified exactly.
* Decidability discipline: `Iv.le` returns `True` (enclosure proves `≤`), `False` (proves `>`), or
  `None` (**undecided**, never a pass and never an exclusion). Undecided counts are zero everywhere
  in §2–§4.
* Independent test of the enclosures (done outside this directory, on these artefacts): 150
  `sincos` cases produced no enclosure violation with maximum width `9.1·10^-37`, 1000 dyadic `sqrt`
  bounds held, and the `π` enclosure was confirmed. That is a check of the kernel only, not of the
  certificate logic.

---

## 2. Root certificate: the complete check list and what it needs

`Π` = double centering (rank 25), `F` = (4.1) as a real 30-vector (real part then imaginary part,
edges `(i,j)`, `i>j`, `i` increasing then `j`), `LP` = (4.2), `n_P(s) = n0 + id·s + C·s²`.

| # | obligation | quantity comes from | arithmetic | measured (48 records) |
|---|---|---|---|---|
| R1 | `dp = p − p_{i0} − p_{0j} + p_{00} − nearest_int`, and the integer lift is part of the witness | stored `p` | exact | no ties in the sample (§6.6) |
| R2 | `‖T*T − I‖_F² ≤ ort²` | `T` | exact + `isqrt` | 48 pass, slack `≥ 1.00e-8` |
| R3 | `‖(I−Π)T‖_F² ≤ hor²` | `T` | exact + `isqrt` | 48 pass, slack `≥ 1.00e-8` |
| R4 | `‖F(P)‖² ≤ froot²` | `p` | interval `e(2πix)` | 48 pass, slack `≥ 1.00e-9` |
| R5 | `mnorm·froot ≤ n0` (4.15b) | scalars | exact | 48 pass, slack `= 1.00e-9` |
| R6 | `‖M‖ ≤ mnorm` (4.15a) | **witness M** | exact + `isqrt` | 48 pass, slack `≥ 2.1e-8` |
| R7 | `‖Π − TT* − M LP Π‖_F² ≤ id²` (4.15c) | **witness M**, `p`, `T` | interval | 48 pass, residual `4.5·10^-14 … 4.9·10^-11`, stored `id = 2.0·10^-6` |
| R8 | `C ≥ π·b` (Lemmas 4.3/4.4) — a *sufficiency* condition on the stored constant, separate from R1–R7 | see §3 | interval + exact | `C_base` 24/48, `C_tensor` 36/48 |

**Reading the table.** R1–R7 (the six comparisons `ort`, `hor`, `froot`, `n0`, `mnorm`, `id`) are the
basic Root checks of Def 4.1/Prop 4.5 and pass 48/48 with zero undecided. R8 is a *different kind of
obligation*: it says the stored scalar `C` is a valid remainder constant. Summing them into one
"Root pass" gives **46 pass / 2 FAIL**; the two files that fail are `coarse0#678` and `coarse3#33`, and
they fail only R8 (§3.2). Nothing in R1–R7 is wrong on those records.

### 2.1 R6/R7 witness: `M` is reconstructible, not serialised

The paper says `M` "is used only to establish the Root assertions and is not serialized". A checker
therefore needs a deterministic reconstruction. Implemented (`sourceM.py`, `rootcheck.m_part`):

```
J      := LP(p)·Q                    # 30×25, Q = q⊗q from buildH::Basis (Helmert columns)
G      := J*J                        # 25×25
G V    := V diag(w)                  # eigen-decomposition (the source's Jacobi sweeps)
T_prop := Q V[:, w<.64]              # the paper's proposal for the k tangent columns
M      := (Q V[:, w≥.64]) · (J V[:, w≥.64] diag(1/w))*        # 36×30, exact in Dy
```

and then *verify*, never assume:

* **R6** as `√(ah·al) ≤ mnorm` with `ah = max_i Σ_j |(HV*HV)_{ij}|` and `al` likewise for `LV` — the
  paper's own factor bound `‖M‖ ≤ ‖HV‖·‖LV‖`. The direct bound `max_i Σ_j |(MM*)_{ij}|` is *weaker*
  on this data (`0.725` vs `0.577`), so the factor form must be in the spec, not left to the
  implementer.
* **R7** with `M` exactly as above and `LP` from interval `e(2πi·p)`.

Measured over the 48-record stratified sample (`out/root_sample.json`):

* the reconstruction reproduces the stored `mnorm` to `−3.7·10^-8 … −5.4·10^-8` relative, i.e. the
  stored constant is exactly `√((ah+1e-8)(al+1e-8)) + 1e-8` for our `ah, al`;
* the eigen-split reproduces the stored `k` in **48/48** records (`25 − #big = k`);
* R7's certified residual is `≤ 4.9·10^-11`, four orders below the stored `id = √err + 2·10^-6`
  (`√err ≈ 5·10^-14`). The `2·10^-6` pad — not the reconstruction quality — is what makes R7 work;
  this check is insensitive to the eigenbasis (the identity `M·LP·Π = Π − TT*` holds for *any* exact
  eigenbasis of the split: measured residuals `10^-14`–`5·10^-11`). Only the norm bound is
  basis-sensitive, and it is reproducible to `5·10^-8` because `ah ≈ 1` is basis-independent.

**Non-claim.** We do not claim our Jacobi/eigh output equals the source's map-for-map; we claim the
checker's own `M` satisfies both obligations of (4.15) and that the stored `mnorm` bounds it. The spec
must freeze the reconstruction (or serialise `M`: `36·30·8 = 8640` bytes/record, ≈30 MB for the whole
run — affordable but unnecessary given the measurement).

### 2.2 Computable from stored fields vs missing witnesses

| quantity | stored? | recomputable from `(p,T)`? | used by |
|---|---|---|---|
| `dp`, `F(P)`, `LP` | no | **yes** | R1, R4 |
| `T*T`, `(I−Π)T` | — | **yes** | R2, R3 |
| `HV`, `LV`, `M` | **no** | **yes**, up to eigenbasis choice | R6, R7 |
| `mnorm` | yes | **yes** (`√(ah·al)` to `5·10^-8`) | R6 |
| `froot` | yes | yes | R4 |
| `id` | yes | no (needs `M`) | R7 |
| `C` (tensor-improved) | yes | **no** (§3) | R8 |
| `U, β, r` (tensor path) | **no** | `S` yes (exact from `M`); `U` up to basis choice | R8 |

---

## 3. The remainder constant `C` and the tensor improvement (4.14)/(4.15)

### 3.1 The two candidates, exactly

* first choice: `C₀ = π·√8·mnorm` (the source stores `C₀ + 10^-7`);
* second choice: with `S` the 30×30 row Gram (4.14), `S_{ab} = sgn(a,b)·Σ_h M_{ha}M_{hb}` (`sgn` from
  the edge-label formula, exact), a proposed real change of basis `U`, `β = ‖U*U − I‖_F`, `X = S U`,
  `r = max_i Σ_j |(U*X)_{ij}|`: `C₁ = π·√(6(r + 2·10^-4)/(1−β)) + 10^-5`, valid when `β < .1`.

Every ingredient of `C₁` except `π` is exact rational given `U`, so `C₁` is checkable with the same
exact/interval kernel — no eigensolver trust, only a `U` witness.

### 3.2 Measured: our `U` reproduces the stored `C` usually, not always — an interface mismatch

* records where the tensor path was not taken (`stored = C₀ + 10^-7`): our `C₀` matches to `−1.0·10^-7`
  and R8 passes with slack exactly `10^-7`;
* tensor-improved records: our `C₁` is **below** the stored `C` for 46/48 (typical `−10^-3 … −8·10^-2`
  relative) and **above** for 2/48 (`coarse0#678 +1.1 %`, `coarse3#33 +4.4 %`, `out/root_sample.json`).

So `C` is witness-dependent at the percent level: the row-sum bound `r` depends on the rotation chosen
inside near-degenerate eigenclusters of `S`, and the stored `C` carries the source's own `U`, which the
saved run does not archive. This is an **interface mismatch between the stored scalar and the data the
certificate carries**, not an error in the Root: R1–R7 still pass on both records, and the paper's
Lemma 4.4 second choice remains a true statement about *the source's* `U`.

### 3.3 The two fixes

1. **Re-issue `C` (recommended).** Define the certificate's `C` as the checker's own
   `max(C₀, C₁(U_cert))` with `U_cert` a documented deterministic proposal, instead of the source's
   minimum. Nothing downstream breaks: `C` is an upper bound used in `n_P` and in `λ = α + γD`, so a
   larger `C` only enlarges radii. Cost: zero witness bytes. Price measured: always using `C₀` (no `U`
   at all) raises `C` by `≤ 9 %` (`C/C₀` ranges `0.913 … 1.000` over `coarse0`), which tightens the
   Stage-B thresholds `ℓ = √(a² − v0²)`; the Stage-B search may need re-running.
2. **Serialise `(U, β, r)`** — 7.2 kB/record (or `(β,r)` + a documented `U`), only if `C` must stay
   bit-identical to the saved run.

### 3.4 Witness-free fallback

`‖S‖² ≤ √(max_i Σ_j |(S²)_{ij}|)` (the `‖G²‖_F` option the source already has in `spectralUpper`) is
exact rational from `S` alone but much weaker here (the eigenbasis improvement is worth ≈9 % of `C`),
so `C₀` is the practical witness-free choice.

---

## 4. Stage B: exact-rational relation ledger

### 4.1 Why Stage B is cheaper to certify than Root

`(5.5)–(5.16)` involve only differences/products of stored binary64 entries, the projection `Π`, `√`,
and one spectral-norm bound of a `k×k` Gram (`k ≤ 10`). No `exp`, no `sin`. Consequently the whole
Stage-B obligation set is decided in exact dyadic arithmetic: the only error sources are `isqrt`
(exactly directed) and the checker's own fixed-point truncation, which is **upward only** (`up`,
`umul`, `usqrt`), so every returned number is an upper bound of the quantity the paper bounds — the
direction the implications need.

### 4.2 The checkable relation object (`stageb.Relation`)

Given a parent `P` (radius `R`), a child `Q` (radius `a`) and a transport map
`Φ = (row[6], col[6], trans, neg)` (Lemma 4.7):

```
dq  := Π( wrap( dp(ΦQ) − dp(P) ) )                              (5.5), exact
η   := T_P^* dq,      n_q := ‖(I − T_P T_P^*) dq‖               (5.5)/(5.6), exact
D   := R + ‖dq‖,      v0 := n0_P + id_P·R + C_P·R² + n_q                (5.7), upward
λ   := id_P + C_P·D,  e0 := mnorm_P·froot_Q                            (5.7), upward
σ   := √(spectralUpper(G) + 10^-7) + 10^-8,   G = W W^*,
       W_a = Π T_{Q,a} − Σ_j ⟨Π T_{Q,a}, T_{P,j}⟩ T_{P,j}             (5.8), upward
β   := √(1+o_P)·√((1+o_P)(1+o_Q))                                      (5.8), upward
z(b):= √(1+o_P)·t,   v(b) := min(v0, (1+o_P)b, λb+e0)
ψ_P(b) := √(z² + v(b)²),  ψ_Q(b) := √((1+o_Q)(βt+σv(b))² + n_Q(b)²),
n_Q(b) = n0_Q + id_Q·b + C_Q·b²
D̂(t) := 30 iterations of b ↦ min(b, ψ_P(b), ψ_Q(b)) from b₀ = min(D, √(z²+v0²))
```

Certified object (Lemma 5.4/5.5): a pair **`(ℓ, D̂(ℓ))` with `D̂(ℓ) ≤ a`**; then every parent solution
in a base box with `t_B(box) ≤ ℓ` lies in `S(Q,a)`, where `t_B(box)² = Σ_a (|u_a − η_{q,a}| + w/2)²`.
Monotonicity of `D̂` is never used — only the single verified value at `ℓ`, and the box test compares
squares exactly.

**Not trusted:** the snap, the eigen-iteration, any `variants` heuristic, our own transport search.
`Φ` and `ℓ` are witnesses; the checker recomputes `D̂(ℓ)` and the box test.

### 4.3 A real record example (reproducible)

Parent `bad10.bin#0` (`R = 0.016`, `k = 4`, `C = 4.38`, `mnorm = 0.50`, `froot = 1.0·10^-9`),
children `fb1.bin#0…#65` (fallback atlas, `τ = 0.011`, `w = 0.0038`), all under the **identity** map
(the exhaustive 2,073,600-map search confirms identity is optimal for `#0…#5`):

| child | `‖dq‖` | `n_q` | `v0` | `λ` | `σ` | `a` | `ℓ` | `D̂(ℓ)` |
|---|---|---|---|---|---|---|---|---|
| #0 | 0.018971 | 2.62e-4 | 1.3775e-3 | 0.15234 | 0.067693 | 0.010999 | 0.010912 | 0.010999 |
| #1 | 0.016273 | 3.06e-4 | 1.4212e-3 | 0.14059 | 0.057861 | 0.010996 | 0.010904 | 0.010996 |
| #2 | 0.018994 | 2.75e-4 | 1.3901e-3 | 0.15244 | 0.067233 | 0.010999 | 0.010911 | 0.010999 |

An independent binary64 port of `relationB::init/eval` (`relfloat.py`, written from the C++ only)
reproduces `σ` to `1.5·10^-6` and `D̂(t)` to `6·10^-8` on these pairs — the residual difference is
exactly the source's `10^-8`/`2·10^-7` float pads, which a rigorous computation does not need. That
cross-check earned its keep: it caught a **missing square root** in our first `spectral_upper`
(`‖G‖ ≤ √‖G²‖_F`, not `‖G²‖_F`), which made `σ` 15× too small and hence `D̂` unsound by `≈3·10^-5`
in the first run of the ledger below. The numbers here are post-fix.

`v0` is dominated by `C_P·R² = 4.38·2.56·10^-4 = 1.12·10^-3`, which is exactly why `ℓ ≈ a`: the
quadratic normal term eats the child radius, `ℓ ≈ √(a² − v0²)`.

**Slack at the boxes the relations actually cover** (1709 boxes, `out/stageb_slack.json`):
`a_Q − D̂(t_B)` has **min `8.51·10^-8`, median `1.25·10^-3`, max `7.15·10^-3`** on `a ≈ 0.011`. So
Stage-B comparisons are decided with `10^-7` margins at the worst box and ≈11 % of the radius
typically: any 80-bit dyadic implementation decides them, no precision escalation anywhere.

### 4.4 Complete base-grid ledger for that parent — and what is missing

Grid (§5.3): `E = √(1+o_P)·R + 10^-7 = 0.0160001`, `w = 0.0038`, `L = ⌈E/w + 0.500001⌉ = 5`,
`n = 11`, **14641 base grid slots**, `3161` of them not outside. These are *slots* (one per integer
multi-index `b`), not relation evaluations: the sweep below computes one exact outside test per slot
and one cheap `t_B² ≤ ℓ²` comparison per surviving slot-edge pair.

| discharge | count | how checked |
|---|---|---|
| outside (`dist(0,B)² > E²`, exact) | **11480** | exact rational, no witness |
| relation-covered (`∃` child with `t_B² ≤ ℓ²`) | **1709** | 66 certified relations, exact |
| **UNRESOLVED** | **1452** | needs evidence the run did not archive |

The run's own summary for this pass is
`parent163 base2386483 inside515243 live17207 split0 … fail0 pair69714/3039760 marks515236`, and
`14641·163 = 2 386 483`, `3161·163 = 515 243` — **exact agreement** with our recomputation of
`(5.20)–(5.22)`. Also `split 0` in `Bmid`, `Bfine` and `C.Bfallback`: **no recorded B pass subdivided**,
so every B discharge is a base-box discharge and the ledger needs no subdivision tree.

Hence the 1452 boxes *were* covered in the run, but not by a direct relation from `P` to an archived
child. The mechanisms that can close them, in increasing cost:

1. **Merge-mediating centres (not archived).** A box solved by snapping produces a centre `Q`; `assign`
   may *merge* it into an existing atlas centre `Z`, growing `r_Z` to `r + ℓ(Z,Q)` (Lemma 5.6). The box
   is then covered by `Z`, but the checker cannot reconstruct `Q`, so either the 36 coordinates of `Q`
   (288 B) or the pair `(r, ℓ)` (72 B) must be emitted per merged box.
2. **Transported-frame relations.** `preload` applies `variants(P, .061, 1, …)` and looks the atlas up
   in transported frames; a child can cover a box in a frame where the identity map does not. `(5.25)`
   guarantees box coordinates are unchanged, so this is still a per-box statement; it needs the parent
   map in the witness (≈14 B).
3. **Subdivision** — not used by any recorded B pass (§4.4 above), so the ledger is flat.

### 4.5 The ledger schema this implies (implementation shape for Q3/H3)

```
ParentLedger :=
  parent: RecordID,  w: float,  tau: float,
  edges:  [ (child: RecordID, map: {row[6], col[6], trans, neg}, ell: float, a: float) ],
  merges: [ (box: int32[k], mediator_center: float[36] | (r: float, ell: float), child: RecordID) ],
  snaps:  [ (box: int32[k], child: RecordID) ]
Check:
  checker recomputes L, n and the outside set (exact), and t_B per box (exact);
  for each edge recomputes (5.5)-(5.8) and verifies  D^(ell) <= a;
  for each box not outside:  assert exists edge with t_B^2 <= ell^2
                            or exists merge/snap record with that box;
  every leftover box is printed as UNRESOLVED with its index, never dropped.
```
Size: ≈60 B per edge (14 B map + 2 floats + id), ≈300 B per merged box. For the fallback:
163 parents × (≈429 edges + ≈105 merge records) ≈ 87 kB. This is the concrete answer to "how the
fallback 163 → 1127 chain can be checked without hiding obligations".

---

## 5. Measured performance (`out/*.json`; VM shared with another swarm, so ranges)

| operation | cost | notes |
|---|---|---|
| `e(2πix)` enclosure | `88 µs` | 26+26-term Taylor at 2^-128 |
| Root record, full R1–R8 | `0.35–0.75 s`, median `0.40 s` | 48 records over `coarse*/mid/fine/fb1` |
| … of which `‖F(P)‖` (36 exps) | `9 ms` | |
| … of which `M` proposal (eigh + exact Dy matmul) | `70 ms` | |
| … of which the (4.15c) residual | `40 ms` | 36×30×12 interval updates |
| Stage-B relation (5.5)–(5.8) + 40-step threshold search | `45 ms` idle / `159 ms` loaded | 66 relations |
| Stage-B box test (outside + `t_B² ≤ ℓ²` over 66 edges) | `193 µs` idle / `889 µs` loaded | `Fraction` arithmetic |
| transport search over all 2,073,600 maps | `2.6 s` idle / `4.8 s` loaded | complete, not heuristic |

Extrapolation from the run's own recorded counts. `base`/`inside` are **grid slot** counts (5.21), and
`pair` is the number of *established* relation edges (`pair`/`pairTry` = established / attempted:
fallback `69714/3039760`, mid `23190828/746841453`, fine `4499828/150522743`). A certificate carries
the edges, so a checker pays the second column, never `pairTry`.

| stage | base grid slots | certified relation edges | prototype (44.5 ms/edge, 193 µs/slot) | fixed-point rewrite — **estimate only** (2 ms, 2 µs) |
|---|---|---|---|---|
| B fallback (163 parents) | `2.39·10^6` | `7.0·10^4` | `1.0 h` | `2.4 min` |
| B mid (3083 parents) | `8.57·10^8` | `2.3·10^7` | `333 h` | `13.4 h` |
| B fine (600 parents) | `5.51·10^8` | `4.5·10^6` | `85 h` | `2.8 h` |
| Root, all ≈3500 records | — | — | `23 min` | `≈1 min` |

The 2 ms / 2 µs column is an **architecture estimate** (factors 20 and 100 over the measured Python
prototype). No fixed-point implementation of either kernel exists in this directory, and nothing in
§2–§4 depends on those numbers.

(Load factor: the same measurements taken while the co-tenant swarm was busy were 3.5–4.6× slower —
`159 ms`/relation, `0.89 ms`/slot — so multiply the prototype column by up to 4.6 on a contended VM.
The judge's own rerun on a contended VM measured 19 s CPU for the 48 Root records, consistent with the
`0.40 s/record` figure above.)

Interpretation, and the design consequence. **Measured:** Root is cheap in the prototype (`≈23 min`
for the whole saved run at `0.4 s/record`), so it can be re-checked in full now. For Stage B the
prototype cost is dominated by the *relation edges*, not by the grid slots, so the implementation
priority is the opposite of what the slot count suggests: a fast exact relation kernel matters more
than a fast slot predicate, and the `mid` pass (`2.3·10^7` edges) is the binding cost. **Estimated,
not measured:** a fixed-point rewrite would bring the total to `≈16 CPU-hours`, a 1–2 day shard that
does not need a Stage-A-style block-outside tree. The gate decision is therefore not "can Stage B be
re-checked" but "is 1–2 days of VM time worth an independently checked Stage B in H3", with the
20×/100× assumptions stated so whoever builds the rewrite can check them.

---

## 6. Explicit unverified items / limitations

1. **Sampling, not census.** Root checks ran on a 48-record stratified sample (k=0, typical k=4,
   smallest radii, all seven files). The exact checks R1–R3, R5–R6 are cheap enough for all ~3500
   records (≈3 min without the interval residual) but that was not run here.
2. **Two complete-Root failures are not resolved by us**: `coarse0#678`, `coarse3#33` fail R8 under
   *both* candidates with our `U`, while their R1–R7 all pass. We report this as "the stored tensor-
   improved `C` is not re-certifiable from `(p,T)` with an independently chosen `U`" — an interface /
   witness mismatch — and give two fixes. We did **not** establish whether the source's own `U` would
   pass (it is not archived), so we make no claim that the stored `C` is wrong.
3. **The Stage-B ledger is complete for one parent only** (`bad10#0`, first fallback parent). The 1452
   unresolved boxes are not certified either way: merged-centre witnesses were not implemented, so we
   cannot say the paper's claim fails — only that the archived data does not re-certify them, with the
   missing witness classes named in §4.4.
4. **Transport maps**: the exhaustive search is complete for the 6 (parent, child) pairs we ran it on.
   For the other 60 cluster children only the identity map was tested, so `1709` covered boxes is a
   **lower bound**; a non-identity map could raise it.
5. **`k = 0` records** (one per file, five in total) pass every check via the `σ = 0`, empty-`T` branch.
   No `k > 4` record exists in the saved data, so `maxK = 10` paths are untested here.
6. **Ties in `nearest_int`**: round-half-even is implemented exactly (matching `nearbyint`); no tie
   occurred in the sampled dephasings. A tie in a certificate-grade record must be recorded explicitly
   (the integer lift is part of the witness).
7. **Range checks** of §5.6 (`C<20`, `n0,froot<10^-6`, `id<10^-4`, `ort,hor<10^-5`, `mnorm<2`, `|p|≤4`,
   `|T|≤1.01`) are enforced by the parser/checker; passing them is not a correctness result.
8. **No claim about the preprint's mathematics.** We verified certificate-side arithmetic on saved
   data. Nothing here says the necessity lemmas hold or that `N(6) = 3` follows; the two `C` findings
   and the Stage-B ledger gap are interface mismatches H2 exists to surface before any "certified"
   sentence is written.

## 7. Concrete asks for the H2 spec

* Freeze `M`'s reconstruction (or serialise `M`); state the factor bound `√(ah·al) ≤ mnorm` explicitly.
* Replace the stored `C` by `max(C₀, C₁(U_cert))` and store `(β, r)` alongside.
* Make `(map, ℓ, a)` the Stage-B edge witness and `(mediator centre | (r,ℓ), child)` the merge witness;
  keep `UNRESOLVED` boxes printed with their indices.
* Put the grid + outside test `(5.20)–(5.22)` inside the checker, not in a comment: it is what
  reproduces the run's `base`/`inside` counters, and it is cheap.
