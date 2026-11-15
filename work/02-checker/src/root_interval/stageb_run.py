"""Complete base-grid Stage-B ledger for ONE real fallback parent.

Established facts used (all from the paper, all checkable from stored fields):
  (5.20)  every parent solution has ||eta|| <= E = sqrt(1+o_P) R + 1e-7,
  (5.21)  the base boxes B(u, w/2), u = b w, |b_a| <= L tile [E]^k, so every
          tangent vector lies in at least one box;
  (5.22)  box outside the ball of radius E => no parent solution in it,
  (5.24)  t_B(box) = sqrt(sum (|u_a - eta_q,a| + h)^2) bounds the tangent distance
          to the child Q from above, uniformly over the box;
  (5.17)  a *verified* pair (l, D^(l)) with D^(l) <= r certifies that every parent
          solution with tangent distance <= l lies in S(Q, r).
No monotonicity of D^ is used: only the verified values at the trial points.

A box is discharged when it is outside, or t_B <= l for one of the listed children.
Everything else is reported as UNRESOLVED, i.e. it needs the subdivision tree,
which the saved run did not archive.
"""
import glob
import sys
import time
from fractions import Fraction as Q

import numpy as np

import align
import num
import rec
import stageb
from num import Dy
from stageb import up, umul, usqrt, umin, Relation

IDENT = ((0, 1, 2, 3, 4, 5), (0, 1, 2, 3, 4, 5), 0, 0)
KMAX = 10


def load_fallback(DATA):
    parents = []
    for b in sorted(glob.glob(DATA + "/batches/bad*.bin")):
        parents += rec.read_records(b)
    fb = rec.read_records(DATA + "/fb1.bin")
    return parents, fb


def cluster(P, children, cut, verbose=False):
    """Contiguous run of atlas children whose identity-map alignment is admissible.
    (The child blocks are contiguous in insertion order; we *test* every child
    rather than assume it.)"""
    dpP = align.dp_matrix(P)
    out, dists = [], []
    for Qi in children:
        d, mp = align.best_map(dpP, align.dp_matrix(Qi), block=720) if False else (None, None)
        dpq = align.dp_matrix(Qi)
        raw = dpq - dpP
        raw = raw - np.rint(raw)
        g = raw.sum() / 36.0
        r = raw.sum(1) / 6.0
        c = raw.sum(0) / 6.0
        E = raw + g - r[:, None] - c[None, :]
        d = float(np.sqrt((E ** 2).sum()))
        dists.append(d)
        if d <= cut:
            out.append(Qi)
        elif out:
            break
    if verbose:
        print("   identity distances of the scanned prefix:", [round(x, 4) for x in dists])
    return out


def certified_threshold(rel, radius, steps=40):
    """Largest *verified* l with D^(l) <= radius (D^ evaluated exactly there)."""
    d0 = rel.D(Q(0))
    if d0.as_fraction() > Q(radius):
        return Q(0), d0
    lo, hi = Q(0), Q(2)
    best = d0
    for _ in range(steps):
        mid = (lo + hi) / 2
        dm = rel.D(mid)
        if dm.as_fraction() <= Q(radius):
            lo, best = mid, dm
        else:
            hi = mid
    return lo, best


def ledger(P, R, children, w, max_children=None, verbose=True):
    k = P.k
    oP = Q(P.ort)
    E2 = (1 + oP) * Q(R) * Q(R)                       # E upper bound below
    E = usqrt((1 + oP) * Q(R) * Q(R))                 # sqrt(1+o_P) R, upward
    E = up(E.as_fraction() + Q(1, 10 ** 7))           # +1e-7 as in (5.20)
    fE = float(E.as_fraction())
    L = int(np.ceil(fE / w + 0.500001))
    n = 2 * L + 1
    total = n ** k
    if verbose:
        print(f"parent {P.source.split('/')[-1]}#{P.index} k={k} R={R:.6g} "
              f"E={fE:.6g} w={w} L={L} n={n} boxes={total}")
    # relations
    t0 = time.time()
    rels = []
    for Qi in (children if max_children is None else children[:max_children]):
        mp = IDENT
        Qt = align.transform(Qi, mp) if mp != IDENT else Qi
        rel = Relation(P, R, Qt, cut=None)
        if rel.sq.as_fraction() > Q(min(.23, R + 0.011 + 1e-6)):
            continue
        ell, dhat = certified_threshold(rel, Qi.radius)
        rels.append((Qi, rel, ell, dhat))
    t_rel = time.time() - t0
    if verbose:
        print(f"  {len(rels)} admissible relations, cost {t_rel:.2f}s "
              f"({t_rel / max(1, len(rels)) * 1e3:.0f} ms each incl. threshold search)")
        for Qi, rel, ell, dhat in rels:
            print(f"    fb1#{Qi.index:<4d} a={Qi.radius:.6f} ||dq||={float(rel.sq.as_fraction()):.5f}"
                  f" sq={float(rel.sq.as_fraction()):.4f} l={float(ell):.6f} D(l)={float(dhat.as_fraction()):.6f}")
    if not rels:
        return dict(total=total, outside=0, covered=0, unresolved=total, rels=[])
    # grid sweep
    t0 = time.time()
    shapes = []
    for a in range(k):
        shapes.append([Q(b * w) for b in range(-L, L + 1)])
    h = Q(w) / 2
    ell2 = [(Qi, ell * ell, ell) for (Qi, rel, ell, dhat) in rels]
    outside = covered = unresolved = 0
    uncov_examples = []
    import itertools
    idx = [range(-L, L + 1)] * k
    for b in itertools.product(*idx):
        u = [Q(b[a] * w) for a in range(k)]
        d2 = Q(0)
        for a in range(k):
            z = abs(u[a]) - h
            if z > 0:
                d2 += z * z
        if d2 > E.as_fraction() ** 2:
            outside += 1
            continue
        hit = None
        for (Qi, rel, ell, dhat) in rels:
            s = Q(0)
            for a in range(k):
                z = abs(u[a] - rel.eta[a]) + h
                s += z * z
            if s <= ell * ell:
                hit = Qi
                break
        if hit is not None:
            covered += 1
        else:
            unresolved += 1
            if len(uncov_examples) < 6:
                uncov_examples.append(b)
    t_box = time.time() - t0
    if verbose:
        print(f"  grid sweep {total} boxes in {t_box:.2f}s ({t_box / total * 1e6:.0f} us/box)")
        print(f"  outside={outside} relation-covered={covered} UNRESOLVED={unresolved}")
        if uncov_examples:
            print(f"  first unresolved box indices: {uncov_examples}")
    return dict(total=total, outside=outside, covered=covered, unresolved=unresolved,
                rels=[(Qi.index, float(ell), float(Qi.radius)) for (Qi, rel, ell, dhat) in rels],
                t_rel=t_rel, t_box=t_box)


def main():
    DATA = sys.argv[1] if len(sys.argv) > 1 else (
        "/workspace/nucleus/work/projects/p-20d35e783d5d4092acb8bd94b19cf30b/repo/.scratch/"
        "h0/dl/verification/saved-run/execution/data")
    parents, fb = load_fallback(DATA)
    w = 0.0038                          # fallback pass width (Section 5.6)
    P = parents[0]
    R = Q(P.radius)
    cut = min(.23, float(R) + 0.011 + 1e-6)
    ch = cluster(P, fb, cut, verbose=True)
    print(f"cluster size {len(ch)} of {len(fb)} children (cut {cut:.4f})")
    res = ledger(P, R, ch, w)
    print(res)


if __name__ == "__main__":
    main()
