#!/usr/bin/env python3
"""m2 / swarm smwhnslql -- reproducible checks for results/symmetry-overnight/m2-dossier.md
and m2-delta-census.md.  Only numpy is required.

Sections
  (1) explicit MUB triples of C^6 from M. Cardenes Wuttig, J. Tindall, arXiv:2611.06917,
      Methods Eqs. (30), (31) and SM Eqs. (136)-(139); unbiasedness checked.
  (2) Delta_X by the ray-permutation method (numerical), with the census drivers.
  (3) Delta_X exactly, in Q(zeta_24) (ray-permutation method, cross-multiplied minors).
  (4) Delta_X exactly, by the PRIMARY SOURCE's own definition (sec. 3): 30x30 projection
      entries P_(ij),(kl), relation vectors e_i-e_j-e_k+e_l, support lattice L_A inside
      Lambda_0, Delta_A = [Lambda_0 : L_A] = index in Z^5; Smith normal form reported.
  (5) The detectors of Conjecture 2 of Matolcsi-Matszangosz-Varga-Weiner, arXiv:2503.14752,
      evaluated literally, IN BOTH VERSIONS.  With
        G_H(g) = |sum_k prod_i H[i,k]^{g_i}|^2 ,  Gtilde_H(g) = sum_{pi in S_6} G_H(pi g),
      and g1 = (1,1,1,-1,-1,-1), g2 = 3*g1:
        v1 (18 Mar 2025): Gtilde_Hj(g1)=0 all j; Gtilde_Hj(g2)=0 for two of the three j
        v2 (19 Jul 2025, current): G_Hj(pi g1)=0 for all j,pi AND
                                   G_Hj(pi g2) G_{Hj^*}(pi g2)=0 for all j,pi,
             equivalently Eq. (4.9) of v2.  Section (5) tests BOTH statements.

USAGE   python3 m2-explicit-triples.py          # smoke test, ~10 s
        python3 m2-explicit-triples.py full     # includes the census of the note, ~3 min
        python3 m2-explicit-triples.py quick    # sections (1),(3),(4) only, ~3 s
"""
import cmath, itertools, math, random, sys
import numpy as np

W3 = cmath.exp(2j*cmath.pi/3)
def Fhat(n):
    return np.array([[cmath.exp(2j*cmath.pi*j*k/n) for k in range(n)] for j in range(n)])/math.sqrt(n)
F3, F2 = Fhat(3), Fhat(2)
I6 = np.eye(6)
SQ6 = 1/math.sqrt(6)

# ------------------------------------------------------------------ (1) explicit triples
def family_triple(t1, t2, ell=1, eps=(1, 1, 1), rootorder=(0, 1, 2)):
    """{I6,U2,U3} member of the continuous family (arXiv:2611.06917 Eq. (31), SM (136)-(139))."""
    beta = (t2 - 2*t1 + 2*cmath.pi*(ell-1))/3
    gamma = -(t1 + t2 + 2*cmath.pi*(ell-1))/3
    sigma = cmath.exp(-1j*beta) + cmath.exp(1j*(beta-gamma)) + cmath.exp(1j*gamma)
    roots = [np.roots([1, sigma, -np.conj(sigma), -1])[i] for i in rootorder]
    r1, r3 = roots[0], roots[2]
    A = np.array([[1, cmath.exp(1j*beta), cmath.exp(1j*gamma)],
                  [cmath.exp(1j*gamma), 1, cmath.exp(1j*beta)],
                  [cmath.exp(1j*beta), cmath.exp(1j*gamma), 1]])
    B = np.array([[1, 1/r1, r3], [r3, 1, 1/r1], [1/r1, r3, 1]])
    FA = F3@A@F3.conj().T; FB = F3@B@F3.conj().T
    lam = np.array([FA[k, k] for k in range(3)])/math.sqrt(6)
    mu = np.array([FB[k, k] for k in range(3)])/math.sqrt(6)
    D = np.zeros((3, 3), dtype=complex); R = np.zeros_like(D); S = np.zeros_like(D)
    for k in range(3):
        D[k, k] = 1j*eps[k]*lam[k]*mu[k]/abs(lam[k]*mu[k])
        R[k, k] = lam[k] + D[k, k]*np.conj(mu[k])
        S[k, k] = lam[k] - D[k, k]*np.conj(mu[k])
    U2 = np.block([[F3, D@F3], [F3, -D@F3]])/math.sqrt(2)
    U3 = np.block([[R@F3, -D@S.conj().T@F3], [S@F3, D@R.conj().T@F3]])/math.sqrt(2)
    return U2, U3

