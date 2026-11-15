# Seed-stage arithmetic audit: source line vs paper, with executable controls

Member m6, direction d1 (INDEPENDENT AUDIT). Subject: `seed.cpp` + `covout.cpp`
(`.scratch/h0/dl/verification/saved-run/compiled-build/source/`, byte-identical to
`.scratch/gh/upstream/`) against preprint §2.1–2.4 and Appendix A.3 (text lines 300–630
and 3150–3260 of `.scratch/h0/preprint.txt`).

**What this is.** Every formula of the seed stage was re-derived from the paper and
*re-implemented from scratch* (no source code reused); every filter was then decided in
exact integer/rational arithmetic or in MPFR interval arithmetic with directed rounding,
and compared with the binary64 decisions of the source over the **complete** domain
(160,389,488 tuples, 178,259,964,648 pairs). Two genuine exact Hadamard matrices are run
through the whole chain as controls. Nothing below is a reading of prose: each verdict
names the executed test that decides it.

**What this is not.** I do not re-derive or check the retained-centre side (reuse
witnesses (2.18)/(2.19) on real data, the 249,878 centres, Stage A onwards). See §7.

---

## 1. Headline results

| quantity | archive / source | my independent value | verdict |
|---|---|---|---|
| weak 5-bin X tuples | — | 160,389,488 = C(116,5) | matches the enumeration loops exactly |
| after (2.7) `a<=l-d+1` | — | 85,349,292 | |
| after (2.8a) `g_x,mid<=1-(l-1)/N` | — | 29,536,175 (alone), 16,197,157 (with (2.7)) | |
| after `sumok` (2.11) | **22,829** (`xs 22829`) | **22,829** | reproduced exactly |
| sumok-passing 5-multisets | — | 169,194 | |
| Y list `|Y|` (max `|Y[a]|`) | — | 829,306 (18,997) | see F5: **not** `5*22,829` |
| pairs entering the (2.8b)/(2.14) tests | — | 298,638,554 | |
| killed by (2.8b) | — | 108,445,934 | |
| killed by (2.14) disjointness | — | 38,448,534 | |
| **checked pairs** | **151,744,086** | **151,744,086** | reproduced exactly |
| exact-vs-binary64 decision disagreements, (2.7), (2.8a) | — | **0** / 160,389,488 | see §1a |
| exact-vs-binary64 decision disagreements, (2.8b) | — | **0** / 178,259,964,648 | see §1a |
| max `|k_j|` reachable with `||k^2||`… `||k||^2<=int(T)` | 5 | 5 | but the bucket reach misses 52 tail-bin pairs (F1) |

"Reproduced exactly" means: computed by a program written from the paper's formulas
(`src/enum_x.cpp`, `src/paircount2.cpp`), with its own `cos`/`sin` (not the source's
`expair`), its own integer gap tests, and its own `extend`; the numbers agree digit for
digit with the archived counters. Run time: 0.4 s, 3.1 s, 8.5 min single core.

### 1a. What "0 disagreements" does and does not mean

It is **decision-level equality between the exact integer forms and a binary64
re-implementation**, and that is all. Concretely: for every tuple and every pair, the
exact predicate `G <= 2(N-l+1)` (resp. `G_y >= 2(N-l-2)`) and the source's floating-point
form `!(g > 1-(l-1)w + 1e-8)` (resp. `!(g + 1e-8 < 1-(l+2)w)`), **as I re-expressed
them**, with my own `cos`/`sin`, my own accumulation order and my own `extend`, return the
same answer. Two things follow and one does not:

* *Follows*: no decision in the seed filter chain sits close enough to its boundary for
  the choice of a correct-to-`1e-16` implementation of `e(x)` to matter. The margins are
  `1.89e-8` (tightest (2.11) rejection), `1e-8` (tightest (2.14) separation) and, for the
  gap tests, exact zero — but the gap tests are *integer* predicates, so "exact zero"
  costs nothing there.
* *Follows*: the counts are not artefacts of one particular rounding history, since an
  independent one gives the same counts.
* *Does not follow*: bit-identity of the source's own expression sequence. I did not
  disassemble or replay the recorded build, so "the source's `expair`, summation order and
  `extend` produce these numbers" remains a claim about that binary, not something this
  audit establishes. A literal operation-order comparison needs either disassembly-level
  identity or a differential run of that binary against a bit-exact emulation — the lead's
  background `audit_sens` run (independent `cos`/`sin`) is the right instrument for the
  former question at *value* level, and the 24 rigorously re-decided (2.11) near-ties plus
  the 59 re-decided (2.14) near-touches are the places where any such difference could
  possibly show up.
