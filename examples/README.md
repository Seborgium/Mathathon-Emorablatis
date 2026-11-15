# examples/ — the code behind the four "Step k on one example" notes

    mub-step2-example.tex/.pdf   frames, the constants q and p, the defect bound
    mub-step3-example.tex/.pdf   the U(2) chart, two Taylor bounds, grid sizes
    mub-step4-example.tex/.pdf   the O and U graphs on the Fourier pair's candidates
    mub-step5-example.tex/.pdf   one documented pass read back: states, ledger, margins

Same arrangement as Step 1 (`mub-step1-example.pdf` with `step1_filter.cpp`): a short
document per step, and a program that produces every number in it.

    ./run_all.sh                 # everything, into out/
    python3 step3_example.py     # one step; prints key/value rows

`out/stepK.txt` is the printed table the corresponding document quotes; `out/stepK.json`
(produced with `--json`) is the same data machine-readable.

## Files

| file | what it does |
|---|---|
| `mubexact.py` | exact arithmetic in Q(w), w = exp(2 pi i/6), and the example matrix H' of Step 1. Self-test at the bottom: `python3 mubexact.py`. |
| `step2_example.py` | the two frames of H', m_B, m_C, A_0, A_*, q, p, the critical seed radii, the defect identity, 40 000 perturbed centres, the degenerate centre b_j = 1/4. |
| `step3_example.py` | the four-angle chart of U(2), the chart coordinates of V = Y/sqrt(6), the cell of V at N_u = 8..256 with the two Taylor bounds, the measured constants, grid sizes, the certify-then-inflate arithmetic. |
| `step4_example.py` | the candidates of the standard + Fourier pair on the 12th-root lattice (exhaustive over 12^5 tuples), the O and U graphs, the four six-cliques, the pattern test, and the edge-test margins with radii. |
| `step5_example.py` | the census of the archived Stage-C pass (23 506 records), the ledger of the three states, three record miniatures, and the binary64 margins. |

## What is exact, and what is not

* Exact: everything in `step2_example.py` that does not involve a norm or a frame (the block
  identities, m_B, m_C, S = sum b_j), and every decision in `step4_example.py` (arithmetic in
  Z[zeta_12]: squared moduli are A + B sqrt3, orthogonality is a four-integer test).
* Binary64, as in the pipeline: frames, singular values, the perturbation experiment
  (`step2`), the chart and its remainder (`step3`), the ball radii (`step4`).
* The 48-candidate count off the lattice (Step 4, §5 of the note) comes from
  `step4_example.py --slow`, a multistart Newton search (about 35 s), not from an enumeration:
  it is evidence, and it is the only number in the four notes that is not either exact or a
  binary64 evaluation of an exact formula. The search also finds 300 orthogonal pairs,
  16 bases, 0 unbiased pairs, and puts exactly 12 of the 48 on the twelfth-root lattice.

## Two conventions worth knowing before changing anything

1. Step 2's perturbation model moves the **centre** and keeps the seed exact, so that
   B'^*B' + D'^*D' = 6I holds and the defect identity 6I - Y^*Y = M_1^*M_1 + M_2^*M_2 is the
   paper's. If the **seed** is moved instead, the identity needs an extra term
   K_B^*(6I - B^*B - D^*D)K_B. `step2_example.py` avoids the issue by moving the centre
   and keeping the seed exact; the extra term was found by a referee in the swarm and is
   recorded here so that nobody re-derives it.
2. Step 3's angles are in radians and the cell is cut with N_u cells per coordinate, so the
   uniform half-width is h = pi/N_u. The measured constants c_1, c_2 (1.58 and 1.16) are
   properties of this convention; a different cell alignment shifts c_2 by a factor ~1.25
   while leaving both bounds true.
