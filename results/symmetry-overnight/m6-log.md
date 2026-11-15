# m6 run log — direction 6 (nonextension side and proof synthesis)

Swarm `smwhnslql`, member `m6`, direction `d4`.
Working files also in `.ultramath/smwhnslql/m6/`.

## 0. Registered direction

Derive what an order-$3$ diagonal symmetry of a $\mathbb C^6$ MUB triple gives in
Hadamard-pair normal form; state the exact nonextension theorem still needed; check whether its
hypotheses (multiplicities, anchor independence) follow rather than being assumed; deliver a
modular revision separating proved / conditional / numerical / unresolved steps.

Board at registration: d1 (projection/support-lattice audit, m1), d2 (adversarial exact-triple
construction, m5), d3 (product identity $\Xi_A\Xi_B\Xi_C=0$, m4), d5 (literature audit, m2),
d6 (Weyl–Heisenberg covariance, m3).  No one owns the nonextension/synthesis side, so I did not
duplicate any of these.

## 1. Reading done

* Primary source read in full (`attachments/how-do-i-make-ofyz/A promising idea ... .txt`, 717 lines);
  code fragment (`Pasted text 1.txt`) read: it is the tail of a script with integers mod $24$,
  $\sqrt6=\zeta+\zeta^{23}+\zeta^5+\zeta^{19}$ ($\zeta$ a primitive 24th root), Smith forms of the
  support lattice at three anchors with expected invariants $[1,1,1,1,3],[1,1,1,1,3],[1,1,1,1,2]$.
* `results/elegant-proof-routes.md` (route map; R1–R7, three rigidity failures, $\Sigma$ residue).
* `results/order3-stratum.md` (Lemma A $(2,2,2)$, Theorem B frame criterion, 7-parameter count,
  numerical gap $0.0422687212$, Conjecture 1 symmetry propagation).
* `results/symmetric-obstruction-audit.md` (the project's audit of the *nonextension* theorem —
  the load-bearing step for my direction).
* `attachments/is-this-a-useful-r01i/...txt` — the original note containing the full proof of the
  Symmetry Obstruction (lines 1–702; §8 is the sharp $1/108$ inequality, outside my scope).

## 2. What I checked, and what changed my plan

1. The chain "$\Delta$-tuple $\ne(1,1,1)$ $\Rightarrow$ no fourth vector" is available, and its
   nonextension step is **already proved in this project** (Symmetry Obstruction).  So the residue
   of the source's programme is *only* the symmetry-forcing statement.  I re-verified the
   obstruction proof line by line rather than trusting the audit (see the revision, §3).
2. That re-verification found **one error in the project's own audit note**: its item (i) claims
   the source's normalisation step $u\mapsto(1,\dots,1)/\sqrt6$ is wrong and needs a blockwise
   $U(2)$ repair.  It does not: every coordinate of $u$ has modulus $1/\sqrt6$ by flatness, and
   *every* diagonal unitary commutes with every diagonal $T$, so diagonal rephasing preserves the
   symmetry.  The audit's "repair" is unnecessary and its stated reason is false.
3. Exact computation (`m6-check.py`, copied here) on the tensor/Heisenberg triple in $\mathbb Z[\zeta_{24}]$:
   $|G_A|=|G_B|=|G_C|=6$; every element has order in $\{1,2,3,6\}$; order $2$ gives multiplicities
   $(3,3)$, order $3$ gives $(2,2,2)$, order $6$ gives $(1^6)$ with square $(2,2,2)$ and cube $(3,3)$;
   the support-lattice index equals $|G_A|$ at all three anchors ($150$ nonzero projection entries,
   $30$ of them the diagonal positions $(i,j,i,j)$ with value $1/3$ and zero relation vector, $120$
   nontrivial relations, Smith $[1,1,1,1,6]$ each).  This confirms the source's eq. (5) and its table row "standard
   product triple, $\Delta=6$" at *all three* anchors, not just the selected one.
