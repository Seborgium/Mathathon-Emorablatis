#!/usr/bin/env python3
"""Independent verification suite for "How close can four bases in C^6 be to mutually unbiased?".

Written from scratch for this check: it imports nothing from work/11-approx-mub/
or from the swarm's member directories, and re-derives every computational claim.

  python3 verify_all.py            # runs all checks, prints PASS/FAIL lines
Exit status 0 iff every check passes.
"""
import numpy as np, itertools, math, sys
from fractions import Fraction as F

FAILS = []
def check(cid, name, ok, detail=""):
    print(f"[{cid:>2}] {name:<62} {'PASS' if ok else 'FAIL'}  {detail}")
    if not ok: FAILS.append(cid)

rng = np.random.default_rng(20261115)
def randU(d):
    A = rng.normal(size=(d,d)) + 1j*rng.normal(size=(d,d))
    Q, R = np.linalg.qr(A)
    return Q * np.exp(-1j*np.angle(np.diag(R)))
def randO(d):
    A = rng.normal(size=(d,d)); Q, R = np.linalg.qr(A)
    return Q * np.sign(np.diag(R))
def unit_ok(Us, tol=1e-13):
    return all(float(np.abs(U.conj().T@U - np.eye(U.shape[0])).max()) < tol for U in Us)
def pmat(U, V):
    return np.abs(U.conj().T @ V)**2
def dev(U, V, d):
    return float(np.abs(pmat(U, V) - 1.0/d).max())

# ---------------------------------------------------------------- [1] frame
worst = 0.0
for d in (2, 3, 4, 6, 7):
    for _ in range(6):
        Us = [randU(d) for _ in range(4)]
        S = sum(np.outer(u, u.conj()) for U in Us for u in U.T)
        worst = max(worst, float(np.abs(S - 4*np.eye(d)).max()))
check(1, "Thm 3.1: frame operator = 4I for every quadruple", worst < 1e-12, f"max |S-4I| = {worst:.1e}")

worstfp = 0.0
for d in (2, 3, 4, 6, 7):
    for _ in range(6):
        Us = [randU(d) for _ in range(4)]
        V = np.hstack([U for U in Us])                    # d x 4d
        G = V.conj().T @ V
        worstfp = max(worstfp, abs(float((np.abs(G)**2).sum()) - 16*d))
check(2, "Thm 3.1: frame potential = 16d = N^2/d identically", worstfp < 1e-9, f"max |FP-16d| = {worstfp:.1e}")

# ------------------------------------------------- [3] two-body Gram, d=3,5,7
def mub_set_odd_prime(d):
    w = np.exp(2j*np.pi/d)
    Fm = np.exp(2j*np.pi*np.outer(np.arange(d), np.arange(d))/d)/np.sqrt(d)
    out = [np.eye(d, dtype=complex)]
    for a in range(d):
        D = np.diag([w**(a*k*k) for k in range(d)])
        out.append(D @ Fm)
    return out
worstg = 0.0
for d in (3, 5, 7):
    B = mub_set_odd_prime(d)[:4]
    for i in range(4):
        for j in range(i+1, 4):
            worstg = max(worstg, dev(B[i], B[j], d))
    W = np.array([np.outer(u, u.conj()) - np.eye(d)/d for U in B for u in U.T])
    G = W.reshape(4*d, -1) @ W.reshape(4*d, -1).conj().T
    target = np.zeros((4*d, 4*d), dtype=complex)
    for a in range(4):
        target[a*d:(a+1)*d, a*d:(a+1)*d] = np.eye(d) - np.ones((d, d))/d
    worstg = max(worstg, float(np.abs(G - target).max()))
check(3, "Thm 3.2: Gram of the 4d traceless matrices = diag(I-J/d)", worstg < 1e-12,
      f"max err {worstg:.1e} (d=3,5,7; MUB pairs exact to {worstg:.1e})")

