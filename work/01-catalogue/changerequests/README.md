# Change requests against the frozen claim inventory

`claims.yaml`, `dependencies.dot`, `notation.tex`, `style.md` and `reader-path.md` were frozen at gate
**G0**. No team edits them after G0, including T1. If you believe an entry is wrong, incomplete or
missing, write a file here and the lead arbitrates in `work/00-lead/decisions.md`.

## Protocol

1. **One file per team**: `work/01-catalogue/changerequests/<team>.md` (e.g. `T2-checker.md`). Append
   new items at the top; do not rewrite other teams' sections. A team with many items may add
   `<team>-<n>.md`.
2. **One item per block**, with this header, then at most 15 lines of argument:

   ```
   ## CR-<team>-<n>: <one-line title>
   claim: <id from claims.yaml, or "new">
   kind: wrong-statement | wrong-status | wrong-dependency | missing-claim | notation | other
   severity: high | medium | low
   proposed: <the replacement text: a statement, a status tag, an edge, or an entry>
   evidence: <file:line, page, equation, or a computation you can point at>
   affects: <teams/artefacts that would have to change>
   ```

3. **What counts as evidence.** A reference into the paper (section, equation, PDF page), a line of a
   file in this repository, or a check you ran and can point at. "I think" is not evidence; write the
   item anyway and mark `severity: low`.
4. **Status changes need the decomposition.** If you propose changing a status, say which of
   `status_parts` (M / M? / S / C / E) moves and why. The file's convention is: `status` is the weakest
   tag the statement as written depends on.
5. **New claims are allowed** and should be expected: a statement that turns out to be load-bearing and
   is not in the inventory is a `missing-claim` request with the full field set of `claims.yaml`.
6. **A change request never blocks work.** Until the lead answers, keep using the frozen entry and note
   the disagreement in your own artefact. A team that stops because of a CR is doing it wrong.
7. **Dependency cycles.** If you find a cycle in `dependencies.dot`, report it as `wrong-dependency`
   with the path. The graph is acyclic as frozen (checked mechanically at generation, see
   `reports/T1-report.md` §2); a real cycle in the *argument* (as opposed to the graph) is a finding for
   `work/09-redteam/`, not a CR.
8. **Notation.** A new symbol that will appear in the final file needs a CR of kind `notation` with its
   name, what it is in words, its type, its first section, and — if it collides — the resolution. T1
   will fold accepted notation CRs into a version 2 of `notation.tex`; T8 does not invent macros.

## Items already expected (do not duplicate)

| CR | from | content |
|---|---|---|
| I2 | T8/T2 | §6.1's admitted ranges are not derived from Definition 4.1 (report §4, high) |
| I3 | T5 | `k ≤ 10` is unreachable at the stated widths (report §4, medium) |
| I4 | T5 | Stage-C clustering cutoff degenerate at `M < 26` (report §4, medium) |
| I5 | T5 | the `1.00000075` intermediate of §A.10 (report §4, low) |
| I8 | T4/T9 | `S(P,R)` as a set of classes vs the union in (5.26) (report §4, medium) |
| I11 | T2 | the Record layout does not store `q_d`, `slack`, `Φ`, `N`, `ℓ` (report §4, low) |
