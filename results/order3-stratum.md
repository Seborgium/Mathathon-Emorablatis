# The order-three stratum of four MUBs in $\mathbb{C}^6$: exact reduction and a gap

Working note, 2026-11-14. Companion to `results/elegant-proof-routes.md` (route map) and
`results/h0-feasibility.md`. Question: can the order-three symmetry that organises *all* MUB triples
in dimension six be turned into an exact, small statement about the *fourth* basis?

**Status summary (read this first).**

| result | status |
|---|---|
| Lemma A: an order-3 symmetry of a flat basis in $\mathbb C^6$ must have eigenvalue multiplicities $(2,2,2)$, and acts in two 3-cycles | **proved** (§2) |
| Theorem B: exact frame criterion for two order-3 symmetric flat bases to be unbiased — 12 real algebraic equations of Parseval-equality type | **proved** (§3), verified to machine precision (§6) |
| Corollary C: in the stratum the "modulus blindness" that kills every global relaxation disappears; unbiasedness is an equality case | **proved** (§4) |
| Numerical: the order-3 stratum contains no 4-tuple; the sharp gap is $0.0422687212\dots$, attained at a 3-level overlap pattern | **numerical, 500 restarts** (§5) |
| Conjecture: the gap is exact and certifiable by elimination over $\mathbb Q(\omega)$ | conjectural (§7) |

Nothing here proves $N(6)=3$; two computer-assisted proofs of that already exist (the 24 Sep 2026
preprint and the topological classification of arXiv:2611.06917). What is new is a proof that the
*symmetric stratum* — the part that carries every known triple — is a 7-parameter family of frames
satisfying a 12-equation algebraic criterion, plus the measured fact that it stops one basis short,
with a definite margin.

---

## 1. Setting

$N(d)$ is the largest size of a family of pairwise mutually unbiased orthonormal bases of
$\mathbb C^d$; two bases are unbiased when $|\langle b_i,c_j\rangle|^2 = 1/d$ for all $i,j$. Fix the
first basis to be $I_6$. A basis $B$ (a unitary up to column phases) is unbiased to $I_6$ iff it is
**flat**, $|B_{jk}| = 1/\sqrt6$, i.e. iff $\sqrt 6\,B$ is a complex Hadamard matrix; and two flat
bases $A,B$ are unbiased iff $A^*B$ is flat.

Three facts from the literature, used below.

1. *Pairs are four-dimensional.* Every order-6 complex Hadamard matrix except Tao's is equivalent to
   $H_+(\theta)$ reconstructed from a dephased $3\times 3$ corner with **four** free phases, the
   reconstruction existing exactly where $R(\theta) = 4g^2\eta-\chi^2 > 0$; the classes form a
   connected space (arXiv:2611.06917, Thms 1–2).
2. *Every triple is order-3 symmetric.* Up to equivalence each MUB triple
   $\{I_6, H/\sqrt6, K/\sqrt6\}$ is fixed by a unitary $T$ with $T^3 = I_6$,
   $T = \mathrm{diag}(1,1,\omega,\omega,\omega^2,\omega^2)$, $\omega = e^{2\pi i/3}$, which fixes every
   vector of one basis up to a phase and permutes each of the other two in two 3-cycles; and triples
   with that symmetry form a two-parameter family plus one isolated Fourier triple
   (arXiv:2611.06917, §III.1 and §V.4, where this is certified on 2,775 phase balls).
3. The two types of triple admit no further basis, so $N(6) = 3$ (ibid., with Grassl and Jaming et
   al. for the family).

So in dimension six **the whole difficulty of a quartet is concentrated in the symmetric stratum**:
any quartet would contain four triples, and *every* triple is order-3 symmetric. The question below
is therefore not a narrowing of convenience — it is the stratum the problem actually lives in.

Conventions. Write $\mathbb C^6 = \mathbb C^2\otimes\mathbb C^3$ and index vectors by
$(a,t)\in\mathbb Z_2\times\mathbb Z_3$. Let $Z = \mathrm{diag}(1,\omega,\omega^2)$ and
$$T \;=\; I_2\otimes Z,\qquad \text{eigenvalues } 1,\omega,\omega^2 \text{ each with multiplicity } 2 .$$
Every order-3 unitary with multiplicities $(2,2,2)$ is unitarily conjugate to $T$, and conjugating a
whole configuration preserves unbiasedness, so the choice of $T$ is no loss of generality. A basis
$B$ is *$T$-covariant* if $TB = B\Pi_B$ for a permutation matrix $\Pi_B$ with $\Pi_B^3 = I$.

## 2. Lemma A — an order-3 symmetry of a flat basis is forced to be of type $(2,2,2)$

