"""Exact parser for the upstream Record format (atlas.cpp saveRecords/readRecords).

Layout (little endian, no padding):
    uint64 count
    per record: int32 k ; double p[36] ; double T[k][36] ; double C,n0,id,ort,hor,mnorm,froot,radius

`Record.p` and `Record.T` are converted to exact rationals (fractions.Fraction) on
request, because every binary64 datum denotes an exact dyadic rational and the
certificate checks below are statements about those exact reals.
"""
import struct
from fractions import Fraction

MAGIC_FIELDS = ("C", "n0", "id", "ort", "hor", "mnorm", "froot", "radius")


class Record:
    __slots__ = ("k", "p", "T", "C", "n0", "id", "ort", "hor", "mnorm",
                 "froot", "radius", "index", "source")

    def __init__(self, k, p, T, scal, index, source):
        self.k = k
        self.p = p
        self.T = T
        (self.C, self.n0, self.id, self.ort, self.hor,
         self.mnorm, self.froot, self.radius) = scal
        self.index = index
        self.source = source

    # exact rational views
    def pQ(self):
        return [[Fraction(x) for x in self.p[6 * i:6 * i + 6]] for i in range(6)]

    def TQ(self):
        return [[Fraction(x) for x in row] for row in self.T]

    def scalQ(self):
        return {name: Fraction(getattr(self, name)) for name in MAGIC_FIELDS}

    def __repr__(self):
        return (f"Record({self.source}#{self.index} k={self.k} C={self.C:.6g} "
                f"mnorm={self.mnorm:.6g} froot={self.froot:.3g} id={self.id:.3g} "
                f"ort={self.ort:.3g} hor={self.hor:.3g} r={self.radius:.6g})")


def read_records(path, source=None):
    source = source or str(path)
    with open(path, "rb") as fh:
        blob = fh.read()
    if len(blob) < 8:
        raise ValueError(f"{path}: file shorter than the count header")
    (count,) = struct.unpack_from("<Q", blob, 0)
    off = 8
    out = []
    for index in range(count):
        if off + 4 > len(blob):
            raise ValueError(f"{path}: truncated at record {index}")
        (k,) = struct.unpack_from("<i", blob, off)
        off += 4
        if not (0 <= k <= 10):
            raise ValueError(f"{path}: record {index} has k={k} outside 0..10")
        need = 8 * (36 + 36 * k + 8)
        if off + need > len(blob):
            raise ValueError(f"{path}: truncated at record {index}")
        vals = struct.unpack_from("<" + "d" * (36 + 36 * k + 8), blob, off)
        off += need
        p = list(vals[:36])
        T = [list(vals[36 + 36 * a: 36 + 36 * (a + 1)]) for a in range(k)]
        scal = list(vals[36 + 36 * k:])
        out.append(Record(k, p, T, scal, index, source))
    if off != len(blob):
        raise ValueError(f"{path}: {len(blob) - off} trailing bytes")
    return out


def census(records):
    """Stratification statistics used to choose the sample."""
    import collections
    by_k = collections.Counter(r.k for r in records)
    radii = sorted(r.radius for r in records)
    n = len(radii)
    return dict(count=n, by_k=dict(sorted(by_k.items())),
                rmin=radii[0] if n else None, rmax=radii[-1] if n else None,
                rmedian=radii[n // 2] if n else None)


if __name__ == "__main__":
    import sys
    for path in sys.argv[1:]:
        recs = read_records(path)
        print(path, census(recs))
