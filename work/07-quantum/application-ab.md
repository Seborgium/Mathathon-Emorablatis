# T7 framing, part (a) and part (b)

Written by swarm member m1. Covers the two sections of `application.md` assigned to this
direction: **(a) what unbiasedness is physically** and **(b) what the theorem says and does
not say**. Sections (c) (usability, $d=10$) and (d) (prior work) are separate files by other
members; see `handoff-1.md` for the assembly.

Sources used, and how they were checked:

* the preprint text (`.scratch/mub6.txt`), §1, §7, Appendix A.1 and the bibliography;
* `results/proof-claims.md` and `results/code-audit.md`;
* every external fact below is either (i) derived here and checked numerically, (ii) taken
  from the preprint's own bibliography, or (iii) fetched from a source listed in
  `references.addition.bib`. Where an item is second-hand through a search snippet rather
  than a read page, it says so.

Markers: **[derived]** = proved in this file; **[paper]** = stated in the preprint and
re-read; **[cited]** = external source, URL in the bib; **[reported]** = the preprint's
observed datum, not independently checkable.

---

## (a) What unbiasedness is physically

### a.1 One definition, three faces

Two orthonormal bases $B=\{b_0,\dots,b_{d-1}\}$, $C=\{c_0,\dots,c_{d-1}\}$ of
$\mathbb{C}^d$ are **mutually unbiased** when

$$|\langle b_j,c_k\rangle|^2=\frac1d\qquad\text{for all }j,k. \tag{a.1}$$

Three readings, all the same equation:

1. **Measurements.** A basis is the family of rank-one spectral projectors of a sharp,
   non-degenerate projective measurement. A MUB pair is a pair of sharp measurements sharing
   no eigenvector.
2. **Prediction.** Prepare the eigenstate $b_j$ of the first measurement, so its outcome is
   certain. Then *every* outcome of the second measurement has probability exactly $1/d$:
   maximal ignorance. Certainty in one basis projects a flat distribution in the other, and
   (a.1) is symmetric, so the statement holds in both directions. This is Bohr
   complementarity made exact and quantitative at finite $d$: the two measurements are as far
   apart as two orthonormal bases can be. The natural distance statistic is
   $c(B,C)=\max_{j,k}|\langle b_j,c_k\rangle|\in[1/\sqrt d,1]$; unbiasedness is the lower end
   $c=1/\sqrt d$ ("nothing in common"), $B=C$ is the upper end.
3. **Matrices.** After a common unitary, $B$ is the coordinate basis and $C$ is the column
   basis of $H/\sqrt d$ with $H$ a **complex Hadamard matrix**: $|H_{jk}|=1$ and
   $HH^{*}=dI$ **[paper, Def. 2.1]**. So a MUB pair is a *flat* unitary: all $d^2$ overlaps
   are simultaneously as small as they can be. There is no basis change relating them that is
   "small".

A set of $N$ pairwise unbiased bases is written $N$ MUBs; $N(d)$ is the maximum. $N(d)$ is an
invariant of the dimension alone.

Informational restatement, which is what makes MUBs a tool rather than a curiosity: knowing
the outcome of one measurement in the set gives zero Shannon information about the outcome of
any other, and a MUB pair saturates the Maassen--Uffink bound $H(B)+H(C)\ge\log d$
**[cited: maassen1988]**, the two-measurement bound being tight at overlap $1/d$; adding
bases strictly strengthens the state-independent bound **[cited: ballester2007]**. For the
application side (tomography, cryptography, uncertainty, contextuality) see
**[paper [20], cited: mcnulty2026]**.

### a.2 Why $d+1$ is the maximum, and which part of that is elementary

**Statement.** For every $d\ge2$: $N(d)\le d+1$. Moreover $N(d)=d+1$ for every prime power
$d$; for no other $d$ is $d+1$ known.

**The upper bound is elementary linear algebra --- five lines, no number theory, no
computer.** *[derived; I re-derived it and checked the Gram matrices numerically for
$d=2,\dots,6$, see a.3.]*

Let $\mathrm{Herm}_d$ be the real vector space of Hermitian matrices, $\dim=d^2$, with the
trace inner product $\langle\!\langle X,Y\rangle\!\rangle=\mathrm{tr}(XY)$. A basis $B$ gives
$d$ projectors $P^B_j=b_jb_j^{*}$ and their traceless parts

$$E^B_j \;=\; P^B_j-\tfrac1d I .$$

