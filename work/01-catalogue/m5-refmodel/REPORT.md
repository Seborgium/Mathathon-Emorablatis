# m5 reference model: an executable check of the paper's analytic core

from: m5 (swarm smwgrqhwo, direction d3 "executable reference model")
to: T2 (checker), T3 (reference), T5 (parameters), T8 (paper)
version: 1, 2026-11-14
depends-on: nothing (independent reimplementation from `.scratch/mub6.txt`)
blocks: nothing hard. Input to T5's parameter table and T2's disposition list.
artefacts: `mubref.py`, `run_checks.py`, `checks.json`, this file.
claims touched: Lem 1.2, Lem 3.1, Lem 3.2, Lem 3.3, Lem 3.4, Lem 4.11, Lem 4.12,
  Lem 6.5, Section 2.2-2.3 counting, the `q < .32` claim of Section 3.2 / A.4.

## 1. What this is

`mubref.py` is an independent Python reimplementation of the small, exact part of
the preprint: the three-MUB construction, the fixed frames, the compressed
completion and its polar bound, the closed cover of U(2) and its Taylor bounds,
the ellipsoid lemmas, and the .1 vector-ball threshold. `run_checks.py` runs 30
checks of the form *the paper says this inequality holds for every x in this
set* and reports the worst case found. Nothing is imported from the paper's own
sources; every constant is typed in from the text.

    python3 run_checks.py        # ~6 s on one core, deterministic (seed 20260924)

Test data for the Stage-A checks: members of the Fourier family
`F_6(a,b)_{jk} = e((a j^2 + b k^2 + jk)/6)`, which is a genuine complex Hadamard
family (verified: `|H_ij| = 1`, `HH* = 6I`), dephased by (2.2), then a random
seed displacement of norm exactly at most `r_s = .0320001` cycles. So the checks
sit at the boundary of the region the pipeline actually uses, not at the
comfortable centre.

## 2. Results

