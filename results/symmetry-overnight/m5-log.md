# m5 running log — swarm `smwhnslql`, direction 4 (adversarial construction)

Working directory for code: `.ultramath/smwhnslql/m5/`. Person-facing files: this directory
(`results/symmetry-overnight/m5-*`). Registered direction (board id `d2`): construct exact
triples and weaker structures, test the source's intermediate lemmas in their general form,
hunt explicit violations; numerics only to locate candidates, never as proof.

## 1. Reading

* Read the primary source in full and the code fragment. The fragment is a *tail only*
  (`support_smith`, `validate_product_control`); the definitions of `E, F, G` are lost, so the
  source's exact `(3,3,2)` example cannot be re-run from the attachment. Reconstructed instead
  (section 4 below).
* Read `results/elegant-proof-routes.md` (route map; R7 dead), `results/order3-stratum.md`
  (frame parametrisation, `T = I (x) Z`, gap numerics), `results/symmetric-obstruction-audit.md`,
  and the project's reusable exact code (`examples/mubexact.py`, `.scratch/mub6/fouriercheck.py`
  for the JMSSW family `{I, F(0,b(t)), C(t)}`).

## 2. Rebuilt the detector from scratch and validated it

`.scratch/mub6sym.py`: for a triple `{A = I6, B, C}` compute
`(P_A)_{ij,kl} = sum_r B_ir conj(B_jr) conj(B_kr) B_lr + (same with C)` on off-diagonal matrix
units, take the exact/float support, form the relation rows `e_i-e_j-e_k+e_l` in `Lambda_0`
coordinates, and report both the Smith index `[Lambda_0 : L_A]` and — independently — the order
of the group obtained by *enumerating* the solutions of `R a = 0 (mod 1)` and testing ray
preservation of `B` and `C` explicitly. In every case the two agree (6, 3, 2, 1), so the
source's (5) is confirmed on all examples below (consistent with m1's no-swap lemma, board
`d1/f15`).

