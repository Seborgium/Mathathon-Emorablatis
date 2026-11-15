# Is the threefold-symmetry obstruction a useful result?

> **Revision — after the literature check and the swarm review.** Three corrections supersede
> parts of what follows.
> (i) The note's "October preprint" is **Hao-Yu Sun, arXiv:2610.12180** (8 Oct 2026): in dimension
> six "an amplitude-profile obstruction proves strong unextendibility of a given mutually unbiased
> triple when its original third-basis rays are invariant under the ternary clock". The conditional
> theorem is therefore essentially already in the literature, as the note concedes.
> (ii) The 2009 paper the November preprint imports — **Jaming–Matolcsi–Móra–Szöllősi–Weiner,
> arXiv:0902.0882** — proves that "for any values of the parameters $(a,b)$, the standard basis and
> $F(a,b)$ cannot be extended to a MUB-quartet", i.e. it covers a whole two-parameter family of
> pairs. So the note's theorem is an **independent second proof of a known conclusion, not a
> gap-filler**; §5 and §7 below overstate its value accordingly.
> (iii) The technique does not generalise: the $3\times3$ sign lemma is **false at four blocks** —
> $M=\tfrac12[(-1,-1,-1),(-1,1,1),(1,-1,1),(1,1,-1)]$ has zero column sums, every row on
> $x^2+y^2+z^2-2xyz=1$ and $\max|\text{entry}|=1/2$ — so $1/\sqrt2$ is $d=6$ numerology.
> What survives: the proof itself (correct, short, machine-free), the sharp constants
> ($1/\sqrt2$ for the lemma — sharp, not improvable; $1/108$ in §8), and an explicit realisation
> of the hypothesis
> ($A=\mathbb 1_6$, $B=X\otimes D(h_0)$, $C=Y\otimes D(h_0u)$ with $u=(1,\omega,\omega)$).

Audit of the 15 KB note *"I found a useful analytic route, but I have not completed a
non-computational proof for four arbitrary bases"* (attachment `is-this-a-useful-r01i`),
against the literature and against numerics. Checks: `results/verify-symmetric-obstruction.py`.

## 1. Verdict

**The conditional theorem is correct, and the proof is short, complete and machine-free.**
What it proves is: *no MUB triple in C^6 carrying an order-three symmetry of the stated type
can be extended by a single vector.* That statement is not new (it is a consequence of the
2009 Fourier-family exclusion of Jaming–Matolcsi–Móra–Szöllősi–Weiner, which the November
preprint 2611.06917 imports verbatim as the last step of its proof). **The proof is new**, it
needs nothing but the symmetry, and it covers both known types of d=6 triple uniformly — more
than the 2012 McNulty–Weigert theorem, which covers product triples only.

It is therefore a real but narrow contribution: it converts the *final* step of the
topological route to N(6)=3 from a cited 2009 analysis of the Fourier family into one page of
elementary algebra. It does not touch the step where the difficulty — and all the certified
computation — actually lives.

## 2. What is actually proved

Let ω = e^{2πi/3}, T = diag(1,1,ω,ω,ω²,ω²) = I₂ ⊗ diag(1,ω,ω²) under C^6 ≅ C² ⊗ C³ with
block coordinates x = (x₀,x₁,x₂), x_j ∈ C². T has order 3, so its orbits on a basis are
(6 fixed) / (3 fixed + one 3-cycle) / (two 3-cycles).

Hypothesis: A, B, C are MUBs with T fixing every vector of A up to phase and cycling the
vectors of B and of C in two 3-cycles each. Conclusion: **no unit vector is unbiased to all
three bases.**

Proof structure, as given in the note and checked here:
1. §2 normalises A = standard and u = 6^{-1/2}(1,…,1); the 3-point DFT then forces
   ⟨u_j,v_j⟩ = 0, i.e. v_j = ν_j 6^{-1/2}(1,−1). This is the analytic normal form that the
   November preprint reaches as its Eq. (33) — the two agree. **But the normalisation step as
   written is wrong**: block-scalar rephasings commuting with T are diag(μ₀,μ₀,μ₁,μ₁,μ₂,μ₂), one
   phase per block, so they preserve the ratio a_j/b_j inside a block and cannot flatten a general
   flat u. The repair is immediate — the commutant of T is U(2)³, and a blockwise U(2) sends each
   u_j to (1,1)/√2 while keeping T and keeping the new A a T-eigenbasis — but "rephasing" must be
   replaced by "a blockwise unitary commuting with T". Small gap, real gap.
