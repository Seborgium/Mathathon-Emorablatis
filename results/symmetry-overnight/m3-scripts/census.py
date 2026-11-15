"""Sample census of Delta-patterns in m5's (source sec.4 uniform) family, by the
definition-based Delta; also tests the conjecture pattern (6,6,6) iff same permutation."""
from itertools import permutations, product
from gen_delta import *

F, seen = family()
allmat = [it for v in seen.values() for it in v]
good = [it[0] for it in allmat if it[1]]
# record the permutation index of each matrix: H = F D P ; recover P by matching columns
perms = list(permutations(range(3)))
PERM3 = [perm3(p) for p in perms]
def perm_of(H0):
    for idx, P in enumerate(PERM3):
        # H0 = F D P  =>  H0 P^{-1} = F D  has columns parallel to F's columns
        Pinv = [[P[j][i] for j in range(3)] for i in range(3)]
        M = rmul(H0, Pinv)
        ok = True
        for i in range(3):
            for j in range(3):
                if not is_zero(M[i][j]):
                    pass
        # check M[i][j]/F[i][j] independent of i
        for j in range(3):
            r = mul(M[0][j], inv_field(F[0][j]))
            for i in range(1,3):
                if mul(M[i][j], inv_field(F[i][j])) != r: ok = False
        if ok: return idx
    return None

Id = [[ONE if i == j else ZERO for j in range(6)] for i in range(6)]
def pattern(H0, H1):
    K0 = rmul(H0, F); K1 = [[mul(I12, x) for x in row] for row in rmul(H1, F)]
    U = block(H0, H1); V = block(K0, K1)
    assert mub(Id,U) and mub(Id,V) and mub(U,V)
    return tuple(len(delta_general(X, Y, Z)) for X, Y, Z in [(Id,U,V),(U,Id,V),(V,Id,U)])

if __name__ == "__main__":
    import random, collections
    random.seed(11)
    idx = list(range(len(good)))
    Random = random.Random(5)
    samples = [(Random.randrange(len(good)), Random.randrange(len(good))) for _ in range(10)]
    cnt = collections.Counter()
    for (a,b) in samples:
        p = pattern(good[a], good[b])
        pa, pb = perm_of(good[a]), perm_of(good[b])
        cnt[p] += 1
        print(f"pair ({a},{b}) perms ({pa},{pb}) -> Delta {p}", flush=True)
    print("counts:", dict(cnt))
