# The proof, claim by claim

Every load-bearing claim in *The maximum number of mutually unbiased bases in dimension six*
(OpenAI, 24 Sep 2026) restated in precise form, in the paper's own order, with the kind of
evidence behind it.

**Status key**

| tag | meaning |
|---|---|
| **M** | mathematical statement with a proof in the paper; I checked the statement and the main steps and, where the argument is a two-line computation, re-derived it |
| **M?** | mathematical statement whose proof is long or whose bookkeeping I could only sample (noted where) |
| **S** | a claim about what a named routine does. Its evidence is the source, which is **not in the packet**; it is a specification claim, not a proved one |
| **C** | carries a hypothesis that a particular finite execution succeeded — an event, not a mathematical condition |
| **E** | observed datum (counts, hashes, timings) |

---

## 1. The top-level claim and how it decomposes

**Theorem 1.1.** No four pairwise MUBs exist in $\mathbb{C}^6$; hence $N(6)=3$ with Lemma 1.2.
Status **C**: hypothesis is "the invocation list of §7.2 met its terminal conditions, with provenance
and batch checks, under the arithmetic of Appendix A".

Its skeleton, with each link's status:

```
Lemma 1.2 (3 MUBs exist, M)
   +
Prop 2.10  every exact H has a seed center within 0.032            [M + S + C]
   +
Prop 4.16  those seeds' completions land in atlas balls of radius ≤ .125  [M + S + C]
   +
Prop 5.7 / Cor 5.8  three B passes shrink to radius ≤ .011         [M + S + C]
   +
Prop 6.9   every emitted ball is not extendible by two more bases  [M + S + C]
   ⇒ Theorem 7.1 (C), then Theorem 1.1
```

Every link is an *implication*, and each is conditional on (i) a routine behaving as described and
(ii) the run having closed. Nothing in the chain asserts that the configurations it must exclude
are absent for a structural reason; closure is empirical.

**Corollary 1.3.** At most three pairwise Killing-orthogonal, adjoint-closed Cartan subalgebras of
$\mathfrak{sl}_6(\mathbb{C})$. Status **M** modulo a citation: the reduction to bases is
Boykin–Sitharam–Tiep–Wocjan [3, Thm 5.2], and the key computation
$\operatorname{tr}((bb^*-I/6)(cc^*-I/6))=|\langle b,c\rangle|^2-1/6$ is verified. Adds nothing to
the MUB statement.

---

## 2. Claims in §1–2 (reductions, symmetries, seed cover)

**Lemma 1.2.** Three MUBs in $\mathbb{C}^6$ from $2\otimes3$: with $A_0=I_2$,
$A_1=\frac1{\sqrt2}\binom{1\ \ 1}{1\ -1}$, $A_2=\frac1{\sqrt2}\binom{1\ \ 1}{i\ -i}$ (all cross entries
squared modulus $1/2$), $B_0=I_3$, $B_1=F$, $B_2=DF$ with $F=\frac1{\sqrt3}(\omega^{jk})$,
$\omega=e^{2\pi i/3}$, $D=\operatorname{diag}(1,\omega,\omega)$; then
$(F^*DF)_{jk}=\frac13\sum_{x=0}^2\omega^{x^2+(k-j)x}$ has modulus$^2=1/3$ for $k\ne j$ (values
$1+2\omega$ and $2+\omega^2$, each of modulus$^2$ 3), so $U_r=A_r\otimes B_r$ are pairwise unbiased.
Status **M** — checked, including the Gauss sums, which are the only non-immediate case. (The
corrected $D$ is what is printed here.)

**Lemma 2.2.** Extendibility is invariant under row/column permutations, row/column rephasings,
complex conjugation, transposition. Status **M**. Transposition is the only non-obvious case; the
proof moves to the pair $(U^*,I)$, swaps the roles and conjugates coordinates, all reversible.

**Lemma 2.3.** $\Pi$ (double centering, (2.1)) is the orthogonal projection onto the subspace of
matrices with zero row and column sums; $\|\Pi z\|_F\le\|z\|_F$; two phase representatives differing
by $z$ are equivalent under row/column rephasings after replacing by $P+\Pi z$; unaffected by
entrywise integer changes. Status **M**. This is the licence for all later "horizontal" reasoning.

