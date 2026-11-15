# Reader path: how six dimensions refuse a fourth basis

*Six pages, no proofs, no code. This is the skeleton T8 writes the final paper around: every
paragraph here has a `[c:…]` pointer to the claim that backs it, and the narrative uses only the names
fixed in `notation.tex`. Prerequisites: Hadamard matrices, tensor products of matrices, and the
unitary group U(2).*

---

## 0. The one-paragraph version

Two orthonormal bases of $\mathbb{C}^d$ are **mutually unbiased** if every vector of one has the same
overlap with every vector of the other. Complete families of such bases are the natural home of
"complementary measurements", and a classical count says a complete family has at most $d+1$ members.
For $d$ a prime power, $d+1$ of them exist. For $d=6$ — the first dimension that is not a prime power
— the long-standing conjecture is that only three exist. This paper proves it, by computer assistance
of an unusual kind: it does not search for four bases, it *covers* the space of all possible second
bases by finitely many certified balls, and then proves locally, in each ball, that no two further
bases fit. The computer's job is to produce the finite cover and to run finitely many one-sided
inequality tests; the mathematical job, which is the bulk of the paper, is to make each of those tests
a *necessary condition* and each of those balls a *certified region*. `[c:thm-1.1]`

---

## 1. What a MUB is, and why dimension six is the first interesting case

Write $e(x) = \exp(2\pi i x)$. Two orthonormal bases $B = (b_1,\dots,b_d)$ and $C = (c_1,\dots,c_d)$ of
$\mathbb{C}^d$ are mutually unbiased if
$$|\langle b_i, c_j\rangle|^2 = \frac1d \qquad \text{for all } i,j.$$
The number $1/d$ is the smallest a squared overlap can be on average, so a pair of MUBs is a pair of
bases that are *as far apart as possible*: knowing which vector you have in one basis tells you
nothing about the other. A family is pairwise unbiased if every two of its members are.

Let $N(d)$ be the largest size of such a family. Three facts frame the problem.
* $N(d) \le d+1$ always, and $N(d) = d+1$ for every prime power $d$ (a construction using finite
  fields; for $d=p$ the second basis is the Fourier matrix).
* $d=2,3,4,5$ are all prime powers, so the upper bound is attained in each and those dimensions are
  settled.
* $d=6 = 2\cdot 3$ is the first dimension that is **not** a prime power, and it is the first case
  where the maximum is unknown. The tensor-product construction gives $N(6) \ge 3$: take three MUBs in
  $\mathbb{C}^2$ and three in $\mathbb{C}^3$ and multiply them, giving three in
  $\mathbb{C}^2 \otimes \mathbb{C}^3 = \mathbb{C}^6$. `[c:lem-1.2]`

So the conjecture — Zauner's, in this dimension — is $N(6) = 3$: the tensor construction is already
optimal and no fourth basis can be added. Everything that follows is devoted to excluding a fourth.

Why is $6$ so much harder than $5$? Because $5$ is prime: there is a formula, and one checks it. A
composite dimension offers no formula, and the objects that a proof must handle are not finite in
number. That is the whole difficulty, and it is why the argument below is a *cover* rather than a
classification.

## 2. Fix the first basis, and the second becomes a Hadamard matrix

Two normalisations cost nothing. First, a common unitary sends the first basis to the coordinate
basis; this is a change of basis and cannot create or destroy a fourth basis. Second, unbiasedness
against the coordinate basis forces every entry of the second basis to have modulus $1/\sqrt6$. So the
second basis is the column basis of $H/\sqrt 6$, where
$$|H_{ij}| = 1 \ \text{ for all } i,j, \qquad HH^* = 6I .$$
Such an $H$ is a **complex Hadamard matrix**. The upper-bound problem has now become: *for every
complex Hadamard matrix $H$ of order six, show that $H$ cannot be extended by two further bases.*
`[c:def-2.1]`

