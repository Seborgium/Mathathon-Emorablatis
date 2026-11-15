# K/m3 — mutation controls (§6) put to the test

Direction k3. Read-only w.r.t. the tree; every experiment below ran on *copies* of the upstream
sources in `.ultramath/smwgt1mg2/m3/probe/`. Upstream files were not modified; the hashes in
`results/recreate-code-plan.md` §0 are untouched.

Everything here is a measurement unless marked **predicted**. Reproduce with the command given
under each finding. The recorded artefacts I compared against are the ones in the saved-run tree
(a copy of it was already in this VM under `.ultramath/smwgrr7ia/m3/.cache/math/...`).

**Verdict up front:** §6's eight controls are not eight controls of the ladder.
Control 7 cannot fail any rung (dead code in all four built binaries). Controls 1, 3, 4 do not
move R2 at all (measured). Control 6 is not an order-only mutation and therefore does not test
what §6 says it tests. Controls 2, 5, 8 are sound, but 2 and 5 land on R3 and R2 respectively —
not on "the harness" in general. "8/8 mutations fail the harness" is not achievable as written.

---

## k3-1 (BLOCKER) Control 7 is unreachable: `mt19937_64 rng(42)` is dead code in every binary the record runs

**Artefact.** `seed.cpp:99` (`mt19937_64 rng(42);`), `seed.cpp:107–111` (the reservoir: `rng` is
consumed *only* when `samples>0`), `seed.cpp:97` (`list(int samples=1000)`), call sites
`ub.cpp:372` and `patchx.cpp:457`, build targets `build.sh:22–25`.

**Why it is unreachable.** The guard chain is: `covout.cpp:1 #define HEADER` (suppresses
`seed.cpp:117 #ifndef HEADER`), `atlas.cpp:1 #define PATCH_HEADER` (suppresses `patchx.cpp:454`),
`patchx.cpp:1 #define UB_HEADER` (suppresses `ub.cpp:368`), `stageB.cpp:1 #define ATLAS_HEADER`
(suppresses `atlas.cpp:216`), `stageC.cpp:1 #define REFINE_HEADER` (suppresses `stageB.cpp:283`).
The only mains that exist in any built binary are covout/atlas/stageB/stageC — i.e. covrun, arun,
brun, crun. `seed.cpp`'s own main calls `list(0)`, which never reaches line 109; `patchx.cpp`'s and
`ub.cpp`'s mains are compiled by nothing, because `build.sh:22–25` never names those files as a
compilation unit. Consequently `rng` is never drawn in the recorded run, and mutating 42→43 cannot
change `centers.txt`, `coarse*.bin`, `mid.bin`, `fine.bin`, `batches/*`, any `results/*.txt`, or
any return code.

**Measured, other direction.** Building the driver by hand
`g++ -std=gnu++17 -O3 -march=native -ffp-contract=off ub.cpp -o urun` and running
`./urun 12 40 .02 2 1 0 1` gives, for seed 42 vs 43:

```
  (42)  0 0 0 0 0 0 0 0 0 0 0        N16 8192.0 870.7 863.8 863.8   percell 0.001414
  (43)  0 0 0 0 0 0 0 0 0 0 17       N16 8192.0 832.6 826.6 826.6   percell 0.001410
```

so the mutation *is* observable in the unbuilt `ub` driver, and only there. Note also that the
same unmutated binary prints `percell 0.001414` and `percell 0.001388` on two consecutive runs:
`ub.cpp:384` (`printf("percell %.6f", …time…/cells.size())`) is wall-clock, so a byte-diff of the
`ub` driver's stdout fails **at baseline**. Any control built on this output must mask line 5.

**Consequence for the plan.** §6 item 7 ("must move `ub` output, must not move the recorded run")
is true in both halves and useless as a ladder control: it cannot make R2–R6 fail, so WU-12's
"8/8 mutations fail the harness" is unsatisfiable unless the harness grows a fifth target that is
*not* part of the recorded run. Two honest repairs:
(a) restate it as a **rogue-path** control: build `urun`, run it pre- and post-mutation with a
fixed argv, compare stdout with the timing line masked, and record in the ledger that this checks
sensitivity-to-drift, not reproduction; or
(b) drop it and replace it with a reachable control that is strictly order-only (k3-5), so that
the eight controls are eight statements about the recorded artefacts.

**Settling test.** `build.sh`-equivalent on a copy of the tree, `diff` of `run(42)` vs `run(43)`
for all four targets; expected: no difference in any artefact (this is the finding, not a gap).

---

## k3-2 (MAJOR) Controls 1, 3 and 4 do not move R2 — measured on 3 000 of the 22 829 cells

