# H0 / Stage C: schema v1-draft — reconciling the two accepted certificate formats

Direction d1 (member m4), swarm `smwgx104w`, extending Q4 / Stage C after `smwguhf32`.
Status: **H0 draft format, not frozen.** Everything below is either a citation to a line of the
upstream source, a recomputation from `certdata/`, or a measurement made here; the two places
where I extrapolate are marked ESTIMATE and say so.

Artefacts (all in this directory):

| path | what |
|---|---|
| `H0-stageC-schema.md` | this document: reconciliation, normative layout, semantics, sizes, costs, limits |
| `src/stagec_schema.py` | the schema implementation: canonical binary + canonical text, encoder/decoder, `validate_record`, `check_coverage`, `certificate_outcome` (stdlib only) |
| `src/mutations.py`, `runs/mutations.out` | 47-case mutation suite; 47/47 refused with the expected code |
| `src/demo_from_dump.py`, `runs/demo/` | one **real** v1 shard (record 0 of `batches/f0.bin`), binary + canonical text, round-trip verified |
| `src/make_coverage_plan.py`, `runs/coverage-plan.json` | the coverage/partition plan of the recorded run, derived from `commands.json` + the record files |
| `src/stagec_composition.py`, `src/make_composition.py` | the composition (**cover**) block: many-to-many incidence relation, both radius roles, cover counters; `runs/composition.bin/.txt/.json` is the real one (163 parents, 1,127 children, 11,838 incidences) |
| `src/outcome_demo.py` | the three certificate outcomes (accept / unresolved / reject) on real record bytes |
| `src/size_accounting.py`, `runs/size_accounting.json` | re-derives all 30 quantities of `h0-stagec-probe-summary.json` (0 mismatches) and prices v1 |
| `src/anal_rules.py`, `runs/rules_summary.json` | separation-rule census + margin decades + phase timing of a 256-record batch |
| `src/patch_rules.py`, `.scratch/build/` | the instrumented **copy** of upstream `stageC.cpp` that produced the census (upstream untouched) |

---

## 0. Bottom line

1. **The two accepted formats are not two formats.** They are two halves of one: A
   (`H0-stageC-criterion.md` §5) is the *evidence* half, B (`H0-stageC-search-controls.md` §3) is
   the *container* half. v1-draft takes B's container (one archive, `manifest.json`, one binary
   stream, LE/binary64) and A's evidence model (per-record facts, non-edges with reasons), and
   states which part is authoritative in each case (§2). Fourteen concrete conflicts are resolved
   in §2, each by a source line, a measurement, or the H1 coverage report.
