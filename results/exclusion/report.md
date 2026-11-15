# Stronger certified exclusion inequalities for Stage-A completion cells

Source: *The maximum number of mutually unbiased bases in dimension six*, 24 Sep 2026,
Sections 3.5-3.7, Lemma 3.9, Corollary 3.10, Appendix A.
All cell data is restated self-containedly in [spec.md](spec.md); the paper text with layout
is `.scratch/rt/paper.txt` (Section 3.5 at line 944, (3.29) at 1071-1090).

**Scope, stated up front.** Everything below concerns the inequality (3.29) of the paper as a
*standalone mathematical object*, on cell data that I rebuild from the paper's own definitions
(Sections 3.1-3.6). It does **not** reproduce the authors' computation, does not use their
proposer, and makes no claim about their run. Cells are built from genuine dephased complex
Hadamard matrices (`F_6` and `F_2 (x) F_3`) placed on the actual bin grid of Section 3.7
(`Nu in {64,...,512}`, `h = pi/Nu`). The authors' datasets for the 249,878 retained centres are
in a different (5-bin + seed index + 4 U-bin) encoding and were not decoded here.

## 0. Findings

1. **The direction problem is a convex conic programme, and its optimum is a distance.**
   `B(y)` is the support function of an explicit compact convex body `K` (the *cell body*), so
   `y -> y.c_all - B(y)` is concave and positively homogeneous. With the Euclidean
   normalization the optimal margin is exactly `dist_2(c_all, K)`, attained at the unique
   direction `y* = c_all - Proj_K(c_all)`; the unnormalized margin at `y*` is `||y*||^2`. The set
   of excluding directions is an open convex cone. [Theorem A2, A3]
2. **A provably stronger inequality, for free.** Replacing the paper's separate treatment of
   the two error terms by the reverse-triangle information `|Z_ij| >= ||D_ij|-1|` (which the
   paper already uses as its independent norm test (3.26)) strictly lowers the right-hand side
   of (3.29) for every direction with a positive flat weight. Measured margin gain: **+13.9 per
   cent median, +50 per cent at best** over 32 cells. On the one-parameter family of Section 7,
   however, the gain vanishes exactly at the cells nearest a completion (there `|D| = 1`), so it
   does *not* move the exclusion boundary. [Theorem B1, Section 7]
3. **A second-order certificate cannot pay for itself at these parameters.** Exploiting the
   exact quadratic term is possible, but the linearization remainder `E_r` caps the total
   achievable gain at `(1/2) Y_max E_r^2`, which is `6e-3` to `2.4e-2` at these parameters, while
   the measured curvature gain is `3e-3`, i.e. about 0.5 per cent of a typical margin. The
   binding quantity is `E_r` (a first-order Taylor remainder with an `h->0` floor of ~0.16), not
   the direction. Any further strengthening must attack `E_r`. [Theorem C1, Proposition C2]
4. **Refinement has a strictly positive floor, and the floor decides.** `E_r -> sqrt(e_off^2+p^2)`
   and `z -> sqrt((...)^2+p^2)` have `h`-independent limits, so the right-hand side of (3.29) does
   not go to zero. Measured on the completion's own cell the margin converges geometrically, by
   `+0.172, +0.064, +0.027` for `Nu = 64,128,256,512` per level step, to a limit near `-0.48`:
   **that cell is excluded at no level**, and the same holds for every cell within a parameter
   distance of about `t_inf ~ 0.05` cycles in `alpha` of the completion's unitary. Those cells
   are not a subdivision problem; they are what the phase-ball coverage of Section 4 is for.
5. **Exact optimisation beats the described heuristic only slightly.** On the benchmark the
   convex optimum exceeds a faithful re-implementation of the paper's own proposer style
   (regularised normal equations plus weight updates, as in `coverSeeds::supdual` of the
   supplied `covout.cpp`) by **9.3 to 17.7 per cent** in median margin. The interesting gain is
   structural (Theorem A2), and the exact optimizer's real value is that it makes the margin a
   *measured*, not a guessed, quantity.

## 1. Independent implementation