**Method.** Copy of `covout.cpp` with one added early exit inside `coverSeeds::run`
(`F(t,X.size()){if(t>=LIMIT)break;`, `-DLIMIT=3000`), otherwise upstream, built with the recorded
flags. The algorithm is greedy and processes cells in index order, so the output for `t<LIMIT` is a
prefix of the full run's output. This is checked, not assumed: the baseline probe's 12 111 centres
are **byte-identical to the first 12 111 centres of the recorded `centers.txt`** (header rewritten,
`112 12111`), which also re-confirms that the faithful build reproduces stage A on this VM.

| variant | centres | stdout counters | artefact |
|---|---|---|---|
| baseline (`-ffp-contract=off`) | 12 111 | checked 5552647 visit 624467049 near 100412429 cheap 1889539 lp 93529007 | = recorded prefix |
| control 1: `fesetround(FE_UPWARD)` after `environment()` | 12 111 | identical, all five | **identical** |
| control 3: `-ffp-contract=fast` | 12 111 | identical, all five | **identical** |
| control 4: `-ffast-math` (on `covout.cpp` only) | 12 111 | identical, all five | **identical** |

The rounding mode really did change: the terminal line prints `N112 r0.0320 …` under the default
mode and `N112 r0.0321 …` under `FE_UPWARD` (glibc `printf` honours the dynamic mode). So the
doubles moved and *no decision moved*: every acceptance test in `covout.cpp` is slack-dominated
(`1e-8` at `seed.cpp:46`, `1e-7`/`1e-5` at `covout.cpp:19–20`, `-.0001` at `covout.cpp:100`), and
the artefact is integers. `-ffast-math` cost 32.06 s in the build phase vs 19.65 s and 55.26 s
total vs 31.35 s — timing only, and the cleaned record (`results/covrun.txt`) contains no timing.

**Consequence.** A harness that runs the controls where §5 says the cheap decisive rung is (R2)
reports 1, 3 and 4 as *missed*, and it would be right about R2. They are only detectable at R3
(k3-3). §8 puts the W2 gate after R3, so the gate can still pass — but the ledger must say which
rung failed, otherwise "control 3 passed" will be recorded as evidence that the byte-identity
gate is sensitive to the floating-point contract, and for stage A it is not.

**Settling test (conclusive).** Full `covrun` (402 s) for each of the three variants,
`sha256sum` against `centers.txt` (`c48bc9a2…`). Predicted: all three match. The 3 000-cell probe
is 13 % of the cells and 4.8 % of the centres; a decision flip would have shown up in `lp` or
`cheap` (both identical), so a full-run flip is unlikely but not excluded.

---

## k3-3 (MAJOR) At R3 the same controls do move — and control 1's failure is nontermination

**Method.** `atlas.cpp` copy, `arun` on the first 200 recorded centres
(`probe/A/out/centers200.txt`, `112 200`, part 0 of 1), recorded flags.

| variant | wall | records | outcome |
|---|---|---|---|
| baseline | 4.50 s (twice, byte-identical) | 27 | `bad0.txt` empty |
| control 3 (`-ffp-contract=fast`) | 8.14 s | 27 | differs from **byte 13** (first record); `candidates` 283228→283230, `patches` 6179→6184 |
| control 1 (`FE_UPWARD` after `checkcpu()`) | >570 s for 200 cells, >90 s for 3 cells (baseline 0.14 s) | 0 written | one bad index written; no output file |

So the doubles stored in a record (`C n0 id ort hor mnorm froot radius`, `atlas.cpp:191–201`) are
sensitive to the FP contract, while stage A's integer decisions are not. Corollary for the harness:
**a per-command timeout and the "terminal bad file is empty" test are load-bearing for control 1**;
without them the control hangs the gate instead of failing it, and the recorded run has no such
signal (all four `bad*.txt` are empty).

Placement matters: `checkcpu()` (`atlas.cpp:6–12`) *aborts* if MXCSR's rounding field is non-zero,
and `environment()` (`seed.cpp:13–16`) aborts unless the mode is already `FE_TONEAREST`. A
`FE_UPWARD` inserted before those guards makes every binary abort at start-up with exit 134 and no
artefact — caught by the program's own guard, so it proves nothing about the comparator. The
control must be inserted **after** `environment()`/`checkcpu()`, and its pass condition must be
"R3 fails on content or timeout with the other rungs unchanged", not "the program aborts".

**Settling test.** As tabulated; `cmp` the two `coarse*.bin`, and `timeout 300 ./arun …` for the
`FE_UPWARD` build.

---

## k3-4 (MAJOR) Control 2 is a different literal than R2's, and both nudges are detectable in 5 s at R3

