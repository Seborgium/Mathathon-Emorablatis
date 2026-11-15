// seed_arith.cpp -- see seed_arith.hpp for the line-by-line provenance.
// Every floating-point expression below is transcribed with its published
// association and its published operation (no reciprocal substitution, no
// reassociation); the build uses -O3 -march=native -ffp-contract=off exactly as
// build.sh does.
#include "seed_arith.hpp"

#include <cfenv>
#include <cmath>
#include <cstdlib>
#include <limits>

namespace mub {
namespace seedc {

void environment() {
  // seed.cpp:14-15
  static_assert(std::numeric_limits<double>::is_iec559 &&
                    std::numeric_limits<double>::digits == 53,
                "binary64 required");
  if (fesetround(FE_TONEAREST) != 0 || fegetround() != FE_TONEAREST) abort();
}

V expair(double x) {
  // seed.cpp:22
  if (!(std::abs(x) <= 16.)) return V{NAN, NAN};
  // seed.cpp:23-25
  const int k = int(std::nearbyint(4 * x));
  const double y = (x - .25 * k) * (2 * pi);
  const double yy = -y * y;
  // seed.cpp:26-29.  Two tails of the same recurrence, interleaved; the
  // interleaving is part of the published text and is kept.
  double a = 1., b = y, ta = 1., tb = y;
  for (int j = 1; j <= 9; j++) {
    ta = (ta * yy) / ((2 * j - 1.) * (2 * j));
    tb = (tb * yy) / ((2 * j) * (2 * j + 1.));
    a += ta;
    b += tb;
  }
  // seed.cpp:30
  switch ((k % 4 + 4) % 4) {
    case 0: return {a, b};
    case 1: return {-b, a};
    case 2: return {-a, -b};
    default: return {b, -a};
  }
}

double hp(double x, double y) { return std::sqrt(x * x + y * y); }  // seed.cpp:32

void Table::build(int nn) {
  // seed.cpp:84
  n = nn;
  w = 1. / n;
  tab.clear();
  for (int i = 0; i < n; ++i) tab.push_back(expair((i + .5) / n));
}

bool sumok(XY& p, const Table& t) {
  const std::vector<V>& tab = t.tab;
  const double w = t.w;
  // seed.cpp:36-40.  c[1] starts at -1/(2*pi): a division, not a reciprocal.
  double c[2] = {0., -1. / (2 * pi)};
  for (auto b : p.b) {
    c[0] += tab[b][1] / (2 * pi);
    c[1] -= tab[b][0] / (2 * pi);
  }
  p.c[0] = c[0];
  p.c[1] = c[1];
  // seed.cpp:41.  ((pi*(w*w/4))*5): keep the association, and keep w*w/4 as a
  // division by 4 rather than a multiply by .25.
  const double err = pi * (w * w / 4) * 5.;
  // seed.cpp:43-47.  !(l > r+1e-8) rather than l <= r+1e-8: the published form
  // accepts when the comparison is unordered (NaN), the rewritten form does
  // not.  Not interchangeable.
  auto chk = [&](double x, double y) {
    double l = std::abs(x * c[0] + y * c[1]), r = hp(x, y) * err;
    for (auto b : p.b) r += (w / 2) * std::abs(x * tab[b][0] + y * tab[b][1]);
    return !(l > r + 1e-8);
  };
  if (!chk(c[0], c[1])) return false;
  // seed.cpp:49.  One test per bin, with the inward normal (-Im, Re).
  for (auto b : p.b)
    if (!chk(-tab[b][1], tab[b][0])) return false;
  return true;
}

}  // namespace seedc
}  // namespace mub
