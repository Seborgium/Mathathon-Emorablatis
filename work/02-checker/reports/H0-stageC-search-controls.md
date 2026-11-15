# H0 / Stage C: measured graph statistics, route verdict, certificate format, edge predicates, soundness review

Author: m1 (swarm `smwguhf32`, direction **d5** — completeness audit of the Stage-C branching search by
positive controls). This file is my deliverable for the Q4 Stage-C core. It is a *measurement and design*
document, not a certificate. Everything labelled **measured** was run on this VM; everything labelled
**estimated** states its estimator.

Artefacts in this directory:

| path | what |
|---|---|
| `src/poscontrol.cpp` | positive-control harness; includes upstream `stageC.cpp` verbatim under `STAGEC_HEADER` and drives `graph::clique` / `graph::exist` / `graph::startDuo` on synthetic adjacency. No search code is copied or edited. |
| `src/stageC_probe.cpp` | a *copy* of `saved-run/compiled-build/source/stageC.cpp` (sha256 `60a1b100…`) with three insertions: an `abort()` trace macro, a per-record `PROBE`/`SEARCH` dump, and an optional adjacency dump. The search and the predicates are untouched. |
| `src/brute_check.py` | independent Python implementation of the *definition* (6.24); used to cross-check real Stage-C graphs. |
| `src/arith_bench.cpp`, `runs/arith_bench.txt` | outward-arithmetic unit-cost benchmark (double / long double / double-double / interval⟨dd⟩) behind §2.2's conversion factors. |
| `runs/VERIFY.md` | the archive's own `VERIFY.md`, which states that result files carry only numerical counters (see §1.1 item 5). |
| `runs/results/C.*.txt` | the 92 archived Stage-C summary files, fetched from `verification/saved-run/execution/results/`. |
| `runs/probe_f0.txt` | per-record measurements, 256 records of `batches/f0.bin`. |
| `runs/probe_hard.txt`, `runs/probe_hard2.txt` | per-record measurements of all 163 cap-hit records, cap raised to 2·10⁸. |
| `runs/probe_mode0.txt`, `runs/probe_mode2.txt` | same 64 records under `searchMode=0` and `searchMode=2`. |
| `runs/poscontrol.txt` | positive-control output. |
| `runs/brute_check.txt` | Python brute-force output on four real records. |
| `runs/g0.txt, g30.txt, g37.txt, g38.txt` | dumped O/U adjacency of four real records (for the independent check). |

Provenance check: `saved-run/compiled-build/source/stageC.cpp` is **byte-identical** to the cached
`.scratch/gh/upstream/stageC.cpp`, sha256 `60a1b10091852809f523d4f5cc70abb28ebe8d7ed691843e7a2d73e9bbd7caae`.
Build used is `build.sh`'s line for `crun`: `g++ -std=gnu++17 -O3 -march=native -ffp-contract=off`.

---

## 1. Measured graph statistics of the recorded run

### 1.1 What the archive actually contains (measured, complete)

`execution/results/C.*.txt` holds 88 initial-batch files (`C.batch0…87`), 4 final-pass files
(`C.final0…3`) and 1 fallback file (`C.Bfallback.txt`). Parsing every `result` line gives, exactly:

| pass | records `done` | `bad` | `graph` | `cap` | `over` | `cluster` |
|---|---|---|---|---|---|---|
| initial (`C.batch*`) | **22,379** | **163** | **0** | **163** | **0** | **0** |
| final (`C.final*`) | **1,127** | **0** | 0 | 0 | 0 | 0 |
| total | **23,506** | 163 | 0 | 163 | 0 | 0 |

Consequences, all read off the archive (no inference):

1. **Every `bad` record is a cap hit.** `bad == cap` per batch (15 of 15 non-empty batches agree) and
   `graph == over == cluster == 0` everywhere. There were **no** positive patterns, **no** bin-cap
   overflows and **no** clustering failures in either pass.
2. **The cap fired on 163 of 22,379 records = 0.73 %** of the initial pass. Those 163 are unresolved by
   pass 1; the negative conclusion for them comes only from the fallback: `C.Bfallback.txt` reports
   `result 1127 bad 0 parent163 …` — 163 parents re-refined by Stage B at `(τ,w)=(.011,.0038)` into
   1,127 records, all of which pass 3 excludes with `cap=0`.
3. **The published Stage-C conclusion therefore rests on 23,343 completed negative graph searches**
   (22,216 in pass 1 + 1,127 in pass 3). The 163 pass-1 cap hits are *superseded*, not re-used: their
   exclusion is carried by the 1,127 pass-3 records. No exclusion anywhere rests on a cap.
4. The 15 non-empty `bad*.bin` files contain exactly **163 records** — verified by parsing them
   (29+32+23+16+14+13+6+2 = 135 in eight files, plus 4+5+8+4+1+2+4 = 28 in seven more). This
   independently corroborates the 163 of the counters.
