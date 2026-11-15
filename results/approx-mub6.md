# Approximate mutually unbiased bases in dimension six

Working notes / research report. Every claim is labelled

* **THEOREM** — proved here, complete argument;
* **CERTIFIED** — rigorous, obtained from a computation that can be re-run: either exact
  rational arithmetic alone (the Cayley certificate of §7) or exact arithmetic plus the
  explicit perturbation lemma of §7;
* **NUMERICAL** — a computation, no global optimality claimed;
* **OPEN**.

Code and data are in `work/11-approx-mub/`, except the swarm members' artefacts, which are
under `.ultramath/smwgxagl5/m*/`.

---

## 1. The problem

For unitary $6\times 6$ matrices $U_1,\dots,U_4$ (orthonormal bases as columns) put

$$P^{ab}_{ij}=\bigl|(U_a^\dagger U_b)_{ij}\bigr|^2,\qquad
\operatorname{dev}(a,b)=\max_{i,j}\Bigl|P^{ab}_{ij}-\tfrac16\Bigr|,$$

$$\varepsilon_6^*=\min_{U_1,\dots,U_4\in U(6)}\ \max_{1\le a<b\le 4}\operatorname{dev}(a,b).$$

The reference preprint (OpenAI, 24 Sep 2026) proves that no four bases in $\mathbb C^6$ are
pairwise unbiased, so $\varepsilon_6^*>0$; it gives no value. The task is to bound
$\varepsilon_6^*$ from both sides and to describe the near-optimal configurations.

**Elementary facts used throughout.**  $P^{ab}$ is doubly stochastic (all row and column
sums equal $1$), so $P^{ab}=J/6+E^{ab}$ with $E^{ab}$ having zero row and column sums;
$\operatorname{dev}(a,b)\le 1/6$ always and $\operatorname{dev}(a,b)=1/6$ iff some entry
of $P^{ab}$ vanishes.  Gauges: $U_1:=I$, $U_a\mapsto U_aD_a$ with $D_a$ diagonal unitary,
and a global left unitary.  Effective dimension $3\cdot 36-18=90$.

---

## 2. Results

| # | Statement | Value | Status |
|---|---|---|---|
| 1 | upper bound from an exact algebraic quadruple | $\varepsilon_6^*\le \tfrac1{18}=0.0555555555555556$ | **THEOREM** |
| 2 | upper bound from an exact-rational certificate | $\varepsilon_6^*\le 0.030224240773$ | **CERTIFIED** |
| 3 | best value found in the numerical search | $0.0302242407724$ | **NUMERICAL** |
| 4 | optimum *within the product class* $U_a=A_a\otimes B_a$ | exactly $\tfrac1{18}$ (both bounds) | **THEOREM** |
| 5 | *real* bases: every pair has $\operatorname{dev}\ge \tfrac1{18}$; the pair optimum is $\tfrac1{12}$ (attained), the quadruple optimum $\approx0.1391$ | $0.0833$ / $0.1391$ | **THEOREM** / NUMERICAL |
| 6 | $\mu_6$-Butson bases: every pair has $\operatorname{dev}\ge\tfrac1{18}$; sharp at $\tfrac1{12}$ in the $F_6$ orbit | $\ge0.0556$, $=0.0833$ | **THEOREM** |
| 7 | cyclic slice $U_a=S^{a-1}$ | $0.053981857147$ | **CERTIFIED** |
| 8 | three exact MUBs + one free basis | $0.079832294321$ | **NUMERICAL** |
| 9 | diagonal-phase orbit $U_a=D_aF_6$ (25 restarts) | $0.0578759465$ | **NUMERICAL** |
| 10 | minimiser of the $\ell^2$ objective $E_2$ | $E_2=0.0512492189963$; $\max\operatorname{dev}=0.0422687210$ | **NUMERICAL**, certified |
| 11 | lower bound valid for *all* quadruples | none beyond $0$ | **OPEN** |

So the honest state of the quantitative question is

$$\boxed{\ 0\ <\ \varepsilon_6^*\ \le\ 0.030224240773\ }$$

and the three interesting structural facts are that (a) the product class is *not* where the
optimum lives — it is a factor $1.84$ worse than the best quadruple found — and (b) every
inequality built from two-body data is provably unable to improve the lower bound $0$
(§3), and (c) the arithmetic of root-of-unity classes alone forces a gap of $1/18$ (§5.2),
which is $1.84$ times the actual scale of the phenomenon.  The number $\varepsilon_6^*$
therefore measures a genuinely four-body, non-arithmetic obstruction.

---

## 3. Why pairwise inequalities cannot bound $\varepsilon_6^*$ from below

The task asks in particular "whether an inequality is capable of distinguishing four bases
in dimension six from exact MUB configurations in dimensions where four MUBs exist".
For the natural class of inequalities — anything that is a function of the two-body data —
the answer is a clean **no**, and it is worth stating as a theorem because it kills a whole
programme (Welch bounds, frame potentials, and every relaxation whose variables are the
Gram matrix of the 24 vectors or the six matrices $P^{ab}$ — note that *higher* moments
$Σ|⟨x,y⟩|^{2t}$, $t≥2$, do vary across quadruples and are not covered by the theorem; they
are the natural object left, cf. the $E_2$ discussion of §6.3).

**Theorem 3.1 (Welch/frame potential saturate identically).**
For *every* quadruple of orthonormal bases of $\mathbb C^d$,
$\sum_{a,i}|u^a_i\rangle\langle u^a_i|=4I$ and therefore
$$\sum_{x,y\in S}|\langle x,y\rangle|^2=\|4I\|_F^2=16d=\frac{N^2}{d},\qquad N=4d,$$
i.e. the frame potential of the $4d$ vectors *equals* the absolute Welch lower bound, for
all quadruples simultaneously.  Hence every inequality of the form
$\sum_{x,y}|\langle x,y\rangle|^{2}\ge N^2/d$ (and every "higher-order frame potential"
bound that is a function of the two-point function) is an identity on the feasible set.

*Proof.*  $\sum_i u^a_i u^{a*}_i=I$ for each basis; sum over the four bases.
$\|4I\|_F^2=16d$; and $(4d)^2/d=16d$. $\square$

