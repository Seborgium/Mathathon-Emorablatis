# Global conditioning of the numeric chain (direction d4)

Team T5 (Parameters), member m6. Script: `experiments/m6_conditioning.py`; table:
`data/m6_conditioning.csv`. Run it with `python3 experiments/m6_conditioning.py`.

**What this document is.** Not the constant-by-constant table — that is `justification.md`, owned by
another member of this team, and I do not touch it. This is one question asked of the whole numeric
layer: *if a quantitative input of the pipeline moves, how far does it move the margin that judges
it, and which link breaks first?* Perturbation in, amplification out, first failure named. Three
perturbation classes are treated separately because they answer different questions: a uniform
inflation of every established error (how much numerical slack is there in total), a uniform
inflation of proportional quantities (radii, which are compared to one another), and a
one-at-a-time movement of a named constant through its own formula (where a single input is
sensitive).

Every formula used below is the paper's own, quoted at the point of use. Nothing is fitted to the
run and no constant is extrapolated.

---

## 1. The chain as 23 comparisons: reserve = margin / established error

Appendix A closes with a table of "established adverse error" against "explicit margin". Sorting the
23 components by reserve (margin ÷ error):

| # | link | established error | margin | reserve |
|---|---|---|---|---|
| 1 | **Candidate external tangent error** | 0.00012 rad | 0.00015 rad | **1.25** |
| 2 | **A flat norm** | 10⁻⁶ | 10⁻⁵ | **10** |
| 3 | A directional comparison | 4·10⁻⁶ | 10⁻⁴ | 25 |
| 4 | C joint support | 10⁻⁸ | 3·10⁻⁷ | 30 |
| 5 | Root identity Frobenius | 5·10⁻⁸ | 2·10⁻⁶ | 40 |
| 6 | B cross-Gram spectral | 2·10⁻⁹ | 10⁻⁷ | 50 |
| 7 | Candidate direct support | 2·10⁻⁶ | 10⁻⁴ | 50 |
| 8–11 | G entry (2nd), seed dual support, Root orthogonal, shared endpoints | — | — | 100 |
| 12–15 | C direct/directional, B projected normal, tensor row bound | — | — | 200 |
| 16 | spectral row bound | 3·10⁻¹³ | 10⁻¹⁰ | 333 |
| 17–19 | seed support, Root horizontal, spectral fourth-norm | — | — | 10³–2·10³ |
| 20 | shared-coordinate numerator | 3.5·10⁻¹¹ | 10⁻⁷ | 2857 |
| 21–22 | G entry (1st), bootstrap update | — | — | 10⁴ |
| 23 | B local update / seed gap | 10⁻¹³ / 10⁻¹⁴ | 10⁻⁸ | 10⁵ / 10⁶ |

* **No reserve is below 1.** The audit of `results/code-audit.md` §4 is confirmed: there is no
  comparison whose margin is smaller than the error it must cover.
* **The chain's global resilience is 1.25.** Inflate *every* established error by a common factor
  `t`; the chain survives iff `t < 1.25`, and the link that breaks first is the Candidate external
  tangent comparison. Second is the A flat-norm comparison at 10, third the A directional
  comparison at 25. Median reserve 200.
* The tangent margin is therefore the one number in Appendix A that deserves printing with its
  derivation: it is itself a sum of three terms — the coefficient and offset errors, the projection
  term (8.81·10⁻⁵ rad) and the centre correction (1.27·10⁻⁵ rad), so 0.00012 is 92% projection plus
  centre. A reader cannot see that from the table, and it is the only reserve under 10.

## 2. One input at a time: amplification, elasticity, tolerance

Each row perturbs one named input, propagates it through the displayed formula that consumes it, and
reports the **elasticity** `d log(margin-consuming quantity) / d log(input)` — how many per cent of
the bound one per cent of the input buys — and the **tolerance**, the input value at which the link's
margin is exhausted.

