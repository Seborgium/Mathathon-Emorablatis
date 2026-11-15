# T1 audit report (m3) — the claim inventory tested against the paper

```
from:        m3 (T1, audit direction d2)
to:          T0 lead; T1 catalogue owner; T2 checker; T4 Lean; T8 paper
version:     1 — 14 Nov 2026
depends-on:  preprint 24 Sep 2026; .scratch/mub6.txt; results/proof-claims.md; results/code-audit.md
blocks:      nothing — read-only input to claims.yaml, dependencies.dot, notation.tex
artefacts:   reports/T1-audit-report.m3.md (this file); reports/sclaims.tsv; reports/statement-uses.tsv;
             reports/implicit-edges.tsv; changerequests/T1-audit.md (CR-T1A-1..9); handoff-1.m3.md;
             handoff-2.md
claims touched: lem-4.4, (6.3), lem-3.7/(3.24), lem-4.10/(4.29), lem-2.7, lem-2.9, (6.8), (6.10),
             (6.22), lem-6.8, prop-4.6, prop-6.9, §5.6, §6.1, §7.2
```

Page numbers are the paper's printed page numbers, which equal the PDF page numbers (verified with
`pdftotext -f N -l N` against `pdfinfo`: the PDF has 76 pages and the title page carries no footer;
`claims.yaml`'s header states 77 pages and "printed = PDF − 1", which is wrong — CR-T1A-6).

## 0. Division of labour, and how this was checked

Two other members hold the catalogue *build* (claims.yaml, dependencies.dot, notation.tex,
reader-path.md). My registered direction (d2) is the audit that *tests* an inventory: for each
statement the paper invokes, does the printed hypothesis set supply what the using step consumes;
does the displayed algebra reproduce; is each constant's unit and source the one claimed. This file
is therefore not a competing catalogue but the correction list, the S-claim triage, and the
dependency evidence that the catalogue needs.

Three methods, and one warning worth more than the methods:

1. **Reference closure.** Every statement label and every `(d.d)` tag in `.scratch/mub6.txt`
   extracted with its line number, and every reference resolved. Results in §3.
2. **Use versus statement.** For each statement, read the places that consume it and ask whether
   the printed quantification (closed/open, ≤/<, "for every"/"there exists", cycles/radians,
   which radius) is the one the consumer needs. Results in §2.
3. **Re-reading the display.** The layout extraction lifts a radical or the numerator of a stacked
   fraction onto the *preceding* text line: `b = 8‖M‖` in the extraction is `b = √8‖M‖` in the PDF.
   Three of the seven corrections below come from this. Where the reading stayed ambiguous I
   resolved it from character coordinates (`pdftotext -bbox-layout -f N -l N`): delimiter and
   exponent positions settle whether a term sits inside a radical or a fraction. Anyone auditing
   this paper from `mub6.txt` should know this before concluding anything about a formula.

I did not re-prove any lemma end to end, I did not see the code, and I ran no numerics.

## 1. Corrections to the restatements

**C1 — Lemma 4.4: the radicals are missing.** The paper (p. 23) reads $b=\sqrt8\,\|M\|$ and
$b=\sqrt6\,\|S\|$, not $8\|M\|$ and $6\|S\|$. Three witnesses: the extraction carries two `√`
glyphs on the line above the display; the proof is Cauchy–Schwarz over edges,
$\sum w_{ij}a_{ij}\le(\sum w_{ij}^2)^{1/2}(\sum a_{ij}^2)^{1/2}\le\|M\|\sqrt8\,\|x\|^2$; and §A.5
(p. 62) states the resulting constant as $\hat C=\pi\sqrt8\,\text{mnorm}+10^{-7}$. *Why it matters:*
with $8\|M\|$ one gets $C\approx25.1\,\text{mnorm}$, and §A.5 requires $C<20$ with
$\text{mnorm}<2$, so the first C-candidate would be unusable and would contradict the paper's own
acceptance threshold. With $\sqrt8$, $C\le17.8<20$.

