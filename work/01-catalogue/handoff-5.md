# handoff-5: executable reference model (m5)

from: m5 / direction d3
to: T2 checker, T5 parameters, T8 paper, T3 reference
version: 1
depends-on: nothing (reimplemented from `.scratch/mub6.txt`, no paper code used)
blocks: nothing hard
artefacts: `m5-refmodel/{mubref.py, run_checks.py, checks.json, REPORT.md}`
claims touched: Lem 1.2, 3.1, 3.2, 3.3, 3.4, 4.11, 4.12, 6.5; Sec 2.2-2.3 counts; Sec 3.1 (3.3),(3.7); Sec 3.2's q<.32; Sec A.4 arithmetic; Table 1's "151,744,086 pairs".
open questions: (i) what exactly is a "pair" in Table 1 — confirm against the archive (F3); (ii) which conjugation convention Lemma 3.1's M carries (F2); (iii) is Lemma 3.1's `ker M*` a slip for `ker M^T` = `ker B0` (F2).

## What was done

An independent Python reimplementation of the paper's exact analytic core plus 30
checks of the form "the paper says this inequality holds for all x in this set".
Run with `cd m5-refmodel && python3 run_checks.py` (6 s, deterministic). All 30
pass. Test data for the Stage-A checks: exact Fourier-family Hadamards at full
seed-ball displacement `r_s = .0320001`.

## Three things for other teams

1. **F1 (T8, T1).** Extraction hazard, not a paper defect: `.scratch/mub6.txt`
   renders Lemma 3.4's `(√42/2) h²` as "42√2/2 h²" because the superscript of `h²`
   lands on the numerator line. The PDF (page 15) and the proof agree on
   `√42/2 = 3.24`; measured 2.98 h², so the constant is sharp. Re-anchor every
   display containing `h²`, `Rs²`, `m²` on the PDF before quoting it.
2. **F2 (T8).** Lemma 3.1 says `range K = ker M*`; (3.5) says `ran K_B = ker B0`
   with `B0 = Mᵀ`. These are conjugate subspaces for complex `M`, and (3.4) is
   `M(M*M)⁻¹ = (M*)^+` while (3.5) needs `B0*(B0B0*)⁻¹ = (Mᵀ)^+`. One sentence on
   which row is conjugated fixes reproducibility of the stored frames.
3. **F3 (T2, T5).** The x-bin index space is exactly 85,349,292 tuples (of
   160,389,488 weakly increasing 5-tuples, cut by `(2.7)`), with 6,913,340 y-tuples
   per x. Table 1's 151,744,086 "pairs" is therefore 1.78 y-pairs per x — a very
   strong statement about the filter chain that the text does not define. Confirm
   from the archive or define "pair" in T8.

Confirmations worth recording in the paper: (3.8) is an exact identity (2.9e-14);
(3.9) holds with 1.7x slack; (3.11) with 2.8x; max q = 0.2411 < .32 at the ball
boundary; the frame threshold `m > 1.239` gives `q ≤ .3037`; the U(2) bins count
`8·4·16·16 = 8192` and tile exactly; Lemma 6.5's `s < .1` gives `20/7 > √6` with
17% margin; Lemma 4.11 is tight at its threshold (`x*G⁺x = 0.9999999`).
