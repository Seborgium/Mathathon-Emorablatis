# m4 final report — direction 3: the product identity $\Xi(P_A)\Xi(P_B)\Xi(P_C)=0$

Swarm `smwhnslql`, member m4, direction d3. Files: `m4-theorem.md` (statements + proofs),
`m4-tables.md` (exact / high-precision computations), `m4-code/` (scripts), `m4-log.md` (running log).

## Outcome in one paragraph

The product identity is, after the source's own equivalence $\Xi(P_X)=0\iff 3\mid\Delta_X$, the
statement **(13′) every triple has some anchor $X$ with $3\mid\Delta_X$**. I prove that the symmetric
locus $Z=\{\exists X:3\mid\Delta_X\}$ is **closed** in the compact space of triples and that
$$(13')\iff Z=\mathcal T\iff Z\ \text{is dense in}\ \mathcal T .$$
So a proof of (13′) on a dense set of triples suffices, and if (13′) failed, the counterexamples would
form a **nonempty open** set (stable under small perturbation). That is the whole logical content of
"symmetry is a closed condition". I also show what does *not* follow: closedness alone does not make
$Z$ clopen. The individual sets $S_X$ need not be open — at the centre of the two-parameter family
$\Delta$ jumps from $(3,3,2)$ to $(3,1,1)$ — so no "one symmetric triple per connected component"
criterion is available. An earlier
version of this report made exactly that invalid inference; §2bis records the correction. The
computations (tensor triple, the whole root-of-unity part of the Fourier chart, the JMSSW family) are
reported as computations of $\Delta$ on known triples, not as a test of (13′).

## 1. The identity, without the detector

For a triple $x=(A,B,C)$ and an anchor $X$ let $\Delta_X(x)$ be the order of the group of diagonal
unitaries (modulo scalars, in the $X$ coordinates) that preserve *each* of the other two bases as a set
of rays. By Proposition 1, $\Delta_X\in\{1,2,3,6\}$ (finite cyclic). The source's identity is exactly
(13′), and the $10$-dimensional projection, the five-term minors and the mod-3 relation lattice are a
device for computing the **3-part** of $\Delta_X$; they carry no further structure.

## 2. The main result (corrected, proved — `m4-theorem.md` §§1–3)

Let $\mathcal T\subset U(6)^3$ be the compact space of triples, $S_X=\{3\mid\Delta_X\}$,
$Z=S_A\cup S_B\cup S_C$, $O=\mathcal T\setminus Z$.

* **Proposition 1.** $G_X$ is finite, abelian, cyclic, of order dividing $6$; hence
  $3\mid\Delta_X\iff G_X$ contains an element of order $3$. (The source's sketch is right but omits
  finiteness; the missing step uses only that a vector unbiased to a basis has no zero coordinate.)
* **Proposition 2.** $S_X$ is **closed** (so $Z$ is closed and $O$ is open). Proof: the cube-root
  clocks form a finite set $\mathcal K_3$ of $3^5=243$ elements; the incidence set
  $\{(x,[T]):[T]\in\mathcal K_3$ preserves both ray sets$\}$ is closed in the compact
  $\mathcal T\times\mathcal K_3$, and a finite-fibre closed projection gives the conclusion.
* **Theorem A.** $Z$ closed, $O$ open, $\mathcal T=Z\sqcup O$, and
  $(13')\iff O=\varnothing\iff Z=\mathcal T\iff Z$ **dense**.
  *Density criterion:* proving $3\mid\Delta_X$ at some anchor for every triple outside a closed
  nowhere-dense exceptional set suffices; the exceptional triples then need no separate treatment.
  This is the source's §7 remark, in its correct form.
  *Failure:* if (13′) fails, $O$ is a nonempty **open** subset of $\mathcal T$, so every counterexample
  is stable under small perturbation of every entry, and $O$ has positive measure in the stratum of
  $\mathcal T$ that contains its smooth points.

## 2bis. What I withdrew from the earlier version (and why)

The earlier version proved $S_X$ closed and then asserted that $Z$ is *clopen*, concluding that (13′)
holds iff no connected component of $\mathcal T$ is symmetry-free, that one symmetric triple per
component suffices, and that a "touching" statement weaker than the classification would do. **None of
that follows.** Closedness is upper semicontinuity: symmetry may appear in a limit, so $\Delta_X$ can
drop, $Z$ can be a proper closed subset of $\mathcal T$, and a component can contain both symmetric and
asymmetric triples. Concrete witness that $\Delta$ is not locally constant: at the centre of the
two-parameter family $\Delta=(3,3,2)$, while every perturbation I computed (and m2's census of 9,320
points) gives $(3,1,1)$ — the *individual* sets $S_X$ change, so no local-constancy statement is
available, and the "component" criteria are withdrawn. What survives is exactly §2: closedness,
the density criterion, and the openness of the failure locus.

## 3. Computations (details and reproduction in `m4-tables.md`)

These compute $\Delta$ on explicit triples; they are not a test of (13′) (see §2bis and §4.3).

| triple | exactness | $(\Delta_A,\Delta_B,\Delta_C)$ |
|---|---|---|
| tensor/product triple $\{I_6,F_2\otimes F_3,SF_2\otimes ZF_3\}$ | exact, $\mathbb Z[\zeta_{24}]$ | $(6,6,6)$, Smith $(1,1,1,1,6)$ at all anchors |
| Fourier chart, 4 triples $\{I_6,F_6,K\}$ from the 12 root-of-unity rays | exact, $\mathbb Z[\zeta_{24}]$ | two triples $(6,6,6)$; two triples $(3,3,2)$ |
| JMSSW family $\{I_6,F(0,b(t)),C(t)\}$, $t=0.5,\dots,1.1$ | 60 digits, gap $10^{27}$ | $(3,1,1)$ at every sampled $t$ |

* The source's projection formula (1) is **correct**: for a genuine MUB pair the $30\times30$ matrix it
  defines is idempotent, Hermitian, rank 10, and equals the true orthogonal projection onto the image of
  $W_{\mathcal B}\oplus W_{\mathcal C}$ (agreement $10^{-16}$). I suspected a normalisation error at
  first; the suspicion was wrong (log §4).
* For each of the 12 anchors of the Fourier chart I computed $\Delta_X$ twice — as the index of the
  support lattice and by direct enumeration of the diagonal clocks — and the two agree, so no
  "exchange" of the two bases occurs there.
* The two $(3,3,2)$ triples have Smith forms $\operatorname{diag}(1,1,1,1,3)$,
  $\operatorname{diag}(1,1,1,1,3)$, $\operatorname{diag}(1,1,1,1,2)$: the source's exact example,
  independently reproduced, and consistent with its order-two lemma.
* Along the JMSSW family the value is *constant* $(3,1,1)$: exactly one anchor carries a threefold
  symmetry, so no strengthening of (13′) to "two anchors" or to "order six" can hold. (A statement about
  that curve, not about the whole triple space.)

## 3bis. Consistency with the other directions (as of my last board read)

* **m2** (`m2-delta-census.md`) samples 4,600 random interior points and 4,720 grid points of the
  two-parameter family and finds only $\{1,1,3\}$, plus $\{2,3,3\}$ at the centre — i.e. the same two
  patterns I compute, on a much larger sample. Their two exact points (Fourier $(6,6,6)$, centre
  $(3,3,2)$) match my exact Fourier-chart patterns.
* **m5** (d2/f2) builds the $\Delta=2$ stratum explicitly and reports $(2,3,3)$ and $(6,6,6)$; I checked
  their $3\times3$ rigidity claim independently (§4bis).
* **m2's dossier §4** reports that the published classification certifies "every triple has
  $3\mid\Delta_X$ for some anchor", i.e. (13′) itself, which would settle $Z=\mathcal T$ — and then
  Theorem A is vacuous-but-informative: it says the classification is *being used* at full strength, not
  through any closedness shortcut. **m6** (d4) labels the same statement (T3).

## 4. Verdicts on the source's claims that I touched

| claim | verdict |
|---|---|
| Projection formula (1); $P^2=P$, rank 10, $(P)_{ij,ij}=1/3$ | **correct** (checked against an independently built projection) |
| $\Delta_X\in\{1,2,3,6\}$, cyclic | **proved** (Prop. 1; finiteness step supplied) |
| $3\mid\Delta_X\iff\operatorname{rank}_{\mathbb F_3}R_X<5$ | **correct in substance** (needs the recovery lemma for "$\Rightarrow$"); the 3-part is robust even if a clock exchanges the two bases |
| $\Delta_X=[\Lambda_0:L_X]$, full group | **proved by m1's subsequent audit (Theorem D)**: $|\operatorname{tr}T|^2=6$ is valid; m1 supplies the missing odd-power/order-three cases. My earlier claim that only $|\operatorname{tr}T|\le\sqrt6$ follows was wrong |
| "symmetry is a closed condition; a proof on a dense subset suffices" (§7) | **correct**, now proved (Prop. 1–2, Theorem A(c)). The converse is *not* available: a non-dense subset proves nothing |
| (13) itself | **not proved here**. Equivalent to density of $Z$ (Theorem A(b)). True if the classification certified in m2's dossier is, which is direction d5's business |

## 4bis. Two observations for the other directions

**The Fourier chart does not consist of one triple.** The multiset
$\{\Delta_A,\Delta_B,\Delta_C\}$ is an invariant of a triple up to unitary equivalence and permutation of
the bases. Among the four Fourier-chart triples $\{I_6,F_6,K\}$ with root-of-unity entries, two have
$\{6,6,6\}$ and two have $\{3,3,2\}$; so there are **at least two inequivalent triples** there, and "the
single isolated Fourier triple" in `results/elegant-proof-routes.md` §R5 should be read as a statement
about the *pair* moduli (the isolated Hadamard class $F_6$ and its 16 third bases). Worth checking
against the preprint's wording (d5) before it enters a revised proof.

**The $3\times3$ rigidity behind the $\Delta=2$ stratum is confirmed.** m5's claim (d2/f2) that $|HF|$
flat for a $3\times3$ complex Hadamard forces $H=FD\Pi$ with $D$ a cube-root diagonal (108 matrices)
reproduces exactly: 108 solutions from the discrete enumeration, none from $2.4\cdot10^6$ random
diagonal-phase candidates (best flatness deviation $3.9\cdot10^{-4}$ there, no near-misses).

## 5. Where this leaves the route

The honest residue is (13′) in the form "prove $3\mid\Delta_X$ at some anchor on a dense subset of
$\mathcal T$". Two things are now known about it: (i) the exceptional triples need no separate analysis
(closedness); (ii) a component-wise shortcut is *not* available, because the symmetric locus is not
locally constant — the family centre shows the jump explicitly. So a direct proof must either establish
the property on a genuinely dense set, or establish it by a global argument that does not pass through
"one point per component". Any such argument must use the MUB equations globally; whether it can be
"algebraic" is left open by my work.

## 5bis. Edits I would make to the source note (only audited material)

| source location | edit |
|---|---|
| §5 eqs. (12)–(13) | state (13) as "every triple has an anchor with $3\mid\Delta_X$"; add that the symmetric locus is closed, so a dense-subset proof suffices, and that the failure locus is open |
| §5 "Where the coupling must enter" | state the equivalent density target; whether a useful global coupling identity exists remains open |
| §5 the polynomial $\Xi$ | keep as a detector of the 3-part (it is correct); drop any suggestion that closedness of the symmetric locus yields a component criterion |
| §3 eq. (5) | qualify: $3\mid\Delta_X\iff\operatorname{rank}_{\mathbb F_3}R_X<5$ is what is proved; $\Delta_X=[\Lambda_0:L_X]$ needs the no-exchange step, whose trace argument does not work |
| §7 "local divisibility under limits" | keep — it is correct — but state it as $S_X$ closed, $O$ open, and (13′) ⟺ $Z$ dense; add the warning that a non-dense subset proves nothing |
| §2 table of $\Delta$-values | the JMSSW family is *identically* $(3,1,1)$ (7 points, 60 digits); the $(3,3,2)$ example is reproduced exactly by two Fourier-chart triples |
| target "force any diagonal symmetry" | state as: prove $3\mid\Delta_X$ for some $X$ on a dense set of triples |

## 6. Reproducibility

Scripts (`m4-code/`): `exact.py`, `flatops.py`, `snap.py`, `symgroup.py`, `run_tensor.py`,
`smith_table.py`, `f6_final.py`, `jmssw2.py`. Exact parts are integer arithmetic in
$\mathbb Z[\zeta_N]$; the family part is mpmath at 60 digits with a printed threshold gap. The one
external input is the JMSSW parametrisation `Fmat(a,b)`, `Cmat(t)` from `.scratch/mub6/fouriercheck2.py`
(an earlier run of this project); the printed MUB residual is the check that it is the triple it claims
to be.
