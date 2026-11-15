// mine_dump.cpp -- driver for the modular arithmetic core (arith/seed_arith.*).
// Output format is test/dump_common.h and matches test/oracle_probe.cpp line by
// line; test/run_all.sh compares the two files with cmp, byte for byte.
//
// The enumeration loops and seeds::mk below are transcribed from seed.cpp:74-96
// ONLY so that the two dumps can be aligned entry by entry.  They are a test
// scaffold, not part of the unit: enumeration, ordering and the index t belong
// to swarm direction d2, and no claim made here rests on the scaffold except
// "it visits the same (b,s,g) in the same order as the published code".
#include <algorithm>
#include <cstdio>
#include <cmath>

#include "../arith/seed_arith.hpp"
#include "dump_common.h"

using namespace mub::seedc;

namespace {

struct Seeds {
  std::vector<XY> xs;
  std::vector<std::vector<XY>> ys;

  // seed.cpp:74-82.  CAREFUL: `sorted` does not touch p.b -- p.b was already
  // assigned from the argument.  It decides whether the LOCAL copy b (the one
  // g is computed from) is sorted first, so mk(t,false).g is the gap of the
  // sorted tuple while mk(t,true).g is the gap of the tuple as given.  The xs
  // loop passes ascending tuples (a<=b<=c<=d<=e) so the two agree there; the ys
  // loop passes (a,b,c,d,e) with a outside the chain, so they do not.
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

  // seed.cpp:83-96
  void build(int nn, const Table& t) {
    for (int e = 0; e < nn; ++e)
      for (int d = 0; d <= e; ++d)
        for (int c = 0; c <= d; ++c)
          for (int b = 0; b <= c; ++b)
            for (int a = 0; a <= b; ++a) {
              if (a > e - d + 1) continue;
              XY p = mk(ar{a, b, c, d, e}, true, t);
              if (p.g > 1. - (e - 1) * t.w + 1e-8) continue;
              if (sumok(p, t)) xs.push_back(p);
            }
    ys.resize(nn);
    for (int a = 0; a < nn; ++a)
      for (int e = 0; e < nn; ++e)
        for (int d = 0; d <= e; ++d)
          for (int c = 0; c <= d; ++c)
            for (int b = 0; b <= c; ++b) {
              XY p = mk(ar{a, b, c, d, e}, false, t);
              if (sumok(p, t)) ys[a].push_back(p);
            }
  }
};

}  // namespace

int main() {
  environment();
  Table t;
  t.build(112);
  Seeds S;
  S.build(112, t);
  std::printf("format 1\n");
  std::printf("n %d\n", t.n);
  std::printf("w %a\n", t.w);
  std::printf("pi %a\n", pi);
  std::printf("xs %zu\n", S.xs.size());
  std::printf("tab\n");
  for (int i = 0; i < t.n; ++i)
    std::printf("%d %a %a\n", i, t.tab[i][0], t.tab[i][1]);
  std::printf("xs\n");
  for (const auto& p : S.xs) dump_seed(p);
  std::printf("ys\n");
  for (int a = 0; a < t.n; ++a) {
    std::printf("a %d %zu\n", a, S.ys[a].size());
    for (const auto& p : S.ys[a]) dump_seed(p);
  }
  return 0;
}
