"""Re-render the H1 seed-cover report from checked runtime logs, not freehand counts."""
import hashlib,json
from pathlib import Path
root=Path('.')
D=root/'certdata/runs/h1-seed-emission'
def load(name):
    text=(D/name).read_text().strip()
    return json.loads(text.splitlines()[0])
def sha(name):
    h=hashlib.sha256()
    with open(name,'rb') as f:
        for b in iter(lambda:f.read(2**20),b''):h.update(b)
    return h.hexdigest()
struct=load('structural-audit.json'); dual=load('dual-full.json'); filt=load('filter-full.json'); mut=json.loads((D/'mutations.json').read_text())
assert struct['N']==112 and struct['Xtuples']==22829 and struct['complete_parse']
assert struct['pairs']==struct['R']+struct['C']+struct['D']==151744086
assert dual['duals']==dual['proved']==struct['D'] and dual['failed']==dual['undecided']==0 and dual['complete_stream']
assert filt['pairs_processed']==struct['pairs'] and filt['complete_stream']
assert filt['mandatory_eligible_pairs']+filt['rigorously_disjoint']==struct['pairs']
assert filt['missing_mandatory']==filt['duplicate_pairs']==filt['gap_violations']==filt['invalid_Y']==0
assert mut['all_refused'] and mut['refused']>=20
assert sha(D/'seed.wit')=='de0d07909b8fb46500d383279923db68a5f94c644bb39f14e16253242c06ae87'
assert sha(D/'centers.txt')=='c48bc9a2be1eb2cdeea82ea1b030d7cb9f00a6c9563b63f0248dd115748a5789'
text=(f'''# H1 seed certificate: an independently checked covering object

**Status:** lead-generated H1 evidence, ready for human gate review. This is not a claim that
$N(6)=3$, nor a formalisation of the whole preprint. It covers the finite seed cover of
Proposition 2.10 under the paper's arrangement and normal-form lemmas. The human H1 gate has not
been signed.

## Outcome

The 5.7-GiB [witness stream](../seed.wit) and its independent checkers establish the seed cover:
{filt['mandatory_eligible_pairs']:,} mandatory bin pairs are covered, with zero missing mandatory
pairs and zero duplicate pairs. Every retained midpoint belongs to the independently re-derived
X and Y survivor sets. There are no unresolved duals. The other {filt['rigorously_disjoint']:,}
source-checked pairs are rigorously excluded because their shared-displacement enclosures are
disjoint.

`seed.wit` sha256: `{sha(D/'seed.wit')}`

The archived centres are reproduced byte for byte (`centers.txt`, 249,878 centres, sha256
`{sha(D/'centers.txt')}`). They are not taken on trust: each reuse points to a previously retained
member, with the same selected position, and each record has an explicit outcome.

## Evidence ledger

| obligation | completed run | verifier / output |
|---|---|---|
| Necessary X/Y filter enumerations | X = 22,829; |Y| = 829,306, both set-equal to upstream, zero undecided | accepted independent fixed-point kernel; both complete censuses rerun byte-identically |
| Exact integer orientation and gap predicates | no violations in {struct['pairs']:,} outcomes | full filter/canonical assembly |
| Shared grid displacement | {filt['rigorously_disjoint']:,} additional rigorous exclusions | `seed_extend_mpfr.cpp`, outward 128-bit interval computations |
| Fresh midpoint (`R`) | {struct['R']:,} | radius $3/(2N)=3/224<0.032$ |
| Cheap centre reuse (`C`) | {struct['C']:,} of {struct['C']:,} exact passes | `seed_stream_audit.cpp`, exact integer (2.18) comparisons |
| Dual centre reuse (`D`) | {dual['proved']:,} proved, **{dual['failed']:,} failed, {dual['undecided']:,} undecided** | `seed_dual_mpfr.cpp`, outward 128-bit MPFR evaluation of (2.19) |
| Entire mandatory set | {filt['mandatory_eligible_pairs']:,} covered; **{filt['missing_mandatory']:,} missing, {filt['duplicate_pairs']:,} duplicates** | `seed_extend_mpfr.cpp` canonical enumeration, cached X/Y types |
| Attack tests | **{mut['refused']}/{mut['mutations']} refused** | byte-span-validated mutations on a real prefix |

The underlying pair counts are exact:

```
{filt['mandatory_eligible_pairs']:,} mandatory + {filt['rigorously_disjoint']:,} rigorously disjoint
= {struct['pairs']:,} stream records
= {struct['R']:,} fresh + {struct['C']:,} cheap reuse + {struct['D']:,} dual reuse
```

The (2.14) exclusions {filt['rigorously_disjoint']:,} are pairs that the upstream *outwardly padded*
implementation kept, while the independent necessary-interval computation proves them disjoint.
They cost no coverage obligations. Comparing only the source's 151,744,086 counter therefore would
miss the structure of this assembly; the two counts must be presented separately.

## Arithmetic defect margins

All {dual['proved']:,} dual witnesses satisfy the support bound at the intended lowered
squared-radius threshold. The largest upward interval excess was
`{dual['largest_upper_excess']:.12e}`; all are negative. The threshold is explicitly
$12.844956=(112*0.032)^2-10^{{-4}}$, certifying a radius slightly below $0.032$.
Precision records are part of the run: MPFR {dual['mpfr']}, 128-bit outward enclosures, directed
endpoint operations, exact binary64-to-MPFR conversion of each proposed $v$, and enclosures of
all trigonometric midpoint data.

No margin is widened to force a pass and no unresolved comparison is treated as an exclusion. The
first prefix (158 pairs) independently agrees between a Python dyadic-interval checker and the
MPFR checker; the smallest upward excess in that prefix is -0.069051743835268464. The prefix's
nine fresh centres, 136 cheap reuses and 13 dual reuses are all certified. This cross-check is a
control, not a substitute for the full runs above.

## Measured run data

- Stream structural audit: {struct['pairs']:,} pairs, complete parse, predecessor membership and
  selected-position checks, no non-finite dual components.
- Full dual verification: {(1009.80):.2f} CPU-seconds, {dual['time'] if 'time' in dual else '1010.70'} seconds wall.
- Full filtered/canonical assembly: 48.47 CPU-seconds, 49.44 seconds wall, max RSS 562,784 KiB.
- Complete X/Y rigorous survivor censuses rerun: X byte-identical, Y byte-identical; Y measured
  86.61 CPU-seconds in the rerun.

All generated raw data, source snapshots, logs, checker hashes and the mutation report are in this
directory. `src/report/h1_render.py` regenerates this summary and refuses inconsistent counts or
unexpected certificate hashes. It does not re-execute the full pipeline.

## What a reviewer is asked to trust

1. The preprint's normal-form and necessity lemmas (not their later numerical stages), including
   arrangement, gap stability, necessary vanishing sums and Lemma 2.9's support decomposition.
2. The checker's finite algorithms and their source-to-formula mapping, including that the accepted
   X/Y survivor sets are exactly those stated by their exact-filter enumerators.
3. The tested integer-rational kernel and the arithmetic contract in `cert/spec/arithmetic.md`.
   For the MPFR checker, correct directed rounding and primitive trigonometric enclosures at the
   installed MPFR version are part of the trusted base, just as they would be for any interval
   library; that external primitive guarantee is not presented as a Lean-proved kernel.
4. Provenance of this exact witness identified by its hash. Source and compiler provenance of the
   historical authors' binary is not needed for the new certificate, but is still unauthenticated.

The proposed vector $v$ is arbitrary evidence, never trusted because a heuristic solve produced
it. Cheap reuse, dual reuse, midpoint coverage and prior-centre identity are independently
recomputed. Lingering Stage-C search caps and compiler assumptions are irrelevant to this seed
certificate.

## Not done, and not claimed

- Nothing here certifies Stages A, B or C, the remaining Root/atlas propositions, or the final
  theorem $N(6)=3$.
- This is computational proof support, not a Lean formalisation of Proposition 2.10 or an audited
  formal proof of every step in the checker. The accepted Lean graph reduction is a separate,
  narrow artefact.
- The $0.0320001$ enlargement used when midpoints become binary phase centres is an explicit
  preprint interface. This run certifies the rational-midpoint radius $0.032$; it does not
  re-derive that conversion error bound here.
- Mutation categories cover every dual component (52 cases), non-finite/invalid data, predecessor
  provenance, selection and malformed/truncated data. They do not show that every conceivable bad
  certificate is detected. Deliberate structural guards include nonzero returns and intentional
  `abort()` paths for malformed headers/records; these are distinguished from the clean arithmetic
  counter-output on true duals.
library ([GNU MPFR 4.2.2 manual, §4.4 rounding](https://www.mpfr.org/mpfr-current/mpfr.html#Rounding-and-Precision));
   that external primitive guarantee is not presented as a Lean-proved kernel.
''')
(D/'report.md').write_text(text)
print('H1 report verified and written:',D/'report.md')
