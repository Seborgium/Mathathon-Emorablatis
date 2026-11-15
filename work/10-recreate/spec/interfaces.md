# Frozen interface specification

Status: **W0 draft, awaiting K sign-off at G-R0.** Owner: O. Changes after freeze are CRs.
Source of truth: the published files (hashes in `verification/code/extraction.json`). Where this
document and the published code disagree, the code is right and this document is a defect.

This document fixes **contracts**: what a caller may rely on, what a file contains, which constants
are nailed down, and which behaviours must be deterministic. It deliberately does **not** fix the
mathematics of each stage — that is the manuscript and the coding units' `NOTES.md`.

---

## 1. Build and translation-unit contract

Four programs, four translation units, built by `build.sh`:

| program | TU | include chain |
|---|---|---|
| `covrun` | `covout.cpp` | `covout.cpp` → `seed.cpp` |
| `arun` | `atlas.cpp` | `atlas.cpp` → `patchx.cpp` → `ub.cpp` → `seed.cpp` |
| `brun` | `stageB.cpp` | `stageB.cpp` → `atlas.cpp` → … (as above) |
| `crun` | `stageC.cpp` | `stageC.cpp` → `stageB.cpp` → … (as above) |

Guards: the includer defines the includee's guard before including it (`stageB.cpp` opens with
`#define ATLAS_HEADER`, `atlas.cpp` with `#define PATCH_HEADER`, `patchx.cpp` with `#define UB_HEADER`,
`ub.cpp` with `#define HEADER`, `stageC.cpp` with `#define REFINE_HEADER`). Each file hides its own `main` behind the guard its **includer**
defines: `seed.cpp` behind `HEADER` (defined by `ub.cpp` and `covout.cpp`), `ub.cpp` behind
`UB_HEADER` (`patchx.cpp`), `patchx.cpp` behind `PATCH_HEADER` (`atlas.cpp`), `atlas.cpp` behind
`ATLAS_HEADER` (`stageB.cpp`), `stageB.cpp` behind `REFINE_HEADER` (`stageC.cpp`), `stageC.cpp`
behind `STAGEC_HEADER` (itself — it is the outermost). Consequence: every file is both a header and a
program, and `stageC.cpp` alone contains the whole 1 900-line program.

Compile lines (exactly, from `build.sh`; `-march=native` and `-ffp-contract=off` are load-bearing):

```
g++ -O3 -march=native -ffp-contract=off                       abi-fp-probe.cpp -o …/abi-fp-probe-covrun
g++ -std=gnu++17 -O3 -march=native -ffp-contract=off          abi-fp-probe.cpp -o …/abi-fp-probe-abc
g++ -O3 -march=native -ffp-contract=off                       covout.cpp      -o …/covrun
g++ -std=gnu++17 -O3 -march=native -ffp-contract=off          atlas.cpp       -o …/arun
g++ -std=gnu++17 -O3 -march=native -ffp-contract=off          stageB.cpp      -o …/brun
g++ -std=gnu++17 -O3 -march=native -ffp-contract=off          stageC.cpp      -o …/crun
```

`build.sh` refuses an existing output directory, exports `LANG=C LC_ALL=C`, and writes
`covrun.disassembly.txt` and `covrun.dynamic-symbols.txt` for the `pow(…,2)` inspection.
The probe hard-requires x86-64 GNU/Linux, GCC (not clang), no `-ffast-math`, binary64, 8-bit bytes,
32-bit `int`, 64-bit `uint64_t == unsigned long`, `FLT_EVAL_METHOD == 0`, round-to-nearest,
gradual underflow, masked exceptions, FTZ/DAZ clear.

**Recreation deliverables are two builds** (§2 of the plan): `faithful` (this shape, these flags —
the only one held to byte-identity) and `portable` (modular TUs, `-O2`, no `-march=native`, gcc and
clang — held to structural equality and to the checker).

---

## 2. Program contracts

Every program calls `environment()` (or `checkcpu()`, which calls it) first: sets/asserts
round-to-nearest and aborts otherwise. Any argv contract violation is `abort()` — not an error
message, not a non-zero exit.

### `covrun <out>`
`argc == 2`. Builds `seeds::build(112)`, covers, writes `<out>` (§3.1). Always exits 0 on success.
stdout: `xs<count> build<sec>`, ` t<t>/<xs> cells<checked> centers<n>` every 10 000 seeds,
`N<n> r<R> dual<d> checked<…> centers<…> visit<…> near<…> cheap<…> lp<…>`, `time <sec>`.
stdout is informational and is **not** gated (its timing fields are not reproducible).

