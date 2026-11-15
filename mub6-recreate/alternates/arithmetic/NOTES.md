# NOTES -- work unit 03, arithmetic core of `seed.cpp` (swarm direction d1)

Re-derivation of the numeric core of the published `seed.cpp`: `pi`,
`environment`, `expair`, `hp`, `tab`, `n`, `w`, `sumok`.
Oracle: `.scratch/gh/upstream/seed.cpp`, 119 lines,
sha256 `3c6c7a7092230de231fdb23b6d1782de0dd9ef6689095763b875d90ce5ddeb44`,
copied verbatim to `test/seed_orig.cpp` and included, never edited.

All line numbers below are lines of that file.  Line-number checks:
`nl -ba test/seed_orig.cpp`.

## 0. Result

`out/oracle.dump` (instrumented build of the published file) and
`out/mine.dump` (this unit) are the **same 66 204 081 bytes**, sha256
`7fb12e3b75f64d97b528f922d81c23686ec7707754c356b913f7b585d125a0f5`, and contain

* `n`, `w`, `pi`;
* all 112 `tab` entries as hex floats;
* all **22 829** `xs` entries with `(b[0..4], s, g, c[0], c[1])` as hex floats;
* all 112 `ys` buckets, 829 306 entries in total, in production order.

So every double the seed stage produces, and every accept/reject decision it
takes, is reproduced bit for bit.  `xs = 22829` is the published count: the
recorded run's stdout begins `xs22829 build19.30`
(`.scratch/gh/covrun.log`; also quoted at `results/recreate-code-plan.md:218`).

Reproduce with `./test/run_all.sh` (exit 0) or `--full` (exit 0).  Timings on
this VM for the same work: oracle probe 20.0 s and our build 19.3 s when the VM
was quiet; 40.0 s and 36.0 s in the `--full` run with other jobs on the four
CPUs (`out/verify.log`).

## 1. What this unit is not

* The enumeration (`seeds::mk`, `seeds::build`, the `a>e-d+1` skip, the gap
  filters) and the `t` index belong to **d2**; the serialisation and the
  ordering of `all` belong to **d4**; the cover (`extend`, `supdual`,
  `testBucket`, `covered`, `insert`, `coverSeeds::run`) belongs to **d3**.
  `test/mine_dump.cpp` and `test/margin_scan.cpp` contain a transcription of
  `mk`/`build` as a **test scaffold only**, so that the two dumps align entry by
  entry.  It is not exported by the unit and nothing here claims to have
  designed it.  It did have to be right for the comparison to mean anything, so
  the two traps in section 3 were found through it.
* Byte identity of `centers.txt` (rung R2) is *not* established here.  What is
  established is that one third of the path -- the part every centre index and
  every centre coordinate depends on -- is exact.
* Nothing in `05-parameters` (whether `err` is the right radius) is touched.
  Section 5 measures the bound; it does not justify it.

## 2. Verification protocol

Three independent layers, all in `test/run_all.sh`:

| layer | what it compares | expected value comes from |
|---|---|---|
| oracle | `cmp out/oracle.dump out/mine.dump` | the published source, compiled here |
| unit tests | `test/unit_tests.cpp`, 23 checks | exact identities, `long double` at 64-bit significand |
| high precision | `test/check_highprec.py` | mpmath at 60 decimal digits, the recorded `centers.txt`, the recorded stdout |

The oracle probe is built with the published flags
`-std=gnu++17 -O3 -march=native -ffp-contract=off` (interfaces.md 1), the same
flags as the unit.  It includes the published file; it does not re-implement
anything, so the comparison cannot degenerate into our code agreeing with our
code.

`check_highprec.py` reads `../../../.scratch/gh/data/centers.txt` and, before
using it, checks its size (7 339 546 B) and sha256 (`c48bc9a2...`).  It then
checks that each of the 249 878 recorded centres carries a `(b[0..4], s)` that
is one of the 22 829 seeds of the dump: 13 557 distinct seeds are used, 0 are
missing.  That is an external check on the seed set that does not go through
our `center`-writing code or through the oracle binary at all.