2. §3 turns unbiasedness into a condition on three angles: constant DFT power ⇔ vanishing
   cyclic autocorrelation, so the *products* z_j \bar z_{j+1} close into a triangle. That yields
   "admissible" angle triples: Σcos²θ_j = 3/2 plus two triangle conditions on
   {|cos θ_j cos θ_{j+1}|} and {|sin θ_j sin θ_{j+1}|}.
3. §4 feeds a hypothetical fourth vector through the same machinery: α, β and β−α would all
   have to be admissible. The phases λ_j, ν_j cancel — this is the step that makes the complex
   problem nine real angles.
4. §5 Heron on the cosine and the sine triangle gives s + 4|t| + s²/12 ≤ 1 (s = Σv_j²,
   t = v₀v₁v₂, v_j = cos 2θ_j), whence |v_j| < 1/√2.
5. §6 the 3×3 matrix M with rows (cos 2α_j, cos 2β_j, cos 2(β_j−α_j)) has zero column sums,
   |entry| < 1/√2 and every row on the surface x²+y²+z²−2xyz = 1. No such M exists: rows have
   negative product, columns are flipped to one negative each (an even number of flips), a row
   (−a,b,c) then forces b+c > a, so rows sum positive while columns sum to zero.

Every step survives checking. Two expository gaps (not errors): §3's "three complex numbers add
to zero" are the products z_j \bar z_{j+1}, not the z_j; and the degenerate cases cos θ_j = 0 or
sin θ_j = 0 cannot occur for an admissible triple (if cos θ₀ = 0 then u₀ = u₂ = 0, hence
u₁ = 0, hence cos θ₁ = cos θ₂ = 0, contradicting Σcos² = 3/2) — worth saying explicitly, since
the note bounds |v_j| < 1/√2 but never rules out v_j = 0.

## 3. What the numerics say (script output)

| check | result |
|---|---|
| Parseval / Fourier observation | holds (sum of squared DFT outputs = 3·Σ|z_j|²) |
| crux: row identity + zero column sums, all \|entry\| < 1/√2 | **no solution**; 250 random-start solutions all have max\|entry\| ≥ 0.7608 |
| constant of the 3×3 lemma | **1/√2, sharp — corrected, see §10.** The infimum of max\|entry\| is 1/√2, approached but not attained, so the note's strict inequality is essential. The value √3−1 recorded here earlier was a local optimum of my search, not the optimum |
| Heron inequality on 20 000 random admissible triples | no violations; largest \|cos 2θ_j\| seen 0.6809 (so the sup is ≈ 0.681, i.e. 1/√2 has ≈4% slack) |
| fourth vector for the two-parameter family (3 parameter points) | triple is MUB, T-orbits (6 fixed)/(3,3)/(3,3); best max-deviation of \|⟨·,h⟩\|² from 1/6 over 120 restarts: 0.052 |
| fourth vector for the isolated Fourier triple (2611.06917 Eq. 30) | same orbit pattern; best max-deviation 0.054 |
| positive control, d = 3 (where 4 MUBs exist) | the same optimiser finds 0.0 — so the 0.05 floor is not an artefact |
| §8: Σ(p−1/6)² ≥ 1/108 | holds; minimum over the family exactly 1/108, attained at a = (1,−1,−1), b = i(1,−ω,−ω²), probabilities 4×(5/36) + 2×(2/9) as claimed |

So the note's own account of its state is accurate: the mechanism is proved, the hypothesis is
not.

## 4. Where it sits: the two claimed proofs of N(6)=3