Two remarks about this reformulation matter for the rest.

* $H$ is a matrix of phases: writing $H = e(P)$ entrywise for a real phase matrix $P$, the condition
  $HH^* = 6I$ becomes thirty real equations in thirty-six real unknowns (six of them are pure gauge).
  The solution set is a real algebraic set of dimension at least a few, and it is where the difficulty
  lives: it is not a finite list of matrices.
* Row and column rephasings, permutations, transposition and complex conjugation all act on $H$ and
  all preserve extendibility. So a proof may quotient by them — but it must say, every time, which
  equivalence it used, because a ball in one chart is a different set after a rephasing.
  `[c:lem-2.2]` `[c:lem-2.7]`

**The obstacle in one sentence.** To prove that no $H$ extends, one would like to examine every $H$;
there are continuously many, and no classification of order-six complex Hadamard matrices is
available.

**The strategy in one sentence.** Replace "every $H$" by finitely many small regions, each carrying a
certificate that says *every* exact Hadamard matrix in it is covered — and then exclude two further
bases throughout each region, not merely at a sample point.

## 3. The idea: nested covers, and tests that can only be right

Four principles are used at every stage, and it is worth naming them once.

1. **Cover, don't sample.** A region is discarded only when it is *covered* by finitely many smaller
   regions with certificates, or *excluded* by a test. A region that is neither stays in the ledger as
   unresolved. Nothing is ever discarded because a search failed to find something.
2. **Tests are necessary conditions.** Every exclusion is the failure of a condition that must hold if
   a fourth basis existed. So a test can be arbitrarily optimistic: it may retain configurations that
   cannot occur, and the proof survives. What it may never do is reject one that can.
3. **Propose ≠ certify.** Every numerical object in the argument (a direction, a frame, a centre, a
   clustering, a search) is *proposed* by a heuristic and then *certified* by evaluating a one-sided
   inequality. The heuristics are allowed to be bad; a bad heuristic loses coverage opportunity, which
   shows up as extra work, not as a false proof.
4. **Freeze the algebra at the centre.** The algebraic objects used at a region (eigenvectors, kernels,
   frames) are computed at the region's *centre*, which need not be an exact Hadamard matrix. Every
   exact solution in the region is then compared to those frozen objects, and the comparison error is
   bounded by the region's radius. This is why approximate centres are legitimate — and why every
   stage carries explicit radius constants.

The shape of the whole argument is then a nested cover:

```
        all complex Hadamard matrices of order 6
                      |  stage 1: cover the second basis
        finitely many seed balls, radius 0.032 cycles
                      |  stage 2: cover all completions of each seed ball
        finitely many certified phase balls (Records), radius <= 0.125 cycles
                      |  stage 3: shrink the balls
        certified balls of radius <= 0.011 cycles
                      |  stage 4: cover every vector of two further bases
        finitely many vector balls + two graphs per Record
                      |  stage 5: exclude the forbidden pattern
        no Record survives with a positive answer
                      |  the ledger: every stage accounted for
        N(6) = 3      (under the stated execution hypothesis)
```

Each arrow is an implication with an explicit hypothesis. The four "finitely many" arrows are where the
mathematics is; the last is where the computation is.

## 4. Stage 1 — cover the second basis

We cannot list the Hadamard matrices, but we can list *where their phases are*. A Hadamard matrix in
dephased form (first row and column equal to $1$) is determined by nine remaining phases: five in the
first row, three more in the first column after choosing a second column, and one shared. Better, the
matrix has a pair of rows at the *minimum circular gap*; after rephasings and permutations that pair
can be taken to be the first two, and the nine phases can be ordered so that
$$x = (0,x_1,\dots,x_5), \quad 0 \le x_1 \le \cdots \le x_5, \quad x_1 \le x_5 - x_4,$$
with a similar list $y$ for the second column. This "seed arrangement" is a normal form: every exact
$H$ has a representative in it. `[c:lem-2.4]`