## 3. Choices the frozen spec does not fix, with the deciding line

(interfaces.md section 4 fixes `pi`, `n = 112`, `w = 1/n` and
`err = pi*(w*w/4)*5`; everything else here is a choice.)

1. **`pi` is a hex literal** -- `seed.cpp:12`.  `0x1.921fb54442d18p+1` is the
   correctly rounded binary64 value of pi (verified bit for bit: bits
   `0x400921fb54442d18`, equal to `(double)acosl(-1.0L)`).  A decimal literal
   with 17 digits would give the same double, 16 would not, `M_PI` would not on
   every libm.  Keep the hex.
2. **`environment()` aborts, it does not report** -- `seed.cpp:13-16`:
   `fesetround(FE_TONEAREST)!=0 || fegetround()!=FE_TONEAREST` -> `abort()`,
   plus a `static_assert` on `is_iec559` and `digits==53`.  Our version keeps
   both, and the unit test drives it from `FE_UPWARD`, `FE_DOWNWARD` and
   `FE_TOWARDZERO` and checks it returns to `FE_TONEAREST` each time.
3. **The domain guard is `!(abs(x)<=16.)`, not `abs(x)>16.`** -- `seed.cpp:22`.
   The two differ on NaN: the published form turns NaN into `{NAN,NAN}` instead
   of letting NaN flow.  Same expression reproduced.
4. **Reduction constant and association** -- `seed.cpp:23-24`:
   `k = int(nearbyint(4*x))`, `y = (x-.25*k)*(2*pi)`.  `2*pi` is an exact
   doubling of the binary64 pi, so it is safe as a folded constant; `4*x` and
   `.25*k` are exact for `x` in the tab grid.
5. **The two tails are interleaved, 9 iterations, degree 19** --
   `seed.cpp:26-29`, denominators `(2*j-1.)*(2*j)` and `(2*j)*(2*j+1.)`, both
   `double` products of exact small integers.  Kept verbatim, including the
   interleaving (it does not change the sums, but it does not have to be
   preserved and is preserved anyway).
6. **Quadrant map** -- `seed.cpp:30`: `switch((k%4+4)%4)`, cases `(a,b)`,
   `(-b,a)`, `(-a,-b)`, `(b,-a)`, i.e. angle `+2*pi*x`.  Measured against
   `cos`/`sin` at 60 digits: worst error over 200 001 points is **5 x 2^-53**,
   worst over the 112 tab points is likewise 5 x 2^-53; 7 of the 112 entries are
   the correctly rounded double.  The published error budget is 3.1e-4, i.e.
   12 orders of magnitude larger, so the series is not the binding constraint.
7. **`hp` is `sqrt(x*x+y*y)`, not `hypot`** -- `seed.cpp:32`.  `hypot` is a
   different (more accurate) function; substituting it changes `r` in `chk` and
   is a CR, not a cleanup.
8. **`tab[i] = expair((i+.5)/n)`** -- `seed.cpp:84`.  `(i+.5)` is a `double`
   before the division; `i` never reaches 2^52 so the conversion is exact.
9. **`w = 1./n`** -- `seed.cpp:84`.  A division, not a reciprocal constant.
10. **`c` accumulation** -- `seed.cpp:36-40`: `c[1]` starts at `-1./(2*pi)`
    (a division), then for each bin in stored order
    `c[0] += tab[b][1]/(2*pi)`, `c[1] -= tab[b][0]/(2*pi)`.  Each is a
    **division by `2*pi`**, not a multiplication by a precomputed `1/(2*pi)`;
    the two differ in the last ulp for some bins and this is the only place the
    centre is computed.  The accumulation order is the bin order `b[0..4]`
    because the loop is over the array (not sorted, not any other order).
