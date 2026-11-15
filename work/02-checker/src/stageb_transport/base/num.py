"""Two number forms, no libm trust.

Dy   : exact dyadic rational n * 2^-s (n:int, s:int>=0).  All four Record scalar
       constants and every stored entry are binary64, hence exactly of this form;
       products/sums of them stay exact, so all of Section 5's relation algebra is
       exact rational arithmetic.
Iv   : closed interval [lo,hi] * 2^-B with B = 128.  Every operation returns an
       enclosure of the exact real result of the corresponding real operation on
       the enclosed values (outward rounding via floor/ceil of integer products).
       sqrt uses integer square roots:  floor(sqrt(x)) = isqrt(x) exactly.
       cos/sin use a rigorous enclosure of pi (Machin's formula, rational series
       with an alternating-series remainder bound) and Taylor series on |r|<=pi/4
       with an explicit tail bound.  No floating-point library function is used
       anywhere in a verdict.

Undecided comparisons are reported as None by the *checkers*, never as truth
values: see `Iv.le` which returns True (enclosure proves <=), False (enclosure
proves >) or None (straddles).
"""
from fractions import Fraction
from math import isqrt

B = 128
ONE = 1 << B


# ---------------------------------------------------------------- exact dyadic
class Dy:
    __slots__ = ("n", "s")

    def __init__(self, n, s=0):
        if s < 0:
            n <<= -s
            s = 0
        self.n = n
        self.s = s

    @staticmethod
    def of(x):
        """Exact conversion of a binary64 (or int) to Dy."""
        if isinstance(x, Dy):
            return x
        if isinstance(x, int):
            return Dy(x, 0)
        f = Fraction(x)                      # exact for binary64
        p = f.denominator
        s = p.bit_length() - 1
        if p != (1 << s):
            raise ValueError(f"not dyadic: {x}")
        return Dy(f.numerator, s)

    def as_fraction(self):
        return Fraction(self.n, 1 << self.s)

    def __add__(self, o):
        o = Dy.of(o)
        if self.s >= o.s:
            return Dy(self.n + (o.n << (self.s - o.s)), self.s)
        return Dy((self.n << (o.s - self.s)) + o.n, o.s)

    __radd__ = __add__

    def __neg__(self):
        return Dy(-self.n, self.s)

    def __sub__(self, o):
        return self + (-Dy.of(o))

    def __rsub__(self, o):
        return Dy.of(o) - self

    def __mul__(self, o):
        o = Dy.of(o)
        return Dy(self.n * o.n, self.s + o.s)

    __rmul__ = __mul__

    def __lt__(self, o):
        o = Dy.of(o)
        return self.as_fraction() < o.as_fraction()

    def __le__(self, o):
        return self.as_fraction() <= Dy.of(o).as_fraction()

    def __gt__(self, o):
        return Dy.of(o) < self

    def __eq__(self, o):
        return isinstance(o, (Dy, int, float, Fraction)) and self.as_fraction() == Dy.of(o).as_fraction()

    def __repr__(self):
        return f"Dy({float(self.as_fraction()):.17g})"

    def __float__(self):
        return float(self.as_fraction())

    def isnonneg(self):
        return self.n >= 0


def _tz(n):
    t = 0
    while n % 2 == 0 and n:
        n //= 2
        t += 1
    return t


def D(x):
    return Dy.of(x)


