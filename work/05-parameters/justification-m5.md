# Justification and sensitivity of every constant (T5)

Subject: *The maximum number of mutually unbiased bases in dimension six* (OpenAI, 24 Sep 2026).
Every number below is printed by a script in `experiments/`; the tables are in `data/*.csv`.
Nothing is quoted from the paper's prose without recomputation, and one number in
`results/plan.md` is corrected (row **N**, and see `N112.md` §5).

Scripts: `n112.py` (bin count and cost curve), `seedcover.py` (cover counts), `caps.py` (all nine
caps), `stagec.py` (F2), `margins.py` (everything else, including the closing table).

Status vocabulary: **justified** (the stated inequality is tight enough to explain the value),
**arbitrary-but-harmless** (the value is a free choice whose failure mode costs work, never
soundness), **needs change** (a defect: the value or its written form can mislead or can become
unsound if another constant moves).

---

## 1. The seed cover: $N$, $w$, $R$

| constant | where | the inequality that constrains it | value | slack | half / double | recommendation | status |
|---|---|---|---|---|---|---|---|
| $N$ (bins per axis) | §2.2 (2.6), §7.3 | $3/(2N)\le R$ (Prop. 2.10 circumradius) **and** $C(N+4,5)<2^{31}$ **and** $N-1\le127$ (int8 bin differences, §7.3) | 112 | window $[47,128]$; 112 is at 74 % of the top | half $\to56$: cover still valid ($.0268<.032$), but the reuse mechanism dies and the centre count goes from $2.5\cdot10^{5}$ to $\ge5.4\cdot10^{6}$ (model, `n112.py`); double $\to224$: **int8 overflows** ($223>127$) and $C(228,5)=4.91\cdot10^{9}>2^{31}$ | keep 112, or 128 (the int8-maximum, dyadic midpoint); 112 costs 6 % above the modelled optimum $N\approx120$ | **needs change** (the stated reason is not the binding one) |
| $w=1/N$ | §2.2 | appears only as $1/N$; no independent inequality | 1/112 | — | scales with $N$ | define as $w:=1/N$ and never tune it separately | justified (derived) |
| $R=0.032$ | §2.4, Prop. 2.10 | $3/(2N)\le R$ (below) and $2\pi(R+10^{-7})<.203$ (above, from the §3 frame budget) | 0.032 | $2.39\times$ above the floor $.01339$; $0.96\%$ below the ceiling $.03231$ | half $\to.016$: still covers ($.016>.01339$) but the retained-centre count explodes as $(R-3/2N)^{-5}\!\sim\!10^{12}$; double $\to.064$: $\mathrm{Rs}=.402>.203$, no certified frame, Stage A yields nothing | keep 0.032; state the two-sided window $[.01339,.03231]$ | justified (nearly tight from above) |
| $0.0320001$ | §2.4, A.3 | covers the $<10^{-14}$ error of converting nine rational midpoints to binary64 | 0.0320001 | increment $10^{-7}$ is $10^{7}\times$ the error it covers | halving the increment to $10^{-12}$ would still be $100\times$ the error; doubling it to $2\cdot10^{-7}$ costs nothing in A but would consume 160 % of the $10^{-4}$ of row **RSQ** if anything ever relied on that | replace $10^{-7}$ by $10^{-12}$ and say which quantity it covers | arbitrary-but-harmless |
| RSQ $=(\mathrm{fl}(.032\cdot112))^{2}-10^{-4}$ | §2.4, A.3, `testBucket` | must dominate the arithmetic error of (2.17)–(2.19), which A.3 bounds by $10^{-12}$ | 12.844956 | over-covers by $10^{8}\times$; see the note | — | keep, but write it as $(\mathrm{fl}(.032N))^2(1-10^{-5})$ so it is dimensionally a *squared-radius* slack | arbitrary-but-harmless |
| $10^{-4}$ (the element of RSQ) | A.3 | same | $10^{-4}$ | $10^{8}\times$ the $10^{-12}$ it must dominate | the same $10^{-4}$ is exactly the *squared* slack that would be needed to absorb the $.032\to.0320001$ inflation at $N=112$ (which costs $0.80\cdot10^{-4}$), and it would fail at $N\ge126$ | do not let the two roles share one number | needs change (documentation) |
| gap-filter thresholds $1-(l-1)/N$, $1-(l+2)/N$ | (2.8) | Lemma 2.5 bounds the gap change by $w=1/N$; the thresholds differ by $3/N$ | ratio 3 | $3\times$ the perturbation, for every $N$ | the ratio is $N$-free, so this filter cannot pin $N$ | say so: (2.8) is a filter, not a constraint on $N$ | justified |
| enumerated "pairs" $=151{,}744{,}086$ | Table 1, §7.5 | must be $\le$ the count of tuples surviving the stated filters | 151,744,086 | see `seedcover.py`: the orientation filter (2.7) alone leaves at most **85,349,292**; with (2.8) at most 16,197,157 | — | report the pre-filter, post-filter and matched counts separately | **needs change** (unreproducible count) |

