# C-REPORT — d6 clean-room probe: 112-bin seed enumeration

**Bottom line.** The manuscript's prose is sufficient to reproduce the 112-bin
seed enumeration exactly: count, membership and order. `xs` comes out 22 829,
the same number the recorded run printed (`xs22829`, `.scratch/gh/covrun.log`
line 1), and the enumeration order `(l,d,c,b,a)` reproduces the recorded file's
`(t, position in ys)` order over all 249 878 lines, including the run's own
cumulative centre counters. None of this was read out of `seed.cpp` or
`covout.cpp`.

## Command and status

    .ultramath/smwgt1mbm/m5 $ ./c-run_d6.sh > ms/run_d6.log 2>&1; echo "EXIT_STATUS=$?"
    ...
    == 6. whole-file tests against the recorded centres
    lines 249878  |xs| 22829  |ys| 368732
    errors {'xs': 0, 's': 0, 'gap2': 0, 'ys': 0, 'order_t': 0, 'order_y': 0, 'count': 0}
    run log t0      centres       5 (recorded       5) ok
    run log t10000  centres   72679 (recorded   72679) ok
    run log t20000  centres  205716 (recorded  205716) ok
    == 7. the forward nesting must be excluded: t-order violations > 0
    forward-nesting t-order violations: 5497
    forward nesting excluded (status 1)  [ok]

    RESULT: PASS
    EXIT_STATUS=0

Full transcript: `ms/run_d6.log` (68 s wall, one core).
## What each check establishes

| check | evidence | result |
|---|---|---|
| `｜xs｜` equals the published count | `sed -n 's/^xs\([0-9]*\) build.*/\1/p' covrun.log` = 22829 | 22 829 = 22 829 |
| every recorded X tuple is in `xs` | 13 557 distinct tuples in `centers.txt` | 0 missing |
| `s` rule | first minimiser of `｜2q_s+1−N｜` | 0 mismatches in 249 878 |
| Lemma 2.6 second gap | `gy_mid ≥ 1−(l+2)/N` on the stored shared-first tail | 0 violations |
| every recorded tail is in `ys` | 76 993 distinct `(h,y)` pairs | 0 missing |
| the order | `(t, ypos)` strictly increasing | 0 violations |
| the order, independently | the run's counters at t = 0, 10 000, 20 000 | 5, 72 679, 205 716 — all exact |
| the wrong order is excluded | lexicographic nesting | 5 497 violations |

## What the prose carries, and what it does not

The prose carries the mathematics completely: every filter, both gap
inequalities, the `sumok` inequality with its coefficient and its 10⁻⁸ margin,
the rule for `s`, and the enumeration's specification ("every weakly increasing
five-bin X tuple"). My implementation needed no source and no guessed constant.

It does not carry three things, and only one of them matters:

1. **The loop nesting (OPEN‑3).** "nested ascending loops" reads as
   lexicographic; the code runs the last coordinate outermost. This is invisible
   to a count check and fatal to byte-identity — 5 497 of 249 878 lines move.
   Of 120 permutations exactly one fits; of the 24 tail permutations exactly one
   (`y4,y3,y2,y1`) fits. Cost of getting it wrong: a correct `xs` and a permuted
   7.3 MB file.
2. **The direction set of `sumok` (OPEN‑1).** The prose says "the residual
   direction and directions perpendicular to the five unit-exponential
   columns". That sentence is load-bearing: residual only gives 30 401,
   perpendiculars only 22 838, both 22 829.
3. **Arithmetic.** `expair` vs libm `cos`/`sin`, and the 10⁻⁸ slack, change
   nothing at this grid (0 vs 10⁻⁸ slack: 22 829 both ways; A.2 bounds the
   exponential difference by 2·10⁻¹⁴). The enumeration is robust to the
   binary64 contract; that is a *result* about this stage, and it does not
   extend to the stages that read real-valued records.

## Handover notes

* **Unit 03 (`seed`)**: `ms/xs_ordered.txt` (`a b c d l s`, 22 829 lines) and
  `ms/ytails_ordered.txt` (`h y1 y2 y3 y4`, 368 732 lines) are fixtures to
  regress a re-derived `seeds::build` against, with `c-ordercheck.py` as the
  test. The enumeration order is part of the contract, not an implementation
  detail.
* **Unit 04 (`covout`)**: the seed enumeration does not produce the centre
  count. All 22 829 X tuples — including the 9 272 that no centre uses — have a
  Y tail passing the second gap inequality, so those 9 272 fall to `extend`'s
  interval intersection. That is where a centre-count discrepancy will come
  from.
* **Spec defect (CR candidate)**: `spec/interfaces.md` §5 item 1 describes the
  enumeration as "(a,b,c,d,e) in nested ascending loops", which under-determines
  `t`. It should read: ascending with `e` outermost, i.e. `(e,d,c,b,a)`.

## Files

| file | what |
|---|---|
| `c-seed_prose.cpp` | the clean-room enumeration (`build`, `mk`, `sumok`, gap), with every open choice behind a flag |
| `c-ordercheck.py` | the whole-file test: membership, `s`, gaps, tails, `(t,ypos)` monotonicity, run-log counters |
| `c-paircheck.py` | the earlier narrower per-centre test (kept as the first probe) |
| `c-run_d6.sh` | one command, exit 0 iff everything passes |
| `C-NOTES.md` | every rule with the sentence that fixes it, and every open choice with its measurement |
| `ms/run_d6.log` | the transcript quoted above |
| `ms/sensitivity.txt` | the 7-run sensitivity table |
| `ms/xs_ordered.txt`, `ms/ytails_ordered.txt` | fixtures in the recorded order |
