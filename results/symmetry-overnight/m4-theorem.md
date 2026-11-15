# The triple product identity is a *density* statement for a closed set of triples

Member m4, direction 3. Status of each item is labelled. **Correction notice.** An earlier version of
this file claimed that $\{3\mid\Delta_X\}$ being closed makes $Z=\{3\mid\Delta_A\}\cup\{3\mid\Delta_B\}
\cup\{3\mid\Delta_C\}$ *clopen*, and derived a "one symmetric triple per connected component" criterion.
That inference is **wrong**: closedness of $Z$ does not give openness of $Z$. Upper semicontinuity of
$\Delta_X$ says symmetry may *appear* in a limit — it is not local constancy. In particular, the
individual sets $S_X$ need not be open (at the centre of the two-parameter family $\Delta$ jumps from
$(3,3,2)$ to $(3,1,1)$ under perturbation; see `m4-tables.md` and m2's census).
Everything that depended on clopenness is withdrawn; what follows is the correct form of the argument.

## 0. Notation

A *triple* is $x=(A,B,C)$, three pairwise mutually unbiased orthonormal bases of $\mathbb C^6$; the set
$\mathcal T\subset U(6)^3$ of triples is closed in the compact $U(6)^3$, hence compact. For an anchor
$X\in\{A,B,C\}$,
$$G_X(x)=\{[T]:\ T\ \text{diagonal in the $X$ coordinates, unitary, modulo scalars},\ T\mathcal B=\mathcal B,\ T\mathcal C=\mathcal C\},$$
where $\mathcal B,\mathcal C$ are the (unordered) ray sets of the other two bases; $\Delta_X(x)=|G_X(x)|$.
Write
$$S_X=\{x\in\mathcal T:\ 3\mid\Delta_X(x)\},\qquad Z=S_A\cup S_B\cup S_C,\qquad O=\mathcal T\setminus Z .$$
The source's identity is
$$\Xi(P_A)\Xi(P_B)\Xi(P_C)=0\quad\text{for every triple},\tag{13}$$
which, given the source's equivalence "$3\mid\Delta_X\iff\Xi(P_X)=0$" (§5 eq. (12) there), is exactly
$$(13')\qquad \forall x\in\mathcal T\ \exists X:\ 3\mid\Delta_X(x)\iff Z=\mathcal T .$$

## 1. Proposition 1 ($\Delta_X\in\{1,2,3,6\}$) — proved

$G_X(x)$ is a finite abelian group with $|G_X(x)|\mid 6$.

*Proof.* (i) *Finiteness.* $G_X$ is closed in the compact torus $\mathcal K_X=(S^1)^6/S^1$. Its identity
component acts continuously on the finite set of rays of $\mathcal B$, hence trivially; and if $Tb_r
\propto b_r$ then $t_i(b_r)_i=\mu(b_r)_i$ for all $i$, where $(b_r)_i\ne0$ because a vector unbiased to
a basis has no zero coordinate, so $t_i=\mu$ for all $i$ and $[T]=1$. Hence $G_X^0=\{1\}$, $G_X$ is
discrete, hence finite. (ii) The same computation shows a non-trivial $[T]\in G_X$ fixes no ray of
$\mathcal B$, so all orbits on the six rays have size $|G_X|$ and $|G_X|\mid6$. (iii) $G_X$ lies in the
abelian $\mathcal K_X$, so it is a finite abelian group of order dividing $6$, hence cyclic. $\square$

Consequently $3\mid\Delta_X(x)$ $\iff$ $G_X(x)$ contains an element of order $3$.

## 2. Proposition 2 ($S_X$ is closed) — proved

$S_X$ is closed in $\mathcal T$; hence $Z$ is closed and $O$ is **open**.

*Proof.* Let $\mathcal K_3=\{T\in(S^1)^6/S^1:T^3=1\}$, a finite set of $3^5=243$ elements. Put
$$\mathcal Z_X=\{(x,[T])\in\mathcal T\times\mathcal K_3:\ |\langle Tb_r(x),b_s(x)\rangle|=1
\ \text{for every } r \text{ and some } s,\ \text{and the same for } c_r(x)\}.$$
Each condition $|\langle Tb_r,b_s\rangle|=1$ is closed in $\mathcal T\times\mathcal K_3$ (equality in a
continuous modulus bounded above by $1$), and the disjunction over the six $s$ is a finite union of
closed sets; so $\mathcal Z_X$ is closed, hence compact. Its projection to $\mathcal T$ has fibre
$G_X(x)\cap\mathcal K_3$ over $x$. If $3\nmid\Delta_X(x)$ then that fibre is $\{1\}$; for each of the
finitely many $[T]\in\mathcal K_3\setminus\{1\}$ the point $(x,[T])$ lies outside the closed set
$\mathcal Z_X$, so there are open $U_T\ni x$, $V_T\ni[T]$ with $(U_T\times V_T)\cap\mathcal Z_X=\varnothing$;
then $U=\bigcap_TU_T$ is a neighbourhood of $x$ on which the fibre is $\{1\}$. Hence
$\{3\nmid\Delta_X\}$ is open and $S_X$ is closed. $\square$

*(Remark, and this is the whole subtlety: this is upper semicontinuity of $\Delta_X$, not local
constancy. $\Delta_X$ can drop in a limit; what cannot happen is that it rises without a limit point.)*

## 3. Theorem A (corrected) — proved

**(a)** $Z$ is closed, $O$ is open, $\mathcal T=Z\sqcup O$.

**(b)** The following are equivalent:
$$(13')\quad\Longleftrightarrow\quad O=\varnothing\quad\Longleftrightarrow\quad Z=\mathcal T
\quad\Longleftrightarrow\quad Z\ \text{is dense in}\ \mathcal T .$$
(The last equivalence uses that $Z$ is closed in the compact space $\mathcal T$.)

**(c) Density criterion — the correct "reduction".** If $Z$ contains a dense subset of $\mathcal T$, then
(13′) holds. In particular it suffices to prove $3\mid\Delta_X$ at *some* anchor for every triple
outside a closed, nowhere-dense exceptional set: the exceptional triples then need no separate analysis.
This is the source's own §7 remark ("an analytic proof on a subset dense in the entire space of exact
triples would automatically cover its limiting singular points"), stated in its correct form. A proof
that covers only a *non-dense* set (for instance a one-parameter family inside a two-dimensional moduli
space, or a single component of a reducible $\mathcal T$) does not suffice.

**(d) What failure looks like.** If (13′) fails, then $O\ne\varnothing$ is a **nonempty open** subset of
$\mathcal T$: every counterexample has a neighbourhood of counterexamples, i.e. all three integers stay
coprime to $3$ under small perturbation of every entry. Since a nonempty open subset of a real-analytic
set contains a smooth point of the maximal local dimension, $O$ then has positive measure with respect to
the volume of the corresponding stratum of $\mathcal T$.

**(e) What failure does *not* look like, and what is withdrawn.** $O$ need *not* be a union of connected
components, so a counterexample does not "occupy its component"; one component may contain both symmetric
and asymmetric triples. Consequently:
- "one symmetric triple per connected component" is **not** a valid criterion (withdrawn);
- "each component touches a known symmetric type" is **not** a valid criterion (withdrawn);
- a counterexample can be a single **rigid** triple, an isolated point of $\mathcal T$ (then $\{x\}$ is
  open, so (d) says nothing new); such points are decided by one exact computation, which is what the
  Fourier-chart computations in `m4-tables.md` do for the known isolated chart;
- nothing here says $\Delta_X$ is locally constant, and it is not (see the family centre).

## 4. Consequences, with their exact scope

1. **Closedness alone yields only:** a proof on a dense subset suffices; a counterexample is stable under
   perturbation; the failure locus is open. That is all. It is *not* an impossibility proof for any
   algebraic route, and it does not show that (13′) "is not an algebraic identity": the equivalence
   (13′) ⟺ "$Z$ is dense" is a geometric restatement, and a global algebraic derivation of (13′) could
   still exist. What the theorem excludes is a specific inference: closedness does not upgrade "$Z$ is
   nonempty" to "$Z$ covers the component", so no argument of the form "every component contains one
   symmetric point" can work.
2. **(13′) is weaker than the classification in one precise sense:** it needs $Z$ to be *dense*, i.e. a
   proof for all triples outside a closed lower-dimensional exceptional locus, and it does not need to
   know *which* triples are exceptional. It is not weaker in the sense of "one point per component"
   (withdrawn).
3. **Evidential status of sampling — qualified.** A distribution on the *full* moduli space that is
   absolutely continuous with respect to the volume of each dimension stratum would detect a nonempty
   open $O$ with positive probability, so for such a sample "no counterexample found" is meaningful
   evidence of the right kind — unlike a search for a fourth basis, which is a codimension-two event
   (`results/elegant-proof-routes.md` §9). A sample restricted to a *lower-dimensional* subfamily
   (my seven points on the JMSSW curve, or m2's 9,320 points on the two-parameter family *unless* that
   family is known to be the whole moduli space) is **not** by itself evidence against a full-dimensional
   open $O$: an open subset of $\mathcal T$ can miss a curve entirely. My family table should be read as a
   computation of $\Delta$ along that curve, not as a test of (13′).
4. **The detector's criterion survives, with one repair.** $3\mid\Delta_X\iff\operatorname{rank}_{\mathbb
   F_3}R_X<5$ concerns the 3-part, which is what Propositions 1–2 use. The source's
   $\Delta_X=[\Lambda_0:L_X]$ needs a further step, because the projection symmetry group
   $$\mathcal G_X=\{T\ \text{diagonal}:\ \operatorname{Ad}_T(W_{\mathcal B}\oplus W_{\mathcal C})
   =W_{\mathcal B}\oplus W_{\mathcal C}\}$$
   may also contain clocks that **exchange** the two bases; the "preserve or exchange" map
   $\mathcal G_X\to S_2$ has kernel $G_X$, so $[\mathcal G_X:G_X]\le2$ and the 3-parts agree:
   $3\mid|G_X|\iff3\mid|\mathcal G_X|$. The source's no-exchange argument is incomplete as written, but is repaired by m1's subsequent
   Theorem D: fixing one swapped ray gives $\operatorname{tr}T=6\mu_r\langle b_r,c_{\pi(r)}\rangle$,
   hence $|\operatorname{tr}T|^2=6$ exactly; odd-power reduction and the order-two/three/four
   multiplicity checks rule out a swap. Thus $\Delta_X=[\Lambda_0:L_X]$ is proved unconditionally.
   An earlier version of this note incorrectly claimed that only $|\operatorname{tr}T|\le\sqrt6$
   follows; that criticism is withdrawn. Independently, all 15 anchors where I computed both sides agree.

## 5. What is not proved here

- (13′) itself. Theorem A(c) says what would suffice (density of $Z$); I do not prove density.
- No statement about connected components, and no claim that an algebraic proof of (13′) is impossible.
- The concentration of the whole route on the *closedness* of the symmetric locus is the source's §7
  observation; my contribution is the correct proof (Propositions 1–2), the correct logical form
  (Theorem A), and the identification of the inference that does **not** follow from it.
