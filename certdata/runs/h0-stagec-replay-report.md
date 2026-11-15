# H0 Stage-C instrumented replay — verified report

Generated from `.scratch/h0/runs/probe-all/` by `src/report/h0_stagec_stats.py` and
`src/report/h0_replay_verify.py`. Machine-readable forms: `h0-stagec-probe.json`,
`h0-stagec-probe-summary.json`, `h0-replay-byte-compare.json`.

## Equivalence to the archived run
All 92 recorded Stage-C commands completed. Probe exit statuses match the recorded return codes
(88 initial batches, 15 of them nonzero, plus four successful final parts). **All 92 output bad-record
files are byte-identical to the archive; zero missing, zero different.** Every command's stdout
`result` counters match. The probe adds per-record stderr lines only. Its source changes are
output-only calls in `.scratch/h0/instr/stageC.cpp`; the build otherwise uses the upstream flags.

The replay took 40 min 34 s elapsed with four workers while sharing the VM with the agent swarm.
Summed per-command wall time is 9,696.47 s, but this is contended wall time, **not CPU time**. The
single-process `f52` anchor is 30.64 s for 256 records. A clean CPU-time measurement is separate
work; "~40 CPU-min" is the order-of-magnitude planning figure, not a benchmark claim.

## Complete census (23,506 records)
- `nopattern`: **23,343** completed negative graph searches (22,216 initial + 1,127 final).
- `cap`: **163**, all at exactly 5,000,001 steps; these are unresolved, not exclusions.
- `emptylayer`, `positive`, `overflow`, `clusterfail`: **zero**. Every exclusion in the recorded run
  therefore uses the graph path of Proposition 6.9; none uses an empty bin layer.
- balls: total 5,272,329; min 49, median 205, mean 224.30, p95 319, max 1,089. Among records that
  need an exclusion certificate the maximum is 732; the 1,089-node graph belongs to a capped record.
- O edges: total 76,381,177; U edges: total 291,738,515.
- completed-negative search steps: **2,932,018,956**; median 38,453, mean 125,605.92,
  p95 526,566, max 4,986,110. Fallback searches total 212,745,404 steps, maximum 3,200,276, no cap.
- pairs over all records: 639,025,953; over completed negatives: 622,704,036.
- O+U edge incidences over completed negatives: 357,191,053; the remaining 265,512,983 pair/relation
  slots are potential non-edge evidence (a pair excluded from both graphs can need two reasons).
- full O+U adjacency storage, using `2*M*ceil(M/64)*8` bytes/record: **350,022,800 bytes** for the
  completed negatives (before centres, radii, indices, manifests or compression).

These are floating-point replay statistics, not exact-arithmetic certificates. They measure the
object that a checker must handle; they do not validate its predicates.

## Consequences for G0
1. Route (a), graph data plus an independent complete checker, is measurable and plausible. The graph
   data is ~350 MB uncompressed, and the binary64 replay is on the order of 40 CPU-min. Exact/interval
   predicates dominate the unknown cost; current kernel models span roughly 1–30 CPU-h, not an
   end-to-end measurement.
2. Default DRAT is unattractive: even one 30-byte line per completed-search node is ~88 GB, 60 bytes
   ~176 GB, before encoding and checking overhead. It remains an optional independence mechanism for
   a selected record, not the run-wide format.
3. The initial 163 cap records must not be charged to the exclusion certificate: their exclusions come
   from the fallback. A separately checked higher-cap alternative is possible (all 163 completed in a
   member's binary64 rerun at max 39,968,282 steps) but is a *different execution* and must not be
   silently substituted for the archived path.
