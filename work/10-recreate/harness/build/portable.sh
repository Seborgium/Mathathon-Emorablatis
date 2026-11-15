#!/usr/bin/env bash
# harness/build/portable.sh -- build and check the portable build (spec §1) with every
# usable compiler, and check that it agrees with the faithful build on real input.
#
# usage: portable.sh [--faithful-out DIR] [--fixture FILE] [--log FILE] [--stamp S]
#                    [--compilers "g++ clang++"] [--src DIR] [--full]
#   --full          after the arun comparison, run the portable covrun end to end and
#                   check it reproduces the recorded centres (≈10-13 min per leg)
#   --faithful-out  reuse an existing faithful build as the reference; default: run
#                   harness/build/faithful.sh first (≈40 s)
#   --fixture       centres file for the arun comparison; default
#                   harness/fixtures/centres-200.txt, generated from the recorded file
# exit: 0 every runnable leg passed; 1 a leg failed; 3 incomplete (a leg could not be
#       run at all -- an unrun check is not a pass)
#
# Legs, per compiler: preflight (can it compile <cstdio> at all), make of the four
# programs, ABI/FP probe where the probe permits it (GCC only -- abi-fp-probe.cpp
# #errors on clang by design), a no-AVX check that -march=native really was not used,
# and a byte comparison of `arun 0 1` records against the faithful build.
set -euo pipefail
export LANG=C LC_ALL=C

self=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
# shellcheck source=../lib/common.sh
. "$self/../lib/common.sh"

FAITHFUL_OUT=
FIXTURE=$HARNESS/fixtures/centres-200.txt
LOG_FILE=$REPO/work/10-recreate/logs/R0-portable.json
STAMP=$(stamp)
SRC_DIR=$REPO/.scratch/gh/upstream
COMPILERS="g++ clang++"
FULL=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --faithful-out) FAITHFUL_OUT=${2:?}; shift 2 ;;
        --fixture) FIXTURE=${2:?}; shift 2 ;;
        --log) LOG_FILE=${2:?}; shift 2 ;;
        --stamp) STAMP=${2:?}; shift 2 ;;
        --compilers) COMPILERS=${2:?}; shift 2 ;;
        --src) SRC_DIR=${2:?}; shift 2 ;;
        --full) FULL=1; shift ;;
        -h|--help) sed -n '2,19p' "$0"; exit 0 ;;
        *) printf 'unknown argument: %s\n' "$1" >&2; exit 2 ;;
    esac
done

# every path here is consumed after a cd (arun_run cds into its output dir, make cds
# nowhere but inherits ours), so absolutise them once: a relative --faithful-out or
# --fixture silently resolves against the wrong directory otherwise.
[[ -n $FAITHFUL_OUT ]] && FAITHFUL_OUT=$(realpath -m -- "$FAITHFUL_OUT")
FIXTURE=$(realpath -m -- "$FIXTURE")
SRC_DIR=$(realpath -m -- "$SRC_DIR")

command -v make >/dev/null 2>&1 || { printf 'make is required\n' >&2; exit 2; }
RECORDED=$REPO/.scratch/gh/data/centers.txt
[[ -f $RECORDED ]] || { printf 'recorded centres not found: %s\n' "$RECORDED" >&2; exit 2; }
[[ -d $SRC_DIR ]] || { printf 'source tree not found: %s\n' "$SRC_DIR" >&2; exit 2; }
mkdir -p -- "$HARNESS/out/tmp" "$HARNESS/fixtures"
LOG_FILE=$(unique_log_path "$(realpath -m -- "$LOG_FILE")")

FACTS=$HARNESS/out/tmp/portable-$STAMP.tsv
: >"$FACTS"
T_START=$(now_us)
SKIPPED=0

fact_s unit "R0-portable"
fact_s script "$0"
fact_s started_utc "$(now_utc)"
fact_s stamp "$STAMP"
fact_s "src.dir" "$SRC_DIR"
fact_s toolchain.glibc "$(ldd --version | head -1)"
fact_s toolchain.cpu.model "$(lscpu | sed -n 's/^Model name:[[:space:]]*//p' | head -1)"
fact "toolchain.cpu.online" "$(nproc)"
fact_s spec.requirement "portable = -O2, no -march=native, gcc and clang, held to structural equality and to the checker (spec §1)"

# arun prints a wall-clock field; every other field of its summary is deterministic.
strip_time() { sed 's/time [0-9][0-9.]*//g' || true; }

