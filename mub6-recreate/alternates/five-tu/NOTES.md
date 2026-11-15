# NOTES — units 03/04 (`seed.cpp`, `covout.cpp`) re-derived, member m4, direction d4

Scope: the seed enumeration (`seed.cpp`) and the covering machine + writer (`covout.cpp`)
of the published verification code, re-derived as modular C++17 in this directory.
Acceptance (rung R2): the build reproduces `.scratch/gh/data/centers.txt` byte for byte.

Result: **it does.** sha256 `c48bc9a2be1eb2cdeea82ea1b030d7cb9f00a6c9563b63f0248dd115748a5789`,
`cmp` clean against the recorded file, and every counter in the recorded `covrun` log
reproduced exactly (`checked151744086 centers249878 visit29769262282 near3341641851
cheap45648766 lp3134060273`, and the `t0/t10000/t20000` lines).

Provenance of the sources I read (never modified):
`upstream/seed.cpp` 119 lines md5 `c26dc3e9c5a6903e600275b07c6281ac`;
`upstream/covout.cpp` md5 of my read-only copy `probe/c-covout-oracle.txt`.
`probe/c-seed-oracle.cpp` is a byte copy of `upstream/seed.cpp` used as an oracle probe.

## Files

| file | role |
|---|---|
| `c-fp.hpp` | `pi`, `environment`, `expair`, `hp` (seed.cpp:11–35) |
| `c-seed.hpp`, `c-seed.cpp` | `xy`, globals `n/w/tab`, `sumok`, `share`, `seeds::{mk,build,list}` (seed.cpp:36–110) |
| `c-cover.hpp`, `c-cover.cpp` | `SI`, `extend`, `cent/RX/indexed`, `coverSeeds::{supdual,testBucket,covered,insert,run}` (covout.cpp:6–169) |
| `c-writer.hpp`, `c-writer.cpp` | the byte-exact writer (covout.cpp:172) |
| `c-covrun.cpp` | program `covrun <out>`, frozen interface (`argc==2`, `abort` otherwise) |
| `c-seeddump.cpp` | dev driver: census + whole seed stream in `%a` hex |
| `c-seedcensus.cpp` | dev driver: stage-by-stage counts of both loops |
| `c-partialrun.cpp` | dev driver: `covrun` stopped after `<tlimit>` seeds (prefix test) |
| `c-test-writer.cpp` | fixture test of the writer on the first 10 recorded lines |
| `results/order-check.py` | ordering claims measured on the recorded file alone |
| `probe/c-probe-seed.cpp` | oracle probe: the same stream from the published `seed.cpp` |
| `c-build.sh`, `c-verify.sh` | build (published flags) and the check suite |

## Enumeration and ordering (direction d4)

**E-1.** Both loops admit *repeated* bins. `F(d,e+1)` means `d ≤ e` (seed.cpp:87,92), so the
xs loop ranges over non-decreasing tuples `a ≤ b ≤ c ≤ d ≤ e`: C(116,5) = 160 389 488
candidates, not C(112,5). Measured: `c-seedcensus 112` prints exactly 160389488.
The ys loop is `a` free plus `b ≤ c ≤ d ≤ e`: 112·C(115,4) = 774 294 080 candidates.

**E-2.** `t` — the seed index that orders the output — is the append order of `xs`:
`F(e,n)F(d,e+1)F(c,d+1)F(b,c+1)F(a,b+1)` (seed.cpp:87), i.e. lexicographic on
`(e,d,c,b,a)` with `e` outermost and `a` innermost. Each surviving tuple is unique, so `t`
is well defined; a seed whose `ys` block yields no centre makes its `t` invisible in the
file. Measured on the recorded file: 13 557 of the 22 829 seeds appear as blocks, and the
sequence of blocks is exactly this order restricted to them (X part non-decreasing,
strictly increasing whenever the tuple changes).