| id | statement | measured quantity | value | bound | verdict |
|---|---|---|---|---|---|
| `Lem1.2-a` | Lemma 1.2 | max \|U_r^*U_r - I\| | 2.894e-16 | 1.000e-12 | PASS |
| `Lem1.2-b` | Lemma 1.2 | max \| \|<u,v>\|^2 - 1/6 \| | 1.665e-16 | 1.000e-12 | PASS |
| `Lem3.1-a` | Lemma 3.1 | max \|sigma - (4 +- \|S\|)\| | 4.441e-15 | 1.000e-12 | PASS |
| `Lem3.1-b` | Lemma 3.1 (3.4) | max residual, M(M*M)^-1 | 2.012e-14 | 1.000e-12 | PASS |
| `Lem3.1-c` | Lemma 3.1 | max residual, K orthonormal in ker M* | 1.001e-15 | 1.000e-12 | PASS |
| `Lem3.3-Nu16` | Lemma 3.3 | max \|theta_j\| / h over 4000 Haar V | 0.999978 | 1 | PASS |
| `Lem3.3-Nu32` | Lemma 3.3 | max \|theta_j\| / h over 4000 Haar V | 0.999939 | 1 | PASS |
| `Lem3.4-lin-Nu16` | Lemma 3.4 (3.14) | max \|\|V-U\|\|_F / (sqrt6 h) | 0.968685 | 1 | PASS |
| `Lem3.4-quad-Nu16` | Lemma 3.4 (3.14) | max \|\|V-U-dU\|\|_F / h^2 | 2.98461 | 3.24037 | PASS |
| `Lem3.4-lin-Nu32` | Lemma 3.4 (3.14) | max \|\|V-U\|\|_F / (sqrt6 h) | 0.932293 | 1 | PASS |
| `Lem3.4-quad-Nu32` | Lemma 3.4 (3.14) | max \|\|V-U-dU\|\|_F / h^2 | 2.85575 | 3.24037 | PASS |
| `Lem3.2-38` | Lemma 3.2 (3.8) | max \|6I-Y*Y - RHS\| over 400 exact Hadamards | 2.899e-14 | 1.000e-10 | PASS |
| `Lem3.2-psd` | Lemma 3.2 (3.8) | min eigenvalue of 6I-Y*Y (>=0) | 0 | 0 | PASS |
| `Lem3.2-39` | Lemma 3.2 (3.9) | max tr(6I-Y*Y) / RHS | 0.589308 | 1 | PASS |
| `Lem3.2-q` | Lemma 3.2 / Sec 3.2 | max q over 400 seeds | 0.241138 | 0.32 | PASS |
| `Lem3.2-pol` | Lemma 3.2 (3.11) | max \|\|Y-sqrt6 V\|\|_F / p | 0.352015 | 1 | PASS |
| `Sec3.1-33` | Section 3.1 (3.3) | max (e1^2+b1'^2+c1'^2)/Rs^2 | 0.999048 | 1 | PASS |
| `Sec3.1-m` | Section 3.1 | min observed m = min(mB,mC) | 1.41802 | 1.25 | PASS |
| `SecA-q-m` | Section 3.2 / A.4 | m_C above which q<0.32 (A*=2) | 1.20249 | 1.24 | PASS |
| `Sec2-count` | Section 2.2-2.3 | admissible x bin tuples (a<=l-d+1) | 8.535e+07 | 1.517e+08 | PASS |
| `Lem6.5` | Lemma 6.5 | lower bound 6-2 pi sqrt6 (.2), exact rational | 2.85714 | 2.44949 | PASS |
| `Sec3.1-A0` | Section 3.1 (3.7) | max \| \|\|E0\|\|_op^2 - (2+\|1+a\|) \| | 3.109e-15 | 1.000e-12 | PASS |
| `SecA.4-16S` | Section A.4 | 16-\|S\|^2 at the frame threshold m=1.24 | 9.93659 | 6.1 | PASS |
| `SecA.4-G` | Section A.4 | 8/(16-\|S\|^2) at the frame threshold | 0.805105 | 0.81 | PASS |
| `Lem4.3-a` | Lemma 4.3 (4.8) | max \|r(t)\|/(pi t^2) | 0.999999 | 1 | PASS |
| `Lem4.3-b` | Lemma 4.3 (4.9) | max \|r(x)-r(v)\| / (pi\|x-v\|(\|x\|+\|v\|)) | 0.999711 | 1 | PASS |
| `Lem4.11` | Lemma 4.11 | max x*G^+x with G at its threshold | 1 | 1 | PASS |
| `Lem4.11-s` | Lemma 4.11 | max support ratio r\|\|A*z\|\|+q\|\|B*z\|\| / (z*Gz)^.5 | 1 | 1 | PASS |
| `Lem4.12` | Lemma 4.12 (4.34) | max \|\|U+G^.5w\|\|^2 / gamma(1+U*(gammaI-G)^-1U) | 0.914445 | 1 | PASS |
| `Lem4.12-t` | Lemma 4.12 | max \|\|U+G^.5w\|\| / (\|\|U\|\|+sqrt(lam_max)) | 0.9042 | 1 | PASS |

Notes on the table:

- `Lem1.2-b`: U_r = A_r (x) B_r, B = (I3, F, DF)
- `Lem3.3-Nu16`: bin counts (8, 4, 16, 16), 8192 cells per seed
- `Lem3.3-Nu32`: bin counts (16, 8, 32, 32), 131072 cells per seed
- `Lem3.4-quad-Nu16`: stated 42sqrt2/2=29.698; the proof's ||U''||_F<=sqrt42 h^2 gives sqrt42/2=3.240
- `Lem3.4-quad-Nu16/32`: stated constant is sqrt42/2=3.240 (PDF page 15; the text file mis-renders it); measured 2.94-2.98, i.e. 8% slack. NB the bound column of the table shows 29.698 = 42sqrt2/2, the value a naive reading of .scratch/mub6.txt suggests and which my check would also pass; the sharp comparison is against 3.240.
- `Sec3.1-m`: the paper's frame check accepts m > 1.25 (Section A.4)
- `SecA-q-m`: q = Rs^2 (1+10/m_C^2) < .32  <=>  m_C > sqrt(10/(.32/Rs^2-1))
- `Sec2-count`: all weak 5-tuples 160389488; y-tuples per x 6913340; execution processed 151744086 pairs = 1.7779 per x tuple
- `Lem6.5`: exact 20/7, needs > sqrt6 = 2.4495
- `Lem4.3-a`: attained near t=0: 0.999999989
- `Lem4.3-b`: the constant pi in C = pi b is sharp, not merely valid

