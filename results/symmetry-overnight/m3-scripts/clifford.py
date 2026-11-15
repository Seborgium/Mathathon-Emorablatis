"""Clifford/Weil action of SL(2,Z_6) = Sp(2,Z_6) on the 12 isotropic line subgroups of
Z_6^2 and on the 24 pairwise-unbiased triples of stabiliser bases.

Only determinant EXACTLY 1 is used: that is the condition A^T J A = J for the commutator
form, i.e. the action that lifts to unitaries (Weil representation) preserving the central
character omega. Matrices with det a unit other than 1 scale the commutator form and have
no such lift; they are excluded.
"""
from itertools import combinations, product
from math import gcd
from cov import MAXISO, intersect_mod_center
keys = list(MAXISO)

def det2(m):
    a,b,c,d = m
    return (a*d - b*c) % 6

MATS = [m for m in product(range(6), repeat=4) if det2(m) == 1]
print("|SL(2,Z_6)| =", len(MATS))
# sanity: SL is closed under multiplication and the form is preserved
J = {(1,0,0,1): None}
def form(u,v): return (u[0]*v[1]-u[1]*v[0]) % 6
for (a,b,c,d) in MATS[:60]:
    for (e,f,g,h) in MATS[:6]:
        assert ((a*e+b*g) % 6, (a*f+b*h) % 6, (c*e+d*g) % 6, (c*f+d*h) % 6) in MATS
print("closure sample ok")

def act(mat, S):
    a,b,c,d = mat
    return frozenset(((a*x+b*y) % 6, (c*x+d*y) % 6) for (x,y) in S)

lines = {k: frozenset(MAXISO[k]) for k in keys}
linevals = list({v for v in lines.values()})
print("distinct line subgroups:", len(linevals))

def orbit_of(x, elements, action):
    seen = {x}; frontier = [x]
    while frontier:
        new = []
        for y in frontier:
            for m in MATS:
                z = action(m, y)
                if z not in seen:
                    seen.add(z); new.append(z)
        frontier = new
    return seen

o = orbit_of(linevals[0], linevals, act)
print("orbit of one line under SL(2,Z_6):", len(o), "of", len(linevals))

triples = {frozenset(lines[k] for k in T) for T in combinations(keys,3)
           if all(intersect_mod_center(x,y) for x,y in combinations(T,2))}
print("triples:", len(triples))
def act_triple(mat, T):
    return frozenset(act(mat, L) for L in T)
T0 = sorted(triples, key=lambda t: sorted(sorted(L) for L in t))[0]
o2 = orbit_of(T0, triples, act_triple)
print("orbit of one triple under SL(2,Z_6):", len(o2), "of", len(triples))

# also: which of the 12 lines are flat (contain an element with unit first coordinate)?
def is_flat_line(S):
    return any(gcd(a,6) == 1 for (a,b) in S)
flat = [k for k in keys if is_flat_line(lines[k])]
print("flat lines (first coordinate a unit somewhere):", len(flat), sorted(flat))
