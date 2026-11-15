// oracle_probe.cpp -- instrumented build of the PUBLISHED seed.cpp.
// seed_orig.cpp is a byte-for-byte copy of .scratch/gh/upstream/seed.cpp
// (sha256 3c6c7a70...); it is included, never edited, exactly as covout.cpp
// includes it (with its guard HEADER defined, which suppresses its main).
// This program is the oracle for test/mine_dump.cpp.  It is not a deliverable
// of the unit: it exists so the comparison is against the published code and
// not against a second copy of my own reasoning.
#define HEADER
#include "seed_orig.cpp"
#include "dump_common.h"

int main() {
  environment();
  seeds S;
  S.build(112);
  printf("format 1\n");
  printf("n %d\n", n);
  printf("w %a\n", w);
  printf("pi %a\n", pi);
  printf("xs %zu\n", S.xs.size());
  printf("tab\n");
  for (int i = 0; i < n; ++i) printf("%d %a %a\n", i, tab[i][0], tab[i][1]);
  printf("xs\n");
  for (const auto& p : S.xs) dump_seed(p);
  printf("ys\n");
  for (int a = 0; a < n; ++a) {
    printf("a %d %zu\n", a, S.ys[a].size());
    for (const auto& p : S.ys[a]) dump_seed(p);
  }
  return 0;
}