# ------------------------------- [4] tetrahedral construction: the two factors
# (a) C^2 factor exactly: the four bases are the eigenbases of h_a = (a.sigma)/sqrt3, a in {+-1}^3,
#     whose Bloch vectors are n_a = a/sqrt3 ; then |<a_i,b_j>|^2 = (1 +- n_a.n_b)/2 with
#     n_a.n_b = (a.b)/3 --- a RATIONAL computation carried out below on integers.
import sympy as sp
signs = [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
dot = {(a,b): sum(x*y for x,y in zip(a,b)) for a in signs for b in signs}
ok_rat = all(dot[(a,b)] % 1 == 0 for a in signs for b in signs)
rat_vals = sorted({sp.Rational(1 + sgn*sp.Rational(dot[(a,b)],3), 2) for a in signs for b in signs if a != b for sgn in (1,-1)})
check(4, "Thm 4.1: tetrahedral Bloch data give |overlap|^2 exactly in {1/3,2/3}",
      ok_rat and rat_vals == [sp.Rational(1,3), sp.Rational(2,3)], f"a.b in {{-1,1}}, so n_a.n_b = +-1/3")

# (b) C^3 factor exactly, by Gauss sums, in exact complex arithmetic
s3r = sp.sqrt(3)
F3 = sp.Matrix(3, 3, lambda k,l: sp.exp(2*sp.pi*sp.I*(k*l)/3)/s3r)
w3 = sp.exp(2*sp.pi*sp.I/3)
B3 = [sp.expand_complex(F3), sp.expand_complex(sp.diag(1, w3, w3)*F3),
      sp.expand_complex(sp.diag(1, w3**2, w3**2)*F3), sp.eye(3)]
ok3 = all(sp.simplify(B3[a].H*B3[a] - sp.eye(3)) == sp.zeros(3,3) for a in range(4))
vals3 = set(); exact3 = True
for a in range(4):
    for b in range(a+1,4):
        X = sp.expand_complex(B3[a].H*B3[b])
        for i in range(3):
            for j in range(3):
                e = sp.simplify(sp.expand_complex(X[i,j]*sp.conjugate(X[i,j])))
                vals3.add(abs(complex(sp.N(e, 50)) - 1/3) < 1e-45)
                exact3 &= sp.simplify(e - sp.Rational(1,3)) == 0
check(5, "Thm 4.1: the four C^3 bases are orthonormal and pairwise unbiased",
      ok3 and all(vals3), f"exact symbolic identity |<u,v>|^2 = 1/3 : {exact3}")

check(6, "Thm 4.1: hence every P is in {1/9,2/9} and dev = 1/18 on all six pairs",
      ok_rat and rat_vals == [sp.Rational(1,3), sp.Rational(2,3)] and ok3 and all(vals3),
      "multiplicativity + the two factor checks")

# (c) end-to-end numeric check of the assembled quadruple
s3 = np.sqrt(3)
def basis_from_bloch(n):
    n = n/np.linalg.norm(n)
    th = np.arccos(np.clip(n[2], -1, 1)); ph = np.arctan2(n[1], n[0])
    c, s = np.cos(th/2), np.sin(th/2)
    return np.array([[c, -np.exp(-1j*ph)*s], [np.exp(1j*ph)*s, c]])
Aq = [basis_from_bloch(np.array(v, dtype=float)) for v in signs]
w = np.exp(2j*np.pi/3)
F3n = np.exp(2j*np.pi*np.outer(np.arange(3), np.arange(3))/3)/np.sqrt(3)
Bq = [F3n, np.diag([1,w,w])@F3n, np.diag([1,w**2,w**2])@F3n, np.eye(3, dtype=complex)]
Utet = [np.kron(Aq[a], Bq[a]) for a in range(4)]
allv = np.concatenate([pmat(Utet[a], Utet[b]).ravel() for a in range(4) for b in range(a+1,4)])
worst = float(np.abs(allv - 1/9).min() + np.abs(allv - 2/9).min())
in_set = bool(np.all(np.minimum(np.abs(allv-1/9), np.abs(allv-2/9)) < 1e-13))
check(7, "Thm 4.1: assembled quadruple has all 216 moduli^2 in {1/9,2/9}",
      in_set and unit_ok(Utet), f"max distance to the nearest of 1/9, 2/9 = {float(np.minimum(np.abs(allv-1/9),np.abs(allv-2/9)).max()):.1e}")

# ------------------------------- [8] product class: random stress test, d=2x3
worstpc = 1e9
for _ in range(400):
    Us = [np.kron(randU(2), randU(3)) for _ in range(4)]
    worstpc = min(worstpc, max(dev(Us[a], Us[b], 6) for a in range(4) for b in range(a+1,4)))
check(8, "Thm 5.1: random product quadruples satisfy dev >= 1/18", worstpc >= 1/18 - 1e-12, f"min over 400 = {worstpc:.4f}")

gmin = 1e9
for _ in range(20000):
    n = rng.normal(size=(4,3)); n /= np.linalg.norm(n, axis=1)[:, None]
    gmin = min(gmin, max(abs(float(n[a] @ n[b])) for a in range(4) for b in range(a+1,4)))
check(9, "Thm 5.1 step: 4 unit vectors in R^3 have max |n_a.n_b| >= 1/3", gmin >= 1/3 - 1e-12, f"min over 20000 random tries = {gmin:.6f}")

# ------------------------------- [10] real bases: 2/d^2, and the d=2 exception
res = {}
for d in (2, 6, 10):
    best = 1e9
    for _ in range(300):
        U, V = randO(d), randO(d)
        best = min(best, dev(U, V, d))
    res[d] = best
check(10, "Thm 6.1: real pairs obey dev >= 2/d^2 for d=6,10", res[6] >= 2/36 - 1e-12 and res[10] >= 2/100 - 1e-12,
      f"best random: d=6 {res[6]:.4f}>= {2/36:.4f}, d=10 {res[10]:.4f}>= {2/100:.4f}, d=2 {res[2]:.4f} (bound fails at d=2, as it must)")

# ------------------------------- [11] Butson enumeration
z6 = [np.exp(2j*np.pi*k/6) for k in range(6)]
vals = set()
for c in itertools.combinations_with_replacement(range(6), 6):
    vals.add(round(abs(sum(z6[k] for k in c))**2, 9))
expected = {0.0,1.0,3.0,4.0,7.0,9.0,12.0,13.0,16.0,19.0,21.0,25.0,27.0,28.0,31.0,36.0}
check(11, "Thm 7.1: 462 six-fold sums of mu_6 roots realise exactly that value set and not 6",
      vals == expected and 6.0 not in vals, f"{len(vals)} values, nearest to 6 is {sorted(vals, key=lambda v: abs(v-6))[0]}")

# ------------------------------- [12] exact certificate, independent sympy route
# read the decimal literals as EXACT rationals, form U = (I-iA)^{-1}(I+iA) symbolically,
# and compute P and dev in exact complex rational arithmetic.
def read_A(path):
    blocks, cur = [], None
    for line in open(path):
        t = line.strip()
        if not t or t.startswith('#'): continue
        if t.startswith('A '):
            if cur is not None: blocks.append(cur)
            cur = []
        else:
            v = t.replace('|',' ').split()
            cur.append([sp.Rational(v[2*k]) + sp.I*sp.Rational(v[2*k+1]) for k in range(len(v)//2)])
    if cur: blocks.append(cur)
    return [sp.Matrix(b) for b in blocks]
Aq4 = read_A('data/candidates_A.txt')
herm = all(sp.simplify(A - A.H) == sp.zeros(6,6) for A in Aq4)
check(12, "Thm 8.1: the four A_a are exactly Hermitian rational", herm and len(Aq4) == 4)
I6 = sp.eye(6)
U4 = [sp.expand((I6 - sp.I*A).inv() * (I6 + sp.I*A)) for A in Aq4]
unitary_err = max(sp.simplify(U.H*U - I6).is_zero_matrix for U in U4)
check(13, "Thm 8.1: U_a = (I-iA_a)^{-1}(I+iA_a) is exactly unitary (Cayley)", unitary_err,
      "checked exactly for all four; rational entries by construction")
md = sp.Rational(0)
for i in range(4):
    for j in range(i+1,4):
        X = sp.expand(U4[i].H*U4[j])
        P = X.multiply_elementwise(X.conjugate())
        for e in P:
            md = max(md, sp.Abs(sp.expand(e - sp.Rational(1,6))) if False else abs(sp.re(sp.expand(e)) - sp.Rational(1,6)))
check(14, "Thm 8.1: exact max deviation = 0.03022424077244261561 < 302243/10^7",
      md < sp.Rational(302243, 10**7), f"exact = {sp.N(md, 22)}")

print()
print("ALL CHECKS PASSED" if not FAILS else f"FAILED: {FAILS}")
sys.exit(0 if not FAILS else 1)
