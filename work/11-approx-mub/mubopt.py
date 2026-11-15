"""Minimise max_{a<b} dev(a,b) over U(6)^4, gauge U_1 = I, by Riemannian gradient descent."""
import numpy as np
from scipy.linalg import expm

D = 6
NB = 3                      # free bases U_2,U_3,U_4

def devs_from(Us):
    return np.concatenate([(np.abs(Us[a].conj().T @ Us[b])**2 - 1.0/D).ravel()
                           for a in range(len(Us)) for b in range(a+1, len(Us))])

def maxdev(Us):
    return np.abs(devs_from(Us)).max()

def e2(Us):
    return float((devs_from(Us)**2).sum())

def lse(Us, beta):
    x = np.abs(devs_from(Us)); m = x.max()
    return m + np.log(np.exp(beta*(x-m)).sum())/beta - np.log(len(x))/beta

def grad_generic(Us, gfun):
    """gfun(v) -> d(objective)/d |D_k| ; returns body gradients (list) and maxdev."""
    n = len(Us)
    G = [np.zeros((D, D), dtype=complex) for _ in range(n)]
    vals, mats = [], []
    for a in range(n):
        for b in range(a+1, n):
            X = Us[a].conj().T @ Us[b]
            mats.append((a, b, X))
            vals.append((np.abs(X)**2 - 1.0/D).ravel())
    v = np.concatenate(vals)
    g = gfun(v)
    off = 0
    for (a, b, Xc) in mats:
        M = (g[off:off+D*D]*np.conj(Xc).ravel()).reshape(D, D)
        off += D*D
        G[a] += Us[b] @ M.T
        G[b] += Us[a] @ np.conj(M)
    out = []
    for a in range(n):
        Hh = Us[a].conj().T @ G[a]
        out.append(Hh - (Hh + Hh.conj().T)/2.0)
    return out, maxdev(Us)

def grad_e2(Us):
    return grad_generic(Us, lambda v: 2.0*v)

def grad_lse_(Us, beta):
    def gfun(v):
        av=np.abs(v); m=av.max(); w=np.exp(beta*(av-m)); w/=w.sum()
        return w*np.sign(v)
    return grad_generic(Us, gfun)

def descend_e2(Us, iters=3000, eta=1.0):
    f=e2(Us)
    for it in range(iters):
        G,_=grad_e2(Us)
        gn=np.sqrt(sum((g.conj()*g).real.sum() for g in G))
        if gn<1e-14: break
        step=eta
        while step>1e-14:
            cand=[Us[0]]+[Us[a+1]@expm(-step*G[a+1]) for a in range(NB)]
            fc=e2(cand)
            if fc<f-1e-18: break
            step*=0.5
        else: break
        Us,f=cand,fc
    return Us,f

    """Riemannian (tangent-space) gradient of lse, list matching Us (U_1 gradient ignored)."""
    n = len(Us)
    G = [np.zeros((D, D), dtype=complex) for _ in range(n)]
    vals, mats = [], []
    for a in range(n):
        for b in range(a+1, n):
            X = Us[a].conj().T @ Us[b]
            P = np.abs(X)**2
            Xc = X
            mats.append((a, b, Xc))
            vals.append((P - 1.0/D).ravel())
    v = np.concatenate(vals); av = np.abs(v); m = av.max()
    w = np.exp(beta*(av-m)); w /= w.sum()
    g = w*np.sign(v)                                    # d f / d |D_k|
    off = 0
    for (a, b, Xc) in mats:
        M = (g[off:off+D*D]*np.conj(Xc).ravel()).reshape(D, D)   # m_ij = w s conj(X_ij)
        off += D*D
        G[a] += Us[b] @ M.T
        G[b] += Us[a] @ np.conj(M)
    out = []
    for a in range(n):
        H = Us[a].conj().T @ G[a]
        H = H - (H + H.conj().T)/2.0                    # remove Hermitian part -> anti-Hermitian
        out.append(H)
    return out, maxdev(Us)

def tangent_basis():
    """orthonormal basis of u(6) (anti-Hermitian), real coordinates."""
    Bs = []
    for i in range(D):
        E = np.zeros((D, D), dtype=complex); E[i, i] = 1j; Bs.append(E)
    for i in range(D):
        for j in range(i+1, D):
            E = np.zeros((D, D), dtype=complex); E[i, j] = 1; E[j, i] = -1; Bs.append(E)
            E = np.zeros((D, D), dtype=complex); E[i, j] = 1j; E[j, i] = 1j; Bs.append(E)
    return Bs

def check_grad(Us, beta, eps=1e-6):
    Bs = tangent_basis()
    G, _ = grad_lse(Us, beta)
    err = 0.0
    for a in range(NB):
        for k in range(D*D):
            Up = list(Us); Up[a+1] = Us[a+1] @ expm(eps*Bs[k])
            Um = list(Us); Um[a+1] = Us[a+1] @ expm(-eps*Bs[k])
            fd = (lse(Up, beta) - lse(Um, beta))/(2*eps)
            an = 2*np.real(np.trace(G[a+1].conj().T @ (Us[a+1] @ Bs[k])))
            err = max(err, abs(fd-an))
    return err

def grad_lse(Us, beta):
    return grad_lse_(Us, beta)

def descend(Us, beta, iters=400, eta=1.0, tol=1e-14):
    f = lse(Us, beta)
    for it in range(iters):
        G, _ = grad_lse(Us, beta)
        gn = np.sqrt(sum((g.conj()*g).real.sum() for g in G))
        if gn < 1e-13: break
        step = eta
        while step > 1e-12:
            cand = [Us[0]] + [Us[a+1] @ expm(-step*G[a+1]) for a in range(NB)]
            fc = lse(cand, beta)
            if fc < f - 1e-15: break
            step *= 0.5
        else:
            break
        Us, f = cand, fc
    return Us, f

def polish(Us, betas=(3e1, 3e2, 3e3, 3e4, 3e5)):
    for b in betas:
        Us, _ = descend(Us, b)
    return Us