`src/exclusion/cell.py` rebuilds every constant of Sections 3.1-3.4 (`E_0,B_0,C_0,G_B,G_C,K_B,K_C,
m_B,m_C,m,A_0,A_*,q,p,z,L,e_off,E_r`), the comparison block `D` (3.15), the linear map `J(s,theta)`
(3.23), the constant `c_all` and the matrix `J_all` (3.28), and the right-hand side `B(y)` of (3.29).

**Validation.** `src/exclusion/test_cell.py` checks the two things that can silently go wrong:

* the unitary parametrisation (3.12) and the four angular derivatives, against finite
  differences (`u_params`, `dU_theta`): agreement to `2e-6` with step `1e-6`;
* the 20 rows of `J_all`, against finite differences of the *literal* orthogonal pieces
  (3.16), (3.17), (3.18) — the seed varied through `E',B',C'` and `D'` varied only through the
  unitary family, which is exactly the sense in which (3.23) is a linear comparison rather than
  a total derivative. Agreement: `max|J_fd - J_all| <= 1.3e-6` over all 20 x 13 entries for both
  seeds and two midpoints.

The duality identity of Theorem A2 is checked numerically as well: at `Nu = 64,512` the margin
of the returned direction equals the dual value to `2e-16` (zero duality gap), and
`y*.c_all - B(y*) = ||y*||^2` to the same accuracy.

`src/exclusion/verify.py` is the independent verifier. It re-evaluates `y.c_all > B(y)` in
60-digit arithmetic from the stored cell data, compares against a 40-digit evaluation to bound
its own rounding, and adds an explicit bound on the *data's* double-precision uncertainty
(`~1e-16` relative on every scalar of `c_all`, `J_all`, `|D|`, propagated through the
Lipschitz constants of `B`). Its verdicts are `CERTIFIED` only when the margin exceeds both by
a factor of ten. Two certificates are certified — see Section 7.

## 2. Result A: the structure of the direction problem

Write `P_D, P_X, P_Y` for the coordinate projections of `R^20` onto the flat block (16 entries),
the two seed-sum pairs, and `W = diag(|D_ij|)`, so `||D o y_D||_F = ||W y_D||_2`. Write
`J_s = J_all[:, :9]`, `J_theta = J_all[:, 9:]`, `N = B` for the right-hand side of (3.29).

**Lemma A1 (cell body).** Each of the five terms of `B` is the support function of a compact
convex set containing the origin, and

```
B(y) = sigma_K(y),   K = J_s(B_Rs) + J_theta([-h,h]^4) + P_D^T W(B_{E_r})
                        + conv{0, -(z^2/2) P_D^T e_k : k=1..16} + P_X^T(B_{Rs^2/2}) + P_Y^T(B_{Rs^2/2}).
```

*Proof.* Norm duality for each term: `R_s||J_s^T y|| = sup_{||w||<=R_s} w^T J_s^T y`, and `J_s w` runs
over `J_s(B_Rs)`; similarly `h||J_theta^T y||_1 = sup_{||u||_infty<=h} u^T J_theta^T y`; the third and
the last two are the same computation with `W` and the coordinate embeddings. For the fourth,
`max(0,max_k(-y_k)) = max{ sum_k alpha_k(-y_k) : alpha >= 0, sum alpha_k <= 1 }`, a linear programme
over the simplex whose optimum puts all mass on the most negative coordinate.
Support functions add under Minkowski sums. QED

Consequently `B` is a seminorm (nonnegative, positively homogeneous, subadditive), `K` is
compact convex with `0 in K`, and `c_all in K` iff `y.c_all <= B(y)` for every `y` (support
function domination plus strict separation of a compact convex set from a point).

**Theorem A2 (the optimum is a distance, and the direction is unique).** For every cell,

```
sup_{||y||_2 <= 1} ( y.c_all - B(y) )  =  dist_2(c_all, K)  =:  delta.
```

The supremum is attained at `y* = c_all - Proj_K(c_all)`; if `y* != 0` then
`y*/||y*||` is *the unique* maximiser, its margin equals `delta`, and `y*` satisfies the exact
identity `y*.c_all - B(y*) = ||y*||_2^2`.

