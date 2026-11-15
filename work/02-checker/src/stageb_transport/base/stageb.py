"""Stage-B relation obligations (Lemma 5.1, Proposition 5.2, Lemma 5.3, Lemma 5.5)
checked on stored Records, in exact rational arithmetic with outward-up square roots.

Why this is exactly checkable.  Every quantity in (5.5)-(5.16) is built from
  * stored binary64 entries (exact dyadic rationals),
  * differences of them and the double-centering projection Pi (rational),
  * two square roots and one spectral-norm upper bound.
There is no transcendental function anywhere in Stage B (unlike Root's ||F(P)||).
So the whole relation ledger runs in exact rational arithmetic; the only outward
rounding is `sqrt` (integer square root) and the fixed-point truncation of
intermediate values at 2^-B, always *upward*, so every returned number is an upper
bound of the quantity the paper bounds.

Conventions follow stageB.cpp relationB exactly:
  dq   = Pi( wrap( dp(Q) - dp(P) ) )                    (5.5), wrap = x - nearest int
  eta  = T_P^* dq ,  nq = || (I-T_P T_P^*) dq ||
  total= R + ||dq||,  nu0 = n0_P + id_P R + C_P R^2 + nq,  lam = id_P + C_P total,
  e    = mnorm_P * froot_Q ,  sigma = sqrt(spectralUpper(G)+1e-7)+1e-8,
  G    = W W^* ,  W_a = Pi S_a - sum_j <Pi S_a, T_P[j]> T_P[j] ,  S_a = Pi T_Q[a]
  beta = sqrt(1+o_P) * sqrt((1+o_P)(1+o_Q))
  z(b)= sqrt(1+o_P) t, v(b) = min(nu0, (1+o_P)b, lam b + e),
  psi_P(b) = sqrt(z^2+v(b)^2), psi_Q(b) = sqrt((1+o_Q)(beta t + sigma v(b))^2 + n_Q(b)^2)
  b_0 = min(D, sqrt(z^2+nu0^2)), b_{j+1} = min(b_j, psi_P(b_j), psi_Q(b_j))
"""
import numpy as np
from fractions import Fraction as Q

import num
import rec
import root_float as rf
from num import Dy, dy_sqrt_up, dy_to_fraction
from rootcheck import proj_rat, _scale

B = num.B
ZERO = Dy(0, 0)


