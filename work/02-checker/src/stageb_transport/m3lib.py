"""m3 shared helpers: exact Stage-B base-grid ledger for one fallback parent.

Everything here mirrors work/02-checker/src/root_interval/stageb_run.py (`ledger`)
line for line, but exposes the *box set* instead of only the counters, so that a
downstream transport search can ask "is THIS box closed, and by how much does the
closest edge miss it".  Conventions are inherited unchanged from stageb.py:
  dq  = Pi(wrap(dp(Phi Q) - dp(P)))
  box b with centre u = b*w and half-width h = w/2 is
      OUTSIDE          iff  sum_a max(|u_a| - h,0)^2  >  E^2,   E = sqrt(1+o_P) R + 1e-7
      RELATION-COVERED iff  exists edge (eta, ell) with  sum_a (|u_a-eta_a| + h)^2 <= ell^2
      UNRESOLVED       otherwise
"""
import itertools
import sys
from fractions import Fraction as Q

sys.path.insert(0, "base")

import numpy as np

import rec
import stageb
from num import Dy
from stageb import up, usqrt
from stageb_run import load_fallback, certified_threshold, IDENT
import align

W = 0.0038          # fallback pass width (Section 5.6 of the paper)
DATA = ("/workspace/nucleus/work/projects/"
        "p-20d35e783d5d4092acb8bd94b19cf30b/repo/.scratch/h0/dl/verification/"
        "saved-run/execution/data")


def load_parent_and_children(DATA=DATA):
    parents, fb = load_fallback(DATA)
    P = parents[0]
    R = Q(P.radius)
    cut = min(.23, float(R) + 0.011 + 1e-6)
    # contiguous-prefix cluster exactly as stageb_run.cluster, but compare with the
    # *exact* dephasing convention (align.dp_matrix) rather than any shortcut
    dpP = align.dp_matrix(P)
    cluster, dists = [], []
    for Qi in fb:
        raw = align.dp_matrix(Qi) - dpP
        raw = raw - np.rint(raw)
        g = raw.sum() / 36.0
        r = raw.sum(1) / 6.0
        c = raw.sum(0) / 6.0
        E = raw + g - r[:, None] - c[None, :]
        d = float(np.sqrt((E ** 2).sum()))
        dists.append(d)
        if d <= cut:
            cluster.append(Qi)
        elif cluster:
            break
    return P, R, fb, cluster, dists, cut


def edges_for(P, R, children, verbose=True):
    """Certified (child, map=IDENT, eta, ell) edges, exactly as stageb_run.ledger."""
    out = []
    for Qi in children:
        rel = stageb.Relation(P, R, Qi)
        if rel.sq.as_fraction() > Q(min(.23, R + 0.011 + 1e-6)):
            continue
        ell, dhat = certified_threshold(rel, Qi.radius)
        out.append(dict(child=Qi.index, rec=Qi, rel=rel, ell=ell, dhat=dhat,
                        eta=[Q(x) for x in rel.eta], radius=Q(Qi.radius)))
    if verbose:
        print(f"  {len(out)} identity edges (||dq|| <= cut), "
              f"ell in [{float(min(e['ell'] for e in out)):.6f}, "
              f"{float(max(e['ell'] for e in out)):.6f}]")
    return out


def grid(P, R, w=W):
    oP = Q(P.ort)
    E = up(usqrt((1 + oP) * Q(R) * Q(R)).as_fraction() + Q(1, 10 ** 7))
    fE = float(E.as_fraction())
    L = int(np.ceil(fE / w + 0.500001))
    return E, L, 2 * L + 1


def box_report(E, L, w, edges, k):
    """Classify every slot; return counters plus the unresolved boxes with deficits."""
    h = Q(w) / 2
    E2 = E.as_fraction() ** 2
    outside = covered = 0
    unresolved = []
    for b in itertools.product(range(-L, L + 1), repeat=k):
        u = [Q(ba * w) for ba in b]
        d2 = Q(0)
        for a in range(k):
            z = abs(u[a]) - h
            if z > 0:
                d2 += z * z
        if d2 > E2:
            outside += 1
            continue
        best = None
        for e in edges:
            s = Q(0)
            for a in range(k):
                z = abs(u[a] - e["eta"][a]) + h
                s += z * z
            deficit = s - e["ell"] * e["ell"]
            if best is None or deficit < best[0]:
                best = (deficit, e["child"], s)
            if deficit <= 0:
                break
        if best is None:
            unresolved.append(dict(idx=b, u=[float(x) for x in u], nearest_child=None,
                                   tB=float("inf"), ell=0.0, deficit=float("inf"),
                                   deficit_sqrt=float("inf")))
            continue
        if best[0] <= 0:
            covered += 1
        else:
            unresolved.append(dict(
                idx=b, u=[float(x) for x in u],
                nearest_child=best[1],
                tB=float(usqrt(best[2]).as_fraction()),
                ell=float(edges[[e["child"] for e in edges].index(best[1])]["ell"]),
                deficit=float(best[0]),
                deficit_sqrt=float(usqrt(best[2]).as_fraction()
                                   - edges[[e["child"] for e in edges].index(best[1])]["ell"])))
    return dict(outside=outside, covered=covered, unresolved=unresolved)
