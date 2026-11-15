"""Reproducible exact verification of source claims (1),(5),(3),(12) on C^6 triples.

Convention: unnormalised Hadamard reps (entries 24th roots of unity or zero); for an
anchor basis W the coefficient matrices of the other two bases in W-coordinates are
K = H_W^{-1} H_V, all of modulus 1/sqrt6; Phi = phase matrix of H_W^* H_V.
Claim (1):  P = (1/36)[ R(Phi_X) + R(Phi_Y) ],  R(Phi)_{ij,kl} = sum_r Phi_ir conj(Phi_jr) conj(Phi_kr) Phi_lr
is the orthogonal projection of the off-diagonal matrix units onto W_B + W_C.
Checks per anchor: Hermitian; idempotent; tr = 10; diagonal 1/3; and P w = w for the
12 "flat" traceless matrices w_r = b_r b_r^* - I/6, c_s c_s^* - I/6.
"""
import itertools
import cyc
from cyc import add, mul, conj, canon, ZERO, zpow
import mubtools as T

N = 6
EDGES = T.EDGES

def phase_pair(HP, HQ):
    return T.pair_phase(HP, HQ)[0]

def anchor_check(X, Y, PhiX, PhiY, label):
    M = T.projections(PhiX, PhiY)
    supp = T.support(M)
    # Hermitian
    herm = all(canon(add(M[((i, j), (k, l))], cyc.neg(conj(M[((k, l), (i, j))])))) == (0,) * 8
               for (i, j) in EDGES for (k, l) in EDGES)
    # idempotent
    idem = T.idempotence_ok(M, supp)
    # trace and diagonal
    tr = ZERO
    for e in EDGES:
        tr = add(tr, M[(e, e)])
    trace_ok = cyc.eq_int(tr, 360)
    diag_ok = all(cyc.eq_int(M[((i, j), (i, j))], 12) for (i, j) in EDGES)
    # P w = w for the 12 flat traceless matrices of the two other bases
    eigen_ok = True
    for Phi in (PhiX, PhiY):
        for r in range(N):
            for (i, j) in EDGES:
                s = ZERO
                for (k, l) in EDGES:
                    if ((i, j), (k, l)) not in supp:
                        continue
                    s = add(s, mul(M[((i, j), (k, l))],
                                   mul(zpow(Phi[k][r]), conj(zpow(Phi[l][r])))))
                target = cyc.scale(mul(zpow(Phi[i][r]), conj(zpow(Phi[j][r]))), 36)
                if canon(add(s, cyc.neg(target))) != (0,) * 8:
                    eigen_ok = False
    rows = T.relations(M, supp)
    k, B = T.index_of(rows)
    r3 = T.rank_f3(rows)
    sols = T.annihilator(B, k) if k else []
    pres = swap = 0
    from fractions import Fraction
    for a in sols:
        t = list(a) + [Fraction(0)]
        p1, p2 = T.ray_perm(PhiX, t), T.ray_perm(PhiY, t)
        if p1 is not None and p2 is not None:
            pres += 1
        elif p1 is None and p2 is None:
            swap += 1
    print(f"[{label}] support {len(supp)}, Hermitian {herm}, idempotent {idem}, tr=10 {trace_ok}, "
          f"diag=1/3 {diag_ok}, P w = w (12 vectors) {eigen_ok}")
    print(f"        HNF diag {[abs(B[i][i]) for i in range(len(B))]}, index {k}, rank_F3 {r3}, "
          f"|Ann| {len(sols)}, preserve {pres}, swap {swap}")
    # clock count check: #{a : 3a = 0} = 3^(5-rank)
    c3 = sum(1 for a in sols if all((3 * x).denominator == 1 for x in a))
    print(f"        3-torsion of Ann: {c3} = 3^(5-rank_F3) = {3**(5-r3)}: {c3 == 3**(5-r3)}")
    return dict(supp=len(supp), index=k, rank_f3=r3, swap=swap, eigen=eigen_ok, idem=idem, herm=herm)

if __name__ == '__main__':
    b2 = {'A2': T.ident(2), 'B2': T.rep(T.B2), 'C2': T.rep(T.C2)}
    b3 = {'A3': T.ident(3), 'B3': T.rep(T.F3), 'C3': T.rep(T.C3), 'D3': T.rep(T.D3)}
    HA = T.kron(b2['A2'], b3['A3'])
    HB = T.kron(b2['B2'], b3['B3'])
    HC = T.kron(b2['C2'], b3['C3'])
    reps = [HA, HB, HC]
    names = 'ABC'
    print("basis checks:", [T.is_basis_rep(M, 6) for M in reps],
          "unbiased:", [T.is_unbiased_rep(reps[i], reps[j], 6) for i in range(3) for j in range(i+1, 3)])
    for x in range(3):
        o = [y for y in range(3) if y != x]
        Phi = [phase_pair(reps[x], reps[y]) for y in o]
        anchor_check(reps[o[0]], reps[o[1]], Phi[0], Phi[1], names[x])
