# Can $N(6)=3$ be proved conceptually? A route map, with three verified identities

Short companion for circulation: `mub-why-no-elegant-proof.pdf` (2 pp.), the same diagnosis without
the technical appendices.

Working notes, 2026-11-14. Companion to `results/proof-summary.md` and `results/improvements.md`.
The question: replace the finite case analysis (25-phase bins, tangent balls, two-graph clique
search) by an argument grounded in structure.

Claim of this note: the conceptual content of the problem is now **nearly complete, and the
residue is one clearly stated finite classification**. Section 2 gives three reasons why the
attractive abstractions provably cannot finish the job; Section 3 lists seven routes with their
exact status; Section 4 records what I verified myself; Section 5 states the reduced problem.

---

## 1. Shape of any proof

Write $N(d)$ for the maximum number of pairwise unbiased orthonormal bases of $\mathbb{C}^d$.
Every proof of $N(6)\le 3$ must exclude a *quartet*. Three equivalent encodings, all used in the
literature:

* **Hadamard form.** After a unitary and a choice of first basis,
  $\{I,\ H_2/\sqrt6,\ H_3/\sqrt6,\ H_4/\sqrt6\}$ with each $H_i$ complex Hadamard
  ($|(H_i)_{jk}|=1$, $H_iH_i^*=6I$) and each cross ratio $H_i^*H_j/\sqrt6$ Hadamard. Equivalent
  and cleaner: *flat unitaries* $U_1=I,U_2,U_3,U_4$ with $U_i^*U_j$ flat for all $i\ne j$.
* **Operator form.** A basis $\leftrightarrow$ its maximal abelian $*$-subalgebra (MASA) of
  $M_6(\mathbb{C})$; unbiased $\leftrightarrow$ orthogonal under $\operatorname{tr}(A_iA_j)=1$.
  So $m$ MUBs $=$ $m$ pairwise orthogonal MASAs, equivalently $m$ pairwise Killing-orthogonal
  Cartan subalgebras of $\mathfrak{sl}_6(\mathbb{C})$.
* **Gram form.** A rank-6 positive semidefinite $24\times24$ matrix whose $6\times6$ blocks are
  $I$ on the diagonal, flat unitaries off it ($1/\sqrt6$ times a unimodular unitary).

All three are *equalities of structure*, not inequalities. This is the first thing to notice about
the problem: **there is no obvious potential function to bound.** Every one of the 25 phases is a
continuous degree of freedom and no invariant is known to be extremised by a quartet. That is why
the existing proofs are coverings of a parameter space rather than estimates.

## 2. Three rigidity failures: why the natural abstractions cannot be completed

These are the load-bearing negative facts. Each is a theorem or an explicit counterexample, not a
guess, and each kills a family of would-be elegant proofs.

**(a) No arithmetic rigidity.** Real Hadamard matrices of order $6$ do not exist, and the reason
is arithmetic: a real Hadamard of order $n>2$ forces $n\equiv 0 \pmod 4$, and $6\equiv 2$. The
complex case has no such obstruction: order-six complex Hadamards contain the two-parameter family
$F(a,b)$ with $a,b$ arbitrary reals, so there are Hadamards with transcendental entries. Any
argument of the form "reduce mod $p$", "the entries are roots of unity", "Galois acts on the
finite solution set and contradicts integrality" is therefore unavailable *unless* it first proves
that a **quartet** forces algebraicity. That extra step is not known, and Section 3 (R6) explains
why, even if granted, it does not finish.

**(b) No forced discrete design.** The classical dictionary is: $d+1$ MUBs in dimension $d=p^k$
$\leftrightarrow$ a spread of $\mathrm{PG}(2k-1,p)$ $\leftrightarrow$ an affine plane of order $d$
$\leftrightarrow$ $d-1$ mutually orthogonal Latin squares of order $d$. For $d=6$ the target does
not exist: no affine plane of order $6$ (Bruck–Ryser: order $6\equiv1,2\pmod4$ needs
$6=a^2+b^2$, impossible), equivalently no pair of orthogonal Latin squares of order $6$ (Tarry
1901, the 36 officers). So a very attractive route exists:

> 4 MUBs in $\mathbb{C}^6$ $\Longrightarrow$ a $4$-net of order $6$ $\Longrightarrow$ 2 MOLS(6),
> contradicting Tarry.

