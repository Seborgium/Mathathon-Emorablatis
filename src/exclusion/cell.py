"""Faithful implementation of the Stage-A cell data of Section 3.1--3.6.

Reference: "The maximum number of mutually unbiased bases in dimension six",
24 Sep 2026, Sections 3.1-3.6, Lemma 3.9, (3.23)-(3.29).

Conventions
-----------
s      : seed displacement, order (sa, sb0..sb3, sc0..sc3)            in R^9
theta  : unitary-cell displacement (alpha, t, beta, gamma) in radians in R^4
y      : direction in R^20 = (yD (4x4 row-major), Re yX, Im yX, Re yY, Im yY)
c_all  : R^20 = (c_ij, Re cX, Im cX, Re cY, Im cY)
Jall   : R^{20 x 13}, columns = d/ds (9) then d/dtheta (4)
"""
import numpy as np

# ---------------------------------------------------------------- seed data
def blocks(a, b, c):
    E0 = np.array([[1.0, 1.0], [1.0, a]], dtype=complex)
    B0 = np.vstack([np.ones(4), np.asarray(b, dtype=complex)])
    C0 = np.column_stack([np.ones(4), np.asarray(c, dtype=complex)])
    return E0, B0, C0


def frames(B0, C0):
    """GB, GC, KB, KC as in (3.5); KB spans ker B0, KC spans ker C0^*."""
    def pinv_right(M):            # M (k x n), return n x k with M M^+ = I  => G = M^*(M M^*)^-1
        return M.conj().T @ np.linalg.inv(M @ M.conj().T)
    GB = pinv_right(B0)                       # B0 is 2x4: B0 B0^* invertible
    GC = C0 @ np.linalg.inv(C0.conj().T @ C0)  # C0 is 4x2: C0^* C0 invertible
    # orthonormal bases of ker B0 (in C^4) and ker C0^* (in C^4)
    def kern(M):
        u, s, vh = np.linalg.svd(M)
        r = int(np.sum(s > 1e-9 * max(1.0, s[0])))
        return vh[r:].conj().T          # columns span ker M
    KB = kern(B0)
    KC = kern(C0.conj().T)
    return GB, GC, KB, KC


def u_params(U):
    """(alpha, t, beta, gamma) in cycles/param ranges of (3.12), from U in U(2)."""
    alpha = np.angle(np.linalg.det(U)) / (4 * np.pi)   # det V = e(2 alpha)
    W = np.exp(-2j * np.pi * alpha) * U
    z, w = W[0, 0], W[0, 1]
    t = np.arccos(min(1.0, abs(z))) / (2 * np.pi)
    beta = np.angle(z) / (2 * np.pi)
    gamma = np.angle(w) / (2 * np.pi) if abs(w) > 1e-14 else 0.0
    return alpha, t, beta, gamma


def dU_theta(U):
    """The four angular derivatives dU_k = dU/dtheta_k at midpoint U, k=(a,t,b,g).

    Radian angles.  alpha-derivative iU; beta-diagonal; gamma off-diagonal;
    t-derivative from the sine/cosine factors of (3.12)."""
    alpha, t, beta, gamma = u_params(U)
    ea = np.exp(2j * np.pi * alpha)
    c, s = np.cos(2 * np.pi * t), np.sin(2 * np.pi * t)
    D = []
    D.append(1j * U)                                            # d/da
    # d/dt
    dt = np.zeros((2, 2), dtype=complex)
    dt[0, 0] = -ea * np.exp(2j * np.pi * beta) * s
    dt[0, 1] = ea * np.exp(2j * np.pi * gamma) * c
    dt[1, 0] = -ea * np.exp(-2j * np.pi * gamma) * c
    dt[1, 1] = -ea * np.exp(-2j * np.pi * beta) * s
    D.append(dt)
    db = np.array([[1j * U[0, 0], 0], [0, -1j * U[1, 1]]], dtype=complex)
    D.append(db)
    dg = np.array([[0, 1j * U[0, 1]], [-1j * U[1, 0], 0]], dtype=complex)
    D.append(dg)
    return np.array(D)


def V_of_params(alpha, t, beta, gamma):
    """(3.12) evaluated; used to check u_params/dU_theta."""
    ea = np.exp(2j * np.pi * alpha)
    E = np.array([[np.exp(2j * np.pi * beta) * np.cos(2 * np.pi * t),
                   np.exp(2j * np.pi * gamma) * np.sin(2 * np.pi * t)],
                  [-np.exp(-2j * np.pi * gamma) * np.sin(2 * np.pi * t),
                   np.exp(-2j * np.pi * beta) * np.cos(2 * np.pi * t)]])
    return ea * E