**Patch.** `atlas.cpp:221`
`const double r=.0320001,target=.103,global=.125;` → `r=.0320002` (or `target=.1031`).

**Measured** (`r=.0320002`, same 200-centre run): all 27 records differ, first difference at
record 0 (**byte 1509** of 40 724), the record **multiset** differs (not a permutation), and
`candidates` 283228→283231 (the `patches` count stays 6179). Predicted: `coarse*.bin` sizes change
too.

**Rung.** R3 only. R2's radius is a *different* constant: `covout.cpp:140` `C.run(S,.032,2)`.
`.0320001` does not appear in covout at all. A harness that runs the controls at R2 would record
control 2 as missed while the mutation is in fact strongly observable — an artefact of the plan's
wording, not of the harness.

Also: control 2 needs `r` and `target` used *inside* the recorded command. `global=.125` is the
Atlas merge radius (`atlas.cpp:223`), so `.125 → .1251` is a third variant; it changes merges and
therefore counts, so it is the strongest of the three. Prefer it if the point of the control is
"one constant".

**Settling test.** `./arun centers200.txt 0 1 c.bin bad.txt` on both builds; `cmp` (5 s).

---

## k3-5 (MAJOR) Control 6 is not order-only, so it cannot test order sensitivity

**Patch as written.** `stageB.cpp:313`
`stable_sort(v.begin(),v.end(),[](const Record&a,const Record&b){return a.radius>b.radius;});`
→ `return a.id<b.id;`.

**Why the label is wrong.** The comparator fixes the *processing* order (`stageB.cpp:315`), and the
processing order fixes the content, not just the order:
- `Atlas::add` merges into an existing record in place and *grows* its radius
  (`atlas.cpp:161` `g.radius=max(g.radius,radius+q.second+1e-8)`; the `find` at `atlas.cpp:150`
  depends on what is already in `G`), so a different insertion order gives different radii and a
  different `G.size()`; the cap at `atlas.cpp:164` is order-dependent too;
- `ref.blockers=&done` (`stageB.cpp:317`): a parent's refinement consults the set of *already
  refined* records, so order changes `bad` membership, not just its order;
- batch slicing is a prefix walk of `A.G` (`stageB.cpp:302–310`), so a different `A.G` changes
  every `batches/f*.bin`, `batches/fdone.txt` and `finebad.bin`.

Hence control 6 is caught by *any* comparator, including one that sorts records before comparing —
so it demonstrates nothing about order sensitivity, and §6's stated expectation ("must move the
batch files") under-describes the failure (counts and sizes move as well).

**The control you want instead.** Same multiset, permuted bytes: in `emit`, reverse the slice before
writing (`stageB.cpp:304`: `vector<Record> dat(A.G.begin()+emitted,…); std::reverse(dat.begin(),dat.end());`).
Expected: `fine.bin`, `fdone.txt`, `finebad.bin` unchanged; every `batches/f*.bin` permuted inside
its 256-record block. That one is caught for free by the shipped checker, which compares batches to
`fine.bin` **in order** (`check_records.py`, `for record in batch: original=next(fine_records)`),
so R6 catches it but a multiset-only R5 does not. That asymmetry is the useful statement.
**Verified** by permuting the first two records of the recorded `batches/f0.bin` (256 records) and
re-running the shipped checker: `{"result": "NOT ESTABLISHED", "error": "batch differs beyond
radius or insertion order: 0"}`; restoring the file returns PASS. So an order-only mutation is
detectable at R6 today, and needs no new machinery — but R5 (batch files alone) must compare
byte-wise, not as multisets.

**Related, and a trap for the replay driver:** `stable_sort` breaks ties on insertion order, so the
*input file order* is load-bearing. `commands.json` `C.Bfallback` passes the 15 fallback inputs in
ASCII order — `bad10, bad3, bad4, bad5, bad52, bad53, bad55, bad56, bad6, bad7, bad78, bad79, bad8,
bad80, bad84` — not numeric order. A driver that re-globs `batches/bad*.bin` numerically changes the
tie-break, and also changes the `bad parent %zu` indices that `check_records.py` parses. Replay
argv verbatim from `commands.json`; never re-derive an input list.

**Settling test.** Apply the reverse-in-`emit` patch; `cmp` each `batches/f*.bin` (must differ),
`cmp fine.bin` (must not). 3.5 h for the full B fine pass, so run it on one 256-record batch:
`brun .016 .005 x.bin xbad.bin - batches/f0.bin`.

---

## k3-6 (MINOR) Control 4's pass condition tests the build, not the harness

