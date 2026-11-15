# The MMVW conjectures, version by version — v1 vs the current v2, with detectors evaluated

*member m2, swarm `smwhnslql`, direction d7 ("version-explicit attack on the current MMVW
conjectures"). Written 2026-11-15. Script: [`m2-explicit-triples.py`](m2-explicit-triples.py)
section (5); run `python3 m2-explicit-triples.py`.*

**Why this note exists.** My first two submissions cited
Matolcsi–Matszangosz–Varga–Weiner (MMVW) from **v1** of arXiv:2503.14752 while naming the
current version: they described Eq. (4.7) as *the* identity, claimed Proposition 4.2 needs
Conjecture 2 alone, and omitted Conjecture 3. That is corrected below, with the two versions kept
apart and the numerical claims scoped. *The published journal version (J. Algebraic Combin. 63
(2026) 26) was not compared with either arXiv version; every citation here names the arXiv
version explicitly.*

| | v1 = arXiv:2503.14752**v1**, 18 Mar 2025 | v2 = arXiv:2503.14752**v2**, 19 Jul 2025 (**current**) |
|---|---|---|
| $\gamma_2$ clause of Conj. 2 | $G_{H_j}(\pi\gamma_2)=0$ **for two of the three $j$**, all $\pi$ | $G_{H_j}(\pi\gamma_2)\,G_{H_j^*}(\pi\gamma_2)=0$ **for every $j$ and every $\pi$** |
| $\gamma_1$ clause | $G_{H_j}(\pi\gamma_1)=0$ for all $j,\pi$ | same |
| single identity | Eq. (4.7): $\sum_j\tilde G_{H_j}(\gamma_1)+\sum_{j<k}\tilde G_{H_j}(\gamma_2)\tilde G_{H_k}(\gamma_2)=0$ | Eq. (4.9): $\sum_j\tilde G_{H_j}(\gamma_1)+\sum_j\tilde G_{H_j}(\gamma_2)\tilde G_{H_j^*}(\gamma_2)=0$ |
| what Prop. 4.2 needs | Conj. 2 alone, plus the Szöllősi exclusion **imported as a theorem** from [11] | **Conj. 2 *and* Conj. 3** (the Szöllősi exclusion is no longer available) |

Here $H_1=\sqrt6X_1^*X_2$, $H_2=\sqrt6X_2^*X_3$, $H_3=\sqrt6X_3^*X_1$, $H^*$ is the conjugate
transpose,
$$G_H(\gamma)=\Big|\sum_k\prod_iH_{ik}^{\gamma_i}\Big|^2,\qquad
  \tilde G_H(\gamma)=\sum_{\pi\in S_6}G_H(\pi\gamma),$$
$\gamma_1=(1,1,1,-1,-1,-1)$, $\gamma_2=3\gamma_1$.

## 1. Conjecture 3 and why v2 has it

**Conjecture 3 (v2).** *Any $S\in X(\alpha)$ in the Szöllősi family (MMVW Eq. (4.2)) cannot be
part of an MUB quadruplet.*

v2 says verbatim: *"In a previous version of this manuscript it was referred to as a proven fact
from the literature, but unfortunately the proof in [11] turned out to be wrong, as pointed out by
[25]."* The chain, verified at the sources:

* [11] = X. Chen, M. Liang, M. Hu, L. Chen, *$H_2$-reducible matrices in six-dimensional mutually
  unbiased bases*, Quantum Inf. Process. **20** (2021) 353 — depends on a lemma of Chen et al.,
  J. Phys. A **50** (2017) 475304;
* [25] = D. McNulty, S. Weigert, *Comment on 'Product states and Schmidt rank of mutually unbiased
  bases in dimension six'*, arXiv:**2504.13067** (17 Apr 2025). Its abstract, verbatim:
  "A lemma by Chen et al. … provides a necessary condition on the structure of any complex
  Hadamard matrix in a set of four mutually unbiased bases in $\mathbb C^6$. **The proof of the
  lemma is shown to contain a mistake, ultimately invalidating three theorems derived in later
  publications.**"

The previously cited proof route is therefore invalid, and **v2 leaves the Szöllősi exclusion as a
conjecture**. Any proof revision following MMVW must cite Conjecture 3 *as a conjecture* and show
which of Conj. 2 / Conj. 3 it uses. A separate, complete classification of all MUB sets may imply
the exclusion independently; that is a different proof route, not a validation of the old citation.

**Structural remark on Conjecture 3 [V].** In the normal form (4.2) all four $3\times3$ blocks of
$S$ are circulant; hence $S$ commutes with $P=C_3\oplus C_3$ ($C_3$ = cyclic shift, a $6\times6$
permutation of order 3, eigenvalues $1,\omega,\omega^2$ each twice). Verified on a random matrix of
that shape: $SP=PS$, and in the $P$-eigenbasis $S$ is block-diagonal with three $2\times2$ blocks
(off-block entries $\le 8.7\cdot10^{-16}$), while the standard basis becomes
$\hat F_3\otimes I_2$. So a pair $\{I,S\}$, $S\in X(\alpha)$, is equivalent to a pair
$\{\hat F_3\otimes I_2,\ \text{three }2\times2\text{ blocks}\}$. That is the $H_2$-reducibility
whose (invalidated) structure lemma was the content of [11] — which is presumably why Conjecture 3
sits exactly where the gap is. **I did not prove Conjecture 3.**

## 2. Both versions, evaluated

Exact representatives: the isolated triple (arXiv:2611.06917 Eq. (30)), the centre of the explicit
family (Eq. (31) at $(\theta_1,\theta_2)=(2\pi/3,-2\pi/3)$), and three generic interior points.
$720=36\times20$ permutations $=36$ copies of each of the 20 sign patterns; all counts below are
over the 720, so a pattern is "nonzero" iff all 36 copies are.

| triple | v1: $\tilde G(\gamma_1)$, $j=1,2,3$ | v1: $\tilde G(\gamma_2)$ | v1 "#$\gamma_2$ vanishing" | v2: $\max_{j,\pi}G(\gamma_1)$ | v2: $\max_{j,\pi}G(\gamma_2)G^*(\gamma_2)$ |
|---|---|---|---|---|---|
| isolated | $2\cdot10^{-28},6\cdot10^{-28},2\cdot10^{-28}$ | all $\le4\cdot10^{-27}$ | 3 of 3 | $2\cdot10^{-30}$ | $3\cdot10^{-58}$ |
| family centre | $\le3\cdot10^{-26}$ | $\le2\cdot10^{-25}$ | 3 of 3 | $7\cdot10^{-29}$ | $2\cdot10^{-55}$ |
| family (1.00,4.20) | $\le8\cdot10^{-27}$ | $\mathbf{6.5\cdot10^3},4\cdot10^{-26},2.9\cdot10^{-27}$ | **2 of 3** | $3\cdot10^{-29}$ | $2\cdot10^{-28}$ |
| family (2.00,4.00) | $\le2\cdot10^{-27}$ | $\mathbf{6.3},2.4\cdot10^{-26},1.6\cdot10^{-27}$ | **2 of 3** | $2\cdot10^{-29}$ | $1\cdot10^{-29}$ |
| family (3.00,0.50) | $\le6\cdot10^{-27}$ | $\mathbf{1.1\cdot10^4},4\cdot10^{-26},1.7\cdot10^{-27}$ | **2 of 3** | $3\cdot10^{-29}$ | $2\cdot10^{-28}$ |

So **both versions hold at every sampled representative**, and both are sharp: v1's $\gamma_2$
clause genuinely fails at one of the three transitions generically, and v2's product clause
genuinely needs the second factor. A further $25$ random interior family points give
$\max_{j,\pi}G(\gamma_1)\le1.6\cdot10^{-28}$ and $\max_{j,\pi}G(\gamma_2)G^*(\gamma_2)\le
3.7\cdot10^{-28}$.

**Scope.** These are numerical statements about the sampled representatives. The full assertion
over the two-parameter family (let alone all triples) is *not* established here; it would follow
from the classification (arXiv:2611.06917 Thm 3) together with a symbolic check on Methods
Eq. (31), which I have not carried out. Say "holds at all sampled representatives", not "holds on
every known triple".

**Fine structure (why the adjoint pairing is the right form).** At $(1.00,4.20)$:

| | $G(\gamma_1)$ nonzero | $G^*(\gamma_1)$ nonzero | $G(\gamma_2)$ nonzero | $G^*(\gamma_2)$ nonzero |
|---|---|---|---|---|
| $H_1$ | 0/720 | 0/720 | **432/720** | 0/720 |
| $H_2$ | 0/720 | 0/720 | 0/720 | 0/720 |
| $H_3$ | 0/720 | 0/720 | 0/720 | **432/720** |

Each transition fails the $\gamma_2$ test in exactly one of the two orientations, and the adjoint
supplies the other. $H_2$ passes both. That is precisely the situation Eq. (4.9) is built for.

## 3. Two proved mechanisms [V]

Write $\omega=e^{2\pi i/3}$. Suppose the order-three symmetry of a triple is
$T=\operatorname{diag}(\omega^{t_r})$ with each cube root occurring twice, and that a transition
$H$ is $T$-covariant with a two-3-cycle column action. Label rows by $(t,a)$ ($t\in\mathbb Z_3$ the
$T$-eigenvalue, $a\in\mathbb Z_2$) and columns by $(s,b)$ ($s$ = position in the 3-cycle,
$b$ = the cycle); then $H_{(t,a),(s,b)}=\omega^{ts}x_{(t,a,b)}$ after column phases/permutations.

**Lemma A (index mechanism, $\gamma_1$ only).** In the above notation
$$\sum_{(s,b)}h_{(s,b)}^{\gamma}=\sum_b\Big(\sum_s\omega^{sT}\Big)\prod_{(t,a)}x_{(t,a,b)}^{\gamma_{ta}},
\qquad T=\sum_{t,a}t\,\gamma_{ta}.$$
*Proof.* Insert the form and collect the $\omega^{ts}$ factor. ∎

Hence every $3{+}3$ split with $T\not\equiv0\pmod3$ vanishes **for every $T$-covariant matrix,
MUB or not** — $12$ of the $20$ patterns for $\gamma_1$ with the family's eigenvalue pairing. For
$\gamma_2=3\gamma_1$ the quantity $T$ is always $\equiv0$, so this mechanism is silent there —
consistent with §2, where $\gamma_2$ is exactly the clause that needs help.

**Lemma B (parity mechanism, adjoint side).** Suppose in addition that the transition has the
normal form of arXiv:2611.06917 Eq. (33),
$$H_{(t,a),(s,b)}=\omega^{ts}(-1)^{ab}x_t^b .$$
Then for **every $\pi\in S_6$ and every $3{+}3$ split $\gamma$** the *row-type* sum vanishes:
$$\sum_{(t,a)}\prod_{(s,b)}H_{(t,a),(s,b)}^{\gamma_{sb}}=0,
\qquad\text{i.e.}\qquad G_{H^*}(\gamma)=0 .$$
*Proof.* The product for row $(t,a)$ equals
$\omega^{tS}(-1)^{aN}\prod_{s,b}x_t^{b\gamma_{sb}}$ with $S=\sum s\gamma_{sb}$ and
$N=\sum_{s,b}b\,\gamma_{sb}=\sum_s\gamma_{s,1}$. Summing over $a\in\{0,1\}$ gives the factor
$1+(-1)^N$, which vanishes whenever $N$ is odd. For a $3{+}3$ split $N=2k-3$ (or $3(2k-3)$ if
$\gamma=3\gamma_1$), with $k$ the number of $+$ signs among the three $b=1$ columns; both are odd.
∎

Since $G_{H^*}(\gamma)=G_{H^{\mathsf T}}(\gamma)$ (as $(H^*)_{ik}=\overline{H_{ki}}$), Lemma B is
a statement about $H^{\mathsf T}$, and it explains the table in §2: the transition that has form
(33) satisfies the $\gamma_2$ clause automatically, in every orientation of every split, and the
product in Eq. (4.9) is then zero without any further input.

*What is not proved here*: that every transition of every triple has form (33). arXiv:2611.06917
asserts (33) for the two transitions out of an anchor; I did not verify it for the third
transition $H^{*}_j$, nor did I complete a symbolic proof of Conj. 2 on the family. So Conj. 2 is
**verified at sampled representatives, with a proof of one of its two clauses for matrices in the
form (33)** — nothing more.
