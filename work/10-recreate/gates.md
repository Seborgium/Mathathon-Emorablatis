# Gate log — recreation programme

| gate | state | criterion | evidence |
|---|---|---|---|
| G-R0 spec frozen | **passed** 2026-11-14 — 4 critic reports, 32 findings, all applied; residual items are harness or parameters scope, not spec | `spec/interfaces.md` covers every CLI argument, constant, record field, exit code and determinism source; K signs that it under-determines nothing that changes output | `spec/interfaces.md`, `findings/K4-*.md` (K4-1 blocker: bucket grid was K=3/m=38, corrected to K=4/m=28) |
| G-R1 reproduction base | **passed** 2026-11-14 — `src/unit0304` reproduces `centers.txt` byte for byte (sha256 `c48bc9a2…`, 400.8 s), format audit OK, determinism OK, ABI probe run, compiler and flags logged. Confirmed independently by two further builds: faithful (524 s) and `-O2` without `-march=native` (623 s) | R0 (probe passes on build host, toolchain logged), R1 (seed/covout unit tests reviewed), R2 (our `covrun` reproduces `centers.txt` byte for byte, sha256 `c48bc9a2…`) | `logs/R0.json`, `logs/R1.json`, `logs/R2.json`; WU-10 accepted 2026-11-14 (`harness/v2-check.sh` 25/25 rejections, 677 checks on the recorded set); WU-11 accepted 2026-11-14 (`harness/replay.sh` selftest 100/100, control 12/12); unit 04 accepted 2026-11-14 (writer reproduces the recorded bytes from the order rules alone); unit 03+04 re-derivation accepted 2026-11-14 at `.ultramath/smwgt1mbm/m4/` |
| G-R2 core | pending | R3 (`coarse0..3.bin` byte-identical, `bad0..3.txt` empty); `ub`/`patchx` unit tests reviewed; mutations 1–3 break the harness | `logs/R3.json`, `findings/K-*` |
| G-R3 refinement | pending | R4 (`mid.bin`), R5 (`fine.bin` + 88 batches + `done.txt`) byte-identical; ordering mutations 6–7 behave as specified | `logs/R4.json`, `logs/R5.json` |
| G-R4 exclusion and replay | pending | R6: all 100 commands replay, return codes match (85×0, 15×1), final bad files empty, the shipped checker passes with our `data/` + recorded `results/`, and our checker passes on our data | `logs/R6.json` |
| G-R5 handover | pending | one-command clean-tree rerun; `docs/` complete; `state/final.md` traceable; no open blocker | `docs/`, `state/` |

## Baseline already measured (before any team)

- Upstream `build.sh` builds on this VM; `abi-fp-probe` passes both ways (gcc 16.2.0).
- Upstream `covrun` reproduces the recorded `centers.txt` exactly: sha256 `c48bc9a2…`, 7 339 546 B, 402 s.
- Upstream `arun` part 0 on the first 200 recorded centres: 4.30 s, 21.5 ms/centre, `failedBalls 0`.
