#!/usr/bin/env python3
"""check_order.py -- does the recorded centres.txt respect my seeds::build order?

Each centre line is  b0 b1 b2 b3 b4 s  y0 y1 y2 y3  (ten ints, each followed by one space).
Centres are emitted grouped by X, so the sequence of distinct (b0..b4,s) keys, in file order,
must be an ordered subsequence of my xs list (xs[t] = the t-th element of seeds::build's xs).
Exit 0 iff it is.  This tests the enumeration order (the t index) without running the cover.
"""
import sys

def read_centres(path):
    with open(path, 'rb') as f:
        header = f.readline().decode()
        if not header.endswith('\n'):
            sys.exit('bad header: no newline')
        parts = header[:-1].split(' ')
        if len(parts) != 2:
            sys.exit('bad header: %r' % header)
        n, count = int(parts[0]), int(parts[1])
        keys, ys, bad = [], [], []
        lines = 0
        for raw in f:
            lines += 1
            if not raw.endswith(b'\n'):
                bad.append(('no-final-newline', lines)); break
            body = raw[:-1]
            if not body.endswith(b' '):
                bad.append(('no-trailing-space', lines))
            f2 = body.split(b' ')
            if len(f2) != 11 or f2[-1] != b'':
                bad.append(('field-count:%d' % len(f2), lines)); continue
            try:
                v = [int(x) for x in f2[:10]]
            except ValueError:
                bad.append(('non-integer', lines)); continue
            k = tuple(v[:6])
            if not keys or keys[-1] != k:
                keys.append(k)
            ys.append(tuple(v[6:]))
    return n, count, lines, keys, ys, bad

def read_xs(path):
    xs = []
    with open(path) as f:
        for line in f:
            p = line.split()
            if len(p) == 7:
                xs.append(tuple(int(x) for x in p[:6]))
    return xs

def main():
    centres, xsdump = sys.argv[1], sys.argv[2]
    n, count, lines, keys, ys, bad = read_centres(centres)
    xs = read_xs(xsdump)
    print('header n=%d count=%d' % (n, count))
    print('data lines=%d (header says %d) %s' % (lines, count, 'OK' if lines == count else 'MISMATCH'))
    print('format problems: %d' % len(bad))
    for b in bad[:5]:
        print('  ', b)
    print('xs entries=%d' % len(xs))
    # ordered-subsequence match
    i = 0
    matched = 0
    first_bad = None
    for g, k in enumerate(keys):
        while i < len(xs) and xs[i] != k:
            i += 1
        if i == len(xs):
            first_bad = (g, k)
            break
        matched += 1
        i += 1
    print('distinct X blocks in file=%d, matched in order=%d' % (len(keys), matched))
    if first_bad:
        g, k = first_bad
        print('FIRST UNMATCHED BLOCK: group %d key %s (searched to end of xs)' % (g, k))
        print('xs exhausted after %d entries checked' % i)
    ok = (first_bad is None and not bad and lines == count and matched == len(keys))
    print('ORDER %s' % ('OK' if ok else 'FAIL'))
    return 0 if ok else 1

sys.exit(main())