def isolated_triple():
    """arXiv:2611.06917 Eq. (30)."""
    return np.kron(F2, F3), np.kron(np.diag([1, 1j])@F2, np.diag([1, W3**2, W3**2])@F3)

def mub_defect(bases):
    worst = 0.0
    for a in range(3):
        worst = max(worst, np.abs(bases[a].conj().T@bases[a]-np.eye(6)).max())
        for b in range(a+1, 3):
            worst = max(worst, np.abs(np.abs(bases[a].conj().T@bases[b])-np.ones((6, 6))*SQ6).max())
    return worst

def entries_flat(M, tol=1e-9):
    return abs(np.abs(M)-SQ6).max() < tol

def sigma_of(t1, t2, ell=1):
    beta = (t2 - 2*t1 + 2*cmath.pi*(ell-1))/3
    gamma = -(t1 + t2 + 2*cmath.pi*(ell-1))/3
    return cmath.exp(-1j*beta) + cmath.exp(1j*(beta-gamma)) + cmath.exp(1j*gamma)

def in_domain(t1, t2, ell=1):
    s = sigma_of(t1, t2, ell)
    return abs(s)**4 + 18*abs(s)**2 + 8*(s**3).real - 27 <= 0.0

# --------------------------------------------------- (2) Delta by ray permutations, numerically
PERMS = list(itertools.permutations(range(6)))
def _frame(bases, anchor):
    W = bases[anchor]; o = [b for k, b in enumerate(bases) if k != anchor]
    return W.conj().T@o[0], W.conj().T@o[1]
def _ratios(X, sig, tol):
    W0 = X[:, sig[0]]/X[:, 0]
    for j in range(1, 6):
        r = (X[:, sig[j]]/X[:, j])/W0; r = r/r[0]
        if not np.all(np.isfinite(r)) or np.abs(r-1).max() > tol: return None
    return W0/W0[0]
def _ok(X, d, sig, tol):
    for j in range(6):
        v = d*X[:, j]/X[:, sig[j]]; v = v/v[0]
        if not np.all(np.isfinite(v)) or np.abs(v-1).max() > tol: return False
    return True
def sym_group(bases, anchor, tol=1e-7):
    X, Y = _frame(bases, anchor); found = {}
    for sig in PERMS:
        d = _ratios(X, sig, tol)
        if d is None or not _ok(X, d, sig, tol): continue
        key = tuple(np.round(d, 7))
        if key in found: continue
        for tau in PERMS:
            if _ok(Y, d, tau, tol): found[key] = (sig, tau, d); break
    return list(found.values())
def delta_triple(bases, tol=1e-7):
    return tuple(len(sym_group(bases, a, tol)) for a in range(3))

def census_random(n_target, seed=20261115):
    random.seed(seed); tally = {}; drawn = 0; used = 0
    while used < n_target:
        t1 = random.uniform(0, 2*math.pi); t2 = random.uniform(0, 2*math.pi); drawn += 1
        if not in_domain(t1, t2): continue
        U2, U3 = family_triple(t1, t2); B = [I6, U2, U3]
        if mub_defect(B) > 1e-9 or not (entries_flat(U2) and entries_flat(U3)):
            tally[("degenerate",)] = tally.get(("degenerate",), 0)+1; used += 1; continue
        d = delta_triple(B); tally[d] = tally.get(d, 0)+1; used += 1
    return tally, drawn, used

def census_grid(N):
    tally = {}; used = 0
    for i in range(N):
        for j in range(N):
            t1 = 2*math.pi*i/N; t2 = 2*math.pi*j/N
            if not in_domain(t1, t2): continue
            U2, U3 = family_triple(t1, t2); B = [I6, U2, U3]
            if mub_defect(B) > 1e-9 or not (entries_flat(U2) and entries_flat(U3)):
                tally[("degenerate",)] = tally.get(("degenerate",), 0)+1; used += 1; continue
            d = delta_triple(B); tally[d] = tally.get(d, 0)+1; used += 1
    return tally, used