**Theorem 3.2 (two-body data of a MUB quadruple is dimension-blind).**
Let $U_1,\dots,U_4$ be pairwise unbiased bases of $\mathbb C^d$ and put
$w^a_i=u^a_i u^{a*}_i-\tfrac1d I$ (traceless Hermitian).  Then
$$\langle w^a_i,w^b_j\rangle_{\mathrm{HS}}=P^{ab}_{ij}-\tfrac1d
=\delta_{ab}\Bigl(\delta_{ij}-\tfrac1d\Bigr),$$
so the Gram matrix of the $4d$ matrices $w^a_i$ is
$$\mathrm{diag}_{a=1..4}\bigl(I_d-\tfrac1d J_d\bigr)=:G_d .$$
$G_d$ is positive semidefinite of rank $4(d-1)$ and its non-zero spectrum is $1$, with
multiplicity $4(d-1)$, **for every $d$**; and $G_d$, divided by its diagonal entry
$1-1/d$, is the same matrix in every $d$ (it is $\mathrm{diag}(I_d-J_d/d)/(1-1/d)$,
i.e. the block-diagonal matrix whose blocks are the projectors onto the traceless
subspaces).  Consequently the *normalised* two-body data of an exact MUB quadruple — the
$P^{ab}$, the normalised Gram matrix of the $4d$ vectors, the normalised $4d$ projectors,
and every moment of order $\le 2$ — is literally the same array in $d=4$ and in any $d$
in which four MUBs exist; a hypothetical exact MUB quadruple in $d=6$ would be
indistinguishable from the $d=4$ one at the level of two-body data.

*Proof.*  $\langle u_iu_i^*,v_jv_j^*\rangle_{\mathrm{HS}}=|\langle u_i,v_j\rangle|^2=P_{ij}$;
$\langle u_iu_i^*,I/d\rangle=1/d$; $\langle I/d,I/d\rangle=1/d$; hence
$\langle w,w\rangle=P_{ij}-1/d$.  For $a\ne b$ and MUB, $P_{ij}=1/d$, giving $0$; for $a=b$
it gives $\delta_{ij}-1/d$.  The spectrum of $I_d-J_d/d$ is $1$ ($d-1$ times) and $0$. $\square$

**Corollary 3.3.**  No inequality in the two-body data can give a positive lower bound for
$\varepsilon_6^*$: any inequality that is a function of the normalised Gram matrix (hence
any inequality whose validity is certified by the two-body moment constraints alone,
including the level-1 Lasserre/PT-moment relaxations of the feasible set) holds equally in
$d=6$ and in $d=4$, and is therefore saturated in $d=6$ by the $d=4$ extremal data.  Any proof of $\varepsilon_6^*>0$ with a numerical
constant must use the three- and four-body structure of the problem (in the language of the
preprint: the Stage-C condition that the two six-cliques $O,U$ have all $36$ cross edges).

*Remark (explicit witness).*  The no-go can be made constructive: the two-body modulus Gram
relaxation is feasible at $\eta=0$ with an explicit PSD point of spectrum
$4,\ 1^{(20)},\ 0^{(3)}$ (found independently by swarm member m8), which is the
dimension-blindness of Theorem 3.2 in coordinates.

*Remark.*  The one place where two-body data does bite is when a *structural constraint
narrows the class*: for real bases (§5) or for product bases (§4) the two-body invariants
are not free, and there one gets genuine positive bounds.  This is exactly why
restricted-class theorems are the realistic target.

---

## 4. An exact construction: $\varepsilon_6^*\le 1/18$, and the product class is exactly $1/18$

### 4.1 The dictionary for $d=2$

For orthonormal bases $A=\{a_1,a_2\}$, $C=\{c_1,c_2\}$ of $\mathbb C^2$ let
$n_A,n_C\in S^2$ be the Bloch vectors of $|a_1\rangle\langle a_1|$,
$|c_1\rangle\langle c_1|$.  Then
$$|(A^\dagger C)_{ij}|^2=\frac{1+(-1)^{i+j}n_A\cdot n_C}{2},$$
so $\operatorname{dev}(A,C)=\tfrac12|n_A\cdot n_C|$: *for $d=2$ the pair deviation is
exactly one half of the modulus of the inner product of two points of $S^2$.*

Two consequences worth recording, because they are easy to get wrong.  (i) $\mathbb C^2$ has
**three** MUBs, not two: the eigenbases of the Pauli $X,Y,Z$ correspond to three mutually
orthogonal points of $S^2$ and are pairwise unbiased ($\operatorname{dev}=0$ exactly, checked;
this is $N(2)=d+1=3$).  It has no fourth, since four points of $S^2$ cannot be pairwise
orthogonal.  (ii) Four bases of $\mathbb C^2$ therefore force
$\max\operatorname{dev}\ge\tfrac12\cdot\tfrac13=\tfrac16$ (the tetrahedron), so
$\varepsilon_2^*=\tfrac16$, the extremal configuration being the regular tetrahedron (unique
up to relabelling and swapping the two vectors inside a basis, since equality forces every
$|n_a\cdot n_b|=\tfrac13$ and $\|G\|_F^2=\tfrac{16}{3}$): the $d=2$ analogue of the problem,
solved exactly.

### 4.2 The construction

Write $\mathbb C^6=\mathbb C^2\otimes\mathbb C^3$.

* $B_1,B_2,B_3,B_4$: the four MUBs of $\mathbb C^3$,  $B_a=F_3\,\mathrm{diag}(1,\omega^a,\omega^a)$
  for $a=0,1,2$ and $B_4=I_3$, $\omega=e^{2\pi i/3}$, $F_3$ the $3\times3$ Fourier matrix.
  (These are pairwise unbiased exactly — quadratic Gauss sums, $\bigl|\sum_k\omega^{k^2+mk}\bigr|^2=3$.)
* $A_1,\dots,A_4$: the four bases of $\mathbb C^2$ whose Bloch vectors are the vertices of a
  regular tetrahedron, $n_a\in\bigl\{(\pm1,\pm1,\pm1)/\sqrt3\bigr\}$ (even number of minus signs).
  Concretely $A(n)=\begin{pmatrix}\cos\frac\theta2&-e^{-i\varphi}\sin\frac\theta2\\
  e^{i\varphi}\sin\frac\theta2&\cos\frac\theta2\end{pmatrix}$, $\theta=\arccos n_z$,
  $e^{i\varphi}=(n_x+in_y)/\sqrt{n_x^2+n_y^2}$; for $n=(1,1,1)/\sqrt3$ this is
  $\cos\frac\theta2=\sqrt{\frac{1+1/\sqrt3}{2}}$, $\sin\frac\theta2=\sqrt{\frac{1-1/\sqrt3}{2}}$,
  $e^{i\varphi}=(1+i)/\sqrt2$ — all entries in $\mathbb Q(\sqrt2,\sqrt3,i)$.
* $U_a=A_a\otimes B_a$, $a=1,2,3,4$.

### 4.3 The construction is exact