The implication is **false as stated**, and the reason is exactly (a): the MUB $\to$ net passage
uses the finite-field/Weil structure, which is what makes the phases discrete. A MUB triple in
$d=6$ carries two continuous parameters (Jaming–Matolcsi–Móra–Szöllősi–Weiner 2009 exhibit an
infinite family), so no discrete transversal design is forced even by three bases. A proof along
this line would need a separate lemma "a *fourth* basis forces discreteness"; nobody has one.

Worse for the route, the design mechanism is not merely short at $k=4$, it is **empty at order 6**:
there is no $(6,k,1)$-difference matrix at all for any $k\ge3$, over either group of order 6
($Z_6$: every permutation sums to $15\equiv3\pmod6$, so $\varphi-\psi$ sums to $0$ where a
permutation needs $3$; $S_3$: exhausted over all $720^2$ pairs of bijections). So no *regular* net of
order 6 exists even with three classes, and the translation-net mechanism produces no MUB in
dimension 6 whatsoever.

And no dimension-uniform rescue exists: "4 MUBs in $\mathbb{C}^d$ $\Rightarrow$ an affine plane of
order $d$" is false, with $d=21$ as witness ($N(3)=4$ and $N(7)=8$ tensor to 4 MUBs in
$\mathbb{C}^{21}$, while $21\equiv1\pmod4$ and $21\ne a^2+b^2$, so Bruck–Ryser–Chowla forbids even a
projective plane of order 21). A *dimension-6-specific* design implication is not excluded by that,
but no candidate for one has survived inspection.

This is the honest content of the standard intuition "6 fails because there is no affine plane of
order 6": the intuition is right about *why*, and cannot be upgraded to a proof of *that*.

**(c) The invariant-theoretic bounds are vacuous at the critical point.** For $n$ unit vectors in
$\mathbb{C}^d$ the frame/Welch bound reads $\sum_{i,j}|\langle u_i,u_j\rangle|^2 \ge n^2/d$. A
union of orthonormal bases **attains** it identically, because each basis alone resolves the
identity: for $m$ MUBs in dimension $d$, $n=md$ and the sum is
$n + n(n-d)\cdot\frac1d = n^2/d$. (Checked: $m=4,d=6$ gives $24+432/6=96=24^2/6$.)

This can now be made a theorem about the whole relaxation family, which is worth doing because it
forecloses a large class of attempts at once. Two statements, both verified:
* *Modulus-level blindness.* For $m$ MUBs the matrix of squared overlaps is the single closed form
  $Q_m = I + \frac1d(J_m - I_m)\otimes J_d$, with spectrum $(m,\,1^{m(d-1)},\,0^{m-1})$ — positive
  semidefinite for **every** $m$ (checked numerically at $m=2,3,4,7,12$: least eigenvalue
  $\ge-2\times10^{-16}$, top eigenvalue exactly $m$). So no bound that sees the overlaps only
  through their moduli — few-distance, relative-design, Welch-type, association-scheme/Delsarte LP —
  can separate $m=3$ from $m=4$.
* *No Gram-level relaxation gap.* A positive semidefinite matrix with diagonal blocks $I_d$ and
  off-diagonal blocks of constant modulus $d^{-1/2}$ has $\operatorname{tr}G=md$ and
  $\operatorname{tr}G^2 = md + m(m-1)d = m^2d$, so Cauchy–Schwarz forces rank $\ge d$; the diagonal
  blocks force rank $\ge d$ as well, and rank $\le d$ because it is a Gram matrix in $\mathbb{C}^d$.
  Hence rank is exactly $d$ and all nonzero eigenvalues equal $m$ (verified for $m=4$: rank 6,
  $\operatorname{tr}G^2=96$, six eigenvalues equal to 4). So PSD feasibility *is* existence: there
  is no relaxation gap to exploit anywhere at the Gram level. The entire difficulty is in the
  phases, which is now a theorem rather than an impression.

There is a numerical counterpart worth stating, because it discourages quantitative stability
arguments: the energy $E_m=\sum_{i<j}\sum_{u,v}|\langle u,v\rangle|^4$ satisfies
$E_m-\binom m2 = \sum_{i<j}\|Y_{ij}-J_d/d\|_F^2 \ge 0$ (identity verified to $10^{-16}$, $Y$
doubly stochastic), so MUB-ness is exactly its zero set; and the measured gap for $d=6,m=4$ is
$\le 5.1\times10^{-2}$, against $2/3$ for $(d,m)=(2,4)$ and $4/3$ for $(3,5)$, which are impossible.
**The obstruction in dimension six is not energetic.**

