# What the published verification apparatus does and does not check

Measured by this programme, 2026-11-14. Each line has a command or a file behind it. These are
findings about the *record*, not about the mathematics, and they belong in our write-up.

## 1. `results/*.txt` is a curated transcript, not stdout
`covrun` prints `xs22829 build19.30`; the record holds `xs 22829`. The `time %.2f` suffixes, the
`coverFailures…` pair, `candidates`/`patches` and `avg bins`/`balls` are absent, and the final timing
line is replaced by `completed_write`. `check_records.py` fullmatches those curated forms, so the
transcript is verified as text, against numbers the checker recomputes from the data files.
Evidence: `execution/results/{A0,Bmid,C.batch0}.txt` against the `printf` format strings in
`atlas.cpp`, `stageB.cpp`, `stageC.cpp`, `covout.cpp`; `check_records.py:240-244,297,336`.

## 2. The command manifest omits two kinds of output
`commands.json` never lists `batches/f*.bin` (consumed by the 88 C entries but never declared as
`Bfine` outputs) and never lists `<prefix>done.txt`. A replay driver that trusts the manifest cannot
know what to expect; it must list the directory and check the partition against the parent count.
Evidence: `Bfine` records only `fine.bin`/`finebad.bin`; `C.batch0` consumes `batches/f0.bin`.

## 3. Three tampered parent records pass both checkers
Corrupt `p[0] += 0.001` in one record of `coarse0.bin`, of `mid.bin`, or of `fb1.bin`: the shipped
checker accepts, and so does our independently written one. Nothing downstream compares the bytes of
a parent record against its children — only counts and partitions are compared. So the published
record does not establish that stage B was run on the stage-A parents it claims; it establishes that
the children *exist* in the right numbers.
Evidence: `harness/v2-check.sh`, cases `silent_coarse_p`, `silent_mid_p`, `silent_fb1_p`; log
`logs/v2-2026-11-14T200507Z.json` (25/28 rejected by both, the 3 expected-accept cases accepted by
both).

Consequence for our ladder: this is exactly the gap R4/R5 close. Our replay *recomputes* the children
from the parents, so a tampered parent cannot pass: our `mid.bin` would differ from the recorded one.
Worth saying in the write-up as the one place where an independent reproduction is strictly stronger
than the published check.

## 4. What the checker does not claim
Its own docstring and `VERIFY.md` say so: numerical consistency only, no compiler, hardware or
provenance authentication. Our programme's R0 and the build logs are what covers that half.