* One asymmetry worth recording: the gap tests' exact ties (7,645,275 of them, F7) are the
  case where the source's binary64 form is *not* self-evidently safe — `g` and the
  threshold each carry `~1e-16` relative error — and the thing that rescues it is the
  `1e-8` outward slack, which is `~10^8` times larger. An exact-arithmetic checker must
  therefore use the integer form, or carry its own outward margin; it must not copy the
  `1e-8` as if the mathematics needed it.

---

## 2. Source line vs paper, formula by formula

`Ver` = verdict. `A` = agree with the paper; `A+` = agree and the numerical slack is
outward (keeping *more* tuples/pairs, which is the sound direction for a necessary
condition). Every "test" column names an executed artefact in `src/` or `logs/`.

| # | paper | source expression | Ver | test |
|---|---|---|---|---|
| 1 | (2.6) closed bins, `u_b=(b+1/2)/N` | `tab[i]=expair((i+.5)/n)`; `extend` uses `tab[p.b[j]]` | A | `expiv` reproduces `e((b+1/2)/N)`; F6 control needs the *closed* bin at `0.5=56/112` |
| 2 | (2.7) `a <= l-d+1` (integral consequence of `x1<=x5-x4`) | `if(a>e-d+1)continue;` | A (exact, no fp) | counts: 85,349,292; and it *does* bite (Tao's illegal lift is rejected by it) |
| 3 | (2.8a) `g_x,mid <= 1-(l-1)/N` | `if(p.g>1.-(e-1)*w+1e-8)continue;` | A+ | exact integer form `G=max(2a+1,2N-2l-1,2·gaps) <= 2(N-l+1)`, i.e. `a<=N-l` and every consecutive bin gap `<= N-l+1`; **0 decision disagreements** with the fp form, over all 160,389,488 tuples (decision-level only: see §1a). It is *not* vacuous: 29,536,175 of 160,389,488 survive. |
| 4 | (2.8b) `g_y,mid >= 1-(l+2)/N` | `if(B.p.g+1e-8<1.-(A.p.b[4]+2)*w)continue;` | A+ | exact `G_y >= 2(N-l-2)`; **0 decision disagreements** over 178,259,964,648 pairs (§1a); 7,645,275 of them are exact ties, which the source keeps because of its `1e-8` |
| 5 | (2.9) `c=(1+Σe(u))/2πi`, `J_j=e(u_j)` | `c[0]=Σtab[b][1]/2π`, `c[1]=-1/2π-Σtab[b][0]/2π` | A | algebra: `-i(a+ib)/2π = (b,-a)/2π`; validated at F6/Tao where `||Jh+Nc|| = 0.0070, 0.0054 <= E=0.0351` |
| 6 | (2.10)/(2.11) coefficient `5πw²/4` | `err=pi*(w*w/4)*5.` | A | `5π/(4N²)=3.1305730365013085e-4`; rigorous enclosure in `audit_kernel.COEFF` |
| 7 | (2.11) tested in 6 directions | `chk(c)` then `chk(-tab[b][1],tab[b][0])` for the five `b` | A | permutation-invariant in the five entries — **this is why the Y list can be derived from 5-multisets at all** (F5) |
| 8 | (2.11) "one-sided margins" | `return !(l>r+1e-8);` | A+ | 24 tuples have `|margin|<1e-6`; all 24 re-decided in MPFR intervals, **all consistent** (`logs/constants_audit.log`); closest is a *rejection* at `-1.89e-8` (F2) |
| 9 | (2.12) `E=5π/(4N)=1.25π/N` | `double err=pi*(w/4)*5.;` in `extend` | A | equals `1.25π/N = 0.0350624` exactly (as reals) |
| 10 | (2.13)/(2.14) support coefficient in **grid** units | `r=hp(x,y)*err; … r+=.5*abs(...)` | A | coefficient is `1/2`, not `w/2`. **I first implemented `w/2` here and the F6 control caught it immediately** (Y interval excluded the true `h_s`) — the single most likely transcription slip in this section, and the control detects it |
| 11 | (2.14) `t=s` for X, `t=0` for Y | `extend(p,p.s)` / `extend(p,0)`; `share` uses `skip={X.s,0}` | A | F6/Tao: true `h_s` inside both intervals |
| 12 | "rejected only when strictly disjoint" | `if(B.hi<A.lo\|\|B.lo>A.hi)continue;` | A | shared endpoint retained; the tightest actual separation is `1.002e-8` (F3) |
| 13 | (2.15) nine coords, shared counted once | `k={e.k[0..4], y[1]-e.y[0],…,y[4]-e.y[3]}` | A | F6/Tao: the shared displacement computed from the X side equals the Y side **exactly** (`true_h` asserts it) |
| 14 | (2.16) `J*h=(J_X(h0..h4); J_Y(h_s,h5..h8))`, `p*=-Nc` | `F(j,5){int h=j?4+j:s; rows[h][2]=B.J[0][j];…}`; `rhs={-n*A.c,-n*B.c}` | **A — mapping is correct** | elementwise equality of the code's `rows[]` with `(J*)^T` of (2.16) for both controls; at F6 the block residuals are `0.00701, 0.00704 <= E` |
| 15 | (2.19) bound | `u=2Σv_a rhs_a + 2·err·(‖vX‖+‖vY‖) + Σ\|k_j-(J*^Tv)_j\|`, `return best+.01` | A | term-by-term match to (2.19); `A.3`'s `10^-4` evaluation-error budget is dominated by `.01` |
| 16 | "replaces `1.25π/N` by `1.251π/N`" | `double err=1.251*pi*w;` | A+ | adds `2.805e-5` to `E` (relative `8e-4`), and `fl(1.251πw) > 5π/(4N)` with slack `2.8e-5·2‖v‖` |
| 17 | "finite proposed components `<=1e4`" | `if(!(abs(v[a])<=1e4))usable=false;` | A | negated comparison also rejects NaN |
| 18 | `RN2 = fl((fl(.032·112))²)-.0001` | `RN2=sq(1)*pow(R*n,2)-.0001;` | A (needs `pow(x,2)=x*x`) | computed: `RN2=12.844956000000001595`, i.e. `(NR)²-1.000e-4`; certified radius `sqrt(RN2)/112 = 0.031999875 < 0.032`. The `pow` lowering is a **build** premise (A.3 says so explicitly); I did not independently disassemble the build |
| 19 | reach: `||k||<=sqrt(RN2)+1.5` | `T=(sqrt(RN2)+1.5)^2; if(s>int(T))continue;` | A (truncation is safe) | `T=25.846914`, `int(T)=25 <= T`, so `||k||²<=25` and `max|k_j|=5` — see F1 |
| 20 | bucket indices | `K=int(R*n+.51)=4; m=(n+K-1)/K=28` | A | `m*K=112>=n`; `K` reach analysis in F1 |
| 21 | "integer differences in `[-111,111]`, int8" | `array<int8_t,5> k;` | A | `N-1=111 <= 127` |
| 22 | weak enumeration | `F(a,b+1)F(b,c+1)F(c,d+1)F(d,e+1)`; Y `F(b,c+1)F(c,d+1)F(d,e+1)` | A | the loops **are** weakly increasing (this was my own first misreading): ties and repeated phases *are* enumerated; verified by total `C(116,5)` and by the Tao control whose tuple has repeats |
| 23 | shared bin matching | `for(auto &B:Y[A.p.b[A.p.s]])` | A | Y indexed by the X shared bin; `covered` restricts to `i<=j<=l` buckets, valid because the tails are sorted |
| 24 | "Only finite proposed components … validity does not depend on how `v` was generated" | `supdual` reweights `ww[j]`, `reg[e]` over `dual=2` iterations | A | heuristic only; acceptance is one-sided, so omitted centres cost work not soundness |

**Direction audit (the specific assignment).** `s` vs `1+s` in supdual: **the source is
right and the suspicion is unfounded.** `J_Y`'s first column (the shared entry) is placed
in row `s` of `J*`, which is what (2.16) says: the Y block acts on `(h_s,h_5,h_6,h_7,h_8)`.
Two mutations were run as controls: moving that column to coordinate `0` and to
`s+1`. At F6 both raise the Y-block residual from `0.00704` to `0.3339`, i.e. `9.5×E`
— the test would have caught the bug. Note the Tao instance does *not* detect the `s+1`
mutation, because there `h_1=h_2=-1/6`: **the control set must contain a matrix whose
shared coordinate differs from its neighbours** (F4).

---

## 3. Controls on genuine exact Hadamard matrices

`src/jstar_control.py`, `src/controls_exact.py`. Two exact H(6):
Fourier `F6` (`P_jk=jk/6`) and Tao's Butson-type matrix (cube roots of unity); both
verified `HH*=6I` in exact roots-of-unity arithmetic, then dephased.

| | F6 | Tao |
|---|---|---|
| x phases | `0,1/6,1/3,1/2,2/3,5/6` | `0,0,1/3,1/3,2/3,2/3` |
| min gap over all 30 row/column pairs | `1/6` = `g_x` of row pair (0,1) | `1/3` = `g_x` |
| orientation `x1<=x5-x4` | equality | equality |
| admissible X bin tuples | `(18,37,55,74,93)`, `(18,37,56,74,93)` | `(0,37,37,74,74)` and the lift `(37,37,74,74,111)` |
| filters | **all accepted, 0 rejected** (4 X×Y assignments) | legal tuple **accepted**; the lift is rejected by (2.8a) |
| true `h` | `(1/6,-1/6,1/2,1/6,-1/6 \| -1/2,-1/2,1/2,1/2)` | `(-1/2,-1/6,-1/6,1/6,1/6 \| -1/2,-1/6,1/6,1/6)` |
| (2.14) | Y interval `(0.465396, 0.5]` contains `h_s=1/2` **as its endpoint** | both intervals `[-1/2,1/2]`, `h_s=-1/6` interior |
| (2.11) margin | `4.19e-5` | `5.57e-5` |

Why these two are the right controls: they contain **repeated phases** (Tao:
multiplicity 2 in all three values; F6: two tail values repeat), a phase **exactly on a
bin boundary** (F6: `1/2 = 56/112`, both closed bins admissible and both accepted), and
**exact displacements of modulus exactly `1/2`** (F6: `h_s=±1/2`; the true value sits on
the endpoint of the certified interval). Any inward rounding anywhere in (2.11)/(2.13)/
(2.14) breaks the F6 control. The Tao lift `(37,37,74,74,111)` (representing the phase
`0` by `1`) is *rejected* by (2.8a) — correctly, because it violates the arrangement
hypothesis `g_x = 1-x_5`; the legal representative is accepted, so completeness is not
affected.

The controls double as **test vectors** for the kernel checker (d3) and the dual/reuse
checker (d4): the F6/Tao tuples, their exact displacements, and the required verdicts.

---

## 4. Findings

**F1 (medium; soundness-neutral, affects the centre count). The bucket reach is
incomplete, so 249,878 is traversal-dependent.**
`K=int(R*n+.51)=4` and `covered()` scans `±1` bucket in the first three tail
coordinates, so a centre is tried only if `|floor(y/K)-floor(y'/K)|<=1`. With
`||k||²<=int(T)=25` a single coordinate can reach `|k_j|=5`, and there are **52**
tail-bin pairs with `|Δ|<=5` at bucket distance 2 (e.g. `3↔8`, `7↔12`), which the search
never reaches. This is *sound* — an untried centre only forces a fresh midpoint
(`3/224<R`) — but it means the retained-centre count is a property of this traversal,
not of the mathematics. Consequence for the certificate: the checker must **not**
reconstruct "the centre that should have absorbed this pair"; the obligation is
per-pair (either a fresh midpoint equal to the pair's own midpoint, or a certified
witness). Settled by: `src/constants_audit.py` output; the count itself by re-running
with `K=5`.

**F2 (low; robustness of the 1e-8 slack).** The (2.11) slack `+1e-8` is *not needed to
absorb floating-point error* — the evaluation error here is `~1e-14`, six orders smaller
(and the same holds for m2's independent kernel). It is nevertheless a
**count-determining constant**: the nearest *rejected* tuple `(0,8,52,60,63)` has exact
margin `-1.8909566e-8`, so a slack of `2e-8` would enumerate 22,830 tuples instead of
22,829. All 24 tuples with `|margin|<1e-6` were re-decided in rigorous intervals and agree
with the source. The audit conclusion is therefore: *the emitter's 22,829 is the exact
set*, but that is a computed fact about this `1e-8`, not a consequence of the error
analysis; a checker must decide (2.11) exactly and treat undecided cases as surviving,
and nobody should retune the slack while believing it only affects rounding.

**F3 (informational). The `1e-5` endpoint inflation makes the checked set a strict
superset of the exactly feasible pairs.** Smallest computed X-interval width is
`1.73955e-5`, i.e. some enumerated X tuples have an *empty* exact (2.13) interval and
survive only because of the `±1e-5` inflation (e.g. X `(0,22,48,70,71)`, `s=2`: the exact
interval has `lo=2.17 > hi=-1.37`, i.e. no feasible `h_s` at all). Sound (it only adds
work), but a checker running exact intervals will legitimately drop such pairs, so the
certificate's pair count will be *slightly smaller* than 151,744,086 and both numbers are
correct in their own arithmetic.

**F4 (low; control design). The `s+1` mutation is invisible on the Tao instance** because
`h_1=h_2`. Any control suite for the reuse side must include an instance with distinct
neighbouring displacements (F6 is such). Recording this because a mutation suite built
only from Butson-type matrices would silently pass a wrong `J*` row mapping.

**F5 (informational; provenance, corrected).** The archived
`execution/results/covrun.txt` line `N112 r0.0320 dual2 checked151744086 centers249878`
has five fields, while the tarball's `printf` emits seven (`visit near cheap lp` as well).
That is **not** evidence of a different source or binary: the archive is explicitly a
*curated subset* — `check_records.py`'s own docstring calls the material "data, cleaned
numerical result lines, and a minimal command record" and states that it "does not execute
any archived program or verify source, binary, or original execution provenance", and
`VERIFY.md` says the result files carry "only … mathematical arguments, completion/exit
facts, and numerical counters". A shorter line is an expected curation transformation.
The substantive point survives, and is the reason this audit exists: because the archive is
curated and expressly does not authenticate source, binary or provenance, the counter
`checked151744086` cannot stand on the archive's authority, and an independent
re-derivation is the right instrument — which is what §1 does, and it confirms the number
exactly. Also note what `checked` *means*: it counts pairs that survive (2.8b) and (2.14),
i.e. pairs for which the program owes either a reuse witness or a fresh centre. It is not
the number of coverage tests attempted (`near`/`visit` are those).

**F6 (informational, for the checker).** `|Y|=829,306`, not `5*|X|`. `ys[]` is built with
`sumok` only — no (2.7), no (2.8a) — so 169,194 5-multisets pass, and each distinct value
of each multiset becomes a shared bin. Any reconstruction of the traversal that starts
from the X list instead (my first attempt) undercounts pairs by `6.85×`
(22,151,402 instead of 151,744,086), while still reproducing 249,878 centres. The
certificate format must therefore carry the Y multiset **or** the rule "sumok only on
the Y side" explicitly.

---

## 5. What was executed

All under `.ultramath/smwgx3s1v/m6/`; each figure above is printed by one of these.

| artefact | what it does | output |
|---|---|---|
| `src/enum_x.cpp` | X enumeration from the paper's formulas; integer filters exact; `sumok` with plain `cos/sin`; near-tie list | `xs=22829`, near-ties → `logs/x_near.txt` |
| `src/paircount2.cpp` | full traversal reconstruction (X + Y + both pair filters), own `extend` | `checked 151744086` |
| `src/audit_sens.cpp` | exact integer form vs my binary64 re-expression, (2.8a) over all tuples and (2.8b) over all 178.3e9 pairs | 0 decision disagreements (§1a) |
| `src/gapstats.cpp` | (2.14) separation statistics, interval widths | `min separation 1.002e-8`, 59 pairs `<1e-6` |
| `src/audit_kernel.py` | MPFR-200 directed-rounding interval kernel: `e(x)`, `c,J`, (2.11), (2.13)/(2.14) | basis of the rigorous verdicts |
| `src/constants_audit.py` | RN2, certified radius, T, int(T), K, m, int8 range, bucket reach, all 24 near-ties rigorously | `logs/constants_audit.log` |
| `src/controls_exact.py` | F6 and Tao: exact Hadamard check, gaps, orientation, all admissible bin assignments through (2.7)/(2.8)/(2.11)/(2.14) | all legal assignments accepted |
| `src/jstar_control.py` | (2.16) `J*` elementwise equality with the code's `rows[]`; block residuals at F6/Tao; `s→0` and `s→s+1` mutations; Lemma 2.9 at a genuine point | mapping correct, mutations detected at F6 |
| `src/centres_audit.cpp` | audits the emitted `centers.txt` line by line against my own enumeration and the four filters; record invariants and file-order diagnostics printed on separate lines | `logs/centres_audit.log`: 0 misses/violations; order: 13,557 groups, 0 inversions vs the source key, 5,497 vs the auditor's key (§5b) |
| `src/expair_probe.cpp` | probes the source's own `expair` against MPFR at all 112 midpoints | `3.33e-16 < 2e-14`, A.2 confirmed |

Reproduce: `make -C src` is not needed; each file is standalone
(`g++ -O2 -o src/x src/x.cpp && ./src/x 112`, `python3 src/constants_audit.py`).

---

## 5b. Artefact-level audit of the emitted `centers.txt`

`src/centres_audit.cpp`, run on
`.scratch/h0/dl/verification/saved-run/execution/data/centers.txt` (7,339,546 B),
against my own enumeration. **Every check passes:**

| check | result |
|---|---|
| header `112 249878` vs line count | 249,878 lines, match |
| each line = 10 integers | yes |
| **record invariant**: X bins weakly increasing | **0 violations** |
| **record invariant**: tail bins weakly increasing | **0 violations** |
| X tuple ∈ my independent 22,829 | **0 misses** |
| Y tuple ∈ my independent `Y[a]`, `a = X[s]` | **0 misses** (829,306-set) |
| `s` = first minimiser of `|2b+1-N|` | **0 misses** |
| (2.7), (2.8a), (2.8b), (2.14) on every retained pair | **0 violations** |
| duplicated (X bins, tail bins) pair | 0 |
| **file order**: X groups | 13,557 ( = the number of distinct X tuples) |
| **file order**: inversions against the source's traversal key `(e,d,c,b,a)` | **0** |
| **file order**: inversions against the auditor's set key `(a,b,c,d,e)` | 5,497 (expected, see below) |

**On the 5,497.** This number is an *ordering* diagnostic and says nothing about any
record. The source visits X tuples with `e` as the outermost loop
(`F(e,n)F(d,e+1)F(c,d+1)F(b,c+1)F(a,b+1)`), so its visit order is lexicographic in
`(e,d,c,b,a)` — the *reverse* of the natural `(a,b,c,d,e)` key, which is how my
`std::set<std::array<int,5>>` orders the same 22,829 tuples when I index them. Comparing
consecutive file lines against the auditor's own index therefore reports a "decrease"
whenever either key's next tuple steps backwards in the other key; with 13,557 groups
that happens 5,497 times. Checked against the correct key the file has **0 inversions**:
the centre list is in exactly the source's traversal order, grouped, with equal X tuples
contiguous (13,557 groups for 13,557 distinct tuples). That is the property the
certificate needs — "previously retained" is a prefix of the file — and it is what the
explicit extra line above records. No record is malformed, mis-sorted, out of range, or
duplicated: the record-level counters are all zero and are printed on their own line
(`record invariants: …`).

Statistics that matter for the certificate (all measured, not read):

* 249,878 centres arise from **13,557** of the 22,829 X tuples (mean 18.4, max 278
  centres per X tuple); the other 9,272 X tuples produced no centre, i.e. *every* one of
  their checked pairs must carry a reuse witness. That is the load the witness stream has
  to bear, and it is a per-X-tuple property a checker can use to bound its own work.
* Centre list is **contiguous by X tuple** (13,557 groups = 13,557 distinct tuples),
  so "previously retained" is a prefix property of the file.
* **9,482 centres (3.8%) have a repeated X bin**, and 29,889 (12%) a repeated tail bin.
  So the weak (non-strict) enumeration is load-bearing for ~3.8% of the centre list: an
  enumeration over *strictly* increasing bins — the reading I first made of
  `F(a,b+1)F(b,c+1)…` — would have silently lost them, and with them the coverage of
  every exact solution whose phases repeat inside a bin.
* `s` distribution: `s=1`: 675, `s=2`: 242,295, `s=3`: 6,908; `s=0` and `s=4` never
  occur. (`s=0` is impossible under (2.7): it forces `a=56=e` and `a<=l-d+1` fails.)
  Since reuse requires equal `s`, the 97% concentration at `s=2` is why the reuse rate is
  high; nothing in the proof depends on it.
* **The 59 tightest (2.14) rejections are all genuine in exact arithmetic.** For every
  pair with computed separation `<1e-6` the exact (2.13)/(2.14) intervals were recomputed
  in MPFR:`0` failures, and no source endpoint is inward past the exact one
  (`logs/tight14.txt`, `logs/tight14_verify.log`). So the outward margins do the job they
  are claimed to do at exactly the places where it matters; the smallest real separation
  is `1.002e-8`.
* A.2's `expair` premise, probed from the source's own function over all 112 midpoints
  (`src/expair_probe.cpp`): max `|expair - e((b+1/2)/N)| = 3.33e-16`, against the stated
  bound `2e-14`. Confirmed with 60× margin.

Cross-check: member m2 (d3), with a completely different kernel (integer fixed point,
Machin π), independently obtained `|X| = 22,829` and `|Y| = 829,306` by set equality with
the upstream enumerations, and the same tightest (2.11) margin `5.296e-8` at
`(1,18,57,57,74)`. Two independent kernels, same sets.

**F7 (high *for the checker design*; the source is fine). Both gap inequalities are
exactly tight on the data, so a checker must not recompute them in floating point.**
Measured (`src/tightness.cpp`): the minimum slack of (2.8a) over the 22,829 accepted X
tuples is **exactly 0**, at X `(0,0,56,56,57)` (`G=112=2(N-l+1)`); the minimum slack of
(2.8b) over the pairs that survive it is **exactly 0**, attained by **7,645,275 of the
190,192,620** gap-accepted pairs (e.g. X `(0,0,55,55,55)`, Y `(55,0,0,55,57)`,
`G_y=110=2(N-l-2)`). This makes T5's earlier observation ("the live comparison has zero
analytic slack") a measured fact, not a remark: the paper's (2.8) is tight, because
Lemma 2.5's allowance `2δ=w` is consumed with equality whenever phases sit at bin
boundaries — which they do (F6's `h=±1/2`). Consequences:

* the source is **correct**: its `+1e-8` is on the keeping side of the comparison, and at
  an exact tie `g+1e-8 < thr` and `g > thr+1e-8` are both false, so ties are kept;
* a checker that recomputes `1-(l+2)/N` in binary64 (or with a different operation
  order) can land `1e-16` above the exact threshold and then **reject a feasible pair**,
  i.e. break Prop 2.10's completeness, on up to 7.6M pairs. The exact comparison is an
  integer one: `G_y >= 2(N-l-2)` and `G <= 2(N-l+1)` with
  `G = max(2a+1, 2N-2l-1, 2·consecutive bin gaps)`. Use it, or relax outward by a
  stated positive margin.

## 5c. Contract the emitter and checkers must satisfy (hand-off)

Derived from the tests above, not from the prose. Coordinates: `q = (x_1..x_5, y_2..y_5)`
with the five X bins weakly increasing in the stored order and the four tail bins weakly
increasing; `s` = first minimiser of `|2b_s+1-N|`, recorded per centre.

**Obligation per bin pair** (this is what Prop 2.10 needs, and it is all it needs):

> For every pair `(X tuple, Y tuple)` with `Y.b[0] = X.b[X.s]` that survives the exact
> necessary filters, either (a) the pair's own rational midpoint is present in the centre
> list (then the whole 9-box is covered by radius `3/224 < 0.032`), or (b) the maker
> supplies a reuse witness `(earlier centre ordinal, same s, cheap|dual, and for dual the
> four exact rational components of v)` verified by (2.17)+(2.18) or (2.19).

A pair may be *dropped* only with an exact violation of a necessary condition:

| filter | exact form the checker must use | ties |
|---|---|---|
| (2.7) | `X.b[0] <= X.b[4]-X.b[3]+1` | integer, no tie issue |
| (2.8a) | `G <= 2(N-l+1)` | **exact ties exist** (F7); keep on equality |
| (2.8b) | `G_y >= 2(N-l-2)` | **7,645,275 exact ties** (F7); keep on equality |
| (2.11) | 6 directions, rigorous enclosure of `(w/2)Σ|v·J_j| + 5πw²/4·‖v‖ - |v·c|` | 24 near-ties, listed in `logs/x_near.txt`; if undecided, **keep** (then a witness is owed) |
| (2.13)/(2.14) | interval per direction with support coefficient **1/2**; drop only on strict disjointness of the exact intervals | tightest real separation `1.002e-8` |

Do **not** reproduce the source's `1e-8`/`1e-5`/`1e-7` slacks as if they were part of the
mathematics: they are its outward devices. Reproduce the *decisions* they implement (this
audit shows the exact decisions equal the source's on every tuple and every pair), or
relax outward with your own stated margin.

**What the emitter must therefore record** (beyond the centre list): per checked pair its
identity `(X bins, s, tail bins)` — or the pair ordinal in a *specified* enumeration order —
plus, when the pair is covered, the retained-centre ordinal and the witness. Recording only
the *covered* pairs is enough for the checker to reconstruct the checked set only if the
enumeration order and the filters are pinned; my advice is to record all `151,744,086`
(≈ 10 bytes/pair in a compact encoding, i.e. ≤ 1.6 GB, or store a 2-bit-per-pair bitmap
over a canonical pair indexing) rather than to rely on re-deriving the filters. Note
`|Y| = 829,306`, **not** `5·22,829` (F6), and the Y side applies `sumok` only.

**Facts the checker may rely on** (all measured here): `|X| = 22,829`;
`|Y| = 829,306`; `checked = 151,744,086`; the centre file has 249,878 records, contiguous
by X tuple, each a legitimate member of both enumerated sets with the correct `s` and all
four filters satisfied; per-X-tuple centre counts run 1..278 (mean 18.4) over 13,557 of
the 22,829 tuples, so 9,272 X tuples carry witnesses for *all* their checked pairs.



## 6. Where the paper's text and the source disagree (and where they do not)

Everything in §2 that I could test agrees, with three qualifications that are *paper*
issues rather than code issues:

1. The archive is a *curated subset*: its result files carry "cleaned numerical result
   lines" (`execution/check_records.py` docstring) and, per `VERIFY.md`, only
   "mathematical arguments, completion/exit facts, and numerical counters". So the five-field
   `covrun.txt` line is a curation format, not a second program's output, and no counter in
   it is self-authenticating — which is exactly why §1 re-derives them. (Corrected from an
   earlier framing that treated the shorter line as a source/binary mismatch; it is not.)
2. F2/F3: A.3 justifies the margins by error budget, but the margins are also doing
   enumeration work at the `1e-8`/`1e-5` scale (one tuple at 1.9e-8, 59 pairs at
   `1e-6`). The paper's phrasing "the numerical gap comparisons include outward slack"
   is right, but the certificate should not inherit the same slack: it must re-decide.
3. A.3's `pow(x,2)` lowering is an explicit build premise. I confirm the *arithmetic*
   (`RN2 = (NR)²-1e-4`, certified radius `0.031999875 < 0.032`) but not the lowering.

---

## 7. Not done, not verified

* The retained-centre side: no reuse witness `(2.18)/(2.19)` on real data, and no check
  that the 151,744,086 pairs are covered. What I *do* now verify about the artefact is
  that every one of the 249,878 centres is a legitimate member of my own enumerated X and
  Y sets, carries the correct `s`, and passes all four necessary filters (§5b) — i.e. the
  fresh-midpoint half of Prop 2.10 is consistent with the documented filters, and the
  remaining obligation is exactly "every checked pair has a witness or is a centre".
  That is d3/d4/d5 work.
* Lemma 2.9's inequalities were evaluated at two genuine points (`2k·h` vs the (2.19)
  right side) but not proved, and `supdual`'s *evaluated* bound was not compared against
  the true `2k·h` on the real traversal.
* `expair`'s Taylor/argument-reduction error bound (A.2: complex error `<2e-14`) was probed
  numerically at all 112 midpoints (`src/expair_probe.cpp`: max `3.33e-16`), but that is a
  measurement over the arguments actually used, not a proof of the stated bound, and the
  argument-reduction path for other phases is not exercised.
* Bit-level identity with the recorded binary's own arithmetic is **not** established
  (§1a): my comparisons are decision-level and use an independent `cos/sin`. A whole-file,
  independent full comparison is the lead's background `audit_sens` run; until it reports,
  "the source's expression sequence yields these decisions" rests on decision-level
  agreement plus the margin measurements, not on operation-order identity.
* No disassembly of the recorded build; no Lean; no re-run of `covrun` (the lead's 401.82 s
  byte-identical `centers.txt` reproduction is taken as given).
* N was only exercised at 112 (the audit needs `N=112`; `int8_t`, `K`, `T` were checked
  as functions of N).
