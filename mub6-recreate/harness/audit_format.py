#!/usr/bin/env python3
"""audit_format.py FILE -- exact-format audit of a centres.txt (interfaces.md §3.1).

Checks, all of them exact:
  header "%d %zu\\n" with n>0 and 0<count<=2000000, count == number of data lines
  every data line: ten decimal integers, each followed by exactly one space, then '\\n',
    no CR, no tab, no leading '+', no leading zeros (except "0"), no other characters
  bins b0..b4 and y0..y3 in [0,n), s in [0,6)
  blocks: the key (b0..b4,s) is contiguous -- once it changes it never returns
Exit 0 iff all hold.  Prints one line per check.
"""
import sys

def main(path):
    fails = []
    with open(path, 'rb') as f:
        raw = f.read()
    if not raw:
        print('FAIL empty file'); return 1
    if not raw.endswith(b'\n'):
        fails.append('file does not end with a newline')
    nl = raw.index(b'\n')
    head = raw[:nl]
    parts = head.split(b' ')
    if len(parts) != 2:
        fails.append('header is not "%%d %%zu": %r' % head)
        n = count = None
    else:
        try:
            n, count = int(parts[0]), int(parts[1])
        except ValueError:
            fails.append('header fields not integers: %r' % head); n = count = None
    if n is not None:
        if not (n > 0):
            fails.append('n=%d not >0' % n)
        if not (0 < count <= 2000000):
            fails.append('count=%d out of (0,2e6]' % count)
    lines = raw[nl+1:-1].split(b'\n') if raw.endswith(b'\n') else raw[nl+1:].split(b'\n')
    body = lines if not (len(lines) == 1 and lines[0] == b'') else []
    if count is not None and len(body) != count:
        fails.append('header count %d != %d data lines' % (count, len(body)))
    badchar = 0; badfield = 0; badtrail = 0; badrange = 0
    prev_key = None; seen_keys = set(); noncontig = 0
    for i, ln in enumerate(body, 1):
        if b'\r' in ln or b'\t' in ln:
            badchar += 1; continue
        if not ln.endswith(b' '):
            badtrail += 1
        f2 = ln.split(b' ')
        if len(f2) != 11 or f2[-1] != b'':
            badfield += 1; continue
        ok = True
        for tok in f2[:10]:
            if tok == b'0':
                continue
            if not tok.isdigit() or tok.startswith(b'0'):
                ok = False
        if not ok:
            badfield += 1; continue
        v = [int(t) for t in f2[:10]]
        if n is not None:
            if any(not (0 <= x < n) for x in v[:5]) or any(not (0 <= x < n) for x in v[6:]):
                badrange += 1
            if not (0 <= v[5] < 6):
                badrange += 1
        key = tuple(v[:6])
        if key != prev_key:
            if key in seen_keys:
                noncontig += 1
            seen_keys.add(key); prev_key = key
    for name, bad in (('no CR/TAB', badchar), ('ten fields', badfield),
                      ('one trailing space before newline', badtrail),
                      ('bins in [0,n), s in [0,6)', badrange),
                      ('blocks contiguous', noncontig)):
        if bad:
            fails.append('%s: %d offending lines' % (name, bad))
        else:
            print('ok   %s' % name)
    print('info data lines=%d blocks=%d' % (len(body), len(seen_keys)))
    for m in fails:
        print('FAIL %s' % m)
    print('AUDIT %s' % ('OK' if not fails else 'FAIL'))
    return 0 if not fails else 1

sys.exit(main(sys.argv[1]))