### Note on RSQ
A.3 says the error before the subtraction is $<10^{-12}$, so $10^{-4}$ is $10^{8}$ times larger than
needed. The number is therefore not a rounding margin at all — it is a *radius* margin of
$1.4\cdot10^{-5}$ cycles ($10^{-4}/(2\cdot112\cdot.032)$). Two consequences worth printing:
(i) it is not scale-free: it buys $1.4\cdot10^{-5}$ cycles at $N=112$ and $8.3\cdot10^{-6}$ at
$N=189$, so a future $N$ change silently changes the meaning of the margin; (ii) it is numerically
almost exactly the *squared* slack that the $.032\to.0320001$ enlargement would need ($0.80\cdot
10^{-4}$ of it), which invites exactly the wrong reading. The paper's own defence — the enlargement
is absorbed on the Stage-A side — is the right one, and should be stated where RSQ is defined.

---

## 2. Stage A: the U(2) grid and the two targets

| constant | where | the inequality that constrains it | value | slack | half / double | recommendation | status |
|---|---|---|---|---|---|---|---|
| $N_u=16$ | §3.3, §7.2 | the cell circumradius in cycles is $\sqrt4\cdot\frac1{2N_u}=\frac1{N_u}$, and a per-cell ball cannot be smaller, so $\frac1{N_u}\le.103$ is necessary: $N_u\ge9.7$, i.e. $N_u\ge12$ (Lemma 3.3 needs $4\mid N_u$) | 16 | $.103\cdot16=1.65\times$ | half $\to8$: $\frac18=.125>.103$ — **no cell can ever be covered**; double $\to32$: 16× the cells (131,072/seed, still under the $10^6$ node cap) and strictly easier coverage per cell, but 4× more work | keep 16 and state the necessary condition $\frac1{N_u}\le.103$; it is the paper's cleanest derivation and it is missing | justified |
| $h=\pi/N_u$ | (3.13) | cell half-width in radians; $h=\pi/16=.1964$ | $\pi/16$ | — | derived from $N_u$ | define once as $h:=\pi/N_u$ | justified (derived) |
| subdivision 16→32→64→…→512 | §3.7 | $N_u^k$ children × cells must fit the $10^6$ node cap; at 64 the grid has $64^4/8=2{,}097{,}152$ cells $>10^6$ | depth 5 (16…512) | 512 is never reachable by enumeration | at 64 and beyond Stage A *must* succeed by coverage, never by enumeration (F5) — the paper says this, one sentence earlier it should be captioned as "completeness at depth $\ge4$ rests on coverage" | print that sentence | needs change (exposition) |
| local target $.103$ | §3.7, §4.6, §7.2 | $\frac1{N_u}=.0625\le.103$ (cells must be coverable) and $.103<.125$ (atlas cap) | .103 | window $[.0625,.125]$; .103 is at 41 % of it | half $\to.0515$: below $\frac1{N_u}$, nothing is coverable; double $\to.206$: above the $.125$ atlas cap, no record can be stored | keep; state the window | justified as a range, arbitrary within it |
| global (atlas) target $.125$ | §4.7, §7.2 | $.103<.125\le\tau_{\max}=.126$ | .125 | $0.8\%$ below $\tau_{\max}$ | double $\to.25$: exceeds $\tau_{\max}$ and violates the Stage-C requirement $r\le.03$ even more; half $\to.0625$: below the local target, so no merge is ever allowed and the atlas grows without compressing | keep; state $.125\le\tau_{\max}$ | justified, **tight** |
| `levels=3, iters=2, first=1` | §7.2 (`arun`) | not stated; the text gives no semantics for these three integers | 3, 2, 1 | — | — | define them in the paper, or drop them from the invocation display | needs change (determinacy) |