**Lemma A.** Let $U$ be a unitary of order $3$ with eigenspaces $E_1,E_2,E_3$ of dimensions
$m_1,m_2,m_3$ (for the eigenvalues $1,\omega,\omega^2$), and let $B$ be a flat basis with $UB = B\Pi$,
$\Pi^3 = I$. If $U$ is not a scalar then $m_1 = m_2 = m_3 = 2$, and $\Pi$ consists of exactly two
3-cycles.

*Proof.* Every $\Pi$-orbit of basis vectors spans a $U$-invariant subspace on which $U$ acts by a root
of unity times the identity of a cyclic shift. If an orbit is a singleton the vector is a
$U$-eigenvector, so it lies in some $E_j$ and all its non-zero coordinates are among the $m_j$
coordinates of $E_j$; flatness gives $m_j\cdot\tfrac16 = 1$, i.e. $m_j = 6$, so $U$ is scalar. Hence
every orbit has size $3$ and there are two of them.

Let $v$ generate one orbit, $v = \sum_t v_t\otimes e_t$ with $v_t\in\mathbb C^2$. Orthonormality of
$\{v,Uv,U^2v\}$ gives $0 = \langle U^k v, v\rangle = \sum_t \omega^{kt}\|v_t\|^2$ for $k = 1,2$;
with $m_t := \dim E_t$ the sets $\{t\}$ have sizes $m_t$ and flatness gives $\|v_t\|^2 = m_t/6$. A
non-trivial triple of real numbers has vanishing first two Fourier coefficients only if they are
equal, so $m_1 = m_2 = m_3$; as $\sum_t m_t = 6$ this is $(2,2,2)$. $\square$

**Consequence (frame coordinates).** After relabelling $t \in \mathbb Z_3$, a flat $T$-covariant
basis is exactly a pair of orbit generators $v,w$ with
$$v = \sum_{t\in\mathbb Z_3} v_t\otimes e_t,\qquad w = \sum_{t\in\mathbb Z_3} w_t\otimes e_t,\qquad
v_t,w_t \in\mathbb C^2,\quad \|v_t\| = \|w_t\| = \tfrac1{\sqrt3},\quad \langle v_t,w_t\rangle = 0 ,$$
and its six vectors are $U^kv, U^kw$ $(k \in \mathbb Z_3)$; flatness is the extra condition that the
two components of each $v_t$ (and of each $w_t$) have modulus $1/\sqrt6$. Two orbits, ordered pairs
of frames and the phases of $v$ and of $w$ are the only ambiguities, so

> a flat $T$-covariant basis is described by the three orthonormal frames $(v_t,w_t)_{t\in\mathbb Z_3}$
> of $\mathbb C^2$, i.e. by $3\times 3$ phases $=9$ real numbers modulo the $2$ global phases of
> $v$ and $w$: **seven real parameters.**

(The count is the point. A general flat basis has $25$; the symmetry removes $18$.)

## 3. Theorem B — the exact unbiasedness criterion in frame coordinates

For two flat $T$-covariant bases $A=(v,w)$, $B=(v',w')$ and $(x,y)\in\{v,w\}\times\{v',w'\}$ put
$$c^{(x,y)}_t := \langle x_t,\,y_t\rangle \in\mathbb C \quad (t\in\mathbb Z_3),\qquad
d^{(x,y)}_k := \sum_{t\in\mathbb Z_3}\omega^{kt}\,c^{(x,y)}_t \quad (k\in\mathbb Z_3).$$

**Theorem B.** $A$ and $B$ are unbiased **iff** for each of the four pairs $(x,y)$
$$\text{(E)}\quad \sum_{t}|c_t|^2 \;=\; \frac16,
\qquad\qquad
\text{(B)}\quad \sum_{t} c_t\,\overline{c_{t-1}} \;=\; 0 ,$$
equivalently iff all twelve numbers $d^{(x,y)}_k$ have modulus exactly $1/\sqrt6$.

