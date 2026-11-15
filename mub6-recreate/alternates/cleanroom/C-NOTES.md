# C-NOTES — d6 clean-room probe: the 112-bin seed enumeration from the manuscript alone

Member m5, swarm `smwgt1mbm`, work unit 03 (`seed`, W1, mode A probe). Direction **d6**.

## Clean-room discipline actually observed

I did not open `seed.cpp` or `covout.cpp`, and I did not open any other file of
`.scratch/gh/upstream/`. Everything below was derived from:

| source | used for |
|---|---|
| `attachments/read-this-proof-condense-v9a3/The-maximum-…-September-24-2026.pdf` (text via `pdftotext -layout`) | §2, §2.2, §2.3, §2.4, A.2, A.3 |
| `work/10-recreate/spec/interfaces.md` | the frozen contract (N=112, header, harness facts) |
| `.scratch/gh/data/centers.txt` | the recorded artefact used as the oracle for *data-side* tests |
| `.scratch/gh/covrun.log` | the recorded run's own stdout (`xs22829`, per-10000 progress counters) |

Nothing was compared against a C++ source; the `covrun` binary was **not** run
(one recorded run per session rule; a byte-identical output already exists).

## What the prose fixes (and where)

| rule | text | where |
|---|---|---|
| `N = 112`, `w = 1/N`, closed bins, midpoint `u_b = (b+1/2)/N` | "Set N = 112 and w = 1/N . All bins are closed: I_b = [b/N,(b+1)/N], u_b = (b+1/2)/N" | §2.2, eq. (2.6), p.8 |
| X tuple is weakly increasing, `0 ≤ a ≤ b ≤ c ≤ d ≤ l < N` | "write the five indices for x1,…,x5 as bX = (a,b,c,d,l)" | §2.2, p.8 |
| orientation filter is integral | "The orientation condition implies the necessary integral restriction … a ≤ l−d+1"; A.3: "The orientation filter is integral." | §2.2 (2.7); A.3 |
| `s` = first minimiser | "choose s ∈ {0,…,4} as the first minimizer of ｜2 bX_s + 1 − N｜. This is the rule in seeds::mk." | §2.2, p.8 |
| the gap `mk` computes | "max{(q0+1/2)/N, (q1−q0)/N, …, (q4−q3)/N, 1−(q4+1/2)/N}" | §2.2, p.9 |
| X gap filter | `gx,mid ≤ 1 − (l−1)/N` | Lemma 2.6, (2.8) first |
| pair gap filter (used by covout, re-checked here) | `gy,mid ≥ 1 − (l+2)/N` | Lemma 2.6, (2.8) second |
| `sumok` inequality | `｜v·c｜ ≤ (5πw²/4)‖v‖ + (w/2)Σ_j｜v·J_j｜`, `c=(1+Σe(u_j))/(2πi)`, `J_j=e(u_j)` | Lemma 2.7, (2.10), (2.11); (2.9) |
| `sumok`'s directions | "tests (2.11) in the residual direction **and** in directions perpendicular to the five unit-exponential columns" | §2.3, p.9 |
| `sumok`'s remainder coefficient and margin | "approximates 5π/(4n²) within 10⁻¹⁵. The actual 10⁻⁸ comparison addition…"; "Their slack is 10⁻⁸" | A.3, p.58 |
| what `seeds::build` enumerates | "visits every weakly increasing five-bin X tuple and applies (2.7), the first inequality in (2.8), and sumok. Separately, for every possible first bin it visits all weakly increasing four-bin Y tails and applies sumok." | §2.3, p.10 |
| Y list is stored shared-first, tails sorted | "preserving the stored shared-first ordering"; `bY = (bX_s, bY_1..bY_4)` weakly increasing | §2.2, p.9 |

## What the prose leaves open — and what measuring it says

Each row is a run of `./c-seed_prose <flag>`; see `ms/sensitivity.txt`.

