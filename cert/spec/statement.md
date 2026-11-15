# Statement and trusted base — v0 (H0 draft, NOT frozen)

## Target
There exist a certificate object $C$ (a versioned directory of data files plus `manifest.json`)
and a checker program $Q$ such that
1. $Q(C)$ terminates with verdict `accept` and an unresolved count of zero; and
2. the assembly argument (human-checked, with the deterministic core and the covering
   implications mechanised in Lean under the scope of decision D2) proves
   $$Q(C)\ \text{accepts} \quad\Longrightarrow\quad \text{no four pairwise mutually unbiased bases in }\mathbb C^6.$$
With the three explicit bases of Lemma 1.2 this yields $N(6)=3$.

## What a reader must trust after this programme
- the necessity lemmas of the preprint, as transcribed in `cert/spec/inequalities.md`;
- the checker $Q$ (target $\le 2000$ readable lines, one entry point);
- the arithmetic kernel contract in `cert/spec/arithmetic.md` and its implementation;
- the assembly argument and its stated hypotheses;
- the certificate format, so that acceptance has a fixed meaning.

## What is explicitly NOT trusted any more
- any particular execution, host, process tree or exit code of the authors' programs;
- binary64 semantics, compiler and libm behaviour, evaluation order, disassembly listings;
- any heuristic search, its enumeration order, its random choices, its caps — these propose only.

## Rules
- Exclusion happens only by strict violation of a necessary condition, certified one-sidedly.
- `unresolved` is never a negative. A nonzero final unresolved count invalidates the target
  statement and must be reported as a smaller theorem, never edited away.
- Every printed number in the final report is regenerated from `certdata/` by `src/report/`.

## Status vocabulary
`accept` / `reject` (a malformed or false certificate) / `unresolved` (a validly formed region
whose fate the certificate does not decide). The target statement requires zero unresolved.
