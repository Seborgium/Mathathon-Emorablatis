// c-writer.cpp -- the byte-exact writer of centers.txt (covout.cpp:172).
#include "c-writer.hpp"

#include <cstdio>
#include <cstdlib>

namespace cov {

void writeCenters(const char* path, int nn, const std::vector<SI>& X, const std::vector<cent>& all) {
  FILE* f = fopen(path, "w");
  if (!f) abort();
  fprintf(f, "%d %zu\n", nn, all.size());
  for (auto u : all) {
    auto& p = X[u.ix].p;
    for (int b : p.b) fprintf(f, "%d ", b);
    fprintf(f, "%d ", p.s);
    for (int b : u.y) fprintf(f, "%d ", b);
    fprintf(f, "\n");
  }
  if (ferror(f) || fclose(f) != 0) abort();
}

}  // namespace cov
