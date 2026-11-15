# K4-0 (map, not a defect) — provenance: module -> manuscript sections -> the artefact that pins it

Source of section numbers: the laid-out text at `.scratch/mub6.txt` (4,164 lines;
section heads at 290, 632, 1155, 1770, 2176, 2708, 2975, appendix at 2984;
subsections at the lines used below). "Pinned by" = the artefact that fails if
the behaviour drifts.

| module | manuscript | appendix | pinned by |
|---|---|---|---|
| seed.cpp | §2.1 gauges; §2.2 Lem 2.4 (2.3)-(2.7), Lem 2.5, Lem 2.6 (2.8); §2.3 Lem 2.7 (2.10)-(2.11); `seeds::mk` named in §2.2; §7.3 binomial bound | A.1-A.3 | centers.txt fields 1-6 (verified below) |
| covout.cpp | §2.2 last para ("the program covout ..."), §2.3 Lem 2.8 (2.13)-(2.14) = `extend`, §2.4 (2.17)-(2.19) = `supdual` (1.251π/N, 1e4 check, .01), §7.3 | A.3 | centers.txt entire (sha + 249878 + all structural invariants); Table 1 counts 22,829 / 151,744,086 / 249,878 |
| ub.cpp | §3.1 frames/blocks, §3.2 `makeD`/`makeJ`, §3.3-3.4 cells & comparison, §3.6 flatness (1.251, `derr`, `trial::certificate`), §4.1 Root fields | A.4-A.5 | coarse0..3.bin (Table 2 sha), Table 1 (764/774/757/788) |
| patchx.cpp | §3.3, §3.5 remainder, §3.7 finite recursion = `Asearch::runA`, §4.1-4.2 `Root`/`buildH`/`snap`/`patch` (.64, 4.35), §4.4-4.5 `covercompute`, §4.6 `bootstrap`, §4.7 | A.5-A.8 | coarse0..3.bin; no separate artefact |
| atlas.cpp | §2.1 equivalence group = `mapH`/`canonicalMap`, §4.3 `variants`, §4.7 `Atlas::find/add`, §7.1 record format (356+288k), §7.2 `arun` constants + exit code | A.6 | coarse0..3.bin sha; bad0..3.txt zero-length; centers.txt as *input* (reader enforces 112, bins<112, s<5) |
| stageB.cpp | §5.1 `relationB`, §5.2 bisection (25 steps), §5.3 L=ceil(E/w+.500001), §5.4 assignments/radius growth, §5.5 blocker induction = `preload`/`blockers`, §5.6 batching + finite limits, §7.2 | A.9 | mid.bin (600), fine.bin (22,379), batches/f0..87.bin = 87*256+107, done.txt, midbad/finebad 8 B |
| stageC.cpp | §6.1-6.6 (`Layer::test`, `cluster`, `single`, edge/joint tests, `graph`), §6.7 margins + "12 4 1 .042 1 1 5000000" + Lloyd=2, §7.3 (2e6 bins, 32 children, 2048 balls, 32 words, 12^5) | A.10-A.12 | batches/bad*.bin (15 nonempty, 163 records, names+order in §7.5 = commands.json argv), 73 exits 0 / 15 exits 1, fb1cbad0..3 zero-count, fb1.bin 1127 |

Verified now against recorded data, no rebuild (all zero-violation on 249,878 lines
of `.scratch/gh/data/centers.txt`, sha c48bc9a2... = Table 2):
 1. fields 1-5 weakly increasing, 0 violations  -> §2.2 the tuple is weakly sorted
 2. field 5 nondecreasing, 0 violations         -> loop nest order (K4-2)
 3. field 6 = first minimizer of |2b_s+1-112|, 0 violations -> `seeds::mk`'s rule, named in §2.2
 4. all X pass `p.g <= 1-(e-1)w+1e-8`, 0 violations -> Lem 2.6 first inequality
 5. all (X,Y) pass `g(Y) >= 1-(e+2)w`, 0 violations -> Lem 2.6 second inequality as covout applies it
 6. covrun stdout of the reproduced run matches Table 1 on xs 22,829, checked
    151,744,086, centers 249,878 (`.scratch/gh/covrun.log`).

Prose/code notes D must carry:
 * §2.2's description of covout covers only its *filters*; what covout *emits* is
   a greedy cover produced by the bucket/LP test, and §A.3 is the only prose about
   that test ("bucket reach, and integer cuts only select reuse attempts"). That
   sentence is written for A's exclusions; in covout a missed attempt *adds* a
   centre, so those knobs are load-bearing for centers.txt (see K4-4).
 * §A.3 justifies every numeric margin of sumok/extend/supdual one by one
   (1e-8, 1e-7, 1e-6, 1e-5, 1.251, .01, .0001, 1.5). Those are the best-documented
   constants in the program; the unnamed ones are in K4-6.
 * code with no artefact at all: `seeds::list` and the three unbuilt drivers
   (K4-7); `Usearch::test/runblock/report` are shadowed by `Asearch::testA`, so
   ub.cpp's *traversal* is pinned by nothing — only its Z/ldl/frame/block/uc/
   makeD/makeJ/scalar/trial/bound/derr are. ~85 of 2,265 source lines are dead.
 * Table 2 (sha) and Table 1 (counts) are the comparators the plan and gates do not
   cite (K4-5).