**Lemma 2.4 (seed arrangement).** For every exact $H$ there is an equivalent dephased representative
such that: a pair of rows attaining the minimum circular gap over all row pairs *and* column pairs
is the first pair; after rephasing and ordering along the complementary arc,
$x=(0,x_1,\dots,x_5)$ with $0\le x_1\le\cdots\le x_5$, gap $g_x=1-x_5$, and
$x_1\le x_5-x_4$; after choosing one of the five non-initial columns and moving it to position 2 and
sorting the last four rows, the second column is $y=(0,\xi,y_2,\dots,y_5)$ with $\xi$ the selected
entry of $x$; moreover $1+\sum_je(x_j)=0$, $1+e(\xi)+\sum_je(y_j)=0$, and $g_y\ge g_x$.
Status **M?**. The three-step construction (min-gap pair → transpose if needed → orientation swap
$x'_i=x_5-x_{5-i}$ attaining the reverse inequality) is correct and the gap invariance under
rephasing/permutation/transposition is immediate; the orientation-swap step is the place a reader
must check carefully, and it is proved in four lines.

**Lemma 2.5.** If two circular multisets are matched pointwise at circular distance $\le\delta$, their
gaps differ by $\le2\delta$. Status **M** (trim $\delta$ from each end of an empty arc).

**Lemma 2.6.** With bins of width $w=1/112$, $g_{x,\mathrm{mid}}\le1-(l-1)/N$ and
$g_{y,\mathrm{mid}}\ge1-(l+2)/N$. Status **M** (Lemma 2.5 plus $x_5\in[l/N,(l+1)/N]$).

**Lemma 2.7.** If $1+\sum_je(u_j+\Delta_j)=0$ with $|\Delta_j|\le w/2$, then
$\|c+J\Delta\|\le5\pi w^2/4$ and $|v\cdot c|\le\frac{5\pi w^2}{4}\|v\|+\frac w2\sum_j|v\cdot J_j|$ for
all $v$, where $c=(1+\sum_je(u_j))/(2\pi i)$, $J_j=e(u_j)$ realified. Status **M** (Taylor with
$|e''|=4\pi^2$; the division by $2\pi i$ is what turns the vanishing sum into $c+J\Delta\approx0$ —
worth stating explicitly, as the paper does not).

**Lemma 2.8.** Shared-coordinate intervals: with $h=N\Delta$, every feasible displacement satisfies
$|Nv\cdot c+(v\cdot J_t)h_t|\le E\|v\|+\frac12\sum_{j\ne t}|v\cdot J_j|$, $E=5\pi/(4N)$, hence a
closed interval for $h_t$; the intervals computed from the $x$-list ($t=s$) and the $y$-list
($t=0$) must intersect. Status **M**.

**Lemma 2.9.** Reuse support bounds: for a current midpoint $u$ and retained $u'$,
$k=N(u-u')\in\mathbb{Z}^9$, $h=N(q-u)\in[-\frac12,\frac12]^9$,
$N^2\|q-u'\|^2=\|k+h\|^2\le\|k\|^2+\frac94+2k\cdot h$, with
$2k\cdot h\le\sum|k_j|$ and the dual bound
$2k\cdot h\le\sum_j|k_j-(J_*^Tv)_j|+2v\cdot p_*+2E(\|v_X\|+\|v_Y\|)$ for any $v\in\mathbb{R}^4$.
Status **M**.

**Proposition 2.10 (exhaustive seed cover).** On a completed `covout` traversal, the written rational
midpoints, with their recorded selected positions, cover the nine seed coordinates of every exact $H$
up to Lemma 2.2, by closed balls of radius $0.032$; after conversion to binary phases,
$0.0320001$ suffices. Status **M + S + C**. The mathematical half is a clean induction: every exact
$H$'s bin pair survives the necessary filters (2.6–2.8), and each processed pair is either certified
into an existing radius-$R$ ball (2.9) or contributes its own midpoint, which lies within
$\sqrt9/(2\cdot112)=3/224<0.032$ of the pair. The two premises are that the enumeration visits all
bin tuples (**S**) and that it completed (**C**).

**Claims about the code inside §2.** `seeds::mk` uses the first minimiser of $|2b_s+1-N|$ as the
selected position (**S**); `sumok` tests (2.11) in the residual direction and directions
perpendicular to the five exponential columns (**S**, sound because (2.11) holds for all $v$);
`extend` intersects the (2.14) intervals for the shared coordinate and omits divisors $<10^{-6}$
(**S**, sound because omitting a constraint only enlarges); `supdual` accepts proposals only with
entries $\le10^4$ in modulus and evaluates (2.19) with $1.251\pi/N$ in place of $1.25\pi/N$ (**S**).

---

## 3. Claims in §3 (Stage A: all completions of one seed)

**Lemma 3.1 (fixed frames).** For unit-modulus $p\in\mathbb{C}^4$, $S=\sum_jp_j$, $M=(1\ \ p)$: the
squared singular values of $M$ are $4\pm|S|$; if $|S|<4$ then
$M(M^*M)^{-1}=\frac{1}{16-|S|^2}(4\mathbf{1}-p\bar S,\ 4p-\mathbf{1}S)$ and an orthonormal $K$ with
$\mathrm{ran}\,K=\ker M^*$ exists, constructible by Gram–Schmidt from the residual of $p$ and
coordinate vectors. Status **M**. This is what makes the frames $G_B,G_C,K_B,K_C$ of (3.5) exist
and stay *fixed* across the whole seed ball.

**Lemma 3.2 (polar comparison).** For a feasible completion, $Y=K_C^*D'K_B$ satisfies
$6I-Y^*Y=K_B^*B'^*B'K_B+K_B^*D'^*P_CD'K_B\succeq0$, its trace is $\le q=R_s^2(1+(A_*^2+6)/m_C^2)$, and
if $q<6$ the polar factor $V=Y(Y^*Y)^{-1/2}\in U(2)$ satisfies
$\|Y-\sqrt6V\|_F\le p^2$ with $p$ as in (3.11). Status **M**. I re-derived (3.8) (using
$K_CK_C^*=I-P_C$) and the trace bound (Cauchy–Schwarz on $A_*b_1'+\sqrt6c_1'$ plus (3.3)); the
consequence is the hinge of the whole proof: **every** completion of a seed gives a point of $U(2)$,
so a fixed cover of $U(2)$ covers all completions.

**Lemma 3.3.** Every $V\in U(2)$ is $e(\alpha)$ times an $SU(2)$ matrix parametrised by
$t\in[0,\frac14]$, $\beta,\gamma\in[0,1]$ as in (3.12); products of closed bins of width $1/N_u$ with
$N_u\equiv0\ (4)$ cover the domain, with bin counts $N_u/2,N_u/4,N_u,N_u$. Status **M**.

**Lemma 3.4 (cell Taylor estimates).** Uniformly on a cell with $|\theta_j|\le h=\pi/N_u$:
$\|V-U\|_F\le\sqrt6\,h$ and $\|V-U-\mathrm dU[\theta]\|_F\le\frac{\sqrt{42}}{2}h^2$.
Status **M** — I re-derived the second-derivative ledger ($\cos^2$ and $\sin^2$ parts contributing
$26h^4$ and $16h^4$ respectively, total $42h^4$).

**Lemma 3.5 (orthogonal comparison pieces).** With $D=D_{\mathrm{span}}+D_{\mathrm{ker}}$,
$D_{\mathrm{span}}=-C_0E_0^*G_B^*$, $D_{\mathrm{ker}}=\sqrt6K_CUK_B^*$, and $Z=D'-D$: the three pieces
$ZP_B$, $P_CZP_K$, $(I-P_C)ZP_K$ are pairwise Frobenius-orthogonal, sum to $Z$, have the explicit
forms (3.16)–(3.18), and $\|Z\|_F\le z$ with $z$ in (3.19). Status **M** (decomposition and orthogonality
are immediate from $P_B=I-P_K$; the norm bookkeeping is the content).

**Lemma 3.6.** $\|[C_0\ D]\|_{\mathrm{op}}\le L$ (3.20), $\|DP_K\|_{\mathrm{op}}=\sqrt6$,
$\|D\|_{\mathrm{op}}\le\max\{\sqrt6,\|C_0\|_{\mathrm{op}}A_0/m_B\}$. Status **M** (cross terms vanish
because the two pieces have orthogonal right domains and ranges).

**Lemma 3.7 (linear remainder).** $\|Z-J(s,\theta)\|_F\le E_r$, $E_r^2=e_{\mathrm{off}}^2+
(\frac{\sqrt6\cdot42}{2})^2h^4+p^2$, with $e_{\mathrm{off}}=\frac{R_s^2(L+A_0+1)}{2m}+\frac{zR_s}{m}$.
Status **M?**: the three remainder groups (seed product terms, $Z$-product terms, the
$|e^{ix}-1-ix|\le x^2/2$ Taylor terms) are each bounded in the right subspace; the arithmetic
combining them is where a slip would hide, and it is checked only in A.4.

**Lemma 3.8 (norm exclusion).** A feasible completion in a cell forces
$\sum_{i,j=0}^3(|D_{ij}|-1)^2\le z^2$. Status **M** (reverse triangle inequality entrywise).

**Lemma 3.9 (directional exclusion).** For any $y\in\mathbb{R}^{20}$, split $y_X,y_Y\in\mathbb{R}^2$,
$y_D\in\mathbb{R}^{16}$, $g=J_{\mathrm{all}}^*y$:
$y\cdot c_{\mathrm{all}}\le R_s\|g_s\|+h\|g_\theta\|_1+E_r\|D\circ y_D\|_F+
\frac{z^2}{2}\max(0,\max_{i,j}(-y_{D,ij}))+\frac{R_s^2}{2}(\|y_X\|+\|y_Y\|)$.
Status **M** (weight the 20 exact equations; the only subtlety is the sign of the quadratic term,
which is why the $\max(0,\cdot)$ appears).

**Corollary 3.10.** A cell with no feasible completion is certified if (3.26) fails or if some
$y$ violates (3.29); the direction may be found heuristically and normalised. Status **M**
(both are necessary conditions, and (3.29) is positively homogeneous in $y$).

**Proposition 3.11 (completion coverage).** Fix a seed ball with certified frames and constants.
If every terminal cell of the finite recursion is either excluded by a certified necessary test or
covered by a certified phase ball, then those balls cover all feasible completions of the seed, up
to the phase-ball equivalences. Status **M + S + C**: the induction is over the cell tree (a
representation can be followed into at least one child since children's closed intervals cover the
parent's), and the premises are the recursion terminating with zero unresolved cells (**S**, **C**).

**Code claims in §3.** `buildH::gen` supplies the residual and derivative (**S**); `eq` stacks
exactly the twenty equations of (3.28) (**S**); `trial::pass` proposes directions by regularised
solves and weight updates, and **only** `trial::certificate` excludes, after checking finiteness,
dividing by the largest coordinate, and using the negative part of $y_D$ (**S** — this is the one
place where the paper's description is exactly the guarantee the proof needs);
`Asearch::testA` is the used path while `Usearch::test` and "scalar routines" supply no exclusions
for this run (**S**, dead code in the certificate path).

---

## 4. Claims in §4 (Root certificates, atlas)

**Definition 4.1 (Root).** Data $(P,T,(C,n_0,id,ort,hor,mnorm,froot))$ with $T\in\mathbb{R}^{36\times k}$,
$0\le k\le10$, such that (4.4) holds and, for **every** horizontal $\delta$ with $F(P+\delta)=0$:
$\|(I-TT^*)\delta\|\le n_P(\|\delta\|)$, $n_P(s)=n_0+id\,s+Cs^2$; $\|\delta\|^2\le(1+ort)\|T^*\delta\|^2+
\|(I-TT^*)\delta\|^2$; and the difference bound (4.7) at any horizontal comparison point. Status:
**definition** (so its *satisfiability* is the substantive claim, Prop. 4.6).

**Remark 4.2.** $T$'s columns are numerical directions only; $\|T\|\le\sqrt{1+ort}$; no
constant-rank or manifold hypothesis is used. Status **M**.

**Lemma 4.3.** $F(P+x)=F(P)+L_Px+R_P(x)$ with $|(R_P(x))_{ij}|\le\pi a_{ij}(x)$,
$|(R_P(x)-R_P(v))_{ij}|\le\pi\sqrt{a_{ij}(x-v)}(\sqrt{a_{ij}(x)}+\sqrt{a_{ij}(v)})$; and if
$\sum_{i>j}w_{ij}(y)a_{ij}(x)\le b\|x\|^2$ for all horizontal $x$ and unit $y$, then
$\|MR_P(x)\|\le\pi b\|x\|^2$ and the difference version. Status **M** (the scalar
$r(t)=(e(t)-1-2\pi it)/(2\pi i)$ satisfies $|r|\le\pi t^2$ and $|r(x)-r(v)|\le\pi|x-v|(|x|+|v|)$).

**Lemma 4.4.** Two admissible remainder constants: $b=8\|M\|$ and $b=6\|S\|$, where $S$ is the
30×216 tensor map $S_{a,:}=M_{:,a}\otimes(e_i-e_j)^*$; hence $\pi$ times the smaller certified upper
bound is a valid $C$; the Gram $SS^*$ computable by the sign-factor formula (4.14). Status **M**
(uses $\sum_{i>j}a_{ij}=6s^2$, $\sum u_i^2\le\frac56s^4$, $\sum a_{ij}^2\le8s^4$).

**Proposition 4.5.** If (4.4) and (4.15) hold — $\|M\|\le mnorm$, $mnorm\cdot froot\le n_0$,
$\|\Pi-TT^*-ML_P\Pi\|\le id$ — and $C$ bounds $\pi b$, then the data are a certified Root.
Status **M** (the Taylor identity and the identity $\|\delta-T\eta\|^2\ge\|\delta\|^2-(1+ort)\|\eta\|^2$,
which needs no exact projectivity of $TT^*$).

**Proposition 4.6.** A successful `buildH::patch` certifies (4.4), (4.15) and a valid $C$, hence
produces Root data. Status **S + C**. This is the single most load-bearing claim in the paper about
code: it says that the direct checks (not the accuracy of the proposed eigendecomposition) establish
everything, with $M$ assembled from stored factors $H_VL_V^*$, its norm bounded by certified row
sums, and the optional tensor improvement accepted only through a checked change of basis $U$ with
$\beta<.1$. Verified only against A.5's budgets.

**Lemma 4.7 (equivalence transport).** For $\Phi$ a signed row/column permutation with optional
transpose and global sign: $\Phi$ is a real isometry commuting with $\Pi$, $\|F(\Phi P)\|=\|F(P)\|$
(via $\|AA^*\|_F=\|A^*A\|_F$ and $\|F(P)\|^2=(\|AA^*\|_F^2-216)/(8\pi^2)$), the Root assertions
transport with the same constants, and extendibility is preserved both ways. Status **M**.

**(4.17).** For centres $P,Q$ and an integer matrix $N$, $d=\Pi(D_0(P)-D_0(Q)-N)$ makes $e(Q+d)$
phase-equivalent to $e(P)$; and for horizontal $\delta$, $e(Q+d+\delta)\sim e(P+\delta)$. Status **M** —
this is what makes a fixed choice of integer lifts sufficient.

**Lemma 4.8 (arc and weighted-arc bounds).** From $\|Z\|_F\le z$, magnitudes $m_j=|D_j|>0$, a
nonnegative slack $\ge z^2-\sum_j(m_j-1)^2$, $m_i$ a lower bound for $\min_jm_j$, $q_d=\mathrm{slack}/m_i<3.8$:
$\|d\|\le \mathrm{arc}$ and $\sum_jm_jd_j^2\le\mathrm{weighted}$, with
$\mathrm{arc}\ge q_d^{1/2}(1-q_d/4)^{-1/2}$ etc. Status **M** (entrywise identity
$|D_j'-D_j|^2=(m_j-1)^2+m_j|D_j'-D_j^\circ|^2$, then $|\arcsin|\le\frac{t}{\sqrt{1-q_d/4}}$).

**Lemma 4.9 (stored centre and support representation).** On a successful `Candidate::prep` there is
$\epsilon$ with $\|\epsilon\|\le2\cdot10^{-6}$ (cycles) such that the feasible phase matrix is
$P_0+\epsilon+u/2\pi$, $\|u\|\le\sqrt{R_s^2+\mathrm{arc}^2}$, and
$u=X(s,\theta)+e_D+e_{\sin}$, $\|e_D\|\le E_r$, $\|e_{\sin}\|_1\le\mathrm{arc}^3/6$.
Status **M + S**. The mathematical content ($\Im(D_j^\circ Z_j)=\sin d_j$, $|d-\sin d|\le|d|^3/6$) is
clean; the $2\cdot10^{-6}$ budget rests on the checked unit-direction test and on the chord bound
$2\sin(\pi t)\ge4t$.

**Lemma 4.10 (direct displacement bound).** With $\Delta=\Pi(P_0-D_0(P)-N)$ and $S_\Delta=\min(S_1,S_2)$
as in (4.27)–(4.28): $\|\delta\|\le\big(\|\Delta\|^2+\frac{R_s^2+\mathrm{arc}^2}{(2\pi)^2}\big)^{1/2}
+\frac{S_\Delta}{\pi}+\|\epsilon\|$. Status **M**.

**Lemma 4.11 (ellipsoid containment).** $As+Bv$, $\|s\|\le r,\|v\|\le q$, lies in
$\{G^{1/2}w:\|w\|\le1\}$ whenever $G\succeq(1+\beta)r^2AA^*+(1+\frac1\beta)q^2BB^*$; holds for
singular $G$. Status **M** (support-function proof given, which is the right way round).

**Lemma 4.12 (offset ellipsoid norm bound).** For $G\succeq0$, $\gamma>\lambda_{\max}(G)$:
$\|U+G^{1/2}w\|^2\le\gamma(1+U^*(\gamma I-G)^{-1}U)$; also $\|U\|+\sqrt{\lambda_{\max}(G)}$; and for a
convex hull of offsets the largest bound at the vertices suffices. Status **M**.

**Proposition 4.13 (bootstrap).** If $s_0\ge\|\delta\|$ and $t_0\ge\|T^*\delta\|$ for all feasible
solutions of a cell, then replacing $s$ by $(n_P(s)^2+(1+ort)t_0^2)^{1/2}$ when that decreases $s$,
for any finite number of steps, preserves coverage. Status **M** (monotonicity of $n_P$, no
convergence claim).

**Definition 4.14, Lemma 4.15 (atlas merge).** A Record is a Root plus a radius; its solution set is
$\{e(P+\delta):\delta$ horizontal, $\|\delta\|\le r$, $F(P+\delta)=0\}$. If $d$ certifies
$\|\Pi(D_0(\Phi P)-D_0(Q)-N)\|\le d$ for an allowed $\Phi$ and integers $N$, the local Record is
covered by the Record at $Q$ with radius $r+d$. Status **M** (triangle inequality).

**Proposition 4.16.** If the seed cover is valid and the completion search processes all seeds with
no failed and no unresolved seed, the A-stage Records cover every exact second-basis Hadamard matrix
up to extendibility-preserving equivalence. Status **M + S + C**.

---

## 5. Claims in §5 (Stage B)

**Lemma 5.1.** For $A=I-TT^*$, $\zeta=T^*x$: $\|T\|\le\sqrt{1+o_P}$, $\|A\|\le1+o_P$,
$\|x\|^2\le(1+o_P)\|\zeta\|^2+\|Ax\|^2$, without horizontality. Status **M** (eigenvalue range
$[0,1+o_P]$ for $TT^*$).

**Proposition 5.2 (relation estimates).** With $d_q=\Pi(D_0Q-D_0P-N)$, $\eta_q=T^*d_q$,
$h'=\delta-d_q$, $\xi=T^*h'$, $\nu=Ah'$, and upper bounds $D\ge R+\|d_q\|$,
$v_0\ge n_P(R)+n_q$, $\lambda\ge\alpha_P+\gamma_PD$, $e_0\ge\mu_P\varepsilon_Q$,
$\sigma\ge\|(\Pi S)^*A\|$, $\beta=\sqrt{(1+o_P)(1+o_P)(1+o_Q)}$:
$d\le D$, $d^2\le(1+o_P)t^2+\|\nu\|^2$, $\|\nu\|\le\min\{v_0,(1+o_P)d,\lambda d+e_0\}$,
$\|S^*h'\|\le\beta t+\sigma\|\nu\|$, $d^2\le(1+o_Q)\|S^*h'\|^2+n_Q(d)^2$, whenever
$t\ge\|\xi\|$. Status **M**. This is the technical heart of Stage B: two Root certificates at
different centres bound the same exact solution.

**Lemma 5.3.** The iteration $b_0=\min\{D,\sqrt{z^2+v_0^2}\}$,
$b_{j+1}=\min\{b_j,\psi_P(b_j),\psi_Q(b_j)\}$ keeps every $b_j$ an upper bound for $d$ over all
parent solutions with $\|\eta-\eta_q\|\le t$; enlarging a proposal or stopping early is harmless.
Status **M** — no contraction, no fixed point.

**Lemma 5.4.** A returned threshold $\rho>10^{-7}$ certifies
$\|\eta-\eta_q\|\le\rho\Rightarrow[e(P+\delta)]\in S(Q,a)$; no monotonicity of $\hat D$ is needed
because the certificate is a single stored trial. Status **M + S** (the search protocol is code).

**Lemma 5.5.** For a tangent box $B(u,h)$, $\max_{\eta\in B(u,h)}\|\eta-\eta_q\|$ equals (5.24), and
hence $t_B\le\rho$ or $\hat D(t_B)\le r$ places all parent solutions of that box in $S(Q,r)$.
Status **M**.

**Lemma 5.6.** If a box is certified into $S(Q,r)$ with $r<\tau$, then either growing an existing
atlas radius by a certified aligned distance $\ell$ (staying $\le\tau$) or inserting $\Phi Q$ covers
it; later failures do not undo the assignment. Status **M**.

**Proposition 5.7 (Stage B coverage).** On a completed run,
$\bigcup_{\text{input}}S(P,R)\subseteq\bigcup_{\mathcal A}S(Q,r)\cup\bigcup_{B}S(P,R)$ where
$\mathcal A$ is the final atlas and $B$ the failed parents. Status **M + S + C**. The proof is two
finite inductions: on subdivision depth, and on the order of completed parents (a "blocker" is only
ever an *already completed* parent — the paper flags this distinction explicitly, and it is exactly
where a circularity would occur).

**Corollary 5.8.** If a batching invocation completes with no bad parents and every emitted batch is
included, the input solution sets are covered by the emitted records at radius $\tau$. Status
**M + S + C** (uses immutable insertion order and $\mathcal S(Q_i,r_i)\subseteq\mathcal S(Q_i,\tau)$).

---

## 6. Claims in §6 (Stage C)

**Lemma 6.1.** For a bin of the five free phases at resolution $M$, with $a=\frac1{2M}$, the centred
displacement $x$ satisfies $\sum_jx_j=0$, $\|x\|\le X_M=\sqrt{29/6}\,a$, $\|x\|_1\le5a$,
$\|x\|_\infty\le\frac32a$. Status **M** (convexity ⇒ vertex maximisation).

**Lemma 6.2.** With $\|x\|\le X$, $\|x\|_1\le L$, $\|\delta\|\le r$:
$\|S'-S\|\le2\pi(KX+r)$, $|S_i'-S_i|\le2\pi(L/\sqrt6+r)$, hence the necessary tests (6.7), where $K$
bounds $\|e(P)/\sqrt6\|_{\mathrm{op}}$ via $\|AA^*-6I\|_F=2\pi^2\|F(P)\|$. Status **M**.

**Lemma 6.3 (weighted Taylor).** For every $y\in\mathbb{R}^6$,
$|y\cdot(c+Jx-B\eta)|\le E(y;X,I)$ with $E$ as in (6.10), and the bin support inequality (6.11)
$|y\cdot c|\le a\sum_{j>0}|(J^*y)_j|+r_H\|B^*y\|+E(y;X_M,I_M)$. Status **M** — I checked the
$2\pi$/$4\pi$ normalisations of $c$, $J$, $B$, $D_O$, $D_U$ and the O/U residual constants
$\pi r_e^2$, $\pi r_e^2(1+|S|/6)$; they are consistent, which is not obvious on a first read.

**Scalar test (6.12)–(6.13).** Without the tangent decomposition,
$|c_i|\le a\sum_{j>0}|J_{ij}|+r\|J_{i,:}\|+\rho$ with $\rho$ the minimum of two remainder bounds.
Status **M**.

**Lemma 6.4 (certified clustering).** If each retained bin midpoint $u$ is assigned a centre $v$, an
integer lift $m$, and a radius $\ge\|h\|+X_M$ with $h$ the centred wrap of $u-v$, then $B_{\mathrm{vec}}(v,s)$
covers the whole bin up to global phase. Status **M + S** (the assignment is heuristic; the final
radius recomputation is what carries the proof).

**Lemma 6.5 (distinct labels).** Two vectors in one $B_{\mathrm{vec}}(v,s)$, $s<.1$, are neither
orthogonal nor unbiased; hence twelve vectors in two further MUBs occupy twelve distinct balls.
Status **M** — the numerical part is $6-2\pi\sqrt6\|z\|>6-\frac{22}{7}>\sqrt6$ with $\|z\|\le.2$;
I re-checked the constants.

**Lemma 6.6 (edge Taylor).** For two balls with radii $s_u,s_v$ and $r_e=s_u+s_v$:
$\|q_O+D_Oz\|\le\pi r_e^2$, $|q_U+D_Uz|\le\pi r_e^2(1+|S|/6)$, and the direct supports (6.20)–(6.21).
Status **M**.

**Lemma 6.7 (joint necessary support).** For one vector from each ball, both unbiased to the
coordinate basis and to the same second basis with displacement $\delta$: (6.23), where the shared
tangent term is $\|(B^0)^*y_0+(B^1)^*y_1\|$ — the single $\eta$ is what makes the joint test
stronger than two separate ones. Status **M**.

**Lemma 6.8 (complete graph search).** Mode-1 `graph::exist` returns false only if no configuration
(6.24) exists (two disjoint $O$-six-cliques with $A\times B\subseteq E(U)$); work-cap exhaustion
never gives a negative certificate. Status **S + M?**. This is the one lemma whose subject is an
algorithm rather than a set: its proof recites the least-vertex enumeration, the root-deletion
convention, the two-pool intersections and the auxiliary six-clique prune. It is therefore correct
*if the code is what the text says*, and the text is the only evidence.

**Proposition 6.9.** If Stage C returns a negative result for a Record, no exact Hadamard
$e(P+\delta)$ in its closed radius-$r$ ball is extendible by two further MUBs together with the
coordinate basis. Status **M + S + C**.

---

## 7. Claims in §7 and Appendix A

**Theorem 7.1 (finite-execution certificate).** With the seven specified sources, the arithmetic
conditions of Appendix A, and all terminal conditions of §7.2 (including provenance, batch and
fallback checks), no four MUBs exist. Status **C**: this is the composition lemma, and its proof is
the chain of §1 above. Its content is that the bookkeeping (counts, hashes, subsequence checks,
modulo partitions) is sufficient to identify the exact solution's record at every stage.

**Terminal conditions (§7.2).** Five numbered requirements: normal builds and a complete centre
file; four A exits 0 with empty bad files; two B exits 0 with zero-count bad files; each initial C
batch processed once with consistent counts; fallback covers every initial failure and the four
final C shards partition the fallback records. Status **S + E**.

**Finite bounds (§7.3).** Pre-filter tuple counts $\binom{116}{5}=160{,}389{,}488$ and
$\binom{115}{4}=6{,}913{,}340$; grid 64 has $64^4/8=2{,}097{,}152$ cells per seed; depth caps; atlas
and record caps; C's $12^5=248{,}832$ first-grid cells and $\le2048$ clusters with 32-word bitsets.
Status **M + E** — all reproduce exactly.

**Table 1 (the run).** 151,744,086 seed pairs → 249,878 centres; A0–A3 process 62,470/62,470/62,469/62,469
(=$249{,}878$) with 764/774/757/788 coarse records; B mid 3083→600; B fine 600→22,379 (88 batches
$=87\cdot256+107$); initial C 22,379 with 163 graph-cap failures; B fallback 163→1127; final C
282+282+282+281=1127; no unresolved records. Status **E**. The counts are mutually consistent (I
checked all of the above arithmetic), which is evidence of bookkeeping discipline, not of correctness.

**Table 2.** SHA-256 digests of eight principal data files. Status **E**, and *unverifiable here*:
the archive itself is not in the packet.

**Lemma A.1.** Dot products of length $m\le2000$ satisfy (A.3) with $\gamma_m=2.1\cdot10^{-16}(m+1)$;
power sums/norms satisfy (A.4). Status **S** (a statement about an arithmetic model).

**Lemma A.2 (unit exponential).** For $|x|\le16$, `expair` is within $2\cdot10^{-14}$ of $e(x)$ in
complex modulus; $\varepsilon_{\exp}=6\cdot10^{-14}$ suffices in all uses; and
$|\hat\pi-\pi|<1.225\cdot10^{-16}$ by Machin's identity, alternating-series bounds and exact rational
arithmetic. Status **S**, but the $\pi$ part is **M** and pleasant: it is a genuine certified
inequality, checkable without a computer algebra system.

**Lemma A.3.** `spectralUpper` returns an upper bound for $\|G\|$ for exact symmetric stored
$G$ with $k\le10$, $|G_{ij}|\le10$. Status **S**.

**The margin table (A.12).** For each certificate path, an established adverse error and an explicit
margin (e.g. C joint support $10^{-8}$ vs $3\cdot10^{-7}$). Status **S**; the numbers are consistent
with the bounds proved in the corresponding sections, but their derivation is not re-derivable
without the code.

---

## 8. What the claim stack actually says

Read as a whole, the paper establishes: **if** the seven programs do what §§2–6 say they do, **and**
the run of §7.5 completed with the stated terminal conditions, **then** $N(6)=3$. The mathematical
half is a correct and rather elegant necessity-and-cover argument; the empirical half is a
well-instrumented computation. The gap between them is exactly the content of the **S** tags above,
and it is concentrated in four places: `buildH::patch` (Prop. 4.6), the stage-B traversal and
blocker bookkeeping (Prop. 5.7), the Stage-C bin/cluster/edge machinery (Props. 6.4–6.9), and the
clique search (Lemma 6.8).
