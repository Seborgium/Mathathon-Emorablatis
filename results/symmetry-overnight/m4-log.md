# m4 log — direction 3: the product identity Xi(P_A)Xi(P_B)Xi(P_C)=0

Member m4, swarm `smwhnslql`, direction d3. Code: `.ultramath/smwhnslql/m4/scratch/`, copied to
`results/symmetry-overnight/m4-code/`. Deliverables: `m4-report.md`, `m4-theorem.md`, `m4-tables.md`.

## 0. Reading done
Primary source (full) and `Pasted text 1.txt` (a fragment: its head is missing, so `E`, `F` and
`smith_normal_form` are cut off and only the tail of `G` survives). Project notes read:
`results/elegant-proof-routes.md` (R1–R7, R7 dead), `results/order3-stratum.md` (Lemma A, Theorem B;
"every known triple is order-3 symmetric" per the cited classification), `results/symmetric-obstruction-audit.md`
(head), `results/order3-check.py`. Board directions at the time: d1 (detector audit), d2/d5/d6/d4 taken by
m5/m2/m3/m6 — I stayed off all of them.

## 1. The source's projection formula (1) is correct
I suspected a normalisation error (the generators `b_r b_r^*` are not an orthonormal frame of `W_B`).
Numerically it is right: for a genuine MUB pair the 30x30 matrix of formula (1) is idempotent, Hermitian,
rank 10, and equals the true orthogonal projection onto the image of `W_B (+) W_C` (agreement 1e-16).
My suspicion came from feeding the routine a non-MUB triple. Recorded so nobody repeats it.

## 2. Independent exact machinery (Z[zeta_24])
`scratch/exact.py`: flat matrices as integer exponent matrices over Z[zeta_N]; exact support of P_X by
reducing sums of N-th roots mod Phi_N; relation rows r_ijkl; Smith normal form over Z; rank over F_3.
`scratch/flatops.py`: exact change of basis between flat matrices, conj-transpose, Kronecker product.
`scratch/symgroup.py`: direct enumeration of the diagonal clock group from the bases (no projection).
Validation: the tensor (product) triple over Z[zeta_24] gives Delta = (6,6,6), 150 nonzero P-entries of
900, 42 distinct relations, rank_F3 = 4, index = 6 at every anchor — matching the source's product
control and its Smith form diag(1,1,1,1,6).

## 3. Structural result (corrected — see §7)
`{3 does not divide Delta_A}` is open and `{3 | Delta_A}` is closed in the compact space of triples
(upper semicontinuity; limits of clocks are clocks, and Delta | 6). Correct conclusion: Z = {some anchor
has 3 | Delta} is closed, O = T \ Z is open, and
  (13) <=> O empty <=> Z is dense in T.
So a proof on a DENSE set of triples suffices, and a failure would be an open set of counterexamples.
Nothing more: Z is NOT clopen, Delta_X is NOT locally constant, and "one symmetric triple per connected
component" is NOT a valid criterion.

## 4. Corrections I had to make (recorded so the swarm does not repeat them)
1. My first numeric run of the JMSSW family reported all-zero supports: `mp.matrix(rows, cols, lambda i,j:
   ...)` in mpmath builds a ZERO matrix (the third argument is a value, not a filler), and my `conjT`/
   `mmul` helpers inherited the bug. Fixed with explicit loops.
2. I compared projective clock classes by their raw exponent vectors without normalising the global
   phase; that made a group of order 6 look like order 2. Fixed by fixing u_0 = 0.
3. I briefly believed the Fourier chart gives Delta = (1,1,2), i.e. a counterexample to the source's
   identity. That was a construction bug (I indexed the sorted ray list instead of the chosen sextuple,
   so the "basis" was six non-orthogonal rays that happened to be MUB to F_6). Corrected: (6,6,6) and
   (3,3,2). Lesson: check orthonormality of the basis itself, not only cross-unbiasedness.
4. My first submitted version claimed Z clopen and a component criterion. WRONG — see §7.

## 5. Results condensed
* Prop. 1: Delta_X in {1,2,3,6}, finite cyclic (proved, with the finiteness step the source omits).
* Prop. 2: {3 | Delta_X} is closed (proved, via the 243 cube-root clocks).
* Theorem A (corrected): Z closed, O open; (13) <=> O empty <=> Z dense; a dense-set proof suffices;
  failure is an open condition; no component criterion.
* Computations: tensor (6,6,6); Fourier chart (6,6,6) twice and (3,3,2) twice (the source's example
  reproduced exactly); JMSSW family (3,1,1) at 7 values of t, 60 digits, gap 1e27.
* Verified m5's 3x3 rigidity claim (108 matrices; no continuous solutions in 2.4e6 random tries).
* The Fourier chart contains at least two INEQUIVALENT triples (the Delta-multiset is an equivalence
  invariant and takes two values there), so "the single isolated Fourier triple" in the project notes
  should be read as a statement about the pair moduli.

## 6. Correction after the first submission (the judge's critique, accepted in full)
The first submission claimed that Prop. 2 (S_X closed) makes Z clopen, hence (13) <=> "no connected
component is 3-free", one symmetric triple per component suffices, and a "touching" statement weaker than
the classification would do. That is an error: closedness is upper semicontinuity, not local constancy;
Z may be a proper closed subset of T, and a component can contain both symmetric and asymmetric triples.
Withdrawn. Also withdrawn: "the identity is not an algebraic identity / no local algebraic proof exists"
— equivalence to a geometric (density) condition is not an impossibility proof for a global algebraic
derivation. The sampling discussion is now qualified: a curve inside a 2-dimensional moduli space cannot
test an open failure locus; only a distribution on the full triple space can.
Witness that local constancy fails (so the correction is not mere caution): at the centre of the
two-parameter family Delta = (3,3,2) and perturbations give (3,1,1) (m2's census, 9,320 points; my exact
Fourier chart shows the same two patterns).

## 7. Final state
Report: `m4-report.md` (verdicts, corrected theorem, edits for the proof revision). Proofs:
`m4-theorem.md` (Prop. 1, Prop. 2, Theorem A). Computations: `m4-tables.md` and `m4-code/`.
Board: f5 (main partial result — superseded by the corrected Theorem A), f12 (verification of m5's
108-matrix rigidity); a correction note is posted for f5. Cross-checked with m2's census and m6's (T3).
Nothing here proves N(6)=3, and nothing here proves (13) either: Theorem A says (13) is equivalent to
density of the closed symmetric locus, which is the honest residue.
