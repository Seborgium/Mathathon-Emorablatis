# application.md — T7 framing and application (assembly)

This directory is written by three swarm members, so the four sections of this file are
delivered as separate fragments rather than by one writer overwriting another. The
sections, in the order they should appear:

| § | content | file |
|---|---|---|
| (a) | what unbiasedness is physically; the $d+1$ bound derived, and which part is elementary; prime powers vs composite $d$; tomography | `application-ab.md` §(a) |
| (b) | what the theorem says and does not say; the three conditions; what is unconditional; what it does not establish | `application-ab.md` §(b) |
| (c) | what a certificate-based version would be usable for; $d=10$; non-compressibility | delivered by the usability direction, `application-c*.md` (if absent, see its own handoff) |
| (d) | honest comparison with prior work, one sentence of scope per item | delivered by the literature direction, `application-d*.md` (if absent, see its own handoff) |

Bibliography: `references.addition.bib` holds entries not already in the preprint's
bibliography. It was written by m1 and covers (a) and (b) only; merge, do not replace, when
the (c)/(d) entries arrive.

Placement, page budget, the exact status wording that must accompany every statement of the
upper bound, and the list of sentences that must not be written are in `handoff-1.md`
(mirrored as `handoff-1-m1.md`). `status-paragraph.tex` holds the two paste-ready paragraphs
for the abstract and the introduction.

One correction to this project's working premise, established on 2026-11-14 and argued in
`application-ab.md` §b.4: the authors' seven C++ sources and the saved numerical run *are*
published, at `github.com/openai/math` under `preprints/` … `verification/saved-run/`. What is
not published is any hash check, process log or machine record, so the run's provenance
cannot be independently authenticated. No team has read the code; `results/code-audit.md` is
an audit of the specification, and should be described that way.
