# m2 — running log (external-input audit: literature side)

Direction (registered, board id d5): audit the published record used or alluded to by the
primary source, with exact hypotheses, and decide what the project may legally cite.
No other member works on the literature.

## 2026-11-15, session 1 — sources read

Read in full: `attachments/how-do-i-make-ofyz/A promising idea ... .txt` (22 kB) and
`attachments/how-do-i-make-ofyz/Pasted text 1.txt` (code fragment).

External items the source relies on, all fetched and checked at the publisher page:

| cited as | actual | status |
|---|---|---|
| "November 2026 classification preprint of Cardenes Wuttig and Tindall" | arXiv:2611.06917, *Using topology to reveal all mutually unbiased bases in dimension six*, v1 4 Nov 2026 | exists, quant-ph |
| "Sun's work ... nonextension under a corresponding ternary-clock hypothesis" | arXiv:2610.12180, Hao-Yu Sun, v1 8 Oct 2026 | exists, but the hypothesis is narrower than the source implies |
| "work of Matolcsi, Matszangosz, Varga and Weiner" | arXiv:2503.14752, *Triplets of Mutually Unbiased Bases* | exists; contains the prior art closest to the source's Xi identity |
| "arithmetic matroids" | arXiv:1105.3220 (arithmetic matroids, Tutte polynomial, toric arrangements) | exists; general-purpose, not a MUB result |

Headline consequence already posted to the board (finding f1): N(6)=3 is **proved**
(twice, 2026), so the source's route is a route to a *conceptual* proof, not to the theorem.

Details and the exact-hypothesis dossier go to `m2-dossier.md`; the one computation I add
(Delta-tuples on the now-complete classification) to `m2-delta-census.md`.

## 2026-11-15, session 2 — what the literature check found

* `m2-dossier.md` written (exact-hypothesis dossier, 9 external items).
* `m2-delta-census.md` + `m2-explicit-triples.py` written (the only computation I add).
* Corrections to my own first reading: the paper's [13] *is* Brierley-Weigert PRA 79 052316, so
  there is no attribution discrepancy for (H3) — my first pass mis-parsed the reference list of
  the HTML. Fixed before circulating.
* New item the source does not mention: 2611.06917 SM .10 states that every classified triple is
  *strongly unextendible* (no extra vector at all), citing Sun Cor. 9.1 for the continuous family
  and McNulty-Weigert IJQI 10 1250056 (2012) for the product triple. With the classification that
  alone gives N(6)=3, independently of the Jaming et al. quartet exclusion.
* The (3,3,2) example of the source is *reproduced exactly*: at the centre of the continuous
  family (theta_1,theta_2) = (2pi/3,-2pi/3) all entries are 24th roots over sqrt6 and
  Delta = (3,3,2) with no tolerances; the source's printed Smith diagonals (1,1,1,1,3),
  (1,1,1,1,3), (1,1,1,1,2) multiply to exactly that.
* MMVW Conj. 2 verified numerically on family + isolated triple: gamma1 vanishes at all three
  transitions, gamma2 at exactly two of three generically (sharp), at all three only at the two
  symmetric points. Shown *not* to be a formality: with the diagonals D,R,S of Methods Eq. (31)
  replaced by arbitrary unit diagonals the detectors blow up to 1e2-1e4.

## 2026-11-15, session 3 — closed out

Deliverables (all in `results/symmetry-overnight/`):
* `m2-dossier.md` — exact-hypothesis dossier for the nine external items the source uses or
  alludes to, a line-by-line verdict on the source's statements about the literature, the
  one-line proof that (Delta_A,Delta_B,Delta_C)=(1,1,1) is impossible given the published
  order-three symmetry, and the citation list the proof revision may use. Sections 3.6 adds
  proofs of the three elementary facts (equilateral triangle, single equivalence class of
  CHM(3), Good-Thomas F6 = F2 (x) F3).
* `m2-delta-census.md` — the only computation I added: Delta on the now-complete classification,
  exact in Q(zeta_24) at the two root-of-unity triples, numerical over the family.
* `m2-explicit-triples.py` — self-contained reproducible script (numpy only, ~20 s).

