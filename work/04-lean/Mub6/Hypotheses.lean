/-
Mub6/Hypotheses.lean — code-dependence made explicit.

Purpose (T4 phase 0, "statements and fidelity"): `results/proof-claims.md` tags every
load-bearing claim with a status.  Two of those tags are claims about *the authors' code*, which is
not in the packet:

  **S**  a claim about what a named routine does (evidence: the source, absent);
  **C**  a claim that a particular finite execution succeeded (an event, not a mathematical
         condition).

The project rule ("Nothing unmarked", `results/plan.md` §2.3) is that such a claim must appear as
an *explicit hypothesis* of the theorem that uses it, never as a proved fact.  This file is the
single place where those hypotheses are given names and types, so that

  * any theorem can take them as binders (`(hc : CodeClaims)`, `(hterm : TerminalConditions r)`),
  * `reports/statements.md` can point at a *field name* instead of quoting prose,
  * a reader can see, in one screen, what the formal statement of Theorem 7.1 actually assumes.

Nothing here is asserted: every field of `CodeClaims` is a hypothesis, and every field of
`RunReport` is data a run must supply.

Paper locators: §2 (covout, seeds::mk, sumok, extend, supdual), §3 (buildH::gen, eq,
trial::pass, trial::certificate, Asearch::testA), §4 (buildH::patch, Candidate::prep),
§6 (graph::exist), §7.2 (the five terminal conditions), §7.5 (Table 1).
-/
import Mathlib

namespace Mub6

/-! ### §7.2 terminal conditions, as data

Theorem 7.1 is conditional on the invocation list of §7.2 meeting all of its terminal conditions.
Those conditions are pure bookkeeping about the *outputs* of a run: exit statuses, counts of
records in named lists, digest checks, and a partition identity.  We type them here so that the
`C`-hypothesis of Theorem 7.1 is an object, not a sentence. -/

/-- The bookkeeping part of a completed run, as reported by the programs of §7.2. -/
structure RunReport where
  /-- exit status of the four Stage-A shards `A0 … A3` (§7.5: all exit 0) -/
  aExit : Fin 4 → ℤ
  /-- sizes of the four Stage-A bad lists (§7.5: all empty) -/
  aBad : Fin 4 → ℕ
  /-- exit status of the two Stage-B invocations (B mid, B fine) -/
  bExit : Fin 2 → ℤ
  /-- sizes of the two Stage-B bad lists (§7.5: both zero) -/
  bBad : Fin 2 → ℕ
  /-- records written by the initial Stage-C batch -/
  initialCBatches : ℕ
  /-- initial Stage-C records whose graph search exhausted its work cap -/
  graphCapFailures : ℕ
  /-- records handed to the fallback Stage-B invocation -/
  fallbackInput : ℕ
  /-- records emitted by the four final Stage-C shards -/
  finalC : Fin 4 → ℕ
  /-- records left unresolved at the end (§7.5: none) -/
  unresolved : ℕ
  /-- provenance and batch-digest checks all passed -/
  provenanceOk : Bool
  /-- the fallback input includes every initial failure (subsequence check) -/
  fallbackCoversFailures : Bool

open scoped BigOperators in
/-- **The terminal conditions of §7.2**, in the order the paper numbers them.

  1. normal builds and a complete centre file (no A shard fails, no bad A record);
  2. four A exits 0 with empty bad lists;
  3. two B exits 0 with zero-count bad lists;
  4. each initial C batch processed once with consistent counts;
  5. the fallback covers every initial failure, and the four final C shards partition the
     fallback records.

The bookkeeping claims of (4) that concern *which* records were processed are not expressible
without the record identities (an `S` claim about the driver); what is expressible, and is what
Theorem 7.1's proof consumes, is the counting identity in (5) together with
`unresolved = 0` and the provenance flags. -/
def TerminalConditions (r : RunReport) : Prop :=
  (∀ i, r.aExit i = 0) ∧ (∀ i, r.aBad i = 0) ∧
  (∀ i, r.bExit i = 0) ∧ (∀ i, r.bBad i = 0) ∧
  r.provenanceOk = true ∧ r.fallbackCoversFailures = true ∧
  r.unresolved = 0 ∧
  (∑ i, r.finalC i) = r.fallbackInput ∧
  r.graphCapFailures ≤ r.fallbackInput

/-- §7.5, Table 1: the published counts are mutually consistent — the four A shards sum to the
centre count, the four coarse-record counts sum to the B-mid input, the fine-B batches are
`87 · 256 + 107`, and the four final-C shards partition the 1127 fallback records.
(`E`-status data, checked arithmetically; this checks the bookkeeping, not the run.) -/
theorem table1_consistent :
    (62470 + 62470 + 62469 + 62469 = 249878) ∧
    (764 + 774 + 757 + 788 = 3083) ∧
    (87 * 256 + 107 = 22379) ∧
    (282 + 282 + 282 + 281 = 1127) := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> norm_num

/-- The Table-1 report satisfies the terminal conditions except for the parts that Table 1 does
not print (provenance flags, bad-list sizes, exit statuses).  This is a *shape* check: it shows
that `TerminalConditions` is satisfiable by the published counts, not that the run satisfied it. -/
theorem table1_has_terminal_shape :
    TerminalConditions
      { aExit := fun _ => 0, aBad := fun _ => 0, bExit := fun _ => 0, bBad := fun _ => 0,
        initialCBatches := 22379, graphCapFailures := 163, fallbackInput := 1127,
        finalC := fun i => if i = 0 then 282 else if i = 1 then 282 else if i = 2 then 282 else 281,
        unresolved := 0, provenanceOk := true, fallbackCoversFailures := true } := by
  refine ⟨fun _ => rfl, fun _ => rfl, fun _ => rfl, fun _ => rfl, rfl, rfl, rfl, ?_, by norm_num⟩
  decide

