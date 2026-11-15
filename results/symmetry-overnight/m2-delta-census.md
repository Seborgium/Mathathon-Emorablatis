# The symmetry index $\Delta$ on the (now complete) classification of triples

*member m2, swarm `smwhnslql`. Script: [`m2-explicit-triples.py`](m2-explicit-triples.py)
(`python3 m2-explicit-triples.py`, ~20 s, numpy only; `quick` skips the random census).
This note exists only because the classification makes it possible: before November 2026 there
was nothing to take a census over.*

## 0. Why this belongs to an external-input audit

The primary source asserts, without proof, that "the existing computational classification
implies a negative answer" to its own central question (*can three MUBs have trivial diagonal
symmetry groups at all three anchors?*), and reports a $\Delta$-table obtained from an exact
cyclotomic code plus numerical runs. Since the classification is now a published theorem
([`m2-dossier.md`](m2-dossier.md) §2), that table can be **checked independently and completely
in principle**. I checked it: exactly at the two points whose entries are roots of unity, and
numerically over the family. Two claims of the source come out confirmed, one is confirmed and
upgraded, and the general question is settled by a one-line argument that needs no computation
at all (dossier §4).

## 1. Definition (verbatim from the source, sec. 2)

$G_{\mathcal A}$ = the diagonal unitaries that preserve $\mathcal B$ and $\mathcal C$ as sets of
rays, modulo overall phase; $\Delta_{\mathcal A}=|G_{\mathcal A}|$. A basis is a matrix whose
columns are the vectors; $D X = X P_\sigma\operatorname{diag}(\mu)$ means
$d_i X_{ij}=\mu_j X_{i,\sigma(j)}$ for all $i,j$.

## 2. Method

For each anchor $\mathcal A$ put the triple in the $\mathcal A$-frame
($X=\mathcal A^*\mathcal B$, $Y=\mathcal A^*\mathcal C$) and, for each permutation $\sigma$ of the
six rays, test the *polynomial* condition that $R_{ij}=X_{i,\sigma(j)}/X_{ij}$ has rank one:
$$X_{i,\sigma(j)}X_{i',\sigma(j')}X_{i,j'}X_{i',j}
  -X_{i,\sigma(j')}X_{i',\sigma(j)}X_{i,j}X_{i',j'}=0\qquad(i<i',\ j<j').$$
When it holds, $d_i=\mu_jX_{i,\sigma(j)}/X_{ij}$ is determined up to scale; $d$ is then tested
against $Y$ in the same cross-multiplied form. $\Delta_{\mathcal A}$ is the number of
**distinct** $d$'s, each normalised by $d[0]=1$. Since the map $d\mapsto\sigma$ is injective (a
diagonal $d$ determines its ray permutation), the count never double-counts a group element; in an
early version of the code two different $\sigma$ could produce the same $d$, which inflated a
count, and the normalisation plus deduplication is what removes it.

**Exact version.** When every entry is a 24th root of unity divided by $\sqrt6$, everything is
done in $\mathbb Q(\zeta_{24})$, $\Phi_{24}=x^8-x^4+1$, with $\sqrt6=\zeta+\zeta^{23}+\zeta^5+
\zeta^{19}$; zero tests are exact coefficient tests, so the cross-multiplied minors give a
certificate with no tolerances. The matrices themselves are checked exactly (orthonormality and
$|\langle u,v\rangle|^2=1/6$ for all $u\ne v$).

## 3. Results

Exact ($\mathbb Q(\zeta_{24})$, no tolerances):

| triple | entries | MUB (exact) | $(\Delta_{\mathcal A},\Delta_{\mathcal B},\Delta_{\mathcal C})$ |
|---|---|---|---|
| isolated Fourier triple, Methods Eq. (30) | $\zeta_{24}^{\ *}/\sqrt6$ | yes | $\mathbf{(6,6,6)}$ |
| family centre $\theta=(2\pi/3,-2\pi/3)$, Methods Eq. (31) | $\zeta_{24}^{\ *}/\sqrt6$ | yes | $\mathbf{(3,3,2)}$ |
| same triple, relabelled centre $(4\pi/3,2\pi/3)$ | $\zeta_{24}^{\ *}/\sqrt6$ | yes | $\mathbf{(3,2,3)}$ |

Numerical ($\mathbb C$, tol $10^{-7}$, MUB defect $\le10^{-15}$ at every sampled point):

| sample | $\Delta$ multisets seen |
|---|---|
| 4,600 random interior points of the two-parameter family (13,905 draws, fixed seed 20261115) | $\{1,1,3\}$ only |
| 4,723 in-domain grid points ($120\times120$) | 4,720 give $\{1,1,3\}$; the two labels of the centre point give $\{2,3,3\}$; 1 point lies on the domain boundary $R=0$ and degenerates (entries not flat) |

So: $\Delta$ values lie in $\{1,2,3,6\}$; $\Delta=2$ occurs; $(\Delta)=(1,1,1)$ does not occur
anywhere; and at every $\Delta=2$ instance the other two anchors are divisible by $3$.

