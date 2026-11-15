# d3 / m2 — Lean-checked global assembly over abstract input interfaces

**Status: the assembly is proved; every premise of it is still a hypothesis.** Nothing here states or
implies $N(6)=3$. The file proves one implication — *given* a seed cover, *given* per-seed Stage-A cell
trees with no unresolved leaf, *given* a per-pass refinement step for Stage B, *given* completed
negative Stage-C verdicts on the last frontier — no point is extendible. Each premise is a named field
of one structure, each is separately falsifiable; the three central data premises are each shown
indispensable by a finite countermodel, and the "no unresolved cell" condition by a separate control.
What is missing is evidence for the fields, not logic.

Files (all under `.ultramath/smwh5efk8/m2/`):

| file | what it is |
|---|---|
| `Mub6AssemblyScoped.lean` | 493 lines, `import Mathlib` only; all theorems proved, no `sorry`, no `native_decide` |
| `AxiomReport.lean` | `#print axioms` on every declaration + `#check` of the two statements the report quotes |
| `run.sh` | rebuilds the olean and the axiom report, logs with `/usr/bin/time`, greps for forbidden devices |
| `logs/build.log`, `logs/axioms.log`, `logs/run_all.log` | the actual output quoted below |
| `field_audit.py`, `logs/field-audit.json`, `logs/field-audit.log` | maps each `Chain` field to the archived quantity that would discharge it, tri-state |
| `.scratch/backup{1..5}.lean` | intermediate compiles (not part of the deliverable) |

## What ran

```
lean --version        Lean (version 4.33.1, x86_64-unknown-linux-gnu, commit 819816b2)
export LEAN_PATH=$PWD:$LEAN_PATH
lean -o Mub6AssemblyScoped.olean Mub6AssemblyScoped.lean   BUILD  wall 3.75 s  user 3.16 s  sys 0.69 s
lean AxiomReport.lean                                      REPORT wall 2.62 s  user 1.80 s  sys 0.64 s
python3 field_audit.py                                     exit 0, 9 rows written to logs/field-audit.json
```

`user` is CPU time; `wall` is contended (4 shared CPUs, five other members running) and varies by
run. The file itself also compiles with the environment's `LEAN_PATH` alone and no `Mub6` olean in
scope, because it imports Mathlib only.

## What is proved

1. **`Box.mem_split` — the subdivision has no gaps.** For a closed box `B ⊆ ℝ^n` and its `2^n`
   children (`Box.split B k`, coordinate `j` cut at its midpoint, `k j` choosing the closed upper or
   lower half), every `x ∈ B` lies in some child. Boundary points lie in both neighbours, which is why
   the children must be closed: `split_boundary_check` proves `1/2` is in both children of `[0,1]`
   while `1/4` is not in the upper one. This is the paper's "the two closed children in each
   coordinate cover the parent interval; their sixteen products cover the parent cell" (here `2^n`,
   for arbitrary `n`).
