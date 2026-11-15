"""Reader for the saved Stage-A/atlas record files, exactly as atlas.cpp readRecords.

Layout (little-endian, native-sized):
  uint64 count
  per record: int32 k; double p[36]; double T[k][36]; double [C,n0,id,ort,hor,mnorm,froot,radius]
Confirmed against .scratch/h0/dl/verification/saved-run/compiled-build/source/atlas.cpp:191-217.
"""
import struct

DATA = ("/workspace/nucleus/work/projects/p-20d35e783d5d4092acb8bd94b19cf30b/repo/"
        ".scratch/h0/dl/verification/saved-run/execution/data/")

FIELDS = ("C", "n0", "id", "ort", "hor", "mnorm", "froot", "radius")


class Root:
    __slots__ = ("k", "p", "T", "C", "n0", "id", "ort", "hor", "mnorm", "froot", "radius")

    def __init__(self, k, p, T, vals):
        self.k = k
        self.p = p
        self.T = T
        self.C, self.n0, self.id, self.ort, self.hor, self.mnorm, self.froot, self.radius = vals

    def __repr__(self):
        return ("Root(k=%d, C=%.6g, n0=%.3g, id=%.3g, ort=%.3g, hor=%.3g, mnorm=%.4g, "
                "froot=%.3g, radius=%.6g)" % (self.k, self.C, self.n0, self.id, self.ort,
                                              self.hor, self.mnorm, self.froot, self.radius))


def read(path):
    with open(path, "rb") as f:
        blob = f.read()
    off = 0
    (count,) = struct.unpack_from("<Q", blob, off)
    off += 8
    out = []
    for _ in range(count):
        (k,) = struct.unpack_from("<i", blob, off)
        off += 4
        p = struct.unpack_from("<36d", blob, off)
        off += 36 * 8
        T = []
        for _a in range(k):
            T.append(struct.unpack_from("<36d", blob, off))
            off += 36 * 8
        vals = struct.unpack_from("<8d", blob, off)
        off += 8 * 8
        out.append(Root(k, list(p), [list(r) for r in T], list(vals)))
    if off != len(blob):
        raise ValueError("trailing bytes: %d of %d" % (len(blob) - off, len(blob)))
    return out


if __name__ == "__main__":
    import sys
    for name in sys.argv[1:]:
        v = read(name if "/" in name else DATA + name)
        print(name, len(v), "records; first:", v[0])
