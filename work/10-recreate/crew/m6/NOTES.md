# NOTES — units 03+04 (`seed.cpp`, `covout.cpp`), determinism register

Author: member m6, direction **d5** (determinism register + R2 harness). Swarm `smwgt1mbm`.
Upstream cited by line: `.scratch/gh/upstream/{seed,covout}.cpp` (119 + 143 lines, unmodified).
My re-derivation: `candidate/include/seed.hpp` (module 03), `candidate/include/cover.hpp` (module 04),
`candidate/src/covrun_main.cpp` (program `covrun`). Test-only drivers: `candidate/tests/`.
Harness: `harness/verify_R2.sh`, `harness/audit_format.py`, `harness/check_order.py`.

## 0. Result (R2)

    bash harness/verify_R2.sh --log logs/R2-full.json          # exit 0, 14m22s wall (774s in-process)

    abi: arithmetic/ABI checks passed
    build: g++ -O3 -march=native -ffp-contract=off -o build/covrun candidate/src/covrun_main.cpp
    sha256 ours: c48bc9a2be1eb2cdeea82ea1b030d7cb9f00a6c9563b63f0248dd115748a5789
    sha256 ref : c48bc9a2be1eb2cdeea82ea1b030d7cb9f00a6c9563b63f0248dd115748a5789
    compare: BYTE IDENTICAL                                        (7 339 546 bytes, 249 878 data lines)
    format: AUDIT OK (all five format checks)
    determinism: locale/TZ/cwd and -O2-generic perturbations identical (t<4)
    R2: PASS (whole)

Second, independent comparison — the stdout counters against the authors' recorded log
(`.scratch/gh/covrun.log`). Mine, from `build/stdout.txt`:

    xs22829 build32.31
     t0/22829 cells42 centers5
     t10000/22829 cells37490183 centers72679
     t20000/22829 cells119874659 centers205716
    N112 r0.0320 dual2 checked151744086 centers249878 visit29769262282 near3341641851 cheap45648766 lp3134060273

Identical field for field to the recorded log except `build`/`time` (timing, not gated):
`cells42 centers5`, `cells37490183 centers72679`, `cells119874659 centers205716`, `checked151744086
centers249878 visit29769262282 near3341641851 cheap45648766 lp3134060273`. 29.7 billion bucket visits
and 3.13 billion small LPs reproduced exactly: not just the emitted centres but every internal
counter of `testBucket`/`supdual` agrees.

Front-end figures (logs/probe_front_112_v1.txt): `xs` = **22829**; `Σ_a |ys[a]|` = 829306;
`RN2 = 0x1.9b09e12a51e33p+3`, `T = 0x1.9d8cf5d94ea5ap+4`, `int(T) = 25`, `K = 4`, `m = 28`.

## 1. Determinism register (every order- or rounding-dependence in these two files)

Class: **O** = output order, **R** = rounding/evaluation order, **D** = dead or unreachable,
**C** = compile/platform. "Settled by" = the check that would catch a change.