| input | formula | amplification | elasticity | tolerance | verdict |
|---|---|---|---|---|---|
| f₀ (Hadamard residual) | (6.3) `K = √(1 + a f₀)`, `a = √(2π²/6) = 1.8138` | `dK/df₀ = a/2K = 0.9069` | **9.1·10⁻⁷** | `f₀ ≤ 1.103·10⁻⁵` = **11.0×** the stated 10⁻⁶ | K is insensitive to f₀; not where the chain is tight |
| q_d | (4.18) `arc ∝ √q_d / √(1−q_d/4)` | at 3.8: `darc/dq = 22.94` | **10.00** | `q_d < 4` ⟹ **+5.26%** | the most elastic constant in the paper: 1% in q_d is 10% in the arc bound; the singular value 4 is only 5.3% away |
| β | (4.32), (4.33) `(x+y)² ≤ (1+β)x² + (1+1/β)y²` | optimal at `β* = √(B/A)`; penalty `≤ 1+β` | bounded | any β > 0 | a mis-set β costs at most 45% / 80%: bounded, never singular |
| C (normal polynomial) | (4.6), (4.38) `nP(s) = n₀ + ιs + Cs²` | the update decreases iff `nP(s) < s` | — | **`C < 1/s`** | see §3 — the admitted `C < 20` is not enough above `s = .05` |
| R | (2.10 coverage) `N ≥ 3/(2R)`; (A.9) `R ≤ .126` | `dN/dR = −3/(2R²) = −1465` | **−1** | `R ∈ [0.013393, 0.126]`, a factor 9.4 | 0.032 is a choice inside a wide interval |
| w | (2.8) gap filter | the spread is **exactly** `w` | **1** | any unrecognised perturbation | **zero analytic reserve** — see §4 |
| w | (A.9) `L = ⌈E/w + .500001⌉`, boxes `(2L+1)^k` | `d log(boxes)/d log w = −k` | **−k = −5…−10** | `w ≥ .005` at pass 2 for k = 5 | the costliest amplification: 10% smaller w costs 50–100% more boxes |
| M | §6.3 `X_M = √(29/6)/(2M)` vs ρ = .042 | elasticity −1; reserve `ρ/X_M` = .46, .92, 1.83, 3.67 at M = 12, 24, 48, 96 | −1 | `M ≥ 27` for a positive base | the square hides the sign (F2) |

Two of these are worth stating in the paper because they invert the emphasis of the appendix: **q_d
is the most elastic constant** (10:1), and **f₀ is the least** (10⁻⁶:1) — yet the appendix argues at
length about f₀'s 10⁻⁶ and says nothing about q_d's 5.3% distance from a singularity.

## 3. A new finding: the admitted range `C < 20` makes the bootstrap inert above s = .05

(A.8) and §4.6: the bootstrap replaces the radius upper `s` by `√(nP(s)² + (1+ort)t₀²)` and accepts
the step only when it decreases `s`. Since `nP(s) = n₀ + ι s + C s²` with `n₀ < 10⁻⁶`, `ι < 10⁻⁴`,
`C < 20`, a decreasing step requires

    nP(s) < s   ⟺   C < 1/s − ι − n₀/s².

Recomputed at the radii that actually occur:

| s | largest C that still decreases s | admitted C < 20 |
|---|---|---|
| 0.016 (fine pass τ) | 62.5 | ok |
| 0.030 (§6.1 hypothesis) | 33.3 | ok |
| 0.050 | 20.0 | **borderline** |
| 0.070 (mid pass τ) | 14.3 | **fails** |
| 0.103 (local target) | 9.7 | **fails** |
| 0.125 (atlas cap) | 8.0 | **fails** |

So for any record with `C` above roughly `1/s`, the ellipsoid/bootstrap path cannot improve the
radius at all: the proposal increases `s`, is rejected, and coverage falls back to the initial `s₀`.
That is **not** a soundness failure — Proposition 4.13 is an implication about *accepted* steps, and
rejecting a step only loses an improvement — but it means the "finite improvement of a certified
radius" does nothing in exactly the upper part of the radius range where the local targets .103 and
.125 sit, and the A.8 estimate "at a current upper s ≤ 3.00001 the normal polynomial is below 181" is
not the operating constraint. The operating constraint is `C < 1/s`. **Recommendation (for T8): print
the observed distribution of `C` and the inequality `nP(s) < s`, or narrow the validated range to
`C < 1/.125 = 8` if that is what the records satisfy.** A record with `C` between 8 and 20 at
`r = .125` is being carried by its initial `s₀` alone.

