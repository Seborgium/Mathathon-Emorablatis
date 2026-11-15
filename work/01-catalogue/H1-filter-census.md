# direction d3 — KERNEL + FILTER CHECKER (member m2)

Rigorous, complete census of the seed-stage necessary filters of Section 2.3 of the preprint,
plus an independent recount of the pair stage and the retained-centre list. Everything below was
executed on this VM; exact commands are at the end. Nothing here is a claim about the coverage
tests (2.18)/(2.19) — those are direction 3's (m3's) reuse checker.

**Headline.** The two `sumok` enumerations of `seeds::build` are *completely* decided in exact
arithmetic, and the accept sets coincide with the pristine upstream binary **exactly**, with zero
undecided cases:

| enumeration | tuples visited | pass (2.7) | pass (2.8)-first | rigorous `sumok` survivors | upstream accepts | symmetric difference |
|---|---|---|---|---|---|---|
| X (`seeds::xs`) | 160,389,488 | 85,349,292 | 16,197,157 | **22,829** | **22,829** | **0** |
| Y (`seeds::ys`) | 774,294,080 | – | – | **829,306** | **829,306** | **0** |

The Y table is per shared bin, 112 bins, and the equality is again set equality, not just a count.
For the pair stage: the exact-integer half of (2.8) agrees with the stored-gap test on **all**
298,638,554 candidate pairs (0 mismatches), and `checked = 151,744,086` is reproduced exactly by a
separate driver built on the upstream source text (no instrumentation of `covrun`).

---

## 1. What is being checked, and in which logical form

The filters below are *necessary* conditions: a bin tuple that can contain an exact Hadamard seed
must pass them. Upstream discards a tuple when a filter returns "reject", so the only question that
matters for Proposition 2.10 is

> **(C) no tuple that can contain an exact solution is rejected.**

The sum test (2.11) has a property that makes (C) checkable without knowing anything about the
code's arithmetic choices:

> (2.11) — derived from (2.10) — holds for **every** `v ∈ R^2`, not merely for the direction the
> code happens to test.

So for the *completeness* direction the code's chosen direction and its rounding are irrelevant:
if a tuple is feasible then (2.11) holds at whatever real vector the code's stored pair represents,
and the code could only reject it by exceeding its own `1e-8` comparison slack. That is a uniform
error-budget question (paper A.3), not a per-tuple search question. What I therefore check per
tuple, in exact arithmetic, is the *mathematical* statement

> `mu_k  =  |v_k·c| - (5 pi w^2/4)||v_k|| - (w/2) sum_j |v_k·J_j|  <=  0`,  `v_1 = c`, `v_{k} = R90(J_{k-1})`,

with `c`, `J_j` built from the exact rational midpoints `u_b = (b+1/2)/N`. Verdicts:

* `HOLDS` — `sup mu_k < 0` proved for all six directions: the tuple cannot be excluded by (2.11);
* `FAILS` — `inf mu_k > 0` proved for some direction: the tuple provably contains no exact solution;
* `UNDECIDED` — an enclosure straddles 0; never resolved by convention, only reported.

The converse direction (a rejection must be genuinely justified) is a per-tuple statement that does
need the code's own arithmetic; it is addressed at the pair stage in §5 by comparing the code's
`extend` intervals with rigorous ones on the tightest rejections.

## 2. Arithmetic kernel (`src/ikernel.py`, `src/filters.py`)

* **Number forms.** Intervals are pairs of Python ints at scale `2^-192`; the midpoint data are
  exact rationals with denominator `2N = 224`. No `binary64`, no `libm`, no `math.cos`, no
  `nextafter` and no vendor correct-rounding claim appears anywhere in the kernel or in a decision.
* **Elementary operations.** `+`, `-`, `*`, `sq` (tight for zero-straddling intervals), `abs`,
  `sqrt` (`math.isqrt` of the exact scaled integer: exact floor/ceil), interval division by a
  sign-separated interval. Each returns an outward enclosure; strictness is only asserted from the
  enclosures (`sup < c`), so a touching endpoint is *undecided* (unit-tested).