### `arun <centers> <part> <parts> <records-out> <bad-out>`
`argc == 6`; `parts ≥ 1`, `0 ≤ part < parts`. Processes centres `i == part (mod parts)` in file order.
Writes records to `<records-out>` and the failing centre indices (ASCII, `%d\n`) to `<bad-out>`.
Returns 1 if the bad file is non-empty, else 0.
Fixed internals: `r = .0320001`, `target = .103`, **Atlas cap `maxR = .125`**, `Asearch{levels 3,
iters 2, detail 0, first 1}`, `Atlas(maxR)` with 8³ bins. Distinguish this cap from the **`validate`
default of `.126`** (§3.2): they are different numbers doing different jobs — `.125` is the geometry
the atlas deduplicates against, `.126` is the widest radius a stored record may carry. `brun` passes
its own `target` to `validate`, so `.126` is the default only where a caller omits it.

### `brun <target> <w> <out> <bad> <prefix> <input>…`
`argc ≥ 7`. `target ∈ [.0001,.126]`, `w ∈ [.0001,.05]` (else abort). Inputs are record files, total
≤ 8 000 000 records; every input record is `validate`d on read. Parents are refined in
`stable_sort` order by **decreasing radius**. Outputs: `<out>` (all refined records), `<bad>` (bad
parents), and if `prefix != "-"` batches `<prefix><n>.bin` of exactly 256 records (last batch may be
short, forced at exit) plus `<prefix>done.txt`. Returns 1 if any parent is bad.
Fixed internals: `validate` cap `.126`; `Atlas(target, target < .03 ? 16 : 8)`; `varlimit = 120`;
batching granularity 256. **Every record written into a batch file has its `radius` replaced by
`target` before the write** (`stageB.cpp`, in `emit`); the main `<out>` file keeps the refined radii.
Keeping the refined radius in the batches changes bytes that `crun` then consumes.

### `crun <M> <layers> <linear> <RB> <detail> <searchMode> <capSteps> <part> <parts> <out> <input>…`
`argc ≥ 12`. Enforced ranges (else abort): `M ∈ [6,24]`, `layers ∈ [1,6]`, `linear ∈ [0,10]`,
`RB ∈ [.012,.09]`, `detail ∈ [0,10]`, `searchMode ∈ [0,2]`, `capSteps ∈ [100,10⁹]`, `parts ≥ 1`,
`0 ≤ part < parts`. Records are indexed over the **concatenation of all inputs** (a running `offset`),
and record `i` is processed iff `i % parts == part`. Writes unresolved records to `<out>` in input
order. Returns 1 if `<out>` is non-empty, else 0.
Defaults in the recorded run: `12 4 1 .042 1 1 5000000`, parts 0..3.

Three programs exist in the source but are **not built and not used** by the recorded run: the
`seed.cpp` main (`<n>…`, prints seed statistics), the `ub.cpp` main (`<n> <samples> <r> <levels>
<iters> <detail> <first>`, prints decile counts), and the `patchx.cpp` main (`<n> <samples> <r>
<target> <levels> …`, Stage-A statistics on a seed sample). Recreate them only if a unit test needs a
driver; the clean-room probe needs the second, nothing needs the third.

---

## 3. Data formats

### 3.1 `centers.txt` (ASCII, written by `covrun`, read by `CenterList::load`)
Header: `"%d %zu\n"` = `112 249878`.
Then one line per centre, exactly:

```
for b in X.b[0..4]: printf("%d ", b)
printf("%d ", X.s)
for b in Y.b[1..4]: printf("%d ", b)
printf("\n")
```

i.e. ten decimal integers, **each followed by one space**, then a newline — the trailing space
before `\n` is part of the format, and a writer that omits it still produces a file the production
loader accepts while failing R2 (measured: `arun` returns byte-identical records for the stripped and
the canonical file). Reading enforces `n == 112`, `0 < count ≤ 2 000 000`, all bins `∈ [0,112)`,
`s ∈ [0,5)`, and reconstructs `Y.b[0] = X.b[X.s]`.

Observable invariants of the recorded file, all checkable without running the cover: 249 878 rows;
13 557 distinct `X.b` prefixes; the five `X` fields nondecreasing and the four `Y` fields
nondecreasing **on every line** (`Y.b[0]` is not printed and need not be the smallest); `s`
histogram `{0:0, 1:675, 2:242295, 3:6908, 4:0}`; first line `0 0 55 55 55 2 0 0 55 55` (37 bytes),
last line `19 37 56 75 93 2 38 55 94 111`.

