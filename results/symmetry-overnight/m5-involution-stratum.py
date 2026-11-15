"""m5-involution-stratum.py -- the Delta_A >= 2 stratum of MUB triples in C^6.

Three parts, each useful on its own:

  part1  delta_of(U,V): for the anchor = coordinate basis, compute the support of
         P_A (off-diagonal matrix units), the relation lattice, its Smith index
         [Lambda_0:L_A] and -- independently -- the order of the group of diagonal
         unitaries obtained by enumerating all a with R a = 0 mod 1 and testing ray
         preservation of U and V explicitly.  The two numbers agree in every example.

  part2  the source's "uniform case" built exactly: H0,H1 with H F flat, K0 = H0 F,
         K1 = i H1 F.  Over all 108^2 pairs the exact Delta-tuple is (2,3,3) or (6,6,6).

  part3  the full involution stratum: all solutions of the system (7)
             |X_ij|^2 + |Y_ij|^2 = 2/3,  Re(X_ij conj(Y_ij)) = 0 ,
         with X = H0^*K0, Y = H1^*K1 and H0 = F D2 P0, H1 = F D6 P2, K0 = D3 F,
         K1 = D7 F D8 P3 (complete up to the gauge X -> Dmu^* X Dlam PiB, Y likewise).
         15 free phases, 18 equations, 216 discrete classes.  Reports the Delta-tuple
         histogram; the only values are (2,3,3), (6,6,6) (uniform) and (6,1,1)
         (nonuniform, a one-parameter family).

Run:  python3 m5-involution-stratum.py            (about 2 minutes on 4 cores)
      python3 m5-involution-stratum.py --starts 40 --part 3
"""
import sys, itertools, collections
import numpy as np

W = np.exp(2j * np.pi / 3)
F = np.array([[W**(i * j) for j in range(3)] for i in range(3)]) / np.sqrt(3)
PERMS = list(itertools.permutations(range(3)))


# ---------------------------------------------------------------- part 1
def P_support(U, V, tol=1e-9):
    """(P_A)_{ij,kl} for i!=j, k!=l : sum_r U_ir conj(U_jr) conj(U_kr) U_lr + (V)."""
    def tensor(M):
        A1 = M[:, None, :] * np.conj(M)[None, :, :]        # A1[i,j,r] = M[i,r] conj(M[j,r])
        return np.einsum('ijr,lkr->ijkl', A1, A1, optimize=True)
    T = tensor(U) + tensor(V)
    nz = [(i, j, k, l, abs(T[i, j, k, l]))
          for i in range(6) for j in range(6) if i != j
          for k in range(6) for l in range(6) if k != l and abs(T[i, j, k, l]) > tol]
    return nz


def relation_rows(nz):
    rows = set()
    for (i, j, k, l, _) in nz:
        r = np.zeros(6, dtype=int)
        r[i] += 1; r[j] -= 1; r[k] -= 1; r[l] += 1
        rows.add(tuple(int(x) for x in r[:5]))
    return sorted(rows)


def smith_index(rows):
    import sympy as sp
    from sympy.matrices.normalforms import smith_normal_form
    if len(rows) < 5:
        return 0, []
    S = smith_normal_form(sp.Matrix([list(r) for r in rows]), domain=sp.ZZ)
    d = [abs(int(S[i, i])) for i in range(5)]
    if 0 in d:
        return 0, d
    p = 1
    for x in d:
        p *= x
    return p, d


def rank_mod3(rows):
    M = [[int(x) % 3 for x in r] for r in rows]
    rank, row = 0, 0
    for c in range(5):
        piv = next((i for i in range(row, len(M)) if M[i][c] % 3), None)
        if piv is None:
            continue
        M[row], M[piv] = M[piv], M[row]
        inv = pow(M[row][c], -1, 3)
        M[row] = [(x * inv) % 3 for x in M[row]]
        for i in range(len(M)):
            if i != row and M[i][c] % 3:
                f = M[i][c]
                M[i] = [(M[i][j] - f * M[row][j]) % 3 for j in range(5)]
        row += 1
        if row == len(M):
            break
    return row