**E-3.** The `ys` loop is *not* the mirror image: `a` is the outermost loop and is stored
**first** (`p.b[0] = a`, seed.cpp:92), while the other four run `e` outermost, `b`
innermost. So `ys[a]` is ordered by `(e,d,c,b)`. Measured on the recorded file: inside
every block the `(e,d,c,b)` sequence is strictly increasing (max block 278 rows).

**E-4.** `mk(b, sorted)` (seed.cpp:76–84) takes `b` **by value**: with `sorted == false`
the `std::sort` at seed.cpp:79 reorders only the local copy, so `p.b` keeps the enumeration
order `(a,b,c,d,e)` and only `g` is computed from the sorted multiset. The xs call passes
`sorted == true` (seed.cpp:89), the ys call `false` (seed.cpp:93).

**E-5.** `s` is `argmin_j |2·b[j]+1−n|` with a **strict** `<` (seed.cpp:78), so ties go to
the earliest index. Measured on the recorded file, which stores `s`: 21 853 of the 249 878
rows have a tied minimiser and in every one of them `s` is the *first* minimiser — a
"last minimiser" rule would differ on all 21 853 rows.

**E-6.** `s` is computed **before** the optional sort (seed.cpp:78 precedes :79), i.e. in the
stored order. This is observable only in the ys loop, where `a` is free: for
`a = 56, b = 55` the minimiser is `j=1` (`|2·55+1−112| = 1` vs `3`), while for `a = 56, c = 56`
the tie is between `j=0` and `j=2` and the strict `<` keeps `j=0`.

**E-7.** The filter `a > e-d+1` (seed.cpp:88) exists only in the xs loop. Applying it to the
ys loop too would change `ys` and hence the output; the ys loop has no filter other than
`sumok`.

**E-8.** The gap filter is `p.g > 1. - (e-1)*w + 1e-8` (seed.cpp:90) — note `(e-1)*w`, so
`e = 0` gives the bound `1+w`; `p.g` is dimensionless (already multiplied by `w` in `mk`).

**E-9.** `sumok` writes `p.c` **before** any test runs (seed.cpp:44–46), so a failing cell
leaves a populated centroid behind. No observable effect: failing cells are dropped by value.

**E-10.** `tab[i] = expair((i+.5)/n)` (seed.cpp:86) — half-bin offset. `n` and `w` are set
*before* `tab` is filled; `sumok`/`extend` read the globals, so the order matters.

**E-11.** `seeds::list` (seed.cpp:97–110, `mt19937_64(42)`) and `share` are dead in the
recorded run but are kept to match the module boundary; they are not gated by any check here.

## Cover and writer (choices the spec leaves open)

**C-1.** Two different interval errors, kept verbatim and not unified: `sumok` uses
`pi*(w*w/4)*5.` (seed.cpp:47), `extend` uses `pi*(w/4)*5.` (covout.cpp:16). They round
differently; "tidying" one into the other changes the output.

**C-2.** `extend` is called with `s = 0` for the Y side (covout.cpp:135) although the Y cell
has its own `mk`-selected `s`. This is right, not a bug: `Y` is indexed by
`Y[A.p.b[A.p.s]]` and the ys enumeration stores the shared bin as `b[0]`, so `s = 0` *is*
the common bin. Using `p.s` there would use the wrong coordinate.

**C-3.** `RN2 = sq(1)*pow(R*n,2)-.0001` and `T = pow(sqrt(RN2)+1.5,2)` (covout.cpp:129–130)
are left as `pow` calls because the published `covrun` really calls `pow@plt`
(`build/covrun.disassembly.txt` lines 4195, 4211). Measured here: glibc's `pow(x,2)` equals
`x*x` bit for bit for both arguments, so either spelling is byte-equal; keeping `pow` keeps
the re-derivation honest.

**C-4.** `K = int(R*n+.51)` = 3 and `m = (n+K-1)/K` = 38 are *computed*, not hardcoded
(covout.cpp:131–133), so a different `R` would still be handled correctly.

**C-5.** The bucket scan uses `j = max(i, b-1)` and `l = max(j, c-1)` (covout.cpp:117–118) —
the `max` against the *previous loop index*, not against `b-1`/`c-1` alone. Copied exactly;
the triangular (rather than cubic) neighbourhood is worth 27 → ≤ 27 visits.

