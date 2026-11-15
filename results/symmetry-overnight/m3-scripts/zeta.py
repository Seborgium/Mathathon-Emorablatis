"""Exact arithmetic in Z[zeta_24] = Z[x]/(x^8 - x^4 + 1).

Elements are tuples of 8 ints (coeffs of 1,x,...,x^7). zeta_24 = x.
Reduction: x^8 = x^4 - 1, so x^k = x^{k-4} - x^{k-8} for k >= 8.
"""
ZERO = (0,)*8
ONE = (1,)+(0,)*7

def mul(a, b):
    c = [0]*15
    for i in range(8):
        ai = a[i]
        if ai:
            for j in range(8):
                if b[j]:
                    c[i+j] += ai*b[j]
    for k in range(14, 7, -1):
        ck = c[k]
        if ck:
            c[k-4] += ck
            c[k-8] -= ck
            c[k] = 0
    return tuple(c[:8])

def add(a, b):
    return tuple(x+y for x, y in zip(a, b))

def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))

def neg(a):
    return tuple(-x for x in a)

def scal(k, a):
    return tuple(k*x for x in a)

ZETA = (0,1,0,0,0,0,0,0)

def zpow(k):
    k %= 24
    r = ONE
    base = ZETA
    e = k
    while e:
        if e & 1:
            r = mul(r, base)
        base = mul(base, base)
        e >>= 1
    return r

POW = [zpow(k) for k in range(24)]

def conj(a):
    """zeta -> zeta^{-1} on basis; extended Z-linearly."""
    out = [0]*8
    for i in range(8):
        if a[i]:
            t = POW[(-i) % 24]
            for j in range(8):
                out[j] += a[i]*t[j]
    return tuple(out)

def inv_monomial(a):
    """Inverse of a monomial (an element equal to zeta^k for some k)."""
    k = monomial_index(a)
    assert k is not None, a
    return POW[(-k) % 24]

def is_zero(a):
    return all(x == 0 for x in a)

def rat(a):
    """Return a as a Fraction if it is rational (constant polynomial)."""
    from fractions import Fraction
    assert all(x == 0 for x in a[1:])
    return Fraction(a[0])

def monomial_index(a):
    """Return k if a = zeta^k, else None."""
    for k in range(24):
        if list(a) == list(POW[k]):
            return k
    return None

W6 = POW[4]           # e^{2 pi i/6} = zeta_24^4
SQRT6 = add(add(POW[1], POW[23]), add(POW[5], POW[19]))  # 2cos(pi/12)+2cos(5pi/12)= sqrt6