The clean chain here is worth printing as a line: $\frac1{N_u}\le.103<.125\le\tau_{\max}=.126$, with
$N_u=16$ leaving the first inequality at $1.65\times$ and the last at $1.008\times$.

---

## 3. Stage B: the refinement ladder and the box cap

| constant | where | the inequality that constrains it | value | slack | half / double | recommendation | status |
|---|---|---|---|---|---|---|---|
| $(\tau,w)$ pairs | §5.6, §7.2 | (i) $w\ge10^{-4}$ and $\tau\le.126$ are locked by $L\le1262$: at $w=10^{-4}$, $L=\lceil.126/w+.500001\rceil=1261$, axis $2523\le2524$; (ii) the grid contains $[-E,E]$ iff $(L+\tfrac12)w\ge E$; (iii) the pass certifies children only up to $\tau-\frac{\sqrt k}{2}w$ | $(.07,.013)$, $(.016,.005)$, $(.011,.0038)$ | (ii) 1.20×, 1.11×, 1.31×; (iii) 4.8×, 2.9×, 2.6× at $k=5$ | halving $w$ doubles $L$ and hence the box count $n^k$; doubling $w$ halves the margin in (ii) — at pass 1 $(L+\frac12)w$ would still exceed $E$, but the child-radius margin (iii) drops to 2.4× | keep the values; print (ii) and (iii), which are the two inequalities that actually pin the ladder | justified |
| $\tau\in[10^{-4},.126]$, $w\in[10^{-4},.05]$ | §5.6 | see row above: $10^{-4}$ and $.126$ are a *pair*, calibrated to the 2524 axis bound | as stated | the corner $(w,\tau)=(10^{-4},.126)$ gives $L=1261$, one axis unit below the stated maximum | doubling $\tau_{\max}$ to .252 doubles $L$ to 2521 and the axis to 5043: the stated 2524 fails | keep; state that the two bounds are one constraint | justified |
| box cap $5\cdot10^{7}$ | §5.6, §7.3 | $n^k\le5\cdot10^7$ with $n=2L+1$ | $5\cdot10^7$ | pass 2 at its largest admissible $k=5$ uses **57.3 %** ($31^5=28{,}629{,}151$) | half $\to2.5\cdot10^7$: $k=5$ becomes inadmissible in pass 2 ($31^5>2.5\cdot10^7$), so no record with $k=5$ could enter B; double: nothing new becomes admissible until $k=6$ ($31^6=8.9\cdot10^8$, still 18× over) | keep; it is the *only* cap with a documented near-binding case | justified |
| $k\le10$ | §6.1, §5.6 | $(2L+1)^k\le5\cdot10^7$ gives $k\le5,5,7$ for the three passes | 10 | unreachable: $k=6$ in pass 2 is $17.8\times$ over the cap | — | restate as $k\le5$ (passes 1–2) and $k\le7$ (pass 3), keeping $k\le10$ only as the `patch` guard | **needs change** (F3) |
| depth 6 | §5.6 | a fully split tree is $\sum_{j\le6}2^{jk}$ boxes: $1.79\cdot10^7$ at $k=4$, $1.11\cdot10^9$ at $k=5$ | 6 | reachable only for $k\le4$; for $k\ge5$ the box cap binds first | — | state "depth 6 is attainable only for $k\le4$" | needs change (exposition) |
| 25 midpoint trials | §5.2 | the bracket is $[0,1.01a]$, $a\le.126$, and a usable $\rho$ must exceed $10^{-7}$: needs $\lceil\log_2(1.01\cdot.126/10^{-7})\rceil=21$ halvings | 25 | $16\times$ the required resolution ($3.8\cdot10^{-9}$) | halving to 13 leaves $1.5\cdot10^{-5}>10^{-7}$ — every $\rho$ would be refused, so the relation stage would fail *silently*; doubling costs 25 more evaluations of $\hat D$ | keep 25; print the $\log_2$ computation | justified |
| 30 bootstrap updates | §4.6 | none: the guard $0\le\mathrm{init}<3$, $t<10$, $C<20$; stopping keeps the previous valid upper | 30 | any cap works | halving only stops improvement earlier; the next stage records the record as unresolved, never negative | keep; say "a work bound, not a soundness bound" | arbitrary-but-harmless |
| Atlas $2\cdot10^{6}$ Roots | §4.7, §7.3 | per seed | $2\cdot10^6$ | not reported (F6); the run had 0 failed seeds and 0 unresolved | — | report the per-seed maximum | needs change (evidence) |
| $256$ records/file, $2\cdot10^6$/$8\cdot10^6$ | §5.6, §7.3 | $32\cdot12^5=7{,}962{,}624\le8\cdot10^6$ | see left | the $8\cdot10^6$ cap is calibrated to **one full C subdivision** with 0.47 % headroom; the $2\cdot10^6$ bin cap is 8× larger and therefore unreachable (retained bins $\le8\cdot10^6/32=250{,}000$) | half the $8\cdot10^6$ cap would make the first C subdivision illegal | keep; state that $8\cdot10^6=32\cdot12^5$ rounded up | justified (the $2\cdot10^6$ bin cap is not) |