**Theorem 4.3.**  The four bases $U_1,\dots,U_4$ are orthonormal and
$\operatorname{dev}(a,b)=\tfrac1{18}$ for all six pairs.  Hence
$\varepsilon_6^*\le \tfrac1{18}$.

*Proof.*  $|(U_a^\dagger U_b)_{(i,k),(j,l)}|^2=|(A_a^\dagger A_b)_{ij}|^2\,|(B_a^\dagger B_b)_{kl}|^2$.
For $a\ne b$ the $B$-factor is exactly $\tfrac13$, and the $A$-factor is $\frac{1\pm r}{2}$ with
$r=n_a\cdot n_b=-1/3$ (tetrahedron).  So $P\in\{\tfrac19,\tfrac29\}$ entrywise and
$\max\bigl|\tfrac19-\tfrac16\bigr|=\max\bigl|\tfrac29-\tfrac16\bigr|=\tfrac1{18}$. $\square$

**CERTIFIED / machine-checked.**  `work/11-approx-mub/exact_tetra.py` recomputes the $4\times4$
array of cross-Grams in SymPy over $\mathbb Q(\sqrt2,\sqrt3,i)$; the set of values of
$|(U_a^\dagger U_b)_{ij}|^2$ over all $6\times36$ entries is exactly $\{1/9,2/9\}$ and the
maximum deviation is exactly $1/18$.  `certify_bound.py tetra_u.npy` independently gives the
inclusion `CERTIFIED eps*_6 <= 0.055555555555564` from floating-point input alone.

### 4.4 The product class is exactly $1/18$

**Theorem 4.5.**  Let $U_a=A_a\otimes B_a$ ($a=1,2,3,4$) be arbitrary *product* bases of
$\mathbb C^2\otimes\mathbb C^3$.  Then
$$\max_{a<b}\operatorname{dev}(a,b)\ \ge\ \frac1{18},$$
with equality for the construction of §4.2.  Hence the optimum of the restricted problem
over product bases is exactly $1/18$.

*Proof.*  Fix a pair $(a,b)$ and let $r=n_{A_a}\cdot n_{A_b}\in[-1,1]$, so the $2\times2$
matrix $\alpha=|A_a^\dagger A_b|^2$ has entries $\frac{1\pm r}{2}$ and max entry
$\frac{1+|r|}{2}$.  Let $\beta=|B_a^\dagger B_b|^2$, doubly stochastic $3\times3$, so
$\max\beta\ge\frac13$.  Take the entry $(i_0,j_0)$ where $\alpha$ is maximal and
$(k_0,l_0)$ where $\beta$ is maximal; the corresponding entry of $P^{ab}=\alpha\otimes\beta$
satisfies $P\ge\frac{1+|r|}{2}\cdot\frac13=\frac{1+|r|}{6}$, hence
$\operatorname{dev}(a,b)\ge\frac{|r|}{6}$.  Now let $G=(n_a\cdot n_b)$ be the $4\times4$ Gram
matrix of the four Bloch vectors: $\operatorname{diag}G=1$, $\operatorname{rank}G\le 3$, so
$$\sum_{a<b}r_{ab}^2=\frac{\|G\|_F^2-4}{2}\ \ge\ \frac{(\operatorname{tr}G)^2/3-4}{2}
=\frac{16/3-4}{2}=\frac23,$$
hence $\max_{a<b}|r_{ab}|\ge\sqrt{(2/3)/6}=\tfrac13$, and the pair attaining it has
$\operatorname{dev}\ge\tfrac16\cdot\tfrac13=\tfrac1{18}$. $\square$

*Scope.*  The theorem is stated for bases of the grid form $\{a_i\otimes b_j\}$, but nothing is
lost: **every** orthonormal basis of $\mathbb C^2\otimes\mathbb C^3$ consisting of product
vectors is such a grid.  (Proof sketch: group the six vectors by the ray of their $\mathbb C^2$
factor.  Vectors in one group have pairwise orthogonal $\mathbb C^3$ factors, so a group has
at most $3$ elements; two groups whose $\mathbb C^2$ rays are not orthogonal must have all
their $\mathbb C^3$ factors cross-orthogonal.  The only admissible multiplicity pattern of the
six vectors is $3+3$: $3+1+1+1$ and $3+3$ with a $3$-group already forces three mutually
orthogonal factors spanning $\mathbb C^3$, killing every other vector; $2+2+2$ and $2+2+1+1$
force four mutually orthogonal vectors in $\mathbb C^3$; $1^6$ forces one of the $\mathbb C^3$
factors to vanish.  Hence the two $\mathbb C^2$ rays are orthogonal and the basis is a
$2\times3$ grid.)  So Theorem 4.5 covers *all* product bases.  (Swarm member m2.)

*Remarks.*  (i) The inequality $\sum_{a<b}r^2\ge 2/3$ is the rank-$3$ Welch bound for four
points of $S^2$; equality holds iff the four points are the regular tetrahedron, so the
extremal configuration of the theorem is unique up to a rotation and relabelling.
(ii) The same argument in $\mathbb C^{d_1}\otimes\mathbb C^{d_2}$ gives: for four product
bases, $\max\operatorname{dev}\ge \frac1{d_2}\cdot\frac1{2}\cdot c_{d_1}$, where
$c_{d_1}$ is the best constant for four points in the appropriate Grassmannian; for
$\mathbb C^2\otimes\mathbb C^{d}$ this gives $\frac1{6d}$ and is attained whenever $\mathbb C^d$
has four MUBs (i.e. $d=3$).
(iii) **The product class is far from optimal**: $1/18=0.0556$ against $0.0302$ for a generic
quadruple (§6).  Product bases are, in this problem, a bad ansatz — the opposite of the
situation for exact MUBs, where all known extremal sets in prime-power dimensions are
Hadamard-orbit objects.

---

## 5. Real bases: every pair already has deviation $\ge 1/18$

**Theorem 5.1.**  Let $d\equiv2\pmod 4$, $d\ge6$, and let $U,V$ be real orthogonal $d\times d$.
Then
$$\max_{ij}\Bigl||(U^TV)_{ij}|^2-\tfrac1d\Bigr|\ \ge\ \frac{2}{d^2}.$$
For $d=6$: every pair of real orthonormal bases has $\operatorname{dev}\ge\frac1{18}$, hence
every quadruple of real bases has $\max_{a<b}\operatorname{dev}(a,b)\ge\frac1{18}$; i.e.
$\varepsilon_6^{*,\mathbb R}\ge 1/18$.

