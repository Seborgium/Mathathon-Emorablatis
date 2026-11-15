# Stage-B transported-frame closure of the fallback ledger (bad10#0)

**Direction d2 — Stage-B merge/transport witnesses.**
Member m3, swarm smwh5efk8. Everything below ran in this VM; commands, logs and
machine-readable output are listed in §8.

**Outcome in one line.** The 1452 boxes that
`work/02-checker/reports/H2-interval-prototype.md` reports as UNRESOLVED are not an
evidence gap. They are an artefact of testing **only the identity transport map**:
with all 2,073,600 transport maps of the paper's own map group and the fallback
atlas as children, parent `bad10#0`'s base grid closes **completely** —
`14641 = 11480 outside + 3161 relation-covered + 0 open` — with 902 certified
edges, exact rational arithmetic, tightest margin `ell^2 - t_B^2 = 1.968e-9`.
No merge mediator and no subdivision is needed for this parent.

Three defects in the reused harness are also established (§3), one of which
changes a published number (1709/1452 becomes 1753/1408 under the correct child
set, before any transport map is used).

---

## 1. What was asked and what is claimed

Direction 3 of the task list: *"produce merge-mediator data or relation directions
to close at least one of the 1452 currently unresolved boxes in the bad10#0
ledger … validate the exact relation/cover arithmetic, not only op counts … if no
feasible witness exists, report that as unresolved and do not fake it."*

Claimed here:

* **C1.** All 1408 boxes left open by the corrected identity-only ledger of
  `bad10#0` are closed by certified transported-frame relations, exactly.
  (§5, §6; independently re-verified in §6.2 from a file.)
* **C2.** The closure is carried by exactly **5** non-identity maps, and those
  5 maps are near-stabilisers of the parent's dephasing class
  (`||dq(P, Phi P)||` between `3.2e-4` and `4.3e-3`, i.e. 6x-85x below the
  admissibility cut, while the stored phase vectors differ by up to 0.74). (§5.2)
* **C3.** The published split 1709 covered / 1452 unresolved is not the correct
  identity-only ledger. The prototype's `cluster()` keeps the *contiguous prefix*
  of admissible children and stops at the first gap; for `bad10#0` that is 66 of
  **158** admissible fb1 records, and the correct identity-only ledger is
  **1753 / 1408**. (§3.3)
* **C4.** The mechanism is real but not universal: on two other fallback parents
  it closes 1952/2000 and 1445/1620 boxes and leaves 48 and 175. Those residuals
  are reported as unresolved with their exact deficits; no cover is faked. (§7)

Explicitly **not** claimed: anything about Stage A, Stage C, Root beyond the exact
parts R1/R2/R4 (§6.4), any of the other 160 fallback parents, or `N(6)=3`.

---

## 2. The object being checked (unchanged conventions)

From `work/02-checker/src/root_interval/stageb.py` (vendored read-only in `base/`):

```
dq  = Pi( wrap( dp(Phi Q) - dp(P) ) )                       (5.5)
Pi  = double centring (drop row, column and grand means)
edge (Q, Phi) is admissible  <=>  ||dq|| <= min(.23, R + tau + 1e-6),  tau = 0.011
certified object (edge, ell):  D^(ell) <= a_Q              (Lemma 5.5, 5.17)
box b: u = b*w, h = w/2, w = 0.0038, L = 5, n = 11, k = 4
  OUTSIDE   iff  sum_a max(|u_a| - h, 0)^2 > (sqrt(1+ort)*R + 1e-7)^2       (5.20)-(5.22)
  COVERED   iff  exists edge: sum_a (|u_a - eta_a| + h)^2 <= ell^2           (5.24)
  else UNRESOLVED
```

`eta = T_P^* dq`; `D^` is the fixed-point function of (5.14)-(5.16). Monotonicity
of `D^` is never used — only the single verified value at `ell`, exactly as in the
prototype. `t_B(box)^2 = sum_a (|u_a - eta_a| + h)^2` bounds `sup_{t in box} ||t - eta||^2`
by the triangle inequality, so the centre-plus-half-width test is sound for the
whole box.

A transport map is `Phi = (row[6], col[6], trans, neg)` acting on the 6x6 stored
phase array exactly as `align.transform` does; there are
`2 * 2 * 720 * 720 = 2,073,600` of them. `Phi Q` is a solution centre: the map
group (signed row/column permutations, transpose) is a symmetry of the MUB
conditions, so if the ball of radius `a_Q` around `p_Q` contains a solution then
the ball of radius `a_Q` around `Phi p_Q` contains one too. `Phi Q` is *not* in the
stored atlas — see §9 item 1 for the obligation this leaves.