---

## 4. Stage C: the clustering cutoff (F2) and the graph cap

| constant | where | the inequality that constrains it | value | slack | half / double | recommendation | status |
|---|---|---|---|---|---|---|---|
| $.042$ (proposed cluster radius) | §6.3, §7.2 (`crun ... .042 ...`) | a merge is geometrically possible only when the effective radius $\ge1/M$; with $.042$ that needs $M\ge51$ | .042 | at the recorded grids 12, 24, 48: **no merge is possible at all** ($.042-1.11/M<1/M$) | doubling to .084 would make $M\ge26$ merge-capable and is otherwise harmless (radii are recomputed); halving to .021 confines compression to $M\ge101$, beyond the deepest grid | keep, but say *where* it can act: only $M=96$ | arbitrary-but-harmless, **mis-described** |
| $1.11$ | §6.3, A.10 | it bounds $X_M=\frac{\sqrt{29/6}}{2M}=\frac{1.099242}{M}$, so $1.11$ is correct as an *upper* bound (1 % high) | 1.11 | 1.0 % | the defect is positional, not numerical: because the base is squared, the sign is lost | use $\sqrt{29/6}/2$ and write $\max(0,\,.042-X_M)^2$ | **needs change** (F2) |
| $2048$ clusters | §6.3, §7.3 | compression $12^5/2048=122{:}1$ would be needed if every grid-12 bin survived; with the corrected cutoff only $M=96$ compresses (up to 5 lattice steps) | 2048 | not reported (F6) | halving forces the centres to be within $.042$ of twice as many bins: with the degenerate cutoff at $M=24$ this fails immediately | report the cluster count per record; fix F2 first | needs change (evidence) |
| graph step cap $5\cdot10^{6}$ | §6.7, §7.2 (`crun ... 5000000`) | none; a cap yields the "possibility/give-up" flag, never a negative certificate | $5\cdot10^6$ | **binding**: 163 of 22,379 initial records (0.73 %) hit it exactly, and all 15 bad files are these | halving would roughly double the number of records routed to the fallback; doubling is untested | keep, and report the 163 as a cost curve: they are the only capped class | justified (binding) |
| ball radii $<.1$, $|v_j|\le2$, $0\le s<.1$ | §6.3, §6.5 | two distinct balls must be separable by the pair tests | see left | the final balls must be $<.1$ while Stage C needs the Hadamard radius $\le.03$: the two are different quantities and the paper never prints both side by side | — | print both radii in one place | needs change (exposition) |

### F2, precisely
`stagec.py` reproduces the audit's numbers and adds the part that decides the severity:
$.042-1.11/M>0$ iff $M>26.43$, so the base is negative for $M\le26$; squaring makes the effective
accept radius $|.042-1.11/M|$, which is *non-monotone* ($.0505,.0042,.0189,.0304$ at
$M=12,24,48,96$). But the consequence is sharper than "no bin can merge at $M=24$": **two distinct
bin midpoints are $1/M$ apart, so no merge can occur at any $M\le50$ regardless of the sign**, i.e.
on three of the four recorded C grids (12, 24, 48) the clustering stage is a no-op. The corrected
formula $\max(0,.042-X_M)^2$ is monotone non-decreasing in $M$ (verified for $M=6..512$) and
preserves the one behaviour the run needs (a merge radius of $.0306$ at $M=96$, i.e. 2.9 lattice
steps).

---

## 5. The undiscussed arithmetic constants