*Proof.*  Write $W=U^TV$, real orthogonal, $W_{ij}=s_{ij}m_{ij}$ with $s_{ij}=\pm1$,
$m_{ij}\ge0$.  Let $\varepsilon=\max|m^2_{ij}-1/d|$ and $m_{ij}=(1+\delta_{ij})/\sqrt d$ with
$|\delta_{ij}|\le D:=\sqrt{1+d\varepsilon}-1$ (so $2D+D^2=d\varepsilon$).  Row orthogonality
$\sum_kW_{ik}W_{jk}=0$ ($i\ne j$) gives, after multiplying by $d$,
$$0=\sum_k s_{ik}s_{jk}(1+\delta_{ik})(1+\delta_{jk})
\ \Longrightarrow\ \Bigl|\sum_k s_{ik}s_{jk}\Bigr|\le\sum_k(2D+D^2)=d\cdot d\varepsilon=d^2\varepsilon .$$
The left side is an integer (a sum of $d$ signs).  If the sign matrix $S=(s_{ij})$ were a real
Hadamard matrix then $SS^T=dI$; but real Hadamard matrices of order $d\equiv2\pmod4$,
$d\ge6$, do not exist ($d$ must be $1,2$ or $\equiv0\pmod4$).  Hence for some $i\ne j$ the
sum is a non-zero even integer, so $2\le d^2\varepsilon$. $\square$

### 5.2 Other restricted classes (all rigorous or certified)

| class | result | source |
|---|---|---|
| product $A\otimes B$ (all product bases, by the scope lemma) | exactly $1/18$ | Thm 4.5 (five independent derivations) |
| real orthogonal | every pair $\ge1/18$ | Thm 5.1 |
| $\mu_6$-Butson (entries in $\frac1{\sqrt6}\mu_6$) | every pair $\ge1/18$; best pair in the $F_6$ orbit $=1/12$ exact | Thm 5.2 below |
| cyclic $U_a=S^{a-1}$ | $\varepsilon_{\rm cyc}\le0.053981857147$ (certified) | §5.3 |
| MUB triple fixed, 4th basis free (standard product triple) | $0.0809327829$ certified; exactly $\sqrt3/18=0.0962250$ if the 4th basis is also a product | **CERTIFIED** / **THEOREM** |
| diagonal orbit $D_aF_6$ | $0.0578759465$ | numerical, 25 restarts |
| $\mu_{12}$ Fourier orbit $\{DF_6:D\in\mu_{12}^6\}$ (exhaustive over $12^5$ phase vectors, exact in $\mathbb Z[\zeta_{12}]$) | $k$ bases: $0$ ($k=2$, exact unbiased pair), $1/12$ ($k=3$), $1/9$ ($k=4$) — exact optima | **THEOREM** |
| quaternionic ($T$-invariant bases, $\mathrm{Sp}(3)\subset U(6)$, 21 params) | pairs unbiased; best 3 bases $0.0251$, best 4 bases $0.0778$ (min/median/max $0.0778/0.0921/0.1020$) | numerical, 26 restarts — **dead end** |

**Theorem 5.2 ($\mu_6$-Butson quantisation).**  Let $U,V$ be unitary $6\times6$ with all
entries of modulus $1/\sqrt6$ lying in $\frac1{\sqrt6}\mu_6$.  Then
$\operatorname{dev}(U,V)\ge\frac1{18}$, and no such pair is exactly unbiased.

*Proof.*  $X_{ij}=\sum_k\overline{U_{ki}}V_{kj}=z_{ij}/6$ with $z_{ij}$ a sum of six 6th roots,
so $z_{ij}\in\mathbb Z[\omega]$, $\omega=e^{2\pi i/3}$, and $P_{ij}=N_{ij}/36$ with
$N_{ij}=|z_{ij}|^2=a^2-ab+b^2\in\mathbb Z_{\ge0}$ (the norm form of $\mathbb Z[\sqrt{-3}]$).
The 462 multisets of six 6th roots realise the values
$\{0,1,3,4,7,9,12,13,16,19,21,25,27,28,31,36\}$ and $6$ is not among them (the prime $2$ is
inert in $\mathbb Q(\sqrt{-3})$, and $2$ divides $6$).  If $\operatorname{dev}<\frac1{18}$ then
$|N_{ij}-6|<2$ for all entries, so $N_{ij}\in\{5,6,7\}$, hence $N_{ij}=7$ for all $36$ entries;
but $X$ is unitary, so the rows of $P$ sum to $1$, i.e. the rows of $N$ sum to $36$, not
$6\cdot7=42$.  Contradiction.  (The same argument with $\mu_4$ uses $a^2+b^2$ and gives
$\ge1/18$; with $\mu_2$ it reproduces Theorem 5.1; with $\mu_3$ it gives $\ge1/12$.  In
$d=3,4$ the analogous obstruction is absent since $3=|2+\omega|^2$ and $4=|2|^2$.)
$\square$

The constant $1/12$ is attained *exactly* inside the class: $U=F_6$,
$V=\mathrm{diag}(\zeta_6^{0,0,0,2,4,2})F_6$ have overlap numerators $\{3,9\}$ only.

### 5.3 The cyclic slice beats $1/18$

For $S\in U(6)$ put $U_a=S^{a-1}$; then $U_a^\dagger U_b=S^{b-a}$, so the six pair matrices
collapse to $|S|^2,|S^2|^2,|S^3|^2$ and
$\varepsilon_{\rm cyc}=\min_S\max_{k\le3}\max_{ij}\bigl||(S^k)_{ij}|^2-\tfrac16\bigr|$
is an upper bound for $\varepsilon_6^*$ on a $34$-real-dimensional slice.  It contains the
MUB obstruction exactly (four MUBs in the slice $\iff$ some $S$ has $S,S^2,S^3$ all flat).
An explicit $S$ gives, in exact rational arithmetic,
$$\varepsilon_{\rm cyc}\le0.053981857136640353,\qquad\text{hence}\qquad
\varepsilon_6^*<\tfrac1{18}.$$
So even the cheapest symmetry slice does better than the best product quadruple.

### 5.4 An exact MUB triple in $\mathbb C^6$

$U_1=I$, $U_2=F_6$, $U_3=\mathrm{diag}(e^{-i\pi l^2/6})_{l=0..5}F_6$ are pairwise unbiased
(exactly; $d_l=e^{-2\pi il^2/12}$ is a **Zadoff–Chu / CAZAC** sequence of length 6, flat
spectrum, so $F_6^\dagger\mathrm{diag}(d)F_6$ is Hadamard).  Note the 12th root: the naive
6th-root dephasing $\mathrm{diag}(\omega^{al^2})F_6$, $\omega=e^{2\pi i/6}$, gives
$\operatorname{dev}=\tfrac16$, not $0$ — checked for all $a$.  This is the same phenomenon as
Theorem 5.2 ($\mathbb Z[\zeta_{12}]\cap\mathbb R=\mathbb Z[\sqrt3]$ is bigger than
$\mathbb Z$, so six 12th roots can sum to $\sqrt3(1+i)$ with $|z|^2=6$).

