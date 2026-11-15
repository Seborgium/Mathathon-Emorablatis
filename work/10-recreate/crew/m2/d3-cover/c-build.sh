#!/usr/bin/env bash
# c-build.sh — build the cover units with the faithful flags of spec §1.
# usage: ./c-build.sh [outdir]      (default: ./build)
set -euo pipefail
cd -- "$(dirname -- "$0")"
out=${1:-build}
mkdir -p -- "$out"
export LANG=C LC_ALL=C
CXX=${CXX:-g++}
FLAGS=(-std=gnu++17 -O3 -march=native -ffp-contract=off -Wall -Wextra -Wno-unused-parameter)
"$CXX" "${FLAGS[@]}" c-covrun.cpp  -o "$out/c-covrun"
"$CXX" "${FLAGS[@]}" c-harness.cpp -o "$out/c-harness"
"$CXX" "${FLAGS[@]}" c-fixture.cpp -o "$out/c-fixture"
printf 'built: %s/c-covrun %s/c-harness %s/c-fixture\n' "$out" "$out" "$out"
