#!/usr/bin/env bash
# harness/reproduce.sh -- R2: the faithful build reproduces the recorded covering file.
#
# Runs the faithful covrun once and compares its output with the recorded artefact,
# byte for byte, plus the deterministic counters covrun prints (which catch a
# divergence long before a file hash does -- the hash only says "different").
#
# usage: reproduce.sh [--build-out DIR] [--src DIR] [--cxx PATH] [--recorded FILE]
#                     [--work DIR] [--log FILE] [--timeout SECONDS] [--no-build] [--stamp S]
#   --build-out  reuse an existing faithful build instead of building a fresh one
#   --no-build   require --build-out; do not run harness/build/faithful.sh
#   --timeout    wall clock limit for covrun, default 3600 s (the recorded run took 402 s)
# exit: 0 the output is byte-identical to the recorded centres; 1 any check failed; 2 refusal
#
# Frozen expectation for the recorded artefact (spec/interfaces.md §3.1):
#   7339546 B, sha256 c48bc9a2be1eb2cdeea82ea1b030d7cb9f00a6c9563b63f0248dd115748a5789,
#   header "112 249878", one line per centre, ten decimal integers each followed by a space.
# The deterministic counters below are transcribed from .scratch/gh/covrun.log, the
# authors' recorded stdout; the script re-reads that file too when it is present.
set -euo pipefail
export LANG=C LC_ALL=C

self=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
# shellcheck source=lib/common.sh
. "$self/lib/common.sh"

BUILD_OUT=
SRC_DIR=
CXX_BIN=${CXX:-g++}
RECORDED=$REPO/.scratch/gh/data/centers.txt
RECORDED_LOG=$REPO/.scratch/gh/covrun.log
WORK_DIR=
LOG_FILE=
TIMEOUT=3600
DO_BUILD=1
STAMP=$(stamp)

while [[ $# -gt 0 ]]; do
    case $1 in
        --build-out) BUILD_OUT=${2:?--build-out needs a directory}; shift 2 ;;
        --src) SRC_DIR=${2:?}; shift 2 ;;
        --cxx) CXX_BIN=${2:?}; shift 2 ;;
        --recorded) RECORDED=${2:?}; shift 2 ;;
        --work) WORK_DIR=${2:?}; shift 2 ;;
        --log) LOG_FILE=${2:?}; shift 2 ;;
        --timeout) TIMEOUT=${2:?}; shift 2 ;;
        --no-build) DO_BUILD=0; shift ;;
        --stamp) STAMP=${2:?}; shift 2 ;;
        -h|--help) sed -n '2,18p' "$0"; exit 0 ;;
        *) printf 'unknown argument: %s\n' "$1" >&2; exit 2 ;;
    esac
done

EXPECT_SHA=c48bc9a2be1eb2cdeea82ea1b030d7cb9f00a6c9563b63f0248dd115748a5789
EXPECT_BYTES=7339546
EXPECT_HEADER='112 249878'
EXPECT_COUNT=249878
EXPECT_XS=22829
EXPECT_CHECKED=151744086
EXPECT_VISIT=29769262282
EXPECT_NEAR=3341641851
EXPECT_CHEAP=45648766
EXPECT_LP=3134060273

# absolute: the covrun subshell cds into WORK_DIR, so a relative --build-out would
# name a different file after the cd (first portable attempt failed exactly that way)
[[ -n $BUILD_OUT ]] && BUILD_OUT=$(realpath -m -- "$BUILD_OUT")
RECORDED=$(realpath -m -- "$RECORDED")
[[ -n $WORK_DIR ]] || WORK_DIR=$HARNESS/out/repro-$STAMP
WORK_DIR=$(realpath -m -- "$WORK_DIR")
[[ -n $LOG_FILE ]] || LOG_FILE=$REPO/work/10-recreate/logs/R2.json
LOG_FILE=$(realpath -m -- "$LOG_FILE")
LOG_FILE=$(unique_log_path "$LOG_FILE")
[[ -f $RECORDED ]] || { printf 'recorded centres not found: %s\n' "$RECORDED" >&2; exit 2; }
mkdir -p -- "$WORK_DIR" "$HARNESS/out/tmp"
FACTS=$HARNESS/out/tmp/reproduce-$STAMP.tsv
: >"$FACTS"
T_START=$(now_us)

fact_s unit "R2"
fact_s script "$0"
fact_s started_utc "$(now_utc)"
fact_s stamp "$STAMP"
fact_s work.dir "$WORK_DIR"
fact "timeout_s" "$TIMEOUT"
fact_s toolchain.glibc "$(ldd --version | head -1)"
fact_s toolchain.cpu.model "$(lscpu | sed -n 's/^Model name:[[:space:]]*//p' | head -1)"
fact "toolchain.cpu.online" "$(nproc)"
fact_s expected.sha256 "$EXPECT_SHA"
fact "expected.bytes" "$EXPECT_BYTES"
fact_s expected.header "$EXPECT_HEADER"
fact "expected.count" "$EXPECT_COUNT"

