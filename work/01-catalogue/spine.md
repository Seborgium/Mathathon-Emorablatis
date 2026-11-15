# The assembly spine: Theorem 1.1 from the six stage statements

**Author** T1/m1 (direction d6). **Status** complete for its scope: the top-level implication
is proved here with explicit quantifiers, and every interface the proof crosses is named and
checked against the paper's own wording. No step is asserted that is not either (i) proved
below, (ii) a quotation of a numbered paper statement, or (iii) an explicit *interface
obligation* listed in §5 with its verdict.

**Scope.** This file does not restate or re-check the analysis inside the six stages. It answers
one question: *do the six stage conclusions, as the paper states them, actually compose into a
proof of Theorem 1.1, and under exactly which side conditions?* It is written so that T4 can
transcribe it (the shape is given in `lean/Interface.lean`) and T8 can cut it up for the paper.

**Source anchors.** `.scratch/mub6.txt` line numbers from the extraction; page numbers from the
PDF where a page was needed. Every quotation below is verbatim from the extraction.

---

## 0. Summary of findings

1. The assembly **is** sound. Composed in the order
   $\text{MUB}\to\text{CHM}\to\text{seed ball}\to A\text{ record}\to B\text{ fine record}\to
   C\text{ batch record}\to\text{negative}$, the implication closes with no missing step.
2. The six stage conclusions all have the **same shape**: a *cover transfer* between regions of
   a single space, up to a fixed equivalence relation. Naming that relation once, and writing
   every stage as `Rep(|in|) ⊆ Rep(|out|)`, makes the assembly three lines. This is the main
   statement simplification of this file.
3. Three interfaces are **implicit** in the paper and load-bearing; see §5.
   The one that is a real constraint rather than a convention is **I3**: Proposition 6.9 is
   stated only for records of radius $r\le .03$, while the preceding stages are stated for radii
   up to $.126$. Composition is possible only after the *second* $B$ pass ($\tau=.016$), never
   after the first ($\tau=.07$). The paper's proof of Theorem 7.1 uses the right order, but the
   inequality that makes it legal is nowhere assembled in one place.
4. Theorem 1.1 has **no mathematical content beyond Theorem 7.1 plus the observed run**:
   Theorem 7.1 $\Rightarrow$ no four MUBs, Lemma 1.2 $\Rightarrow$ three exist. The paper's
   main theorem therefore has an *execution record* in its hypothesis. This is a statement of
   fact about the paper, not a criticism; T8 should say it in the abstract rather than let a
   reader discover it in §7.4.
5. Corollary 1.3 rests on an external citation that this project cannot check ([3, Thm 5.2]).
   It is the only claim in the paper whose evidence is outside the packet.

---

## 1. The object, fixed once

The paper carries the same objects under several names (`Root`, `Record`, `ball`, `sphere`,
`cell`, `bin`, `box`) and the same constants under three naming systems. For the assembly only
five notions are needed, and they are fixed here for the rest of this file.

**1.1 Phase matrices.** $P\in\mathbb R^{6\times 6}$, identified with $\mathbb R^{36}$ by
row-major order. $e(P)_{ij}=\exp(2\pi i P_{ij})$. Entries of $P$ are in **cycles**; the paper's
`e(t)` takes cycles. $\Pi$ is the double centering (2.1) and
$\mathcal H=\operatorname{ran}\Pi$ is the *horizontal subspace* (zero row and column sums).
$\|\cdot\|$ is Euclidean on $\mathbb R^{36}$ (Frobenius on matrices).

**1.2 Residual.** $F(P)\in\mathbb C^{15}\cong\mathbb R^{30}$ by
$F_{ij}(P)=\frac1{2\pi i}\sum_{g}e(P_{ig}-P_{jg})$, $i>j$, ordered by increasing $i$ then $j$
(4.1). $\|F(P)\|$ is the Frobenius norm of the realified vector.

> **Lemma S.1 (residual $\leftrightarrow$ Hadamard).** For $P\in\mathbb R^{36}$,
> $F(P)=0 \iff e(P)e(P)^*=6I$. Since $e(P)$ is square and every entry has modulus one, this also
> gives $e(P)^*e(P)=6I$. Hence $F(P)=0\iff e(P)$ is complex Hadamard in the sense of
> Definition 2.1. Moreover $\|F(P)\|^2=(\|AA^*\|_F^2-216)/(8\pi^2)$ for $A=e(P)$.

*Proof.* On the diagonal of $AA^*$ every entry is $\sum_g 1=6$ automatically, so $AA^*=6I$ is
equivalent to the vanishing of the 15 off-diagonal entries, i.e. of the sums
$\sum_g e(P_{ig}-P_{jg})$. Invertibility of $e(P)$ turns $AA^*=6I$ into $A^*A=6I$: multiply by
$A^{-1}$ on the left and by $A$ on the right. The norm identity is the paper's, used in the
proof of Lemma 4.7; it follows by expanding $\|AA^*-6I\|_F^2=\|AA^*\|_F^2-432+216$ and
cyclicity of the trace in $\|AA^*\|_F^2=\|A^*A\|_F^2$. $\square$

*Consequence used everywhere:* a "certified centre" need not satisfy $F(P)=0$; the residual
only needs to be *small* and *bounded*.

**1.3 Solutions and Records.** For $P\in\mathbb R^{36}$ and $R\ge0$ put

$$\mathrm{Sol}(P,R)=\{\,e(P+\delta)\;:\;\delta\in\mathcal H,\ \|\delta\|\le R,\ F(P+\delta)=0\,\}.$$

This is the solution set of the Record $(P,R)$ (Definition 4.14), written as a set of *matrices*
rather than a set of classes. For a finite family $\mathcal R$ of pairs $(P,R)$,
$|\mathcal R|=\bigcup_{(P,R)\in\mathcal R}\mathrm{Sol}(P,R)$.

**1.4 The equivalence group.** Let $\mathcal G$ be the group generated by

* row permutations, column permutations ($S_6\times S_6$);
* row rephasings and column rephasings: $M\mapsto e(r_i)M e(c_j)$ with $r,c\in\mathbb R^6$;
* entrywise integer phase changes $M_{ij}\mapsto e(N_{ij})M_{ij}$, $N\in\mathbb Z^{6\times6}$;
* complex conjugation $M\mapsto\overline M$;
* transposition $M\mapsto M^T$;
* a global sign $M\mapsto -M$.

Write $M\sim M'$ iff $M'=gM$ for some $g\in\mathcal G$, and $\mathrm{Rep}(X)=\bigcup_{x\in X}[x]$
for a set $X$ of matrices. Note that $r,c,N$ are *not* required to be bounded: $\mathcal G$
contains rephasings by arbitrary reals, so $\mathrm{Sol}(P,R)$ and $\mathrm{Sol}(P+z,R)$ with
$z$ constant on rows and columns are $\sim$-equivalent as *sets of classes*, which is exactly
the freedom (4.17) uses.

