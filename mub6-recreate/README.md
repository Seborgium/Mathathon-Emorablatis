# mub6-recreate — reproduction of the covering step in the dimension-six MUB verification record

This directory is self-contained: the code, the harness, the evidence and the paper describing what
was reproduced and what was not.

It reproduces, from scratch, the first program of the verification record published with
[*The maximum number of mutually unbiased bases in dimension six*](https://github.com/openai/math)
(OpenAI, 24 September 2026): the covering step that turns a 112-bin seed enumeration into 249 878
covering centres. The output matches the recorded `centers.txt` byte for byte (7 339 546 bytes,
SHA-256 `c48bc9a2…789`) and matches all five of the program's internal counters.

    paper/mub6-recreate.pdf      the report: method, results, what the prose determines, limits

## Layout

| path | contents |
|---|---|
| `src/` | the canonical implementation: `include/seed.hpp`, `include/cover.hpp`, `src/covrun_main.cpp`, `tests/` |
| `alternates/five-tu/` | the second, independent implementation (five translation units) that also reproduces the file |
| `alternates/arithmetic/` | the arithmetic core, checked bit-for-bit against a probe that includes the published `seed.cpp` |
| `alternates/cover/` | a third re-derivation of the cover, with a bitwise fixture against the published `covout.cpp` (7 670 878 checks) and an exact accounting of every candidate pair |
| `alternates/cleanroom/` | the prose-only reconstruction used to measure what the manuscript alone determines |
| `harness/` | `verify_R2.sh` (build, run, compare), `replay.sh` (replays the 100 recorded commands), `check_records_indep.py` + `v2-check.sh` (independent record checker), `selftest.sh`, `check_order.py`, `audit_format.py` |
| `docs/interfaces.md` | the frozen contract: arguments, formats, constants, determinism register |
| `docs/apparatus-findings.md` | three measured properties of the published verification apparatus |
| `docs/wave-1-cleanroom.md` | the clean-room measurement in full |
| `evidence/` | the JSON logs every claim is drawn from |

## Quick start

```sh
bash harness/verify_R2.sh --src src --log evidence/R2.json   # ~7 min: build, run, compare
bash harness/replay.sh selftest           # <1 s: 100 commands against the record
bash harness/replay.sh control            # ~1 s: 12 planted corruptions must be caught
bash harness/v2-check.sh                  # ~90 s: independent checker, 28 corruption cases
bash alternates/arithmetic/test/run_all.sh  # ~30 s: bit-exactness of the arithmetic core
```

Expected: `R2: PASS (whole)`; `100/100`; `12/12`; 25 of 28 corruptions rejected with the three
expected-accept cases named; `ALL CHECKS PASSED`.

`verify_R2.sh` needs the recorded reference at `.scratch/gh/data/centers.txt`; `replay.sh` fetches the
recorded tree with `harness/fetch_saved_run.py` if it is absent.

## What is established, and what is not

Established: the covering step reproduces the recorded artefact byte for byte and decision for
decision, from three builds — two independently written implementations, and a third with `-O2` and no
`-march=native` (623 s against 524 s) — so identity here is not fragile to the compiler flags; the arithmetic is bit-identical to the published
source; the stage has a minimum interval slack of 1.043e-9 over 4.74e9 tests, so it has no knife-edge;
the manuscript's prose determines the seed set but not its order.

Not established: the three refinement stages (`arun`, `brun`, `crun`) are not re-derived; the
100-command pipeline has not been replayed with this build; nothing here bears on the theorem itself.

## Provenance

Upstream: `github.com/openai/math`, `preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/verification/saved-run/`,
commit `42907c9e` (2026-10-26), Apache-2.0. Nothing of the published record is copied here, with one
exception: `alternates/arithmetic/test/seed_orig.cpp` is the published `seed.cpp` verbatim
(© OpenAI, Apache-2.0), kept because the bit-exactness probe includes it; its SHA-256 is checked
against the manifest on every run. `harness/fetch_saved_run.py` retrieves everything else. See
`src/PROVENANCE.md` for the per-module derivation record.

The working tree, the gate ledger and the team reports this package was assembled from are in
`work/10-recreate/`, with the plan at `results/recreate-code-plan.md`.
