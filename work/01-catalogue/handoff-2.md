# handoff-2 — to the catalogue owner (d1) and T8: missing ids, and the evidence for the notation table

```
from:         m3 (T1, audit direction d2)
to:           T1 catalogue owner (claims.yaml, dependencies.dot, notation.tex); T8
version:      1 — 14 Nov 2026
depends-on:   the preprint; reports/T1-audit-report.m3.md §§2, 4.2
blocks:       nothing (input only)
artefacts:    reports/T1-audit-report.m3.md, reports/sclaims.tsv, handoff-2.md
claims touched: (4.5),(4.6),(4.7),(4.15),(4.17),(5.17),(6.2),(A.16); the three Root naming systems
open questions: I3 (k<=10), I4 (Stage C radius range)
```

## 1. Five unnumbered statements missing from the mission's list

Add to `claims.yaml` (each is load-bearing and already has consumers):

| proposed id | statement | locator | consumer |
|---|---|---|---|
| `root-disp-n` | for every horizontal $\delta$ with $F(P+\delta)=0$, $\|(I-TT^*)\delta\|\le n_0+id\,s+Cs^2$, $s=\|\delta\|$ | Def 4.1, (4.5), p. 21 | Prop 4.13, (5.9)–(5.10), (6.2) |
| `root-disp-s` | $s^2\le(1+ort)\|\eta\|^2+\|(I-TT^*)\delta\|^2$ with $\eta=T^*\delta$ | Def 4.1, (4.6), p. 21 | Prop 4.13, Lemma 5.1 |
| `root-diff` | for horizontal $v$, $\|(I-TT^*)h'\|\le[id+C(\|\delta\|+\|v\|)]\|h'\|+\text{mnorm}\|F(P+v)\|$ | Def 4.1, (4.7), p. 22 | Prop 5.2's third bound in (5.10) |
| `root-suff` | (4.4) + $\|M\|\le\text{mnorm}$, $\text{mnorm}\cdot\text{froot}\le n_0$, $\|\Pi-TT^*-ML_P\Pi\|\le id$, $C\ge\pi b$ ⇒ certified Root | Prop 4.5, (4.15), p. 24 | Prop 4.6, the checker's Root test |
| `Dhat-spec` | $\|\eta-\eta_q\|\le t\Rightarrow\|\delta-d_q\|\le\hat D(t)$, $0\le t\le 2$ | (5.17), p. 35 | (5.18), Lemma 5.4, Lemma 5.5 |
| `stageC-iface` | $\eta=T^*\delta$, $\|\eta\|\le r_H=\sqrt{1+\omega}\,r$, $\|\nu\|\le n_0+\iota r+\Gamma r^2$ | (6.1)–(6.2), p. 41 | every §6 inequality |
| `patch-out` | on every successful `buildH::patch` path the six inequalities (A.16) hold | §A.5, p. 63 | Prop 4.6 |

(`patch-out` is the checkable form of Prop 4.6 and the value of `disposition = CHECK` for
`S-Root-1` in `reports/sclaims.tsv`.)

## 2. The seven Root constants: three naming systems, with locators

All seven are **nonnegative real stored numbers**; the acceptance ranges are §5.6 p. 39 and
§A.5 p. 63. The polynomial is $n_P(s)=n_0+id\,s+C s^2$ (4.3), evaluated at $s=r$ in (6.2).

| Def 4.1 (p. 21), and §7.1's record (p. 50) | §5.1 (5.2) p. 33 | §6.1 p. 41 | what it is, in words | type / unit | bound |
|---|---|---|---|---|---|
| $C$ | $\gamma_P=C_P$ | $\Gamma$ | coefficient of the quadratic term of the normal-displacement bound; an upper bound for $\pi b$ of Lemma 4.3/4.4 | real ≥0, cycles$^{-1}$ (multiplies $s^2$) | $<20$ |
| $n_0$ | $n_{0P}$ | $n_0$ | constant term: how far an exact solution may sit off the stored tangent frame at $s=0$; must dominate $\text{mnorm}\cdot\text{froot}$ | real ≥0, cycles | $<10^{-6}$ |
| $id$ | $\alpha_P$ | $\iota$ | coefficient of the linear term; the *difference* bound (4.7) uses it as the $s=0$ slope | real ≥0, dimensionless | $<10^{-4}$ |
| $ort$ | $o_P$ | $\omega$ | Gram defect $\|T^*T-I\|$: how far the stored tangent columns are from orthonormal | real ≥0, dimensionless | $<10^{-5}$ |
| $hor$ | $\text{hor}_P$ | — (not used) | $\|(I-\Pi)T\|$: how far the stored tangent columns are from horizontal | real ≥0, cycles | $<10^{-5}$ |
| mnorm | $\mu_P$ | — (not used) | an upper bound for $\|M\|$, the auxiliary right inverse of $L_P$ ($M$ is not serialized) | real ≥0, dimensionless | $<2$ |
| froot | $\varepsilon_P$ | $f_0$ | $\|F(P)\|$: the residual of the stored centre | real ≥0, cycles | $<10^{-6}$ |