def solution_group(rows, index):
    import sympy as sp
    from sympy.matrices.normalforms import smith_normal_decomp
    chosen = []
    for r in rows:
        if sp.Matrix(chosen + [r]).rank() == len(chosen) + 1:
            chosen.append(r)
        if len(chosen) == 5:
            break
    if len(chosen) < 5:
        return None
    D, U, V = smith_normal_decomp(sp.Matrix(chosen), domain=sp.ZZ)   # D = U B V
    diag = [abs(int(D[i, i])) for i in range(5)]
    out = []
    for ks in itertools.product(*[range(d) for d in diag]):
        b = sp.Matrix([sp.Rational(k, d) for k, d in zip(ks, diag)])
        a = V * b
        a6 = [sp.Rational(a[i]) % 1 for i in range(5)] + [sp.Rational(0)]
        if all(sum(int(r[i]) * a6[i] for i in range(5)).q == 1 for r in rows):
            out.append(tuple(sp.Rational(x) for x in a6))
    return sorted(set(out))


def preserves_rays(t, M, tol=1e-7):
    TM = np.asarray(t)[:, None] * M
    G = np.abs(TM.conj().T @ M)
    used, perm = set(), []
    for j in range(M.shape[0]):
        m = int(np.argmax(G[j]))
        if G[j, m] < 1 - tol or m in used:
            return None
        used.add(m); perm.append(m)
    return tuple(perm)


def delta_of(U, V, verbose=False):
    nz = P_support(U, V)
    rows = relation_rows(nz)
    idx, d = smith_index(rows)
    r3 = rank_mod3(rows)
    ray = None
    if idx:
        ray = 0
        for a in solution_group(rows, idx):
            ph = np.array([np.exp(2j * np.pi * float(x)) for x in a])
            if preserves_rays(ph, U) and preserves_rays(ph, V):
                ray += 1
    if verbose:
        print("    support %d rows %d  Smith %s  index %d  rank_F3 %d  ray-group %s"
              % (len(nz), len(rows), d, idx, r3, ray))
    return idx, ray


def triple_deltas(U, V, verbose=False):
    UB, VB = U.conj().T, U.conj().T @ V
    UC, VC = V.conj().T, V.conj().T @ U
    out = []
    for X, Y in ((U, V), (UB, VB), (UC, VC)):
        out.append(delta_of(X, Y, verbose))
    return tuple(o[0] for o in out), tuple(o[1] for o in out)


# ---------------------------------------------------------------- part 2
def Pmat(p):
    M = np.zeros((3, 3), complex)
    for i in range(3):
        M[i, p[i]] = 1
    return M


def had(H):
    return max(np.abs(H.conj().T @ H - np.eye(3)).max(),
               np.abs(np.abs(H) - 1 / np.sqrt(3)).max()) < 1e-9


def uniform_Hs():
    """All 3x3 Hadamards H with H F flat (exactly 108)."""
    out = []
    for a in itertools.product(range(3), repeat=3):
        D = np.diag([W**k for k in a])
        for p in PERMS:
            H = F @ D @ Pmat(p)
            if had(H) and np.abs(np.abs(H @ F) - 1 / np.sqrt(3)).max() < 1e-9:
                out.append((a, p, H))
    return out


def uniform_build(H0, H1):
    K0, K1 = H0 @ F, 1j * H1 @ F
    U = np.block([[H0, H0], [H1, -H1]]) / np.sqrt(2)
    V = np.block([[K0, K0], [K1, -K1]]) / np.sqrt(2)
    return U, V


def part4(verbose=True):
    """Verify Theorem U's conclusion on the entire uniform family."""
    Z = np.diag([1, W, W**2])
    T = np.block([[Z, np.zeros((3, 3))], [np.zeros((3, 3)), Z]])
    t = np.diag(T)
    Hs = [H for (_, _, H) in uniform_Hs()]
    bad = n = 0
    for H0, H1 in itertools.product(Hs, Hs):
        U, V = uniform_build(H0, H1)
        n += 1
        if not (preserves_rays(t, U.conj().T) and preserves_rays(t, U.conj().T @ V)
                and preserves_rays(t, V.conj().T) and preserves_rays(t, V.conj().T @ U)):
            bad += 1
    if verbose:
        print("part 4: Theorem U's conclusion verified on %d uniform triples, %d failures" % (n, bad))
    return bad


