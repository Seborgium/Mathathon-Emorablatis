# Stage-C composition: identifier and layout repair (lead action)

## Problem -> repair

`composition-v1.bin` previously matched only 14/163 intended parents. The remaining 149 addresses
resolved to non-capped records. The root cause was **index-space confusion**: `PCOV` iterates capped
records inside each `bad{batch}.bin`, so a parent entry's `(batch, batch_index)` in the recovered
map is a local ordinal in the *bad file*, not the capped record's position in the full batch.

Using either `256*batch + batch_index` or the recycled label `fine_index` as the actual global index
was wrong. The repaired builder reads `certdata/runs/h1-coverage/coverage-manifest.json`, whose
`batch_index` is the original capped position, composes `(batch, bad-local ordinal)`, and imports
the actual capped `fine_index`. It does not reinterpret the recovered counter map's `fine_index`
label as a self-authenticating global position.

The replacement binary contains **the same parent counters, the same 1,127 child entries and the
same 11,838 ordered incidences** as before, with all 163 actual capped identifiers and:
- 515,236 relation marks + 7 snap-closed cells = 515,243 inside cells;
- 10,711 inherited incidences; zero missing and zero wrong parent addresses;
- zero duplicates; internal counter/degree invariants and round-trip checks passing.

Builder: `work/02-checker/src/make_composition_fixed.py`. Reproduce from repository root:

```sh
python3 work/02-checker/src/make_composition_fixed.py \
  .ultramath/smwgx104w/m2 .scratch/composition-fixed \
  certdata/runs/h1-coverage/coverage-manifest.json
```

## Independently checked

The resulting block was regenerated and compared against the capped manifest: 163/163 correct
parent addresses, no counter multiset changes, and identical ordered links. `audit/checks.py`'s
byte-derived independent capped-set reader now accepts the address row as well.
Replacement SHA-256: `fd61d25749c9ba55cd3082af7023b1b52b09c4715b64fdc2dbcac54616e0f819`.
The preceding misaddressed object is retained outside the proof path for audit at
`.scratch/composition-v1-bad-parent-addresses.bin`.

## Format correction

The 28-byte header is now: magic (8), version major/minor (2+2), parent `pass_id` (4),
`n_parents` (4), `n_children` (4), `n_links` (4). **There is no reserved header word.** The prior
written order had `n_parents/n_children/n_links/reserved`, contradicting the emitted layout and
causing an alternative parser to infer only 5,188 bytes. Parent entries are 32 B and retain the
previous counter fields. Parent `global` is a position in the parent pass's input stream, never an
ordinal in a bad file.

`work/02-checker/spec/cert-format-stageC.md` and the layout comment in
`work/02-checker/src/stagec_composition.py` now agree with the produced bytes.

## Remaining boundary

This repairs an **identifier format**, not the geometric cover. The block by itself does not contain
per-cell witness data; the 515,243 inside cells remain obligations (515,236 relation-marked plus 7
snap-closed). The 321,004,555 upstream cells remain obligations too; their count is arithmetic and
record-derived, not completed per-cell certification.

The Root `slack[mnorm]` and `mnorm_rel` discrepancy is a different, notation-only issue: the former
is a one-sided norm verification slack and the latter compares an approximate norm expression. The
stored constant agrees with the independent factor reconstruction to about `2e-17` on the sampled
case. It must not be presented as a counterexample to the Root norm criteria.

The separate `g0.txt` comparison also needs the proper serialization/index-order treatment. Its
byte discrepancy after ball canonicalisation is not, by itself, evidence about graph soundness.

## Lead verification after map repair

The current cover map's `fine_index` is now the independently verified original
batch/fine offset, with `batch_index` retained as the local bad-file ordinal.
Its SHA-256 is `83516ece860722cad3307181b91a22ac26bbf3cc65630ccef807c15467bc0150`.
`comp.patch_recorded` and `comp.covermap_indices` pass.

The independent `g0` comparison has eight relation-preserving ball permutations,
from three interchangeable pairs, **not a unique permutation**. Decoding big-endian
and carrying a chosen map verifies both graphs on all ordered pairs. This is
encoding/isomorphism evidence, not predicate soundness. The old first-solution
search was insufficient and its uniqueness claim was rejected.

See `results/evidence-audit-review.md` and generated `results/matrix.json`.
The format remains v1-draft; no geometric cover is inferred from this metadata.
