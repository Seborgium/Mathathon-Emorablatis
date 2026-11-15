# m3 log — Heisenberg-covariant slice (swarm smwhnslql, direction d6)

Member m3. Direction: the Weyl–Heisenberg group over Z_6 and its stabiliser ("covariant")
MUBs; determine exactly how many pairwise unbiased stabiliser bases C^6 has, and isolate
the zero-divisor obstruction. Running log, in order.

## 0. Reading (start of run)

* Read the primary source in full (`attachments/how-do-i-make-ofyz/A promising idea ...txt`)
  and the code fragment (`Pasted text 1.txt`: exact Z[ζ_24] validation of a (3,3,2) triple
  and of the product control with Smith form [1,1,1,1,6]).
* Read `results/order3-stratum.md` (Lemma A on (2,2,2) multiplicities; the 7-parameter
  T-covariant stratum; the claim that every triple is order-3 symmetric, from the
  classification preprint) and skimmed `results/elegant-proof-routes.md`,
  `results/symmetric-obstruction-audit.md`.
* Board at start-up: five directions (detector audit; adversarial construction; product
  identity; nonextension/synthesis; literature audit). My first four registration attempts
  were refused as duplicates of those; the direction finally registered (d6) is the
  covariant slice, which none of the other five touches.

## 1. Exact arithmetic engine

Built `zeta.py`: elements of Z[ζ_24] = Z[x]/(x^8−x^4+1) as 8-tuples of integers, with
multiplication by convolution plus the reduction x^k = x^{k−4} − x^{k−8} (k ≥ 8).
Sanity checks: ζ^24 = 1, ω = ζ^4 has ω^3 = −1, √6 = ζ+ζ^{23}+ζ^5+ζ^{19} squares to 6.
Pitfall found and fixed: ζ^8 reduces to the two-term vector x^4 − 1, so a monomial must
be identified by its *exponent*, not by having a single nonzero coefficient.

## 2. The group and its maximal abelian subgroups

