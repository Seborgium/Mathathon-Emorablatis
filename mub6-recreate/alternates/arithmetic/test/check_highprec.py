#!/usr/bin/env python3
"""High-precision checks of the arithmetic core, independent of any C++ code.

Reads a dump produced by test/mine_dump.cpp or test/oracle_probe.cpp
(test/dump_common.h format) and checks it against

  T7  the seed count recorded in the published run's stdout (xs22829),
  T8  cos/sin(2 pi (i+1/2)/112) evaluated at 60 decimal digits with mpmath,
  T9  the recorded covering file .scratch/gh/data/centers.txt: every centre's
      (b[0..4], s) must be one of the 22829 seeds of the dump.

Nothing here takes an expected value from our own code.  Exit status 0 iff all
checks pass.
"""
import hashlib
import sys
from fractions import Fraction

import mpmath as mp

mp.mp.dps = 60
PI = mp.pi
CENTERS_SHA = "c48bc9a2be1eb2cdeea82ea1b030d7cb9f00a6c9563b63f0248dd115748a5789"
CENTERS_BYTES = 7339546

fails = []


def ck(cond, what):
    print("%-66s %s" % (what, "PASS" if cond else "FAIL"))
    if not cond:
        fails.append(what)


def parse(path):
    d = {"tab": [], "xs": [], "ys": {}}
    with open(path) as f:
        assert f.readline().strip() == "format 1"
        for _ in range(3):
            k, v = f.readline().split()
            d[k] = v
        n = int(d["n"])
        line = f.readline()
        assert line.startswith("xs "), line
        d["xs_count"] = int(line.split()[1])
        assert f.readline().strip() == "tab"
        for _ in range(n):
            i, a, b = f.readline().split()
            d["tab"].append((int(i), float.fromhex(a), float.fromhex(b)))
        assert f.readline().strip() == "xs"
        for _ in range(d["xs_count"]):
            v = f.readline().split()
            d["xs"].append((tuple(int(x) for x in v[:5]), int(v[5]),
                            float.fromhex(v[6]), float.fromhex(v[7]), float.fromhex(v[8])))
        assert f.readline().strip() == "ys"
        for _ in range(n):
            a, cnt = f.readline().split()[1:]
            a, cnt = int(a), int(cnt)
            rows = []
            for _ in range(cnt):
                v = f.readline().split()
                rows.append((tuple(int(x) for x in v[:5]), int(v[5]),
                             float.fromhex(v[6]), float.fromhex(v[7]), float.fromhex(v[8])))
            d["ys"][a] = rows
    return d


UNIT = 2.0 ** -53


def ulps(got, want):
    """Signed difference in units of 2^-53 (the spacing of doubles below 1).

    A relative measure is wrong here: cos and sin are O(1) but pass through 0,
    and near a zero of the function the double spacing shrinks without the
    absolute error doing so."""
    return (got - want) / UNIT


def main():
    dump = sys.argv[1] if len(sys.argv) > 1 else "out/mine.dump"
    centers = sys.argv[2] if len(sys.argv) > 2 else "../../../.scratch/gh/data/centers.txt"

    print("dump: %s  sha256 %s" % (dump, hashlib.sha256(open(dump, "rb").read()).hexdigest()))
    d = parse(dump)
    n = int(d["n"])

    # ---- T7: the recorded seed count.
    # The published run's stdout, cached at .scratch/gh/covrun.log (6 lines).
    logpath = "../../../.scratch/gh/covrun.log"
    head = open(logpath, "r", errors="replace").read(400)
    recorded = int(head[2:].split()[0]) if head.startswith("xs") else None
    print("recorded stdout (%s) starts: %r"
          % (logpath, head[:48].replace("\n", "|")))
    ck(d["xs_count"] == 22829, "T7 xs count == 22829 (published stdout)")
    ck(recorded == 22829, "T7 the cached published stdout says xs22829")
    ck(n == 112, "T7 n == 112")
    ck(float.fromhex(d["w"]) == 1.0 / 112, "T7 w == 1/112 exactly")
    ck(float.fromhex(d["pi"]) == float(PI), "T7 pi == the correctly rounded binary64 pi")

    # ---- T8: the 112 table entries against 60-digit cos/sin.
    worst, worst_i, exact = 0.0, -1, 0
    for i, a, b in d["tab"]:
        th = 2 * PI * (mp.mpf(i) + mp.mpf(1) / 2) / 112
        ca, cb = mp.cos(th), mp.sin(th)
        ea, eb = ulps(a, float(ca)), ulps(b, float(cb))
        if a == float(ca) and b == float(cb):
            exact += 1
        e = max(abs(ea), abs(eb))
        if e > worst:
            worst, worst_i = e, i
    print("     tab: %d/112 entries are the correctly rounded double of cos/sin;"
          " worst %.2f x 2^-53 at i=%d" % (exact, worst, worst_i))
    ck(worst <= 8.0, "T8 every tab entry is within 8 x 2^-53 of the 60-digit value")

    # ---- T9: the recorded covering file knows only seeds we also produced.
    data = open(centers, "rb").read()
    ck(len(data) == CENTERS_BYTES, "T9 centers.txt is %d bytes" % CENTERS_BYTES)
    ck(hashlib.sha256(data).hexdigest() == CENTERS_SHA, "T9 centers.txt sha256 matches the record")
    lines = data.decode("ascii").split("\n")
    hdr = lines[0]
    ck(hdr == "112 249878", "T9 header is '112 249878'")
    body = [l for l in lines[1:] if l]
    ck(len(body) == 249878, "T9 249878 centre lines")
    ck(all(l.endswith(" ") for l in body), "T9 every line ends with one space before the newline")
    have = set((b, s) for b, s, *_ in d["xs"])
    used = set()
    missing = 0
    for l in body:
        v = [int(x) for x in l.split()]
        key = (tuple(v[0:5]), v[5])
        used.add(key)
        if key not in have:
            missing += 1
    print("     centres reference %d distinct (b,s) pairs; %d not among the dump's seeds"
          % (len(used), missing))
    ck(missing == 0, "T9 every centre's (b[0..4],s) is a seed of the dump")
    ck(used <= have, "T9 the centres use no seed the dump lacks")

    # ---- T10: how far the published association is from the exact real product.
    w = Fraction(1, 112)
    exact_err = PI * mp.mpf(w.numerator) ** 2 / (mp.mpf(w.denominator) ** 2) / 4 * 5
    got = float.fromhex("0x1.4843ae1860576p-12")
    print("     seed err = pi*(w*w/4)*5 = %.20e ; exact real value = %s ; delta = %.2f x 2^-53"
          % (got, mp.nstr(exact_err, 21), ulps(got, float(exact_err))))
    ck(abs(ulps(got, float(exact_err))) <= 1.0,
       "T10 the seed err constant is within 1 x 2^-53 of pi*w^2*5/4")

    print()
    if fails:
        print("FAILED: %d check(s)" % len(fails))
        return 1
    print("ALL PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
