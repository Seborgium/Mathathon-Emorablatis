# Arithmetic kernel contract — v0 (H0 draft)

## Number forms
1. **Exact rationals** for bin indices, midpoints and every quantity constructed from them.
   Phases in cycles are multiples of $1/(2N)$ with $N=112$; midpoints $(b+\tfrac12)/N$,
   the radius $0.032$ and its stated inflation $0.0320001$ are inputs as exact decimal strings,
   never as binary64 literals.
2. **Outward intervals**, endpoints at $\ge100$-bit precision with documented directed rounding,
   for every transcendental or square-root quantity. Every primitive returns an enclosure of the
   exact real value, including conversion and input parsing.

## Elementary functions
$e(x)=e^{2\pi i x}$ is evaluated as an enclosing complex rectangle from enclosures of
$2\pi x$, $\cos$ and $\sin$, with argument reduction that is itself enclosed. Any use of a library
`cos`/`sin`/`sqrt` requires (a) documented error bounds at the working precision and (b) an
outward bump that covers them; "correctly rounded" is not assumed from a vendor's prose.

## Decidability discipline
A certified comparison is a one-sided implication: the checker must establish the strict form
(e.g. $\sup I < c$). If an enclosure straddles the decision point the result is
`undecided at precision p`; the driver may raise $p$ and retry, recording the precision used in
the witness. It may never resolve such a case to pass or fail by convention.

## Validation required of the kernel (H1 gate input)
- unit tests against exact rational identities and high-precision references;
- adversarial cases: exact ties, near-ties at the decision slack, subnormal-scale values,
  argument reduction near multiples of $\pi/2$;
- an explicit list of every library function relied on, with its guarantee and version.

## H0 throughput measurement (not a correctness result)
`src/kernel/bench_h0.py`, output `src/kernel/bench_h0.json` on this VM:
binary64 covrun baseline $151{,}744{,}086$ pairs in $401.82$ s $\approx 2.65\,\mu$s/pair;
gmpy2 `mpq` rational gap arithmetic $\approx0.68\,\mu$s/pair ($\approx103$ s single-core if applied
to all pairs); gmpy2 MPFR 100-bit `cos` $\approx0.92\,\mu$s per evaluation; mpmath at 40 dps
$\approx14.9\,\mu$s per evaluation. These are loop micro-benchmarks, not the real predicates; they
show only that a Python+gmpy2 certify path is not obviously infeasible. A native MPFR/FLINT kernel
remains an option if profiling demands it (no system GMP/MPFR headers are installed here).
