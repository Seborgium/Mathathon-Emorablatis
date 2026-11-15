# crew/m3 (K, direction k3 — mutation controls)

`findings/k-m3-mutations.md` is the deliverable; this file only says where the evidence lives.

Probes (copies only — no upstream file was modified) are under
`.ultramath/smwgt1mg2/m3/probe/`:

- `cov/{base,fast,up,fm}/covout.cpp` — upstream + one early exit (`t>=LIMIT`, `-DLIMIT=3000`).
  `out/c-*.txt` artefacts, `s-*.txt` stdout, `t-*.txt` timings. `c-base.txt` reproduces the first
  12 111 lines of the recorded `centers.txt`.
- `A/{base,fast,up,rn}/atlas.cpp` — upstream, `-ffp-contract=fast`, `fesetround(FE_UPWARD)` after
  `checkcpu()`, `r=.0320002`. Ran on `out/centers200.txt` (first 200 recorded centres, part 0 of 1).
- `a/`, `b/` — standalone `ub.cpp` driver, seed 42 vs 43; `o42.txt`, `o43.txt`, `o42b.txt`.
- `chk/` — copy of the saved-run execution tree; shipped checker clean (`ok.txt`) and with one byte
  appended to `data/coarse0.bin` (`bad1.txt`).

Rebuild lines are in `findings/k-m3-mutations.md` under each finding.