*Remarks on Theorem 5.1.*  (i) The bound is intrinsic to each pair: over $\mathbb R$ there is not even an
approximately unbiased *pair* once $\varepsilon<2/d^2$; the whole obstruction of the
complex problem is absent from the real one, and the complex phases are what allow
$0.0302\ll 1/18$.
(ii) $1/18$ is **not** attained over $\mathbb R$.  The real pair optimum is
$1/12=0.0833$: two real bases with $P$ taking only the values $\{1/12,1/4\}$ exist and are
exact (entries $\pm\tfrac12,\pm\tfrac{\sqrt3}{6}$, checked in $\mathbb Q(\sqrt2,\sqrt3)$), and
three real bases with *all three* pairwise deviations equal to $1/12$ exist as well.
Numerically the optimum for two real bases is $1/12$ (81 restarts, none lower) and for four
real bases it is $0.1390615033$ (certified $\le0.1390616$; **NUMERICAL** optimality).  So the
real problem is a factor $1/12\div0.0302=4.6$ worse than the complex one, and the parity
bound of Theorem 5.1 is off by a factor $1.5$ ($\tfrac1{12}$ vs $\tfrac1{18}$) even for a
single pair.  (Swarm member m7.)

---

## 6. Numerical search

### 6.1 Method

`work/11-approx-mub/mubopt.py`.  Gauge $U_1=I$; the variables are $U_2,U_3,U_4\in U(6)$
(90 real parameters after the diagonal gauge).  The minimax objective is smoothed by
$$\mathrm{LSE}_\beta\bigl(|D|\bigr)=\max|D|+\beta^{-1}\log\sum_k e^{\beta(|D_k|-\max|D|)}
-\beta^{-1}\log 216,\qquad D_k=P^{ab}_{ij}-\tfrac16,$$
and minimised by Riemannian gradient descent with backtracking, continuing
$\beta=30\to3\cdot10^5$ (up to $10^9$ for the final polish).  The Riemannian (body)
gradient is computed analytically: with $M^{ab}_{ij}=w^{ab}_{ij}\operatorname{sign}(D^{ab}_{ij})
\overline{X^{ab}_{ij}}$, $X^{ab}=U_a^\dagger U_b$,
$$G_a=\sum_{b>a}U_b (M^{ab})^{\!\top},\qquad G_b=\sum_{a<b}U_a\overline{M^{ab}},\qquad
\nabla_a=\bigl(U_a^\dagger G_a\bigr)-\tfrac12\bigl(U_a^\dagger G_a+(U_a^\dagger
G_a)^\dagger\bigr),$$
and the retraction $U_a\mapsto U_a\exp(-\eta\nabla_a)$.  The gradient was checked against
central finite differences on all $108$ generators: maximum discrepancy $1.7\times10^{-10}$
(`run_ms.py:gradcheck`, `mubopt.py` for the $E_2$ gradient, $8.4\times10^{-10}$).
Random unitaries are drawn by QR of a complex Gaussian (Haar).

### 6.2 Results

* 300 random restarts with moderate polishing: minimum $0.031382$, median $0.066900$,
  maximum $0.081381$.  The basin of the good configurations is *rare* (2 of 300).  An
  independent 240-restart sweep by the swarm (7 seed families, exchange-LP polish on the true
  max) reaches $0.0302242408$ with all six pairs tied to $6\cdot10^{-6}$; that is the best
  value known and is the one certified in §7.
* Basin hopping from the best point (perturbations of size $3\cdot10^{-3}$ to $3\cdot10^{-1}$,
  re-polished): all scales converge to the same point,
  $$\varepsilon_{\mathrm{num}}=0.0302377998905\ldots,\qquad E_2=0.1410938477 .$$
  The value is stable to $10^{-9}$ over independent perturbations, so it is a genuine local
  minimum of the nonsmooth objective, not an artefact of under-convergence.  A longer run
  (120 basin hops at five scales, 40 tetrahedral-product seeds, 80 fresh random starts) ends
  with **every** one of its 240 polished points inside $[0.0302377890,\ 0.0302378006]$ once
  it is in this basin, i.e. the basin is a single point to $10^{-9}$ — the difficulty of the
  problem numerically is *finding* the basin, not resolving the minimum.
* The deviation matrix at that point (rows/columns ordered $1,2,3,4$):

```
       0          0.02355143  0.02814959  0.02353907
       0.02355143 0          0.03023780  0.03023780
       0.02814959 0.03023780 0          0.03023780
       0.02353907 0.03023780 0.03023780 0
```

  Three pairs sit exactly on the maximum; the *global* maximum is attained at only $6$ of
  the $216$ entries.  Bases $2$ and $4$ have identical modulus patterns
  ($|(U)_{ij}|\sqrt6\in[0.9267,1.0683]$ for both), so the configuration looks like it has a
  $\mathbb Z_2$ symmetry exchanging them and fixing basis $3$; the moduli are
  $[0.9116,1.0812]$ for basis $3$.  The near-optimal configurations are *not* Hadamard:
  the moduli vary by $\pm8\%$, so the optimum balances modulus deviation against phase
  deviation — it does not sit on the Hadamard manifold.
* *Why the minimiser sits slightly off every exact MUB pair.*  Fixing a MUB triple and
  optimizing only the fourth basis costs a factor $2.7$: for the standard product triple the
  completion value is $0.0809327829$ (certified), and it is exactly $\sqrt3/18=0.0962250$ if
  the fourth basis is also required to be a product (exact, attained).  Restricting to *three*
  exact MUB pairs is worse still: the $\ell^2$ minimiser of §6.3 has three exact MUB pairs and
  pays $0.0423$.  So the unconstrained optimum must break the exact MUB pairs and spread the
  bias over all six — which is exactly what the deviation matrix above shows.
* Restricted class, diagonal-phase orbit $U_a=D_aF_6$ ($a=2,3,4$, $D_a$ diagonal unitary;
  $15$ real parameters, $25$ restarts each): best $\max\operatorname{dev}=0.0578759465$,
  i.e. *worse* than the tetrahedral $1/18=0.05556$.  (This is the class in which the
  prime-power MUB construction lives; in $d=6$ it collapses.)

### 6.3 The $\ell^2$ objective $E_2$ has a *different* minimiser