**C-6.** `all` is ordered by `(t, position in ys)` (covout.cpp:150); `byX[t]` receives the
same centres in the same order, and `insert` therefore sees them in that order.

**W-1.** Each of the ten integers is written as `"%d "` (covout.cpp:172) — the space before
`"\n"` is part of the format and is present in the recorded file (verified on all 249 878
lines by `results/order-check.py`).

**W-2.** The header is `"%d %zu\n"` with `all.size()`; it is written before the rows, so a
development run stopped early produces a header that does not match its own body. That is
why `c-partialrun` is only ever compared as a *body prefix*.

**W-3.** No `setlocale` call exists anywhere, and the writer uses only `%d`/`%zu`, so no
LC_NUMERIC can reach it. Measured: `c-test-writer` built with `-DC_TEST_SETLOCALE` (which
calls `setlocale(LC_ALL,"")`, the only way a process could acquire a non-C LC_NUMERIC) gives
identical bytes with `LC_NUMERIC=C`, `LC_NUMERIC=en_US.utf8` and with `de_DE.UTF-8` (that
locale is not installed here, so it falls back to `C`). Caveat: no installed locale has a
non-`'.'` decimal point, so the invariance is also structural — only `%d`/`%zu` are used.

## Deviations (each is a CR candidate; none affects the gated artefact)

**D-1.** `coverSeeds::run` has an extra trailing parameter `size_t stopAfter = size_t(-1)`
for the prefix test. The frozen program passes the default. It cannot change the result:
the loop `break`s before processing any `t >= stopAfter`, and `c-covrun.cpp` never passes it.

**D-2.** The unit is split into five translation units instead of one. Cost, measured on this
4-CPU VM: full `covrun` 759.6 s wall against the published build's 401.8 s, while the seed
build is *faster* (13.4 s vs 19.3 s). Byte-identity is unaffected (all arithmetic is
per-element IEEE, no reductions). If the DAG has a wall-clock budget, the faithful build
should keep the single TU.

**D-3.** Kept deliberately: `#pragma STDC FENV_ACCESS ON`, `environment()` called first in
every `main`, `-O3 -march=native -ffp-contract=off`, and the dead `share`/`seeds::list`/`RX`
so that the module boundary of spec §6 is not widened or narrowed.

## Measured results (one-sided checks, no tolerance anywhere)

| check | command | result |
|---|---|---|
| seed stream, 852 135 lines, `%a` hex | `./c-seeddump 112 dump \| sha256sum` | `841e230b…` = oracle probe `probe/c-probe-seed.cpp` |
| xs stream alone | `./c-seedcensus 112` | `aa9e83fb…` = the `X` lines of the oracle stream |
| census | `./c-seedcensus 112` | 160389488 / 85349292 / 16197157 / 22829; ys 774294080 / 829306 |
| ys per bin | `./c-seeddump 112` | `results/mine-counts.txt` (min 4849 at a=0 and a=111, max 18997 at a=55,56) |
| writer, 10 lines | `./c-test-writer results/fixture-first10.txt …` | byte-identical, 289 bytes |
| ordering on the recorded file | `python3 results/order-check.py` | 4 claims hold on 249 878 rows |
| prefix | `./c-partialrun out 200` (321 centres) | `cmp` clean against the file prefix |
| whole file | `FULL=1 ./c-verify.sh` | sha256 `c48bc9a2…`, `cmp` clean |

Timings on this VM: seed build 13.4 s; `c-seeddump 112 dump` 13.3 s; `c-verify.sh` (cheap
checks, exit 0) 52 s; the full `covrun` 759.6 s.

`FULL=1 ./c-verify.sh` runs the same whole-file comparison. It was **not** run a second
time: the recorded full run above was performed once, by hand, with its exit status and
`sha256`/`cmp` output in `results/covrun-mine.log`, because a second full run costs the
shared 4-CPU VM another 13 minutes for the same bytes.