### 3.2 Record file (binary, written by `saveRecords`, read by `readRecords`)
Little-endian, no padding, no header beyond the count:

```
uint64   count                      (≤ 2 000 000 on read; abort beyond)
count × {
  int32  k                          (0 ≤ k ≤ 10 = maxK, enforced on read)
  double p[36]
  double T[k][36]                   (k·36 doubles; k = 0 writes none)
  double C, n0, id, ort, hor, mnorm, froot, radius   (8 doubles, this order)
}
```

On read, `dp` is **not** stored; it is recomputed as `dp[i] = dephase(p)[i]` with
`dephase(p)[6i+j] = p[6i+j] − p[6i] − p[j] + p[0]  (row term p[6i] = M(i,0), column term p[j] = M(0,j))`, then `wrap`ped by `nearbyint` into the **closed** interval `[−½, ½]` (`nearbyint` is ties-to-even,
so `wrap(±½) = ±½`).
A recreated reader that stores `dp` instead is wrong: the byte layout has no room for it.

Range invariants checked by `validate` (abort on violation), used by `brun` and `arun`-written records:
`radius ∈ [0,.126]`, `C ∈ [0,20)`, `n0 ∈ [0,1e-6)`, `froot ∈ [0,1e-6)`, `id ∈ [0,1e-4)`,
`ort ∈ [0,1e-5)`, `hor ∈ [0,1e-5)`, `mnorm ∈ [0,2)`, `|p[h]| ≤ 4`, `|T[a][h]| ≤ 1.01`.

### 3.3 Bad files (ASCII)
`arun` writes centre **indices**; `brun` writes bad-parent records into a binary `<bad>` file (and
the batch machinery writes the 256-record batches); `crun` writes unresolved **records** as a binary
file, and `batches/bad<n>.bin` are **`crun` outputs** (its `argv[10]`), not `brun`'s. All bad files are record files (§3.2) except `arun`'s `bad<k>.txt`, which is `%d\n` per line.
An empty (count 0) bad file is 8 bytes: the `uint64` zero. A zero-length file is a different thing
and appears only for the four `bad0..3.txt`.

### 3.5 Console transcripts (`results/*.txt`) — curated, not stdout

The 100 files under `execution/results/` are **not** what the programs print. They are a normalised
transcript: `covrun`'s `xs%zu build%.2f` becomes `xs <count>`; the `time %.2f` suffixes, the
`coverFailures<…>+<…>` pair, `candidates`/`patches` and `avg bins`/`balls` are removed; and the final
timing line is replaced by the bare marker `completed_write`. `check_records.py` `fullmatch`es these
curated forms — A: `done (\d+) G(\d+) failedBalls(\d+)` and `total done(\d+) global(\d+)
failedBalls(\d+)`; B and C have their own — and separately enforces the membership of `data/` and
`results/`.

Consequences. (i) Our raw stdout cannot be compared to those files. (ii) A replay that produced the
right records but different counts would still be caught, because the recorded transcript pins the
cumulative `done/G` sequences, the terminal totals and the batch partition. (iii) R6 therefore runs
the shipped checker with **our `data/`, the recorded `results/` and the recorded `commands.json`**: a
pass means our records agree with the recorded console facts. (iv) Reproducing the transcript itself
is a separate, optional rung — normalise our stdout and compare — and the normalisation must be
declared before it is applied, not tuned until it matches.

### 3.4 `done.txt`
`"%zu %zu\n"` = number of batches emitted, number of records emitted.

Caveat on the manifest: `commands.json` **never lists** `batches/f*.bin` or `<prefix>done.txt` as
outputs — the `Bfine` entry records only `fine.bin` and `finebad.bin`, while the 88 `C.batch<k>`
entries consume `batches/f<k>.bin`. A replay driver that trusts the manifest will not know which
batch files to expect; it must list the directory and check the partition against the parent count.
`crun`'s outputs are recorded, so the bad-batch chain is recoverable, but the fine batches are not.

---

## 4. Constants that must not drift

