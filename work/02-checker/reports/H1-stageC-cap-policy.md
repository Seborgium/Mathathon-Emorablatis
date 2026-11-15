# H0 / Stage C: the search cap is a false economy — cap policy and what it deletes from the certificate

Direction d7 (member m4), swarm `smwgx104w`. Object: the **cap parameter** `capSteps` and its
downstream consequences, not the schema. All inputs are measurements made by other members or by
me; **no new execution was run** for this note (`src/cap_policy.py` is arithmetic on those files).

Artefacts: `src/cap_policy.py`, `runs/cap_policy.json` (every number below), plus the appendix
correction to the v1 files.

---

## 0. Bottom line

1. **The 163 cap hits are the only reason the certificate has a second pass.** They are 0.73 % of
   the 22,379 initial records, and they force (i) a Stage-B re-refinement into 1,127 fallback
   records, (ii) 163 unresolved parents, (iii) the **11,838-incidence composition cover** that
   soundness needs for those parents, and (iv) the one *external* hypothesis that Stage C cannot
   check (that the children cover the parents).
2. **Raising `capSteps` from 5·10⁶ to 10⁸ completes every one of them.** Measured (m1,
   `probe_hard*.txt`, cap raised to 2·10⁸): max **39,968,282** steps, total **1,925,134,199**,
   **68.2 s** single-threaded, `gaveup = 0`, `positive = 0`. A cap of 10⁸ leaves **60,031,718**
   steps of headroom (2.5×); 4·10⁷ would leave only **31,718** (0.08 %) and is not a safe choice.
3. **What that deletes:** the 1,127-record fallback pass, the 163 unresolved parents, the
   composition block (**57,104 B**), and the **fallback** cover obligation — 11,838 incidences
   over **515,243 inside cells**, which m2 measure at **5.49 CPU-s** to re-derive (their
   instrumented refiner, `brun-cov`). It does **not** delete the upstream Stage-A/B cover: the 163
   records remain records of the initial certificate and need the same Bmid/Bfine cover evidence as
   the other 22,216, so **321,004,555 of m2's 321,519,798 inside-cell obligations remain**. m2's
   **35–55 CPU-min** is the price of that whole layer, not of the fallback part.
4. **The one-pass certificate is a *proposed* path, not a completed one.** Today the archived
   fallback pass and its many-to-many map are the baseline; the cap headroom below is a
   measurement at cap 2·10⁸, and the high-cap run itself has not been performed. Nothing here
   closes the mid/fine cover obligations either — they are upstream of the cap and unaffected.
5. **What it costs:** +1,110,134,036 search steps = **+39.3 s** single-threaded (at the measured
   35.4 ns/step), against **126.2 s** of Stage-C fallback-pass work (1,127 × 0.112 s, measured
   per-record rate) and 4.93 s of Stage-B re-refinement (m2) — i.e. **net ≈ 92 s saved**, and a
   cheaper checker: pairs 622,704,036 → **617,899,097**, evidence entries 888,217,019 →
   **880,354,276**.
6. **Bytes:** the certificate *shrinks* by **14,056,421 B (−13.4 MiB)**: the 163 dense records
   cost less than the 1,127 fallback records that replace them, and the composition block goes
   to zero.
7. The cap is a **producer parameter, not a certificate field**: the format already records
   `cap_steps` and `steps_used` per record, so a raised-cap run is representable without any
   schema change, and `EXCLUDED ⇒ steps_used ≤ cap_steps` (already an enforced identity) is what
   makes the safety auditable per record.

---

## 1. Measurements used, and their provenance