> **Lemma S.2 (the equivalence is admissible).** For $M,M'$ unit-entry $6\times6$ matrices with
> $M\sim M'$: $M$ is complex Hadamard iff $M'$ is, and $M$ is extendible by two further bases
> together with the coordinate basis iff $M'$ is.

*Proof.* This is Lemma 2.2 plus three trivial generators. Permutations/rephasings/global sign
act as a common unitary on all four bases or as a relabelling of vectors inside a basis; complex
conjugation preserves orthogonality and all moduli $|\langle b,c\rangle|$; transposition is
Lemma 2.2's argument. The extra generators are either common unitaries (global sign) or
dephasings (integer shifts, subsumed by rephasings). See §6.3 for the transposition proof
written out. $\square$

*This lemma is the licence for every "up to equivalence" clause in the paper, and it is the only
place the assembly uses any geometry at all.* Two corollaries are used silently by every stage
statement and are worth recording:

> **Corollary S.3.** (a) $\mathrm{Rep}(\mathrm{Rep}(X))=\mathrm{Rep}(X)$.
> (b) If $\mathrm{Rep}(X)\subseteq\mathrm{Rep}(Y)$ and $\mathrm{Rep}(Y)\subseteq\mathrm{Rep}(Z)$
> then $\mathrm{Rep}(X)\subseteq\mathrm{Rep}(Z)$. (c) If $X\subseteq Y$ then
> $\mathrm{Rep}(X)\subseteq\mathrm{Rep}(Y)$.

*Proof.* (a) $\mathcal G$ is a group. (b) transitivity of $\subseteq$. (c) monotonicity. $\square$

**1.5 Extendibility.** Call a complex Hadamard matrix $H$ **extendible** if the coordinate basis
and the columns of $H/\sqrt 6$ belong to a family of four pairwise mutually unbiased orthonormal
bases (Definition 2.1). "$\mathrm{Ext}(M)$" below means: $M$ is unit-entry and extendible.
By Lemma S.2, $\mathrm{Ext}$ is $\mathcal G$-invariant.

**1.6 The cover relation.** For finite families $\mathcal R,\mathcal S$ of Records write

$$\mathcal R\ \sqsupseteq\ \mathcal S \quad:\Longleftrightarrow\quad
 \mathrm{Rep}(|\mathcal S|)\subseteq\mathrm{Rep}(|\mathcal R|).$$

By Corollary S.3, $\sqsupseteq$ is reflexive and transitive. **Every stage conclusion in the
paper is an instance of $\sqsupseteq$, or of its pointwise version** "every extendible exact $H$
lies in $\mathrm{Rep}(|\mathcal R|)$". The assembly is then a chain of $\sqsupseteq$.

---

## 2. The six stage statements, in fixed form

Each stage is quoted (abridged only where marked `…`) and then written in the fixed notation of
§1. Where the paper's statement is weaker or vaguer than the fixed form, the difference is named
in **bold brackets** and adjudicated in §5.

### 2.1 I0 — from four MUBs to an extendible complex Hadamard matrix

Paper, §1 (p. 3): *"A common unitary transformation makes one basis the coordinate basis. The
second is then the column basis of $H/\sqrt6$, where $H$ is a complex matrix satisfying
$|H_{ij}|=1$, $HH^*=6I$. Such an unscaled matrix is called a complex Hadamard matrix. … The
second basis is unrestricted: the argument covers arbitrary complex Hadamard matrices …"*

Fixed form. **Let $m\ge2$ and let $B_0,\dots,B_{m-1}$ be pairwise mutually unbiased orthonormal
bases of $\mathbb C^6$. Then there is a unitary $U$ and a complex Hadamard $H$ such that
$UB_0$ is the coordinate basis and $UB_1$ is the column basis of $H/\sqrt6$; and if $m=4$ then
$H$ is extendible.**

Proved in §6.1 below (G1). This is the only *input* conversion in the whole proof; everything
after it is in the language of phase matrices.

### 2.2 S0 — the seed cover (Proposition 2.10)

Paper, p. 11, verbatim: *"For a completed execution of the specified `covout` traversal under the
arithmetic conditions of Section A, the written rational midpoint centers, each with its recorded
selected position, cover the seed coordinates of every exact complex Hadamard matrix up to the
equivalences of Lemma 2.2, by closed Euclidean balls of radius $0.032$. After the indicated
column ordering and conversion of the centers to binary phase values, radius $0.0320001$ is
sufficient."*

Fixed form. **Let $\mathrm{Cov}\subset\mathbb Q^9\times\{0,1,2,3,4\}$ be the set of written
centres of a completed `covout` traversal, each with its recorded selected position. Then for
every $P$ with $F(P)=0$ there are $(u,s)\in\mathrm{Cov}$ and a representative $P'\sim e(P)$ (as a
phase matrix) such that, after the ordering of §2.4 with selected position $s$, the nine seed
coordinates $q(P')\in\mathbb R^9$ satisfy $\|q(P')-u\|\le 0.0320001$.**

