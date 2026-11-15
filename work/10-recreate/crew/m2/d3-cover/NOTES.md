# NOTES — cover unit (direction d3), team C / m2

Scope: re-derivation of `covout.cpp` (SI, extend, cent, indexed, coverSeeds) plus the
`seed.cpp` core it consumes (Lattice, expair, hp, xy, sumok, mk, Seeds::build).
Files: `c-cover.hpp` (unit), `c-seedcore.hpp` (its only dependency), `c-covrun.cpp`
(program contract), `c-harness.cpp` (experiments), `c-fixture.cpp` (bit-level fixture),
`c-verify.py` (file comparison), `c-build.sh`.

Every choice the frozen spec does not fix is listed below with the line of source that
decided it. Line numbers are upstream (`.scratch/gh/upstream/`).

## B1. Arithmetic core

| # | choice | decided by |
|---|---|---|
| B1.1 | `pi = 0x1.921fb54442d18p+1` (binary64), not `acos(-1)` | seed.cpp:12 |
| B1.2 | `environment()` sets FE_TONEAREST, re-reads it, `abort()`s otherwise; IEC559 + 53-bit static asserts | seed.cpp:13-16 |
| B1.3 | the table entry of bin `i` is `expair((i+.5)/n)` — bin `i` sits at a **half** offset, not at `i/n` | seed.cpp:84 |
| B1.4 | `expair` = 9-term Taylor after reduction `k = nearbyint(4x)`, `y = (x-.25k)·2π`, then a quarter-turn switch on `((k%4)+4)%4`; `\|x\|>16` returns NaN | seed.cpp:21-31 |
| B1.5 | `hp = sqrt(x*x+y*y)`, **not** `hypot` (hypot is correctly rounded and would differ) | seed.cpp:32 |
| B1.6 | cell = `{b[5], s, g, c[2]}`; `c[2]` is written by `sumok`, so a cell is only valid after `sumok` | seed.cpp:33-51 |
| B1.7 | `c = {0, -1/(2π)} + Σ_b (± tab[b]/2π)`; the `-1/(2π)` initial value is the shift origin | seed.cpp:36-39 |
| B1.8 | `sumok` err = `π·(w²/4)·5`, per-bin residual weight `w/2`, tolerance `1e-8` | seed.cpp:41-46 |
| B1.9 | `s` = **first** argmin of `\|2b+1-n\|` over indices 0..4 in the *given* (unsorted) order; `p.s` starts at 0 so ties keep the lower index | seed.cpp:75-76 |
| B1.10 | `mk`: `p.b = b` is stored **before** the optional sort, so `g` of a Y cell is computed from the unsorted order `(a,b,c,d,e)` with `a` arbitrary | seed.cpp:75-80 |
| B1.11 | `g = w · max( ½max(2b₀+1, 2n−2b₄−1), b₁−b₀, b₂−b₁, b₃−b₂, b₄−b₃ )` | seed.cpp:78-80 |
| B1.12 | enumeration loops are **non-strict** (`F(d,e+1)` etc.), so bins may repeat: cells are non-decreasing 5-tuples, e.g. record line 1 is `0 0 55 55 55 2`. Do not write a set-of-5-bins model | seed.cpp:85,92 |
| B1.13 | xs filters: `a > e-d+1` → skip; `g > 1-(e-1)w+1e-8` → skip; then `sumok` | seed.cpp:86-89 |
| B1.14 | xs loop order `e,d,c,b,a` (all ascending) fixes the cell index `t`; ys loop order `a` then `e,d,c,b` fixes each `ys[a]` order | seed.cpp:85,92 |
| B1.15 | each Y multiset occurs once per choice of its "free" bin `a`, i.e. in 5 different `ys[a]` lists (829 306 Y cells from 22 829 A cells, an xs/ys ratio near 36) | seed.cpp:92-95 |

## B2. The cover

