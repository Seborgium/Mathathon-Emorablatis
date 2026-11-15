# Lead note for all H0 agents (2026-11-14, ~20:22 UTC)

Full upstream tree + saved run is now local: `.scratch/h0/dl/verification/` (sources, execution
data, results, commands.json, check_records.py) and the preprint PDF at
`.scratch/h0/dl/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026.pdf`.
Tree listing: `certdata/upstream/tree.json`; hashes: `.scratch/h0/upstream-manifest.json`.
Use these local copies instead of re-fetching. Do not edit them; copy into your own directory.

Measured from the saved C logs (all 92 crun commands):
total done = 23,506 records; bad = 163; graph (completed candidate searches) = **0**;
cap = **163** (15 batches); overflow = 0; cluster = 0. Final fallback parts: done 282, bad 0,
graph 0, cap 0. So in the recorded run NO record ended in an uncapped positive graph search; the
only graph searches that matter are the 163 capped ones (5,000,000-step cap). Interpretation needs
care: `graph` counts `stats.positive`, i.e. records where `g.candidate()` returned true without
`gaveup`. Records can also be excluded before graph construction (empty bin layers) or by a cheap
`candidate()==false`. Distinguishing these per record is an H0 measurement, not an assumption.

A0..A3 totals: done 62,470/62,470/62,469/62,469 = 249,878 centres, failedBalls 0 everywhere.
covrun log: `N112 r0.0320 dual2 checked151744086 centers249878`, completed_write; reproduced on
this VM in 401.82 s with byte-identical centres.txt.

Background job jmwgun4xw is replaying the worst batch (f52, 29 capped records) with the stock
binary to time it and compare bad52.bin byte-for-byte. Do not run heavy jobs concurrently.

## Update 20:27 — full record fetched, checker run, instrumented replay in flight
- All 309 upstream files (82.5 MB) are at `.scratch/h0/dl/verification/`, hashes in
  `certdata/upstream/manifest.json`. Authors' `check_records.py`: PASS within numerical
  consistency scope (`certdata/runs/h0-record-check.json`).
- Stock `crun` on the worst batch f52 reproduces `bad52.bin` byte-identically, 30.64 s.
- An output-only instrumented build (`.scratch/h0/instr/crun-probe`, sources beside it) prints per
  record `REC idx category bins B balls B O n U m steps s`; on f52 it produces the same stdout and
  the same bad52.bin. Example: `REC 1 nopattern bins23042 balls248 O2530 U13568 steps31324`.
- Job jmwgus4ci is running that probe on all 88 batches + the 4 final parts, 4-way parallel
  (about 45 CPU-min total). Results: `.scratch/h0/runs/probe-all/<tag>/{stdout,stderr}.log`.
  Please do NOT launch another full sweep; read these logs as they appear. Reuse them for your
  graph-size/density/step statistics (steps are the branching-search work, not graph size).
- Q4 members: note that per-record `steps` for uncapped no-pattern records ranges ~3e4 to ~1.8e6 on
  f52, so route (a) independent exhaustive recheck is a live option; the cap cases are the ones to
  design for. Exact predicate checking in interval arithmetic is a separate cost you should estimate.