Results (all reproduce the source's table):

| triple | `(Delta_A,Delta_B,Delta_C)` | Smith at A |
|---|---|---|
| product triple `{I, F2(x)F3, (diag(1,i)F2)(x)(diag(1,w^2,w^2)F3)}` | (6,6,6) | (1,1,1,1,6) |
| JMSSW family, 240 sampled `t` in both allowed intervals | (3,1,1) throughout | (1,1,1,1,3) |
| uniform-case triple, section 4 | (2,3,3) | (1,1,1,1,2) |
| nonuniform involution triple, section 5 | (6,1,1) | (1,1,1,1,6) |

The `(2,3,3)` Smith forms are `(1,1,1,1,2),(1,1,1,1,3),(1,1,1,1,3)` — the source's exact example,
as a multiset.

## 3. Two traps found while reproducing (worth knowing before auditing further)

1. **The support is not invariant under rescaling one of the two bases.**
   `(P_A)_{ij,kl}` is homogeneous of degree `|c|^4` in each basis separately, so the *sum* over
   the two bases only sees them if the two scalars have equal modulus. Passing `B^*` (correctly
   normalised) together with `6*B^*C` silently changed the support from 246 to 276 nonzero
   entries while leaving the Smith index at 3. Any reimplementation must carry the scalars.
2. **Float thresholds are not an exact test.** With tolerance `1e-9` the float computation agreed
   with the exact one here (smallest nonzero about `1e-2`, largest "zero" about `4e-18`), but that
   is an empirical accident; `m5-exact-certificate.py` decides zeros in `Z[z]`, `z = zeta_24`,
   exactly.

## 4. Built the source's "uniform case" explicitly (new, and it exists)

Take `X = H0^* K0 = F`, `Y = H1^* K1 = iF`, `K0 = H0 F`, `K1 = i H1 F`, and
`B = 2^{-1/2}[[H0,H0],[H1,-H1]]`, `C` likewise from `(K0,K1)`. Then (7) holds iff `H0 F` and
`H1 F` are flat. Solving `|H F| = 1/sqrt3` over 3x3 Hadamards: exactly 108 solutions, all of the
form `H = F D Pi` with `D` a cube-root diagonal (no continuous family). Over all `108^2` ordered
pairs the exact `Delta`-tuple takes exactly two values: `(2,3,3)` (5832 cases) and `(6,6,6)`
(5832 cases). So genuine triples with `Delta_A = 2` exist, and the divisibility lemma holds on
this whole family; this independently confirms the source's `(3,3,2)` example, whose code was
lost.

`m5-exact-certificate.py` verifies one such triple exactly in `Z[z]`, `z = zeta_24`
(`Phi_24 = x^8-x^4+1`, entries `z^k/sqrt6`, `sqrt6 = z+z^23+z^5+z^19`), including a check that
the stored matrices equal `3 sqrt6` times the numerical ones, and reproduces the Smith forms.

## 5. The full involution stratum (all solutions of (7))

Parametrisation (complete up to the stated gauge): `H0 = F D2 P0`, `H1 = F D6 P2`, `K0 = D3 F`,
`K1 = D7 F D8 P3`; gauge `X -> Dmu^* X Dlam PiB`, `Y -> Dmu^* Y Dlam PiB`, fixed by `K0 = D3 F`;
15 free phases + 3 discrete permutations, 18 real equations (7). Exhaustive multistart search
over all `216` discrete classes (`m5-involution-stratum.py`):

| type | `Delta`-tuple | count | geometry |
|---|---|---|---|
| uniform | (2,3,3) | 2244 | isolated points |
| uniform | (6,6,6) | 1115 | isolated points |
| nonuniform | (6,1,1) | 3205 | one-parameter family |

The nonuniform solutions have exactly the structure the source's section 4 describes: `X` a
twisted circulant with three distinct magnitudes `(|x0|,|x1|,|x2|) = (1/sqrt3, 0.7486..., 0.3260...)`
with `|x1|^2+|x2|^2 = 2/3`, `Y` the reflected circulant, Bargmann invariants `+-i`. The source's
predicted clock at the anchor is present: `diag(Z, wZ) in G_A` (verified). At the `Delta_A = 2`
points the source's predicted clocks at B and C are present: `diag(Z,Z)` in B-coordinates
preserves all three bases (verified), and likewise in C-coordinates.

**No counterexample to `Delta_A = 2 => 3 | Delta_B, 3 | Delta_C` was found**, and `Delta_A = 2`
occurred only in the uniform case, where I can prove the conclusion (`m5-report.md`, Theorem U).

## 6. What I did not do

* Did not verify the source's normal-form step (8) as a *normalisation*: it requires the column
  permutation of `H0` to be trivial. My nonuniform examples realise it in the class
  `P0 = P2 = P3 = id`, but I have neither a proof that it is always attainable nor a
  counterexample. Its *conclusion* is confirmed on the whole nonuniform stratum.
* Did not implement the preprint's explicit two-parameter family (arXiv:2611.06917, Methods
  Eqs. (A.136)-(A.139)), so "all triples" is not covered — only the involution stratum and the
  JMSSW curve.
* Did not touch `Xi` or the product identity (other members' directions).

## 7. Proving the uniform case (added after §5 above)

Reproduced the source's §4 uniform-case argument and found it needs a *row* form of the
`3 x 3` Hadamard lemma (componentwise multiplication by `(1,w,w^2)` permutes the rows of `H^*`
by a cyclic shift) that the source only states in the column form; the row form follows because
every permutation of `Z/3` is affine. With it the uniform case is a complete proof
(`m5-report.md`, Theorem U). The conclusion was then checked directly on all 11664 uniform
triples: zero failures (`m5-involution-stratum.py --part 4`).

## 8. Nonuniform clock: labelling dependence

Tested the source's displayed `T = diag(Z, psi Z)` on the 108 discrete classes of the nonuniform
family: present in 54, absent in 54 (there `a_{3+j} = -a_j`, the mirror form). The criterion is
that the affine slopes `u` of the row permutations of `H_0` and `H_1` agree, because `Z` shifts
the column index by `-a/u` inside each block. `3 | Delta_A` holds in all 108 classes. Recorded in
`m5-report.md` §8; it does not affect the divisibility lemma.

## 9. Hand-off

Board posts: `f20` (Theorem U), `f21` (the `Delta_A = 2` stratum), `f22` (the rescaling trap),
`f24` (the labelling caution). Report: `results/symmetry-overnight/m5-report.md`. Scripts:
`m5-exact-certificate.py`, `m5-involution-stratum.py`.