| constant | where | the inequality that constrains it | value | slack | half / double | recommendation | status |
|---|---|---|---|---|---|---|---|
| $.64$ eigenvalue split | §4.2, `buildH::patch` | none: it *proposes* T columns, and `patch` then certifies $T^*T-I$, $(I-\Pi)T$, $\|F(P)\|$ and the 36-coordinate identity | .64 | free | half $\to.32$: more columns proposed, and $>10$ proposed columns is a failure — costs work, never soundness; double $\to1.28$: if no structural eigenvalue is below it, $k=0$, and §5.6 makes an unresolved cell with $k=0$ a **parent failure** | keep; say explicitly that it is a proposal threshold, so the failure mode is asymmetric | arbitrary-but-harmless (but see half/double) |
| $K=1.00001$ | §6, A.10 | $\omega<10^{-5}$ gives $\|T\|\le\sqrt{1+\omega}=1.000005$ | 1.00001 | $2\times$ in the excess over 1 ($1.0\cdot10^{-5}$ vs $5.0\cdot10^{-6}$) | halving the excess would leave $K<\sqrt{1+\omega}$ and the tangent-entry bound would fail | replace by $K:=\sqrt{1+\omega}$ and delete the constant | justified but redundant |
| $q_d<3.8$ | §4.8, A.7 | the arc bound uses $(1-q_d/4)^{-1/2}$, which needs $q_d<4$; $3.8$ leaves 5 % and inflates a chord by at most $4.47\times$ | 3.8 | 5 % below the hard bound 4 | double $\to7.6$: the square root is undefined — the constant *must* stay below 4 | keep; print the hard bound 4 and the 4.47× inflation | justified |
| $\beta=.45$, $\beta=.8$ | §4.5, A.7 | Lemma 4.11 holds for every $\beta>0$; the values give $(1+\beta,1+1/\beta)=(1.45,3.22)$ and $(1.8,2.25)$ | .45, .8 | no inequality pins either | any value works; the choice only changes the ellipsoid's tightness | say "chosen to minimise the enclosures at the two centres; any $\beta>0$ is sound" | arbitrary-but-harmless |
| $\beta<.1$ (tensor step) | §4.2 | $\|U^*U-I\|\le\beta<.1$ gives $\|U^{-1}\|^2\le1/(1-\beta)$ | .1 | 10 % | doubling to .2 costs 25 % in the inverse bound and is still sound | keep | justified |
| sentinel $100$ (`ell`) | A.8 | A.8 proves the certified spectral bound is $\le100.1$ | 100 | **none** — the sentinel lies inside the legitimate range | — | use a non-representable sentinel (NaN with a checked `isnan`, or a status flag) | **needs change** (F4) |
| sentinels $10$ (`bootstrap`, `relationB::eval`) | §4.6, §5.2 | the bootstrap guard is $t<10$; the usable range is $C<20$, $\mathrm{init}<3$ | 10 | the guard is what excludes 10 from the useful range, so the sentinel is *just* outside it | any change to the $t<10$ guard silently re-admits the sentinel as data | replace by a status flag; do not rely on a threshold to encode failure | **needs change** (F4) |
| $10^{-6}$ divisor skip (`extend`) | §2.3, A.3 | skipping $\lvert a\rvert<10^{-6}$ *removes* a constraint, so the interval can only be too large | $10^{-6}$ | at $\lvert a\rvert>0.999\cdot10^{-6}$ the quotient is $<1.2\cdot10^{8}$ (A.3) | a larger skip weakens the filter (more bins retained); a smaller skip risks a huge quotient | keep; add the one sentence "this can only enlarge the interval" | justified |
| closing-table margins | A.12 | each margin must exceed the error it covers | 23 rows | see below | — | print the ratio column | mostly justified |

### The closing table, with ratios
`margins.py` recomputes every row. The ratios span five orders of magnitude: median $200\times$,
range $1.25\times$ to $10^{6}\times$. The tightest are **Candidate external tangent error
$1.2\cdot10^{-4}$ vs $1.5\cdot10^{-4}$ rad ($1.25\times$)** — four times tighter than anything else
— then **A flat norm ($10\times$)** and **A directional comparison ($25\times$)**. The loosest are
the seed-gap ($10^{6}\times$), the B local update ($10^{5}\times$) and the bootstrap update
($10^{4}\times$). A margin of $1.25\times$ is not evidence of a defect, but it is the one place
where a change of any nearby constant (the $.103$ target, the tangent bound, $K$) should be
re-checked; the paper should say so. The whole ratio column is one line of the paper's work and
would remove the "margins are assertions" objection at a stroke.
