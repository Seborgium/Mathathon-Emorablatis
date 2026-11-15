# style.md — writing rules for T8 (the single final file)

Binding on `work/08-paper/`. Each rule has a test a reviewer can apply mechanically; a draft that
fails a test is not ready for G5. The rules exist because the paper's own defects are of four kinds:
prose that hides a quantifier, constants without units, code claims without a disposition, and three
names for one object.

Sources: `claims.yaml` (claim ids and statements), `notation.tex` (symbols and units),
`reader-path.md` (the narrative T8 writes around).

---

## 1. One reader path

1.1 The file has exactly one intended route: **one-page summary → six-page narrative (reader-path.md)
→ the five assembly statements → the mathematics that supports them → verification**.

1.2 Every section declares its place in that route with one of four labels in its first line:
`[narrative]`, `[assembly]`, `[support]`, `[verification]`. A section with no label is deleted or
labelled.

1.3 No forward dependency that the reader cannot follow: if §n uses a defined object, that object is
defined in §m ≤ n or in the narrative. Appendix material may be used only after it is named.

1.4 The five assembly statements (Prop 2.10, Prop 3.11, Prop 4.16, Prop 5.7/Cor 5.8,
Prop 6.9, then Theorem 7.1) appear **once**, together, in a single "assembly" section, each as a
displayed implication. Their per-stage machinery lives in `[support]` sections behind them.

**Test:** the table of contents can be read as a sentence; a reader who stops after the narrative
knows what is claimed, why it is plausible, and what the machine part contributes.

## 2. Statements in explicit quantifier form

2.1 Every numbered statement begins, in its first sentence, with its quantifier structure:
"For every …, there exists …", "If … then …", "There exists … such that …". A statement whose first
sentence is a noun phrase ("The exhaustiveness of …") is rewritten.

2.2 No statement uses "cover" without naming the space, the covering family and the tolerance:
"the closed balls of radius 0.032 cycles cover the nine seed coordinates of every exact Hadamard
matrix up to the equivalences of Lemma 2.2".

2.3 **"Up to equivalence" is always spelled out** — which equivalences (Lemma 4.7's signed
permutations, transpositions, rephasings, integer phase additions), and whether they preserve
extendibility in both directions. Never "up to symmetry".

2.4 Hypotheses that are *events* (a run completed, a routine returned) are stated as hypotheses, not
as facts, in the same sentence as the conclusion. The word "certifies" may not stand in for "proved
under the hypothesis that".

2.5 "Closed" is stated wherever it matters (balls, bins, cells, boxes, intervals). If a region is
closed, say so at first use and do not repeat; if a region is half-open, the cover is broken and the
paper must say why it is not.

2.6 Universally quantified heuristics: whenever a numerical object is *proposed* (a direction `y`, a
cluster assignment, a relation, a clique candidate) the statement says "for every admissible …" so
that the proposition does not depend on how it was found.

**Test:** take any numbered statement and ask "what is the set being quantified over, and is it
closed?" If the answer needs the paper's prose, the statement fails.

## 3. Every numerical constant carries its unit

3.1 Units are **cycles** (phase divided by 2π), **radians**, or **dimensionless**. Every constant in
running text or a display carries one of them, in words on first use: "radius 0.032 cycles",
"halfwidth h = π/N_u radians".

3.2 The conversion appears exactly where it is used, with its factor:
`R_s = 2π r_s` (seed radius, radians from cycles) and the `/(2π)` and `/π` in Lemma 4.10.

3.3 Radii of Records, phase balls, vector balls and bins are in **cycles**; angular displacements,
`h = π/N_u`, the `θ`-coordinates, `arc` and `d_j` are in **radians**. A sentence that adds or
compares two of these across units is a bug, not a style issue.

3.4 Every constant that is a *bound* says what it bounds and by what inequality:
"C = π·(smaller certified upper bound) is the quadratic coefficient of the normal polynomial n_P
(3.24)", not "C = 0.9".