11. **`p.c` is written before the tests and regardless of the outcome** --
    `seed.cpp:40`.  A rejected seed leaves a defined `c` behind.  Reproduced;
    a unit that only writes `c` on acceptance would differ for every rejected
    seed, which matters for any later code that looks at a rejected seed.
12. **`err` association** -- `seed.cpp:41`: `pi*(w*w/4)*5.` is
    `((pi*(w*w/4))*5.)` and equals `0x1.4843ae1860576p-12` for `n=112`.
    The same real number written `5*pi/(4*112*112)` is
    `0x1.4843ae1860577p-12`, **one ulp higher**.  The published association is
    1 ulp below the correctly rounded product, i.e. very slightly optimistic.
    Irrelevant at the 1e-8 absolute slack that the test carries (section 5), but
    it is a choice, so: keep the published association.
13. **`chk`'s arithmetic** -- `seed.cpp:43-47`: `l = abs(x*c[0]+y*c[1])`,
    `r = hp(x,y)*err`, then `r += (w/2)*abs(x*tab[b][0]+y*tab[b][1])` for
    `b = p.b[0..4]` **in stored order**; `(w/2)` is a division by 2 (exact);
    the acceptance is `!(l > r + 1e-8)`, deliberately **not** rewritten as
    `l <= r + 1e-8` (different on NaN).  Tests are not reordered and not
    deduplicated even though `b` may contain repeated bins in `ys` seeds.
14. **Order of the six tests and short-circuiting** -- `seed.cpp:48-50`: the
    centre test first, then the five normal tests `(-tab[b][1], tab[b][0])` in
    stored order, returning at the first failure.  The order is observable only
    through the return value here, but it is what the published text does.
15. **`mk`'s `sorted` flag is not dead code** -- `seed.cpp:74-82`.
    `p.b = b` happens first, so sorting the *local* `b` does not touch `p.b`; it
    only changes the tuple that `g` is computed from (`seed.cpp:78-79`).
    Consequently `mk(t,true).g` is the gap of the tuple as given and
    `mk(t,false).g` is the gap of the sorted tuple.  The `xs` loop passes
    ascending tuples (`a<=b<=c<=d<=e`, `seed.cpp:85`) so the two agree there;
    the `ys` loop (`seed.cpp:92-93`) passes `(a,b,c,d,e)` with `a` outside the
    chain, so they do **not** agree.  Measured: my first transcription dropped
    the sort as a no-op and produced 81 248 bytes more dump than the oracle --
    1 160 extra seeds, first divergence at dump line 27 803, bucket `a=1`,
    seed `(1,0,56,56,56)`, oracle `g = 0x1.fb6db6db6db6dp-2`, mine `g = 0x1p-1`.
    Every `c` was identical at that point; only `g` differed, and `g` is what
    `coverSeeds::run` filters on (`covout.cpp`, `B.p.g+1e-8<1.-(A.p.b[4]+2)*w`),
    so this single quirk moves centres.  **If you are re-deriving d2, sort the
    local copy only when `!sorted`, and compute `g` from that local copy.**
16. **`s` is the first minimiser** -- `seed.cpp:76`: strict `<`, so ties go to
    the smallest index; `b[p.s]` is read before `p.s` is updated (it starts at
    0).  `|2b[j]+1-n|` is integer arithmetic; `n=112` keeps it in range.
17. **`g`'s association** -- `seed.cpp:78-80`: `.5*max(2*b[0]+1, 2*n-(2*b[4]+1))`,
    then `max` with each gap `double(b[j+1]-b[j])`, then `*= w`.  Written here as
    `(.5*x)*w`; `x*.5` is exact (a power-of-two scaling) and `w` is not, so both
    groupings round exactly once and agree -- but the published order is
    reproduced rather than argued about.  The integer `max` arguments are `int`
    arithmetic (`2*n-(2*b[4]+1)`), converted to `double` by the `.5*`; no
    overflow for `n = 112`.
