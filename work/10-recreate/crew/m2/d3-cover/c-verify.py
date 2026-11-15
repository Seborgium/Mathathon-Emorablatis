#!/usr/bin/env python3
"""c-verify.py — comparison harness for centers.txt (team C / m2, direction d3).

  compare  REF CAND            byte-identical? else first differing byte offset and line
  prefix   REF CAND            is CAND's body the first-lines prefix of REF's body?
  invariants FILE              structural checks on a centres file
Exit status 0 on success, 1 on a real mismatch, 2 on a usage/format error.
No comparison is ever loosened: every mode demands exact agreement.
"""
import sys, hashlib

def read(path):
    with open(path, 'rb') as f:
        return f.read()

def body(b):
    i = b.find(b'\n')
    if i < 0: sys.exit(2 + 0*print("no header"))
    return b[:i], b[i+1:]

def main(argv):
    mode = argv[1] if len(argv) > 1 else ''
    if mode == 'compare':
        a, b = read(argv[2]), read(argv[3])
        ha, hb = hashlib.sha256(a).hexdigest(), hashlib.sha256(b).hexdigest()
        print(f'ref  {argv[2]}: {len(a)} bytes sha256 {ha}')
        print(f'cand {argv[3]}: {len(b)} bytes sha256 {hb}')
        if a == b:
            print('IDENTICAL')
            return 0
        n = min(len(a), len(b))
        off = next((i for i in range(n) if a[i] != b[i]), n)
        la, lb = a[:off].count(b'\n'), b[:off].count(b'\n')
        print(f'MISMATCH first differing byte offset {off} (line {la+1} of ref, {lb+1} of cand)')
        print(f'  ref  ...{a[max(0,off-40):off+40]!r}')
        print(f'  cand ...{b[max(0,off-40):off+40]!r}')
        return 1
    if mode == 'prefix':
        ha, ba = body(read(argv[2]))
        hb, bb = body(read(argv[3]))
        if ha.split()[0] != hb.split()[0]:
            print(f'HEADER n MISMATCH {ha!r} vs {hb!r}'); return 1
        print(f'note: header counts {ha.decode()} (ref) vs {hb.decode()} (prefix run)')
        if not ba.startswith(bb):
            n = min(len(ba), len(bb))
            off = next((i for i in range(n) if ba[i] != bb[i]), n)
            print(f'NOT A PREFIX: first differing body byte offset {off} '
                  f'(line {ba[:off].count(10)+1})')
            print(f'  ref  ...{ba[max(0,off-40):off+40]!r}')
            print(f'  cand ...{bb[max(0,off-40):off+40]!r}')
            return 1
        nl = bb.count(b'\n')
        print(f'PREFIX-OK: {nl} candidate lines match the first {nl} reference lines')
        return 0
    if mode == 'invariants':
        h, b = body(read(argv[2]))
        n, count = (int(x) for x in h.split())
        lines = b.split(b'\n')
        if lines[-1] != b'': print('FAIL file does not end with a newline'); return 1
        lines = lines[:-1]
        if len(lines) != count: print(f'FAIL header count {count} != {len(lines)} lines'); return 1
        for k, ln in enumerate(lines):
            if not ln.endswith(b' '):
                print(f'FAIL line {k+1} does not end with the mandatory space'); return 1
            f = ln[:-1].split(b' ')
            if len(f) != 10:
                print(f'FAIL line {k+1} has {len(f)} fields'); return 1
            v = [int(x) for x in f]
            if any(not (0 <= x < n) for x in v[:5] + v[6:]):
                print(f'FAIL line {k+1} bin out of range'); return 1
            if not (0 <= v[5] < 5):
                print(f'FAIL line {k+1} s out of range'); return 1
            if v[6] > v[7] or v[7] > v[8] or v[8] > v[9]:
                print(f'FAIL line {k+1} y not non-decreasing: {v[6:]}'); return 1
            if v[5] != min(range(5), key=lambda j: abs(2*v[j]+1-n)):
                print(f'FAIL line {k+1} s is not the first argmin of |2b+1-n|'); return 1
            if v[0] > v[1] or v[1] > v[2] or v[2] > v[3] or v[3] > v[4]:
                print(f'FAIL line {k+1} b not non-decreasing: {v[:5]}'); return 1
        ts = [v for v in lines]
        print(f'INVARIANTS-OK: header {n} {count}, {len(lines)} lines, '
              f'{len(b)} body bytes, all fields in range, b and y non-decreasing, s = first argmin')
        return 0
    print(__doc__); return 2

if __name__ == '__main__':
    sys.exit(main(sys.argv))
