# What the primary source may and may not cite — an exact-hypothesis dossier

*member m2, swarm `smwhnslql`, direction "external-input audit (literature side)".
Written 2026-11-15. Every item below was checked against the publisher's own page
(arXiv abstract / HTML full text / GitHub) on that date; nothing here is quoted from memory.*

Labels used throughout: **[P]** proved in the cited source · **[V]** verified by me in this
run (script `m2-explicit-triples.py`) · **[C]** conditional on a stated external theorem ·
**[N]** numerical only · **[U]** unresolved.

---

## 1. Verdict in one paragraph

$N(6)=3$ **is proved**, twice, in 2026 (§2). The primary source's central research target —
"prove that every MUB triple in $\mathbb C^6$ has a nontrivial diagonal symmetry" — is not an
open problem: it is *step (H2) of the published proof* (§2.1, §2.3), established there by
interval-certified local computation, not by an algebraic identity. Consequently the source's
unresolved identity $\Xi(P_{\mathcal A})\Xi(P_{\mathcal B})\Xi(P_{\mathcal C})=0$ is **true
given the published classification** (§4, [C]), and the only open content of the proposed route
is to *re-derive* that classification's key step without a computer. The technical slot the
source's identity is meant to fill is already occupied by a published conjecture of Matolcsi,
Matszangosz, Varga and Weiner (§3.3), stated in the same "sum of nonnegative detectors"
form — arXiv **v2**, which pairs each transition with its adjoint and adds a companion
Conjecture 3 on the Szöllősi family that v1 wrongly imported as a theorem. A proof revision that presents $N(6)=3$ as open, or the forcing of diagonal symmetry as
the missing lemma, would be wrong.

---

## 2. Status of the theorem

### 2.1 Wuttig–Tindall, arXiv:2611.06917 (v1, 4 Nov 2026) [P]

*Using topology to reveal all mutually unbiased bases in dimension six*, Mateo Cárdenes Wuttig,
Joseph Tindall (quant-ph/math-ph/math.CO). Companion: arXiv:**2608.18053** (18 Aug 2026),
*A Complete Classification of Complex Hadamard Matrices of Order Six* [P].

Structure of the proof, as stated in the paper:

| step | content | status there |
|---|---|---|
| Thm 1 | every order-6 complex Hadamard matrix except Tao's is reconstructed from a dephased $3\times3$ corner with **four** free phases | human proof (SM §.6) |
| Thm 2 | $\mathcal X=$ (CHM(6) minus Tao's orbit) is **connected** | human proof, using Thm 1 + 18 maximal seeds |
| Thm 3 | **every MUB triple in $\mathbb C^6$ is equivalent to** a member of one explicit two-parameter family *(Methods Eq. (31))* **or** to one isolated triple *(Methods Eq. (30))* | **computer-assisted**: 2,775 four-dimensional phase balls + a chart at $F_6$, interval arithmetic, 3.3 GB certificates |
| Thm 3 ⇒ $N(6)=3$ | neither type extends to a fourth basis | reduces to Jaming et al. 2009 (§3.1) |
| second proof | quartet exclusion directly from the same cover | computer-assisted |

Two features matter for us and are stated explicitly in the paper:

* **The order-three symmetry is the load-bearing step.** In every ball they certify that a
  triple either fails to exist or **has an order-three symmetry** $T$ ($T^3=I_6$) that fixes
  every vector of one basis up to a phase and permutes each of the other two bases in two
  $3$-cycles, i.e. after ordering $T=\operatorname{diag}(1,1,\omega,\omega,\omega^2,\omega^2)$.
  They then solve the symmetric case *exactly* (SM §.8.5): every triple with this symmetry is in
  the two-parameter family or is the isolated triple. **No interval arithmetic is used in the
  symmetric case.**
* **The symmetry is not derived algebraically.** It is obtained from derivative/contraction
  bounds uniform on each certified ball ("SM Eq. (tc-symmetry)"), i.e. by a finite machine
  check. This is precisely the gap the primary source proposes to close.

### 2.2 OpenAI, "OpenAI Math Release preprint", 24 Sep 2026 [P, but see hypothesis]

*The maximum number of mutually unbiased bases in dimension six*
(`github.com/openai/math/blob/main/preprints/...-September-24-2026/...pdf`), cited as [63] in
2611.06917. Own abstract: "We prove that the maximum number of mutually unbiased orthonormal
bases in $\mathbb C^6$ is three … The upper bound is computer-assisted: **under the stated
binary64 arithmetic and compiler conditions**, a complete execution of the documented
verification pipeline excludes four arbitrary complex bases." Companion: *Exact Fourier
certificates for complex Hadamard matrices of order six* (same release, [62]).

Note the hypothesis: binary64 arithmetic + compiler conditions, *not* interval arithmetic. Any
revision citing it must carry that qualifier. 2611.06917 states its own proof is "logically
independent of theirs" and relies on none of their certificates.

### 2.3 Lean 4 formalization (mub6-triples-lean, Zenodo 10.5281/zenodo.23993900) [V]

Jinze Yang (with Claude Opus 5.5), formalizing item 3 of 2611.06917's Theorem `all-mubs`.
Main statement:

```
theorem MUBTriples.mubTriple_classification (C : TripleCertificate piece ordering) :
    TripleClassification
-- ∀ U, IsMUBTriple U → (∃ V, IsFamilyMember V ∧ TripleEquiv U V) ∨ TripleEquiv U isolatedTriple
```

**This is a formalization modulo three hypotheses**, not an unconditional one:

* **(H1) `covered`** — every non-Tao CHM(6) lands in a piece of the cover.
  Computer-assisted (Thm 2 + the 2,775 certified balls).
* **(H2) `classified`** — on every piece, every triple "has an order-three symmetry"
  (`HasOrder3Symmetry`). **Computer-assisted**: the 3.3 GB interval certificates of release
  `tc-verification-2026-11-04`, four balls (IDs 1035, 1217, 1622, 2705) with
  minimum-transition scope.
* **(H3) `taoNoThird`** — Tao's matrix admits no third unbiased basis. **Literature**, kept as a
  hypothesis.

Formalized *without* hypotheses (worth citing as the rigorous core): `symmetricRecognition`
(every triple with the order-three symmetry is equivalent to a family member or the isolated
triple), the abstract contraction principle `Contraction.symmetry_criterion`, the seed
parametrization, and non-equivalence of the two alternatives via a Bargmann invariant
($\sum_{e,f,g}(\langle e|f\rangle\langle f|g\rangle\langle g|e\rangle)^4$, value
$-2592(1+2\omega)/6^8$ for the isolated triple). Axiom audit: only
`propext, Classical.choice, Quot.sound`.

**Attribution of (H3) [V].** The paper's own [13] is S. Brierley, S. Weigert, *Constructing
mutually unbiased bases in dimension six*, Phys. Rev. A **79**, 052316 (2009), which is also what
the Lean README cites for (H3); the NoFourMUBS development re-checks it in
`proof/theorems/TC_triple_classification/tao.py`. So (H3) is consistently attributed — but it is
a *literature input kept as a hypothesis* in the formalization, not something proved there. A
revision citing it should say exactly that.

---

## 3. The external items the source relies on

### 3.1 Jaming–Matolcsi–Móra–Szöllősi–Weiner 2009 [P]

arXiv:**0902.0882**, J. Phys. A **42**, 245305 (2009). Abstract, verbatim in substance: they
exhibit an infinite family of MUB *triplets* in dimension 6 involving the Fourier family
$F(a,b)$, **and prove that for any $(a,b)$ the standard basis and $F(a,b)$ cannot be extended to
a MUB quartet**. This is the nonextension theorem the whole symmetry route terminates in, and
it is unconditional (human proof, 2009).

How both Wuttig–Tindall types reduce to it [P, stated in 2611.06917 §I and §IV]:
each type contains a pair whose transition lies in the Fourier family. For the isolated triple
this is the Good–Thomas identity $F_6\cong F_2\otimes F_3$ up to permutations, plus the fact
that every $2\times2$ and every $3\times3$ Hadamard is equivalent to $F_2$, $F_3$; so its
transition $\big(\hat F_2^\dagger D_2\hat F_2\big)\otimes\big(\hat F_3^\dagger D_3\hat F_3\big)
\sim F_6=F(1,1)$. (I did not machine-check this equivalence; it is a two-line argument and is
asserted with a proof pointer in 2611.06917.)

### 3.2 Sun, arXiv:2610.12180 (v1, 8 Oct 2026) [P, narrower than the source implies]

Hao-Yu Sun, *Mutually unbiased bases: common states, completion, and extension obstructions*.
**Theorem 8.2**: let $I, K_\eta, V$ be pairwise MU bases in dimension six, where $K_\eta$ is a
displayed phase-deformed Fourier family; **if the six original rays of $V$ are setwise
$D$-invariant**, where $D$ is the diagonal ternary clock, then no unit vector is unbiased to all
three (strong unextendibility). Exact reproduction is in Sun's §E.5.

Two corrections for the source's sentence "Sun's work also proves strong nonextension under a
corresponding ternary-clock hypothesis":
1. the hypothesis is on a triple of the *displayed form* $(I,K_\eta,V)$ together with
   clock-invariance of the third basis's rays — not "a triple with a threefold diagonal
   symmetry" in general, and not the source's $\Delta$-criterion;
2. Sun states explicitly: "These results do not determine the global maximum number of mutually
   unbiased bases or classify all triples." Sun's theorem is therefore an *alternative*
   nonextension route for a subclass, not a substitute for 2611.06917.

### 3.3 Matolcsi–Matszangosz–Varga–Weiner — **cite v2, and mind Conjecture 3**

arXiv:**2503.14752**, two versions that differ materially; published in J. Algebraic Combin.
**63** (2026) 26 (which of the two versions the journal text reproduces — I did not check, so all
citations below name the arXiv version). *Triplets of Mutually Unbiased Bases.*

The paper introduces the $d\times d\times d$ **Hadamard cube** of a triplet and states:

* **Conjecture 1** — every MUB triplet in $d=6$ is equivalent to one built from two
  Fourier-family members. **This is now a theorem**: it is [WT26a] Theorem 3, and 2611.06917 says
  so explicitly ("This proves Conjecture 1 of Ref. [47]").
* **Conjecture 2** — the detector identity, in the two versions:
  * **v1** (18 Mar 2025): $G_{H_j}(\pi\gamma_1)=0$ for all $j,\pi$, and
    $G_{H_j}(\pi\gamma_2)=0$ **for two of the three $j$**; single identity Eq. (4.7), a sum of
    pairwise products $\tilde G_{H_j}(\gamma_2)\tilde G_{H_k}(\gamma_2)$;
  * **v2** (19 Jul 2025, *current*): $G_{H_j}(\pi\gamma_1)=0$ and
    $G_{H_j}(\pi\gamma_2)\,G_{H_j^*}(\pi\gamma_2)=0$ **for every $j$ and every $\pi$**;
    single identity Eq. (4.9), pairing each transition with its **adjoint**.
  with $G_H(\gamma)=|\sum_k\prod_iH_{ik}^{\gamma_i}|^2$, $\tilde G_H=\sum_{\pi\in S_6}G_H(\pi\cdot)$,
  $\gamma_1=(1,1,1,-1,-1,-1)$, $\gamma_2=3\gamma_1$.
* **Conjecture 3** (new in v2) — no $S\in X(\alpha)$ of the Szöllősi family is part of a
  quadruplet. In v1 this was imported as a *theorem* from [11] (Chen–Liang–Hu–Chen, QIP **20**
  (2021) 353, resting on a lemma of Chen et al., J. Phys. A **50** (2017) 475304); McNulty–Weigert,
  arXiv:**2504.13067** (17 Apr 2025), showed that "the proof of the lemma … contains a mistake,
  ultimately invalidating three theorems derived in later publications". Hence v2's own remark:
  "[it] was referred to as a proven fact from the literature, but unfortunately the proof in [11]
  turned out to be wrong, as pointed out by [25]."
* **Prop. 4.2 (v2)** — *Conjectures 2 **and** 3* imply $N(6)=3$. (v1's Prop. 4.2 needed
  Conjecture 2 alone because it imported the Szöllősi exclusion.)

So: v2 leaves the Szöllősi-family exclusion **as a conjecture**, because the old proof route was
invalidated, and an MMVW-based nonextension chain must say which of Conj. 2 / Conj. 3 it uses. A
separate complete MUB classification may imply the exclusion independently; whether [WT26a]'s
classification is intended to supersede Conjecture 3 explicitly is a separate question.

This is also the same *device* the primary source proposes — a sum of nonnegative detectors
attached to the three transitions, asserted to vanish as an algebraic consequence of the MUB
equations. The source's $\Xi(P_{\mathcal A})$ is a different detector (support-lattice based,
anchored at bases rather than at transitions), but the role, the shape (sum of nonnegatives $=0$)
and the claimed consequence coincide.

