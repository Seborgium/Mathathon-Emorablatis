# m4: exact and high-precision tables of the diagonal symmetry indices

All numbers below were produced by my own code (`.ultramath/smwhnslql/m4/scratch/`, copies in
`results/symmetry-overnight/m4-code/`), independently of the source's fragment. Method:
flat unitary matrices are stored as integer exponent matrices over $\mathbb Z[\zeta_{24}]$;
the support of the projection $P_X$ is decided exactly by reducing sums of 24th roots of unity
modulo $\Phi_{24}$; the relation lattice $L_X$ is Smith-reduced over $\mathbb Z$; the symmetry
group $G_X$ is *also* computed directly from the two bases by enumerating monomial congruences
(no projection, no recovery lemma), and the two answers are compared.

Recall $S_X$ = Smith diagonal of the relation matrix, $\Delta_X=\prod S_X$ = index = $|G_X|$;
$r_X=\operatorname{rank}_{\mathbb F_3}R_X$; by the criterion $3\mid\Delta_X\iff r_X<5$.

## 1. Tensor (product) triple — exact, $\mathbb Z[\zeta_{24}]$

$A=I_6$, $B=F_2\otimes F_3$, $C=(S F_2)\otimes(Z F_3)$, $S=\operatorname{diag}(1,i)$,
$Z=\operatorname{diag}(1,\omega,\omega^2)$ — the standard three MUBs of $\mathbb C^2\otimes\mathbb C^3$.

| anchor $X$ | $\#$ supp $P_X$ (of 900) | $\#$ distinct relations | $S_X$ | $\Delta_X$ | $r_X$ |
|---|---|---|---|---|---|
| $A=I_6$ | 150 | 42 | (1,1,1,1,6) | 6 | 4 |
| $B$ | 150 | 42 | (1,1,1,1,6) | 6 | 4 |
| $C$ | 150 | 42 | (1,1,1,1,6) | 6 | 4 |

This reproduces the source's product control (its Smith form $\operatorname{diag}(1,1,1,1,6)$) and
its "standard product triple has $\Delta=6$". All three anchors carry a threefold symmetry, so (13)
holds here — **and every anchor also carries an order-two symmetry** ($\Delta=6$).

## 2. The Fourier chart: every triple $\{I_6,F_6,K\}$ with entries in $\mu_{24}$ — exact

