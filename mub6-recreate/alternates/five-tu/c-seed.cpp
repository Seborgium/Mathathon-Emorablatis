// c-seed.cpp -- the definitions of the seed module: globals, enumeration, and the
// two drowsy drivers that the recorded run does not use.
//
// Provenance: seed.cpp lines 37-38 (globals), 54-73 (share), 85-110 (build, list).
#include "c-seed.hpp"

#include <algorithm>
#include <cstdint>
#include <utility>

namespace cov {

int n;
double w;
std::vector<V> tab;

// seed.cpp:54-73.  Low/up is the intersection over both cells of the t-interval
// compatible with every bin direction; a common point exists iff low <= up.
bool share(const xy& X, const xy& Y) {
  int b = Y.b[0], skip[2] = {X.s, 0};
  double low = -w / 2, up = w / 2;
  F(t, 2) {
    auto& p = t ? Y : X;
    double err = pi * (w * w / 4) * 5.;
    auto clip = [&](double x, double y) {
      double v = x * p.c[0] + y * p.c[1], a = x * tab[b][0] + y * tab[b][1];
      if (std::abs(a) < 1e-6) return;
      double r = hp(x, y) * err;
      F(j, 5) if (j != skip[t]) r += (w / 2) * std::abs(x * tab[p.b[j]][0] + y * tab[p.b[j]][1]);
      double mid = -v / a;
      r /= std::abs(a);
      low = std::max(low, mid - r - 1e-10);
      up = std::min(up, mid + r + 1e-10);
    };
    clip(tab[b][0], tab[b][1]);
    F(j, 5) if (j != skip[t]) {
      int d = p.b[j];
      clip(-tab[d][1], tab[d][0]);
    }
  }
  return low <= up;
}

// seed.cpp:85-96.
//
// The xs recursion admits non-decreasing bin tuples (a <= b <= c <= d <= e) and
// prunes with a <= e-d+1; the surviving cell is kept iff its gap is not too large
// and sumok's five interval tests pass.  Appends happen in the loop order, which
// is (e,d,c,b,a) -- see c-seed.hpp.
//
// The ys recursion is *not* the same enumeration: a is the outermost loop and is
// stored first (b[0] = a), while the remaining four bins satisfy b <= c <= d <= e
// and are enumerated with e outermost and b innermost.  mk is told b is unsorted,
// so p.b keeps (a, b, c, d, e) as constructed and only the gap g is computed from
// the sorted multiset.
void seeds::build(int nn) {
  n = nn;
  w = 1. / n;
  tab.clear();
  F(i, n) tab.push_back(expair((i + .5) / n));
  F(e, n) F(d, e + 1) F(c, d + 1) F(b, c + 1) F(a, b + 1) {
    if (a > e - d + 1) continue;
    xy p = mk({a, b, c, d, e}, true);
    if (p.g > 1. - (e - 1) * w + 1e-8) continue;
    if (sumok(p)) xs.push_back(p);
  }
  ys.resize(n);
  F(a, n) F(e, n) F(d, e + 1) F(c, d + 1) F(b, c + 1) {
    xy p = mk({a, b, c, d, e}, false);
    if (sumok(p)) ys[a].push_back(p);
  }
}

// seed.cpp:97-110.  Dead in the recorded run (samples == 0 in every recorded
// command, and covrun never calls it); reproduces the printed statistics.
std::vector<std::pair<xy, xy>> seeds::list(int samples) {
  std::vector<std::pair<xy, xy>> out;
  std::mt19937_64 rng(42);
  uint64_t m = 0, h = 0, ym = 0, v = 0;
  (void)v;
  for (auto X : xs)
    for (auto Y : ys[X.b[X.s]]) {
      ++ym;
      if (Y.g < 1. - (X.b[4] + 2.0001) * w) continue;
      ++h;
      if (!share(X, Y)) continue;
      m++;
      if (out.size() < size_t(samples)) out.emplace_back(X, Y);
      else if (samples > 0) {
        auto j = rng() % m;
        if (j < uint64_t(samples)) out[j] = {X, Y};
      }
    }
  printf("%d xs%zu avg y %.1f counts gap %lu share %lu out %zu\n", n, xs.size(), ym / double(xs.size()), h, m,
         out.size());
  return out;
}

}  // namespace cov