2. **`seed_bin_dist_le` — the arithmetic half of Proposition 2.10, proved not quoted.** If
   `|x j - m j| ≤ 1/(2·112)` for all nine coordinates then
   `Real.sqrt (∑ j, (x j - m j)^2) ≤ 3/224`, and `seed_bin_lt_radius : 3/224 < 0.032`. The remaining
   `0.0320001` (Section A's joint binary-midpoint error below `10^-14`) is **not** formalised.
3. **`CellTree.covers` — the branch-following argument of Proposition 3.11.** `CellTree` has exactly
   three constructors: `excl` (no extendible point with seed coordinates in this cell), `ball` (every
   such point lies in record `b`'s closed ball), `node` (all `2^n` `Box.split` children certified).
   There is no fourth constructor for a live/capped/failed cell, so "the run closed with zero
   unresolved cells" is the *type* of a term, not a side condition. The proof follows the paper's
   sentence: take the point, descend through the subdivision (using `mem_split`), and at a leaf either
   the exclusion contradicts extendibility or the ball covers.
4. **`chain_excluded_emb` — the finite refinement chase, with the paper's equivalences.** `frontier i`
   is the list of records live after pass `i`; `hstep` says every exact point of a live record is
   `emb`-equivalent to an exact point of a record on the next frontier; `hfinal` says every record of
   the last frontier carries a completed negative verdict; `hneg` says a negative verdict excludes
   extendibility in its whole closed ball. Conclusion: no point of a first-frontier ball is
   extendible. Proved by `Nat` induction carrying a *different representative* on each pass and using
   `hinv` (Lemma 4.7) to transport extendibility. **This theorem depends on no axioms at all.**
   The un-transported version `chain_excluded` is kept as the core.
   A *failed* parent is not excluded by this formulation: the run re-emits it unchanged into the next
   bad list, so it reappears as the same record on the next frontier and `hstep` holds with
   `b' = b`, `y = x`. What `hstep` forbids is dropping the record or substituting a different ball
   with no witness — precisely "handing off an unexploded box".
5. **`Chain.no_extendible` — the scoped assembly.** `Chain Pt Ball` bundles 22 fields, each documented
   with the paper proposition it encodes; the theorem is `Chain.no_extendible (C : Chain Pt Ball) :
   ∀ x, ¬ C.ext x`. `Chain.false_of_four` is the conditional contradiction from `∃ x, C.ext x`.
6. **The interface list is satisfiable and the premises are load-bearing** (see below).

## The interfaces, and what would discharge each

Four of the 22 fields are the `emb` structure (the equivalence relation and Lemma 4.7's invariance);
the rest are the paper's stage obligations. `field_audit.py` reads only JSON
artefacts, never prose, and answers for each stage field one of `DISCHARGED_NUMERICALLY`,
`NOT_DISCHARGEABLE`, `INTERFACE_ONLY`:

| `Chain` field | paper | status from the archive | quantity / why not |
|---|---|---|---|
| `hseed` | Prop 2.10 | INTERFACE_ONLY | `centres=249878`, `checked_pairs=151744086` — the coverage *relation* exists, the 2.10 induction from pairs to a ball cover is not formalised here (this is the archive's own counter; it is not the same counter as the H1 "151,742,926 covered pairs" figure, and I re-derived neither) |
| `tree` (+ `𝔅`) | Prop 3.11 | **NOT_DISCHARGEABLE** | cell counts only (`C.Bfallback`: base 2386483, inside 515243, live 17207, snaps 17207, split 0, fail 0; upstream inside-cell obligations 321004555). No per-cell verdict is archived, so a tree with a verdict at every leaf cannot be built |
| `hball_le` | Prop 4.16 | **NOT_DISCHARGEABLE** | only coarse-archive counts (764/774/757/788 per shard); no per-ball A→coarse write-out map |
| `frontier`, `hstep` | Prop 5.7 / Cor 5.8 | **NOT_DISCHARGEABLE** | fallback parent `bad10#0`: 11480 outside + 1709 relation-covered of 14641 boxes, **1452 without an archived merge mediator**. The run's own `fail0`/`split0` counters are not a refinement witness |
| `hfinal` on the **final** frontier | Prop 6.9 + §7.2 | DISCHARGED_NUMERICALLY | four modulo-4 shards 282/282/282/281, `union_is_all=true`, and all 1,127 final records are completed negatives (`nopattern=23343 = 22216 initial + 1127 final`) |
| `hfinal` on the **initial** frontier | Prop 6.9 + §7.2 | **NOT_DISCHARGEABLE** | `capped=163` at exactly 5000001 steps: a cap is an unresolved search, not a negative verdict. So the initial pass cannot terminate the chain and the fallback frontier is load-bearing |
| `Neg`, `hneg` | Prop 6.9 | INTERFACE_ONLY | radii are inside the paper's 0.1: fine max 0.015999906, fb1 max 0.010999811. Whether `nopattern` *means* "negative graph search" is the predicate-fidelity obligation (d1/m1), not certified here |
| `hext`, `emb` fields | Lemma 1.2 / 2.2 / 4.7 | INTERFACE_ONLY | definitional |

Read the rows marked NOT_DISCHARGEABLE critically: the 163 capped records are exactly why the
chain has a fallback pass, and the 1452 unexploded boxes are exactly why `hstep` cannot be asserted
for `bad10#0`. A record count (`fail0`, `bad=163`, 515,243 inside cells) never discharges a field; the
field asks for a witness, and the archive has a count.

## Negative controls and load-bearing checks (all proved in Lean)

* `live_defeats_covers` — `CellTreeLive` is `CellTree` plus one constructor `live` carrying nothing
  (the cap-hit / give-up / failed-frame cell). For the one-dimensional `[0,1]` seed cell with an
  extendible point at `1/2` and an empty family of written balls, the analogue of `CellTree.covers` is
  **false**. So dropping "no unresolved cell" from the assembly is unsound, not merely inelegant.
* `hseed_needed`, `hstep_needed`, `hfinal_needed` — three explicit finite models in which every other
  data interface holds and the conclusion fails (an extendible point survives). `hseed` with an empty
  seed list; `hstep` with one record on the only frontier and nothing on the next; `hfinal` with a
  reachable frontier and no terminal verdict. `emb` is taken as equality in these models, so the three
  structural `emb` fields hold automatically; the models falsify one *data* premise each.
* `consistentChain` / `consistentChain_no_extendible` — the interface is inhabited by non-degenerate
  data (real seed cube, real Stage-A ball leaf, one-pass frontier, real refinement step, terminal
  verdict), so `Chain.no_extendible` is not an implication over an empty class of inputs. The only
  empty field in that witness is `ext` itself — which is forced: any inhabited `Chain` has an empty
  `ext` by the theorem.

## Axiom and device audit

`logs/axioms.log`, from `#print axioms` on all 15 audited declarations (plus two `#check`s of the
statements quoted above):

* `chain_excluded` and `chain_excluded_emb`: **no axioms**;
* every other declaration: `[propext, Classical.choice, Quot.sound]` — Lean's three standard axioms;
* no `sorryAx`, no `Lean.ofReduceBool` (no `native_decide`), no user-introduced axiom;
* `run.sh` fails the build if `:= sorry`, `:= by sorry`, `admit` or `native_decide` appears.

## What still fails — and what a checker must not read into this

1. **No decoder.** There is no Lean definition mapping an archived record file (centre, radius,
   `nopattern` flag) to `Chain.mem` / `Chain.Neg`. The carrier is abstract: `mem` and `Neg` are
   predicates, not parsed bits. A checker cannot conclude "the archive satisfies `Chain`" from this
   file; it can only conclude "if the archive satisfies `Chain`, the conclusion follows".
2. **The bookkeeping links are modelled, not verified.** §7.2's marker completeness, per-batch done
   counts, fallback-input subsequence check and the four modulo-4 final shard partition appear in the
   chase as passes whose refinement is the identity (`b' = b`, `emb x x`). The shard arithmetic itself
   is a record property (282+282+282+281 = 1127, `union_is_all`), audited by `field_audit.py`, **not**
   by Lean.
3. **`tree` is not merely unproved, it is not archived.** The ledger reports counts and `snaps`, not
   per-cell verdicts. A Stage-A cell-certificate tree has to be emitted by an instrumented Asearch
   prefix (that is d4/m6's direction), not reconstructed from this ledger.
4. **`hstep` fails for a named region.** 1452 boxes of `bad10#0` have no archived merge mediator or
   transport; `hstep` is false for them *as archived evidence*. If the run covered them (the report
   says it did, by merge-mediating centres), the witness is missing, not the coverage. My chain says
   exactly this and refuses to pass — that is the intended behaviour, not a defect.
5. **The analytic content is untouched.** `hseed` (2.10, including the `10^-14` margin and the
   `0.0320001` radius), `hneg` (6.9 and its (6.16)/(6.20)/(6.21) predicates), and `hext` (1.2) are
   hypotheses. `seed_bin_dist_le` proves only the `3/224 < 0.032` half of 2.10's arithmetic.
6. **The Root certificate is not a separate field.** `mem b x` says only "`x` lies in the closed ball
   of record `b`". The Root data of Definition 4.1 (the stored tensor `U`, the residual bound, the
   atlas merge of Lemma 4.15) is not modelled, so the assembly assumes records are already
   Root-certified and checks no merge inequality. Adding a `Root` predicate with a bound field is a
   straightforward extension of the structure; omitting it is deliberate, because a field that no
   artefact in the archive can discharge yet would only be decoration.
7. **`emb` is a relation, not an action.** I assume reflexivity, transitivity and invariance of
   extendibility; I do not formalise signed permutations, transposition or rephasing, nor that they
   generate the equivalence used by the run. `hinv` is where a disguised assumption could hide and
   should be read as a hypothesis.

## Handoff

* To use: provide a `C : Chain Pt Ball`. The only work left is producing the fields; no proof work
  inside `Chain.no_extendible` is needed and no case split is deferred.
* To check the assembly itself: `bash run.sh` (≈3 s CPU), then read `logs/axioms.log`.
* To close a field: `tree` needs d4/m6's per-cell verdicts; `hstep` needs d2/m3's mediators;
  `Neg`/`hneg` need d1/m1's predicate fidelity; `hseed` needs the 2.10 induction on the completed
  covout pairs. Until all four land, this file is a proved skeleton with named holes — and the holes
  are exactly the four directions the swarm is working.
* Prior art in the repository: `work/04-lean/Mub6/Interface.lean` and `AssemblyCover.lean` (previous
  window, m3) prove the same composition shape with `Cover.Cert` and `Cover.accumulate_covered`. This
  file does not import them (it is Mathlib-only so that the judge can recheck it without the `Mub6`
  oleans). Differences worth noting: the Stage-A cover here is derived from the *one-step subdivision*
  (`Box.split`, `mem_split`) rather than assumed as a decomposition (`S ⊆ ⋃₀ U`); the chase is
  `emb`-aware and multi-pass; and this file adds the four load-bearing/negative-control theorems and a
  consistency witness, which the earlier scaffold does not have.