Now put a grid of width $1/112$ on the nine coordinates. Every exact representative lies in exactly
one closed bin tuple, and two cheap necessary tests (a gap filter and a vanishing-sum test, both
consequences of orthogonality of the rows and columns) throw most tuples away before any work is done.
`[c:lem-2.6]` `[c:lem-2.7]` `[c:lem-2.8]` What survives is a finite list of *seed pairs*, and for each
one the algorithm either certifies that its whole feasible part lies inside an already-retained ball
of radius $0.032$ cycles, or retains its own midpoint as a new centre. Either way, every exact
$H$ is within $0.032$ cycles of a retained centre in all nine coordinates. `[c:prop-2.10]`

The number is worth pausing on: $151{,}744{,}086$ seed pairs are examined and $249{,}878$ centres are
retained. The ratio is the point. Bins are cheap; centres are expensive; the tests are strong enough
that two hundred thousand balls cover a nine-dimensional torus of phases. `[c:run-7.5]`

## 5. Stage 2 — cover all completions of one seed

Fix one seed ball. Its nine phases are known only up to $0.032$ cycles, but that is enough to freeze
the algebra. Write the matrix in blocks of size $2+4$:
$$H' = \begin{pmatrix} E' & B' \\ C' & D' \end{pmatrix}.$$
The seed fixes $E'$, $B'$ and $C'$ up to small displacements, and leaves the $4\times4$ block $D'$ to be
determined by the Hadamard equations. The two known blocks $B'$ and $C'^*$ have rank two, so they have
two-dimensional kernels inside $\mathbb{C}^4$; compressing $D'$ between those kernels gives a $2\times
2$ matrix $Y$. The Hadamard equations then say something remarkably rigid: $Y$ is close to $\sqrt6$
times a *unitary* $2\times2$ matrix, with an explicit bound on the distance. `[c:lem-3.1]`
`[c:lem-3.2]`

This is the hinge of the whole proof. A four-dimensional completion problem has become a point of
$U(2)$ plus a bounded error. And $U(2)$ is four-dimensional and can be covered by closed cells: every
unitary has a representation
$$V = e(\alpha)\begin{pmatrix} e(\beta)\cos 2\pi t & e(\gamma)\sin 2\pi t \\
-e(-\gamma)\sin 2\pi t & e(-\beta)\cos 2\pi t\end{pmatrix},
\qquad 0\le\alpha\le\tfrac12,\ 0\le t\le\tfrac14,\ 0\le\beta,\gamma\le 1,$$
so a grid of width $1/N_u$ in the four angles covers it. `[c:lem-3.3]`

Now recurse. Each cell is tested by two necessary inequalities, both derived from a uniform Taylor
expansion around the cell's midpoint: a *norm* test and a *directional* test (a linear functional
applied to the twenty exact equations, with a witness direction $y$). A cell that fails either is
empty of feasible completions and is discarded. A cell that passes too much is subdivided into
sixteen children, whose closed intervals cover it. A cell whose entire feasible content can be placed
inside one phase ball of radius at most $0.125$ cycles is covered by a Record. Recursion stops at
depth 3 or at grid 64, and the induction is airtight: an exact completion is never in an excluded
cell, and it can always be followed into at least one child. `[c:lem-3.4]` `[c:lem-3.5]`
`[c:cor-3.10]` `[c:prop-3.11]`

The output of Stage 2 is a finite atlas of Records: each is a centre, a tangent frame, seven bounds,
and a radius, with the guarantee that every exact Hadamard matrix equivalent to something in the seed
ball lies inside some Record's ball. `[c:prop-4.16]`

*Where the seven bounds come from.* A Root certificate is not a parametrisation of the Hadamard locus;
it is a *frame plus an error budget*. $T$ is a $36\times k$ matrix of numerical tangent directions
($k\le 10$, typically 3 to 5), and $n_P(s) = n_0 + \mathrm{id}\,s + Cs^2$ is the bound on the part of a
displacement that the frame misses. Nothing about $T$ is exact: it need not be orthogonal, it need not
be horizontal, and the normal directions are bounded rather than eliminated. `[c:def-4.1]`
`[c:rem-4.2]`