Since $\sum_jP^B_j=I$ we have $\sum_jE^B_j=0$, so the $E^B_j$ lie in the hyperplane
$H_0=\{X:\mathrm{tr}\,X=0\}$ of dimension $d^2-1$, and they span exactly $d-1$ dimensions
there (the $P^B_j$ are linearly independent).

If $B\ne C$ are unbiased then for all $j,k$

$$\langle\!\langle E^B_j,E^C_k\rangle\!\rangle
=\mathrm{tr}(P^B_jP^C_k)-\tfrac1d
=|\langle b_j,c_k\rangle|^2-\tfrac1d=0, \tag{a.2}$$

so the subspaces $V_B=\mathrm{span}\{E^B_j\}$ and $V_C$ are orthogonal in $H_0$. For $N$
pairwise unbiased bases the $V_B$ are pairwise orthogonal, each of dimension $d-1$, hence

$$N\,(d-1)\;\le\;\dim H_0\;=\;d^2-1\;=\;(d-1)(d+1)
\qquad\Longrightarrow\qquad N\le d+1. \tag{a.3}$$

That is the whole upper bound. Nothing is hidden in it: (a.2) is a two-line computation and
(a.3) is a dimension count.

Two consequences of the same computation, used in a.3:

* within one basis, $\langle\!\langle E^B_j,E^B_k\rangle\!\rangle=\delta_{jk}-\frac1d$, i.e.
  the Gram block is $I_d-\frac1dJ_d$, which is the identity on the traceless subspace
  $\{\theta:\sum_j\theta_j=0\}$ and zero on the constants;
* a complete set ($N=d+1$) saturates (a.3), so $\{\sqrt{d/(d-1)}\,E^B_j\}_{B,j}$ is then an
  **orthonormal basis of $H_0$**: the $d^2-1$ traceless projectors are not merely independent,
  they are an equal-norm orthogonal frame.

**What is elementary and what is not.** The upper bound is elementary. *Attainment* is not
elementary in the same sense: it requires a construction, and the known construction exists
exactly when $d$ is a prime power. None of the present paper's difficulty lives in (a.3); the
difficulty is entirely in the exact value of $N(d)$ when $d$ is not a prime power.

### a.3 State tomography: why a complete set is the natural target

Measuring a MUB set gives, for an unknown state $\rho$, the probabilities
$p^B_j=\mathrm{tr}(\rho P^B_j)$. Write $\theta^B_j=p^B_j-\frac1d$. By the orthonormality in
a.2, for a complete set

$$\rho=\frac1d I+\sum_{B}\sum_j \theta^B_j E^B_j ,\qquad
\sum_j\theta^B_j=0\ \text{for each }B, \tag{a.4}$$

and the coefficients are *read off directly*: no matrix inversion, because the frame is an
orthogonal basis. There are $(d+1)(d-1)=d^2-1$ of them, exactly the number of real parameters
of a density matrix, and the $d+1$ normalisation constraints account for the redundancy among
the $(d+1)d$ probabilities.

* **Qubit.** $d=2$, $d+1=3$: the three Pauli directions $\sigma_x,\sigma_y,\sigma_z$ are the
  three MUBs of $\mathbb{C}^2$ and (a.4) is the Bloch decomposition.
* **Why $d+1$ and not fewer.** $k$ MUBs determine at most $k(d-1)$ parameters by (a.3) with
  $N$ replaced by $k$, and informationally complete tomography needs $d^2-1$; so $k\ge d+1$.
  Two MUBs in $d=2$ span only $2$ of the $3$ Bloch directions --- measuring $\sigma_x$ and
  $\sigma_z$ leaves $\langle\sigma_y\rangle$ undetermined. The tomographic threshold and the
  combinatorial bound are the *same* dimension count.
* **Optimality.** Wootters and Fields proved that a complete set of MUBs is the optimal choice
  of $d+1$ measurement settings, minimising the total statistical uncertainty of the estimate,
  and constructed such sets in every prime-power dimension **[paper [24]; the optimality
  statement is confirmed by the account in [1], cited: bandyopadhyay2002]**. In the
  orthogonal-frame form above it is transparent: the estimator is unbiased with the *same*
  variance in every direction of $H_0$, so no parameter is estimated worse than any other ---
  a property no other choice of $d+1$ bases has.

