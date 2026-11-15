# work/05-parameters — T5 "Parameters"

Deliverables of this team (see `results/plan.md` §3 T5 and §9):

| file | what it is |
|---|---|
| `justification.md` | the master table: every constant with its governing inequality, slack, half/double behaviour, recommendation and status |
| `N112.md` | the full argument for the bin count: window [47,128]/[47,189], the constraint list, the cost curve, the recommendation, and what breaks at 56 and 224 |
| `handoff-1.md` | paste-ready paragraphs for T8 (the paper) |
| `experiments/exp_*.py` | one script per constant group; each prints its numbers and writes `data/*.csv`; run `python3 experiments/<name>.py` from this directory |
| `data/*.csv` | the tables of the markdown files, one CSV per table |

Script map: `exp_n112_window.py` (bin count, window, cost curve), `exp_seed_radius.py` (R, .0320001,
the testBucket threshold), `exp_u2_grid.py` (N_u, h, Taylor remainders, the targets .103/.125),
`exp_refinement.py` (the three (tau,w) pairs, L, the admissible k, depth), `exp_caps.py` (all caps vs
the recorded run), `exp_stagec_cutoff.py` (F2), `exp_margins.py` (Appendix A's closing table with
ratios), `exp_conditioning.py` (the chain's conditioning, K, q_d, beta, the counts),
`exp_misc.py` (.64, 1e4, 1e10, .249/.23, the small margins).

Unprefixed files in `experiments/` and `data/` belong to another member of the swarm; they are not
mine and I have not modified them.