5. `avg bins` / `avg balls` **are not in the archive**: the archived progress lines stop at
   `(graph… cluster…)`, although `stageC.cpp:553` prints `avg bins%.0f balls%.0f time %.1f` after it.
   This is by design, not a discrepancy: `saved-run/VERIFY.md` states that the command and result files
   "contain only relative program/data names, mathematical arguments, completion/exit facts, and numerical
   counters. Timing, PID, host, absolute-path, resource, and provenance fields are not required"
   (`runs/VERIFY.md`), and `check_records.py:198` accepts exactly that short form with `re.fullmatch`.
   So the per-record work statistics were cleaned out of the result files rather than never produced.
   Counts are unaffected — I reproduce `C.batch0.txt` exactly below — but the paper's per-record
   bins/balls/steps cannot be read off the archive, which is why section 1.2 re-runs a batch.

### 1.2 Node counts, edge counts, densities (measured on a real batch)

`batches/f0.bin` (256 records, all `k=4`, all `radius=.016`) re-run with the recorded parameters
`crun 12 4 1 .042 1 1 5000000 0 1`. My run prints
`result done256 bad0 (graph0 cap0 over0 cluster0)`, i.e. **it reproduces `C.batch0.txt` exactly**
(0 of 256 excluded by cap, overflow or cluster failure; 256 negatives). Per record (`runs/probe_f0.txt`):

| quantity | min | p25 | median | p75 | p95 | max | mean |
|---|---|---|---|---|---|---|---|
| balls `M` | 180 | 213 | **239** | 265 | 285 | 305 | 239.2 |
| O edges | 1,530 | 2,039 | **2,613** | 3,502 | 5,175 | 6,257 | 2,890 |
| U edges | 7,388 | 10,005 | **12,371** | 14,543 | 16,844 | 18,417 | 12,380 |
| max O-degree | 25 | 32 | 39 | 55 | 85 | 96 | 45.3 |
| max U-degree | 102 | 129 | 151 | 166 | 179 | 193 | 147.1 |
| O density | 8.2 % | 8.9 % | **9.3 %** | 10.2 % | 12.7 % | 14.7 % | 9.8 % |
| U density | 39.3 % | 41.9 % | **43.2 %** | 44.5 % | 45.8 % | 46.5 % | 43.1 % |
| #O-6-cliques | 0 | 0 | **0** | 1,352 | 412,318 | 1,110,045 | 47,421 |
| search steps | 13,570 | 21,476 | **32,944** | 74,570 | 479,468 | 1,042,869 | 95,106 |
| search time | 0.2 ms | 0.3 ms | **0.5 ms** | 5.0 ms | 23.7 ms | 55 ms | 4.4 ms |

Two structural facts matter for the certificate design:

* **U is dense (≈43 %) and O is sparse (≈9 %).** Consequently the U-side certificate ideas are useless:
  the **U 6-core is the whole vertex set in all 256 records** (nothing peels), so "U has no K₆,₆ because
  U is 5-degenerate" cannot fire. I checked this deliberately; it is a dead end (posted to the board).
* **162 of 256 records have no O-6-clique at all**, and the remaining 94 have up to 1.1·10⁶ of them. So
  a "list every O-6-clique and check the pairs" certificate is not compact: at 12 bytes per clique (six
  16-bit labels) the worst f0 record alone needs ≈ 13 MB, and a dense cap-hit record with 1.45·10⁸
  cliques ≈ 1.7 GB; the *completeness* of such a list still needs a search. Dead end too. The obstruction
  is on the O side (`A`,`B` must each be 6-cliques of a 9 %-dense graph), not on the U side.
* **The certificate can be stratified, and two thirds of it is much cheaper than the paper's criterion.**
  In this batch (6.24) is a strengthening of the simpler statement "`O` has no 6-clique": for 162 of 256
  records `ω(O) ≤ 5`, so no candidate basis exists at all and the U graph is irrelevant. `exist` decides
  that without ever reaching the second pool, which is why those records take a median 2.4·10⁴ steps
  against 1.0·10⁵ for the rest. Only the 94 records
  with `ω(O) ≥ 6` need the second pool. A checker should report which reason fired per record, because
  "no O-6-clique" is a far weaker claim to audit than "no two U-complete disjoint O-6-cliques".

### 1.3 The 163 cap-hit records (measured, all of them)

Re-running all 163 with the cap raised to 2·10⁸ (`runs/probe_hard.txt`, `runs/probe_hard2.txt`):