# ------------------------------------------------- (3) Delta exactly, Q(zeta_24), permutations
ONE = ((1, 0, 0, 0, 0, 0, 0, 0), 1); ZERO = ((0,)*8, 1)
def _red(c):
    c = list(c)
    while len(c) > 8:
        k = len(c)-1; a = c.pop()
        if a: c[k-4] += a; c[k-8] -= a
    while len(c) < 8: c.append(0)
    return tuple(c)
def cadd(A, B):
    a, da = A; b, db = B
    n = da*db//math.gcd(da, db); fa, fb = n//da, n//db
    return (tuple(fa*x+fb*y for x, y in zip(a, b)), n)
def cneg(A): return (tuple(-x for x in A[0]), A[1])
def csub(A, B): return cadd(A, cneg(B))
def cmul(A, B):
    a, da = A; b, db = B; out = [0]*15
    for i in range(8):
        if a[i]:
            for j in range(8):
                if b[j]: out[i+j] += a[i]*b[j]
    return (_red(out), da*db)
def is_zero(A): return all(x == 0 for x in A[0])
def from_phase(k, den=1):
    k %= 24; res = [1]+[0]*7; x = [0, 1]+[0]*6
    for _ in range(k):
        tmp = [0]*15
        for i in range(8):
            if res[i]:
                for j in range(8):
                    if x[j]: tmp[i+j] += res[i]*x[j]
        res = list(_red(tmp))
    return (tuple(res), den)
def cconj(A):
    c, den = A; out = ZERO
    for i in range(8):
        if c[i]: out = cadd(out, cmul((tuple([c[i]]+[0]*7), 1), from_phase(-i)))
    return (out[0], out[1]*den)
SQRT6 = cadd(cadd(from_phase(1), from_phase(23)), cadd(from_phase(5), from_phase(19)))
INV_SQRT6 = (SQRT6[0], SQRT6[1]*6)
def ee(k): return cmul(from_phase(k), INV_SQRT6)
def mat_mul(A, B):
    C = []
    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            acc = ZERO
            for k in range(len(B)): acc = cadd(acc, cmul(A[i][k], B[k][j]))
            row.append(acc)
        C.append(row)
    return C
def dagger(A): return [[cconj(A[j][i]) for j in range(len(A))] for i in range(len(A[0]))]
def exact_from_numeric(M):
    return [[ee(int(round(np.angle(M[i, j])*24/(2*math.pi))) % 24) for j in range(6)] for i in range(6)]
def to_exact_bases(U2, U3):
    Z = [[ONE if i == j else ZERO for j in range(6)] for i in range(6)]
    return [Z, exact_from_numeric(U2), exact_from_numeric(U3)]
def exact_mub_ok(bases):
    sixth = ((1, 0, 0, 0, 0, 0, 0, 0), 6)
    for X in bases:
        G = mat_mul(dagger(X), X)
        for i in range(6):
            for j in range(6):
                if i == j:
                    if not is_zero(csub(G[i][j], ONE)): return False, "not orthonormal"
                elif not is_zero(G[i][j]): return False, "not orthogonal"
    for a in range(3):
        for b in range(a+1, 3):
            G = mat_mul(dagger(bases[a]), bases[b])
            for i in range(6):
                for j in range(6):
                    if is_zero(G[i][j]): return False, "zero overlap"
                    if not is_zero(csub(cmul(G[i][j], cconj(G[i][j])), sixth)): return False, "|overlap|^2 != 1/6"
    return True, ""
def _rank1(X, sig):
    for i in range(6):
        for ip in range(i+1, 6):
            for j in range(6):
                for jp in range(j+1, 6):
                    lhs = cmul(cmul(X[i][sig[j]], X[ip][sig[jp]]), cmul(X[i][jp], X[ip][j]))
                    rhs = cmul(cmul(X[i][sig[jp]], X[ip][sig[j]]), cmul(X[i][j], X[ip][jp]))
                    if not is_zero(csub(lhs, rhs)): return False
    return True