$E_2=\sum_{a<b}\sum_{ij}(P^{ab}_{ij}-\frac16)^2=\sum_{a<b}\bigl(\|P^{ab}\|_F^2-1\bigr)$
(the second equality is exact: $\sum_{ij}P_{ij}=6$ and $\sum_{ij}P_{ij}^2=\|P\|_F^2$
give $\|P-J/6\|_F^2=\|P\|_F^2-1$).  So $E_2\ge0$ with equality iff all pairs are exactly
unbiased, and the trivial bound is sharp for a *pair*.

400 random restarts of the $E_2$ gradient flow all converge to (an independent 30/30 restart
sweep by the swarm lands on the same number to 12 digits)
$$E_2=0.0512492189963,\qquad \max_{a<b}\operatorname{dev}(a,b)=0.0422687210 .$$
The minimiser has a striking structure: $U_1=I$ and $U_2,U_3,U_4$ are **exactly Hadamard**
(all $|$entries$|=1/\sqrt6$, unitarity defect $3\cdot10^{-15}$), the three pairs
$(1,a)$ are **exactly unbiased**, and the three remaining pairs all have
$\operatorname{dev}=0.0422687210$ (each contributing $0.0170830730$; $3\times0.0170830730
=0.0512492190$).  So the $\ell^2$ minimiser is "three exact MUBs plus three mutually
compromising Hadamards", while the minimax minimiser of §6.2 breaks the exact MUB pairs to
spread the error — the standard phenomenon that $\ell^2$ and $\ell^\infty$ regularisations
of a minimax problem have different minimisers.  Quantitatively:
$\max\operatorname{dev}$ at the $E_2$ minimiser is $0.0423$, i.e. $40\%$ worse than
$0.0302$; and $E_2$ at the minimax point of §6.2 is $0.1411$ ($2.75$ times the minimum; the swarm's
slightly better minimax point has $E_2=0.1656$, so the ratio depends on which minimax local
minimum one takes — the *minimisers differ* is the robust statement, not the ratio).
Because $\max\operatorname{dev}\ge\sqrt{E_2/216}$, any lower bound $E_2\ge c$ would give
$\varepsilon_6^*\ge\sqrt{c/216}$ — but since $E_2\ge0$ is sharp for pairs, no such bound is
available either (same obstruction as §3).

### 6.4 A pitfall worth recording

A natural-looking restricted class — "all four bases Hadamard, optimise the $3\times36$
phases of $\exp(i\theta_{kj})/\sqrt6$" — gives spectacularly small values
($0.0053$, then $0.0041$ after unconstrained polishing).  **These are artefacts**: a matrix
with all entries of modulus $1/\sqrt6$ need not be unitary, and $\exp(i\theta)/\sqrt6$ is
in general *far* from unitary ($\|U^\dagger U-I\|_F\approx1.0$).  The objective
$|(U_a^\dagger U_b)_{ij}|^2-\frac16$ is meaningless then (the $P^{ab}$ are not even doubly
stochastic).  The assertion in `certify_bound.py` ("unitarity defect $<1/100$") is what
caught this.  Lesson: in this problem every candidate must be certified unitary *before* any
deviation is quoted; a phase-only parametrisation of "Hadamard bases" is only legitimate if
orthogonality is imposed, which is exactly the hard constraint.

---

## 7. Certification of the numerical bound

`work/11-approx-mub/certify_bound.py FILE.npy` turns any stored quadruple of complex
$6\times6$ float64 matrices into a rigorous upper bound on $\varepsilon_6^*$.  The chain:

1. **Exactness.**  Every float64 number is a dyadic rational; all $8\cdot36$ real and
   imaginary parts are converted to `fractions.Fraction`.  The Gram matrices
   $G_a=U_a^*U_a$ and all cross-Grams $\langle u^a_i,u^b_j\rangle$ are computed in
   $\mathbb Q(i)$ *exactly*, as are the $216$ numbers $q^{ab}_{ij}=|\langle u^a_i,u^b_j\rangle|^2$.
2. **Polar correction.**  If $\|G_a-I\|_2=\eta_a<1$ and $V_a=U_aG_a^{-1/2}$, then $V_a$ is
   exactly unitary and $\|V_a-U_a\|_2\le\sqrt{1+\eta_a}\bigl((1-\eta_a)^{-1/2}-1\bigr)$.
   The script uses the (rational) bound $\Delta\ge2\max_a\eta_a$, valid for $\eta_a\le1/2$.
3. **Perturbation.**  For unit vectors $v,v'$ and $u,u'$ with $\|u-v\|,\|u'-v'\|\le\Delta$:
   $\bigl||\langle u,u'\rangle|^2-|\langle v,v'\rangle|^2\bigr|\le( \sqrt q+C)^2-q$ with
   $C=2\Delta+\Delta^2$, and q bounded by exact rational square-root enclosures.
4. Taking the maximum over $6\times36$ entries and subtracting $\frac16$ gives an exact
   rational upper bound; only the final printing is floating point.

Output on the stored data:

| file | exact max deviation of the given (rounded) matrices | certified $\varepsilon_6^*\le$ |
|---|---|---|
| `tetra_u.npy` | $0.055555555555556$ | $0.055555555555564$ |
| `best_hard.npy` | $0.031248403474735$ | $0.031248403476123$ |
| `e2best.npy` | $0.042268721005460$ | $0.042268721005524$ |
| `best2.npy` | $0.030237799890528$ | $0.030237799893315$ |
| m6's quadruple (`candidates_U.txt`) | $0.030224240772443$ | $\mathbf{0.030224240772506}$ |

The loss with respect to the raw value is $\sim10^{-12}$, entirely from step 2 with
$\eta\approx10^{-13}$; feeding exactly-unitary input (the tetrahedral construction) gives
loss $1.6\times10^{-14}$.

**A cleaner route, no error budget at all (swarm member m6).**  Write every basis as a
*Cayley transform* $U_a=(I-iA_a)^{-1}(I+iA_a)$ of a **rational Hermitian** $A_a$.  Then $U_a$
is exactly unitary (Cayley maps Hermitian to unitary) and has exactly rational complex
entries, so $P^{ab}_{ij}$, and hence $\operatorname{dev}(a,b)$, are *exact rationals*: no
perturbation lemma, no interval arithmetic.  The certificate is the list of the four rational
$A_a$; recomputing it (`m6/exact_verify.py`, standard library only) gives
$$\max_{a<b}\operatorname{dev}(a,b)=0.03022424077244261561\ \Longrightarrow\
\varepsilon_6^*\le \frac{302243}{10^{7}}=0.0302243 .$$
Running my independent certifier on the same quadruple gives $0.030224240772506$, consistent;
the two methods agree to $10^{-13}$.  This is the recommended way to state the bound.

