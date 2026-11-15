# m1 — running log (direction 1: detector / lattice / recovery-lemma audit)

Board direction `d1`. Deliverable: `m1-audit.md`; scripts `m1-scripts/`.

## Session 1 — read the sources

* Read in full: `attachments/how-do-i-make-ofyz/A promising idea force any diagonal symmetry,
  then recover the threefold symmetry.txt` (22 kB, sections 1–7).
* Read `attachments/.../Pasted text 1.txt`: a *truncated* fragment of
  `mub_symmetry_exact_checks.py`. What survives: `cyclotomic_powers()` (`Z[z]/Phi_24`), `validate_triple`,
  `support_smith`, `validate_product_control`, and the last six rows of one 6x6 exponent array.
  The arrays `E` and the definition of `G` are cut off, so the source's exact `(3,3,2)` triple
  cannot be reconstructed from the fragment. `validate_product_control` asserts Smith
  `(1,1,1,1,6)` for the product triple — verified independently here (log 8.1 of the report).
* Read `results/elegant-proof-routes.md`, `results/order3-stratum.md`,
  `results/symmetric-obstruction-audit.md` (and `results/symmetry-overnight/README.md`,
  `m2-log.md`): the project has no prior analysis of the projection/support-lattice detector, so
  the audit is new work in the project. m2 is on literature, m3 on the group-covariant slice,
  m4 on the Xi identity, m5 on counterexample search, m6 on the nonextension bridge.

## Session 2 — exact arithmetic and the projection formula

* Built `cyc.py`: elements of `Z[zeta_24]` as dicts `{k: coeff}`, canonical form mod
  `Phi_24 = x^8 - x^4 + 1`. Two bugs found and fixed in my own code (a `_reduce` pad that failed
  for k > 15, and `neg` accidentally aliased to conjugation). Sanity: `sqrt6^2 = 6`,
  `1+w+w^2 = 0`, `i^2+1 = 0`.
* Derived formula (1) from the frame operator: the Gram matrix of `{b_r b_r^* - I/6}` is `I - J/6`,
  which is self-inverse on its range, so `P_B = sum_r w_r w_r^*`; the cross term cancels on
  off-diagonal indices. This is the proof in Theorem A of the report; no hand-waving needed about
  pseudo-inverses.
* Built the standard product triple `A = I`, `B = F_2 (x) F_3`, `C = diag(1,i)F_2 (x) chirp F_3`.
  First attempt used `C_3 = diag(1,w,w^2)F_3`, which is **not** unbiased to `F_3`
  (`F_3^* D F_3` is `3 delta` for a linear chirp); the correct chirp is `d_r = w^{r^2}`, i.e.
  `diag(1,w,w)`, or the source's `diag(1,w^2,w^2)`. Fixed and verified exactly.
* Verified exactly at all three anchors: `36P` Hermitian, `(36P)^2 = 36·36P`, `tr = 360`,
  diagonal 12, support 150, and `P w = w` for the twelve flat traceless matrices (the check that
  (1) is the projection, not just an idempotent). Smith `(1,1,1,1,6)`, index 6, `rank_{F_3} = 4`,
  `|Ann| = 6`, no swap, 3-torsion 3.

## Session 3 — the two gaps in the source, and their repairs

* Recovery lemma: the source's uniform case ("these give a projector from C") is a gap. Repair:
  if all `B`-diagonals are `1/d` then `w_B = 0`, so `rho = (1/d)I + w_C` is *diagonal in the C
  basis*; being a projection its entries are 0 or 1, and the trace forces exactly one 1. Written up
  as Theorem B.
* No-exchange claim. First attempted proof via "`T` diagonal and `T(B)=C` implies `|tr T|^2 = 6`"
  — this part is right and clean (sum `lambda_i = 6 mu_r c_{pi(r),i} conj(b_{r,i})` over `i`).
  Then the multiplicity check: order 2, 3, 4 are excluded by hand; my `noswap.py` showed that
  order 12 *does* allow `|tr|^2 = 6` (exactly 120 multiplicity vectors), so the source's
  "reduce to order 2 or 4" step is not automatic. Repair: take an odd power (`T^3` for orders 6
  and 12), which is again a swap and has order 2 or 4. Written up as Theorem D.
  Note `d = 2` is a genuine exception (`diag(1,i)` swaps the two `C^2` bases), and in `d = 3`
  the order-3 count does have a solution; the lemma is a `d = 6` statement.