| quantity | value | source |
|---|---|---|
| initial records / cap hits | 22,379 / 163 | `certdata/runs/h0-stagec-probe.json` (`category`) |
| steps burned by the 163 at the 5·10⁶ cap | 815,000,163 (= 163 × 5,000,001) | census |
| steps the same 163 need with the cap raised | total 1,925,134,199, max 39,968,282, 68.2 s | m1, `probe_hard.txt` + `probe_hard2.txt` (all 163 re-run at cap 2·10⁸; `gaveup = positive = 0`) |
| Stage-C per-record cost | 0.112 s/record | my instrumented batch (256 records), agreeing with m1's 0.117 s |
| Stage-B fallback re-refinement | 4.93 s | m2, `H0-stageC-coverage.md` §0.3 (byte-identical `fb1.bin`) |
| composition cover | 163 parents, 1,127 children, 11,838 incidences, 10,711 inherited | m2, recovered map |
| cover re-derivation cost, **whole layer** (Bmid+Bfine+fallback, 321,519,798 inside cells) | 35–55 CPU-min | m2 §0.5 |
| cover re-derivation cost of the **fallback** part only (515,243 cells) | **5.49 CPU-s** | m2 §6 (`brun-cov`, with the 17,207 snaps) |
| fallback records' certificate cost | see §2 | census (M, \|O\|, \|U\| per record) |

The 163 records' `|O|` and `|U|` are **complete even when the search is capped**: `graph::init()`
builds the whole adjacency matrix before the search starts (`stageC.cpp:400-405`), so the
per-pair exclusion evidence of a capped record is exactly the evidence it would carry after the
cap is raised. Only `steps_used` and the verdict change.

---

## 2. The arithmetic

Certificate sizes use the v1 payload formula of `H0-stageC-schema.md` §6 (stage-B `356+288k`,
56 B/ball, `ceil(2P/8) + ceil(4E/8)` for the evidence with `E = 2P − |O| − |U|`), computed
per record from the census; `k = 4` for every record involved here (`fine.bin` and `fb1.bin`
both parsed for their actual k, §Appendix).

| | today (cap 5·10⁶) | cap ≥ 4·10⁷ | delta |
|---|---|---|---|
| records | 23,343 (22,216 initial + 1,127 fallback) | 22,379 (one pass) | **−964** |
| passes | 2 | 1 | −1 |
| unresolved records | 163 → covered by 1,127 children | **0** | −163 |
| payload bytes | 926,657,563 | 912,658,246 | **−14,056,421** |
| composition block | 57,104 B | 0 | −57,104 |
| **fallback** cover obligation | 11,838 incidences, 515,243 inside cells, 5.49 CPU-s (m2) | none | removed |
| upstream Stage-A/B cover (unchanged) | 321,004,555 inside cells | 321,004,555 inside cells | 0 |
| m2's whole-layer estimate | 35–55 CPU-min for 321,519,798 cells | 35–55 CPU-min, re-scoped to 321,004,555 cells | ≈ unchanged |
| pair tests the checker runs | 622,704,036 | 617,899,097 | −4,804,939 |
| evidence entries | 888,217,019 | 880,354,276 | −7,862,743 |
| producer search seconds | 815,000,163 steps at the cap, then 126.2 s of fallback work | 1,925,134,199 steps ≈ 68.2 s | **≈ −92 s** |

Why the capped records are not the expensive ones: the 163 are *denser* (m1: O density 14.5–30.3 %,
median 25.0 %, balls 260–1,089) than the 1,127 fallback records they replace (radius `.011`, and
their graph is built at the same cost per pair but there are 4.8 M more pairs).

---

## 3. Recommendation

For any **re-generated** Stage C:

1. Set `capSteps = 10⁸` (2.5× headroom over the measured maximum) and **drop the fallback pass**.
   Do not use 4·10⁷: 0.08 % headroom is not a margin, it is a coincidence of this input family.
2. Keep the fallback machinery in the producer but expect it to produce nothing: the certificate
   should still be *able* to express a second pass (`passes`, composition block) because the cap
   is a budget, not a proof, and a future input may exceed any chosen cap.
3. Record `cap_steps` per record as the format already requires. The checker's obligation then
   stays exactly what it is today — `EXCLUDED` requires `steps_used ≤ cap_steps` and a completed
   search — so a raised cap changes no verification rule, only the amount of work.
4. This is a *measured* recommendation for this input family: the maximum is a property of the
   22,379 records of this run, not a bound on the method. It is also cheap to revisit: a single
   run at the new cap reproduces the whole census in ≈44 CPU-min.

### 3.1 Safeguards and scope, stated so this cannot be over-read

