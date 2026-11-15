"""Exact arithmetic in Z[zeta_24], zeta = e^{2 pi i/24}, Phi_24(x) = x^8 - x^4 + 1.

An element is a dict {k: coeff} meaning sum coeff*zeta^k (k mod 24): a representative
of Z[x]/(x^24-1) mapping onto Z[zeta_24].  Sums and products are correct under that
map; ZERO TESTS must use canon(), which reduces modulo Phi_24 (x^8 = x^4 - 1).
"""

def _reduce(p):
    n = max(len(p), 32)
    p = list(p) + [0] * (n - len(p))
    for k in range(n - 1, 7, -1):
        c = p[k]
        if c:
            p[k - 4] += c
            p[k - 8] -= c
            p[k] = 0
    return tuple(p[:8])

POW = [_reduce([1] + [0] * k if False else [0] * k + [1]) for k in range(24)]

def canon(a):
    res = [0] * 8
    for k, v in a.items():
        pk = POW[k % 24]
        for j in range(8):
            if pk[j]:
                res[j] += v * pk[j]
    return tuple(res)

def is_zero(a):
    return canon(a) == (0,) * 8

def eq_int(a, n):
    c = canon(a)
    return c == ((n,) + (0,) * 7 if n else (0,) * 8)

def mul(a, b):
    r = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            k = (ka + kb) % 24
            r[k] = r.get(k, 0) + va * vb
    return {k: v for k, v in r.items() if v}

def add(*xs):
    r = {}
    for a in xs:
        for k, v in a.items():
            r[k] = r.get(k, 0) + v
    return {k: v for k, v in r.items() if v}

def scale(a, c):
    return {k: v * c for k, v in a.items() if v * c}

def conj(a):
    return {(-k) % 24: v for k, v in a.items()}

def neg(a):
    return {k: -v for k, v in a.items()}   # additive inverse

def zpow(e):
    return {e % 24: 1}

ZERO = {}
ONE = {0: 1}

def norm2(a):
    """|a|^2 = a * conj(a)."""
    return canon(mul(a, conj(a)))

def is_nonneg_int(a):
    c = canon(mul(a, conj(a)))
    return c[1:] == (0,) * 7 and c[0] >= 0, c[0]

SQRT6 = add(zpow(1), zpow(23), zpow(5), zpow(19))  # 2cos15 + 2cos75 = sqrt6

def phase_of_flat(s):
    """Return e with s = sqrt6*zeta^e, or None if s is not such a product."""
    c = canon(mul(s, conj(SQRT6)))     # should be 6 zeta^e
    for e in range(24):
        if c == tuple(6 * p for p in POW[e]):
            return e
    return None

def phase_of_monic(s):
    """Return e with s = zeta^e, or None."""
    c = canon(s)
    for e in range(24):
        if c == POW[e]:
            return e
    return None