# ---------------------------------------------------------------- the fixture
# 200 centres from the recorded covering file, with the header count rewritten: a
# truncated file that still says 249878 aborts in CenterList::load (it reads exactly z).
if [[ ! -f $FIXTURE ]]; then
    { printf '112 200\n'; sed -n '2,201p' -- "$RECORDED"; } >"$FIXTURE"
    fact_s "fixture.generated_from" "$RECORDED"
fi
fixture_lines=$(wc -l <"$FIXTURE")
fixture_header=$(head -c 8 -- "$FIXTURE")
fact_file fixture "$FIXTURE"
fact "fixture.lines" "$fixture_lines"
if [[ $fixture_lines -eq 201 && $fixture_header == "112 200" ]]; then pass_check fixture.format; else
    fail_check fixture.format "fixture has $fixture_lines lines, header '$fixture_header'"
fi

# ---------------------------------------------------------------- faithful reference
if [[ -z $FAITHFUL_OUT ]]; then
    base_log=$REPO/work/10-recreate/logs/build-base-$STAMP.json
    bstatus=0
    bout=$("$HARNESS/build/faithful.sh" --src "$SRC_DIR" --out "$HARNESS/out/faithful-base" \
        --log "$base_log" --force 2>&1) || bstatus=$?
    fact "faithful.exit" "$bstatus"
    fact_s "faithful.log" "$base_log"
    if (( bstatus != 0 )); then
        fail_check faithful.build "faithful.sh exited $bstatus; cannot compare portable output"
    else
        pass_check faithful.build
        FAITHFUL_OUT=$(sed -n 's/.*out=\([^ ]*\).*/\1/p' <<<"$bout" | tail -1)
    fi
fi
fact_s faithful.out "$FAITHFUL_OUT"
if [[ -x $FAITHFUL_OUT/arun ]]; then pass_check faithful.arun; else
    fail_check faithful.arun "no faithful arun in '$FAITHFUL_OUT'"
fi

# ---------------------------------------------------------------- arun on the fixture
arun_run() { # arun_run <dir> <binary>  -> echoes the exit status
    local dir=$1 bin status=0
    bin=$(realpath -m -- "$2")
    dir=$(realpath -m -- "$dir")
    mkdir -p -- "$dir"
    ( cd -- "$dir" && "$bin" "$FIXTURE" 0 1 records.bin bad.txt ) \
        >"$dir/stdout" 2>"$dir/stderr" || status=$?
    printf '%s' "$status"
}

if [[ -x $FAITHFUL_OUT/arun ]]; then
    ref=$HARNESS/out/tmp/arun-faithful-$STAMP
    st=$(arun_run "$ref" "$FAITHFUL_OUT/arun")
    fact "reference.exit" "$st"
    fact_file reference.records "$ref/records.bin"
    fact_file reference.bad "$ref/bad.txt"
    fact_s reference.stdout "$(strip_time <"$ref/stdout" || true)"
    if [[ -f $ref/records.bin ]]; then pass_check reference.records; else
        fail_check reference.records "faithful arun wrote no records for the fixture"
    fi
fi