* **pi.** `src/ikernel.py:pi_certificate()` re-derives the preprint's (A.8)/(A.9) independently, in
  exact rational arithmetic, from Machin's formula with alternating-series tails:
  `|pi_hat - pi| <= 1.2254e-16 < 2e-16`, and the exact sign of `pi_hat - s` is negative. A sharper
  bracket (70/20 terms, width 6.6e-99) is used for the working enclosure.
* **e(midpoint).** `expair_iv(theta)` encloses `2 pi theta` from the pi bracket, reduces by
  `pi - x` for `x > pi/2` and by `e(theta) = -e(theta-1/2)` for `theta >= 1/2`, then evaluates
  degree-92/93 Taylor series in fixed point with a rigorous geometrical tail majorant
  (`first omitted term / (1 - 16/((2n+1)(2n+2)))`, `n = 46`). Resulting endpoint width over all 224
  table entries: **8.4e-57**. All 224 entries were additionally checked against 70-digit `mpmath`
  (a control, not part of the certificate): 0 violations.
* **Filters implemented.** (2.7) orientation (exact integers); both halves of (2.8) as exact integer
  comparisons of the scaled gap numerator (`gap_num`, units of `1/(2N)`, includes the fixed zero);
  (2.11) in the six code directions; (2.14) shared displacement, including the fact that the support
  sum in (2.13) omits the *shared* index in every direction (my first transcription omitted the
  direction's own index instead; the containment test in §5 caught it — see `filters.py`
  `extend_clip`).

`src/census.cpp` is the same kernel at 50 fractional bits with `__int128` products (integer only),
used to decide all 934M enumerated tuples; `src/sharp_pass.py` re-decides every survivor at 192
bits.

## 3. Complete census of the two `sumok` enumerations

`./census x 112`, `./census y 112`: all weakly increasing five-bin tuples, in the same order as
`seeds::build`, with (2.7) and the first half of (2.8) as exact integers and then the six-direction
(2.11).

```
x: visit 160389488 orient 85349292 gap 16197157 summed 16197157 holds 22829 undecided 0
y: visit 774294080 summed 774294080 holds 829306 undecided 0
```