3.5 The constants T5 owns (N = 112, R = 0.032, 0.0320001, N_u, 0.103, 0.125, the three (τ,w) pairs,
every cap, k ≤ 10, the eigenvalue split 0.64, K = 1.00001, q_d < 3.8, every margin) are printed
**once**, in T5's justification table, and referenced by name+value elsewhere. No local re-justification.

**Test:** grep every numeral in the draft. Each one is (a) followed by a unit, (b) an index/count, or
(c) cross-referenced to the constants table.

## 4. No claim about code without a pointer to its disposition

4.1 Every sentence whose subject is a program, routine, file, run, exit status, count or hash carries
one of four markers, in the form `[CODE: <claim id> → <disposition>]`:

| disposition | meaning |
|---|---|
| `promoted` | the statement is now an explicit hypothesis of the printed theorem, cited by name |
| `evaluated` | the statement is replaced by an inequality the checker evaluates on stored data |
| `formalised` | the statement is a statement about sets and is proved (T4) |
| `reported` | it stays an observation, printed as such, and no theorem depends on it |

4.2 The disposition of each claim is the `owner_team` + `open_questions` of its entry in `claims.yaml`.
A code sentence whose claim id has no disposition is a defect: write the disposition, or delete the
sentence and the claim it supports.

4.3 The seven sources, the four entry points and the archive are named once, in the verification
section, with the statement that **the packet contains none of them**. The word "verified" is not
applied to anything that depends on them unless the disposition is `evaluated` or `formalised`.

4.4 No stage summary may say "the program excluded all cases". The correct form is: "the run returned
a negative result for every record; by Proposition 6.9 that excludes every exact solution in each
such record, provided …".

**Test:** every paragraph that mentions a routine can be traced to a `claims.yaml` id and its
disposition. Otherwise it is narrative, and the narrative says so.

## 5. Vocabulary

5.1 Use `notation.tex` names only: the seven Root constants in Definition 4.1 form; `D^{cmp}` for the
comparison block; `D̂(t)` for the computed Stage-B function; `n_P(s)` for the normal polynomial;
`m_B, m_C, m` with subscripts; `ṁ_j = |D_j|`; `m` bold for the integer lift; `ε` for the centre
correction in cycles; `ε_exp` for 6·10⁻¹⁴; `N_grid` for 112; `N` bold for the integer lift matrix.

5.2 Ban the word **sphere**; write **ball**. Ban **region** unless it means one of bin/cell/box/ball
(Table 3 of `notation.tex`). Ban **point** for a phase matrix without saying "the phase matrix at".

5.3 `Root` and `Record` are capitalised everywhere (Table 3). A Root has no radius; a Record has one.

5.4 Say **phase ball** or **vector ball**, never just "ball", in any sentence where both are in play.

## 6. Claims discipline

6.1 Every numbered statement in the final file carries the id of its `claims.yaml` entry, in the form
`[c:lem-3.2]`. A numbered statement with no id is a new claim: it goes in a change request, it is not
printed.

6.2 Status is printed honestly. A statement tagged `C` prints its execution hypothesis; a statement
tagged `S` prints what it assumes about the routine; a statement tagged `M?` prints that its
bookkeeping was sampled. The reader is entitled to see which parts of the argument are air.

6.3 Cor 1.3 (Cartan subalgebras) is an application, not a step of the proof. It appears after the
theorem or in T7's section, never inside the chain.

## 7. Figures

7.1 Each of T6's figures is cited by exactly one named paragraph; an uncited figure is deleted at G5.
7.2 Figure F1 (the five nested covers) must appear on the page where the narrative names the five
stages, not in an appendix.

## 8. Length and build

8.1 Targets: 1-page summary, ≤ 6-page narrative, ≤ 45 pages total, verification appendix ≤ 4 pages
(replacing the 20 pages of Appendix A budgets by an interval-arithmetic statement plus the margin
table).

8.2 The build is `latexmk -outdir .scratch/build`, no warnings that indicate undefined references,
no `??` in the PDF.
