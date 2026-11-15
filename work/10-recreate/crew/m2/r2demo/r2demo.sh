#!/usr/bin/env bash
# r2demo.sh - settling test for findings H-1..H-6 (K/m2, direction k2).
# Shows, in seconds, which plausible R2 harnesses report PASS for a covrun that
# did not produce the recorded centres.  Each "stub" stands in for ./build/covrun;
# the harness code is the thing under test.
# Usage: bash r2demo.sh [REFERENCE_CENTERS]
set -u
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO=$(CDPATH= cd -- "$HERE/../../../../.." && pwd)
REF=${1:-$REPO/work/10-recreate/crew/m3/saved-run/execution/data/centers.txt}
D=$HERE/tmp; rm -rf "$D"; mkdir -p "$D"

cp -- "$REF" "$D/REF.txt"            # demo never mutates the real reference
REFHASH=$(sha256sum "$D/REF.txt" | cut -d' ' -f1)
SIZE=$(stat -c %s "$D/REF.txt")

stub_good()   { cp -- "$D/REF.txt" "$1"; printf 'N112 r0.0320 dual2 checked151744086 centers249878 visit29769262282 near3341641851 cheap45648766 lp3134060273\n'; }
stub_noop()   { :; }
stub_abort()  { ( exit 134 ); }
stub_stdout() { printf 'N112 r0.0320 dual2 checked151744086 centers249878 visit29769262282 near3341641851 cheap45648766 lp3134060273\ntime 401.82\n'; }
stub_trunc()  { head -c 4096 "$D/REF.txt" > "$1"; }
stub_wrong()  { head -c 4096 /dev/zero > "$1"; }

h_naive() {   # run, then cmp; no rm, exit status ignored
  local out=$D/work/centers.txt; mkdir -p "$D/work"
  "$@" "$out" >"$D/h1.log" 2>&1
  if cmp -s "$out" "$D/REF.txt"; then echo PASS; else echo FAIL; fi
}
h_stdout() {  # gate the informational summary instead of the artefact
  local out=$D/work/centers.txt; mkdir -p "$D/work"
  "$@" "$out" >"$D/h2.log" 2>&1
  if grep -q 'centers249878' "$D/h2.log"; then echo PASS; else echo FAIL; fi
}
h_wrongfile() {  # hash computed with cwd in the directory holding the reference
  local out=$D/work/centers.txt; mkdir -p "$D/work"
  "$@" "$out" >"$D/h3.log" 2>&1
  if ( cd "$D" && sha256sum REF.txt | grep -q "^$REFHASH" ); then echo PASS; else echo FAIL; fi
}
h_samefile() {   # OUT is the reference itself: the argv the recorded run used
  "$@" "$D/REF.txt" >"$D/h4.log" 2>&1
  if cmp -s "$D/REF.txt" "$D/REF.txt"; then echo PASS; else echo FAIL; fi
}
h_guarded() {    # the checklist in findings/harness-2
  local out=$D/work/g/centers.txt; rm -rf "$D/work/g"; mkdir -p "$D/work/g"
  [ -e "$out" ] && { echo "FAIL(stale)"; return; }
  [ "$out" -ef "$D/REF.txt" ] && { echo "FAIL(inode)"; return; }
  local rc=0; "$@" "$out" >"$D/h5.log" 2>&1 || rc=$?
  [ $rc -eq 0 ] || { echo "FAIL(rc=$rc)"; return; }
  [ -f "$out" ] || { echo "FAIL(missing)"; return; }
  [ "$(stat -c %s "$out")" -eq "$SIZE" ] || { echo "FAIL(size)"; return; }
  [ "$(tail -c1 "$out" | od -An -c | tr -d ' ')" = '\n' ] || { echo "FAIL(newline)"; return; }
  [ "$(sha256sum "$out" | cut -d' ' -f1)" = "$REFHASH" ] || { echo "FAIL(hash)"; return; }
  [ "$(sha256sum "$D/REF.txt" | cut -d' ' -f1)" = "$REFHASH" ] || { echo "FAIL(ref-mutated)"; return; }
  echo PASS
}
prep_stale() { mkdir -p "$D/work"; cp -- "$D/REF.txt" "$D/work/centers.txt"; }

printf '%-10s %-9s %-9s %-11s %-14s %-9s %s\n' STUB naive stdout wrongfile samefile guarded EXPECTED
for s in good noop abort stdout trunc wrong; do
  exp=PASS; case $s in noop|abort|stdout|trunc|wrong) exp=FAIL;; esac
  prep_stale; a=$(h_naive     "stub_$s")
  prep_stale; b=$(h_stdout    "stub_$s")
  prep_stale; c=$(h_wrongfile "stub_$s")
  cp -- "$D/REF.txt" "$D/REF.bak"; d=$(h_samefile "stub_$s")
  refok=ok; cmp -s "$D/REF.txt" "$D/REF.bak" || refok=DESTROYED
  cp -- "$D/REF.bak" "$D/REF.txt"
  e=$(h_guarded "stub_$s")
  printf '%-10s %-9s %-9s %-11s %-14s %-9s %s\n' "$s" "$a" "$b" "$c" "$d/$refok" "$e" "$exp"
done
echo; echo "REF sha256 $REFHASH size $SIZE"
