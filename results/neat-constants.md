# Choosing constants that make the seed computation exact

*A four-page typeset version of this note, laid out as a drop-in replacement for the paper's
scattered constant justifications, is `mub-constants.pdf` in the project root.*

**Question.** The preprint fixes `N = 112`, `w = 1/112`, `R = .032`, `r_s = .0320001`, and a
comparison radius `RN2 = (fl(.032·112))² − 10⁻⁴`. Can other constants be chosen so that the finite
computation ("the bash") is *neater* — i.e. so that the floating-point justification shrinks instead
of being patched?

**Answer.** Yes, and the choice is almost forced: **`N = 128`, `w = 2⁻⁷`, `R = 2⁻⁵ = 1/32`,
`r_s = R`, `RN2 = (NR)² = 16`.** With these, every seed-side quantity the proof compares is an exact
binary64 number: the bin midpoints, the grid displacements, `NR`, `(NR)²`, and the comparison
threshold. The `+10⁻⁷` enlargement of the seed ball, the `10⁻¹⁴` phase-conversion error and the
"`pow(x,2)` must be lowered to a multiplication" code-generation premise all leave the proof.
The price is 1.76× the tested pairs and a 29 % dearer cover, offset almost exactly by 8 % fewer
retained centres: measured on the authors' own code, the run is cost-neutral (§6).

---

## 1. Why this is forced, not chosen

Three of the paper's own premises pin the range:

| # | premise | where | consequence |
|---|---|---|---|
| P1 | bin differences are stored in `int8_t`, and δ = 0 is claimed to be in range | §7.3 | `N − 1 ≤ 127`, i.e. **N ≤ 128** |
| P2 | the A-field bound `Rs = 2πR < .203` | A.13 | **R < .032309** |
| P3 | the *cheap* reuse test (2.18) can only fire if the whole bin fits: `R ≥ √17/(2N)` | Lemma 2.9, eq. (2.18) | **N ≥ 66** for the cheap path; below it only the dual bound (2.19) can merge |

P3 needs care, because three natural versions of it are wrong in different directions. Two distinct
midpoints differ by an integer vector `k ≠ 0`; the ball of radius `R` about one contains the whole
box of the other only if `R ≥ max_{|h|≤½} ‖k+h‖/N`, and the minimum over `k ≠ 0` is at `k = e₁`:

  `√((3/2)² + 8·(½)²)/N = √17/(2N) = 2.0616/N`.

That is the exact reach of the cheap test (2.18), whose bound `‖k‖² + 9/4 + Σ|kⱼ|` is attained at
the corner. The triangle-inequality form `1/N + 3/(2N) = 2.5/N` (used in an earlier audit as "N ≥ 79")
is a strict overestimate; so is any use of the *infimum* rather than the supremum. But the dual
bound (2.19) does not need to cover the whole box — it certifies the *feasible portion* of a bin,
which is a 5-dimensional slice of the 9-dimensional box, so (2.19) can merge bins below this floor.
Hence P3 bounds only the cheap path; it does not prove that reuse dies at small `N`.

Now impose exactness. Midpoints are `(b + ½)/N = (2b+1)/(2N)`, exactly representable in binary64
**iff `2N` is a power of two**, i.e. iff `N` is. With P1 (`N ≤ 128`) and the circumradius bound
(`N ≥ 47`) the only powers of two are **64 and 128**. N = 64 is not excluded by an inequality; it is
excluded by cost. At `N = 64`, `R ≤ .03231` gives an effective separation
`δ = R − 3/(2N) ≤ .0087`, half of the bin spacing `1/64 = .0156`, so no bin's own midpoint is ever
within the cheap test's reach and the whole merging load falls on the dual bound; if it fails there,
every checked pair becomes a Stage-A seed at ~8 ms each. **N = 128** is the choice that works: `NR = 4`, so
`(NR)² = 16` and the comparison radius is an exact integer, and `δ = 5/256` is 2.5 bin spacings.

For `R`, exactness only needs `R` dyadic: in `[2.0616/128, .032309]` the dyadic values are `m/256`
for `m = 5,…,8`. `R = 1/32 = 8/256` is the largest ball (fewest centres) and the only one giving
`NR = 4`, a power of two. 112 is not selectable at all (midpoints with denominator 224), 96 neither
(192).

