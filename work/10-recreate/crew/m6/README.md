# crew/m6 — determinism register + R2 harness (team C, units 03+04)

Direction d5 of swarm smwgt1mbm. The authoritative copy of everything here lives in
`.ultramath/smwgt1mbm/m6/`; this is the copy for team C to collect.

**R2 passes.** `covrun` rebuilt from `candidate/` produces
sha256 `c48bc9a2be1eb2cdeea82ea1b030d7cb9f00a6c9563b63f0248dd115748a5789`,
byte-identical to `.scratch/gh/data/centers.txt` (7 339 546 bytes, 249 878 centres), in 774 s wall,
and its stdout counters match `.scratch/gh/covrun.log` field for field
(`checked151744086 centers249878 visit29769262282 near3341641851 cheap45648766 lp3134060273`).

    bash harness/verify_R2.sh                       # full: build, run, sha256, audit, perturb  (~13 min)
    bash harness/verify_R2.sh --stop-t 4            # prefix only (~40 s + 3 perturbation runs)
    bash harness/verify_R2.sh --no-run --out FILE   # verify an existing artefact

Read `NOTES.md` first: §1 is the determinism register (29 items, source line per item), §3 the
spec defects, §2 the choices the frozen spec did not fix. Note §3.1: **`K=4, m=28`**, not the
`K=3, m=38` printed in `spec/interfaces.md` §4.

Layout: `candidate/include/seed.hpp` (module 03), `candidate/include/cover.hpp` (module 04),
`candidate/src/covrun_main.cpp` (the frozen `covrun <out>` program), `candidate/tests/`
(probe_front: xs/ys digests + cover constants; covrun_capped: `--stop-t` subject),
`harness/` (verify_R2.sh, audit_format.py, check_order.py), `logs/`.

This is a proposal for team C's `src/`, not a certification of it: the modular split is
`seed.hpp` + `cover.hpp` + one `main` TU, all definitions inline, so the faithful build is still a
single translation unit and `-O3 -march=native -ffp-contract=off` inlines exactly as upstream does.
