# m1 deliverables — fidelity/status audit pipeline, §2 gap layer, hypotheses ledger

from: T4 / m1 (direction d4)
to: the merge (T4 lead / T8), and anyone running the status table
version: 2 — **supersedes version 1**, whose headline finding about Lemma 5.1 was wrong and is
retracted (see "Retraction" below).

## Files added to `work/04-lean/` by m1

| file | what it is |
|---|---|
| `Mub6/Gap.lean` | circular multisets (`CircDistLE`, `IsEmptyArc`, `NearMap`, `GapLE`, `circGap`) and **paper Lemma 2.5 proved** in three forms; no `sorry`, standard axioms only |
| `Mub6/Hypotheses.lean` | `CodeClaims` (the 18 `S` claims as named hypotheses), `RunReport` + `TerminalConditions` (§7.2 as data), §7.5 Table 1 arithmetic checked |
| `audit/spec.py` | the fidelity data: one row per declaration, with paper locator, verbatim quote, binder-by-binder audit, deliberate changes, code-dependence disposition |
| `audit/audit.py` | report generator: compiles the merged tree, dumps `#check @decl` and `#print axioms decl`, writes `reports/statements-m1.md` and `reports/status-m1.md` |
| `reports/statements-m1.md` | **generated** fidelity table over the merged tree: 36 rows, 35 resolving to real declarations, 1 pending (Lemma 5.1 — `Refine.lean` is a stub) |
| `reports/status-m1.md` | **generated** proof status: compiles yes/no, remaining goals, axiom footprint (`sorryAx` is derived, so a hole cannot hide) |
| `reports/DEPGRAPH-m1.md` | module DAG, claim dependencies, infrastructure vs assembly, Mathlib reuse map, **conformance with the merged interface (§5)**, **the public `openai/math` development (§6)** |
| `handoff-1-m1.md`, `handoff-2-m1.md` | to T8 and T9. `handoff-{1,2}.md` already exist (other members); the m1 versions are additions — in particular `handoff-1-m1.md` retracts the Lemma 5.1 finding |

## How to regenerate

From `work/04-lean/`:

```sh
python3 audit/audit.py       # writes Audit-m1/Dump.lean + reports/{statements,status}-m1.md
```

It compiles every module of the tree in dependency order into `.build-m1/` (no `lake`, no writes
outside this directory), then elaborates one `#check`/`#print axioms` pair per row. Rows appended
to `audit/spec.py` (fields `decl`, `module`, `paper`, `tag`, `quote`, `binders`, `changes`,
`code_dep`, `owner`) appear in both reports automatically.

## Retraction (important for the record)

An earlier version of this submission claimed Lemma 5.1 is **false as printed** and needed an extra
hypothesis `T*T ⪰ (1 − o_P)I`. **That was wrong.** Definition 4.1's (4.4) contains the two-sided
Gram bound `‖T*T − I‖ ≤ ort`, which yields both `‖T‖² ≤ 1 + o_P` (Remark 4.2, a consequence) and
`T*T ⪰ (1 − o_P)I`; expanding `‖Ax‖² = ‖x‖² − 2‖ζ‖² + ‖Tζ‖²` then gives Lemma 5.1 for every `x`,
with no horizontality condition. My proposed witness (`T = εP`, `o_P = 0`) violated (4.4). The
claim is retracted in `audit/spec.py` (Lemma 5.1 row), `reports/statements-m1.md`,
`handoff-1-m1.md`, `handoff-2-m1.md`, and corrected on the swarm board. What survives, correctly
stated: the formal statement must take (4.4) itself as the binder (or `T*T = I`), not the weaker
`‖T‖ ≤ √(1+o_P)`, and must add no horizontality hypothesis on `x` or on the columns of `T`.

## Conformance with the merged interface (checked, not assumed)

`Mub6/Interface.lean` (`Mub6.Cover`: `Cert`, `Covered`, `accumulate_covered`, `Cov`) plus
`Mub6/AssemblyCover.lean` (`prop_2_10`, `prop_3_11`, `prop_4_16`, `prop_5_7`, `prop_6_9`,
`theorem_7_1`, `theorem_1_1`) are the merged assembly. The fidelity rows for the six paper
statements point at those declarations, and each `code_dep` cell names the `CodeClaims` field that
supplies the corresponding S-premise. One gap is recorded rather than papered over: **§7.2's
terminal conditions are not a hypothesis of `theorem_7_1`** — the interface absorbs them into the
existence of each `Cert` and the chain of `Cov` links between named sets. `TerminalConditions` +
`CodeClaims.driver_bookkeeping_identifies_records` are exactly the missing premise; closing it
needs the record identities, i.e. an `S`-claim about the file formats. See `reports/DEPGRAPH-m1.md`
§5.

## Known defects in the merged tree that m1 did not fix

1. **Lemma 2.5 exists twice**: `Mub6/Seed.lean` states `Mub6.gap_stability` in the sorted-list
   carrier and leaves it `sorry`; `Mub6/Gap.lean` proves the same lemma in the arc carrier with no
   sortedness and no permutation. The missing lemma is the bridge
   `seedGap x = circGap (image x univ)` for sorted representatives in `[0,1)`; proving it removes
   the `sorry` and reconciles the two carriers.
2. Lemma 5.1 has no declaration at all (`Mub6/Refine.lean` is a stub).
3. `github.com/openai/math`'s `lean/OAI/Analysis/MutuallyUnbiased/` is a parallel development.
   Either rehome this tree under it, or record in the status report why the parallel tree is
   deliberate and list the statements it duplicates. See `reports/DEPGRAPH-m1.md` §6.
