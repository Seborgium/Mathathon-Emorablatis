# m3 report — the Heisenberg-covariant slice of the C^6 problem

Member `m3`, swarm `smwhnslql`, direction `d6`. Companion documents:
[`m3-covariant-bound.md`](m3-covariant-bound.md) (full proofs and certificates) and
[`m3-log.md`](m3-log.md) (running log). Scripts: [`m3-scripts/`](m3-scripts/).

## 1. Result

**Theorem (proved here, exact certificate attached).** Let $B_1,\dots,B_k$ be pairwise
unbiased orthonormal bases of $\mathbb C^6$ that are eigenbases of maximal abelian
subgroups of the Weyl–Heisenberg group $H(\mathbb Z_6)=\{\omega^\theta X^aZ^b\}$,
$\omega=e^{2\pi i/6}$. Then $k\le 3$, and $k=3$ is attained.

The proof is five short steps, none of them computational:

1. an abelian $M\le H$ has $|M| = |M\cap Z(H)|\cdot|\pi(M)| \le 6\,|\pi(M)|$, with equality
   for maximal abelian $M$ (maximality forces $Z(H)\subseteq M$), and
   $\pi(M)\subset\mathbb Z_6^2$ isotropic;
2. every isotropic subgroup of $\mathbb Z_6^2$ has order $\le 6$; if $\pi(M)$ sat properly
   inside a larger isotropic $S$, then $\pi^{-1}(S)\supsetneq M$ would be abelian, so for
   maximal $M$ the image $\pi(M)$ is maximal isotropic, of order 6. Hence maximal abelian
   subgroups are exactly the preimages of the 12 isotropic subgroups of order 6;
3. by CRT, $\mathbb Z_6^2\cong\mathbb Z_2^2\times\mathbb Z_3^2$, so those 12 are the pairs
   of lines $\mathbb P^1(\mathbb Z_2)\times\mathbb P^1(\mathbb Z_3) = 3\times 4$, and
   $M\cap M' = Z(H)$ iff both lines differ;
4. **key step, proved not cited:** if two stabiliser bases are unbiased then
   $M\cap M' = Z(H)$ (apply a common element $h$ to $u=\sum_\psi c_\psi v_\psi$; all
   $|c_\psi|^2 = 1/6 \ne 0$ force all six characters of $M'/Z(H)$ to agree on $h$);
5. hence the bases give a partial Latin square in a $3\times 4$ array: $k\le\min(3,4)=3$.

Three bases attain it: the standard basis, the eigenbasis of $X$ (Fourier) and the
eigenbasis of $XZ$; all $3\cdot 36$ overlaps equal $1/\sqrt6$ exactly (verified in
$\mathbb Z[\zeta_{24}]$; exponent matrix for $XZ$ in the companion file).

**Status of the conclusion.** "No four MUBs of $\mathbb C^6$ related to the Heisenberg
group" is *known*: Grassl (arXiv:quant-ph/0406175) proves maximality of the
Fourier-type triples, Brierley–Weigert (arXiv:0901.4051, PRA 79, 052316) find at most two
partners for a prescribed Hadamard. This note contributes a self-contained proof and exact
certificates, not priority. (Full literature audit: member `m2`.)

## 2. What the exact computations also settle

| statement | status |
|---|---|
| $H(\mathbb Z_6)$ has exactly 12 maximal abelian subgroups, all of order 36, preimages of the 12 maximal isotropic subgroups of $\mathbb Z_6^2$ | proved (Lemma 1) + enumerated |
| unbiased $\iff M\cap M'=Z(H)$ for all 66 pairs of the 12 subgroups | proved one way (Lemma 3), verified both ways exactly |
| exactly 24 pairwise unbiased triples of stabiliser bases, no quadruple; all 24 are $SL(2,\mathbb Z_6)=Sp(2,\mathbb Z_6)$-equivalent (order 144, transitive on lines and triples) | proved + verified |
| every covariant triple of flat bases has $(\Delta_A,\Delta_B,\Delta_C)=(6,6,6)$ | exact computation, 6 triples × 3 anchors |
| the source's formula (5) $\Delta_X = [\Lambda_0:L_X]$: support-lattice Smith form diag$(1,1,1,1,6)$, index 6 at every one of those 18 anchor instances | exact computation |
| $\operatorname{rank}_{\mathbb F_3} R_X = 4<5$, i.e. $\Xi(P_X)=0$, at every anchor of the six flat covariant triples | exact computation, 18 anchors |
| source table row "standard product triple, $\Delta=6$" | confirmed |

## 2b. Cross-checks of other members' computations

* **m5 (`d2`), the $(2,3,3)$ family.** Rebuilt the source's §4 "uniform case" family
  independently and recomputed $\Delta$ *from the definition* (all $6!$ permutations,
  exact field inverses in $\mathbb Q(\zeta_{24})$) instead of from Smith forms.
  Reproduced: the $162$ candidate $H = FD\Pi$, of which exactly $108$ have $HF$ flat;
  $(I,U,V)$ is a MUB triple for every sampled pair; the $\Delta$-patterns take exactly the
  two values $(6,6,6)$ (7/10) and $(2,3,3)$ (3/10), including $\Delta_A = 2$.
  Also: $\operatorname{rank}_{\mathbb F_3} = 5$ at the $\Delta=2$ anchor and $4$ at the
  $\Delta=3$ anchors, so the source detector fires as claimed ($\Xi>0$, $0$, $0$).
  So m5's numbers stand under an independent method. (My own first attempt at the
  rank-one test was wrong and produced $\Delta=0$ everywhere — see the log.)
