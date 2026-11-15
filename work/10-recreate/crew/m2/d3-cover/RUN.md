# RUN — exact commands, exit statuses, evidence (m2, direction d3)

Machine: 4-CPU x86-64 Linux VM, g++ (conda-forge gcc 16.2.0), LANG=C LC_ALL=C.
All commands below run from this directory; every exit status is the shell's.

| # | command | exit | result |
|---|---|---|---|
| 1 | `./c-build.sh` | 0 | builds `build/c-covrun`, `build/c-harness`, `build/c-fixture` with `-std=gnu++17 -O3 -march=native -ffp-contract=off` |
| 2 | `./build/c-fixture 112` | 0 | `FIXTURE-OK checks=7670878 fails=0` — my module vs the published sources, bit for bit, in one TU |
| 3 | `./build/c-harness --dump-seeds run/seeds-n112.bin --out run/prefix3000.txt --tmax 3000 --stats run/prefix3000.json` | 0 | `xs22829 ys829306`; 12111 centres; `PREFIX-OK` |
| 4 | `./build/c-harness --load run/seeds-n112.bin --out run/mine-centers.txt --stats run/full.json` | 0 | 249 878 centres, 797.96 s (build without inlining) — **IDENTICAL** |
| 5 | `./build/c-harness --load run/seeds-n112.bin --out run/abl-<c>.txt --tmax 3000 <opts>` for c in base, K3m38, nogap, noiv, dual0, dual6, nopre | 0 each | table F4 |
| 6 | `./build/c-harness --load run/seeds-n112.bin --out run/mine-centers-inlined.txt --stats run/full-inlined.json` | 0 | 249 878 centres, **434.82 s** — **IDENTICAL** (shipped build) |
| 7 | `./c-verify.py compare .scratch/gh/data/centers.txt run/mine-centers-inlined.txt` | 0 | `IDENTICAL`, sha256 `c48bc9a2be1eb2cdeea82ea1b030d7cb9f00a6c9563b63f0248dd115748a5789` |
| 8 | `./c-verify.py invariants run/mine-centers-inlined.txt` | 0 | `INVARIANTS-OK: header 112 249878, 249878 lines, 7339535 body bytes` |
| 9 | `./c-verify.py invariants .scratch/gh/data/centers.txt` | 0 | same, on the recorded file |
| 10 | `./c-verify.py prefix .scratch/gh/data/centers.txt run/prefix3000.txt` | 0 | `PREFIX-OK: 12111 candidate lines match the first 12111 reference lines` |
| 11 | `./build/c-covrun run/from-covrun.txt` (the program contract: `covrun <out>`, argc==2) | 0 | stdout `xs22829 build13.32` / the published `N112` line / `time 435.21`; output **IDENTICAL**, sha256 `c48bc9a2...` |

The two full sweeps (rows 4 and 6) are two runs of *my* program. No `covrun` from
`.scratch/gh/build` was executed at all: the reference used is the recorded
`.scratch/gh/data/centers.txt`, whose hash the task states and which I re-verified.

## Comparison discipline
`c-verify.py compare` is byte equality on the whole file, no tolerances. `c-verify.py
prefix` compares the body only and reports that the header counts differ: a prefix sweep
legitimately writes `112 12111`. That is a different claim from equality, and it is
labelled as such; no comparison is ever relaxed to make a test pass. The half of the
verification that does not depend on the file at all is the counter equality in row 4/6
(`visit` is a function of the bucket layout, so it pins `K`, `m`, and every scan order).

## Not done here (outside this direction)
- No `arun`/`brun`/`crun` work, no changes to `work/10-recreate/src`, `spec/`, `harness/`.
- The other six published sources were not re-derived by me.
- The 42/123-seeded RNGs, `stable_sort` and `unordered_set` of the determinism register
  belong to other units; this unit has none of them (see WHY-249878.md §1).