**Detector data, both versions, and two proved mechanisms:**
[`m2-v2-detector.md`](m2-v2-detector.md). Summary: at every sampled representative (isolated
triple, family centre, three generic interior points, plus 25 random interior points) **both**
versions hold — $\max_{j,\pi}G_{H_j}(\pi\gamma_1)\le1.6\cdot10^{-28}$ and
$\max_{j,\pi}G_{H_j}(\pi\gamma_2)G_{H_j^*}(\pi\gamma_2)\le3.7\cdot10^{-28}$ — and both are
*sharp*: v1's $\gamma_2$ clause fails at exactly one of the three transitions generically, and v2's
product genuinely needs its second factor. Scope: these are statements about the **sampled
representatives**; the full-family assertion is not established (it would follow from [WT26a]
Thm 3 plus a symbolic check on Methods Eq. (31), not done). A *proof* is given for one clause:
for a transition in the normal form of [WT26a] Eq. (33), the adjoint $\gamma_2$ detector vanishes
identically for every $\pi$ and every $3{+}3$ split (parity of the number of $+$ signs in the
$b=1$ half of the columns), and the $\gamma_1$ detector vanishes for the 12 of 20 splits with
$\sum t\gamma_t\not\equiv0\pmod3$ (index mechanism). Both mechanisms are stated and proved in
that note.

