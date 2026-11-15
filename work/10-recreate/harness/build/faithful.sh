#!/usr/bin/env bash
# harness/build/faithful.sh -- the faithful build of spec/interfaces.md §1.
#
# One translation unit per program, the upstream include chain verbatim, the exact
# published flags (g++ -O3 -march=native -ffp-contract=off, -std=gnu++17 for the three
# later binaries), abi-fp-probe gated in, include-chain and pow(x,2) checks, and a
# provenance JSON log with compiler, CPU, glibc, flags and every artefact's sha256.
#
# usage: faithful.sh [--src DIR] [--out DIR] [--log FILE] [--cxx PATH] [--stamp S]
#                    [--no-probe] [--force]
#   --src      sources to build; default .scratch/gh/upstream, else work/10-recreate/src/amalgam
#   --out      output directory; default harness/out/faithful-<stamp> (never clobbered)
#   --log      JSON log; default work/10-recreate/logs/build-<stamp>.json
#   --cxx      compiler; default $CXX or g++
#   --no-probe build without running abi-fp-probe (the gate R0 check then fails)
#   --force    accept an existing --out by building into a fresh suffixed directory
# exit: 0 every check passed; 1 a check failed (log still written); 2 usage/refusal
#
# The two commands this script exists to make checkable:
#   harness/build/faithful.sh --src .scratch/gh/upstream
#   harness/reproduce.sh            # R2: covrun must reproduce centers.txt
set -euo pipefail
export LANG=C LC_ALL=C

self=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
# shellcheck source=../lib/common.sh
. "$self/../lib/common.sh"

CXX_BIN=${CXX:-g++}
SRC_DIR=
OUT_DIR=
LOG_FILE=
STAMP=$(stamp)
DO_PROBE=1
FORCE=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --src) SRC_DIR=${2:?--src needs a directory}; shift 2 ;;
        --out) OUT_DIR=${2:?--out needs a directory}; shift 2 ;;
        --log) LOG_FILE=${2:?--log needs a file}; shift 2 ;;
        --cxx) CXX_BIN=${2:?--cxx needs a compiler}; shift 2 ;;
        --stamp) STAMP=${2:?--stamp needs a value}; shift 2 ;;
        --no-probe) DO_PROBE=0; shift ;;
        --force) FORCE=1; shift ;;
        -h|--help) sed -n '2,22p' "$0"; exit 0 ;;
        *) printf 'unknown argument: %s\n' "$1" >&2; exit 2 ;;
    esac
done

if [[ -z $SRC_DIR ]]; then
    if [[ -d $REPO/.scratch/gh/upstream ]]; then
        SRC_DIR=$REPO/.scratch/gh/upstream
    else
        SRC_DIR=$REPO/work/10-recreate/src/amalgam
    fi
fi
[[ -d $SRC_DIR ]] || { printf 'source directory not found: %s\n' "$SRC_DIR" >&2; exit 2; }
SRC_DIR=$(CDPATH= cd -- "$SRC_DIR" && pwd)
command -v -- "$CXX_BIN" >/dev/null 2>&1 || [[ -x $CXX_BIN ]] ||
    { printf 'compiler not found: %s\n' "$CXX_BIN" >&2; exit 2; }
[[ -n $OUT_DIR ]] || OUT_DIR=$HARNESS/out/faithful-$STAMP
[[ -n $LOG_FILE ]] || LOG_FILE=$REPO/work/10-recreate/logs/build-$STAMP.json
# absolute: callers cd, and a relative --out/--log then silently writes elsewhere
OUT_DIR=$(realpath -m -- "$OUT_DIR")
LOG_FILE=$(realpath -m -- "$LOG_FILE")
LOG_FILE=$(unique_log_path "$LOG_FILE")

# never clobber an earlier build: suffix instead
if [[ -e $OUT_DIR && -n $(ls -A -- "$OUT_DIR" 2>/dev/null) ]]; then
    if (( FORCE )); then
        n=2
        while [[ -e $OUT_DIR-$n ]]; do n=$((n + 1)); done
        OUT_DIR=$OUT_DIR-$n
    else
        printf 'refusing: output directory is not empty: %s\n' "$OUT_DIR" >&2
        printf 'pick another --out, or pass --force to build into a fresh suffixed directory\n' >&2
        exit 2
    fi