## 3. The seven routes

**R1. Finite geometry / designs.** See 2(b). Status: *dead as a route to the theorem*, with a clean reason
and one genuinely useful finite by-product.

The by-product is the exact form of the "no affine plane of order 6" obstruction. Let $A$ be a finite
abelian group of order $d^2$ with a nondegenerate alternating form, $W$ a Weyl system on $A$, and
$L_1,\dots,L_m$ isotropic subgroups of order $d$. The adapted bases are pairwise unbiased iff
$L_i\cap L_j=\{0\}$, and then $A\to A/L_i\times A/L_j$ is a bijection, so $m$ bases give an
orthogonal array $\mathrm{OA}(d^2,m,d,2)$. I verified the resulting counts exhaustively (max clique
in the "trivial intersection" graph):

| $d$ | group | subgroups of order $d$ | max pairwise transversal |
|---|---|---|---|
| 2 | $Z_2^2$ | 3 | 3 |
| 3 | $Z_3^2$ | 4 | 4 |
| 4 | $Z_4^2$ (clock and shift) | 6 cyclic (+1 torsion) | **3** |
| 4 | $F_4^2=\mathbb{F}_2^4$ (field) | 35 | **5** |
| 5 | $Z_5^2$ | 6 | 6 |
| 6 | $Z_6^2$ | 12 | **3** |

There is only one group in the last row: $Z_2^2\oplus Z_3^2\cong Z_6^2$ by CRT, and a nondegenerate
alternating bicharacter forces each Sylow part to be elementary abelian ($Z_{p^2}$ carries only the
trivial alternating form), so **$Z_6^2$ is the only abelian group of order 36 carrying an irreducible
Weyl system of dimension 6.** Hence the table proves: **there is no set of 4 Galois-type MUBs in
$\mathbb{C}^6$** — a complete finite result, independent of Tarry.

The $d=4$ rows are the interesting ones. Prime-powerness enters through the *field*, not the size:
$Z_4^2$ has only 3 transversal lines (so clock-and-shift gives 3 MUBs in $\mathbb{C}^4$) while the
additive group of $F_4$ gives 5, a spread of $\mathrm{PG}(3,2)$, and the bound $15/3=5$ is attained.
At $d=6$ there is no field at all and both groups collapse $12\to3$.

The sharp statement of the collapse is worth recording, because it is often mis-stated. The Weyl
system in dimension 6 is unique up to equivalence (there is exactly one index-1 nice error basis),
its maximal isotropic subgroups are the $3\times4$ CRT grid (three lines of $\mathbb{F}_2^2$ times
four of $\mathbb{F}_3^2$), and two are transversal iff *both* components differ. So the cap is
$\min(N(2),N(3))=\min(3,4)=3$: **the qubit side runs out of lines.** That is an arithmetic reason
($\mathbb{F}_2^2$ has three one-dimensional subspaces), not the usual "6 is not a prime power".
It also explains the classical triple: it is the tensor of the complete qubit triple with three of
the four qutrit bases (verified: worst deviation $3.9\times10^{-16}$; the natural fourth candidate
has overlaps of modulus$^2$ exactly $1/3$).

What this does *not* do is bound $N(6)$, because "MUB $\Rightarrow$ Galois type" is false: it fails
already at $m=3$ (JMSSW's triplet family has non-root-of-unity entries, and countably many
transcendental members), and a self-contained $m=2$ counterexample is immediate — $F(\sqrt2,\sqrt3)$
has a transcendental entry while Galois-type pairs are algebraic. So the four-basis problem needs a
rigidity theorem with no analogue one level down, which is nobody's theorem today.

**R2. Lie algebra: orthogonal decompositions.** $m$ MUBs $=$ $m$ pairwise Killing-orthogonal Cartan
subalgebras of $\mathfrak{sl}_6(\mathbb{C})$ **that are closed under the adjoint**
$X\mapsto\bar X^T$ (Boykin–Sitharam–Tiep–Wocjan 2007). Status: *equivalent restatement only with the
star hypothesis, and the star hypothesis is essential — so Lie theory alone is provably insufficient.*