*Proof.* By Lemma A1, `B(y) = max_{v in K} v.y`. Hence

```
sup_{||y||<=1} (y.c_all - B(y)) = sup_{||y||<=1} min_{v in K} (c_all - v).y .
```

The function is affine in each variable and both sets are compact and convex, so Sion's minimax
theorem gives

```
sup_{||y||<=1} min_{v in K} (c_all - v).y = min_{v in K} sup_{||y||<=1} (c_all - v).y = min_{v in K} ||c_all - v||_2 .
```

Let `v* = Proj_K(c_all)`, `y* = c_all - v*`. The projection is unique (closed convex set), and
the projection inequality `(c_all - v*).(v - v*) <= 0` for all `v in K` says exactly
`v.y* <= v*.y*`, i.e. `B(y*) = v*.y*`. Therefore

```
y*.c_all - B(y*) = y*.(v* + y*) - v*.y* = ||y*||^2 ,
```

so the margin of the unit vector `y*/||y*||` is `||y*|| = delta`, and it is a maximiser. If `ŷ` is
another maximiser then `(c_all - v).ŷ` is maximised at `v*` and `||ŷ||=1` forces `ŷ = y*/||y*||`
by the equality case of Cauchy-Schwarz. QED

**Theorem A3 (the excluding directions form an open convex cone).**
`E = {y : y.c_all > B(y)}` is a convex cone, open, positively homogeneous, and `E != empty`
iff `c_all not in K`. Every convex combination of two certified directions with positive
coefficients is again a certified direction, and any `y in E` may be rescaled at will — so a
verifier need only check one representative per ray.

*Proof.* `y.c_all - B(y)` is concave and positively homogeneous; the strict superlevel set of a
concave function is convex, and homogeneity gives the cone property. Emptiness is Theorem A2's
identity with `delta = 0`. QED

**Why this matters for the paper.** The paper's `trial::pass` proposes directions heuristically
and its verifier only checks the final inequality, which is sound. Theorem A2 says the
proposer may be replaced by a *certified* one that attains the global optimum: the primal
`sup_{||y||<=1}` is a second-order-cone programme (`||.||_2`, `||.||_1`, `||.||_2`, a simplex
support and two more Euclidean norms), and its dual is the projection above. The duality gap is
an exact optimality certificate: at any candidate `y`, `gap = B(y)*... ` — precisely,
`y.c_all - B(y) <= delta` always, with equality iff `y` is optimal, so evaluating the margin of
the returned direction *is* the certificate that it is optimal.

Note the normalization dependence: under the gauge normalization `B(y) <= 1` the optimal set can
be a whole face of the polar (this happens when the active constraints include the `l_1`-block or
the simplex block); under the Euclidean normalization above the optimizer is always unique. Both
statements are true and they concern different points.

## 3. Result B: a strictly stronger inequality at no cost

**Theorem B1 (merged certificate).** For every `y in R^20` and every feasible completion in the
cell,

```
y.c_all  <=  B(y)  -  (1/2) sum_{ij} (y_D,ij)_+ (|D_ij| - 1)^2 .                            (B)
```

The subtracted term is nonnegative, so the right-hand side is at most that of (3.29), with
strict decrease whenever some `y_D,ij > 0` and `|D_ij| != 1`.

*Proof.* Repeat the proof of Lemma 3.9 with the exact flatness identity. The exact equations are
`c_ij + Jbar_ij + Re(conj(D_ij) R_ij) + |Z_ij|^2/2 = 0` with `Z = J(s,theta) + R`, and
`|D_ij + Z_ij| = |D'_ij| = 1` for every feasible completion. Weight the sixteen flat equations by
`y_D`, the two complex seed-sum equations by `y_X, y_Y`, add, and move everything except
`y.c_all` to the right:

```
y.c_all = - g.u - (1/2) sum_ij y_D,ij |Z_ij|^2 - <y_D, Re(conj(D) o R)> - <rho> .
```

