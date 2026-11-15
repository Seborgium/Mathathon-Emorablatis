// c-covrun.cpp — faithful driver for the cover: the covrun program contract of
// spec/interfaces.md §2 ("covrun <out>", argc == 2), same stdout lines as
// upstream covout.cpp:135-143.
//
// Deviations: none in behaviour. The unit is header-only (c-cover.hpp); this TU is the
// only place with main, so the module boundary of spec §6 is preserved.
#include "c-cover.hpp"
#include <chrono>

int main(int argc, char** argv) {
  mub::environment();
  if (argc != 2) abort();
  auto st = std::chrono::steady_clock::now();
  mub::Seeds S; S.build(112);
  printf("xs%zu build%.2f\n", S.xs.size(),
         std::chrono::duration<double>(std::chrono::steady_clock::now() - st).count());
  mub::coverSeeds C;
  mub::Options opt;                       // R=.032, dual=2, upstream bucket derivation
  C.run(S, opt);
  if (!C.writeCenters(argv[1])) abort();
  printf("N%d r%.4f dual%d checked%lu centers%zu visit%lu near%lu cheap%lu lp%lu\n",
         C.n, C.R, C.dual, (unsigned long)C.checked, C.all.size(),
         (unsigned long)C.nvisit, (unsigned long)C.ncover, (unsigned long)C.ncheap,
         (unsigned long)C.nlp);
  printf("time %.2f\n",
         std::chrono::duration<double>(std::chrono::steady_clock::now() - st).count());
  return 0;
}