---

## 3. Defects found in the reused harness (all reproducible)

### 3.1 The promoted Stage-B code does not import

`work/02-checker/src/root_interval/rootcheck.py` does `import records as R` and
`from derive import Qbasis, PI36, fullL`; neither module exists anywhere in the
repository (`rg --files | rg '(records|derive)\.py$'` → no hit). `stageb.py` does
`from rootcheck import proj_rat, _scale`, so
`python3 work/02-checker/src/root_interval/stageb_run.py` fails at import with
`ModuleNotFoundError: No module named 'records'`. The copy that actually produced
the H2 numbers is the self-contained `.ultramath/smwgx2sv0/m5/` (its `rootcheck.py`
defines `proj_rat` and `_scale` itself, and needs only `rec/num/sourceM/root_float`).
This report vendors that copy into `base/` unchanged; **no file outside this
directory was modified.**

### 3.2 `align.best_map` is not the certified distance for maps that move index 0

`best_map` evaluates `Pi(wrap(+-dpQ[row_i, col_j] - dpP))`, i.e. it keeps the
*parent's* dephasing anchor (index 0) while permuting the child. The certified
quantity re-depasses the transported child at **its own** anchor `(r[0], c[0])`.
The two agree only when `r[0] = c[0] = 0`. Consequence: the banked record
`certdata/runs/h1-root-interval/stageb_parent0.json` marks
`"identity": true` for children `#0..#5`, but under the exact convention child
`#4` has a non-identity map with `||dq|| = 0.016833 < 0.018783` (identity) and
child `#7` has `0.018737 < 0.021782` (log `logs/selftest.log`, T1a). This is a
*proposal*-step defect, not a soundness defect — every verdict in this report is
recomputed from `stageb.Relation` with the explicit map — but it means the
prototype's statement "identity is optimal" was never established.

### 3.3 `stageb_run.cluster` discards admissible children

`cluster()` appends while the identity distance `<= cut` and **breaks at the first
child that does not** (`elif out: break`). The fb1 list is not sorted by
proximity to a given parent, so this is a prefix heuristic, not a cluster:

| parent | children within the cut | `cluster()` keeps |
|---|---|---|
| bad10#0 | 158 | 66 |
| bad10#1 | 74 | 24 |
| bad10#2 | 103 | 2 |

For `bad10#0`, records 0..65 are admissible, record 66 has identity distance
0.0391, and 92 records *after* 66 are admissible again. Re-running the identity
ledger with all 158 gives **11480 outside / 1753 covered / 1408 unresolved**
instead of 11480 / 1709 / 1452. Both numbers reproduced in this report
(`logs/repro.log` for 66 children, `logs/witness.log` for 158).

---

## 4. The exact reduction that makes the scan cheap

For a stored 6x6 phase array `X` write `Z_X(u,v) = X_uv - X_u0 - X_0v + X_00` (raw
double difference, in cycles). For `Phi = (r, c, t, s)` with anchor `(a,b) = (r[0], c[0])`,
`B = Q` or `Q^T`, and `M(u,v) = B_uv - B_ub - B_av + B_ab`:

```
  dp(Phi Q)(i,j) = s * wrap(M(r_i, c_j))
  ==>  wrap( dp(Phi Q)(i,j) - dp(P)(i,j) ) = wrap( s*M(r_i,c_j) - Z_P(i,j) )      (*)
```

independent of the integer-lift conventions. Because the anchor is fixed per map,
grouping the 2,073,600 maps by `(t, a, b)` gives 144 blocks of 120x120 permutation
pairs, each a fixed 6x6 matrix `M` against `Z_P` — one `numpy` contraction, no
Python loop over maps. `(*)` is asserted against the slow exact path
(`align.transform` + `stageb.dephase`, `Fraction`s) on 120 random maps:
**max entrywise difference 1.2e-16** (`logs/selftest.log`, T2), and the identity
map reproduces `stageb.Relation.dq` to **1.2e-16** for every child (T1a).

Cost: **0.8 s per child for all 2,073,600 maps** (single core), i.e.
158 children in 70 s on 3 processes.

