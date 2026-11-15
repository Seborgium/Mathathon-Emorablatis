# Stage-cost budget for a full replay (measured, not extrapolated from the paper)

Method: `bash work/10-recreate/harness/replay.sh replay .scratch/gh/build --only '<cmd>'`,
executing the published binaries against the recorded inputs, one command per process,
wall clock from the replay log (`elapsed_ms` in `logs/replay/R*.json`).
Nothing here ran the full pipeline.

## Measured on this VM (4 vCPU, gcc 16.2.0 build in `.scratch/gh/build/`)

| command | records | wall | s/record |
|---|---|---|---|
| `C.batch0` (256-rec batch) | 256 | 29.3 s | 0.114 |
| `C.batch3` (256-rec batch, rc 1) | 256 | 31.4 s | 0.123 |
| `C.batch87` (short last batch) | 107 | 9.5 s | 0.089 |
| `C.final0` | 282 | 24.1 s | 0.085 |
| `C.final1` | 282 | 22.0 s | 0.078 |
| `C.final2` | 282 | 22.3 s | 0.079 |
| `C.final3` | 281 | 24.2 s | 0.086 |

Repeat runs of the same commands on a busier VM gave 0.17–0.23 s/record, so treat stage C
as 0.09–0.23 s per record depending on load; the spread is contention, not algorithm.

Baselines already measured before this wave (`work/10-recreate/INDEX.md`):
`covrun` 402 s for 249878 centres; `arun` 21.5 ms per centre, i.e. 1343 s per part of
62470 centres.

## Projections (single process at a time)

| stage | count | per unit | total |
|---|---|---|---|
| `covrun` | 1 | 402 s | 402 s |
| `arun` parts 0–3 | 4 | 1343 s | 5373 s (90 min) |
| `brun` Bmid, Bfine, Bfallback | 3 | not measured | — |
| `crun` C.initial | 22379 rec in 88 batches | 0.09–0.23 s/rec | 2000–5150 s (33–86 min) |
| `crun` C.final parts 0–3 | 1127 rec | 0.085 s/rec | ~100 s |
| **total** | | | **~2 h 10 min + stage B** |

## With 4 CPUs (independent commands in parallel, which is what the recorded schedule allows)

`arun` 0–3 are independent (1343 s wall for all four), the 88 `crun` batches are independent
(22379 × 0.115 / 4 ≈ 640 s wall), the four `C.final` parts are independent (~25 s wall):

    covrun 402 + A 1343 + B (n/a) + C.initial 643 + C.final 25  ≈ 2410 s + stage B ≈ 40 min + B

Caveat: one `crun` process keeps one core busy (2 m 43 s wall used 2 m 37 s user over seven
sequential commands), so the speed-up is lane parallelism only. Stage B is the one stage
with no measurement here; its recorded stdout counters suggest the largest work is
`Bfine` (600 parents, 22 379 refinements), so budget B as the largest single unknown.