**C2 — §6.1: $\|AA^*-6I\|_F=2\pi\sqrt2\,\|F(P)\|$, not $2\pi^2\|F(P)\|$.** Since
$(AA^*)_{ij}=2\pi iF_{ij}$ off the diagonal, $\|AA^*-6I\|_F^2=4\pi^2\sum_{i\ne j}|F_{ij}|^2
=8\pi^2\|F\|^2$, the same $8\pi^2$ that the paper's own identity in the proof of Lemma 4.7 uses.
So (6.3)'s constant is $\sqrt2\pi/3\approx1.481$ and $K<1.00001$ follows from $f_0<10^{-6}$ with
three orders to spare.

**C3 — Lemma 3.7: the fourth-order coefficient is 63, not 2646.**
$E_r^2=e_{\mathrm{off}}^2+(\sqrt6\sqrt{42}/2)^2h^4+p^2=e_{\mathrm{off}}^2+63h^4+p^2$; the proof's
own line is "$p+\sqrt6(\sqrt{42}/2)h^2$" (p. 19) and §A.4's $E_3=\tfrac12\sqrt{252}h^2+\mathrm{pol}$
is the same coefficient. $\frac{\sqrt6\cdot42}{2}=21\sqrt6$ overstates the term by a factor 42.

**C4 — Lemma 4.10: $S_\Delta/\pi$ is inside the radical in (4.29).** By character coordinates on
p. 28 the closing delimiter is at $x=358.29$, after $S_\Delta/\pi$ ($x=342$–$356$) and before the
exponent $\tfrac12$ ($x=366$). So
$\|\delta\|\le(\|\Delta\|^2+\frac{R_s^2+\mathrm{arc}^2}{(2\pi)^2}+S_\Delta/\pi)^{1/2}+\|\epsilon\|$,
which is exactly what `covercompute::value` computes,
`sqrt(nd + d2 + (supp+.0001)/pi + 1e-5)`. With the term outside, the inequality is false in the
operating range. **This is not a defect of the paper**, only of every restatement of it.

**C5 — kinds.** 6.4 is a **Lemma** (p. 44), not a Proposition; 4.5, 4.6, 4.13, 4.16, 5.2, 5.7, 6.9
are Propositions and 3.10, 5.8 are Corollaries as usually listed. `claims.yaml` should carry the
paper's kind.

**C6 — "the margin table (A.12)"** is §A.12 (p. 74), an unnumbered summary table; the equation tag
(A.12) is the $|\Delta G_{ij}|<10^{-12}$ bound in §A.4. Fine in prose, wrong as a pointer.

**C7 — `claims.yaml` v1 (19:18) reproduces C1, C3 and C4**, so those three are live errors in the
frozen inventory: `lem-4.4` carries `b = 8 ||M||`; `lem-3.7` and `eq-3.24` carry
`((sqrt6 * 42)/2)^2`; `lem-4.10` puts `S_Delta/pi` outside the radical. Two further slips are its
own: `lem-2.7` states `u, Delta in R^6` where §2.3 and the lemma use five varying coordinates
($\mathbb R^5$, $j=0..4$), and `lem-2.9`'s (2.18) is printed as the tautology
`2k.h <= 2k.h + sum_j |k_j|` instead of `2k.h <= sum_j |k_j|`. All are filed as
`changerequests/T1-audit.md` CR-T1A-1..9, with the blocking ones marked.

## 2. Internal inconsistencies in the paper

**I1 — (6.8) has the wrong conjugation and contradicts the line below it. Severity: statement
error, no numerical consequence.** The paper defines $J_{ij}=-\operatorname{Im}(S_iq_{ji})$ and
immediately asserts $\sum_jJ_{ij}=0$. But $\sum_jq_{ji}=S_i$, so
$\sum_jJ_{ij}=-\operatorname{Im}(S_i^2)=-2\operatorname{Re}S_i\operatorname{Im}S_i$, zero only for
special $S_i$. The identity holds for $J_{ij}=-\operatorname{Im}(\overline{S_i}q_{ji})$, which is
also what the expansion produces: $S'_i=S_i+2\pi i\sum_jq_{ji}(x_j-\delta_{ji})+\dots$ gives
$2\operatorname{Re}(\overline{S_i}\Delta_i)/(4\pi)=\sum_jJ_{ij}(x_j-\delta_{ji})$ only with the
conjugate. It is used — the proof of (6.11) needs "$Jx=Jd$ because every row of $J$ sums to zero".
Nothing downstream changes numerically (every later use of $J$ is inside an absolute value or a
support), so the fix is one sign; it must be in the frozen statement before T4 formalises (6.8).

