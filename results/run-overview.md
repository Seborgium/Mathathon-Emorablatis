# Run overview — dimension-six MUB proof: accessibility and accuracy programme

Manager-level. Status at the end of the first two waves. Detail lives in `work/00-lead/decisions.md`
(decision log), `work/00-lead/gates.md` (gate ledger) and each stream's `README.md`.

---

## 1. Bottom line

1. **The technical work succeeded beyond the plan in two places and failed in one.** The preprint's
   parameter choices are now justified (N = 112 in particular), the assembly of its proof has been
   formalised as an equivalence rather than an implication, and the seed cover has been reproduced
   **byte-for-byte** against the published record. What has *not* happened is the thing originally
   asked for: there is no accessible preprint yet.
2. **Two premises changed under the project, both for the better.** The authors' code is public, and
   an independent proof of the same theorem now exists (arXiv:2611.06917, 4 Nov 2026). The paper we
   are working on is no longer the only evidence for its own headline claim.
3. **The largest error in the run was mine**, not a team's: I published four "verified errata" about
   the paper that were all false, caused by reading extracted text instead of rendered pages. They
   are retracted, and a binding rule now prevents a recurrence.
4. **Decision needed:** whether the deliverable is a verification report on this proof plus the
   independent one, or a standalone exposition of this proof alone. That decision gates the writing
   stream, which is the only stream that produces the requested artefact.

---

## 2. What was asked, and what exists

| asked for | state | where |
|---|---|---|
| a summary of the proof | delivered | `results/proof-summary.md` |
| every claim restated and classified | delivered | `results/proof-claims.md`, `work/01-catalogue/claims.yaml` (91 nodes, 178 edges) |
| a code audit | **partly** — the code was located and built; a byte-exact reproduction was achieved; no full source audit yet | `work/10-recreate/` |
| areas for improvement, stated as gap → action | delivered | `results/improvements.md` |
| a plan with teams, files, command structure | delivered and executed | `results/plan.md`, `work/*/README.md` |
| parameter justification (N = 112 etc.) | delivered | `work/05-parameters/` |
| formalisation (scoped) | delivered with named holes | `work/04-lean/` (22 modules) |
| quantum framing and honest status | delivered | `work/07-quantum/` |
| **one accessible preprint** | **not started** | `work/08-paper/` (empty) |

---

## 3. Two work streams are running

**Stream A — the four swarms I launched and judged.** 19 members across four teams: catalogue,
parameters, quantum framing, formalisation. 20 verdicts issued, **17 accepted**, 3 rejected and all
3 recovered on a second attempt. All four swarms ended solved.

**Stream B — the recreation programme.** Present on disk, run in parallel, not mine:
`work/10-recreate/` (667 files), three further swarms live (13 members: coding, harness, critics),
a frozen-contract spec, and a gate ladder G-R0…G-R5. Its baseline finding is the strongest evidence
in the project:

- the upstream sources build on this VM (gcc 16.2.0, both ABI probes pass);
- **upstream `covrun` reproduces the recorded `centers.txt` byte-for-byte** — sha256 `c48bc9a2…`,
  7,339,546 bytes, 402 s — matching Table 2 of the paper;
- upstream `arun` part 0: 21.5 ms/centre, `failedBalls 0` on the first 200 recorded centres.

The two streams intersect but are not yet joined: Stream A justifies parameters analytically, Stream B
can measure them; Stream A formalised the assembly, Stream B holds the code the assembly is about.
**Joining them is the main integration task remaining.**

---

## 4. Deliverables on disk

| location | files | what it is |
|---|---|---|
| `results/` | 6 | the five documents above plus `recreate-code-plan.md` (Stream B) |
| `work/01-catalogue/` | 33 | claim inventory (91 nodes), dependency graph, notation table, reader path, audit report, S-claim ledger, reconciliation diff |
| `work/05-parameters/` | 108 | constraint/slack/cost table over ~40 constants, N = 112 argument, paste-ready handoff, 44 scripts, 16 CSVs |
| `work/04-lean/` | 54 | 22 Lean modules, 17 reports, fidelity and status tables, 23 declared holes |
| `work/07-quantum/` | 9 | physical framing, status paragraphs, comparison with prior work, bibliography |
| `work/10-recreate/` | 667 | spec, harness, source units, logs, gate ledger (Stream B) |
| `work/02,03,06,08,09-*` | 5 | skeleton only — checker, reference implementation, figures, paper, red team: **not launched** |
| `.ultramath/` | 7 swarms | boards, transcripts, per-member directories |

Total: 879 files under `work/`, 22 Lean files, 58 Python files.

---

## 5. What succeeded — ranked by how much it changes the paper

1. **The seed cover is reproducible.** Byte-exact `centers.txt` from a from-scratch build of the
   published sources. This converts "a run was reported" into "a run can be repeated here", which is
   the single largest reduction in trust base the project achieved.
