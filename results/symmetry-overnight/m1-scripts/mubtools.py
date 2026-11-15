"""Exact machinery for the m1 audit (Z[zeta_24] arithmetic from cyc.py).

A basis of C^d is stored as its 6 x d (or d x d) coefficient matrix in a fixed
coordinate system, entries in Z[zeta_24] as dicts (zero entries allowed).
"""
from fractions import Fraction
import cyc
from cyc import add, mul, conj, zpow, is_zero, canon, ZERO

N = 6
EDGES = [(i, j) for i in range(N) for j in range(N) if i != j]

# ---------- bases of C^2 and C^3 (exponent matrices of unnormalised Hadamards) ----------
B2 = [[0, 0], [0, 12]]                    # [[1,1],[1,-1]]
C2 = [[0, 0], [6, 18]]                    # diag(1,i)[[1,1],[1,-1]] = [[1,1],[i,-i]]
F3 = [[0, 0, 0], [0, 8, 16], [0, 16, 8]]  # 3x3 Fourier
C3 = [[8 * r * r + F3[r][s] for s in range(3)] for r in range(3)]   # chirp w^(r^2)
D3 = [[16 * r * r + F3[r][s] for s in range(3)] for r in range(3)]  # chirp w^(2r^2)

def ident(n):
    return [[{0: 1} if i == j else {} for j in range(n)] for i in range(n)]

def rep(exp):
    d = len(exp)
    return [[zpow(exp[i][j]) for j in range(d)] for i in range(d)]