18. **`xs` filter and `ys` filter are different** -- `seed.cpp:86-88` skips
    `a>e-d+1` and then rejects by gap; `seed.cpp:92-94` has no gap test at all.
    Asymmetry is deliberate in the published code; do not "unify" it.

## 4. Determinism evidence (measured, this VM, gcc 16.2.0, znver1)

* **Invariance across build shape.** The unit compiled at `-O0`, at `-O2`, at
  `-O2 -march=x86-64` (no AVX/FMA at all) and at `-O3 -march=native` produces
  the same 66 204 081 bytes (`out/verify.log`, four `PASS ... byte-identical`
  lines; `-O0` takes 232 s against 32 s at `-O2`).  So the core is not optimiser-
  or ISA-sensitive at the tab/centre/decision level; the `portable` build's structural-equality
  claim for this unit is not in doubt.
* **The decision surface has no knife-edge.** `test/margin_scan.cpp` repeats
  both enumeration loops and evaluates all six `chk` tests of every visited seed
  without short-circuiting: 790 491 237 seeds, 852 135 accepted
  (22 829 + 829 306), 4 742 947 422 tests.  The smallest `|slack|` where
  `slack = (r + 1e-8) - l` is **1.043e-9** (seed `(54,7,28,63,84)`, the centre
  test).  A perturbation would have to move one of the six linear forms by
  1e-9 to change a single seed, i.e. by ~1e7 times the binary64 spacing of
  these quantities.  Only 457 of 4.7e9 tests come within 1e-8 of the boundary,
  and none within 1e-10.
* **`-ffp-contract=off` is not load-bearing *for this unit*.** Rebuilt with
  `-ffp-contract=fast` (42 FMA instructions actually emitted, 41 of them in
  `sumok`, 1 in `hp`), the dump is still byte-identical.  The centre itself is
  insensitive by construction (its only operations are a division and an add,
  which cannot be fused), and the decisions are insensitive by the margin above.
  This is a measurement about `seed`; the spec calls the flag load-bearing for
  the whole build and nothing here says otherwise for `patchx`/`stageB`/`stageC`,
  whose decisions are much tighter.
* **`sumok`'s enclosure is real.** For 4 000 sampled seeds, the published `c`
  is within **7.1e-13 relative to its own `err`** of the value computed in
  `long double` from exact angles (`unit_tests.cpp` T6).  The bound is 12
  orders of magnitude looser than the error it covers -- which is the reason
  the `1e-8` slack exists and the reason the seed set is stable.
* The oracle probe and our unit agree on 852 135 acceptances out of 790 491 237
  visits, which is also a check that `sumok`'s *decision* (not just its `c`)
  was re-derived correctly.

## 5. Files

```
arith/seed_arith.hpp      the unit's interface (exported names, line citations)
arith/seed_arith.cpp      the unit's implementation
test/seed_orig.cpp        verbatim copy of the published seed.cpp (119 lines)
test/dump_common.h        the one text format both dumps use (%a for every double)
test/oracle_probe.cpp     instrumented build of the published file (the oracle)
test/mine_dump.cpp        our unit + a test-scaffold enumeration, same output
test/unit_tests.cpp       23 independent checks (C++, long double reference)
test/check_highprec.py    independent checks (mpmath 60 digits, recorded artefacts)
test/margin_scan.cpp      no-knife-edge scan over all 4.7e9 tests
test/run_all.sh           the gate: build, dump, compare, test; exit status
out/oracle.dump           oracle output, 66 204 081 B, sha256 7fb12e3b...
out/mine.dump             our output, byte-identical
out/verify.log            the transcript of the last run_all.sh
```

## 6. Reproduce

```
./test/run_all.sh          # ~2 min, exit 0 == every check passed
./test/run_all.sh --full   # + the invariance runs and margin_scan, ~10 min
```

Last run: exit status 0, `out/verify.log` ends `ALL CHECKS PASSED`.
