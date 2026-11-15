# Two former tensor-C Root failures (lead verification)

## Status

`coarse0.bin#678` and `coarse3.bin#33`, the only two `root != pass` entries in
`certdata/runs/h1-root-interval/root_sample.json`, now have explicit rescaled
Root witnesses at exact signed-permutation images. `coarse0#547` remains a
`k=0` base-$C$ control, not another failure.

The worker's d2 report was abandoned without submission. This record is a
separate lead check, not an accepted swarm submission and not a human gate.

## What was rerun

From the member directory, `./run_all.sh` was executed end-to-end in
**12.82 s wall, 12.63 s user, 0.18 s sys**. The pristine `patchx.cpp`, `ub.cpp`,
`seed.cpp` hashes match upstream. The copy adds 24 retention-only lines and no
code removals. The worker's record parser independently caught and corrected
its earlier snapshot bug before these final run artifacts were checked.

At the stored representation, (4.4), $mnorm$, and the residual hold, but tensor
$C$ remains unresolved: the source's $C$ is a remainder bound from the
canonicalisation centre, not a scalar function determined by the stored centre
alone. Rescaling $M$, $LV$, and $A$ by respectively $1-\varepsilon$ and
$(1-\varepsilon)^2$, $\varepsilon=10^{-7}$, preserves $U$'s diagonalisation and
keeps the residual below $id$. At the exact image:

- both `root` verdicts are `pass`, with tensor-C margin approximately
  $4.7\times10^{-7}$;
- $mnorm$ margin is about $7.8\times10^{-8}$ and residual is about
  $4.58\times10^{-7} < id \simeq2\times10^{-6}$;
- $C_{\rm base}$ still fails: the tensor branch is the necessary one;
- the base-$C$ control passes, including its stated $10^{-7}$ slack;
- the `M*1.2`, matrix-entry, smaller-$mnorm$, and smaller-$C$ mutations are all
  rejected appropriately.

The image matches the source tensor formula only to roughly $10^{-13}$ in this
replay. No claim is made to recover the original pre-canonical centre or original
$M$. The scale factor is an explicitly constructed **existential** witness under
Definition 4.1, not a recovery of the original execution's tensors.

## Independently checking transport

`.scratch/verify_two_root_transfers.py` re-reads the raw record bytes, applies the
selected row/transpose mapping to phases and tangent columns, and checks the phase
mapping is exactly the stored record (bitwise in this dyadic data). It then
computes $TT^*$ exactly, rather than mistakenly comparing arbitrary tangent bases,
and bounds the Frobenius projector-discrepancy:

| record | squared discrepancy | upper square-root bound | verdict with q-residual |
|---|---|---|---|
| `coarse0#678` | $5.4555650122791624\times10^{-27}$ (float display) | $7.386179670356769\times10^{-14}$ | $4.58\times10^{-7}$ plus bounded projector change is $<2\times10^{-6}$ |
| `coarse3#33` | $4.0358116831458996\times10^{-27}$ | $6.35280385589379\times10^{-14}$ | likewise $<2\times10^{-6}$ |

These measured bounds are **larger than the worker's approximate $2.5e-15$** but
many orders below $id$. The object with exact rational squares and the square-root
bound is `certdata/runs/h1-root-interval/two-tensor-transport-check.json`, SHA-256
`63944ad5d84edbf4febb14b236277f450b0ba0d4446969d871099e3bb727afb5`.

This yields an existential Root/C witness for these two records **conditional on
the preprint's Lemmas 4.4 and 4.7**, the arithmetic for which my check reads and
evaluates. It does not re-prove those lemmas, does not certify all other Root
clauses or all other records, and does not extend to the nine undecided members
of the separate different-$U$ cohort. Full Stage A/B/C and $N(6)=3$ remain open.