| quantity | value |
|---|---|
| balls `M` | 260 – **1,089** (median 299) |
| O density | 14.5 % – 30.3 % (median 25.0 %) — about 2.7× denser than the f0 batch |
| U density | 37.6 % – 53.5 % (median 39.7 %) |
| #O-6-cliques | 1.39·10⁵ – 1.45·10⁸ (median 3.5·10⁷) |
| steps at cap 2·10⁸ | **5,077,605 – 39,968,282** (median 10,052,292; p90 19,732,679) |
| gaveup / positives | **0 / 0** — every one of the 163 *completes* and returns negative |
| total search work | 1.925·10⁹ steps, **68.2 s** single-threaded |

So the 163 "unresolved" records were **not** genuinely hard: they are 1.02×–8.0× over the 5·10⁶ cap, and
raising the cap to 4·10⁷ resolves all of them. This is a costed alternative to the published fallback:
one pass at `capsSteps = 4·10⁷` costs ≈ 68 s more than the 5·10⁶ pass and removes the entire
163-parent → 1,127-record Stage-B/Stage-C fallback. (Measured end-to-end check of the accounting: I also
re-ran one of them at the recorded cap and got `steps 5000001, gaveup 1` → `(graph0 cap1)`, matching the `cap29`
counter in `C.batch52.txt` for that batch.)

### 1.4 Per-record steps for the rest of the run: estimate, not measurement

Only 256 + 163 = 419 records were re-run (1.8 % of the 23,506 record instances). For the remaining 21,960 records the estimator is
"f0 batch mean × count", and it is biased: 163 of those records are known to be ≈ 10⁷ steps, not 10⁵.

* total Stage-C search work ≈ 23,506 × 9.5·10⁴ ≈ 2.2·10⁹ steps (f0 mean), of which 1.9·10⁹ is the
  measured hard set — so ≈ 2.4·10⁹ steps ≈ 90 s single-threaded;
* total O/U edges ≈ 23,506 × 2,613 ≈ 6.1·10⁷ and 23,506 × 12,371 ≈ 2.9·10⁸;
* the unmeasured part is validatable in ≈ 46 CPU-min of binary64 work by re-running all 88 batches with
  the probe (0.117 s CPU/record). I did not spend that here (measurement phase).

---

## 2. Route verdict, with numbers

### 2.1 The search is complete: this is what makes route (a) a certificate rather than a re-run

Lemma 6.8's proof is correct as a description of the code, and I checked the code line by line against it.
The two-pool enumeration is: base 1 = 6-clique of `O` built vertex-by-vertex in increasing index order
with pools intersected (`stageC.cpp:428-451`), base 2 = `clique(pool,6)` on the intersection of the `U`
neighbourhoods of all six base-1 vertices (`stageC.cpp:416-426`). Completeness has three load-bearing
points, each of which I checked by construction rather than by reading:

1. **Every configuration is reached.** For any `(A,B)` satisfying (6.24), let `a = min(A∪B)` and swap
   names so `a ∈ A`. The root loop tries roots in increasing order and maintains
   `u ← u \ {tried root}` cumulatively, so at root `a` the second pool still contains all of `B`
   (`u.del(i)` at `stageC.cpp:433` mutates the local copy, which is *intended*: every deleted vertex is
   smaller than `a` and hence in neither `A` nor `B`). Recursively, pools are intersected with
   `O(i)`/`U(i)`, which every remaining member of `A`/`B` satisfies.
2. **Disjointness is enforced only by the absence of `U` self-loops.** Base-1 vertices are removed from
   the second pool because `v ∉ N_U(v)`, *not* by an explicit deletion — except for the root vertex.
   **Demonstrated**: build 12 labels, 0–10 complete in both graphs, `U[5][5]=1`, 11 isolated. The
   definition (6.24) has no solution (needs 12 usable labels); the search returns **true**, reusing label
   5 in both bases (`runs/poscontrol.txt`, line `SELFLOOP brute0 search_mode1=1`). `pairtest` never sets
   the diagonal, so the real run is safe — but this is a hypothesis a checker must *assert*, not assume.
3. **The mode-1 prune is exact.** `clique(pool,6)` before recursing (`stageC.cpp:439`) can only reject a
   pool that genuinely has no 6-clique, and later intersections only shrink it. Measured: on 64 real
   records, `searchMode=0` (no prune) and `searchMode=1` produce **identical step counts** (6,244,180
   each) and the same answers, i.e. the prune is inert on this data; `searchMode=2` (`duo`) costs 8.8 %
   more steps and gives the same answers.

Positive controls (`src/poscontrol.cpp`, `runs/poscontrol.txt`):

* **400 random instances**, `M = 12…15`, O density 15–70 %, U density 15–100 %, half of them seeded with
  a planted (6.24) pattern: `mode 0`, `mode 1`, `mode 2` all agree with a definitional brute force that
  enumerates every O-6-clique and every disjoint pair. **0 mismatches** (200 pattern / 200 no-pattern).
* **Planted patterns at production scale**, `M = 12, 64, 128, 256, 512, 1024`, planted vertices pushed to
  the *end* of the index order (the worst case for least-vertex branching), sparse O (15 %) and
  moderate U (40 %): 54/54 runs found the pattern, worst 3.24·10⁶ steps.