**I2 — the same letter $S$ is two different sums, one subsection apart. Severity: comprehension,
load-bearing for a formaliser.** (6.5): $S_i=\sum_jq_{ji}$, $q_{ji}=e(u_j-P_{ji})/\sqrt6$, necessary
condition the *linear* $|S'_i|=1$. (6.15): $S=\sum_jQ_j$, $Q_j=e(u_j-v_j)$, no $1/\sqrt6$,
necessary condition the *quadratic* $|S'|=\sqrt6$ — which is why (6.16) tests
$\bigl||S|/\sqrt6-1\bigr|$. Each subsection is self-consistent; a reader or a Lean statement that
carries one $S$ across §6.2→§6.4 is wrong by $\sqrt6$. Recommend $S^{[1]},S^{[2]}$, or always
include $1/\sqrt6$ and state $|S'|=1$.

**I3 — $k\le10$ is stated three times and is unreachable at the declared widths. Severity:
internal tension, no soundness gap.** Def. 4.1 (p. 21), §5.6 (p. 39), §7.3 (p. 52) allow
$0\le k\le10$; §5.6 also caps the base grid at $5\cdot10^7$ boxes with $L=\lceil E/w+0.500001\rceil$
and $E\le\sqrt{1+o_P}R$. At the three prescribed $(w,R)$ pairs this gives $L=11,15,5$, i.e.
$23^k,31^k,11^k$ boxes and $k\le5,5,7$. Table 1 reports zero bad parents, so the run itself
certifies $k\le5$ for every record entering B: the stated allowance is dead, half of §A.9's
$k$-dependence is never exercised, and "the Root dimension is at most 10" is not what the run used.
Already `results/code-audit.md` F3; recorded here because it must be an open question with an
owner (T5), not a silent number.

**I4 — the Stage-C and Stage-B radius ranges are incompatible globally. Severity: bookkeeping, must
be a hypothesis.** §6.1 needs a Record radius $0\le r\le.03$; §5.6 admits $10^{-4}\le\tau\le.126$
and input radii up to $.126$. Only the $.016$ and $.011$ passes qualify, and §7.2 confirms C reads
the $.016$ batches. So "Stage C is applied to records of radius $\le.03$" is a pipeline condition
never stated as one; composing Prop 5.7 with Prop 6.9 at $\tau=.07$ gives a meaningless statement.

**I5 — (6.22) versus (6.10)/(A.24): print the factor 2.** (6.10) has $2/\sqrt6$ on
$\|S\circ y\|Xr$ and $1/\sqrt6$ on $\|S\circ y\|_\infty r^2$; (A.24) has the same pair. The layout
of (6.22) is ambiguous about the first. I claim no error — only that T8 must typeset (6.22) with
explicit coefficients, because a factor 2 there sits at the $2\cdot10^{-7}$ margin.

**I6 — trivial but print it right.** (2.5) writes $\sum_{j=0}^{5}e(x_j)=0$ for the six-entry list
$x=(0,x_1,\dots,x_5)$; correct, but every later use is "$1+\sum_{j=1}^{5}e(x_j)=0$".

**I7 — the §2/§3 coordinate correspondence is never written down. Severity: comprehension.**
§2 covers $q=(x_1,\dots,x_5,y_2,\dots,y_5)\in\mathbb R^9$ (2.15); §3 uses the nine entries at
row-major positions $(7,8,9,10,11,13,19,25,31)$, i.e. $s=(a,b_0,\dots,b_3,c_0,\dots,c_3)$ in
radians. I verified the identification: $x_1,\dots,x_5$ are row 1, columns 1–5 (positions 7–11)
with $a=x_s$ the shared entry (the selected column moved to position 1); $y_2,\dots,y_5$ are
column 1, rows 2–5 (positions 13,19,25,31) after the row permutation. Nine numbers, the shared one
counted once, and §2.4 states the selected-column permutation preserves the distance — so Prop 2.10's
ball and §3.1's seed ball are the same object in two coordinate systems, one in cycles and one in
radians ($R_s=2\pi r_s$). This map belongs in `notation.tex`: it is what lets Prop 2.10 feed
Prop 3.11.

