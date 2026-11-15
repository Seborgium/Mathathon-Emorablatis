# handoff-1 — T4 (Lean) to T8 (the single final file)

from: T4 / m1 (direction d4: fidelity & status audit, §2 gap layer)
to: T8 / work/08-paper
version: 1 (phase 0, 2026-09-24 window)
depends-on: `results/proof-claims.md`, `results/code-audit.md`, `results/plan.md` §3 (T4),
            the preprint `attachments/.../The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026.pdf`
            (text at `.scratch/mub6.txt`)
blocks: nothing hard; supplies the status table (§P4.5 of the plan) and the fidelity discipline
         that the paper's formalisation appendix should cite
artefacts (all relative to `work/04-lean/` once merged):
  * `Mub6/Gap.lean` — circular multisets, Lemma 2.5 (Lemma 2.5 **proved**, three forms)
  * `Mub6/Hypotheses.lean` — `CodeClaims` (the 18 `S` claims as named hypotheses),
    `RunReport` + `TerminalConditions` (§7.2's five conditions as data)
  * `reports/statements.md` — generated fidelity table, one row per in-scope declaration
  * `reports/status.md` — generated proof status, axiom footprints
  * `reports/DEPGRAPH.md` — module DAG, claim dependency view, Mathlib reuse map
  * `audit/spec.py`, `audit/audit.py` — the generator (rerun over the merged tree)
  * `lakefile.lean`, `lean-toolchain` — documentation-only build description
claims touched: 1.2, 2.2, 2.3, **2.5**, 3.1, 3.8, 3.9, 4.11, 4.12, 5.1, 6.5 (scope A);
  2.10, 3.11, 4.16, 5.7, 6.9, 7.1 (scope B); §7.2, §7.5 Table 1

## What is actually proved

**Lemma 2.5 (Stability of circular gaps) is proved, with no `sorry` and no axiom beyond
`propext, Classical.choice, Quot.sound`.** Three forms, `Mub6/Gap.lean`:

| Lean name | statement |
|---|---|
| `isEmptyArc_transfer` | an empty arc of length `L` in `A` yields an empty arc of length `L - 2δ` in `B`, given only that every point of `B` is within `δ` of a point of `A` |
| `gapLE_transfer` | an upper bound `t` for the gap of `A` gives the upper bound `t + 2δ` for the gap of `B` |
| `circGap_stability` | the literal paper statement, `|gap A - gap B| ≤ 2δ`, for a two-sided pointwise matching |

The paper's remark "No preservation of the sorted order is used" is confirmed: the formalisation
never sorts. The `L ≤ 2δ` case that the paper dismisses in one clause is discharged by the fact
that an arc of non-positive length is vacuously empty.

**§7.5 Table 1 arithmetic is checked in Lean** (`Mub6.table1_consistent`): 62 470 + 62 470 + 62 469
+ 62 469 = 249 878; 764 + 774 + 757 + 788 = 3 083; 87·256 + 107 = 22 379; 282 + 282 + 282 + 281 =
1 127. This is a consistency check of the bookkeeping, not of the run — label it `E`, as
`results/proof-claims.md` already does.

## What is stated only (and how it should be printed)

Nothing in scope is stated-but-unproved in this tree: the other in-scope statements are owned by
sibling directions (d1 §5–6 + assembly, d2 §3–4, d3 scaffold + §1–2). `reports/status.md` prints
their rows as `PENDING` with the owner, and fills in automatically when `python3 audit/audit.py` is
run over the merged tree. **Print the generated table, not a hand-typed one** — the axiom footprint
column is the only way a reader can tell a proved statement from a quoted one.

## What is assumed (and must be printed as assumed)

1. `Mub6.CodeClaims` — 18 named hypotheses, one per `S` claim of `results/proof-claims.md`:
   `covout_visits_all_tuples`, `seeds_mk_selection_rule`, `sumok_restricted_directions_sound`,
   `extend_dropping_sound`, `supdual_margins_sound`, `stageA_system_matches_equations`,
   `stageA_certificate_is_necessary_test`, `stageA_terminates_fully_resolved`,
   `stageA_unused_routines_supply_nothing`, `patch_certifies_root_data`,
   `candidate_prep_represents_stored_centre`, `completion_search_processes_all_seeds`,
   `stageB_threshold_protocol`, `stageB_no_bad_parents`, `graph_search_false_is_a_certificate`,
   `stageC_clustering_complete`, `stageC_negative_paths_only`,
   `driver_bookkeeping_identifies_records`.
   The paper can print this list as the formal form of Appendix A's "the code does what §2–§6 says":
   it is the *complete* list, and each item is one sentence.
2. `Mub6.TerminalConditions r` — §7.2's five conditions as a predicate on a `RunReport`. This is
   the `C` hypothesis of Theorem 7.1 in printable form: exit statuses, bad-list sizes, the
   partition identity, `unresolved = 0`, and the two Boolean checks.
3. The Appendix A arithmetic contract (the binary64 error model) is **not** modelled here; it is a
   separate binder in the assembly statement. Do not let the paper's status table blur it into (1).

## Findings the paper should fix or explain

1. **Lemma 5.1: RETRACTED claim — the lemma is TRUE as printed.** An earlier version of this
   handoff said its third inequality was not derivable from the stated hypotheses and needed an
   extra lower bound on `T*T`. That was wrong, and the correction matters for the record:
   Definition 4.1's (4.4) contains the TWO-SIDED bound `‖T*T − I‖ ≤ ort`, which gives both
   `‖T‖² ≤ 1 + o_P` (Remark 4.2, a consequence) and `T*T ⪰ (1 − o_P) I`; expanding
   `‖Ax‖² = ‖x‖² − 2‖ζ‖² + ‖Tζ‖²` then gives Lemma 5.1 exactly. My proposed witness violated
   (4.4). The formal statement should take (4.4) as its binder and add no horizontality
   hypothesis; that is all. (Reported on the board as a correction.)
2. **Quantifier-order traps in the four coverage propositions.** Each is written in prose that can
   be read with the quantifiers the other way round; `reports/statements.md` records the correct
   order for each. The three worth checking on the page:
   * Prop. 2.10: `∀ H ∃ (equivalence, centre with its recorded selected position)` — *not*
     `∃ equivalence ∀ H`, and the ball radius is `0.032`, with `0.0320001` a *second, weaker*
     statement after binary conversion;
   * Prop. 4.16: the conclusion quantifies over **extendible** exact `H` only ("required for the
     four-basis problem"); saying it for all exact `H` is a strengthening;
   * Prop. 5.7: the failed-parent term on the right is `S(P,R)` with the **input** radius `R`, not
     the refined `τ`.
3. **Lemma 3.1's `|S| < 4` is stronger than the `K` assertion needs** (at `|S| = 4`, `ker M*` is
   three-dimensional). Keeping it as printed is fine; a reader will ask.
4. **Lemma 6.5's carrier** is phase classes modulo global phase, not `ℂ⁶` vectors — the proof
   "removes global phases" before summing `e(z_j)`. Worth one clause in the statement.
5. **Proposition 6.9's "negative result" must not be read as "not positive"**. Only two paths are
   negative (empty completed bin layer, completed negative graph search); overflow, clustering
   failure, a surviving graph possibility and work-cap exhaustion are *unresolved*. A Boolean
   formalisation would silently equate them, so the assembly statement needs an outcome type with
   four constructors.

## Open questions for T8

* Should the paper print the 18 `CodeClaims` fields as a numbered list (§A.0) and cite the field
  names in §§2–6? That would replace "the code does X" with "`CodeClaims.X`", which is checkable by
  a reader without the sources.
* Does the 6-page narrative path want Lemma 2.5 as its one worked formalisation? It is 3 lines of
  mathematics, 60 lines of Lean, and it is the only in-scope statement proved in this window.