## 4. The tightest analytic link has zero reserve

Lemma 2.5 bounds the change of a circular gap by `2δ`; each seed phase is within `w/2` of its
midpoint, so the gap filters of (2.8) may use `w` — and the derivation uses *exactly* `w`, no more:

    x₅ ≤ (l+1)/N  ⟹  g_x ≥ 1 − (l+1)/N,   g_y ≥ g_x  ⟹  g_y,mid ≥ g_y − w ≥ 1 − (l+2)/N.

The distance between the exact lower bound and the midpoint threshold is exactly `w`. **The reserve
on this link is 1: the proof spends its entire perturbation allowance in one comparison**, and the
only thing behind it is the 10⁻⁸ comparison slack of A.3 (which is itself 8 orders above the 10⁻¹⁴
rounding it covers). It is a defensible design — the filter is exactly what Lemma 2.6 proves — but it
is the one place where the word "margin" in the appendix is misleading, and it should be said
plainly. (The first inequality of (2.8) is a separate matter: as printed it cannot reject anything,
because `g_{x,mid} = 1 − (l+½)/N` always exceeds `1 − (l−1)/N` by `1.5/N`. I record that here as a
statement defect; the constant work belongs to `justification.md`.)

## 5. Classes of perturbation and the first link that fails

| what is inflated uniformly | first link to fail | critical factor |
|---|---|---|
| every established error | Candidate external tangent (0.00012 → 0.00015) | **1.25×** |
| every record radius | atlas cap .125 against A.9's validated bound .126 | **1.008×** (0.79%) |
| the A.9 scale sum `R + ‖d_q‖` against .377 | Root certificate total | **1.0053×** (0.53%) |
| the tangent error alone | the same tangent comparison | 1.25× |
| f₀ | `K = 1.00001` | 11.0× |
| q_d | the arc multiplier, at the singular value 4 | 1.053× |
| R downward | coverage `3/(2N) ≤ R` | 0.419× (0.032 → 0.0134) |
| N upward | int8 five-coordinate differences | 1.143× (112 → 128) |
| N upward (32-bit clause only) | `C(N+4,5) < 2³¹` | 1.688× (112 → 189) |
| w upward | the gap filter (reserve exactly 1) | **1.000×** — any increase |
| τ_fine upward | §6.1's `r ≤ .03` | 1.875× |
| M downward | `X_M > .042`, clustering cutoff | M ≤ 26 |

The qualitative result, and the one I would carry into the paper: **the chain does not break first on
a numerical error.** Its tightest proportional link is a radius ratio (0.8%), its tightest analytic
link is a filter with zero reserve, and the celebrated 1.25 tangent reserve is the third of the three
stories — the only one that is stated in radians and the only one a reader can currently see.

## 6. Precision requirement

`binary32` has `eps = 1.19·10⁻⁷`. Of the 23 tabulated margins, **12 are below it** (10⁻⁷ entries and
smaller: cross-Gram, second G entry, Root orthogonal, B projected normal, spectral row, seed support,
Root horizontal, shared numerator, first G entry, bootstrap, B local, seed gap). So binary64 is
required, and the requirement comes entirely from those twelve; the other eleven would survive in
single precision. That is the right way to state the arithmetic hypothesis of the paper: not "binary64
throughout" but "binary64 at the twelve comparisons whose margins are under 10⁻⁷".

## 7. Retractions and scope corrections (my earlier submission)

Two claims I made in the first submission were wrong, and this is where I withdraw them. Both are
also printed by the script (§E2, §E3) so that the withdrawal is reproducible.

