// c-seeddump.cpp -- development driver (not part of the frozen interface).
//   c-seeddump <n> [dump]
// Prints the enumeration census to stderr and, with `dump`, the whole seed stream
// to stdout in the fixed text form
//   X b0 b1 b2 b3 b4 s g c0 c1
//   Y a b0 b1 b2 b3 b4 s g c0 c1
// with doubles in %a (exact hex).  The same form is emitted by the oracle probe
// probe/c-probe-seed.cpp, so `sha256sum` of the two streams must agree.
#include <cstring>

#include "c-seed.hpp"

int main(int argc, char** argv) {
  cov::environment();
  int nn = argc > 1 ? atoi(argv[1]) : 112;
  bool dump = argc > 2 && !strcmp(argv[2], "dump");
  cov::seeds S;
  S.build(nn);
  size_t tot = 0;
  fprintf(stderr, "n %d xs %zu\n", nn, S.xs.size());
  for (int a = 0; a < nn; ++a) {
    fprintf(stderr, "ys %d %zu\n", a, S.ys[a].size());
    tot += S.ys[a].size();
  }
  fprintf(stderr, "ys total %zu\n", tot);
  if (!dump) return 0;
  for (auto& p : S.xs)
    printf("X %d %d %d %d %d %d %a %a %a\n", p.b[0], p.b[1], p.b[2], p.b[3], p.b[4], p.s, p.g, p.c[0], p.c[1]);
  for (int a = 0; a < nn; ++a)
    for (auto& p : S.ys[a])
      printf("Y %d %d %d %d %d %d %a %a %a\n", a, p.b[0], p.b[1], p.b[2], p.b[3], p.b[4], p.s, p.g, p.c[0],
             p.c[1]);
  return 0;
}
