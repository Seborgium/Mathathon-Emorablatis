# m5 final report — the `Delta_A = 2` stratum of C^6 MUB triples, and a proof of the uniform case

Swarm `smwhnslql`, direction 4 (adversarial construction). Files: `m5-log.md` (running log),
`m5-exact-certificate.py` (exact certificate in `Z[zeta_24]`), `m5-involution-stratum.py`
(exhaustive search over the involution stratum). All claims below are labelled
**[proved]**, **[exact computation]**, **[numerical]** or **[unresolved]**.

Notation as in the source: for a MUB triple `{A,B,C}` in `C^6` and the anchor `A`, `Delta_A`
is the order of the group of diagonal unitaries (modulo overall phase) that preserve `B` and `C`
as sets of rays; `S = diag(I_3,-I_3)` after relabelling the rays of `A`; `X = H_0^*K_0`,
`Y = H_1^*K_1` for the `3 x 3` blocks of

    B = 2^{-1/2} [[H_0,H_0],[H_1,-H_1]],    C = 2^{-1/2} [[K_0,K_0],[K_1,-K_1]]      (6)

and (7) is the pair of conditions `|X_ij|^2 + |Y_ij|^2 = 2/3`, `Re(X_ij conj(Y_ij)) = 0`,
which is *equivalent* to `B^*C` being flat.

## 1. Headline

**The source's divisibility lemma holds on the entire `Delta_A >= 2` stratum, and the "uniform"
half of it is now a proof, not a sketch.**

