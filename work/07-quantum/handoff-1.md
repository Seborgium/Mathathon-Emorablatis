# handoff-1 — T7 (quantum framing) to T8 (the single final file)

> This is **m1's** handoff. All three members of this swarm were asked for a
> `handoff-1.md`, so this filename may be overwritten by a sibling. If the text
> below does not mention "m1", an identical copy is preserved at
> `work/07-quantum/handoff-1-m1.md`, and the framing files it refers to are
> `application-ab.md`, `status-paragraph.tex` and `references.addition.m1.bib`.

from: T7 / swarm smwgrr7ia / member m1 (direction d2)
to: T8 (paper writer); copy to T0 (integration desk) — §5 contains a
    correction to decision D1 that T0 must arbitrate
version: 1
depends-on: the 24 Sep 2026 preprint §1, §7, Appendix A.1 and its bibliography;
    `results/proof-claims.md`; `results/code-audit.md`; the published archive
    listing checked 2026-11-14 (see §5)
blocks: G5 — the abstract and introduction of `work/08-paper/mub6.tex` cannot be
    written until the status wording of §2 is adopted
artefacts:
    work/07-quantum/application-ab.md      framing parts (a) and (b); spliced into
                                           application.md, then into the new §1
    work/07-quantum/status-paragraph.tex   two paste-ready paragraphs (abstract,
                                           introduction)
    work/07-quantum/references.addition.bib  new BibTeX entries with URLs
    (other T7 members supply parts (c) and (d) as separate files in this directory)
claims touched: Theorem 1.1 and its three antecedent conditions; Lemma 1.2;
    Corollary 1.3; the abstract's "four arbitrary complex bases"; the phrase
    "resolving Zauner's dimension-six MUB conjecture"; the $d+1$ bound as used
    in the introduction

---

## 1. Where each block goes

| artefact | destination in `work/08-paper/mub6.tex` | budget | must sit next to |
|---|---|---|---|
| `status-paragraph.tex`, block (1) | abstract, as its last sentence or two | 6 lines | nothing else in the abstract should restate conditionality; delete any duplicate |
| `status-paragraph.tex`, block (2) | end of §1, after the historical scope and before the strategy section | ½ page | must precede the strategy section, so the reader knows what is conditional before seeing how it is proved |
| `application-ab.md` §(a) a.1–a.4 | new §1.1 "Physical meaning" (or a standalone §2 if §1 is kept short) | 2–2½ pp | immediately after the definition of $N(d)$; before any statement of the theorem |
| `application-ab.md` §(b) b.1–b.2 | new §1.2 "What is and is not established" | 1½ pp | directly after Theorem 1.1 |
| `application-ab.md` §(b) b.3–b.5 | continuation of §1.2, or a short §8 "Scope of the result" | 1 p | after the proof of the main theorem, before the appendix |
| `application-ab.md` §(b) b.6 | a footnote at first mention of the result, or the related-work paragraph | 4 lines | where the Nov 2026 preprint is first mentioned |
| `application-ab.md` §(b) b.4 | the verification appendix, opening paragraph | ½ p | at the head of the appendix, before the arithmetic contract |
| `application-ab.md` §(b) b.7 | abstract, replacing one clause | 0 | — |
| `application-c…` and `application-d…` (other members) | as `application.md` §§2–3 and the related-work paragraph | per their handoffs | do not merge (a)+(b) and (c)+(d) into one long section; the reader path needs (a) physics → (b) status → (c) use → (d) literature or (d)→(c) |

Page budget for the whole T7 material: **4–5 pages**. If the paper has to shrink, cut
`b.6` first, then `a.3`'s qubit example, and never cut `a.2` or `b.1–b.2`: those carry the
derivation of the bound and the conditionality, which are the two things the document
currently lacks.