* **Baseline stays the archive.** The installed, currently completed certificate is the 23,343-record
  two-pass set with the 1,127-record fallback and the 11,838-incidence many-to-many map; nothing
  below replaces it. The cap = 10⁸ run is an *alternate* that has not been executed.
* **Required safeguards if the alternate is adopted:** `capSteps ≥ max_measured_steps + 1` (so
  10⁸ against 39,968,282 measured); **zero cap-hit records** in the produced pass, checked from the
  census, not assumed; and the conditional caveat below.
* **What it cannot delete:** the Stage-A/B cover of the 163 records into the initial certificate
  (Bmid/Bfine, 321,004,555 inside cells) still has to be certified, and the mid/fine stages still
  have to run. Only the fallback layer — 515,243 cells, 0.16 % of the whole cover obligation —
  and its 11,838 incidences go away.

**Caveat that must travel with the number.** m1's raised-cap run is a *second execution* of the
same deterministic code on the same inputs; the lead's baseline treats it as a different execution
and refuses to substitute it silently. Nothing here depends on that substitution: the claim is
conditional — *if* the 163 records are run at cap ≥ 39,968,283, *then* they complete, and then the
fallback pass and the composition layer are unnecessary. If a re-run's step counts differ from
m1's, the policy conclusion changes only in the cap value, not in the structure.

---

## 4. What this direction did **not** do

* No new Stage-C execution: the row "cap ≥ 4·10⁷" is arithmetic on the census and m1's raised-cap
  run. I did not re-run the 163 records myself, and I did not verify m1's step counts
  independently — they are quoted with their file and their own fidelity check
  (output-identical counters on the batches they re-ran).
* No claim that a higher cap is always better: a cap exists so that a pathological record cannot
  hang the producer; the recommendation is to set it above the measured maximum *and* to keep the
  fallback path in the producer for the case where it still fires.
* No change to any soundness argument: the cap never was a soundness device (a cap hit is
  unresolved, `stageC.cpp:483-487`), and removing the cap hits removes *obligations*, not
  guarantees.

---

## Appendix — correction to the v1 composition block (counter semantics)

The v1 files in this directory carried a mislabelled counter; this fixes it and records the
semantics from the source.

* `stageB.cpp:37` declares `statsB {parents, base, inside, live, splits, snaps, badSnap, fails,
  pairTry, pairs, pairMarks}`. `st.live++` at `:170` counts **cells visited** (not outside, not
  already excluded); `st.snaps++` at `:175` counts **cells that reach a Hadamard snap attempt**.
  For the fallback pass the producer prints `parent163 base2386483 inside515243 live17207 split0
  snaps17207 bad0 fail0` (m2 §6 line 283, reproduced by their instrumented copy in 5.49 s CPU):
  the two operation counts happen to coincide here, and both are three orders above the 7
  snap-*closed* cells, which is the confusion this correction removes.
* m2's per-parent `inside_cells` and `marks` are **cell classifications**: `inside = 3,161` per
  parent, `marks = relation_marks`, and `515,243 = 515,236 + 7` over the run, so exactly **7 cells**
  in the whole pass were closed by the snap path rather than by a relation mark.
* The block therefore now packs, per parent, `relation_marks` **and** `snap_closed_cells` as two
  `u32`s (32 B/parent, was 28) with the enforced identity
  `inside = relation_marks + snap_closed_cells`; the producer's `snaps`/`live` are **not encoded**
  (a checker cannot verify an operation count from cells, and the 7 is not 17,207).
  Block size 57,104 B = 28 + 32·163 + 4·1,127 + 4·11,838. Validator identities:
  `inside = relation_marks + snap_closed_cells ≤ cells_total`, `fail = 0`, `snap_closed_cells ≤
  inside`, plus the previous degree/creation/counter rules.
* Regenerated: `runs/composition.bin`/`.txt` (sha changed), `runs/composition.json`
  (`snap_closed_cells` total 7, `relation_marks` total 515,236, identity holds), the mutation suite
  now **47/47** (one new case: `inside ≠ relation_marks + snap_closed_cells` →
  `E_COVER_COUNTERS`), and `runs/size_accounting.json` totals shift by +652 B.
