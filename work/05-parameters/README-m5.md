# 05-parameters — files written by swarm member m5 (smwgrqwth)

Prefixed to avoid the lost-update race on the shared deliverable names. Unprefixed
`justification.md`, `N112.md`, `handoff-1.md` currently hold *this* member's version;
identical copies are kept here so a concurrent write cannot destroy them.

| file | content |
|---|---|
| `justification.md` = `justification-m5.md` | the master constant table (8 groups, ~35 rows) |
| `N112.md` = `N112-m5.md` | the bin count: window, constraints, cost curve, half/double, and the cover-count inconsistency |
| `handoff-1.md` = `handoff-1-m5.md` | paste-ready paragraphs for T8 |

Scripts (each runnable as `python3 experiments/<name>.py` from this directory, each writes one CSV):

| script | covers | CSV |
|---|---|---|
| `n112.py` | N: constraints C1–C7, cost curve, exponent sensitivity | `data/m5-cost-curve-N.csv` |
| `seedcover.py` | the cover's own counts; the 151,744,086 inconsistency | `data/m5-seedcover-counts.csv` |
| `caps.py` | all nine caps, admissible k, depth-vs-box-cap interaction | `data/m5-caps.csv` |
| `stagec.py` | F2: the clustering cutoff, the M<=50 no-op result, the corrected formula | `data/m5-stagec-cutoff.csv` |
| `margins.py` | R, .0320001, the reuse threshold, N_u, .103/.125, (tau,w), K, q_d, beta, .64, 25/30, 1e-6, and A.12 with ratios | `data/m5-margins.csv` |

Headline numbers: the admissible window for N is **[47,128]**, not [47,189] — the paper's own
`int8_t` claim in §7.3 is the binding upper bound; the reuse test cannot fire at all below N=79;
the modelled cost optimum is N≈120 and 112 costs 6% more; Table 1's 151,744,086 "pairs" exceeds the
maximum the stated filters can leave (85,349,292) by 1.78×.