That correction is worth stating precisely, because the folk version omits it. Orthogonality of the
Cartan subalgebras $h_{C_a}=\{C_a\operatorname{diag}(\lambda)C_a^{-1}\}$ and $h_{C_b}$ is exactly
$$T\circ(T^{-1})^{\mathsf T} = J_6/6,\qquad T=C_a^{-1}C_b .$$
For **unitary** frames $(T^{-1})_{ji}=\overline{T_{ij}}$, so this is precisely $|T_{ij}|^2=1/6$, the MUB
condition. For non-unitary frames it is strictly weaker, and no column rescaling unitarises a general
frame (column scaling is invisible to $h_C$, since eigenvectors are unchanged). Consequently four
pairwise Killing-orthogonal Cartan subalgebras exist whose bases are *not* unbiased — verified
explicitly: four distinct $5$-dimensional abelian traceless subalgebras, all pairwise Killing pairings
$\le5.4\times10^{-16}$, self-pairings $2$, whose polar bases miss unbiasedness by $0.19$–$0.31$.

So any proof proceeding from the Lie bracket and the Killing form alone cannot work: the
Lie-theoretic statement without star-closedness is **false**. The Hilbert-space structure
(positivity, the adjoint) is doing essential work. The preprint does state the hypothesis; the
slogan version usually does not.

**R3. OMAS classification (Beauchamp–Nicoara 2008).** Classifies orthogonal maximal abelian
$*$-subalgebras of $M_6$ in the algebra sense. Status: *structural, but the moduli survive*. An
OMAS classification up to equivalence still leaves continuous families (the Hadamard families are
continuous), so it cannot by itself bound $m$.

**R4. Positive definite functions / dual SDP bounds (Kolountzakis–Matolcsi–Weiner 2018;
Bandeira–Doppelbauer–Kunisky 2022).** The only abstract method in this area with rigorous
computer-free-feeling bounds: it produces *dual certificates* (a positive definite function, or a
PSD matrix, that certifies an upper bound). Status: *vacuous at $d=6$* by 2(c). Worth knowing
because it is the template for what a "certificate instead of a case check" would look like.

**R5. Topology and connectedness (Wuttig–Tindall, arXiv:2611.06917, 4 Nov 2026).** This is the
real conceptual advance, and it is recent enough that it deserves to be read before anything else
is attempted.

* *Dimension collapse.* Every order-six complex Hadamard except Tao's is determined, up to
  equivalence, by a dephased $3\times3$ corner
  $E(\theta)=\begin{pmatrix}1&1&1\\1&e^{i\theta_1}&e^{i\theta_2}\\1&e^{i\theta_3}&e^{i\theta_4}\end{pmatrix}$
  with **four** free phases — not 25. Orthogonality fixes the block Gram matrices
  $G_h=6I-EE^\dagger$, $G_v=6I-E^T\bar E$; a scalar invariant
  $\Psi(B)=\operatorname{perm}(B)\det(B)^2/\prod B_{jk}$ is determined up to the two conjugate
  values $\Psi_\pm=(-\chi\pm i\sqrt R)/2$, and $R=4g^2\eta-\chi^2\ge0$ decides whether the corner
  is a *strict seed*. So the space of pairs is a $4$-torus (plus one chart at $F_6$), not a
  $25$-torus.
* *Connectedness.* $\{\theta: R(\theta)>0\}$ is connected, and hence so is the space $X$ of all
  non-Tao Hadamard classes. This is the step that replaces "cover by bins" with "cover by finitely
  many balls, which connectedness makes sufficient".
* *Classification.* With the space connected, they cover it by 2,775 four-dimensional balls plus
  the $F_6$ chart, and in each ball show that every triple is of a known type: either a member of a
  two-parameter family or the single isolated Fourier triple. Since neither extends to a fourth
  basis (Jaming et al. 2009 for the family), $N(6)=3$.
* *Residue.* 2,775 certified balls and a local graph search in each. Conceptually this is a
  *classification of the 2-dimensional moduli space of triples*, not a search of a 25-dimensional
  one — a different order of thing from the preprint's pipeline, but still a finite machine check.

