"""Delta-tuples of the 24 product MUB triples in C^6 = C^2 (x) C^3, computed exactly."""
import itertools, time
import mubtools as T

b2 = {'A2': T.ident(2), 'B2': T.rep(T.B2), 'C2': T.rep(T.C2)}
b3 = {'A3': T.ident(3), 'B3': T.rep(T.F3), 'C3': T.rep(T.C3), 'D3': T.rep(T.D3)}
names3 = ['A3', 'B3', 'C3', 'D3']

rows = []
t0 = time.time()
for perm in itertools.permutations(names3, 3):
    HA = T.kron(b2['A2'], b3[perm[0]])
    HB = T.kron(b2['B2'], b3[perm[1]])
    HC = T.kron(b2['C2'], b3[perm[2]])
    res = T.analyze_triple(HA, HB, HC)
    labels = ''.join(perm)
    tup = tuple(res[k]['index'] for k in 'ABC')
    rows.append((labels, tup, res))
    print(labels, 'indices (Delta_A,Delta_B,Delta_C) =', tup,
          ' rankF3 =', tuple(res[k]['rank_f3'] for k in 'ABC'),
          ' nsup =', tuple(res[k]['nsup'] for k in 'ABC'),
          ' swaps =', tuple(res[k]['swap'] for k in 'ABC'),
          ' idem/trace/diag =', [(res[k]['idem'], res[k]['trace_ok'], res[k]['diag_ok']) for k in 'ABC'],
          f'({time.time()-t0:.0f}s)')
print()
print("distinct index-tuples up to relabelling:")
seen = {}
for labels, tup, res in rows:
    key = tuple(sorted(tup))
    seen.setdefault(key, []).append(labels)
for k, v in sorted(seen.items()):
    print("  ", k, "->", len(v), "labellings, e.g.", v[:3])