**Route A — OpenAI (24 Sep 2026), the preprint this project is about.** 112 bins of nine phases,
Stage A/B compression to U(2), then a finite graph search (two disjoint 6-cliques in O/U
vector-ball graphs) over 23 506 Stage-C records, no symmetry assumption anywhere.
*The note contributes nothing to this route*: it never classifies triples, so it never has a
symmetric triple to exclude. This is not a criticism of either side — the two proofs are
differently shaped. But if the question is "how does this bear on the solution of the problem
as this project understands it", the honest answer is: not at all.

**Route B — Cárdenes Wuttig & Tindall, arXiv:2611.06917 (4 Nov 2026).** The note's
"November preprint" is real and claims exactly the symmetry the note isolates:
- connectedness of all order-six complex Hadamard matrices except Tao's (Lean-formalised),
  2 775 interval-certified phase balls, and inside each ball either a graph search or a proof
  that every triple carries the order-three symmetry T = diag(1,1,ω,ω,ω²,ω²);
- an *analytic* classification of symmetric triples (SM §8.5): every triple with that symmetry
  is in the two-parameter family (Jaming et al. 2009) or is the isolated Fourier triple;
- and then: "Both types of triple contain a pair related by a matrix in the Fourier family,
  which has been excluded from a quartet [34]."

So the step that finishes the proof is an imported exclusion from a 2009 paper — different in
form from the note's theorem (it constrains a *pair* of bases of the triple, not the symmetry of
the triple) but serving the same purpose for exactly the same two types. **The note is a
self-contained elementary replacement for that import.** Both known types have the note's
symmetry with the same orbit pattern — verified numerically here on the two-parameter family
and on the isolated Fourier triple of Eq. (30) — so one argument covers both, and covers more
than McNulty–Weigert 2012 (arXiv:1203.6887), which is product triples only.

## 5. So: is it useful?

Useful as a **replacement for a trusted import**, not as progress on the open step.

- It makes the final exclusion in Route B elementary, human-checkable, and independent of the
  Fourier-family theory of 2009. In a proof whose remainder is 2 775 interval-certified balls
  plus a Lean-formalised connectedness theorem, deleting one non-trivial imported analysis is
  real value — and it is the kind of value that survives: the argument does not care about the
  two-parameter structure, only about the symmetry.
- It does **not** shorten or weaken the computational part by one byte, and the note says so.
- Its §8 is a clean sharp statement (a genuine 1/108 gap, attained) and is a quantitative
  strengthening of the 2012 product-triple result; the note is right that it should be checked
  against the literature before being claimed.

Missed opportunity in the note's framing: it presents itself as "an obstruction looking for a
rigidity proof". The stronger and better-supported framing is the converse — "**all known d=6
triples are unextendible, elementarily**", i.e. the last step of Route B, self-contained. That
is a claim the note can actually make, today, without the missing rigidity.

## 6. How large is the missing step?

Not a lemma to be filled by cleverness. "Every MUB triple in C^6 has this symmetry" is the
conjecture of Matolcsi–Matszangosz–Varga–Weiner (numerically searched, only the two types
found), and it is what Route B proves by covering the Hadamard space. Two structural reasons a
cheap argument will not do:

- **Dimension.** Symmetric triples already form a two-parameter family and the classification
  says the whole moduli space of triples is two-dimensional. A dimension count cannot force the
  symmetry; the statement is that the known family is *everything* — a rigidity/covering
  statement, not a generic-position statement.
- **Coverage.** The certified cover is over the space of order-six complex Hadamards, i.e. over
  the transition matrix of a pair of bases, not over triples. Any analytic proof of the
  symmetry must decide, for every complex Hadamard H, whether a third basis exists — which is
  the classification problem itself.

## 7. Three things worth doing with it

1. **Retarget the write-up** as in §5 and drop the "route" framing: state and prove
   "every d=6 MUB triple with an order-three symmetry is unextendible", note that both known
   types have the symmetry, and note that this replaces the [34] import in Route B. That is a
   lemma a referee can check in ten minutes and it is the note's actual asset.
2. **There is no slack in the lemma** (corrected, see §10): 1/√2 is sharp, so the sign step cannot be
   weakened. What is not sharp is the Heron input — admissibility numerically gives
   max_j|cos 2θ_j| ≤ 0.681 against the 1/√2 the lemma allows (sup not established, only bounded above
   by 1/√2). So if a simplification exists it must come from the Heron side, not from relaxing 1/√2.