**R6. Exact algebra / quantifier elimination.** The quartet conditions are polynomial equations
with integer coefficients in the matrix entries and their conjugates, so the quartet locus is a
real-algebraic set defined over $\mathbb{Q}$, and the set $\Sigma$ of pairs admitting a third basis
is its projection: **semialgebraic**, closed in the compact pair space, of real dimension 2.
Consequences worth stating precisely:
* a *rigid* (isolated) quartet would have algebraic entries — but that buys nothing, because
  algebraic numbers of modulus 1 need not be roots of unity, so 2(a) still blocks the arithmetic
  finish;
* in principle $\Sigma$ has an exact semialgebraic description, obtainable by quantifier
  elimination. That would be a genuinely conceptual proof (an explicit finite list of polynomial
  conditions cutting out exactly the extendable pairs). It is far out of reach computationally:
  the elimination is over the entries of three $6\times6$ matrices with unimodularity constraints.
  Worth recording as the *ideal form* of the answer, not as a plan.

**R7. Monodromy: local constancy of the completion count.** *Status: dead, by the following
proposition (swarm `smwgyflhh`, verified).* Let $X$ be the connected space of non-Tao Hadamard
classes, $\Sigma\subset X$ the classes admitting a third basis, $n(H)$ the number of third bases, and
suppose (H1) $\Sigma\ne X$ and (H2) $\Sigma$ has empty interior. Then **no proper closed
$\Delta\subsetneq X$ has $n$ locally constant on $X\setminus\Delta$.**

*Proof.* $X\setminus\Sigma$ is open and nonempty by (H1), and $n\equiv0$ there. If
$H\in\Sigma\setminus\Delta$, then $n(H)\ge1$ and local constancy gives $n\ge1$ on a neighbourhood,
which by (H2) meets $X\setminus\Sigma$ — contradiction. So $\Sigma\subseteq\Delta$. $\square$

Both hypotheses hold as consequences of the classification ($\Sigma$ is the image of a two-parameter
moduli space in the four-parameter $X$), so the one-fibre architecture is not an independent route:
**the discriminant must already contain the whole answer.** This is the precise form of the caveat I
had only gestured at ("the discriminant locus is exactly as hard to describe as $\Sigma$"), and it is
why the cover in R5 is not an artefact of method. The residual step is now stated exactly: prove
that $\Sigma$ lies in the image of the order-three-symmetric family — the one statement the 2,775
balls certify, and one that is vacuous on the dense open $X\setminus\Sigma$.

## 4. What I verified myself

Independent of the preprint and of R5's Lean development, using the definitions rather than the
printed formulas (`pdftotext` mangles exactly these expressions, so I recomputed them).

**(a) The four-phase invariants.** Take a corner $E(\theta)$, $G_h=6I-EE^\dagger$, and any
unimodular $B$ with $BB^\dagger=G_h$ (three phases of gauge freedom; fit by least squares to
$10^{-13}$). Put
$g=|\det B|^2$, $\eta=|\operatorname{perm}B|^2$, $\chi=-2\operatorname{Re}\Psi(B)$,
$p=X+Y+Z$, $J=2\operatorname{Re}(sr\bar t)$ with $s,t,r$ the off-diagonals of $G_h$ and
$X=|s|^2,Y=|t|^2,Z=|r|^2$. Over 70 random strict seeds:

| identity | max residual |
|---|---|
| $g = 27-3p+J$ | $4.6\times10^{-14}$ |
| $\eta = 9-p+J$ | $2.9\times10^{-14}$ |
| $\chi = (XY+YZ+ZX) - XYZ - (p-9)(p-18) + (p-15)J$ | $6.1\times10^{-13}$ |

So $g,\eta$ depend on the corner only through $p,J$, and $\chi$ through the elementary symmetric
functions of $X,Y,Z$ as well: the four-phase reduction is real, and it is an *algebraic* statement
about $3\times3$ blocks, not an analytic accident.

The maximum of $R$ over the corner torus is attained (600 restarts) at
$\cos\theta=(17/32,\,-7/8,\,-7/8,\,1/4)$ — note the $\arccos(1/4)$ of their Fig. 2 — where
$$g=\frac{3^5}{2^4},\qquad \eta=\frac{3^2\cdot13}{2^4},\qquad \chi=-\frac{3^6\cdot7}{2^6},\qquad
4g^2\eta-\chi^2=\frac{3^{12}(52-49)}{2^{12}}=\frac{3^{13}}{2^{12}}=389.239013671875,$$
confirming the published $R_{\max}=3^{13}/2^{12}$ and, with it, my reading of the invariant.
(An intermediate run of mine gave $9478$; that was my own wrong $\chi$, off by the sign of $XYZ$.
Worth recording because it is the exact failure mode a reader will hit.)