* **Cap semantics**: with `capSteps ∈ {200, 5000, 100000}` the run stops at exactly `cap+1` steps with
  `gaveup=1` and is classified `unresolved(cap)` — never positive, never negative. `tick()` returns
  *true* (i.e. "found") on exhaustion (`stageC.cpp:412-415`), so safety rests entirely on `gaveup`
  being consulted at `stageC.cpp:487` (`return q || gaveup;`) and `stageC.cpp:527-529`.
* **Independent check on real graphs**: for four real records (indices 0, 30, 37, 38 of `f0.bin`,
  0 / 1,997 / 326 / 1,344 O-6-cliques) the Python implementation of the definition — enumerate all
  O-6-cliques as bitmasks, then test every disjoint pair for all 36 U-entries — returns **no pattern**,
  agreeing with the C++ search, and reproduces the clique counts exactly.

### 2.2 Route (a): a small independent checker, exhaustive per record — FEASIBLE

The checker re-derives, for each of the 23,506 record instances: (i) the retained bins and their
clustering into balls (Lemma 6.4 covering), (ii) the O/U adjacency from the edge predicates of §4,
(iii) the pattern search. **The following is a measurement of the generator's own binary64 work** — it is
what stageC.cpp costs, not what an exact-arithmetic checker costs:

| stage | per record | 23,506 records (binary64) |
|---|---|---|
| bins + balls + O/U adjacency (0.117 s CPU, dominated by ≈ M²/2 ≈ 2.9·10⁴ pair tests at `M≈239`) | 0.117 s | **≈ 46 CPU-min** |
| search, f0-like records (1.12 s per 256 records) | 4.4 ms | ≈ 100 s |
| search, the 163 dense records (68.2 s measured at cap 2·10⁸) | 0.42 s | 68 s |
| **total, single-threaded, binary64** | | **≈ 47 CPU-min** (≈ 12 min on 4 cores) |

**Exact / interval arithmetic is a different number.** The pair test is a flop-bound kernel (a 12×12
in-place elimination plus six 6-term dot products and a square root, `graph::joint`), so the conversion
factor can be measured on that kernel rather than guessed. `src/arith_bench.cpp` times the same kernel in
four arithmetics (`runs/arith_bench.txt`, this VM, `-O3 -march=native -ffp-contract=off`, 12×12, 0.4 s per
measurement):

| arithmetic | µs per kernel call | factor | route (a) extrapolated |
|---|---|---|---|
| `double` (53-bit, the generator) | 0.655 | 1.00 | **46 CPU-min** (measured) |
| `long double` (x87, 64-bit significand) | 6.64 | 10.1 | ≈ 7.8 CPU-h |
| double-double (Dekker, ≈106 bits) | 10.06 | 15.4 | ≈ 11.8 CPU-h |
| interval ⟨double-double⟩ (two endpoints) | 19.68 | 30.1 | ≈ 23.0 CPU-h |

So the honest statement is: **46 CPU-min in binary64, ≈ 8 CPU-h in 80-bit arithmetic and ≈ 23 CPU-h
single-threaded in outward-rounded double-double intervals (≈ 6 h on 4 cores)**, and a rational-arithmetic
checker would be worse still and was not benchmarked. Two caveats on the extrapolation: it multiplies the
*measured* call count by a kernel factor, so it is not a measurement of a full interval checker; and it
assumes the interval version needs no extra calls (a branch-and-bound variant over `detail` iterations
could need more). The ball/bin stage uses `expair`, a 14-term polynomial, so the same flop factor should
carry over there; no trigonometric library calls occur per pair.

With `capSteps ≥ 4·10⁷` (or no cap and a progress bound) no record is left unresolved. That is cheap
enough that the H0 gate should treat route (a) as the default: the whole Stage-C layer can be re-checked
in one machine-day at worst, and the only trust placed in the generator is that the ball centres and radii
it wrote down cover the retained bins.

What the checker must not inherit: the generator's *clustering* (any covering by balls with `s<.1` is
admissible, so the checker may re-cluster freely), the generator's search order (any complete search is
fine), and the generator's arithmetic (see §4).

### 2.3 Route (b): DRAT/LRAT refutation — feasible in principle (≈ 2.4·10⁹ clauses), not built

