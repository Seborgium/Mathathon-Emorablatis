# Gate log

| gate | state | criterion | evidence |
|---|---|---|---|
| G0 claim inventory frozen | pending | every numbered claim has id, statement, status, deps, owner; notation table used by the reader path | work/01-catalogue/claims.yaml, notation.tex, reader-path.md |
| G1 controls | pending | d=3 and d=4 exaggerate nothing: they must NOT exclude; d=2 must exclude; the two known cases excluded by a cleared certificate naming the test | work/03-reference/controls/ |
| G2 checker | pending | accepts a valid synthetic certificate; rejects >= 20/20 seeded corruptions; 1000 records in < 10 min; clique-witness route documented | work/02-checker/tests/, spec/cert-format.md |
| G3 parameters | pending | every constant has constraint, slack, cost curve, recommendation; N=112 resolved with a measured curve | work/05-parameters/justification.md |
| G4 formalisation | **met with three named repairs** (see below) | every scoped statement transcribed with an explicit fidelity row; proof status reported separately; assembly interface proved or its obstruction documented | work/04-lean/reports/{statements,status}.md |
| G5 draft | pending | single file compiles, <= 45 pp, 1-page summary + <= 6-page narrative, 12 cited figures, verification appendix <= 4 pp, no claim absent from the inventory | work/08-paper/mub6.tex |
| G6 red team | pending | no open defect above minor; remaining defects printed as limitations | work/09-redteam/findings.md |

## Gate history

- 2026-11-14 W1 launched: swarms smwgrqhwo (T1 catalogue, 6), smwgrqwth (T5 parameters, 6),
  smwgrr7ia (T7 quantum, 3), smwgrrpxy (T4 Lean phase 0, 4). All on deepseek/deepseek-v4.1-flash at
  maximum reasoning effort; 90-150 minute windows.

## Recreation programme (D6)

`work/10-recreate/` runs its own ledger, `work/10-recreate/gates.md`, with gates G-R0 … G-R5. G2 is
restated by D6 as: our checker accepts the recorded data and our reproduction, rejects ≥ 20/20 seeded
corruptions including a one-byte append, and runs the full record set in under 10 minutes.

- 2026-11-14 W0/W1 launched: `spec/interfaces.md` drafted and frozen for comment; swarms C (6 members,
  120 min), V (3, 120 min), K (4, 90 min) on `deepseek/deepseek-v4.1-flash` at maximum reasoning effort.
  G-R0 and G-R1 pending.

## G4 evidence — 2026-11-14

All 14 Lean modules in `work/04-lean/Mub6/` elaborate with `lean`, exit 0, no errors. 23 declared
holes project-wide, all named in the members' status tables:

| file | holes | what is missing |
|---|---|---|
| Basic | 0 | Lemma 2.3 complete; Def 2.1 one-sided; Lemma 1.2's Gauss sums |
| Hadamard | 7 | Lemma 2.2's six clauses (transpose clause invalid as printed; repairable by monomial transport) |
| Seed | 1 | Lemma 2.5's arbitrary matching |
| ThreeMUB | 2 | `FDF_entry`, `three_mub_exists` (the lower bound N(6) >= 3) |
| Frames | 7 | Lemma 3.1 beyond the operator statement |
| Exclusion | 1 | Lemma 3.9's linear bound (needs the paper's `eq` layout as a hypothesis) |
| Ellipsoid | 4 | Lemma 4.12's remaining goals |
| Exclude | 1 | Lemma 6.1 `bin_displacement` — the shared blocker |
| Completion, Refine, Assembly | 0 | claim-free stubs: zero holes because they assert nothing |
| Interface, AssemblyCover | 0 | the assembly implications, proved with every S/C premise a binder |

Not stated at all: §5.1-5.6 (Stage B relations). The status table T8 prints must say so.

## G4 verdict — 2026-11-14, all four T4 members accepted

Met, subject to three repairs that change what T8's status table may say:

1. **`theorem_7_1` does not hypothesise §7.2's terminal conditions.** Verified by reading the
   signature: it takes seven `Cov` hypotheses plus `hCneg` and nothing else. So the paper's
   Theorem 7.1 is two steps — an assembly over covers, and a driver whose bookkeeping realises the
   covers — and the second is not in the formal statement. Add `TerminalConditions` as a binder
   (one member's Hypotheses.lean already has it as data).
2. **Lemma 2.5 is duplicated**: proved in `Mub6/Gap.lean`, still `sorry` in `Mub6/Seed.lean`
   (`gap_stability`). The sorry count is pessimistic where a proof exists.
3. **Lemma 5.1's retraction** is verified in spec.py, statements-m1.md and handoff-1-m1.md. The
   surviving requirement: bind (4.4) itself, never the weaker `||T|| <= sqrt(1+o_P)`.

Standing: Lemma 6.1 `bin_displacement` remains the only Stage-C hole; §5.1-5.6 (Stage B relations)
remains unstated; Completion/Refine/Assembly are claim-free stubs carrying no obligation.

## Swarms — state after wave 1 and 2
T1 catalogue: ended solved, 6 accepted. T5 parameters: ended solved, 5 accepted.
T7 quantum: ended solved, 2 accepted. T4 Lean: ended solved, 4 accepted. Total 17 accepted artefacts.
Not yet launched: T2 (checker), T3 (reference + controls), T6 (figures), T8 (paper), T9 (red team).

## Certificate programme gates (D8/D9)

| gate | state | evidence | decision needed |
|---|---|---|---|
| H0 / feasibility | **ready for human decision** | `results/h0-feasibility.md`; full 92-command byte-identical replay; two accepted Q4 submissions | approve route (a), H1 scope and exact-pilot budget |
| H1 / seed + schemas v1 | pending | — | human initiation |
| H2 / Stage A + atlas | pending | — | human initiation; Q3 authorised but still held |
| H3 / Stage B + C | pending | — | human initiation |
| H4 / assembly + replay | pending | — | human initiation |
| H5 / condensation | pending | — | human initiation |

H0 feasibility completed under D9; D11 reopened it and D12 authorises H1-H5 in an eight-hour execution window. Schemas are still v0, not frozen v1.

### D12 execution note
H1-H5 authorised by the owner with an eight-hour execution window; lead work and Q3/Q4 are active.
Gate acceptance still requires the evidence rows, and condensation will report incomplete checking
as such rather than converting elapsed compute into a theorem claim.

### H1 evidence state (2026-11-15)
H1 is **ready for human gate review**. `certdata/runs/h1-seed-emission/report.md` plus `reproduce.sh`:
exact filtered enumeration + all 151,742,926 mandatory seed-pair outcomes, 249,878 fresh centres,
45,648,766 exact cheap reuses, and 105,845,442/105,845,442 dual reuses proved. No failures,
undecided cases or missing mandatory pairs; 1,160 extra source-checked pairs are rigorously
disjoint. Genuine real-prefix baseline is accepted; 62/62 byte-validated mutations refused.
Zero remaining unresolved seed-cover obligations in this run. H1 is NOT a final theorem certificate,
nor a signed human gate. Exact Stages A--C remain open; the binary-phase conversion enlargement
0.0320001 is an interface explicitly outside this run.

### H2/H3 progress after targeted continuation (2026-11-15)
Composition identifiers and g0's encoding/isomorphism comparison are corrected
and reproducible; see `results/evidence-audit-review.md`. The Stage-B local
source-transport bridge for bad10#0 is now exact for 902 edges and 3161 closed
boxes (see `work/02-checker/reports/H2-stageb-source-transport.md`). Exact
uncapped (6.24) checks are complete on only four distinct real graphs, and
finite seed-symmetry checks are accepted with their measured populations.
Neither H2 nor H3 is globally met: tiny/full Stage-A trees, remaining Root/C
witnesses, analytic graph predicates, the other parents and the final assembly
remain open. No human gate approval is implied.