# ---------------------------------------------------------------- compiler legs
leg() { # leg <tag> <compiler words...>
    local tag=$1; shift
    local -a cxx=( "$@" )
    local cxx_str="${cxx[*]}"
    fact_s "leg.$tag.compiler" "$cxx_str"
    fact "leg.$tag.compiler_present" "$(command -v -- "${cxx[0]}" >/dev/null 2>&1 && echo true || echo false)"

    # preflight: can this compiler build a <cstdio> program at all?
    local hello=$HARNESS/out/tmp/hello-$tag-$STAMP.cpp
    local hstatus=0 hlog=$HARNESS/out/tmp/hello-$tag-$STAMP.log
    printf '#include <cstdio>\nint main(){std::printf("ok\\n");}\n' >"$hello"
    "${cxx[@]}" -O2 "$hello" -o "$hello.bin" >"$hlog" 2>&1 || hstatus=$?
    fact "leg.$tag.preflight_exit" "$hstatus"
    if (( hstatus != 0 )); then
        fact_s "leg.$tag.status" "skipped"
        fact_s "leg.$tag.reason" "preflight failed: $(head -c 400 -- "$hlog" | tr '\n' ' ')"
        SKIPPED=$((SKIPPED + 1))
        printf 'SKIP leg %s: the compiler cannot build a <cstdio> program (%s)\n' \
            "$tag" "$(head -1 -- "$hlog")" >&2
        return 0
    fi
    pass_check "leg.$tag.preflight"

    # the portable build itself
    local out=$HARNESS/out/portable-$tag-$STAMP
    local blog=$HARNESS/out/tmp/portable-$tag-$STAMP.log
    local bstatus=0
    make -f "$HARNESS/build/portable.mk" MODE=mono SRC="$SRC_DIR" OUT="$out" \
        CXX="$(printf '%s ' "${cxx[@]}" | sed 's/ $//')" all >"$blog" 2>&1 || bstatus=$?
    fact "leg.$tag.build_exit" "$bstatus"
    fact_s "leg.$tag.build_log" "$blog"
    fact "leg.$tag.warnings" "$(grep -c 'warning:' "$blog" || true)"
    if (( bstatus == 0 )); then pass_check "leg.$tag.build"; else
        fail_check "leg.$tag.build" "make exited $bstatus, see $blog"
    fi
    local built=0 p
    for p in covrun arun brun crun; do
        [[ -x $out/$p ]] && built=$((built + 1))
        fact_file "leg.$tag.artefacts.$p" "$out/$p"
    done
    fact "leg.$tag.programs" "$built"
    if (( built == 4 )); then pass_check "leg.$tag.programs"; else
        fail_check "leg.$tag.programs" "only $built of 4 programs built"
    fi

    # -march=native must not be in effect.  On this AVX2 host the faithful build emits
    # VEX-encoded scalar SSE (vmovsd/vaddsd/...); the x86-64 baseline cannot.
    if [[ -x $out/covrun ]]; then
        vex=$(objdump -d "$out/covrun" | grep -cE '\bv(movsd|addsd|mulsd|subsd|divsd|sqrtsd|xorp[ds]|ucomisd)\b' || true)
        fact "leg.$tag.covrun_vex_instructions" "$vex"
        if (( vex == 0 )); then pass_check "leg.$tag.no_march_native"; else
            fail_check "leg.$tag.no_march_native" "portable covrun has $vex AVX-encoded scalar instructions, so AVX was enabled"
        fi
    fi
    if [[ -x $FAITHFUL_OUT/covrun && -x $out/covrun ]]; then
        fvex=$(objdump -d "$FAITHFUL_OUT/covrun" | grep -cE '\bv(movsd|addsd|mulsd|subsd|divsd|sqrtsd|xorp[ds]|ucomisd)\b' || true)
        fact "leg.$tag.faithful_vex_instructions" "$fvex"
    fi

    # the probe, where the probe permits it
    if [[ ${cxx[0]} == clang* ]]; then
        fact_s "leg.$tag.probe.status" "skipped"
        fact_s "leg.$tag.probe.reason" "abi-fp-probe.cpp #errors when __clang__ is defined; the probe hard-requires GCC (spec §1)"
        SKIPPED=$((SKIPPED + 1))
    else
        local pstatus=0 plog=$HARNESS/out/tmp/probe-$tag-$STAMP.log
        make -f "$HARNESS/build/portable.mk" MODE=mono SRC="$SRC_DIR" OUT="$out" \
            CXX="$(printf '%s ' "${cxx[@]}" | sed 's/ $//')" probe >>"$blog" 2>&1 || pstatus=$?
        local prun=0 pout=
        if [[ -x $out/abi-fp-probe ]]; then pout=$("$out/abi-fp-probe" 2>&1) || prun=$?; fi
        fact "leg.$tag.probe.build_exit" "$pstatus"
        fact "leg.$tag.probe.exit" "$prun"
        fact_s "leg.$tag.probe.stdout" "$pout"
        if (( pstatus == 0 && prun == 0 )) && [[ $pout == *"checks passed"* ]]; then
            pass_check "leg.$tag.probe"
        else
            fail_check "leg.$tag.probe" "portable probe build $pstatus, exit $prun, stdout '$pout'"
        fi
    fi

    # structural equality on real input: records from the portable arun must match
    if [[ -x $out/arun && -f $HARNESS/out/tmp/arun-faithful-$STAMP/records.bin ]]; then
        local dir=$HARNESS/out/tmp/arun-$tag-$STAMP st
        st=$(arun_run "$dir" "$out/arun")
        fact "leg.$tag.arun_exit" "$st"
        fact_file "leg.$tag.arun_records" "$dir/records.bin"
        fact_file "leg.$tag.arun_bad" "$dir/bad.txt"
        fact_s "leg.$tag.arun_stdout" "$(strip_time <"$dir/stdout" || true)"
        if cmp -s -- "$HARNESS/out/tmp/arun-faithful-$STAMP/records.bin" "$dir/records.bin"; then
            pass_check "leg.$tag.arun_records"
        else
            fail_check "leg.$tag.arun_records" "portable arun records differ from the faithful build's on the fixture"
        fi
        if cmp -s -- "$HARNESS/out/tmp/arun-faithful-$STAMP/bad.txt" "$dir/bad.txt"; then
            pass_check "leg.$tag.arun_bad"
        else
            fail_check "leg.$tag.arun_bad" "portable arun bad file differs from the faithful build's"
        fi
        if [[ $(strip_time <"$dir/stdout") == $(strip_time <"$HARNESS/out/tmp/arun-faithful-$STAMP/stdout") ]]; then
            pass_check "leg.$tag.arun_stdout"
        else
            fail_check "leg.$tag.arun_stdout" "per-leg stdout differs from the faithful build's (time fields excluded)"
        fi
    fi

    # optional end-to-end: does this leg's covrun reproduce the recorded covering file?
    if (( FULL )) && [[ -x $out/covrun ]]; then
        local rlog=$REPO/work/10-recreate/logs/R2-portable-$tag-$STAMP.json rstatus=0
        "$HARNESS/reproduce.sh" --no-build --build-out "$out" --log "$rlog" \
            --work "$HARNESS/out/repro-$tag-$STAMP" >"$HARNESS/out/tmp/full-$tag-$STAMP.txt" 2>&1 || rstatus=$?
        fact "leg.$tag.full_reproduction_exit" "$rstatus"
        fact_s "leg.$tag.full_reproduction_log" "$rlog"
        if (( rstatus == 0 )); then pass_check "leg.$tag.full_reproduction"; else
            fail_check "leg.$tag.full_reproduction" "portable covrun did not reproduce centers.txt (exit $rstatus, log $rlog)"
        fi
    fi
    fact_s "leg.$tag.status" "ran"
}