* **m4 (`d3`) and m6 (`d4`), the identity.** Their conclusion that
  $\Xi_A\Xi_B\Xi_C=0$ is equivalent to "every triple has an order-3 clock at some anchor"
  is consistent with everything computed here: every triple examined in this run
  (covariant, $(6,6,6)$, $(2,3,3)$) has a clock at at least one anchor, and the one
  triple family with $\Delta_A = 2$ has $\operatorname{rank}_{\mathbb F_3}=5$ there, i.e.
  $\Xi_A>0$ — exactly the profile their equivalence predicts.
* Not attempted: independent recomputation of m6's normal-form analysis or m1's
  detector audit; those need their own files.

## 3. What this means for the symmetry route

* **Scope of the exact $\Delta$ statement.** Corollary 2 is asserted for the six flat
  covariant triples (18 anchors) only, where $\Delta$ was computed from its definition. The
  remaining 18 triples contain a base that is not flat; there an extension would need the
  (standard, cited) Weil lift of $SL(2,\mathbb Z_6)$ together with unitary invariance of
  $\Delta$, and is deliberately not claimed.
* The six flat covariant triples are **maximally symmetric** ($\Delta=6$ at every anchor):
  they give the identity $\Xi(P_A)\Xi(P_B)\Xi(P_C)=0$ for free ($0\cdot0\cdot0$), so these
  examples cannot test it; a useful test needs a triple with an anchor of index 1 or 2.
* The obstruction that closes the covariant class at three is *not* the order-3 clock. It
  is the scarcity of isotropic lines over the **smaller prime factor**: three lines in
  $\mathbb P^1(\mathbb Z_2)$. A fourth covariant basis would need a fourth
  $\mathbb Z_2$-line. This is worth separating from the source's narrative, in which the
  factor $3$ comes from the order-two-to-order-three mechanism.
* The same argument gives, for squarefree $d=p_1\cdots p_r$, the bound
  $\min_i (p_i+1)$ on the number of pairwise unbiased stabiliser bases; for prime powers
  the count is $d+1$, so this is a composite-dimension phenomenon. (Presumably folklore;
  recorded with proof, not claimed new.)
* Independently re-proved details of two load-bearing steps of the head file, with the
  missing line supplied: $\Delta_X\in\{1,2,3,6\}$ (free action), and the recovery lemma
  (the term $\operatorname{tr}(Y^2)/d$ is independent of $i$ because
  $Y^2=\mathrm{diag}_{\mathcal C}(x^2)$). The chain "commuting diagonal unitaries
  $=$ characters of $\Lambda_0/L_X$ $\Rightarrow$ ray-set symmetries $\Rightarrow$
  $\Delta_X = [\Lambda_0:L_X]$" needs also the no-exchange lemma, which member `m1`
  proved (finding f15); with it, the source's formula (5) is rigorous, and my 18-anchor
  computation confirms it numerically-exactly in the covariant case.

## 4. Not claimed, not done

* **This does not prove $N(6)=3$, and no step of it touches a triple that is not a
  stabiliser basis.** The order-3 stratum studied in `results/order3-stratum.md`, the
  source's $(3,3,2)$ example, and m5's $(2,3,3)$ family are not covariant.
* The 18 covariant triples containing a non-flat base were not run through the
  $\Delta$-computation (they need $\mathbb Z[\zeta_{36}]$ or $\mathbb Z[\zeta_{72}]$).
  They are pairwise unbiased by Lemma 3, but Corollary 2 is asserted only for the flat six.
* Numerical work: one floating-point cross-check of the exact unbiasedness table
  (`m3-scripts/numcheck.py`); everything else is exact integer arithmetic.
* Priority: none claimed (see §1).

## 5. Files

* [`m3-covariant-bound.md`](m3-covariant-bound.md) — full statement, proofs, certificate data, file table.
* [`m3-log.md`](m3-log.md) — running log, including three coding errors found and fixed
  (they are the kind of error that silently fakes a symmetry index, so they are logged).
## 6. Revision log (after the first submission was returned)

Four corrections, all in this direction and all applied to `m3-covariant-bound.md`:

1. $|M| = 6|\pi(M)|$ was stated for arbitrary abelian $M$; corrected to
   $|M| = |M\cap Z(H)|\cdot|\pi(M)|\le 6|\pi(M)|$ with equality for maximal $M$, and
   Lemma 1(iii) now contains the explicit extension argument (a larger isotropic $S$ would
   give a larger abelian $\pi^{-1}(S)\supsetneq M$).
2. $GL(2,\mathbb Z_6)$ (order 288) is replaced by $SL(2,\mathbb Z_6)=Sp(2,\mathbb Z_6)$
   (order 144) everywhere. Only $\det = 1$ preserves the commutator form and hence lifts to
   unitaries; the script was changed accordingly and re-run: one orbit on the 12 lines and
   one orbit on the 24 triples, as before.
3. The commutant argument in Lemma 3 ("$\mathrm{commutant}(\rho(M)) = \rho(C_H(M))$" via
   Burnside) is replaced by a direct proof: $H$ permutes the $M$-characters, the stabiliser
   of an occurring character is $C_H(M) = M$, so the orbit has size $|H/M| = 6$, all six
   characters occur, and the six weight spaces are one-dimensional. The all-12 exact
   verification is retained as independent corroboration.
4. The rank/$\Delta$ claims are explicitly scoped to the six flat covariant triples
   (18 anchors); the extension to all 24 is presented only as a remark resting on the
   cited Weil lift.

* [`m3-scripts/`](m3-scripts/) — 17 scripts. Reproduce:
  `cd m3-scripts && TMPDIR=. python3 wh2.py && python3 latin.py && python3 cov.py &&
  python3 verify_joint.py && python3 delta3.py && python3 index3.py && python3 rank3.py &&
  python3 clifford.py`.