# ------------------------------------------------------------ up-arithmetic
def up(x):
    """Upward dyadic bound of a nonnegative rational/dyadic."""
    if isinstance(x, Dy):
        d = x
    elif isinstance(x, float):
        d = Dy.of(x)
    else:
        f = Q(x)
        if f < 0:
            raise ValueError("up() of a negative quantity")
        n, dnm = f.numerator, f.denominator
        n <<= B
        return Dy(-((-n) // dnm), B)
    if d.s <= B:
        return Dy(d.n << (B - d.s), B)
    return Dy(-((-d.n) // (1 << (d.s - B))), B)


def umul(a, b):
    return up(a.as_fraction() * b.as_fraction())


def uadd(a, b):
    return up(a.as_fraction() + b.as_fraction())


def usqrt(a):
    return dy_sqrt_up(up(a), B)


def umin(*xs):
    return min(xs, key=lambda x: x.as_fraction())


# ------------------------------------------------------------------ dephasing
def nearest_int(x):
    """Nearest integer, ties to even (C nearbyint under FE_TONEAREST)."""
    f = Q(x) + Q(1, 2)
    fl = f.numerator // f.denominator
    if f == fl and fl % 2 != 0:       # exact tie and odd candidate -> take the even one
        fl -= 1
    return fl


def dephase(p):
    """dp[i][j] = p_ij - p_i0 - p_0j + p_00 - nearest_int(...), exact."""
    p = [Q(x) for x in p]
    out = []
    for i in range(6):
        for j in range(6):
            z = p[6 * i + j] - p[6 * i] - p[j] + p[0]
            out.append(z - nearest_int(z))
    return out


def wraps(u, v):
    """wrap(v - u) entrywise: any integer lift is sound (Section 5.1)."""
    raw = []
    for h in range(36):
        d = v[h] - u[h]
        raw.append(d - nearest_int(d))
    return raw


# --------------------------------------------------------------- relation core
def spectral_upper(G, k):
    """min(symmetric absolute row bound, sqrt(||G^2||_F)) as an upper bound of ||G||."""
    row = Q(0)
    for i in range(k):
        row = max(row, sum(abs(G[i][j]) for j in range(k)))
    fro4 = Q(0)
    for i in range(k):
        for j in range(k):
            a = sum((G[i][l] * G[l][j] for l in range(k)), Q(0))
            fro4 += a * a
    # ||G||^2 = ||G^2|| <= ||G^2||_F   =>   ||G|| <= sqrt(||G^2||_F);
    # the row bound bounds ||G|| directly.  Both are upper bounds of ||G||.
    fro = usqrt(fro4)                      # ||G^2||_F, upward
    bound = usqrt(fro.as_fraction())       # sqrt(||G^2||_F) >= ||G||
    return min(bound.as_fraction(), row)


class Relation:
    """The certified relation from parent P (radius R) to child Ch."""

    def __init__(self, P, R, Ch, cut=None):
        self.P, self.Ch = P, Ch
        self.R = Q(R)
        self.dpP = dephase(P.p)
        self.dpQ = dephase(Ch.p)
        self.raw = wraps(self.dpP, self.dpQ)
        self.cut = cut
        # (5.5)
        self.dq = proj_rat(self.raw)
        self.sq = usqrt(sum((x * x for x in self.dq), Q(0)))
        self.eta = []
        TP = [[Q(v) for v in row] for row in P.T]
        for a in range(P.k):
            self.eta.append(sum((TP[a][h] * self.dq[h] for h in range(36)), Q(0)))
        w = list(self.dq)
        for a in range(P.k):
            for h in range(36):
                w[h] -= self.eta[a] * TP[a][h]
        self.nq = usqrt(sum((x * x for x in w), Q(0)))
        # (5.7)
        self.total = up(self.R + self.sq.as_fraction())
        self.nu0 = up(Q(P.n0) + Q(P.id) * self.R + Q(P.C) * self.R * self.R
                      + self.nq.as_fraction())
        self.lam = up(Q(P.id) + Q(P.C) * self.total.as_fraction())
        self.e = up(Q(P.mnorm) * Q(Ch.froot))         # e0 >= mu_P * eps_Q   (5.7)
        self._setup()

    def _setup(self):
        """(5.8): sigma >= ||Sh^* A|| from the child tangent frame, beta factor."""
        P, Qr = self.P, self.Ch
        k, kq = P.k, Qr.k
        if kq == 0:
            self.sigma = ZERO
        else:
            TP = [[Q(v) for v in row] for row in P.T]
            TQ = [[Q(v) for v in row] for row in Qr.T]
            S = [proj_rat(TQ[a]) for a in range(kq)]
            W = []
            for a in range(kq):
                wa = list(S[a])
                for j in range(k):
                    cross = sum((S[a][h] * TP[j][h] for h in range(36)), Q(0))
                    for h in range(36):
                        wa[h] -= cross * TP[j][h]
                W.append(wa)
            G = [[sum((W[i][h] * W[j][h] for h in range(36)), Q(0)) for j in range(kq)]
                 for i in range(kq)]
            self.sigma = up(usqrt(spectral_upper(G, kq) + Q(1, 10 ** 7)).as_fraction()
                            + Q(1, 10 ** 8))
        oP, oQ = Q(P.ort), Q(Qr.ort)
        self.beta = umul(usqrt(1 + oP), usqrt((1 + oP) * (1 + oQ)))
        self.oP, self.oQ = oP, oQ

    # ---- the computed function D^(t) of (5.14)-(5.16)
    def D(self, t, iters=30):
        t = up(t)
        z = umul(usqrt(1 + self.oP), t)
        onep = 1 + self.oP
        b = umin(self.total, usqrt(z.as_fraction() ** 2 + self.nu0.as_fraction() ** 2))
        for _ in range(iters):
            v = umin(self.nu0, up(onep * b.as_fraction()),
                     up(self.lam.as_fraction() * b.as_fraction() + self.e.as_fraction()))
            psiP = usqrt(z.as_fraction() ** 2 + v.as_fraction() ** 2)
            tq = up(self.beta.as_fraction() * t.as_fraction()
                    + self.sigma.as_fraction() * v.as_fraction())
            nQ = up(Q(self.Ch.n0) + Q(self.Ch.id) * b.as_fraction()
                    + Q(self.Ch.C) * b.as_fraction() * b.as_fraction())
            psiQ = usqrt(up((1 + self.oQ) * tq.as_fraction() ** 2 + nQ.as_fraction() ** 2)
                         .as_fraction())
            nb = umin(b, psiP, psiQ)
            if nb.as_fraction() >= b.as_fraction():
                break
            b = nb
        return b

    def corner(self, u, h):
        """t_B of Lemma 5.5 (5.24): max over the box of ||eta - eta_q||."""
        s = Q(0)
        for a in range(self.P.k):
            d = abs(Q(u[a]) - self.eta[a]) + Q(h)
            s += d * d
        return usqrt(s)

    def covers(self, u, h, radius):
        """Lemma 5.5: box -> sphere inclusion, certified upper bound <= radius."""
        t = self.corner(u, h)
        if t.as_fraction() > 2:
            return None, None, None
        d = self.D(t)
        return (d.as_fraction() <= Q(radius)), d, t