`src/compare_sets.py` joins these with the pristine enumeration dumped by `./probe xs 112`
(that probe includes the upstream translation unit with `main` renamed, so the accept sets are
upstream's own):

```
X: upstream 22829, rigorous survivors 22829     rigorous \ upstream 0     upstream \ rigorous 0
Y: upstream 829306, rigorous survivors 829306   (per shared bin: 0 in either direction)
```

`src/sharp_pass.py` re-decides all 22,829 + 829,306 survivors at 192 bits: **0 disputes**. The
tightest provable slack over all accepted X tuples, all six directions, is
**5.296e-08**, attained by the tuple `(1,18,57,57,74)` (which occurs both as an X list and as a
Y list); the evaluation error of the code's own arithmetic is of order 1e-16, so the `1e-8`
comparison slack is not load-bearing anywhere in the observed data. There is **no** tuple at any
stage whose verdict is `UNDECIDED` at 192 bits, so no near-tie had to be classified either way.

## 4. Exact ties, exact-boundary data and controls

* (2.8) equality is *real and frequent*: `gap_num` attains the threshold exactly for many tuples
  (e.g. `(28,57,84,84,84)` at `l=84`: threshold 58, gap 58), and the exact filter, like the code's
  `<` test, retains equality. Unit test `tests/test_filters.py::test_exact_ties` covers equality,
  one integer step over the threshold, equality in (2.7), and the kernel's refusal to decide at a
  touching endpoint.
* Pair stage: `1,378,441` candidate pairs have the *stored* gap exactly equal to the threshold, and
  `min |gap_num - exact threshold| = 0`; the code retains all of them, and the exact integer test
  agrees with the code's stored test on all 298,638,554 pairs (0 mismatches).
* Small-N controls (a different exhaustively checkable instance of the same code path): for
  N = 2,3,4,5 every X tuple (after (2.7)) and every Y tuple was compared with the pristine
  `sumok`: 16, 65, 191, 460 tuples respectively, **0 disputes, 0 undecided**.
* `tests/test_filters.py`: 25 assertions, all passing (`python3 tests/test_filters.py`).

## 5. Pair stage

`./probe pairs 112` re-implements only the four-line inner loop of `coverSeeds::run` (gap test, then
the `extend` disjointness test) on top of the upstream objects, with no bucket/coverage machinery:

```
pairs cand 298638554 gappass 190192620 checked 151744086 exactgap 1378441
gapfilter mismatch_vs_exact 0  min_exact_distance 0
extend rejected 38448534 accepted 151744086
extend rejected min_margin 0x1.5849928p-27  (1.0020e-08)  m<1e-7: 6   m<1e-5: 554   m<1e-3: 52781
extend accepted closest-to-touch 0x1.3779786p-26 (1.8130e-08)
```

`checked = 151,744,086` is thus **reproduced exactly** by a driver that shares only the source text
with the recorded run — the audit finding that the number is unreproducible is resolved at the level
of the filter chain (this is not a byte-identical re-run of `covrun`, and the coverage test itself is
not re-done).

**Retained centres** (`src/retained_pairs.py`, all 249,878 lines of `centres.txt`, 547 s): the
`X` list and the `Y` list of each centre are in the rigorous survivor sets; the second half of (2.8)
holds exactly; the rigorous (2.14) enclosures of the two lists intersect; and the code's own
`extend` interval **contains** the rigorous enclosure for both lists in every one of the 249,878
pairs (0 failures, worst containment slack 1.178e-05 = the code's `1e-5` endpoint inflation plus its
`1e-7/|a|` radius inflation, as (A.3) claims). `mk`'s recomputed selected position agrees with the
stored `s` in all 249,878 lines.

**Tightest rejections** — the soundness side. 5,589 of the 38,448,534 `extend` rejections have
code-side disjointness distance below 1e-4; the 1,500 closest (from 1.002e-08 upward) were checked
rigorously: the code's intervals contain the rigorous enclosures (0 failures) and the rigorous
enclosures are **disjoint** in all 1,500 (0 unjustified rejections, smallest code-side distance
1.0020e-08). So the rejected pairs in this tight band really are infeasible for the shared
displacement, with a margin.

## 6. What is *not* verified here

1. **The uniform binary64 error budget** of `expair`/`sumok`/`extend` (paper A.3) is **not
   re-derived**. §3 establishes, completely, that the code's accept sets *equal* the exact survivor
   sets; it does not prove the general implication "feasible ⟹ accepted" independently of A.3.
   Closing that needs either an exact binary64 emulation of `expair`/`sumok` per tuple (feasible:
   every operation except `sqrt` is rational; my probe would need a `mu`-printing mode) or a
   re-derivation of A.3. The measured headroom is 8 orders of magnitude (5.3e-08 vs 1e-16).
2. **`extend` containment is verified on the 249,878 accepted pairs and the 1,500 tightest
   rejections**, not on all 38,448,534 rejections (5,589 of them are within 1e-4 of the boundary).
3. **The coverage tests (2.18)/(2.19) and the coverage witness stream are out of scope** (m3/m1).
   Nothing here says that 249,878 centres cover; only that the filters and the centre list are
   consistent and complete.
4. (2.8)'s first half is enforced during the X enumeration only; that is what the source does, and
   the paper only claims it there.
5. The Y census used `verdict()` on the multiset, which is legitimate because `sumok`'s six
   directions are order-independent; the code's *order* of testing only affects which direction
   rejects first, not acceptance.

## 7. Files, API, reproduction

```
src/ikernel.py      192-bit integer-interval kernel, pi certificate, e(midpoint) enclosures
src/filters.py      (2.7), (2.8) exact integers; (2.11) six-direction status; (2.14) extend_clip
src/gen_table.py    emits data/tab50_n*.txt (outward-rounded 50-bit tables for the C++ census)
src/census.cpp      complete X/Y census, integer only            (build: g++ -O2 src/census.cpp -o census)
src/probe.cpp       read-only probe over the pristine upstream TU (modes xs, query, gap, extend,
                    share, ydump, pairs)                          (build command in §8)
src/compare_sets.py set comparison vs upstream;  src/sharp_pass.py 192-bit re-decision of survivors
src/retained_pairs.py  §5 retained-centre checks;  logs/  all raw outputs below
tests/test_filters.py  kernel discipline, exact ties, exact-boundary data, N=2..5 controls
```

**API for other members** (all pure Python, no dependencies beyond the stdlib):

```python
import sys; sys.path.insert(0, "<m2>/src")
import filters as F
st = F.SumTest()                              # 112-bin table, ~0.07 s
F.gap_x_ok(bins5); F.gap_y_ok(ybins5, xbins5); F.orientation_ok(bins5)   # exact, booleans
F.gap_num(bins5)                              # exact numerator in units of 1/(2N)
F.SumTest.status(bins5)                       # ('HOLDS'|'FAILS'|'UNRESOLVED', per-direction data)
F.extend_clip(bins5, shared_pos, st)          # (lo, hi, per-direction enclosures) as Fractions
```
`extend_clip` returns an outward enclosure of the feasible shared grid displacement for one list;
intersect the two and test `loA <= hiB and loB <= hiA`. It is the natural input for a reuse checker
that needs the shared coordinate, and for a pair-level completeness checker for any emitted stream.

**Raw logs**: `logs/census_x112.{txt,err}` (22,829 survivors + per-tuple margin),
`logs/census_y112.{txt,err}` (829,306), `logs/census_*_sharp.jsonl` (192-bit slacks),
`logs/probe-xs.txt` (upstream X/Y enumeration, 10.8 MB), `logs/probe-pairs112.txt`,
`logs/rejected_tight.txt` (5,589 tight rejections), `logs/retained_pairs.log`.

## 8. Exact commands run

```sh
cd .ultramath/smwgx3s1v/m2
python3 src/ikernel.py                    # pi certificate + table + mpmath control
python3 tests/test_filters.py             # 25 assertions incl. exact ties and N=2..5 controls
python3 src/gen_table.py
g++ -O2 -march=native src/census.cpp -o census
./census x 112 > logs/census_x112.txt     # 7.5 s
./census y 112 > logs/census_y112.txt     # 343 s
SRC=.../saved-run/compiled-build/source
g++ -std=gnu++17 -O3 -march=native -ffp-contract=off -I"$SRC" src/probe.cpp -o probe
./probe xs 112 > logs/probe-xs.txt        # 21 s; reproduces xs 22829, ys 829306
python3 src/compare_sets.py               # set equality, both enumerations
python3 src/sharp_pass.py x               # 6 s, 0 disputes
python3 src/sharp_pass.py y               # 536 s, 0 disputes
./probe pairs 112 logs/rejected_tight.txt # 67 s; checked 151744086
python3 src/retained_pairs.py             # 547 s; 249,878 centres
```

`build(112)` inside the probe takes 20.9 s, matching the recorded `covrun` build.

## 9. Verdict for the H1 gate

Supported by this direction: the seed-stage **filter block** of Proposition 2.10 has no unresolved
case, no exact-boundary ambiguity, and its accept sets are exactly reproduced in exact arithmetic at
N=112 on the complete enumerations; the pair count 151,744,086 is reproduced; the retained-centre
file is consistent with the filters and with its own (2.14) intervals. Not supported by this
direction: the uniform binary64 error budget (A.3) as a *proof*, and everything downstream of the
filters (coverage, witness stream, later stages).

## 10. Addendum: first-failure vs decisive direction

The C++ census records, for a rejected tuple, the *first* direction in the code's order whose
(2.11) instance is proved violated. The smallest such first-failure violation on the X side is
3.2706e-09, at `(8,29,50,71,78)`. That number is **not** a decision margin of the code: that
tuple's residual-direction margin (+3.27e-09) lies *inside* the code's `1e-8` slack, and the tuple
is rejected on its perpendicular direction for bin 50, where the margin is +6.0e-04. So for this one
tuple out of 160,389,488 the rejection does not rest on the residual direction, and a checker
looking only at `v = c` with a `1e-8` slack would have accepted it. The set equality of §3 shows the
outcome is nevertheless correct in every case (the code evaluates all six directions).

The quantity that bounds how close a *rejection* comes to the `1e-8` comparison slack is
`min over rejected tuples of (max over the six directions of inf mu)`. It is computed here only for
the X enumeration (first-failure statistics above); for the Y enumeration (774,294,080 tuples, and
the six-direction maximum needs the early exit removed) it would cost roughly 20 minutes of CPU and
was **not** run. This is the one number in this direction that a follow-up should fill in.