Notation to keep identical (T1's `notation.tex` will fix the final forms): $N(d)$,
$H$, $E^B_j=P^B_j-I/d$, $H_0$, $\theta^B_j=p^B_j-1/d$, and the phrases "condition (A)
arithmetic model", "(B) execution", "(C) implementation" — T8 should use those three
labels consistently, because every downstream warning in §3 refers to them.

## 2. The status wording — adopt, do not paraphrase

`status-paragraph.tex` is written to be pasted, not rewritten. Two reasons it is worded as
it is:

1. **It names the antecedent, not the confidence.** Sentences of the form "this is a
   computer-assisted proof, which is standard in the field" concede nothing and inform
   nobody. The antecedent has three parts of three different kinds (a model, an event, a
   conformance claim), and stating them is the whole content of the status.
2. **It keeps the lower bound out of the conditional.** $N(6)\ge3$ is elementary and
   unconditional. An abstract that makes the entire theorem sound conditional underclaims;
   the field's current belief in $N(6)\ge3$ does not depend on any computation.

Every place the upper bound appears — abstract, introduction, theorem, conclusion,
caption of the summary figure, any sentence in (c) about reuse — must carry "conditional"
or an explicit cross-reference to the paragraph that states the conditions. The paper's
own abstract is already careful ("under the stated binary64 arithmetic and compiler
conditions"); the risk is that the rebuilt document, which will be shorter and more
assertive, drops the qualifier in the summary.

## 3. What must not be overstated

Each line gives the sentence to avoid and the defensible replacement.

| do not write | write |
|---|---|
| "resolves Zauner's conjecture" | "establishes $N(6)\le3$, hence $N(6)=3$, subject to (A)–(C)" |
| "Zauner's conjecture" (unqualified, anywhere) | "Zauner's dimension-six MUB conjecture". Unqualified, the phrase means the SIC-POVM statement (Weyl–Heisenberg fiducial, Zauner unitary); a reader outside MUB theory will read it that way and conclude something about SICs was proved. Nothing about SICs is proved here. |
| "excludes four arbitrary complex bases" (current abstract) | "excludes every quartet", or "excludes an extension of any pair of bases by two further bases" |
| "We prove $N(6)=3$" with no qualifier in the same sentence | "We prove $N(6)=3$, conditionally on (A)–(C) as stated in §7.1 and Appendix A" |
| "a computer-assisted proof, as is now standard" | delete. The relevant comparison is not other computer-assisted proofs but what a referee can check; a single sentence saying what is and is not checkable does the work. |
| "the proof classifies the MUB triples of $\mathbb{C}^6$" | nothing of the kind: $N(6)=3$ is a maximum, and an infinite family of inequivalent triplets is known [paper [15]] |
| "the only / the definitive / the first proof" | "one of two independent computer-assisted arguments now reporting the same answer" (see §4) |
| "verified" / "formal verification" / "certified" as a description of the whole | "computer-assisted, conditional"; reserve "certified" for the individual inequalities the paper proves, never for the pipeline as a whole |
| "the code has been audited" | it has not. `results/code-audit.md` audits the *specification* in prose; say so in those words. |
| "settles the problem for composite dimensions" | it settles $d=6$ only. The methods are $d$-specific ($2+4$ split, 36 phases, 12 vectors, six-cliques, $12^5$ bins). |
| "the argument applies to all $d$" or any $d=10$ extrapolation | nothing transfers without new work; see (c) |

Two further traps, both of which have appeared in project artefacts:

* **"unconditional upper bound".** Nothing in the paper is unconditional except the
  reduction lemmas. If T8 needs a single sentence of the form "what is unconditional is
  ...", it is: Lemma 1.2, and the covering/exclusion lemmas of §§2–6 as implications.
* **"three MUBs is the maximum, so the tensor construction is optimal".** Optimal in
  cardinality, not extremal in any other sense: triples are not unique, and $N(6)=3$ says
  nothing about how many MUB vectors can be adjoined to a given pair (the
  unextendibility questions), which is where the remaining physics interest sits.

## 4. What to say about the second, independent argument

`application-ab.md` b.6 records two 2026 preprints by Cárdenes Wuttig and Tindall
(arXiv:2608.18053, order-six Hadamard classification; arXiv:2611.06917, an independent
topological argument that no four MUBs exist plus a classification of triples). The second
one appeared **ten days before this swarm started**. Handling:

* mention it in related work, in one sentence, with the explicit hedge that it is an
  unrefereed preprint whose proofs we have not read;
* do **not** use it as corroboration ("independently confirmed") — that would be
  outsourcing the load-bearing judgement of one preprint to another;
* do **not** omit it: a document dated after 4 Nov 2026 that presents this as the only
  argument will be read as either careless or dishonest, and either reading hurts the
  paper's credibility more than the hedge costs.

## 5. Correction to the project premise (for T0 to arbitrate)

`results/plan.md` and `work/00-lead/decisions.md` D1 rest on: "the seven sources, the
execution archive and the certificates are not available". That is true of the packet
(the PDF alone) and **false of the world**. Checked 2026-11-14 via the GitHub API:

* repository `github.com/openai/math`, directory
  `preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/`,
  containing the PDF (817,737 bytes — byte-for-byte the same size as the packet copy),
  `build/`, and `verification/`;
* `verification/code/` contains **only** `extraction.json` — a manifest of file name, byte
  length and SHA-256 for seven files. It contains no code.
* `verification/saved-run/compiled-build/source/` contains the seven sources plus an
  arithmetic probe: `seed.cpp`, `covout.cpp`, `ub.cpp`, `patchx.cpp`, `atlas.cpp`,
  `stageB.cpp`, `stageC.cpp`, `abi-fp-probe.cpp`. Every byte length matches the manifest.
  There is also `build.sh`.
* `verification/saved-run/` contains `VERIFY.md` and an `execution/` directory described
  there as holding the numerical records, `commands.json`, `results/`, and a
  `check_records.py` consistency checker.
* `VERIFY.md` states that the directory contains "no compiled programs, archive
  inventories, hash checks, raw process logs, machine/session records, supervision code, or
  review narratives", and that the checker is "a numerical consistency check, not an
  authentication of the historical archive, a proof of the C++ implementation, or a
  verification of compiler and hardware behavior."

What this changes, and what it does not:

* **Changes:** condition (C) is *inspectable*. The framing text must not say the sources are
  unavailable; it must say they are published and (for this project) not inspected. Any
  team whose statement depends on "we could not read the code" (including
  `results/code-audit.md`'s scope paragraph and T2/T3's need for a reference
  implementation) is stating something about this project, not about the paper.
* **Does not change:** condition (A) is still an assumption in the authors' own words;
  condition (B)'s provenance evidence is still unpublished (no logs, no hash-checks, so
  Table 2 remains unverifiable); and no one has read the sources. Nothing in this handoff
  rests on their content.
* **Suggested action for T0:** amend D1's first sentence to "not in the packet; published
  at <URL> and not inspected by any team", and decide whether T2/T3 should now read them.
  That decision is not T7's, and T7 has not read them.

I did not fetch, read, build or run anything from that repository beyond the directory
listings, the two small text files quoted above, and the file sizes. Anyone writing about
the code must say the same.

## 6. Assembly of `application.md`

`application.md` is the concatenation, in this order:

1. `application-ab.md` → §(a) physical meaning, §(b) what the theorem says;
2. the (c) file from the usability direction → usability, certificate reuse, $d=10$;
3. the (d) file from the literature direction → honest prior-work comparison;
4. `references.addition.bib` → merged with the (d) file's entries (single bib key space),
   then merged into the paper's bibliography.

Note on the bib, because a duplicate key here silently breaks the build. The preprint's
bibliography is numbered by first appearance and already contains, among others, [1]
Bandyopadhyay et al. (`bandyopadhyay2002`), [13] Ivanović, [15] Jaming et al., [16]
Klappenecker–Rötteler, [20] McNulty–Weigert (`mcnulty2026`), [24] Wootters–Fields. Those are
**not** in `references.addition.bib`; that file holds only entries genuinely absent from the
paper, and its header lists the mapping for the ones that resolve to existing numbers. Where
`application-ab.md` writes "paper [20]" it means the existing numbered entry.

Keys used by (a)+(b), all of them real entries in one file or the other:
new — `maassen1988`, `ballester2007`, `fuchs2017sic`, `cardeneswuttig2026hadamard`,
`cardeneswuttig2026topology`, `openai2026mub6archive`;
existing — `bandyopadhyay2002` [1], `mcnulty2026` [20].
`references.addition.bib` was checked by running `bibtex` on a minimal document; it parses
clean and every entry carries a DOI or arXiv identifier plus a URL.

## 7. Open questions for T8 / T0

1. **Does the abstract keep "resolving Zauner's dimension-six MUB conjecture"?** Defensible
   only with (A)–(C) in the same breath. My recommendation: keep the phrase, and let block
   (1) of `status-paragraph.tex` follow it immediately as the last sentences of the
   abstract. If the abstract must be shortened, drop the claim of resolution to "and hence
   $N(6)=3$" and let §1 carry the framing.
2. **Should the paper state a margin?** It never says how much slack the run had (no node
   counts, no per-record histograms; see `results/code-audit.md` F6). Stating that the
   question is not answered is better than leaving a reader to assume robustness.
3. **Who owns the (c)/(d) splice?** If both other members deliver a full `application.md`
   rather than a fragment, someone must merge by hand; I wrote only `application-ab.md` to
   avoid clobbering their files. If `application.md` does not exist when T8 starts, T8
   should build it by concatenation as in §6.