def _okY(Y, d, tau):
    for i in range(6):
        for ip in range(i+1, 6):
            for j in range(6):
                lhs = cmul(cmul(d[i], Y[i][j]), Y[ip][tau[j]])
                rhs = cmul(cmul(d[ip], Y[ip][j]), Y[i][tau[j]])
                if not is_zero(csub(lhs, rhs)): return False
    return True
def exact_delta(bases):
    out = []
    for anchor in range(3):
        W = bases[anchor]; o = [b for k, b in enumerate(bases) if k != anchor]
        X = mat_mul(dagger(W), o[0]); Y = mat_mul(dagger(W), o[1]); n = 0
        for sig in PERMS:
            if not _rank1(X, sig): continue
            d = [cmul(X[i][sig[0]], cconj(X[i][0])) for i in range(6)]
            inv = cconj(d[0]); d = [cmul(x, inv) for x in d]
            for tau in PERMS:
                if _okY(Y, d, tau): n += 1; break
        out.append(n)
    return tuple(out)

# ------------------------------------- (4) Delta exactly, by the source's support-lattice index
def snf(rows, d=5):
    """Smith normal form diagonal of the integer matrix with the given rows."""
    M = [list(map(int, r)) for r in rows if any(r)]
    if not M: return []
    n = len(M); r = 0; inv = []
    while r < min(n, d):
        pos = None
        for i in range(r, n):
            for j in range(r, d):
                if M[i][j] != 0 and (pos is None or abs(M[i][j]) < abs(M[pos[0]][pos[1]])):
                    pos = (i, j)
        if pos is None: break
        i0, j0 = pos
        M[r], M[i0] = M[i0], M[r]
        for row in M: row[j0], row[r] = row[r], row[j0]
        while True:
            done = True
            for i in range(r+1, n):
                if M[i][r] != 0:
                    q = M[i][r] // M[r][r]
                    for j in range(r, d): M[i][j] -= q*M[r][j]
                    if M[i][r] != 0: done = False
            for j in range(r+1, d):
                if M[r][j] != 0:
                    q = M[r][j] // M[r][r]
                    for i in range(r, n): M[i][j] -= q*M[i][r]
                    if M[r][j] != 0: done = False
            if done: break
            pos = None
            for i in range(r, n):
                for j in range(r, d):
                    if M[i][j] != 0 and (pos is None or abs(M[i][j]) < abs(M[pos[0]][pos[1]])):
                        pos = (i, j)
            if pos is None: break
            i0, j0 = pos
            M[r], M[i0] = M[i0], M[r]
            for row in M: row[j0], row[r] = row[r], row[j0]
        inv.append(abs(M[r][r])); r += 1
    return inv

def _qtable(X):
    return {(i, j): [cmul(X[i][r], cconj(X[j][r])) for r in range(6)]
            for i in range(6) for j in range(6) if i != j}

def support_lattice(bases, anchor):
    """(Smith diagonal, index, number of nonzero projection entries) for the anchor."""
    order = [k for k in range(3) if k != anchor]
    W = bases[anchor]
    B = mat_mul(dagger(W), bases[order[0]]); C = mat_mul(dagger(W), bases[order[1]])
    QB, QC = _qtable(B), _qtable(C)
    rel = set(); nnz = 0
    for (i, j) in QB:
        for (k, l) in QB:
            acc = ZERO
            for r in range(6): acc = cadd(acc, cmul(QB[(i, j)][r], cconj(QB[(k, l)][r])))
            for r in range(6): acc = cadd(acc, cmul(QC[(i, j)][r], cconj(QC[(k, l)][r])))
            if not is_zero(acc):
                nnz += 1
                row = [0]*6; row[i] += 1; row[j] -= 1; row[k] -= 1; row[l] += 1
                if any(row): rel.add(tuple(row[:5]))
    inv = snf(sorted(rel))
    idx = 1
    for x in inv: idx *= x
    return inv, idx, nnz, len(rel)