| constant | value | where |
|---|---|---|
| `n` (bins) | 112 | `covrun` main; enforced on `centers.txt` load |
| `w` | `1/n` | everywhere |
| cover radius | `.032`, `dual = 2` | `covrun` main |
| `RN2` | `(R·n)² − .0001` | `coverSeeds::run` |
| `T` | `(√RN2 + 1.5)²` | `coverSeeds::run` |
| bucket `K`, `m` | `max(1, int(R·n + .51)) = 4` (`int(3.584 + .51) = int(4.094)`), `m = ⌈n/K⌉ = 28` | `coverSeeds::run` |
| seed interval error | `π·(w²/4)·5` | `sumok` |
| centre interval error | `π·(w/4)·5` | `extend` |
| Stage A | `r = .0320001`, `target = .103`, `cap = .125`, levels 3, iters 2, detail 0, first 1 | `arun` main |
| Atlas bins / key | 8³ over `dp` at indices `{14,22,27}`; cap `.126` | `Atlas` |
| Stage B widths | `.07/.013` (mid), `.016/.005` (fine), `.011/.0038` (fallback); batch 256; `varlimit 120` | `commands.json` |
| Stage C | `M 12`, `layers 4`, `linear 1`, `RB .042`, `detail 1`, `searchMode 1`, `capSteps 5 000 000` | `commands.json` |
| `maxK` | 10 | `patchx.cpp`, enforced by record I/O |
| `pi` | `0x1.921fb54442d18p+1` (the binary64 value, written as a hex literal) | `seed.cpp` |

Anything not in this table but constant in the source is still part of the contract; record it in the
unit's `NOTES.md` with its line.

### 4.1 Constants that change output and that the paper does not justify

The cover is governed by four knobs besides `R` and `dual`. They are part of the published algorithm,
so a recreation must reproduce them exactly — but they carry no mathematical justification, and a
reader should be told that rather than shown a formula:

1. `dual = 2` is the **iteration count** of the dual bound, and `dual != 0` is also a switch that
   enables the LP step at all (`if(!dual || s-a > RN2) continue;`);
2. the bucket scan is the fixed 3×3×3 block around `(b1/K, b2/K, b3/K)` — reach 1, not derived from
   `R`;
3. the cheap-accept margin `s + a + 2.25 < RN2`, a flat 1.5² on the absolute-value slack;
4. the cheap-discard test `s - a > RN2`, which drops a pair before the LP is ever called.

Each of these can change `all.size()` or its membership. They belong in the parameters workstream
(`05-parameters`) as **unjustified constants of the published algorithm**; this programme reproduces
them and says so.

---

## 5. Determinism register

The recorded run is a single-threaded, single-process-per-command execution. To reproduce it, every
ordering and every floating-point operation must be fixed. Known order-carrying constructs:

1. `seeds::build` enumerates with `e` **outermost** and `a` **innermost**, and the bounds are
   **non-strict**: `F(i,n)` runs `i = 0 … n−1` and the inner bounds are `e+1, d+1, c+1, b+1`, so
   `a ≤ b ≤ c ≤ d ≤ e`. `xs` is therefore lexicographically ascending in
   `(b[4], b[3], b[2], b[1], b[0])` — 0 decreases over the recorded 249 878 lines, 39 distinct values
   of field 5. `ys[a]` uses the nest `a` outermost, then `e, d, c, b`, so `ys[a]` is ascending in
   `(e,d,c,b)` = `(y3,y2,y1,y0)`; within one `t` the file is therefore ascending in `(y3,y2,y1,y0)`
   and **not** in `(y0,y1,y2,y3)` — 236 321 within-group pairs, all strictly increasing.
   **`mk`'s `sorted` argument does not reorder the stored tuple**: `p.b = b` runs before the
   `std::sort` on the local copy, which only feeds `p.g`. The written bins are the enumeration order,
   not the sorted order — which is why `Y.b[0] = X.b[X.s]` may exceed `Y.b[1]` on line 1 of the
   recorded file (`X.b[X.s] = 55`, `y = (0,0,55,55)`). This order defines the `t` index of every
   centre, and the pair `(t, position within ys)` is a total order: all 249 878 `(key, y)` pairs are
   distinct, so no tie-break is needed and `std::sort` with that comparator reproduces the file.
2. `coverSeeds::run` iterates `t` ascending and, inside, `Y[A.b[A.s]]` in stored order; `all` is
   therefore ordered by `(t, position in ys)`. The output file inherits that order.
3. `CenterList::load` reads in file order and — when `samples > 0` only — reservoir-samples with
   `mt19937_64(123)`. The recorded run passes no sample count, so the reservoir path is dead there.
