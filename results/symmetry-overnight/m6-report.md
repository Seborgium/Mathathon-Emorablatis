# m6 final report — the nonextension step is not the residue

Swarm `smwhnslql`, member m6, direction d4 (nonextension side and proof synthesis).
Deliverables in this directory: `m6-report.md` (this file), `m6-proof-revision.md` (the modular
revision with all proofs), `m6-check.py` (exact script), `m6-log.md`.

## Outcome in one paragraph

The diagonal-symmetry route to $N(6)=3$ needs **no new nonextension theorem**.  The nonextension
statement it requires — "a MUB triple in $\mathbb C^6$ carrying an order-$3$ diagonal symmetry has
no fourth basis" — is already proved in this project, and I re-verified its proof line by line; its
hypotheses (eigenvalue multiplicities $(2,2,2)$, two $3$-cycles on each of the other two bases,
symmetry at one anchor only) are **consequences** of $3\mid\Delta_X$, not extra assumptions.  What
remains is exactly one symmetry-forcing statement.  **Unconditionally that statement is $(T3)$**
("every triple has $3\mid\Delta_X$ at some anchor"), equivalently the source's $(T1)$; everything
downstream of $(T3)$ is proved here.  If one also grants the source's divisibility lemma **(I3)**
(order $2$ at an anchor forces order $3$ at the other two — the one input I did not verify), the
target weakens to $(T2)$: *every MUB triple in $\mathbb C^6$ has $\Delta_X\ge2$ for some anchor $X$*,
equivalently "every triple is invariant, as a ray-set triple, under a non-scalar diagonal unitary at
some anchor".  So the correct implication is $(T2)+(I3)\Rightarrow(T3)\Rightarrow$ no fourth basis;
without (I3) the open target is $(T3)$, not $(T2)$.  I also prove that $(T2)$ is a **closed** condition whose
complement is open: it propagates from a dense family of triples to all triples, but no argument
that works only on an open subset, by perturbation, or by local constancy can establish it.  Finally
I show that the source's central identity (13) is *exactly* the order-$3$ form of the same
statement (not a weaker target), i.e. the hard step in algebraic clothing.

## Verdicts (detail and proofs in `m6-proof-revision.md`)

**[P] proved here.**

1. *Lemma 1*: $G_X$ is a finite abelian group with $\Delta_X\in\{1,2,3,6\}$, acting freely on the
   rays of the other two bases.  The source's proof is missing the finiteness step; the free action
   on one other basis already gives an injection $G_X\hookrightarrow\mathrm{Sym}(6)$, which supplies
   it.  (Source §2 thereby validated as stated.)
2. *Lemma 2*: an element of projective order $3$ acts as two $3$-cycles and has spectrum
   $(2,2,2)$.  The source's "acts in two $3$-cycles, giving $\operatorname{tr}T=0$" needs one
   inserted line (in the permuted basis $T$ is monomial with a fixed-point-free permutation, hence
   traceless); then $2+2+2$ follows from $1+\omega+\omega^2=0$.  (Project `order3-stratum.md`
   Lemma A proves the same statement by a different route; the two agree.)
3. *Lemma 3*: $3\mid\Delta_X$ for one anchor implies the Symmetry Obstruction's hypothesis verbatim.
   Hence multiplicities, both-other-bases, and anchor independence are all automatic.
4. *Symmetry Obstruction re-verified* (all six sections of
   `attachments/is-this-a-useful-r01i`): normalisation, the $3\times3$ Fourier forcing
   $v_j=\nu_j(1,-1)/\sqrt6$, the Fourier/triangle observation, the $\lambda_j$-cancellation in the
   fourth-vector step, the Heron inequality $s+4|t|+s^2/12\le1$ (I checked the underlying identity
   $16\Delta^2=(12-12s-s^2+48t)/64$ symbolically), the $3\times3$ sign lemma (row products negative
   by a two-case bound, then even column flips, then $b+c>a$ versus zero column sums).  It is
   correct.  **One error in the project's own audit note is corrected**: its item (i) calls the
   normalisation step wrong and proposes a blockwise $U(2)$ repair; the step is valid as written,
   because flatness gives every coordinate of $u$ modulus $1/\sqrt6$ and *every* diagonal unitary
   commutes with *every* diagonal $T$.  The audit's justification (only block-scalar rephasings
   commute with $T$) is false.
5. *Residue shape* **[P]**: $\{\Delta_X\ge2\}$ and $\{3\mid\Delta_X\}$ are closed — the second
   without any further input, because $\Delta_X\ge2$ iff $G_X$ meets the finite set of diagonal
   clocks with sixth-root-of-unity entries, and "$[T]\in G_X(x)$" is a closed condition in $x$.
   Hence $\{\Delta_X=1$ for all $X\}$ is open: a *dense* family of triples suffices, but nothing
   smaller does, so no local-constancy, perturbation or near-miss argument can close the residue.
   (The finer statement $\Delta_X(x_n)\mid\Delta_X(x)$ under limits is **[C]** on the source's (5) =
   the rank-one recovery lemma; it is not needed for closedness.)
