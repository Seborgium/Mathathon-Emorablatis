# W1 measurement — can the manuscript alone rebuild the seed enumeration?

Mode A probe, one agent, sources for `seed.cpp` and `covout.cpp` not opened. Question: if a reader
had only §2 and Appendix A.2–A.3, would they get the recorded enumeration? Answer: **the set yes,
the order no.** This is the only part of the reproduction that can be settled without the code, and
it settles it in the paper's disfavour.

## What was run

    .ultramath/smwgt1mbm/m5 $ ./c-run_d6.sh        # exit 0, 63 s, one core

Transcript `ms/run_d6.log`. Fixtures `ms/xs_ordered.txt` (22 829 lines, `a b c d l s`) and
`ms/ytails_ordered.txt` (368 732 lines).

## Result

| check | evidence | result |
|---|---|---|
| `|xs|` | 22 829, equal to the recorded run's `xs22829` | exact |
| every recorded `X` tuple present | 13 557 distinct tuples in `centers.txt` | 0 missing |
| skip index `s` | first minimiser of `|2q_s+1−N|` | 0 mismatches in 249 878 |
| every recorded tail present | 76 993 distinct `(h,y)` pairs | 0 missing |
| order | `(t, ypos)` strictly increasing with `(l,d,c,b,a)` nesting | 0 violations |
| wrong nesting excluded | lexicographic/forward nesting | 5 497 violations |

The 5 497 is not a new number: when I first probed the file with the natural lexicographic key I
measured exactly 5 497 decreases. Two independent routes to the same defect.

## What the prose leaves open, and what it costs

| open choice | prose alone | correct reading | effect on the count |
|---|---|---|---|
| loop nesting | "nested ascending loops" reads lexicographic | last coordinate outermost, `(l,d,c,b,a)` | none — 22 829 either way |
| `sumok` direction set | "residual direction and directions perpendicular to the five columns" | **both** | residual only 30 401; perpendiculars only 22 838; both 22 829 |
| the `1−(l−1)/N` gap rule | stated | applied | off → 9 584 |
| `expair` vs libm | A.2 bounds the difference at 2e-14 | either | none |
| the 1e-8 slack | stated | applied | none at this grid |

So: one open choice (nesting) is invisible to every count, fatal to byte-identity, and not stated in
the prose; the two arithmetic choices the paper worries about are inert here.

## Consequence for the paper

A reader cannot reproduce `centers.txt` from the manuscript. They can reproduce the *set* of 22 829
seeds and the count of 249 878 centres — the numbers the paper quotes — but not the file, because
the enumeration order is not written down. That is a cheap fix in the text (one sentence: "the
enumeration runs with the last coordinate outermost, so `xs` is ascending in `(e,d,c,b,a)`"), and it
should go in before the preprint is read as reproducible. It also answers a question the paper's
§7.5 leaves implicit: the artefact depends on the code in a way the prose does not capture, and the
dependency is *ordering*, not arithmetic.

## Note for unit 04

Every one of the 22 829 `X` tuples, including the 9 272 that no centre uses, has a `Y` tail passing
the second gap inequality. So the 9 272 unused seeds are rejected by `extend`'s interval
intersection, not by the enumeration — a centre-count discrepancy will come from the cover, and the
count is therefore a check on `extend`, not on `seeds::build`.