**I8 — units.** The paper's convention ("an angle is in radians only when this is stated
explicitly", p. 6) is followed consistently; the hazard is that the same letters recur in both
units.

| quantity | unit | where |
|---|---|---|
| seed phases $x_j,y_j$; seed radius $.032$, $.0320001$ | cycles | §2, (2.15), Prop 2.10 |
| $q\in\mathbb R^9$, $h=N(q-u)$, $k=N(u-u')$ | cycles (grid units) | §2.3–2.4 |
| $s\in\mathbb R^9$ and $R_s=2\pi r_s$ | radians | §3.1, (3.3) |
| cell angles $\theta$, $\lvert\theta_j\rvert\le h=\pi/N_u$ | radians | (3.13) |
| $D$, $Z$, $z$, $E_r$, $p$ | dimensionless (entry scale) | §3.4–3.5 |
| $d_j$, arc, weighted, $q_d$ | radians | Lemma 4.8 |
| raw $u$ (radians) vs centre correction $\epsilon$ (cycles): $P_0+\epsilon+u/2\pi$ | mixed, explicitly | (4.21) |
| $\delta,\Delta$; all ball and Record radii $r$, $\tau$, $R$ | cycles | §4.5–§5 |
| $\eta$, $n_0$, $id$, $C$ (normal-displacement constants) | cycles | Def 4.1, (4.5), (6.2) |
| external tangent error $.00012$, margin $.00015$ then $/2\pi$ | radians then cycles | p. 30 |
| vector phases $x$, bins $w=1/M$, $s<.1$, $X_M,L_M,I_M$ | cycles | §6, Lemma 6.1 |
| $2\pi$ in (6.6), (6.9), (6.18) | cycles→radians conversion | §6.2, §6.4 |

## 3. Checks that came out clean

* **No dangling reference.** 58 statement labels, 137 equation tags; every `(d.d)` reference
  resolves. Every label is named at least once in the paper, but for 17 of the 58 the only naming
  is its own statement (§7), so the graph is sparse, not broken. The four apparent misses are
  bibliographic: "[15, Theorem 1.4]" (p. 3), "[10, Corollary 2.3]", "[3, Theorem 5.2]" (p. 5),
  "[11, Theorem 2.5]" (p. 57).
* **Identities re-derived and matching**: (4.13) $\sum_{i>j}a_{ij}=6s^2$ and $\sum_{i>j}a_{ij}^2
  \le8s^4$; (4.19); (3.8) with the trace bound (3.9) and $q=R_s^2(1+(A_*^2+6)/m_C^2)$; (6.18)–(6.19)
  with $E_O=\pi r_e^2$ and $E_U=\pi r_e^2(1+|S|/6)$; (4.17); (5.11)'s $\beta$, where the extra
  $(1+o_P)$ comes exactly from $\|S_h^*T(I-T^*T)\xi\|$.
* **Lemma 6.5's numeric chain** is $6-2\pi\sqrt6\|z\|\ge6-\frac{2\pi}{5}\sqrt6>6-\frac{22}{7}>\sqrt6$
  at $\|z\|\le.2$; the extraction hides the $/5$ and the middle inequality is $2.921>2.857$. Not an
  error.
* **Table 1 is internally consistent**: $62{,}470\cdot2+62{,}469\cdot2=249{,}878$;
  $764+774+757+788=3083$; $87\cdot256+107=22{,}379$; $3\cdot282+281=1127$; $73+15=88$; $163$ = the
  sum over the fifteen `bad*.bin` files. Bookkeeping discipline, not correctness.
* **The Stage-C reduction chain is right**: Lemma 6.5's $s<.1$ makes twelve labels distinct,
  Lemma 6.4 covers each retained bin by one closed ball, (6.24) is exactly the pattern two further
  MUBs need, and Prop 6.9 ← Lemmas 6.4, 6.5, 6.7, 6.8 is complete.
* **(4.29) read correctly** (C4): the term is inside the radical. Do not file a change request
  against the paper on that point.

## 4. Every S-claim, with a disposition

Full table: `reports/sclaims.tsv` — 40 rows (38 `S`, 2 `E`), columns
`id, paper_locator, subject, statement, kind, evidence, disposition, owner, rationale`. Vocabulary
from `results/plan.md` §9.2: **PROVE** (by hand, in a line), **CHECK** (a stored number plus an
inequality the checker re-evaluates in interval arithmetic), **FORMALISE** (T4 proves it about a
finite algorithm), **HYPOTHESIS** (into Theorem 7.1's finite-execution hypothesis), **OBSOLETE**
(about the old code, no analogue), **SPLIT** (mixes two).

Counts: 20 CHECK, 7 PROVE, 5 OBSOLETE, 4 HYPOTHESIS, 2 CHECK+PROVE, 1 SPLIT, 1 FORMALISE.

### 4.1 The punchline

The paper's ~30 distinct code claims collapse to **three surviving obligations and one hypothesis
group**:

1. **Seed enumeration completeness** (`S-seed-5`) — the only part of Prop 2.10 not proved from the
   text. Becomes structural in the reference implementation (nested loops over a declared index box)
   and a range-and-count check in the checker. Owner T2+T3.
2. **Clique-search completeness** (`S-C-4`, Lemma 6.8) — the one lemma whose subject is an
   algorithm. Formalise it in T4 as a function on finite graphs with spec "false ⇒ (6.24)
   infeasible" (about 30 lines over a bitset model), cross-check T3 against it; T2's
   witness-characterisation is the fallback. Owner T4, fallback T2.
3. **Certificate-type discipline** (`S-C-5`, `S-B-6`) — a negative record carries its witness, a
   coverage record carries its radius and the bound that justifies it, no cap exhaustion is ever
   negative. This stops being a claim about code once the format enforces it. Owner T2.
4. **The finite-execution hypothesis** (`S-7-2`, `E-1`) — five terminal conditions become one
   sentence, "the checker accepts the certificate file", with the observed run reported as a datum.
   Owner T8.

Everything else is either a heuristic whose output the proof never needs (mk's tie-break, sumok's
directions, trial::pass, snapping, Lloyd iterations, mapH's signature, relationB's cuts, the
ρ-search's 25 trials, integer lifts) — one line of PROVE deletes it; or a stored number the checker
re-evaluates (the Root constants of Prop 4.6, the supports of (4.29), (4.37), (5.17), the §6 bin/edge/
joint tests); or an artefact of the binary64 model (Lemmas A.1–A.2, §7.1's platform conditions)
which disappears if the checker evaluates in exact/interval arithmetic — the largest available
simplification, and the one that shrinks Appendix A from 20 pages to about 4.

Prop 4.6 deserves its own sentence, because `results/code-audit.md` F1 calls it the heaviest
unverifiable claim and it is: but in the certificate reformulation it stops being a claim about
`buildH::patch`. The record stores $(P,T,M,C,n_0,id,ort,hor,\text{mnorm},\text{froot})$; the checker
verifies (4.4) and (4.15) directly from the stored data; Prop 4.5 then applies verbatim. That is a
finite arithmetic check, which is why no eigensolver has to be trusted.

### 4.2 Completeness of the unnumbered-statement list

The fifteen the mission lists — (2.6), (2.12), (2.14), (3.19), (3.24), (3.26), (3.29), (4.17),
(4.20), (4.38), (5.26), (6.7), (6.11), (6.23), (6.24) — all exist and are correctly identified.
Six more belong in the same list and are missing from it (proposed ids and texts in `handoff-2.md`
and CR-T1A-4):

* **(4.5), (4.6), (4.7)** — the three displacement assertions of Def. 4.1. They *are* the content of
  a Root; without them the definition carries no obligations and F1's finding is unstatable.
* **(4.15)** — the three inequalities Prop 4.5 turns into a certificate. This is the interface
  between the checker and the proof; with no id, T2 has nothing to cite.
* **(5.17)** — the semantic property of $\hat D$: $\|\eta-\eta_q\|\le t\Rightarrow\|\delta-d_q\|\le
  \hat D(t)$, $0\le t\le2$. It deserves to be the *statement* of Lemma 5.4 rather than a remark.
* **(6.2)** — the Stage-C interface ($\eta=T^*\delta$, $\|\eta\|\le r_H=\sqrt{1+\omega}r$,
  $\|\nu\|\le n_0+\iota r+\Gamma r^2$): the third naming system, and the only place §6 depends on §4.
* **(A.16)** — the six inequalities §A.5 establishes on every successful Root path: the checkable
  content of Prop 4.6 and the natural target of the checker's Root test.
* **(6.22)** — $E_t^{\text{ball}}$, the bound `graph::joint` evaluates (CR-T1A-9).

## 5. Open questions for other teams

* **Q1 (T2, T9).** Is (6.22)'s $Xr$ coefficient $2/\sqrt6$? (6.10) and (A.24) say yes; the layout of
  (6.22) is ambiguous (I5). One coordinate pass on p. 46 settles it.
* **Q2 (T5).** Resolution of $k\le10$ vs the $5\cdot10^7$ box cap (I3): raise the cap, lower the
  allowance to $k\le7$ with the operative bound $k\le5$, or report the histogram. The catalogue
  needs one as the hypothesis.
* **Q3 (T2).** Does the checker verify (4.29) as a support bound (quantified over $u$ via
  $\Delta\cdot\Pi u$) or at a stored $u$? The paper's (4.29) is the former, `covercompute`'s `s0` is
  the latter plus margins; the difference changes what a rejected record means.
* **Q4 (T4, T9).** Formalising (6.8) needs the conjugate of I1; confirm that no step after (6.9)
  uses the *sign* of $J$ before the statement is frozen.
* **Q5 (T8).** The paper never says what a certificate *is*, in one sentence. Proposed: "a
  certificate is a finite list of records $(P,T,C,n_0,id,ort,hor,\text{mnorm},\text{froot},r)$, each
  with either a coverage witness (the ball it covers and the bound that justifies it) or an
  exclusion witness (the necessary inequality that fails and its direction), such that the covered
  balls contain every exact second-basis Hadamard matrix up to equivalence and no record carries an
  exclusion witness." Everything in §§2–7 is then either "this witness type is sound" or "this is
  how witnesses are found" — the division of labour T8 wants.
* **Q6 (T5, T8).** Does the archive contain the per-record $k$ histogram and the per-stage maxima
  (`results/code-audit.md` F3, F6)? If not, "no unresolved record" rests on the terminal flags alone
  and the paper should say so in one sentence.

## 6. What I did not do

* No end-to-end re-derivation of Lemmas 3.2–3.9, 4.8–4.13, 5.2–5.6, 6.3–6.7: I checked that each
  printed statement supplies what its consumer needs, and re-derived the identities in §3, not every
  algebraic step of the Taylor ledgers.
* No code audit (the sources are not in the packet) and no verification of any `E` claim.
* No numerics, no Lean, no figures. Nothing here proves anything; it is a statement about
  statements.
* The catalogue files themselves are the other members' work; this dir also contains
  `handoff-2.md`, which supplies the catalogue owner with the missing ids and the evidence locators
  for the three Root-constant naming systems.

## 7. Files, and the one thing the catalogue owner cannot get from the paper

| file | what it is |
|---|---|
| `T1-audit-report.m3.md` | this file |
| `sclaims.tsv` | 40 rows: every `S`/`E` claim with locator, evidence, disposition, owner, rationale |
| `statement-uses.tsv` | the paper's *named* citation graph, mechanically extracted: 58 labels, section, line, every place each is named (enumerations such as "Lemmas 5.5 and 5.6" included) |
| `implicit-edges.tsv` | 85 dependency edges with `where_used` and `inference` ∈ {named, implicit-stated, implicit-by-content}; acyclic as written. Rows read "**from** is used by **to**" |

The one thing to know before trusting `dependencies.dot`: **the paper's named-reference graph is
sparse and cannot be the dependency graph.** 17 of the 58 labels are never named after their own
statement, and twelve of those are load-bearing (`lem-3.4`, `lem-3.7`, `lem-3.8`, `lem-3.9`,
`cor-3.10`, `prop-3.11`, `prop-4.6`, `lem-4.9`, `lem-4.10`, `prop-4.13`, `lem-6.2`, `lem-6.7`) —
the paper writes "the polar and unitary Taylor bounds", "the preceding lemmas", "these are exactly
the two successful negative paths". So every edge needs a semantic justification;
`implicit-edges.tsv` supplies 85 with a location and tags how each was inferred. Edges tagged
`implicit-by-content` should be re-checked by the owner of the consumer. The graph is sparse, not
broken: every `(d.d)` reference resolves and every label is named somewhere.