*Numerical check of the identities used here* ($\texttt{numpy}$, $d=2,\dots,6$, run while
writing): with $B$ the coordinate basis and $C$ the Fourier basis, the Gram matrix of the
$E^B_j$ is block-diagonal with blocks $I_d-\frac1dJ_d$ and zero cross-blocks (entrywise error
$<10^{-16}$), its rank is $2(d-1)$, and the identity
$\mathrm{tr}(P^B_jP^C_k)-1/d=|\langle b_j,c_k\rangle|^2-1/d$ holds to machine precision. So
(a.2) and the frame claim are confirmed, not merely asserted.

### a.4 Why prime powers are solved and composite dimensions are not

**Attainment for $d$ a prime power.** Identify $\mathbb{C}^d$ with functions on the field
$\mathbb{F}_d$ and let $X$ (cyclic shift) and $Z$ (diagonal phases) be the Weyl--Heisenberg
generators, $ZX=\omega XZ$ with $\omega=e^{2\pi i/d}$. Two Weyl operators $Z^{u}X^{v}$ and
$Z^{u'}X^{v'}$ commute exactly when $vu'-v'u=0\bmod d$, i.e. when $(u,v)$ and $(u',v')$ are
proportional; over a *field* the classes are the $d+1$ points of the projective line, and
taking one operator from each class gives $d+1$ operators whose eigenbases are pairwise
unbiased --- equivalently, the $d$ bases indexed by the finite slopes $a\in\mathbb{F}_d$
(eigenbases of $ZX^{-a}$, which includes $Z$ itself at $a=0$) together with the $X$-eigenbasis,
the Fourier basis, as the class at infinity **[paper [13],[24]; finite fields in [1], cited:
bandyopadhyay2002]**. I checked the two claims used here numerically for $d=2,3,5,7$: the
commutation criterion $vu'-v'u\equiv0$ holds for every pair of Weyl operators, and the
resulting $d+1$ eigenbases are pairwise unbiased to machine precision. The field enters exactly
here: proportionality must be an equivalence relation with $d+1$ classes, and nonzero
differences must be invertible. That is why the argument generalises verbatim from $d=p$ to
$d=p^m$ --- replace $\mathbb{Z}/p$ by $\mathbb{F}_{p^m}$, a field that is not a ring of
residues --- and stops there. Over $\mathbb{Z}/d$ with $d$ composite, zero divisors destroy both
properties, so this index set is not available; and no complete set is known in any composite
dimension **[cited: mcnulty2026]**.