fi
mkdir -p -- "$OUT_DIR" "$HARNESS/out/tmp"

T_START=$(now_us)
FACTS=$HARNESS/out/tmp/faithful-$STAMP.tsv
: >"$FACTS"

PROGRAMS=(covrun arun brun crun)
SOURCES=(abi-fp-probe.cpp seed.cpp ub.cpp patchx.cpp atlas.cpp stageB.cpp stageC.cpp covout.cpp)

fact_s unit "R0-build"
fact_s script "$0"
fact_s started_utc "$(now_utc)"
fact_s stamp "$STAMP"
fact_s "src.dir" "$SRC_DIR"
fact_s "out.dir" "$OUT_DIR"
fact "probe.enabled" "$([[ $DO_PROBE -eq 1 ]] && echo true || echo false)"

# ---------------------------------------------------------------- toolchain facts
CXX_PATH=$(command -v -- "$CXX_BIN" || printf '%s' "$CXX_BIN")
fact_s toolchain.compiler.path "$CXX_PATH"
fact_s toolchain.compiler.version "$("$CXX_BIN" --version | head -1)"
fact_s toolchain.compiler.full_version "$("$CXX_BIN" --version | tr '\n' ';' | sed 's/;*$//')"
fact_s toolchain.compiler.target "$("$CXX_BIN" -dumpmachine)"
fact_s toolchain.compiler.dumpversion "$("$CXX_BIN" -dumpfullversion -dumpversion)"
fact_s toolchain.compiler.search_path "$(echo | "$CXX_BIN" -x c++ -E -v - 2>&1 | awk '/#include <...> search starts here/{f=1;next}/End of search list/{f=0}f{print}' | tr '\n' ' ')"
fact_s toolchain.compiler.libstdcxx "$(strings "$("$CXX_BIN" -print-file-name=libstdc++.so 2>/dev/null)" 2>/dev/null | sed -n 's/^GCC: \(.*\)/\1/p' | head -1)"
fact_s toolchain.glibc "$(ldd --version | head -1)"
fact_s toolchain.kernel "$(uname -sr)"
fact_s toolchain.distro "$(sed -n 's/^PRETTY_NAME=//p' /etc/os-release 2>/dev/null | tr -d '\"')"
fact_s toolchain.cpu.model "$(lscpu | sed -n 's/^Model name:[[:space:]]*//p' | head -1)"
fact_s toolchain.cpu.family "$(lscpu | sed -n 's/^CPU family:[[:space:]]*//p')"
fact_s toolchain.cpu.model_no "$(lscpu | sed -n 's/^Model:[[:space:]]*//p')"
fact_s toolchain.cpu.stepping "$(lscpu | sed -n 's/^Stepping:[[:space:]]*//p')"
fact_s toolchain.cpu.hypervisor "$(lscpu | sed -n 's/^Hypervisor vendor:[[:space:]]*//p')"
fact_s toolchain.cpu.flags "$(lscpu | sed -n 's/^Flags:[[:space:]]*//p')"
fact "toolchain.cpu.online" "$(nproc)"
fact_s toolchain.cpu.march_native "$("$CXX_BIN" -march=native -Q --help=target 2>/dev/null | awk '/^  -march=/{print $2; exit}')"
fact_s toolchain.flags.faithful "-O3 -march=native -ffp-contract=off"
fact_s toolchain.flags.faithful_gnu17 "-std=gnu++17 -O3 -march=native -ffp-contract=off"
fact_s toolchain.fp_options "$("$CXX_BIN" -Q --help=optimizers -x c++ /dev/null 2>/dev/null | awk '/fp-contract|math-errno|rounding-math|trapping-math|unsafe-math-optimizations/{gsub(/^[ \t]+|[ \t]+$/,""); printf "%s; ", $0}')"
fact_s toolchain.probe_requirements "x86-64 GNU/Linux; GNU GCC (not clang); no -ffast-math; binary64; 8-bit bytes; 32-bit int; 64-bit uint64_t==unsigned long; FLT_EVAL_METHOD==0; FE_TONEAREST; gradual underflow; masked exceptions; FTZ/DAZ clear"

