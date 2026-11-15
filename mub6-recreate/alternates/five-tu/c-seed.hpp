// c-seed.hpp -- seed enumeration: bins, grid cells, the interval test, and the
// two nested-loop enumerations whose append order fixes the centre index t.
//
// Provenance: seed.cpp lines 18-20 (types), 36 (struct xy), 37-38 (globals),
// 39-53 (sumok), 54-73 (share), 74-107 (struct seeds).
//
// ORDER IS PART OF THE CONTRACT.  seeds::build appends to xs in
//   (e, d, c, b, a)  lexicographic ascending order   [e outermost, a innermost]
// and to ys[a] in
//   (e, d, c, b)     lexicographic ascending order   [e outermost, b innermost]
// for fixed a.  xs's index is the `t` of covout.cpp, so the second loop's order
// is invisible in centres.txt but the first loop's order is the file's row order
// within each t block.  See NOTES.md.
#ifndef C_SEED_HPP
#define C_SEED_HPP
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdio>
#include <random>
#include <utility>
#include <vector>

#include "c-fp.hpp"

namespace cov {

using ar = std::array<int, 5>;

// seed.cpp:36  struct xy{ar b; int s; double g,c[2];};
//   b[0..4] the five bins of the cell, in the order the enumeration produced them;
//   s       the index of the bin nearest the centre n/2 (of b as passed to mk);
//   g       the gap of the cell, in units of w, from the *sorted* multiset of bins;
//   c[0..2] the centroid of the cell, filled in by sumok.
struct xy {
  ar b;
  int s;
  double g, c[2];
};

// seed.cpp:37-38  int n; double w; vector<V> tab;
// n = number of bins, w = 1/n, tab[i] = e^{2*pi*i*(i+1/2)/n} = expair((i+.5)/n).
extern int n;
extern double w;
extern std::vector<V> tab;

// seed.cpp:39-53  sumok: the cell centroid c satisfies five interval tests
//   |<u,c>| <= hp(u)*err + sum_j (w/2)*|<u,tab[b_j]>|,   err = pi*(w*w/4)*5,
// one for u = c and one for each u = (-tab[b_j][1], tab[b_j][0]).
// Returns false as soon as a test fails; on true, p.c holds the centroid.
inline bool sumok(xy& p) {
  double c[2] = {0., -1. / (2 * pi)};
  for (auto b : p.b) {
    c[0] += tab[b][1] / (2 * pi);
    c[1] -= tab[b][0] / (2 * pi);
  }
  p.c[0] = c[0];
  p.c[1] = c[1];
  double err = pi * (w * w / 4) * 5.;
  auto chk = [&](double x, double y) {
    double l = std::abs(x * c[0] + y * c[1]), r = hp(x, y) * err;
    for (auto b : p.b) r += (w / 2) * std::abs(x * tab[b][0] + y * tab[b][1]);
    return !(l > r + 1e-8);
  };
  if (!chk(c[0], c[1])) return false;
  for (auto b : p.b)
    if (!chk(-tab[b][1], tab[b][0])) return false;
  return true;
}

// seed.cpp:54-73  share: do the two cells X and Y have a common point of the
// projected torus?  Not used by covrun (only by the unbuilt seeds::list driver)
// but part of the seed module boundary.
bool share(const xy& X, const xy& Y);

struct seeds {
  // xs: every 5-subset of bins with a <= e-d+1 and gap filter, in
  //     (e,d,c,b,a) lexicographic order -- the order that defines t.
  // ys[a]: for the outer-loop bin a, the four remaining bins in (e,d,c,b)
  //     lexicographic order; p.b = (a,b,c,d,e) with b<=c<=d<=e but a free.
  std::vector<xy> xs;
  std::vector<std::vector<xy>> ys;

  // seed.cpp:76-84  mk: fill s and g of a cell.
  //   s = argmin_j |b[j]*2+1-n|, ties going to the earliest j, scanning j = 0..4
  //       in the *passed* order (before the optional sort);
  //   g = 0.5*max(2*b_min+1, 2*n-(2*b_max+1)) maximised over adjacent gaps of the
  //       sorted multiset, scaled by w.  `sorted` means "b is already sorted".
  static xy mk(ar b, bool sorted) {
    xy p{};
    p.b = b;
    F(j, 5) if (std::abs(b[j] * 2 + 1 - n) < std::abs(b[p.s] * 2 + 1 - n)) p.s = j;
    if (!sorted) std::sort(b.begin(), b.end());
    p.g = .5 * std::max(2 * b[0] + 1, 2 * n - (2 * b[4] + 1));
    F(j, 4) p.g = std::max(p.g, double(b[j + 1] - b[j]));
    p.g *= w;
    return p;
  }

  // seed.cpp:85-96  build: tabulate, then enumerate.
  void build(int nn);

  // seed.cpp:97-110  list: the reservoir-sampled share test (seeded mt19937_64(42)).
  // Not used by the recorded run; kept so that the module boundary matches.
  std::vector<std::pair<xy, xy>> list(int samples = 1000);
};

}  // namespace cov
#endif