| # | item | source | class | what a re-derivation must keep | settled by |
|---|---|---|---|---|---|
| 1 | `xs` append order: `e,d,c,b,a` nested, `a` innermost, so `(a,b,c,d,e)` ascending | seed.cpp:85-90 | O | the loop nesting itself; it *is* the centre index `t` | check_order.py (13 557 blocks in recorded order) |
| 2 | `ys[a]` append order: `a` outermost, then `e,d,c,b` | seed.cpp:92-95 | O | `a` outermost; within `a`, `b` innermost | full-file sha256 (order inside a block) |
| 3 | `all` order = `(t, position in ys[A.b[A.s]])` | covout.cpp:121-128 | O | insertion order into `all`; no sort | full-file sha256 |
| 4 | `mk` return of `p.b` is the **argument** order, un-sorted when `sorted==false` | seed.cpp:74-77 | O | `std::sort(b,…)` sorts the *parameter copy*; `p.b` keeps the caller's order | `ys` digests; every centre line's `y` fields |
| 5 | `p.s` = first argmin of `|2b+1-n|` (strict `<`, index ascending) | seed.cpp:76 | O | `p.s` starts 0; strict `<` keeps the FIRST minimum | full-file sha256 (ties are reachable: `n` even) |
| 6 | `sumok` accumulates `c[0],c[1]` over `p.b` in stored order | seed.cpp:37-39 | R | left-to-right, no reassociation | full-file sha256 |
| 7 | `sumok::chk` adds the 5 per-bin terms in `p.b` order after `hp(x,y)*err` | seed.cpp:43-46 | R | `r=hp*err` first, then `r+=…` in b order | full-file sha256 |
| 8 | `err = pi*(w*w/4)*5.` parses as `((pi*(w*w/4))*5)` | seed.cpp:41 | R | left-associative, `w*w` first | full-file sha256 |
| 9 | `err = pi*(w/4)*5.` in `extend` | covout.cpp:12 | R | same | full-file sha256 |
| 10 | `expair` range reduction `k=int(nearbyint(4x))`, then `(x-.25k)*(2*pi)` | seed.cpp:23-24 | R | `nearbyint` (round-half-**even**) not `floor(x+.5)`; `0.25*k` exact | `tab_digest` 14c320f9346c140f; and see note (a) |
| 11 | Taylor recurrence `ta=(ta*yy)/((2j-1.)*(2j))` — multiply then divide | seed.cpp:26-29 | R | must not become `ta*(yy/div)`; 9 terms, fixed j ascending | `tab_digest` |
| 12 | `tab[i]=expair((i+.5)/n)` — one rounded division per bin | seed.cpp:84 | R | order of construction is irrelevant (independent per i) | `tab_digest` |
| 13 | `hp(x,y)=sqrt(x*x+y*y)` | seed.cpp:32 | R | `x*x` then `+y*y` then correctly rounded sqrt | full-file sha256; binary uses `sqrtsd`, 28 sites |
| 14 | `RN2=sq(1)*pow(R*n,2)-.0001`, `T=pow(sqrt(RN2)+1.5,2)` | covout.cpp:100-101 | R | `pow(x,2)` must be correctly rounded — either libm `pow` or `x*x`, they agree here (note (b)) | probe: `pow_square_identical 1`; counters |
| 15 | `K=int(R*n+.51)`, `K=max(1,K)`, `m=(n+K-1)/K` | covout.cpp:102-103 | R | truncation toward zero, and `R*n` exactly `.032*112` | counters `visit/near/cheap/lp` (they depend on the bucket grid) |
| 16 | `int(T)` in `if(s>int(T))` | covout.cpp:79,118 | R | truncation of T, not `round` | counters `near` |
| 17 | `u.k[j]` narrows `int`→`int8_t`; diff of two bins ∈[-111,111] | covout.cpp:28,116; seed.hpp:… | C | safe, but only because bins < 112; a sign bug is silent | full-file sha256 |
| 18 | bucket grid index `(i*m+j)*m+l` with `i,j,l` clamped to `[0,m-1]` | covout.cpp:89-97 | O | `j` starts at `max(i,b-1)`, `l` at `max(j,c-1)` (not `b-1`/`c-1`) | counters |
| 19 | `covered` is a boolean OR of `testBucket` over the pool in ascending `(i,j,l)`; the *decision* is order-free, the *counters* are not | covout.cpp:89-94 | O | keep the scan order if the stdout counters are gated | counters literally match the recorded log |
| 20 | `F(h,t)` inserts X[h] with `p.s==A.p.s` into buckets in ascending `h` | covout.cpp:111-120 | O | ascending `h`; pool order affects `nvisit` | counters |
| 21 | `nn` = 112 is hard-wired in `main`; `w=1./n` | covout.cpp:138, seed.cpp:84 | C | `w` is one rounded division | `w = 0x1.2492492492492p-7` |
| 22 | `mt19937_64(42)` in `seeds::list` | seed.cpp:99 | D | reachable only from the unbuilt seed driver; `covrun` never calls `list` | `nm build/covrun | grep -c mt19937` = 0 |
| 23 | `mt19937_64(123)` in `CenterList::load` | atlas.cpp:176 | D | **not in this unit**: `covout.cpp:2` includes only `seed.cpp`, so atlas is not in the `covrun` translation unit | binary has no centerlist symbols |
| 24 | no `rand`, `getenv`, `time`, `setlocale`, threads, `unordered_*`, `map`, `set` in either file; the only clock read is `chrono::steady_clock::now()` feeding the two informational stdout fields | grep; covout.cpp:137,139,142 | C | keep the artefact free of every clock/environment read | `objdump -d \| grep -cE 'call.*<(rand\|getenv\|time\|setlocale\|clock_gettime)'` = 0 |
| 25 | writer `fprintf("%d ")`/`"%zu"` — C locale is process default because nothing calls `setlocale` | covout.cpp:141 | C | no `'` flag, no float conversion | harness runs the binary under `LC_ALL=en_US.UTF-8`, `LC_ALL=C.UTF-8`, `TZ=Asia/Tokyo`, different cwd: identical |
| 26 | file opened `"w"` (text mode) | covout.cpp:141 | C | Linux: no translation; `\n` only | audit_format.py (no CR) |
| 27 | `#pragma STDC FENV_ACCESS ON` is ignored by GCC (warning `-Wunknown-pragmas`) | seed.cpp:8 | C | the pragma is inert here; nothing changes the rounding mode after `environment()` | build log |
| 28 | `environment()` forces `FE_TONEAREST` and aborts otherwise; called first in `main` | seed.cpp:13-16, covout.cpp:136 | C | argv check comes *after* `environment()` | abi probe + main order |
| 29 | compile flags `-O3 -march=native -ffp-contract=off`, no `-ffast-math` | build.sh | C | `-march=native` here defines `__FMA__`, so `-ffp-contract=off` is the only thing stopping fusion of `a*b+c` into one rounding | the binary contains 0 `vfmadd`/`vfmsub`; harness also builds `-O2` generic: identical (t<4) |

