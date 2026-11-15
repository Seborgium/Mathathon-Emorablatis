# Code audit: what could be checked, and what I found

Companion to `results/proof-claims.md`. Subject: *The maximum number of mutually unbiased bases in
dimension six* (OpenAI, 24 Sep 2026), §§2–7 and Appendix A.

## 0. Scope: the code is not in the packet

The paper's certificates rest on seven sources (`seed.cpp`, `covout.cpp`, `ub.cpp`, `patchx.cpp`,
`atlas.cpp`, `stageB.cpp`, `stageC.cpp`), four entry points, and an archive referenced as
`verification/code/`, `verification/computation/`, `verification/REPRODUCE.md`.

I could not audit the code, for reasons that are facts about the packet rather than choices:

* only the PDF was supplied; it contains no embedded files (`/Filespec` and `EmbeddedFile` counts are
  zero), and no source, no archive, no `extraction.json`, no `build-manifest.json`;
* no code listing appears in the paper — every routine is described in prose;
* no repository connection is available here, so the archive cannot be fetched.

Consequently the hashes in Table 2 are unverifiable, and so is every statement of the form "`x` checks
`y`". What follows is therefore an audit of the **specification**: for each routine, does the
behaviour the paper attributes to it suffice for the lemma that depends on it, are its stated guards
and thresholds large enough to dominate the errors the paper proves, and is the described behaviour
determinate enough to be checked at all. That is the strongest audit available from the document, and
it does catch a class of defect: a specification that is inconsistent with itself or with the
mathematics cannot be right whatever the code says.

Three concluding sections: findings with severity, the numerical consistencies that *do* hold, and
the minimal packet that would make a real audit possible.

## 1. Method

For each routine I asked three questions.

1. **Sufficiency.** Does the lemma that cites this routine need exactly what the description
   provides? (If a lemma needs an enumeration to be complete, or a check to be one-sided, the
   description must say so.)
2. **Domination.** Are the stated acceptance thresholds and added margins strictly larger than the
   per-quantity error the corresponding Appendix A subsection derives? A margin below the error it
   is meant to cover would silently break soundness; a margin far above costs only work.
