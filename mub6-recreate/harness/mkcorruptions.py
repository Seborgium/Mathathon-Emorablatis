#!/usr/bin/env python3
"""Build the seeded-corruption suite for the saved-run record set.

Usage: python3 mkcorruptions.py <pristine-execution-dir> <sandbox-root>

Each case is a hardlink copy of the pristine directory (so 25 cases cost no
disk) in which exactly one file is replaced by a modified copy.  The pristine
directory is never written: every mutation reads, edits in memory, unlinks and
re-creates the file.  `manifest.json` in <sandbox-root> lists the cases with the
check id that is expected to fire, and the sha256 of every pristine file before
and after the run (the two must agree).
"""
import hashlib
import json
import os
import shutil
import struct
import sys

SLOTS = ["C", "n0", "id", "ort", "hor", "mnorm", "froot", "radius"]
HEAD = 8


def walk_sizes(data):
    """(count, [(file_offset, k, record_size)]) for one record file."""
    n = struct.unpack_from("<Q", data, 0)[0]
    off = HEAD
    out = []
    for _ in range(n):
        (k,) = struct.unpack_from("<i", data, off)
        size = 4 + 288 + 288 * k + 64
        out.append((off, k, size))
        off += size
    return n, out


def read(rel, root):
    with open(os.path.join(root, "data", rel), "rb") as f:
        return f.read()


def rewrite(rel, data, root):
    full = os.path.join(root, "data", rel)
    if os.path.exists(full):
        os.remove(full)          # break the hardlink before writing
    with open(full, "wb") as f:
        f.write(data)


def slot_off(off, k, slot_index):
    return off + 4 + 288 + 288 * k + 8 * slot_index


def patch_slot(root, rel, idx, slot, value):
    data = bytearray(read(rel, root))
    n, recs = walk_sizes(bytes(data))
    off, k, _size = recs[idx]
    struct.pack_into("<d", data, slot_off(off, k, SLOTS.index(slot)), value)
    rewrite(rel, bytes(data), root)
    return "%s record %d %s := %r" % (rel, idx, slot, value)


def patch_p(root, rel, idx, h, value):
    data = bytearray(read(rel, root))
    n, recs = walk_sizes(bytes(data))
    off, k, _size = recs[idx]
    struct.pack_into("<d", data, off + 4 + 8 * h, value)
    rewrite(rel, bytes(data), root)
    return "%s record %d p[%d] := %r" % (rel, idx, h, value)


def nudge_p(root, rel, idx, h, delta):
    data = bytearray(read(rel, root))
    n, recs = walk_sizes(bytes(data))
    off, k, _size = recs[idx]
    pos = off + 4 + 8 * h
    old = struct.unpack_from("<d", data, pos)[0]
    struct.pack_into("<d", data, pos, old + delta)
    rewrite(rel, bytes(data), root)
    return "%s record %d p[%d] %r -> %r (inside the |p|<=4 bound)" % (rel, idx, h, old, old + delta)


def patch_T(root, rel, idx, a, h, value):
    data = bytearray(read(rel, root))
    n, recs = walk_sizes(bytes(data))
    off, k, _size = recs[idx]
    struct.pack_into("<d", data, off + 4 + 288 + 288 * a + 8 * h, value)
    rewrite(rel, bytes(data), root)
    return "%s record %d T[%d][%d] := %r" % (rel, idx, a, h, value)


def set_count(root, rel, delta):
    data = bytearray(read(rel, root))
    n = struct.unpack_from("<Q", data, 0)[0]
    struct.pack_into("<Q", data, 0, n + delta)
    rewrite(rel, bytes(data), root)
    return "%s count %d -> %d" % (rel, n, n + delta)


def set_k(root, rel, idx, k):
    data = bytearray(read(rel, root))
    n, recs = walk_sizes(bytes(data))
    off, k0, _size = recs[idx]
    struct.pack_into("<i", data, off, k)
    rewrite(rel, bytes(data), root)
    return "%s record %d k %d -> %d (record bytes unchanged)" % (rel, idx, k0, k)


