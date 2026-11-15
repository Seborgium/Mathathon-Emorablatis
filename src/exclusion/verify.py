"""Independent deterministic verifier for a certificate y.

The inequality y.c_all > B(y) is re-evaluated in 60-digit arithmetic from the cell
data, and the data's own double-precision uncertainty is bounded explicitly, so the
verdict does not rest on any float64 comparison.
"""
import numpy as np
from mpmath import mp, mpf, sqrt, fabs, nsum
mp.dps = 60

def _v(x):
    return [mpf(float(t)) for t in np.asarray(x).reshape(-1)]

def margin_hp(cell, y, dps=60):
    mp.dps = dps
    c = _v(cell.c_all); Y = _v(y); J = [[mpf(float(t)) for t in r] for r in cell.Jall]
    yD = np.asarray(y, float)[:16]
    # g = Jall^T y
    g = [sum(J[i][k] * Y[i] for i in range(20)) for k in range(13)]
    gs = sqrt(sum(g[k] ** 2 for k in range(9)))
    gt = sum(fabs(g[k]) for k in range(9, 13))
    W = _v(cell.Wabs); y16 = Y[:16]
    WD = sqrt(sum((W[i] * y16[i]) ** 2 for i in range(16)))
    neg = max([mpf(0)] + [-y16[i] for i in range(16)])
    xy = (sqrt(y16[0] * 0 + Y[16] ** 2 + Y[17] ** 2) + sqrt(Y[18] ** 2 + Y[19] ** 2))
    R_s = mpf(float(cell.Rs)); h = mpf(float(cell.h)); E_r = mpf(float(cell.Er)); z = mpf(float(cell.z))
    B = R_s * gs + h * gt + E_r * WD + (z ** 2) * neg / 2 + (R_s ** 2) * xy / 2
    lhs = sum(c[i] * Y[i] for i in range(20))
    return lhs, B, lhs - B

def data_uncertainty(cell, y, u=1.1e-16):
    """Crude but explicit bound on how much the margin moves if every stored scalar of
    c_all, Jall, D carries a relative error <= u (the budget of the double-precision
    linear algebra that produced them)."""
    y = np.asarray(y, float)
    d1 = u * np.abs(cell.c_all).sum() * np.abs(y).max() * 20
    d2 = u * (cell.Rs * np.abs(y).sum() + cell.h * np.abs(y).sum()) * np.abs(cell.Jall).sum()
    d3 = u * 4 * cell.Er * np.abs(y[:16]).sum()
    return d1 + d2 + d3

def certify(cell, y, label=""):
    lhs, B, m = margin_hp(cell, y)
    j = margin_hp(cell, y, dps=40)
    err = fabs(m - j[2])
    du = data_uncertainty(cell, y)
    ok = (m > 0) and (m > 10 * max(err, mpf(1e-50))) and (m > 10 * du)
    return dict(label=label, margin=str(m), dps_gap=str(err), data_bound=float(du),
                verdict="CERTIFIED" if ok else "NOT CERTIFIED")
