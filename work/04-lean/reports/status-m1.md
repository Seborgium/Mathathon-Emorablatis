# Proof status (generated — separate from source fidelity)

This table answers ONE question per declaration: what does Lean accept? It says
nothing about whether the statement matches the paper; that is `reports/statements-m1.md`.
The two are never merged into one judgement.

Dump run: `lean Audit-m1/Dump.lean` -> exit 0.

Axiom footprint key: `none` = proved outright; `propext, Classical.choice, Quot.sound`
= only Lean's standard axioms (the normal footprint of ordinary mathematics);
`sorryAx` = the declaration is STATED ONLY (it, or something it uses, has a hole).

## 1. Declarations present in this tree

| declaration | module | compiles | remaining goals | axiom footprint |
|---|---|---|---|---|
| `Mub6.CircDistLE` | Mub6.Gap | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.IsEmptyArc` | Mub6.Gap | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.NearMap` | Mub6.Gap | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.GapLE` | Mub6.Gap | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.circGap` | Mub6.Gap | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.isEmptyArc_transfer` | Mub6.Gap | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.gapLE_transfer` | Mub6.Gap | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.circGap_stability` | Mub6.Gap | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.IsEmptyArc.le_one` | Mub6.Gap | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.circGap_le_one` | Mub6.Gap | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.three_mub_exists` | Mub6.ThreeMUB | yes | 1+ (sorryAx) | propext, sorryAx, Classical.choice, Quot.sound |
| `Mub6.extendible_iff_all` | Mub6.Hadamard | yes | 1+ (sorryAx) | propext, sorryAx, Classical.choice, Quot.sound |
| `Mub6.expMat_Pi_rephasing` | Mub6.Hadamard | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.frameMat_sq_singular_pair` | Mub6.Frames | yes | 1+ (sorryAx) | propext, sorryAx, Classical.choice, Quot.sound |
| `Mub6.norm_exclusion` | Mub6.Exclusion | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.directional_exclusion` | Mub6.Exclusion | yes | 1+ (sorryAx) | propext, sorryAx, Classical.choice, Quot.sound |
| `Mub6.ellipsoid_containment` | Mub6.Ellipsoid | yes | 1+ (sorryAx) | propext, sorryAx, Classical.choice, Quot.sound |
| `Mub6.offset_ellipsoid_bound` | Mub6.Ellipsoid | yes | 1+ (sorryAx) | propext, sorryAx, Classical.choice, Quot.sound |
| `Mub6.StageC.distinct_labels` | Mub6.Exclude | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.AssemblyCover.prop_2_10` | Mub6.AssemblyCover | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.AssemblyCover.prop_3_11` | Mub6.AssemblyCover | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.AssemblyCover.prop_4_16` | Mub6.AssemblyCover | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.AssemblyCover.prop_5_7` | Mub6.AssemblyCover | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.AssemblyCover.prop_6_9` | Mub6.AssemblyCover | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.AssemblyCover.theorem_7_1` | Mub6.AssemblyCover | yes | 0 | none |
| `Mub6.RunReport` | Mub6.Hypotheses | yes | 0 | none |
| `Mub6.TerminalConditions` | Mub6.Hypotheses | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.table1_consistent` | Mub6.Hypotheses | yes | 0 | propext |
| `Mub6.table1_has_terminal_shape` | Mub6.Hypotheses | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.CodeClaims` | Mub6.Hypotheses | yes | 0 | none |
| `Mub6.Cover.Cert.covered` | Mub6.Interface | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.Cover.accumulate_covered` | Mub6.Interface | yes | 0 | propext |
| `Mub6.AssemblyCover.seed_radius` | Mub6.AssemblyCover | yes | 0 | propext, Classical.choice, Quot.sound |
| `Mub6.gap_stability` | Mub6.Seed | yes | 1+ (sorryAx) | propext, sorryAx, Classical.choice, Quot.sound |
| `Mub6.AssemblyCover.theorem_1_1` | Mub6.AssemblyCover | yes | 0 | none |

## 2. Declarations in scope but not in this tree

| declaration | paper locator | owner |
|---|---|---|
| `~Mub6.operator_bounds` | Lemma 5.1 | d1 (m3); Mub6/Refine.lean is a STUB in the merged tree, so 5.1 is not yet formalised |

## 3. Elaboration diagnostics

No errors and no warnings.