read -r -a compilers <<<"$COMPILERS"
for c in "${compilers[@]}"; do
    tag=$(printf '%s' "$c" | tr -c 'a-zA-Z0-9' '_')
    if ! command -v -- "$c" >/dev/null 2>&1; then
        # a driver spelled `clang --driver-mode=g++` is the usual way a clang++ is missing
        if [[ $c == clang++ ]] && command -v clang >/dev/null 2>&1; then
            leg clang clang --driver-mode=g++
            continue
        fi
        fact_s "leg.$tag.status" "skipped"
        fact_s "leg.$tag.reason" "'$c' is not on PATH"
        SKIPPED=$((SKIPPED + 1))
        printf 'SKIP leg %s: %s is not on PATH\n' "$tag" "$c" >&2
        continue
    fi
    leg "$tag" "$c"
done

# ---------------------------------------------------------------- finish
fact "checks.total" "$CHECKS"
fact "checks.failures" "$FAILS"
fact "legs.skipped" "$SKIPPED"
fact "duration_ms" "$(ms_since "$T_START")"
fact_s finished_utc "$(now_utc)"
fact_s log.path "$LOG_FILE"
if (( FAILS > 0 )); then
    fact_s status "fail"
    fact "pass" false
    emit_json "$FACTS" "$LOG_FILE"
    printf 'FAIL unit=R0-portable pass=false checks=%d failures=%d skipped=%d log=%s\n' \
        "$CHECKS" "$FAILS" "$SKIPPED" "$LOG_FILE"
    exit 1
fi
if (( SKIPPED > 0 )); then
    fact_s status "incomplete"
    fact "pass" false
    emit_json "$FACTS" "$LOG_FILE"
    printf 'INCOMPLETE unit=R0-portable pass=false checks=%d skipped=%d log=%s: a required leg could not be run\n' \
        "$CHECKS" "$SKIPPED" "$LOG_FILE"
    exit 3
fi
fact_s status "pass"
fact "pass" true
emit_json "$FACTS" "$LOG_FILE"
printf 'PASS unit=R0-portable pass=true checks=%d log=%s\n' "$CHECKS" "$LOG_FILE"
exit 0
