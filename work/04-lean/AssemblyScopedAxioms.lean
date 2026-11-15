/-
  AxiomReport.lean -- machine-checked axiom footprints for the scoped assembly.

  Run:  LEAN_PATH=$PWD:$LEAN_PATH lean AxiomReport.lean

  Every declaration of `Mub6AssemblyScoped.lean` is quoted with `#print axioms`.  A complete proof
  reports only Lean's three standard axioms (`propext`, `Classical.choice`, `Quot.sound`); any
  `sorryAx` or project-introduced axiom would appear here.
-/
import Mub6AssemblyScoped

#print axioms Mub6.AssemblyScoped.Box.mem_split_of
#print axioms Mub6.AssemblyScoped.Box.mem_split
#print axioms Mub6.AssemblyScoped.seed_bin_dist_le
#print axioms Mub6.AssemblyScoped.seed_bin_lt_radius
#print axioms Mub6.AssemblyScoped.CellTree.covers
#print axioms Mub6.AssemblyScoped.chain_excluded
#print axioms Mub6.AssemblyScoped.chain_excluded_emb
#print axioms Mub6.AssemblyScoped.Chain.no_extendible
#print axioms Mub6.AssemblyScoped.Chain.false_of_four
#print axioms Mub6.AssemblyScoped.live_defeats_covers
#print axioms Mub6.AssemblyScoped.split_boundary_check
#print axioms Mub6.AssemblyScoped.hseed_needed
#print axioms Mub6.AssemblyScoped.hstep_needed
#print axioms Mub6.AssemblyScoped.hfinal_needed
#print axioms Mub6.AssemblyScoped.consistentChain_no_extendible

-- the names and statements the report quotes
#check @Mub6.AssemblyScoped.Chain.no_extendible
#check @Mub6.AssemblyScoped.CellTree.covers
