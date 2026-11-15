#!/bin/sh
set -eu
# Run from the repository root. Heavy commands are explicit; no network fetch.
g++ -O3 -march=native -ffp-contract=off src/emit/covout.cpp -o src/emit/covrun-emit
src/emit/covrun-emit certdata/runs/h1-seed-emission/centers.new certdata/runs/h1-seed-emission/seed.new
cmp certdata/runs/h1-seed-emission/centers.new .scratch/h0/dl/verification/saved-run/execution/data/centers.txt
g++ -O3 src/qcheck/seed_stream_audit.cpp -o src/qcheck/seed_stream_audit
src/qcheck/seed_stream_audit certdata/runs/h1-seed-emission/seed.new certdata/runs/h1-seed-emission/centers.new > certdata/runs/h1-seed-emission/structural-audit.new.json
g++ -O3 src/qcheck/seed_dual_mpfr.cpp -lmpfr -lgmp -o src/qcheck/seed_dual_mpfr
src/qcheck/seed_dual_mpfr certdata/runs/h1-seed-emission/seed.new > certdata/runs/h1-seed-emission/dual-full.new.json
(cd .ultramath/smwgx3s1v/m2 && g++ -O2 -march=native src/census.cpp -o census && \
  ./census x 112 > logs/census_x112.txt && ./census y 112 > logs/census_y112.txt)
g++ -O3 src/qcheck/seed_extend_mpfr.cpp -lmpfr -lgmp -o src/qcheck/seed_extend_mpfr
src/qcheck/seed_extend_mpfr certdata/runs/h1-seed-emission/seed.new \
  .ultramath/smwgx3s1v/m2/logs/census_x112.txt \
  .ultramath/smwgx3s1v/m2/logs/census_y112.txt 0 \
  > certdata/runs/h1-seed-emission/filter-full.new.json
python3 src/qcheck/seed_mutations.py src/emit/prefix2.wit --report certdata/runs/h1-seed-emission/mutations.json
python3 src/report/h1_render.py