The natural encoding is exact: variables `x_{v,1}, x_{v,2}` (vertex `v` in base 1 / base 2), clauses
`¬x_{u,1} ∨ ¬x_{v,1}` for each non-O pair and `¬x_{u,2} ∨ ¬x_{v,2}` likewise, `¬x_{u,1} ∨ ¬x_{v,2}` and
`¬x_{v,1} ∨ ¬x_{u,2}` for each non-U cross pair, `¬x_{v,1} ∨ ¬x_{v,2}` (disjointness), plus exactly-six
cardinality per side (sequential counter). The CNF is satisfiable iff (6.24) holds, provided the
cardinality encoding is the standard propagation-complete one; then UNSAT is a refutation. Least-vertex
branching maps to a tree-like resolution refutation whose size is the number of branch nodes, i.e. the
`steps` counter: measured median 3.3·10⁴, max 4.0·10⁷ per record, ≈ 2.4·10⁹ clauses over the run
(≈ 10–20 GB of DRAT text at ≥ 5 bytes/literal), and a DRAT check whose cost is of the same order as
several full re-runs. I did **not** build this route (that is d1's/d2's line); my contribution is the
number the gate needs. Like for like: route (a) costs 46 CPU-min in binary64 or ≈ 23 CPU-h in interval
arithmetic (§2.2); route (b) costs a ≈ 2.4·10⁹-clause proof plus a DRAT check. On this data (a) wins on
cost either way; (b) wins only on the trust placed in a formally verified DRAT checker, and the right use
of the resolution/log idea here is the *optional trace* of §3.4, needed only if the checker's own search
is not to be trusted.

### 2.4 If neither is accepted: the smallest weakening that is still a certificate

A trace-checking checker (route a′): the certificate carries, per record, the sequence of branch
decisions of the search (depth, vertex index, and a one-byte reason code for every prune: pool too small,
no auxiliary 6-clique, completed search). The checker replays it against its own adjacency: each prune
reason is a local claim it verifies (a bitset cardinality or a `clique(pool,6)` call), the depth sequence
must be a complete depth-first traversal, and the final count of explored branches must equal the number
of leaves. Cost: the same ≈ 46 CPU-min of binary64 adjacency work (unavoidable — the adjacency is where the
geometry enters) plus a linear trace replay; trace size ≈ `steps` bytes ≈ 100 KB/record, ≈ 2.4 GB for the
run, so it is worth storing only for the 163 dense records (≈ 1.9 GB) or for an audited sample.

---

## 3. Certificate format for Stage C

One archive, one JSON manifest, one binary stream. Everything is little-endian; integers 64-bit; `double`
IEEE-754 binary64. The manifest pins: preprint sha256, the seven source sha256s, build line, the
`(M, layers, linear, RB, detail, searchMode, capSteps)` tuple actually used (`12 4 1 .042 1 1 5000000`),
the CPU/libm probes, and the sha256 of the record stream.

### 3.1 Record stream (unchanged from §7.1; the format is fully pinned by `atlas.cpp:191-215`)

8-byte count, then per record: `int32 k`, `double p[36]` (row-major phases in cycles), `double T[k][36]`,
`double values[8] = (C, n0, id, ort, hor, mnorm, froot, radius)`. Size `356 + 288k` bytes. 23,506 records
at measured `k=4` ⇒ 1,508 bytes each. For Stage C the radius is `.016` (passes 1–2) or `.011` (fallback).

The **shared Hadamard displacement** `η` of (6.23) is never stored: it enters only through its bound
`r_H = √(1+ort)·r + 1e-9`, derived from the record's own `ort` and `radius`. The checker must recompute
`r_H` from the record (and, for the layer tests, `r_t = √(1+ort)·r + 1e-9` and
`r_n = n0 + id·r + C·r² + 1e-9`, `stageC.cpp:502-505`), so a certificate that omits `ort` is
un-checkable. Every per-record scalar the checker needs is therefore in the 8 stored doubles.

### 3.2 Ball layer (new; the generator's clustering is a *hint*, not a proof)

Per record: `int32 M`, then `M × (double v[6], double s)` — the closed vector ball `B_vec(v,s)` of (6.14),
centre in cycles, radius in the same units. Invariants the checker must establish, and may establish by
*re-clustering itself* if the declared list fails:

* `0 ≤ s < .1` and `|v_j| ≤ 2` for every ball (else: unresolved, `stageC.cpp:219-220`);
* **covering**: every retained bin midpoint `u` (computed by the checker from its own layer run) is within
  `s` of some centre after subtracting the coordinate wraps and the mean — Lemma 6.4's `h`, i.e.
  `‖h(u,v)‖ + X_M ≤ s` with `X_M = √(29/6)/(2M_k)` at the last grid;
* `M ≤ 2048` (`cluster` cap) and `M ≤ 2048` is also the hard bitset limit (`BS::L=32` words).

### 3.3 Edge layer