**(b) The dimension of the triple variety.** Using the explicit JMSSW triple family
$\{I,\ F(0,b(t))/\sqrt6,\ C(t)/\sqrt6\}$ (reproduced to $4\times10^{-41}$ at $t=0.6,0.9,1.1$, so
$N(6)\ge3$ is concrete), I linearised all $96$ real conditions — $30$ for $H$ Hadamard, $30$ for $K$,
$36$ for $|(H^*K)_{ij}|^2=6$ — with respect to the $72$ entry phases at $t=0.9$. The Jacobian has
rank $53$, so the solution variety through that point is $19$-dimensional. The rephasing group
$U(1)^6_r\times U(1)^6_c\times U(1)^6_{c'}$ has rank $17$ (18 generators, one relation: the global
phase), every one of its directions lies in the kernel ($\max|JV|=5\times10^{-8}$, finite-difference
noise), and $19-17=2$.

So **the MUB triples in $\mathbb{C}^6$ form a two-parameter family, and I have the dimension count
locally as well as from the literature.** This is the single most important number in this note: the
object a proof must kill is a $2$-dimensional moduli space sitting inside a $4$-dimensional space of
pairs, not a finite list of configurations. It is why a purely combinatorial argument cannot be
complete (2(b)) and why the only known complete arguments must either classify that surface (R5) or
describe it exactly (R6).

## 5. The reduced problem

Everything above compresses to one statement, which I would put to anyone claiming a conceptual
proof:

> **Describe $\Sigma\subset T^4$ exactly.** $\Sigma$ is the set of corner data of pairs
> $(I,H)$ that admit a third basis. It is closed, semialgebraic, of real dimension 2, and contains
> the two-parameter family of Matolcsi–Matszangosz–Varga–Weiner. Prove that it *equals* that
> family.

Given such a description, $N(6)=3$ follows from Jaming et al.'s symbolic non-extendability of the
family (no covering, no floating point). Without it, every route known to me either restates the
problem (R2, R3) or must cover a 4-dimensional space (R5) or fails outright (R1, R4).

## 6. Verdict

* A pencil-and-paper proof of $N(6)=3$ does not exist, and 2(a)–(c) say why: the object is a
  continuous moduli problem with no arithmetic rigidity, no forced discrete design, and no
  positivity gap at the critical parameter. That is a structural obstruction, not a gap in effort.
* The most conceptual proof available is R5: 25 phases $\to$ 4 phases, connectedness instead of
  bins, and a classification of *all* triples rather than an exclusion of quartets. It still ends
  in 2,775 certified balls, but each is a local statement about a 4-dimensional chart, and the
  global statement is a classification theorem.
* The one genuinely open conceptual target is $\Sigma$ (Section 5). The monodromy technique that
  looked like the way to reach it (R7) is now *proved* unable to help as an independent route: the
  discriminant must contain $\Sigma$. So there is at present no candidate technique at all, and that
  is the honest bottom line: the mathematics stops being conceptual exactly at the classification of
  a two-dimensional transcendental surface, and every route proposed to avoid that classification has
  been closed.

## 7. Swarm verdicts (swarm `smwgv618l`, 8 members, `deepseek-v4.1-flash`)

Six of the eight directions were accepted, on the standard "checked it myself" rule. Two were
rejected (one antiunitary note that constrained the symmetry of a quartet rather than its existence,
and one MVW-cube verification that only covered the families the identity was designed to
characterise), and two of the six were accepted only on resubmission after their first versions
overclaimed. What each accepted direction established:

| direction | accepted result | my check |
|---|---|---|
| group-covariance | There is exactly one index-1 nice error basis in dimension 6 ($G\cong Z_6^2$); its 12 maximal isotropics are the $3\times4$ CRT grid; the largest unbiased family is $\min(N(2),N(3))=3$, attained by the tensor triple. | Built the tensor triple ($3.9\times10^{-16}$); the natural fourth candidate has overlaps of modulus$^2$ $1/3$. |
| design / nets | No $(6,k,1)$-difference matrix for any $k\ge3$ over either group of order 6; no dimension-uniform design implication ($d=21$ is a counterexample). | $S_3$ case exhaustive over $720^2$ pairs; $Z_6$ sum argument ($15\equiv3$); $21\ne a^2+b^2$. |
| Lie / Galois | $Z_4^2$ has 7 order-4 subgroups (6 cyclic plus the torsion $\{0,2\}^2$), max 3; $F_4^2$ has 35, max spread 5 $=15/3$. MUB-ness does not imply Galois type at $m\le3$. | Re-ran both counts; both correct. |
| Lie / Cartan | The Cartan restatement is an equivalence only with adjoint-closedness. Four pairwise Killing-orthogonal Cartan subalgebras of $\mathfrak{sl}_6$ exist whose bases are not unbiased — so Lie theory alone cannot prove the theorem. | Rebuilt all four subalgebras: abelian, 5-dimensional, traceless, distinct, cross pairings $\le5.4\times10^{-16}$, self-pairings 2, polar bases off by $0.19$–$0.31$. |
| product-type | $r\le3$ for pairwise-unbiased product-type bases of $\mathbb{C}^2\otimes\mathbb{C}^n$ — the *grid* hypothesis is removable. | Ran their verifier: the twisted triple is exactly MUB and its third basis is provably not a grid. |
| variational | Modulus-level relaxations are blind for every $m$ ($Q_m\succeq0$ always); the Gram-level PSD problem has **no relaxation gap** (rank is forced to be exactly $d$, all nonzero eigenvalues $=m$); $E_m-\binom m2=\sum\|Y_{ij}-J_d/d\|_F^2\ge0$. | Identity to $10^{-16}$; rank 6, $\operatorname{tr}G^2=96$, all nonzero eigenvalues 4. |

Rejected, and why, because the reasons matter more than the verdicts:

* A "meta-theorem" that restriction-then-exclusion can never reduce the problem. It is a tautology:
  given the rest of a proof, the key lemma is always equivalent to the theorem. Accepted on
  resubmission once the tautology was removed and it said instead that MUB-ness does not imply Galois
  type at $m\le3$, so the route needs a new rigidity theorem with no lower-dimensional analogue.
* A verification of the Matolcsi–Matszangosz–Varga–Weiner cube identity on the Fourier and Weyl
  families. Correct and careful work, but those are exactly the families the identity is designed to
  characterise, so it neither proves nor refutes the conjecture. Its useful residue: the identity
  is *not* vacuous (generic Hadamards give $\max_I|S_I|=3$), and a numerical trap ($\gamma_2$ sums are
  cubes and look violated by $10^3$ at residual $10^{-8}$).
* A product-type ceiling that overclaimed: "not all four bases product-type" does not give "no
  product vector in any of them". Its Theorem A is nevertheless a genuine strengthening of the grid
  version (a product-type basis need not be a grid), so the fix is small.

The swarm was stopped once all eight directions had reported; further member time would not have
changed any of the conclusions above.

## 8. A correction, and what it changes

An earlier reading of mine — that the reconstruction's strict-seed condition $R>0$ *excludes*
extendability, so that $N(6)=3$ would follow from a single lemma "strict seeds admit no third basis" —
is **wrong**, and I verified the refutation rather than assume it.