def truncate(root, rel, nbytes):
    data = read(rel, root)
    rewrite(rel, data[:-nbytes], root)
    return "%s truncated by %d bytes (%d -> %d)" % (rel, nbytes, len(data), len(data) - nbytes)


def append(root, rel, blob):
    data = read(rel, root)
    rewrite(rel, data + blob, root)
    return "%s: %d byte(s) appended (%d -> %d)" % (rel, len(blob), len(data), len(data) + len(blob))


def drop_last_record(root, rel):
    data = bytearray(read(rel, root))
    n, recs = walk_sizes(bytes(data))
    off, k, size = recs[-1]
    del data[off:off + size]
    struct.pack_into("<Q", data, 0, n - 1)
    rewrite(rel, bytes(data), root)
    return "%s: last record dropped and count set to %d (self-consistent file)" % (rel, n - 1)


def duplicate_record(root, rel, idx):
    data = bytearray(read(rel, root))
    n, recs = walk_sizes(bytes(data))
    off, k, size = recs[idx]
    data.extend(data[off:off + size])
    struct.pack_into("<Q", data, 0, n + 1)
    rewrite(rel, bytes(data), root)
    return "%s: record %d appended, count %d -> %d" % (rel, idx, n, n + 1)


def swap_records(root, rel, i, j):
    data = read(rel, root)
    n, recs = walk_sizes(data)
    a, b = recs[i], recs[j]
    ra, rb = data[a[0]:a[0] + a[2]], data[b[0]:b[0] + b[2]]
    if len(ra) != len(rb):
        raise SystemExit("records %d and %d differ in size" % (i, j))
    out = bytearray(data)
    out[a[0]:a[0] + a[2]] = rb
    out[b[0]:b[0] + b[2]] = ra
    rewrite(rel, bytes(out), root)
    return "%s: records %d and %d exchanged (same bytes, different order)" % (rel, i, j)


def edit_text(root, rel, old, new, where="data"):
    full = os.path.join(root, where, rel)
    with open(full, "r") as f:
        txt = f.read()
    if old not in txt:
        raise SystemExit("%s: pattern %r not found" % (rel, old))
    os.remove(full)
    with open(full, "w") as f:
        f.write(txt.replace(old, new, 1))
    return "%s: %r -> %r" % (rel, old, new)


def edit_argv(root, key, mutate):
    full = os.path.join(root, "commands.json")
    with open(full) as f:
        doc = json.load(f)
    before = list(doc["children"][key]["argv"])
    mutate(doc["children"][key])
    after = list(doc["children"][key]["argv"])
    os.remove(full)
    with open(full, "w") as f:
        json.dump(doc, f, indent=1)
    return "commands.json %s argv %r -> %r" % (key, before, after)


def drop_file(root, rel):
    full = os.path.join(root, "data", rel)
    os.remove(full)
    return "%s deleted" % rel


