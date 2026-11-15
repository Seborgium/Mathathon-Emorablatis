# 01-catalogue — claim inventory and notation (T1)

Frozen at gate **G0**. Downstream teams cite ids from `claims.yaml`; they do not edit these files.

| file | what it is | who reads it |
|---|---|---|
| `claims.yaml` | 86 entries: every numbered claim of the paper plus the 18 load-bearing displays, the §7 execution items and the Appendix A items. Fields: `id, kind, title, paper_locator, one_line_statement, hypotheses, status, status_parts, depends_on, owner_team, evidence, open_questions`. | everyone |
| `dependencies.dot` | claim dependency graph, generated from `claims.yaml`, acyclic (checked mechanically at generation) | T2, T4, T9 |
| `notation.tex` | the three naming systems for the seven Root constants, every letter that carries two objects, the words (bin/cell/box/ball/sphere/Root/Record), and the macro block. Compiles standalone. | T2, T3, T4, T6, T8 |
| `style.md` | writing rules for T8: one reader path, explicit quantifiers, units on every constant, no code claim without a disposition | T8, T9 |
| `reader-path.md` | the six-page undergraduate narrative (no proofs) T8 writes the paper around | T8, T7, T6 |
| `reports/T1-report.md` | what changed vs `results/proof-claims.md`, every S-statement with a disposition, every defect I believe is in the paper | lead, all teams |
| `handoff-1.md` | the interface note: what T2/T4/T8 must take from here and in what form | T2, T4, T8 |
| `changerequests/` | other teams write here; protocol in `changerequests/README.md` | all teams |

## The three conventions a reader must know

1. **`status` is the weakest tag the claim as stated depends on.** A coverage proposition whose
   argument is a proof but whose hypothesis is a completed run is tagged `C`; `status_parts` carries
   the decomposition `M: … ; S: … ; C: …`. Filtering on `status: M` gives the 58 statements that are
   mathematics only.
2. **`owner_team` is who must discharge the claim next**, not who proved it.
3. **Page numbers in `paper_locator` are PDF pages** of `.scratch/mub6.pdf` (77 pp; the printed number
   is one less). Section and equation numbers are authoritative.

`results/` and `attachments/` are read-only to T1; nothing outside this directory is written by T1
except the handoff and change-request conventions stated above.
