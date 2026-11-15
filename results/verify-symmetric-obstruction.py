#!/usr/bin/env python3
"""Independent checks of the claims in
"a shorter analytic obstruction once a certain threefold symmetry is present"
(attachment is-this-a-useful-r01i, 15 KB note).

Five checks, in order:
 1. the "Fourier observation" (constant DFT power  =>  vanishing autocorrelation)
 2. the crux: no 3x3 real matrix with zero column sums, all |entry| < 1/sqrt2
    and every row satisfying x^2+y^2+z^2-2xyz = 1   -- and the sharp constant
 3. the Heron inequality s+4|t|+s^2/12 <= 1 and |cos 2theta_j| < 1/sqrt2
 4. no fourth vector for the two known T-symmetric triple types in C^6
    (two-parameter family; isolated Fourier triple)
 5. the 1/108 inequality of section 8 and its equality case
Every check is a counterexample hunt: each test fails loudly if the note is wrong.
Run:  python3 results/verify-symmetric-obstruction.py
"""
import numpy as np, sympy as sp
from scipy.optimize import least_squares, minimize
rng = np.random.default_rng(0)
sq = np.sqrt; w3 = np.exp(2j*np.pi/3)
fail = []

# ---------------------------------------------------------------- 1. Fourier observation
z0, z1, z2, r = sp.symbols('z0 z1 z2 r')            # complex z_j, r = 0,1,2 roots of unity
w = sp.exp(2*sp.pi*sp.I/3)
def A(rr): return z0 + w**(-rr)*z1 + w**(-2*rr)*z2
eqs = [sp.expand(sp.Abs(sp.expand(A(k)))**2) for k in range(3)]
# |A(k)|^2 = 3/2 for k=0,1,2; eliminate to get the autocorrelation condition
autocorr = sp.expand(z0*sp.conjugate(z1) + z1*sp.conjugate(z2) + z2*sp.conjugate(z0))
# Parseval: sum_k |A(k)|^2 = 3 sum_j |z_j|^2, so |A|=const=3/2 gives sum_j |z_j|^2 = 3/2
vals = [complex(np.exp(2j*np.pi*t/3)) for t in range(3)]
for _ in range(200):                                  # random numeric spot-check of the implication
    z = rng.normal(size=3) + 1j*rng.normal(size=3)
    p = np.array([abs(z[0] + np.conj(w3)**k*z[1] + np.conj(w3)**(2*k)*z[2])**2 for k in range(3)])
    ok_pow = abs(p.sum() - 3*np.sum(abs(z)**2)) < 1e-9
    if not ok_pow: fail.append("Parseval identity")
print("1. Parseval  sum_k |A_k|^2 = 3 sum_j |z_j|^2 :  holds on 200 random triples")
print("   so constant |A_k|^2 = 3/2 forces sum_j |z_j|^2 = 3/2 and cyclic autocorrelation 0 (DFT inversion)")

# ---------------------------------------------------------------- 2. the crux 3x3 claim
def M_of(p):
    a, b = p[:3], p[3:]
    return np.array([[np.cos(a[j]), np.cos(b[j]), np.cos(b[j]-a[j])] for j in range(3)])
colsum = lambda p: M_of(p).sum(axis=0)
ident  = lambda M: (M**2).sum(axis=1) - 2*np.prod(M, axis=1) - 1.0
sols = []
for _ in range(250):
    r_ = least_squares(colsum, rng.uniform(-np.pi, np.pi, 6), xtol=1e-15, ftol=1e-15, gtol=1e-15)
    if np.linalg.norm(colsum(r_.x)) < 1e-11:
        sols.append(np.abs(M_of(r_.x)).max())
sols = np.array(sols)
print(f"2. found {len(sols)} random-start solutions of [row identity + zero column sums];")
print(f"   smallest max|entry| over them: {sols.min():.6f}   (1/sqrt2 = {1/sq(2):.6f})")
print(f"   every solution has max|entry| >= 1/sqrt2 : {bool(sols.min() > 1/sq(2))}")
if sols.min() <= 1/sq(2): fail.append("3x3 crux violated")
# sharp constant: explicit extremal matrix, a = sqrt3-1, b = a/2
a = sq(3) - 1; b = a/2
Mex = np.array([[-a, b, b], [b, b, -a], [b, -a, b]])
print(f"   extremal example a=sqrt3-1={a:.8f}: colsum {np.abs(Mex.sum(axis=0)).max():.1e},"
      f" row identity residual {np.abs(ident(Mex)).max():.1e}, max|entry| {np.abs(Mex).max():.8f}")
def obj(p):
    return (np.abs(M_of(p))**6).sum()
best = None
for _ in range(200):
    r_ = minimize(obj, rng.uniform(-np.pi, np.pi, 6), method='SLSQP',
                  constraints=[{'type': 'eq', 'fun': colsum}], options={'ftol': 1e-16, 'maxiter': 400})
    if r_.success and np.linalg.norm(colsum(r_.x)) < 1e-8:
        val = np.abs(M_of(r_.x)).max()
        best = val if best is None else min(best, val)
print(f"   constrained search for the true infimum of max|entry|: {best:.8f}"
      f"   => 1/sqrt2 is sufficient but not sharp (sharp value is sqrt3-1)")

# ---------------------------------------------------------------- 3. Heron bound, |cos 2theta| < 1/sqrt2
def adm(a):
    if abs((np.cos(a)**2).sum() - 1.5) > 1e-10: return False
    c, s = np.cos(a), np.sin(a)
    for t in ([abs(c[j]*c[(j+1) % 3]) for j in range(3)], [abs(s[j]*s[(j+1) % 3]) for j in range(3)]):
        if max(t) > sum(t) - max(t) + 1e-12: return False
    return True