# ---------------------------------------------------------------- the recorded file
fact_file recorded "$RECORDED"
rec_sha=$(sha256_of "$RECORDED")
rec_bytes=$(size_of "$RECORDED")
rec_header=$(head -c 10 -- "$RECORDED")
if [[ $rec_sha == "$EXPECT_SHA" ]]; then pass_check recorded.sha256; else
    fail_check recorded.sha256 "recorded file hashes to $rec_sha, spec says $EXPECT_SHA"
fi
if [[ $rec_bytes -eq $EXPECT_BYTES ]]; then pass_check recorded.bytes; else
    fail_check recorded.bytes "recorded file is $rec_bytes B, spec says $EXPECT_BYTES"
fi

# ---------------------------------------------------------------- the build
covrun=
if (( DO_BUILD )); then
    build_out=${BUILD_OUT:-$HARNESS/out/faithful-$STAMP}
    build_log=$REPO/work/10-recreate/logs/build-$STAMP.json
    bstatus=0
    argv=( "$HARNESS/build/faithful.sh" --out "$build_out" --log "$build_log" --cxx "$CXX_BIN" )
    [[ -n $SRC_DIR ]] && argv+=( --src "$SRC_DIR" )
    bout=$("${argv[@]}" 2>&1) || bstatus=$?
    fact "build.exit" "$bstatus"
    fact_s "build.log" "$build_log"
    fact_s "build.stdout" "$(head -c 4000 <<<"$bout")"
    fact_s "build.argv" "${argv[*]}"
    if (( bstatus != 0 )); then
        fail_check build "faithful.sh exited $bstatus (log $build_log)"
    else
        pass_check build
        # faithful.sh suffixes an occupied --out and an occupied --log, so take both
        # back from its own PASS line rather than assuming what we asked for
        covrun=$(sed -n 's/.*out=\([^ ]*\).*/\1/p' <<<"$bout" | tail -1)
        blog=$(sed -n 's/.*log=\([^ ]*\).*/\1/p' <<<"$bout" | tail -1)
        [[ -n $blog ]] && build_log=$blog
    fi
else
    [[ -n $BUILD_OUT ]] || { printf '--no-build needs --build-out DIR\n' >&2; exit 2; }
fi
[[ -n $covrun ]] || covrun=$BUILD_OUT
fact_s build.out_dir "$covrun"
if [[ -x $covrun/covrun ]]; then
    pass_check build.covrun_present
    fact_file build.covrun "$covrun/covrun"
else
    fail_check build.covrun_present "no executable covrun in $covrun"
fi

# ---------------------------------------------------------------- the run
RUN_STATUS=0
T_RUN=$(now_us)
if [[ -x $covrun/covrun ]]; then
    if ( cd -- "$WORK_DIR" && timeout -- "$TIMEOUT" "$covrun/covrun" centers.txt ) \
            >"$WORK_DIR/covrun.stdout" 2>"$WORK_DIR/covrun.stderr"; then
        RUN_STATUS=0
    else
        RUN_STATUS=$?
    fi
fi
RUN_MS=$(ms_since "$T_RUN")
FRESH=$WORK_DIR/centers.txt
fact "run.exit" "$RUN_STATUS"
fact "run.ms" "$RUN_MS"
fact_s "run.stdout" "$(head -c 4000 -- "$WORK_DIR/covrun.stdout" 2>/dev/null || true)"
fact_s "run.stderr" "$(head -c 2000 -- "$WORK_DIR/covrun.stderr" 2>/dev/null || true)"
if (( RUN_STATUS == 0 )); then pass_check run.exit; else
    fail_check run.exit "covrun exited $RUN_STATUS after ${RUN_MS} ms (timeout ${TIMEOUT}s)"
fi