`-ffast-math` is refused by the probe's own preprocessor test (`abi-fp-probe.cpp:18–20 #error`,
verified: `g++ -ffast-math abi-fp-probe.cpp` → `error: #error Fast math is not permitted`). That is
a property of the mutated source, not of any comparator, and it only fires if the harness applies
the flag to the probe (`build.sh:17`, `:19`). Mutating the *programs* (`build.sh:22–25`) leaves the
probe untouched; and per k3-2 the artefact does not move. Keep the probe as a build assertion — it
is a good one — but do not count it as a mutation control, and do not record it as evidence that
"the harness is sensitive to fast-math".

---

## k3-7 (MINOR) Control 5 has two sites on two rungs; write it with the site named

- `seed.cpp:46` `return !(l>r+1e-8);` → `!(l<r+1e-8)`. **Measured** at n=12 with `seed.cpp`'s own
  main: `xs197 avg y 199.1 counts gap 38368 share 34782` → `xs387 avg y 416.9 counts gap 129033
  share 26`. The seed set nearly doubles and the share test collapses from 34 782 to 26, so
  `centers.txt` must change → **R2 fails on content** (and covrun gets slower; expect xs≈4·10⁴ and
  a cover pass of tens of minutes, so give it a generous timeout).
- `ub.cpp:207` `if(d.e.c[j+4]>t || -d.e.c[j+4]>t+.5*b.z*b.z)return false;` → `<` on the first
  clause: `scalar()` then rejects almost everything, changing the patch sets and the `c.scalar`
  counter (`patchx.cpp:428`) → **R3 fails**.
  Use the `seed` variant for the cheap control; keep the `scalar` one as the R3 control.

---

## k3-8 (MINOR, resolves §6's escalation) Control 8 is caught by the shipped checker — verified

`check_records.py` finishes its record iterator with `need(stream.read(1)==b"", f"trailing
bytes: {path}")`, and `Records.verify()` (called from `NumericalCheck.records()` for every data file
it names) exhausts the iterator, so one appended byte is caught:

```
clean tree:            {"result": "PASS within numerical consistency scope", …}     4.9 s
printf 'A' >> data/coarse0.bin
                       {"result": "NOT ESTABLISHED",
                        "error": "trailing bytes: …/data/coarse0.bin"}             exit 1
truncate 1 byte of mid.bin
                       "error": "truncated record: …/data/mid.bin/599"            exit 1
swap records 0,1 of batches/f0.bin
                       "error": "batch differs beyond radius or insertion order: 0" exit 1
```

So the shipped checker is order-sensitive within a batch, and frame-length-exact. §6's conditional
finding for D resolves negative: it does not miss the appended byte.
The caveat is what control 8 actually tests: `commands.json` carries no digests (child fields are
`stage, argv, inputs, outputs, returncode, completed, stderr_empty`), so no byte-level corruption
is caught by the *record*; it is caught because the checker re-derives each frame length from `k`
and demands EOF exactly. That is a statement about `check_records.py`, not about our harness, and
WU-10's "20 seeded corruptions" should therefore be phrased as tests of the checker's frame
re-derivation, with mutation 8 as one of the 20.

---

## Ranked: which control a naive harness misses, and why

1. **Control 7** — missed by every harness that only reproduces the recorded run, because the
   mutated line is unreachable (k3-1). Not a harness defect: a plan defect.
2. **Control 4** — missed whenever `-ffast-math` is applied to the programs (which is what
   "mutation" means here) rather than to the probe; artefact identical (k3-2, k3-6).
3. **Controls 1 and 3** — missed by any harness that runs the controls at R2 (k3-2). Detected at
   R3.
4. **Control 6** — caught by everything, including a comparator that sorts records; so it is not
   the order-sensitivity control it is claimed to be (k3-5).
5. **Controls 2, 5, 8** — sound, with the rung/site caveats above.

**Escalate first: k3-1.** It is the only one that makes a gate item unsatisfiable, and the fix is a
decision (what counts as a control), not more work.

## Files

- `probe/cov/{base,fast,up,fm}/` — truncated-covrun variants + builds; outputs in `probe/cov/out/`
  (`c-*.txt` the artefacts, `s-*.txt` the stdout, `t-*.txt` the timings).
- `probe/A/{base,fast,up,rn}/` — `arun` variants; `probe/A/out/centers200.txt`, `coarse-*.bin`.
- `probe/a`, `probe/b` — standalone `ub.cpp` driver, seed 42 vs 43, with outputs `o42.txt`,
  `o43.txt`, `o42b.txt` (the repeat run showing the timing line is nondeterministic).
- `probe/chk/` — copy of the saved-run execution tree, run of the shipped checker clean and with a
  byte appended to `data/coarse0.bin` (`ok.txt`, `bad1.txt`).
