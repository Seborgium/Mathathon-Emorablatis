"""m1 audit: projection formula (1), support lattice, index/Delta, swap test -- exact.

Triple in C^6 (standard product construction):
   A = standard basis            (exponent matrix E = 0)
   B = F_2 (x) F_3               (unnormalised Hadamards, entries are 24th roots)
   C = diag(1,i) F_2 (x) diag(1,w,w) F_3   (chirp d_r = w^(r^2))
Index order:  i = 3*a + r with a in Z_2, r in Z_3.
All arithmetic in Z[zeta_24] (cyc.py).
"""
import itertools
from fractions import Fraction
import cyc
from cyc import add, mul, conj, zpow, is_zero, canon, ZERO, ONE

N = 6
F2 = [[0, 0], [0, 12]]
F3 = [[0, 0, 0], [0, 8, 16], [0, 16, 8]]
C2 = [[6 * a + F2[a][b] for b in range(2)] for a in range(2)]      # diag(1,i) F_2
C3 = [[8 * (r * r) + F3[r][s] for s in range(3)] for r in range(3)]  # chirp diag(1,w,w) F_3
E = [[0] * N for _ in range(N)]
F = [[F2[i // 3][j // 3] + F3[i % 3][j % 3] for j in range(N)] for i in range(N)]
C = [[C2[i // 3][j // 3] + C3[i % 3][j % 3] for j in range(N)] for i in range(N)]
MATS = {'A': E, 'B': F, 'C': C}

def unnorm(Phi):
    return [[zpow(Phi[i][j]) for j in range(N)] for i in range(N)]

def check_hadamard(Phi, name):
    M = unnorm(Phi)
    ok = True
    for i in range(N):
        for j in range(N):
            s = ZERO
            for k in range(N):
                s = add(s, mul(M[k][i], conj(M[k][j])))
            target = 6 if i == j else 0
            if not cyc.eq_int(s, target):
                ok = False
    print(f"  {name} Hadamard (H^*H = 6I, exact): {ok}")
    return ok

def star_product(P, Q):
    """(P^* Q)_{ij} = sum_k conj(P_{ki}) Q_{kj}, entries as cyclotomic dicts."""
    R = [[ZERO] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            s = ZERO
            for k in range(N):
                s = add(s, mul(conj(zpow(P[k][i])), zpow(Q[k][j])))
            R[i][j] = s
    return R

def flat_check(Phi, Psi, name):
    R = star_product(Phi, Psi)
    bad = [R[i][j] for i in range(N) for j in range(N) if cyc.norm2(R[i][j]) != (6,) + (0,) * 7]
    print("  |(" + name + ")_ij|^2 = 6 for all i,j (exact): " + str(not bad))
    # extract the phase exponents
    Ph = [[None] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            Ph[i][j] = cyc.phase_of_flat(R[i][j])
    print(f"    all 36 entries are sqrt6 * (24th root): {all(x is not None for row in Ph for x in row)}")
    return Ph

def Rmat(Phi):
    """R[i][j][k][l] = sum_r zeta^(Phi_ir - Phi_jr - Phi_kr + Phi_lr)  (dicts)."""
    R = [[[[ZERO] * N for _ in range(N)] for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            for k in range(N):
                for l in range(N):
                    s = {}
                    for r in range(N):
                        e = (Phi[i][r] - Phi[j][r] - Phi[k][r] + Phi[l][r]) % 24
                        s[e] = s.get(e, 0) + 1
                    R[i][j][k][l] = {e: c for e, c in s.items() if c}
    return R

EDGES = [(i, j) for i in range(N) for j in range(N) if i != j]

def projection_data(PhiX, PhiY, label):
    """P = (1/36)(R(PhiX) + R(PhiY)) restricted to off-diagonal matrix units."""
    RX = Rmat(PhiX)
    RY = Rmat(PhiY)
    idx = {p: n for n, p in enumerate(EDGES)}
    M = [[ZERO] * 30 for _ in range(30)]
    support = []
    for p, (i, j) in enumerate(EDGES):
        for q, (k, l) in enumerate(EDGES):
            M[p][q] = add(RX[i][j][k][l], RY[i][j][k][l])
    # exact idempotence:  M^2 = 36 M   (equivalently (M/36)^2 = M/36)
    ok = True
    tr = ZERO
    for p in range(30):
        for q in range(30):
            s = ZERO
            for t in range(30):
                if is_zero(M[p][t]) or is_zero(M[t][q]):
                    continue
                s = add(s, mul(M[p][t], M[t][q]))
            if canon(add(s, cyc.scale(M[p][q], -36))) != (0,) * 8:
                ok = False
    for p in range(30):
        tr = add(tr, M[p][p])
    print(f"[{label}] nonzero entries of 36P: {sum(1 for p in range(30) for q in range(30) if not is_zero(M[p][q]))}")
    print(f"[{label}] trace of 36P (exact) = {canon(tr)[:1]}, i.e. tr P = 10: {cyc.eq_int(tr, 360)}")
    print(f"[{label}] diagonal entries 36P_ss = 12 (i.e. 1/3): "
          f"{all(cyc.eq_int(M[p][p], 12) for p in range(30))}")
    print(f"[{label}] (36P)^2 = 36*(36P) entrywise (exact idempotence): {ok}")
    return M

def relations(M):
    rows = set()
    for p, (i, j) in enumerate(EDGES):
        for q, (k, l) in enumerate(EDGES):
            if is_zero(M[p][q]):
                continue
            r = [0] * N
            r[i] += 1; r[j] -= 1; r[k] -= 1; r[l] += 1
            if any(r):
                rows.add(tuple(r[:5]))
    return sorted(rows)

def rank_f3(rows):
    A = [[v % 3 for v in r] for r in rows]
    rank = 0
    piv = 0
    for col in range(5):
        pr = None
        for i in range(piv, len(A)):
            if A[i][col] % 3:
                pr = i; break
        if pr is None:
            continue
        A[piv], A[pr] = A[pr], A[piv]
        inv = {1: 1, 2: 2}[A[piv][col] % 3]
        A[piv] = [(x * inv) % 3 for x in A[piv]]
        for i in range(len(A)):
            if i != piv and A[i][col] % 3:
                f = A[i][col] % 3
                A[i] = [(a - f * b) % 3 for a, b in zip(A[i], A[piv])]
        piv += 1
        rank += 1
    return rank

def snf_index(rows):
    import sympy as sp
    from sympy.matrices.normalforms import smith_normal_form
    Mx = sp.Matrix(rows)
    S = smith_normal_form(Mx, domain=sp.ZZ)
    diag = [abs(int(S[i, i])) for i in range(min(S.shape))]
    d = [x for x in diag if x]
    idx = 1
    for x in d:
        idx *= x
    return diag, idx, len(d)

def annihilator(rows, index):
    """All a in (Q/Z)^5 with r.a = 0 mod 1 for all r in rows. Uses index*Z^5 subset L."""
    sols = []
    for a in itertools.product(range(index), repeat=5):
        a = [Fraction(x, index) for x in a]
        if all(sum(Fraction(r[j]) * a[j] for j in range(5)).denominator == 1 for r in rows):
            sols.append(a)
    return sols

def ray_perm_test(Phi, t, tol=0):
    """Does diag(phase t_i) (t in turns) permute the rays (columns) of Phi?"""
    cols = [[Fraction(t[i]) + Fraction(Phi[i][r], 24) for i in range(N)] for r in range(N)]
    base = [[Fraction(Phi[i][r], 24) for i in range(N)] for r in range(N)]
    perm = {}
    for r in range(N):
        found = None
        for s in range(N):
            d0 = (cols[r][0] - base[s][0])
            if all(((cols[r][i] - base[s][i]) - d0) % 1 == 0 for i in range(N)):
                found = s; break
        if found is None:
            return None
        perm[r] = found
    return perm

# ---------------------------------------------------------------- driver
if __name__ == '__main__':
    import time
    print("== step 1: the triple is a genuine MUB triple (exact, in Z[zeta_24]) ==")
    check_hadamard(F, 'B = F2 (x) F3')
    check_hadamard(C, 'C = diag(1,i)F2 (x) diag(1,w,w^2)F3')
    print("  A = standard basis: trivially orthonormal, all |A_ij| in {0,1}")

    # phase matrices of the pairs seen from each anchor
    # anchor A: coordinate matrices of B and C are F and C themselves
    # anchor B: A -> F^*,  C -> F^* C  (= sqrt6 * phase matrix)
    # anchor C: A -> C^*,  B -> C^* F
    PhaseA_B = F
    PhaseA_C = C
    print("== step 2: cross-unbiasedness (exact) ==")
    PhaseB_C = flat_check(F, C, 'B^*C')

    anchors = {
        'A': dict(X=F, Y=C, desc="coordinate basis A, pair (B,C)"),
        'B': dict(X=None, Y=None, desc="coordinate basis B, pair (A,C)"),
        'C': dict(X=None, Y=None, desc="coordinate basis C, pair (A,B)"),
    }
    # F^* is the conjugate transpose of the exponent matrix: exponent -> -exponent
    Fstar = [[(-F[j][i]) % 24 for j in range(N)] for i in range(N)]
    Cstar = [[(-C[j][i]) % 24 for j in range(N)] for i in range(N)]
    anchors['B']['X'] = Fstar
    anchors['B']['Y'] = PhaseB_C
    anchors['C']['X'] = Cstar
    # C^* F: entries conj(C_ki) F_kj
    PhaseC_B = flat_check(C, F, 'C^*F')
    anchors['C']['Y'] = PhaseC_B

    results = {}
    for lab in ('A', 'B', 'C'):
        t0 = time.time()
        X = anchors[lab]['X']; Y = anchors[lab]['Y']
        print(f"\n== anchor {lab}: {anchors[lab]['desc']}  ({time.time()-t0:.1f}s) ==")
        M = projection_data(X, Y, lab)
        rows = relations(M)
        diag, index, rank = snf_index(rows)
        print(f"[{lab}] relation rows: {len(rows)}; Smith diag {diag}; rank {rank}; index [Z^5:L] = {index}")
        r3 = rank_f3(rows)
        print(f"[{lab}] rank over F_3 of the relation matrix = {r3}  ->  3 | index: {index % 3 == 0}  <->  rank<5: {r3 < 5}")
        sols = annihilator(rows, index)
        print(f"[{lab}] |Ann(L)| by brute force = {len(sols)} (equals index: {len(sols) == index})")
        # classify group elements: preserve each basis, or swap?
        kinds = {'id': 0, 'pres': 0, 'swap': 0, 'neither': 0}
        for a in sols:
            t = [a[j] for j in range(5)] + [Fraction(0)]
            pb = ray_perm_test(F, t)
            pc = ray_perm_test(C, t)
            if pb is not None and pc is not None:
                kinds['id' if all(x == 0 for x in t) else 'pres'] += 1
            elif pb is not None or pc is not None:
                kinds['neither'] += 1
            else:
                kinds['swap'] += 1
        print(f"[{lab}] group elements: {kinds}  (swap = an element mapping B-rays onto C-rays)")
        order3 = [a for a in sols if all((3 * x) % 1 == 0 for x in a) and any(x % 1 != 0 for x in a)]
        print(f"[{lab}] elements of projective order 3 in Ann(L): {len(order3)}")
        results[lab] = dict(index=index, diag=diag, rows=rows, r3=r3, kinds=kinds)