Three remarks the notation table should carry:

* `hor` and `mnorm` genuinely disappear at Stage C, because (4.5) (not (4.7)) is the only Root
  assertion Stage C uses. The "–" entries in §6.1 are correct, not an omission.
* $n_P$ is a *function*, $n$ in (6.2) is its value at $s=r$, and $n$ is also $112$ in §2 and
  $n=2L+1$ in §5.3. Three meanings, one letter. Recommend $n_P(\cdot)$, $n_{\text{rec}}$, $N=112$,
  $n_{\text{grid}}$.
* $\varepsilon$ occurs four times: $\epsilon$ (centre correction, cycles, (4.20)),
  $\varepsilon_P=\text{froot}$ (§5.1), $\varepsilon_{\exp}$ (expair, (A.10)), and
  $\varepsilon$ the unit roundoff $u=2\cdot10^{-16}$ in (A.1) — which the paper also calls $u$,
  colliding with the Stage-B displacement $u$ in (5.21). Four distinct objects.

## 3. The other clashes, with locators (for `notation.tex`)

* **$D$** is six things: the comparison block (3.15) p. 16 (stated explicitly: "The symbol $D$
  henceforth denotes this comparison block"); $D'$ the lower-right block of the feasible
  completion (3.1); $D_j$ its entries, $m_j=|D_j|$, $D_j^\circ$ (Lemma 4.8); $D_0$ the unwrapped
  dephasing (2.2); $D_O,D_U$ the edge-derivative rows (6.17); and $\hat D(t)$ the Stage-B
  distance function (5.17) — which is the *iteration output*, not a block, and is the one that
  must not be confused with $D$. Recommend $D_{\text{cmp}}$, $D'$, $D_0$, $D_O,D_U$,
  $\hat D(\cdot)$.
* **$m$** is three things: $m=\min(m_B,m_C)$ the pair of lower singular bounds (3.5) p. 14;
  $m_j=|D_j|$ (Lemma 4.8) p. 26; and the integer vector $m\in\mathbb Z^6$ of Lemma 6.4 p. 44.
* **$M$** is two things: the auxiliary map $\mathbb R^{30}\to\mathbb R^{36}$ (Prop 4.5);
  $M$ the Stage-C bin resolution (Lemma 6.1). Also $N$ is two: the seed grid $112$ (§2.2) and the
  integer matrix in (4.17)/(5.5).
* **ball / cell / bin / box / sphere / Record / Root.** Recommend exactly this usage:
  * **bin** — a closed interval in one phase coordinate, at resolution $N=112$ (§2) or $M\in
    \{12,24,48,96\}$ (§6); "bin pair" = the seed pair; "bin path" = the nested Stage-C chain.
  * **cell** — a product of four closed angular intervals in the $U(2)$ parametrisation (3.12),
    i.e. one node of the Stage-A subdivision tree. Never a phase region.
  * **box** — a product of closed intervals in *tangent* coordinates, $B(u,h)\subset\mathbb R^k$
    (5.21); "base box" is one node of the Stage-B grid.
  * **ball** — a closed Euclidean ball: `seed ball` (radius $.0320001$ in $\mathbb R^9$),
    `phase ball` = the solution set $S(P,r)$ of a Record (5.1), `vector ball` $B_{\text{vec}}(v,s)$
    (6.14, closed modulo global phase).
  * **sphere** — the source's word for a phase ball; the paper's Def 4.14 already glosses it
    ("The term sphere in the source includes the interior and boundary of this closed ball").
    Do not use it in the new text except in that gloss.
  * **Root** — the certificate (Def 4.1): centre, tangent frame, seven constants. Data, no radius.
  * **Record** — Root + radius (Def 4.14); the serialized file object (§7.1, $356+288k$ bytes).
  * **atlas** — the merged list of Records; **blocker** — an earlier *completed* parent (§5.5).