# ---------------------------------------------------------------- source facts
missing=0
for f in "${SOURCES[@]}"; do
    k=${f//[-.]/_}
    if [[ -f $SRC_DIR/$f ]]; then
        fact_s "src.files.$k.path" "$SRC_DIR/$f"
        fact_s "src.files.$k.sha256" "$(sha256_of "$SRC_DIR/$f")"
        fact "src.files.$k.bytes" "$(size_of "$SRC_DIR/$f")"
    else
        fact "src.files.$k.missing" true
        fail_check "src.present" "missing source file: $SRC_DIR/$f"
        missing=1
    fi
done
if (( missing == 0 )); then pass_check src.present; fi

if [[ $SRC_DIR != "$REPO/.scratch/gh/upstream" && -d $REPO/.scratch/gh/upstream ]]; then
    same=0; diffn=0
    for f in "${SOURCES[@]}"; do
        if [[ -f $SRC_DIR/$f && -f $REPO/.scratch/gh/upstream/$f ]] &&
           [[ $(sha256_of "$SRC_DIR/$f") == "$(sha256_of "$REPO/.scratch/gh/upstream/$f")" ]]; then
            same=$((same + 1))
        else
            diffn=$((diffn + 1))
        fi
    done
    fact "src.vs_published_cache.identical_files" "$same"
    fact "src.vs_published_cache.differing_files" "$diffn"
    fact_s "src.origin" "recreation-src"
else
    fact_s "src.origin" "published-cache"
fi

# ------------------------------------------------- include chain (spec §1, guards)
# each includer defines the includee's own guard on line 1 and includes it on line 2.
# fields: <file> <defines> <includes> <own guard>
chain=(
    "covout.cpp  HEADER        seed.cpp    -"
    "ub.cpp      HEADER        seed.cpp    UB_HEADER"
    "patchx.cpp  UB_HEADER     ub.cpp      PATCH_HEADER"
    "atlas.cpp   PATCH_HEADER  patchx.cpp  ATLAS_HEADER"
    "stageB.cpp  ATLAS_HEADER  atlas.cpp   REFINE_HEADER"
    "stageC.cpp  REFINE_HEADER stageB.cpp  STAGEC_HEADER"
    "seed.cpp    -             -           HEADER"
)
for row in "${chain[@]}"; do
    read -r file defines includes own <<<"$row"
    k=${file//./_}
    ok=1; detail=""
    if [[ $defines != - ]]; then
        line1=$(sed -n '1p' "$SRC_DIR/$file")
        [[ $line1 == "#define $defines" ]] || { ok=0; detail+="line 1 is '$line1' not '#define $defines'; "; }
        line2=$(sed -n '2p' "$SRC_DIR/$file")
        [[ $line2 == "#include \"$includes\"" ]] || { ok=0; detail+="line 2 is '$line2' not '#include \"$includes\"'; "; }
    fi
    if [[ $own != - ]]; then
        n=$(grep -c "^#ifndef $own\$" "$SRC_DIR/$file" || true)
        [[ $n -eq 1 ]] || { ok=0; detail+="'#ifndef $own' occurs $n times; "; }
        main_line=$(grep -n 'int main' "$SRC_DIR/$file" | head -1 | cut -d: -f1 || true)
        guard_line=$(grep -n "^#ifndef $own\$" "$SRC_DIR/$file" | cut -d: -f1 || true)
        if [[ -n $main_line && -n $guard_line ]] && (( main_line < guard_line )); then
            ok=0; detail+="its main is not hidden behind $own; "
        fi
    fi
    if (( ok )); then pass_check "chain.$k"; else fail_check "chain.$k" "$detail"; fi
done

# each program's preprocessed TU must contain exactly one main: the include chain, not
# the linker, is what keeps the other stages' drivers out.
if (( missing == 0 )); then
    for pair in "covrun:covout.cpp" "arun:atlas.cpp" "brun:stageB.cpp" "crun:stageC.cpp"; do
        prog=${pair%%:*}; top=${pair##*:}
        n=$(cd -- "$SRC_DIR" && { "$CXX_BIN" -std=gnu++17 -E -P -x c++ "$top" 2>/dev/null || true; } |
            grep -o 'int main' | wc -l || true)
        fact "tunit.$prog.main_definitions" "$n"
        fact_s "tunit.$prog.top_file" "$top"
        if [[ $n -eq 1 ]]; then pass_check "tunit.$prog"; else
            fail_check "tunit.$prog" "preprocessed $top has $n 'int main', expected 1"
        fi
    done
fi

# ---------------------------------------------------------------- compilation
BUILD_FAILED=0
# compile <output-name> <source-path> [compiler flags...] -- published command shape
compile() {
    local name=$1 source=$2; shift 2
    local out=$OUT_DIR/$name
    local clog=$OUT_DIR/compile-$name.log
    local t0 status=0
    t0=$(now_us)
    if ( cd -- "$SRC_DIR" && "$CXX_BIN" "$@" "$source" -o "$out" ) >"$clog" 2>&1; then
        status=0
    else
        status=$?
    fi
    fact "builds.$name.status" "$status"
    fact_s "builds.$name.argv" "$CXX_BIN $* $source -o $out"
    fact "builds.$name.ms" "$(ms_since "$t0")"
    fact "builds.$name.warnings" "$(grep -c 'warning:' "$clog" || true)"
    if (( status != 0 )); then
        BUILD_FAILED=1
        fail_check "build.$name" "compiler exit $status, see $clog"
        tail -n 15 -- "$clog" >&2
    else
        pass_check "build.$name"
    fi
}

# probe first: spec §1 -- refuse to proceed if it fails
compile abi-fp-probe-covrun "$SRC_DIR/abi-fp-probe.cpp" -O3 -march=native -ffp-contract=off
compile abi-fp-probe-abc "$SRC_DIR/abi-fp-probe.cpp" -std=gnu++17 -O3 -march=native -ffp-contract=off

run_probe() { # run_probe <label> <binary>
    local label=$1 bin=$2 status=0 out
    out=$("$bin" 2>&1) || status=$?
    fact "probe.$label.exit" "$status"
    fact_s "probe.$label.stdout" "$out"
    if (( status == 0 )) && [[ $out == *"checks passed"* ]]; then
        pass_check "probe.$label"
    else
        fail_check "probe.$label" "exit $status, stdout '$out'"
    fi
}

if (( DO_PROBE )); then
    run_probe abi_probe_covrun "$OUT_DIR/abi-fp-probe-covrun"
    run_probe abi_probe_abc "$OUT_DIR/abi-fp-probe-abc"
    if (( FAILS > 0 )); then
        fact_s refused "the ABI/FP probe did not pass; the four programs were not built"
        fact "pass" false
        fact "checks.total" "$CHECKS"
        fact "checks.failures" "$FAILS"
        fact "duration_ms" "$(ms_since "$T_START")"
        fact_s finished_utc "$(now_utc)"
        fact_s log.path "$LOG_FILE"
        emit_json "$FACTS" "$LOG_FILE"
        printf 'REFUSED unit=R0-build log=%s: abi-fp-probe failed, no programs built\n' "$LOG_FILE" >&2
        exit 1
    fi
else
    fact_s probe.skipped "--no-probe given: the R0 gate cannot pass without the probe"
    fail_check probe.enabled "--no-probe was given"
fi

compile covrun "$SRC_DIR/covout.cpp" -O3 -march=native -ffp-contract=off
compile arun   "$SRC_DIR/atlas.cpp"  -std=gnu++17 -O3 -march=native -ffp-contract=off
compile brun   "$SRC_DIR/stageB.cpp" -std=gnu++17 -O3 -march=native -ffp-contract=off
compile crun   "$SRC_DIR/stageC.cpp" -std=gnu++17 -O3 -march=native -ffp-contract=off

# --------------------------------------------- cover squares: pow(x,2) == x*x (§5.9)
sites=$(grep -c 'pow(' "$SRC_DIR/covout.cpp" || true)
fact "pow.source_sites" "$sites"
if [[ $sites -eq 2 ]]; then pass_check pow.source_sites; else
    fail_check pow.source_sites "covout.cpp has $sites pow( sites, expected 2"
fi

if [[ -x $OUT_DIR/covrun ]]; then
    nm -D "$OUT_DIR/covrun" >"$OUT_DIR/covrun.dynamic-symbols.txt"
    objdump -d -C "$OUT_DIR/covrun" >"$OUT_DIR/covrun.disassembly.txt"
    calls=$(grep -c 'call.*<pow@plt>' "$OUT_DIR/covrun.disassembly.txt" || true)
    imports=$(nm -D "$OUT_DIR/covrun" | grep -c 'pow@' || true)
    fact "pow.calls_in_covrun" "$calls"
    fact "pow.folded_to_multiply" "$([[ $calls -eq 0 ]] && echo true || echo false)"
    fact "pow.imports_libm" "$([[ $imports -gt 0 ]] && echo true || echo false)"
    if [[ $calls -eq 0 || $calls -eq $sites ]]; then
        pass_check pow.call_shape
    else
        fail_check pow.call_shape "covrun makes $calls pow calls for $sites pow( sites"
    fi
fi

# The numeric question behind §5.9: for the two arguments the cover uses, does the
# libm call return exactly the bits of a single multiply?  The published build keeps
# the call, so this -- not the folding -- is what byte-identity depends on.  The probe
# also reports how far the identity holds over 8e6 random doubles (on glibc 2.43 it
# fails on 4.5e-4 of them by 1 ulp; at the two cover arguments it holds).
if [[ -f $HARNESS/probe/cover-square-probe.cpp ]]; then
    compile cover-square-probe "$HARNESS/probe/cover-square-probe.cpp" -O3 -march=native -ffp-contract=off
    if [[ -x $OUT_DIR/cover-square-probe ]]; then
        imports=$(nm -D "$OUT_DIR/cover-square-probe" | grep -c 'pow@' || true)
        fact "pow.probe_libm_imports" "$imports"
        status=0
        out=$("$OUT_DIR/cover-square-probe" 2>&1) || status=$?
        fact "pow.equivalence_exit" "$status"
        fact_s "pow.equivalence_stdout" "$out"
        sweeps=$(sed -n 's/.*mismatches=\([0-9][0-9]*\).*/\1/p' <<<"$out" | head -1)
        fact "pow.sweep_mismatches" "${sweeps:-0}"
        if (( status == 0 )) && [[ $out == *"at_cover_arguments=yes"* ]] && (( imports > 0 )); then
            pass_check pow.equivalence
        else
            fail_check pow.equivalence "probe exit $status, libm imports $imports, stdout '$out'"
        fi
    else
        fail_check pow.equivalence "probe/cover-square-probe.cpp did not build"
    fi
else
    fail_check pow.equivalence "harness/probe/cover-square-probe.cpp is missing"
fi

# ---------------------------------------------------------------- artefacts
for f in "${PROGRAMS[@]}" abi-fp-probe-covrun abi-fp-probe-abc cover-square-probe \
         covrun.disassembly.txt covrun.dynamic-symbols.txt; do
    [[ -e $OUT_DIR/$f ]] || continue
    k=${f//[-.]/_}
    fact_file "artefacts.$k" "$OUT_DIR/$f"
done
built=0
for p in "${PROGRAMS[@]}"; do [[ -x $OUT_DIR/$p ]] && built=$((built + 1)); done
fact "artefacts.programs_built" "$built"
if (( built == 4 )); then pass_check artefacts.all_programs; else
    fail_check artefacts.all_programs "only $built of 4 programs were produced"
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
    printf 'PASS unit=R0-build pass=true checks=%d log=%s out=%s\n' "$CHECKS" "$LOG_FILE" "$OUT_DIR"
    exit 0
fi
fact "pass" false
emit_json "$FACTS" "$LOG_FILE"
printf 'FAIL unit=R0-build pass=false checks=%d failures=%d log=%s out=%s\n' "$CHECKS" "$FAILS" "$LOG_FILE" "$OUT_DIR"
exit 1
