# Work unit 03 (arithmetic core of `seed.cpp`) -- report

Swarm direction `d2` (member m3), team C, wave W1.  Unit 03 of the recreation
plan; part of rung R2.

## Claim

The numeric core of the published `seed.cpp` -- `pi`, `environment`, `expair`,
`hp`, `tab = {expair((i+.5)/112)}`, `n`, `w`, and the interval acceptance test
`sumok` (with `err = pi*(w*w/4)*5`) -- is re-derived as a modular C++17 unit
(`arith/seed_arith.{hpp,cpp}`) whose output is **bit for bit** that of the
published file on every value the seed stage produces:

* all 112 `tab` entries;
* all **22 829** `xs` seeds, each as `(b[0..4], s, g, c[0], c[1])`;
* all 112 `ys` buckets, 829 306 entries in total, in production order;

66 204 081 bytes, sha256
`7fb12e3b75f64d97b528f922d81c23686ec7707754c356b913f7b585d125a0f5`, identical
to the dump of an instrumented build of the published source (`cmp` silent).
`xs = 22829` is the published count: the recorded run's stdout begins
`xs22829 build19.30` (`.scratch/gh/covrun.log`).

## How this was established (and why it is not circular)

* `test/seed_orig.cpp` is the published file, copied verbatim (sha256
  `3c6c7a70...`), and `test/oracle_probe.cpp` is that file **included**, not
  re-implemented, with a dump `main`.  It is built with the published flags
  (`-std=gnu++17 -O3 -march=native -ffp-contract=off`).  The comparison is
  therefore published code vs our code, never our code vs itself.
* `test/unit_tests.cpp` -- 23 checks whose expected values never come from our
  code: `pi` equals `(double)acosl(-1.0L)` and its bits are `0x400921fb54442d18`;
  `environment()` restores `FE_TONEAREST` from `FE_UPWARD`, `FE_DOWNWARD` and
  `FE_TOWARDZERO`; `expair` is exact at 0, 1/4, 1/2, 3/4, returns `{NAN,NAN}`
  outside `|x| <= 16`, and is within 5 x 2^-53 of the `long double` exponential
  over 200 001 points; `sumok`'s `c` is inside its own `err` ball for 4 000
  sampled seeds (worst ratio 7.1e-13).
* `test/check_highprec.py` -- mpmath at 60 decimal digits and the recorded
  artefacts: every `tab` entry within 3 x 2^-53 of `cos`/`sin(2 pi (i+.5)/112)`;
  and each of the 249 878 recorded centre lines carries a `(b[0..4], s)`
  belonging to one of the 22 829 seeds (13 557 distinct, 0 missing), which ties
  the seed set to `centers.txt` without going through our writer or the oracle.
* `test/margin_scan.cpp` -- the determinism evidence: over 790 491 237 visited
  seeds and 4 742 947 422 `chk` tests, the smallest slack
  `|(r + 1e-8) - l|` is **1.043e-9**, i.e. ~1e7 times the binary64 spacing of
  these quantities.  No decision is within 1e-10 of flipping, so a few-ulp
  re-derivation cannot change the seed set.  Consistent with the measurement
  that `-ffp-contract=fast` (42 FMAs emitted, 41 in `sumok`) leaves the whole
  dump byte-identical, and that `-O0`, `-O2` and `-O2 -march=x86-64` do too.
* The transcription decisions the frozen spec does not fix -- 18 of them, each
  with its deciding line of `seed.cpp` -- are in `NOTES.md` section 3.

## The one trap worth naming

`seeds::mk(b, sorted)` (`seed.cpp:74-82`) assigns `p.b = b` **before** sorting the
local copy, so the `sorted` flag changes only the tuple `g` is computed from.
The `xs` loop passes ascending tuples and the `ys` loop does not, so the two
loops disagree about `g` for the same `(b, s, c)`.  Dropping the sort as a
no-op (my first attempt) adds 1 160 seeds: first divergence at dump line 27 803,
seed `(1,0,56,56,56)`, oracle `g = 0x1.fb6db6db6db6dp-2`, mine `g = 0x1p-1`.
`g` is what `coverSeeds::run` filters on, so this moves centres.  Independently
seen by m1 (their N9).

## Limits

Rung R2 is **not** claimed: the enumeration ordering (d2/m4), the cover (d3/m2)
and the serialisation (d4/m1) are other members' units, and the 402 s `covrun`
was not run.  What is claimed is that one third of the path -- the part every
centre index and every coordinate depends on -- is exact, and that the published
`err` constant is 1 ulp below the correctly rounded `5*pi/(4*112^2)` (both
associations and their difference are recorded in `NOTES.md` item 12).

## Command and exit status

```
./test/run_all.sh        # exit 0, out/verify.log ends "ALL CHECKS PASSED", ~50 s
./test/run_all.sh --full # exit 0, adds the invariance runs and margin_scan, ~10 min
```

Last run: `./test/run_all.sh --full`, exit status 0, 432 s wall; `out/verify.log`
is the transcript and ends `ALL CHECKS PASSED` after 13 gate lines, all PASS.