`wh.py`: H = {ω^θ X^a Z^b}, group law (θ,a,b)(θ',a',b') = (θ+θ'+a'b, a+a', b+b'),
matrix representation verified against the law. `wh2.py`: enumerated the 30 subgroups of
Z_6^2, found 20 isotropic and 12 maximal isotropic (all of order 6); the preimages are
exactly the 12 abelian subgroups of H of order 36. This matches the CRT picture:
3 lines in P^1(Z_2) times 4 lines in P^1(Z_3).

## 3. Eigenbases and the exact unbiasedness table

`cov.py`: for each of the 12 subgroups, an eigenbasis computed from a generator with a unit
shift part (so the eigenvectors are monomials; each column has support 6, entries
ζ^k/√6). Six of the twelve are flat (slopes 0..5); the other six ("vertical") are not.
`verify_joint.py`: for all 12 subgroups, every computed ray is a simultaneous eigenvector
of all 36 elements — this mattered, because a generator whose spectrum is degenerate would
silently produce a wrong basis.

`cov.py` table: the 66 pairwise unbiasedness tests agree exactly with the criterion
"M ∩ M' = Z(H)" — including the converse direction, which the proof does not need.
Bugs found and fixed on the way (recorded because they are exactly the kind of error the
route's audits must catch): (i) I first compared unnormalised inner products with 1
instead of with the product of the squared norms — the standard basis has norm 1 per
vector, the others √6, so the correct test is 6·|⟨u,v⟩|² = ‖u‖²‖v‖²; (ii) a first
"flatness" test asked all entries of the *basis matrix* to be nonzero, which correctly
rejects the standard basis — flatness is only required of the bases other than the anchor;
(iii) Smith normal form moved to `sympy.matrices.normalforms`.

`latin.py`: CRT invariants of the 12 subgroups (3 × 4 table printed), the criterion
verified on all 66 ordered pairs, and the maximal pairwise-unbiased subfamilies counted:
12 singletons, 36 pairs, **24 triples, no quadruple**.

`clifford.py`: GL(2,Z_6) has order 288, acts transitively on the 12 lines and on the 24
triples — so the covariant triple is unique up to Clifford equivalence. (CORRECTED in the
revision, see §8: the right group is SL(2,Z_6), order 144; SL is transitive on both sets
too, and only det = 1 lifts to unitaries.)

## 4. Delta and the source's detector on the covariant triples

`delta.py`/`delta3.py`: Δ computed from its definition (all 6! column permutations, exact
proportionality tests), at all three anchors, for the six covariant triples of flat bases:
**Δ = (6,6,6)** in every case. `index3.py`: the support lattice of the source at each
anchor, Smith form diag(1,1,1,1,6), index 6 — i.e. the source's formula (5)
Δ_X = [Λ_0:L_X] holds at all 18 anchor instances, and its table row for the product
triple is confirmed. `rank3.py`: rank_{F_3} R_X = 4 < 5 at all 18 anchors, so the
source's Ξ(P_X) vanishes at every anchor of every covariant triple: the product identity
holds there trivially (0·0·0), so covariant triples cannot test it.

## 5. Literature check (limited; m2 owns the full dossier)

Searched for the covariant/Heisenberg statement. Found: Grassl, "On SIC-POVMs and MUBs in
Dimension 6" (arXiv:quant-ph/0406175): the Heisenberg/Fourier-type triples in d = 6 are
maximal; and Brierley–Weigert (arXiv:0901.4051, PRA 79, 052316): a prescribed Hadamard
admits at most two mutually unbiased partners. So the *conclusion* of my theorem is known.
I claim no priority; the value here is a self-contained proof plus exact certificates.

## 6. Two steps of the head file re-proved independently

* Δ_X ∈ {1,2,3,6}: nonidentity elements of G_X act freely on the rays of the other bases
  (a fixed ray forces all diagonal entries equal), so the action is free, |G_X| divides 6,
  and a finite abelian group of order dividing 6 is cyclic. (Same conclusion as m4's
  Proposition 1, reached independently.)
* Recovery lemma: the source's missing line is Y² = diag_C(x²) for
  Y = Σ_j x_j c_j c_j*, which gives (Y²)_{ii} = (1/d)Σ_j x_j² for every i; without it the
  claim "the extra term is independent of i" is unjustified. With it, the rest of the
  source's argument goes through for d > 2.

## 6b. Cross-check of m5's (2,3,3) family

Rebuilt m5's "uniform case" family from scratch and recomputed Δ from the definition
(brute force over 6! permutations, exact field inverses), as an independent check of their
Smith-form computation (`gen_delta.py`, `census.py`, `xi_check.py`):

* H = F D Π over Z[ζ_24]: 162 matrices, exactly 108 with |HF|² = 3 (their classification
  step reproduced);
* (I, U, V) is a MUB triple, verified exactly for every sampled pair;
* Δ-patterns over 10 sampled pairs: (6,6,6) seven times, (2,3,3) three times — the same
  two values m5 reports, now obtained without any lattice/Smith input;
* F_3 ranks (source Ξ): (2,3,3) instance → rank 5 at the Δ=2 anchor (Ξ > 0), rank 4 at the
  Δ=3 anchors; (6,6,6) instance → rank 4 everywhere.

Bug I made and fixed here (logged because the failure mode matters): my first rank-one
test used a mis-signed cross-multiplication and returned Δ = 0 for every triple —
a silent false negative in exactly the computation the project uses to read off
symmetries. The correct identity is
X_{iσ(j)}X_{i'σ(j')}X_{ij'}X_{i'j} = X_{iσ(j')}X_{i'σ(j)}X_{ij}X_{i'j'}; simultaneously I
re-verified the ring itself (associativity samples and a sympy polynomial cross-check,
`diag4.py`).

## 7. Not done

* The 18 covariant triples that contain a non-flat base were not run through the
  Δ-computation (they need a larger cyclotomic field, Z[ζ_36] or Z[ζ_72], for the
  spectral projectors). They are pairwise unbiased by Lemma 3 and the criterion table,
  but Corollary 2 is asserted only for the flat six.
* No attempt at N(6) = 3; the covariant slice is closed at 3 by a different mechanism
  (the qubit factor's three lines), which is not what the source's route uses.

## 8. Corrections after the first submission was returned

The judge returned the submission with four repairable defects; all are fixed and logged
here rather than quietly applied.

1. *Lemma 1 was mis-stated*: I wrote $|M| = 6|\pi(M)|$ for every abelian $M$, which is false
   without $Z(H)\subseteq M$. Corrected to
   $|M| = |M\cap Z(H)|\cdot|\pi(M)| \le 6|\pi(M)|$, with equality for maximal $M$.
   Lemma 1(iii) now also carries the explicit extension argument: a larger isotropic
   $S\supsetneq\pi(M)$ would make $\pi^{-1}(S)\supsetneq M$ abelian, contradicting
   maximality, so $\pi(M)$ is maximal isotropic and (by CRT) of order 6.
2. *Wrong group*: `clifford.py` selected $\det$ a unit ($GL$, 288 matrices). Equivalence of
   MUB configurations needs $\det = 1$, i.e. $SL(2,\mathbb Z_6) = Sp(2,\mathbb Z_6)$ (144
   matrices), the only part of $GL$ that preserves the commutator form and lifts to
   unitaries. Script and prose changed; re-run: still one orbit on the 12 lines and one
   orbit on the 24 triples.
3. *Unjustified commutant claim*: the switch
   $\mathrm{commutant}(\rho(M)) = \rho(C_H(M))$ (Burnside) is replaced by a direct argument:
   $H$ permutes the characters of $M$; the stabiliser of an occurring character is
   $\{g : \chi([M,g]) = 1\} = C_H(M) = M$ since $[M,g]\subseteq Z(H)$ and $\chi|_{Z(H)}$ is
   injective; so each occurring character has orbit $|H|/|M| = 6$, all six occur, and the
   six weight spaces are one-dimensional because they sum to $\dim\mathbb C^6 = 6$. The
   exact all-12 verification stays in as corroboration only.
4. *Scope*: the $\Delta$ and rank claims are now explicitly confined to the six flat
   covariant triples (18 anchors), where $\Delta$ was computed from its definition. The
   extension to all 24 is a labelled remark resting on the cited Weil lift of
   $Sp(2,\mathbb Z_6)$, not a claimed result.

Nothing in the computed numbers changed: 12 maximal abelian subgroups, 24 triples, no
quadruple, $\Delta = (6,6,6)$ on the flat six, index 6 and $\mathbb F_3$-rank 4 at all 18
anchors, and the cross-check of m5's $(2,3,3)$ family.
