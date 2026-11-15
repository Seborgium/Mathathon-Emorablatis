# handoff-6 — conditioning paragraphs for T8

from: T5 (Parameters), member m6
to: T8 (the single final file)
version: 1.0
depends-on: `conditioning-m6.md`, `experiments/m6_conditioning.py`, `data/m6_conditioning.csv`;
App. A closing table; §4.6, §A.8 (bootstrap); §2.2–2.3 (gap filters); Lemma 4.8 (q_d)
blocks: the verification-report chapter (P8.4) and the parameter chapter (P8.5), where a reader is
told how much numerical slack the proof has and where it is thinnest
artefacts: `work/05-parameters/conditioning-m6.md` (+ the script and CSV named there)
claims touched: Prop. 4.13 / A.8 (bootstrap range), §2.2 (2.8), Lemma 4.8, App. A closing table
open questions: the observed distribution of the Root constant `C` (one CSV would settle §3 below);
whether the validated range `C < 20` is narrowed to `C < 8`

The constant-by-constant table is `justification.md`, owned by another member of T5; I do not
duplicate it here. The paragraphs below are only the conditioning result. Numbers in **bold** are
recomputed by `experiments/m6_conditioning.py`.

---

## 1. New subsection for the verification report: "Reserve and amplification"

> Every comparison in this paper has the form "a certified bound, plus a margin, against a
> threshold". We report the *reserve* of each: the margin divided by the established adverse error.
> Across the twenty-three components tabulated at the end of Appendix A the reserves run from
> **1.25** to **10⁶**, with median **200**; no reserve is below one. Three facts follow.
>
> First, the chain's global resilience is **1.25**: if every established error were inflated by a
> common factor, the first comparison to fail would be the external tangent bound, where the
> established error is **0.00012 rad** against a margin of **0.00015 rad**. That bound is itself a
> sum — coefficient and offset errors, the projection term **8.81·10⁻⁵ rad**, and the centre
> correction **1.27·10⁻⁵ rad** — so **92%** of it is the last two terms, and we print the three
> addends. Second, the next reserves are 10 (the flat-norm test) and 25 (the A directional
> comparison): the chain is not uniformly tight, and a reader who wants to check one number should
> check those. Third, precision: **12 of the 23 margins are below the binary32 unit roundoff
> 1.19·10⁻⁷**, so the arithmetic hypothesis is not "binary64 throughout" but "binary64 at the twelve
> comparisons whose margins are under 10⁻⁷"; the other eleven would survive in single precision.
>
> A different perturbation class breaks the chain sooner than any error. Every radius in the pipeline
> is compared with another radius, and the tightest of those comparisons is the atlas cap **0.125**
> against the validated Stage-B input bound **0.126** of §A.9 — a **0.79%** proportion. The second is
> §A.9's own scale inequality `R + ‖d_q‖ < .377`, which holds at **0.375002**, a **0.53%** reserve.
> So the proof's tightest links are proportional, not numerical, and the Appendix should say so where
> each of those two numbers appears.

## 2. §A.8 / §4.6, the bootstrap: replace the paragraph on "at most 30 updates"

> The bootstrap replaces a certified radius upper `s` by `√(n_P(s)² + (1+ort)t₀²)` with
> `n_P(s) = n₀ + ιs + Cs²`, and accepts the step only when it decreases `s`. A decreasing step
> exists exactly when `n_P(s) < s`, i.e.
>
>     C < 1/s − ι − n₀/s².
>
> At the radii this pipeline actually uses — **0.07**, **0.103**, **0.125** — the right-hand side is
> **14.3**, **9.7**, **8.0**, all below the validated ceiling `C < 20`; it is above 20 only for
> `s < 0.05`. So for any record with `C` between `1/s` and 20 the ellipsoid path cannot improve the
> radius at all: the proposal increases `s`, is rejected, and the record is carried by its initial
> `s₀`. This is not a soundness failure — Proposition 4.13 is an implication about accepted steps, and
> a rejected step only loses an improvement — but the "finite improvement" mechanism is inert in the
> upper part of the radius range, which is where the local targets sit. We therefore either print the
> observed distribution of `C` alongside the inequality `n_P(s) < s`, or narrow the validated range to
> `C < 8`, which is `1/0.125`. The count "at most 30 updates" is a time cap and carries no correctness
> weight: with a per-step contraction `λ` the gap closes by `λ³⁰`, which is 9·10⁻¹⁰ at `λ = .5` and
> 4·10⁻² at `λ = .9`.

## 3. §2.2, one sentence after Lemma 2.6

> The gap filters consume the perturbation allowance of Lemma 2.5 **exactly**: the distance between
> the exact lower bound `g_x ≥ 1 − (l+1)/N` and the midpoint threshold `g_{y,mid} ≥ 1 − (l+2)/N` is
> precisely `w`. There is no analytic reserve on this link at any `N`; what stands behind it is the
> `10⁻⁸` comparison slack of §A.3.

## 4. §4.8, one sentence after Lemma 4.8

> The arc bound's multiplier is `(1 − q_d/4)^{-1/2}`, so the quantity is not `q_d` itself but its
> distance from the singular value 4: at `q_d = 3.8` the multiplier is **4.47** and the elasticity
> `d log(arc)/d log(q_d)` is exactly **10**. Of all the constants in this paper `q_d` is the most
> sensitive to its own perturbation — a 1% change in `q_d` moves the arc bound by 10%, and the
> admission `q_d < 3.8` is only 5.3% from the singularity.