3. **Determinacy.** Is the behaviour pinned down (order of enumeration, tie-breaking, choice of
   integer lifts, sentinel values), or does a lemma's truth depend on an unspecified choice? An
   unspecified choice is *harmless* if the lemma is universally quantified over it ("for every
   admissible lift"), and *fatal to checkability* otherwise.

Two structural facts made the audit tractable and are worth stating: every exclusion in the paper is
a violation of a **necessary** condition, and every heuristic step is separated from its certificate.
So the recurring verdict is "undetermined but harmless", and the real risks are (i) claims where a
*covering* property is asserted of a heuristic (clustering, radius growth, atlas merges), and (ii)
claims whose subject is an algorithm (the clique search).

## 2. Routine-by-routine

Verdicts: **OK** description suffices; **OK-U** sound but leaves a choice free (harmless where the
lemma is universally quantified); **TENSION** two stated limits cannot hold at once; **UNCHK**
requires the source to judge; **DEAD** present but supplies nothing to the certificate.

### Seed cover (§2)

| Routine | What the paper says | What the proof needs | Verdict |
|---|---|---|---|
| `seeds::build` | visits every weakly increasing 5-bin $x$ tuple; applies (2.7), (2.6) first inequality, `sumok`; separately every first bin × weakly increasing 4-bin $y$ tails | *completeness of enumeration* (2.10) | UNCHK, but the enumeration is arithmetic and should be checkable from `centers.txt` |
| `seeds::mk` | selects $s$ = first minimiser of $\lvert2b_s+1-N\rvert$; total gap uses sorted midpoint bins | that a specific but arbitrary $s$ is chosen and recorded | OK (the rule is explicit, and validity is independent of which one) |
| `sumok` | tests (2.11) in the residual direction and directions $\perp$ the five exponential columns | soundness needs only that (2.11) holds for *all* $v$ | OK-U: testing a finite set of directions can only retain more bins |
| `extend` | starts from $[-1/2,1/2]$, intersects (2.14) for $t=s$ (X) and $t=0$ (Y); skips divisors $<10^{-6}$; rejects only on strict disjointness of the two intervals | (2.8) plus one-sided endpoints | OK-U: skipping a divisor *removes* a constraint, so the intersection is too large, never too small |
| `covout` | matches the shared bin, applies (2.6) second inequality, intersects shared-displacement intervals | same | OK |
| `supdual` | proposes $v$ with entries $\le10^4$; evaluates (2.19) with $1.251\pi/N$ for $1.25\pi/N$; adds a final support margin | (2.9) for the *stored* $v$, which is exact rational data | OK: the larger constant is conservative, and the proposal method is irrelevant |
| `testBucket` | tries (2.18), then the dual bound; succeeds only if the resulting upper bound on (2.17) is below a *lowered* threshold for $(NR)^2$ | that success certifies the whole feasible part of the bin pair | OK; note the threshold is $(.032\cdot112)^2-10^{-4}$, i.e. slightly *smaller* than the nominal radius — conservative in the right direction |

### Stage A (§3)

| Routine | What the paper says | What the proof needs | Verdict |
|---|---|---|---|
| `block::setup`, `makeD`, `makeJ` | assembles the fixed frames, the comparison block $D$, the linear map $J$ from the entrywise formulas printed in §3.7 | (3.1)–(3.7), (3.23) | UNCHK, but §3.7 prints the coefficient formulas explicitly — this is the one place where a reader could re-derive the matrix and compare |
| frame check | computes $S$, $m=\sqrt{4-\lvert S\rvert}$, pseudo-inverse numerators, Gram–Schmidt complement; fails the seed if $m\le1.25$ or a residual is too small | Lemma 3.1's hypotheses ($\lvert S\rvert<4$) plus the lower bounds $m_B,m_C>0$ | OK (A.4 gives the propagation: $m>1.24$ ideal, $16-\lvert S\rvert^2>6.1$) |
| `uc::init`, `uc::initDeriv` | assembles the four angular derivatives of (3.12) at the cell midpoint | Lemma 3.4's differential | OK: §3.3 states the four derivatives in closed form |
| `eq` | stacks exactly the twenty equations of (3.28) (16 flat + 2×2 seed sums) | Lemma 3.9's $\mathbb{R}^{20}$ | OK |
| `trial::pass` | proposes directions by regularised linear solves and weight updates | nothing (heuristic) | OK |
| `trial::certificate` | rejects nonfinite directions; requires max magnitude in $(10^{-100},10^{100})$; divides by the max; uses the negative part of the flat weights | Cor. 3.10: that the *stored* normalised $y$ satisfies (3.29) with the $\max(0,\cdot)$ term | OK — and this is exactly the guarantee the lemma needs, correctly specified |
| `Asearch::testA` | the used Stage-A path | Prop. 3.11 | UNCHK |
| `Usearch::test`, scalar routines | present; "do not supply additional exclusion tests for this run" | nothing | DEAD |

### Roots and atlas (§4)

| Routine | What the paper says | What the proof needs | Verdict |
|---|---|---|---|
| `buildH::gen` | $F$, $L_P$; rejects $\lvert p_j\rvert>4$ or nonfinite | Def. 4.1, (4.1)–(4.2) | OK |
| `buildH::patch` | proposes a horizontal basis from the 25-coordinate horizontal Jacobian; eigenvalues $<.64$ propose $T$ columns, the rest factor $H_V,L_V$ for $M$; factor entries checked $\le2$; $>10$ tangent columns ⇒ failure; checks $T^*T-I$, $(I-\Pi)T$, $\|F(P)\|$, and the full 36-coordinate identity $\Pi-TT^*-ML_P\Pi$ | Prop. 4.6, i.e. (4.4) and (4.15) with a valid $C$ | UNCHK — **highest-consequence unverifiable claim in the paper** (see F1) |
| optional tensor step | forms row Gram (4.14), proposes $U$, checks $\beta<.1$, certifies $\|S\|^2\le r/(1-\beta)$, takes the min with the other $C$ | Lemma 4.4's second constant | OK-U; the check is a congruence bound, not an eigenvalue assertion |
| `Candidate::prep` | checks direction and magnitude: $\mathrm{mag}_j>.15$, unit-chord discrepancy $<10^{-7}$; sets slack, $q_d<3.8$, `invmag` | Lemma 4.8 plus the $2\cdot10^{-6}$ centre correction of Lemma 4.9 | OK (A.7 supplies $5.5\cdot10^{-8}$ direction error and $1.56\cdot10^{-7}$ chord) |
| `Candidate::delta` | rounded dephase and wrap, giving integer lifts | (4.17) — that *some* fixed integers work | OK-U: the integer choice is free |
| `covercompute::value` | direct support bounds (4.27)–(4.28), `+.0001` before dividing by $\pi$, $+10^{-8}$ on $d^2$ | Lemma 4.10 | OK, margin $10^{-4}$ vs error $2\cdot10^{-6}$ |
| `ell` | triangular bound, then $\gamma$-candidates with `gap` $=\gamma-gu-10^{-9}\ge10^{-6}$; trial solve $z$ with $\lvert z\rvert<10^8$; returns a certified inverse quadratic form | Lemma 4.12, and the signed-addition argument of A.8 | OK-U: the solve merely proposes $z$; the residual certificate is checked. See F4 on the sentinel |
| `spectralUpper` | min of max absolute row sum $+10^{-10}$ and a fourth-norm bound with $2\cdot10^{-7}$ | Lemma A.3 | OK (A.8: downward error $<10^{-10}$ vs $2\cdot10^{-7}$) |
| `bootstrap` | ≤30 updates of (4.38); inflates $t$ by $.00002$, radius by $10^{-6}$; requires $0\le\mathrm{init}<3$, $C<20$; sentinel $10$ | Prop. 4.13 | OK |
| `local::test` | success only after a certified `covercompute` bound fits `.103`; grows the radius to cover, $+10^{-8}$; else snapping proposes a new centre | Prop. 3.11 + 4.16 | OK-U: snapping must re-pass `patch` and the same covering computation |
| `mapH`, `variants`, `canonicalMap` | signed permutation/transpose maps; pivot list, largest-gap tie-breaks, "the signature used to choose among these maps need not be a canonical invariant" | Lemma 4.7 + 4.15: existence of *an allowed* $\Phi$ suffices | OK-U; correctness does not need canonicity, but see F7 |
| `Atlas::find`, `Atlas::add` | wrapped dephased difference, projected, norm $+10^{-7}$; grows radius to at least $r+d$, $+10^{-8}$, cap check with $2\cdot10^{-8}$ | Lemma 4.15 | OK (A.6: projection error $<10^{-11}$ vs $10^{-7}$) |

### Stage B (§5)

| Routine | What the paper says | What the proof needs | Verdict |
|---|---|---|---|
| `relationB::init` | wrapped difference, cut at most $.249$ (direct-proposal path) and $.23$ (ordinary reuse); inward cuts "only decline a relation" | Lemma 5.4's $a$-containment and Prop. 5.2's $D\ge R+\|d_q\|$ | OK — the cut is the only thing that can be wrong, and a wrong cut loses an opportunity, not coverage |
| `relationB::eval` | ≤30 improvements of (5.16); guard $0\le t\le2$; sentinel $10$; enlargements $2\cdot10^{-8}$, $10^{-9}$, $10^{-8}$ | Lemma 5.3 | OK (A.9: local errors $<10^{-13}$ vs $10^{-8}$) |
| ρ-search (`init`) | 25 midpoint trials, ℓ replaced only on a successful trial; returns $\rho=\max(0,\ell-10^{-8})$ and requires $\rho>10^{-7}$ | Lemma 5.4 | OK, and the paper is right that no monotonicity of $\hat D$ is needed — a single stored trial is the certificate |
| `outside` | lower version of (5.22), $10^{-8}$ inside each nonnegative part, compared with inflated $E^2$ | Lemma 5.5 + grid coverage | OK (A.9: rounding $<4\cdot10^{-17}$ vs $9.9\cdot10^{-15}$ separation) |
| `corner`, `markRec` | corner norm $+10^{-8}$; `markRec` accumulates per-coordinate inflated radii and keeps a branch while the partial sum $\le(\rho-5\cdot10^{-8})^2$ | Lemma 5.5 and whole-box marking | OK; the paper is explicit that a subbox success does **not** license marking its base box — correct and easy to get wrong |
| `assign` | merge if $r+\ell+2\cdot10^{-8}<\tau$, grow to $r+\ell+10^{-8}$; else insert $\Phi Q$ with radius $r$ | Lemma 5.6 | OK |
| `inverseTransform`, `addNear` | optional pull-back and fresh relation | nothing required (failure cannot undo an assignment) | OK-U/DEAD-ish: an optional step whose failure is silently ignored |
| batch writer | ≤256 records per file, radius replaced by $\tau$, atomic rename, count marker | Cor. 5.8 | OK; the "count marker alone is not a certificate" caveat is stated |

### Stage C (§6)

| Routine | What the paper says | What the proof needs | Verdict |
|---|---|---|---|
| `Layer::test` | (6.7), then (6.12), then (6.11) for proposed directions; proposals normalised by max entry in $(10^{-100},10^{100})$ | Lemmas 6.2, 6.3 | OK |
| `single::support` | forms $J^*y$ and the real companion sums; coefficient array starts at zero for the pure-vector remainder | Lemma 6.3, and Lemma 6.7's "cannot be decreased by cancellation with an edge coefficient" | OK, and this ordering detail is essential — correctly specified |
| `cluster` | ≤2 assignment iterations, Lloyd-like; final iteration does not move centres; radii recomputed from assignments; caps 2048 centres, $\lvert v_j\rvert\le2$, $0\le s<.1$ | Lemma 6.4 | OK-U for assignment, OK for radii. See F2 on the cutoff formula |
| `graph::joint` | ≤14 rows; shared tangent coefficient accumulates both $-(B^t)^*y_t$ before taking the norm | Lemma 6.7 | OK, and this is the right place for the only genuine coupling between the two vectors |
| `graph::exist` (mode 1) | least-vertex two-pool enumeration, root deletion when the first-clique target is 6, auxiliary six-clique prune on the second pool, step cap 5,000,000 with a persistent give-up flag | Lemma 6.8 | UNCHK — F9 |
| `negative` | exactly two negative paths: empty completed bin layer, or completed negative graph search | Prop. 6.9 | OK: the statement that caps and failures are never negative is repeated consistently in §§6.3, 6.6, 6.7 |
| `expair` | guarded range, checked arguments | Lemma A.2 | OK (arguments bounded: $\lvert P\rvert\le4$, $\lvert v\rvert\le2$, differences $\le6$) |

## 3. Findings

### F1 — The heaviest unverifiable claim is `buildH::patch` (Prop. 4.6). Severity: high
The whole atlas rests on it: if `patch` can return a Root whose constants do not actually satisfy
(4.4)/(4.15), every ball is a fiction and no later stage notices. The paper's defence is good in
principle (direct checks, not eigensolver accuracy; checked Gram defects; one-sided row sums; a
Frobenius residual for the full 36-coordinate identity, not just the projected one). But it is
asserted, and A.5's budgets — $2.1\cdot10^{-11}$ for the factor product, $10^{-9}$ per entry for the
identity residual, `id`'s $2\cdot10^{-6}$ addition — cannot be checked without the code.
*Settled by:* the certificate, or `patch`'s source plus one worked record re-derived at high precision.

### F2 — The Stage-C clustering cutoff is degenerate at the two coarsest grids. Severity: medium (not a soundness issue)
§6.3 states the candidate threshold is $(.042-1.11w)^2$ with $w=1/M$. But $1.11w$ bounds $X_M$, and
by Lemma 6.1, $X_M=\sqrt{29/6}\,a$ with $a=\frac1{2M}$ — i.e. $1.11w\approx X_M$. So the base of that
square is negative exactly when $X_M>.042$, i.e. for $M\le 26$ ($1.11/26=.0427$):

| $M$ | $X_M$ | $1.11w$ | $.042-1.11w$ | effective accept-radius |
|---|---|---|---|---|
| 12 | .0916 | .0925 | $-$.0505 | .0505 |
| 24 | .0458 | .0462 | $-$.0042 | .0042 |
| 48 | .0229 | .0231 | +.0189 | .0189 |
| 96 | .0114 | .0116 | +.0304 | .0304 |

Squaring hides the sign, so the "cutoff" is an absolute value, and the effective merge radius is
**non-monotone in the grid**: $.0505\to.0042\to.0189\to.0304$. At $M=24$, neighbouring bin midpoints
differ by $1/24=.0417$ in a coordinate, far above the coordinate cutoff $\sqrt2\cdot.0042=.0060$, so
*no* bin can merge into an existing centre and clustering degenerates to one centre per retained bin.
That is the most expensive and weakest regime, and it is where the 2048-centre cap would trip
(clustering failure ⇒ unresolved, not negative, so soundness survives).

**Corrected 2026-11-14, from T5 (member m3):** the sign defect is the smaller half of the problem.
A merge is *geometrically* possible only when the effective radius reaches the midpoint spacing
$1/M$, i.e. $.042-1.11/M\ge 1/M$, which needs $M\ge 51$. So on three of the four recorded Stage-C
grids (12, 24, 48) clustering cannot merge anything at all, whatever the sign, and the corrected
formula $\max(0,.042-X_M)^2$ is monotone in $M$ and keeps the one behaviour the run needs
(radius $.0306$ at $M=96$, 2.9 lattice steps).
*Settled by:* reporting the number of retained bins and clusters per grid. If cluster counts at
$M=24$ are close to bin counts, the formula is behaving as described here.

### F3 — The stated root dimension $k\le10$ is unreachable at the specified refinement widths. Severity: medium (spec, not soundness)
The base grid has $(2L+1)^k$ boxes with $L=\lceil E/w+0.500001\rceil$, capped at $50{,}000{,}000$.
With the three passing parameters and the input radii those passes receive:

| pass | $w$ | input radius | $L$ | boxes/axis | max $k$ with $(2L+1)^k\le5\cdot10^7$ |
|---|---|---|---|---|---|
| 1 (mid) | .013 | ≤.125 | 11 | 23 | **5** |
| 2 (fine) | .005 | ≤.07 | 15 | 31 | **5** |
| 3 (fallback) | .0038 | .016 | 5 | 11 | **7** |

So every record entering B must have $k\le5$ (passes 1–2) or $k\le7$ (pass 3); a record with $k=6$
in `mid.bin` fails its parent outright, and the run would have ended with a nonempty bad list. Since
the run reports zero bad parents, the observed tangent dimensions must all be $\le5$. The stated
"$0\le k\le 10$" is therefore an unused allowance, and half of A.9's $k$-dependence is never
exercised.
*Settled by:* the histogram of $k$ over 3083 coarse and 22,379 fine records. If any record has
$k\ge6$, the run as described in §7.5 could not have completed, which would be a real inconsistency.

### F4 — `ell`'s invalid return value 100 lies inside the legitimate range. Severity: low
A.8 shows the certified spectral bound satisfies $gu\le100.1$, so 100 is not a distinguishable
sentinel: a *valid* bound could equal it. Safety comes not from the value but from the subsequent
conversion to cycles (which exceeds 10) and the `.103` local target. It works, but it is a
value-overloading that will break silently if any threshold in that neighbourhood is retuned.
Same class of hazard: `bootstrap`'s failure sentinel is 10, `relationB::eval`'s is 10, and §4.6
relies on the guard "$t<10$".
*Settled by:* a distinct non-representable sentinel (NaN with a checked `isnan`, or a separate status
flag).

### F5 — A tolerance at Nu = 64+ defeats exhaustive enumeration, by design. Severity: low
Stage A's grid at $N_u=64$ has $64^4/8=2{,}097{,}152$ cells per seed, above the $1{,}000{,}000$
deeper-node cap; at 128 it is $33.5$M, at 512 it is $8.6$G. So from grid 64 downward a seed is
never enumerated exhaustively: success must come from the phase-ball cover firing, and a seed that
needs enumeration is recorded unresolved. The paper says this, but the consequence deserves one
sentence: *Stage A's completeness at depth $\ge4$ rests on coverage, not on enumeration*, so the
coverage rate is the real measure of the stage's strength.
*Settled by:* per-seed counts of cells offered to `local::test` and the fraction covered at each grid.

### F6 — Node counts are not reported anywhere. Severity: medium (evidence)
For a run whose conclusion is "no region survived", the informative quantities are the ones near
their caps: nodes per seed, cells per seed, boxes per parent, graph steps, clusters per record. Only
terminal outcomes are given. The 163 graph-cap hits are named as a class, but not characterised.
*Settled by:* one table of per-stage maxima and their argmin/argmax.

### F7 — A non-canonical atlas signature enters the certificate. Severity: low
§4.7: "The signature used to choose among these maps need not be a canonical invariant." Correct
(Lemma 4.15 needs only *some* allowed $\Phi$ with a certified distance), but it means two runs of the
same code on the same input could produce different merges — so the certificate is a witness, not a
function of the input. That is fine, provided the certificate records the chosen map. It is not
stated that it does.
*Settled by:* including $\Phi$ and $N$ in each merged record.

### F8 — Three naming systems for the same seven constants. Severity: low, comprehension
Def. 4.1: $(C,n_0,id,ort,hor,mnorm,froot)$. §5.1: $(\gamma_P,\ n_{0P},\ \alpha_P,\ o_P,\ \mathrm{hor}_P,\ \mu_P,\ \varepsilon_P)$.
§6.1: $(C,\ n_0,\ \iota,\ \omega,\ -,\ -,f_0)$. §7.1's record stores the first set. A reader tracking
one constant through Stages A→B→C has to translate twice, and the paper never prints the mapping in
one place.
*Settled by:* one table.

### F9 — Lemma 6.8 is the one lemma that argues about a program. Severity: medium
Its proof describes the search (least-vertex enumeration, root-deletion convention, two-pool
intersections, auxiliary six-clique prune, persistent give-up flag) rather than establishing a
mathematical property of the graphs. There is no independent characterisation against which the code
could be checked, so its correctness is inseparable from the implementation — the only such place in
the paper. Combined with F5-of-the-earlier-review (no compact witness for a negative clique search),
this is the weakest link in the Stage-C chain.
*Settled by:* (a) a mathematical criterion for (6.24) infeasibility — e.g. a maximal-biclique
characterisation that a checker can verify directly on the adjacency sets — or (b) an emitted search
trace checked by an external tool.

### F10 — Dead and unused paths in a certificate chain. Severity: low
`Usearch::test` and "scalar routines" supply no exclusions in this run (§3.6); `addNear` is optional
and silently ignorable; the "standalone sample drivers are not executed". Each is defensible
(the paper is explicit), but a reader auditing the chain must know which code is *not* part of the
certificate, and the paper gives that information only in passing.

### F11 — N = 112 is defensible, but not for the paper's reason. Severity: medium (exposition)
**Added 2026-11-14 from T5.** §2.2 fixes $N=112$ with one sentence and §7.3 offers one reason:
$\binom{116}{5}$ "is below the signed 32-bit limit". That reason is inert (the same paragraph says
pair traversals use 64-bit counters) and far weaker than the text needs ($N\le189$). Two constraints
in the paper's own machinery are sharper. *Below:* Prop. 2.10's fresh-centre ball needs
$1.5/N<R=.032$, so $N\ge47$ exactly. *Above:* the five-coordinate bin differences are stored in
`int8_t`, so $N-1\le127$, i.e. $N\le128$ — and at the value the printed reason permits (189) a
difference of 188 would overflow. *What actually picks 112:* the reuse test can be guaranteed to
succeed only when $\|k\|\le NR-1.5$, so the $|k|=2$ shell opens exactly at $N\ge110$;
112 is the smallest multiple of 16 above that, i.e. $16\lceil 3.5/(16R)\rceil$ for every admissible
$R$. That is a real argument; the paper has neither the window nor the reach.

### F12 — Two seed-stage defects the audit missed. Severity: medium
**Added 2026-11-14 from T5.** (a) (2.8)'s first inequality
$g_{x,\mathrm{mid}}\le1-(l-1)/N$ cannot reject any tuple whose last midpoint gap is the largest —
which the orientation condition (2.7) delivers — because $g_{x,\mathrm{mid}}=1-(l+1/2)/N$ sits
$1.5/N$ below the bound; it does bite on mis-sorted tuples, and there it is sound. The live
comparison is between the exact bound $1-(l+1)/N$ and the midpoint threshold $1-(l+2)/N$, whose
spread is exactly $w=1/N$ — the whole Lemma 2.5 allowance, with **zero analytic slack**. (b) The
reuse threshold is written `fl((fl(.032*112))^2) - 1e-4` (A.3), so the constant $N$ is baked into
the squared radius: at $N=56$ the same test would certify $2R$ and the seed-radius claim of
Prop. 2.10 would fail silently. Both want a defect entry and a one-line fix.

## 4. What did check out

Every numerical consistency I could test reproduces exactly. This is worth recording because it is
the main evidence available that the specification is disciplined:

* $\binom{116}{5}=160{,}389{,}488$, $\binom{115}{4}=6{,}913{,}340$ — the pre-filter tuple counts;
* $64^4/8=2{,}097{,}152$ — the grid-64 cell count quoted in §7.3; $12^5=248{,}832$ — the first C grid;
* $249{,}878/4\to 62{,}470,62{,}470,62{,}469,62{,}469$ — the A shards; $764+774+757+788=3083$;
* $87\cdot256+107=22{,}379$ — the B-fine batches; $282\cdot3+281=1127$ — the final C partition;
* $73+15=88$ — initial C invocations; $163=\sum$ of the fifteen bad files;
* record size $356+288k$ bytes (i.e. $4+36\cdot8+288k+8\cdot8$); a zero-count file exactly 8 bytes;
* $2048/64=32$ words per adjacency set; $\approx2.1$M vertex pairs; $\le14$ rows in the joint test;
* $R_s=2\pi(.0320001)=.20106<.203$; $q=R_s^2(1+(A_*^2+6)/m_C^2)=.304<.32$; $h=\pi/64=.0491$;
  $z=\sqrt{(R_s(\sqrt6+A_*)/m)^2+(6h+\mathrm{pol})^2}=.808<1.5$ (the bound is very loose);
* $X_M=1.099/M\approx1.11w$ for every $M$ — which is what makes F2's arithmetic go through;
* $L\le1262$ from $w\ge10^{-4}$: $E/w=1260\Rightarrow L=1261$;
* the $\ell_1/\ell_\infty$ bin constants at $M=12$: $X_M=.0916<.19$, $L_M=.208<.42$, $I_M=.0625<.126$.

**Corrected 2026-11-14, from T5 (member m3).** My earlier statement that every margin clear the
error by two to three orders of magnitude was wrong. Recomputed over all 23 rows of Appendix A's
closing table, the ratios span five orders: median $200\times$, loosest $10^{6}\times$ (seed gap),
and the **tightest is $1.25\times$** — Candidate's external tangent error $1.2\cdot10^{-4}$ rad
against its $.00015$ rad margin, four times tighter than anything else (then A flat norm $10\times$,
A directional comparison $25\times$). No margin is below its own error, so nothing is unsound; but a
$1.25\times$ margin is the one place where any change to a nearby constant (the $.103$ target, the
tangent bound, $K$) must be re-checked, and the paper should say so rather than leave the reader to
find it. `data/appendixA_margins.csv` in `work/05-parameters/` has the full ratio column.

## 5. What would make a real audit possible

In the order that would let an outsider make progress fastest:

1. the seven sources and the four entry points, byte-identical to the run;
2. one worked record end to end: a centre, its Root constants, and the four or five checked
   inequalities that certify it, with intermediate quantities — this alone would confirm or refute
   F1;
3. per-record histograms of $k$, nodes, boxes, clusters, graph steps (F3, F5, F6);
4. the $O/U$ adjacency sets for the 163 cap-hit records (F9);
5. whether each merged record stores its $\Phi$ and $N$ (F7).

Without (1) the code cannot be audited at all; without (2) even the specification's weakest link
stays unverified; (3)–(5) are cheap and would settle three of the findings above.
