# Slide notes — 20-minute run

Two decks, same content, two registers.

- `deck1.pdf` (19 slides) — content deck. Numbers on the slide, denser, for a technical room.
- `deck2.pdf` (16 slides) — presentation deck. One claim per slide, larger type, warmer palette.
  This is the one to stand in front of; `deck1` is the handout.
- `video/stageC-demo.mp4` (0:44) — the demo, played from slide 10 (deck 2) / slide 9 (deck 1).
  Poster frame in `video/poster.png`; the source is `examples/step4_example.py`.

## Timing (deck 2)

| min | slide | what to say |
|---|---|---|
| 0:00 | title | the object: N(6), open since 2004 |
| 1:30 | what unbiased means | one sentence, let the picture do it |
| 3:00 | interlude "how many" | pause; the answer is three |
| 3:30 | six is the awkward dimension | prime power vs not; 3 ≤ N(6) ≤ 7 |
| 5:00 | the move | fix basis 1 → one Hadamard → 25 phases; the quantifier is new |
| 7:00 | five steps | cover / compress / shrink / count / close |
| 8:30 | cover the circle | 151,744,086 → 249,878; only necessary inequalities |
| 10:00 | U(2) | the one genuinely clever device |
| 11:30 | shrink | 0.125 → 0.011 with witnesses; obligations never pass |
| 13:00 | count | two hexagons, 36 cross edges, pattern absent |
| 14:30 | video | play it; say nothing over it |
| 15:30 | the fine print | three assumptions, plainly |
| 16:30 | what we checked | the three numbers; say what is *not* claimed |
| 18:00 | cannot add one vector | 45 phases, 45 conditions, +5 vs +10 |
| 19:00 | what it means | one line each; the caution last |
| 20:00 | close | what is settled / what is not |

## Sentences that must not be said

- "We have proved N(6)=3." (The preprint claims it; our work verifies fragments.)
- "The proof is formalised." (The Lean assembly is conditional and stops at N(6) ≤ 5.)
- "The computation has been fully verified." (One covering step reproduced; four Stage-C batches,
  one Stage-B parent, Stage A cells, Root witnesses.)
- "A fourth basis is impossible because there is not even one vector." That is true for the triples
  decided, and it is *stronger* than N(6)=3, not implied by it — in C⁴ both phenomena coexist.
- Anything with "Zauner" as if the conjecture were about Hadamard matrices; it is about MUBs.