**Composite $d$.** There is no field of order $6$, so the construction has nothing to run on,
and no substitute is known in any dimension that is not a prime power: "it remains unknown if
complete sets of MUBs exist in Hilbert spaces of dimensions different from a prime power, i.e.
in composite dimensions such as six or ten" **[cited: mcnulty2026, abstract]**. The problem
also changes character: for composite $d$ the second basis is not confined to a
low-dimensional family, and for $d=6$ the relevant variety of complex Hadamard matrices
contains continuous families together with isolated points (Tao's matrix) **[paper [7],[2]]**.
Any method that works by enumerating families must therefore control a genuinely continuous
object, which is exactly the obstruction the present paper attacks with covers.

Two general bounds frame the question:

* $N(d_1d_2)\ge\min\{N(d_1),N(d_2)\}$ (tensor a set for $d_1$ with the identity on the other
  factor). Hence $N(d)\ge p+1$ for $p$ the smallest prime factor of $d$; for $d=6$ this gives
  $N(6)\ge\min\{N(2),N(3)\}=\min\{3,4\}=3$. **[paper, Lemma 1.2; the general statement is
  derived from it]**
* $N(d)\le d+1$ by (a.3).

So before the present work the state of the smallest non-prime-power dimension was
$3\le N(6)\le7$, with the further remark that $N(6)\neq6$ (a general result of Weiner,
reported in **[cited: mcnulty2026]** --- second-hand from the review's text as returned by a
search, not from a read page). Every exact value of $N(d)$ known before now came from the
prime-power construction; $d=6$ is the first case where the value cannot be read off a
construction, and it is the smallest such case because $2,3,4,5$ are prime powers.

---

## (b) What the theorem says, and what it does not say

### b.1 The statement, in the paper's own terms

> **Theorem 1.1 (Computer-assisted).** Under the arithmetic and compiler conditions in
> Appendix A, the fresh complete execution documented in Section 7.5 certifies that there are
> no four pairwise mutually unbiased orthonormal bases in $\mathbb{C}^6$. Consequently
> $N(6)=3$. **[paper]**

and the lower bound, which is a theorem of the ordinary kind:

> **Lemma 1.2.** There exist three pairwise mutually unbiased orthonormal bases in
> $\mathbb{C}^6$. **[paper]** --- the tensor construction $U_r=A_r\otimes B_r$, $r=0,1,2$, with
> $A_0=I_2$, $A_1=\tfrac{1}{\sqrt2}\binom{1\ \ 1}{1\ -1}$,
> $A_2=\tfrac{1}{\sqrt2}\binom{1\ \ 1}{i\ -i}$, and $B_0=I_3$, $B_1=F$,
> $B_2=\mathrm{diag}(1,\omega,\omega)F$ where $F=(\omega^{jk}/\sqrt3)$ and $\omega=e^{2\pi i/3}$;
> then $(A_r^{*}A_s)\otimes(B_r^{*}B_s)$ has every entry of squared modulus $1/6$ for $r\ne s$.

I re-derived Lemma 1.2, including the Gauss sums
$(F^{*}DF)_{jk}=\frac13\sum_x\omega^{x^2+(k-j)x}$, which give
$|1+2\omega|^2=|2+\omega^2|^2=3$, so the lemma stands **[derived]**.

The theorem's logical shape is an implication. Write

* **(A) arithmetic and compiler model** --- binary64 IEEE-754 arithmetic, round-to-nearest,
  separately rounded operations with `-ffp-contract=off` and no fast-math or reassociation,
  correctly rounded square root, gradual underflow, no flush-to-zero, masked exceptions, and a
  stated ABI, compiler and platform **[paper, §7.1, A.1]**;
* **(B) execution** --- one particular run: 100 native invocations, begun 03:10:26 and
  completed 04:24:56 UTC on 4 October 2026, meeting the five terminal conditions of §7.2
  (empty bad files, zero unresolved records, consistent batch counts, fallback covering every
  initial failure, final shards partitioning the fallback) **[paper, §7.2, §7.5]**;
* **(C) implementation** --- seven C++ sources that do what §§2--6 say they do **[paper,
  §7.1]**.

Then **(A) and (B) and (C) imply: no four MUBs in $\mathbb{C}^6$**, i.e. $N(6)\le3$.

The mathematics --- the reduction of "no four MUBs" to a finite conjunction of checked
inequalities --- is *not* conditional on anything. It is a chain of lemmas, each an
implication, from the seed cover of §2 through the completion cover of §§3--4, the refinement
of §5 and the exclusion of §6 to the finite-execution theorem of §7.4. What is conditional is
that the antecedent of that final implication was satisfied in the physical world.

### b.2 What is unconditional, what is conditional, what is reported

| item | status |
|---|---|
| $N(6)\ge3$ (Lemma 1.2) | unconditional, elementary, verified **[derived]** |
| the covering/exclusion lemmas of §§2--6, as statements | unconditional mathematics, written out; audited statement by statement in `results/proof-claims.md`, with the long ones sampled rather than fully re-derived |
| the assembly Propositions 2.10, 3.11, 4.16, 5.7, 6.9 and Theorem 7.1 | unconditional *as implications*; each carries a premise that a routine behaves as described, or that a traversal closed |
| (A) arithmetic model | **assumption**. The paper says so itself: "those semantics remain assumptions" **[paper, §7.1]** |
| (B) the 4 October 2026 run | **event**, documented in Tables 1--2 and, in part, in the published archive |
| (C) the seven programs | **conformance claim** unless the sources are read. They are published (see b.4); I have not read them |
| Table 1 counts, Table 2 digests | **[reported]** |
| Corollary 1.3 (Cartan subalgebras) | inherits (A) and (B) and (C) from Theorem 1.1, and rests on a citation [3, Thm 5.2]; adds no difficulty of its own |

This is *not* a formal verification: no proof assistant is involved, no checker verifies a
certificate, and the trust base is seven programs plus the compiler plus the machine. It is
also not a proof of the kind the field has historically demanded for a conjecture of this age
--- a written argument a referee can follow to the conclusion without running anything. It is
a third kind of object: **a certified negative outcome of a finite computation**, whose
mathematical content is the reduction and whose empirical content is the run.

The paper is careful about provenance in one place worth crediting: an earlier run of 7
September 2026 is described and then explicitly *not* relied on --- "The complete evidence
packet for the execution reported on 7 September 2026 was not recovered ... this agreement does
not authenticate the earlier execution" **[paper, §7.5]**. The proof uses only the new run.

### b.3 If the execution is sound, what is established

1. **$N(6)=3$**, hence the first exact value of $N(d)$ in a dimension that is not a prime
   power. If sound, this is a new theorem about $\mathbb{C}^6$, not a sharpening of an
   existing estimate.
2. An upper bound that quantifies over **all** complex Hadamard matrices of order 6 --- the
   second basis is arbitrary, with no restriction to a family. That is strictly stronger than
   Grassl's exclusion of quartets containing the coordinate and Fourier bases **[paper [9]]**
   and than the exclusion of the coordinate basis with any member of the two-parameter Fourier
   family **[paper [15]]**. The gap between "known families" and "all matrices" is exactly the
   gap this paper claims to close.
3. A single negative answer where previously there was a range: the question had stood open
   since at least Zauner's 1991 diploma thesis **[paper [25]]**, and was explicit as
   Conjecture 1 of **[paper [16]]**.
4. The Lie-algebra corollary: at most three pairwise Killing-orthogonal, adjoint-closed Cartan
   subalgebras of $\mathfrak{sl}_6(\mathbb{C})$ **[paper, Cor. 1.3]**, *conditional on the same
   three items*.

What it does **not** establish, even if the execution is sound:

* **not** a classification of MUB triples in $\mathbb{C}^6$. An infinite family of inequivalent
  triplets is known **[paper [15], title]**, so $N(6)=3$ does not say the tensor triple of
  Lemma 1.2 is the only one, nor does it say anything about which triples exist.
* **not** uniqueness or rigidity of anything: the theorem bounds a maximum, not a structure.
* **nothing about Zauner's other, better-known conjecture.** "Zauner's conjecture",
  unqualified, denotes in the quantum-information literature the *SIC-POVM* statement ---
  existence in every dimension of a Weyl--Heisenberg SIC fiducial that is an eigenvector of an
  order-three Clifford unitary, the "Zauner unitary" **[cited: fuchs2017sic]**. The MUB
  statement $N(6)=3$ is a different conjecture from the same thesis. The abstract's phrase
  "Zauner's dimension-six MUB conjecture" is correct and must not be shortened to "Zauner's
  conjecture".
* **nothing about other composite dimensions**, in particular nothing about $d=10$: the
  pipeline uses the $2+4$ block split, 36 phases, twelve candidate vectors, six-cliques and
  $12^5$ bins, all dimension-6 specific. See section (c).
* **no compact, human-checkable object.** The certificate is the run --- 249,878 seed centres,
  22,379 fine records, 1,127 fallback records, 100 invocations. There is no short witness to
  inspect.
* **no robustness statement.** That the run *completed* is not the same as that it completed
  with margin; the margins live in Appendix A and were not stress-tested.

### b.4 What a reader can actually check (correcting a premise of this project)

The project's working premise --- "the seven sources, the execution archive and the certificates
are not available" (`results/plan.md`, `work/00-lead/decisions.md` D1) --- is true of the packet
that was supplied (the PDF alone) but **not** true of the world. I checked on 2026-11-14 by
querying the GitHub API:

* the preprint PDF is public under
  `github.com/openai/math/tree/main/preprints/`, directory
  `The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026`
  (file size 817,737 bytes --- identical to the packet copy `.scratch/mub6.pdf`);
* the **seven sources are published**: `verification/saved-run/compiled-build/source/` contains
  `seed.cpp` (3514 B), `covout.cpp` (5286 B), `ub.cpp` (11557 B), `patchx.cpp` (16137 B),
  `atlas.cpp` (8821 B), `stageB.cpp` (12030 B), `stageC.cpp` (17471 B), plus
  `abi-fp-probe.cpp` (2496 B). Every byte length agrees with `verification/code/extraction.json`,
  and that manifest is the *only* thing in `verification/code/` --- it is not code;
* `verification/saved-run/` also holds `VERIFY.md`, `compiled-build/build.sh`, and an
  `execution/` directory described there as containing the numerical records, `commands.json`,
  `results/` and a `check_records.py` consistency checker;
* the authors' `VERIFY.md` states what is *not* published: "no compiled programs, archive
  inventories, hash checks, raw process logs, machine/session records, supervision code, or
  review narratives", and describes `check_records.py` as "a numerical consistency check, not an
  authentication of the historical archive, a proof of the C++ implementation, or a verification
  of compiler and hardware behavior."

Consequences, stated precisely:

* condition (C) is *inspectable*, not unavailable. I have not read the sources, so I make no
  claim about whether they implement §§2--6; `results/code-audit.md` is an audit of the
  *specification* and stays valid as such;
* condition (B) is *partly* inspectable: the numerical records and their consistency can be
  re-checked, but the provenance evidence tying them to the stated machine and date is not
  published, and Table 2's SHA-256 values cannot be compared against any published archive;
* condition (A) remains an assumption in the paper's own words, and no published artefact
  discharges it.

That is a materially better status than "unauditable" and a materially worse one than "formal
verification". It is what the status paragraph has to say.

### b.5 How it can fail, and why the failure mode is benign

The architecture makes failure *visible*: every exclusion tests a **necessary** condition, and
an exhausted search cap or a failed certification retains the region as unresolved rather than
declaring it empty **[paper, §1.2, §6.7]**. So a timeout, a cap, or an unconverged heuristic
produces a nonzero unresolved count --- which the terminal conditions of §7.2 explicitly forbid
--- rather than a false exclusion. In this run 163 records did exhaust the graph-step cap at
initial Stage C and were routed to the fallback, which returned no unresolved record **[paper,
Table 1]**. That is the mechanism working as designed.

The residual risk is therefore not "the search gave up quietly" but three narrower things:
(i) a certifying routine whose *specification* is unsound, so that a check passes when it should
not --- `results/code-audit.md` F1 nominates `buildH::patch` (Prop. 4.6) as the highest
consequence instance, with the Stage-B traversal, the Stage-C bin/cluster machinery and the
clique search (Lemma 6.8, the one lemma whose subject is a program) behind it; (ii) a mismatch
between the assumed arithmetic and what the compiled code does; (iii) an implementation defect
in a one-sided comparison. All three are *checkable* --- that is the point of publishing the
sources --- and none is checkable from the PDF alone.

### b.6 Related independent claims (August--November 2026)

Two preprints by Cárdenes Wuttig and Tindall are relevant and must not be conflated with this
one:

* **arXiv:2608.18053v2** (18 Aug 2026), *A Complete Classification of Complex Hadamard Matrices
  of Order Six* --- an exact finite-incidence classification of order-six complex Hadamard
  matrices up to standard equivalence, supplying "the global step missing from Szöllősi's
  dilation method". It classifies Hadamard matrices; it does not by itself settle MUB
  compatibility **[cited: cardeneswuttig2026hadamard, abstract fetched]**.
* **arXiv:2611.06917v1** (4 Nov 2026), *Using topology to reveal all mutually unbiased bases in
  dimension six* --- reports an independent proof that no four MUBs exist in $\mathbb{C}^6$
  **and** a classification of all MUB triples, via connectedness of the space of order-six
  complex Hadamard matrices outside Tao's matrix, certified with interval arithmetic
  **[cited: cardeneswuttig2026topology, abstract fetched]**.

If the second claim is sound it corroborates the conclusion by a different route with a
different trust base: connectedness of the order-six Hadamard space plus interval-arithmetic
certification of a finite cover, rather than nine-phase balls plus binary64 margins plus a
100-process run. The two arguments also do not share their inputs, and the difference cuts in
the preprint's favour: the topological route rests on the order-six classification of
**[cited: cardeneswuttig2026hadamard]** (whose result it uses as the connectedness input),
whereas the covering argument of the present preprint depends on no Hadamard classification at
all --- it quantifies over all complex Hadamard matrices directly. That is the correct way to
state the relation: *not* more of the same, and *not* logically independent in the sense of
sharing nothing, but complementary in what each has to trust.

Caveats that must survive into the final text: it is a ten-day-old preprint; I have read only
its abstract, not its proof; and it is not peer reviewed. So the draft should not call this
paper the only or the definitive argument, and should not borrow "independently confirmed"
either. The honest sentence is: *two independent computer-assisted arguments, with different
verification technologies and different dependencies, now report the same answer.*

### b.7 One wording fix in the abstract

The abstract says the pipeline "excludes four arbitrary complex bases". Read literally that
says four particular bases are excluded; what is meant is that *every* quartet is excluded, or
equivalently that no four bases exist. Suggest "excludes every quartet of bases", or "excludes
an extension of any pair of bases by two further bases". This is the kind of phrase a referee
reads as a hedge and an opponent reads as an error.
