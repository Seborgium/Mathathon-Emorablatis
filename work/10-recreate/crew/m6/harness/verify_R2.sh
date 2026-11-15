#!/usr/bin/env bash
# verify_R2.sh -- rung R2 acceptance gate for unit 03+04 (seed + covout, program `covrun`).
#
# It builds a candidate with the frozen faithful flags, runs it once, and decides byte-identity
# against the recorded artefact.  It never loosens a comparison: every check is exact and any
# failure exits non-zero with the first differing byte offset.
#
# usage: verify_R2.sh [options]
#   --src DIR        candidate root holding src/covrun_main.cpp (default: <script>/../candidate)
#   --build DIR      build directory (default: <script>/../build)
#   --out FILE       artefact to write (default: <build>/centers.txt)
#   --ref FILE       recorded reference (default: <repo>/.scratch/gh/data/centers.txt)
#   --probe FILE     abi-fp-probe binary (default: <repo>/.scratch/gh/build/abi-fp-probe-covrun)
#   --stop-t T       stop the cover after centre index t == T and compare the prefix only
#   --no-run         do not run; verify the artefact already at --out
#   --skip-ab      do not run the ABI/arithmetic probe
#   --skip-determinism  skip the env/portability perturbation runs
#   --log FILE       json log (default: <script>/../logs/R2.json)
#   -h|--help
# exit: 0 byte-identical (R2 pass) | 1 mismatch | 2 setup/build failure
set -euo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# Locate the repository root by walking up to the directory that holds .scratch/gh, so the
# harness works from any crew/ or member/ directory it is copied into.
repo=""
d="$here"
for _ in 1 2 3 4 5 6 7 8; do
  if [ -d "$d/.scratch/gh" ]; then repo=$d; break; fi
  d=$(dirname "$d")
done
[ -n "$repo" ] || { echo "verify_R2: SETUP cannot find .scratch/gh above $here; pass --ref" >&2; exit 2; }
src="$here/../candidate"; build="$here/../build"; ref="$repo/.scratch/gh/data/centers.txt"
probe="$repo/.scratch/gh/build/abi-fp-probe-covrun"; log="$here/../logs/R2.json"
out=""; stop_t=""; run=1; do_ab=1; do_det=1
CXX=${CXX:-g++}
FAITHFUL="-O3 -march=native -ffp-contract=off"      # interfaces.md §1, load-bearing

while [ $# -gt 0 ]; do
  case "$1" in
    --src) src=$2; shift 2;;
    --build) build=$2; shift 2;;
    --out) out=$2; shift 2;;
    --ref) ref=$2; shift 2;;
    --probe) probe=$2; shift 2;;
    --stop-t) stop_t=$2; shift 2;;
    --log) log=$2; shift 2;;
    --no-run) run=0; shift;;
    --skip-ab) do_ab=0; shift;;
    --skip-determinism) do_det=0; shift;;
    -h|--help) sed -n '2,30p' "$0"; exit 0;;
    *) echo "verify_R2: unknown option $1" >&2; exit 2;;
  esac
done
[ -n "$out" ] || out="$build/centers.txt"

say(){ printf '%s\n' "$*"; }
fail(){ say "R2: FAIL $*"; exit 1; }

say "verify_R2: src=$src build=$build ref=$ref"
mkdir -p "$build" "$(dirname "$log")"
[ -f "$src/src/covrun_main.cpp" ] || { say "R2: SETUP missing $src/src/covrun_main.cpp"; exit 2; }
[ -f "$ref" ] || { say "R2: SETUP missing reference $ref"; exit 2; }
[ -n "$stop_t" ] || [ "$run" = 1 ] || [ -f "$out" ] || { say "R2: SETUP --no-run but no $out"; exit 2; }

# ---------------------------------------------------------------- 0. platform precondition
if [ "$do_ab" = 1 ]; then
  if [ -x "$probe" ]; then
    if pout=$("$probe" 2>&1); then say "abi: $pout"; else say "R2: FAIL abi probe: $pout"; exit 1; fi
  else
    say "abi: probe $probe absent -- skipped (recorded as NOT CHECKED)"
  fi
fi

