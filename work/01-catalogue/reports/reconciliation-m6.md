# Reconciliation: my 84-entry catalogue against the canonical 91-entry inventory

T1 / m6, rewrite of my rejected submission. Machine-readable form: `reconciliation-m6.tsv`
(94 rows: 81 matched, 3 only-mine, 10 only-canonical, with per-entry status and edge differences).

## 0. Three corrections to what I submitted before

**(a) The duplicate catalogue is gone.** `work/01-catalogue/` again contains exactly one interface:
the canonical `claims.yaml`, `dependencies.dot`, `notation.tex`, `style.md`, `reader-path.md` and
`reports/sclaims.tsv`. I deleted my parallel `*.m6.*` copies from that directory (they remain in
`.ultramath/smwgrqhwo/m6/` for the record). The seven consumer teams should cite the canonical ids.

**(b) My external claim was false and is retracted.** I wrote that $M(6)=3$ is "still open". As of
**4 November 2026** it is not: **arXiv:2611.06917**, M. Cárdenes Wuttig and J. Tindall, *Using topology
to reveal all mutually unbiased bases in dimension six* (v1, Wed 4 Nov 2026 18:59:48 UTC), proves that
no four MUBs exist in dimension six by an independent route — a topological connectedness result for
order-six complex Hadamard matrices (all but Tao's form) reducing the classification to finitely many
four-dimensional phase balls certified by interval arithmetic — and classifies all MUB sets in
dimension six. Verified on the arXiv abstract page. My statement rested on sources accessed
7 September 2026, before that paper existed. **Consequences for the inventory:** (i) the preprint under
catalogue is no longer the only evidence, so the honest external framing is "two independent
computer-assisted proofs with different certificate formats", not "the burden of proof rests on one
preprint"; (ii) T2's `cert-format.md` should be tested against *both* routes — agreement of two
independently written checkers on the same statement is the strongest evidence available here;
(iii) the same authors appear as reference [7] of the preprint (order-six Hadamard classification), so
the two works are related and the citation should be updated by T7/T8.

**(c) The two withdrawn findings, named.** *I3* — I suspected (3.24)'s constant was wrong. It is not:
the PDF reads $E_r=\sqrt{e_{\mathrm{off}}^2+\left(\frac{\sqrt{6\cdot42}}{2}\right)^2h^4+p}$, and
$\left(\frac{\sqrt6\sqrt{42}}{2}\right)^2=63$ is exactly what the proof's own bound
$p+\frac{\sqrt6\sqrt{42}}{2}h^2$ squares to; the canonical entry's $63h^4$ is right and mine was an
extraction artefact. *I7* — I claimed the margin table was not in §A.12. It is: the unnumbered table
*Summary of the comparison margins*, p. 74, 18 rows, every margin strictly larger than its adverse
error. `results/proof-claims.md`'s pointer was correct. Both retractions are in my own
`reports/T1-report.md`; nothing else from my inconsistency list is retracted.

## 1. Method

Ids are compared after a synonym map for renamings (`sec-7.2`→`flow-7.2`, `sec-7.3`→`bounds-7.3`,
`tab-1`→`run-7.5`, `tab-2`→`hashes-7.5`, `tab-A12`→`margin-a.12`, `lem-A.k`→`lem-a.k`); everything
else matches by id. "Matched" = 81 entries present in both. Status comparison is on the single
`status` field (the canonical file's `status_parts` is finer and I did not diff it). Edge comparison is
on the transitive closure of one-step `depends_on`, both mapped through the same synonyms.

## 2. (a) Presence: what one file has and the other lacks

**Only in mine (3), and all three should stay out of the canonical file.** `fig-1`, `fig-2`: the
canonical inventory has no figure nodes. Figures carry no proof obligation and T6 can cite the paper
directly; if an id is wanted, it should be `status: D`, not `M` as I had. `sec-6.7`: I gave the
margin *prose list* its own node; the canonical modelling folds it into `margin-a.12` (the table) plus
`app-a4-a11` (the derivations), which is better — one node for numbers, one for proofs. Drop mine.

**Only in the canonical file (10), and every one is a genuine addition to what I had:**

| id | what it adds | verdict |
|---|---|---|
| `prem-arith` | the arithmetic premises as a **node** instead of a repeated hypothesis | the single best structural idea in the canonical graph: it makes the undefined "compiler conditions" (my I1) visible as a node with no proof |
| `root-disp-n`, `root-disp-s`, `root-diff`, `root-suff` | Definition 4.1's three assertions and Prop. 4.5's sufficiency split into separate nodes | better than my monolithic `def-4.1`: each is one Lean lemma (T4) and one check (T2) |
| `eq-2.7` | the tuple/gap inequality Lemma 2.6 actually uses | my `lem-2.6` pointed at 2.4/2.5; theirs is precise |
| `eq-5.17` | the semantic property of $\hat D(t)$, including its $0\le t\le2$ guard | exactly the object my own open question 1 was about; I had it only inside `lem-5.3` |
| `eq-6.12` | the scalar test (6.12)–(6.13) | I had it inside `lem-6.3`'s text |
| `stagec-iface` | the Stage-C interface as a node | I had none |
| `app-a4-a11` | the derivations of the A.4–A.11 constants, used by `prop-4.6` and `margin-a.12` | I had only `tab-A12` |

**Conclusion (a):** my file is a strict subset in structure; there is nothing in my three extra nodes
that the canonical inventory needs. Freeze the canonical set.

## 3. (b) Status disagreements: 17, of which 16 resolve in the canonical file's favour

| class | ids | mine | canonical | verdict |
|---|---|---|---|---|
| definitions | `def-2.1`, `def-4.1`, `def-4.14` | M | D | **canonical.** I overloaded M for "no proof obligation"; D is the right tag and the plan's key has it |
| coverage propositions whose hypothesis is a completed run | `prop-2.10`, `prop-3.11`, `prop-4.16`, `prop-5.7`, `cor-5.8`, `eq-5.26`, `prop-6.9` | S | C | **canonical**, under "weakest tag on which the claim as stated depends". The code content is carried by named rows in `sclaims.tsv`, so C is not a weakening |
| lemmas with a certified-routine premise | `lem-4.9`, `eq-4.20`, `lem-5.4`, `lem-6.4` | S | M | **canonical**, and it is stronger: the mathematical statement is M once the routine's checks are a separate (checked) row — `S-Root-2`, `S-B-3`, `S-C-3`. My own report argued exactly this for `lem-6.4` while my tag said S: my file was internally inconsistent here |
| a lemma whose subject is an algorithm | `lem-6.8` | M? | S | **canonical.** "Correct if the code is what the text says" *is* S; M? hid that |
| a corollary that inherits the contract | `cor-1.3` | M | C | **canonical.** It is invoked under Theorem 1.1's hypotheses |
| a section treated as a claim | `sec-7.2` / `flow-7.2` | S | E | **neither as tagged.** We are describing different objects: mine is the five terminal conditions (a specification; the canonical ledger's own `S-7-2` calls it HYPOTHESIS), theirs is the control flow (also a specification). Neither is an observed datum. Fix in D2 below |

## 4. (b′) Statement and hypothesis disagreements found by reading

1. **`lem-4.8` — one real disagreement, and it must be settled before T4 formalises.** The canonical
   statement bounds $\sqrt{\sum_j m_jd_j^2}\le\text{weighted}$; mine bounded
   $\sum_jm_jd_j^2\le\text{weighted}$. The two differ by a square root, and §4.4's subsequent use
   (Lemma 4.9's `arc`/`weighted` budget) uses one of them. Canonical also states the direction of
   $q_d$ explicitly ($q_d\ge \mathrm{slack}/m_i$, an *upper* bound, which is the valid direction since
   $\mathrm{arc}$ is increasing); mine wrote $=$. Recommendation: keep canonical's $q_d$ direction and
   settle the weighted bound against p. 26–27.
2. **`lem-3.7` / `eq-3.24`.** Canonical: $E_r^2=e_{\mathrm{off}}^2+63h^4+p^2$,
   $63=(\sqrt6\sqrt{42}/2)^2$. Correct, and my earlier doubt was wrong (§0c). What survives is a
   **transcription hazard** for T3/T4: `.scratch/mub6.txt` renders this display as `sqrt6*42/2` with
   the radical's extent lost and the power of $h$ inconsistent. Radicals must be read from the PDF.
3. **`lem-2.6`.** Canonical adds the tuple condition $a\le l-d+1$ and
   $a/N\le x_1\le x_5-x_4\le(l+1-d)/N$. Mine is a strict subset, so canonical wins — and the extra
   condition is precisely what decides which filter binds at $N=112$, i.e. T5's question.
4. **`lem-3.2`.** Canonical inlines $p=\sqrt{q/(6+\sqrt6-q)}$ and flags that (3.11) needs care in
   transcription; mine deferred to the paper's number. Canonical wins.
5. **`prop-6.9` / my I5, narrowed.** Canonical's hypothesis list already contains "a completed negative
   Stage C result (not a cap, not a failure)", so the *cap* half of my I5 is covered. What remains is
   the **clustering half**: the proof assumes no genuine vector's bin path was lost in clustering, and
   no hypothesis says so. That half stands; it is worth one clause.
6. **`lem-4.9` / my I4, sharpened rather than answered.** Canonical states the unit ("in cycles")
   explicitly — good — which is what makes the cycle/radian question a real question: (4.30) and
   Lemma 4.10 add $\|\varepsilon\|$ to radian-scale quantities. I4 stands and now needs an answer, not
   a definition.
7. **`cor-1.3`.** Canonical's wording ("closed under one and the same standard adjoint", "and three is
   attained") is sharper than mine. Canonical wins.

## 5. (c) S-claim dispositions: my 16 entries against the canonical 40-row ledger

Agreements (11 of 16, and they are the load-bearing ones): `prop-4.6`↔`S-Root-1` (CHECK),
`lem-5.4`↔`S-B-3` (CHECK), `prop-6.9`↔`S-C-5` (HYPOTHESIS), terminal conditions↔`S-7-2`
(HYPOTHESIS), `lem-6.4`↔`S-C-3` (CHECK), margins↔`margin-a.12`/`app-a4-a11` (CHECK),
`lem-A.1`/`A.2`↔`OBSOLETE`, `prop-2.10`'s mathematical half↔`S-seed-5` (SPLIT → T2+T3).
Differences, all five worth recording:

1. **`prop-2.10`: mine was too coarse.** The canonical ledger splits it into six rows of which two
   (`S-seed-1`, `S-seed-2`) are resolved by *deletion* — the choice of selected position and the
   direction set are immaterial because the lemmas are quantified over all choices. That is better
   than my "split + evaluate": it removes two checks instead of performing them.
2. **`lem-4.9`/`eq-4.20`: mine said hypothesis + formalise; canonical says CHECK (`S-Root-2`:
   $\mathrm{mag}_j>.15$, chord $<10^{-7}$, slack).** Canonical is stronger — adopt; my I4 then becomes
   a question about the number, not about its status.
3. **`lem-A.3`: mine said "replace or hypothesis"; canonical says CHECK (`S-Root-6`: smaller of
   (max abs row sum $+10^{-10}$) and ($\|G^2\|_F+2\cdot10^{-7}$)).** Canonical is stronger — adopt.
4. **`cor-5.8`: mine said "evaluate the file-level completeness"; canonical says HYPOTHESIS
   (`S-B-6`, batch writer).** Not a conflict but a division of labour: *assume* the writer is atomic
   (HYPOTHESIS) and *check* the contents (T2 provenance). Both rows should stand.
5. **`lem-6.8`: mine said "checker witness (DRAT or structural characterisation)"; canonical says
   FORMALISE (`S-C-4`).** A live fork that needs a lead decision: formalising the enumeration argument
   (T4) versus certifying each negative clique answer by witness (T2). `plan.md` P2.4 already names
   both routes; the inventory should not carry two dispositions for one claim.
6. **The one genuine gap in the frozen ledger.** There is **no row** for the premise that
   `prop-3.11`, `prop-4.16` and `prop-5.7` all assume: *the recursion / refinement ends with zero
   unresolved cells, no failed seed and no failed parent*. `S-A-6` records that a failed frame check
   leaves a seed unresolved "never excluded", and `S-7-2` covers the file-level terminal conditions,
   but no row asserts the absence of unresolved regions at the end. Three C-claims depend on it, so
   the contract needs three named premises. This is the cheapest high-value fix in the whole
   reconciliation, and it is the residue of my I5/I6 that the canonical file does not already carry.

## 6. Defects in the canonical files, with paste-ready fixes

**D1 — `lem-4.11` and `lem-4.12` are orphans (no in-edges), yet `lem-4.10`'s proof invokes them.**
The paper uses Lemma 4.11 twice ("with $\beta=.45$", "with $\beta=.8$") inside 4.10's bounds. Fix:
`lem-4.10: depends_on += [lem-4.11, lem-4.12]` (or route the ellipsoid bound through `covercompute`;
the use is in 4.10 and in `root-suff`).

**D2 — `flow-7.2` is tagged `E` (observed datum) but describes a specification.** `E` belongs to
`run-7.5` and `hashes-7.5`. Fix: `status: S` (or add a `spec` tag used for control flow only), and keep
the five terminal conditions where they already are, in `S-7-2`/the theorem contract.

**D3 — the three missing termination premises of §5(6).** Three rows: `H-A-term` (every seed processed,
none left failed or unresolved), `H-B-term` (every parent completed, none left unresolved),
`H-C-term` (no cap hit in any test that contributed to a negative result — partially covered by
`S-C-5`, make the pointer explicit). Owner T8; they print in Theorem 7.1's contract.

**D4 — document the display-node convention in the header.** In the canonical graph `eq-X` is a
*conclusion* of the claim that asserts it (`eq-3.24` ← `lem-3.7`); in mine it was a *premise*
(`lem-3.7` → `eq-3.24`). Both are acyclic; the canonical direction is the better one to freeze (later
claims cite the inequality without inheriting the lemma), but `depends_on` then means "uses or
concludes", which should be said once or the graph will be read wrongly downstream.

## 7. Verdict on the frozen inventory

81 of my 84 entries (96 %) are present in the canonical 91; of the 17 status disagreements, **16
resolve in the canonical file's favour and 1 (`flow-7.2`) is a defect in it**; across the 81 matched
pairs the canonical graph is a strict superset on 23 and mine on 9, and the 20 "different" cases are
granularity or the display convention of D4 — **no edge in either file is wrong**. The canonical
91-entry inventory is the right thing to freeze at G0. The five fixes above (D1–D4 and the three
premises) are the whole delta I would ask the lead to accept, plus the three statement items in §4
(`lem-4.8`'s square root, `flow-7.2`'s tag, `prop-6.9`'s clustering clause).

## 8. What survives from my work, and where it goes

* **I4** (epsilon in cycles added to radian norms, Lemma 4.10/(4.30)) — not in the canonical report;
  needs an answer before T8 writes. T2 + T5.
* **I5 narrowed** (Prop 6.9's clustering premise) — T8, one clause.
* **I6** (§7.2's five conditions are not derived from the stages' failure classes; §7.3's caps can
  convert an exclusion into a silent failure) — T2/T8.
* **I1** (the contract's "compiler conditions" has no definition in the paper; the run's build record
  in the source — `g++ 13.3.0 -O3 -march=native -ffp-contract=off`, per the canonical `S-7-1` row —
  is the only closed form available). Recommendation: import that record into `prem-arith` or delete
  the phrase. T8.
* **I8** (warning only): `results/proof-claims.md`'s top-level skeleton omits Props 3.11 and 4.6; do
  not quote it as the decomposition. The canonical graph has both.
* **Extraction hazard** (§4.2) and the **literature correction** (§0b) — T3/T4 and T7/T8 respectively.
* The notation and reader-path work is in the canonical directory already; my versions were removed
  so there is one interface.
