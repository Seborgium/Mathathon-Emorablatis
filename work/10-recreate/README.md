# 10-recreate — the code-recreation programme (six agent teams)

Plan: `results/recreate-code-plan.md` (approved mode C, 2026-11-14). Decision D6.
Object: the seven C++ sources + probe + build script + checker published with the preprint, re-derived
so that the 100 recorded commands reproduce the recorded artefacts.

## Tree and write scopes

| path | owner | contents |
|---|---|---|
| `spec/` | O (desk) | `interfaces.md` — the frozen contract. Nobody but O writes here; changes are CRs. |
| `src/` | C | modular sources + `amalgamate.sh` + `NOTES.md` per unit |
| `harness/` | V | build scripts, replay driver, comparators, `verify.sh` |
| `logs/` | V | one log per rung, JSON; never edited, only added |
| `docs/` | D | module docs, CLI reference, record format, reproduction guide, provenance |
| `state/` | S | `wave-<n>.md`, `discrepancies.md`, `final.md` |
| `findings/` | K | `<team>-<n>.md`, numbered, each with the test that settles it |
| `crew/` | swarm members | private scratch per member; O collects what it needs |

## Rules

1. `spec/interfaces.md` is frozen at G-R0. Code that disagrees with it is wrong, or files a CR.
2. Propose ≠ certify: a generator proposes, a one-sided check certifies. Never "fix" a certificate.
3. No silent deviation: any choice the spec does not fix goes in the unit's `NOTES.md` with the line
   of manuscript or source that decided it.
4. No team writes outside its scope. Cross-scope requests go to O as numbered CRs.
5. A claim without a command and a log path is not evidence and is rejected at the gate.

## Where the upstream files are

Canonical: `github.com/openai/math`, `preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/verification/`.
Cached for this session at `.scratch/gh/upstream/` (10 files) and `.scratch/gh/data/centers.txt`.
Re-fetch rather than trust the cache once the programme is under way.