class Cell:
    """All Stage-A cell data for one (seed centre, U(2) midpoint, level Nu)."""

    def __init__(self, a, b, c, U, Nu, rs=0.0320001):
        self.a, self.b, self.c, self.U, self.Nu = a, np.asarray(b, complex), np.asarray(c, complex), U, Nu
        self.rs = rs
        self.Rs = 2 * np.pi * rs
        self.h = np.pi / Nu
        self.E0, self.B0, self.C0 = blocks(a, b, c)
        self.GB, self.GC, self.KB, self.KC = frames(self.B0, self.C0)
        self.mB = np.linalg.svd(self.B0, compute_uv=False)[-1]
        self.mC = np.linalg.svd(self.C0, compute_uv=False)[-1]
        self.m = min(self.mB, self.mC)
        self.A0 = np.sqrt(2 + abs(1 + a))
        self.As = min(2.0, self.A0 + self.Rs)
        self.PK = self.KB @ self.KB.conj().T
        self.PB = np.eye(4) - self.PK
        self.PC = np.eye(4) - self.KC @ self.KC.conj().T
        self.D = -self.C0 @ self.E0.conj().T @ self.GB.conj().T \
            + np.sqrt(6) * self.KC @ U @ self.KB.conj().T
        self.q = self.Rs ** 2 * (1 + (self.As ** 2 + 6) / self.mC ** 2)
        self.p = np.sqrt(self.q) / (np.sqrt(6) + np.sqrt(6 - self.q))
        self.z = np.sqrt((self.Rs * (np.sqrt(6) + self.As) / self.m) ** 2 + (6 * self.h + self.p) ** 2)
        self.C0op = np.linalg.norm(self.C0, 2)
        self.L = max(np.sqrt(6), self.C0op * np.sqrt(1 + (self.A0 / self.mB) ** 2))
        self.eoff = self.Rs ** 2 * (self.L + self.A0 + 1) / (2 * self.m) + self.z * self.Rs / self.m
        self.Er = np.sqrt(self.eoff ** 2 + (np.sqrt(6) * 42 / 2 * self.h ** 2 + self.p) ** 2)
        self.dU = dU_theta(U)
        self._build_all()

    # ------------------------------------------------ J(s,theta)  (3.23)
    def J(self, s, th=(0, 0, 0, 0)):
        E1 = np.zeros((2, 2), dtype=complex); E1[1, 1] = 1j * self.a * s[0]
        B1 = np.zeros((2, 4), dtype=complex); B1[1, :] = 1j * self.b * np.asarray(s[1:5])
        C1 = np.zeros((4, 2), dtype=complex); C1[:, 1] = 1j * self.c * np.asarray(s[5:9])
        dU = sum(np.asarray(th, float)[k] * self.dU[k] for k in range(4))
        return ((-C1 @ self.E0.conj().T - self.C0 @ E1.conj().T - self.D @ B1.conj().T) @ self.GB.conj().T
                + self.GC @ (-self.E0.conj().T @ B1 - C1.conj().T @ self.D) @ self.PK
                + np.sqrt(6) * self.KC @ dU @ self.KB.conj().T)

    def _build_all(self):
        self.Jall = np.zeros((20, 13))
        self.Jc = np.zeros((4, 4, 13), dtype=complex)   # dJ_ij/du_k, u=(s,theta)
        for k in range(13):
            u = np.zeros(13); u[k] = 1.0
            Jk = self.J(u[:9], u[9:])
            self.Jc[:, :, k] = Jk
            self.Jall[:16, k] = np.real(np.conj(self.D).reshape(-1) * Jk.reshape(-1))
        # seed-sum rows: cX + JX s, weight i.e. cX = (1+a+sum b)/i
        cX = (1 + self.a + self.b.sum()) / 1j
        cY = (1 + self.a + self.c.sum()) / 1j
        self.cX, self.cY = cX, cY
        coefX = np.zeros(9, complex); coefX[0] = self.a; coefX[1:5] = self.b
        coefY = np.zeros(9, complex); coefY[0] = self.a; coefY[5:9] = self.c
        self.Jall[16, :9] = np.real(coefX)
        self.Jall[17, :9] = np.imag(coefX)
        self.Jall[18, :9] = np.real(coefY)
        self.Jall[19, :9] = np.imag(coefY)
        self.c_all = np.concatenate([((np.abs(self.D) ** 2 - 1) / 2).reshape(-1),
                                     [np.real(cX), np.imag(cX), np.real(cY), np.imag(cY)]])
        self.flat = np.zeros((4, 4))
        self.Wabs = np.abs(self.D).reshape(-1)          # for ||D o yD||_F = ||W yD||

    # ------------------------------------------------ (3.29)
    def B1(self, y):
        """Right-hand side of (3.29) -- the paper's bound."""
        y = np.asarray(y, float)
        yD = y[:16].reshape(4, 4)
        g = self.Jall.T @ y
        gs, gt = g[:9], g[9:]
        return (self.Rs * np.linalg.norm(gs) + self.h * np.abs(gt).sum()
                + self.Er * np.linalg.norm(self.Wabs * y[:16])
                + 0.5 * self.z ** 2 * max(0.0, -yD.min())
                + 0.5 * self.Rs ** 2 * (np.linalg.norm(y[16:18]) + np.linalg.norm(y[18:20])))

    def margin(self, y):
        return y @ self.c_all - self.B1(y)

    def normtest(self):
        """(3.26)"""
        return np.sum((np.abs(self.D) - 1) ** 2) - self.z ** 2