The float scan only *proposes*. Every proposed `(Q, Phi)` is rebuilt with
`align.transform` and `stageb.Relation` in exact rational arithmetic, and the
threshold `ell` is found by the prototype's own `certified_threshold`
(largest bisected `t` with `D^(t) <= a_Q`, verified value at that `t`). In the
66-child run, **0 of 792** proposals were rejected by the exact recomputation, and
the float-to-exact agreement is `1.6e-16` in `||dq||` (§6.3), so the probe cut
`0.06` (2.2x the admissibility cut) cannot have hidden an admissible map.

---

## 5. Results — parent `bad10#0`

### 5.1 Two child pools, identity map only

| pool | children | outside | covered | unresolved | edges |
|---|---|---|---|---|---|
| prototype `cluster()` prefix | 66 | 11480 | 1709 | 1452 | 66 |
| all fb1 within the cut | 158 | 11480 | **1753** | **1408** | 158 |

### 5.2 All maps, 158 children — the grid closes

* scanned: `158 x 2,073,600 = 327,628,800` (child, map) pairs, complete over the
  map group for this child set.
* admissible edges: **902** (`||dq|| <= 0.0270001` and `D^(ell) <= a` exact).
* full grid classification: **`14641 = 11480 outside + 3161 covered + 0 open`**.
* boxes closed that the identity map missed: **1408 / 1408**.
* closure margins `ell^2 - t_B^2` over those 1408: min `1.968e-9`,
  median `2.541e-5`, max `1.054e-4`. In `t_B` units over the 66-child run:
  min `9.0e-8`, median `1.25e-3`, max `7.15e-3`.
* the tightest box in the whole grid is `(2,0,2,-4)` at `ell^2 - t_B^2 = 1.968e-9`,
  i.e. `ell - t_B >= 8.9e-8` — five orders above the arithmetic's own
  `2^-B` fixed-point resolution, so nothing here needs precision escalation.

### 5.3 Which maps do the work

Over the 66-child pool, only **5** non-identity maps are ever the covering edge:

| map `(row, col, trans, neg)` | boxes closed | `\|\|dq(P, Phi P)\|\|` |
|---|---|---|
| `(2,5,0,4,3,1) (1,0,3,2,5,4) 0 1` | 486 | 0.003937 |
| `(3,4,5,0,1,2) (5,2,1,4,3,0) 0 1` | 394 | 0.004253 |
| `(1,0,4,5,2,3) (3,4,5,0,1,2) 0 1` | 272 | 0.000316 |
| `(5,2,3,1,0,4) (2,5,4,1,0,3) 0 0` | 201 | 0.004105 |
| `(4,3,1,2,5,0) (4,3,0,5,2,1) 0 0` | 99 | 0.004105 |

Each is admissible for all 66 children (the fourth column is `||dq||` of the map
applied to the **parent itself**, `Pi(wrap(dp(Phi P) - dp(P)))`). For scale: the
identity distance of a typical child is `0.016-0.022`, and `dp(P)` itself has
`max|dp| = 0.4999`. So these five maps fix the parent's *dephasing class* to
within `3e-4 .. 4.3e-3` — 6x to 85x below the admissibility cut — while the
stored phase vectors differ by `max|Phi p - p| = 0.59 .. 0.74`. The invariance is
in the double differences, not in the stored representation, and the five
transported images of a child are **5 distinct centres** (max deviation
`0.588 .. 0.743`), not the same point repeated.

Interpretation: the atlas contains, besides the 158 stored children of `bad10#0`,
five more near-copies of that child cluster obtained by the stabiliser-like maps
above. Their `eta` vectors point in different directions, and it is exactly those
directions that the 1452 boxes needed. This is mechanism 2 of the H2 report
("transported-frame relations") and it is what the source's
`preload`/`variants(P, .061, 1, ...)` lookup does; the prototype's ledger simply
never exercised it.

---

## 6. Verification — every number re-derived cold

`logs/verify_closed.log`, `logs/crosscheck_float.log`, `logs/witness.log`,
`logs/complete_witness.log`.

1. **V1** all 205 distinct edges used by the 1452 closures of the 66-child run were
   rebuilt from `fb1.bin` with a fresh `stageb.Relation`: `||dq|| <= cut` and
   `D^(ell) <= a` hold exactly, `dq`/`ell`/`eta` bit-identical to the scan.
