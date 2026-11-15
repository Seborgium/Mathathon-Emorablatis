// c-covrun.cpp -- program `covrun`, frozen interface (spec/interfaces.md §2):
//   covrun <out>   argc == 2, always exits 0 on success.
// Builds seeds::build(112), covers with R = .032 and dual = 2, writes centers.txt.
#include <chrono>
#include <cstdio>

#include "c-cover.hpp"
#include "c-writer.hpp"

int main(int argc, char** argv) {
  cov::environment();
  if (argc != 2) abort();
  auto st = std::chrono::steady_clock::now();
  cov::seeds S;
  S.build(112);
  printf("xs%zu build%.2f\n", S.xs.size(), std::chrono::duration<double>(std::chrono::steady_clock::now() - st).count());
  cov::coverSeeds C;
  C.run(S, .032, 2);
  cov::writeCenters(argv[1], cov::n, C.X, C.all);
  printf("time %.2f\n", std::chrono::duration<double>(std::chrono::steady_clock::now() - st).count());
  return 0;
}