# ---------------------------------------------------------------- the comparison
if [[ -f $FRESH ]]; then
    fact_file fresh "$FRESH"
    fresh_sha=$(sha256_of "$FRESH")
    fresh_bytes=$(size_of "$FRESH")
    fresh_header=$(head -c 10 -- "$FRESH")
    fresh_lines=$(wc -l <"$FRESH")
    if [[ $fresh_sha == "$EXPECT_SHA" ]]; then pass_check fresh.sha256; else
        fail_check fresh.sha256 "fresh output hashes to $fresh_sha, recorded is $EXPECT_SHA"
    fi
    if [[ $fresh_bytes -eq $EXPECT_BYTES ]]; then pass_check fresh.bytes; else
        fail_check fresh.bytes "fresh output is $fresh_bytes B, recorded is $EXPECT_BYTES"
    fi
    if [[ $fresh_header == "$EXPECT_HEADER" ]]; then pass_check fresh.header; else
        fail_check fresh.header "fresh header is '$fresh_header', expected '$EXPECT_HEADER'"
    fi
    if [[ $fresh_lines -eq $((EXPECT_COUNT + 1)) ]]; then pass_check fresh.lines; else
        fail_check fresh.lines "fresh output has $fresh_lines lines, expected $((EXPECT_COUNT + 1))"
    fi
    if cmp -s -- "$RECORDED" "$FRESH"; then
        pass_check fresh.cmp
    else
        off=$(cmp -- "$RECORDED" "$FRESH" 2>/dev/null | sed -n 's/.*byte \([0-9]*\).*/\1/p' | head -1)
        fail_check fresh.cmp "output differs from the recorded file at byte ${off:-?}"
        fact_s "fresh.first_difference_byte" "${off:-}"
    fi
    # §3.1 layout: every centre line is ten decimal integers, each followed by one space
    fmt=$(
        python3 - "$FRESH" "$EXPECT_COUNT" <<'PY'
import re, sys
path, count = sys.argv[1], int(sys.argv[2])
line = re.compile(rb'\A(?:[0-9]+ ){10}\n\Z')
bad = 0
n = 0
with open(path, 'rb') as handle:
    handle.readline()
    for n, raw in enumerate(handle, 1):
        if not line.match(raw):
            bad += 1
            if bad <= 3:
                sys.stderr.write('bad line %d: %r\n' % (n, raw[:60]))
print('lines=%d bad=%d' % (n, bad))
sys.exit(0 if bad == 0 and n == count else 1)
PY
    ) || true
    fact_s fresh.format "$fmt"
    if [[ $fmt == "lines=$EXPECT_COUNT bad=0" ]]; then pass_check fresh.format; else
        fail_check fresh.format "centers.txt layout violated: '$fmt' (want lines=$EXPECT_COUNT bad=0)"
    fi
else
    fail_check fresh.present "no output file at $FRESH"
fi

# ------------------------------------------- deterministic counters from stdout
# These diverge long before a hash does, and they name which stage moved.
nline=$(grep -m1 '^N112 ' "$WORK_DIR/covrun.stdout" 2>/dev/null || true)
fact_s counters.line "$nline"
field() { awk -v k="$1" '{for (i = 1; i <= NF; i++) if (index($i, k) == 1) { print substr($i, length(k) + 1); exit }}' <<<"$nline"; }
for pair in "checked:$EXPECT_CHECKED" "centers:$EXPECT_COUNT" \
            "visit:$EXPECT_VISIT" "near:$EXPECT_NEAR" "cheap:$EXPECT_CHEAP" "lp:$EXPECT_LP"; do
    key=${pair%%:*}; want=${pair##*:}
    got=$(field "$key" || true)
    fact "counters.$key" "${got:-0}"
    if [[ ${got:-} == "$want" ]]; then pass_check "counters.$key"; else
        fail_check "counters.$key" "stdout has $key=${got:-<absent>}, recorded run has $want"
    fi
done
xsline=$(grep -m1 '^xs[0-9]' "$WORK_DIR/covrun.stdout" 2>/dev/null || true)
xs=$(sed -n 's/^xs\([0-9]*\) .*/\1/p' <<<"$xsline" | head -1)
fact "counters.xs_line" "${xs:-0}"
if [[ ${xs:-} == "$EXPECT_XS" ]]; then pass_check counters.xs_line; else
    fail_check counters.xs_line "stdout seed count is ${xs:-<absent>}, recorded run has $EXPECT_XS"
fi

# The recorded stdout is itself a recorded artefact; agree with it verbatim on the
# deterministic lines (everything except the build/time fields).
if [[ -f $RECORDED_LOG ]]; then
    fact_s recorded_log.path "$RECORDED_LOG"
    strip() { grep -E '^(xs[0-9]+| t[0-9]+/|N[0-9]+ )' "$1" 2>/dev/null | sed 's/build[0-9.]*//; s/time [0-9.]*//' || true; }
    r=$(strip "$RECORDED_LOG"); f=$(strip "$WORK_DIR/covrun.stdout")
    if [[ -n $r && $r == "$f" ]]; then pass_check counters.vs_recorded_stdout; else
        fail_check counters.vs_recorded_stdout "deterministic stdout lines differ from $RECORDED_LOG"
        fact_s "counters.recorded_stdout" "$r"
        fact_s "counters.fresh_stdout" "$f"
    fi
else
    fact "counters.recorded_stdout_absent" true
fi

# ---------------------------------------------------------------- finish
fact "checks.total" "$CHECKS"
fact "checks.failures" "$FAILS"
fact "duration_ms" "$(ms_since "$T_START")"
fact_s finished_utc "$(now_utc)"
fact_s log.path "$LOG_FILE"
if (( FAILS == 0 )); then
    fact "pass" true
    emit_json "$FACTS" "$LOG_FILE"
    printf 'PASS unit=R2 pass=true checks=%d sha256=%s bytes=%s run_s=%s log=%s\n' \
        "$CHECKS" "$(sha256_of "$FRESH")" "$(size_of "$FRESH")" "$(awk "BEGIN{printf \"%.1f\", $RUN_MS/1000}")" "$LOG_FILE"
    exit 0
fi
fact "pass" false
emit_json "$FACTS" "$LOG_FILE"
printf 'FAIL unit=R2 pass=false checks=%d failures=%d log=%s\n' "$CHECKS" "$FAILS" "$LOG_FILE"
exit 1