One caveat on `R`: `1/32` is not the largest *dyadic* admissible. `R = 33/1024 = .032227` is dyadic,
keeps `NR = 4.125` and `(NR)² = 17.015625` exact, and would (on a packing model) retain about 16 %
fewer centres — but it leaves `Rs = 2πR = .202485` only 0.25 % below `.203` instead of 3.3 %. That is
precisely the near-tight constant this exercise is trying to remove, so `1/32` is the right trade;
the alternative should be stated, not hidden.

## 2. The constant sheet

| quantity | paper | dyadic | comment |
|---|---|---|---|
| bins per axis `N` | 112 | **128** | largest allowed by P1, and the only power of two that reuses |
| bin width `w` | `1/112` (stored ≈) | **`2⁻⁷` = 1/128** | stored value exact |
| cover radius `R` | .032 | **`2⁻⁵` = 1/32** | `NR = 4` exact |
| enlarged seed radius `r_s` | .0320001 | **`1/32`** | no enlargement needed |
| comparison radius `RN2` | `(fl(.032·112))² − 10⁻⁴` = 12.844956 | **`16`** | exact; no slack needed (§4) |
| bin circumradius `3/(2N)` | 3/224 ≈ .013393 | **3/256** = .011719 | |
| effective separation `δ = R − 3/(2N)` | .018607 | **5/256** = .019531 | larger, so fewer centres |
| `Rs = 2πR` | .201062 | **π/16** = .196350 | 3.4 % below .203 instead of 0.94 % |

## 3. Every pinning inequality at both points

| inequality | paper | slack | dyadic | slack |
|---|---|---|---|---|
| `3/(2N) ≤ R` (bin fits the ball) | .013393 ≤ .032 | 2.39× | .011719 ≤ .03125 | **2.67×** |
| `R < .203/(2π)` (A.13 field bound) | .032 < .032309 | 0.96 % | .03125 < .032309 | **3.3 %** |
| `R ≥ √17/(2N)` (reuse can fire) | .032 ≥ .018407 | 1.74× | .03125 ≥ .016106 | 1.94× |
| `N − 1 ≤ 127` (`int8_t`) | 111 ≤ 127 | 16 | **127 ≤ 127** | **0** |
| `C(N+4,5) < 2³¹` (32-bit count) | 1.604·10⁸ | 13.4× | 3.093·10⁸ | 6.9× |
| `NR` exact in binary64 | 448/125, no | — | **4, yes** | — |
| `(NR)²` exact | 12.844956, no | — | **16, yes** | — |
| slack subtracted from `(NR)²` | `10⁻⁴` (to cover its own rounding) | — | **0** | the rounding is now zero |
| midpoint `(2b+1)/(2N)` exact | no (÷224) | — | **yes (÷256)** | — |

Two slacks get worse and they are worth naming: the `int8_t` bound is now met with **zero** margin
(N = 128 is the last admissible value), and the 32-bit tuple count halves its margin. The first is a
*soundness* margin, not a cost one: `covout` stores `A.b_j − p.b_j` in an `int8_t`, and a wrapped
difference would understate `s` and could certify a coverage that does not hold. So `N ≤ 128` is an
invariant with a type-theoretic reason, `N = 128` is the last value at which the cover means
anything, and any finer cover must widen the storage type first.

**A spot check on the seed that must never be rejected.** The exact Fourier matrix
`e(ij/6)` is the seed the whole computation has to keep. At `N = 128` its X bins are
`(21,42,64,85,106)` with `s = 2`, its Y bins `(64,21,42,85,106)`; it passes the orientation filter
(`21 ≤ 106−85+1 = 22`, by 1), both gap filters (`g = .171875` against `.179688` and `.156250`), the
shared-interval test, and `sumok` in all six directions. Its thinnest `sumok` margin is
`3.10·10⁻⁵` at `N = 128` (against `4.19·10⁻⁵` at `N = 112`; the test tightens because `w` shrinks),
still six orders above the `10⁻⁸` additions. And its shared displacement is exactly `h_s = −½`:
`x_s = ½` and `u_s = ½ + 1/(2N)`, so the critical seed sits on the closed boundary of `[−½,½]⁹` at
*every* `N`. Every use of that box — (2.12), (2.17), (2.18), the initial interval of `extend` — must
stay inclusive; that is the one place where "shrinking by ε" while re-parameterising would silently
lose the cover.