## 6. Stage 3 — shrink the balls

The cover so far is a cover by balls of radius at most $0.125$ cycles. Stage 4 will need small balls,
because its tests get weak when a ball is large. So the next stage replaces each ball by finitely many
smaller ones — without any regularity assumption on the Hadamard locus.

The mechanism is the Root certificate read as a *two-coordinate description*. A displacement
$\delta$ splits into its tangent part $\eta = T^*\delta$ ($k$ coordinates) and its normal part
$\nu = \delta - T\eta$. The tangent part is searched exhaustively: a grid of boxes in the $k$ tangent
coordinates covers the ball, and the farthest tangent distance of a box can be computed exactly.
`[c:lem-5.1]` `[c:lem-5.5]` The normal part is not searched; it is bounded, using the normal
polynomial $n_P$. Two Roots at nearby centres $P$ and $Q$ give two independent bounds on the same
exact solution, and taking the minimum of the two repeatedly can only improve. `[c:prop-5.2]`
`[c:lem-5.3]`

Two things make this sound. First, every bound is one-sided: each computed number is an upper bound for
a distance, so any amount of arithmetic slop in the *proposal* is harmless. Second, the decision "this
box belongs to that ball" is certified by a *stored* evaluation of the computed function
$\hat D(t)$, not by a monotonicity assumption about floating-point arithmetic. `[c:eq-5.17]`
`[c:lem-5.4]`

Running this twice (a "mid" pass with target radius $0.07$ and a "fine" pass with target $0.016$, then a
fallback pass at $0.011$) takes $3083$ coarse records to $22{,}379$ fine ones. The bookkeeping is the
delicate part: a box may be assigned to an existing atlas ball, merged into it, or given its own new
centre; a parent that fails is *retained* as an obligation, never dropped; and the induction is over
*already completed* parents only, which is exactly what stops the argument from going in a circle.
`[c:prop-5.7]` `[c:cor-5.8]`

## 7. Stage 4 — cover every possible extra vector

Now fix one Record: a small ball of exact second bases, all equivalent to a common centre $P$ and
tangent displacement $\delta$. Suppose two further bases exist. Each of their twelve vectors is
unbiased to the coordinate basis, so it has the form $e(\beta)/\sqrt6$ with five free phases; and each
is also unbiased to the *same* second basis. Cover the five phases at resolution $M$ by closed bins,
and each bin by a small vector ball. `[c:lem-6.1]` `[c:lem-6.2]` `[c:lem-6.4]`

Two facts organise what is left.

* **The twelve vectors have distinct labels.** Two vectors in the same vector ball of radius $<0.1$
  are neither orthogonal nor unbiased, so no two of the twelve can share a ball. `[c:lem-6.5]`
* **The tests are pairwise.** For each pair of retained balls, a necessary test decides whether the
  pair *could* be orthogonal, and another whether it *could* be unbiased. Each test keeps the pair
  unless it can rule it out, and the joint unbiasedness test keeps one shared tangent variable — the
  common displacement $\delta$ — which is the only genuine coupling between the two vectors and makes
  the joint test strictly stronger than two separate ones. `[c:lem-6.6]` `[c:lem-6.7]`

The result is two graphs on the retained labels, an orthogonality graph $\mathcal O$ and an
unbiasedness graph $\mathcal U$. Two further bases would give two disjoint six-cliques in
$\mathcal O$ with all thirty-six cross edges present in $\mathcal U$. Stage 4's last act is to show
that this pattern does not occur: a finite, exhaustive two-clique search that either finds the pattern
or proves that it is absent. When it proves absence, the Record contributes a negative result — no
exact second basis in this ball can be extended. `[c:eq-6.24]` `[c:lem-6.8]` `[c:prop-6.9]`