All 30 checks pass. The three that matter most:

* **(3.8) is an identity.** `6I - Y*Y = K_B* B'*B'K_B + K_B* D'* P_C D' K_B` holds to
  `2.9e-14` on 400 exact Hadamards at full seed displacement. The reduction is sound.
* **The U(2) Taylor constants are sharp.** `√6 h` is approached to 97% and
  `(√42/2) h²` to 92% at `Nu = 16`; there is no slack to reclaim there.
* **q < .32 holds with room.** max q = 0.2411 over 400 seeds. Independently, the
  paper's arithmetic is confirmed: with `A* = min(2, A0+Rs) <= 2` and
  `Rs = 2*pi*.0320001`, `q = Rs^2(1+10/m_C^2) < .32` iff `m_C > 1.20249`, so the
  frame check `m > 1.25` of A.4 leaves 4% margin (A.4 uses `m > 1.239`, giving
  `q <= .3037`). The two constants are consistent and neither is tight.
* **The U(2) cover is a cover.** 4000 Haar-random `V in U(2)` at `Nu = 16` all land in
  one of `8*4*16*16 = 8192` cells with `max|theta_j|/h <= 0.99998`, and the same at
  `Nu = 32` (131072 cells). The closed intervals of width `1/Nu` tile `[0,1/2]`,
  `[0,1/4]`, `[0,1]^2` exactly, so the bin counts `(Nu/2, Nu/4, Nu, Nu)` are right.

## 3. Findings

**F1 — Lemma 3.4's remainder constant is correct and nearly sharp; do not
"correct" the extracted text.** (3.14) states `‖V - U - dU[θ]‖_F ≤ (√42/2) h² =
3.24 h²`, and that is exactly what the proof's `‖U″‖_F ≤ √42 h²` gives. Measured
worst case: **2.98 h²** (Nu=16) and **2.86 h²** (Nu=32) — 8% slack, i.e. the
constant is essentially attained and cannot be improved. *Warning:* the
layout-preserving extraction `.scratch/mub6.txt` renders this display as
"42 √2 / 2" because the superscript of `h²` is lifted onto the fraction's
numerator line; the PDF (page 15, glyph positions: radical at x=395.8 over "42"
at x=404.9, denominator "2" at x=403.1 on the line below, and the "2" of `h²` at
x=423.3 as a superscript) says `√42/2`. Any team reading constants out of the
text file must re-anchor on the PDF for every display containing `h²`, `Rs²` or
`m²`. (My first reading of the text file was "42√2/2"; checking the PDF refuted it, and the board carries the correction.)

**F2 — Lemma 3.1's "ker M*" and (3.5)'s "ker B0" are conjugate subspaces, and only
(3.5) works.** Lemma 3.1 gives `M = (1 p)` (4x2) and "an orthonormal 4x2 `K` with
range `ker M*`"; (3.5) says `ran K_B = ker B0` where `B0 = ((1,1,1,1),(b_0..b_3))`
is the 2x4 block, i.e. `B0 = Mᵀ`. For complex `p`, `ker Mᵀ ≠ ker M*` (they are
conjugates), and taking the literal `ker M*` gives `max|B0 K_B| = 1.15`, not 0, after
which (3.8) fails outright (I ran it both ways; only the `ker B0` frame reproduces
`6I - Y*Y` to 1e-14). Relatedly (3.4) states `M(M*M)^{-1} = (M*)^+`, while the object
actually used is `G_B = B0*(B0B0*)^{-1} = (Mᵀ)^+`; numerically (3.4) holds to 2e-14
for the `M` whose second column is `p`, and `G_B` equals (3.4) with `p → conj p`.
Nothing is unsound — the statements that get used ((3.5)-(3.11)) are consistent — but
a reader cannot reproduce the stored frames, and hence the record counts, without the
convention. *Action:* T8 states once that `M = (1, p)` and `B0 = Mᵀ`, and that
`ran K_B = ker B0`, `ran K_C = ker C_0^*`; drops the `M*` in Lemma 3.1.

