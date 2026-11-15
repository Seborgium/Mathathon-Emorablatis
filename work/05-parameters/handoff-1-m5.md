# handoff-1

- **from**: T5 (swarm smwgrqwth, member m5)
- **to**: T8 (the paper)
- **version**: 1, from `work/05-parameters/justification.md` + `N112.md`
- **depends-on**: PDF §2.2–2.4, §3.3, §3.7, §4.2–4.8, §5.2–5.6, §6.1–6.3, §7.2–7.5, A.3, A.10,
  A.12; `results/code-audit.md` F2/F3/F4 (all three confirmed below, one sharpened, one corrected)
- **blocks**: nothing; the numbers here can be pasted without further work
- **artefacts**: `justification.md` (table), `N112.md` (bin count), `experiments/*.py` (every number),
  `data/*.csv` (the tables)
- **claims touched**: the §7.3 storage claim (`int8_t`), the §2.3 enumeration count, the §2.4 reuse
  threshold, the §5.6 `k≤10` allowance, the §6.3 clustering cutoff, A.8's sentinel, A.12's margin
  table
- **open questions**: (1) what "pair" means in Table 1 (see §6 below); (2) the semantics of
  `levels=3, iters=2, first=1`; (3) the per-seed maxima of nodes/Roots/clusters/depth, which the
  paper never reports and which four of the nine caps need

Everything below is written to be pasted. Numbers come from the scripts named in brackets.

---

## 1. Replace the sentence that justifies $N=112$ (§2.2, first line of the bin discussion)

**Delete**: "The former bound is below the signed 32-bit limit."

**Insert** (after (2.6)):

> Three bounds fix $N$, and only the last is a choice. A bin of nine seed phases has circumradius
> $\sqrt9/(2N)=3/(2N)$, which must fit the radius $0.032$ of the balls of Proposition 2.10, so
> $N\ge47$. Bin differences are stored in `int8_t` and lie in $[-(N-1),N-1]$, so $N\le128$. The
> 32-bit bound $C(N+4,5)<2^{31}$ permits $N\le189$ and is therefore not binding. Within $[47,128]$
> the resolution trades enumeration against reuse: a bin is assimilated into an existing centre only
> if the whole bin fits inside the ball, so reuse requires
> $R-3/(2N)\ge1/N$, i.e. $N\ge79$, and below that every admissible pair becomes a seed. We take
> $N=112$, which is two-thirds of the way up the admissible window and within $6\%$ of the modelled
> cost optimum near $N=120$ (Appendix, Table 2). [n112.py]

Then add a short appendix table (new Table 2) with columns
$N$, $C(N+4,5)$, $3/(2N)$, $R-3/(2N)$, modelled retained centres, modelled wall time, ratio to
$N=112$: the rows of `data/m5-cost-curve-N.csv`. One sentence after it: "the centre counts are a model
calibrated on the measured $151{,}744{,}086\to249{,}878$ of §7.5, not a second measurement."

## 2. §2.4, the reuse threshold

**Insert** after the definition of the radius-$0.032$ test:

> The comparison value is $(\mathrm{fl}(.032N))^2-10^{-4}$. The $10^{-4}$ is not a rounding margin:
> the pre-subtraction error is below $10^{-12}$ (A.3), so it is $10^8$ times larger than needed, and
> in radius it buys $10^{-4}/(2\cdot112\cdot.032)=1.4\cdot10^{-5}$ cycles. Its role is to be a
> *squared-radius* slack, deliberately larger than the $8.0\cdot10^{-5}$ that the enlargement
> $0.032\to0.0320001$ would consume in the same units, so that no change of the two can make the
> test pass on a pair it should reject. [margins.py]

## 3. §3.7 and §4.7: why $N_u=16$ and why the targets are $.103$ and $.125$

**Insert** at the end of the base-grid paragraph (§3.7):

> The grid is not free. A cell of width $1/N_u$ in cycles has circumradius $1/N_u$, and no ball
> certifying a cell can be smaller, so $1/N_u\le.103$ is necessary: $N_u\ge10$, and $N_u\ge12$ given
> the divisibility $4\mid N_u$ of Lemma 3.3. The base grid $N_u=16$ leaves a factor $1.65$. At
> $N_u=8$ no cell could ever be covered. [margins.py]

**Insert** after the atlas radius cap (§4.7):

> The two targets satisfy $1/N_u=.0625\le.103<.125\le\tau_{\max}=.126$: the local target must be at
> least a cell circumradius and at most the atlas cap, and the atlas cap must be at most the largest
> refinement cap, since Stage B receives atlas records with their stored radius
> ($.125\le.126$, the $.126$ of §5.6). The chain has $0.96\%$ slack at its top and is the reason the
> two targets are not interchangeable.

## 4. §5.2/§5.6: the twenty-five trials and the $(\tau,w)$ ladder

**Insert** after the definition of $L$ in §5.3:

> Two inequalities pin the width. The grid contains $[-E,E]$ exactly when
> $(L+\tfrac12)w\ge E$, which holds with ratios $1.20$, $1.11$, $1.31$ for the three passes. And by
> Lemma 5.5 a child box of half-width $w/2$ in $k$ coordinates over-estimates the tangent radius by
> at most $\sqrt k\,w/2$, so a pass with cap $\tau$ certifies children only up to
> $\tau-\sqrt k\,w/2$; at $k=5$ the slack is $4.8$, $2.9$, $2.6$. A width comparable to $\tau$ would
> leave nothing certifiable, which is why $w<\tau$ is not an aesthetic preference.
> [margins.py]