# case id, mutation callable, the check id(s) at least one of which must fire
# ([] = predicted undetectable, i.e. expected to be ACCEPTED by both checkers), description
CASES = [
    # --- record stream integrity (tier A: the frozen format)
    ("count_too_large", lambda r: set_count(r, "batches/f10.bin", +1), ["recordfiles.parse"],
     "count field one too large: a record is read past end of file"),
    ("count_too_small", lambda r: set_count(r, "batches/f10.bin", -1), ["recordfiles.parse"],
     "count field one too small: one record's bytes are left trailing"),
    ("k_bounds_high", lambda r: set_k(r, "batches/f0.bin", 0, 11), ["recordfiles.parse"],
     "record k = 11, above maxK"),
    ("k_bounds_negative", lambda r: set_k(r, "batches/f0.bin", 0, -1), ["recordfiles.parse"],
     "record k = -1, below 0"),
    ("k_shrink_unresized", lambda r: set_k(r, "batches/f0.bin", 0, 0), ["recordfiles.parse"],
     "record k 4 -> 0 without shrinking the record: the stream loses alignment"),
    ("truncate_mid_record", lambda r: truncate(r, "batches/f52.bin", 4), ["recordfiles.parse"],
     "last 4 bytes of a batch removed"),
    ("truncate_at_boundary", lambda r: drop_last_record(r, "batches/f0.bin"),
     ["B.batches[partition]", "B.batches[size]"],
     "last record of a batch dropped and count decremented: parses, but is no longer the first "
     "piece of the fine.bin partition"),
    ("append_one_byte", lambda r: append(r, "batches/bad3.bin", b"\x00"), ["recordfiles.parse"],
     "one byte appended to an unresolved-record file"),
    # --- value tampering inside one record
    ("swap_two_tails", lambda r: swap_slots(r, "batches/f0.bin", 3, "id", "ort"),
     ["B.rec[batch0].constants", "B.batches[partition]"],
     "id and ort exchanged in one record: both stay inside the format's bounds"),
    ("wrong_radius_batch", lambda r: patch_slot(r, "batches/f0.bin", 5, "radius", 0.0159),
     ["B.rec[batch0].radius_is_target", "B.batches[partition]"],
     "batch radius 0.016 -> 0.0159; brun emit() forces every batch radius to the target"),
    ("wrong_radius_fine", lambda r: patch_slot(r, "fine.bin", 100, "radius", 0.02),
     ["B.rec[Bfine].bounds", "B.batches[partition]"], "fine.bin radius set above the .016 target"),
    ("radius_above_global", lambda r: patch_slot(r, "mid.bin", 0, "radius", 0.13),
     ["B.rec[Bmid].bounds"], "radius 0.13, above the .126 cap of validate"),
    ("C_out_of_range", lambda r: patch_slot(r, "batches/f0.bin", 1, "C", 20.5),
     ["B.rec[batch0].bounds", "B.batches[partition]"], "C = 20.5, the format requires C < 20"),
    ("nan_in_p", lambda r: patch_p(r, "batches/f0.bin", 2, 7, float("nan")),
     ["B.rec[batch0].finite", "B.rec[batch0].bounds", "B.batches[partition]"],
     "one p entry replaced by NaN"),
    ("p_above_four", lambda r: patch_p(r, "batches/f0.bin", 3, 0, 4.5),
     ["B.rec[batch0].bounds", "B.batches[partition]"], "|p| = 4.5, above the 4 cap"),
    ("T_above_1_01", lambda r: patch_T(r, "batches/f0.bin", 0, 0, 5, 1.02),
     ["B.rec[batch0].bounds", "B.batches[partition]"], "|T| = 1.02, above the 1.01 cap"),
    # --- cross-artefact structure (tier B: the recorded run schedule)
    ("batch_count_wrong", lambda r: edit_text(r, "batches/fdone.txt", "88 22379", "87 22379"),
     ["B.batches[emitted]", "files.declared", "B.batches[partition]"],
     "done.txt claims 87 batches while 88 exist"),
    ("non_partition_duplicate", lambda r: duplicate_record(r, "batches/f10.bin", 0),
     ["B.batches[size]", "B.batches[partition]", "C.index[C.batch10]"],
     "a record duplicated in a batch: 257 records, so the partition is broken"),
    ("non_partition_order", lambda r: swap_records(r, "batches/f10.bin", 0, 1),
     ["B.batches[partition]"], "two records of a batch exchanged"),
    ("missing_fallback_input", lambda r: edit_argv(
        r, "C.Bfallback", lambda c: c["argv"].remove("batches/bad53.bin")
        or c["inputs"].__setitem__(slice(None), c["argv"][6:])),
     ["C.fallback_inputs"], "a non-empty C failure file is not fed to the fallback"),
    ("unordered_fallback_input", lambda r: edit_argv(
        r, "C.Bfallback", lambda c: swap_argv(c, "batches/bad3.bin", "batches/bad4.bin")),
     ["C.fallback_inputs"], "fallback inputs in the wrong order (bad4 before bad3)"),
    ("returncode_wrong", lambda r: edit_rc(r, "C.batch0", 1), ["C.bad[C.batch0]"],
     "return code 0 -> 1 for a batch with no unresolved record"),
    ("a_shard_missing", lambda r: edit_argv(r, "A3", lambda c: c["argv"].__setitem__(2, "2")),
     ["A.partition"], "A part 3 relabelled part 2: shard 3 is never produced"),
    ("final_bad_absent", lambda r: drop_file(r, "fb1cbad2.bin"),
     ["files.declared", "C.final_bad[C.final2]", "C.final_bytes[C.final2]"],
     "one of the four final bad files deleted"),
    ("results_counter_wrong", lambda r: edit_text(
        r, "C.batch10.txt", "result done256 bad1", "result done255 bad1", where="results"),
     ["C.index[C.batch10]"], "the recorded stdout counter disagrees with the batch size"),
    # --- predicted-undetectable: in-bounds tampering of a parent record that no other
    #     artefact of the run is compared against (only re-running the stage can see it)
    ("silent_coarse_p", lambda r: nudge_p(r, "coarse0.bin", 0, 0, +0.001), [],
     "coarse0.bin p[0] += 0.001 (|p| <= 4): the A shards are only counted downstream"),
    ("silent_mid_p", lambda r: nudge_p(r, "mid.bin", 0, 7, +0.001), [],
     "mid.bin p[7] += 0.001: mid is the parent of fine.bin, whose records are recomputed, "
     "not copied"),
    ("silent_fb1_p", lambda r: nudge_p(r, "fb1.bin", 0, 3, +0.001), [],
     "fb1.bin p[3] += 0.001: the four final C runs leave empty files, so nothing compares fb1"),
]