2. **Two semantic defects in the accepted documents**, both in the verdict vocabulary:
   (i) A's §5 lists `empty` among the `UNRESOLVED` reasons, but `stageC.cpp:520` does
   `stats.negative++; return true` — an empty bin layer is a *completed exclusion* (A's own §7.1
   item 5 says so, so A contradicts itself); (ii) B says `POS` "is *not* an unresolved outcome",
   but at the statement level (`cert/spec/statement.md`: unresolved = "a validly formed region
   whose fate the certificate does not decide") a record carrying a (6.24) pattern is undecided
   and must count in the unresolved total. v1 keeps *seven* codes, mapped onto the statement's
   tri-state: `{NEG, EMPTY_BINS} → excluded`, `{POS, CAP, OVERFLOW, CLUSTER_FAIL, INTERNAL} →
   unresolved`, and `INVALID` is a *checker* verdict = reject, never a record verdict.
3. **The size accounting in both documents is 3.3× too small for the evidence layer.** Neither
   measures how many non-edge *entries* a certificate needs. On 256 real records the identity
   `E_O = pairs − |O|`, `E_U = pairs − |U|` holds in 256/256 cases, so the entry count is
   `2·pairs − |O| − |U|` — not `pairs − |O| − |U|`, which is what both documents price. Over the
   23,343 completed negatives that is **888,217,019 entries**, not 265,512,983 (§6).
4. **A measured certificate, from the probe census** (exact arithmetic on measured per-record
   values, with each record's actual `k` parsed from the archive): mode **R** (checker recomputes)
   payload **35.0 MiB**, TOTAL **35.1 MiB**; mode **W** (witnessed non-edges, balls stored)
   payload 885.2 MiB, TOTAL **885.2 MiB**; W + the optional adjacency cache TOTAL 1,219.1 MiB;
   W + stored joint-test directions `y` TOTAL 7,142.7 MiB (ESTIMATE). "TOTAL" adds the 30,509 B
   container (92 shard headers + manifest) and the mandatory 57,104 B composition block; "payload"
   is the per-record bytes alone. B's adjacency layer alone is 333.8 MiB packed — or 2.54 GiB in
   the fixed 32-word layout upstream actually uses.
5. **The certificate also needs a composition (cover) map, and a creation parent cannot stand in
   for it.** The accepted H1 coverage report (`.ultramath/smwgx104w/m2/H0-stageC-coverage.md`)
   measures **11,838 covering incidences** between the 163 unresolved records and the 1,127
   fallback records, **10,711 of them (90.5 %) inherited** from records created for a different
   parent. v1 therefore carries the covering relation as its own canonical block (§3.6), keeps
   a per-record **`atlas_radius`** distinct from the pass envelope (`pass_radius`), and encodes
   creation provenance nowhere in Stage C (it is Stage-B work). §4 states which part is checked.
6. **This does not make checking cheap, and the reason is measured** — but the numbers after the
   measurements are **extrapolations**, not measured costs (§5). Phase timing of the producer on
   one batch of 256 records: bin/cover layer 82.0 %, clustering 8.0 %, pair tests 8.9 %, search
   1.1 %. Any independent checker must verify the cover (H1) itself and the composition map on
   top of it, so no choice of graph representation removes that work; the best case saving from a
   witnessed evidence layer is under 9 % of producer time in that model. This contradicts A's
   cost model, which prices only the pair tests.
7. **`y` must not be stored.** The joint test (6.23) decides only **6.9 %** of non-edges on real
   records (measured: O 2.52 %, U 4.39 %), and its winning margins are large: the minimum decade
   over all 10.9 M entries of the batch is `1e-7` for both joint rules, and exactly **one** entry
   in 10.9 M lies below `1e-10`. So an outward checker re-deriving the joint test at a `1e-10`
   budget loses essentially nothing on this evidence — while storing `y` would cost 7 GiB.
   v1 therefore *forbids* stored `y` (flag reserved, must be 0).
8. **A real v1 record exists**: record 0 of `batches/f0.bin`, 49,033 bytes, binary and canonical
   text round-trip exactly, validates with 0 errors (including `atlas_radius` 0.0159919…
   ≤ `pass_radius` 0.016). Its adjacency agrees with m1's independent probe dump
   `g0.txt` **after** decoding each eight-byte group of the printed dump as big-endian and
   applying one of its explicitly recovered ball permutations; the two byte strings themselves differ.
   Exhaustive enumeration finds eight equivalent bijections, arising from three interchangeable
   pairs, so this is an explicit (but **not unique**) permutation witness.
   The archive alone cannot produce one (no ball radii, no ball list, no per-record verdict)
   — which is exactly the gap §8 quantifies.
9. **47/47 mutations are refused with the expected code** (§9), including the soundness-shaped
   ones: an edge silently dropped from the cache, an exclusion dropped while the cache keeps the
   edge, a record silently missing from a shard, a covering child that is not itself excluded,
   an unresolved record with no composition incidence, `atlas_radius > pass_radius`.

---

## 1. What each accepted format contributes, and what it lacks

| | A = `H0-stageC-criterion.md` §5 | B = `H0-stageC-search-controls.md` §3 |
|---|---|---|
| container | "one file per record", canonical text, JSON schema suggested | one archive + one `manifest.json` + one binary stream (LE, `u64`, binary64) |
| global pinning | per-record `fp {probe hash}` | manifest pins preprint sha256, 7 source sha256s, build line, the param tuple, CPU/libm probes, record-stream sha256 |
| stage-B data | full copy of `atlas.cpp`'s layout per record | unchanged upstream stream (356 + 288k B/record) |
| ball layer | `v, s, members{count, sha256(bin list)}` + `criterion{s_max, cover_ok, diam_ok}` | `s` only, "members are a hint; the checker may re-cluster" |
| graph | `excluded` list with `rule`, optional `y`, `slack`; bitsets redundant | full adjacency bitsets; union rule; "reject if the declared set misses an edge its own arithmetic retains" |
| verdicts | tri-state `EXCLUDED / UNRESOLVED{cap,overflow,cluster,empty,invalid} / PATTERN` | seven values in three groups, `NEG, EMPTY_BINS / POS / CAP, OVERFLOW, CLUSTER_FAIL, INTERNAL` |
| coverage | requires the `(offset, parts)` map + parent links, but does not define them | not addressed |
| composition cover | one `parent` per record, one `s_max` per record | not addressed (m2 measures that it is many-to-many and needs both radii) |
| numbers | hex float or "decimal with a declared outward radius", never bare `%.17g` | binary64 in the stream; manifest floats unspecified |
| sizing | `balls 56 B ≈ 13 KB/rec`, `excluded 8.5–14e3/rec at 1 B`, total 0.7–1 GB text / 0.3 GB binary | adjacency `2·M·ceil(M/64)·8` = 15,296 B at M=239, 0.36 GB total |

A is the stronger document on *semantics* (it says what evidence a non-edge needs and why a
certificate without `s` is vacuous) and the weaker on *mechanics* (no container, no partition
map, per-record `fp`). B is the stronger on *mechanics* and the weaker on *semantics* (adjacency
without reasons, `POS` miscounted, partition map absent). v1-draft is B's container with A's
evidence model, and both defects above fixed.

---

## 2. The fourteen conflicts and how v1 resolves them

**R1 — container granularity.** A: one file per record. B: one archive, one stream.
*Resolution (B).* A certificate is a *set*; per-file granularity makes "which records exist" a
directory listing rather than a checked fact, which is the D2 failure mode A itself identifies.
v1: one binary stream per shard, one canonical `manifest.json`, and a **derived canonical text
rendering** (A's idea, kept for auditability) that must be byte-deterministic from the binary.
Measured: text is **8.59×** the binary on the real record (§8), so text is for review, not
distribution.

**R2 — where the ABI/FP probe lives.** A: `fp` inside every record. B: in the manifest.
*Resolution (B).* An ABI probe is a property of the run; duplicating it per record costs bytes and
creates the possibility of two records claiming different FP environments. v1 keeps it in the
manifest only.

**R3 — the empty-bin-layer verdict.** A: `UNRESOLVED, reason ∈ {cap, overflow, cluster, empty,
invalid}`. B: `EMPTY_BINS` is a legitimate completed exclusion.
*Resolution (B), and A is internally inconsistent.* Upstream `stageC.cpp:520`:
`if(prev.empty()){stats.negative++;return true;}` — `true` is the *excluded* return; the same
function returns `false` for both `cap` and `positive` and the difference is only in the `gaveup`
flag (`graph::candidate()` returns `q || gaveup`, `stageC.cpp:487`). A's own §7.1 item 5 agrees
("`:520`, which IS an exclusion and is legitimate"). The recorded run has **zero** empty-layer
records (lead census: all 23,506 records reached the graph stage), so this defect costs nothing in
practice, but the format may not contain it: otherwise a future certificate could report an
exclusion as unresolved (harmless) *or* the reverse by editing one enum.

**R4 — the POS verdict.** B: "`POS` … is *not* an unresolved outcome and must not be counted with
the next group."
*Resolution: rejected.* `cert/spec/statement.md` defines `unresolved` as "a validly formed region
whose fate the certificate does not decide"; a region where the search *found* a (6.24) pattern is
exactly that (the pattern is not a configuration — it is a reason the record survived). v1 keeps
`POS` as its own code (it is a positive *witness*, and unlike `CAP` it is a function of the graph,
not of a budget) but classifies it as unresolved for the roll-up. The statement's target requires
the unresolved count to be zero; a format in which `POS` is neither excluded nor unresolved cannot
express that.

**R5 — invalid records.** A: "each step's failure invalidates the record, and `invalid` is never
`excluded`." Correct but incomplete: if invalidity were merely "not excluded", a certificate could
be filled with garbage and still report zero unresolved. *Resolution:* `INVALID` is not a record
verdict at all. A structurally wrong record, or a record whose declared facts fail verification,
makes the **certificate** `reject` — never `unresolved`. This is implemented in
`certificate_outcome` and exercised in `runs/mutations.out`.

**R6 — what is authoritative for the graph.** A: the `excluded` list is the content; bitsets are
redundant. B: the bitsets are the content, the checker may take the union with its own graph and
"must reject if the declared set is missing an edge its own arithmetic retains".
*Resolution: A's direction, with B's union rule shown to be bought at no gain.* If `G_rec` and
`G_dec` both over-approximate the true relation graph then so does `G_rec ∪ G_dec`; hence under
B's rule **the declared adjacency contributes nothing to soundness** — the checker re-derives
every pair anyway — while B still stores 333.8 MiB. v1 therefore: (i) the declared **non-edge set
with evidence** is authoritative (mode W); (ii) adjacency is an *optional cache* that must
**equal** the graph rebuilt from the non-edge set (`E_ADJ_EXCL`), not a union, which turns it into
a free cross-check; (iii) mode R carries no graph at all. Measured consequence in §6/§7: the cache
costs 10× the whole mode-R certificate and buys no trust.

**R7 — the joint-test direction `y`.** A: "store `y` only when the checker cannot re-derive a
witness". B: does not store it.
*Resolution (B), measured.* `graph::joint<m>` computes `y` itself from a solve, so `y` is
derivable; but the honest reason not to store it is size and redundancy: joint rules are 6.9 % of
entries (measured), `y` is 14 (O) or 13 (U) doubles = 112/104 B per entry, and over the run that
is **7.0 GiB ESTIMATE** for a quantity a `1e-10`-budget outward re-derivation reproduces on
≥ 99.9999 % of entries (margin census, §7). v1 reserves the flag (`FLAG_Y`, must be 0) so the
choice is explicit and auditable rather than silently absent.

**R8 — ball member lists.** A: per ball, `members{count, sha256(bin index list)}`; plus per layer
the retained count and a hash of the bin index list. B: no members.
*Resolution (B), with A's cover obligation preserved.* Measured: the final-layer retained bin count
over the run is **485,599,722** bins (`h0-stagec-probe-summary.json`); at the tightest honest
encoding (33-bit bin index + a `u16` ball assignment per bin) that is 2.8–3.2 GiB of member data
whose only verification value is as a cross-check of a set the checker must re-derive *anyway* to
prove cover (a retained bin set is only an over-approximation of the admissible vectors; covering
it needs the layer tests). v1 stores the ball list without members and makes the cover obligation
a **checker obligation**, with `cover_mode ∈ {RECLUSTER, BINSET}` (BINSET = the shard ships the
retained-bin *set*, not per-ball lists) and `BOXCERT` reserved for the monotone box-covering
certificate that would actually make the cover cheap (§7.3).

**R9 — coverage / partition semantics.** A requires the map and the parent links but never defines
the upstream rule; B omits it entirely.
*Resolution: defined from the source and instantiated on the real run.* `stageC.cpp:546-559`:
`size_t offset` accumulates across `argv[11..]` in order; record `offset+i` is processed iff
`(offset+i) % parts == part`; `argv[10]` is the *bad* output file; `return bad.empty()?0:1`. v1
therefore places the partition rule in the **shard header** (`pass`, `part`, `parts`) and the
identity of every record in the **record header** (`input_file`, `input_index`), so coverage is
checked per record rather than by counts. `runs/coverage-plan.json` is the resulting plan for the
recorded run: **pass `initial` = 88 commands, 88 input files, 22,379 records, `parts=1` each;
pass `final` = 4 commands over the single file `fb1.bin`, 1,127 records, `parts=4`**. Note this is
*not* one `parts=4` split of 22,379 records (each batch command was its own shard), which is why a
pass in v1 is a list of commands, not a single `(part, parts)` pair.

**R10 — number canonicalisation.** A forbids bare `%.17g`; B leaves manifest floats unspecified.
*Resolution: split by layer.* (i) In the binary stream every double is a binary64 **bit pattern**;
`-0.0` is canonicalised to `+0.0` and NaN/Inf are forbidden in every field (`E_NONFINITE`). (ii) In
`manifest.json` there are **no non-integer JSON numbers at all** — JSON's number is parsed with
implementation-defined precision, so any float is a portability defect; non-integers are
hex-float strings (`0x1.5810624dd2f1bp-5`), integers above 2^53 must be decimal strings, keys must
be ASCII and sorted, duplicate keys are refused, and the file must equal its own re-serialisation
byte for byte (`E_MANIFEST_CANON`). (iii) The canonical **text** form uses `float.hex()`
round-trip-exact and is *derived*; authority stays with the binary.

**R11 — ball ordering.** Neither document fixes an order, yet both address balls by index, so the
same mathematical content serialises differently for different producers and a hash comparison is
meaningless. *Resolution:* balls are sorted by the IEEE **totalOrder** key of `(v0..v5, s)` and must
be strictly increasing (`E_BALL_ORDER`, duplicates `E_BALL_ORDER`); exclusions and adjacency use
that order. On the real record the required permutation is **non-trivial** (§8), i.e. without this
rule the record's bitsets would not be comparable to any other producer's.

**R12 — sizing basis.** Both documents size the evidence by `pairs − |O| − |U|`. *Resolution:
rejected, see §6* — the entry count is `2·pairs − |O| − |U|`, 3.345× larger on the run.

**R13 — the composition (cover) map, and what a `parent` field can mean.** A's obligation 9 and B
both speak of "parent links", and A's §5 sketch has a single `parent` per record.
*Resolution: rejected as insufficient — the accepted H1 coverage report
(`.ultramath/smwgx104w/m2/H0-stageC-coverage.md`, §0.4/§5) measures that the cover relation of the
recorded run is many-to-many and cannot be replaced by a per-record parent:* 163 unresolved records
are covered by 1,127 fallback records through **11,838 covering incidences**, **10,711 (90.5 %)
inherited** from records created for a different parent (median 71 children per parent, max 161;
only 4 of 163 parents use no inherited child). A per-record `parent` would be wrong for 159 of the
163. v1 therefore: (i) **removes** the per-record parent field; (ii) makes the covering relation a
mandatory canonical **composition block** per pass transition (§3.6), with the per-parent cover
counters (`base, inside, snaps, fail`) m2 asks for; (iii) states explicitly that **creation
provenance** (which `fine.bin` record a fallback record was built from) is **not** part of Stage C
— it is Stage-B evidence and is not encoded, deliberately (not "forgotten": the cover map is what
soundness consumes). The repaired block costs 57,104 B; its identifier-only provenance patch is
explicitly recorded in `certdata/runs/h1-coverage/composition-v1.patch.json`.

**R14 — two radius roles per record.** A stores `radius` once (inside its copy of the stage-B
record) and B inherits the same single field. *Resolution: rejected — one radius cannot serve both
layers.* The batch files are an order-preserving copy of `data/fine.bin` with the final radius
**overwritten by the pass envelope** (`.016`, `.011`); the refiner's own cover was computed at the
*atlas* radius, which is strictly smaller (measured worst-case slack `9.4188e-8` in the initial pass
and `1.8892e-7` in the fallback, m2 §3/§6). A checker that used the envelope for the refiner's cell
lattice would be checking a larger region than the one that was covered. v1 therefore carries
**both**: `atlas_radius` as a new record-header field (offset 36, binary64) and `pass_radius` as the
stage-B radius field, with the validator enforcing `0 ≤ atlas_radius ≤ pass_radius ≤ .03`
(`E_RADIUS`, `E_RADIUS_ORDER`). On record 0 of `batches/f0.bin`: `atlas_radius = 0.015991855587698802`,
`pass_radius = 0.016`.

---

## 3. Normative layout (exact widths, endianness, canonical form)

All integers and all double bit patterns are **little-endian**; doubles are IEEE-754 binary64.
`u8/u16/u32/u64` are unsigned fixed width. No field is ever reordered or omitted; reserved fields
must be zero (`E_RESERVED`). Implemented and round-trip tested in `src/stagec_schema.py`
(`REC_FMT = '<IBBBBHHIHHIIIIBBBBIIQQ'`, `struct.calcsize == 64`).

### 3.1 Shard file = header (80 B) + body (records, concatenated)

| off | size | field | rule |
|---|---|---|---|
| 0 | 8 | `magic` | ASCII `SCV1STAG` (`E_MAGIC`) |
| 8 | 2 | `version_major` | 1 (`E_VERSION`) |
| 10 | 2 | `version_minor` | 0 |
| 12 | 4 | `pass_id` | index into `manifest.passes` |
| 16 | 4 | `part` | must equal the command index of the pass (R9) |
| 20 | 4 | `parts` | `1 ≤ parts`, `part < parts` (`E_PART`) |
| 24 | 8 | `n_records` | |
| 32 | 8 | `body_bytes` | must equal the file length − 80 (`E_LEN`) |
| 40 | 32 | `sha256(body)` | checked before anything else (`E_BODY_HASH`) |
| 72 | 8 | reserved | 0 |

The body hash is the outermost integrity check: any flipped payload byte is reported as
`E_BODY_HASH`, not as a downstream semantic error (one mutation demonstrates exactly this).

### 3.2 Record header (64 B)

| off | size | field | semantics |
|---|---|---|---|
| 0 | 4 | `len` | total record bytes including this header (`E_LEN`) |
| 4 | 1 | `kind` | 1 = `BODY` (stage-B payload inline), 2 = `REF` (take it from the input file named by `input_file`/`input_index`) |
| 5 | 1 | `evidence` | 0 = `RECOMPUTE`, 1 = `WITNESS` |
| 6 | 1 | `verdict` | 1..7, table 3.4 |
| 7 | 1 | `cover_mode` | 0 = `RECLUSTER`, 1 = `BINSET`, 2 = `BOXCERT` (**reserved, refused**) |
| 8 | 2 | `flags` | bit0 `ADJ`, bit1 `BALLS`, bit2 `Y` (reserved, must be 0) |
| 10 | 2 | reserved | 0 |
| 12 | 2 | `input_file` | position in the *command's* input list (R9) |
| 14 | 2 | reserved | 0 |
| 16 | 4 | `input_index` | index inside that input file (with `input_file` this *is* the verdict's provenance; there is deliberately no `parent` field, see R13) |
| 20 | 4 | `n_balls` | ≤ 2048 (`E_BALL_CAP`, = upstream `cluster` cap and `BS::L·64`) |
| 24 | 4 | `n_excl` | number of non-edge entries (not pairs) |
| 28 | 4 | `n_bins_last` | retained bins at the final layer, ≤ 2·10⁶ (`E_BINS_BOUNDS`) |
| 32 | 1 | `empty_at_layer` | 1..6 for `EMPTY_BINS`, else 0 |
| 33 | 1 | `detail` | recorded `detail`, 0..10; `detail = 0` makes (6.23) vacuous (`stageC.cpp:309`) so it must be recorded |
| 34 | 1 | `search_mode` | recorded `searchMode`, 0..2 |
| 35 | 1 | reserved | 0 |
| 36 | 8 | `atlas_radius` | binary64: the radius the refiner's cover was computed at (`fine.bin` value), `0 ≤ atlas_radius ≤ pass_radius` (R14) |
| 44 | 4 | `k` | stage-B tangent count, 0..10; must equal the inline stage-B `k` (`E_K_MISMATCH`) |
| 48 | 8 | `steps_used` | search steps consumed (`graph::steps`) |
| 56 | 8 | `cap_steps` | recorded cap, 100 .. 10⁹ (upstream argument check) |

`pass_radius` is not a new field: it is the stage-B record's own radius (payload item 1, the 8th
double), which for this archive is the pass envelope. The format requires the two roles to be
*distinguishable*, not stored twice.

Payload, in this fixed order, present only when the predicate says so:

1. `kind == BODY`: the upstream record, byte for byte — `int32 k`, 36 × binary64 `P`,
   `k·36` × binary64 `T`, 8 × binary64 `(C, n0, id, ort, hor, mnorm, froot, radius)`; size
   `356 + 288k`. (`kind == REF` stores 0 bytes.)
2. `evidence == WITNESS` or `flags·BALLS`: `n_balls × 56` B = 6 × binary64 centre (cycles) +
   binary64 radius.
3. `evidence == WITNESS`: the exclusion block (3.3).
4. `flags·ADJ`: `2 · n_balls · ceil(n_balls/64) · 8` B: for each of O then U, row-major
   `n_balls` rows of `ceil(n_balls/64)` u64 words.
5. `verdict == POS`: `12 × u32` ball labels, the first 6 the A-side, the last 6 the B-side.

### 3.3 Exclusion block

`P = C(n_balls, 2)`, `E = n_excl`. Bytes = `ceil(2P/8) + ceil(4E/8)`.

* **bitmap**: pair `(i,j)`, `i<j`, occupies bit `2p` and `2p+1` of a bit stream packed LSB-first,
  where `p` is the pair's position in **lexicographic order**:
  ```
  p(i,j) = i·n − i(i+1)/2 + (j − i − 1),      n = n_balls
  ```
  bit `2p` = "the relation **O** is excluded for this pair", `2p+1` = "**U** is excluded".
  A pair with neither bit set is an edge in *both* graphs; that is the free direction.
* **codes**: one 4-bit code per set bit, in the order (pair ascending, O before U), packed
  LSB-first. 0..5 = table 3.4.
* Invariants: `popcount(bitmap) == n_excl` (`E_EXCL_COUNT`); each code's relation must match its
  slot (`E_EXCL_REL`); codes are ≤ 5 (`E_EXCL_CODE`); the decoded list is strictly increasing in
  `(i, j, O<U)` (`E_EXCL_ORDER`).
* Exactly one identity ties the two representations: an **O edge exists iff the pair carries no
  O-exclusion**, likewise U. When a cache is present the validator checks it
  (`E_ADJ_EXCL`), which is the mutation that catches "the cache and the evidence disagree".

### 3.4 Verdicts and rules

| code | verdict | class | required facts |
|---|---|---|---|
| 1 | `NEG` | **excluded** | `n_balls ≥ 1`, `1 ≤ steps_used ≤ cap_steps`, `empty_at_layer = 0` |
| 2 | `EMPTY_BINS` | **excluded** | `empty_at_layer ∈ 1..6`, `n_balls = 0`, `n_excl = 0`, `steps_used = 0` |
| 3 | `POS` | unresolved (a witness of survival) | 12 distinct in-range labels; the adjacency must be present and contain 15+15 O edges and 36 U edges (`E_POS_EDGE`) |
| 4 | `CAP` | unresolved | `steps_used > cap_steps` (`E_CAP`) |
| 5 | `OVERFLOW` | unresolved | — (`Layer::binCap = 2·10⁶`, `stageC.cpp:35`) |
| 6 | `CLUSTER_FAIL` | unresolved | — (`stageC.cpp:204`, `:219`, `:220`) |
| 7 | `INTERNAL` | unresolved | any other failure path |

| code | rule | relation | extra bytes | evidence the checker must verify |
|---|---|---|---|---|
| 0 | (6.16) left | O | 0 | `|S|/(2π√6) > s_l + s_l'` |
| 1 | (6.16) right | U | 0 | `‖S‖/√6 − 1|/(2π) > s_l + s_l'` |
| 2 | (6.20) | O | 0 | `|S|²/(2π) > 6 r_e ‖D_U‖ + π r_e² |S|` |
| 3 | (6.21) | U | 0 | `|q_U| > r_e ‖D_U‖ + π r_e²(1+|S|/6)` |
| 4 | (6.23) with (6.22), ℓ = 2 | O | 0 (y refused) | ∃y: `|c·y| > support_O(y)` |
| 5 | (6.23) with (6.22), ℓ = 1 | U | 0 (y refused) | ∃y: `|c·y| > support_U(y)` |

Note how little the evidence costs in *bytes*: only (6.23) could have needed a direction vector,
and it is refused; rules 0–3 are witnessed entirely by the two ball centres and radii that the
ball list already stores. The 4-bit code is therefore the whole per-entry cost.

### 3.5 Canonical JSON manifest

Canonical form: UTF-8, ASCII-only escapes, no BOM, one trailing `\n`, no whitespace after `,`/`:`,
object keys sorted by code point, **no non-integer JSON numbers** (hex-float strings instead),
integers ≤ 2^53 as numbers and larger ones as decimal strings, duplicate keys refused. The
validator re-serialises and compares bytes (`E_MANIFEST_CANON`), which makes "canonical" a
*checked* property rather than a convention. Required keys: `format = "stagec-v1"`,
`preprint_sha256`, `sources` (the seven upstream files + build line), `params`, `arithmetic`
(the kernel contract id, `cert/spec/arithmetic.md`), `passes` (§4), `radii` (which layer uses which
radius, R14), `composition` (the block file, its counts and the exact-string `composition_metric`,
§3.6), `trust` (what Stage C does not check). `runs/coverage-plan.json` is a real, canonical instance of the `params` and `passes`
sections for the recorded run (18,953 B).

### 3.6 Composition (cover) block — mandatory when a pass leaves records unresolved

One canonical block per pass transition, as its own file (28-byte header + three tables):

| off | size | field |
|---|---|---|
| 0 | 8 | magic `SCV1COMP` |
| 8 | 2+2 | version 1.0 |
| 12 | 4 | `pass_id` — the parent pass index (children live in `pass_id + 1`) |
| 16 | 4 | `n_parents` |
| 20 | 4 | `n_children` |
| 24 | 4 | `n_links` |
| 28 | 32·n_parents | parents: `u32 global, u32 base, u32 inside, u32 relation_marks, u32 snap_closed_cells, u32 fail, u16 created, u16 inherited, u16 degree, u16 reserved` |

There is **no reserved header word after these counts**. In particular, the initial pass uses
`pass_id = 0`, and `global` is a record's global position in that parent pass's input stream, not
its ordinal within a `bad*.bin` file. For this run the capped-record identity mapping is recovered
by `(batch index in the input bad file, ordinal inside that file)`, then translated to the original
batch/fine position by the capped-record manifest. The current `composition-cover-map.json` carries
that actual offset in `fine_index`, retains the bad-file ordinal in `batch_index`, and states the
convention in `index_scheme`. The eventual v1 format should make each parent's record digest a
mandatory field: the present unsigned index is pinned by the manifest and the byte-derived capped
set, not intrinsically by the block alone. The repaired block is
`certdata/runs/h1-coverage/composition-v1.bin` (SHA-256
`fd61d25749c9ba55cd3082af7023b1b52b09c4715b64fdc2dbcac54616e0f819`).
Its deliberate replacement of the earlier misaddressed emission is documented in the adjacent
`composition-v1.patch.json`; that earlier emission is not a byte-identical provenance twin.
| … | 4·n_children | children: `u32` global index in the child pass |
| … | 4·n_links | links: `u16 child_local, u16 parent_local` |

Canonical order: parents and children strictly increasing by global index, links strictly increasing
by `(child_local, parent_local)`, duplicate-free. The **cover metric** is not data: it lives in the
manifest as exact strings (`composition_metric`: `w`, `target_child_radius`, `E_formula`,
`naxis`, `cells_total_per_parent`, `inside_cells_per_parent`, `cover_criterion`) — for the recorded
run: `w = 0.0038`, `target_child_radius = 0.011`, `E = sqrt(1+ort)·R + 1e-7` with `R` the
*parent's* `atlas_radius`, `naxis = 11`, `14,641` cells per parent, `3,161` of them inside
(m2's model and criterion, cited not re-derived).

Size for the recorded run: **57,104 B** = 28 + 5,216 + 4,508 + 47,352 (m2 estimated 23,676 B at
2 B/incidence for the relation alone; the block also carries the counters and the child table).
Internal checks (`check_composition`, no records needed): sortedness, no duplicate incidence,
`degree` = number of incidents, `created + inherited = degree`, `Σcreated = n_children`,
`Σinherited = n_links − n_children`, `fail = 0`, `inside = relation_marks + snap_closed_cells ≤ cells_total`, and the metric's
declared `inside_cells_per_parent` where it is constant (it is, for all 163). Record-level checks:
every parent is an unresolved record of the parent pass, every child is an `EXCLUDED` record of the
child pass, and every unresolved record appears exactly once as a parent. The real block
(`runs/composition.bin`, from m2's recovered map) passes the internal checks with
163 / 1,127 / 11,838 / 10,711.

--- 

## 4. Coverage, partition and roll-up semantics

**Pass = one logical batch**, with a pass-level index space = the concatenation of `pass.inputs`
in order — exactly the `offset += v.size()` space of `stageC.cpp:546-559`. **Command = one
upstream invocation**: a list of file indices (argv order), `parts`, `part`, and the single shard
it wrote (identified by `pass_id`/`part` in the shard header).

`check_coverage` enforces three things:

1. *inside a command*: the shard's records are exactly `{g : g % parts == part}` over that
   command's own index space, each once (`E_COV_PART`, `E_COV_DUP`, `E_COV_MISSING`);
2. *across a pass*: every pass-level global index occurs exactly once — a dropped input record
   cannot pass as success (`E_COV_MISSING` names the count and the first missing indices);
3. *across passes* — the **composition** block (§3.6), never a per-record parent: every
   unresolved record of pass *p* appears exactly once as a parent of the block
   (`E_COVER_MISSING`), every incidence points at a child that is itself `EXCLUDED`
   (`E_COVER_CHILD_STATE`), the counters are consistent (`E_COVER_DEGREE`, `E_COVER_CREATION`,
   `E_COVER_COUNTERS`), and the block exists whenever pass *p* leaves anything unresolved
   (`E_COVER_MISSING`). **Creation** provenance (which `fine.bin` record a fallback record was
   built from) is not in Stage C at all (R13).

The recorded run instantiates as: pass `initial` = 88 commands × (1 input file, `parts=1`) =
22,379 records with `pass_radius = .016`; pass `final` = 4 commands × (the single file `fb1.bin`,
`parts=4`) = 1,127 records with `pass_radius = .011` (`runs/coverage-plan.json`, derived from
`commands.json` and the record files, not from prose), plus one composition block linking the 163
unresolved initial records to their covering fallback records (`runs/composition.bin`, from m2's
recovered map).

**Certificate roll-up** (`certificate_outcome`): any structural error ⇒ `reject`; else any
unresolved record ⇒ `unresolved`; else `accept`. `reject` dominates `unresolved`, so a producer
cannot hide a malformed record by labelling it unresolved (R5).

**What Stage C does not check, stated in `trust`:** that the children of an unresolved record
*cover that record's region* (a Stage-B obligation: the re-refinement `(.011, .0038)` of the
cap-hit records), the L1 parameter arithmetic (§6.9 of A: `tau, comb` per layer), and the
arithmetic kernel contract. These are outside Stage C by construction and must appear as explicit
hypotheses, not be silently implied.

---

## 5. What the checker must still do, and what it costs

Ordered obligations. Steps 1, 2 and 6 are implemented here; 3, 4, 5, 7 and 8 are the mathematical
obligations the format exists to make checkable. **Only steps 1–2 and the producer's own timing are
measured. Every total in this section is an extrapolation, and is labelled as such.**

| # | obligation | where | cost |
|---|---|---|---|
| 1 | parse, body hash, `validate_record` (bounds, canonical order, adjacency invariants, verdict consistency, `E_ADJ_EXCL`, the two radius roles) | `src/stagec_schema.py` | linear in bytes |
| 2 | `check_coverage` (rules 1–2 of §4) + `check_composition` (rule 3) + roll-up | `src/stagec_schema.py`, `src/stagec_composition.py` | linear in records + incidences |
| 3 | **cover (H1)**: recompute the bin layer for the record's `(P, T, k, r)` with outward thresholds, then exhibit for every retained bin a ball with `‖h‖ + X_M ≤ s` | checker obligation, `cover_mode` | measured share of producer time: 82 % (+ 8 % clustering) |
| 4 | **composition cover**: for every incidence, re-derive the cell-lattice cover of the parent box by the child ball, at `E = sqrt(1+ort)·R + 1e-7` with `R` = the parent's `atlas_radius` | checker obligation (§3.6 metric) | m2: **35–55 CPU-min** at their measured re-derivation rate (their number, for this obligation) |
| 5 | **each non-edge**: verify its rule outward (table 3.4) — rules 0–3 need only the two balls; rules 4/5 re-derive the joint test (0.102 solves per pair, measured on the batch) | obligation | ≤ 9 % of producer time (batch model) |
| 6 | **graph rebuild**: `O` = pairs without an O-exclusion, `U` likewise; a cache must be *equal*, not merged | implemented | free |
| 7 | **search (H4)**: complete (6.24) search, no pattern, `cap_hit = false`; a `POS` witness is confirmed by direct edge check (36 U + 30 O edges), never by search | obligation | 1.1 % of producer time (batch model) |
| 8 | L1 parameters (`tau`, `comb` per layer) and the kernel contract | `cert/spec/arithmetic.md`, A §6.9 | once per `(params, r)` |

### 5.1 What is actually measured

Instrumented copy of upstream `stageC.cpp`, **one batch: 256 records of `batches/f0.bin`**
(2.9 % of the initial pass), reproducing `C.batch0.txt` and all five probed per-record fields of
the lead's log 256/256:

| phase | share of that batch's CPU |
|---|---|
| bin layer (`Layer::gen0/gen1/test`) | **82.0 %** |
| clustering (`cluster`, Lloyd) | 8.0 % |
| pair tests (`graph::init` → `pairtest`) | 8.9 % |
| search (`exist`) | 1.1 % |

and, uncontended, **0.112 s/record** for the whole pipeline (agreeing with m1's 0.117 s/record).
The share run itself was contended (105 s wall for 28.7 s of work), so the *shares* are the robust
output and the absolute per-record figure comes from the uncontended runs.

### 5.2 What is extrapolated (not measured)

* **43.6 CPU-min** for the 23,343 record-verdicts in binary64 = 23,343 × 0.112 s. This is one
  batch's rate applied to the run; the run contains 163 denser cap-hit records and 1,127 fallback
  records that were not timed here. It agrees with m1's independent 47 CPU-min estimate.
* **7–22 CPU-hours for an "exact" checker**: 43.6 min × {10.1, 15.4, 30.1} (m1's long-double,
  double-double and interval⟨dd⟩ factors). Those factors came from a **dot-product/solve-shaped
  kernel benchmark**, not from an exact bin-layer or clustering kernel — the two phases that carry
  90 % of the time. **No exact or outward Stage-C run exists**, in this swarm or anywhere I know of.
  The figure is a model, and a *cover certificate* (§7 below, `cover_mode = BOXCERT`) could change
  it substantially in either direction.
* **"under 9 % saving from a witnessed evidence layer"**: 0.63 joint solves per pair in the
  producer against 0.102 joint entries per pair in mode W (both measured on the batch) applied to
  the 8.9 % pair-phase share. It is arithmetic on two measured ratios, not an end-to-end trial.
* **The batch census cannot set a run-wide floor.** Anything of the form "checking costs at least
  X" is unsupported: §7's margins and the phase shares are one batch's, the cap-hit records are
  2.7× denser in `O`, and no exact run exists to compare against. The only defensible statement is
  conditional: *if* the exact kernel carries the same relative cost as the binary64 one, the floor
  is dominated by the bin/cover and composition layers, not by the graph evidence.

## 6. Size accounting, recomputed from the census

`src/size_accounting.py` first **re-derives every number of `h0-stagec-probe-summary.json`** from
the 23,506-row per-record table (`pairs`, `O_plus_U`, `nonedge_reason_slots`, `adjacency_bytes`,
`steps` for each of `all / initial / final / completed_negatives / capped`, 30 quantities) and
asserts equality: **0 mismatches**. It then prices the certificate from those same per-record
`(balls, |O|, |U|)`, with each record's **actual `k`** parsed from the archived record streams
(the certificate set is k = 4 for 23,342 records and **k = 0 for one** — `fine.bin` index 22,378,
the last record of `batches/f87.bin` — so its stage-B payload is 356 B, not 1,508 B).

| quantity | value (23,343 completed negatives = the certificate set) |
|---|---|
| pairs `C(M,2)` | 622,704,036 |
| `|O| + |U|` | 357,191,053 |
| non-edge **slots** `pairs − |O| − |U|` (A/B's sizing basis) | 265,512,983 |
| non-edge **entries** `2·pairs − |O| − |U|` (v1's basis) | **888,217,019** |
| ratio entries / slots | **3.345** |
| balls (sum of `M`) | 5,208,425 (5,272,329 including the 163 cap records) |
| k histogram | 23,342 × k=4, 1 × k=0 |
| steps | 2,932,018,956 |

Why the entry count is exact: on all 256 records of batch 0 the two identities
`E_O = pairs − |O|` and `E_U = pairs − |U|` hold (`runs/rules_summary.json`; mismatch count 0 over
256 × 2 identities). A pair may be a non-edge in **both** relations and then needs **two** entries
with different rules, so `pairs − |O| − |U|` is not the number of things a certificate must say.

**Payload** = bytes carried per record; **container** = 92 shard headers (88 initial + 4 fallback
commands) + the canonical manifest (coverage plan 19,631 B + 32 B per shard hash + the metric
block); **composition** = the cover block of §3.6, which this run cannot omit because it has 163
unresolved records.

| layer | bytes | per record | MiB |
|---|---|---|---|
| stage-B record (`356 + 288k`, actual k) | 35,200,092 | 1,508 | 33.6 |
| balls (56 B each) | 291,671,800 | 12,495 | 278.2 |
| evidence (2-bit pair bitmap + 4-bit codes) | 599,793,258 | 25,695 | 572.0 |
| record headers (64 B, ×23,343) | 1,493,952 | 64 | 1.4 |
| adjacency, `ceil(M/64)` words | 350,022,800 | 14,995 | 333.8 |
| adjacency, upstream's fixed 32-word layout (`BS::L = 32`) | 2,666,713,600 | 114,240 | 2,543.2 |
| container (shard headers + manifest) | 30,509 | 1.3 | 0.0 |
| composition (cover) block | 57,104 | 2.4 | 0.1 |

| certificate variant | bytes | per record | MiB | notes |
|---|---|---|---|---|
| **mode R** payload | 36,694,044 | 1,572 | 35.0 | stage-B + headers only: the graph and the ball family are checker obligations |
| **mode R TOTAL** | **36,781,657** | 1,576 | **35.1** | + container + composition |
| **mode W** payload | 928,159,102 | 39,762 | 885.2 | + balls + evidenced non-edges |
| **mode W TOTAL** | **928,246,715** | 39,765 | **885.2** | A's design, priced correctly |
| mode W + adjacency cache TOTAL | 1,278,269,515 | 54,760 | 1,219.1 | B's design; the cache must *equal*, not union |
| mode W + stored joint `y` TOTAL **ESTIMATE** | 7,489,709,867 | 320,855 | 7,142.7 | 61,368,976 joint entries × 112/104 B, rule mix extrapolated from batch 0 |

Corrections to the accepted documents' numbers:

* A's `balls 56 B ≈ 13 KB/record` — **confirmed** (12,495 B/record measured).
* A's/B's evidence estimate of `8.5–14 KB/record at 1 byte` (or 265 MB total) — **3.345× too
  small**: the measured need is 25,695 B/record, 572 MiB, because entries, not pairs, are what a
  certificate stores.
* A's total "~0.7–1 GB text / ~0.3 GB binary" — the binary TOTAL is **885.2 MiB** (mode W) or
  **35.1 MiB** (mode R); no variant reaches 0.3 GB.
* B's adjacency "≈0.36 GB" — **confirmed packed** (333.8 MiB), and **2.48 GiB** in the layout the
  upstream binary actually uses. Since (R6) that layer buys no trust, this is the least defensible
  byte in either design.
* `member` lists (A's `sha256(bin index list)` per ball) would be 2.8–3.2 GiB (`485,599,722`
  retained bins at 6.1–7 B each) and verify nothing the checker does not re-derive.
* Neither document prices the **composition** block (57,104 B, R13) or the second radius role
  (R14, 8 B/record = 187 KB): both are small, but they are the two items without which the
  certificate does not type-check against the run's own structure.

## 7. Decidability census: would an outward checker retain the same non-edges?

Measured on batch 0 (256 records, 10,911,169 entries), by instrumenting the *producer's* decision
points and histogramming each entry's margin by decade (`runs/rules_summary.json`):

| rule | entries | share | per record | min decade | < 1e-10 | < 1e-8 | < 1e-6 |
|---|---|---|---|---|---|---|---|
| (6.16) O | 5,995,139 | 54.94 % | 23,418 | 1e-8 | 0 | 0 | 41 |
| (6.16) U | 3,198,826 | 29.32 % | 12,495 | 1e-9 | 0 | 2 | 54 |
| (6.20) O | 400,134 | 3.67 % | 1,563 | 1e-8 | 0 | 0 | 17 |
| (6.21) U | 563,192 | 5.16 % | 2,200 | **1e-11** | **1** | 2 | 43 |
| (6.23) O | 275,000 | 2.52 % | 1,074 | 1e-7 | 0 | 0 | 2 |
| (6.23) U | 478,878 | 4.39 % | 1,871 | 1e-7 | 0 | 0 | 36 |
| total | 10,911,169 | | 42,622 | | 1 | 4 | 193 |

Reading, stated as narrowly as the evidence allows:

* The producer's slacks (`+2e-7` on the distance tests, `+2e-8` on `E_O/E_U`, `+3e-7` on the joint
  test, `+1e-10` on `r_e`) are *conservative*, so the margin recorded here is a **lower bound** on
  the margin an exact check would see. At a `1e-10` outward budget, **1 entry of 10.9 M** becomes
  undecidable in this batch; at `1e-8`, 4; at `1e-6`, 193 (0.002 %). Those entries would be
  *retained as edges* (the sound direction), so the effect is a slightly denser graph, never a
  false exclusion.
* The joint rules are the *safest* (min decade `1e-7`, nothing below `1e-7`), which is why refusing
  stored `y` (R7) is not a soundness trade: re-deriving them costs 14 CPU-min over the run and
  loses nothing measurable.
* This is **one batch of 256** records (2.9 % of the initial pass, all with `pass_radius = .016`)
  and the cap-prone records are denser in `O`; the census must be repeated on the 163 cap-hit
  records and on a fallback sample before any global claim. Not done here (CPU shared with five
  other members; the heavy runs belong to the members who own them). **No statement in this
  document about "how many exclusions an exact checker keeps" is run-wide**; and since there is no
  exact Stage-C run, nothing here is evidence about the exact kernel's *speed*, only about how
  close the producer's decisions sit to the decision boundary.

---

## 8. A real v1 record, and what the archive cannot supply

`src/demo_from_dump.py` builds record 0 of `batches/f0.bin` into a shard and checks it two ways
(`runs/demo/`):

```
stageB: k=4 radius=0.016 |P|max=0.483      dump: M=212 W=4, 32,857 entries, verdict 0 (no pattern)
atlas_radius (fine.bin record 0) = 0.015991855587698802   pass_radius (batch radius) = 0.016
cross-check vs m1/runs/g0.txt (independent probe dump): equivalent, not byte-identical
  decode every eight-byte hex group of the dump as big-endian; symmetric on all 22,366
  unordered O/U pairs; exhaustive backtracking gives eight ball permutations (three
  interchangeable pairs), with every map verified on all 44,732 ordered pairs;
  one explicit permutation and the full enumeration are SHA-256-pinned by the audit
  (the raw byte strings differ because of encoding and ball order)
canonicalised: ball permutation is nontrivial
validate_record: 0 errors
binary round trip: 49,113 bytes; text: 421,700 bytes (8.59x)
record 49,033 B = hdr 64 + stageB 1,508 + balls 11,872 + excl 22,021 + adj 13,568
```

Three things this establishes: (i) the instrumented build agrees with an independent dump as a
labelled O/U relation, after decoding its big-endian print format and applying the explicit ball
permutation (and all five probed per-record fields match the lead's log in 256/256 records);
(ii) the canonical order is a real constraint (the permutation is non-trivial, so without R11 the
bitsets would be uncomparable); (iii) the exclusion block of 22,021 B (5,592 bitmap + 16,429 codes)
reproduces the 13,568 B adjacency exactly — the `E_ADJ_EXCL` consistency the schema requires is
what the producer's `pairtest` guarantees. This is a graph-representation check, not an exact
verification of the geometric non-edge predicates or of the completed graph search.

**What the archive cannot do:** there is no ball radius, no ball list and no per-record verdict in
`batches/*.bin` — `cluster()` keeps `s` local and `saveRecords` writes only the 8 numbers
(`atlas.cpp:191-201`), so today the only honest v1 records are mode **R** (the checker rebuilds the
ball family, the graph and the search) or the instrumented-dump reconstruction used here. The
fields R8/R11 add (`s`, the ball list, the canonical order, the verdict, `steps_used`) are exactly
what D1/D2 of A identified as missing; this document adds only their encoding and their measured
size.

---

## 9. Mutation suite

`python3 src/mutations.py runs/demo/stagec-initial-0000.scv runs/mutations.out` → **47/47 refused
with the expected code** (≈25 s). Classes:

| class | examples | codes |
|---|---|---|
| container / canonical form | magic, version, body-hash flip, truncation, `len` off by one, reserved ≠ 0 | `E_MAGIC E_VERSION E_BODY_HASH E_LEN E_RESERVED` |
| ball layer | `s = 0.1`, `|v| > 2`, two balls swapped or duplicated | `E_S_BOUNDS E_V_BOUNDS E_BALL_ORDER` |
| adjacency | diagonal bit, asymmetric bit, bit ≥ M, size | `E_DIAG E_ASYM E_HIGHBIT E_ADJ_SIZE` |
| evidence ↔ graph | exclusion dropped (cache keeps the edge), cache edge dropped (evidence keeps the exclusion), `n_excl` off by one, code 6 | `E_ADJ_EXCL E_EXCL_COUNT E_EXCL_REL` |
| modes / reserved | `FLAG_Y`, `cover_mode = 2`, ball hint without `FLAG_BALLS`, mode R carrying exclusions | `E_Y_RESERVED E_COVER E_BALLS_FLAG E_EXCL_EMPTY` |
| verdict consistency | `NEG` with `steps > cap`, `CAP` without exceeding the cap, `EMPTY_BINS` with balls, `POS` without labels, `POS` with a pattern that is not in the graph, `k` mismatch | `E_CAP E_EMPTY E_POS_LABELS E_POS_EDGE E_K_MISMATCH E_PARENT` |
| manifest | bare float, unsorted keys, duplicate key, int > 2^53, trailing blank line | `E_MANIFEST_FLOAT E_MANIFEST_CANON E_MANIFEST_DUP E_MANIFEST_INT53` |
| coverage / partition | record missing, record duplicated, record in the wrong part | `E_COV_MISSING E_COV_DUP E_COV_PART` |
| composition (cover) | unresolved parent with no block or an extra parent, child not excluded, degree mismatch, duplicate incidence, `created+inherited ≠ degree`, `inside` ≠ the metric's constant | `E_COVER_MISSING E_COVER_CHILD_STATE E_COVER_DEGREE E_COVER_ORDER E_COVER_CREATION E_COVER_COUNTERS` |
| radius roles | `atlas_radius > pass_radius` | `E_RADIUS_ORDER` |

and the three roll-up outcomes on real bytes (`src/outcome_demo.py`): one real `NEG` record →
`accept`; the same record with `verdict = CAP` → `unresolved`; radius 0.1 → `reject`; a 2-record
input with 1 record present → `reject` (`E_COV_MISSING`).

Two classes were added after the first review, because the schema had no place for them: the
**two radius roles** (`atlas_radius` above `pass_radius` → `E_RADIUS_ORDER`) and the
**composition block** (unresolved parent with no block → `E_COVER_MISSING`; a covering child that is
not excluded → `E_COVER_CHILD_STATE`; `degree` mismatch → `E_COVER_DEGREE`; duplicate incidence →
`E_COVER_ORDER`; `created+inherited ≠ degree` → `E_COVER_CREATION`; `inside` differing from the
metric's constant → `E_COVER_COUNTERS`; a parent that is not unresolved → `E_COVER_MISSING`).
The real block (`runs/composition.bin`, 57,104 B) passes the internal half of these checks with
163/1,127/11,838/10,711.

---

## 10. What is NOT verified here

* **No mathematical predicate is re-implemented or re-derived in this direction.** Steps 3–4 of §5
  are obligations with a price, not code. `(6.23)`'s transcription (with `detail = 1`, the
  `fE/fB/fJ` rescaling and the `±3e-7`) is *not* audited here; that is d2/m5. The schema only fixes
  how a producer states the outcome and what field pins `detail`.
* **No exact/outward arithmetic was run.** The margin census of §7 reads the producer's binary64
  decision points; it bounds what an outward checker would decide, it does not implement it.
* **The census is one batch (256 records, 2.9 %).** The rule mix and margin decades are not
  established for the 163 cap-hit records or the 1,127 fallback records; the joint-entry count in
  the 7.0 GiB ESTIMATE is that extrapolation and is labelled as such.
* **No cover certificate.** `cover_mode = BOXCERT` is reserved and refused, deliberately: defining
  it before the monotone coverage argument exists would be speculative. Cover is a checker
  obligation throughout.
* **No Lean.** The schema's excluded/unresolved split is *aligned* with
  `work/04-lean/Mub6/StageCNecessity.lean` (its hypotheses `hV`, `hdiam`, `hO`, `hU`, `hpat` are
  exactly "ball family with diameter bound + over-approximating graphs + no pattern"), but nothing
  in the Lean file checks this format; the mapping is documentary.
* **`REF` records are implemented but not exercised on a full pass** — the demo has one record and
  cannot show a 22,379-record pass.
* **Timing is shared-VM timing.** One of the runs was contended by 2× wall; shares only.
* **No exact Stage-C run exists.** All CPU-hour figures in §5.2 are extrapolations from one
  binary64 batch plus a dot-product/solve-shaped kernel benchmark (m1's) — not from an exact
  bin-layer or clustering kernel. A cover certificate could change the model, and no run-wide
  lower bound is claimed.
* **The composition cover criterion is not re-derived here.** `check_composition` verifies the
  block's *structure and consistency*, not that the listed child balls cover the parent's box under
  `E = sqrt(1+ort)·R + 1e-7`; that arithmetic is m2's (`H0-stageC-coverage.md`), and their
  35–55 CPU-min re-derivation estimate is quoted, not reproduced. The real block's 11,838
  incidences come from their instrumented refiner, not from the archive.
* **The record-level half of `check_composition` is exercised only on a 4-record synthetic
  fixture** (the mutation cases), not on the 22,379 + 1,127-record passes: that needs a full
  certificate, which the archive cannot supply (§8). The real block is checked internally
  (sortedness, degrees, creation sums, counters) and against m2's counts, not against a built
  certificate.
* **`k` is parsed from the archive, `|O|`/`|U|`/`balls` from the lead's probe.** The two agree on
  the one record where both are known (`f0#0`), but the pairing of probe `index` (1-based) with the
  record stream was only spot-checked, on batch 0 and on the k = 0 record's position.
* The `params` section of `runs/coverage-plan.json` carries `RB` as the exact binary64 of `.042`
  (`0x1.5810624dd2f1bp-5`); the other parameter values are integers parsed by `atoi`, so the
  manifest's param record is exact — but I did not verify that the archived binaries parsed the
  same strings to the same values beyond the reproduction of `C.batch0.txt`.

---

## 11. Next steps that would actually change the H1 decision

1. **Adopt mode R as the shipped format** (35.0 MiB, no evidence layer) and treat mode W as an
   optional audit artefact; the measured cost of doing so is under 9 % of checker time and the
   saved bytes are 850 MiB. Then the interesting object becomes the *cover* certificate.
2. **Define `cover_mode = BOXCERT`** from d4's monotone/padding chain: per layer, a list of boxes
   in bin-index space with a rule tag and an outward margin, so that "no admissible vector was
   dropped" stops costing a full `N^5`-scale re-enumeration. With the composition layer (m2:
   35–55 CPU-min for 11,838 incidences), the cover obligations are where the checker's cost sits;
   the graph evidence is the cheap part. This is a model, not a measured floor.
3. **Freeze the two radii and the composition block** (R13, R14) — a certificate that stores one
   radius or one parent per record does not describe this run, whatever its Stage-C graphs say.
3. **Repeat §7's census** on the 163 cap-hit records (denser: O density 2.7×) and on a fallback
   sample; if any rule's min decade drops below the kernel's error budget, that rule (not the
   whole pipeline) needs the two-tier treatment.
4. **Freeze the verdict vocabulary and the coverage rules as the thing two implementations must
   agree on** (§3.4, §4): they are the only parts of the format where a wrong choice silently
   turns "unresolved" into "excluded".
5. If a producer ever ships mode W, add the one measured cross-check that is currently free: the
   adjacency cache must *equal* the graph rebuilt from the evidence (`E_ADJ_EXCL`), which is what
   catches a producer whose two layers disagree.