# --------------------------------------------------- (5) MMVW detectors, v1 and v2
PERMS6 = list(itertools.permutations(range(6)))
G1 = (1, 1, 1, -1, -1, -1); G2 = (3, 3, 3, -3, -3, -3)
def Gdet(H, g):
    tot = 0j
    for k in range(6):
        p = 1+0j
        for i in range(6):
            e = g[i]
            p = p*H[i, k] if e == 1 else (p/H[i, k] if e == -1 else p*H[i, k]**e)
        tot += p
    return abs(tot)**2
def Gtilde(H, g):
    return sum(Gdet(H, tuple(g[p[i]] for i in range(6))) for p in PERMS6)
def perms_values(H, g):
    return [Gdet(H, tuple(g[p[i]] for i in range(6))) for p in PERMS6]
def transitions(U2, U3):
    return [math.sqrt(6)*U2, math.sqrt(6)*(U2.conj().T@U3), math.sqrt(6)*U3.conj().T]
def report_v1(U2, U3):
    return [Gtilde(X, G1) for X in transitions(U2, U3)], [Gtilde(X, G2) for X in transitions(U2, U3)]
def report_v2(U2, U3):
    """(max over j,pi of G_Hj(pi g1); max over j,pi of G_Hj(pi g2)G_{Hj^*}(pi g2); per-j detail)."""
    rows = []; w1 = 0.0; wp = 0.0
    for j, X in enumerate(transitions(U2, U3)):
        a1 = perms_values(X, G1); a2 = perms_values(X, G2); b2 = perms_values(X.conj().T, G2)
        prod = [x*y for x, y in zip(a2, b2)]
        w1 = max(w1, max(a1)); wp = max(wp, max(prod))
        rows.append((j+1, max(a1), sum(1 for x in a1 if x > 1e-8),
                     max(a2), sum(1 for x in a2 if x > 1e-8),
                     max(b2), sum(1 for x in b2 if x > 1e-8), max(prod)))
    return w1, wp, rows
def individual_sums(H, scale):
    """|sum_k prod_i H[i,k]^(scale*sign_i)| for the 20 sign splits (v1-style, per split)."""
    out = []
    for sgn in itertools.combinations(range(6), 3):
        g = tuple(scale*(1 if i in sgn else -1) for i in range(6))
        tot = 0j
        for k in range(6):
            p = 1+0j
            for i in range(6):
                p = p*H[i, k] if g[i] == 1 else (p/H[i, k] if g[i] == -1 else p*H[i, k]**g[i])
            tot += p
        out.append(abs(tot))
    return out