/-! ### The `S` claims, as named hypotheses

Each field is one claim about the behaviour of a named routine, with the locator and the reason it
is needed.  A theorem that consumes the claim takes this structure as a binder; the field name is
then the citation used by `reports/statements.md`. -/

/-- The code-behaviour hypotheses of §§2–6 and §7.2 (`S` and `S + M?` tags in
`results/proof-claims.md`).  Every field is a hypothesis: none is proved, and none can be proved
from the material in the packet, because the seven source files are not available. -/
structure CodeClaims where
  /-- §2, `covout` (`S`): the seed traversal visits every nondecreasing bin tuple
  `a ≤ b ≤ c ≤ d ≤ l < N` of the five varying seed phases.  Consumed by Prop. 2.10. -/
  covout_visits_all_tuples : Prop
  /-- §2, `seeds::mk` (`S`): the selected column is the first minimiser of `|2 b_s + 1 − N|`, and
  the invented Y bin ordering is the one of Lemma 2.4.  Consumed by Lemma 2.6 and Prop. 2.10. -/
  seeds_mk_selection_rule : Prop
  /-- §2, `sumok` (`S`): the vanishing-sum filter is evaluated only in the residual direction and
  in directions perpendicular to the five exponential columns.  Sound because (2.11) is required
  for all `v`; consumed by Prop. 2.10. -/
  sumok_restricted_directions_sound : Prop
  /-- §2, `extend` (`S`): the interval intersection is performed with outward margins and drops
  only divisors `< 10⁻⁶`.  Omitting a constraint only enlarges, so this is sound; consumed by
  Lemma 2.8. -/
  extend_dropping_sound : Prop
  /-- §2, `supdual` (`S`): proposals are accepted only with entries `≤ 10⁴` in modulus, and (2.19)
  is evaluated with `1.251π/N` in place of `1.25π/N`.  Consumed by Lemma 2.9 / Prop. 2.10. -/
  supdual_margins_sound : Prop
  /-- §3, `buildH::gen`, `eq` (`S`): the residual, its derivative, and exactly the twenty
  equations of (3.28) are assembled.  Consumed by Lemmas 3.7, 3.9. -/
  stageA_system_matches_equations : Prop
  /-- §3, `trial::certificate` (`S`): an exclusion is issued only after a finiteness check, a
  division by the largest coordinate, and use of the negative part of `y_D` — exactly the
  guarantee that Corollary 3.10 needs.  Consumed by Prop. 3.11. -/
  stageA_certificate_is_necessary_test : Prop
  /-- §3, `Asearch::testA` (`S`): the recursion terminates with zero unresolved cells, and every
  terminal cell is either excluded by a certified necessary test or covered by a certified phase
  ball.  Consumed by Prop. 3.11. -/
  stageA_terminates_fully_resolved : Prop
  /-- §3/§4, dead code (`S`): `Usearch::test` and the "scalar routines" supply no exclusions in
  this run, so the used certificate path is `Asearch::testA` alone. -/
  stageA_unused_routines_supply_nothing : Prop
  /-- §4, `buildH::patch` (`S + C`): a successful patch certifies (4.4), (4.15) and a valid `C`,
  hence produces certified Root data.  Consumed by Props. 4.5, 4.16. -/
  patch_certifies_root_data : Prop
  /-- §4, `Candidate::prep` (`M + S`): the stored centre and support representation holds with
  `‖ε‖ ≤ 2·10⁻⁶`.  Consumed by Lemma 4.10. -/
  candidate_prep_represents_stored_centre : Prop
  /-- §4/§5, the completion search processes every seed (`S + C`): no failed and no unresolved
  seed.  Consumed by Prop. 4.16 and, after Stage B, by Prop. 5.7. -/
  completion_search_processes_all_seeds : Prop
  /-- §5, the search protocol of Lemma 5.4 (`S`): a returned threshold `ρ > 10⁻⁷` certifies the
  implication `‖η − η_q‖ ≤ ρ → [e(P+δ)] ∈ S(Q,a)` from a single stored trial. -/
  stageB_threshold_protocol : Prop
  /-- §5, §7.5 (`S + C`): Stage B completes with no bad parents, so the `B` list of (5.26) is
  empty in both invocations.  Consumed by Cor. 5.8. -/
  stageB_no_bad_parents : Prop
  /-- §6, `graph::exist` (`S + M?`): returning `false` certifies that no configuration (6.24)
  exists; work-cap exhaustion never yields a negative certificate.  Consumed by Prop. 6.9. -/
  graph_search_false_is_a_certificate : Prop
  /-- §6, `graph::exist` (`S`): the clustering of Lemma 6.4 is complete, every retained bin has a
  centre, integer lift and radius, and a failed clustering is reported as unresolved rather than
  negative.  Consumed by Prop. 6.9. -/
  stageC_clustering_complete : Prop
  /-- §6, the negative paths of Stage C (`S`): only an empty completed bin layer or a completed
  negative graph search is reported as negative; overflow, clustering failure, a surviving graph
  possibility and work-cap exhaustion are all unresolved.  Consumed by Prop. 6.9. -/
  stageC_negative_paths_only : Prop
  /-- §7.2, the driver (`S`): each initial C batch is processed exactly once with consistent
  counts, and the record identities used by the proof (marker entries, done counts, subsequence
  and fallback-input checks) are actually checked by the programs. -/
  driver_bookkeeping_identifies_records : Prop

end Mub6