Board findings posted under d5: f1 (literature status), f9 (status correction for d3's (13) and
d4's (T1)-(T3)), f10 (strong unextendibility => N(6)=3), f11 (prior art for the Xi identity),
f13 (character-orthogonality mechanism for the MMVW detector; 12 of 20 splits formal for gamma1).

What I did NOT do, and said so: did not complete the last 8 of 20 splits of the MMVW detector;
did not re-derive the support-lattice Smith forms for generic (non-root-of-unity) family members
(the exact SNF is computed only for the isolated triple and the two family centres);
did not machine-check the Good-Thomas / Fourier-family matching of the isolated triple; did not
audit the source's lattice/detector machinery (directions 1/3 of the swarm) nor its order-two
argument (direction 2), beyond checking the resulting Delta bookkeeping.

## 2026-11-15, session 4 — CORRECTION after the first submission was rejected

The judge found a real bug in my MMVW detector: `Gtilde(H, gam)` ignored `gam` and summed the
+-1 splits whatever gamma was, so gamma2 = 3*gamma1 was never evaluated and my claim "all three
gamma2 detectors vanish" was false. Fixed (`mmvw2.py`, now in `m2-explicit-triples.py` section 5,
literal 720-term S_6 sum). Corrected results: gamma1 vanishes at all three transitions (all 20
individual split sums too); gamma2 vanishes at exactly TWO of three generically (at (1.00,4.20):
6.5e3, 4e-26, 2.9e-27), and at all three only at the isolated triple and the family centre. So
MMVW's "two of three" clause is sharp, not slack. My earlier structural remark is right for
gamma1 only: for 3*gamma1 the character-orthogonality parameter T is always 0 mod 3, so nothing
is formal there - consistent with the gamma2 detector genuinely failing at H1.

Also added, in response to "make the advertised checks reproducible":
* section (2) now contains both census drivers (random with a fixed seed: 13905 draws, 4600
  in-domain, all (3,1,1); grid 120x120: 4723 in-domain -> 4720 (3,1,1), one (3,3,2), one (3,2,3),
  one degenerate limit);
* section (4) implements the source's OWN definition: exact 30x30 projection entries, relation
  vectors, support lattice, Smith normal form. It reproduces the source's printed diagonals
  (1,1,1,1,3), (1,1,1,1,3), (1,1,1,1,2) at the family centre, index (3,3,2), and (1,1,1,1,6) at
  each anchor of the isolated triple - so "Smith indices exactly" is now substantiated by the
  script, and it independently confirms Delta = lattice index on these examples;
* section (5) prints the 20 individual split sums per transition.

## 2026-11-15, session 5 — second rejection, new direction d7, and the v2 repair

The second rejection was on the literature side: I cited MMVW arXiv:2503.14752 from **v1** while
naming the current version. Checked at the source: v1 = 18 Mar 2025, v2 = 19 Jul 2025 (current),
and they differ in the *conjecture itself*:

* v1: G_{H_j}(pi g2) = 0 for TWO of the three j; single identity Eq. (4.7) with pairwise products.
* v2: G_{H_j}(pi g2) * G_{H_j^*}(pi g2) = 0 for EVERY j and every pi; Eq. (4.9) pairs each
  transition with its adjoint. And v2's Prop. 4.2 needs Conjecture 2 **and** Conjecture 3.
* Conjecture 3 (new in v2): no S in the Szollosi family X(alpha) is in a quartet. v1 called this a
  theorem ([11] = Chen-Liang-Hu-Chen, QIP 20 (2021) 353, resting on a Chen et al. J. Phys. A 50
  (2017) 475304 lemma); McNulty-Weigert arXiv:2504.13067 (17 Apr 2025) showed that lemma's proof
  "contains a mistake, ultimately invalidating three theorems derived in later publications".

New direction d7 = version-explicit attack on the current conjectures. Done:
* `m2-v2-detector.md`: the v1/v2 comparison table, the Conjecture 3 provenance chain, and both
  versions evaluated at the sampled representatives. Both hold; both are sharp; v2's adjoint
  pairing is exactly what is needed (at (1.00,4.20) H1 fails the gamma2 test only in the column
  orientation, H3 only in the row orientation, H2 in neither).
* Two proved mechanisms: the index mechanism (column sums vanish for splits with
  sum t*gamma_t != 0 mod 3, for any T-covariant matrix) and the parity mechanism (for a transition
  in the [WT26a] Eq. (33) normal form, the ADJOINT gamma-sum vanishes for every pi and every 3+3
  split, because the number of + signs in the b=1 half of the columns is odd). The second is a
  proof of one clause of v2's Conjecture 2 for matrices in that normal form; I did not show every
  transition has that form, so the conjecture stays "verified at sampled representatives".
* Structural remark on Conjecture 3: the (4.2) normal form of X(alpha) has four circulant 3x3
  blocks, hence commutes with C3+C3 and is block diagonal (2,2,2) in the P-eigenbasis while the
  standard basis becomes F3 (x) I2 - the H2-reducibility that [11] was about. Not a proof.
* Script section (5) now tests v1 and v2 separately over all 720 permutations, with per-split and
  per-orientation counts.
