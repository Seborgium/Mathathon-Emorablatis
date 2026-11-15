"""Delta_A, Delta_B, Delta_C for every H(Z_6)-covariant MUB triple of C^6.
Anchor coordinates are handled directly from the definition:
  Delta_X = |{diag(lambda) : diag(lambda) preserves the ray sets of the other two bases}|,
modulo global phase.  Exact arithmetic in Z[zeta_24]."""
from itertools import combinations, permutations
from zeta import *
from cov import MAXISO, eigenbasis, generator, norm2, unbiased
from delta import all_flat_bases, lattice_index
from latin import intersect_mod_center, keys

n = 6
fb = all_flat_bases()

def matching(adj):
    """perfect matching in a bipartite graph given as adj[j] = set of allowed j'."""
    match = {}
    def try_assign(j, seen):
        for jp in adj[j]:
            if jp in seen: continue
            seen.add(jp)
            if jp not in match or try_assign(match[jp], seen):
                match[jp] = j
                return True
        return False
    for j in range(len(adj)):
        if not try_assign(j, set()): return False
    return True

def prop(c, cp, lam):
    """(lam_j c_j)_j proportional to cp ? (no division)"""
    for j in range(n):
        for l in range(n):
            if mul(POW[lam[j]], mul(c[j], cp[l])) != mul(POW[lam[l]], mul(c[l], cp[j])):
                return False
    return True

def delta_std_anchor(E1, E2):
    """anchor = standard basis; E1, E2 exponent matrices (normalisation 1/sqrt6)."""
    out = set()
    for sigma in permutations(range(n)):
        lam = tuple((E1[i][sigma[0]] - E1[i][0]) % 24 for i in range(n))
        if any(len({(lam[i] + E1[i][j] - E1[i][sigma[j]]) % 24 for i in range(n)}) != 1 for j in range(n)):
            continue
        adj = {}
        for j in range(n):
            adj[j] = {t for t in range(n)
                      if all((lam[i] + E2[i][j] - E2[i][t]) % 24 == (lam[0] + E2[0][j] - E2[0][t]) % 24 for i in range(n))}
        if matching([adj[j] for j in range(n)]):
            c = lam[0]; out.add(tuple((x - c) % 24 for x in lam))
    return out

def general_matrix(Bexp, Cexp):
    """C in the coordinates of basis B (columns of Bexp, entries zeta^e/sqrt6)."""
    MC = [[ZERO]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = ZERO
            for k in range(n):
                s = add(s, POW[(-Bexp[k][i] + Cexp[k][j]) % 24])
            MC[i][j] = s
    return MC

def standard_in_B(Bexp):
    """the standard basis expressed in the coordinates of basis B (monomial entries)."""
    return [[POW[(-Bexp[j][i]) % 24] for j in range(n)] for i in range(n)]

def delta_general_anchor(Bexp, mats):
    """anchor = basis B; mats = list of 2 matrices (as 6x6 lists of ring elements)
    expressing the other two bases in B coordinates."""
    MA = standard_in_B(Bexp)
    cols = [[[mats[t][i][j] for i in range(n)] for j in range(n)] for t in (0, 1)]
    out = set()
    for sigma in permutations(range(n)):
        lam = tuple(((-Bexp[sigma[0]][i]) - (-Bexp[0][i])) % 24 for i in range(n))
        # monomial condition against the standard basis
        def mono_ok():
            for j in range(n):
                vals = {(lam[i] - Bexp[j][i] + Bexp[sigma[j]][i]) % 24 for i in range(n)}
                if len(vals) != 1: return False
            return True
        if not mono_ok(): continue
        good = True
        for t in (0, 1):
            adj = [{tp for tp in range(n) if prop(cols[t][j], cols[t][tp], lam)} for j in range(n)]
            if not matching(adj): good = False; break
        if good:
            c = lam[0]; out.add(tuple((x - c) % 24 for x in lam))
    return out

if __name__ == "__main__":
    FLAT = {'inf','m0','m1','m2','m3','m4','m5'}
    triples = [s for s in combinations(keys, 3) if all(intersect_mod_center(x, y) for x, y in combinations(s, 2)) and set(s) <= FLAT]
    print("pairwise-unbiased 3-subsets:", len(triples))
    patterns = set()
    for T in triples:
        for x, y in combinations(T, 2):
            assert unbiased(eigenbasis(*generator(x)[1:]), eigenbasis(*generator(y)[1:])), (x, y)
        pat = []
        for anchor in T:
            others = [u for u in T if u != anchor]
            if anchor == 'inf':
                E = [fb[u][0] for u in others]
                D = delta_std_anchor(E[0], E[1])
            else:
                Bexp = fb[anchor][0]
                mats = [standard_in_B(Bexp) if u == 'inf' else general_matrix(Bexp, fb[u][0]) for u in others]
                D = delta_general_anchor(Bexp, mats)
            pat.append(len(D))
        patterns.add(tuple(pat))
        print(T, "Delta pattern", pat, flush=True)
    print("\ndistinct patterns:", patterns)