Per record, a full adjacency matrix per graph: `M` rows of `ceil(M/64)` 64-bit words, i.e.
**256 bytes per row per graph at `M=2048`** (32 words of 8 bytes) and 512 bytes per row counting both
graphs, so the total for `O` and `U` is `2 · M · ceil(M/64) · 8` bytes — **15,296 bytes at the measured
median `M=239`** and **1,048,576 bytes (1 MiB) at the hard limit `M=2048`**. Over the 23,506 record
instances that is ≈ 0.36 GB at `M≈239` (≈ 24 GB only if every record sat at the 2048 limit, which none
does; the measured maximum is `M=1089`, i.e. 313,632 bytes). Three asserted invariants: **diagonal zero**
(§2.1, point 2 — measured to be load-bearing), symmetry, and all bits `≥ M` zero. Non-edges are the content; over-approximating edges is sound, so a checker may
recompute and take the union of its own and the declared adjacency, and must reject if the declared set
is missing an edge its own arithmetic retains.

### 3.4 Verdict and witness

Per record, one of six values, in three groups that must not be conflated:

* **excluded** (both are legitimate completed exclusions): `NEG` = completed negative search, and
  `EMPTY_BINS` = the completed bin layer is empty, which is the *first* of the two negative paths in
  `negative()` (`stageC.cpp:520`) and is just as much a finished exclusion as `NEG`;
* **not excluded**: `POS` = a (6.24) pattern was found, i.e. the record survives and needs the fallback or
  a human decision. It is *not* an unresolved outcome and must not be counted with the next group;
* **unresolved**: `CAP`, `OVERFLOW`, `CLUSTER_FAIL`, and any internal failure (`INTERNAL`); no verdict, the
  record stays open.

For `NEG` the *witness is the checker's own complete search* (§2.1) — no per-record pattern data is
needed; for `EMPTY_BINS` the witness is the checker's own bin layer being empty. For `POS` the witness is
12 ball indices `(a_0…a_5, b_0…b_5)`, verified directly against the adjacency (15+15 O edges and 36 U
edges, no search needed). Optionally, per record, the branch trace of §2.4 (≈3 bytes per node) for
trust-minimal checking.

A record's Stage-C conclusion holds when its verdict is `NEG` or `EMPTY_BINS`; a batch's is the
conjunction; the archive's is the conjunction over 23,506 record instances with `POS`, `CAP`, `OVERFLOW`,
`CLUSTER_FAIL` and `INTERNAL` all counted and reported (the archive has `POS = CAP = OVERFLOW =
CLUSTER_FAIL = 0` in pass 3 and 163 `CAP` in pass 1, superseded by the fallback).

---

## 4. Edge predicates the checker must re-evaluate

All are *necessary* conditions, so the checker may evaluate them in exact rational or outward-rounded
interval arithmetic and must retain the edge when the comparison is inconclusive. `stageC.cpp`'s binary64
version and the paper's margins are: radius sum `+1e-10`; distance tests `(6.16)` a further `2e-7`; `E_O`,
`E_U` `+2e-8`; `(6.20)`,`(6.21)` a further `2e-7`; `(6.23)` `+3e-7` (§6.7 of the paper).

