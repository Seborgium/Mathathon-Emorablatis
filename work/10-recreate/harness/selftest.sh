#!/usr/bin/env bash
# selftest.sh -- proves the R2 gate actually fails, and that it reports the right byte offset.
# It mutates a copy of the reference in three ways and requires verify_R2.sh to reject each one
# with the exact first-differing-byte offset it planted, then requires the pristine copy to pass.
# usage: selftest.sh [--ref FILE]
set -euo pipefail
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
V="$here/verify_R2.sh"
work="$here/../logs/selftest"; rm -rf "$work"; mkdir -p "$work"
repo=""; d="$here"
for _ in 1 2 3 4 5 6 7 8; do if [ -d "$d/.scratch/gh" ]; then repo=$d; break; fi; d=$(dirname "$d"); done
ref="${repo:-}/.scratch/gh/data/centers.txt"
[ $# -gt 0 ] && ref=$2
[ -f "$ref" ] || { echo "selftest: no reference at $ref" >&2; exit 2; }
ok=0; bad=0
expect_fail_at(){ # name offset(file) 1-based, or "EOF"
  local name=$1 want=$2 file=$3 got rc=0
  got=$(bash "$V" --no-run --out "$file" --skip-determinism --skip-ab \
        --log "$work/$name.json" 2>&1) || rc=$?
  if [ "$rc" -eq 0 ]; then echo "SELFTEST FAIL $name: gate accepted a mutated artefact"; bad=$((bad+1)); return; fi
  local got_off
  got_off=$(printf '%s\n' "$got" | sed -n 's/.*first differing byte offset \([0-9]*\).*/\1/p')
  if [ -z "$got_off" ]; then
    printf '%s\n' "$got" | tail -4 | sed 's/^/    /'
    echo "SELFTEST FAIL $name: no offset reported (expected $want)"; bad=$((bad+1)); return
  fi
  if [ "$got_off" = "$want" ]; then echo "SELFTEST ok   $name: rejected at byte $got_off (exit $rc)"; ok=$((ok+1));
  else echo "SELFTEST FAIL $name: rejected at byte $got_off, planted $want"; bad=$((bad+1)); fi
}
# 1. pristine copy must pass
cp "$ref" "$work/pristine.txt"
if bash "$V" --no-run --out "$work/pristine.txt" --skip-determinism --skip-ab --log "$work/pristine.json" >/dev/null 2>&1; then
  echo "SELFTEST ok   pristine copy accepted"; ok=$((ok+1))
else echo "SELFTEST FAIL pristine copy rejected"; bad=$((bad+1)); fi
# 2. one flipped digit at a known offset
python3 - "$ref" "$work/onedit.txt" <<'PY'
import sys
src, dst = sys.argv[1], sys.argv[2]
b = bytearray(open(src,'rb').read())
i = 5000                      # 1-based offset 5000
old = b[i-1]
b[i-1] = ord('7') if old != ord('7') else ord('8')
open(dst,'wb').write(bytes(b)); print('planted byte %d: %r -> %r' % (i, chr(old), chr(b[i-1])))
PY
expect_fail_at one-byte 5000 "$work/onedit.txt"
# 3. two bytes swapped at a known offset (same multiset of bytes, count unchanged)
python3 - "$ref" "$work/twoedit.txt" <<'PY'
import sys
src, dst = sys.argv[1], sys.argv[2]
b = bytearray(open(src,'rb').read())
i = 123457                    # 1-based offset
b[i-1], b[i] = (b[i-1] + 1) & 0x7f, b[i]
open(dst,'wb').write(bytes(b)); print('planted byte %d' % i)
PY
expect_fail_at two-bytes 123457 "$work/twoedit.txt"
# 4. truncated artefact
head -c 1000 "$ref" > "$work/short.txt"
expect_fail_at truncated 1001 "$work/short.txt"
# 5. one extra trailing byte
cp "$ref" "$work/long.txt"; printf 'x' >> "$work/long.txt"
expect_fail_at extra-byte 7339547 "$work/long.txt"
echo "SELFTEST: $ok ok, $bad fail"
[ "$bad" -eq 0 ] || exit 1