Notes:
(a) `nearbyint(4x)` with `x=(i+.5)/112` can never hit a tie: `4x=(2i+1)/56`, and a tie needs
    `(2i+1)/56 = k+1/2`, i.e. `2(2i+1)=56(2k+1)`: the left side is `≡2 (mod 4)`, the right `≡0`.
    So the half-even rule is *not exercised by `tab`*, and any correctly rounded-to-nearest map
    (including `floor(4x+.5)`, which is exact here since `4x` is at least `1/56` from an integer)
    gives the same `k`. The choice is therefore not load-bearing **at n=112** — but truncation
    (`int(4x)`) would be, and `expair` is also called for other `n` by the unbuilt seed driver.
(b) `pow(x,2)` vs `x*x`: at `x=R*n` both give `4029b0ab2e1693c1`. Both binaries call libm `pow`
    twice (`objdump -d | grep -c 'call.*<pow'` = 2 in mine and 2 in the authors'
    `covrun.disassembly.txt`), so this is not even a difference between us.
(c) Instruction counts differ between my build and the recorded disassembly (my g++ is 16.2.0;
    `mulsd` 616 vs 512, `sqrtsd` 28 vs 20). Different unrolling, identical results — which is
    itself evidence that no reassociation is happening (a reassociation would change the file).

## 2. Choices the spec does not fix, and what decided them