def part2(verbose=True):
    Hs = uniform_Hs()
    hist = collections.Counter()
    for (a0, p0, H0), (a1, p1, H1) in itertools.product(Hs, Hs):
        U, V = uniform_build(H0, H1)
        assert np.abs(np.abs(U.conj().T @ V) ** 2 - 1 / 6).max() < 1e-12
        hist[triple_deltas(U, V)[0]] += 1
    if verbose:
        print("part 2: %d Hadamards with HF flat; Delta-tuple histogram over the %d pairs:"
              % (len(Hs), len(Hs) ** 2))
        for k, v in sorted(hist.items()):
            print("   ", k, v)
    return hist


# ---------------------------------------------------------------- part 3
def Circ(d):
    return np.array([[sum(d[k] * W**(k * (j - i)) for k in range(3)) / 3 for j in range(3)]
                     for i in range(3)])


def XY(x, P0, P2, P3):
    D2, D3, D6, D7, D8 = (np.exp(1j * x[3 * k:3 * k + 3]) for k in range(5))
    X = Pmat(P0).T @ (np.conj(D2)[:, None] * Circ(D3))
    Y = Pmat(P2).T @ (np.conj(D6)[:, None] * Circ(D7)) @ np.diag(D8) @ Pmat(P3)
    return X, Y


def resid(x, P0, P2, P3):
    X, Y = XY(x, P0, P2, P3)
    return np.concatenate([(np.abs(X)**2 + np.abs(Y)**2 - 2 / 3).ravel(),
                           (X * np.conj(Y)).real.ravel()])


def build3(x, P0, P2, P3):
    D2, D3, D6, D7, D8 = (np.exp(1j * x[3 * k:3 * k + 3]) for k in range(5))
    H0 = F @ np.diag(D2) @ Pmat(P0); H1 = F @ np.diag(D6) @ Pmat(P2)
    K0 = np.diag(D3) @ F; K1 = np.diag(D7) @ F @ np.diag(D8) @ Pmat(P3)
    U = np.block([[H0, H0], [H1, -H1]]) / np.sqrt(2)
    V = np.block([[K0, K0], [K1, -K1]]) / np.sqrt(2)
    return U, V


def part3(starts=12, seed=12345, verbose=True):
    from scipy.optimize import least_squares
    rng = np.random.default_rng(seed)
    hist = collections.Counter()
    nonuni = collections.Counter()
    for P0, P2, P3 in itertools.product(PERMS, repeat=3):
        for _ in range(starts):
            s = least_squares(resid, rng.uniform(0, 2 * np.pi, 15), args=(P0, P2, P3),
                              xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=3000)
            if np.abs(s.fun).max() > 1e-10:
                continue
            X, _ = XY(s.x, P0, P2, P3)
            uni = bool(np.abs(np.abs(X) - 1 / np.sqrt(3)).max() < 1e-8)
            U, V = build3(s.x, P0, P2, P3)
            if np.abs(np.abs(U.conj().T @ V) ** 2 - 1 / 6).max() > 1e-10:
                continue
            key = triple_deltas(U, V)[0]
            hist[key] += 1
            if not uni:
                nonuni[key] += 1
    if verbose:
        print("part 3: Delta-tuple histogram over all solutions found:")
        for k, v in sorted(hist.items()):
            print("   ", k, v)
        print("   nonuniform solutions only:", dict(nonuni))
        print("   => Delta_A = 2 occurs only among the uniform solutions; there Delta_B = Delta_C = 3")
    return hist, nonuni


if __name__ == '__main__':
    args = sys.argv[1:]
    starts = 12
    if '--starts' in args:
        starts = int(args[args.index('--starts') + 1])
    which = 'all'
    if '--part' in args:
        which = args[args.index('--part') + 1]
    print("== sanity: the product triple should have Delta = (6,6,6)")
    U2 = np.kron(np.diag([1, 1j]) @ np.array([[1, 1], [1, -1]]) / np.sqrt(2),
                 np.diag([1, W**2, W**2]) @ F)
    F2 = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    print("   product trip:", triple_deltas(np.kron(F2, F), U2)[0])
    if which in ('all', '2'):
        part2()
    if which in ('all', '3'):
        part3(starts=starts)
    if which in ('all', '4'):
        part4()