Bound the linear term by `R_s||g_s|| + h||g_theta||_1` (the exact maximum over the seed ball and
the angle box), the `R`-term by `E_r||D o y_D||_F` (Cauchy-Schwarz and `||R||_F <= E_r`), and the
seed remainders by `(1/2)R_s^2(||y_X||+||y_Y||)` as in (3.27). The only new step is the quadratic
term, where the paper uses `|Z_ij|^2 >= 0` for positive weights and `|Z_ij|^2 <= z^2` for negative
ones. Keep the first but sharpen it: the reverse triangle inequality applied to
`|D_ij| = |D'_ij - Z_ij|` gives `|Z_ij| >= |1 - |D_ij||`, hence for `y_D,ij >= 0`

```
-(1/2) y_D,ij |Z_ij|^2  <=  -(1/2) y_D,ij (|D_ij| - 1)^2 ,
```

while for `y_D,ij < 0` the paper's `(1/2) z^2 max(0, max_ij(-y_D,ij))` bound is kept unchanged.
Summing gives (B). QED

**Remarks.**
* The gain is the *weighted* form of the paper's own norm test (3.26): it is
  `(1/2) sum (y_D)_+ (|D_ij|-1)^2`, and (3.26) is the unweighted `sum (|D_ij|-1)^2 <= z^2`. So (B)
  folds (3.26) into the directional test; a cell can be excluded by (B) while neither (3.26) nor
  (3.29) alone excludes it, because the direction may concentrate its weight on the entries where
  the centre is far from the unit circle.
* The gain vanishes exactly on the cells that matter most for coverage — those containing a
  feasible completion have `|D_ij|` close to 1 — but it is largest on the cells that are
  hardest to exclude at coarse levels, where `D` is far from flat.

Measured: see Section 7, column `mu_merged`.

## 4. Result C: what a second-order certificate can and cannot buy

The exact quadratic term is `-(1/2) sum_ij y_D,ij |J_ij(u) + R_ij|^2`. Keeping it (instead of
dropping it) turns the direction problem into

```
max over (u,R) in K x {||R||_F <= E_r} of  -g.u - (1/2) sum_ij y_D,ij |J_ij(u)+R_ij|^2 - <y_D,Re(conj(D) o R)> ,
```

a convex programme when `y_D >= 0`, and its value is an upper bound for `y.c_all` that is
strictly below `B(y)` — this is the natural "second-order" strengthening. It is worth very
little at the paper's parameters, and one can say exactly why.

**Theorem C1 (cap on the second-order gain).** For `y_D >= 0`, `q(u) = sum_ij y_D,ij |J_ij(u)|^2`
and `c = sqrt(Y_max) E_r` with `Y_max = max_ij y_D,ij`,

```
- (1/2) sum_ij y_D,ij |J_ij(u)+R_ij|^2  <=  (1/2) c^2      for every (u,R) in K x {||R||_F <= E_r}.
```

*Proof.* `||sqrt(y_D) o R||_F <= sqrt(Y_max)||R||_F <= c`, so
`sum y_D,ij|J_ij+R_ij|^2 >= (sqrt(q(u)) - c)^2`, and `-(1/2)(sqrt(q)-c)^2 <= (1/2)c^2`. QED

**Corollary C2.** The total improvement available from the quadratic term, relative to the
paper's choice of dropping it, is at most `(1/2) Y_max E_r^2`. On the benchmark `Y_max <= 0.57`
(the optimal directions put most weight on a few flat entries) and `E_r <= 0.29`, giving a cap of
`2.4e-2` (`6e-3` at `E_r = 0.156`), while the measured gain of the optimal curvature term is
`3e-3`. The quadratic route is therefore closed at these parameters:
`E_r` is never small enough relative to `||J(u)||_F`. Since `E_r` is dominated by the `h`-independent
part `e_off = R_s^2(L+A_0+1)/(2m) + z R_s/m ~ 0.16`, no amount of subdivision helps. A stronger
second-order certificate would need a *tighter linearization remainder* (a second-order seed
expansion), not a cleverer direction.

## 5. Scaling in the subdivision level