| # | choice | decided by |
|---|---|---|
| B2.1 | X cells are extended with their own `s`; **all** Y cells are extended with `s = 0` | covout.cpp:105-106 |
| B2.2 | the list of B candidates at `t` is `Y[A.p.b[A.p.s]]`, i.e. the B whose free bin equals A's distinguished bin. That shared bin is why supdual's row `s` carries both A's and B's coefficients | covout.cpp:121, 42-45 |
| B2.3 | extend err = `π·(w/4)·5`; `lo,hi` start at `∓.5`; `clip` returns early if `\|a\| < 1e-6` (a free, unconstrained half-plane) | covout.cpp:12-16 |
| B2.4 | clip order: the self row `(J0[s],J1[s])` first, then the four `j≠s` as `(-J1[j], J0[j])` in ascending `j` | covout.cpp:22-23 |
| B2.5 | clip slack: `r = (hp·err + Σ_{j≠s} ½\|·\| + 1e-7)/\|a\|`, then endpoints `mid ∓ r ∓ 1e-5` | covout.cpp:17-20 |
| B2.6 | `RN2 = pow(R·n,2) − 1e-4`; `T = pow(sqrt(RN2)+1.5, 2)`; truncation `int(T)` is used, so `int(T) = 25` (T = 25.846914147239978) | covout.cpp:100-101, 79 |
| B2.7 | `K = max(1, int(R·n+.51)) = 4`, `m = (n+K-1)/K = 28` → 21952 buckets. The spec's "3 / 38" is a defect (F1) | covout.cpp:102-103 |
| B2.8 | supdual row layout: rows 0..4 = A's five bins in columns 0,1; row `s` additionally holds B's bin 0 in columns 2,3; rows 5..8 = B's bins 1..4. `rhs = -n·(A.c[0],A.c[1],B.c[0],B.c[1])` | covout.cpp:43-46 |
| B2.9 | supdual constants: `err = 1.251·π·w`; regularisation `reg = {.2,.2}` then `2err/max(.02,q)`; weights `ww = 1` then `1/max(\|z\|,.03)`; `best` starts at `1e10`; unusable iterate (`\|v_a\|>1e4`) breaks out **keeping the previous best**; returns `best+.01` | covout.cpp:47-71 |
| B2.10 | supdual's 4×4 solve is LDLᵀ by hand (diagonal `D[i]=1/M[i][i]`, no pivoting, no symmetry check); upper triangle only is accumulated (`F(b,a+1)`), including the diagonal | covout.cpp:52-62 |
| B2.11 | testBucket order: `s = xsq + Σk²`; skip if `s > int(T)`; then `a = xab + Σ\|k\|`; cheap accept if `s+a+2.25 < RN2`; skip if `!dual \|\| s-a > RN2`; LP accept if `s+2.25+supdual(k,A,B,dual) < RN2` | covout.cpp:77-85 |
| B2.12 | the two `2.25` terms and the `1.5` inside `T` are the squared cell radius `(3/2)²`; they are constants of the method, not derived in the spec | covout.cpp:82,85,101 |
| B2.13 | `covered` scans the 3³ bucket window around B's `(b₁,b₂,b₃)` and restricts to `i≤j≤l` via `max(i,b-1)`/`max(j,c-1)`. Valid because `B.p.b[1..4]` is non-decreasing. Bucket key `(i·m+j)·m+l` | covout.cpp:89-95 |
| B2.14 | `insert` buckets by `(y0,y1,y2)` but `covered` windows on `y1,y2,y3`; the `y0` coordinate is never bounded — that asymmetry is upstream's and is compensated by the `s ≤ int(T)` test | covout.cpp:96-98, 90 |
| B2.15 | buckets are **cleared at every t**; only cells with the same `s` and `h < t` (plus cells already accepted at this `t`) can cover | covout.cpp:108-113 |
| B2.16 | the x-side prefilter `s > int(T) \|\| s-ab > RN2` is applied to `u.k` after assignment; `\|k_j\| ≤ 111` always fits `int8_t`, so no wrap is reachable | covout.cpp:116-118 |
| B2.17 | the two candidate filters, in this order: gap `B.p.g+1e-8 < 1-(A.p.b[4]+2)w`; interval `B.hi < A.lo \|\| B.lo > A.hi` | covout.cpp:122-123 |
| B2.18 | `all` is appended in `(t, position in Y[A.b[A.s]])` order; `byX[t]` gets the same sequence, so the two are consistent by construction | covout.cpp:127 |
| B2.19 | writer: header `"%d %zu\n"`; then `b[0..4]`, `s`, `y[0..3]`, every field `"%d "`, then `"\n"`; the trailing space is part of the format | covout.cpp:141 |
| B2.20 | `main`: `environment()` first, `argc != 2` → `abort()`, `fopen`/`fclose` failure → `abort()`; timing prints are informational only | covout.cpp:136-142 |

## B3. Deliberate differences from the published text (all verified bit-neutral)

1. Globals `n`, `w`, `tab` became `Lattice` parameters. The fixture compares every
   table entry, cell field, interval endpoint and supdual value bit for bit against the
   published code compiled in the same TU: `FIXTURE-OK checks=7670878 fails=0`.
2. Hard-coded constants became `Options`, defaults = the recorded run. Every ablation
   that changes an option also changes the counters, which is how the defaults were
   confirmed against the published run.
3. `square_pow` spells `pow(x,2)` as upstream does; `square_mul` is the folded form.
   They agree bit for bit at both arguments (F2).
4. supdual is `always_inline` (`MUB_AI`); the published build has no out-of-line
   supdual symbol either (F8). Performance only.
5. supdual's dead local `double y[4]` and the unused `v` in `seeds::list` are dropped.
6. `cent c{(int)t, ...}`: upstream passes `size_t t` into an `int` field.
7. Extra counters (`lpok`, `dropgap`, `dropiv`) exist only in `c-harness.cpp`; the
   program contract (`c-covrun.cpp`) prints exactly the published lines.
8. The harness seed cache (`CSEED1`) is private; it is not part of the frozen interface.

## B4. What a re-derivation must NOT do

- Do not substitute `hypot` for `hp`, or `i/n` for `(i+.5)/n`.
- Do not sort `p.b` for Y cells (it changes `g` and therefore the candidate set).
- Do not use `floor(T)`/`ceil(T)` where upstream truncates via `int(T)`.
- Do not scan the bucket window without the `i≤j≤l` restriction *and* expect the same
  `visit`/`near` counters (the centre set happens to be unchanged for K=4, F4).
- Do not iterate an unordered container anywhere in this unit; the only containers are
  vectors, iterated in appended order.
