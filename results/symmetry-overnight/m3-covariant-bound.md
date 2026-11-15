# The Heisenberg-covariant slice of the C^6 MUB problem: exactly three bases

Member `m3` (swarm `smwhnslql`), direction `d6`. All statements below are either
proved in this file or certified by the exact computations in `m3-scripts/`
(integer arithmetic in $Z[\zeta_{24}] = Z[x]/(x^8-x^4+1)$, no floating point).

**Literature status.** The *conclusion* "no four MUBs of C^6 that are related to the
Heisenberg-Weyl group exist" is known: Grassl (arXiv:quant-ph/0406175, v2 2009) shows
that certain triples in dimension six are maximal, and Brierley-Weigert
(arXiv:0901.4051, PRA 79, 052316) confirm computationally that a prescribed Hadamard
matrix admits at most two more. What is new here is only the self-contained proof and
the exact certificates; no priority is claimed. (Literature audit: member `m2`, `d5`.)

---

## 1. Conventions

Let $\omega = e^{2\pi i/6}$ and identify $\mathbb C^6$ with $\ell^2(\mathbb Z_6)$ with
standard basis $e_0,\dots,e_5$. Define the clock and shift unitaries

$$Z e_j = \omega^{j} e_j, \qquad X e_j = e_{j+1 \ (\mathrm{mod}\,6)}, \qquad ZX = \omega XZ .$$

The Weyl-Heisenberg group is
$H = H(\mathbb Z_6) = \{\, \omega^{\theta} X^a Z^b \;:\; \theta,a,b \in \mathbb Z_6 \,\}$,
$|H| = 216$, with centre $Z(H) = \{\omega^\theta I\} \cong \mathbb Z_6$, so
$H/Z(H) \cong \mathbb Z_6^2$. Writing a group element as $(\theta,a,b)$, the law and the
commutator are