**Proposition A4 (monotonicity).** `K` is monotone increasing in `(R_s, h, E_r, z)`, so `B` and
hence the margin are monotone decreasing in each; exclusion is easier for smaller cells. In
particular the margin is monotone increasing in `Nu` at fixed cell centre (only `h`, `z`, `E_r`
change).

**The floor.** `E_r = sqrt(e_off^2 + ((sqrt6*42/2)h^2 + p)^2)` and
`z = sqrt((R_s(sqrt6+A_*)/m)^2 + (6h+p)^2)` tend to `h`-independent limits as `h -> 0`, so
`B(y) >= R_s||g_s|| + e_off||D o y_D||_F + (z_0^2/2) max(0,max(-y_D)) + (1/2)R_s^2(...)` for all
`Nu`. A cell whose limit margin is negative is not excluded at *any* level: subdivision cannot
replace the phase-ball coverage of Section 4. Measured (Section 7): on the completion's own cell
the margin is `-0.719, -0.547, -0.483, -0.456` at `Nu = 64,128,256,512`, so the gains per level
step are `0.172, 0.064, 0.027` and the limit is near `-0.48`. Exclusion of that cell is not a
question of depth.

## 6. Benchmark protocol

* **Cells.** `Nu in {64,128,256,512}` (the levels at which Section 3.7 uses the directional
  test; at `Nu = 16` the paper itself uses only the norm test, and indeed (3.29) is vacuous
  there — I verified that `c_all in K` at `Nu = 16`). Midpoints are the bin centres of the
  parametrisation of Lemma 3.3 in the counts `(Nu/2, Nu/4, Nu, Nu)`; `h = pi/Nu`.
* **Seeds.** `F_6` and `F_2 (x) F_3`, dephased; the nine seed entries are read at the positions
  (7,8,9,10,11,13,19,25,31) of the row-major 6x6 phase array, in the order
  `(a,b0..b3,c0..c3)`. Both are genuine complex Hadamard matrices, so the cells are genuine
  Stage-A cells; they are *not* the paper's 22,829 retained centres.
* **Directions.** `opt` = the exact optimum of Theorem A2 (dual projection, FISTA, gap
  `<= 1e-15`); `heur` = the analogue of the paper's proposer described in `analyze.heuristic`
  (regularised normal equations with weight updates `1/max(||A_k^T y||, .03)`, mirroring
  `coverSeeds::supdual` in the supplied `covout.cpp`, lines 40-72).
* **Metrics.** the scale-free margin `mu(y) = y.c_all - B(y)` at `||y||_2 = 1`; the merged margin
  `mu_merged = mu + (1/2)sum (y_D)_+ (|D|-1)^2`; the fraction of cells with `mu > 0`; the
  distance-to-completion boundary.

## 7. Measurements

| Nu | cells | median mu (opt) | median mu (merged) | median mu (heuristic) | merged gain | opt vs heur | excluded |
|---|---|---|---|---|---|---|---|
| 64 | 8 | 0.952 | 1.095 | 0.879 | +17.5% | +9.3% | 8/8 |
| 128 | 8 | 0.762 | 0.843 | 0.702 | +11.5% | +10.8% | 8/8 |
| 256 | 8 | 0.734 | 0.827 | 0.632 | +13.4% | +14.7% | 8/8 |
| 512 | 8 | 1.115 | 1.296 | 0.955 | +13.8% | +17.7% | 8/8 |

Median merged gain over all 32 cells: **13.8%** (max 50.7%). Median optimum-over-heuristic: **14.4%**. Margins span 0.098 to 1.801; `E_r` in 0.156..0.289, `z` in 0.523..0.711. All 32 cells are excluded by both methods, so this table measures margin strength, not reach.

