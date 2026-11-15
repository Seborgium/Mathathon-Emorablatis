# Uniform involution case: lead-reviewed proof

Status: **proved here**, independently checked after m5's submission. This is deliberately narrower
than m5's numerical stratum claims: it proves the uniform half of the source's order-two-to-order-three
argument and nothing about completeness of the numerical nonuniform enumeration.

Let $A=I_6$ and suppose the other two MUBs are paired by $S=\operatorname{diag}(I_3,-I_3)$:
$$U=\frac1{\sqrt2}\begin{pmatrix}H_0&H_0\\H_1&-H_1\end{pmatrix},\qquad
V=\frac1{\sqrt2}\begin{pmatrix}K_0&K_0\\K_1&-K_1\end{pmatrix},$$
where all four $3\times3$ matrices are normalized complex Hadamards. Put $X=H_0^*K_0$ and
$Y=H_1^*K_1$. Unbiasedness of $U,V$ is equivalent to
$$|X_{ij}|^2+|Y_{ij}|^2=\frac23,\qquad \Re(X_{ij}\overline{Y_{ij}})=0.$$
The **uniform case** is $|X_{ij}|=1/\sqrt3$ everywhere.

**Theorem.** In the uniform case $T=Z\oplus Z$, with $Z=\operatorname{diag}(1,\omega,\omega^2)$,
belongs to both $G_U$ and $G_V$. Thus $3\mid\Delta_U$ and $3\mid\Delta_V$.

## 1. Two Hadamard lemmas

**Column lemma.** Every normalized $3\times3$ Hadamard satisfies $ZH=HD\Pi$ for some diagonal
unitary $D$ and permutation $\Pi$.

*Proof.* Write $H=D_1FD_2\Pi_2$, where $F$ is the qutrit Fourier matrix. Every $3\times3$ Hadamard
has this form (dephase, then use that three equal-modulus numbers summing to zero are rotated cube
roots). Since $ZF=FS$ for a cyclic column shift $S$, and $SD_2=D_2^\sigma S$ for the corresponding
permuted diagonal, the equations used above give
$$ZH=D_1FD_2^\sigma S\Pi_2=H\bigl(\Pi_2^{-1}D_2^{-1}D_2^\sigma S\Pi_2\bigr),$$
a diagonal matrix times a permutation. $\square$

**Row/conjugate lemma.** For every normalized $3\times3$ Hadamard $H$ and every diagonal
unitary $C$ whose entries are $(\omega^{aj+b})_{j=0}^2$ with $a\in\{1,2\}$ and $b\in\mathbb Z_3$,
right multiplication $H^*C$ equals $H^*D\Pi$ for a diagonal $D$ and permutation $\Pi$. Thus multiplying
each row of $H^*$ componentwise by the same cube-root character permutes the rows up to phases.

*Proof.* Apply the column lemma to $H^{\mathsf T}$, with $Z^a$ in place of $Z$:
$Z^aH^{\mathsf T}=H^{\mathsf T}D_a\Pi_a$. Complex conjugation gives
$\overline{Z^a}H^*=H^*\overline{D_a}\overline{\Pi_a}$. For $a=1,2$ the left factor covers
$(1,\omega^2,\omega)$ and $(1,\omega,\omega^2)$, respectively; the extra global factor $\omega^b$ is
harmless. $\square$

## 2. Sign factorisation

Uniformity and the two compatibility equations give $|Y_{ij}|=1/\sqrt3$ and
$Y_{ij}=i\epsilon_{ij}X_{ij}$ with $\epsilon_{ij}=\pm1$. For distinct rows $r,r'$, unitarity yields
$$0=\sum_j\epsilon_{rj}\epsilon_{r'j}\,X_{rj}\overline{X_{r'j}}.$$
The three products $X_{rj}\overline{X_{r'j}}$ have modulus $1/3$ and themselves sum to zero, hence
point in the three distinct cube-root directions. Changing signs on any proper nonempty subset cannot
preserve that zero sum. Consequently $\epsilon_{rj}\epsilon_{r'j}$ is independent of $j$, so
$\epsilon_{rj}=q_rc_j$.

Exchanging the two rays in selected $S$-pairs replaces $H_1$ by $H_1D_r$ and $K_1$ by $K_1D_c$ for
sign diagonals. It leaves $X$ unchanged and turns $Y$ into $D_rYD_c$, hence absorbs $q_rc_j$. These
are only rephrasings/reorderings of rays. We may therefore assume $Y=iX$, giving
$$U^*V=K\otimes X,\qquad K=\frac12\begin{pmatrix}1+i&1-i\\1-i&1+i\end{pmatrix}.$$

## 3. The clock at $U$

In $U$-coordinates the triple is $(I,U^*,K\otimes X)$. The diagonal $T$ fixes $I$. By the column lemma,
$$T(K\otimes X)=K\otimes(ZX)=K\otimes(XD\Pi)=(K\otimes X)(I\otimes D\Pi),$$
so $T$ preserves $K\otimes X$ as a ray set.

The columns of $U^*$ have the forms $(v_r;v_r)/\sqrt2$ and $(w_r;-w_r)/\sqrt2$, where
$v_r=\overline{\operatorname{row}_r(H_0)}$ and $w_r=\overline{\operatorname{row}_r(H_1)}$.
Applying $T$ multiplies the entries of $v_r,w_r$ by $(1,\omega,\omega^2)$. By the row/conjugate lemma,
this sends each plus-type column to a phase of another plus-type column, and each minus-type column to
a phase of another minus-type column. Hence $T$ preserves $U^*$ as a ray set. Since $T^3=I$ and $T$ is
nonscalar, $T\in G_U$ and $3\mid\Delta_U$.

## 4. The clock at $V$

Run the same argument after interchanging $U,V$. In $V$-coordinates the other matrices are $V^*$ and
$V^*U=K^*\otimes X^*$; the latter is again a Hadamard, so the column lemma applies. The row/conjugate
lemma applies to $K_0,K_1$. Therefore $T\in G_V$ and $3\mid\Delta_V$. $\square$

## 5. Checks and remaining limitation

`m5-exact-certificate.py` was rerun successfully: one exact instance has
$\Delta=(2,3,3)$ and Smith diagonals $(1,1,1,1,2)$, $(1,1,1,1,3)$, $(1,1,1,1,3)$.
`m5-involution-stratum.py --part 4` was also rerun successfully: the clock condition holds in all
$108^2=11664$ uniform constructed examples, with zero failures.

The nonuniform case, the normal form (8) as a universal normalization, and completeness of the
multistart involution-stratum search remain open. In particular the full implication
$\Delta_A=2\Rightarrow3\mid\Delta_B,\Delta_C$ is still conditional on that unresolved part; the
numerical search is evidence only, and support monotonicity does not make $\Delta$ locally constant.