Note carefully what "proves absence" means here. Exhausting a work cap, or failing a heuristic, is
*not* a negative result: it makes the Record unresolved and pushes it into a fallback pass. Only a
completed exhaustive search, or an empty terminal bin layer, counts. This distinction is repeated in
every stage of the paper for the same reason: the pipeline must be able to say "I don't know".
`[c:prop-6.9]`

## 8. Stage 5 — the ledger

What is left is bookkeeping of an unusually high standard, and it is where the theorem's hypothesis
comes from. The run consists of one cover process, four Stage-2 shards, two sequential Stage-3
refinements, one Stage-4 process per batch, a fallback for the records that Stage 4 could not decide,
and four final Stage-4 shards. The claim is not that any single program is correct; it is that *if*
every invocation exits normally, *if* every stage processes every record it was given, *if* the counts
and hashes agree and the fallback inputs are an ordered subsequence of the failures, *then* the exact
second basis of any hypothetical four-family is carried by an unbroken chain of coverage from the seed
cover to a Record with a negative Stage-4 result — which is a contradiction. `[c:thm-7.1]`
`[c:flow-7.2]`

In the documented run the chain closes. The numbers are in Table 1 of the paper: $249{,}878$ centres,
$3083$ coarse records, $600$ after the first refinement, $22{,}379$ after the second, $163$ records
that hit the graph work cap, $1127$ after the fallback, and zero unresolved records at the end.
`[c:run-7.5]` `[c:bounds-7.3]`

## 9. What is proved, and what is assumed

This is the part the reader is entitled to have stated plainly, and T8 should not soften it.

* The **mathematical** content is a correct necessity-and-cover argument: every exclusion is the
  failure of a necessary condition, every cover is by closed regions, and the composition of the five
  stages is an implication. Most of it is checkable by hand and a good part of it is being formalised.
* The **empirical** content is the run: that a particular set of programs, on a particular machine with
  binary64 arithmetic, completed with the stated terminal conditions. The paper states the arithmetic
  premises explicitly, derives twenty pages of error budgets from them, and prints the counts and
  hashes. It does not supply the sources or the archive, so neither the budgets nor the run can be
  audited from the document alone.
* The gap between the two is exactly the list of statements about code: that the Root builder's
  direct checks really do certify the seven constants, that the refinement's bookkeeping really is
  complete, that the clique search really is exhaustive, that the arithmetic really is as analysed.
  `[c:prop-4.6]` `[c:prop-5.7]` `[c:lem-6.8]` `[c:lem-a.1]`

The honest form of the theorem therefore names its hypothesis. That is not a weakness of this proof
in particular; it is what a computer-assisted proof of a statement about a continuum looks like unless
the certificate format is designed for independent checking — which is the next thing to do.

## 10. Map to the paper

| narrative | paper | claim ids |
|---|---|---|
| §1 MUBs, $d=6$ | §1, §7.5 | `thm-1.1` `lem-1.2` `cor-1.3` |
| §2 Hadamard reformulation | §2.1 | `def-2.1` `lem-2.2` `lem-2.3` |
| §4 cover the second basis | §2.2-2.4 | `lem-2.4`-`lem-2.9` `prop-2.10` |
| §5 cover the completions | §3, §4.1-4.2 | `lem-3.1`-`prop-4.6` |
| §6 shrink the balls | §4.3-4.7, §5 | `lem-4.7`-`prop-4.16` `lem-5.1`-`cor-5.8` |
| §7 cover extra vectors, exclude the pattern | §6 | `lem-6.1`-`prop-6.9` |
| §8 the ledger | §7 | `thm-7.1` `flow-7.2` `bounds-7.3` `run-7.5` |
| §9 what is proved | §A, §7.1 | `prem-arith` `app-a4-a11` `margin-a.12` |
