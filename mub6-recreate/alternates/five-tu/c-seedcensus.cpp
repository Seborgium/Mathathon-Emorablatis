// c-seedcensus.cpp -- development driver: stage-by-stage census of the two
// enumerations of seeds::build, with the surviving xs tuples written to stdout in
// the same text form as c-seeddump, so that the census and the stream are checked
// together.
//   c-seedcensus <n> > xs.txt
#include <cstdio>

#include "c-seed.hpp"

int main(int argc, char** argv) {
  cov::environment();
  int nn = argc > 1 ? atoi(argv[1]) : 112;
  using cov::n; using cov::w; using cov::tab; using cov::xy;
  n = nn;
  w = 1. / n;
  tab.clear();
  F(i, n) tab.push_back(cov::expair((i + .5) / n));
  unsigned long long rawX = 0, afterLow = 0, afterGap = 0, keptX = 0;
  F(e, n) F(d, e + 1) F(c, d + 1) F(b, c + 1) F(a, b + 1) {
    ++rawX;
    if (a > e - d + 1) continue;
    ++afterLow;
    xy p = cov::seeds::mk({a, b, c, d, e}, true);
    if (p.g > 1. - (e - 1) * w + 1e-8) continue;
    ++afterGap;
    if (!cov::sumok(p)) continue;
    ++keptX;
    printf("X %d %d %d %d %d %d %a %a %a\n", p.b[0], p.b[1], p.b[2], p.b[3], p.b[4], p.s, p.g, p.c[0], p.c[1]);
  }
  unsigned long long rawY = 0, keptY = 0;
  F(a, n) F(e, n) F(d, e + 1) F(c, d + 1) F(b, c + 1) {
    ++rawY;
    xy p = cov::seeds::mk({a, b, c, d, e}, false);
    if (cov::sumok(p)) ++keptY;
  }
  fprintf(stderr, "n %d\n", nn);
  fprintf(stderr, "xs candidates %llu  after a<=e-d+1 %llu  after gap %llu  after sumok %llu\n", rawX, afterLow,
          afterGap, keptX);
  fprintf(stderr, "ys candidates %llu  after sumok %llu\n", rawY, keptY);
  return 0;
}