| seed | Nu | mu at t=0 (cell holding the completion) | t* (opt) | t* (merged) | mu at t=0.10 |
|---|---|---|---|---|---|
| F6 | 64 | -0.719 | 0.075 | 0.075 | +0.186 |
| F6 | 128 | -0.547 | 0.060 | 0.060 | +0.329 |
| F6 | 256 | -0.483 | 0.050 | 0.050 | +0.384 |
| F6 | 512 | -0.456 | 0.050 | 0.050 | +0.408 |
| F2xF3 | 64 | -0.604 | none up to 0.10 | none | -0.115 |
| F2xF3 | 128 | -0.508 | 0.085 | 0.085 | +0.079 |
| F2xF3 | 256 | -0.478 | 0.075 | 0.075 | +0.128 |
| F2xF3 | 512 | -0.466 | 0.070 | 0.070 | +0.148 |

`t` is a displacement of the `alpha` parameter only, in cycles, from the completion's own unitary `V* = polar(K_C^* D' K_B)`. `mu` is the best margin of Theorem A2 over that cell's centre. The cell at `t = 0` contains the completion and must have `mu < 0`; it does, at every level. The crossing `t*` is the exclusion boundary: cells closer to the completion than `t*` are not excluded by (3.29) at that level.

| seed | direction | certified margin (60 digits) | 60-vs-40-digit gap | data-uncertainty bound | verdict |
|---|---|---|---|---|---|
| F6 | Nu=64 optimal | 1.124493428105… | 1e-41 | 1e-14 | **CERTIFIED** |
| F6 | Nu=64 heuristic | 1.011631767172… | 8e-42 | 1e-14 | **CERTIFIED** |
| F2xF3 | Nu=512 optimal | 0.239981650417… | 3e-42 | 6e-15 | **CERTIFIED** |
| F2xF3 | Nu=512 heuristic | 0.210872321034… | 3e-42 | 6e-15 | **CERTIFIED** |

## 8. What this does and does not say about the dimension-six proof

**Does.**
* (3.29) is a first-order (support-function) certificate whose best possible strength is a
  *computable* convex quantity, `dist_2(c_all, K)`, and whose optimizer is unique. Any
  implementation can therefore be measured against an exact benchmark instead of against
  another heuristic.
* The certificate can be strengthened for free by (B), and the strengthening is largest exactly
  where the paper's recursion works hardest — at coarse levels, where `D` is far from flat.
* The second-order route is quantitatively closed by Theorem C1: at `E_r ~ 0.2` it can buy at
  most `~1e-2` of margin. This is a *negative* result with a proof, and it redirects the effort
  to `E_r`.
* Refinement of the angle box stops improving the certificate by `Nu ~ 128`, so the
  "number of subdivisions" is governed by the floor, not by `h`.

**Does not.**
* It does not show that the paper's run used a suboptimal direction, nor that any specific cell
  would have been excluded earlier. The cells here are reconstructions, not the run's cells.
* It does not shorten the proof. Whether (B) or the exact optimizer shorten the actual recursion
  depends on how many cells are decided by the directional test versus by phase-ball coverage,
  which I cannot measure without the run's data in decoded form.
* It says nothing about the correctness of the paper's Appendix A arithmetic, or about the
  sources of `E_r`, `z`, `p`, which I take from the paper as stated. If `E_r` is improvable (and
  the structure suggests it is), everything in Section 4 improves with it.

## 9. Reproduction

```
python3 src/exclusion/test_cell.py     # validates J_all against (3.16)-(3.18); ~2 s
python3 src/exclusion/run_all.py       # all measurements; writes results/exclusion/measurements.json
python3 src/exclusion/bench.py         # the random-cell table alone
```
`verify.py` is imported by `run_all.py` and can be called directly:
`certify(cell, y)` returns the 60-digit margin, its own rounding gap, and the data-uncertainty
bound.

## 10. Open items

1. Decode the run's own centre file (`centers.txt`: 5 bin coordinates, a seed index, 4 U-bin
   coordinates) into the nine seed phases via `seed.cpp`, and re-run the benchmark on it. That
   would turn the benchmark into a statement about the paper's computation.
2. Improve `E_r` by a second-order seed expansion; Theorem C1 says this is where the remaining
   strength is.
3. Decide whether the merged certificate (B) changes any level decision in the recursion; that
   needs the per-cell record of which test decided each cell, which the paper's Table 1 does not
   break down.
