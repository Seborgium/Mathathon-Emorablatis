# Proof status for section m3 (direction `d1`) — separate from source fidelity

Fidelity is judged in `reports/statements.md` §m3.  This file judges only *what the machine
checked*.  Build: `lean Mub6/Interface.lean`, then (with `LEAN_PATH="$LEAN_PATH:."`)
`lean Mub6/Exclude.lean`, `lean Mub6/Assembly.lean` — Lean 4.33.1, Mathlib from `LEAN_PATH`,
validated 2026-11-14 in this window, one compile at a time.  Axiom footprint measured with
`#print axioms` (`.scratch/Ax.lean`).

## Compiled: yes, no `sorry`

| declaration | remaining goals | axiom footprint |
|---|---|---|
| `Cover.Covered`, `Cover.Cert`, `Cover.Cov` (defs) | — | — |
| `Cover.covered_empty`, `Covered.mono`, `Covered.union`, `Covered.iUnion` | none | `propext, Classical.choice, Quot.sound` |
| `Cover.Cert.covered` | none | `propext, Classical.choice, Quot.sound` |
| `Cover.Cert.mono` | none | `propext, Classical.choice, Quot.sound` |
| `Cover.accumulate_covered` | none | `propext` |
| `Cover.Cov.refl`, `Cov.trans`, `Cov.excludes` | none | none |
| `StageC.e_add`, `e_int`, `norm_e` | none | `propext, Classical.choice, Quot.sound` |
| `StageC.sq_nonneg'`, `sq_sub_le`, `sum_abs_le` | none | `propext, Classical.choice, Quot.sound` |
| `StageC.ip_norm_gt` | none | `propext, Classical.choice, Quot.sound` |
| `StageC.distinct_labels` (**Lemma 6.5**) | none | `propext, Classical.choice, Quot.sound` |
| `StageC.cross_le`, `sq_add_le` | none | `propext, Classical.choice, Quot.sound` |
| `StageC.certified_clustering` (**Lemma 6.4**) | none | `propext, Classical.choice, Quot.sound` |
| `StageC.prop_6_9` (**Prop. 6.9**) | none | `propext, Classical.choice, Quot.sound` |
| `Assembly.seed_radius` | none | `propext, Classical.choice, Quot.sound` |
| `Assembly.prop_2_10` | none | `propext, Classical.choice, Quot.sound` |
| `Assembly.prop_3_11` | none | `propext, Classical.choice, Quot.sound` |
| `Assembly.prop_4_16` | none | `propext, Classical.choice, Quot.sound` |
| `Assembly.prop_5_7` | none | `propext, Classical.choice, Quot.sound` |
| `Assembly.cor_5_8` | none | `propext, Classical.choice, Quot.sound` |
| `Assembly.prop_6_9` | none | `propext, Classical.choice, Quot.sound` |
| `Assembly.theorem_7_1` | none | none |
| `Assembly.theorem_1_1` | none | none |

All footprints are the Mathlib-wide default (`propext`, `Quot.sound`, and `Classical.choice` where
a `Finset`/`Set`/classical case split is used).  No `sorryAx` anywhere above; no custom axioms;
no `native_decide`.

## Compiled: yes, with one explicit `sorry`

| declaration | paper claim | remaining goal | axiom footprint |
|---|---|---|---|
| `StageC.bin_displacement` | **Lemma 6.1** (bin displacement bounds) | the convexity/vertex maximisation: `sq x ≤ (29/6)a²`, `∑|x_j| ≤ 5a`, `|x_j| ≤ 3a/2` from `|d_j| ≤ a`, `d_0 = 0` | `propext, sorryAx, Classical.choice, Quot.sound` — **`sorryAx` is present, so this declaration is `stated`, not proved** |

This is the only unproved declaration in my three files, and it is marked `stated` here and in the
statement table (C4).  It is a lemma about five real variables and could be discharged by
interval/`nlinarith` case analysis on the signs of `d_j`; it was not attempted in a
files-and-statements window.

## Not attempted (out of this direction's scope)

* Lemma 5.1 (operator bounds for `A = I - TT*`), Lemma 5.2 (relation estimates), 5.3-5.6
  (iteration, threshold, box, radius growth), 6.2, 6.3, 6.6, 6.7, 6.8 — these need a real
  Hilbert-space norm on `ℝ^36` (`Matrix.l2_opNorm` / spectral bounds) and their own statement
  files.  I did **not** state them; m4 (`d2`) owns §3–4 and the §5 instances belong to a
  follow-up wave.  See `handoff-1.md` for the exact Mathlib situation (no polar decomposition,
  no matrix spectral-order API used here).
* Lemma 2.5 (circular-gap stability): m1 (`d4`) owns it.

## Honest summary

* Group (B)'s *assembly* is done: six propositions and the top-level chain are theorems with
  explicit **S**/**C** binders, and the two inductions they rest on are proved once, generically.
* §6's arithmetic core (Lemma 6.5) and its combinatorial consequence (Prop. 6.9's graph step,
  including "twelve distinct labels") are proved.
* Lemma 6.1, the §5 estimates, and the geometric instances of 2.10/3.11/4.16 (which live in
  `Seed.lean`, `Frames.lean`, `Hadamard.lean`) are **not** proved by me.

## Rename

The assembly module is `Mub6/AssemblyCover.lean` (the scaffold owner's `Mub6/Assembly.lean` stub
was written over it; the stub now carries a pointer).  Final build order, each with
`LEAN_PATH="$LEAN_PATH:."`: `lean -o Mub6/Interface.olean Mub6/Interface.lean`,
`lean -o Mub6/Exclude.olean Mub6/Exclude.lean`, `lean Mub6/AssemblyCover.lean`.  All exit 0;
only `StageC.bin_displacement` carries `sorryAx`.
