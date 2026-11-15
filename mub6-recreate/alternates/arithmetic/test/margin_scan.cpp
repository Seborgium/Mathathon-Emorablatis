// margin_scan.cpp -- how far is every sumok decision from flipping?
//
// sumok accepts iff, for each of its six linear tests, l <= r + 1e-8 (written
// as !(l > r + 1e-8)).  This program repeats the published enumeration
// (seed.cpp:83-96, a test scaffold as in mine_dump.cpp) and, instead of
// short-circuiting, evaluates all six tests of every visited seed and records
// the slack  s = (r + 1e-8) - l.  The decision changes iff some slack changes
// sign; the smallest |s| seen bounds how large a perturbation of the arithmetic
// could be without changing the seed set at all.
//
// This is the determinism evidence for the arithmetic core: it says that the
// accept/reject surface has no knife-edge, so a re-derivation that agrees to a
// few ulp cannot move a seed across it.
#include <algorithm>
#include <cstdint>
#include <cmath>
#include <cstdio>

#include "../arith/seed_arith.hpp"

using namespace mub::seedc;

namespace {
struct Scan {
  const Table& t;
  // thresholds, ascending
  static constexpr int NB = 9;
  static constexpr double band[NB] = {1e-300, 1e-18, 1e-15, 1e-12, 1e-10,
                                      1e-8,   1e-6,  1e-4,  1e99};
  uint64_t below[NB] = {0};
  uint64_t tests = 0, seeds = 0, accepted = 0;
  double worst = 1e300, worst_at = 0., worst_l = 0., worst_r = 0.;
  ar worst_b{};
  int worst_j = -1;
  bool worst_acc = false;

  explicit Scan(const Table& tt) : t(tt) {}

  void note(double slack, const ar& b, int j, bool acc) {
    ++tests;
    double a = std::fabs(slack);
    if (a < worst) { worst = a; worst_at = slack; worst_b = b; worst_j = j; worst_acc = acc; }
    for (int i = 0; i < NB; ++i)
      if (a < band[i]) { ++below[i]; break; }
  }

  // seed.cpp:35-51 with the short-circuit removed and the slack reported.
  bool sumok_scan(XY& p) {
    ++seeds;
    const std::vector<V>& tab = t.tab;
    const double w = t.w;
    double c[2] = {0., -1. / (2 * pi)};
    for (auto b : p.b) {
      c[0] += tab[b][1] / (2 * pi);
      c[1] -= tab[b][0] / (2 * pi);
    }
    p.c[0] = c[0];
    p.c[1] = c[1];
    const double err = pi * (w * w / 4) * 5.;
    auto chk = [&](double x, double y, int j) {
      double l = std::abs(x * c[0] + y * c[1]), r = hp(x, y) * err;
      for (auto b : p.b) r += (w / 2) * std::abs(x * tab[b][0] + y * tab[b][1]);
      note((r + 1e-8) - l, p.b, j, true);
      return !(l > r + 1e-8);
    };
    bool ok = chk(c[0], c[1], 0);
    for (int j = 0; j < 5; ++j) ok = chk(-tab[p.b[j]][1], tab[p.b[j]][0], 1 + j) && ok;
    if (ok) ++accepted;
    return ok;
  }

  static XY mk(ar b, bool sorted, const Table& t) {
    XY p{};
    p.b = b;
    for (int j = 0; j < 5; ++j)
      if (std::abs(b[j] * 2 + 1 - t.n) < std::abs(b[p.s] * 2 + 1 - t.n)) p.s = j;
    if (!sorted) std::sort(b.begin(), b.end());
    p.g = .5 * std::max(2 * b[0] + 1, 2 * t.n - (2 * b[4] + 1));
    for (int j = 0; j < 4; ++j) p.g = std::max(p.g, double(b[j + 1] - b[j]));
    p.g *= t.w;
    return p;
  }

  void run(int nn) {
    for (int e = 0; e < nn; ++e)
      for (int d = 0; d <= e; ++d)
        for (int c = 0; c <= d; ++c)
          for (int b = 0; b <= c; ++b)
            for (int a = 0; a <= b; ++a) {
              if (a > e - d + 1) continue;
              XY p = mk(ar{a, b, c, d, e}, true, t);
              if (p.g > 1. - (e - 1) * t.w + 1e-8) continue;
              sumok_scan(p);
            }
    for (int a = 0; a < nn; ++a)
      for (int e = 0; e < nn; ++e)
        for (int d = 0; d <= e; ++d)
          for (int c = 0; c <= d; ++c)
            for (int b = 0; b <= c; ++b) {
              XY p = mk(ar{a, b, c, d, e}, false, t);
              sumok_scan(p);
            }
  }
};
constexpr double Scan::band[];
}  // namespace

int main() {
  environment();
  Table t;
  t.build(112);
  Scan s(t);
  s.run(112);
  printf("seeds visited (both loops) %llu, accepted %llu, tests %llu\n",
         (unsigned long long)s.seeds, (unsigned long long)s.accepted,
         (unsigned long long)s.tests);
  printf("smallest |slack| over all tests: %.6e\n", s.worst);
  printf("  at seed b=%d,%d,%d,%d,%d test#%d (0=centre, 1..5=normals), slack %a\n",
         s.worst_b[0], s.worst_b[1], s.worst_b[2], s.worst_b[3], s.worst_b[4],
         s.worst_j, s.worst_at);
  printf("counts of tests by |slack| < threshold:\n");
  for (int i = 0; i < Scan::NB; ++i)
    printf("  < %-8.0e : %llu\n", Scan::band[i], (unsigned long long)s.below[i]);
  return 0;
}
