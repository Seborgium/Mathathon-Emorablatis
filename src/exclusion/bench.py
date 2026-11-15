"""Benchmark: exclusion margins over the actual bin grid of Section 3.7.

Cells: bin midpoints on the U(2) parameter grid of Lemma 3.3
       alpha in [0,1/2], t in [0,1/4], beta,gamma in [0,1]  (cycles), Nu bins each
       (counts Nu/2, Nu/4, Nu, Nu); midpoint = bin centre; h = pi/Nu.
Directions: opt1 = exact optimum of (3.29); quad = second-order certificate at opt1.
"""
import numpy as np, json, sys, time
from cell import Cell, V_of_params
from analyze import dual_optimal, B2, margin2, sigma_J
from test_cell import F6, F23, hadamard_seed

def grid_cells(seed_i, Nu, rng, n_rand=6):
    """All-or-sampled bin midpoints; returns list of (params, U)."""
    al = (seed_i['alpha'] if False else 0)
    Ns = {'alpha': Nu // 2, 't': Nu // 4, 'beta': Nu, 'gamma': Nu}
    out = []
    for _ in range(n_rand):
        i = rng.integers(0, Nu // 2); j = rng.integers(0, Nu // 4)
        k = rng.integers(0, Nu); l = rng.integers(0, Nu)
        p = [(i + .5) / Nu, (j + .5) / Nu, (k + .5) / Nu, (l + .5) / Nu]
        out.append((p, V_of_params(*p)))
    return out

def run(name, H, Nus=(64, 128, 256, 512), n_rand=8, seed=0):
    a, b, c, Dp = hadamard_seed(H)
    rng = np.random.default_rng(seed)
    rows = []
    for Nu in Nus:
        for p, U in grid_cells(None, Nu, rng, n_rand):
            cell = Cell(a, b, c, U, Nu)
            y, v, dist = dual_optimal(cell)
            nrm = np.linalg.norm(y)
            if nrm < 1e-12:
                mu1 = -np.inf; mu2 = -np.inf; yn = np.zeros(20)
            else:
                yn = y / nrm
                mu1 = (yn @ cell.c_all - cell.B1(yn))
                mu2, d = margin2(cell, yn)
            rows.append(dict(seed=name, Nu=Nu, mu1=mu1, mu2=mu2, dist=dist,
                             z=cell.z, Er=cell.Er, p=cell.p, normtest=cell.normtest(),
                             cnorm=float(np.linalg.norm(cell.c_all))))
    return rows

if __name__ == "__main__":
    out = []
    for nm, H in [("F6", F6), ("F2xF3", F23)]:
        out += run(nm, H)
    json.dump(out, open("../../results/exclusion/bench_raw.json", "w"), indent=1)
    print("%-7s %5s %6s %11s %11s %11s %6s" % ("seed", "Nu", "n", "med mu1", "med mu2", "med z", "excl%"))
    for nm in ("F6", "F2xF3"):
        for Nu in (64, 128, 256, 512):
            R = [r for r in out if r['seed'] == nm and r['Nu'] == Nu]
            m1 = np.array([r['mu1'] for r in R]); m2 = np.array([r['mu2'] for r in R])
            print("%-7s %5d %6d %11.4e %11.4e %11.4f %6.0f%%   (mu2>mu1 in %d/%d)"
                  % (nm, Nu, len(R), np.median(m1), np.median(m2), np.median([r['z'] for r in R]),
                     100 * np.mean(m1 > 0), np.sum(m2 > m1), len(R)))