def swap_slots(root, rel, idx, s1, s2):
    data = bytearray(read(rel, root))
    n, recs = walk_sizes(bytes(data))
    off, k, _size = recs[idx]
    o1, o2 = slot_off(off, k, SLOTS.index(s1)), slot_off(off, k, SLOTS.index(s2))
    v1 = struct.unpack_from("<d", data, o1)[0]
    v2 = struct.unpack_from("<d", data, o2)[0]
    struct.pack_into("<d", data, o1, v2)
    struct.pack_into("<d", data, o2, v1)
    rewrite(rel, bytes(data), root)
    return "%s record %d: %s (%r) <-> %s (%r)" % (rel, idx, s1, v1, s2, v2)


def swap_argv(c, a, b):
    av = c["argv"]
    i, j = av.index(a), av.index(b)
    av[i], av[j] = av[j], av[i]
    c["inputs"][:] = av[6:]


def edit_rc(root, key, value):
    full = os.path.join(root, "commands.json")
    with open(full) as f:
        doc = json.load(f)
    old = doc["children"][key]["returncode"]
    doc["children"][key]["returncode"] = value
    os.remove(full)
    with open(full, "w") as f:
        json.dump(doc, f, indent=1)
    return "commands.json %s returncode %r -> %r" % (key, old, value)


def digest(root):
    out = {}
    for dirpath, _dn, fns in os.walk(root):
        for fn in fns:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            h = hashlib.sha256()
            with open(full, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
            out[rel] = h.hexdigest()
    return out


def main(argv):
    pristine, sandbox = argv[0], argv[1]
    before = digest(pristine)
    os.makedirs(sandbox, exist_ok=True)
    manifest = {"pristine": os.path.abspath(pristine), "cases": []}
    for cid, fn, expect, desc in CASES:
        case = os.path.join(sandbox, cid)
        if os.path.isdir(case):
            shutil.rmtree(case)
        # hardlink copy: instant, and each mutation replaces the one file it touches
        shutil.copytree(pristine, case, copy_function=os.link)
        detail = fn(case)
        manifest["cases"].append({"id": cid, "description": desc, "mutation": detail,
                                  "expect_check": expect, "expect_miss": not expect,
                                  "dir": os.path.abspath(case)})
        print("%-24s %s" % (cid, detail))
    after = digest(pristine)
    if before != after:
        changed = [k for k in before if before.get(k) != after.get(k)]
        raise SystemExit("the pristine directory was modified: %r" % changed)
    manifest["pristine_files"] = len(before)
    manifest["pristine_sampled_sha256"] = {k: before[k] for k in
                                           sorted(before)[:3] + ["data/centers.txt"]
                                           if k in before}
    with open(os.path.join(sandbox, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    print("\n%d cases written to %s; pristine unchanged (%d files)"
          % (len(manifest["cases"]), sandbox, len(before)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
