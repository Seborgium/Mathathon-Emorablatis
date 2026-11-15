# Evidence audit and composition repair — lead review

Scope: the emitted formats, actual hashes and bounded witnesses. This is not a
person-approved gate or a proof of `N(6)=3`.

## Reproduced results

From the repository root:

```sh
cd .ultramath/smwh5efk8/m4 && python3 audit/run_audit.py --out results-verified
python3 .ultramath/smwgx104w/m4/src/mutations.py \
  .ultramath/smwgx104w/m4/runs/demo/stagec-initial-0000.scv \
  .scratch/schema-mutations-verified.out
python3 work/02-checker/src/make_composition_fixed.py \
  .ultramath/smwgx104w/m2 .scratch/composition-rebuild \
  certdata/runs/h1-coverage/coverage-manifest.json
```

- The lead-corrected audit returns **55 claims: 42 CERTIFIED, 4 CONTRADICTED,
  9 UNSUPPORTED; all 26 controls pass**, with no baseline mismatch.
  [`matrix.json`](matrix.json) and its Markdown rendering are generated, not
  hand-counted. The m4 auditor's own report was **not accepted** as submitted:
  its first-solution search had not established uniqueness.
- The independent graph check gives **eight** valid permutations, not one.
  Three interchangeable pairs cause the ambiguity. Every one of the eight maps
  preserves both O and U on all 44,732 ordered record pairs (357,856 total
  checks). One explicit map has SHA-256
  `6571b3aed4dd610259549471a41f33c337e089fd59b679a0de80e0d6b321949c`.
  This is valid graph-equivalence evidence, not uniqueness or soundness of the
  geometric predicates. `work/02-checker/spec/cert-format-stageC.md` §8 now says
  big-endian decoding plus a non-unique permutation, not byte identity.
- The composition map has SHA-256
  `83516ece860722cad3307181b91a22ac26bbf3cc65630ccef807c15467bc0150`;
  its actual `fine_index` fields agree with the byte-derived capped-record map.
  Its `batch_index` remains the ordinal inside a bad file.
- The repaired composition block hashes to
  `fd61d25749c9ba55cd3082af7023b1b52b09c4715b64fdc2dbcac54616e0f819` and
  rebuilds byte-for-byte. All 163 parents match the independently recovered
  capped set. It contains 1,127 children and 11,838 incidences, including 10,711
  inherited, with 515,236 relation marks + 7 snap-closed cells = 515,243.
  `composition-v1.patch.json` now explicitly records the original emission
  (699bbc40…), the repaired emission, the builder and the preserved fields.
- The current composition has `pass_id`, `n_parents`, `n_children`, `n_links`
  at offsets 12, 16, 20, 24 in its 28-byte header. There is no reserved word
  following the counts. Its reserved words in parent entries are now also
  checked explicitly.
- The independent schema suite passes **47/47** mutations; the canonical
  composition round-trip and internal checks have zero errors.

## What the four CONTRADICTED rows mean

`comp.spec_layout_old`, `rec.g0_bytes` and `comp.prod_identity` retain
historical false byte/layout claims. The repaired current objects are not
thereby corrupt. `cap.delta_naive` uses raised minus today, while
`cap.delta_defn` additionally subtracts composition; their values are not
interchangeable. The cap-payload quantity remains raised − today − composition
= 14,056,421 B, not the naive 13,999,317 B.

## Still unresolved

`comp.percell` remains `UNSUPPORTED / COUNTER_ONLY`; global geometric coverage
does not follow from identifiers and counters. `cap.capped_covered` is now
unsupported for that reason, not because parent addressing is broken. The
source-stage threshold transcription, Root matrices/tensors, and exact graph
predicates are not re-checked by this summary audit. The seed semantic row is
out of scope for this particular auditor even though the separate 5.7 GiB
stream and its MPFR check exist; that is a division-of-labour fact, not absence
of the stream.

The underlying member submission d5 was rejected for the false uniqueness
claim. The useful corrected executable code remains an explicitly lead-corrected
artefact, not an accidentally accepted report or a full certificate.
