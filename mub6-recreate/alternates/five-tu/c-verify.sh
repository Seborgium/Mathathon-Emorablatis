#!/usr/bin/env bash
# c-verify.sh -- one command that re-checks everything this unit claims.
#
#   ./c-verify.sh          build + all cheap checks (about 45 s)
#   FULL=1 ./c-verify.sh   also run the full covrun and compare against the
#                          recorded centers.txt (adds ~13 min of 4-CPU VM time)
#
# Every check is one-sided: an expected constant is compared, never adjusted.
set -uo pipefail
cd "$(dirname "$0")"
export LANG=C LC_ALL=C
REC=${REC:-../../../.scratch/gh/data/centers.txt}
# recorded constants (from the project brief and the recorded covrun log)
WANT_SEEDS=841e230ba00b70bff1ba833a04ee63512f45f359e6b067ce6247ee9a58eab66c
WANT_XS=aa9e83fbfe3342e9a6e7bbad1aa73c9a668b667c821203686e329296511589f5
WANT_FILE=c48bc9a2be1eb2cdeea82ea1b030d7cb9f00a6c9563b63f0248dd115748a5789
FAIL=0
note() { printf '\n=== %s\n' "$*"; }
ck() { if [ "$2" = "$3" ]; then echo "PASS $1: $2"; else echo "FAIL $1: got $2 want $3"; FAIL=1; fi; }

note "build"
./c-build.sh || { echo "FAIL build"; exit 1; }
g++ -O3 -march=native -ffp-contract=off -std=gnu++17 c-test-writer.cpp c-writer.cpp -o c-test-writer || exit 1
g++ -O3 -march=native -ffp-contract=off -std=gnu++17 c-seedcensus.cpp c-seed.cpp -o c-seedcensus || exit 1

note "1. enumeration census (xs, ys[a]) at n = 112"
./c-seeddump 112 dump 2> results/verify-counts.txt > results/verify-seeds.txt
ck "xs count = 22829"      "$(grep -c '^X' results/verify-seeds.txt)" 22829
ck "xs+ys stream digest"   "$(sha256sum < results/verify-seeds.txt | cut -d' ' -f1)" "$WANT_SEEDS"

note "2. stage-by-stage census of both loops"
./c-seedcensus 112 > results/verify-census-xs.txt 2> results/verify-census.txt
cat results/verify-census.txt
ck "candidates xs = C(116,5)" "$(awk '/xs candidates/{print $3}' results/verify-census.txt)" 160389488
ck "xs x-stream digest"       "$(sha256sum < results/verify-census-xs.txt | cut -d' ' -f1)" "$WANT_XS"
ck "ys candidates = 112*C(115,4)" "$(awk '/ys candidates/{print $3}' results/verify-census.txt)" 774294080

note "3. writer fixture test (first 10 recorded lines, byte level)"
head -11 "$REC" > results/fixture-first10.txt
./c-test-writer results/fixture-first10.txt results/test-writer.out
ck "writer fixture" "$?" 0

note "4. ordering claims, measured on the recorded file alone"
python3 results/order-check.py "$REC" || FAIL=1

if [ "${FULL:-0}" = 1 ]; then
  note "5. FULL run and whole-file comparison"
  /usr/bin/time -f 'wall %e s' ./c-covrun results/mine-centers.txt > results/covrun-mine.log 2>&1
  tail -3 results/covrun-mine.log
  got=$(sha256sum < results/mine-centers.txt | cut -d' ' -f1)
  if cmp -s results/mine-centers.txt "$REC"; then
    echo "PASS whole file: byte-identical, sha256 $got"
  else
    echo "FAIL whole file: sha256 $got"
    cmp -l results/mine-centers.txt "$REC" | head -3 | awk '{printf "  first differences at byte %d (got %d want %d)\n",$1,strtonum("0"$2),strtonum("0"$3)}'
    FAIL=1
  fi
  ck "whole-file digest" "$got" "$WANT_FILE"
fi

note "result"
if [ $FAIL = 0 ]; then echo "ALL CHECKS PASSED"; else echo "SOME CHECKS FAILED"; fi
exit $FAIL
