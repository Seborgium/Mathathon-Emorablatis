"""Emit the Stage-C coverage manifest: the 163 unresolved records and the 1127 fallback
records, each with its provenance in the archived streams.

Provenance rule (verified byte-exactly by coverage_audit.py T2/T3):
  fine.bin record i  <->  batches/f{i//256}.bin record i%256   (byte-identical except the
  final radius double, which the batch writer overwrites with the pass target 0.016)
  byte offset of record i in fine.bin = 8 + 1508*i   (all 22378 records before the last have
  k=4; the last record, index 22378, has k=0 and 356 bytes)
  fb1.bin record j   <->  the fallback stream; its producing command is C.Bfallback with the
  15 non-empty bad files as input (updated in place? no: written afresh)
The fallback's per-parent covering map is NOT in the archive and is not inferred here.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recparse as R

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = "/workspace/nucleus/work/projects/p-20d35e783d5d4092acb8bd94b19cf30b/repo"
EXEC = os.path.join(ROOT, ".scratch/h0/dl/verification/saved-run/execution")
DATA = os.path.join(EXEC, "data")
BATCH = os.path.join(DATA, "batches")
PROBE = os.path.join(ROOT, "certdata/runs/h0-stagec-probe.json")
OUT = os.path.join(HERE, "coverage-manifest.json")


def main():
    probe = json.load(open(PROBE))
    caps = {}
    for r in probe["records"]:
        if r["category"] == "cap":
            caps.setdefault(r["command"], []).append(r["index"])
    fine = R.parse_records(os.path.join(DATA, "fine.bin"))
    fb1 = R.parse_records(os.path.join(DATA, "fb1.bin"))

    unresolved = []
    for i in range(88):
        for local in sorted(caps.get("batch%d" % i, [])):
            gi = 256 * i + (local - 1)
            body = R.record_bytes(fine, gi)
            unresolved.append({"batch": i, "batch_index": local - 1, "fine_index": gi,
                               "fine_byte_offset": 8 + 1508 * gi,
                               "record_bytes": len(body),
                               "sha256": hashlib.sha256(body).hexdigest()})
    per_batch = {}
    for u in unresolved:
        per_batch[str(u["batch"])] = per_batch.get(str(u["batch"]), 0) + 1
    fallback = []
    for j in range(fb1["count"]):
        k, pv, T, v, b = R.record_view(fb1, j)
        fallback.append({"fb1_index": j, "byte_offset": 8 + 1508 * j,
                         "k": k, "radius": v[7],
                         "sha256": hashlib.sha256(b).hexdigest()})
    out = {
        "streams": {
            "fine": {"path": "data/fine.bin", "records": fine["count"],
                     "bytes": os.path.getsize(os.path.join(DATA, "fine.bin")),
                     "sha256": R.sha(fine["blob"])},
            "fb1": {"path": "data/fb1.bin", "records": fb1["count"],
                    "bytes": os.path.getsize(os.path.join(DATA, "fb1.bin")),
                    "sha256": R.sha(fb1["blob"])},
        },
        "unresolved": {"count": len(unresolved), "per_batch": per_batch,
                       "records": unresolved},
        "fallback": {"count": len(fallback), "records": fallback},
        "caveats": [
            "the replay census records a per-command positional index, not a global one; the",
            "mapping above is the source rule (offset+i)%parts==part with parts=1 for the",
            "initial pass, verified against the bad-file bytes (T3) and the signature-",
            "distinctness of fine.bin (T9).",
            "the fallback parent->child covering map is absent from the archive; see",
            "H0-stageC-coverage.md section 5 and pcov-summary.json.",
        ],
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print("unresolved", len(unresolved), "per_batch", per_batch)
    print("fallback", len(fallback))
    print("fine sha256", out["streams"]["fine"]["sha256"])
    print("fb1  sha256", out["streams"]["fb1"]["sha256"])


if __name__ == "__main__":
    main()
