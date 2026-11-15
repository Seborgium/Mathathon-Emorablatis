"""Finite check behind the no-exchange (no-swap) lemma in d=6.

If a diagonal unitary T maps the rays of B onto those of C and vice versa, then
  (i) |tr T|^2 = 6   (the sum over coordinates of lambda_i = 6 mu_r c_{pi(r),i} conj(b_{r,i})
      has modulus 6/sqrt6 = sqrt6), and
  (ii) T^12 is a scalar, so after removing a global phase T_0^12 = 1.
Hence tr T_0 = sum_j n_j zeta_12^j with n_j >= 0, sum n_j = 6, and |tr T_0|^2 = 6.
This script shows that no multiplicity vector gives |.|^2 = 6.
"""
from itertools import product
import cyc

def comps(total, parts):
    """all tuples of `parts` nonneg integers summing to total"""
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in comps(total - first, parts - 1):
            yield (first,) + rest

hits = []
best = {}
for m in (2, 3, 4, 6, 12):
    n = 0
    for multi in comps(6, m):
        s = {}
        for j, c in enumerate(multi):
            if c:
                e = (24 // m) * j % 24
                s[e] = s.get(e, 0) + c
        s = {k: v for k, v in s.items() if v}
        sq = cyc.canon(cyc.mul(s, cyc.conj(s)))
        if sq[1:] == (0,) * 7 and sq[0] == 6:
            hits.append((m, multi))
        n += 1
    print(f"order {m:2d}: {n:6d} multiplicity vectors tested, running total of |tr|^2 = 6 hits: {len(hits)}")
print("multiplicity vectors with |tr T_0|^2 = 6 for some order dividing 12:", hits)
print("=> no diagonal T with |tr T|^2 = 6 can have T^12 scalar of projective order in {1,2,3,4,6,12}")