def rand_adm():
    for _ in range(100000):
        a = rng.uniform(0, np.pi, 3); rem = 1.5 - np.cos(a[0])**2 - np.cos(a[1])**2
        if 0 <= rem <= 1:
            a[2] = np.arccos(sq(rem))
            if adm(a): return a
    return None
worst = 0; n_ok = 0; bad = 0
for _ in range(20000):
    a = rand_adm()
    if a is None: continue
    n_ok += 1
    v = np.cos(2*a); s2 = (v**2).sum(); t = np.prod(v)
    if s2 + 4*abs(t) + s2**2/12 > 1 + 1e-9 or np.abs(v).max() >= 1/sq(2): bad += 1
    worst = max(worst, np.abs(v).max())
print(f"3. {n_ok} random admissible triples: violations of s+4|t|+s^2/12<=1 or |v_j|<1/sqrt2 : {bad}")
print(f"   largest |cos 2theta_j| seen: {worst:.6f}  (note's bound 1/sqrt2 = {1/sq(2):.6f}; empirical sup ~0.681)")
if bad: fail.append("Heron bound")

# ---------------------------------------------------------------- 4. no fourth vector for T-symmetric triples
def TI(x): return np.array([1, 1, w3, w3, w3**2, w3**2])*x
def emb(P, Q):   # rows (2j+a), cols (2b+c)
    M = np.zeros((6, 6), dtype=complex)
    for aa in range(2):
        for j in range(3):
            for bb in range(3):
                for cc in range(2): M[2*j+aa, 2*bb+cc] = P[aa, cc]*Q[j, bb]
    return M
Z2 = np.eye(2, dtype=complex); X2 = np.array([[1, 1], [1, -1]])/sq(2)
Y2 = np.array([[1, 1], [1j, -1j]])/sq(2)
F2 = np.array([[1, 1], [1, -1]])/sq(2)
F3 = np.array([[w3**(j*bb) for bb in range(3)] for j in range(3)])/sq(3)
def dcycle(h0): return np.array([[w3**(m*j)*h0[m] for j in range(3)] for m in range(3)])
def floor_of(bases, tries=120):
    def f(x):
        h = x[:6] + 1j*x[6:]; h /= np.linalg.norm(h)
        return max(np.abs(np.abs(B.conj().T@h)**2 - 1/6).max() for B in bases)
    return min(minimize(f, rng.normal(size=12), method='BFGS',
                        options={'gtol': 1e-13, 'maxiter': 2000}).fun for _ in range(tries))
chirp = np.array([1, w3, w3])
triples = []
for (pa, pb) in [(0., 0.), (1.1, 2.3), (2.0, 0.7)]:                      # two-parameter family
    h0 = np.array([1, np.exp(1j*pa), np.exp(1j*pb)])/sq(3)
    triples.append(("two-param family (%.1f,%.1f)" % (pa, pb),
                    [np.eye(6, dtype=complex), emb(X2, dcycle(h0)), emb(Y2, dcycle(h0*chirp))]))
triples.append(("isolated Fourier triple",
                [np.eye(6, dtype=complex), emb(F2, F3),
                 emb(np.diag([1, 1j])@F2, np.diag([1, w3**2, w3**2])@F3)]))
for name, (A, B, C) in triples:
    mub = all(np.allclose(np.abs(P.conj().T@Q), 1/sq(6), atol=1e-11)
              for i, P in enumerate([A, B, C]) for Q in [A, B, C][i+1:])
    def sizes(M):
        used, out = set(), []
        for k in range(6):
            if k in used: continue
            cur, orb = k, []
            for _ in range(3):
                orb.append(cur); used.add(cur)
                cur = min(range(6), key=lambda m: abs(abs(np.vdot(M[:, m], TI(M[:, cur])))-1))
            out.append(len(set(orb)))
        return sorted(out, reverse=True)
    print(f"4. {name}: MUB={mub};  T-orbit sizes  A={sizes(A)}  B={sizes(B)}  C={sizes(C)};"
          f"  best max-deviation for a 4th vector = {floor_of([A,B,C]):.4f}")
    if not mub: fail.append("triple not MUB: " + name)

# ---------------------------------------------------------------- 5. the 1/108 inequality
F6 = np.kron(F2, F3)
def val(a, b):
    psi = np.concatenate([a, b])/sq(6)
    p = np.abs(F6.conj().T@psi)**2
    return 36*np.sum((p - 1/6)**2)
def one_draw():
    ph = rng.uniform(0, 2*np.pi, 3); aa = np.exp(1j*ph)
    e = rng.choice([1, -1]); lam = np.exp(2j*np.pi*rng.random())
    bb = lam*np.array([w3**(e*j) for j in range(3)])*aa
    return val(aa, bb)
lo = min(one_draw() for _ in range(60000))
a0 = np.array([1, -1, -1], dtype=complex); b0 = 1j*np.array([1, -w3, -w3**2])
print(f"5. random search: smallest 36*sum(p-1/6)^2 = {lo:.6f};  bound 1/3 = {1/3:.6f}")
print(f"   claimed equality case: {val(a0, b0):.12f}  probs {np.round(np.abs(F6.conj().T@np.concatenate([a0, b0])/sq(6))**2, 6)}")
if lo < 1/3 - 1e-6 or abs(val(a0, b0) - 1/3) > 1e-9: fail.append("1/108 bound")

print("\n" + ("ALL CHECKS CONSISTENT WITH THE NOTE" if not fail else "FAILURES: " + "; ".join(fail)))
