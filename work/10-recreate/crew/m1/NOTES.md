# m1 (team V, W1) — work unit 10: independent record checker

Direction d2 on the swarm board. Files, all under `work/10-recreate/harness/`:

| file | what it is |
|---|---|
| `check_records_indep.py` | the checker. `python3 check_records_indep.py <execution-dir> [--json F] [--verbose]`. Exit 0 PASS / 1 FAIL, JSON on stdout. |
| `mkcorruptions.py` | builds the 28-case seeded-corruption suite (hardlink copies; the pristine tree is hashed before and after and must not change). |
| `v2_check.py` | driver: my checker on the recorded set, then on every case, plus the published checker as a black-box oracle; writes `logs/v2-<date>.json` and `.md`. |
| `v2-check.sh` | the one command: `bash work/10-recreate/harness/v2-check.sh` (~3 min, exit 0 = PASS). |
| `fetch-recorded.sh` | fetches the recorded `saved-run/execution` tree (not in this repo; ~80 MB) by blobless sparse clone. |

## Derivation

`check_records_indep.py` was written from `spec/interfaces.md` §1–§5, the
published sources (`atlas.cpp` `saveRecords`/`readRecords`, `stageB.cpp`
`main`/`validate`/`emit`, `stageC.cpp` `main`, `covout.cpp`), `VERIFY.md` and
`commands.json`. `check_records.py` was **never opened, imported or copied**; it
is executed only as a black box on the same directories, and its verdict is
whatever its own exit status and `result` field say.

Checks are tagged by what forces them: **A** the frozen format (byte layout,
EOF exactness, `k ∈ [0,10]`, the `validate` bounds, zero-length vs 8-byte
count-zero bad files), **B** the recorded run schedule (A shards = 0..3 mod 4;
`results/*.txt` counters equal the artefact record counts — `global`,
`result <n> bad <b> parent<p>`, `done<d> bad<b>`; fine.bin ↔ the 88 batches are
one partition outside the 8-byte radius slot; every `batches/bad<n>.bin` is an
ordered subsequence of `batches/f<n>.bin`; the 15 non-empty failure files are
exactly the `C.Bfallback` inputs in ASCII order; the four final runs cover
`fb1.bin` 0..3 mod 4 and leave count-zero files), **C** empirical invariants of
this data set (`id`, `ort`, `hor` lie in bands 1e-6 wide relative to their
value; every batched record's radius is exactly the `brun` target, because
`stageB.cpp` `emit()` overwrites it).

## Result (logs/v2-2026-11-14T195414Z.json, exit 0)

* recorded set: mine PASS, 677 checks, 2.0 s; published PASS, 7.5 s.
* 25 seeded corruptions: mine rejects 25/25 with the predicted check; the
  published checker rejects 25/25 as well, with its own diagnostics.
* 3 predicted-undetectable cases: **both checkers accept** an in-bounds
  `p` perturbation in `coarse0.bin`, `mid.bin`, `fb1.bin`. Neither of those
  files is byte-compared against any later artefact (only their record counts
  are), so no consistency check over the artefacts can see it.

## What this does NOT verify

* It does not run any program. It says nothing about the C++ implementation,
  the compiler, the CPU or the FP contract; only about the recorded artefacts.
* It is not authentication: the bytes were fetched over git (content-addressed
  against the server's own tree, not against an independently published hash).
  The one hash that *is* pinned in `spec/interfaces.md` checks out:
  `centers.txt` = `c48bc9a2be1eb2cdeea82ea1b030d7cb9f00a6c9563b63f0248dd115748a5789`.
* In-bounds tampering of a parent record that no later artefact is compared
  against (above) is invisible; so is a *coordinated* tampering of fine.bin and
  its batches. Only re-running the preceding stage closes those.
* The A shards are checked as commands, counts and per-record validity; the
  shards cannot be verified to be a partition of `centers.txt` without
  re-running `arun`.