* Lattice theorem: `D_A ≅ Hom(Lambda_0/L_A, T)`; finite by Theorem B; `rank L_A = 5`;
  `|D_A| = [Lambda_0:L_A]`; `3 | index ⟺ rank_{F_3} R_A < 5` by the snake lemma; `D_A = G_A` by
  Theorem D. Written up as Theorem C.

## Session 4 — computations, cross-checks, other members

* 24 product triples x 3 anchors: all `(6,6,6)`, support 150, Smith `(1,1,1,1,6)`, no swaps
  (`product_family.py`). Product triples cannot test the detector's `Delta != 6` branch.
* Rebuilt m5's certificate triple from the board (his direction d2 family) in my own framework
  and ran my machinery: `Delta = (2,3,3)` — index and `|Ann|` equal 2 at the standard anchor and
  3 at the other two; Smith `(1,1,1,1,2),(1,1,1,1,3),(1,1,1,1,3)`; `rank_{F_3} = 5,4,4`; no swaps
  at any anchor. This (i) is the discriminating test for formula (5) at `Delta = 2`, (ii)
  confirms Theorem D where it matters, (iii) reproduces the source's claimed Smith forms.
  Discrepancy noted, harmless: m3 reports 276 nonzero entries at the `Delta = 3` anchors of their
  instance; my reconstruction gives 246 (and 360 at the `Delta = 2` anchor, matching m3). Most
  likely a different instance of the same family.
* Confirmed the 80 projective relation types `15+20+45` by enumeration.
* Board: posted the no-exchange lemma (f15) and the recovery-lemma repair + lattice theorem (f16).

## Session 5 — write-up

* `m1-audit.md`: verdict table, Theorems A–E with complete proofs, exact computations, and an
  explicit list of what is *not* proved here (identity (13) above all).
* No claim about `N(6)=3`; §4 of the source was left to direction 2.

## Session 6 — cross-checks against other members, and the Delta = 2 anchor

* Read m3's `d6` findings, m4's `m4-theorem.md`, m5's `m5-report.md`, m6's `m6-proof-revision.md`
  (all in this directory). Three items in my scope:
  1. m5 reports 276 nonzero `P`-entries at the `Delta = 3` anchors and a "normalisation" caveat.
     I reproduced both numbers: with both coefficient matrices at modulus `1/sqrt6` I get 246; with
     the second basis scaled by 6 I get exactly 276 at the same lattice. So the discrepancy is a
     normalisation artefact, not a lattice disagreement (report §8.4).
  2. m5's relation-row counts 121/79 are my 120/78: the difference is the always-nonzero position
     `(i,j) = (k,l)`, whose relation vector is `0` and which imposes nothing. Report §8.4.
  3. m6's status table §10 lists "§3 (5) `Delta_X = [Lambda_0:L_X]` — general proof = Recovery
     Lemma" and the `(3,3,2)` example as not reproduced. Both move to proved/reproduced here
     (Theorems B, C, D and report §8.2, Appendix A.2). I also record that the chain
     `Xi(P_X) = 0 <=> 3 | Delta_X` does **not** need the no-exchange lemma (Appendix A.1).
* `involution.py`: identified the `Delta = 2` symmetry of the `(2,3,3)` triple exactly
  (`diag(-1,-1,-1,+1,+1,+1)`, three transpositions on each other basis), verified the source's
  §4 block normal form (6) and condition (7) entry by entry, and found the instance to be in the
  **uniform** branch `|X_{ij}|^2 = 1/3` — the branch whose §4 conclusion is "clocks at both other
  anchors", consistent with the independently computed `(2,3,3)`. This is a consistency check of
  §4, not a proof of it; §4 remains direction 2's (unregistered) job.
* Posted: f15 (no-exchange lemma), f16 (recovery lemma + lattice theorem), f19 (normalisation /
  zero-relation traps + the reproduced Smith forms), f23 (status upgrades and the
  `Xi = 0 <=> 3 | Delta` separation).
* Report `m1-audit.md` final: verdict table, Theorems A–E, §7 closure, §8 exact computations
  (24 product triples, the `(2,3,3)` triple, traps, §4 normal form), §9 non-claims, Appendix A.
