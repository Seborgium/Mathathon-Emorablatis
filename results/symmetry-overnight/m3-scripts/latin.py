"""CRT structure of the twelve maximal abelian subgroups of H(Z_6) and the
Latin-square bound for pairwise unbiased H-covariant bases."""
from itertools import combinations
from cov import MAXISO, MM, intersect_mod_center, CENT

def sig(key):
    """(line in Z_2^2, line in Z_3^2) of the isotropic subgroup pi(M)."""
    S = MAXISO[key]
    l2 = sorted({(a % 2, b % 2) for (a, b) in S})
    l3 = sorted({(a % 3, b % 3) for (a, b) in S})
    assert len(l2) == 2 and len(l3) == 3, (key, l2, l3)
    return (tuple(l2), tuple(l3))

keys = list(MAXISO)
S = {k: sig(k) for k in keys}
print("CRT signature (line in PG(1,2) x line in PG(1,3)):")
for k in keys:
    print(f"  {k:4s} {S[k]}")

# distinct lines
lines2 = sorted({s[0] for s in S.values()})
lines3 = sorted({s[1] for s in S.values()})
print("lines in PG(1,Z_2):", len(lines2), " lines in PG(1,Z_3):", len(lines3))
print("all 3*4 = 12 pairs present:", len(set(S.values())) == 12)

# criterion check: M cap M' = Z  <=>  signatures differ in both coordinates
ok = True
for k1 in keys:
    for k2 in keys:
        if k1 == k2: continue
        pred = (S[k1][0] != S[k2][0]) and (S[k1][1] != S[k2][1])
        actual = intersect_mod_center(k1, k2)
        if pred != actual:
            ok = False; print("MISMATCH", k1, k2, pred, actual)
print("criterion 'trivial intersection <=> both CRT coordinates differ':", ok)

# maximum pairwise-unbiased subsets
import itertools
best = []
for r in range(1, 13):
    found = []
    for sub in combinations(keys, r):
        if all(intersect_mod_center(x, y) for x, y in combinations(sub, 2)):
            found.append(sub)
    if found:
        best = found
        print(f"size {r}: {len(found)} subsets, e.g. {found[0]}")
    else:
        print(f"size {r}: none")
        break