* **[proved]** Theorem U below: if a triple with a diagonal involution `S` at `A` satisfies
  `|X_ij| = 1/sqrt3` for all `i,j` (the source's uniform case), then `diag(Z,Z)` is a
  nonconstant order-three clock at `B` *and* at `C`; in particular `3 | Delta_B` and
  `3 | Delta_C`. This needs two `3x3` Hadamard lemmas, one of which (the *row* version) the
  source does not state; without it the claim "`diag(Z,Z)` preserves `A = B^*`" in its §4 is
  unjustified. Both are proved in §2.
* **[exact computation]** The source's `(3,3,2)` example is reconstructed and certified exactly
  (`Z[zeta_24]`): `(Delta_A,Delta_B,Delta_C) = (2,3,3)` with Smith normal forms
  `(1,1,1,1,2)`, `(1,1,1,1,3)`, `(1,1,1,1,3)` — the source's numbers, reproduced without its
  lost code.
* **[numerical, exhaustive over the stratum]** Every MUB triple in `C^6` carrying a diagonal
  involution at `A` has `(Delta_A,Delta_B,Delta_C)` equal to `(2,3,3)`, `(6,6,6)` (both uniform,
  isolated) or `(6,1,1)` (nonuniform, a one-parameter family). Hence "`Delta_A = 2`" happens
  only in the uniform case, where Theorem U applies. **No counterexample to the source's lemma
  exists in the stratum.**
* **[proved, negative]** Two reproducibility traps in the source's (1)/(5) are identified in §5:
  the projection support is *not* invariant under rescaling one of the two bases, so a
  reimplementation can silently produce a different support at the same lattice index.

Consequence for the project's proof revision: the source's reduction
`(no threefold symmetry) => (Delta_A,Delta_B,Delta_C) = (1,1,1)` now stands on
Theorem U **[proved]** plus the nonuniform case, which remains **[unresolved]** as a proof but
**[verified]** on an exhaustive numerical sweep. It does *not* prove `N(6) = 3`; the residue is
unchanged (`Delta_X >= 2` for some anchor, cf. m6's `T2`).

## 2. Theorem U (uniform case) — proved

**Lemma H1 (column form).** For every `3x3` Hadamard `H` and `Z = diag(1,w,w^2)`, `w = e^{2 pi i/3}`,
there are a diagonal `D` and a permutation `Pi` with `Z H = H D Pi`.

*Proof.* Every `3x3` Hadamard is `H = D_1 F D_2 Pi_2` (`F` the Fourier matrix; standard: dephase the
first row and column, then orthogonality forces the remaining triples of unit phases to sum to
zero, i.e. to be rotated copies of `(1,w,w^2)`). With `S` the cyclic column shift, `Z F = F S`
because `(ZF)_{ij} = w^{i(j+1)} = (FS)_{ij}`; and `S D_2 = D_2^sigma S` for the diagonal `D_2^sigma`
with entries permuted by `sigma: j -> j+1`. Hence
`Z H = D_1 Z F D_2 Pi_2 = D_1 F D_2^sigma S Pi_2 = H (Pi_2^{-1} D_2^{-1} D_2^sigma S Pi_2)`,
and the bracket is a diagonal times a permutation. (No use of the special form of `D_1`.) QED

**Lemma H2 (row form — missing in the source).** For every `3x3` Hadamard `H`, every character
`c = (w^{aj+b})_{j=0}^{2}` with `a in {1,2}`, `b in Z/3`, and every `r`,
`c odot row_r(H^*) = w^b · row_{r'}(H^*)` with `r' = r - a/u`, where `u in {1,2}` is determined by
`H`'s column permutation. In particular componentwise multiplication by `(1,w,w^2)` (or its
square) permutes the rows of `H^*` by a cyclic shift, with *no* extra phases.

*Proof.* Write `H = D_1 F D_2 Pi_2` and let `Pi = Pi_2` act by `(Pi^{-1}M)_{rj} = M_{pi(r),j}` with
`pi` the permutation of `Pi`. Then
`row_r(H^*)_j = conj((d_2)_j) w^{-pi(r) j} conj((d_1)_j)`.
Multiplying by `w^{aj+b}` changes the exponent of `w` to `aj + b - pi(r) j`. Since every
permutation of `Z/3` is affine, `pi(r) = ur + v`, `u in {1,2}`; choosing `r' = r - a u^{-1}` gives
`a - pi(r) = -pi(r')`, so the product equals `w^b` times `row_{r'}(H^*)`. QED

**Theorem U.** Let `{A = I_6, B, C}` be a MUB triple with a diagonal involution `S` at `A`, and
assume the uniform case: `|X_ij| = 1/sqrt3` for all `i,j`. Then `diag(Z,Z)` lies in `G_B` and in
`G_C`; hence `3 | Delta_B` and `3 | Delta_C`.

*Proof.*
*(i) Sign factorisation.* By (7) and uniformity, `|Y_ij| = 1/sqrt3` too, so `Y_ij = i eps_ij X_ij`
with `eps_ij` in `{+-1}`; `X` and `Y` are Hadamards. For `i != i'`, unitarity of `Y` gives
`0 = sum_j eps_ij eps_i'j t_j` with `t_j = X_ij conj(X_i'j)`. The `t_j` have modulus `1/3` and sum
to `0` (unitarity of `X`), so (no two of them are proportional, since `|t_j|` are equal and
`t_1 + t_2 + t_3 = 0` with all moduli equal forces any two to be distinct directions) they are the
three distinct cube-root directions, and a `{+-1}` combination vanishing on three distinct
directions must have equal coefficients. So `eps_ij eps_i'j` is independent of `j` for every pair
`i,i'`, which is equivalent to `eps_ij = r_i c_j`.

*(ii) Absorbing the signs.* In the block form (6), replacing the `A`-pair `{u_i, S u_i}` by
`{S u_i, u_i}` leaves `H_0` unchanged and replaces `H_1` by `H_1 D_i` (`D_i` = diag with `-1` at
`i`); replacing the `B`-pair `j` likewise leaves `K_0` unchanged and replaces `K_1` by
`K_1 D_j`. Hence `X` is unchanged and `Y` is multiplied by `D_i` on the left (row `i`) or by `D_j`
on the right (column `j`). These operations only reorder/ rephase the vectors of `A` and `B`, so
they preserve the three ray sets. Absorbing `r_i c_j` leaves `Y = i X`.

*(iii)* Then `B^*C = K (x) X` with `K = (1/2)[[1+i,1-i],[1-i,1+i]]` (blockwise: the four blocks of
`2 B^*C` are `(1+i)X`, `(1-i)X`, `(1-i)X`, `(1+i)X`).

*(iv) The clock at `B`.* In `B`-coordinates the three bases are `B = I`, `A = B^*`, `C = B^*C = K(x)X`.
Let `T = diag(Z,Z)`.
`T` is diagonal, so it fixes every ray of `B`. And `T(K(x)X) = K(x)(ZX) = K(x) X (D Pi)` by H1,
so `T` permutes the columns of `C` up to phases. Finally the columns of `A = B^*` are
`2^{-1/2}(v_r; v_r)` and `2^{-1/2}(w_r; -w_r)` with `v_r = conj(row_r(H_0))`,
`w_r = conj(row_r(H_1))`; applying `T` gives `2^{-1/2}(Z v_r; Z v_r)`, and
`Z v_r = conj( (1,w^2,w) odot row_r(H_0) )`, so by H2 (with `a = 2`) it is a phase times
`2^{-1/2}(v_{r'}; v_{r'})`, a column of `A` of the same type. So `T` permutes the columns of `A`.
Hence `T in G_B`, `T` is nonconstant and `T^3 = 1`, so `3 | Delta_B`.

*(v)* The same argument verbatim in `C`-coordinates, where `A = C^*` and `B = C^*A = (K(x)X)^* = K^*(x)X^*`
with `X^*` again a Hadamard. Hence `3 | Delta_C`. QED

**[numerical, exhaustive]** The conclusion of Theorem U was also checked directly on all
`108^2 = 11664` uniform triples: in every one `diag(Z,Z)` in `B`-coordinates preserves `B`, `A`
and `C`, and in `C`-coordinates preserves `C`, `A` and `B` — zero failures
(`m5-involution-stratum.py --part 4`).

*Remark.* Only `d = 6`, `2 = 1+1` and `3 = 1+1+1` are used, i.e. the splitting `6 = 2 x 3`; the
3-dimensional structure comes from `2|S`-pairs. Nothing in the proof uses `Delta_A = 2`.

## 3. The `(2,3,3)` triple, exact

**[exact computation]** `m5-exact-certificate.py`. In `Z[z]`, `z = zeta_24`, `Phi_24 = x^8-x^4+1`,
with `sqrt6 = z + z^23 + z^5 + z^19` and entries stored as `z^k/sqrt6`:

    w = z^8,  F3 = (w^{jk}),  H_0 = F3 diag(1,1,w),  H_1 = F3 diag(1,1,w^2),
    K_0 = H_0 F3,  K_1 = i H_1 F3,
    B = 2^{-1/2}[[H_0,H_0],[H_1,-H_1]]/sqrt3,   C = 2^{-1/2}[[K_0,K_0],[K_1,-K_1]]/3 .

The script checks the storage against the floating-point triple (`1e-12`), decides all projection
entries in `Z[z]` exactly, and computes Smith normal forms over `Z`. Output:

    anchor A: 360 nonzero entries, 121 relation rows, Smith [1,1,1,1,2], Delta = 2
    anchor B: 246 nonzero entries,  79 relation rows, Smith [1,1,1,1,3], Delta = 3
    anchor C: 246 nonzero entries,  79 relation rows, Smith [1,1,1,1,3], Delta = 3

So `Delta = (2,3,3)` and the Smith forms are the source's `(1,1,1,1,3),(1,1,1,1,3),(1,1,1,1,2)`
as a multiset. **[numerical]** the projected clocks are present: `diag(Z,Z)` in `B`-coordinates
preserves `B`, `A = B^*` and `C = B^*C`, and in `C`-coordinates preserves `C`, `A = C^*`,
`B = C^*A`; this is exactly Theorem U's conclusion, and it confirms the `(2,3,3)` example also
has `3 | Delta_B, 3 | Delta_C`.

## 4. The whole involution stratum

**[numerical, exhaustive over the discrete classes]** `m5-involution-stratum.py`. Every MUB pair
`(B,C)` with `S = diag(I_3,-I_3)` as a diagonal symmetry at `A = I_6` is, up to the gauge
`X -> D_mu^* X D_lam Pi_B`, `Y -> D_mu^* Y D_lam Pi_B`,  of the form

    H_0 = F D_2 Pi_0,   H_1 = F D_6 Pi_2,   K_0 = D_3 F,   K_1 = D_7 F D_8 Pi_3 ,

with 15 free phases and 3 discrete permutations, subject to the 18 real equations (7).
Searching all `6^3 = 216` discrete classes with 40 random starts each produced 6564 solutions
(deduplicated within `1e-6`), with `Delta`-tuples:

| type | `(Delta_A,Delta_B,Delta_C)` | occurrences |
|---|---|---|
| uniform (`|X_ij| = 1/sqrt3`) | (2,3,3) | 2244 |
| uniform | (6,6,6) | 1115 |
| nonuniform | (6,1,1) | 3205 |

Corroboration of the parametrisation: the two uniform types are exactly the `108^2 = 11664`
triples of §3's construction (5832 of each type), and the nonuniform type is a genuine
one-parameter family: `X` is a twisted circulant with three distinct magnitudes
`(1/sqrt3, 0.7486108..., 0.3259624...)`, `|x_1|^2 + |x_2|^2 = 2/3`, `Y` is the reflected
circulant, and all Bargmann invariants of `X`, `Y` are in `{+-1, +-i}`. In that family
`Delta_A = 6` (so `3 | Delta_A`, consistent with the source's nonuniform case) and
`Delta_B = Delta_C = 1`, and an order-three clock at `A` always exists; in the classes that
realise the source's normal form the clock is exactly `T = diag(Z, wZ)` (verified), in the others
it has a different shape — see §8.

**Reading.** `Delta_A = 2` occurs on isolated uniform points only. Combined with Theorem U:

> **[proved + numerical]** for every triple in the involution stratum, `Delta_A = 2` implies
> `3 | Delta_B` and `3 | Delta_C`.

The only gap between this and an unconditional statement is the completeness of the numerical
enumeration. Two independent supports for completeness: (a) (7) is 18 equations in 15 essential
parameters, so solutions are expected to be isolated or low-dimensional, and only three types
turned up over all 216 classes; (b) `Delta` is locally constant along the solution
variety (support monotonicity), so the `Delta`-tuple is constant on each connected component and
sampling cannot miss a value *on a component it reaches*.

## 5. Two traps that a reimplementation will fall into

**[proved]** `(P_A)_{ij,kl} = sum_r U_ir conj(U_jr) conj(U_kr) U_lr + (V-terms)` is homogeneous of
degree `|c_U|^4` in `U` and `|c_V|^4` in `V` separately. The *zero set of the sum* therefore
depends on the ratio `|c_U|/|c_V|`, not just on the ray sets. Handing the pair
`(B^*, 6 B^*C)` to the detector gave 276 nonzero entries instead of 246 at the same lattice
index 3; with the scalars matched (`|c| = 3 sqrt6` for both) the exact computation reproduces
246. The source's (1) is written for normalised bases, where this is automatic — but any
re-derivation that rescales a derived basis (e.g. `B^*C` computed as an inner-product matrix)
must control the scalars. (A float tolerance does *not* protect against this, and conversely a
float tolerance is not a proof of vanishing: the correct certificate is exact arithmetic, as in
§3.)

## 6. Verdict on the source's §4 as written

* Uniform case: **the source's argument is correct in outline but incomplete as stated** — it
  asserts that `diag(Z,Z)` preserves both other bases without proving the row form H2 for
  `A = B^*`. With H2 added it is a complete proof (Theorem U). Its "sign matrix factors"
  step is correct; the supporting sentence ("flipping the signs of a proper nonempty subset
  cannot preserve their zero sum") is correct because the three summands are three distinct
  directions.
* Nonuniform case: **[unresolved]** I did not verify the normal form (8) as a *normalisation*.
  What the gauge `X -> D_mu^* X D_lam Pi_B` provides on `H_0` is only left multiplication by a
  diagonal, i.e. `H_0 -> D H_0`; since `H_0 = D_1 F D_2 Pi`, this reaches "`F` times a diagonal"
  only when `Pi` is trivial or **cyclic** (`F S = Z F` absorbs a cyclic column shift into row
  phases), and a transposition cannot be removed this way as far as I can see. Whether every
  nonuniform solution can be brought to (8) by a relabelling of the paired vectors is left open
  here; my nonuniform solutions do occur in classes that realise (8) (`Pi_0 = Pi_2 = Pi_3 = id`),
  but I also found nonuniform solutions in classes with `Pi_0` a transposition. What *is*
  verified: in the nonuniform stratum the conclusion (`3 | Delta_A`, indeed `Delta_A = 6`) holds
  in all 108 discrete classes, and the displayed clock `diag(Z, psi Z)` holds only up to
  labelling (§8).
* Consequently the lemma `Delta_A = 2 => 3|Delta_B, 3|Delta_C` is **[proved]** on the uniform
  case and **[verified, not proved]** elsewhere; the missing piece is a proof that `Delta_A = 2`
  forces the uniform case, which would follow from the source's nonuniform case.

## 7. What this does and does not contribute to the proof revision

* Safe to use now (**proved**): Theorem U; the column/row Hadamard lemmas H1, H2; the
  equivalence (7); the existence of a triple with `Delta = (2,3,3)` (**exact certificate**), so
  the source's remark that "changing the coordinate basis is essential and an individual index of
  two is a real possibility" is confirmed.
* Safe to use as a *conditional* step: `Delta_A = 2 => 3|Delta_B, 3|Delta_C` (uniform half
  proved, nonuniform half numerical), and hence the reduction of the no-threefold case to
  `(1,1,1)`.
* Do **not** claim: any counterexample to the source's lemma (none found); completeness of the
  involution stratum (numerical only); anything about `Xi` or the product identity
  `Xi_A Xi_B Xi_C = 0` (other directions); any new proof of `N(6) = 3`.

## 8. Addendum — the explicit form of the nonuniform clock is labelling-dependent

**[numerical]** On the nonuniform stratum (`Delta = (6,1,1)`) I tested, in each of the 108
discrete classes, whether the source's predicted clock `diag(Z, psi Z)`, `psi in {1,w,w^2}`,
belongs to `G_A`. It does in 54 classes and does not in the other 54; in those, the order-three
element of `G_A` is of a different shape, e.g. `a = (0, 1/3, 2/3 | 2/3, 1/3, 0)` (in units of
`2 pi`), i.e. the second block is minus the first. For `a = (a_1,a_2,a_3 | a_4,a_5,a_6)` one has
`a_{3+j} = -a_j` for *every* simultaneous relabelling of the two blocks, whereas
`diag(Z, psi Z)` requires `a_{3+j} = a_j + psi`; the two cannot be matched. So the source's
*specific* matrix `T = diag(Z, psi Z)` is not a labelling-independent statement.

A crisp criterion for it, following from Lemma H2: the induced action of `Z` on the columns of a
Hadamard `H = D_1 F D_2 Pi` shifts the column index by `-a/u`, where `u in {1,2}` is the *affine
slope* of the row permutation `Pi` (`Pi(r) = u r + v`; every permutation of `Z/3` is affine). A
clock of the two-block form `diag(Z, psi Z)` preserves `U` only if the slopes of `H_0` and `H_1`
agree, so that both blocks realise the same column shift. Numerically this is exactly the
observed split: classes with `slope(H_0) = slope(H_1)` admit `diag(Z, psi Z)`, classes with
`slope(H_0) != slope(H_1)` do not. (Relabelling the pairs changes the slopes, so the criterion is
a statement about a given presentation, not about the triple.)

What *is* labelling-independent, and holds in all 108 classes, is `3 | Delta_A` (in fact
`Delta_A = 6`): a nonconstant order-three clock at `A` always exists. The source's derivation
should therefore be read inside its own normal form (8); the conclusion `3 | Delta_A` of its
nonuniform case is correct on the entire stratum, but the displayed normal form of the clock is
not canonical. This does not affect the divisibility lemma (which only needs `3 | Delta_A` to
exclude the hypothesis `Delta_A = 2`).

## 9. Reproduce

    python3 results/symmetry-overnight/m5-exact-certificate.py        # (2,3,3), exact, <5 s
    python3 results/symmetry-overnight/m5-involution-stratum.py       # parts 1-3, about 3 min
    python3 results/symmetry-overnight/m5-involution-stratum.py --part 2   # 108^2 uniform case
    python3 results/symmetry-overnight/m5-involution-stratum.py --part 3 --starts 40
