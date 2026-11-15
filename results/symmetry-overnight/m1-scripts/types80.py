"""Count the projective types of relation vectors r_{ij,kl} = e_i-e_j-e_k+e_l mod 3."""
from itertools import product
from collections import Counter
N = 6
types = {}
for i, j, k, l in product(range(N), repeat=4):
    if i == j or k == l:
        continue
    r = [0]*N
    r[i] += 1; r[j] -= 1; r[k] -= 1; r[l] += 1
    if not any(r):
        continue
    v = tuple(x % 3 for x in r)
    if next(x for x in v if x) == 2:          # v and 2v are the same relation line
        v = tuple((-x) % 3 for x in v)
    types.setdefault(v, set()).add(tuple(r))
print("projective types of nonzero relations mod 3:", len(types))
fam = Counter()
for v in types:
    supp = [i for i in range(N) if v[i]]
    if len(supp) == 2:
        fam['2(e_i - e_j)'] += 1
    elif len(supp) == 3:
        fam['2e_i - e_j - e_k = -(e_i+e_j+e_k)'] += 1
    elif len(supp) == 4:
        fam['e_i + e_l - e_j - e_k'] += 1
for k, n in fam.items():
    print(f"  {k}: {n}")
print("  total:", sum(fam.values()))