3. ~~**Quantify it.**~~ **Retired — see the addendum at the end.** The single-vector floor is
   ≈ 0.05 for every known triple, but it is ≈ 0.03–0.05 for a *random* triple of orthonormal
   bases too, so it measures nothing about extendibility. The quantitative version has to be
   stated about bases — six mutually orthogonal unbiased vectors — not about one vector.

## 8. Status of the note's own claims

| claim in the note | status |
|---|---|
| symmetry obstruction (§2–§6) | correct; proof checked line by line and numerically |
| 1/√2 bound on \|cos 2θ_j\| | correct, not sharp (true sup ≈ 0.681) |
| 3×3 sign argument | correct; sharp constant √3−1, not 1/√2 |
| §8 1/108 inequality | correct and sharp; equality case reproduced exactly |
| "the conditional theorem is not new" | correct: Sun, arXiv:2610.12180; and implied for the known triples by Jaming et al., arXiv:0902.0882 |
| "arXiv:2611.06917 proves the symmetry computationally" | correct: 2 775 certified balls + Lean-formalised connectedness; Methods §V.4 states the symmetry verbatim, SM §8.5 the classification |
| "an October preprint gives an analytic obstruction under a related symmetry hypothesis" | correct, and identified: Hao-Yu Sun, arXiv:2610.12180 (8 Oct 2026) |

## 9. Addendum: the single-vector conclusion is generic, which retires the "quantify it" idea

Measured twice (swarm member m4; repeated here independently): three Haar-random triples of
orthonormal bases in C^6 — not MUB, no structure — admit **no** unit vector unbiased to all three
(max-deviation floors 0.033, 0.050, 0.052 over 150 restarts each), while a triple sitting inside a
complete set of MUBs in d=5 does (floor 3·10⁻⁸). So "no single $h$" is a codimension-5 condition
satisfied by essentially every triple of bases, and by itself it says almost nothing about
extendibility. In particular the ≈0.05 floor of the symmetric triples is numerically
indistinguishable from that of a random triple: the single-vector floor is not a discriminator.

So a quantitative version of the obstruction must be stated about **bases** — six mutually
orthogonal unbiased vectors — not about single vectors. Proving a positive lower bound on the
single-vector gap would establish something already true of every triple of bases, which is why
§7.3 is struck out.

## 10. Correction: 1/√2 is sharp (a number I gave earlier was wrong)

I reported √3−1 ≈ 0.732051 as the infimum of max|entry| over the matrices of the 3×3 lemma. That is
wrong. Swarm member m3 produced an explicit circulant family —
M = [[−S,−b,−c],[c,S,−b],[b,−c,S]] with b+c = S and bc = (2S²−1)/(2−2S) — which satisfies zero
column sums and the row identity *exactly* for every S in (1/√2, √3−1], with max|entry| = S. Verified
here at S = 0.708, 0.710, 0.715, 0.720, 0.725, 0.7320508: column sums 0 to 10⁻¹⁶, row-identity
residual 0, max|entry| = S. At S = 1/√2 the family degenerates to a matrix with an entry exactly
zero, so the infimum of max|entry| is 1/√2, and it is not attained.

Consequences. The note's strict inequality |entry| < 1/√2 cannot be weakened: 1/√2 is the sharp
constant of the lemma, and there is no slack in the sign step. The √3−1 I reported came from a
minimisation whose starting points were not diverse enough to see the family; the symmetric extremal
matrix I exhibited is a member of a larger family, not its boundary. What is *not* sharp is the Heron
input — the admissible triples I sample reach only max|cos 2θ_j| ≈ 0.681 against the 1/√2 the lemma
allows (m6 gives the closed form √(2√3−3) ≈ 0.68125, consistent with my sampling to 3·10⁻⁴; I have
not re-derived it) — so the only direction in which this argument could be simplified is the Heron
step.

The sign step itself is now machine-checked: m3's Lean file
(`.ultramath/smwgxyj9c/m3/lean/SignStep.lean`) compiles under `lean` on this VM, exit 0.