---

## 8. What is missing: a lower bound

**OPEN.**  No $c>0$ is known with $\varepsilon_6^*\ge c$.  By §2 the gap is at most
$0.0302243$; the restricted-class bounds of §5 give $1/18$ only under extra hypotheses
(product, real, $\mu_6$-Butson, cyclic), and every such hypothesis is genuinely restrictive
because a generic quadruple beats all of them.  What would be needed:

1. A *quantitative* form of the preprint's Stage-C exclusion: the preprint excludes every
   box of an adaptive covering of the space of near-MUB quadruples; a stability constant
   would require re-running the covering with a slack parameter $\eta$ and showing that the
   excluded set contains the whole $\eta$-neighbourhood of the exact-MUB variety.  Since the
   Stage-C radii are of order $10^{-2}$ (layers $M=12,24,48,96$, radius $(.042-1.11w)^2$),
   and the numerical optimum is $0.030$ — the same order — such an extraction is delicate
   but not hopeless: it would give $c$ of order the Stage-C final radius.
2. Alternatively a *four-body inequality*: by Corollary 3.3 the inequality must involve
   triple or quadruple inner products, e.g. quantities of the form
   $\sum_{i,j,k}|(U_a^\dagger U_b)_{ij}|^2|(U_b^\dagger U_c)_{jk}|^2|(U_c^\dagger U_a)_{ki}|^2$
   (which are traces of products and hence algebraic in the entries), or the rank-one
   constraint $w^a_i+I/6\succeq0$ with $\operatorname{rank}1$ in a moment relaxation of
   order $\ge4$.  A Lasserre relaxation of order $4$ in the $90$ effective parameters has a
   monomial space of size $\binom{90+4}{4}\approx2.9\cdot10^6$; with the $U(1)^6$ and
   permutation symmetries it may be reducible, but not by us here.

---

## 9. Quantum-information reading (exact statements)

**(a) Outcome bias.**  If $\operatorname{dev}(a,b)\le\varepsilon$ then for every basis state
$|\psi\rangle=u^a_i$ of basis $a$, the measurement in basis $b$ gives
$p_j=|\langle v_j|\psi\rangle|^2\in[\frac16-\varepsilon,\frac16+\varepsilon]$, so the ratio
of the most to the least likely outcome is at most
$$\frac{1+6\varepsilon}{1-6\varepsilon}.$$
For $\varepsilon=1/18$ this ratio is $\le2$; for our best rigorous bound $\varepsilon=0.0302243$
it is $\le1.444$.
Nothing else in the problem is needed: this is the exact content of the deviation for the
statistics of a single state.