| test | paper | inputs needed | code |
|---|---|---|---|
| direct O / U distance test | (6.16) with (6.15): `Q_j = e(u_j−v_j)`, `S = Σ Q_j`, `r_e = s_u+s_v`, `z = x_u−x_v`; reject O if `|S|/(2π√6) > r_e`, reject U if `||S|/√6−1|/(2π) > r_e` | two ball centres `v` (6 phases each) and radii; 6 complex exponentials per pair | `pairtest` `stageC.cpp:368-379` |
| O direct support | (6.20) `|S|²/(2π) ≤ 6 r_e ‖D_U‖ + E_O |S|`, `E_O = π r_e²` | `D_U` from (6.17) with `Re S, Im S`; `‖D_U‖` | `stageC.cpp:386-392` |
| U direct support | (6.21) `|q_U| ≤ r_e ‖D_U‖ + E_U`, `q_U = (|S|²/6−1)/(4π)`, `E_U = π r_e²(1+|S|/6)` | same | `stageC.cpp:394-399` |
| O joint test | (6.23) with `ℓ=2`, `q_O = (Re S, Im S)/(2π)`, `D_O` from (6.17); `E_t^ball(y)` from (6.22) | per ball: `c_i`, `J[i][j]`, `B[i][k] = Σ_j J[i][j] T[k][j][i]`, `S_i` (all derived from the centre and the record's `p`, `T`, `k`); the shared Hadamard tangent displacement `η`, bounded by `r_H = √(1+ort)·r + 1e-9`; the per-record constants `K = 1.00001`, `r`, `rt = √(1+ort)·r + 1e-9`, `rn = n0 + id·r + C·r² + 1e-9` | `graph::joint<2>` `stageC.cpp:308-359` |
| U joint test | (6.23) with `ℓ=1`, `q_U` from (6.19) | as above | `graph::joint<1>` |

The checker also needs the *layer* constants for the bin stage (6.7)/(6.11)/(6.12) — `(p, K, r, rt, rn)`
plus `X_M, L_M, I_M` — but those decide *which bins survive*, hence which balls exist, not the edges.

Two implementation traps that the format must pin, because they change the graph:

* `detail` (`0` makes `joint` return true, i.e. every pair an edge, `stageC.cpp:309`) — the run used
  `detail=1`; a checker must use the recorded value;
* `searchMode` (`1` in the run) and `capSteps`. Mode 0/1/2 agree on my 400 random instances and on 64
  real records, but the *certificate* must state the mode so that the trace, if any, replays.

---

## 5. Soundness review: what the certificate must contain, and the defects I found

The certificate must make each of the following unrepresentable rather than merely unlikely.

1. **A cap that reads as a negative.** `tick()` returns *true* on exhaustion (`stageC.cpp:412-415`), so the search's return value
   is meaningless once the cap fires; only `gaveup` distinguishes. Verified by construction (steps are
   exactly `cap+1`, `gaveup=1`), and verified on a real record (cap 5·10⁶ on `bad52` #0 →
   `steps 5000001 gaveup1` → `graph0 cap1`, matching `C.batch52.txt`). **Certificate requirement**: the
   verdict is a 6-valued field, not a bool, and `CAP` is never `NEG`.
2. **A search that cannot find what exists.** Positive controls are the only defence; the run has none.
   Mine: 200/200 planted patterns found, 54/54 at scale, 0/400 disagreements with brute force. The
   capability is real, and the search's completeness is also proved (Lemma 6.8, checked in §2.1).
3. **A silent reliance on loop-freeness — a certificate hypothesis, not a defect in the archived run.**
   Demonstrated: the search accepts a 12-label configuration that reuses a label if `U` has a self-loop
   (`runs/poscontrol.txt`: `SELFLOOP brute0 search_mode1=1`), because non-root base-1 vertices leave the
   second pool only through `v ∉ N_U(v)`. The archived run is unaffected: `pairtest` writes `O`/`U` only
   for `i ≠ j` (`stageC.cpp:391,399`), so both graphs are loop-free by construction, and the paper's
   Lemma 6.8 proof states the hypothesis explicitly ("the lack of U self-loops also removes every
   selected first-clique vertex"). What is missing is only that **the certificate must carry it**: assert
   `diag(O) = diag(U) = 0` and check it, so that a checker cannot be handed a loop-carrying adjacency.
4. **Clustering failures and the merge no-op.** Measured: `cluster = 0` and `over = 0` in all 92 archived batches,
   so no exclusion rests on a failed clustering. The F2 defect (merge impossible for `M ≤ 50`, and a
   non-monotone cut-off at `M < 26`) is visible in the data: with `M_k = 12, 24, 48, 96` the ball counts
   are 180–305, i.e. clustering is at best a mild compression at the coarsest grids. It is
   **soundness-neutral** — the covering lemma does not need merges, and a bin that fails its cut-off
   becomes its own centre — but it *does* inflate `M`, hence the `M²` pair-test cost that dominates
   route (a) (§2.2). The certificate must therefore carry the ball list (or let the checker re-cluster)
   and check the covering, not count centres.
5. **Sentinel/value overloading inside the run.** `detail=0` (above); `BS::first()` calls `abort()` on an
   empty set (`stageC.cpp:293-294`) — unreachable given the call sites, but an `abort()` is not a verdict;
   `graph::init()` calls `abort()` if `words > 32` (`stageC.cpp:404`), and since `cluster` caps at 2048
   centres this is unreachable only by an implicit coupling between two constants in different stages.
   A checker should classify these as `INTERNAL` failures, never as exclusions.
6. **Unresolved bookkeeping in the archive.** 163 records were unresolved in pass 1 and only pass 3
   negatives them; the paper's Table 1 must present the composite (22,379 + 1,127 records, 163 cap hits,
   0 overflow, 0 cluster failures), because a reader who sees only "0 unresolved" for the initial pass is
   reading a different run. **Measured**: 0.73 % of pass-1 records hit the cap, and all of them complete
   at cap 4·10⁷ (§1.3) — so the honest cost of a cap-free single pass is ≈ 68 s, and the fallback was not
   necessary.
7. **The one thing a checker cannot re-derive**: the ball centres/radii cover the retained bins. If the
   checker re-clusters from its own bin run, it inherits nothing from the generator except the record's
   constants — which is the design in §3.2, and why the ball list is a hint.

**Findings with file:line evidence** (S1 is a hypothesis the certificate must carry, not a defect of the
archived run; S2–S5 are code-level defects, all soundness-neutral for this run):

| # | evidence | status |
|---|---|---|
| S1 | `graph::exist` relies on `v ∉ N_U(v)` for the non-root base-1 vertices (`stageC.cpp:433` deletes only the root); my self-loop instance makes it return a false positive | **hypothesis, not a defect**: the run is loop-free because `pairtest` sets `O/U` only for `i≠j` (`stageC.cpp:391,399`); the certificate must assert `diag = 0` |
| S2 | `tick()` returns `true` on cap exhaustion (`stageC.cpp:412-415`); a caller that ignores `gaveup` would read "found" | safe in the run (`stageC.cpp:487`, `527-529`); certificate must carry a 6-valued verdict |
| S3 | 163 cap hits (0.73 %) not characterised in the archive; no per-record `steps`, no `avg bins`/`avg balls` (progress line truncated in `results/*.txt` vs `stageC.cpp:553`) | measured here (§1.3): max 3.997·10⁷ steps, all complete |
| S4 | `graph::init()` `abort()` when `words > BS::L` (`stageC.cpp:404`), reachable only if `cluster`'s 2048 cap (`stageC.cpp:204`) were retuned upward | latent coupling; classify as `INTERNAL` |
| S5 | F2 merge no-op at `M ≤ 50`: confirmed indirectly — `M = 180…305` balls per record at grids 12/24/48/96, so no compression at the coarse grids; `cluster` returns `false` at 2048 centres (`stageC.cpp:204`) and on a bad radius (`stageC.cpp:219-220`) | soundness-neutral, cost-relevant |

---

## 6. What I did **not** verify

* I re-ran 419 of 23,506 records (256 from `f0.bin`, all 163 cap-hit records). The other 21,960 records'
  graph statistics are an estimate (§1.4); the estimator is the f0 mean.
* I did **not** re-implement the edge predicates in exact/interval arithmetic, and I did **not** check
  that `pairtest`/`joint` implement (6.16)/(6.20)/(6.21)/(6.23) faithfully. §4 is a reading of the code
  against the paper, not an independent evaluation. That correspondence is the largest remaining risk in
  Stage C and belongs to the predicate/differential-testing line (d1).
* I did **not** build route (b) (DRAT/LRAT); §2.3 gives the encoding and a size estimate only.
* I did **not** verify the record stream's Root constants against (4.4)/(4.15) — I take the 23,506 records
  as given by the archive.
* My "independent" check on four real records uses stageC's *adjacency*; only the pattern decision is
  independent. An adjacency-level independent check needs the interval implementation, which I did not
  write.
* I did not test the fallback records (`fb1.bin`, 1,127 records) — they are f0-like in shape but
  `radius = .011`, so their `M` and pair counts will be smaller; the 46 CPU-min binary64 estimate assumes
  f0's measured cost, which is therefore an upper bound for them.
* The interval-arithmetic figures in §2.2 are a *kernel* benchmark (measured factors 10.1×/15.4×/30.1×
  applied to the measured binary64 call count). I did **not** implement an interval version of `pairtest`
  or the checker, so the 8/12/23 CPU-hour numbers are extrapolations with a stated unit-cost factor, not
  end-to-end measurements. The double-double 12×12 solve is the only place where the factor could move
  materially (division and square root dominate it).
* Compute used for this document: ≈ 7 CPU-min on this VM (256-record pass 31 s, 163 hard records 68 s,
  two 64-record mode passes, controls < 5 s, Python brute force 5 s), noted on the board.

---

## 7. Bottom line for the gate

1. The recorded Stage-C conclusion consists of **23,343 completed negative graph searches** (22,216 in
   pass 1 + 1,127 in pass 3). Of the 22,379 pass-1 records, 163 (0.73 %) were unresolved at the 5·10⁶ cap
   and were resolved only through the Stage-B fallback; there were **no** overflows, **no** clustering
   failures and **no** positives anywhere.
2. The searches are **not expensive**: median 3.3·10⁴ steps (0.5 ms), and the hardest record needs
   4.0·10⁷ steps. A cap of 4·10⁷ resolves all 163 without the fallback (≈ 68 s).
3. **Route (a) is the recommendation**: an independent checker that recomputes bins, balls, adjacency and
   runs a complete two-pool search needs no per-record witness, and its cost is **46 CPU-min for the whole
   run in binary64** (the measured generator cost: ≈ 45 of it in the M² pair tests, not in the search),
   **≈ 8 CPU-h in 80-bit and ≈ 23 CPU-h in outward-rounded double-double intervals** — measured kernel
   factors 10.1× and 30.1×, §2.2. Per record it should record which exclusion fired — "empty bin layer",
   "no O-6-clique" (63 % of the sampled batch) or "no U-complete disjoint pair" (the rest). The search it
   runs is the paper's own algorithm, whose completeness I checked line by line and whose behaviour I
   verified against a definitional brute force on 400 synthetic and 4 real instances, plus 254 planted
   patterns.
4. The certificate must carry the six-valued verdict, the loop-free adjacency invariant, the ball layer
   with its covering check, and the `detail`/`searchMode`/`capSteps` parameters. With those, caps,
   clustering failures, the merge no-op and sentinel values cannot turn into exclusions.