| choice | decided by |
|---|---|
| bucket grid `K=4, m=28` — **the spec's `K=3, m=38` is arithmetically wrong** | covout.cpp:102-103 with `R=.032`, `n=112`: `int(3.584+.51)=int(4.094)=4`, `m=(112+3)/4=28` |
| `int(T)=25`, `T=25.8469…` | covout.cpp:101,103 |
| the "skip index" `s` is the index of the bin **nearest the middle** `n/2`, ties → lowest index | seed.cpp:76 |
| `p.g` for `ys` is *not* the cyclic gap: it is measured on the argument order (a may exceed b) | seed.cpp:74-80; covout.cpp:122 uses it, so it matters |
| a centre line's `y` fields are `B.b[1..4]`, i.e. `(b,c,d,e)` of the ys tuple, not the sorted b | covout.cpp:126; interfaces.md §3.1 says the same |
| `all` is grouped by `t` with no sort | covout.cpp:127 |
| the second loop of `build` puts `a` outermost, so `ys[a]` is not sorted by `e` | seed.cpp:92 |
| `share` and `seeds::list` are dead in `covrun` but exported | interfaces.md §6; covout.cpp never calls them |

## 3. Spec defects (to raise as CRs, not to fix here)

1. **`interfaces.md` §4, bucket `K`,`m`: says `= 3`, `m = 38`. Actual: `K = 4`, `m = 28`.**
   `int(.032*112+.51) = int(4.094) = 4`; `(112+4-1)/4 = 28`; the grid is 28³ = 21952 buckets, not 38³.
   Anyone who copies 38 from the spec cannot reproduce `centers.txt`, and the counters
   (`visit`, `near`, `cheap`, `lp`) will differ even if the centres happen to.
2. §4 "`pi` … written as a hex literal" — fine; but §4 does not list `1.251*pi*w`, the `supdual`
   error (`covout.cpp:47`), nor the `1e-7/1e-5/1e-8` slack constants, which are equally
   load-bearing for the counters.
3. §5 item 3 and item 4 describe `mt19937_64(123)` and `(42)`: neither is reachable from `covrun`
   (atlas.cpp is not in the translation unit; `list` is not called). True statements, but they
   should be marked "not gated by R2" so that nobody looks for them.

## 4. What my harness checks, and what it does not

`verify_R2.sh` checks: ABI probe; build with the frozen flags; run; sha256 of the whole artefact
(whole mode) or of the data lines with a clean-block-boundary assertion (`--stop-t T` prefix mode);
first differing byte offset and line on mismatch; a five-way format audit; and three perturbation
runs (LC_ALL/LANG/TZ/cwd, and an `-O2` generic-x86 build) that must be byte-identical.

It does **not** check: the four other programs; the mathematics (whether 249 878 is the right
number); the record format; anything about `seeds::list` or `share`, which `covrun` never calls.
The counters in §0 are compared by eye against `.scratch/gh/covrun.log`; a machine check would
need that log to be treated as a gated artefact, which is a decision for O/V, not for me.

## 4b. The gate's failure path is itself tested

A gate that has only ever returned PASS is not evidence. `harness/selftest.sh` plants five defects in
a copy of the reference and requires `verify_R2.sh --no-run` to reject each one *at the exact byte it
planted* (`bash harness/selftest.sh`, exit 0):

    SELFTEST ok   pristine copy accepted
    SELFTEST ok   one-byte: rejected at byte 5000 (exit 1)
    SELFTEST ok   two-bytes: rejected at byte 123457 (exit 1)
    SELFTEST ok   truncated: rejected at byte 1001 (exit 1)
    SELFTEST ok   extra-byte: rejected at byte 7339547 (exit 1)
    SELFTEST: 5 ok, 0 fail

The last two exercise the case `cmp -l` cannot report (one file a prefix of the other); the harness
detects it from the sizes and names the offset where the shorter file ends. Exit codes: 0 identical,
1 different, 2 setup/build failure — and the first failing check stops the gate.

## 5. Timings on this VM (4 vCPU, shared)

`seeds::build(112)` = 11.7 s alone (13-32 s under load), full `covrun` = 774 s wall / 475 s user
(the authors' recorded run: 401.8 s). Build 1.4-4.2 s.