# ---------------------------------------------------------------------------- driver
def show_triple(name, U2, U3, exact=True):
    B = [I6, U2, U3]
    print("  %-32s MUB defect %.2e   flat=%s" % (name, mub_defect(B), entries_flat(U2) and entries_flat(U3)))
    print("     Delta (ray permutations, numeric):", delta_triple(B))
    if exact:
        Xb = to_exact_bases(U2, U3)
        ok, why = exact_mub_ok(Xb)
        print("     exact MUB in Q(zeta_24):", ok, why)
        if ok:
            print("     Delta (ray permutations, EXACT):", exact_delta(Xb))
            for a in range(3):
                inv, idx, nnz, nr = support_lattice(Xb, a)
                print("     anchor %d: support-lattice Smith %s  index %d   (%d nonzero P entries, %d relations)"
                      % (a, inv, idx, nnz, nr))

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    print("== (1)/(3)/(4) explicit triples: Delta three ways")
    show_triple("isolated triple Eq. (30)", *isolated_triple())
    show_triple("family centre (2pi/3,-2pi/3)", *family_triple(2*math.pi/3, -2*math.pi/3))
    show_triple("family centre (4pi/3, 2pi/3)", *family_triple(4*math.pi/3, 2*math.pi/3))
    print("  generic family points (numeric ray-permutation Delta only):")
    for (t1, t2) in [(1.0, 4.2), (2.0, 4.0), (3.0, 0.5)]:
        U2, U3 = family_triple(t1, t2); B = [I6, U2, U3]
        print("     (%.2f,%.2f) defect %.1e  Delta %s" % (t1, t2, mub_defect(B), delta_triple(B)))
    if mode == "quick":
        return

    print("== (2) census over the continuous family")
    if mode == "full":
        t, drawn, used = census_random(4600)
        print("   random: %d draws, %d in-domain, tally %s" % (drawn, used, t))
        t, used = census_grid(120)
        print("   grid 120x120: %d in-domain, tally %s" % (used, t))
    else:
        t, drawn, used = census_random(300)
        print("   random (smoke, 300 in-domain): %d draws, tally %s" % (drawn, t))
        t, used = census_grid(36)
        print("   grid 36x36 (smoke): %d in-domain, tally %s" % (used, t))

    print("== (5) MMVW detectors, v1 (18 Mar 2025) and v2 (19 Jul 2025, current arXiv)")
    for name, (U2, U3) in [("isolated triple", isolated_triple()),
                           ("family centre", family_triple(2*math.pi/3, -2*math.pi/3)),
                           ("family (1.00,4.20)", family_triple(1.0, 4.2)),
                           ("family (2.00,4.00)", family_triple(2.0, 4.0)),
                           ("family (3.00,0.50)", family_triple(3.0, 0.5))]:
        r1, r2 = report_v1(U2, U3)
        w1, wp, rows = report_v2(U2, U3)
        print("   %-20s v1: Gtilde(g1)=%s ; Gtilde(g2)=%s  (#vanishing %d of 3)"
              % (name, ["%.0e" % x for x in r1], ["%.0e" % x for x in r2],
                 sum(1 for x in r2 if x < 1e-8)))
        print("   %-20s v2: max_{j,pi} G(g1)=%.0e ; max_{j,pi} G(g2)G(g2)^*=%.0e"
              % ("", w1, wp))
        for (j, m1, n1, m2, n2, mb2, nb2, mp) in rows:
            print("        j=%d: G(g1) nonzero for %3d/720 pi | G(g2) %3d/720 | G^*(g2) %3d/720 | max product %.0e"
                  % (j, n1, n2, nb2, mp))
    U2, U3 = family_triple(1.0, 4.2)
    print("   per-split detail at (1.00,4.20) (v1 quantities; 20 sign splits, 720 = 36 x 20):")
    for j, H in enumerate(transitions(U2, U3)):
        a1 = individual_sums(H, 1); a2 = individual_sums(H, 3)
        a1s = individual_sums(H.conj().T, 1); a2s = individual_sums(H.conj().T, 3)
        print("      H%d: |sum|>1e-8 for gamma1 %d/20, gamma1^* %d/20, gamma2 %d/20, gamma2^* %d/20"
              % (j+1, sum(1 for x in a1 if x > 1e-8), sum(1 for x in a1s if x > 1e-8),
                 sum(1 for x in a2 if x > 1e-8), sum(1 for x in a2s if x > 1e-8)))

    if mode == "full":
        print("   v2 sweep over 25 random interior family points:")
        random.seed(4242); n = 0; w1 = 0.0; wp = 0.0
        while n < 25:
            t1 = random.uniform(0, 2*math.pi); t2 = random.uniform(0, 2*math.pi)
            if not in_domain(t1, t2): continue
            U2, U3 = family_triple(t1, t2)
            if mub_defect([I6, U2, U3]) > 1e-9: continue
            a, b, _ = report_v2(U2, U3); w1 = max(w1, a); wp = max(wp, b); n += 1
        print("      max_{j,pi} G(g1) = %.1e ; max_{j,pi} G(g2)G(g2)^* = %.1e" % (w1, wp))

    print("== (6) the Delta = 2 locus is a point: scan a neighbourhood of the centre")
    c1, c2 = 2*math.pi/3, -2*math.pi/3
    for v in [(1, 0), (0, 1), (1, 1)]:
        row = []
        for d in [0.0, 1e-6, 1e-3, 1e-2, 1e-1, 3e-1]:
            t1, t2 = c1 + d*v[0], c2 + d*v[1]
            if not in_domain(t1, t2): row.append("%g: outside" % d); continue
            row.append("%g:%s" % (d, delta_triple([I6]+list(family_triple(t1, t2)))))
        print("   direction %s -> %s" % (v, "; ".join(row)))

if __name__ == "__main__":
    main()