## 4. What leaves the proof

Deletions (with the line numbers of the text extraction `.scratch/mub6.txt`):

1. **The `+10⁻⁷` enlargement.** `r_s = .0320001` occurs in five places (lines 607, 628, 666, 2780,
   3231) and in `atlas.cpp:221`. All become `r_s = 1/32`.
2. **A.3's closing paragraph** (line 3231): "the nine division-rounded seed phases differ from their
   rational midpoints in norm by less than 10⁻¹⁴, which is absorbed when the A seed radius is
   increased to .0320001." The division is exact; the paragraph goes.
3. **A.3's `RN2` paragraph** (lines 3222–3230) and the code-generation clause of §7.1 (lines
   2764–2772). That clause exists because `RN2 = pow(R*n, 2) − 1e-4` has to be a *lower* bound for
   `(RN)²`, and at 112 its operands are inexact — so the paper inspects the saved disassembly to pin
   the instruction sequence, and re-checks it on every new build. At `N = 128, R = 1/32` the argument
   `R*n` is exactly `4`, so `pow(4,2) = 16` both under a correctly rounded `pow` and under the
   multiply lowering: the clause becomes one sentence about an exact integer. That is not a
   cosmetic point: a rebuild of `covout.cpp` with this VM's g++ 16.2 and the paper's own flags emits
   two `call pow@plt`, so **the paper's §7.1 condition is not satisfied by a rebuild here** — the
   recorded run depends on a codegen choice of gcc 13.3. At (128, 1/32) the condition is vacuous.
   (The second `pow`, in `T`, has a non-exact argument, but `T` only decides which previous centres
   to *try* — a wrong `T` cannot certify anything.)

   The `−10⁻⁴` can be deleted rather than replaced, and this is worth spelling out because it is the
   one place where removing a margin is safe. The threshold's `10⁻⁴` covered the *threshold's own*
   computation error (`< 10⁻¹²` at 112); at 128 that error is zero, so `RN2 = (NR)² = 16`. The two
   tests that use it are still conservative: the cheap test evaluates `s + a + 9/4`, which is exactly
   the supremum of `‖k+h‖²` over the box (all integers plus `9/4`), and the dual test evaluates
   `s + 9/4 + supdual`, where `supdual` already carries a `+0.01` addition over a bound accurate to
   `10⁻⁴`, so it exceeds `2k·h` by about `0.009` — three orders above the one binary64 rounding of
   the sum (`≤ 1.8·10⁻¹⁵`). Hence `computed < 16` implies `‖k+h‖² < 16` at both branches. A slack
   of `2⁻¹⁴` is harmless but unnecessary; the neater constant is no constant.

   With the threshold exact, the whole seed-side arithmetic reduces to one integer comparison. The
   cheap test is `s + a + 9/4 < 16` with `s = ‖k_X‖²` and `a = ‖k_Y‖₁` non-negative integers, i.e.

     **`s + a ≤ 13`**,  with no floating point in the decision at all,

   which is the one line a referee can check by hand and the reason the choice among `16`,
   `16 − 10⁻⁴` and `16 − 2⁻¹⁴` is cosmetic: all three give the same cut, because the left side is
   quantised to integers plus `9/4`.
4. **A.3's opening** (line 3168): "Here n = 112 and the stored w approximates 1/n" becomes "n = 128
   and w = 1/128 exactly; the stored reciprocal is exact", and the 10⁻¹⁴ gap-comparison bound becomes
   zero: with `w = 2⁻⁷` the thresholds `1 − (e−1)/N` are exact, and the only inexact ingredient left
   is the one-sided `+10⁻⁸`, which can only keep extra tuples.

What does **not** leave: the ~2·10⁻¹⁴ error of the trigonometric evaluation (`expair`, §A.2) and the
`sumok`/`extend`/`supdual` margins. Those are about the polynomial evaluation of `e(x)` and are
independent of `N`; they keep their form with `N = 128` substituted.