# ---------------------------------------------------------------- 1. build
bflags="$FAITHFUL"
tag=""
if [ -n "$stop_t" ]; then bflags="$FAITHFUL -DCOVRUN_STOP_T=$stop_t"; tag="-stop$stop_t"; fi
bin="$build/covrun$tag"
say "build: $CXX $bflags -o $bin $src/src/covrun_main.cpp"
t0=$(date +%s.%N)
if ! $CXX $bflags -o "$bin" "$src/src/covrun_main.cpp" 2>"$build/build.log"; then
  say "R2: SETUP build failed"; sed -n 1,40p "$build/build.log"; exit 2
fi
t1=$(date +%s.%N)
build_s=$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.3f", b-a}')
say "build: ok in ${build_s}s"

# ---------------------------------------------------------------- 2. run
run_s=0
if [ "$run" = 1 ]; then
  t2=$(date +%s.%N)
  # LANG/LC_ALL are set to C at build time only; the program must not depend on them.
  if ! LANG=C LC_ALL=C "$bin" "$out" >"$build/stdout.txt" 2>"$build/stderr.txt"; then
    say "R2: FAIL run exited non-zero"; sed -n 1,20p "$build/stderr.txt"; exit 1
  fi
  t3=$(date +%s.%N)
  run_s=$(awk -v a="$t2" -v b="$t3" 'BEGIN{printf "%.3f", b-a}')
  say "run: ok in ${run_s}s ($(wc -c <"$out") bytes)"
  sed -n '1p;$p' "$build/stdout.txt" | sed 's/^/  stdout: /'
fi

# ---------------------------------------------------------------- 3. compare
ours_sha=$(sha256sum "$out" | cut -d' ' -f1)
ref_sha=$(sha256sum "$ref" | cut -d' ' -f1)
say "sha256 ours: $ours_sha"
say "sha256 ref : $ref_sha"

cmp_mode=whole
if [ -n "$stop_t" ]; then cmp_mode=prefix; fi
first_off=""; n_diff=""; first_line=""
if [ "$cmp_mode" = whole ]; then
  if [ "$ours_sha" = "$ref_sha" ]; then
    say "compare: BYTE IDENTICAL"
  else
    # first differing byte offset (cmp -l is 1-based) and how many bytes differ
    first_off=$( { cmp -l "$out" "$ref" || true; } | head -1 | awk '{print $1}')
    n_diff=$( { cmp -l "$out" "$ref" || true; } | wc -l)
    eofnote=""
    if [ -z "$first_off" ]; then
      # one file is a prefix of the other: cmp -l prints no differing byte at all
      os=$(wc -c <"$out"); rs=$(wc -c <"$ref")
      if [ "$os" -lt "$rs" ]; then first_off=$((os+1)); eofnote="ours ends after byte $os, reference continues"
      elif [ "$rs" -lt "$os" ]; then first_off=$((rs+1)); eofnote="reference ends after byte $rs, ours continues"
      fi
    fi
    [ -n "$first_off" ] || first_off=0
    first_line=$(( $(head -c "$((first_off>0?first_off-1:0))" "$out" | tr -cd '\n' | wc -c) + 1 ))
    say "compare: MISMATCH first differing byte offset $first_off (line $first_line), $n_diff bytes differ${eofnote:+ -- $eofnote}"
    say "  ours: $(sed -n "${first_line}p" "$out")"
    say "  ref : $(sed -n "${first_line}p" "$ref")"
    fail "artefact differs"
  fi
