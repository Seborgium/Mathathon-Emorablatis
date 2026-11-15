"""Independent parser for the saved-run record files (Stage A/B/C interchange format).

Format per atlas.cpp saveRecords/readRecords (saved-run/compiled-build/source/atlas.cpp:191-215):
  uint64 count                     (8 bytes, little endian on this machine)
  per record:
    int32  k                       (4 bytes)
    36 x binary64 p                (288 bytes)
    k x 36 binary64 T              (k*288 bytes)
    8 x binary64 values            C, n0, id, ort, hor, mnorm, froot, radius   (64 bytes)
Total per record: 356 + 288*k bytes.  k = 4 -> 1508 bytes.

The parser refuses trailing bytes: file_size must equal 8 + sum(356+288*k_i).
It is written from the layout, not imported from the repository's Python tools.
"""
import struct
import hashlib

REC = struct.Struct("<i36d")          # k followed by p (36 doubles)
EIGHT = struct.Struct("<8d")
U64 = struct.Struct("<Q")


def parse_records(path):
    with open(path, "rb") as f:
        blob = f.read()
    return parse_blob(blob, path)


def parse_blob(blob, name="<blob>"):
    if len(blob) < 8:
        raise ValueError(f"{name}: shorter than header")
    (count,) = U64.unpack_from(blob, 0)
    off = 8
    out = []
    for i in range(count):
        if off + 4 > len(blob):
            raise ValueError(f"{name}: truncated at record {i}")
        (k,) = struct.unpack_from("<i", blob, off)
        if k < 0 or k > 10:
            raise ValueError(f"{name}: record {i} has k={k}")
        need = off + 4 + 288 + 288 * k + 64
        if need > len(blob):
            raise ValueError(f"{name}: truncated at record {i} (k={k})")
        out.append((off, need, k))
        off = need
    if off != len(blob):
        raise ValueError(f"{name}: {len(blob)-off} trailing bytes after {count} records")
    return {"count": count, "records": out, "blob": blob, "name": name}


def record_view(parsed, i):
    """Return (k, p tuple, T list of tuples, values tuple, byte slice)."""
    off, end, k = parsed["records"][i]
    blob = parsed["blob"]
    (kk, *p) = REC.unpack_from(blob, off)
    assert kk == k
    tvals = list(struct.unpack_from("<%dd" % (k * 36), blob, off + 4 + 288)) if k else []
    T = [tuple(tvals[36 * a:36 * a + 36]) for a in range(k)]
    vals = EIGHT.unpack_from(blob, end - 64)
    return k, tuple(p), T, vals, blob[off:end]


def record_bytes(parsed, i):
    off, end, k = parsed["records"][i]
    return parsed["blob"][off:end]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def hi_lo(x):
    """High/low 32-bit words of a binary64, for exact 'same double' tests."""
    return struct.unpack("<II", struct.pack("<d", x))