| # | open choice | reading taken | effect on ｜xs｜ | verdict |
|---|---|---|---|---|
| OPEN‑1 | which vectors "directions perpendicular to the five unit-exponential columns" means | for each column `J_t`: `v_t = (−J_t.y, J_t.x)` (unit norm; A.3 "its norm is less than 1.1") | **decisive**: residual only → 30 401; perpendiculars only → 22 838; **both → 22 829** | prose fixes it ("and"), the count confirms the reading |
| OPEN‑2 | the fixed leading phase contributes the `1` of `1+Σe(u_j)` | yes | dropping it → 9 584 | prose fixes it; count confirms |
| OPEN‑3 | **nesting direction** of the five X loops, and of the four tail loops | ascending, **last coordinate outermost**: `for l for d≤l for c≤d for b≤c for a≤b`; tails `for y4 for y3≤y4 for y2≤y3 for y1≤y2` | **none** (set unchanged) | **prose does not fix it** — see below |
| OPEN‑4 | residual direction normalised | `c/‖c‖` | none (22 829 either way) | immaterial |
| OPEN‑5 | the 10⁻⁸ comparison additions | present | none (0 vs 10⁻⁸ gives 22 829 both ways) | immaterial at this grid |
| OPEN‑6 | `expair` (degree-18/19 polynomial) vs libm | libm `cos`/`sin` of `2πu` | none; A.2 bounds the difference by 2·10⁻¹⁴, far below the 10⁻⁸ slack | immaterial for the enumeration, **not** bit-identical |

OPEN‑3 is the real gap, and it is the expensive one: the spec's determinism
register says only "`seeds::build` enumerates (a,b,c,d,e) in nested ascending
loops", which a reader takes for lexicographic. A lexicographic implementation
gets the **right set and the right count** and the **wrong order**, so every
centre index `t` moves and the 7.3 MB file is permuted. Measured on the
recorded file: 5 497 of 249 878 lines have a decreasing `t` under the
lexicographic nesting (`./c-run_d6.sh` step 7), and only one of the 120
permutations of the five letters gives zero violations — `(l,d,c,b,a)`. The
same test on the tails leaves exactly one of the 24 permutations — `(y4,y3,y2,y1)`.

## What my attempt gets wrong

1. **First version: order.** My first dump used lexicographic `(a,b,c,d,l)`
   nesting. Count correct, order wrong (5 497 monotonicity violations), fixed
   by OPEN‑3. This is exactly the failure mode that the *count* check cannot
   see, and it is why the order test above exists.
2. **Unverified content.** 22 829 − 13 557 = 9 272 X tuples of my `xs` are used
   by no recorded centre, so no artefact pins their membership. I verify
   `xs ⊇ observed`, `｜xs｜ = 22 829`, and the order of the observed part; I do
   *not* verify the other 9 272 independently.
3. **Unverified tails.** `ys[h]` is verifiable only for the first bins the
   recorded centres use, `h ∈ [37, 73]` (37 values). The prose does not say
   whether the tails range over all of `[0,N)` — I read it as all — and the
   data cannot distinguish that from a wider-looking restriction that still
   admits every observed tail.
4. **The seed enumeration alone does not explain the centre count.** All
   22 829 X tuples — the 13 557 used *and* the 9 272 unused — have at least one
   Y tail passing Lemma 2.6's second inequality in my `ys`. So the 9 272
   missing centres are rejected later, by `extend`'s interval intersection
   (§2.3, (2.13)–(2.14)), not by the enumeration. That is unit 04's business,
   not this unit's, and it is the first thing I would tell the `covout` owner.

## Result (command, exit status)

    ./c-run_d6.sh            -> RESULT: PASS, exit 0     (log: ms/run_d6.log)

* `xs` = **22 829** entries, matching the recorded run's own `xs22829`
  (`covrun.log` line 1) and its `t<n>/22829` progress lines.
* every one of the **13 557** distinct X tuples in `centers.txt` is in `xs`
  (0 missing), and every stored `s` equals the (2.7) rule (0 mismatches).
* every one of the **76 993** distinct `(h, y1..y4)` tails in the file is in my
  `ys` (368 732 accepted tails over 37 first bins, 255 793 580 tuples visited).
* the pair `(t, position in ys[h])` is **strictly increasing** over all 249 878
  lines (0 violations), and the cumulative centre counts at the run's own print
  boundaries reproduce exactly: t=0 → 5, t=10 000 → 72 679, t=20 000 → 205 716.
