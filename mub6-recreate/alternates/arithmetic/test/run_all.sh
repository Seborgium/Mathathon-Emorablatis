#!/usr/bin/env bash
# run_all.sh -- rebuild and re-run every test of the seed arithmetic core.
#
#   ./test/run_all.sh            the gate: oracle comparison + unit tests + high precision
#   ./test/run_all.sh --full     adds the optimiser/contraction invariance runs (~8 min)
#
# Exit status 0 iff every check passes.  Log: out/verify.log (the whole
# transcript of this script; each line is also echoed to the terminal).
set -u -o pipefail
cd "$(dirname "$0")/.." || exit 2
mkdir -p out
LOG=out/verify.log
: > "$LOG"
exec > >(tee -a "$LOG") 2>&1
FULL=0
[ "${1:-}" = "--full" ] && FULL=1
fails=0
say() { printf '%s\n' "$*"; }
res() { if [ "$1" -eq 0 ]; then say "PASS  $2"; else say "FAIL  $2"; fails=$((fails+1)); fi; }

say "== 0. the oracle copy is the published file, byte for byte"
sum=$(sha256sum test/seed_orig.cpp | cut -d' ' -f1)
say "   test/seed_orig.cpp sha256 $sum"
[ "$sum" = "3c6c7a7092230de231fdb23b6d1782de0dd9ef6689095763b875d90ce5ddeb44" ]
res $? "seed_orig.cpp is the published seed.cpp (sha256 3c6c7a70...)"

say "== 1. build"
# The published flags, from upstream build.sh (interfaces.md section 1).
F="-std=gnu++17 -O3 -march=native -ffp-contract=off"
g++ $F test/oracle_probe.cpp -o out/oracle_probe; res $? "build oracle_probe (published seed.cpp, published flags)"
g++ $F arith/seed_arith.cpp test/mine_dump.cpp -o out/mine_dump; res $? "build mine_dump (modular arith unit + test scaffold)"
g++ -std=gnu++17 -O2 -march=native -ffp-contract=off arith/seed_arith.cpp test/unit_tests.cpp -o out/unit_tests
res $? "build unit_tests (-O2 -march=native -ffp-contract=off)"

say "== 2. dumps (each ~20 s; run concurrently)"
( /usr/bin/time -f "oracle_probe %e s" ./out/oracle_probe > out/oracle.dump ) 2> out/oracle.time &
p1=$!
( /usr/bin/time -f "mine_dump    %e s" ./out/mine_dump    > out/mine.dump    ) 2> out/mine.time &
p2=$!
wait $p1; r1=$?
wait $p2; r2=$?
say "   $(cat out/oracle.time)   rc=$r1"
say "   $(cat out/mine.time)   rc=$r2"
[ $r1 -eq 0 ] && [ $r2 -eq 0 ]; res $? "both dumps ran to completion"
say "   oracle.dump $(sha256sum out/oracle.dump | cut -d' ' -f1)  $(stat -c%s out/oracle.dump) B"
say "   mine.dump   $(sha256sum out/mine.dump   | cut -d' ' -f1)  $(stat -c%s out/mine.dump) B"

say "== 3. R2-style gate of this unit: the two dumps are the same bytes"
cmp out/oracle.dump out/mine.dump; res $? "cmp oracle.dump mine.dump (pi, n, w, 112 tab entries, 22829 xs, all ys)"

say "== 4. independent unit tests (no expected value comes from our own code)"
./out/unit_tests | tail -30; res ${PIPESTATUS[0]} "unit_tests"

say "== 5. high precision + recorded artefacts"
python3 test/check_highprec.py out/mine.dump;   res $? "check_highprec on mine.dump"
python3 test/check_highprec.py out/oracle.dump | tail -2

if [ "$FULL" = 1 ]; then
  say "== 6. invariance across optimisation level, ISA and FP contraction (~8 min)"
  for v in "O0:-O0 -march=native -ffp-contract=off" "O2:-O2 -march=native -ffp-contract=off" \
           "O2baseline:-O2 -march=x86-64 -ffp-contract=off" "contractfast:-O3 -march=native -ffp-contract=fast"; do
    name=${v%%:*}; flags=${v#*:}
    g++ -std=gnu++17 $flags arith/seed_arith.cpp test/mine_dump.cpp -o out/mine_$name || { res 1 "build $name"; continue; }
    /usr/bin/time -f "$name %e s" ./out/mine_$name > out/mine_$name.dump 2> out/mine_$name.time
    rc=$?
    say "   $(cat out/mine_$name.time)"
    [ $rc -eq 0 ] && cmp -s out/oracle.dump out/mine_$name.dump
    res $? "$name build is byte-identical to the oracle ($flags)"
  done
  g++ -std=gnu++17 -O2 -march=native -ffp-contract=off arith/seed_arith.cpp test/margin_scan.cpp -o out/margin_scan
  /usr/bin/time -f "margin_scan %e s" ./out/margin_scan > out/margin_scan.log 2>out/margin_scan.time
  res $? "margin_scan ran"
  cat out/margin_scan.log
fi

say ""
if [ $fails -eq 0 ]; then say "ALL CHECKS PASSED"; else say "FAILED: $fails check(s)"; fi
say "log: $LOG"
exit $([ $fails -eq 0 ] && echo 0 || echo 1)
