"""Two audit remarks: (i) formula (1) needs BOTH coefficient matrices normalised to modulus
1/sqrt6 (otherwise the support changes -- reproducing m5's 276 vs 246); (ii) relation-row counts
for the (2,3,3) triple, to compare with m5's report."""
import cyc
from cyc import add, mul, canon, ZERO
import mubtools as T
import delta2_test as D   # builds A, B6, C6 and runs the analysis

reps = [D.A, D.B6, D.C6]
Ph = {}
for i in range(3):
    for j in range(3):
        if i != j:
            Ph[(i, j)] = T.pair_phase(reps[i], reps[j])[0]

print("relation rows and support, correctly normalised (phase-matrix formula):")
for x in range(3):
    o = [y for y in range(3) if y != x]
    M = T.projections(Ph[(x, o[0])], Ph[(x, o[1])])
    supp = T.support(M)
    print(f"  anchor {'ABC'[x]}: {len(supp)} nonzero 36P entries, {len(T.relations(M, supp))} relation rows")

print("with the second basis scaled by 6 (i.e. modulus^2 36 instead of 6) -- WRONG normalisation:")
for x in range(3):
    o = [y for y in range(3) if y != x]
    MX = T.projections(Ph[(x, o[0])], Ph[(x, o[1])])
    # emulate V -> 6V : the V-term (a sum of phases, modulus 1) is multiplied by 6^4 = 1296
    MY = T.projections(Ph[(x, o[0])], Ph[(x, o[1])])
    RX = T.R_of(Ph[(x, o[0])]); RY = T.R_of(Ph[(x, o[1])])
    supp = set()
    for p in T.EDGES:
        for q in T.EDGES:
            s = add(RX[(p[0], p[1], q[0], q[1])], cyc.scale(RY[(p[0], p[1], q[0], q[1])], 6**4))
            if not cyc.is_zero(s):
                supp.add((p, q))
    print(f"  anchor {'ABC'[x]}: {len(supp)} nonzero entries")
