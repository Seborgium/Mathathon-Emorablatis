# Recreation programme — index

Plan `results/recreate-code-plan.md`; decision D6; gate ledger `gates.md`; frozen contract
`spec/interfaces.md`.

| artefact | owner | state |
|---|---|---|
| `spec/interfaces.md` | O | drafted 2026-11-14, frozen for comment; K sign-off pending (G-R0) |
| upstream pointer + hashes | O | done |
| `src/` (units 03–09) | C | W1 covers units 03/04 only |
| units 03+04 **integrated, R2 passed** | desk | `src/unit0304/`; `logs/R2.json`: byte-identical, 400.8 s `-O3 -march=native -ffp-contract=off`, gcc 16.2.0 |
| units 03+04 re-derivation (accepted) | C/m4 | five-TU modular build; `results/mine-centers.txt` byte-identical to the recorded file and every counter identical; 759.6 s against the published 401.8 s |
| unit 04 serialisation (accepted) | C/m1 | `.ultramath/smwgt1mbm/m1/` — writer + strict reader + 7-part test, `C-TEST PASS`, rebuilds all 7 339 546 bytes to `c48bc9a2…`; wire-in recipe in `c-NOTES.md` N14 |
| `harness/` (units 02, 10, 11) | V | WU-10 accepted (independent checker, 25/25 rejections, 677 checks); WU-11 accepted (`harness/replay.sh`: selftest 100/100 over 196 artefacts / 82.3 MB, control 12/12, replay of 2 commands 52 s byte-identical); unit 02 in progress |
| swarms C, V, K | all | **closed solved** 2026-11-14: C 6/6, V 3/3, K 4/4 reports accepted |
| `findings/` | K | **swarm closed, 4/4 reports accepted**: K4 provenance map (9), K1 spec attack (15), K2 harness attack (12), K3 mutation controls (8). 32 findings applied. |
| `docs/` | D | not started (W2) |
| `state/` | S | not started (W1 digest pending) |

## Distribution package (2026-11-14)

`mub6-recreate/` — self-contained: `src/` (canonical implementation), `alternates/` (the independent
five-TU build, the arithmetic core, the clean-room probe), `harness/`, `docs/`, `evidence/`, and
`paper/mub6-recreate.pdf` (11 pp., titles the result as the covering step plus the prose measurement).
Smoke-tested from its own directory: `verify_R2.sh --stop-t 200` → `R2: PASS (prefix)`.

## Live runs

| swarm | team | members | window | started |
|---|---|---|---|---|
| `smwgt1mbm` | C (coding 03/04) | 6 | 120 min | 2026-11-14 |
| `smwgt1mdy` | V (harness 02/10/11) | 3 | 120 min | 2026-11-14 |
| `smwgt1mg2` | K (critics) | 4 | 90 min | 2026-11-14 |

## Baseline facts (measured before staffing)

- Upstream builds on this VM with gcc 16.2.0; both probe builds pass.
- Upstream `covrun` reproduces the recorded `centers.txt` exactly: `c48bc9a2…`, 7 339 546 B, 402 s.
- Upstream `arun` part 0: 21.5 ms per centre, `failedBalls 0` on the first 200 recorded centres.
