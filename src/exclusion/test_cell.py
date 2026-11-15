"""Deterministic checks on the cell implementation.

(1) u_params / V_of_params / dU_theta consistency: finite differences on (3.12).
(2) J(s,theta) against finite differences of the *literal* orthogonality pieces
    (3.16),(3.17),(3.18), with the seed varied in E',B',C' and D' varied only
    through the unitary family -- the precise sense in which (3.23) is a linear
    comparison and not a total derivative.
"""
import numpy as np
from cell import Cell, V_of_params, u_params, dU_theta

def rand_U(seed):
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    Q, R = np.linalg.qr(A)
    return Q * (np.diag(R) / abs(np.diag(R)))

def hadamard_seed(H):
    Hd = H / H[:, 0][None, :] / H[0, :][:, None]
    return Hd[1, 1], Hd[1, 2:6], Hd[2:6, 1], Hd[2:, 2:]

F6 = np.exp(2j * np.pi * np.outer(range(6), range(6)) / 6)
F23 = np.kron(np.exp(2j * np.pi * np.outer(range(2), range(2)) / 2),
              np.exp(2j * np.pi * np.outer(range(3), range(3)) / 3))

def test_dU():
    for sd in range(5):
        U = rand_U(sd)
        al, t, be, ga = u_params(U)
        assert np.allclose(V_of_params(al, t, be, ga), U)
        D = dU_theta(U); h = 1e-6
        for k in range(4):
            p = [al, t, be, ga]; p[k] += h / (2 * np.pi)   # radians -> cycles
            assert np.allclose((V_of_params(*p) - U) / h, D[k], atol=2e-6), k
    print("dU_theta: OK  (4 derivatives, 5 random U, finite differences of (3.12))")

def Z_pieces(cell, s, V, Umid=None):
    E0, B0, C0 = cell.E0, cell.B0, cell.C0
    E1 = np.zeros((2, 2), complex); E1[1, 1] = 1j * cell.a * s[0]
    B1 = np.zeros((2, 4), complex); B1[1, :] = 1j * cell.b * np.asarray(s[1:5])
    C1 = np.zeros((4, 2), complex); C1[:, 1] = 1j * cell.c * np.asarray(s[5:9])
    Ep, Bp, Cp = E0 + E1, B0 + B1, C0 + C1
    Um = cell.U if Umid is None else Umid
    Dp = -C0 @ E0.conj().T @ cell.GB.conj().T + np.sqrt(6) * cell.KC @ V @ cell.KB.conj().T
    z16 = (-(Cp - C0) @ E0.conj().T - Cp @ (Ep - E0).conj().T - Dp @ (Bp - B0).conj().T) @ cell.GB.conj().T
    z17 = cell.GC @ (-E0.conj().T @ (Bp - B0) - (Cp - C0).conj().T @ Dp) @ cell.PK
    z18 = cell.KC @ (cell.KC.conj().T @ Dp @ cell.KB - np.sqrt(6) * Um) @ cell.KB.conj().T
    return z16 + z17 + z18

def test_J(cell, h=1e-6):
    U = cell.U
    al, t, be, ga = u_params(U)
    Z0 = Z_pieces(cell, np.zeros(9), U)
    Jfd = np.zeros((20, 13))
    coefX = np.zeros(9, complex); coefX[0] = cell.a; coefX[1:5] = cell.b
    coefY = np.zeros(9, complex); coefY[0] = cell.a; coefY[5:9] = cell.c
    for k in range(9):
        e = np.zeros(9); e[k] = h
        Zp = Z_pieces(cell, e, U)
        Jfd[:16, k] = np.real(np.conj(cell.D).reshape(-1) * ((Zp - Z0) / h).reshape(-1))
        Jfd[16, k] = np.real(coefX)[k]; Jfd[17, k] = np.imag(coefX)[k]
        Jfd[18, k] = np.real(coefY)[k]; Jfd[19, k] = np.imag(coefY)[k]
    for k in range(4):
        th = np.zeros(4); th[k] = h
        p = [al + th[0] / (2 * np.pi), t + th[1] / (2 * np.pi),
             be + th[2] / (2 * np.pi), ga + th[3] / (2 * np.pi)]
        Zp = Z_pieces(cell, np.zeros(9), V_of_params(*p), Umid=U)
        Jfd[:16, 9 + k] = np.real(np.conj(cell.D).reshape(-1) * ((Zp - Z0) / h).reshape(-1))
    return np.abs(Jfd - cell.Jall).max()

if __name__ == "__main__":
    test_dU()
    for name, H in [("F6", F6), ("F2xF3", F23)]:
        a, b, c, Dp = hadamard_seed(H)
        for iu, U in enumerate((rand_U(1), rand_U(2))):
            cell = Cell(a, b, c, U, 16)
            err = test_J(cell)
            print("%-6s U%d m=%.6f A0=%.6f p=%.3e z=%.4f Er=%.3e |c_all|=%.2e rankJ=%d  max|J_fd-J|=%.2e"
                  % (name, iu, cell.m, cell.A0, cell.p, cell.z, cell.Er,
                     np.linalg.norm(cell.c_all), np.linalg.matrix_rank(cell.Jall), err))