**Insert** after (5.19):

> Twenty-five halvings of the bracket $[0,1.01a]$, $a\le.126$, leave an interval of
> $3.8\cdot10^{-9}$, while a usable threshold requires $\rho>10^{-7}$; the number of trials needed
> is $\lceil\log_2(1.01\cdot.126/10^{-7})\rceil=21$. The margin is therefore $16\times$, and a
> reduction to 13 trials would refuse every threshold silently. [margins.py]

**Replace** the stated range "0 ≤ k ≤ 10" (§5.6) by:

> The stored Root dimension satisfies $k\le5$ in passes 1–2 and $k\le7$ in pass 3. These are not
> design choices: with $L=11,15,5$ the per-axis box counts are $23,31,11$, and the
> $50{,}000{,}000$-box cap admits $23^5$, $31^5$ and $11^7$ but not $23^6$, $31^6$ or $11^8$
> ($23^6=1.48\cdot10^8$, $31^6=8.88\cdot10^8$). The bound $k\le10$ is the guard in `buildH::patch`,
> not a reachable dimension, and the observed $k$ must satisfy $k\le5$ since the run reports no bad
> parent. Report the histogram of $k$. [caps.py]

At the same place:

> The depth cap of six is reachable only for $k\le4$: a fully split tree has
> $\sum_{j\le6}2^{jk}$ boxes, which is $1.79\cdot10^7$ at $k=4$ but $1.11\cdot10^9$ at $k=5$, above
> the box cap. [caps.py]

## 5. §6.3: the clustering cutoff (F2) — one sentence and one formula

**Replace** "(.042 − 1.11 w)²" by

$$\Bigl(\max\bigl(0,\ .042-\tfrac{\sqrt{29/6}}{2M}\bigr)\Bigr)^{2}$$

and add:

> The squared form matters. Since $1.11/M$ bounds $X_M=\frac{\sqrt{29/6}}{2M}$, the base
> $.042-1.11/M$ is negative for $M\le26$, and squaring turns the cutoff into an absolute value:
> the effective radius is $.0505,.0042,.0189,.0304$ at $M=12,24,48,96$, i.e. non-monotone in the
> grid. The consequence is stronger than a wasted heuristic: distinct bin midpoints are $1/M$ apart,
> so a merge is impossible for every $M\le50$ — including all three of the coarsest recorded grids
> — and the single-vector compression rests entirely on $M=96$. With the corrected form the cutoff
> is monotone non-decreasing in $M$, is zero for $M\le26$ (correctly: those bins are too coarse to
> fit), and still admits a radius of $.0306$ at $M=96$, i.e. $2.9$ lattice steps. Alternatively
> delete the cutoff and let the recomputed radii carry the covering property of Lemma 6.4: the
> radius recomputation, not the cutoff, is what the lemma uses. [stagec.py]

## 6. §7.3 and §7.5: three counts

**Insert** in §7.3, after the two tuple bounds:

> Three counts should be distinguished, and only the first is currently stated: the number of X
> tuples offered to the filters, $C(116,5)=160{,}389{,}488$; the number surviving them, at most
> $85{,}349{,}292$ because the orientation filter (2.7) is integral and applies to every tuple
> ($16{,}197{,}157$ if the midpoint-gap filter (2.8) is also applied); and the number of matched
> $(X,Y)$ pairs handed to the reuse test. Table 1's "151,744,086 pairs" is $94.6\%$ of the
> pre-filter total and $1.78\times$ the post-filter maximum, so it is none of these and should be
> replaced by the three numbers. [seedcover.py]

## 7. A.3 and A.8: the sentinels (F4)

**Replace** in A.3 the sentence about the comparison radius by the same content with the two roles
of $10^{-4}$ separated (see insert 2 above), and in A.8:

> The certified spectral bound satisfies $gu\le100.1$, so the value $100$ is *not* a distinguishable
> failure marker: a valid bound can equal it. The same holds for the sentinel $10$ of `bootstrap`
> and `relationB::eval`, which is excluded from the usable range only by the guards
> $0\le\mathrm{init}<3$, $C<20$ and $t<10$. Replace all three by a status flag or a checked NaN, so
> that no threshold in the neighbourhood can silently re-admit the sentinel as data.

## 8. A.12: add a ratio column

The margins table already lists error and margin; add the quotient. Recomputed `margins.py`:
median $200\times$, range $1.25\times$–$10^{6}\times$, tightest **Candidate external tangent error
$1.2\cdot10^{-4}$ vs $1.5\cdot10^{-4}$ rad ($1.25\times$)**, then A flat norm ($10\times$) and A
directional comparison ($25\times$). One sentence to add under the table:

> The ratios are deliberately uneven: the tightest is $1.25\times$ and the loosest $10^{6}\times$.
> The tight one is the tangent comparison, which is the quantity most sensitive to the local target
> $.103$ and to $K=1.00001$; a change to either should be re-checked against it.

## 9. Three things T8 must not print

1. Not "$\binom{116}{5}$ is below the 32-bit limit" as the reason for $N$ — the binding bound is
   `int8_t`, $N\le128$ (insert 1).
2. Not "$0\le k\le10$" as a range: $k\le5$ in passes 1–2, $k\le7$ in pass 3 (insert 4).
3. Not "$(.042-1.11w)^2$" without the $\max(0,\cdot)$: at $M\le26$ the sign is lost (insert 5).
