"""Exact arithmetic in Q(w), w = exp(2*pi*i/6), and the worked example matrix.

A number is a + b*w with a, b rational.  Since w^2 = w - 1 the two-rational
form is closed under multiplication; conjugation is w -> 1 - w.  The example
matrix of mub-step1-example.pdf and every check of steps 2 and 3 that can be
done in exact arithmetic is done here.  Floating point is used only to print
and for quantities (norms, frames) that are irrational by nature.

Run this file directly for a self test.
"""
from fractions import Fraction
import cmath

# ---------------------------------------------------------------- the field
class Qw:
    """a + b*w with w = exp(2*pi*i/6); w^2 = w - 1."""
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)

    def __add__(self, o):
        return Qw(self.a + o.a, self.b + o.b)

    def __sub__(self, o):
        return Qw(self.a - o.a, self.b - o.b)

    def __neg__(self):
        return Qw(-self.a, -self.b)

    def __mul__(self, o):
        # (a+bw)(c+dw) = ac + (ad+bc)w + bd w^2 = (ac-bd) + (ad+bc+bd)w
        a, b, c, d = self.a, self.b, o.a, o.b
        return Qw(a * c - b * d, a * d + b * c + b * d)

    def __truediv__(self, o):
        n = o.norm()
        if n == 0:
            raise ZeroDivisionError
        return self * Qw(o.a + o.b, -o.b) * Qw(1 / n)

    def norm(self):
        """a^2 + ab + b^2 = |z|^2, a rational."""
        return self.a * self.a + self.a * self.b + self.b * self.b

    def conj(self):
        return Qw(self.a + self.b, -self.b)

    def __eq__(self, o):
        return isinstance(o, Qw) and self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def is_zero(self):
        return self.a == 0 and self.b == 0

    def complex(self):
        return complex(float(self.a) + float(self.b) * 0.5,
                       float(self.b) * (3 ** 0.5) / 2)

    def __repr__(self):
        return fmt(self)

    def __abs__(self):
        return self.norm() ** 0.5

ZERO = Qw(0, 0)
ONE = Qw(1, 0)


def wp(m):
    """w^m as a Qw."""
    return Qw({0: (1, 0), 1: (0, 1), 2: (-1, 1), 3: (-1, 0),
               4: (0, -1), 5: (1, -1)}[m % 6][0],
              {0: (1, 0), 1: (0, 1), 2: (-1, 1), 3: (-1, 0),
               4: (0, -1), 5: (1, -1)}[m % 6][1])


def fmt(z):
    """Print a Qw as a power of w when it is one, else as a decimal."""
    for m in range(6):
        if z == wp(m):
            return "w^%d" % m if m else "1"
    c = z.complex()
    return "%.6f%+.6fi" % (c.real, c.imag)


# ------------------------------------------------------------- matrices
def mat(rows):
    return [[Qw(x) if not isinstance(x, Qw) else x for x in r] for r in rows]


def mmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum_qw(A[i][t] * B[t][j] for t in range(k)) for j in range(m)]
            for i in range(n)]


def sum_qw(xs):
    s = ZERO
    for x in xs:
        s = s + x
    return s


def madd(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def msub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def dagger(A):
    return [[A[j][i].conj() for j in range(len(A))] for i in range(len(A[0]))]


def maxabs(A):
    return max((abs(x) for r in A for x in r), default=0.0)


def to_cplx(A):
    import numpy as np
    return np.array([[x.complex() for x in r] for r in A], dtype=complex)


# ---------------------------------------------------------- the example
# The dephased gauged Fourier matrix of mub-step1-example.pdf is F = (w^(jk)).
# Step 1's canonical arrangement permutes rows to (0,1,2,4,3,5) and columns
# to (0,3,1,2,4,5).  Everything below is that arrangement, called H'.
ROW_ORDER = (0, 1, 2, 4, 3, 5)
COL_ORDER = (0, 3, 1, 2, 4, 5)


def F_matrix():
    return mat([[wp(j * k) for k in range(6)] for j in range(6)])


def Hprime():
    F = F_matrix()
    return [[F[ROW_ORDER[i]][COL_ORDER[j]] for j in range(6)] for i in range(6)]


def blocks(H=None):
    H = H or Hprime()
    E = [r[0:2] for r in H[0:2]]
    B = [r[2:6] for r in H[0:2]]
    C = [r[0:2] for r in H[2:6]]
    D = [r[2:6] for r in H[2:6]]
    return E, B, C, D


# --------------------------------------------------------- exact linalg
def nullspace(M):
    """Basis of {x : M x = 0} for a matrix over Q(w), exact."""
    A = [[x for x in r] for r in M]
    rows, cols = len(A), len(A[0])
    piv, r = [], 0
    for c in range(cols):
        p = None
        for i in range(r, rows):
            if not A[i][c].is_zero():
                p = i
                break
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = Qw(1) / A[r][c]
        A[r] = [x * inv for x in A[r]]
        for i in range(rows):
            if i != r and not A[i][c].is_zero():
                f = A[i][c]
                A[i] = [A[i][j] - f * A[r][j] for j in range(cols)]
        piv.append(c)
        r += 1
        if r == rows:
            break
    free = [c for c in range(cols) if c not in piv]
    basis = []
    for fc in free:
        v = [ZERO] * cols
        v[fc] = ONE
        for i, pc in enumerate(piv):
            v[pc] = -A[i][fc]
        basis.append(v)
    return basis


def gram(V):
    """Hermitian Gram matrix of a list of exact vectors, as Qw."""
    return [[sum_qw(V[i][k] * V[j][k].conj() for k in range(len(V[i])))
             for j in range(len(V))] for i in range(len(V))]


def self_test():
    # field
    w = wp(1)
    assert w * w == wp(2) and wp(6) == ONE and (w / w) == ONE
    assert abs(wp(2) * wp(3)) == 1
    assert (ONE + wp(2) + wp(4)) == ZERO    # 1 + w^2 + w^4 = 0
    # the matrix is Hadamard
    H = Hprime()
    HH = mmul(dagger(H), H)
    for i in range(6):
        for j in range(6):
            assert HH[i][j] == (Qw(6, 0) if i == j else ZERO), (i, j, HH[i][j])
    E, B, C, D = blocks(H)
    assert E == mat([[1, 1], [1, -1]])
    assert B == mat([[1, 1, 1, 1], [wp(1), wp(2), wp(4), wp(5)]])
    assert C == mat([[1, 1], [1, 1], [1, -1], [1, -1]])
    # the block identities used by step 2, exactly
    six = lambda n: [[Qw(6, 0) if i == j else ZERO for j in range(n)] for i in range(n)]
    assert madd(mmul(dagger(B), B), mmul(dagger(D), D)) == six(4)  # B*B + D*D = 6I
    assert madd(mmul(dagger(E), B), mmul(dagger(C), D)) == [[ZERO] * 4 for _ in range(2)]
    print("mubexact self test: OK")
    print("  B'B'* =", [[fmt(x) for x in r] for r in mmul(B, dagger(B))])
    print("  C'C'* =", [[fmt(x) for x in r] for r in mmul(C, dagger(C))])
    print("  D'    =", [[fmt(x) for x in r] for r in D])


if __name__ == "__main__":
    self_test()