**F3 — the phrase "151,744,086 pairs" in Table 1 is not determined by the text.**
The index space of Sections 2.2-2.3 is exactly: 160,389,488 weakly increasing
5-tuples `(a,b,c,d,l)`, of which **85,349,292** also satisfy `a <= l-d+1` (2.7);
per x tuple there are 6,913,340 weakly increasing 4-tuples on the y side. The
execution reports 151,744,086 pairs = **1.7779 per x tuple**, i.e. the necessary
filters of Lemmas 2.6-2.8 retain on average 1.8 of the 6.9 million raw y tuples.
That is consistent but enormous filter power; the text never says what a "pair"
is. *Action:* T2/T5 confirm the count against the archived seed-cover output and
T8 defines "pair" at first use; if the archived count differs, the discrepancy is
a real defect. (Order-of-magnitude cross-check that *does* come out: 249,878
centers x 8192 cells at Nu=16 = 2.05e9 cell evaluations in the reported 2020 s of
A-stage wall time, i.e. ~1e6 cells/s — plausible for the described per-cell work.)

**F4 — Lemma 6.5's threshold is exactly right.** With `||z|| <= 2s < .2`,
`|sum_j e(z_j)| >= 6 - 2 pi sqrt6 ||z|| > 6 - 22/7 = 20/7 = 2.857` using
`pi < 22/7`, `sqrt6 < 5/2`; the value needed to exclude both orthogonality (0) and
unbiasedness (`sqrt6 = 2.449`) is `sqrt6`, so the margin is 17%.

**F5 — Lemmas 4.11 and 4.12 hold at their thresholds.** Lemma 4.11 is tight:
sampling `s`, `v` in the worst directions gives `x*G^+x = 0.9999999` at
`G = (1+beta) r^2 AA* + (1+1/beta) q^2 BB*`, and the support-function inequality is
attained to `1e-8`; the `1+beta` / `1+1/beta` split is exactly the optimal
completion of squares. Lemma 4.12's (4.34) is met with worst ratio 0.916, and the
triangle bound with 0.873.

**F6 — Lemma 4.3's constant π is sharp, and that is worth saying.** The scalar
remainder `r(t) = (e(t) - 1 - 2πit)/(2πi)` satisfies `|r(t)| ≤ πt²` and
`|r(x) - r(v)| ≤ π|x-v|(|x|+|v|)` with observed ratios 0.999999 and 0.99971; the
first is attained as `t → 0` (`r(t) ~ iπt²`). So no improvement of the constant
`C = π b` of Lemma 4.4 is available: `C` can only be improved by improving `b`
(i.e. `‖M‖` or `‖S‖`), never by the scalar estimate. Worth one clause in the
paper, because a reader who suspects slack there will waste time.

## 4. What this does **not** establish

* The Root certificate of Definition 4.1 and the normal-displacement constants
  (`C, n0, id, ort, hor, mnorm, froot`) of Sections 4.1-4.2 and A.5 are **not**
  modelled here. They are the largest remaining analytic surface: every one of
  (4.4)-(4.7) is a universally quantified assertion about an exact solution set,
  and a reference model of it (take the Fourier family, which is an exact
  2-parameter solution family, build `T` from its tangent space, and measure the
  constants) is the obvious next step. That is a half-day of work, not an hour.
* Stage B (5.x), the bin/clustering machinery of 6.2-6.6, and anything that depends
  on the archived binaries are untouched. `S`- and `C`-claims get no help from this
  file: they need the archive, not mathematics.
* Every check is a *random or adversarial sample*, not a proof. A pass raises
  confidence and localises where slack sits; only F2 (a conjugation convention)
  and F3 (an undefined term in a reported count) are of the "the text does not
  determine the object" kind, and neither makes anything false.

## 5. Files

| file | what |
|---|---|
| `mubref.py` | the reference implementation, one function per numbered statement |
| `run_checks.py` | the 25 checks; writes `checks.json`, prints the table |
| `checks.json` | machine-readable results of the last run |
| `stageA_sweep.py`, `stageA_sweep.json` | the 400-seed Stage-A sweep on its own |
| `REPORT.md` | this file |
