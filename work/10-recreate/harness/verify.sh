#!/usr/bin/env bash
# harness/verify.sh -- the single entry point for the V harness (units 02, 10, 11).
#
# usage: verify.sh [r0] [r2] [portable] [all]      (no argument means all)
#   r0        faithful build of the published sources: abi-fp-probe, include chain,
#             pow(x,2) equivalence, artefact hashes          -> logs/R0.json
#   r2        the rebuilt covrun reproduces the recorded covering file byte for byte
#                                                              -> logs/R2.json
#   portable  -O2 / no -march=native build with gcc and clang, and arun record equality
#             against the faithful build                        -> logs/R0-portable.json
#   all       r0, portable, r2   (r2 last: it is by far the longest)
#
# Every unit prints one machine-readable line naming its log:
#   RESULT unit=r0 status=pass pass=true exit=0 log=work/10-recreate/logs/R0.json
# exit: 0 every requested unit passed; 1 a unit failed; 3 a requested unit is
#       incomplete because a leg could not be run (an unrun check is not a pass).
set -uo pipefail
export LANG=C LC_ALL=C

self=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
# shellcheck source=lib/common.sh
. "$self/lib/common.sh"

UNITS=()
for arg in "$@"; do
    case $arg in
        r0|r2|portable) UNITS+=("$arg") ;;
        all) UNITS=(r0 portable r2) ;;
        -h|--help) sed -n '2,19p' "$0"; exit 0 ;;
        *) printf 'unknown unit: %s\n' "$arg" >&2; exit 2 ;;
    esac
done
if (( ${#UNITS[@]} == 0 )); then UNITS=(r0 portable r2); fi

STAMP=$(stamp)
T0=$(now_us)
mkdir -p -- "$HARNESS/out/tmp" "$REPO/work/10-recreate/logs"
LOGDIR=$REPO/work/10-recreate/logs
declare -a names=() codes=() paths=()

run_r0() {
    local blog=$(unique_log_path "$LOGDIR/build-$STAMP.json") gate=$(unique_log_path "$LOGDIR/R0.json")
    local out=$HARNESS/out/tmp/r0-$STAMP.txt st=0 gs=0
    "$HARNESS/build/faithful.sh" --log "$blog" >"$out" 2>&1 || st=$?
    tail -n 3 -- "$out" | sed 's/^/  /'
    if [[ -f $blog ]]; then
        python3 -- "$HARNESS/lib/gate.py" R0 "$blog" "$gate" \
            "R0: probe passes on the build host, toolchain logged (gates.md, G-R1)" \
            >"$HARNESS/out/tmp/r0-gate-$STAMP.txt" 2>&1 || gs=$?
    else
        gs=1
        printf '  gate: no detailed log at %s\n' "$blog" >&2
    fi
    names+=(r0); paths+=("$gate")
    if (( st == 0 && gs == 0 )); then codes+=(0); else codes+=(1); fi
}

run_r2() {
    local log=$(unique_log_path "$LOGDIR/R2.json") out=$HARNESS/out/tmp/r2-$STAMP.txt st=0
    "$HARNESS/reproduce.sh" --log "$log" >"$out" 2>&1 || st=$?
    tail -n 3 -- "$out" | sed 's/^/  /'
    names+=(r2); codes+=("$st"); paths+=("$log")
}

run_portable() {
    local log=$(unique_log_path "$LOGDIR/R0-portable.json") out=$HARNESS/out/tmp/portable-$STAMP.txt st=0
    "$HARNESS/build/portable.sh" --log "$log" >"$out" 2>&1 || st=$?
    tail -n 3 -- "$out" | sed 's/^/  /'
    names+=(portable); codes+=("$st"); paths+=("$log")
}

for unit in "${UNITS[@]}"; do
    printf 'unit %s: running\n' "$unit"
    "run_$unit"
done

fails=0
incomplete=0
for i in "${!names[@]}"; do
    name=${names[$i]}
    code=${codes[$i]}
    log=${paths[$i]}
    case $code in
        0) status=pass ;;
        3) status=incomplete; incomplete=1 ;;
        *) status=fail; fails=1 ;;
    esac
    rel=${log#"$REPO"/}
    printf 'RESULT unit=%s status=%s pass=%s exit=%s log=%s\n' \
        "$name" "$status" "$([[ $status == pass ]] && echo true || echo false)" "$code" "$rel"
done

elapsed=$(awk "BEGIN{printf \"%.1f\", $(ms_since "$T0")/1000}")
if (( fails )); then
    printf 'overall=FAIL elapsed_s=%s\n' "$elapsed"
    exit 1
elif (( incomplete )); then
    printf 'overall=INCOMPLETE elapsed_s=%s (a requested leg could not be run)\n' "$elapsed"
    exit 3
fi
printf 'overall=PASS elapsed_s=%s\n' "$elapsed"
exit 0
