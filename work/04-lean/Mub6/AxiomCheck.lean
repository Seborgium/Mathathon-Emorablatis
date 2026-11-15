/-
Mub6/AxiomCheck.lean — reporting artifact, not part of the library DAG.

Every declaration of `Mub6/*.lean` that this window leaves unproved is printed with its axiom
footprint, so that reports/status.md can quote machine output instead of a claim.  Run:

    LEAN_PATH=$PWD:$LEAN_PATH lean Mub6/AxiomCheck.lean

Expected: the proved declarations do not appear here at all; each listed declaration reports
`[sorryAx]`; nothing reports a user-introduced axiom (there are none in this project).
-/
import Mub6.Basic
import Mub6.Hadamard
import Mub6.Seed
import Mub6.ThreeMUB

-- Lemma 2.2, five clauses and their packaged form
#print axioms Mub6.extendible_permRows
#print axioms Mub6.extendible_permCols
#print axioms Mub6.extendible_rephaseRows
#print axioms Mub6.extendible_rephaseCols
#print axioms Mub6.extendible_conjMat
#print axioms Mub6.extendible_transposed
#print axioms Mub6.extendible_iff_all
-- Lemma 2.5, paper form
#print axioms Mub6.gap_stability
-- Lemma 1.2
#print axioms Mub6.FDF_entry
#print axioms Mub6.three_mub_exists

-- Proved declarations spot-checked: must report only the three standard axioms
#print axioms Mub6.Pi_frobSqR_le
#print axioms Mub6.seedGap_lipschitz
#print axioms Mub6.gauss_one
#print axioms Mub6.normSq_two_add_omega_sq
#print axioms Mub6.e_add_int
#print axioms Mub6.expMat_int_shift
#print axioms Mub6.horizontal_iff_Pi_eq_self
#print axioms Mub6.expMat_Pi_rephasing
