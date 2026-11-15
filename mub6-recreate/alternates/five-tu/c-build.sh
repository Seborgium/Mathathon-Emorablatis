#!/usr/bin/env bash
# c-build.sh -- build the re-derived programs with the published compile line.
# Mirrors .scratch/gh/upstream/build.sh for covrun (spec/interfaces.md §1):
#   g++ -O3 -march=native -ffp-contract=off covout.cpp -o covrun
# -march=native and -ffp-contract=off are load-bearing for byte-identity.
set -euo pipefail
cd "$(dirname "$0")"
export LANG=C LC_ALL=C
CXX=${CXX:-g++}
BASE="-O3 -march=native -ffp-contract=off"
STD="-std=gnu++17"
set -x
$CXX $BASE $STD c-covrun.cpp   c-cover.cpp c-seed.cpp c-writer.cpp -o c-covrun
$CXX $BASE $STD c-seeddump.cpp      c-seed.cpp                     -o c-seeddump
$CXX $BASE $STD c-partialrun.cpp c-cover.cpp c-seed.cpp c-writer.cpp -o c-partialrun