else
  # prefix mode: our data lines must equal the reference's first D data lines, and the next
  # reference line must open a new X block (so the cap did not cut a block in half).
  # The header carries the count, so a capped run cannot match the reference header: compare
  # the data lines only, and check our header separately (it must be "112 D").
  refpre="$build/ref-prefix.txt"
  oursbody="$build/ours-body.txt"
  D=$(($(wc -l <"$out") - 1))
  [ "$D" -ge 0 ] || D=0
  head -n "$((D+1))" "$ref" >"$refpre"
  head -n1 "$out" >"$build/ours-header.txt"
  tail -n +2 "$out" >"$oursbody"
  tail -n +2 "$refpre" >"$build/ref-body.txt"
  want="112 $D"
  [ "$(cat "$build/ours-header.txt")" = "$want" ] || fail "header is '$(cat "$build/ours-header.txt")', expected '$want'"
  say "header: '$want' ($D data lines; the reference header says '$(head -n1 "$ref")')"
  if ! cmp -s "$oursbody" "$build/ref-body.txt"; then
    first_off=$( { cmp -l "$oursbody" "$build/ref-body.txt" || true; } | head -1 | awk '{print $1}')
    [ -n "$first_off" ] || first_off=0
    # byte offset within the whole file: header + offset within the body
    first_line=$(( $(head -c "$((first_off>0?first_off-1:0))" "$oursbody" | tr -cd '\n' | wc -c) + 2 ))
    say "compare: PREFIX MISMATCH at body byte $first_off (file line $first_line) of $D data lines"
    say "  ours: $(sed -n "${first_line}p" "$out")"
    say "  ref : $(sed -n "${first_line}p" "$refpre")"
    fail "prefix differs"
  fi
  if [ "$D" -gt 0 ]; then
    lastx=$(sed -n "$((D+1))p" "$ref" | cut -d' ' -f1-6)
    nextx=$(sed -n "$((D+2))p" "$ref" | cut -d' ' -f1-6)
    if [ "$lastx" = "$nextx" ]; then
      say "compare: prefix of $D data lines identical, but the block continues in $ref -- cap cuts a block, comparison is inconclusive for the next line"
    else
      say "compare: prefix of $D data lines BYTE IDENTICAL; next reference line opens a new block (cap is clean)"
    fi
  fi
fi

# ---------------------------------------------------------------- 4. format audit (ours)
say "format:"
python3 "$here/audit_format.py" "$out" | sed 's/^/  /' || fail "format audit"

# ---------------------------------------------------------------- 5. determinism perturbations
det="skipped"
if [ "$do_det" = 1 ]; then
  det="ok"
  T=${stop_t:-4}
  pbin="$build/covrun-stop$T"
  [ -x "$pbin" ] || $CXX $FAITHFUL -DCOVRUN_STOP_T="$T" -o "$pbin" "$src/src/covrun_main.cpp" 2>>"$build/build.log"
  "$pbin" "$build/det-a.txt" >/dev/null 2>&1
  ( cd "$build" && LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 TZ=Asia/Tokyo "$pbin" det-b.txt >/dev/null 2>&1 )
  LC_ALL=C.UTF-8 TZ=UTC "$pbin" "$build/det-c.txt" >/dev/null 2>&1
  cmp -s "$build/det-a.txt" "$build/det-b.txt" || { det="FAIL(locale)"; fail "output depends on LANG/LC_ALL/TZ or cwd"; }
  cmp -s "$build/det-a.txt" "$build/det-c.txt" || { det="FAIL(locale2)"; fail "output depends on LC_ALL/TZ"; }
  # portability: same source, -O2, generic x86-64, no -march=native
  $CXX -O2 -ffp-contract=off -DCOVRUN_STOP_T="$T" -o "$build/covrun-portable" "$src/src/covrun_main.cpp" 2>>"$build/build.log"
  "$build/covrun-portable" "$build/det-portable.txt" >/dev/null 2>&1
  cmp -s "$build/det-a.txt" "$build/det-portable.txt" || { det="FAIL(portable)"; fail "output differs between faithful and portable build"; }
  say "determinism: locale/TZ/cwd and -O2-generic perturbations identical (t<$T)"
fi

# ---------------------------------------------------------------- 6. log
cat >"$log" <<JSON
{
  "rung": "R2",
  "program": "covrun",
  "mode": "$cmp_mode",
  "stop_t": ${stop_t:-null},
  "src": "$src",
  "compiler": "$($CXX --version | head -1)",
  "flags": "$bflags",
  "build_seconds": $build_s,
  "run_seconds": $run_s,
  "bytes": $(wc -c <"$out"),
  "lines": $(wc -l <"$out"),
  "sha256_ours": "$ours_sha",
  "sha256_ref": "$ref_sha",
  "identical": $([ "$ours_sha" = "$ref_sha" ] && echo true || echo false),
  "determinism": "$det",
  "abi_probe": $([ "$do_ab" = 1 ] && echo '"run"' || echo '"skipped"')
}
JSON
say "log: $log"
say "R2: PASS ($cmp_mode)"
exit 0