# ------------------------------------------------------------- intervals [lo,hi]
class Iv:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        self.lo = lo
        self.hi = lo if hi is None else hi

    # construction
    @staticmethod
    def rat(n, d=1, shift=0):
        """Enclosure of (n/d) * 2^-shift, outward."""
        num = n << B
        den = d << shift
        return Iv(num // den, -((-num) // den))

    @staticmethod
    def frac(f):
        f = Fraction(f)
        num = f.numerator << B
        den = f.denominator
        return Iv(num // den, -((-num) // den))

    @staticmethod
    def dy(x):
        x = Dy.of(x)
        num = x.n << B
        den = 1 << x.s
        return Iv(num // den, -((-num) // den))

    @staticmethod
    def exact_int(n):
        return Iv(n << B, n << B)

    # basic
    def __add__(self, o):
        o = _iv(o)
        return Iv(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __neg__(self):
        return Iv(-self.hi, -self.lo)

    def __sub__(self, o):
        o = _iv(o)
        return Iv(self.lo - o.hi, self.hi - o.lo)

    def __rsub__(self, o):
        return _iv(o) - self

    def __mul__(self, o):
        o = _iv(o)
        if self.lo == self.hi and o.lo == o.hi:
            p = self.lo * o.lo
            return Iv(p // ONE, -((-p) // ONE))
        a = self.lo * o.lo
        b = self.lo * o.hi
        c = self.hi * o.lo
        d = self.hi * o.hi
        return Iv(min(a, b, c, d) // ONE, -((-max(a, b, c, d)) // ONE))

    __rmul__ = __mul__

    def div_int(self, k):
        assert k > 0
        return Iv(self.lo // k, -((-self.hi) // k))

    def mul_int(self, k):
        if k >= 0:
            return Iv(self.lo * k, self.hi * k)
        return Iv(self.hi * k, self.lo * k)

    def sq(self):
        """x*x for x in [lo,hi]: the range really is [0,max(lo^2,hi^2)] when the
        interval straddles 0 (the plain multiplication formula would report a
        negative left end, which is not the range of the square)."""
        if self.lo >= 0:
            return Iv((self.lo * self.lo) // ONE, -((-(self.hi * self.hi)) // ONE))
        if self.hi <= 0:
            return Iv((self.hi * self.hi) // ONE, -((-(self.lo * self.lo)) // ONE))
        hi = max(self.lo * self.lo, self.hi * self.hi)
        return Iv(0, -((-hi) // ONE))

    def abs(self):
        if self.lo >= 0:
            return self
        if self.hi <= 0:
            return -self
        return Iv(0, max(-self.lo, self.hi))

    def sqrt(self):
        assert self.lo >= 0, "sqrt of interval with negative lower end"
        lo = self.lo << B
        hi = self.hi << B
        return Iv(isqrt(lo), isqrt(hi) + 1)

    def min(self, o):
        o = _iv(o)
        return Iv(min(self.lo, o.lo), min(self.hi, o.hi))

    def max(self, o):
        o = _iv(o)
        return Iv(max(self.lo, o.lo), max(self.hi, o.hi))

    def may_contain_neg(self):
        return self.lo < 0

    # verdicts
    def le(self, o):
        """True if enclosure proves self <= o; False if proves self > o; else None."""
        o = _iv(o)
        if self.hi <= o.lo:
            return True
        if self.lo > o.hi:
            return False
        return None

    def ge(self, o):
        o = _iv(o)
        return -self <= -o if False else _le(-o, -self)

    def width(self):
        return Fraction(self.hi - self.lo, ONE)

    def mid(self):
        return Fraction(self.lo + self.hi, 2 * ONE)

    def __float__(self):
        return float(self.mid())

    def __repr__(self):
        return f"[{float(Fraction(self.lo,ONE)):.17g},{float(Fraction(self.hi,ONE)):.17g}]"


def _iv(x):
    if isinstance(x, Iv):
        return x
    if isinstance(x, Dy):
        return Iv.dy(x)
    if isinstance(x, int):
        return Iv.exact_int(x)
    if isinstance(x, Fraction):
        return Iv.frac(x)
    if isinstance(x, float):
        return Iv.frac(Fraction(x))
    raise TypeError(type(x))


def _le(a, b):
    if a.hi <= b.lo:
        return True
    if a.lo > b.hi:
        return False
    return None


# ------------------------------------------------------------------------ pi
def _atan_inv(n, terms):
    """Enclosure of arctan(1/n) for integer n>1 by the alternating series."""
    total = Fraction(0)
    p = Fraction(1, n)
    n2 = n * n
    sign = 1
    for k in range(terms):
        total += sign * p / (2 * k + 1)
        p /= n2
        sign = -sign
    # next term bounds the tail (alternating, decreasing)
    tail = p / (2 * terms + 1)
    return total - tail, total + tail


def pi_interval():
    """pi = 16 atan(1/5) - 4 atan(1/239) (Machin), enclosed."""
    a_lo, a_hi = _atan_inv(5, 120)
    b_lo, b_hi = _atan_inv(239, 40)
    return Iv.frac(16 * a_lo - 4 * b_hi), Iv.frac(16 * a_hi - 4 * b_lo)


PI_LO, PI_HI = pi_interval()
PI = Iv(PI_LO.lo, PI_HI.hi)
PIO2 = Iv(PI.lo // 2, -((-PI.hi) // 2))


def _sincos_small(r):
    """cos/sin of the interval r with |r| <= pi/4 + eps, rigorous Taylor."""
    assert abs(r.hi) <= (ONE * 4 // 5) + 8 and abs(r.lo) <= (ONE * 4 // 5) + 8, r
    r2 = r * r
    # cos
    c = Iv.exact_int(1)
    t = Iv.exact_int(1)
    sign = -1
    for k in range(1, 27):
        t = (t * r2).div_int((2 * k - 1) * (2 * k))
        c = c + (t.mul_int(sign))
        sign = -sign
    # sin
    s = r
    t = r
    sign = -1
    for k in range(1, 27):
        t = (t * r2).div_int((2 * k) * (2 * k + 1))
        s = s + (t.mul_int(sign))
        sign = -sign
    # tail bounds: |r|^(2*27)/(2*27)!  (first omitted term)
    rmax = max(abs(Fraction(r.lo, ONE)), abs(Fraction(r.hi, ONE)))
    fac = 1
    for k in range(1, 55):
        fac *= k
    tail = Fraction(rmax) ** 54 / fac
    T = Iv.frac(tail)
    return c + Iv(-T.hi, T.hi), s + Iv(-T.hi, T.hi)


def sincos(theta):
    """Enclosure of {cos t} and {sin t} for all t in the interval theta."""
    # reduce: t = k*(pi/2) + r
    m = theta.mid() / (Fraction(PI.mid()) / 2)
    k = int(m + Fraction(1, 2)) if m >= 0 else -int(-m + Fraction(1, 2))
    for _ in range(4):
        r = theta - PIO2 * k
        if r.hi <= ONE * 4 // 5 + 8 and r.lo >= -(ONE * 4 // 5 + 8):
            break
        k += 1 if r.hi > 0 else -1
    else:
        raise RuntimeError("argument reduction failed")
    c, s = _sincos_small(r)
    q = k % 4
    if q == 0:
        return c, s
    if q == 1:
        return -s, c
    if q == 2:
        return -c, -s
    return s, -c


def e2pii(x):
    """Enclosure of cos(2*pi*x), sin(2*pi*x) for an exact dyadic (or int/Fraction)."""
    if isinstance(x, Dy):
        x = x.as_fraction()
    theta = (PI * Iv.frac(Fraction(x))) * 2
    return sincos(theta)


def pi_precision_check(terms=(120, 200, 400)):
    """Self-consistency: enclosures from different truncations must intersect and
    their intersection must have the expected width."""
    out = []
    for t in terms:
        a_lo, a_hi = _atan_inv(5, t)
        b_lo, b_hi = _atan_inv(239, t // 3)
        out.append((16 * a_lo - 4 * b_hi, 16 * a_hi - 4 * b_lo))
    return out


def dy_sqrt_up(x, shift=B):
    """Smallest dyadic n*2^-shift with n*2^-shift >= sqrt(x) for x a Dy >= 0."""
    if not isinstance(x, Dy):
        x = Dy.of(x)
    if x.n < 0:
        raise ValueError
    # sqrt(n * 2^-s) <= m * 2^-shift  <=>  n * 2^(-s) <= m^2 2^(-2 shift) <=> n << (2*shift) <= m^2 << s
    num = x.n << (2 * shift)
    den = 1 << x.s
    m = isqrt(-((-num) // den)) + 1        # ceil(sqrt(num/den)) then one more (safe)
    while (m * m) * den >= num:            # tighten: largest m with m^2*den < num
        m -= 1
    m += 1                                 # now m^2 * den >= num
    return Dy(m, shift)


def dy_sqrt_down(x, shift=B):
    if not isinstance(x, Dy):
        x = Dy.of(x)
    num = x.n << (2 * shift)
    den = 1 << x.s
    m = isqrt(num // den)
    while (m * m) * den > num:
        m -= 1
    return Dy(m, shift)


def dy_matmul(A, B):
    """Exact dyadic matrix product (A: m x n, B: n x p of Dy/int/float)."""
    m = len(A)
    n = len(B)
    p = len(B[0])
    out = []
    for i in range(m):
        Ai = [x if isinstance(x, Dy) else Dy.of(x) for x in A[i]]
        row = []
        for j in range(p):
            s = Dy(0, 0)
            for k in range(n):
                if Ai[k].n:
                    b = B[k][j]
                    b = b if isinstance(b, Dy) else Dy.of(b)
                    s = s + Ai[k] * b
            row.append(s)
        out.append(row)
    return out


def dy_to_fraction(x):
    return Fraction(x.n, 1 << x.s) if isinstance(x, Dy) else Fraction(x)
