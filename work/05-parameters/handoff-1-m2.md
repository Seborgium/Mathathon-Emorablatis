# handoff-1 (m2) — paste-ready text for the paper

```
from:        T5 / Parameters, member m2
to:          T8 (the single final file); cc T0 lead, T9 red team
version:     m2-v1, 24 Sep 2026 tree; does not supersede m1/m3/m5/m6 handoffs
depends-on:  the PDF sections named in each item; experiments/*.py of this member
blocks:      G3 sign-off on N = 112, on F2/F3/F4 wording, and on the Table-1 pair count
artefacts:   work/05-parameters/N112-m2.md, justification-m2.md, experiments/*.py,
             data/{seedcover_sweep,boxes_k,stagec_cutoff,stagec_clusters,constants,
             margins,cost_model,caps}.csv
claims:      touches 2.5, 2.6, 2.7, 2.9, 2.10, 4.6, 4.8, 4.12, 5.5, 6.3, 6.4, 7.3,
             A.3, A.5, A.8, A.9, A.13, and Table 1 of section 7.5
open:        (1) what 151,744,086 counts; (2) the observed k histogram; (3) the per-level
             cluster counts; (4) whether .042 in section 6.3 is meant as a radius or an
             offset
```

## 1. Replace the §7.3 paragraph on N (delete the 32-bit sentence)

> The seed cover uses N = 112 bins. The binding restriction on N is the storage of the
> five-coordinate bin differences in the signed eight-bit type of §7.3 and A.3: the
> differences range over [−(N−1), N−1], so N ≤ 128, and at N = 112 they lie in
> [−111, 111] as recorded. The fresh-centre bound of §2.4, 3/(2N) < 0.032, requires
> N ≥ 47, so the admissible window is 47 ≤ N ≤ 128. The pre-filter tuple count
> C(N+4,5) < 2³¹ gives the weaker ceiling N ≤ 189 (C(193,5) = 2,118,000,528), which is
> dominated and does not constrain the value. The wall clock is flat over the window: a
> replay of the filters of §2.3 reproduces the cover's pair counts exactly (see Table 1
> note) and gives 3788 s at N = 64, 4470 s at N = 112 and 5065 s at N = 128, with the
> retained-centre count essentially independent of N. N = 112 therefore keeps 16 units
> of headroom in the difference, a factor 2.4 in the fresh-centre inequality, and costs
> within 18% of the window's cheapest value.

## 2. Add a note under Table 1 (the pair count)

> The seed-cover row reports the pairs of §2.3: one X list together with one Y list in
> the same shared bin. For N = 112 the filters of §2.3 give 22,829 X lists and 829,306 Y
> lists (mean 7,404 per shared bin), hence at most 112,160,350 pairs; the count in the
> table is the number of pairs *offered to* `covout`, before the shared-displacement
> interval test removes its share. Any 32-bit statement about these counts is vacuous,
> since the traversals use 64-bit counters.

*(If the actual meaning of 151,744,086 is instead "pairs offered to covout", this
sentence is exactly right and the number becomes reproducible; if it means something
else, the honest alternative is to print 22,829 / 829,306 / ≤112,160,350.)*

## 3. Replace the Stage-C cutoff sentence (§6.3) — F2

> With w = 1/M the candidate threshold is (.042 − 1.11w)², whose base is negative for
> M < 26: the expression is |.042 − 1.11w|², not a monotone radius. The coordinate
> cutoff is then (2·threshold)^{1/2} + 10⁻¹⁰, i.e. 7.1·10⁻² at M = 12, 6.0·10⁻³ at
> M = 24, 2.7·10⁻² at M = 48 and 4.3·10⁻² at M = 96; since the smallest nonzero
> *projected* midpoint separation is (5/6)/M, no two distinct bins can merge at M = 24
> and clustering there degenerates to one centre per retained bin. These constants
> affect only the choice of assignments; the proof is the final radius update in
> Lemma 6.4, so the degeneracy costs work but never soundness.

And in the list of constants (or a footnote): *the merge cutoff is a performance
parameter; the covering property is certified by the radius recomputed from the final
assignment.*

## 4. Replace the allowance k ≤ 10 (§5.6, §7.3, A.9) — F3

> The recorded Root dimension satisfies k ≤ 5 for the records entering the first two
> refinement passes and k ≤ 7 for those entering the third, because the base grid
> (2L+1)^k with L = ⌈R/w + 0.500001⌉ is capped at 5·10⁷ boxes: L = 11, 15, 5 give
> (2L+1)^k = 23^k, 31^k, 11^k, so k ≤ 5, 5, 7. The general allowance k ≤ 10 is retained
> for the Root definition (4.1), but it is not attained by any record of this run; the
> largest admissible grid at k = 5 in the second pass is 28,629,151 boxes, 57% of the
> cap.

## 5. Sentinels (F4) — one paragraph in §4.6 or A.12

> Sentinel values are represented by NaN with an explicit isnan check, not by a number:
> `ell`'s scale failure, `bootstrap`'s failure and `relationB::eval`'s failure all return
> it, and no downstream test compares a sentinel with a threshold. (The values 100 and
> 10 previously used lie inside or adjacent to the legitimate range: A.8 bounds the
> certified spectral quantity by 100.1, so 100 is not distinguishable from a valid
> value, and §4.6's guard "t < 10" would have to be retuned with any change to the
> .103 local target.)

## 6. State the four pinned constants (§4 and A.13) — a short "the numbers are not free" paragraph

> Four constants are fixed by inequalities rather than chosen: R < .203/(2π) = .032309
> (A.13 with R_s = 2π·.0320001 = .201063), so the seed radius is within 1% of its
> ceiling; the base grid must satisfy h = π/N_u < .197, i.e. N_u ≥ 16, so the base grid
> 16 is the smallest admissible; the atlas radius cap .125 is below the Stage-B input
> cap .126 by 0.8%; and K = 1.00001 exceeds the required ‖T‖ = √(1+ort) by exactly a
> factor 2 in the excess, since ort < 10⁻⁵ gives 1.000005. Conversely β = .45, β = .8,
> the 30 bootstrap updates, the 25 midpoint trials and the .64 eigenvalue split are free
> parameters: any admissible value works, and none of them can make a certificate wrong.

## 7. One sentence for the margins table

> The thinnest comparison margin in Appendix A is the Candidate external tangent arc,
> 1.2·10⁻⁴ rad against .15·10⁻³ rad (a ratio of 1.25); every other row is at least ten
> times its error and most are 10²–10⁵ times it (the ratio is printed in the last
> column).

## 8. Two numbers the paper should print but does not

* the observed histogram of the Root dimension k (to justify the k statement of §4);
* the per-level cluster counts at M = 12, 24, 48, 96 (to show the Stage-C cap 2048 is
  not close, or that it is: a 2-torus model reaches 1,626 at M = 24).