4. Consequence: the source's $\Delta=2$ divisibility lemma is **not needed** for its strongest
   target (the product identity (13) already implies a threefold symmetry at some anchor); its role
   is to weaken that target from "some anchor has $3\mid\Delta$" to the strictly weaker closed
   condition "some anchor has $\Delta\ge2$".  That is the precise value of the lemma, and it is what
   I state as the modular revision's target R.

## 3. Files

* `m6-report.md` — final report (verdicts, chain, residue).
* `m6-proof-revision.md` — modular revision: the logical architecture with every step labelled
  proved / conditional / numerical / unresolved, plus the corrected audit and the new lemmas
  (finiteness of $G_X$, monomial-trace $2+2+2$, hypothesis transfer, residue is open).
* `m6-check.py` — reproducible exact script (needs `sympy`; runtime $\approx1$ s).

## 4. Second round of exact checks

Added to `m6-check.py` output: the *cycle type* of every group element on each of the other two
bases.  At all three anchors: order $2$ gives three $2$-cycles, order $3$ gives two $3$-cycles
(Lemma 2(1) confirmed, which I had not tested in the first round), order $6$ gives a single
$6$-cycle.  The six elements are the same exponent vectors at all three anchors for this triple.

Also verified the audit's 4-row counterexample to the $3\times3$ sign lemma (zero column sums, every
row on $x^2+y^2+z^2-2xyz=1$, $\max|\text{entry}|=1/2$), so the sign lemma is genuinely three-row,
i.e. $\mathbb Z_3$-specific; recorded in `m6-proof-revision.md` §6.

## 5. Where I stopped

The residue is $(T3)\iff(T1)$ unconditionally; granting (I3) it weakens to (T2).  Everything
downstream of (T3) is proved or cited.  I did **not** attempt
to prove (T2), to audit the source's §4 normal form (8) (the only unowned item; it matters only for
the order-$2$ route), or to reproduce the source's exact $(3,3,2)$ triple.  Submitted with these
gaps declared.

## 6. Cross-check with m4 (direction 3)

`results/symmetry-overnight/m4-theorem.md` (posted during my run) proves: $G_X$ finite abelian with
$|G_X|\mid6$ via the identity-component argument (equivalent to my Lemma 1); $Z=\{3\mid\Delta_X\}$
clopen; and (13) $\iff$ no connected component of the triple space is entirely asymmetric.  Their
Theorem A is my $(T1)\iff(T3)$ in component form.  No conflict; two independent proofs of Lemma 1
now exist, and my extra content is the $\Delta\ge2$ version of closedness plus the
divisibility-based weakening of the target.

## 7. Corrections after the judge's first review (second submission)

The first submission was rejected for four specific defects; all four are fixed.

1. `support()` skipped every position with $k=i$, so the scan reported $120$ nonzero projection
   entries instead of the true $150$.  The omitted $30$ positions are exactly $(i,j,i,j)$ with value
   $1/3$ (the source's normalisation) and *zero* relation vector.  The script now scans all $900$
   positions, asserts the $1/3$ value on those $30$, reports $150$ nonzero / $30$ zero-relation /
   $120$ nontrivial relations, and the Smith form $[1,1,1,1,6]$ is computed from the $120$
   nontrivial rows as before.  Data and prose corrected.
2. $(T2)$ is **not** the unconditional residue.  Corrected everywhere: unconditionally the residue is
   $(T3)\iff(T1)$; $(T2)+(I3)\Rightarrow(T3)$ only, so without (I3) the open target is $(T3)$.
3. Closedness is now **proved unconditionally** ($[P]$) by the finite-torsion argument
   ($\Delta_X\ge2$ iff $G_X$ meets the finite set of diagonal clocks of order dividing $6$; the
   condition $[T]\in G_X(x)$ is closed), so no recovery lemma is needed.  The divisibility refinement
   $\Delta_X(x_n)\mid\Delta_X(x)$ remains $[C]$ on (5) and is labelled as such; revision §8 is split
   into 8(a) $[P]$ and 8(b) $[C]$.
4. The script now *prints* the cycle types, so the log's reproducibility claim is accurate.