6. *Architecture*: with $(T1)$ = the source's equation (13), $(T3)$ = step (H2) of the published
   classification ($\exists X:3\mid\Delta_X$), $(T2)$ = the residue above, and $(I3)$ = the source's
   divisibility lemma,
   $$(T1)\iff(T3)\ \Longrightarrow\ (T2),\qquad (T2)+(I3)\Longrightarrow(T3)\ \Longrightarrow\ \neg(N(6)\ge4).$$
   The equivalence $(T1)\iff(T3)$ is immediate from the definition of $\Xi$ ($\Xi>0$ iff some
   $5\times5$ minor of the relation matrix is nonzero mod $3$), given the source's criterion (3) and
   the rank-one recovery lemma.  So (13) is not a weaker target: it *is* the hard step.

**[P] exact computation** (`m6-check.py`, arithmetic in $\mathbb Z[\zeta_{24}]$, $\approx1$ s, scans
all $900$ matrix-unit positions): for the tensor triple $\{\mathbb 1_6,\ H\otimes F_3,\ H'\otimes
F'_3\}$ — $\Delta_{\mathcal A}=\Delta_{\mathcal B}=\Delta_{\mathcal C}=6$; element orders
$1,2,3,3,6,6$ with multiplicity patterns $(6),(3,3),(2,2,2),(2,2,2),(1^6),(1^6)$ and cycle types on
each of the other two bases $(2,2,2),(3,3),(3,3),(6),(6)$; **$150$** nonzero projection entries at
each anchor, of which exactly $30$ are the positions $(i,j,i,j)$ with value $1/3$ (the source's
normalisation) and **zero** relation vector, leaving $120$ nonzero relations with support-lattice
Smith form $[1,1,1,1,6]$, so the source's identity (5) $\Delta_X=[\Lambda_0:L_X]$ holds exactly
here.  The value $6$ is *proved*, not just searched: every element of $G_X$ commutes with
$P_X$, the latter's phases form the character group of a lattice of index $6$ (a group of order $6$,
all of whose characters are $6$th roots of unity), and six are exhibited.  This confirms the
source's table row "standard product triple, $\Delta=6$" at all three anchors.

**[C] conditional inputs I did not verify.** (i) the source's divisibility lemma (I3) (source §4;
needed only to pass from order $2$ to order $3$ — the $(T1)/(T3)$ route does not use it); (ii) the
rank-one recovery lemma, used only to identify projection symmetries with geometric ones; (iii) the
literature: $N(6)=3$ is **proved** (m2's board finding: arXiv:2611.06917 with arXiv:0902.0882), and
$(T3)$ is certified there by 2,775 interval balls.  This report presents no new proof of $N(6)=3$.

**[O] unresolved.** $(T3)$, equivalently $(T1)$ — the unconditional residue — and with it $(T2)$; the source's exact $(3,3,2)$ example (its support-lattice
Smith forms $[1,1,1,1,3],[1,1,1,1,3],[1,1,1,1,2]$ are *not* those of the tensor triple, which gives
$[1,1,1,1,6]$ three times, so it is a genuinely different exact triple and I could not reconstruct
it); whether an anchor with $\Delta=2$ exists at all in exact arithmetic.

## Cross-check against another member's board work

m4 (direction 3) has posted `m4-theorem.md`, which independently proves (i) $G_X$ finite abelian with
$|G_X|\mid6$ — by the identity-component argument, instead of my injection into $\mathrm{Sym}(6)$;
the two proofs agree — and (ii) that $Z=\{3\mid\Delta_X\text{ for some }X\}$ is closed/clopen, and
(iii) that (13) holds for all triples iff no connected component of the triple space consists of
triples with $3\nmid\Delta_X$ for all $X$.  Their (iii) is my $(T1)\iff(T3)$ seen component-wise; the
two formulations are consistent, and their Proposition 1 is a second, independent proof of my
Lemma 1.  Nothing in their file conflicts with anything here; the addition here is that the same
finite-torsion argument with $6$-torsion in place of $3$-torsion gives closedness of $\{\Delta\ge2\}$
too, and that the divisibility lemma — if granted — lets one work with order $2$ instead of order $3$.

## What this changes for the project

* The bridge to $N(6)=3$ is complete except for one closed-condition statement about *triples*,
  namely $(T3)$ (unconditionally) or $(T2)$ (granting (I3)); the fourth-basis analysis, the
  multiplicities and the anchor-independence questions are all discharged, and no graph search or
  classification of completions is needed.  In particular the source's programme does not
  need the "symmetry propagation" conjecture of `results/order3-stratum.md` §8.
* The source's strongest target (13) and the published step (H2) are the *same* statement; so no
  amount of extra structure in $\Xi$ can make (13) easier than (H2).  A counterexample to (13) would
  refute (H2) and therefore the published classification, which is why none exists in the known
  families.
* The one place where the source's own §4 could still fail is the normal form (8) and the
  uniform/nonuniform dichotomy; nothing else in the route uses it.  It matters only for the weaker
  $(T2)$ version of the target, so an error there would not damage the $(T3)$ route.
