"""Maximal abelian subgroups of the Weyl-Heisenberg group over Z_6, exact.

H(Z_6) = {omega^t X^a Z^b : t,a,b in Z_6}, |H| = 216, center = {omega^t I}.
Group law: (t,a,b)(s,c,d) = (t+s+bc, a+c, b+d).
Commutator phase of (a,b),(c,d): omega^{bc - ad}.
"""
from itertools import product
from wh import glaw, ginv, GROUP

def eform(u, v):
    """alternating form on Z_6^2: <(a,b),(c,d)> = a d - b c mod 6 ; commutator = omega^{<u,v>}?"""
    (a, b), (c, d) = u, v
    return (a*d - b*c) % 6

def subgroup_of_Z62(gens):
    S = {(0, 0)}
    frontier = [(0, 0)]
    while frontier:
        new = []
        for g in frontier:
            for h in gens:
                k = ((g[0]+h[0]) % 6, (g[1]+h[1]) % 6)
                if k not in S:
                    S.add(k); new.append(k)
        frontier = new
    return frozenset(S)

# all subgroups of Z_6^2
allsubs = set()
pts = [(a, b) for a in range(6) for b in range(6)]
for r in (1, 2, 3):
    for gens in __import__("itertools").combinations(pts, r):
        allsubs.add(subgroup_of_Z62(gens))
print("subgroups of Z_6^2:", len(allsubs))
iso = [S for S in allsubs if all(eform(u, v) == 0 for u in S for v in S)]
maxiso = [S for S in iso if not any(S < T for T in iso)]
print("isotropic subgroups:", len(iso), "maximal ones:", len(maxiso), "orders:", sorted({len(S) for S in maxiso}))

# preimage in H of an isotropic subgroup, and check abelian
def preimage(S):
    M = set()
    for (t, a, b) in GROUP:
        if (a, b) in S:
            M.add((t, a, b))
    return frozenset(M)

def is_ab(S):
    L = sorted(S)
    for i in range(len(L)):
        for j in range(i, len(L)):
            if glaw(L[i], L[j]) != glaw(L[j], L[i]):
                return False
    return True

print("\nmaximal abelian subgroups of H: preimages of maximal isotropic subgroups")
maxabel = []
for S in maxiso:
    M = preimage(S)
    assert is_ab(M), S
    maxabel.append((S, M))
    print("  pi(M) =", sorted(S), " |M| =", len(M))
print("count:", len(maxabel))

# are they really maximal abelian? check every abelian subgroup of H is inside one of them
# (any abelian subgroup has isotropic image, hence image inside some maximal isotropic -> M inside preimage)
# verify upper bound: |M| = 6 |pi(M)|
print("\nsanity: |M| =", {len(M) for _, M in maxabel})

# classify the 12 by slope data under CRT
import json
def crt(a):
    return (a % 2, a % 3)
info = []
for S, M in maxabel:
    pts_ = sorted(S)
    info.append(pts_)
for p in info:
    print(p)
