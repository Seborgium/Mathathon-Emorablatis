"""Per-obligation cost breakdown of the exact Root check on one record."""
import time, sys
import numpy as np
import kernel as K, records as R, rootcheck as C
Q = K.Q
v = R.read(R.DATA + (sys.argv[1] if len(sys.argv) > 1 else "fb1.bin"))
r = v[0]
t0 = time.time()
E = C.exp_table(r.p); t1 = time.time()
F = C.F_enclosure(r.p, E); f2 = C.F_norm_sq_ub(F); t2 = time.time()
T = C.Tmat(r); d1 = C.frob2_gram_defect(T, r.k); d2 = C.pi_T_defect_sq(T, r.k); t3 = time.time()
Mf, HV, LV, lam, krec = C.derive_factors(r); t4 = time.time()
M = [[Q(float(x)) for x in row] for row in Mf]
gH = C.exact_gram(HV); gL = C.exact_gram(LV); ah = C.gram_rowsum(gH); al = C.gram_rowsum(gL); t5 = time.time()
LP = [C.project_iv(row) for row in C.LP_pi_rows(r.p, E)]; t6 = time.time()
dub = C.defect_F_ub(r, M, E, LP); t7 = time.time()
A = C.signed_gram(M); t8 = time.time()
Uf = np.linalg.eigh(np.array([[float(A[i][j]) for j in range(30)] for i in range(30)]))[1]
row = C.congruence_rowsum(A, Uf); t9 = time.time()
print("phase timings (s), record %s[0]:" % sys.argv[1:])
for nm, a, b in [("e(P) 36 exps", t0, t1), ("F(P) + norm", t1, t2), ("R1,R2 exact Gram defects", t2, t3),
                 ("derive factors (numpy)", t3, t4), ("R5 ah,al exact Grams", t4, t5),
                 ("L_P Pi rows (30x36)", t5, t6), ("R6 defect 36x36 interval", t6, t7),
                 ("A = signed Gram of M", t7, t8), ("R7 congruence row sums", t8, t9)]:
    print("   %-28s %6.3f" % (nm, b - a))
print("   TOTAL %.2f s" % (t9 - t0))
