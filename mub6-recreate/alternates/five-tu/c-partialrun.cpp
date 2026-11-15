// c-partialrun.cpp -- development driver (deviation D-1 in NOTES.md).
//   c-partialrun <out> <tlimit>
// Same pipeline as covrun but stops the seed loop after <tlimit> seeds, so that the
// resulting (short) file must be a byte-exact prefix of centers.txt.  Costs seconds
// instead of the 6m41s full run; the frozen interface never uses it.
#include <cstdio>
#include <cstdlib>

#include "c-cover.hpp"
#include "c-writer.hpp"

int main(int argc, char** argv) {
  cov::environment();
  if (argc != 3) abort();
  size_t lim = strtoul(argv[2], nullptr, 10);
  cov::seeds S;
  S.build(112);
  printf("xs%zu\n", S.xs.size());
  cov::coverSeeds C;
  C.run(S, .032, 2, lim);
  cov::writeCenters(argv[1], cov::n, C.X, C.all);
  return 0;
}