def kron(X, Y):
    d = len(Y)
    nx = len(X)
    return [[mul(X[i // d][j // d], Y[i % d][j % d]) for j in range(nx * d)] for i in range(nx * d)]

def kron_exp(X, Y):
    d = len(Y); nx = len(X)
    return [[X[i // d][j // d] + Y[i % d][j % d] for j in range(nx * d)] for i in range(nx * d)]

def mm(A, B):
    n, m, p = len(A), len(B), len(B[0])
    C = [[ZERO] * p for _ in range(n)]
    for i in range(n):
        for j in range(p):
            s = ZERO
            for k in range(m):
                if A[i][k] and B[k][j]:
                    s = add(s, mul(A[i][k], B[k][j]))
            C[i][j] = s
    return C

def dagger(A):
    n, m = len(A), len(A[0])
    return [[conj(A[j][i]) for j in range(n)] for i in range(m)]

def real_int(a):
    c = canon(a)
    if c[1:] == (0,) * 7 and c[0] >= 0:
        return c[0]
    return None

def colnorm(M):
    """common value of |column|^2 as an integer, or None"""
    G = mm(dagger(M), M)
    vals = {real_int(G[i][i]) for i in range(len(M[0]))}
    if len(vals) != 1:
        return None
    return next(iter(vals))

def is_basis_rep(M, d):
    """M^*M = c I with c > 0 (any positive normalisation)."""
    G = mm(dagger(M), M)
    c = colnorm(M)
    if not c:
        return False
    return all(cyc.eq_int(G[i][j], c if i == j else 0) for i in range(d) for j in range(d))

def is_unbiased_rep(MP, MQ, d):
    """|p_i|^2 |q_j|^2 / d = |<p_i,q_j>|^2 for all i,j."""
    cp, cq = colnorm(MP), colnorm(MQ)
    if not cp or not cq or (cp * cq) % d:
        return False
    target = (cp * cq // d,) + (0,) * 7
    for i in range(d):
        for j in range(d):
            s = ZERO
            for k in range(d):
                s = add(s, mul(conj(MP[k][i]), MQ[k][j]))
            if cyc.norm2(s) != target:
                return False
    return True

def pair_phase(HP, HQ):
    """Exponent matrix of the phases of H_P^* H_Q (requires all entries nonzero, equal modulus)."""
    K = mm(dagger(HP), HQ)
    mods = {cyc.norm2(K[i][j]) for i in range(N) for j in range(N)}
    assert len(mods) == 1 and mods != {(0,) * 8}, ("not flat / zero entries", mods)
    m = next(iter(mods))
    assert m[1:] == (0,) * 7 and m[0] > 0
    k00 = K[0][0]
    mm_ = m[0]
    out = [[None] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            q = mul(K[i][j], conj(k00))          # = mm_ * zeta^e
            c = canon(q)
            e = None
            for cand in range(24):
                if c == tuple(mm_ * p for p in cyc.POW[cand]):
                    e = cand
                    break
            assert e is not None, ("entry is not (modulus) x (24th root)", i, j)
            out[i][j] = e
    return out, mm_

def R_of(Phi):
    R = {}
    for i in range(N):
        for j in range(N):
            for k in range(N):
                for l in range(N):
                    s = {}
                    for r in range(N):
                        e = (Phi[i][r] - Phi[j][r] - Phi[k][r] + Phi[l][r]) % 24
                        s[e] = s.get(e, 0) + 1
                    R[(i, j, k, l)] = {e: c for e, c in s.items() if c}
    return R

def projections(PhX, PhY):
    RX, RY = R_of(PhX), R_of(PhY)
    return {(p, q): add(RX[(p[0], p[1], q[0], q[1])], RY[(p[0], p[1], q[0], q[1])])
            for p in EDGES for q in EDGES}

def support(M):
    return {(p, q) for p in EDGES for q in EDGES if not is_zero(M[(p, q)])}

def idempotence_ok(M, supp):
    """(36P)^2 = 36 (36P) on the off-diagonal block, using only the support."""
    for p in EDGES:
        for q in EDGES:
            s = ZERO
            for t in EDGES:
                if (p, t) in supp and (t, q) in supp:
                    s = add(s, mul(M[(p, t)], M[(t, q)]))
            if canon(add(s, cyc.scale(M[(p, q)], -36))) != (0,) * 8:
                return False
    return True

def relations(M, supp):
    rows = set()
    for (i, j), (k, l) in supp:
        r = [0] * N
        r[i] += 1; r[j] -= 1; r[k] -= 1; r[l] += 1
        if any(r):
            rows.add(tuple(r[:5]))
    return sorted(rows)

def rank_f3(rows):
    A = [[v % 3 for v in r] for r in rows]
    rank, piv = 0, 0
    for col in range(5):
        pr = next((i for i in range(piv, len(A)) if A[i][col] % 3), None)
        if pr is None:
            continue
        A[piv], A[pr] = A[pr], A[piv]
        inv = 1 if A[piv][col] % 3 == 1 else 2
        A[piv] = [(x * inv) % 3 for x in A[piv]]
        for i in range(len(A)):
            if i != piv and A[i][col] % 3:
                f = A[i][col] % 3
                A[i] = [(a - f * b) % 3 for a, b in zip(A[i], A[piv])]
        piv += 1
        rank += 1
    return rank

def hnf(rows):
    """Upper-triangular basis of the integer row lattice."""
    M = [list(r) for r in rows if any(r)]
    cur = 0
    for col in range(5):
        if cur >= len(M):
            break
        while True:
            cand = [i for i in range(cur, len(M)) if M[i][col] != 0]
            if len(cand) <= 1:
                break
            # Euclid on the two entries of smallest absolute value
            cand.sort(key=lambda i: abs(M[i][col]))
            i0, i1 = cand[0], cand[1]
            q = M[i1][col] // M[i0][col]
            M[i1] = [a - q * b for a, b in zip(M[i1], M[i0])]
        cand = [i for i in range(cur, len(M)) if M[i][col] != 0]
        if not cand:
            continue
        i0 = cand[0]
        M[cur], M[i0] = M[i0], M[cur]
        for i in range(len(M)):
            if i != cur and M[i][col] != 0:
                q = M[i][col] // M[cur][col]
                M[i] = [a - q * b for a, b in zip(M[i], M[cur])]
        cur += 1
    return [M[i] for i in range(cur)]

def index_of(rows):
    B = hnf(rows)
    if len(B) < 5:
        return None, B
    k = 1
    for i in range(5):
        k *= abs(B[i][i])
    return k, B

def annihilator(B, k):
    """All a in (Q/Z)^5 with B a in Z^5; B upper triangular, det +-k."""
    B = [row[:] for row in B]
    for i in range(5):
        if B[i][i] < 0:
            B[i] = [-x for x in B[i]]
    sols = []
    def rec(i, part):
        if i < 0:
            sols.append(tuple(part))
            return
        d = B[i][i]
        dot = sum((Fraction(B[i][j]) * part[j] for j in range(i + 1, 5)), Fraction(0))
        for t in range(d):
            part[i] = (-dot / d + Fraction(t, d)) % 1
            rec(i - 1, part)
        part[i] = None
    rec(4, [None] * 5)
    assert len(sols) == k, (len(sols), k)
    return sols

def ray_perm(Phi, t):
    cols = [[Fraction(t[i]) + Fraction(Phi[i][r], 24) for i in range(N)] for r in range(N)]
    base = [[Fraction(Phi[i][r], 24) for i in range(N)] for r in range(N)]
    perm = {}
    for r in range(N):
        found = None
        for s in range(N):
            d0 = cols[r][0] - base[s][0]
            if all(((cols[r][i] - base[s][i]) - d0) % 1 == 0 for i in range(N)):
                found = s
                break
        if found is None:
            return None
        perm[r] = found
    return perm

def analyze_anchor(PhX, PhY):
    """PhX, PhY: phase matrices of the two other bases in this anchor's coordinates."""
    M = projections(PhX, PhY)
    supp = support(M)
    rows = relations(M, supp)
    k, B = index_of(rows)
    r3 = rank_f3(rows)
    res = dict(nsup=len(supp), nrows=len(rows), index=k, hnfdiag=[abs(B[i][i]) for i in range(len(B))],
               rank_f3=r3, idem=idempotence_ok(M, supp),
               diag_ok=all(cyc.eq_int(M[((i, j), (i, j))], 12) for (i, j) in EDGES),
               trace_ok=None, nann=0, pres=0, swap=0, ord3=0)
    tr = ZERO
    for (i, j) in EDGES:
        tr = add(tr, M[((i, j), (i, j))])
    res['trace_ok'] = cyc.eq_int(tr, 360)
    if k:
        sols = annihilator(B, k)
        res['nann'] = len(sols)
        for a in sols:
            t = list(a) + [Fraction(0)]
            p1, p2 = ray_perm(PhX, t), ray_perm(PhY, t)
            if p1 is not None and p2 is not None:
                res['pres'] += 1
            elif p1 is None and p2 is None:
                res['swap'] += 1
        res['ord3'] = sum(1 for a in sols if all((3 * x).denominator == 1 for x in a)
                          and any(x.denominator != 1 for x in a))
    return res

def analyze_triple(HA, HB, HC, names=('A', 'B', 'C')):
    reps = [HA, HB, HC]
    Ph = {}
    for i in range(3):
        for j in range(3):
            if i != j:
                Ph[(i, j)], _ = pair_phase(reps[i], reps[j])
    out = {}
    for x in range(3):
        o = [y for y in range(3) if y != x]
        out[names[x]] = analyze_anchor(Ph[(x, o[0])], Ph[(x, o[1])])
    return out
