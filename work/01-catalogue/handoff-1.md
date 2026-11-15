# handoff-1 — T1 catalogue → T2 checker, T4 lean, T8 paper

```
from:        T1 catalogue (G0)
to:          T2 checker, T4 lean, T8 paper (T3, T5, T6, T7 read-only consumers)
version:     1.0 (frozen at G0)
depends-on:  results/proof-claims.md, results/code-audit.md, .scratch/mub6.txt
blocks:      T2 cert-format.md (I1, I11), T4's assembly statements (I8), T8's theorem statement (I2)
artefacts:   work/01-catalogue/{claims.yaml, dependencies.dot, notation.tex, style.md, reader-path.md,
             reports/T1-report.md, changerequests/README.md}
claims touched: all 86; the ones that matter for the interface are listed below
open questions: see reports/T1-report.md §4 (I2 and I8 are the two that change a statement)
```

## The four things to take from here, and nothing else

1. **Ids.** Every claim you state, implement or check carries its `claims.yaml` id. No new claims in
   downstream artefacts without a change request.
2. **Statements.** `one_line_statement` is written in explicit quantifier form and is what you translate.
   Do not re-derive the statement from the paper's prose; if the two differ, that is a CR.
3. **Names.** `notation.tex` is the only source of symbols. In particular: the seven Root constants are
   always `(C, n0, id, ort, hor, mnorm, froot)`; `D^{cmp}` is the comparison block, `D̂(t)` the computed
   Stage-B function, `D^{ub}` the scalar bound of Proposition 5.2; `n_P(s)` is a bound, `m_B, m_C, m`
   are singular bounds, `ṁ_j = |D_j|`, `m` bold is the integer lift; `ε` is the centre correction in
   cycles, `ε_exp = 6·10⁻¹⁴`; `N_grid = 112`, `N` bold the integer lift matrix. Radii in cycles,
   angles in radians, and every constant printed with its unit.
4. **Dispositions.** `reports/T1-report.md` §3 gives each statement-about-code its disposition
   (E evaluate / F formalise / H prove by hand / P promote to hypothesis / R report only). Your work
   order is that table.

## Specific asks

**T2 (checker).** The certificate format must carry, per region, the witness of the claim that
disposes of it: for Stage A cells the direction `y` and both sides of (3.26)/(3.29); for Records the
seven constants, the frame `T`, and — beyond the paper's 356+288k-byte layout (report I11) — `q_d`,
`slack`, `Φ`, `N`, and the Stage-B `ℓ` with its stored `D̂(ℓ)` evaluation (`eq-5.17`); for Stage-C
records the vector-ball centres and radii plus the `O`/`U` adjacency sets and the clique witness
(`lem-6.8`, report §3.5). Start with `prop-4.6` (`buildH::patch`): it is the one claim whose failure
makes every other certificate vacuous, and it is checkable directly from a stored Root.

**T4 (lean).** Five assembly implications, in this order: `prop-3.11`, `prop-2.10`, `prop-4.16`,
`prop-5.7`/`cor-5.8`, `prop-6.9`, then `thm-7.1`. State coverage **per exact matrix**, not per
equivalence class (report I8), and state Stage B's blocker induction with the "already completed
parent" order hypothesis explicit (`prop-5.7`). Lemma 6.5's numerical chain needs the rational `22/7`,
not a decimal. `eq-4.17` should become a named lemma (it is used inside every merge and never isolated).

**T8 (paper).** Write the narrative from `reader-path.md` (it is 6 pp. and has the `[c:…]` pointers),
apply `style.md` mechanically, and take the theorem's hypothesis from the P-dispositions of
`reports/T1-report.md` §3: `prop-4.6` (Root builder), `eq-5.17` (computed distance function),
`lem-6.8` (clique search exhaustiveness), plus the arithmetic premise. Those four are the air; naming
them costs four sentences and makes the rest of the paper checkable.

## What T1 will not do after G0

Edit `claims.yaml`, `notation.tex`, `style.md`, `reader-path.md` or `dependencies.dot`. Accepted change
requests are folded in by the lead at the next gate. An item you think is a defect goes to
`work/01-catalogue/changerequests/<team>.md` using the header in `changerequests/README.md`.