## 5. Edits to the argument itself

The symbolic lemmas (2.4–2.9) are stated for general `N` with `w = 1/N` and carry over verbatim.
Only the numbers move:

| place | now | becomes |
|---|---|---|
| §2.2 (line 413) | "Set N = 112 and w = 1/N" | "Set N = 128 and w = 1/N = 2⁻⁷" |
| §2.4 (line 545) | "3/(2N) < 0.032" | "3/(2N) = 3/256 < 1/32" |
| §2.4 (line 586) | "Set R = 0.032" | "Set R = 2⁻⁵ = 1/32" |
| Prop. 2.10 (line 607) | "radius 0.0320001 is sufficient" | "radius 1/32 is exact" |
| Prop. 2.10 proof (line 628) | "Section A bounds … 10⁻¹⁴ … enlarged radius" | "each midpoint is exact, so no enlargement" |
| §3.1 (line 666) | `rs = .0320001` | `rs = 1/32` |
| §7.2 (line 2780) | "seed radius .0320001" | "seed radius .03125" |
| §7.3 (line 2850) | "differences lie in [−111,111]" | "[−127,127]" |
| A.3 (line 3168) | "n = 112 … w approximates 1/n" | "n = 128 … w = 1/128" |
| A.3 (line 3222) | `RN2 = fl((fl(.032·112))²) − .0001` | `RN2 = (NR)² = 16` (no subtraction) |
| A.3 (line 3188) | "multiply the sharpened residual bound by 112 … residual below 112" | "… by 128 … below 128" |
| A.3 (A.11) | `3.3·10⁻¹¹, 3·10⁻¹¹, 2.4·10⁻⁶ < 2.5·10⁻⁶` | `3.8·10⁻¹¹, 3.5·10⁻¹¹, 2.8·10⁻⁶ < 2.9·10⁻⁶` |
| §7.3 (line 2841) | `C(115,4) = 6,913,340` tails per shared bin | `C(131,4) = 11,716,640` |
| `covout.cpp:138,140` | `build(112); run(S,.032,2)` | `build(128); run(S,1./32,2)` |
| `atlas.cpp:175,221` | `n!=112`; `r=.0320001` | `n!=128`; `r=.03125` |

`Newly inserted midpoint needs radius only 1.5/112 < .032` becomes `1.5/128 = .0117 < .03125`.

Three arithmetic margins **grow**, because they carry a factor `N`: the `extend` rows
`|Δv|`, `|Δa|`, `|Δr|` and the `supdual` right-hand-side error all scale as `128/112 = 1.143`.
The worst is the signed-term input error, `2.4·10⁻⁶ → 2.8·10⁻⁶` against a `10⁻²` addition
(`< 2.5·10⁻⁶ → < 2.9·10⁻⁶` in the text), still four orders of magnitude from binding.

## 6. Cost — measured, not modelled

A note on one figure before the table: the recorded run's `151,744,086` is the number of **(X,Y)
pairs** that reach the coverage test, not the number of X tuples. `covrun`'s own log prints
`xs22829` and `checked151744086`, and the paper's Table 1 quotes the latter. An earlier audit read
it as an X-tuple count and called it inconsistent with the `85,349,292` upper bound on X tuples;
that is a misreading — the two numbers count different things and are consistent.

I rebuilt the authors' cover (`seed.cpp` + `covout.cpp`, the Apache-2.0 sources at
`.scratch/gh/upstream/`) with `N = 128`, `R = 1/32` and ran it to completion on this machine. Both
runs are the authors' own code; only three constants changed.

| | paper (112, .032) | dyadic (128, 1/32) | ratio |
|---|---|---|---|
| X tuples surviving the filters (`xs`) | 22,829 | 32,018 | 1.40 |
| pairs tested (`checked`) | 151,744,086 | 267,628,436 | 1.76 |
| **retained centres** | **249,878** | **229,979** | **0.92** |
| cover CPU time | 402 s | 517 s | 1.29 |
| cover wall time here | — | 1,876 s (27 % CPU: the VM carried a load of 15–17) | — |
| bucket visits | 2.977·10¹⁰ | 3.217·10¹⁰ | 1.08 |
| cheap-path certifications | 4.56·10⁷ | 7.34·10⁷ | 1.61 |
| dual-path evaluations | 3.134·10⁹ | 3.540·10⁹ | 1.13 |
| enumeration `C(N+4,5)` | 160,389,488 | 309,319,296 | 1.93 |
| Y tails `N·C(N+3,4)` | 774,294,080 | 1,499,729,920 | 1.94 |

