# FINAL VERSION — submission bundle, team Emorablatis

| file | what it is | pages |
|---|---|---|
| `mub-digest.tex` / `mub-digest.pdf` | the **report** (required): one self-contained `.tex`, no figures, no `.bib`, compiles alone | 17 |
| `mub-slides.tex` / `mub-slides.pdf` | the **slides** (required): version 1 of `slides/deck1`, retitled for the team, 20 frames | 20 |
| `figs/`, `video/` | the slide assets (needed only to rebuild the deck) | — |

## Build

```
pdflatex mub-digest.tex      # twice; needs nothing else
pdflatex mub-slides.tex      # twice; needs figs/ and video/
```

## What changed from the working versions

* **Title block** now carries the team name, the four names, the MIT affiliation and the
  submission line — and nothing else in the body names anyone. If you submit by GitHub link,
  edit one macro at the top of `mub-digest.tex`:
  `\newcommand{\repoblurb}{Repository: \url{https://github.com/...} at commit <hash>}`
* **Report**: new §1 (every main claim C1–C14 with status and where to check it), new §2 (AI tools:
  Open Math OS with DeepSeek V4.1 Flash and Kimi K3.1 Pro; ChatGPT Astra and Claude Opus; and the
  three rules their output was held to), a 12-entry bibliography with in-text `\cite`s, and
  cross-references to the body sections.
* **Slides**: title frame (team + names + MIT), the demo frame now embeds the 44 s clip
  (`media9` RichMedia; the extracted stream is byte-identical, sha256 `e6d1b920…`), and a closing
  frame listing the sources named in the deck and the AI tools.

## Video in the PDF — what to expect

The clip is embedded in `mub-slides.pdf` (frame 11, "Discarding the candidates"), playable in
Acrobat/Reader and in `pdfpc`; most browser PDF viewers ignore RichMedia annotations and show the
poster frame instead. The identical `video/stageC-demo.mp4` is shipped alongside, so nothing is lost
if a viewer refuses it.

## Still to do before the 12 p.m. deadline (not done here)

* Insert the repository URL in `\repoblurb` if submitting by link rather than ZIP.
* Assemble the ZIP: this folder + the supplementary tree (`mub6-recreate/`, `work/`, `results/`,
  `certdata/`, `examples/`, `verify/`, the `mub-*.tex` notes). Optional Lean project: `work/04-lean/`.
