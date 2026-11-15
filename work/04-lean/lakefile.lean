/-
lakefile.lean — documentation artifact only.

The project keeps its own `lean-toolchain` (Lean 4.33.1) and DOES NOT build here:
`/opt/mathlib` is root-owned and shared with the other teams, so `lake build` against it fails
and must not be attempted. Every module in `Mub6/` is validated with

    lean Mub6/<Module>.lean

against the pre-built Mathlib on `LEAN_PATH`. The lakefile records how the package would be
assembled once a writable Mathlib copy exists; it is not used by any check in this window.
-/
import Lake
open Lake DSL

package «mub6» where
  -- The mathematical content is Mathlib-only; Mub6/*.lean add carriers, statements and proofs.
  leanOptions := #[
    ⟨`autoImplicit, false⟩,          -- every variable must be declared in each declaration
    ⟨`relaxedAutoImplicit, false⟩
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.33.1"

@[default_target]
lean_lib Mub6 where
  -- Deliberate import DAG (see reports/DEPGRAPH.md):
  --   Basic  <-  Hadamard  <-  Seed  <-  Completion  <-  Refine  <-  Exclude  <-  Assembly
  -- No module may import a later one on that spine.
  roots := #[`Mub6.Basic, `Mub6.Hadamard, `Mub6.Seed, `Mub6.Completion, `Mub6.Refine,
             `Mub6.Exclude, `Mub6.Assembly]