Notation: $q(P)=(x_1,\dots,x_5,y_2,\dots,y_5)$ is (2.15), the nine phases other than the fixed
zeros in the dephased first two rows and columns. "With selected position $s$" means: the five
$x$-coordinates are permuted so that $x_{s+1}$ comes first (paper, p. 11: *"The resulting order is
the selected X entry, the other four X entries in order, and the four Y tail entries. These are
precisely the nine entries of the dephased first two rows and columns used in the next stage."*).

**The entries of $u$ are in cycles, and so is the radius $0.032$.** The number $0.032$ is
$\frac{3}{2N}=3/224$ rounded up, $N=112$; it is *not* an angle in radians.

*What S0 does not say, and does not need to:* that the centre is exact; that a given $H$ is
reached by the *same* equivalence used later; that the ball is unique. All three freedoms are
consumed by Lemma S.2 and Corollary S.3.

### 2.3 A — completion over one seed ball (Propositions 3.11 and 4.16)

Paper, Prop. 3.11 (p. 20): *"Fix a seed ball for which the frame and bound constructions are
certified. Suppose that every final unitary cell is either excluded by a certified
necessary-condition test or covered by a certified phase ball as in Section 4. Then those phase
balls cover all feasible Hadamard completions of the seed ball, with the equivalences specified
by the phase-ball certificates. The Stage A recursion establishes precisely this conclusion if
it terminates with zero unresolved cells."*

Paper, Prop. 4.16 (p. 32): *"Suppose the initial seed cover is valid and the completion search
processes all its seeds with no failed or unresolved seed. Then the A-stage Records cover, up to
extendibility-preserving equivalence, every exact second-basis Hadamard matrix required for the
four-basis problem."*

Fixed form. **Let $\mathcal R_A$ be the union of the four coarse record files of a Stage A run in
which every seed centre was processed, no seed failed, and no seed has an unresolved cell. Then
for every $P$ with $F(P)=0$ whose seed coordinates at its recorded selected position lie in the
seed ball of a processed centre, $\mathrm{Rep}(\{e(P)\})\subseteq\mathrm{Rep}(|\mathcal R_A|)$.**

Two remarks that matter for the assembly.

* **"required for the four-basis problem" can be replaced by "every".** Prop. 4.16's *proof*
  follows *any* feasible matrix through the cell tree: *"The completion parametrization covers
  each feasible matrix in a seed by its closed unitary cells. Follow any such matrix through
  containing cells."* Feasibility here is $F(P+\delta)=0$, not extendibility. The word
  "required" is therefore a weakening of what is proved, and the fixed form above uses the
  stronger statement. **Proposed to T8: delete "required for the four-basis problem".**
* Prop. 3.11 is about *cells*, Prop. 4.16 about *seeds*. The assembly only uses 4.16; 3.11 is an
  internal step. It is listed here because it is the statement a reader needs in order to see why
  A is a finite object at all.

### 2.4 B — refinement of a record family (Proposition 5.7, Corollary 5.8)

Paper, Prop. 5.7 (p. 38), verbatim: *"Suppose Stage B is run on a finite list of records with
valid Root certificates, under the arithmetic assumptions and error bounds of Section A. On a
completed run, let $\mathcal A$ be its final atlas of children and let $\mathcal B$ be the list of
input parents whose refinement failed. Then*
$$\bigcup_{(P,R)\ \text{input}}\!\! S(P,R)\;\subseteq\;\bigcup_{(Q,r)\in\mathcal A}\!\!S(Q,r)\ \cup\ \bigcup_{(P,R)\in\mathcal B}\!\! S(P,R).$$
*In particular, a completed run with no bad parents replaces the input cover by a child cover. A
nonempty bad list remains an obligation."*

Paper, Cor. 5.8 (p. 39): *"Under the hypotheses of Proposition 5.7, suppose a batching invocation
completes with no bad parents and every emitted batch is included. Then the input solution sets
are covered, up to the permitted equivalences, by the emitted records with their stored target
radius $\tau$."*

Fixed form. **Let $\mathcal I$ be a finite family of Records with valid Root certificates, and
let a Stage B invocation with parameters $(\tau,w)$ complete on $\mathcal I$ with no failed
parent, every emitted batch included. Let $\mathcal O$ be the emitted batch records at radius
$\tau$. Then $\mathcal O\sqsupseteq\mathcal I$, i.e.
$\mathrm{Rep}(|\mathcal I|)\subseteq\mathrm{Rep}(|\mathcal O|)$.**

The paper's $\mathcal S(P,R)$ in (5.1) is my $\mathrm{Sol}(P,R)$, written with classes; the
inclusion is stated there for plain sets, which is stronger.

### 2.5 C — local exclusion in one record (Proposition 6.9)

Paper, §6.1 (p. 41): *"Fix a Record with center $P\in\mathbb R^{6\times6}$, radius
$0\le r\le .03$, and real tangent matrix $T\in\mathbb R^{36\times k}$, where $0\le k\le 10$."*

Paper, Prop. 6.9 (p. 48), verbatim: *"Assume the root certificate (6.1)–(6.2) and the arithmetic
guarantees of Section A. If Stage C returns a negative result for the Record, then no exact
Hadamard $e(P+\delta)$ in its closed horizontal radius-$r$ ball can be extended, together with
the coordinate basis, by two further mutually unbiased orthonormal bases."*

Fixed form. **Let $(P,r)$ be a Record with $0\le r\le .03$, a Root certificate in the sense of
Definition 4.1 with constants in the admitted ranges of §5.6, and a negative Stage C result.
Then $\mathrm{Rep}(\mathrm{Sol}(P,r))\cap\{\text{extendible unit-entry matrices}\}=\varnothing$.**

The passage from the paper's "no exact $e(P+\delta)$ in the ball" to my class statement is
Lemma S.2: extendibility is $\mathcal G$-invariant, so excluding the ball excludes every class
that meets it. This step is used in the assembly and is *not* written in the paper.

### 2.6 X — the execution conditions (Section 7.2)

Paper, p. 51, verbatim: *"The required terminal conditions are:*
1. *successful builds, a normally completed cover, and a complete center file;*
2. *four A exits 0, all assigned centers processed, terminal `failedBalls=0`, and four empty bad
   text files;*
3. *both B exits 0, all input parents processed, agreement of logged and saved output counts, and
   zero-count B bad files;*
4. *every initial C batch processed exactly once with consistent exit, done count, bad count, and
   saved records;*
5. *every initial C bad record included in fallback, fallback exit 0 with all parents processed
   and zero saved failures, and four final C exits 0 with total done equal to the fallback count
   and zero saved failures."*

Fixed form, as the seven predicates the assembly consumes:

| id | predicate | used at |
|---|---|---|
| X1 | the cover run completed normally and `centers.txt` is complete | S0 |
| X2 | the four A shards partition the centre indices and each exited 0 with `failedBalls=0` and all centres processed | A |
| X3 | `mid.bin` = B mid's complete output, no failed parent | B (first) |
| X4 | `fine.bin` = B fine's complete output, no failed parent | B (second) |
| X5 | every record of `fine.bin` appears in exactly one emitted batch, with radius $\tau=.016$, and every batch was processed by initial C exactly once | I3, C |
| X6 | the initial-C bad files are ordered subsequences of their batch inputs, and B fallback consumed all of them | fallback |
| X7 | B fallback and the four final C shards completed with zero saved failures, and the shards partition the fallback records | C (final) |

X5 and X7 are *identity* conditions (counts, partitions, subsequences), not geometric ones. The
paper says this: *"counts and hashes establish the identity and completeness of the finite chain,
not those inequalities in isolation"* (p. 53). T8 should keep that sentence.

### 2.7 What a "completed run" is not

Three times the paper relies on the distinction between a *diagnostic* and a *failure*, and once
it is easy to misread:

* A's `ownfail` counter increments on unsuccessful proposals of a local Root cover that are
  followed by subdivision. §7.5 records that *"A0 reported such a diagnostic in this run; its
  terminal unresolved count was nevertheless zero."* So **`ownfail > 0` is compatible with X2**,
  and the assembly must use the terminal `failedBalls`/unresolved counts, not the diagnostic.
* Run-cap exhaustion (grid 50M, atlas 2M, depth 6, graph 5M steps, bin cap 2M, 2048 clusters)
  is *never* an exclusion (Lemmas 5.6, 6.4, 6.8; Prop. 6.9's last paragraph).
* An intermediate batch file is not a certificate: *"The existence of an intermediate batch, or
  even a count marker without the exit and bad-list checks, is not a certificate that all parents
  were covered"* (§5.6, p. 39).

---

## 3. The assembly theorem

### 3.1 Statement

**Theorem 3.1 (assembly).** Let the following hold.

* **(A1) Cover.** $\mathrm{Cov}$ is a finite set of centres-with-selected-position satisfying
  S0 of §2.2, and the cover run completed (X1).
* **(A2) Seed-radius compatibility.** Stage A reads exactly the centres $\mathrm{Cov}$, and its
  seed radius satisfies $r_s\ge 0.0320001$.
* **(A3) A.** The four Stage A shards partition the centre indices, satisfy X2, and their output
  $\mathcal R_A$ satisfies A of §2.3 for every processed centre.
* **(A4) B.** The two Stage B invocations satisfy X3, X4 and B of §2.4 on their respective input
  families: $\mathcal O_{\mathrm{mid}}\sqsupseteq\mathcal R_A$ and
  $\mathcal O_{\mathrm{fine}}\sqsupseteq\mathcal O_{\mathrm{mid}}$.
* **(A5) Batching.** X5 holds, and the batch target radius satisfies
  $\tau_{\mathrm{fine}}=.016\le .03$.
* **(A6) C, first pass.** Every record of the fine batch family $\mathcal O_{\mathrm{bat}}$
  satisfies the hypotheses of C of §2.5 (valid Root certificate, $r\le .03$), and each initial
  C invocation either returns negative or saves the record as a failure.
* **(A7) C, final pass.** X6 and X7 hold; the fallback family $\mathcal O_{\mathrm{fb}}$
  satisfies C of §2.5 with $\tau_{\mathrm{fb}}=.011$, and all four final shards return negative.

Then there do not exist four pairwise mutually unbiased orthonormal bases of $\mathbb C^6$.

### 3.2 Proof

Suppose $B_0,B_1,B_2,B_3$ are pairwise mutually unbiased orthonormal bases.

**Step 0 (I0).** By §6.1 (G1) there are a unitary $U$ and an extendible complex Hadamard $H$
such that $UB_0$ is the coordinate basis and $UB_1$ is the column basis of $H/\sqrt6$. Replace
the family by its image; unbiasedness, orthonormality and the cardinality are unchanged. So it
suffices to derive a contradiction from "there is an extendible complex Hadamard $H$".

**Step 1 (S0).** Put $P$ with $e(P)=H$, so $F(P)=0$ by Lemma S.1. By (A1) and S0 there are
$(u,s)\in\mathrm{Cov}$ and a phase matrix $P'\sim P$ such that $\|q(P')-u\|_{\mathbb R^9}\le
0.0320001$ at selected position $s$. By Lemma S.2, $e(P')$ is an extendible complex Hadamard.

**Step 2 (A).** The pair $(u,s)$ is a row of the Stage A input by (A2), and the distance bound is
within the seed radius $r_s$. By (A3) and A of §2.3 applied to the exact matrix $e(P')$,
$$\mathrm{Rep}(\{e(P')\})\ \subseteq\ \mathrm{Rep}(|\mathcal R_A|).$$
So there is a record $\rho_A\in\mathcal R_A$ with $e(P')\in\mathrm{Rep}(\mathrm{Sol}(\rho_A))$.

**Step 3 (B, twice).** By (A4), Corollary S.3(b) and two applications of $\sqsupseteq$,
$\mathcal O_{\mathrm{fine}}\sqsupseteq\mathcal R_A$. Hence
$e(P')\in\mathrm{Rep}(|\mathcal O_{\mathrm{fine}}|)$.

**Step 4 (batching).** Each record $(Q,r)$ of $\mathcal O_{\mathrm{fine}}$ has $r\le
\tau_{\mathrm{fine}}$ (Corollary 5.8 emits at $\tau$), so
$\mathrm{Sol}(Q,r)\subseteq\mathrm{Sol}(Q,\tau_{\mathrm{fine}})$, and by X5 the family
$\mathcal O_{\mathrm{bat}}$ is exactly $\{(Q,\tau_{\mathrm{fine}})\}$ over the same centres.
Hence $\mathrm{Rep}(|\mathcal O_{\mathrm{fine}}|)\subseteq
\mathrm{Rep}(|\mathcal O_{\mathrm{bat}}|)$ and $e(P')\in
\mathrm{Rep}(|\mathcal O_{\mathrm{bat}}|)$. Let $\rho_{\mathrm{bat}}$ be the batch record
involved.

**Step 5 (C, two branches).** Run initial C on $\rho_{\mathrm{bat}}$. By (A6) exactly one of two
things happens.

* *Negative.* By (A5) $r=.016\le .03$ and by (A6) the Root certificate is valid, so C of §2.5
  gives $\mathrm{Rep}(\mathrm{Sol}(\rho_{\mathrm{bat}}))\cap\{\text{extendible}\}=\varnothing$.
  But $e(P')\in\mathrm{Rep}(\mathrm{Sol}(\rho_{\mathrm{bat}}))$ and $e(P')$ is extendible.
  Contradiction.
* *Saved as a failure.* By X6 that record of $\mathrm{Sol}(\rho_{\mathrm{bat}})$ is an input
  parent of B fallback, so by B (with $\tau_{\mathrm{fb}}=.011$) and (A7),
  $e(P')\in\mathrm{Rep}(|\mathcal O_{\mathrm{fb}}|)$ with no failed parent; the four final
  shards partition $\mathcal O_{\mathrm{fb}}$ (X7), so $e(P')$ lies in the class of a record of a
  final shard. That shard returned negative, and $r=.011\le.03$, so C of §2.5 again gives
  $\mathrm{Rep}(\mathrm{Sol}(\cdot))\cap\{\text{extendible}\}=\varnothing$, contradicting
  extendibility.

Either branch is contradictory, so no extendible complex Hadamard exists, so no four MUBs exist.
$\blacksquare$

### 3.3 The same proof in three lines

Using §1.6, the chain is
$$\{H\}\ \xrightarrow{\ \mathrm{S0}\ }\ \mathcal R_A\ \xrightarrow{\ \mathrm{B}_{\mathrm{mid}}\ }\ \mathcal O_{\mathrm{mid}}\ \xrightarrow{\ \mathrm{B}_{\mathrm{fine}}\ }\ \mathcal O_{\mathrm{fine}}\ \xrightarrow{\ \text{batch}\ }\ \mathcal O_{\mathrm{bat}}\ \xrightarrow{\ \mathrm{C}\ }\ \varnothing,$$
where every arrow means $\mathrm{Rep}(\text{target})\supseteq\mathrm{Rep}(\text{source})$ and the
last means $\mathrm{Rep}(|\mathcal O_{\mathrm{bat}}|)\cap\{\text{extendible}\}=\varnothing$. The
fallback is the second exit from the last arrow, not a separate stage.

### 3.4 Where the proof is fragile, exactly

Nothing in Theorem 3.1's *logic* can fail; the proof is a chain of inclusions. Four things can
fail, and they are the four things to check:

1. **A hypothesis in (A1)–(A7) not actually met by the run.** This is the whole empirical
   content: the paper's §7.5 says it was met, and the evidence is the execution archive, which
   this project does not have (decision D1 in `work/00-lead/decisions.md`).
2. **A stage statement weaker than the fixed form used here.** Adjudicated in §4; the only
   substantive one is C's radius bound (I3).
3. **The equivalence being used inconsistently between stages** (I6). Adjudicated in §4.
4. **A stage's own proof being wrong.** Out of scope here; that is T2/T3/T9.

So Theorem 3.1 reduces the paper to six statements plus seven bookkeeping predicates, and no
step of the reduction is left implicit. **That is the deliverable: the paper's main theorem is
equivalent to "S0 + A + B + C + X1–X7".** No claim of the paper is used in the assembly beyond
these.

---

## 4. Interface register

Eleven interfaces are crossed by Theorem 3.1. For each: what the assembly needs, what the paper
supplies and where, and the verdict. **Verdicts**: *supplied* (the paper states it, the assembly
only has to cite it); *implicit* (true and provable from what the paper states, but never
assembled in one place); *constraint* (an inequality that a reader must check and that the paper
never states as a condition of composition); *ambiguity* (the paper's wording admits two
readings, one of which breaks the assembly).

| id | interface | what the assembly needs | what the paper supplies (locator) | verdict | action |
|---|---|---|---|---|---|
| **I0** | MUB $\to$ CHM | any 4-tuple of MUBs maps by a common unitary to $(I,H/\sqrt6,B_3,B_4)$ with $H$ complex Hadamard and extendible | §1, p. 3, paragraph after Thm 1.1; Def. 2.1 | implicit (elementary; proved here §5.1) | T8: state as Lemma 0 and prove in 4 lines |
| **I1** | S0 $\to$ A, radius | cover radius $0.032\le$ A's seed radius $r_s$ | Prop. 2.10 last sentence ($0.0320001$); §7.2 `arun` constants ($r_s=.0320001$) | supplied | — |
| **I2** | S0 $\to$ A, coordinates | A's input row is the *same* 9-tuple, permuted so the selected entry is first; the phase positions are $(7,8,9,10,11,13,19,25,31)$ | end of §2.4, p. 11; (3.2), p. 13 | supplied | T8: one sentence linking §2.4 to (3.2) |
| **I3** | A $\to$ B, certificates | every A record carries a *valid* Root certificate | Prop. 4.6 (`S + C`), §4.2; Prop. 5.7's hypothesis | supplied but **S-conditional**: rides on `buildH::patch` | T8: mark Prop. 4.6 as a code claim wherever it is used, not only in §4 |
| **I4** | A $\to$ B, radii | A radii $\le.125$; B admits input radii $\le.126$ | §7.2 (global target $.125$); §5.6 (*"Input radii satisfy $0\le R\le 0.126$"*) | supplied | — |
| **I5** | **B $\to$ C, radii** | Prop. 6.9 needs $r\le.03$; B mid emits $\tau=.07$; **only B fine's $\tau=.016$ qualifies** | §6.1 (*"radius $0\le r\le .03$"*); §5.6 $\tau$ list; §7.2 | **constraint** | T8: state the inequality $\tau_{\mathrm{fine}}\le.03$ where the two sections meet; never compose C with B mid |
| **I6** | batching | each fine record $\to$ one batch record at the *same* centre with radius raised to $\tau$; raising a radius keeps the Root valid | §5.6 (5.27), p. 39; Def. 4.1 (*"These assertions have no radius restriction"*, p. 22) | implicit (needs the "no radius restriction" remark, which is 17 pages earlier) | T8: cite Def. 4.1's last sentence at (5.27) |
| **I7** | equivalence class in (5.1) | $[\,\cdot\,]$ must be the class under the *whole* group of I0/I8, and $\mathrm{Rep}$ must be idempotent for Corollary S.3(a) | (5.1) says *"the equivalence classes used in the preceding sections, including the permitted signed permutation and transpose operations"* — "including", not "generated by" | **ambiguity** | T8: define the class once in §2 and stop re-listing generators |
| **I8** | extendibility transport | exclude a matrix $\Rightarrow$ exclude everything $\sim$-equivalent to it (the step from C's ball statement to the class statement) | Lemma 2.2 (conjugation, rephasing), Lemma 4.7 (signed perm, transpose, global sign) — never stated jointly | implicit | T8: one joint lemma (spine.md Lemma S.2) |
| **I9** | "required" | A of §2.3 for *every* exact $H$ in the seed ball | Prop. 4.16's *proof* gives the stronger statement; its *statement* says "required for the four-basis problem" | statement weaker than proof | T8: delete the phrase |
| **I10** | diagnostics vs failure | use terminal `failedBalls`/unresolved counts, not `ownfail` | §7.2 last paragraph, p. 51; §7.5 (*"A0 reported such a diagnostic …"*) | supplied | T8: keep, it prevents a misreading |
| **I11** | units at the seed ball | $\|q(P')-u\|_{\text{cycles}}\le.0320001$ becomes $\|s\|_{\text{rad}}\le R_s=2\pi r_s$ | §3.1, p. 13 (*"The enlarged seed radius in cycles is denoted by $r_s$, and $R_s=2\pi r_s$"*) | supplied | T8: see §6 below |

### 4.1 The two interfaces that need a decision, not a citation

**(I5) Radius composability.** This is the only place where a stage *statement* has a side
condition that the preceding stage does not obviously meet. Prop. 6.9's hypothesis $r\le.03$
sits at the top of §6.1 as a range declaration, in the same breath as $0\le k\le10$, and reads
like a typing convention. It is not: it excludes composing C with B mid ($\tau=.07$) and with A
($\le.125$). The paper's chain of §7.4 does compose in the legal order, and §7.2 supplies
$\tau_{\mathrm{fine}}=.016$, so nothing is missing — but a reader who tries to run C on the coarse
atlas produces a false claim. **Recommended wording for T8:** "Stage C applies to Records of
radius at most $0.03$; the second refinement pass emits at $0.016$, which is why the pipeline
refines twice before excluding."

Note also that $r\le.03$ is used *only* through the Appendix A margins and the range checks; the
proof of Prop. 6.9 itself would go through for any $r$ for which (6.1)–(6.3) hold. So the
constraint is arithmetic, not geometric. If T5/T2 ever re-certify the arithmetic at larger radii,
this interface widens.

**(I7) The bracket.** (5.1) defines the solution set and then says *"Here brackets denote the
equivalence classes used in the preceding sections, including the permitted signed permutation and
transpose operations."* Two readings:

* *Reading L (listed):* the class is generated by signed permutations and transpose only. Then
  Lemmas 2.2's rephasings and conjugation are *not* in the class, and Step 1 of Theorem 3.1 fails,
  because S0 produces $P'\sim P$ by an arbitrary element of Lemma 2.2's group, including
  conjugation.
* *Reading G (generated):* the class is generated by everything the preceding sections allow.
  Then everything composes.

Reading G is the intended one — §5.6 and Def. 4.14 speak of "the extendibility-preserving
equivalences of Lemma 4.7", and Lemma 4.7 itself adds rephasing and integer shifts to the residual
invariance. The assembly needs G. **Recommended wording:** replace "including" by "generated by
all the operations of Lemma 2.2 and Lemma 4.7" — literally one line, in §2, where the operations
are first listed.

### 4.2 What the register buys

Every remaining hypothesis of Theorem 3.1 is now either a numbered paper statement (six of them)
or one of X1–X7. There is no seventh mathematical idea hiding in the assembly. In particular the
`M`/`M?`/`S`/`C` status of the paper's chain is *inherited unchanged* by Theorem 3.1: the
assembly adds no new S-claim and no new `C`-hypothesis. That is the sense in which
"Theorem 1.1 = S0 + A + B + C + X" is an equality and not a slogan.

---

## 5. The reduction glue, proved out

These are the steps the paper states in one sentence or cites. Each is proved here in full, so
that the paper can point at them instead of asking a reader to trust them.

### 5.1 G1 — four MUBs give an extendible complex Hadamard matrix (I0)

**Lemma S.4.** Let $B_0,\dots,B_{m-1}$ ($m\ge2$) be pairwise mutually unbiased orthonormal bases
of $\mathbb C^d$. Then there are a unitary $U$ and a complex Hadamard $H$ with $UB_0$ the
coordinate basis and $UB_1$ the column basis of $H/\sqrt d$. If $m=4$ then $H$ is extendible.

*Proof.* Let $F_0\in U(d)$ have the vectors of $B_0$ as columns, and put $U=F_0^*$. Then
$UF_0=I$: the image of $B_0$ is the coordinate basis. Let $W=UF_1=F_0^*F_1$. Orthonormality of
each basis gives $W^*W=F_0^*F_1^*F_1F_0=I$. Unbiasedness gives, for all $i,j$,
$$|W_{ij}|^2=|\langle (B_0)_i,(B_1)_j\rangle|^2=\tfrac1d .$$
Set $H=\sqrt d\,W$. Then $|H_{ij}|=1$ and $H^*H=dI$. Since $H$ is square and invertible,
$H^*H=dI$ gives $HH^*=dI$; so $H$ is complex Hadamard and $H/\sqrt d=W$ is the second basis.
For $m=4$, carry $B_2,B_3$ along: $(I,W,UF_2,UF_3)$ are four pairwise mutually unbiased
orthonormal bases with the first two as required, which is exactly extendibility.
$\square$

Two remarks. (i) The argument uses only that unbiasedness is a statement about moduli of inner
products, so it is stable under everything in $\mathcal G$. (ii) It shows that the passage
"$d+1$ MUBs" $\leftrightarrow$ "a Hadamard extendible by $d-1$ further bases" is a bijection on
equivalence classes — which is the reason the whole proof can be run in the language of a single
matrix $H$.

### 5.2 G2 — dephasing (used by S0 and by Stage A)

**Lemma S.5.** Let $H$ be a complex Hadamard $6\times6$ matrix. Then $H=e(P)$ for a real phase
matrix $P$, and there is $P'\sim e(P)$ with $P'_{0j}=P'_{i0}=0$ for all $i,j$ and $P'$ still
exact.

*Proof.* $|H_{ij}|=1$ gives $H_{ij}=e(\tilde P_{ij})$ for a real $\tilde P$. Put
$P'_{ij}=\tilde P_{ij}-\tilde P_{i0}-\tilde P_{0j}+\tilde P_{00}$. This equals $D_0(\tilde P)$ of
(2.2), and $e(P')=e(\tilde P)$ rephased by the row phases $e(-\tilde P_{i0})$ and the column
phases $e(-\tilde P_{0j}+\tilde P_{00})$, both allowed in $\mathcal G$. Keeping the (0,0) entry,
this is $P'_{0j}=P'_{i0}=0$. Exactness is Lemma S.2. $\square$

*Note:* the same computation with $P$ replaced by a *centre* $Q$ that is not exact is (4.17),
$d=\Pi(D_0(P)-D_0(Q)-N)\Rightarrow e(Q+d)\sim e(P)$; the proof is one line: $\Pi D_0=\Pi$, and
$X-\Pi X$ is constant on rows plus constant on columns.

### 5.3 G3 — extendibility and exactness are invariant (Lemma S.2)

The paper's Lemma 2.2 asserts the conclusion. Its proof contains one sentence that is true in
substance but not as written: *"A row permutation or row rephasing is a common unitary operation
on all four bases; it preserves the standard basis up to the same irrelevant changes."* Applying a
diagonal unitary to the coordinate basis does not leave the coordinate basis; a reader who tries
to run that sentence literally gets stuck. The repair is short and worth having in the paper:

**Lemma S.6 (monomial transport).** Let $V\in U(6)$ be *monomial*: every row and every column has
exactly one nonzero entry, of modulus $1$. If $(I,M,B_3,B_4)$ are four pairwise mutually unbiased
orthonormal bases then so are $(I,VM,VB_3,VB_4)$.

*Proof.* $VM,VB_3,VB_4$ are orthonormal ($V$ unitary) and pairwise unbiased (a common unitary
preserves $|\langle\cdot,\cdot\rangle|$). $I$ is unbiased to $VM$ because
$|(VM)_{ij}|=|M_{ij}|$ for monomial $V$; likewise to $VB_3$ and $VB_4$. Its own orthonormality is
unchanged. $\square$

With Lemma S.6 in hand each generator of $\mathcal G$ is immediate:

| generator | argument |
|---|---|
| column permutation, column rephasing | relabels / rephases the vectors of $B_1$: the *basis* is unchanged |
| row permutation, row rephasing | Lemma S.6 with $V$ a permutation / diagonal unitary |
| global sign | Lemma S.6 with $V=-I$; or a global phase on each vector |
| entrywise integer shifts | $e(P+N)=e(P)$: the matrix does not change at all |
| complex conjugation | inner products satisfy $\langle\bar u,\bar v\rangle=\overline{\langle u,v\rangle}$, so moduli and orthogonality are preserved |
| transposition | see below |

*Transposition, written out.* Let $U=M=H/\sqrt6$ and suppose $(I,U,B_3,B_4)$ are MUB. Apply the
common unitary $U^*$: the four bases become $(U^*,I,U^*B_3,U^*B_4)$. Interchange the first two
(the order of a family is irrelevant): $(I,U^*,U^*B_3,U^*B_4)$. Conjugate every coordinate:
$(I,\overline{U^*},\overline{U^*}B_3,\overline{U^*}B_4)$ — still four MUB, since conjugation
preserves moduli of inner products. Now $\overline{U^*}=U^T$: indeed $U^*=\overline U^{\,T}$, so
$\overline{U^*}=U^T$. Hence $(I,U^T,\dots)$ are four MUB and $U^T=H^T/\sqrt6$ is extendible.
Every step is an equivalence, so the implication runs both ways. $\square$

*Consequence.* $\mathrm{Ext}$ is $\mathcal G$-invariant, which is Lemma S.2, which is what turns
C's ball statement into a class statement (I8).

### 5.4 G4 — three MUBs exist (Lemma 1.2 of the paper), re-derived

The paper's construction is $U_r=A_r\otimes B_r$ in $\mathbb C^2\otimes\mathbb C^3$ with

$$A_0=I_2,\quad A_1=\tfrac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},\quad
A_2=\tfrac1{\sqrt2}\begin{pmatrix}1&1\\i&-i\end{pmatrix},$$
$$B_0=I_3,\quad B_1=F=\tfrac1{\sqrt3}(\omega^{jk})_{j,k=0}^{2},\quad
B_2=DF,\quad \omega=e^{2\pi i/3},\ D=\operatorname{diag}(1,\omega,\omega).$$

*Unitarity.* Each $A_r$ is unitary; $F$ is unitary because the rows of $(1,\omega^{jk})$ are
orthogonal (geometric sums, $1+\omega+\omega^2=0$); $D$ is unitary.

*Cross products, the $2\times2$ factor.* $A_1^*A_2=\frac12\begin{pmatrix}1+i&1-i\\1-i&1+i\end
{pmatrix}$, all entries of modulus $\frac{\sqrt2}{2}=\frac1{\sqrt2}$, so squared modulus $\frac12$.

*Cross products, the $3\times3$ factor.* With $D_{xx}=\omega^{x^2}$ (that is, $d_0=0,d_1=d_2=1$),
$$(F^*DF)_{jk}=\tfrac13\sum_{x=0}^{2}\omega^{-xj}\omega^{x^2}\omega^{xk}
=\tfrac13\sum_{x=0}^{2}\omega^{x^2+(k-j)x}.$$
For $t=k-j \bmod 3$: $t=0$ gives $\frac13(1+2\omega)$, and $t=1,2$ give $\frac13(2+\omega^2)$.
$|1+2\omega|^2=1+4+4\operatorname{Re}\omega=5-2=3$ and $|2+\omega^2|^2=4+1+4\operatorname{Re}
\omega^2=5-2=3$. Hence $|(F^*DF)_{jk}|^2=\frac13$ for $j\ne k$, and $|(DF)_{jk}|^2=\frac13$ by
inspection, so $B_1,B_2$ are unbiased. $B_0$ against $B_1,B_2$ is the same modulus statement.

*Tensor.* $\langle a\otimes b,a'\otimes b'\rangle=\langle a,a'\rangle\langle b,b'\rangle$ for the
paper's convention, so $A_r^*A_s\otimes B_r^*B_s$ has every entry of squared modulus
$\frac12\cdot\frac13=\frac16$ for $r\ne s$. Hence $U_0,U_1,U_2$ are three pairwise mutually
unbiased orthonormal bases, and $U_0=I_6$. $\square$

The only step with content is the Gauss-sum evaluation, and it is the $2+1$ case of the standard
quadratic Gauss sum; the paper's display is correct as printed.

### 5.5 G5 — the two halves of $N(6)=3$

Let $N(6)$ be the largest cardinality of a pairwise mutually unbiased family of orthonormal bases
of $\mathbb C^6$. "No four exist" gives $N(6)\le3$: if $N(6)\ge4$ the first four members would be
four. Lemma 1.2 of the paper gives $N(6)\ge3$. Hence $N(6)=3$. Theorem 1.1's *"Consequently
$N(6)=3$"* is exactly this two-line step, and it is the only place the lower bound is used.

### 5.6 G6 — the Lie-algebra corollary (Corollary 1.3): what is checked and what is cited

For a unit vector $b\in\mathbb C^6$ let $X_b=bb^*-I/6$, traceless and Hermitian. For unit $b,c$,
$$\operatorname{tr}\big((bb^*-\tfrac16I)(cc^*-\tfrac16I)\big)
=\operatorname{tr}(bb^*cc^*)-\tfrac16-\tfrac16+\tfrac16
=|b^*c|^2-\tfrac16 .$$
So $b,c$ are unbiased iff $\operatorname{tr}(X_bX_c)=0$. Since $\{X_b\}_b$ spans the Cartan
subalgebra of the traceless diagonal-in-$B$ matrices, and $K(X,Y)=12\operatorname{tr}(XY)$, the
identity $\operatorname{tr}(X_bX_c)=|b^*c|^2-\frac16$ says:

> two orthonormal bases are mutually unbiased $\iff$ their Cartan subalgebras are
> Killing-orthogonal.

Each $X_b$ is Hermitian, so each such Cartan is closed under the standard adjoint. The *converse*
— that every collection of pairwise Killing-orthogonal Cartan subalgebras closed under the same
standard adjoint arises from a collection of MUBs of the same cardinality — is the content of
[3, Theorem 5.2] (Boykin–Sitharam–Tiep–Wocjan). **That citation is the only load-bearing step in
the paper whose evidence lies outside the packet.** It is also not checked here; see
`reports/m1-report.md`.

Given the citation, Corollary 1.3 is Theorem 1.1 transported along a bijection that preserves
cardinality, plus Lemma 1.2 for attainment. Nothing else is used.

---

## 6. Units at the hand-offs

The assembly crosses three unit conventions. The paper states each of them, but never in one
place, and every one of them is a factor $2\pi$ that a transcription can lose.

| section | displacements and radii | unit |
|---|---|---|
| §2 seed cover | $q\in\mathbb R^9$, centres $u$, radius $0.032$ / $0.0320001$ | **cycles** |
| §3 seed displacement | $s=2\pi(q-u)\in\mathbb R^9$, radius $R_s=2\pi r_s$ | **radians** |
| §3 U(2) cells | $\theta\in\mathbb R^4$, $|\theta_j|\le h=\pi/N_u$ | **radians** |
| §3–4 blocks | $E',B',C',D',Z,z,p,E_r$ (unit-entry matrices and chord norms) | pure numbers |
| §4.4–4.6 | $\delta=\Delta+\Pi(\epsilon+u/2\pi)$: $\delta,\Delta,\epsilon$ cycles, $u$ radians | **mixed by design** |
| §4–5 Records | $R,r,\tau,w$, $\eta=T^*\delta$, $\nu$, $n_P(s)$, $t$ | **cycles** |
| §6 bins and balls | $x$, $X_M=\sqrt{29/6}\,a$, $a=1/(2M)$, $r$, $\delta$ | **cycles** |
| §6 chord comparisons | $2\pi(KX+r)$, $2\pi(L/\sqrt6+r)$ | cycles $\times2\pi$ |

The three bridges, and only these:
$$s=2\pi(q-u),\qquad R_s=2\pi r_s \quad(\S3.1),\qquad
\delta=\Delta+\Pi\!\left(\epsilon+\frac{u}{2\pi}\right)\quad(4.26),\qquad
\text{chord}\;\le 2\pi(\text{cycle displacement}).$$

**Safest reading for T8:** every radius and displacement in the proof is in *cycles*; the only
radian quantities are the seed displacement $s\in\mathbb R^9$, the four $U(2)$ angles
$\theta_1,\dots,\theta_4$, and the arc matrix $u$ of Lemma 4.9. Each of those three appears
targeted by an explicit $2\pi$. If the paper's notation table declares that, the rest is automatic.

---

## 7. Twelve words, one meaning each

The paper uses more words than objects. For the assembly the inventory is complete and small; this
table is the assembly's usage, not a replacement for `notation.tex` (which owns the seven Root
constants and the three naming systems).

| word | object | lives in | first use |
|---|---|---|---|
| **bin** | a closed interval of one phase, $[b/N,(b+1)/N]$ | $[0,1]$ (seed), $[0,1)^5$ (vector) | (2.6), §6.2 |
| **cell** | a product of bins, one per coordinate; also used for a product of $U(2)$ bins | $\mathbb R^4$ (§3), $\mathbb R^5$ (§6) | §3.3 |
| **box** | a product of intervals in *tangent* coordinates | $\mathbb R^k$, $k\le10$ | §5.3 (5.21) |
| **seed ball** | a closed Euclidean ball in the nine seed phases | $\mathbb R^9$, radius $.0320001$ | §2.4, Prop. 2.10 |
| **phase ball** / **sphere** | the solution set $\mathrm{Sol}(P,R)\subset$ unit-entry matrices | $\mathbb R^{36}$ modulo $2\pi\mathbb Z$ | Def. 4.14; "sphere" is the source's word for it |
| **Record** | a certified Root *plus* a radius; the unit of transport between stages | — | Def. 4.14 |
| **Root** | centre $P$, tangent columns $T$, seven constants; certificates (4.4)–(4.7) | — | Def. 4.1 |
| **vector ball** | $B_{\mathrm{vec}}(v,s)$, a ball in the five free phases of one vector | $\mathbb R^6/2\pi\mathbb Z^6$ | (6.14) |
| **atlas** | the finite family of Records a stage has produced so far | — | §4.7, §5.4 |
| **parent** / **child** / **blocker** | an input Record of Stage B / an output Record / an *already completed* input Record used for reuse | — | §5.5 |
| **record file** | serialized finite family $\{(P,T,\text{constants},r)\}$ | `.bin` | §7.1 |
| **shard** / **batch** | a modulo-4 part of a record file / a group of $\le256$ atlas records | — | §7.2 |

Three of these are overloaded and the assembly depends on keeping them apart:
*sphere* is the source's alias of a Record's phase ball and is **not** a vector ball;
*cell* means a $U(2)$ cell in §3 and a phase bin product in §6;
*box* is never a phase region — it is tangent coordinates only.

---

## 8. What this file does not do

* It does not check the analysis inside S0, A, B or C. Each is quoted at its statement and used
  only at its statement.
* It does not check Proposition 4.6 (`buildH::patch` produces certified Roots). That is an
  `S + C` claim and it is **load-bearing for I3**: without it, the Records that B refines have no
  solution sets to cover. The assembly inherits the paper's status here, unchanged.
* It does not re-derive the 30-constant arithmetic of Appendix A.
* It does not verify [3, Theorem 5.2] (Corollary 1.3's citation).
* It does not decide whether the October 2026 run happened. It says exactly what the run must
  have been for Theorem 3.1 to apply, which is X1–X7.

**What T4 can take from here.** §1 and Theorem 3.1 are already in the shape of a Lean development
over an abstract region interface: three primitive notions (`mem` = class membership, `Exact`,
`Ext`) and one theorem. `lean/Interface.lean` in this directory does more than sketch it: it
compiles with `lean Interface.lean`, imports nothing, and proves

| declaration | what it is | status |
|---|---|---|
| `Mub6Assembly.assembly` | Theorem 3.1, all batch records C-negative | proved, no `sorry` |
| `Mub6Assembly.assembly_fallback` | Theorem 3.1 with the two-branch exit of §3.2 Step 5 | proved, no `sorry` |
| `Refines`, `refines_trans` | the relation `⊒` of §1.6 and its transitivity | proved, no `sorry` |
| `Excludes`, `excludes_of_refines` | what Stage C exports, and its monotonicity | proved, no `sorry` |

`sh lean/check.sh` prints `'...' does not depend on any axioms` for all four. So the assembly is
machine-checked *relative to* the six stage statements, which enter as the hypotheses `h0`, `hA`,
`hBm`, `hBf`, `hBat`, `hC`. Two things to know before transcribing:

* `mem R H` is deliberately **class membership** ("the $\sim$-class of $H$ meets $R$"), not set
  membership. That single choice absorbs the "up to equivalence" clause of every stage at once,
  and it is why no equivalence bookkeeping appears in the proofs.
* five of the six hypotheses are the paper's stage statements verbatim; only `hC` consumes a
  lemma of this file (Lemma S.2), because Proposition 6.9 speaks about the ball while the
  assembly needs the class. That is the one place T4 needs an extra lemma, and it is proved here.

The remaining work for T4 is the instantiation of the six hypotheses, not the assembly.

**What T8 can take from here.** Answers, in order of value: the three-line chain of §3.3; the
joint equivalence lemma of §5.3 (it replaces a sentence that does not survive a literal reading);
the radius ordering of I5; the units table of §6.