1. **The `(2NR/3)⁹` "reuse ceiling" is withdrawn.** It is not a bound on the quantity I compared it
   with. The number of unit bins a radius-R ball can contain at all is the lattice-point count
   `#{k ∈ Z⁹ : ‖k‖ ≤ NR}`, which at N = 112 (`NR = 3.584`) is exactly **284,055** (volume estimate
   3.2985·(NR)⁹ = 321,832) — 112× my 2538, and the right order for the judge's 5.1·10⁵ volume figure.
   And `607 = pairs/centres` is a *compression* ratio that mixes filtering (infeasible pairs need no
   centre) with reuse, so comparing it to a geometric capacity was a category error. What survives,
   and is derivable, is the **reach**: by (2.17) a previous centre can be tried only for a bin whose
   grid offset `k = N(u−u′)` satisfies `‖k‖ ≤ NR − 1.5`, and the exact number of such offsets is
   `#{k ∈ Z⁹ : ‖k‖ ≤ NR−1.5}`:

   | N | 47 | 56 | 64 | 96 | **112** | 128 | 160 | 189 | 224 |
   |---|---|---|---|---|---|---|---|---|---|
   | reachable offsets | 1 | 1 | 1 | 163 | **2,869** | 14,581 | 409,335 | 2,634,777 | 20,950,491 |

   At N = 112 this is 2869 — the same reach another member reported (his is a sufficient bound from
   (2.18); mine is the exact lattice count, and they agree), and at N = 56 it is 1, i.e. reuse
   degenerates to exact coincidence. *That* is the defensible form of "halving N kills reuse".
2. **The centre-count extrapolation is withdrawn.** Fitting one constant to the single observation
   249,878 reproduces that observation by construction, so "within 5.7%" is not evidence, and the
   values I quoted at N = 56 and N = 224 were two doublings of extrapolation. The record determines
   only: 151,744,086 pairs in 621.59 s (4.10 µs/pair), 22,829 x-lists retained, 249,878 centres.
   Nothing in it separates filtering from reuse; the centre count as a function of N is **not
   determined** by the published data.
3. **F3 scope corrected.** "k ≤ 10 is unreachable at every admitted width" is false: with w = .05 and
   a small-radius record (`E ≈ .016`), `L = ⌈.016/.05 + .5⌉ = 1` and `3¹⁰ = 59,049 ≤ 5·10⁷`, so k = 10
   is admissible. The correct statement, and the one to keep, is the narrow one: at the three
   specified (E,w) pairs the per-axis counts are 23, 31, 11, and the 5·10⁷ cap admits 23⁵, 31⁵ and
   11⁷ but not the next powers, so every record in the recorded run has k ≤ 5 (passes 1–2) and k ≤ 7
   (pass 3). The stated allowance 0 ≤ k ≤ 10 is then an unused allowance at those widths, not an
   impossibility.

## 8. Corroboration of numbers reported by other members (independent recomputation)

Labelled as corroboration: these are not my contributions, they are recomputed by my own code from
the paper's text.

| quantity | other member's value | my recomputation | script |
|---|---|---|---|
| C(116,5) | 160,389,488 | **160,389,488** | `m6_conditioning.py` §E1 |
| C(115,4) | 6,913,340 | **6,913,340** | §E1 |
| largest N with C(N+4,5) < 2³¹ | 189 | **189**, C(193,5) = 2,118,000,528 | §E1 |
| 3/(2N) at N = 112 as a fraction of R | 0.0134, "40% of R" | **0.0133929 = 41.85% of R** | §E1 |
| reach at N = 112 under (2.18) | 2869 | **2,869** offsets k | §E2 |
| L and the admissible k per pass | 11/15/5, k ≤ 5/5/7 | **11, 15, 5; k ≤ 5, 5, 7** | `exp_refinement.py` |
| base of the Stage-C cutoff negative for | M < 26 | **M ≤ 26** (M = 26: −6.92·10⁻⁴) | `exp_stagec_cutoff.py` |
| reserves in Appendix A, minimum | "one to three orders" | **min 1.25, median 200** | §A |

## 9. What I could not verify

The paper reports no counter for Stage A nodes, retained bins, clusters, the k histogram, or the
distribution of the Root constant `C`. §3 above would be settled by one CSV of `C` per record; the
reach table in §7 by one CSV of centres per N. Without them, the conditioning analysis is exact in its
formulas and silent, by design, on the observed values: I have not fitted anything to the single
observation the run provides.