*Proof.* The $(k,x),(k',y)$ entry of $A^*B$ is
$\langle U^kx,U^{k'}y\rangle = \sum_t \omega^{(k'-k)t}\langle x_t,y_t\rangle = d_{k'-k}$, so the
matrix $A^*B$ is a $2\times 2$ array of $3\times 3$ circulant blocks with symbols $d^{(x,y)}$.
Unbiasedness says every entry has modulus $1/\sqrt6$, i.e. $|d_k| = 1/\sqrt6$ for all $k$ and all
four blocks.

Now $|d_k|^2 = \sum_t|c_t|^2 + 2\,\mathrm{Re}\big(\omega^{k}P\big)$ with
$P := \sum_t c_t\overline{c_{t-1}}$. If $P \neq 0$, writing $P = \rho e^{i\varphi}$, the three numbers
$\cos(\varphi + 2\pi k/3)$, $k=0,1,2$, are not all equal — for equality the first two give
$\varphi \equiv -\pi/3 \pmod \pi$, and the third then equals $-\rho$ against $+\rho/2$; so the moduli
$|d_k|$ cannot be equal. Hence $|d_0|=|d_1|=|d_2|$ forces $P = 0$, and then
$|d_k|^2 = \sum_t|c_t|^2$ for every $k$, which together with $|d_k|^2 = 1/6$ is (E). The converse is
immediate. $\square$

Three remarks that matter for what follows.

* **(B) is one complex — not two real — condition per block.** $P$ is a "cyclic correlation" of the
  three numbers $c_t$; it is the obstruction to the three block symbols having equal modulus.
* **Parseval makes (E) an equality case, not an inequality.** $\sum_k|d_k|^2 = 3\sum_t|c_t|^2$
  identically. So (E) says: *the Parseval inequality for the length-3 Fourier transform of
  $c^{(x,y)}$ is attained.* Equivalently, the projection of the orbit vector $x$ onto the
  $U$-invariant 3-space spanned by $y$'s orbit is exactly $\tfrac12$, the value forced by
  completeness. There is no slack to exploit and none to lose.
* **Twelve real equations.** Four blocks $\times$ ((E): 1 real, (B): 2 real). Measured Jacobian rank
  at the explicit triple $F_2\otimes F_3$, $(\mathrm{diag}(1,i)F_2)\otimes(\mathrm{diag}(1,\omega^2,\omega^2)F_3)$
  is 9; at generic solutions of the criterion it is 7. So the equations are not independent, and the
  stratum's pair locus is $9$–$11$ dimensional in the 18 phases.

Theorem B replaces 36 modulus equations by 12 real algebraic equations on frame data — but its real
content is the next corollary.

## 4. Corollary C — why this stratum is where a positivity argument can work

In the *full* 25-phase problem the modulus-level relaxation is provably blind: for $m$ MUBs the
matrix of squared overlaps is $Q_m = I+\frac1d(J_m-I_m)\otimes J_d$, positive semidefinite for every
$m$, and the Gram-level PSD problem has no relaxation gap at all (rank is forced to be exactly $d$
with all non-zero eigenvalues equal to $m$; see `results/elegant-proof-routes.md` §2(c)). Hence no
Welch-type, few-distance, relative-bound or SDP-over-moduli argument can separate $m=3$ from $m=4$.

**In the symmetric stratum the opposite holds.** By Theorem B, unbiasedness of two order-3 symmetric
flat bases is *equivalent* to two equalities: the Parseval equality (E) and the vanishing of the
cyclic correlation (B). There is no inequality with slack anywhere; the feasible set is cut out by an
equality case of a positive semidefinite form. Consequently:

> the order-3 stratum is the unique place in dimension six where the "no potential function" verdict
> of the route map flips. Any analytic (rather than enumeration) attack on the fourth basis should be
> mounted here, and it must prove infeasibility of an equality system, not the failure of an
> inequality.

This also explains the shape of every known construction. With all frames constant in $t$
("product-type" configurations) $c_t$ does not depend on $t$, so $P = 3c_0\bar c_0 \ne 0$ and (B)
fails identically: **no two product-type order-3 symmetric bases are unbiased.** Unbiasedness forces
the frames to be $t$-dependent, and the minimal such twist is a chirp $v_t \propto \omega^{\alpha t}$;
this is exactly the diagonal twist $D(t)$ in the known two-parameter family. The symmetry does not
merely organise the triples: it predicts that any fourth basis must be twisted at every scale.

## 5. The gap: numerics

Parametrise each flat $T$-covariant basis by its nine phases
$v_t = (a_t,b_t)/\sqrt6$, $w_t = \lambda_t(\overline{b_t},-\overline{a_t})/\sqrt6$ with
$|a_t|=|b_t|=|\lambda_t|=1$, build the six vectors $U^kv,U^kw$, and minimise
$$\Delta \;=\; \max_{\text{all }108\text{ ordered pairs}}\Big|\;|\langle\,\cdot\,,\,\cdot\,\rangle|^2 - \tfrac16\Big|$$
over three independent such bases (27 phases) together with the identity basis, i.e. over
$T$-covariant quartets. Five hundred independent random starts (`scipy` L-BFGS-B on the sum of
squares, then on the max) all return the same value to nine digits:

$$\boxed{\;\Delta_{\min} \;=\; 0.0422687212\dots\;}$$

so **there is no order-3 symmetric quartet**, with a margin. Two structural facts about the minimiser.

* Its 108 squared overlaps take exactly **three** values,
  $$0.124397945884,\qquad 0.1514019756,\qquad 0.1810500186 ,$$
  and the binding constraint is on the **small** side: a squared overlap is forced down to
  $1/6 - 0.0422687$, while the largest reaches only $1/6 + 0.0143834$. In words: four order-3
  symmetric bases must contain a pair of vectors that are *too parallel*, not too orthogonal.
* The optimum is not a boundary artefact: it is stationary in all 27 phases, and 500 starts from
  random phases find it, so the landscape appears to be a single basin.

Two consistency checks. With the first two bases fixed to the explicit Fourier triple the gap rises to
$0.11215$ (as it must: fewer degrees of freedom), and the identity basis contributes defect zero
identically, because a flat $T$-covariant basis has all entries of modulus $1/\sqrt6$ by construction.

**Honest limits.** This is a numerical statement about a compact 27-torus: no interval arithmetic was
used, so it is evidence, not proof. What it establishes beyond doubt is that the symmetric stratum
does *not* contain four bases by any accident of a poor parametrisation: the parametrisation is
complete (Lemma A plus the frame count), the criterion it is checked against is exact (Theorem B,
verified independently), and the deficit does not shrink under refinement.

## 6. Verification

`results/order3-check.py` reproduces, from the definitions and without any input from the preprint:
the flatness and covariance of the model bases; the exactness of Theorem B on the explicit triple
(criterion residual $1.4\times10^{-16}$); that all 80 independently minimised zeros of the criterion
are genuinely unbiased pairs; and the quartet search of §5. The three-phase corner invariants
$g = 27-3p+J$, $\eta = 9-p+J$, $\chi = [XY+XZ+YZ-XYZ-(p-9)(p-18)+(p-15)J]$ and
$R_{\max} = 3^{13}/2^{12}$ used to fix the pair picture were re-derived earlier in the same
workspace and agree to $10^{-13}$.

## 7. What would make this a theorem, and what it would replace

**The remaining step.** Prove $\Delta_{\min} > 0$ exactly. The natural route is elimination over
$\mathbb Q(\omega)$: the nine phases per basis are unit-modulus variables, so set
$a_t = x_t/x_t^*$, etc., and add the relations $x_tx_t^* = 1$; the criterion (E),(B) is polynomial in
$(x_t,x_t^*)$ of degree $\le 4$, and non-existence of a real point is a radical-membership question in
a $54$-variable polynomial system with a $\mathbb Z_3$ symmetry. That is far smaller than the
primal problem (three $6\times 6$ matrices of phase variables) and is the natural target for
computer algebra; a certified Sturm/Sturm–Habicht or interval branch-and-bound argument on the
$\lambda_t$ would give the theorem with an explicit (not sharp) constant.

**What it replaces in the reference paper.** The preprint's Stage C is 92 of its 100 recorded
commands: per pair $(I,H)$, a 5-phase vector space, boxes, labels, and a two-graph search for two
disjoint 6-cliques with all 36 cross edges present. Inside the symmetric stratum that whole pipeline
collapses to the 12 equations of Theorem B in seven parameters per basis, with the measured gap
$\Delta_{\min}$ as the certificate. Concretely, a certified version of §5 would replace, for every
order-3 symmetric configuration, the Stage-C graph search by a single scalar inequality; and because
*every* triple is order-3 symmetric, this covers the configurations a quartet is actually made of.

**What it does not replace.** A quartet need not share one $T$ among all four bases; a quartet only
has each of its four triples symmetric, possibly for four different $T$'s. Lemma A says each such $T$
has type $(2,2,2)$, but nothing here forces them to agree — so an asymmetric quartet is not excluded
by §5. That gap is exactly where the preprint's Stage C and the topological classification's
order-three-symmetry certificates do their work, and closing it analytically is a separate theorem
("symmetry propagation": a basis unbiased to an order-3 symmetric triple must itself be covariant for
the same $T$). That is the sharpest formulation of what remains, and it is the statement I would put
to anyone claiming a conceptual proof.

## 8. Conjectures

**Conjecture 1 (symmetry propagation).** If $\{I,H/\sqrt6,K/\sqrt6\}$ is an order-3 symmetric MUB
triple with symmetry $T$, and $L$ is a basis unbiased to all three, then $T L = L\Pi$ for some
permutation $\Pi$ with $\Pi^3 = I$. Together with §5 this would give a computer-free proof of
$N(6)=3$ *given* the classification of triples, with no covering at the fourth basis.

**Conjecture 2 (sharp gap).** $\Delta_{\min}$ is attained and is an algebraic number of degree $\ge 6$
(it is not a rational polynomial in $\sqrt2,\sqrt3,\sqrt5,\sqrt6,\sqrt7$, checked by integer relation
search on fifteen digits); the minimiser is unique up to the symmetries of the stratum.

**Conjecture 3 (the three-value law).** Every local maximum of the "MUB defect" over order-3 symmetric
4-tuples has squared overlaps taking at most three values, and the extremal ones are characterised by
two of the three blocks having equal block-energies. This would explain the 3-level pattern of §5
rather than merely record it.
