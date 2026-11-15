# handoff-1 (m3) — to T2 (checker) and T8 (paper): what must be printed differently

```
from:         m3 (T1, audit direction d2)
to:           T2 checker; T8 paper
version:      1 — 14 Nov 2026
depends-on:   reports/T1-audit-report.m3.md §§1–2; reports/sclaims.tsv; changerequests/T1-audit.md
blocks:       T2's Root test can start now; T2's joint test and T4's (6.8)/(4.29) statements cannot
artefacts:    reports/T1-audit-report.m3.md, reports/sclaims.tsv, changerequests/T1-audit.md
claims touched: lem-4.4, lem-3.7, lem-4.10, lem-2.7, lem-2.9, (6.8), (6.10), (6.22), prop-4.6, prop-6.9
```

The first two items change a *statement*, so they must be settled before T2 implements a test or T4
writes a Lean statement. Item 7 is a warning about reading the paper at all.

1. **(6.8) needs a conjugate.** The paper prints $J_{ij}=-\operatorname{Im}(S_iq_{ji})$ and then
   asserts $\sum_jJ_{ij}=0$; with $\sum_jq_{ji}=S_i$ that is $-\operatorname{Im}(S_i^2)$, not zero.
   $J_{ij}=-\operatorname{Im}(\overline{S_i}q_{ji})$ gives the identity and is what the expansion of
   $|S'_i|^2$ produces. T2: implement the conjugated form; do not test the row sum against the
   printed one. T8: print the bar. No numerical value changes downstream.
2. **Two different $S$ in §6.** (6.5) $S_i=\sum_je(u_j-P_{ji})/\sqrt6$, $|S'_i|=1$; (6.15)
   $S=\sum_je(u_j-v_j)$, $|S'|=\sqrt6$. A checker or Lean statement carrying one $S$ across §6.2→§6.4
   is wrong by $\sqrt6$. T2: two code paths, two names. T8: $S^{[1]},S^{[2]}$.
3. **Prop 4.6 is not a code claim in the new pipeline.** The record stores
   $(P,T,M,C,n_0,id,ort,hor,\text{mnorm},\text{froot})$; the checker verifies (4.4) and (4.15) from
   the stored data in interval arithmetic; Prop 4.5 applies verbatim. T2: implement this first — it
   is a finite arithmetic check and it retires the paper's heaviest `S`-claim (`code-audit.md` F1).
   Field list = (A.16) plus $r$.
4. **(4.29)'s $S_\Delta/\pi$ is inside the radical** (character coordinates on p. 28; the code's
   `s0` computes it inside). T4 and T2 must state it inside; it is *not* outside as the extraction
   suggests. Rejecting it as "false" would be an error caused by the text file.
5. **(6.22)'s $Xr$ coefficient.** (6.10) and (A.24) give $2/\sqrt6$; the printed (6.22) is ambiguous.
   T2: implement $2/\sqrt6$. T8: typeset it explicitly. A factor 2 here sits at the $2\cdot10^{-7}$
   margin.
6. **Stage C's radius range is a hypothesis.** §6.1 needs $0\le r\le.03$; §5.6 admits $\tau\le.126$;
   only the $.016$ and $.011$ passes qualify and §7.2 confirms C reads the $.016$ batches. T2:
   reject records with $r>.03$ at Stage C input. T8: state it in Theorem 7.1.
7. **Reading the paper's formulas.** In `.scratch/mub6.txt` a radical or the numerator of a stacked
   fraction is lifted onto the preceding text line, so `b = 8‖M‖` there is $b=\sqrt8\|M\|$, and
   (6.22)/(6.16)/(6.5) show the same effect. Four errors in the current restatements come from this
   (CR-T1A-1, -2, -3, -7). When a constant looks wrong by a factor, check the line above before
   concluding the paper is wrong; `pdftotext -bbox-layout -f N -l N` settles it by coordinates.

Two notes for T2's `inequalities.md`: (6.3)'s constant is $\sqrt2\pi/3$, not $2\pi^2/6$, and
$K=1.00001$ follows from $f_0<10^{-6}$ with three orders to spare; and (3.24)'s fourth-order
coefficient is $63$, not $2646$. And one for T8's certificate definition: see Q5 of
`reports/T1-audit-report.m3.md` §5.
