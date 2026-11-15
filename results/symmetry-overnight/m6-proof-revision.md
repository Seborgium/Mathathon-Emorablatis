# Modular revision of the diagonal-symmetry route to $N(6)=3$ — member m6

Status: working document, 2026-11-15, swarm `smwhnslql`, direction `d4` (nonextension side and
proof synthesis).  Every statement below is labelled

* **[P]** proved here (complete hypotheses + derivation),
* **[C]** conditional (the listed input is not proved here),
* **[N]** numerical/symbolic evidence only,
* **[O]** open / unresolved,
* **[L]** literature claim I did not verify myself.

Nothing in this file is a new proof of $N(6)=3$.  $N(6)=3$ is proved in the published record
(member m2's board finding: Wuttig–Tindall arXiv:2611.06917 + Jaming–Matolcsi–Móra–Szöllősi–Weiner
arXiv:0902.0882); what follows isolates *which* steps of the diagonal-symmetry programme are
already available, *which* one is missing, and what precisely its hypotheses are.

---

## 1. Definitions

Let $\mathcal A,\mathcal B,\mathcal C$ be pairwise unbiased orthonormal bases of $\mathbb C^6$.
For an anchor $X\in\{\mathcal A,\mathcal B,\mathcal C\}$ let

$$G_X=\{\,U\in U(6)\;:\; U \text{ diagonal in the } X\text{-basis},\ U\mathcal Y=\mathcal Y\cdot
(\text{diagonal phases})\cdot(\text{permutation})\ \text{for both other bases }\mathcal Y\,\}\big/\ U(1),$$

and $\Delta_X=|G_X|$.  ("Diagonal in the $X$-basis" plus "preserves the other two ray sets" is the
source's definition; $U$ fixing $X$'s rays is automatic, since a diagonal unitary fixes every
coordinate ray.)  All bases are flat with respect to each other: $|\langle x,y\rangle|=1/\sqrt6$ for
$x\in X$, $y\in Y$, $X\ne Y$.

The four statements that occur below:

* **(T1)** (the source's equation (13)) $\ \Xi(P_{\mathcal A})\Xi(P_{\mathcal B})\Xi(P_{\mathcal C})=0$
  for every triple, with $\Xi$ the five-term minor detector of source (11).
* **(T3)** $=$ step **(H2)** of the published classification: every triple has $3\mid\Delta_X$ for
  some anchor $X$.
* **(T2)** $=$ **R**: every triple has $\Delta_X\ge 2$ for some anchor $X$.  **R is not the
  unconditional residue** — it becomes sufficient only together with (I3); without (I3) the residue
  is (T3), equivalently (T1).
* **(I3)** the source's divisibility lemma (§4): $\Delta_X=2\Rightarrow 3\mid\Delta_{\mathcal Y}$
  for both other anchors.

---

## 2. [P] Lemma 1 (the symmetry group is finite cyclic of order $1,2,3,6$)

$G_X$ is a finite abelian group of order in $\{1,2,3,6\}$, and every non-identity element acts on
each of the other two bases as a fixed-point-free permutation of its six rays.

*Proof.*  **(a)** $G_X$ is abelian: its elements are diagonal matrices modulo scalars.

**(b) No non-identity element fixes a ray of another basis.**  Let $U\in G_X$ be diagonal in the
$X$-basis and suppose $Uy=\mu y$ for a ray $y$ of $\mathcal B$.  Unbiasedness gives $|y_i|=1/\sqrt6$
for all $i$; with $U=\operatorname{diag}(u_i)$ and $u_iy_i=\mu y_i$ we get $u_i=\mu$ for all $i$, so
$U=\mu\,\mathbb 1$, i.e. $U$ is the identity of $G_X$.

**(c) Finiteness.**  By (b) the action of $G_X$ on the six rays of $\mathcal B$ has trivial kernel,
so $G_X\hookrightarrow \mathrm{Sym}(6)$ is injective and $G_X$ is finite.

**(d) Order.**  By (b) the action on the six rays of $\mathcal B$ is free, so all orbits have size
$|G_X|$ and $|G_X|$ divides $6$.  With (a), $G_X$ is cyclic of order $1,2,3$ or $6$.  $\square$

*Remark.*  The source's §2 argues "its action is therefore free, so its order divides six".  The
finiteness needed for that sentence is exactly (c); without it $G_X$ is *a priori* a closed subgroup
of a torus and can be infinite.  The injection into $\mathrm{Sym}(6)$ supplied by (b) is the missing
step; with it the source's claim is correct as stated.

## 3. [P] Lemma 2 (an order-$3$ element acts in two $3$-cycles and has spectrum $(2,2,2)$)

Let $U\in G_X$ have projective order $3$.  Then

1. $U$ acts on each of the two other bases as a product of two $3$-cycles;
2. $U^3$ is a scalar, and the eigenvalues of $U$ are $1,\omega,\omega^2$ ($\omega=e^{2\pi i/3}$),
   each with multiplicity exactly $2$.  In particular, after reordering the $X$-coordinates and
   multiplying by a scalar,
   $$U=\operatorname{diag}(1,1,\omega,\omega,\omega^2,\omega^2).$$

*Proof.*  (1) is Lemma 1(b,d): a fixed-point-free permutation of order $3$ on six points is two
$3$-cycles.  (2) Let $Y$ be a basis permuted by $U$ with $Uy_s=\lambda_s y_{\sigma(s)}$,
$|\lambda_s|=1$.  Then
$$(Y^*UY)_{rs}=\langle y_r,Uy_s\rangle=\lambda_s\langle y_r,y_{\sigma(s)}\rangle=\lambda_s\,\delta_{r,\sigma(s)},$$
so $Y^*UY$ is monomial with permutation $\sigma$.  Since $\sigma$ has no fixed point,
$\operatorname{tr}(Y^*UY)=0$, and the trace is basis independent: $\operatorname{tr}U=0$.  On the
other hand $U^3$ is a scalar, so after multiplying $U$ by a cube root of that scalar,
$U=\operatorname{diag}(\omega^{a_1},\dots,\omega^{a_6})$ with $a_i\in\{0,1,2\}$.  Let $m_\nu$ be the
multiplicity of $\omega^\nu$; then
$$m_0\omega^0+m_1\omega+m_2\omega^2=\operatorname{tr}U=0,\qquad m_0+m_1+m_2=6 .$$
Over $\mathbb Q$ the only linear relation among $1,\omega,\omega^2$ is a multiple of
$1+\omega+\omega^2=0$, so $m_0=m_1=m_2$ and hence $m_\nu=2$.  $\square$

*Remark.*  The source's §2 writes "a nonconstant diagonal clock cannot fix a flat ray.  It therefore
acts in two three-cycles, giving $\operatorname{tr}T=0$."  The last inference is *not* immediate from
the permutation: it needs the monomial-matrix argument above (the permutation alone gives a
monomial matrix, whose trace is zero only because $\sigma$ is fixed-point-free).  With that one line
inserted, the claim, and with it the source's "the required $2+2+2$ multiplicities follow
automatically", is **[P]**.

## 4. [P] Lemma 3 (the hypotheses of the nonextension theorem follow, with no extra input)

If $3\mid\Delta_X$ for **one** anchor $X$, then the triple $(\mathcal A,\mathcal B,\mathcal C)$
satisfies the hypothesis of the Symmetry Obstruction (section 6) verbatim: there is a unitary $T$
with $T^3$ scalar, $T$ diagonal in the $X$-basis with eigenvalues of multiplicity $2$, fixing each
ray of $X$ and permuting each of the other two bases in two $3$-cycles.

*Proof.*  $G_X$ is cyclic of order divisible by $3$ (Lemma 1), so it contains an element $U$ of
projective order $3$; apply Lemma 2 with the two other bases in either order.  $\square$

*Consequences.*

* **Multiplicities**: $(2,2,2)$ is not an assumption; it is forced.
* **Both other bases**: the same $U$ works for both, because $G_X$ preserves both ray sets
  simultaneously.
* **Anchor independence**: the theorem requires the symmetry at *one* anchor only, and the two other
  bases enter it symmetrically.  So "$\exists X: 3\mid\Delta_X$" is exactly the hypothesis, and no
  condition linking the three anchors is needed.

## 5. [P] Normal form of a symmetric triple (frame coordinates; agrees with the project's Lemma A)

Let $T=I_2\otimes Z_3=\operatorname{diag}(1,1,\omega,\omega,\omega^2,\omega^2)$ in
$\mathbb C^6=\mathbb C^2\otimes\mathbb C^3$, blocks $x=(x_0,x_1,x_2)$, $x_j\in\mathbb C^2$.  A flat
basis $B$ is $T$-covariant ($TB=B\Pi$, $\Pi^3=1$) iff, after choosing a generator $v$ of one orbit
and $w$ of the other,
$$v=\sum_{t\in\mathbb Z_3}v_t\otimes e_t,\quad w=\sum_{t}w_t\otimes e_t,\qquad
\|v_t\|=\|w_t\|=1/\sqrt3,\quad \langle v_t,w_t\rangle=0\ \ \forall t,$$
and flatness is the extra condition that both components of every $v_t,w_t$ have modulus $1/\sqrt6$;
the basis is $\{T^av,T^aw\}$.  Each $t$ carries a $2\times2$ frame $(v_t,w_t)=(a_t,b_t;\ \bar
b_t,-\bar a_t)/\sqrt6\cdot(\text{phases})$, i.e. three phases; the two global phases of $v,w$ are
gauge, so a $T$-covariant flat basis has $3\cdot3-2=7$ real parameters (against $25$ for a general
flat basis).

*Proof.*  Orthonormality of $\{T^av,T^bw\}$ is $\sum_t\omega^{(a-b)t}\langle v_t,w_t\rangle=0$ for all
$a,b$ and $\sum_t\omega^{(a-b)t}\|v_t\|^2=0$ for $a\ne b$, i.e. $\langle v_t,w_t\rangle=0$ and
$\|v_t\|$ constant in $t$; $\sum_t\|v_t\|^2=1$ then gives $\|v_t\|^2=1/3$.  Flatness is coordinatewise.
Conversely such data give a $T$-covariant flat basis.  $\square$

This is the project's `results/order3-stratum.md` Lemma A plus its 7-parameter count; I re-derived
both (the count and the equivalence) and the exact example of section 7 realises it with
$T=\operatorname{diag}(1,\omega,\omega^2,1,\omega,\omega^2)$ at anchor $\mathcal A$.  It is the
"Hadamard-pair normal form" asked for in my direction: the symmetry removes 18 of the 25 phases of
each of the two other bases.

## 6. [P] The Symmetry Obstruction (the nonextension theorem), re-verified line by line

**Theorem (Symmetry Obstruction; source `attachments/is-this-a-useful-r01i`, audited in
`results/symmetric-obstruction-audit.md`).**  Let $\mathcal A,\mathcal B,\mathcal C$ be a MUB triple
in $\mathbb C^6$ and $T$ as in section 4.  Then no unit vector is unbiased to all three bases; in
particular the triple lies in no set of four MUBs.

I re-derived every step.  The skeleton, with the points that need care:

1. **Normalisation.** $\mathcal B=\{u,Tu,T^2u,v,Tv,T^2v\}$; every coordinate of $u$ has modulus
   $1/\sqrt6$ (flatness, i.e. $\mathcal B\perp\mathcal A$), so diagonal rephasing makes
   $u=(1,\dots,1)/\sqrt6$.  Diagonal rephasing commutes with **every** diagonal $T$, so the symmetry
   survives.  *(Correction: the project's audit note claims this step is wrong and needs a blockwise
   $U(2)$; it is not, and the audit's stated reason — that only block-scalar rephasings
   $\operatorname{diag}(\mu_0,\mu_0,\mu_1,\mu_1,\mu_2,\mu_2)$ commute with $T$ — is false.  Any two
   diagonal matrices commute.  The step is **[P]** as written.)*
2. **The second cycle is forced.** $\langle T^ru,T^sv\rangle=\sum_j\omega^{j(s-r)}\langle u_j,v_j
   \rangle=0$ for all $r,s$; the $3\times3$ Fourier matrix is invertible, so
   $\langle u_j,v_j\rangle=0$ for every block $j$, and with $u_j=(1,1)/\sqrt6$,
   $v_j=\nu_j(1,-1)/\sqrt6$, $|\nu_j|=1$.
3. **Fourier observation.** If $|z_0+\omega^{-r}z_1+\omega^{-2r}z_2|^2$ is the same constant for
   $r=0,1,2$, then $\sum_j|z_j|^2$ equals that constant and $z_0\bar z_1+z_1\bar z_2+z_2\bar z_0=0$
   (both are Fourier coefficients of the constant sequence $|w_r|^2$).  Hence three complex numbers
   summing to zero, i.e. side lengths of a triangle.
4. **Angle form.** For $g$ unbiased to $\mathcal A$ write $g_j=(p_j/\sqrt6)(e^{i\alpha_j},
   e^{-i\alpha_j})$; unbiasedness to the two cycles of $\mathcal B$ gives
   $\sum_j\cos^2\alpha_j=\tfrac32$ and triangles with side lengths
   $|\cos\alpha_j\cos\alpha_{j+1}|$ and $|\sin\alpha_j\sin\alpha_{j+1}|$ ("admissible").  The phases
   $p_j,\nu_j$ cancel.  Same for $w_j=\lambda_j(\bar g_{j1},-\bar g_{j0})$ and for a candidate
   fourth vector $h$: $\alpha$, $\beta$, $\beta-\alpha$ must all be admissible.  *(This is the step
   that makes the complex problem nine real angles; I reproduced all the overlaps, including the
   $\lambda_j$-cancellation.)*
5. **Heron.** With $v_j=\cos2\theta_j$: $\sum v_j=0$, and the cosine and sine triangles give
   $12-12s-s^2\pm48t\ge0$ with $s=\sum v_j^2$, $t=v_0v_1v_2$; hence $s+4|t|+s^2/12\le1$.  If
   $|v_0|=x\ge1/\sqrt2$ then $s+4|t|\ge2x^2\ge1$ with $s^2/12>0$, a contradiction, so
   $|v_j|<1/\sqrt2$ for every admissible triple.  *(I verified the algebraic identity
   $16\Delta_{\text{Heron}}^2=(12-12s-s^2+48t)/64$ symbolically under $\sum v_j=0$, and the
   $x\ge1/\sqrt2$ estimate by hand: $-2u+4x|u|\ge0$ for every sign of $u=v_1v_2$.)*
6. **$3\times3$ sign lemma.** The array $M_{j}=(v_j(\alpha),v_j(\beta),v_j(\beta-\alpha))$ has zero
   column sums, entries of modulus $<1/\sqrt2$, and every row on $x^2+y^2+z^2-2xyz=1$ (verified
   symbolically for $x=\cos A,y=\cos B,z=\cos(B-A)$).  No such array exists: a row product
   $xyz\ge0$ is impossible (sort $|x|\ge|y|\ge|z|=a\ge b\ge c$; if $b\le\tfrac12$ then
   $a^2+b^2+c^2<1$; if $b>\tfrac12$ then $a^2+b^2+c(c-2ab)\le a^2+b^2<1$, both against $=1$), so
   every row product is negative and no entry vanishes; flip columns so each column has exactly one
   negative entry (an even number of flips, so all row products stay negative); then each row has
   exactly one negative entry, say $(-a,b,c)$ with $a,b,c>0$ and $a^2+b^2+c^2+2abc=1$, and
   $b+c\le a$ would give $1=a^2+(b+c)^2-2bc(1-a)\le2a^2<1$; so every row has positive sum while
   every column sums to zero.  Contradiction.  $\square$

*Sharpness check.*  The `3` in the sign lemma is essential: with four rows the analogous statement
is false.  The audit's array $M=\tfrac12[(-1,-1,-1),(-1,1,1),(1,-1,1),(1,1,-1)]$ has zero column
sums, every row on $x^2+y^2+z^2-2xyz=1$ (I verified: $\sum r_j^2-r_0r_1r_2=4$ for each unscaled row,
hence value $1$ after halving) and $\max|M_{jk}|=1/2<1/\sqrt2$.  So the obstruction is genuinely
three-row, i.e. it uses the $\mathbb Z_3$ structure of dimension six, not dimension counting.

**Verdict: [P].**  With Lemma 3 the theorem applies to *any* triple with $3\mid\Delta_X$ at any
anchor.  No additional nonextension theorem, no classification, and no extra hypothesis about
multiplicities or anchor dependence is needed beyond it.  This answers the first half of my
direction: the nonextension step is **not** where the residue is.

## 7. [P] Exact data: the tensor/Heisenberg triple

Script `m6-check.py` (this directory; exact arithmetic in $\mathbb Z[\zeta_{24}]$, $\sqrt6=\zeta+
\zeta^{23}+\zeta^5+\zeta^{19}$) computes, for
$\mathcal A=\mathbb 1_6$, $\mathcal B=H\otimes F_3$, $\mathcal C=H'\otimes F'_3$ with
$H=\frac1{\sqrt2}\binom{1\ 1}{1\ {-1}}$, $H'=\frac1{\sqrt2}\binom{1\ \ 1}{i\ {-}i}$, $F_3$ the
qutrit DFT and $F'_3$ the $XZ$ eigenbasis:

| check | result |
|---|---|
| $\mathcal B,\mathcal C$ orthonormal, $\mathcal B^*\mathcal C$ flat | exact (all entries certified as $\zeta_{24}^e/\sqrt6$) |
| $\Delta_{\mathcal A}=\Delta_{\mathcal B}=\Delta_{\mathcal C}$ | $6,6,6$ (exhaustive over $720$ permutations per basis) |
| orders of the six elements | $1,2,3,3,6,6$ — all in $\{1,2,3,6\}$ |
| multiplicities | order $2$: $(3,3)$; order $3$: $(2,2,2)$; order $6$: $(1^6)$, with square $(2,2,2)$ and cube $(3,3)$ |
| cycle types on each of the other two bases | order $2$: $(2,2,2)$; order $3$: $(3,3)$; order $6$: $(6)$ — Lemma 2(1) confirmed |
| nonzero entries of $P_X$ (all $900$ positions scanned) | $150$ at each anchor |
| of these, zero relation vector | exactly the $30$ positions $(i,j,i,j)$, $i\ne j$, with $(P_X)_{ij,ij}=1/3$ (the source's normalisation, verified exactly) |
| nonzero relation vectors $\to$ Smith form of $L_X$ | $120$ rows, $[1,1,1,1,6]$ at each anchor, index $6=\Delta_X$ |

The cycle-type row is Lemma 2(1) on the nose: an order-$3$ element acts as two $3$-cycles on
each of the other two bases, and an order-$2$ element as three $2$-cycles.  So the source's table row
"standard product triple, selected coordinate basis, $\Delta=6$" is
confirmed **at all three anchors**, Lemma 1 and Lemma 2 are confirmed on an exact example, and the
source's identity (5) $\Delta_X=[\Lambda_0:L_X]$ is confirmed exactly here (its general proof is the
rank-one Recovery Lemma, audited in direction d1).  Two different counts must not be confused:
$P_X$ has $150$ nonzero entries, but only $120$ of them supply a *nonzero* relation $r_{ij,k\ell}$;
the other $30$ are the diagonal matrix-unit positions $(i,j,i,j)$, whose relation vector vanishes
identically.  The source's normalisation $(P_X)_{ij,ij}=1/3$ is thereby verified exactly, and the
index $6$ is the Smith index of the $120$ nontrivial relations (adding the $30$ zero rows changes
nothing).  Note that this triple is *not* the source's
$(3,3,2)$ example: its entries are 24th roots, but all three indices are $6$.  The source's exact
$(3,3,2)$ example is **[O]** here: I did not reproduce it, and a $\Delta=2$ triple is exactly what
would test **(I3)** (it is consistent with (I3), since $(3,3,2)$ has $3\mid3$ and $3\mid3$).

## 8. Closedness of the residue [P]; divisibility in limits [C on (5)]

**(a) [P] $\{x:\Delta_X(x)\ge2\}$ and $\{x:3\mid\Delta_X(x)\}$ are closed; no Recovery Lemma is
needed.**  By Lemma 1, $\Delta_X\ge2$ iff $G_X$ contains an element of order $2$ or $3$, i.e. iff
$G_X\cap\mathcal K\ne\{1\}$ where $\mathcal K=\{[T]:T^6=1\}$ is the finite set of diagonal clocks
with entries in the sixth roots of unity (up to scalars).  For fixed $[T]\in\mathcal K$ the condition
$[T]\in G_X(x)$ is: for each ray $y_r$ of each of the other two bases, $Ty_r$ is proportional to some
$y_s$; since both are unit vectors this is $|\langle Ty_r,y_s\rangle|=1$ for some $s$, a finite union
of closed conditions, continuous in $x$ and invariant under rephasing.  Hence
$$\{x:\Delta_X(x)\ge2\}=\bigcup_{[T]\in\mathcal K\setminus\{1\}}\{x:[T]\in G_X(x)\}$$
is a finite union of closed sets.  (Phrased in the gauge where the anchor $X$ is the standard basis,
i.e. on the triple space modulo the compact rephasing group; for another anchor apply the same
argument after the continuous relabelling that makes that anchor standard, which carries $G_X$ to
the corresponding group.  The condition is invariant under rephasing by construction.)  Replacing
$\mathcal K$ by the $3$-torsion gives the same statement for $\{x:3\mid\Delta_X(x)\}$ (this is member
m4's Proposition 2, independently).  Consequently $\{\Delta=(1,1,1)\}$ is open.

**(b) [C on (5)] Divisibility in limits.**  Additionally, if $x_n\to x$ then
$\Delta_X(x_n)\mid\Delta_X(x)$: with $L_X$ as in section 1, a relation present at $x$ is present at
$x_n$ for large $n$ (nonvanishing is open), so $L_X(x)\subseteq L_X(x_n)$, and indices are
multiplicative in towers, so $[\Lambda_0:L_X(x_n)]$ divides $[\Lambda_0:L_X(x)]$; by the source's
(5) (equivalently the Recovery Lemma) this is the asserted divisibility.  This is the precise form of
the source's §7 remark.  Note that (a) does **not** need (5); only the divisibility refinement (b)
does.

Consequences:

* Read positively: since $\{\Delta_X\ge2\text{ for some }X\}$ is closed, it suffices to prove
  symmetry-existence on a **dense** family of triples; closedness then propagates it to all triples.
  This is the reason the residue is the right *shape* of target.
* Read negatively: nothing smaller than a dense set suffices.  A proof that produces a diagonal
  symmetry on an open subset (however large), a local-constancy or perturbation argument, or a
  near-miss computation proves nothing about the residue, because the complement of (T2) is open and
  therefore either empty or carrying interior.  In this respect (T2) has the same shape as the
  project's route R7 verdict.

## 9. The modular chain, and the exact residue

Write $N(6)\ge4$ for the existence of a quartet.  Then:

$$
\underbrace{\text{(T1)}}_{[O]}\iff\underbrace{\text{(T3)}=(H2)}_{[L]\ \text{certified in the literature}}
\Longrightarrow\underbrace{\text{(T2)}}_{[O]}\overset{\text{(I3)}}{\Longrightarrow}\text{(T3)}
\overset{\text{Lemmas 1--3, Thm 6}}{\Longrightarrow}\neg(N(6)\ge4).
$$

* **(T1) $\Rightarrow$ (T3) [P].**  $\Xi(P)\ge0$ is a sum of nonnegative terms, and
  $\Xi(P_X)>0$ iff five positions with all entries nonzero carry five relations independent mod $3$,
  iff $\operatorname{rank}_{\mathbb F_3}R_X=5$ (a matrix has rank $5$ iff some $5\times5$ minor is
  nonzero).  So $\Xi(P_X)=0\iff3\mid\Delta_X$ — this is the source's (12) and it is immediate from
  (3) plus the Recovery Lemma.  Hence (T1) says exactly: some anchor has $3\mid\Delta_X$.  **Note
  that (T1) does not use (I3) at all.**
* **(T3) $\Rightarrow$ (T2) [P]**, since $3\mid\Delta_X$ implies $\Delta_X\ge2$.
* **(T2) + (I3) $\Rightarrow$ (T3) [P]**: if $\Delta_X\ge2$ then either $3\mid\Delta_X$, or
  $\Delta_X=2$ and (I3) gives $3\mid\Delta_{\mathcal Y}$.  So *given (I3), (T2) and (T3) are
  equivalent*; the source's reduction is what licenses replacing the order-$3$ target by the weaker
  closed condition "$\Delta\ge2$", i.e. it is worth something exactly if order-$2$ symmetries are
  easier to force than order-$3$ ones (which is the whole content of the source's §4).
* **(T3) $\Rightarrow\neg(N(6)\ge4)$ [P]** by Lemmas 1–3 + the Symmetry Obstruction (section 6).

Hence, **unconditionally, the residue of the diagonal-symmetry route is (T3), equivalently (T1)**:
"every MUB triple in $\mathbb C^6$ has $3\mid\Delta_X$ at some anchor $X$".  Everything downstream of
(T3) is proved (Lemmas 1–3 + the Symmetry Obstruction).  If **(I3)** — the source's divisibility
lemma, the one input I did not verify — is granted, the residue weakens to **(T2) = R**: "every
triple has $\Delta_X\ge2$ for some anchor", equivalently "every triple is invariant, as a ray-set
triple, under some non-scalar diagonal unitary at some anchor".  So the correct statement is:

> **(T2) + (I3) $\Rightarrow$ (T3) $\Rightarrow$ no fourth basis**, and without (I3) the open target
> is (T3) (equivalently (T1)), not (T2).

## 10. Status table for the source's claims in my scope

| source claim | status |
|---|---|
| §2 $\Delta_X\in\{1,2,3,6\}$ and $G_X$ cyclic | **[P]** Lemma 1 (finiteness step supplied) |
| §2 non-identity elements act freely on the other two bases | **[P]** Lemma 1(b) |
| §2 "the $2+2+2$ multiplicities follow automatically" | **[P]** Lemma 2 (monomial-trace line inserted) |
| §2 $\Delta_X=2\Rightarrow3\mid\Delta_{\mathcal Y}$ | (**I3**) not verified here; consistent with the source's $(3,3,2)$ example |
| §3 (12) $\Xi=0\iff$ threefold symmetry | **[P]** $\Xi>0\iff$ some $5$-minor $\not\equiv0\pmod3$ (section 9), given (3)+Recovery |
| §3 (5) $\Delta_X=[\Lambda_0:L_X]$ | **[P]** here exactly for the tensor triple ($6=6$, three anchors); general proof = Recovery Lemma (**[L]**/d1) |
| §4 order-$2\Rightarrow$order-$3$ (equilateral triangles, $3\times3$ Hadamards) | not my direction; **(I3)** is the only place my chain needs it |
| §5 (13) $\Xi_{\mathcal A}\Xi_{\mathcal B}\Xi_{\mathcal C}=0$ | **[O]**; if proved it gives (T3) directly, hence $N(6)=3$ through sections 4 and 6 |
| §6 table "standard product triple: $\Delta=6$" | **[P]** exact, in fact $6$ at **all three** anchors |
| §6 exact $(3,3,2)$ example with Smith $[1,1,1,1,3],[1,1,1,1,3],[1,1,1,1,2]$ | **[O]** not reproduced; different from the tensor triple |
| §7 "$\Delta_X(x_n)\mid\Delta_X(x)$ under limits" | **[C]** on (5)/Recovery (section 8(b): index tower).  Closedness of $\{\Delta\ge2\}$ itself is **[P]** unconditionally (section 8(a), finite 6-torsion) |
| §7 "an analytic proof on a dense subset suffices" | **[P] correct as stated**, because $\{\exists X:3\mid\Delta_X\}$ is closed and the triple space is compact: a dense subset has closure everything.  The honest caveat is the one the source states (isolated components must be reached by the dense set).  This is what makes (T2)/(T3) the right *shape* of target: symmetry-existence on any dense family of triples extends to all triples |

## 11. What a completion would have to prove, and what it would not replace

* It would **not** need a new nonextension theorem, a classification of triples, or any statement
  about multiplicities/anchor dependence beyond Lemma 3.
* It **would** need (T3), equivalently (T1) — the statement the literature certifies through 2,775
  interval balls.  Granting (I3) as well, (T2) suffices, and (T2) is the weakest of the three; it is
  closed, so any proof of it (or of (T3)) must be global.
* Because (T1) ⟺ (T3), proving (T1) is *equivalent* to proving the symmetry-forcing step, i.e. the
  source's central identity is not a weaker target but exactly the hard step in algebraic form.  It
  also shows (13) is a legitimate target: it is an identity of nonnegative polynomials, so it cannot
  be false on an open set without contradicting the literature's (T3) — a numerical or exact
  counterexample to (13) would therefore refute (T3), hence would be a major result.  I found no
  counterexample; direction d3 is testing it.
