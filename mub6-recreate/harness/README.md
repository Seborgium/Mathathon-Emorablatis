# `harness/` — build and reproduction harness (team V, units 02/10/11)

Owner: V. Everything here is runnable as one command and prints one machine-readable
line naming its JSON log. No algorithm code lives here; the sources are read from
`src/` (team C) or, for now, from the published cache `.scratch/gh/upstream/`.

## The one command

```
work/10-recreate/harness/verify.sh all      # r0, portable, r2
work/10-recreate/harness/verify.sh r0       # 15 s: faithful build + probe + pow checks
work/10-recreate/harness/verify.sh r2       # 13 min: covrun reproduces centers.txt
work/10-recreate/harness/verify.sh portable # 45 s: -O2 build, gcc and clang
```

Exit status: `0` every requested unit passed · `1` a unit failed · `3` a requested leg
could not be run at all (an unrun check is not a pass). Each unit also prints
`RESULT unit=<u> status=<pass|fail|incomplete> log=<path>`.

## Files

| file | what it does | log |
|---|---|---|
| `build/faithful.sh` | the faithful build of spec §1: one TU per program, the upstream include chain reproduced, `g++ -O3 -march=native -ffp-contract=off` (`-std=gnu++17` for the three later binaries); refuses to proceed if `abi-fp-probe` fails; checks the include-guard discipline and the `pow(x,2)` equivalence; hashes every artefact | `logs/build-<stamp>.json` |
| `build/portable.mk` | `make` form of the portable build: `-O2`, no `-march=native`, `gcc` and `clang`; `MODE=mono` (published TUs) or `MODE=modular` (team C's module tree, refused with a CR until `src/` exists) | — |
| `build/portable.sh` | runs `portable.mk` per compiler, probes, checks no AVX was enabled, and compares `arun` records with the faithful build's | `logs/R0-portable.json` |
| `reproduce.sh` | R2: builds, runs `covrun` once, and compares with the recorded covering file byte for byte plus the deterministic counters | `logs/R2.json` |
| `verify.sh` | the entry point above | `logs/R0.json`, `logs/R2.json`, `logs/R0-portable.json` |
| `probe/cover-square-probe.cpp` | decides `pow(v,2) == v*v` at the two cover-square arguments (determinism register item 9) | in `build/*.json` |
| `fixtures/centres-200.txt` | 200 centres from the recorded file, header rewritten to `112 200` (a truncated file that still says 249878 aborts in `CenterList::load`) | — |
| `lib/facts.py`, `lib/gate.py`, `lib/common.sh` | TSV→JSON log assembly, gate-record condensation, shell helpers | — |
| `out/` | **disposable** build/replay products, git-ignored; nothing here is evidence except through the log that names it | — |

## Established facts (this wave)

1. **R2 passes.** The faithful build's `covrun` writes 7 339 546 B, sha256
   `c48bc9a2…748a5789` — byte-identical to `.scratch/gh/data/centers.txt` (`cmp` silent),
   and the deterministic stdout counters match the recorded run exactly:
   `xs22829 checked151744086 centers249878 visit29769262282 near3341641851 cheap45648766
   lp3134060273`. Evidence: `logs/R2.json`.
2. **`pow(x,2)` is not folded in the published build, and does not have to be.** The
   published `covrun` imports `pow@GLIBC_2.29` and calls `pow@plt` twice, at
   `coverSeeds::run+0x5a` and `+0x9f` (`.scratch/gh/build/covrun.disassembly.txt`,
   offsets `0x53fa`, `0x543f`). spec §5.9 says the squares "must be a single multiply";
   the numbers that matter are, at the two arguments the cover uses,
   `pow(v,2) == v*v` bit for bit (`RN2 = 0x1.9b09e12a51e33p+3`,
   `T = 0x1.9d8cf5d94ea5ap+4`), which `probe/cover-square-probe.cpp` checks. The identity
   is **not** universal: under glibc 2.43 it fails on 4.5e-4 of random doubles, always by
   exactly 1 ulp (glibc `pow` is <0.52 ulp, not correctly rounded). GCC 15.2.0 folds both
   sites, GCC 16.2.0 and the recorded 14.3.1 keep the call — all give the same bytes.
   Consequence for the recreation: replacing `pow(x,2)` by `x*x` is safe *at these two
   arguments* and nowhere else.
3. **The portable build reproduces the recorded artefact too.** `gcc -O2
   -ffp-contract=off`, no `-march=native`: the covering run also writes
   7 339 546 B, sha256 `c48bc9a2…`, byte-identical, in 623 s (`logs/R2-portable-gcc.json`,
   18/18 checks). So on this host neither `-O3` nor `-march=native` is load-bearing for
   `covrun`'s output — worth knowing before team C's modular `-O2` build is blamed for a
   byte difference. Reproduce with `portable.sh --full`.
4. **The portable build agrees with the faithful one on real input.** `gcc -O2
   -ffp-contract=off` (no `-march=native`) produces `arun` records byte-identical to the
   `-O3 -march=native` build on 200 centres (`sha256 1d357c69…`), and the same bad file
   and stdout. Evidence: `logs/R0-portable.json`.
5. **Fixture provenance.** `fixtures/centres-200.txt` hashes to `1e5a82a9…`, the same
   bytes as the pre-existing `.scratch/gh/data/small.txt`; the records it produces hash to
   `1d357c69…`, the same as the pre-existing `.scratch/gh/data/small-out.bin`.

## Not verified here

- **The clang leg.** `clang++` is not on `PATH`; the only `clang` is Lean's stub at
  `/opt/lean/lib/clang/22` with no `include/` directory, so it cannot compile `#include
  <cstdio>`. `portable.sh` runs the leg anyway, records the compiler's own error and marks
  the unit `incomplete` (exit 3) rather than passing it. `abi-fp-probe.cpp` refuses clang
  by design, so on any host the clang leg can never include the probe.
- **`MODE=modular`.** `src/` is empty (team C, units 03–09). `portable.mk` refuses with a
  named CR instead of guessing their header layout.
- **`brun`/`crun`.** Not exercised by any unit here; replaying the recorded batches is
  unit 11 (the replay driver) and the record formats are unit 10 (the independent checker).
- **The record reader/writer.** `saveRecords`/`readRecords` byte layout is not re-derived
  here; `reproduce.sh` only checks `centers.txt`.

## Log registry (`../logs/`)

| log | produced by | verdict |
|---|---|---|
| `R0.json` | `verify.sh r0` (gate record over `build-<stamp>.json`) | pass |
| `build-<stamp>.json` | `build/faithful.sh` | pass, 25 checks |
| `R2.json` | `reproduce.sh` (faithful build) | pass, 19 checks |
| `R2-portable-gcc.json` | `reproduce.sh --no-build --build-out <portable gcc dir>` | pass, 18 checks |
| `R2-portable.json` | first attempt at the line above with a **relative** `--build-out`; my script resolved it after `cd`, so `covrun` never ran | **fail, kept as evidence of a harness bug, not of the code** |
| `R0-portable.json` | `build/portable.sh` | incomplete (exit 3): gcc leg pass, clang leg cannot be run on this VM |

The relative-path bug above is fixed in `reproduce.sh`/`faithful.sh`, which now
absolutise `--out`, `--log`, `--build-out`, `--work`, `--recorded`.

## Reproduction of this harness's own numbers

```
work/10-recreate/harness/build/faithful.sh --src .scratch/gh/upstream
work/10-recreate/harness/reproduce.sh                    # ~13 min under load
work/10-recreate/harness/build/portable.sh               # gcc leg passes, clang skipped
```
