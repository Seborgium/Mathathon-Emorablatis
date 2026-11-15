# FINDINGS — cover unit (m2). Each finding names the test that settles it.

## F1 (spec defect, blocking for anyone gating the cover log). Bucket constants are 4/28, not 3/38.
`spec/interfaces.md` §4: "bucket `K`, `m` | `max(1, int(R·n+.51)) = 3`, `m = ⌈n/K⌉ = 38`".
With R=.032, n=112 the published expressions give `int(3.584+0.51) = int(4.094) = 4` and
`m = (112+3)/4 = 28`, i.e. 21 952 buckets. Settled by: (a) `objdump` of
`.scratch/gh/build/covrun` at `coverSeeds::run+0x6b` — `vcvttsd2si` on `R·n+.51` yields 4,
`cmovle` realises `max(1,·)`, then `lea -1(%r12,%rcx,1)` builds `n+K-1`; (b) my rebuild with
4/28 reproduces `visit=29769262282` and `near=3341641851` exactly, and `visit` is a direct
function of the bucket layout; (c) with 3/38 the t<3000 prefix gives `visit=372855144`
instead of `624467049`. The centre file cannot distinguish them (identical 12 111 lines,
because a candidate needs `|k_i| ≤ 5` per coordinate while the scan reaches ±5 for K=3 and
±7 for K=4).

## F2 (spec defect, cosmetic). `pow(x,2)` is not folded.
`spec/interfaces.md` §5.9 says "`pow(x,2)` must be a single multiply (inspect the
disassembly of `covrun`)". `covrun.disassembly.txt` shows two `call pow@plt` (53fa, 543f)
inside `coverSeeds::run`. Settled by: `c-fixture.cpp` asserts `pow(x,2) == x*x` bitwise at
both published arguments — it holds, so either spelling is safe.

## F3. Byte identity of `centers.txt` (rung R2, cover part). **PASS.**
`run/mine-centers.txt` = 7 339 546 bytes, sha256
`c48bc9a2be1eb2cdeea82ea1b030d7cb9f00a6c9563b63f0248dd115748a5789`, identical to
`.scratch/gh/data/centers.txt` (`c-verify.py compare`, exit 0). All six published counters
reproduce: `checked151744086 centers249878 visit29769262282 near3341641851 cheap45648766
lp3134060273`. The counters are the sharper test: they are sensitive to the bucket layout,
so they also pin `K=4, m=28`.

## F4. Sensitivity table (t<3000 prefix; the recorded prefix is 12 111 centres / 351 454 body bytes).
Command shape: `./build/c-harness --load run/seeds-n112.bin --out run/abl-<name>.txt --tmax 3000 <opts>`

| config | centres | checked | visit | near | cheap | lp | prefix = recorded? |
|---|---|---|---|---|---|---|---|
| base `K=4 m=28 dual=2` | 12111 | 5552647 | 624467049 | 100412429 | 1889539 | 93529007 | **yes** |
| `--K 3 --m 38` | 12111 | 5552647 | 372855144 | 96054606 | 1926068 | 89270258 | **yes** (byte identical) |
| `--no-gap` | 62736 | 35587005 | 6542082171 | 723374301 | 11194775 | 672773327 | no |
| `--no-iv` | 12210 | 6897351 | 751934256 | 114561627 | 1999642 | 106544479 | no |
| `--dual 0` | 37407 | 5552647 | 2092964965 | 390108136 | 5515240 | 0 | no |
| `--dual 6` | 10793 | 5552647 | 547829817 | 84959169 | 1603519 | 79133745 | no |
| `--no-cheap --no-prefilter` | 12141 | 5552647 | 627146478 | 100672686 | 0 | 100672686 | no |

Consequences, all measured rather than assumed:
1. **Bucket layout is not mathematics.** 3/38 and 4/28 give byte-identical centre lists;
   only the counters move. A correct cover does not depend on `K`/`m`.
2. **The gap filter (covout.cpp:122) is a canonicalisation, not a feasibility test.**
   Removing it multiplies the centre count by 5.2 and `checked` by 6.4, because it admits
   only pairs whose two bin clusters lie inside one span. It is the representative choice
   for the rotational symmetry, and the 249 878 figure is only meaningful with it on.
3. **The interval filter (covout.cpp:123) is a real feasibility test.** Removing it adds
   99 centres on the prefix (12111 -> 12210) that admit no common shift.
4. **70% of the covering power is the LP certificate.** Without it (`dual=0`) the count
   triples. The cheap L2 short-circuit additionally certifies 30 cells that the LP does
   not (12141 with the cheap path disabled).
5. **`dual=2` is part of the specification, not an implementation detail.** More dual
   iterations tighten the bound and change the count (10793 at `dual=6`), so the number
   249 878 cannot be reproduced by "any valid bound".

## F5. Cells have repeated bins; the enumeration is non-strict.
Record line 1 is `0 0 55 55 55 2 0 0 55 55`, i.e. `a=b=c=0` is legal: the loops are
`F(d,e+1)` etc., so cells are non-decreasing 5-tuples of 112 bins (C(116,5) = 160 389 488
candidates), not 5-element subsets. Settled by: `c-verify.py invariants` accepts the
recorded file only under `≤` (a strict-ascending check fails on line 1). Consequence for
any re-derivation: `B.p.b[1..4]` is only *non-decreasing*, which is exactly why the
`sorted triangle` restriction `i≤j≤l` in `covered()` is sound.

## F6. The greedy cover is not monotone in the certificate strength, so 249 878 has no closed form.
At `dual=6` the set is not a subset of the `dual=2` set (checked as a subsequence on the
prefix). Removing a centre can expose a later cell that the removed centre used to cover.
So the count is the output of one fixed sequential procedure; it is not the size of a
minimal cover and not a monotone function of how strong the covering test is. Any claim
that some *other* parameter choice "should" give the same number is unfounded — only
`K`/`m` is provably neutral (F4.1).

## F7. Performance: supdual must be inlined.
The published `covrun` has no out-of-line `supdual` symbol (`nm -C`), i.e. it is inlined.
With supdual left as a real call, my build ran the full sweep in 797.96 s against the
published 401.82 s (same bytes, same counters). Adding `always_inline` (`MUB_AI`) removes
the symbol and takes the t<3000 prefix from 18.94 s to 12.68 s, and the full sweep from
797.96 s to **434.82 s** (1.08x the published 401.82 s), with identical counters and
identical bytes. The remaining 8% is the `Options` indirection in the inner loop.