2. **N = 112 is justified, and not by the paper's reason.** The paper's stated 32-bit argument is
   inert (it permits 189 and the code uses 64-bit counters). The real constraints are: coverage gives
   N ≥ 47; `int8_t` bin differences give N ≤ 128; the reuse reach gives N ≥ 110; and `testBucket`
   hardwires 112, so the *printed* pipeline is sound only for N ≥ 112. 112 is the left endpoint of
   the window it is itself consistent with. Three members reached this independently.
3. **The paper's assembly is an equivalence, not an implication.** Theorem 1.1 = six stage
   statements + §7.2's terminal conditions, formalised with "up to equivalence" absorbed by class
   membership. This exposed that **Theorem 7.1 needs a driver hypothesis it does not state** — the
   formal version takes seven coverage facts and no bookkeeping condition.
4. **Three parameter defects are confirmed and quantified**: the Stage-C clustering cutoff is inert
   on three of four grids (no merge possible for M ≤ 50); the root dimension is k ≤ 5, 5, 7 at the
   three widths, not the stated 10; and the sentinel `100` lies inside the legitimate range.
5. **Table 1's "pairs" count is undefined**, and three independent replays agree: one reproduces the
   paper's 22,829 X-lists exactly, after which the Y side admits at most 112,160,350 pairs against
   the printed 151,744,086.
6. **Lemma 5.1 was in dispute between two members and is true as printed.** Adjudicated by
   derivation and by a compiling Lean proof; the contrary claim was retracted.
7. **An independent proof now exists** (arXiv:2611.06917), with a certificate-and-interval-arithmetic
   architecture — which is precisely the recommendation this project made in its first week.

---

## 6. What failed, and what it cost

### Mine, and the most serious of the run
I reported **four verified errata in the preprint — all four were wrong.** The paper is correct in
every one of those places (Lemma 4.4's √8, (3.24)'s 63, (4.29)'s bracket, (6.3)'s √2π/3). Cause: I
checked `pdftotext` output, which drops radicals drawn on the line above a fraction, despite two
members having flagged exactly this trap earlier in the same round. Corrected in the decision log
with a binding rule: no formula-level claim without a rendered-page check. One team member caught it;
without that, a list of four false errata would have gone into a document about someone else's paper.

### Earlier corrections to my own analysis
"Every margin clears its error by 2–3 orders" — wrong; the tightest is 1.25×. The Stage-C no-merge
threshold is M ≤ 50, not 24. The N-window is [47,128], not [47,189]. Each was corrected within the
run by a team, and each is on the record.

### Team failures — three rejections, all recovered
- A member submitted another member's three files as its own, with two new claims that were wrong (a
  false "reuse ceiling" and a circular cost model). Rejected; it returned to its own direction and
  produced a valid conditioning analysis.
- A duplicate parallel claim inventory, plus a false "the problem is still open". Rejected; it
  returned with the reconciliation diff that caught my errata.
- A "Lemma 5.1 is FALSE" headline backed by a witness that violated the lemma's hypothesis. Rejected;
  the retraction is verified in three places.

### Process failures
- **Redundancy.** Five members of the parameters team produced substantially the same constant table
  under five different filename suffixes. Registering distinct *directions* did not prevent four
  people building the same *deliverable*. This is the largest waste in the run.
- **File collisions.** Two members overwrote files owned by others (`handoff-1.md`,
  `Assembly.lean`). Both self-reported; the single-writer rule needs enforcement, not just statement.
- **Duplicated proofs.** Lemma 2.5 is proved in one module and still `sorry` in another, so the hole
  count is pessimistic where a proof exists.
- **The original goal is unstarted.** No accessible paper, no figures, no checker, no red team. The
  run produced raw material of good quality and has not yet produced the artefact requested.

---

## 7. Open risks

| risk | severity | note |
|---|---|---|
| Two streams diverge (Stream A's analyses vs Stream B's frozen spec) | high | join at G-R0; the spec must cite the parameter findings |
| The paper's framing is now wrong about its own status | high | "the only proof" and "resolves the conjecture" are both untenable since 4 Nov |
| Formalisation overstated in the write-up | medium | 23 holes, §5 unstated; the status table must print both |
| Formula-level claims made from extracted text | medium | recurred once already; now a standing red-team item |
| Stream B unowned by this session | medium | 13 members, 3 live swarms; its gates are not in `work/00-lead/gates.md` |

---

## 8. Decisions requested

1. **Deliverable shape.** Verification report on this proof *plus* the independent one, or standalone
   exposition of this proof? Recommended: the former, with the accessibility layer (reader path and
   figures) preserved. This decides `work/08-paper/`.
2. **Integration gate.** Freeze Stream B's spec and require it to consume Stream A's parameter
   findings, so the code and the justification do not drift.
3. **Next staffing.** Recommended order: red team on the inventory and the errata record first (cheap,
   and it has already paid twice); then figures and paper once framing is fixed; then the checker,
   built against the frozen spec rather than in parallel with it.