* $R$ is a genuine corner invariant: for $F(0,0.3)$ the corner formula gives
  $R=12.4376941013$, and the definitional value $4(\operatorname{Im}\Psi)^2$ computed from the actual
  corner block $B$ agrees to all printed digits, with $g=3$, $\eta=1$ in both routes. So the formula
  and my implementation are right. ($F_6$ gives $R=0$ on all $400$ of its $3+3$ corners, confirming
  the paper's "every corner" claim.)
* Consequently $F(0,0.3)$ is **not** equivalent to $F_6$. Jaming–Matolcsi–Móra–Szöllősi–Weiner's
  $F(a,b)$ is a two-parameter family of pairwise *inequivalent* Hadamards, not the gauge orbit of
  $F_6$ (which is what I had assumed, and which would have made their "infinite family of triplets"
  a family of equivalent triples).
* Decisively: for the *extendable* pairs $(I, F(0,b(t)))$ of that family, the second matrix has
  $R = 14.97,\ 5.71,\ 35.82$ at its natural corner ($t=0.6,0.9,1.1$), and $R>0$ on $144$ of $400$
  corners. So extendable pairs **do** have strict corners.

Hence the true shape of the proof is a **classification**, not an exclusion: cover the pair space,
and in each ball show that every triple through a pair in the ball is *equivalent to a known triple*
(two-parameter family, or isolated Fourier triple), after which those are known not to extend. There
is no shortcut lemma of the form "strict seed $\Rightarrow$ no triple", and the residual difficulty
is exactly the classification. This strengthens rather than weakens §2's diagnosis: the problem is
irreducibly a codimension-two phenomenon inside a generic locus.

Two by-products worth keeping. The extendable locus is two-parameter *because* the Fourier-type
family is two-parameter — that is the conceptual source of the $19-17=2$ count. And neither the
JMSSW second basis nor its third basis is Fourier-type (each has $R>0$ on $144/400$ corners), so
both sides of a triple are genuinely non-Fourier; there is no asymmetry to exploit.

## 9. Progress from the second run (`smwgyflhh`): the extendable locus made explicit

Four members, four accepted. This run did not produce the proof, but it moved the *statement* of the
residue from "describe $\Sigma$" to two equations, and it closed three more mechanisms.

**The explicit description.** The dephased corner of the JMSSW family is
$$E=\begin{pmatrix}1&1&1\\1&e^{i\pi/3}x&\omega\\1&\omega y&\omega^2\end{pmatrix},\quad
x=e^{2\pi ia},\ y=e^{2\pi ib},\ \omega=e^{2\pi i/3},$$
and I verified at four parameter values that $(\theta_1,\theta_2,\theta_3,\theta_4)=(\frac\pi3+2\pi a,
\frac{2\pi}3,\frac{2\pi}3+2\pi b,\frac{4\pi}3)$ to $10^{-15}$. So **two of the four corner phases are
pinned at cube roots of unity** across the whole family, and

$$\Sigma\ \supseteq\ T_0=\{\theta_2=2\pi/3,\ \theta_4=4\pi/3\},\qquad\text{i.e.}\quad E_{23}=\omega,\ E_{33}=\omega^2 .$$

Conjecture (the residue, now in closed form): $\Sigma$ is the symmetry orbit of $T_0$ and nothing else.
Given it, $N(6)=3$ follows from Jaming–Matolcsi–Móra–Szöllősi–Weiner, symbolically in $(a,b)$.

**One direction is now provable.** In the four-dimensional pair space local constancy of the
completion count fails (R7), because $\Sigma$ has empty interior there. On $T_0$ the dimensions match
($\dim T_0=2=\dim\Sigma$), the completions are isolated, the solution set is closed, and the implicit
function theorem makes each non-degenerate completion persist. Hence one extendable point plus
transversality at that point gives $T_0\subseteq\Sigma$ on all of $T_0$. The $\supseteq$ half is a
finite rank check; only $\Sigma\subseteq T_0$ remains.

**Three more mechanisms closed, and one methodological warning.**
* *Monodromy.* R7 is dead (Section 3): the discriminant must already contain $\Sigma$.
* *Galois, one level below Hadamards.* Of the 48 perfect (CAZAC) lines of length 6, only one 12-element
  orbit has root-of-unity entries; the other 36 have algebraic non-root-of-unity entries, e.g.
  $2\cos\theta=\sqrt3-1$ (checked: $z$ is not a root of unity, $\min_{n\le60}|z^n-1|=0.015$). So no
  root-of-unity argument survives even for a single column of a biflat unitary.
* *Covariance, inside the Fourier chart.* Only 2 of the 16 third bases of $\{I,F_6\}$ are
  group-covariant, so the "one error basis, cap $\min(N(2),N(3))=3$" argument sees 2 of the 16 objects
  it would have to exclude.
* *Warning.* Random-start optimisation is worthless as negative evidence here: at a point that
  provably has completions, 80 random multi-starts find nothing (residuals $0.7$–$1.2$), and their own
  verifier undercounts at 9 of 36 grid points. **"We searched and found no fourth basis" carries almost
  no evidential weight in this problem.** Margin arguments (a certified gap of $0.36$ in
  $\sum_{ij}|\langle u_i,v_j\rangle|^4\ge1$) survive; searches do not.

**State of the residue.** Prove: if $H=AB$ is a product of two flat unitaries, then in its dephased
corner $\theta_2=\omega$ and $\theta_4=\omega^2$. A two-equation rigidity on a four-torus, with the
three-like structure of $6$ as the only visible mechanism.
