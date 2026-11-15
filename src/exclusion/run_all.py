"""All measurements reported in results/exclusion/report.md."""
import numpy as np, json
from test_cell import F6, F23, hadamard_seed
from cell import Cell, V_of_params, u_params
import analyze as A
from verify import certify

out = {}

def best_dir(cell):
    y, v, dist = A.dual_optimal(cell)
    n = np.linalg.norm(y)
    if n < 1e-13:
        return cell.c_all / max(np.linalg.norm(cell.c_all), 1e-300)
    return y / n

def one(cell, tag, store):
    yo = best_dir(cell)
    mh, yh = A.heuristic(cell)
    store.append(dict(tag=tag, Nu=cell.Nu, n=cell.Nu,
                      mu_opt=float(cell.margin(yo)),
                      mu_opt_merged=float(A.margin3(cell, yo)),
                      mu_heur=float(mh),
                      mu_heur_merged=float(A.margin3(cell, yh)),
                      mu_delta=float(cell.margin(yo) - cell.margin(yh)),
                      z=cell.z, Er=cell.Er, p=cell.p, cnorm=float(np.linalg.norm(cell.c_all))))

# ---------------- A. random cells at the levels where (3.29) is used
rows = []
for nm, H in [("F6", F6), ("F2xF3", F23)]:
    a, b, c, Dp = hadamard_seed(H)
    rng = np.random.default_rng(11)
    for Nu in (64, 128, 256, 512):
        for i in range(4):
            p = [(rng.integers(0, Nu // 2) + .5) / Nu, (rng.integers(0, Nu // 4) + .5) / Nu,
                 (rng.integers(0, Nu) + .5) / Nu, (rng.integers(0, Nu) + .5) / Nu]
            one(Cell(a, b, c, V_of_params(*p), Nu), nm, rows)
out['random_cells'] = rows

# ---------------- B. distance-to-completion boundary
bd = []
for nm, H in [("F6", F6), ("F2xF3", F23)]:
    a, b, c, Dp = hadamard_seed(H)
    tmp = Cell(a, b, c, np.eye(2), 64)
    Y = tmp.KC.conj().T @ Dp @ tmp.KB
    Us, s, Vh = np.linalg.svd(Y); Vstar = Us @ Vh
    al, t_, be, ga = u_params(Vstar)
    for Nu in (64, 128, 256, 512):
        ts = np.linspace(0, 0.10, 21)
        rec = dict(seed=nm, Nu=Nu, t=list(ts), mu_opt=[], mu_merged=[], normtest=[], muEr0=[])
        for t in ts:
            cell = Cell(a, b, c, V_of_params(al + t, t_, be, ga), Nu)
            y = best_dir(cell)
            rec['mu_opt'].append(float(cell.margin(y)))
            rec['mu_merged'].append(float(A.margin3(cell, y)))
            rec['normtest'].append(float(cell.normtest()))
            E = cell.Er; cell.Er = 0.0
            rec['muEr0'].append(float(cell.margin(y))); cell.Er = E
        bd.append(rec)
out['boundary'] = bd

# ---------------- C. rigorous verification of two certificates
cert = []
for nm, H, Nu in [("F6", F6, 64), ("F2xF3", F23, 512)]:
    a, b, c, Dp = hadamard_seed(H)
    rng = np.random.default_rng(7)
    p = [(rng.integers(0, Nu // 2) + .5) / Nu, (rng.integers(0, Nu // 4) + .5) / Nu,
         (rng.integers(0, Nu) + .5) / Nu, (rng.integers(0, Nu) + .5) / Nu]
    cell = Cell(a, b, c, V_of_params(*p), Nu)
    y = best_dir(cell)
    rec = certify(cell, y, "%s Nu=%d optimal" % (nm, Nu)); rec['seed'] = nm; rec['Nu'] = Nu
    cert.append(rec)
    ym = A.heuristic(cell)[1]
    rec2 = certify(cell, ym, "%s Nu=%d heuristic" % (nm, Nu)); rec2['seed'] = nm; rec2['Nu'] = Nu
    cert.append(rec2)
out['certificates'] = cert
json.dump(out, open("../../results/exclusion/measurements.json", "w"), indent=1)
print("done", len(rows), len(bd), len(cert))
