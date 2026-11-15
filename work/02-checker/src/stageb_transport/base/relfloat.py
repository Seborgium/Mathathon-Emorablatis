"""Faithful float port of stageB.cpp relationB::init/eval, used ONLY to cross-check
the exact-rational implementation of stageb.Relation (independent code path)."""
import numpy as np
import root_float as rf


def wrap(x):
    return x - np.rint(x)


def dephase_f(p):
    p = np.asarray(p, float).reshape(6, 6)
    z = p - p[:, :1] - p[:1, :] + p[0, 0]
    return (z - np.rint(z)).reshape(36)


def relation_float(P, Q, R, target, allowFar=False):
    k, kq = P.k, Q.k
    TP = np.asarray(P.T, float).reshape(-1, 36)
    TQ = np.asarray(Q.T, float).reshape(-1, 36)
    dpP, dpQ = dephase_f(P.p), dephase_f(Q.p)
    raw = wrap(dpQ - dpP)
    cut = .249 if allowFar else min(.23, R + target + 1e-6)
    if np.max(np.abs(raw)) > 2 * cut + 1e-7:
        return None
    dq = rf.proj(raw)
    sq = float(np.linalg.norm(dq))
    if not sq <= cut + 1e-6:
        return None
    eta = TP @ dq
    nq = float(np.linalg.norm((dq - TP.T @ eta))) + 1e-8
    total = R + sq + 1e-8
    nu0 = P.n0 + P.id * R + P.C * R * R + nq + 1e-8
    lam = P.id + P.C * total + 1e-8
    e = P.mnorm * Q.froot + 1e-7
    if kq == 0:
        sig = 0.0
    else:
        S = np.array([rf.proj(TQ[a]) for a in range(kq)])
        W = np.array([S[a] - sum(S[a] @ TP[j] * TP[j] for j in range(k)) for a in range(kq)])
        G = W @ W.T
        row = np.max(np.sum(np.abs(G), axis=1))
        fro4 = 0.0
        for i in range(kq):
            for j in range(kq):
                a = G[i] @ G[:, j]
                fro4 += a * a
        su = min(row + 1e-10, np.sqrt(np.sqrt(fro4)) + 2e-7)
        sig = float(np.sqrt(su + 1e-7) + 1e-8)
    beta = np.sqrt(1 + P.ort) * np.sqrt((1 + P.ort) * (1 + Q.ort))
    oP, oQ = P.ort, Q.ort

    def D(t):
        t = t + 2e-8
        z = np.sqrt(1 + oP) * t + 1e-9
        d = min(total + 1e-8, np.hypot(z, nu0) + 1e-8)
        for _ in range(30):
            v = min(nu0, min((1 + oP) * d, lam * d + e)) + 1e-8
            ep = (1 + oP) * np.sqrt((1 + oP) * (1 + oQ)) * t + sig * v + 1e-8
            d1 = np.hypot(z, v) + 1e-8
            d2 = np.hypot(np.sqrt(1 + oQ) * ep, Q.n0 + Q.id * d + Q.C * d * d) + 1e-8
            nd = min(d1, d2)
            if nd >= d:
                break
            d = nd
        return d + 1e-8
    return dict(dq=dq, sq=sq, eta=eta, nq=nq, total=total, nu0=nu0, lam=lam, e=e,
                sigma=sig, beta=float(beta), D=D)
