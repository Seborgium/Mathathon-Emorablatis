# Overnight symmetry run — consolidated result

Run `smwhnslql`: six members, `deepseek/deepseek-v4.1-flash`, maximum reasoning effort. It ended
early with **five accepted scoped solutions**; the elapsed time was about 54 minutes. This is a
summary of what was actually checked by the lead reviewer. **It is not a new proof of $N(6)=3$, and
no complete direct proof of the global symmetry-forcing statement was found.**

## 1. Strongest proved proof architecture

For a MUB triple in $\mathbb C^6$, define $\Delta_X$ at anchor $X$ as the order of the group of
unitaries, diagonal in the $X$ basis and considered modulo scalars, which preserve each of the other
two bases as ray sets.

The following now has a complete proof:

1. $\Delta_X\in\{1,2,3,6\}$ and the group is finite cyclic.
2. The projection/support-lattice detector satisfies
   $$\Delta_X=[\Lambda_0:L_X],\qquad
   \Xi(P_X)=0\iff \operatorname{rank}_{\mathbb F_3}R_X<5\iff 3\mid\Delta_X.$$
   Two missing proofs were supplied: the uniform case of the rank-one recovery lemma, and the
   dimension-six no-exchange theorem for diagonal projection symmetries.
3. The locus $Z=\{3\mid\Delta_X\text{ for some }X\}$ is closed. Consequently
   $$Z=\mathcal T\iff Z\text{ is dense in }\mathcal T.$$
   A proof on a dense subset of the **entire** triple space suffices. Closedness alone does not give
   a componentwise criterion.
4. If $3\mid\Delta_X$ at one anchor, the order-three element has spectrum $(2,2,2)$ and two
   3-cycles on each other basis. The project's elementary symmetric nonextension theorem therefore
   applies: no vector—and hence no fourth basis—can extend that triple.

Write
- **T3**: every triple has $3\mid\Delta_X$ at some anchor;
- **T2**: every triple has $\Delta_X\ge2$ at some anchor;
- **I3**: $\Delta_X=2\Rightarrow3\mid\Delta_Y$ at both other anchors;
- **T1**: $\Xi(P_A)\Xi(P_B)\Xi(P_C)=0$ for every triple.

The exact logical status is
$$T1\iff T3,\qquad T2+I3\Rightarrow T3\Rightarrow\text{no fourth basis}.$$
T3 follows from the cited Wuttig–Tindall classification, but was not derived directly here. The
full I3 is also unresolved. Therefore **T3 (equivalently T1) is the remaining direct target**;
T2 becomes sufficient only after I3 is proved.

## 2. Accepted advances

### Detector and lattice audit — m1

[m1-audit.md](m1-audit.md) proves the projection formula, the repaired rank-one recovery lemma, the
lattice/annihilator identification, the no-exchange theorem, and the detector equivalences. The trace
identity $|\operatorname{tr}T|^2=6$ is valid; the new work supplies odd-power order reduction and
the order-two/three/four exclusions. This supersedes the earlier incorrect criticism that only an
inequality follows.

### Nonextension and synthesis — m6

[m6-proof-revision.md](m6-proof-revision.md) verifies that the symmetric nonextension theorem's
hypotheses follow from $3\mid\Delta_X$, not additional assumptions. It also corrects the earlier
normalisation audit: diagonal rephasing preserves a diagonal clock because all diagonal unitaries
commute.

The older conditional entries in that document about the recovery lemma and formula (5) are now
upgraded by m1's accepted audit. I3 remains unproved.

### Closedness — m4

[m4-theorem.md](m4-theorem.md) proves the closedness/density statement. Its first version's
clopen/component inference was rejected and withdrawn; a single symmetric point per component is not
enough.

### Covariant slice — m3

[m3-covariant-bound.md](m3-covariant-bound.md) gives a self-contained proof that at most three
pairwise unbiased Heisenberg-stabiliser bases exist in $\mathbb C^6$. The bound is attained; there
are 24 covariant triples and no quadruple; $SL(2,\mathbb Z_6)$ (order 144) is transitive on them.
This says nothing about non-stabiliser triples.

### Current-v2 MMVW audit — m2 (direction d7)

[m2-v2-detector.md](m2-v2-detector.md) distinguishes the superseded v1 detector from current v2.
The latter uses $G_{H_j}(\gamma_2)G_{H_j^*}(\gamma_2)$ and v2 Proposition 4.2 needs Conjectures
2 **and** 3. A parity lemma proves the adjoint detector vanishes for matrices in the Eq. (33) normal
form; this is only one clause of v2 Conjecture 2.

## 3. Additional reviewed uniform-case proof

[uniform-case-reviewed.md](uniform-case-reviewed.md) repairs the source's **uniform** involution
argument. It adds the missing row/conjugate Hadamard lemma by applying the column lemma to a
transpose and taking complex conjugates. It proves that, in the uniform case, $Z\oplus Z$ is an
order-three clock at both other anchors.

This does **not** finish I3: the nonuniform case and completeness of the numerical involution-stratum
enumeration remain open. m5's broader whole-stratum assertion was rejected because support
monotonicity does not imply local constancy or exhaustive component coverage.

## 4. Reproduced computations

Checks rerun by the lead reviewer include:

- exact $\Delta=(2,3,3)$, Smith diagonals $(1,1,1,1,2)$, $(1,1,1,1,3)$, $(1,1,1,1,3)$;
- exact isolated/product data $\Delta=(6,6,6)$ and Smith diagonals $(1,1,1,1,6)$;
- exact family-centre data $\Delta=(3,3,2)$ and relabelled $(3,2,3)$;
- 24 product triples at all 72 anchors: index 6, rank 4, no swap;
- $108^2=11664$ uniform constructions: zero clock failures;
- 4,600 random family points and a 120-by-120 grid: the reported $\Delta$ tallies match;
- current-v2 MMVW checks plus a seeded 25-point sweep: maximum $\gamma_1$ detector
  $1.61\times10^{-28}$ and maximum adjoint product $3.72\times10^{-28}$.

These are exact where labelled exact, and numerical evidence only otherwise. No $(1,1,1)$ example was
found, but the samples do not prove its nonexistence.

## 5. Corrections made during review

Several initial submissions were rejected and repaired rather than accepted on plausibility:

- m4's invalid clopen/component argument was withdrawn;
- m2's $\gamma_2$ implementation bug and v1/v2 literature confusion were corrected;
- m3's maximality and Clifford-group issues were repaired;
- m6's projection-entry count and unconditional-residue wording were corrected;
- m5's numerically overclaimed whole-stratum conclusion was narrowed;
- m4's incorrect trace criticism and a duplicate identity-order helper bug were corrected during
  integration.

## 6. What remains open

1. A direct algebraic or analytic proof of T3, equivalently T1.
2. The nonuniform half of I3, including the status of the source's normal form (8).
3. A full symbolic proof of current-v2 MMVW Conjecture 2 on the continuous family, and a proof of
   v2 Conjecture 3 within the MMVW route.
4. Publication-level novelty. The computations and proof repairs support the proposed direction, but
   do not establish that the detector or its overall method is new.

The useful outcome is therefore a much smaller and better audited proof architecture, with exact
counterexample checks and two repaired analytic arguments—not a completed elegant proof of the full
dimension-six theorem.
