"""Small certified-arithmetic kernel for the Root obligations (self-contained).

Forms
  Q  = gmpy2.mpq : exact rational.  Every binary64 read from a record converts to Q exactly.
  Iv = [lo,hi] of Q : an outward enclosure.  Only +,-,*,/ and comparisons are used; every
       transcendental quantity (pi, cos, sin, sqrt) enters already enclosed.
Trusted imports: gmpy2.mpq (exact arithmetic only) and math.isqrt (integer sqrt, correctly
rounded by the Python spec).  No floating-point library function is ever asked for a value.
"""
from gmpy2 import mpq, mpz
from math import isqrt

__all__ = ["Q", "Iv", "pi_bounds", "cos_sin_2pi", "sqrt_bounds", "exact", "frob2_upper"]


def Q(x, d=None):
    """Exact rational from a binary64 / int / str, or Q(n,d)."""
    if d is not None:
        return mpq(mpz(x), mpz(d))
    if isinstance(x, mpq) or isinstance(x, mpz):
        return mpq(x)
    if isinstance(x, float):
        return mpq(x)                      # gmpy2 converts a float exactly
    return mpq(x)


class Iv:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        self.lo = Q(lo)
        self.hi = self.lo if hi is None else Q(hi)
        assert self.lo <= self.hi

    def __add__(s, o):
        o = as_iv(o); return Iv(s.lo + o.lo, s.hi + o.hi)

    __radd__ = __add__

    def __neg__(s):
        return Iv(-s.hi, -s.lo)

    def __sub__(s, o):
        o = as_iv(o); return Iv(s.lo - o.hi, s.hi - o.lo)

    def __rsub__(s, o):
        return as_iv(o) - s

    def __mul__(s, o):
        o = as_iv(o)
        c = (s.lo * o.lo, s.lo * o.hi, s.hi * o.lo, s.hi * o.hi)
        return Iv(min(c), max(c))

    __rmul__ = __mul__

    def __truediv__(s, o):
        o = as_iv(o)
        if o.lo <= 0 <= o.hi:
            raise ZeroDivisionError("interval divisor straddles 0")
        c = (s.lo / o.lo, s.lo / o.hi, s.hi / o.lo, s.hi / o.hi)
        return Iv(min(c), max(c))

    def sq(s):
        if s.lo >= 0:
            return Iv(s.lo * s.lo, s.hi * s.hi)
        if s.hi <= 0:
            return Iv(s.hi * s.hi, s.lo * s.lo)
        return Iv(0, max(s.lo * s.lo, s.hi * s.hi))

    def abs_hi(s):
        return max(abs(s.lo), abs(s.hi))

    def __repr__(s):
        return "[%.17g, %.17g]" % (float(s.lo), float(s.hi))


def as_iv(x):
    if isinstance(x, Iv):
        return x
    return Iv(x)


# ---------------------------------------------------------------- pi (Machin, alternating)
def pi_bounds(terms=60):
    """Rational enclosure of pi from pi = 16 arctan(1/5) - 4 arctan(1/239).

    arctan(1/m) = sum_{k>=0} (-1)^k /((2k+1) m^(2k+1)); the series is alternating with
    decreasing terms, so the partial sum brackets the value with an error of modulus <= the
    first omitted term.  Pure rational arithmetic, no library constant is trusted.
    """
    def ard(m, n):
        lo = hi = Q(0)
        mm = Q(m * m)
        pw = Q(m)
        for k in range(n):
            t = Q(1) / ((2 * k + 1) * pw)
            if k % 2 == 0:
                lo += t; hi += t
            else:
                lo -= t; hi -= t
            pw *= mm
        first = Q(1) / ((2 * n + 1) * pw)               # |first omitted term|
        return Iv(lo - first, hi + first)

    a = ard(5, terms)
    b = ard(239, terms)
    lo = 16 * a.lo - 4 * b.hi
    hi = 16 * a.hi - 4 * b.lo
    return Iv(lo, hi)


_PI = None
_FACT = None


def pi():
    global _PI
    if _PI is None:
        _PI = pi_bounds()
    return _PI


def _fact_inv(n):
    """1/(2k)! for k=0..n as exact rationals."""
    global _FACT
    if _FACT is None:
        f = [Q(1)]
        for k in range(1, n + 1):
            f.append(f[-1] / ((2 * k - 1) * (2 * k)))
        _FACT = f
    return _FACT


def cos_sin_x(x, n=14):
    """Enclosures of cos(x), sin(x) for an interval x with |x| <= 4.

    Taylor at a 60-bit dyadic midpoint, plus the Lipschitz radius r (|cos'|,|sin'| <= 1) which
    also absorbs the midpoint rounding, plus the Lagrange remainder |R_N| <= |m|^(N+1)/(N+1)!.
    Sound for every real x.
    """
    x = as_iv(x)
    mid = (x.lo + x.hi) / 2
    r = (x.hi - x.lo) / 2
    mm = mpz(mid * (mpz(2) ** 60))
    m = Q(mm, mpz(2) ** 60)
    r += abs(mid - m)
    fi = _fact_inv(n + 1)
    m2 = m * m
    c = Q(0); s = Q(0)
    pw = Q(1)                                   # m^(2k)
    for k in range(n):
        sign = 1 if k % 2 == 0 else -1
        c += sign * pw * fi[k]
        s += sign * pw * fi[k] * m / (2 * k + 1)
        pw *= m2                                # after the loop: m^(2n)
    am = abs(m)
    rem_c = pw * fi[n]                          # |m|^(2n)/(2n)!
    rem_s = pw * am * fi[n] / (2 * n + 1)       # |m|^(2n+1)/(2n+1)!
    w = r + rem_c
    cos_i = Iv(c - w, c + w)
    w = r + rem_s
    sin_i = Iv(s - w, s + w)
    return cos_i, sin_i


def cos_sin_2pi(t, n=14):
    """Enclosure of (cos 2pi t, sin 2pi t) for a rational t (argument reduction is exact)."""
    t = Q(t)
    k = int(t)
    if t - k >= Q(1, 2):
        k += 1
    elif t - k <= Q(-1, 2):
        k -= 1
    s = t - k                                    # |s| <= 1/2, and e(2pi i t) = e(2pi i s)
    two_pi = Iv(pi().lo * 2, pi().hi * 2)
    x = two_pi * s if s >= 0 else -(two_pi * (-s))
    return cos_sin_x(x, n)


def sqrt_bounds(a):
    """Outward rational enclosures of sqrt(a) for a >= 0.

    isqrt gives floor(sqrt(N)) for an integer N; scaling by 2^64 twice keeps 32 correct bits
    of the square root, then a strict check tightens the interval.
    """
    a = Q(a)
    if a < 0:
        raise ValueError("sqrt of a negative")
    if a == 0:
        return Iv(0)
    sh = 2 * 96
    N = mpz(a.numerator) * (mpz(2) ** sh) // mpz(a.denominator)
    r = isqrt(N)                                  # floor(sqrt(a) * 2^96)
    lo = Q(r, mpz(2) ** 96)
    while lo * lo > a:                            # guard against a slip: shrink
        lo -= Q(1, mpz(2) ** 96)
    hi = lo + Q(1, mpz(2) ** 96)
    while hi * hi < a:                            # widen until the upper bound is sound
        hi += Q(1, mpz(2) ** 96)
    return Iv(lo, hi)


def exact(x):
    """Exact rational value of a stored binary64."""
    return Q(x)


def frob2_upper(entries):
    """Upper bound for a sum of squares given exact entries (returns an exact Q)."""
    return sum((e * e for e in entries), Q(0))
