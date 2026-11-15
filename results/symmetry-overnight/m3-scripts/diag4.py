import random, sympy as sp
from zeta import *
x = sp.Symbol('x')
phi = sp.Poly(x**8 - x**4 + 1, x)
def to_sp(a): return sum(int(c)*x**i for i,c in enumerate(a))
def from_sp(p):
    p = sp.rem(sp.Poly(p, x), phi)
    return tuple(int(p.nth(i)) for i in range(8))
random.seed(1)
els = [tuple(random.randrange(-3,4) for _ in range(8)) for _ in range(6)]
# associativity
for a in els:
    for b in els[:3]:
        for c in els[:3]:
            assert mul(mul(a,b),c) == mul(a,mul(b,c)), (a,b,c)
print("associative on samples")
# correctness vs sympy
for a in els:
    for b in els[:3]:
        p = sp.expand(to_sp(a)*to_sp(b))
        got = mul(a,b)
        want = from_sp(p)
        assert got == want, (a,b,got,want)
print("matches sympy polynomial multiplication")