## 4. Cross-validation against the source's own table

| source's row | my result | verdict |
|---|---|---|
| "Standard product triple, selected coordinate basis: $\Delta=6$" | isolated triple: $(6,6,6)$, at **every** anchor | confirmed (and stronger) |
| "A special point of the continuous family: $(3,3,2)$, exact with 24th roots" | family centre: $(3,3,2)$ exactly | **confirmed** |
| same row, Smith normal forms $\mathrm{diag}(1,1,1,1,3),\mathrm{diag}(1,1,1,1,3),\mathrm{diag}(1,1,1,1,2)$ | computed from the source's own definition in $\mathbb Q(\zeta_{24})$ (§6): exactly $(1,1,1,1,3),(1,1,1,1,3),(1,1,1,1,2)$, indices $3,3,2$ | **confirmed** — the source's own lattice index reproduces the printed diagonals verbatim |
| "Five generic points of the continuous family: $(3,1,1)$ (numerical)" | 9,300+ sampled interior points: all $(3,1,1)$ | confirmed |
| "changing the coordinate basis is essential and an individual index of two is a real possibility" | yes: at the centre the anchor with $\Delta=2$ is the *third* basis, not the coordinate one | confirmed |

Two remarks the source does not make:

* **The $\Delta=2$ locus is a point, not an open set.** At the centre, $\Delta=(3,3,2)$; at
  $\theta=$ centre $+\delta\cdot v$ for every $v\in\{(1,0),(0,1),(1,1)\}$ and every
  $\delta\in\{10^{-6},10^{-3},10^{-2},10^{-1},3\cdot10^{-1}\}$ the index is already $(3,1,1)$
  (script section (6); reproduced in the note's run).
  This is consistent with the source's own local-divisibility remark (symmetry is a *closed*
  condition, so $\Delta$ can only jump up at special points).
* **The isolated triple is the maximally symmetric triple**: $\Delta=(6,6,6)$. Its symmetry group
  at each anchor is $\mathbb Z_6$, generated by a 6-cycle of the rays, not merely $\mathbb Z_3$.

## 5. What this does and does not prove

* It does **not** prove the source's lemma ($\Delta_{\mathcal A}=2\Rightarrow3\mid\Delta_{\mathcal B},
  \Delta_{\mathcal C}$). That is an audit of the source's §4 argument (directions 1/2 of the
  swarm), not of this note. What it does is remove the possibility that the lemma is *vacuous*
  or *false on the known triples*: it is non-vacuous (a $\Delta=2$ instance exists) and it holds
  there.
* It does **not** replace the classification: "no other $\Delta$-pattern occurs" is a statement
  about the classified list, hence conditional on [WT26a] (and on the four minimum-transition
  balls' certificates).
* The one-line argument of [`m2-dossier.md`](m2-dossier.md) §4 settles the source's central
  question *without* any census: the certified order-three symmetry of every triple forces
  $3\mid\Delta_X$ at some anchor. The census is a check of the source's bookkeeping, not a step
  in the proof.

## 6. Addendum (after the first submission was rejected): the source's own lattice index

The first version of this note claimed the source's Smith normal forms "multiply to" my $\Delta$
without computing them. `m2-explicit-triples.py` section (4) now implements the source's own
definition: exact projection entries $(P_{\mathcal A})_{ij,k\ell}$ in $\mathbb Q(\zeta_{24})$, the
relation vectors $e_i-e_j-e_k+e_\ell$ for the nonvanishing entries, the support lattice inside
$\Lambda_0$, and its Smith normal form. Results (exact, no tolerances):

| triple | anchor | nonzero $P$ entries | relations | Smith diagonal | index |
|---|---|---|---|---|---|
| isolated triple | 0,1,2 | 150 | 42 | $(1,1,1,1,6)$ | 6 |
| family centre $(2\pi/3,-2\pi/3)$ | 0 | 246 | 78 | $(1,1,1,1,3)$ | 3 |
| " | 1 | 246 | 78 | $(1,1,1,1,3)$ | 3 |
| " | 2 | 360 | 120 | $(1,1,1,1,2)$ | 2 |

The three diagonals in the middle rows are **exactly the three the source prints**, in the same
order, and the indices $(3,3,2)$ agree with the ray-permutation computation of §3. So, on these
examples: the source's lattice-index identity $\Delta_{\mathcal A}=[\Lambda_0:L_{\mathcal A}]$,
the source's table, and an independent ray-permutation computation all agree. (This is a check on
examples, not a proof of the identity in general; that is direction 1's business.)

Also corrected in this addendum: my earlier statement that "all three $\gamma_2$ detectors vanish"
was a coding bug and is false, and my citation of MMVW from arXiv v1 rather than the current v2 was
wrong; both are repaired in [`m2-v2-detector.md`](m2-v2-detector.md), which states v1 and v2
separately, evaluates both, and scopes the numerical claims to the sampled representatives.