The identity is not a formality of the block shape: replacing the diagonals $D,R,S$ of Methods
Eq. (31) by arbitrary unit diagonals keeps the block form but destroys unbiasedness (defect
$\approx0.3$) and the detectors blow up to $\sim10^2$–$10^4$. So it genuinely encodes the MUB
equations.

### 3.4 "Arithmetic matroids", arXiv:1105.3220 [V: exists, unused]

*Arithmetic matroids, Tutte polynomial, and toric arrangements.* Real, but the source uses no
theorem from it; the lattice-index machinery it wants is standard Smith-normal-form theory.
Citing it lends no support to the $\Xi$ proposal.

### 3.5 Strong unextendibility of every triple — the stronger nonextension input [P]

2611.06917 §IV.1 and SM §.10: **every** MUB triple in $\mathbb C^6$ is *strongly unextendible* —
no unit vector at all is unbiased to all three bases (in the constellation notation of the 2026
McNulty–Weigert review, Quantum **10**, 2051: $\{5,5,5,1\}_6$ is empty; this settles Problem 10.3
there). The two inputs named are:

* **continuous normal form** — H. Sun, arXiv:2610.12180, **Corollary 9.1** ("Fourier-localized
  companion"): if $I,S,C_\nu$ are pairwise MU bases of the displayed frequency-localized form,
  no unit vector is unbiased to all three;
* **isolated (product) triple** — D. McNulty, S. Weigert, *On the impossibility to extend triples
  of mutually unbiased product bases in dimension six*, Int. J. Quantum Inf. **10**, 1250056
  (2012).

Why this matters for the bridge, and a remark I did not find stated in 2611.06917:

> **Lemma [V].** If every MUB triple in $\mathbb C^6$ is strongly unextendible, then $N(6)=3$.

*Proof.* A quartet contains a triple $(A,B,C)$. Every unit vector of the fourth basis has
squared overlap $1/6$ with each of the $18$ vectors of $A,B,C$, so it is a unit vector unbiased to
all three of them — contradicting strong unextendibility. $\square$

So, given the classification of triples, the nonextension step can be discharged by
strong unextendibility instead of by the Jaming et al. quartet exclusion. 2611.06917 itself uses
the Jaming et al. route (and a direct quartet exclusion from the cover); the two are
independent, which is worth knowing if one of them is ever doubted. (I did not verify the
matching of the normal form to Sun's $C_\nu$ setup; that matching is asserted in [WT26a] SM §.10.)

### 3.6 Three elementary facts the source (and several members) use, with proofs [V]

1. **Three unit complex numbers summing to zero are a rotation of $(1,\omega,\omega^2)$.**
   If $u+v+w=0$ with $|u|=|v|=|w|=1$ then $u,v,w$ are the vertices of an equilateral triangle,
   i.e. $\{u,v,w\}=z\{1,\omega,\omega^2\}$. (Used by the source's §4 and by the whole
   order-two argument.) Proof: $|u+v|=|w|=1=|u|=|v|$ forces $\operatorname{Re}(u\bar v)=-\tfrac12$,
   i.e. $v/u\in\{\omega,\omega^2\}$, and then $w/u$ is the third root.
2. **Every $3\times3$ complex Hadamard matrix is equivalent to $F_3$** up to row/column phases
   and permutations. Proof: dephase (first row and column $=1$), write
   $H=\begin{pmatrix}1&1&1\\1&a&b\\1&c&d\end{pmatrix}$; row orthogonality gives $b=-1-a$, so
   $|a|=|b|=1$ forces $a\in\{\omega,\omega^2\}$ and $b$ the other root; the same for $c,d$; the
   remaining $(2,3)$ orthogonality then leaves exactly **two** dephased solutions, $F_3$ and
   $F_3$ with its last two rows exchanged — verified by exhaustive enumeration. Note it is a
   *finite* classification: no continuous family in order three, which is exactly what the
   order-two-to-order-three argument needs.
3. **Good–Thomas**: $F_6$ is permutation-equivalent to $F_2\otimes F_3$ (CRT
   $\mathbb Z/6\cong\mathbb Z/2\times\mathbb Z/3$, so $\omega_6^{jk}$ factorises). This is what
   makes the isolated triple's transitions Fourier-family matrices (§3.1).

---

## 4. What the source says about the literature, checked line by line

| source claim | verdict |
|---|---|
| "This symmetry is already central to the November 2026 classification preprint of Cárdenes Wuttig and Tindall. Their global argument forces it through interval-certified local computations." | **Correct** [V]. It is step (H2); see §2.1, §2.3. |
| "Sun's work also proves strong nonextension under a corresponding ternary-clock hypothesis." | **Half correct**; the hypothesis is narrower and Sun disclaims the global theorem (§3.2). |
| "The existing computational classification implies a negative answer" to *can all three $\Delta$ be trivial?* | **Correct, and now provable in one line** — see below. |
| "Hadamard cubes and polynomial identities for MUB triples are already an established approach in the work of Matolcsi, Matszangosz, Varga and Weiner." | **Correct**, and stronger than the source says: their Conj. 2 is the same device, in the adjoint-paired v2 form (§3.3). |
| "I did not find this particular MUB support-lattice detector in the targeted literature search, but that is not sufficient to establish publication-level novelty." | **Correctly cautious.** The detector is plausibly new as a construction; the *method* is not. |

**The one-line proof the source only asserts.** Let $(A,B,C)$ be a MUB triple in $\mathbb C^6$
and let $T$ be the order-three symmetry of [WT26a] (certified for every triple, (H2)). $T$
fixes the rays of one basis — call it $A$ — so in the $A$-frame $T$ is diagonal; and $T$
permutes the rays of $B$ and of $C$. Hence the class of $T$ mod overall phase is an element of
order $3$ of the source's own group $G_A$, so $3\mid\Delta_A$. ∎

So **[C] (on [WT26a] (H2)): every MUB triple in $\mathbb C^6$ has an anchor $X$ with
$3\mid\Delta_X$; consequently $(\Delta_A,\Delta_B,\Delta_C)=(1,1,1)$ is impossible, and the
source's "reduced obstruction" is empty.** This is what the source means when it writes "the
existing computational classification implies a negative answer"; the argument is one line and
should replace the assertion.

**Corollary [C].** Granting [WT26a] Theorem 3 and the source's own detector equivalence
(12) — "$\Xi(P_{\mathcal A})=0$ iff a nonconstant order-three diagonal clock exists at
$\mathcal A$" — the product identity (13) $\Xi(P_A)\Xi(P_B)\Xi(P_C)=0$ is **true for every MUB
triple in $\mathbb C^6$**. It is therefore not a conjecture about MUBs but a consequence of the
classification. A direct proof of (13) remains open and is the only content of the route.

---

## 5. Consequences for the proof revision

Cite, in this order, with these exact hypotheses:

1. **Brierley–Weigert**, Phys. Rev. A **79**, 052316 (2009): Tao's isolated CHM(6) admits no
   third unbiased basis. *(Attribution note in §2.3.)*
2. **Wuttig–Tindall**, arXiv:2608.18053: complete classification of CHM(6) (four-phase
   reconstruction).
3. **Wuttig–Tindall**, arXiv:2611.06917: Theorem 3 = classification of all MUB triples
   (computer-assisted: 2,775 phase balls, interval arithmetic); Methods Eqs. (30)–(31) for the
   two explicit types; SM §.8.5 for the exact solution of the symmetric case.
4. **mub6-triples-lean** (Zenodo 23993900): the same classification in Lean 4 **modulo (H1)–(H3)**;
   cite it for `symmetricRecognition` and the formal skeleton, not as an unconditional proof.
5. **Jaming–Matolcsi–Móra–Szöllősi–Weiner**, arXiv:0902.0882 / J. Phys. A **42**, 245305 (2009):
   no quartet contains a pair $\{I,F(a,b)\}$. Unconditional, human proof.
6. **Matolcsi–Matszangosz–Varga–Weiner**, arXiv:2503.14752 — **cite v2 (19 Jul 2025)**, not v1:
   Hadamard cubes; Conjecture 1 (now a theorem, = [WT26a] Thm 3); Conjecture 2 v2 = the "nonnegative
   detector identity" Eq. (4.9) with each transition **paired with its adjoint**; **Conjecture 3**
   (Szöllősi family admits no quartet) is a *conjecture* in v2 — v1's import of it as a theorem
   from Chen–Liang–Hu–Chen (2021) is invalid, see McNulty–Weigert arXiv:2504.13067 — and v2's
   Prop. 4.2 needs Conjectures 2 **and** 3. Journal version J. Algebraic Combin. **63** (2026) 26;
   I did not check which arXiv version it reproduces.
7. **Sun**, arXiv:2610.12180, Theorem 8.2: strong unextendibility for clock-invariant triples of
   the displayed form. **Not** a general nonextension theorem.
8. **OpenAI** 2026 (two preprints): a second, independent computer-assisted proof; hypothesis
   "binary64 arithmetic and compiler conditions".

Do **not** write: that $N(6)=3$ is open; that forcing a diagonal symmetry is the missing
lemma; that the order-two divisibility lemma is needed; that the nonnegative-detector device is
new; that Sun's theorem covers all symmetric triples.

---
Script for §3.2-§3.6 (and for every [V] item): [`m2-explicit-triples.py`](m2-explicit-triples.py). Census table and the
exact $\Delta$ certificates: [`m2-delta-census.md`](m2-delta-census.md).
