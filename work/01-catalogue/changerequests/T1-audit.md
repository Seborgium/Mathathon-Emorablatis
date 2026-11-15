# Change requests from the audit (m3, direction d2) to the catalogue owner

Filed at 19:35, after claims.yaml v1 (19:18). Items 1–4 are **blocking**: each is a statement that
would be formalised (T4) or implemented (T2) in a form stronger than, or false as, printed.
Evidence and reasoning: `reports/T1-audit-report.m3.md` §1. Page numbers below are the paper's **printed**
page numbers (the number in the footer), i.e. PDF page minus one.

### CR-T1A-1  lem-4.4  [blocking]
- wanted: `b = sqrt(8) * ||M||` and `b = sqrt(6) * ||S||` (currently `8 ||M||`, `6 ||S||`).
- why: Cauchy–Schwarz over edges gives `sum w_ij a_ij <= (sum w_ij^2)^{1/2} (sum a_ij^2)^{1/2}
  <= ||M|| * sqrt(8) * ||x||^2`; the paper's radicals sit on the line above the display; and §A.5
  states the resulting constant as `pi*sqrt(8)*mnorm`.
- evidence: p. 23 (display), §A.5 p. 62 (`C^ = pi sqrt8 mnorm + 1e-7`).
- if refused: T4 will state `C <= 8 pi ||M||`, which contradicts §A.5's acceptance check `C < 20`
  whenever `mnorm > 0.8`, so the first of the two C-candidates becomes unusable for no reason.

### CR-T1A-2  lem-3.7 / eq-3.24  [blocking]
- wanted: `E_r^2 = e_off^2 + 63 h^4 + p^2`, i.e. the coefficient is `(sqrt6 * sqrt42 / 2)^2 = 252/4`.
- why: the proof's last line is `p + sqrt6 * (sqrt42/2) h^2`; §A.4's field `E_3 = (1/2) sqrt(252) h^2
  + pol` is the same number. `(sqrt6*42)/2` overstates the term by a factor 42.
- evidence: p. 19 (proof), §A.4 p. 60 (`E_3`), Lemma 3.4 (3.14).
- if refused: harmless as an upper bound but a mismatch with the paper and with T4's statement.

### CR-T1A-3  lem-4.10 / (4.29)  [blocking]
- wanted: `S_Delta / pi` **inside** the radical:
  `||delta|| <= ( ||Delta||^2 + (R_s^2+arc^2)/(2 pi)^2 + S_Delta/pi )^{1/2} + ||epsilon||`.
- why: character coordinates on p. 28 put the closing delimiter at x=358.29, after `S_Delta/pi`
  (x=342–356) and before the exponent 1/2 (x=366); and `covercompute::value` computes
  `sqrt(nd + d2 + (supp+.0001)/pi + 1e-5)`, i.e. inside. With the term outside, the bound is
  smaller than the exact worst case `sqrt(||Delta||^2 + b^2 + S_Delta/pi)` in the operating range.
- evidence: p. 28 (display), §4.5 p. 28 (covercompute paragraph).
- if refused: T4 would formalise a false inequality; T2 would accept certificates the paper's own
  code would reject.

### CR-T1A-4  missing ids  [blocking for T2]
- wanted: entries for (4.5), (4.6), (4.7), (4.15), (6.2) and (A.16). Proposed ids and texts are in
  `handoff-2.md` §1 (`root-disp-n`, `root-disp-s`, `root-diff`, `root-suff`, `stageC-iface`,
  `patch-out`).
- why: (4.5)–(4.7) are the *content* of Def 4.1; (4.15) is the checker's Root test; (6.2) is the
  only place §6 depends on §4; (A.16) is the checkable form of Prop 4.6. Without ids, T2's
  `inequalities.md` cannot cite the claim it implements and G0's "every claim has an id" is
  satisfied only on paper.
- evidence: claims.yaml v1 ids list; `reports/T1-audit-report.m3.md` §4.2.
- if refused: T2 cites `def-4.1` and `prop-4.6` for three distinct inequalities each.

### CR-T1A-5  (6.8)  [non-blocking]
- wanted: wherever `J_ij` is defined, use `J_ij = -Im(conj(S_i) q_ji)` and note that the paper
  prints `-Im(S_i q_ji)`, which contradicts its own next line `sum_j J_ij = 0`.
- why: `sum_j q_ji = S_i`, so `sum_j -Im(S_i q_ji) = -Im(S_i^2) ≠ 0` in general.
- evidence: p. 42, (6.8) and the sentence after it; derivation in `reports/T1-audit-report.m3.md` §2 I1.
- if refused: a Lean statement of (6.8) will not typecheck against the row-sum lemma it is used
  with.

### CR-T1A-6  header `page_convention` and `paper` fields  [non-blocking, but affects every evidence string]
- wanted: "printed page number = PDF page number (the title page is PDF 1 and carries no footer);
  the PDF has 76 pages, not 77".
- why: the header currently says "77 pages" and "printed page number is N-1". Both are wrong.
  Verified: `pdfinfo` reports 76 pages, and `pdftotext -f 21|22|23 -l ...` shows the footers 21,
  22, 23 on PDF pages 21, 22, 23. The citations themselves are right; only the convention note is
  wrong, and a reader who trusts it will look one page early everywhere.
- evidence: pdfinfo; pdftotext -f 21 -l 23.
- if refused: every evidence string in claims.yaml and every cross-team citation inherits a
  documented one-page offset that is not real.

### CR-T1A-7  lem-2.7  [non-blocking]
- wanted: `u in R^5, Delta in R^5` (currently `R^6`), with the index range `j = 0..4`.
- why: §2.3 defines u = (u_0,...,u_4) as the five varying midpoints (the sixth entry of the phase
  list is the fixed 0), and Lemma 2.7's hypothesis sums j = 0..4. J is therefore 2x5 realified and
  J_h in (2.12) is 5x5, which is what (2.13)-(2.14) and Lemma 2.9's J_* in R^{4x9} use.
- evidence: §2.3 p. 9, (2.9); Lemma 2.7 p. 10.
- if refused: T4 states Lemma 2.7 over R^6 and cannot apply (2.13).

### CR-T1A-8  lem-2.9 / (2.18)  [non-blocking]
- wanted: "(2.18): `2 k.h <= sum_{j=0}^{8} |k_j|`". The entry currently prints
  `2k.h <= 2k.h + sum_j |k_j|`, which is a tautology and loses the only content of (2.18).
- why: (2.18) is the coordinate bound sum_j 2k_j h_j <= sum_j |k_j| with |h_j| <= 1/2.
- evidence: Lemma 2.9 p. 11, (2.18).
- if refused: T2's reuse test and T4's statement lose the simpler of the two support bounds.

### CR-T1A-9  (6.22) has no id  [non-blocking, T2 input]
- wanted: an entry `eq-6.22` for E_t^ball (the Stage-C joint bound), with the coefficient of the
  `X r` term printed as `2/sqrt6` (as in (6.10) and (A.24)).
- why: (6.22) is the quantity `graph::joint` evaluates and the object Lemma 6.7 consumes; it is
  currently named only inside lem-6.7's evidence. The layout of the printed (6.22) is ambiguous
  about the factor 2, and a formaliser needs it settled.
- evidence: §6.5 p. 46; (6.10) p. 42; (A.24) p. 71.
- if refused: T2 has no id to cite for the inequality it implements, and T4 has no statement of
  the bound the joint test uses.