2. **V2** all 1452 box inequalities re-decided exactly from the re-derived `eta`:
   **1452/1452 pass**, tightest `ell^2 - t_B^2 = 1.968e-9`.
3. **V3** identity-only edge set reproduces `11480 / 1709 / 1452`.
4. **V4** controls. `C1`: for the 40 *tightest* closures, between **2 and 12** of
   the 418 admissible edges close the box (median 5) — the cover is a genuine
   union, not "everything covers everything". `C2`: shrink `ell` by `1e-3` →
   **0/40** survive. `C3`: empty edge set → `0` covered, 3161 unresolved (so no
   box is covered by default). `C4`: `eta_0 += 2e-3` on the used edge → 31/40
   still close, because most boxes have a second covering edge; recorded as a
   weak control, not as evidence.
5. **V6** the independent binary64 port `base/relfloat.py` (written from the C++
   only, shares no code with the exact kernel) agrees on all 205 edges:
   `|dq|` to `1.6e-16`, `D^(ell)` to `6.06e-8` (the port's own `1e-8` pads), and
   confirms `D^(ell) <= a` on **205/205**. This is the check that previously
   caught a missing square root in `spectral_upper`.
6. **V5** transport does not destroy the child's Root status: for three used
   edges, `rootcheck.exact_part` (R1 `||T*T-I||`, R2 `||(I-Pi)T||`,
   R4 `n0 >= mnorm*froot`, all exact) returns the **same verdicts and numerically
   identical slack** before and after the transport.
7. **Cold file check** (`logs/witness.log`): `out/witness_bad10_0.json` re-read
   from disk, all 902 edges rebuilt from `fb1.bin`, `dq`/`ell`/`eta` equal as
   exact rationals, `D^(ell) <= a` for all, then all 3161 box closures re-decided
   exactly: **failures 0**, `open_boxes` empty,
   `11480 + 3161 + 0 = 14641`.

---

## 7. Other fallback parents (same pipeline, complete over fb1 x all maps)

| parent | children (cut / prefix) | identity: covered/unresolved | closed by transport | still open | worst remaining deficit |
|---|---|---|---|---|---|
| bad10#0 | 158 / 66 | 1753 / 1408 | **1408** | **0** | — |
| bad10#1 | 74 / 24 | 1161 / 2000 | 1952 | 48 | `7.97e-3` |
| bad10#2 | 103 / 2 | 1541 / 1620 | 1445 | 175 | `9.01e-3` |

Deficit = `t_B - ell` of the best available edge; `sqrt(t_B^2-ell^2)` values.
So the mechanism closes one parent completely and two others mostly: it is a real
covering mechanism, not a per-parent accident, and it is **not** sufficient in
general. The 48 and 175 residuals are genuine open obligations and are *not*
covered by anything produced here.

---

## 8. What ran (all times `/usr/bin/time`-style user+sys from the shell)

| command | wall | output |
|---|---|---|
| `python3 repro.py` | 4.0 s | `logs/repro.log` — reproduces 11480/1709/1452 |
| `python3 selftest.py` | 7.5 s | `logs/selftest.log` — reduction (*) to 1.2e-16, map census, 0.8 s/child |
| `python3 scan_all.py cluster 3` | 34 s | `logs/scan_cluster.log`, `out/scan_cluster.json` |
| `python3 verify_closed.py` | 9.6 s | `logs/verify_closed.log` — V1-V5 |
| `python3 crosscheck_float.py` | 5.2 s | `logs/crosscheck_float.log` — V6 + map census |
| `python3 generality.py` | 81 s | `logs/generality.log` — the 5 maps as parent stabilisers |
| `python3 ledger_all.py 3 0,1,2` | 180 s | `logs/ledger_all.log`, `out/ledger_all.json` |
| `python3 witness.py 3` | 122 s | `logs/witness.log` — 902 edges, cold check |
| `python3 complete_witness.py` | 30 s | `logs/complete_witness.log` — full 3161-box accounting |

Code: `base/` (vendored prototype, unmodified) + `m3lib.py`, `transcan.py`,
`repro.py`, `selftest.py`, `scan_all.py`, `verify_closed.py`,
`crosscheck_float.py`, `generality.py`, `ledger_all.py`, `witness.py`,
`complete_witness.py`.  Artifacts: `out/*.json`, `logs/*.log`.

## 9. Witness schema — the precise handoff

`out/witness_bad10_0.json` (`schema: stage-b-transported-edge-v1`):

```
parent : {file, index, k, R=[num,den], w, tau, C, n0, id, ort, hor, mnorm, froot}
grid   : {L, n, boxes, rule}
edges  : [{ child_file, child_index,
            map = [row[6], col[6], trans, neg],
            ell  = [num,den],          # certified: D^(ell) <= radius
            radius = [num,den],        # a_Q
            dq   = [num,den],          # ||dq||, for the admissibility test
            eta  = [[num,den] x k],    # T_P^* dq
            dhat = [num,den] }]        # D^(ell), i.e. the verified bound
boxes  : [{ idx = [int x k], edge = <index into edges> }]
open_boxes : []                        # every leftover box, never dropped
accounting : {grid, outside, covered, open}
check  : {outside_rule, cover_rule, edge_rule}
```

Checker obligations, all exact rational except the records themselves:
recompute `dp`, `Pi`, `dq`, `eta`, `D^(ell)` from `(p, T)` plus `map`; verify
`||dq|| <= min(.23, R+tau+1e-6)` and `D^(ell) <= radius`; verify the outside rule
on every slot; verify `sum_a (|u_a-eta_a| + w/2)^2 <= ell^2` for every
`(box, edge)` pair; print any slot in none of the three classes. Size as written
1.08 MB (902 edges + 3161 boxes); **only 303 of the 902 edges are ever
referenced**, so a minimised file is ≈0.3 MB for this parent. Per the H2 report's
own size estimate (≈60 B/edge, ≈300 B/merged box) this replaces the estimated
87 kB of merge records for this parent by 0 merge records and a per-parent list of
stabilising maps.

**What the schema must carry that the prototype's does not**: the `map` field on
every edge, and the per-parent list of maps that must be tried. Without them a
checker that tests identity only re-derives 1408 spurious UNRESOLVED boxes for
`bad10#0` — which is exactly what happened.

## 10. What this does not establish, and what is still open

1. **Chain transport is not done.** `Phi Q` is a solution centre (the map group is
   a symmetry of the MUB conditions, and V5 shows the exact Root obligations are
   invariant), but `Phi Q` is *not* an archived record, so the downward chain
   needs `Phi Q`'s own Stage-B ledger, obtained by applying the same map to `Q`'s
   edges. That is mechanical and I did not run it. Until it is run, the 3161
   covered boxes are a *cover* statement, not a completed obligation ledger.
2. **Only fb1 children were scanned** (1127 records, all `k=4`, `a ≈ 0.011`).
   `mid` (`a = 0.07`), `fine` (`a = 0.016`) and `coarse*` (`a = 0.125`) records are
   admissible as covering centres in principle and would, if any of their orbits
   lay within the cut of a parent, close much larger regions. The full
   `~27,000 records x 2,073,600 maps` scan is ≈16 CPU-hours in this Python; it was
   not attempted. The 48/175 residuals of §7 are therefore "unresolved over
   `fb1 x all maps`", not "unresolved".
3. **Only 3 of 163 fallback parents** were measured, and `split 0` in the run
   means every B discharge is a base box, so nothing here needs a subdivision tree
   — but this was verified only for those 3.
4. **No merge mediator was needed** for `bad10#0`, so this report does not produce
   one. It does give the exact criterion that would be needed if the transported
   edges were unavailable: a box with `t_B > max_Q a_Q ≈ 0.011` cannot be closed by
   any relation at all, and with `ell <= a_Q (1+ort/2)^{-1}` the count of boxes that
   are *relation-closable in principle* is those with `t_B <= a_Q`.
5. **Nothing about Stage A, Stage C, Root transitively, or `N(6)=3`.** The Root
   evidence is untouched except for the R1/R2/R4 invariance check in §6(6).

### Two asks for the H2/H3 spec, in priority order

* Make `(map, ell)` the Stage-B edge witness and emit, per parent, the list of
  maps the atlas lookup actually used — otherwise the checker cannot tell a
  missing witness from a missing cover. Store `ell` and `eta` as exact rationals
  (`num/den`), not as binary64: the tightest decision here is `1.97e-9` in
  `ell^2 - t_B^2` and is only comfortable because the arithmetic is exact.
* Replace `stageb_run.cluster`'s `elif out: break` by a full scan of the record
  list. It costs 0.1 s per parent and for `bad10#0` alone it moves 92 admissible
  children back into the ledger (1709/1452 → 1753/1408 before any transport map).