$F_6=(\zeta_6^{jk})_{j,k=0}^{5}/\sqrt 6$. Of the 48 rays unbiased to $\{I_6,F_6\}$ (Grassl's count,
reproduced in the project's notes), exactly **12** have root-of-unity entries; writing them in the
normalisation "first coordinate $=1/\sqrt6$" with phases in $\mu_{12}$, they admit exactly **4**
orthonormal sextuples. All four are analysed exhaustively; each of the four triples is exactly MUB
(checked: columns orthonormal, all three cross matrices flat, in $\mathbb Z[\zeta_{24}]$).

| sextuple (indices of the 12 rays) | $S_A$ | $S_B$ | $S_C$ | $(\Delta_A,\Delta_B,\Delta_C)$ | $r_A,r_B,r_C$ |
|---|---|---|---|---|---|
| (0,2,5,6,8,11) | (1,1,1,1,6) | (1,1,1,1,6) | (1,1,1,1,6) | (6,6,6) | 4,4,4 |
| (0,3,5,7,8,10) | (1,1,1,1,3) | (1,1,1,1,3) | (1,1,1,1,2) | (3,3,2) | 4,4,5 |
| (1,2,4,6,9,11) | (1,1,1,1,3) | (1,1,1,1,3) | (1,1,1,1,2) | (3,3,2) | 4,4,5 |
| (1,3,4,7,9,10) | (1,1,1,1,6) | (1,1,1,1,6) | (1,1,1,1,6) | (6,6,6) | 4,4,4 |

Two independent computations of each line: the lattice index, and the direct enumeration of
$G_X=\{[T]:T$ preserves both ray sets$\}$, give the same order in all 12 cases (no exchanging
clocks). Group structures: for $\Delta=6$ the group is cyclic of order 6 (element orders
1,2,3,3,6,6); for $\Delta=3$ it is $C_3$ (element orders 1,3,3); for $\Delta=2$ it is $C_2$
(element orders 1,2).

**The two middle rows reproduce the source's exact example**: its Smith forms
$\operatorname{diag}(1,1,1,1,3),\operatorname{diag}(1,1,1,1,3),\operatorname{diag}(1,1,1,1,2)$ with
$\Delta=(3,3,2)$ are exactly these, on a triple whose entries are 24th roots of unity. (The source
calls it "a special point of the continuous family"; whether it lies in the family or in the isolated
Fourier chart, the arithmetic is the same.) Note that this example is consistent with the source's
order-two lemma: the anchor with $\Delta=2$ has the other two divisible by 3.

## 3. The explicit JMSSW one-parameter family — 60-digit arithmetic

The family $\{I_6,\ F(0,b(t))/\sqrt6,\ C(t)/\sqrt6\}$ of
`.scratch/mub6/fouriercheck2.py` with $b(t)$ the value returned by `Cmat(t)` (real for
$t\in[0.5,1.1]$), mpmath at 60 digits, zero threshold $10^{-30}$.

| $t$ | MUB residual | anchor $A$: supp / $S_A$ | anchor $B$ | anchor $C$ |
|---|---|---|---|---|
| 0.5 | $1.0\cdot10^{-31}$ | 276 / (1,1,1,1,3) | 660 / (1,1,1,1,1) | 660 / (1,1,1,1,1) |
| 0.6 | $2.0\cdot10^{-31}$ | 276 / (1,1,1,1,3) | 660 / (1,1,1,1,1) | 660 / (1,1,1,1,1) |
| 0.7 | $6.9\cdot10^{-31}$ | 276 / (1,1,1,1,3) | 660 / (1,1,1,1,1) | 660 / (1,1,1,1,1) |
| 0.8 | $5.9\cdot10^{-30}$ | 276 / (1,1,1,1,3) | (degenerate: $b(0.8)\approx0.004$, near $F_6$) | |
| 0.9 | $3.5\cdot10^{-31}$ | 276 / (1,1,1,1,3) | 660 / (1,1,1,1,1) | 660 / (1,1,1,1,1) |
| 1.0 | $3.0\cdot10^{-31}$ | 276 / (1,1,1,1,3) | 660 / (1,1,1,1,1) | 660 / (1,1,1,1,1) |
| 1.1 | $2.0\cdot10^{-31}$ | 276 / (1,1,1,1,3) | 660 / (1,1,1,1,1) | 660 / (1,1,1,1,1) |

So along the whole explicit family
$$(\Delta_A,\Delta_B,\Delta_C)=(3,1,1),$$
for $t\ne0.8$ the smallest retained projection entry is $\ge2.4\cdot10^{-4}$ and the largest
discarded one is $\le2.8\cdot10^{-31}$: a gap of 27 orders of magnitude, i.e. the support decision is beyond
reasonable doubt (it is not a rigorous interval certificate; a routine interval version would make it
one). This confirms and sharpens the source's five numerical family points: the pattern is
**constant** along the family, and (13) is *sharp* there — exactly one anchor carries a threefold
symmetry, exactly one, so no strengthening of (13) to "two anchors" or to "order six" can hold.

Note also: the family anchor with $\Delta=3$ is the coordinate ancestor in which the dephased corner
of the pair $(A,B)$ has the two pinned cube-root entries $E_{23}=\omega$, $E_{33}=\omega^2$
(`results/elegant-proof-routes.md` §9). My computation does not prove a causal link, but it is
consistent with §9's conjecture that the extendable locus is characterised by that pinning.

## 4. What these tables do and do not show

They compute $\Delta_A,\Delta_B,\Delta_C$ on explicit triples: exactly for the tensor triple and for the
four root-of-unity Fourier-chart triples, and at 60 digits (gap $10^{27}$) for seven members of the JMSSW
family.

* They are a check of the *invariants*: they reproduce the source's $(3,3,2)$ Smith data exactly, confirm
  the source's "product triple has $\Delta=6$", and put the source's five numerical family points on a
  rigorous footing of sorts (same value at seven parameters, with a large gap).
* They are **not** a test of (13). The JMSSW family is a curve inside a two-dimensional moduli space, and
  the failure locus of (13), if nonempty, is *open* in the triple space (Proposition 2); an open set can
  miss a curve. So the constant value $(3,1,1)$ along that curve says nothing about triples off it, and
  the fact that no counterexample appears here carries no weight against a full-dimensional open failure
  locus. The same caveat applies to m2's 9,320-point census of the two-parameter family unless that family
  is independently known to be the whole moduli space — which is the classification, not a sampling
  result.
* By contrast, a sample drawn from the *full* triple space with a density (w.r.t. the volume of each
  dimension stratum) would detect a nonempty open failure locus with probability one; that is the kind of
  sampling that would be evidence. I did not perform one (it requires a random-triple generator, i.e. a
  solver on the 2-dimensional moduli space).

## 5. Reproduction

```bash
cd <repo>/.ultramath/smwhnslql/m4
python3 scratch/run_tensor.py      # section 1  (exact, Z[zeta_24])
python3 scratch/smith_table.py     # section 2  (exact; also prints the tensor triple again)
python3 scratch/f6_final.py        # section 2, second route: index vs. direct group enumeration
python3 scratch/jmssw2.py          # section 3  (mpmath, dps=60)
```
Dependencies: `numpy`, `sympy` (Smith normal form), `mpmath`; the JMSSW script additionally reads
`<repo>/.scratch/mub6/fouriercheck2.py` for the family formulas `Fmat(a,b)`, `Cmat(t)` written by an
earlier run of this project (I did not re-derive them; the MUB residual printed above is the check
that they are the triple they claim to be).