So the dyadic constants make the bash **exact but not cheaper**: the cover costs 29 % more CPU, the
retained-centre count falls 8 %, and since Stage A's recorded cost is 2,020 s for 249,878 centres
(8.08 ms each), the downstream saving is about 160 s against the cover's extra 115 s. Net ≈ −1 % of
the 4,470 s recorded run — a wash.

The pair count cannot be extrapolated linearly from the run's progress lines, and all three attempts
in this project (mine included) got it wrong. Pairs added per X tuple, from the run's own
checkpoints: at N=128, 3,845 over the first 10,000 X tuples, 7,903 over the second, 11,975 over the
third and 15,062 over the last 2,018; at N=112 the same three-stage growth is 3,749 / 8,238 / 11,266.
The density grows roughly in proportion to the X index, because X tuples are walked lexicographically
and a larger largest bin admits more Y tails, so the total scales like `T²/2` in the index rather
than like `T`. Any two-checkpoint extrapolation undershoots by about 1.3×; a two-parameter linear-density fit on the
first two blocks reproduces both runs' totals to better than 0.6 %.

The pair growth is accounted for rather than fitted: an exact combinatorial count of every filter but
the shared-interval test and the Y-side `sumok` gives `1.451·10¹¹ → 3.440·10¹¹` (2.3706×), and the
residual acceptance rate falls to 0.744 (the Y-side `sumok` accepts 0.775× as often at the centre bin,
times about 0.96 for the interval test). `2.3706 × 0.744 = 1.7637`, the measured ratio. Visits grow
only 8 % because the centres per bucket fall from 11.4 to 7.0 as the bucket grid goes from 28³ to
32³. A packing model `M ∝ (R − 3/(2N))⁻⁵` calibrated at 112 predicted
0.65–0.78× the centres; the measurement gives 0.92×. The model is wrong because the seed set is a
*lattice* of vanishing-sum configurations, not a continuum, so the greedy cover saturates faster than
`δ⁻⁵`. **Do not price this change on the model.**

The output is well formed: `centers128.txt` has header `128 229979`, every bin index is in
`[0,127]` (the int8 range is used to the last unit, as the table in §3 says), and the histogram of
selected positions matches the 112 run's (581 / 222,707 / 6,691 against 675 / 242,295 / 6,908).

## 7. Two things the seed change does and does not fix

**It does improve the conditioning, slightly.** The `sumok` acceptance test bounds `|1 + Σⱼ e(uⱼ)|`
at every retained centre by `κ(N) = 2π(5w/2 + 5πw²/4) + 2·10⁻⁶`, and `m = √(4 − |S|) ≥ √(2 − κ)`.
That gives `m ≥ 1.3630` at `N = 112` and `m ≥ 1.3696` at `N = 128` — a *proof*, not a measurement
(on the recorded centres the observed `|1+T_X|` is 0.1402 against the 0.1422 bound). So the frame
construction is defined on every centre at either resolution, and the code's `m > 1.25` check is
provably never binding.

**It does not touch the tightest constant in the chain.** After the seed fix, the smallest slack is
`h = π/N_u = .196350 < .197` — 0.33 % — and `h` also drives `uget = 6h + pol = 1.241 < 1.26`
(1.5 %). `N_u = 16` is the pinch, not `N`, `R` or `r_s`; `N_u = 20` would give `h = .157` (25 %
slack) at 2.44× the Stage A cells (20,000 vs 8,192 per seed), which is the expensive place to buy
slack. Worth saying plainly in the paper: **`h < .197` is the one inequality in the chain that is
actually tight, and it is tight because `π/16` is just under a round number.**

## 8. The rest of the chain

Changing the seed constants does not touch Stages A–C, but four things there are worth fixing in the
same pass:

- **Stage A targets.** `.103` and `.125` sit in the window `[1/N_u, .125) = [.0625, .125)`. They are
  performance knobs, not mathematics; `3/32` and `1/8` would be dyadic and admissible. Not
  recommended: they pin the recorded run and buy nothing (the comparisons are not on the critical
  numeric path).
- **`k ≤ 10` (Stage B).** Unreachable. The base grid is `n = 2L+1` with `L = ⌈E/w + .500001⌉` and
  `E ≈ R_parent`, so the box cap `n^k ≤ 5·10⁷` gives `k ≤ 5` in passes 1–2 (`n = 23, 31`) and
  `k ≤ 7` in pass 3 (`n = 11`). The paper's error budgets assume `k ≤ 10`, which is the safe
  direction, but the stated cap should read `k ≤ 5, 5, 7`.
- **The Stage C cutoff.** `cluster()` is called once, after the four bin layers, so the `M` in
  `(.042 − 1.11/M)²` is always the deepest grid 96 — the paper never says which `M`, and reading the
  four grids 12/24/48/96 is wrong. `.042` is the clustering's *output* ball radius; the acceptance
  threshold should be `(R − X_M)²` with `X_M = √(29/6)/(2M) = .01145` — the code's own `xnorm` —
  and not `1.11/M`, since `1.11` exceeds `√(29/6)/2 = 1.09924` by 1 %. The defect is only the
  squaring, which loses the sign: `R − 1.11/M < 0` for `M ≤ 26`, so the merge radius is
  non-monotone (`.0505, .0042, .0189, .0304` at `M = 12, 24, 48, 96`) and on a one-layer invocation
  the implied radius bound is `.1421 > .1`, at which every record fails. The fix is one line,
  `τ = max(0, R − X_M)`, and it turns the radius bound into the clean invariant `s ≤ R + 1.001·10⁻⁹`
  (the paper's form gives `s ≤ R − 1.12·10⁻⁴ + 10⁻⁹`). **Keep the value `.042`**: measured on the
  pipeline's own records, `.03` multiplies the ball count by 5.7× (306 → 1755), the edge counts by
  about 25× and the stage's CPU by 4×, and still leaves 12/12 hardest records over the graph cap,
  while `.06/.075/.09` shrink the balls but cost the U-test its discriminating power (1/3/4 of 12
  records return a candidate instead of a negative). The fix itself is free: the two forms give
  identical clustering.
- **The Stage C graph cap, not the cutoff, is the real defect there.** All 163 records that
  exhausted the 5·10⁶ step cap in the recorded run terminate *negative* at 5·10⁷ — median
  9.9·10⁶ steps, maximum 39,038,705, zero candidates, zero give-ups — so the cap sits inside the
  body of the step-count distribution, not its tail. Raising it to 10⁸ costs about 1.9·10⁹ graph
  steps, ≈48 s of CPU, and deletes the whole fallback round: 163 → B fallback → 1127 records → 4
  final C shards, five rows of Table 1, the bad-file list of §7.5 and 5 of the 100 recorded
  invocations. That is the largest reduction in the size of the bash available without changing a
  single mathematical constant.

## 9. What is not better

- **The enumeration grows 1.93× in tuples and 1.76× in tested pairs**, the cover costs 29 % more
  CPU, and the `int8_t` headroom is gone. The compensating 8 % fall in centres makes the whole
  recorded run about 1 % *faster*, i.e. nothing. The gain of this change is exactness, not speed.
- **The proofs of Lemmas 2.6–2.9 are unchanged** — this is a re-parameterisation, not a
  simplification of the mathematics. The gain is confined to the arithmetic appendix, the trust base
  and the run.
- **Nothing here touches the paper's structural premises** (no specialist review, the binary64 model
  of §7.5, the atlas/cover heuristics). Those remain assumptions whatever the constants.

## 10. Reproduce

```
cd .scratch/gh/n128
g++ -std=gnu++17 -O3 -march=native -ffp-contract=off -DNBINS=128 -DSEEDRAD=0.03125 \
    source/covout.cpp -o covrun128
./covrun128 centers128.txt          # prints xs/checked/centres/time
```
`source/covout.cpp` and `source/atlas.cpp` are the authors' files with `NBINS`/`SEEDRAD` macros
substituted for the literals; nothing else is changed.