4. `seeds::list` reservoir-samples with `mt19937_64(42)`. Not used by the recorded run (it is used by
   the unbuilt `ub` driver), so it must exist but is not gated.
5. `brun` sorts parents by decreasing `radius` with `stable_sort`: ties keep input order.
6. `stageB::refiner` holds an `unordered_set<uint64_t>` for deduplication. Membership only — if a
   reimplementation ever iterates it, order becomes implementation-defined and the batch files change.
   A unit test must assert that iteration is never used.
7. `Atlas::add` canonicalises by a `mapH` built from `variants(...)`. The choice is **band-based, not
   a strict minimum**: pivots are collected where `g[k] + tol >= best` and then filtered by
   `P.gap <= ming + tol`, with `tol` supplied by the caller. The band and the scan order
   (`t`, `neg`, `i`, `j`) are part of the contract.
8. `Atlas::add` **merges or appends**: if a nearby centre is already in `G` and
   `radius + q.second + 2e-8 < maxR`, it raises that record's radius in place and returns false;
   otherwise it appends. Record files are therefore in **first-insertion order**, and a record's
   radius may have been updated after it was inserted. Reproducing the bytes means reproducing the
   merge decisions, not just the set of records.
9. No locale, environment, clock, thread or address dependence. `build.sh` sets `LANG=C LC_ALL=C`;
   the programs must not read `getenv`, time or `rand()`.
10. Floating point: no reassociation, no contraction, no vectorised reductions with a different
   summation order; `sqrt` correctly rounded. The two cover-square sites in `covout.cpp` compile to
   **calls to libm `pow`** — the published `covrun` has `pow@plt` at two addresses; the compiler did
   not strength-reduce them. At both actual arguments `pow(v,2)` and `v*v` agree bit for bit, so the
   record cannot distinguish them, but they differ by 1 ulp on about $4.5\times10^{-4}$ of random
   doubles. A faithful build calls `pow`; a modular build may substitute the multiply only by
   declaring the deviation.

11. `mk` scans `j = 0 … 4` for the skip index with a **strict** `<` against the running minimum, and
   `p.s` starts at 0, so the **smallest** index among ties wins. Ties are common: 21 853 of the
   249 878 recorded rows have one.

Any reimplementation that changes an item above is not a defect by itself — it is a **CR**, and it
loses the right to claim byte-identity for the affected artefact.

---

## 6. Module boundary (what each module may expose)

| module (upstream file) | exports | may depend on |
|---|---|---|
| `seed` | `xy`, `seeds`, `sumok`, `share`, `expair`, `hp`, `pi`, `n`, `w`, `tab`, `environment` | libstdc++ only |
| `ub` | `Z`, `nr/ab/dot`, `ldl<N>`, `frame`, `block`, `uc`, `bound`, `triglev`, `dataU`, `makeD`, `makeJ`, `scalar`, `derr`, `trial`, `Usearch`, `countL` | `seed` |
| `patchx` | `Basis`, `proj`, `jacobi<N>`, `dephase`, `Root`, `buildH`, `circle`, `Candidate`, `spectralUpper`, `chol`, `ell`, `bootstrap`, `covercompute`, `Astats`, `Asearch`, `dk/hvar/ne/DIM/maxK` | `ub` |
| `atlas` | `mapH`, `complement`, `pivot`, `yseq`, `variants`, `Record`, `Atlas`, `CenterList`, `saveRecords`, `readRecords`, `writeExact`, `readExact`, `checkcpu`, `wrap`, `turn` | `patchx` |
| `stageB` | `inverseTransform`, `Choice`, `statsB`, `relationB`, `refiner`, `validate` | `atlas` |
| `stageC` | `cx`, `Layer`, `ball`, `pt`, `cluster`, `single`, `BS`, `node`, `graph`, `paramsC`, `statC`, `negative`, `RB`, `detail`, `searchMode`, `capSteps` | `stageB` |
| `covout` | `SI`, `extend`, `cent`, `RX`, `indexed`, `coverSeeds` | `seed` |

A module may not widen its exports without a CR. In the modular build the same boundary is a header;
in the faithful build it is the include order above.

---

## 7. Not in this document

- The mathematics of any stage (what `scalar` certifies, what `graph` excludes): manuscript
  §2–§6, per-unit `NOTES.md`.
- The tolerances that are *mathematically* justified rather than merely constant: `05-parameters`.
- The probe's and checker's internals: WU-10 re-derives them independently, and its report is the
  authority on whether this spec is complete enough to re-derive them.