**(a') Entropic uncertainty, sharp.**  Since $\max_{ij}P^{ab}_{ij}\le\frac16+\varepsilon$, the
Maassen–Uffink inequality applied to the two orthonormal bases $a,b$ gives, for **every**
state $\rho$,
$$H(p^a)+H(p^b)\ \ge\ -\log_2\Bigl(\max_{ij}P^{ab}_{ij}\Bigr)\ \ge\ -\log_2\Bigl(\tfrac16+\varepsilon\Bigr),$$
with $H$ the Shannon entropy of the outcome distribution.  For $\varepsilon=0$ this is the
classical bound $\log_2 6$.  With the certified $\varepsilon=0.0302243$ one gets
$H(p^a)+H(p^b)\ge2.344$ bits for all six pairs and all states (for the tetrahedral quadruple
the bound at $\varepsilon=1/18$ is $\log_2(27/4)=2.755$ bits and is *not* saturated — the
entropic bound is only tight for the pair of bases, not for the quadruple).

**(b) Sequential measurements.**  On the maximally mixed state, the joint distribution of
the outcome pair $(i,j)$ from measuring first in basis $a$ and then in basis $b$ is
$\Pr(i,j)=\frac16\operatorname{Tr}(\Pi^a_i\Pi^b_j)=\frac16P^{ab}_{ij}$, i.e.
$\frac1{36}(1+6E^{ab}_{ij})$ with $|E^{ab}_{ij}|\le\varepsilon$.  Hence the total variation
distance from the uniform distribution on $36$ outcomes is
$$\mathrm{TV}\le\tfrac12\cdot36\cdot\frac{6\varepsilon}{36}=3\varepsilon,$$
and the min-entropy of the pair is at least $\log_2\frac{36}{1+6\varepsilon}$.  So a bound
$\varepsilon\le0.03024$ certifies that two consecutive projective measurements in any two of
the four bases are uniform to within $0.0907$ in total variation.

**(c) Tomography: a negative but exact statement.**  Four bases give $4\times6=24$
probabilities with $4$ sum constraints, i.e. $20$ real numbers — fewer than the $35$
parameters of a density matrix on $\mathbb C^6$.  So *no* quadruple, unbiased or not, is
tomographically complete; the deviation $\varepsilon$ therefore cannot be a tomographic
condition number.  What approximate unbiasedness does control is the *uniformity* of the
"basis-change" statistics: the exact identity for a complete set of $d+1$ MUBs,
$\sum_{a=1}^{d+1}\sum_i p^a_i\Pi^a_i=\rho+\operatorname{Tr}(\rho)I$, holds because the
$d(d+1)$ vectors form a tight projective $2$-design; with only $4<7$ bases the design
condition fails by an amount controlled by $\varepsilon$ only if all $\binom72$ pairs are
controlled, which is exactly the impossible configuration.  This is the precise sense in
which "approximate MUBs do not give approximate tomography".

**(d) Experimental simplicity.**  Our best configurations (§6.2) have no product or
group-covariant structure: the moduli vary by $8\%$ and the phases are generic.  Exact MUB
sets in $d=4,5$ are group-covariant (Pauli/Heisenberg–Weyl orbits of a single fiducial) and
are therefore easy to implement; the near-optimal $d=6$ quadruples are *less* structured, so
the quantitative obstruction does not come with a cheap experimental substitute.

---

## 10. Mapping onto the requested outputs

| Requested | Delivered | Status |
|---|---|---|
| 1. strongest numerical candidate | best: the swarm's quadruple `.ultramath/smwgxagl5/m6/candidates_{U,A}.txt`, $\max\operatorname{dev}=0.0302242407724$; an independent one: `best2.npy`/`best2_matrices.txt`, $0.0302377998905$ | NUMERICAL |
| 2. explicit matrices / compact parametrisation | (a) the tetrahedral construction: closed form in §4.2, exact algebraic; (b) the numerical quadruple as 4 unitaries, 17 digits, `best2_matrices.txt` | THEOREM / NUMERICAL |
| 3. certified upper bound | $\varepsilon_6^*\le0.030224240773$ (Cayley, exact rational; independently $\le0.030237799893315$ by §7) and $\le1/18$ exactly | CERTIFIED / THEOREM |
| 4. nontrivial lower bound | $\ge1/18$ within the product class (§4.4) and for real bases (§5); no general bound | THEOREM / OPEN |
| 5. structural theorem | Corollary 3.3 (two-body data is blind); Theorem 4.5 (product class); Theorem 5.1 (parity); §6.3 ($\ell^2$/$\ell^\infty$ minimisers differ) | THEOREM / NUMERICAL |
| 6. quantum-information reading | §9, items (a)–(d), all identities exact | THEOREM |

---

## 11. Files and reproduction

All in `work/11-approx-mub/`.

| file | what it does |
|---|---|
| `mubopt.py` | the optimiser: $P^{ab}$, $\max\operatorname{dev}$, $E_2$, analytic Riemannian gradient (LSE and $E_2$), retraction, line search |
| `run_ms.py` | gradient check + random multi-start driver |
| `search2.py` | basin hopping around a stored point |
| `tetra.py`, `exact_tetra.py` | the tetrahedral construction; SymPy exact verification that the cross-Gram moduli squared are exactly $\{1/9,2/9\}$ |
| `certify_bound.py` | exact rational certification of any stored quadruple (§7) |
| `best2.npy`, `best2_matrices.txt` | the best quadruple found ($0.0302377998905$) |
| `best_hard.npy` | an earlier, slightly worse local minimum ($0.031248403475$) |
| `e2best.npy` | the $E_2$ minimiser ($E_2=0.0512492190$) |
| `tetra_u.npy` | the tetrahedral quadruple ($1/18$) |
| `hadlib.py`, `had2.py`, `hadclass.py`, `campaign2.py` | the flat-modulus experiment of §6.4 — kept only as a record of the artefact; **their output is not valid** |
| `diag_F6.npy` | best diagonal-orbit quadruple ($0.0578759465$) |

Reproduce the headline numbers:

```
cd work/11-approx-mub
python3 tetra.py                 # 1/18 construction, numeric
python3 exact_tetra.py           # ... and symbolic: values {1/9, 2/9}, max dev 1/18
python3 certify_bound.py best2.npy tetra_u.npy e2best.npy
```

---

## 12. Honest caveats

* The lower bound $\varepsilon_6^*>0$ is *quoted* from the preprint; I have not reproved
  $N(6)=3$.  Nothing in this report depends on the proof, only on its statement.
* $0.030224240773$ is an upper bound, **not** the value.  I have no evidence that the
  configuration of §6.2 is globally optimal: the basin is found by 2 of 300 random starts,
  which suggests that other, better basins may exist and merely be rarer.  A search that
  seeds from structured families (product, Hadamard-orbit, clock-and-shift) does *not* reach
  it, which is why the honest statement is "$\varepsilon_6^*\le0.0302$" and not
  "$\varepsilon_6^*=0.0302$".  The best value $0.0302242408$ came from a *different* search
  (seeded from three exact MUBs plus a random fourth basis, with an exchange-LP polish on the
  true max), which is further evidence that seed family, not just restart count, decides what
  is found.
* The $E_2$ minimiser of §6.3 is the lowest of 400 restarts; the same caveat applies, and
  §6.4 shows that this landscape punishes confident claims.
* The choice of gauge $U_1=I$ and the sampling distribution (Haar random $U(2..4)$) bias
  which basins are found; the multi-start statistics in §6.2 should be read with that in mind.

---

## 13. Provenance of the results in this report

The work was done in two strands, and it matters which is which.

* **Mine** (`work/11-approx-mub/`): §3 (Theorems 3.1, 3.2, Corollary 3.3), §4 (the tetrahedral
  construction, Theorem 4.5 with its exact SymPy check), §5.1 (Theorem 5.1), the numerical
  picture of §6.1–6.3 with the certification tool of §7, §9, and the pitfall of §6.4 — that
  last one was my own error, caught by my own unitarity assertion, and is recorded because the
  false value ($0.0041$) was a factor $7$ better than the truth and would have been believed.
* **Swarm `smwgxagl5`** (8 members, three submissions accepted after independent checking):
  * m6 — the exact-rational **Cayley certificate** of §7 and the best bound
    $0.030224240773$; an independent proof of Theorem 4.5; the exact MUB triple of §5.4
    (Zadoff–Chu); the $3$-MUB-completion value $0.0798$; a 240-restart basin census.
  * m3 — §5.3, the cyclic slice at $0.053981857147$.
  * m1 — Theorem 5.2 (§5.2) and its $\mu_3,\mu_4,\mu_2$ analogues, plus the $1/12$ sharpness.
  * m7 — Theorem 5.1 found independently, plus the real-class constants: $1/12$ attained for
    two and three real bases, $0.1390615033$ for four (certified, §5.1 remark (ii)).
  * m5 — the MUB-triple completion value of §6.2 ($\sqrt3/18$ exactly for product fourth
    bases, $0.0809327829$ certified in general, for the standard product triple), which
    explains why the minimiser does not sit on an exact MUB triple.
  * m2 — the scope lemma of §4.5 (every product basis of $\mathbb C^2\otimes\mathbb C^3$ is a
    $3+3$ grid, which closes a real gap in my statement of Theorem 4.5) and the exact
    $\mu_{12}$ Fourier-orbit optima $0,\ 1/12,\ 1/9$ for $k=2,3,4$ bases (§5.2);
    also a sixth derivation of $1/18$.
  * m4 — the entropic item (a') of §9 and the "$24<35$, never tomographically complete" point,
    with a verifier; the $\mathbb C^2$-has-three-MUBs correction; an independent certified
    $0.03025917239$ (superseded by m6's) and a fourth derivation of $1/18$.
* **Corrections to my own brief.**  Two, both caught by members: (i) I wrote that $\mathbb C^2$
  has two MUBs and no three; it has three (Pauli), found by m4 — rectified in §4.1 and it does
  not affect the tetrahedral argument, which is about four points of $S^2$; (ii) my task
  statement asserted that the pairing
  $A_1\otimes B_1, A_1\otimes B_2, A_2\otimes B_1, A_2\otimes B_2$ gives $\operatorname{dev}=1/6$;
  it gives $1/3$ (the pair sharing the qutrit factor has $P=(J_2/2)\otimes I_3$, entries
  $0,\frac12$).  The $1/6$ version needs four *distinct* qutrit MUBs.  m3 and m6 both caught
  this independently.  The $1/18$ tetrahedral construction was found twice, independently
  (by me and by m1); m6 reproved the product-class theorem independently as well.
