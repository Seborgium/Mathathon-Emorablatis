// c-cover.cpp -- extend() and the covering loop.
//
// Provenance: covout.cpp lines 9-31 and 127-169.
#include "c-cover.hpp"

#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstdlib>

namespace cov {

// covout.cpp:9-31.  The interval of the shared coordinate s compatible with the
// five bins of p, in units of 1/n.  Note (w/4), not (w*w/4): the coordinate is
// the arc length, not the bin coordinate.
SI extend(xy p, int s) {
  SI o{};
  o.p = p;
  F(a, 2) F(j, 5) o.J[a][j] = tab[p.b[j]][a];
  double err = pi * (w / 4) * 5.;
  o.lo = -.5;
  o.hi = .5;
  auto clip = [&](double x, double y) {
    double v = (x * p.c[0] + y * p.c[1]) * n, a = x * o.J[0][s] + y * o.J[1][s];
    if (std::abs(a) < 1e-6) return;
    double r = hp(x, y) * err;
    F(j, 5) if (j != s) r += .5 * std::abs(x * o.J[0][j] + y * o.J[1][j]);
    double mid = -v / a;
    r = (r + 1e-7) / std::abs(a);
    o.lo = std::max(o.lo, mid - r - 1e-5);
    o.hi = std::min(o.hi, mid + r + 1e-5);
  };
  clip(o.J[0][s], o.J[1][s]);
  F(j, 5) if (j != s) clip(-o.J[1][j], o.J[0][j]);
  return o;
}

// covout.cpp:127-169.
void coverSeeds::run(seeds& S, double r, int d, size_t stopAfter) {
  R = r;
  dual = d;
  RN2 = sq(1) * pow(R * n, 2) - .0001;
  T = pow(sqrt(RN2) + 1.5, 2);
  K = int(R * n + .51);
  K = std::max(1, K);
  m = (n + K - 1) / K;
  buckets.resize(m * m * m);
  for (auto p : S.xs) X.push_back(extend(p, p.s));
  Y.resize(n);
  F(i, n) for (auto p : S.ys[i]) Y[i].push_back(extend(p, 0));
  byX.resize(X.size());
  F(t, X.size()) {
    if (size_t(t) >= stopAfter) break;
    const SI& A = X[t];
    for (auto& L : buckets) L.clear();
    // every earlier seed with the same s, bucketed by its accepted centres
    F(h, t) {
      const xy& p = X[h].p;
      if (p.s != A.p.s) continue;
      indexed u{};
      int s = 0, ab = 0;
      F(j, 5) {
        int k = A.p.b[j] - p.b[j];
        u.k[j] = k;
        s += sq(k);
        ab += std::abs(k);
      }
      u.xsq = s;
      u.xab = ab;
      if (s > int(T) || s - ab > RN2) continue;
      for (auto cent : byX[h]) {
        u.y = cent.y;
        insert(u);
      }
    }
    // the candidate partners of A: the cells ys[a] with a = A.b[A.s]
    for (auto& B : Y[A.p.b[A.p.s]]) {
      if (B.p.g + 1e-8 < 1. - (A.p.b[4] + 2) * w) continue;
      if (B.hi < A.lo || B.lo > A.hi) continue;
      checked++;
      if (covered(A, B)) continue;
      cent c{t, {B.p.b[1], B.p.b[2], B.p.b[3], B.p.b[4]}};
      all.push_back(c);
      byX[t].push_back(c);
      indexed u{};
      u.y = c.y;
      insert(u);
    }
    if (!(t % 10000)) printf(" t%d/%zu cells%lu centers%zu\n", t, X.size(), checked, all.size());
  }
  printf("N%d r%.4f dual%d checked%lu centers%zu visit%lu near%lu cheap%lu lp%lu\n", n, R, dual, checked, all.size(),
         nvisit, ncover, ncheap, nlp);
}

}  // namespace cov