$$(\theta,a,b)(\theta',a',b') = (\theta+\theta'+a'b,\; a+a',\; b+b'), \qquad
[(a,b),(c,d)] = \omega^{\,bc-ad}.$$

The commutator is a scalar, so the alternating form
$\langle (a,b),(c,d)\rangle = bc-ad \in \mathbb Z_6$ is well defined on $H/Z(H)$.
For an abelian subgroup $M \le H$ put $\pi(M) \subseteq \mathbb Z_6^2$ for its image.

**Definition.** A *stabiliser basis* of $\mathbb C^6$ is an orthonormal basis whose rays
are the common eigenspaces of a maximal abelian subgroup $M \le H$. (This is the class
in which the standard Heisenberg construction of $d+1$ MUBs in prime-power dimensions
lives: there the bases are the eigenbases of the "lines" of $\mathbb Z_d^2$.)

The question treated here is: **how many pairwise unbiased stabiliser bases can
$\mathbb C^6$ have?**

---

## 2. The maximal abelian subgroups of $H(\mathbb Z_6)$

**Lemma 1.** (i) Every abelian $M \le H$ satisfies $|M| = |M\cap Z(H)|\cdot|\pi(M)|$,
hence $|M| \le 6\,|\pi(M)|$; in particular $|M| = 6\,|\pi(M)|$ as soon as $M$ is
maximal abelian.
(ii) $\pi(M)$ is isotropic, and every isotropic subgroup of $\mathbb Z_6^2$ has order
$\le 6$.
(iii) A maximal abelian subgroup has order $36$, and $M \mapsto \pi(M)$ is a bijection
between maximal abelian subgroups of $H$ and isotropic subgroups of $\mathbb Z_6^2$ of
order $6$.

*Proof.* (i) $\ker\pi = Z(H)$, so $|M| = |M\cap Z(H)|\cdot|\pi(M)|$; if $M$ is abelian
then $Z(H)M$ is abelian, so maximality forces $Z(H) \subseteq M$ and $|M| = 6|\pi(M)|$.
(ii) Commutators inside $M$ are trivial, so $\langle u,v\rangle = 0$ for $u,v\in\pi(M)$.
By the Chinese remainder theorem $\mathbb Z_6^2 \cong \mathbb Z_2^2\times\mathbb Z_3^2$
and every subgroup is a product $H_2\times H_3$ of subgroups of the two factors; the
form, and hence isotropy, splits accordingly. On $\mathbb Z_p^2$ ($p$ prime) with a
nondegenerate alternating form, an isotropic subgroup has order $\le p$: the only
subgroup of order $p^2$ is everything, and it is not isotropic. Hence
$|\pi(M)| \le 2\cdot 3 = 6$.
(iii) From (i), (ii), $|M| \le 36$. Let $M$ be maximal abelian and suppose $\pi(M)$ were
properly contained in a larger isotropic subgroup $S \le \mathbb Z_6^2$. Then
$\pi^{-1}(S) \supsetneq M$ is abelian - its elements have classes in the isotropic $S$,
which pairwise commute, and $\ker\pi = Z(H)$ is central - contradicting the maximality of
$M$. Hence $\pi(M)$ is *maximal* isotropic; by (ii) together with the CRT splitting of
Lemma 2 every maximal isotropic subgroup of $\mathbb Z_6^2$ has order $2\cdot 3 = 6$, so
$|M| = 36$ and $M = \pi^{-1}(\pi(M))$ (an element whose class lies in $\pi(M)$ commutes
with everything in $M$). Conversely, for isotropic $S$ of order $6$ the preimage
$\pi^{-1}(S)$ is abelian of order $36$, hence maximal. $\square$

**Lemma 2 (CRT structure).** Under $\mathbb Z_6^2\cong\mathbb Z_2^2\times\mathbb Z_3^2$,
isotropic subgroups of order $6$ correspond to pairs $(L_2,L_3)$ with $L_p$ a line
(a subgroup of order $p$) in $\mathbb Z_p^2$; every line in $\mathbb Z_p^2$ is isotropic.
Hence there are exactly
$$|\mathbb P^1(\mathbb Z_2)| \cdot |\mathbb P^1(\mathbb Z_3)| = 3\cdot 4 = 12$$
maximal abelian subgroups. For two of them, with invariants $(L_2,L_3)$ and
$(L_2',L_3')$,
$$M\cap M' = Z(H) \iff L_2 \ne L_2' \text{ and } L_3 \ne L_3' .$$

*Proof.* A subgroup of order $6 = 2\cdot3$ of a product $\prod_p\mathbb Z_p^{2}$ is the
product of its $p$-parts, which have orders $2$ and $3$. Distinct lines in
$\mathbb Z_p^2$ meet only in $0$. Since $M\cap M' = \pi^{-1}(\pi(M)\cap\pi(M'))$, the
intersection is $Z(H)$ exactly when $\pi(M)\cap\pi(M') = \{0\}$, i.e. when both
components differ. $\square$

*Computation* (`m3-scripts/wh2.py`, `m3-scripts/latin.py`): $H$ has exactly $12$ abelian
subgroups of order $36$ (brute-force enumeration over $\mathbb Z_6^2$: $30$ subgroups,
$20$ isotropic, $12$ maximal isotropic of order $6$); the four-factor table of Lemma 2
and the criterion of the last display were checked on all $66$ ordered pairs, with no
mismatch.

---

## 3. Unbiased stabiliser bases have disjoint stabilisers

**Lemma 3.** Let $B, B'$ be stabiliser bases with stabilisers $M, M'$. If
$|\langle u,v\rangle|^2 = 1/6$ for all $u \in B$, $v\in B'$, then
$M \cap M' = Z(H)$.

*Proof.* The $6$-dimensional representation $\rho$ of $H$ is irreducible; restricted to an
abelian subgroup it splits into weight spaces, and only characters with $\chi(\omega I) =
\omega$ occur. There are exactly $|M/Z(H)| = 6$ such characters of $M$, so at most six
occur. **The occurring ones form a single $H$-orbit**: $H$ acts by
$(g\cdot\chi)(h) = \chi(g^{-1}hg)$, and the stabiliser of an occurring $\chi$ is
$\{g : \chi([M,g]) = 1\} = C_H(M) = M$, because $[M,g]\subseteq Z(H)$ and
$\chi|_{Z(H)}$ is injective ($Z(H)\cong\mathbb Z_6$ acts by $\chi(\omega^tI) = \omega^t$).
Hence each occurring character has orbit size $|H|/|M| = 216/36 = 6$, so *all six* occur;
each weight space has dimension $\ge 1$, and $\sum_\chi \dim V_\chi = 6$, so every
weight space is one-dimensional. The weight vectors are exactly the rays of $B$. (For all
twelve subgroups in $d=6$ this is also verified directly - each computed ray is a
simultaneous eigenvector of all $36$ elements and the six characters are distinct,
`m3-scripts/verify_joint.py` - but the argument above does not depend on that
computation.) Same for $M'$, whose weight vectors $v_\psi$ are indexed by the $6$
characters $\psi$ of $M'/Z(H)$.

Let $u \in B$ be the weight vector of the character $\chi$, so $hu = \chi(h) u$ for
$h \in M$. Unbiasedness writes
$u = \sum_\psi c_\psi v_\psi$ with $|c_\psi|^2 = 1/6 \ne 0$ for every $\psi$. Suppose
$h \in M\cap M'$ acts on $v_\psi$ by $\psi(h)$. Then
$$\sum_\psi \psi(h) c_\psi v_\psi = h u = \chi(h) u = \sum_\psi \chi(h) c_\psi v_\psi,$$
so $\psi(h) = \chi(h)$ for all six characters $\psi$ of $M'/Z(H)$. Characters of a finite
abelian group separate points of the quotient, hence $h \in Z(H)$. $\square$

*Remark.* Lemma 3 is the only place where unbiasedness enters. It is the
"trivial-intersection criterion" of the stabiliser formalism, proved here rather than
cited. The converse (trivial intersection $\Rightarrow$ unbiased) also holds and was
verified exactly for all $66$ pairs in $d=6$ (`m3-scripts/cov.py`); it is not needed
below.

---

## 4. Main theorem

**Theorem.** Let $B_1,\dots,B_k$ be pairwise unbiased stabiliser bases of $\mathbb C^6$.
Then $k \le 3$. The bound is attained.

*Proof.* Let $M_i$ be the stabiliser of $B_i$ and $(L_{i,2},L_{i,3})$ its invariants from
Lemma 2. By Lemma 3, $M_i\cap M_j = Z(H)$ for $i\ne j$, so by Lemma 2
$L_{i,2}\ne L_{j,2}$ and $L_{i,3}\ne L_{j,3}$ whenever $i \ne j$. Thus
$i \mapsto (L_{i,2},L_{i,3})$ injects into
$\mathbb P^1(\mathbb Z_2)\times\mathbb P^1(\mathbb Z_3)$ with all first coordinates
distinct and all second coordinates distinct - a partial Latin square in a $3\times 4$
array. Hence $k \le \min(3,4) = 3$. $\square$

**Existence (exact certificate).** The following three bases are pairwise unbiased:

* $B_\infty$: the standard basis (stabiliser: the subgroup $\{\omega^\theta Z^b\}$);
* $B_0$: the eigenbasis of $X$ (the Fourier basis), entries $\zeta_{24}^{-4ij}/\sqrt 6$;
* $B_1$: the eigenbasis of $XZ$, whose exponent matrix
  $(z_{ij})$ with entries $\zeta_{24}^{z_{ij}}/\sqrt 6$ is
  $$\begin{pmatrix}
  0&0&0&0&0&0\\
  22&18&14&10&6&2\\
  0&16&8&0&16&8\\
  6&18&6&18&6&18\\
  16&0&8&16&0&8\\
  6&10&14&18&22&2
  \end{pmatrix}.$$

Verification (`m3-scripts/cov.py`): all $3\cdot 36$ inner products between different
bases have modulus exactly $1/\sqrt 6$ and all $3\cdot 6$ vectors have norm $1$, checked
in $Z[\zeta_{24}]$ by reduction to integer vectors. The stabilisers of $B_\infty,B_0,B_1$
are the lines of slopes $\infty,0,1$, which pairwise differ in both CRT coordinates.
$\square$

**Corollary 1.** There are exactly $24$ pairwise unbiased triples of stabiliser bases;
they are the partial Latin squares using three of the four $\mathbb P^1(\mathbb Z_3)$
lines. All $24$ are carried to one another by $SL(2,\mathbb Z_6) = Sp(2,\mathbb Z_6)$
(order $144$), acting on the $12$ lines and on the $24$ triples transitively
(`m3-scripts/clifford.py`). So there is, up to Clifford equivalence, a unique
Heisenberg-covariant MUB triple in $\mathbb C^6$.

*Why $SL$ and not $GL$:* $SL(2,\mathbb Z_6)$ is exactly the stabiliser of the commutator
form $\langle (a,b),(c,d)\rangle = bc-ad$, i.e. $A^{T}JA = J$; this is the part of
$GL(2,\mathbb Z_6)$ that lifts to unitaries preserving the central character (Weil
representation). A matrix with $\det \ne 1$ scales the commutator form and has no such
lift, so it must not be used for equivalence of MUB configurations. (Restricting to
$\det = 1$ costs nothing: transitivity on the 12 lines and on the 24 triples holds for
$SL$, as the script shows.)

---

## 5. What this says about the symmetry route

For a MUB triple $(A,B,C)$ let $\Delta_A,\Delta_B,\Delta_C$ be the orders of the groups of
diagonal unitaries fixing one basis and preserving the other two as ray sets, modulo
global phase.

**Corollary 2 (exact computation).** Every Heisenberg-covariant triple in $\mathbb C^6$
whose three bases are flat with respect to a common basis has
$(\Delta_A,\Delta_B,\Delta_C) = (6,6,6)$, and at every anchor the source's relation
lattice has Smith normal form $\mathrm{diag}(1,1,1,1,6)$ and $\mathbb F_3$-rank $4$.

Checks (`m3-scripts/delta3.py`, `m3-scripts/index3.py`, `m3-scripts/rank3.py`): for the
six covariant triples whose three bases are flat with respect to a common basis (the
other $18$ covariant triples contain a non-flat base; see §7), the diagonal symmetry
group was computed from its definition (all $6!$ column permutations and exact
proportionality tests over $Z[\zeta_{24}]$) at all three anchors, giving $6$ each time;
independently the support lattice index $[\Lambda_0:L_X]$ of the source's formula (5) was
computed from the exact support of $P_X$, giving $6$ at all $18$ anchor instances, with
Smith form $\mathrm{diag}(1,1,1,1,6)$. Consequently $\mathrm{rank}_{\mathbb F_3}R_X = 4 <
5$ and the source's detector satisfies $\Xi(P_X) = 0$ at all three anchors.

Three consequences for the overnight programme.

1. *The identity $\Xi(P_A)\Xi(P_B)\Xi(P_C)=0$ is not tested by the six flat covariant
   triples*: there all three factors vanish. Any test of the identity needs a triple in which at least
   one anchor has no clock ($\Delta_X \in \{1,2\}$). Member `m5` (`d2`) produces such
   triples with patterns $(2,3,3)$ and $(6,6,6)$.
2. *The source's table row "standard product triple: $\Delta = 6$" is confirmed*, and its
   formula (5) "$\Delta_A = [\Lambda_0:L_A]$" holds at every anchor of the covariant
   triples. In general that formula needs three ingredients: diagonal unitaries
   commuting with $P_A$ are exactly the characters of $\Lambda_0/L_A$; the recovery lemma
   turns them into ray-set symmetries; and a **no-exchange lemma** is needed to rule out
   a symmetry that swaps the two bases (the source only sketches this). Member `m1`
   (`d1`, finding f15) supplies the missing proof: a swap forces $|\mathrm{tr}\,T|^2 = 6$,
   while projective orders $2,3,4$ give $|\mathrm{tr}\,T|^2 \in \mathbb Z$ even, $\ne 6$,
   or a two-square obstruction. With that, the group is cyclic of order in
   $\{1,2,3,6\}$ and $\Delta_A = [\Lambda_0:L_A]$, and $3 \mid \Delta_A$ iff
   $\mathrm{rank}_{\mathbb F_3}R_A < 5$.
3. *The "3" here is not the order-3 clock.* The three covariant bases are limited by
   $|\mathbb P^1(\mathbb Z_2)| = 3$, i.e. by the **qubit** factor of
   $\mathbb C^6=\mathbb C^2\otimes\mathbb C^3$, not by the qutrit factor. The covariant
   triple is maximally symmetric ($\Delta=6$ at every anchor), so symmetry does not
   obstruct it; what obstructs a fourth covariant basis is the scarcity of isotropic
   lines over the smaller prime. This is worth keeping separate from the source's
   narrative, in which the factor $3$ is produced by the order-two-to-order-three
   mechanism.

---

## 6. The same argument for squarefree $d$ (remark)

Nothing in Lemmas 1-3 uses $d=6$ except the numbers. For squarefree
$d = p_1\cdots p_r$ the identical argument gives: the maximal abelian subgroups of
$H(\mathbb Z_d)$ biject with $r$-tuples of lines in $\mathbb P^1(\mathbb Z_{p_i})$, two of
them intersect in the centre iff all coordinates differ, and hence

$$\#\{\text{pairwise unbiased stabiliser bases of } \mathbb C^d\} \;\le\; \min_i\,(p_i+1).$$

For $d=6$ this is $3$; for prime powers the count is $d+1$ (the classical Heisenberg
construction), so the bound is a composite-dimension phenomenon. This is presumably
folklore in the stabiliser-MUB literature; it is recorded here with proof, not claimed
as new.

---

## 7. What is *not* proved here

* This is a slice result. It says nothing about triples that are not stabiliser bases:
  $N(6)=3$ is untouched. In particular the 2-parameter family of triples in
  `results/order3-stratum.md` and the $(3,3,2)$ example of the source are **not**
  covariant, and no part of this note constrains a fourth basis for them.
* The six flat covariant triples were treated with exact exponent matrices; the remaining
  $18$ (those containing a "vertical" base that is not flat with respect to either of the
  other two) were not run through the $\Delta$-computation. They are pairwise unbiased by
  Lemma 3 and the criterion table, but Corollary 2 is asserted only for the flat six.
  Remark (not used above, and conditional on a cited standard fact): $\Delta$ is invariant
  under unitary conjugation of the whole triple, and Corollary 1 puts all $24$ triples in
  one $SL(2,\mathbb Z_6) = Sp(2,\mathbb Z_6)$ orbit, which lifts (projectively) to
  unitaries by the Weil representation of $Sp(2,\mathbb Z_d)$ - the standard metaplectic
  lift, cited here, not reproved. Modulo that lift the values $(6,6,6)$ would extend to
  all $24$; the statement of Corollary 2 is nevertheless kept to the six flat triples
  whose $\Delta$ was computed directly.
* No claim about publication priority. Grassl's and Brierley-Weigert's results already
  cover the conclusion.

---

## 8. Files

| file | content |
|---|---|
| `m3-scripts/zeta.py` | exact arithmetic in $Z[\zeta_{24}]$ |
| `m3-scripts/wh.py` | $H(\mathbb Z_6)$, matrices, group law |
| `m3-scripts/wh2.py` | enumeration of maximal abelian subgroups |
| `m3-scripts/cov.py` | eigenbases of all 12 subgroups; exact unbiasedness table |
| `m3-scripts/verify_joint.py` | the 6 rays really are simultaneous eigenvectors of $M$ |
| `m3-scripts/latin.py` | CRT invariants, trivial-intersection criterion, max subsets |
| `m3-scripts/delta.py`, `m3-scripts/delta3.py` | $\Delta$ from the definition; all anchors |
| `m3-scripts/index3.py` | support lattice index at all anchors (source formula (5)) |
| `m3-scripts/rank3.py` | $\mathbb F_3$ rank of $R_X$ (source detector $\Xi$) |
| `m3-scripts/clifford.py` | $SL(2,\mathbb Z_6)$ transitivity on lines and triples |
| `m3-scripts/numcheck.py` | independent floating-point check of the unbiasedness table |
| `m3-scripts/diag4.py` | associativity / sympy cross-check of the ring arithmetic |
| `m3-scripts/gen_delta.py` | independent (definition-based) Delta for m5's (2,3,3)/(6,6,6) family |
| `m3-scripts/census.py` | sample census of the Delta patterns in that family |
| `m3-scripts/xi_check.py` | $\mathbb F_3$ ranks (detector $\Xi$) at all anchors of those triples |

Reproduce with `cd m3-scripts && TMPDIR=../.scratch python3 cov.py` (etc.).

---

## 9. Cross-check of member m5's (2,3,3) family (independent method)

m5 (`d2`) reported that the source's section-4 "uniform case" realises genuine MUB
triples with $(\Delta_A,\Delta_B,\Delta_C) = (2,3,3)$, computed from Smith normal forms of
the support lattice. I rebuilt the family and recomputed $\Delta$ **from the definition**
(brute force over all $6!$ permutations, exact proportionality tests with field inverses
in $\mathbb Q(\zeta_{24})$, scripts `gen_delta.py`, `census.py`):

* $H = F D\Pi$ over $\mathbb Z[\zeta_{24}]$: 162 matrices, exactly **108** with
  $|HF|^2 = 3$, i.e. $HF$ flat - m5's classification step reproduced.
* $U = [[H_0,H_0],[H_1,-H_1]]$, $V = [[K_0,K_0],[K_1,-K_1]]$, $K_0 = H_0F$,
  $K_1 = iH_1F$: $(I,U,V)$ is a MUB triple, verified exactly (108 overlaps).
* $\Delta$-patterns over a sample of 10 pairs: only $(6,6,6)$ (7 times) and $(2,3,3)$
  (3 times) - the same two values, including $\Delta_A = 2$.
* the pattern is **not** a function of the permutations $(\Pi_0,\Pi_1)$ alone, so m5's
  "5832 + 5832" split is not explained by the permutation classes.
* source detector: for a $(2,3,3)$ instance, $\mathrm{rank}_{\mathbb F_3} = 5$ at the
  $\Delta = 2$ anchor ($\Xi > 0$, 360 nonzero $P$ entries) and $=4$ at the two
  $\Delta = 3$ anchors ($\Xi = 0$, 276 entries); for a $(6,6,6)$ instance rank $4$
  everywhere (180 entries).

So every triple examined in this run (covariant, $(6,6,6)$, $(2,3,3)$) has at least one
anchor with a clock, and the identity $\Xi_A\Xi_B\Xi_C=0$ is satisfied trivially. A
genuine test requires all three $\Delta_X \in \{1,2\}$.

**Caveat on this cross-check.** My first version of the rank-one test used a mis-signed
cross-multiplication and returned $\Delta = 0$ for every triple; the correct test is
$X_{i\sigma(j)}X_{i'\sigma(j')}X_{ij'}X_{i'j} =
X_{i\sigma(j')}X_{i'\sigma(j)}X_{ij}X_{i'j'}$. The bug is logged in `m3-log.md`; the
numbers above are from the corrected code, and they agree with m5's independently
obtained values, which is what makes the agreement meaningful.
