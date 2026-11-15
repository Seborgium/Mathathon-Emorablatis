# handoff-10 — findings that need a second pair of eyes

- **from** T1/m1, direction d6 (assembly spine)
- **to** T2 checker, T3 reference, T5 parameters, T9 red team; cc T8
- **version** 1, 2026-11-14
- **depends-on** `spine.md` §§4–6; catalogue ids `prop-2.10`, `prop-4.6`, `prop-4.16`,
  `prop-5.7`, `cor-5.8`, `prop-6.9`, `def-4.1`
- **blocks** nothing hard; supplies five test obligations and one correction to a catalogue
  open question
- **artefacts** `spine.md` §4 (interface register), §5.3 (equivalence lemma and monomial repair),
  §5.4 (paper's Lemma 1.2 re-derived), §6 (units)
- **claims touched** `prop-6.9`, `prop-4.6`, `lem-2.2`, `prop-4.16`
- **open questions** F4's distinguishability question, F6

## F1 — radius composability (`prop-5.7` / `cor-5.8` / `prop-6.9`)

Prop. 6.9 is stated only for Records of radius `r ≤ .03`; A emits `≤ .125`, B mid `τ = .07`,
B fine `τ = .016`. So Stage C composes with B fine and with the fallback (`.011`), and with
nothing earlier. `spine.md` interface I5. Not a gap — the run and §7.4's proof use the legal
order — but the inequality is never stated as a condition of composition.
**T2:** make `r ≤ .03` a hard precondition of every Stage C verdict.
(Independently found by the catalogue direction as its I4; recorded here because the assembly now
depends on it explicitly.)

## F2 — `lem-2.2`, the row-rephasing sentence

Applying a diagonal unitary to the four bases gives `(D, DH/√6, DB3, DB4)`, whose first member is
not the coordinate basis, so it does not establish extendibility of `DH` as Definition 2.1 defines
it. The conclusion is true. `spine.md` Lemma S.6 repairs it: if `V` is monomial and unitary then
`(I, VM, VB3, VB4)` are four MUBs whenever `(I, M, B3, B4)` are, because `V` preserves entrywise
moduli and unitarity. Nothing else in the paper changes.

## F3 — `prop-4.16`, the word "required"

The statement covers "every exact second-basis Hadamard matrix *required for the four-basis
problem*"; its proof follows *any* feasible matrix through the cell tree. The stronger statement
("every exact `H` in the seed ball") is what is proved and what the assembly prefers. T8: delete
the qualifier. T4: formalise the stronger form.

## F4 — `prop-6.9`, the admitted ranges: a correction to the catalogue's open question

`claims.yaml` asks how the ranges of (6.2) (`n0<1e-6`, `ι<1e-4`, `Γ<20`, `ω<1e-5`,
`mnorm<2`, `froot<1e-6`) are produced, and calls this "the sharpest internal gap", noting that
Definition 4.1 does not contain them. They are produced at two places the definition does not
mention: **§5.6, p. 39** (*"the normal constants are nonnegative and are checked against γ_P<20,
n0_P, ε_P<1e-6, α_P<1e-4, o_P, hor_P<1e-5, µ_P<2"*, as admission filters on stored Roots) and
**§A.9, p. 67** (*"`validate` enforces 0≤R≤.126, 0≤C<20, 0≤n0,froot<1e-6, 0≤id<1e-4,
0≤ort,hor<1e-5, 0≤mnorm<2, 0≤k≤10, |p_j|≤4"*, on every B input). A Record violating a range is
not admitted; its seed or parent fails; that is exactly what terminal conditions X2/X3/X4 exclude.
So the ranges hold for every Record that reached Stage C **conditional on the run's terminal
conditions** — weaker than "proved", stronger than "not known".
**Open for T9:** is a validation abort distinguishable from a failed seed in the archive? That
distinguishability is what carries the argument.

## F5 — the units bridge (`prop-2.10` → `prop-3.11`)

The seed cover is in cycles (`.0320001`); Stage A's seed displacement `s` is in radians
(`R_s = 2π r_s`, §3.1). This is the only place where a factor `2π` changes a *radius*, and it is
completeness-critical rather than soundness-critical: in cycles the seed ball would be 6.3× too
small and the cover would silently fail to be exhaustive. **T5:** make it a parameter with a unit
tag. **T2:** reject a certificate whose seed displacement is not `2π`× the cycle radius.
(Units table: `spine.md` §6; the catalogue's I8 has the same ledger.)

## F6 — what the assembly does *not* need

The dual support bound (2.19), the ellipsoid machinery of §4.5 and the clique search of Lemma 6.8
are each consumed inside one stage and never by the top-level argument. So a regression that
breaks (2.19) damages the *efficiency* of the seed cover, not the validity of the chain, provided
the cover still completes. **T2:** distinguish "certificate rejected" from "search got slower".
**T3:** the reference model may legally use the brute-force midpoint radius `3/(2N)` instead of
the reuse test and still satisfy Prop. 2.10.

## Test obligations for T2

1. Reject a Stage C verdict on a Record with `r > .03` (F1).
2. Reject a certificate whose seed ball is expressed in radians at the cycle radius (F5).
3. Accept mid → fine composition; reject C composed directly on the coarse atlas (F1).
4. Accept a run in which A's `ownfail` diagnostic is nonzero while `failedBalls = 0`
   (`spine.md` §2.7; §7.5 says exactly this happened for A0).
5. `prop-4.6` remains untestable without the source; `spine.md` I3 records that it is
   load-bearing for the whole assembly.
