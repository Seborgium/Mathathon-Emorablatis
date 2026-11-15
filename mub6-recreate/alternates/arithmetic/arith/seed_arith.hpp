// seed_arith.hpp -- modular re-derivation of the numeric core of the published
// seed.cpp (verification/saved-run/seed.cpp, 119 lines,
// sha256 3c6c7a7092230de231fdb23b6d1782de0dd9ef6689095763b875d90ce5ddeb44).
// Every "seed.cpp:N" citation below is a line of that file as cached at
// .scratch/gh/upstream/seed.cpp and copied verbatim to test/seed_orig.cpp.
//
// Scope of this unit (swarm direction d1): pi, environment, expair, hp, tab,
// n, w, and the interval acceptance test sumok.  The enumeration (seed.cpp:74-96,
// seeds::mk/seeds::build) and the serialisation are NOT part of this unit; the
// test driver transcribes them only so that the two dumps line up entry by
// entry.  See NOTES.md.
#ifndef MUB_SEED_ARITH_HPP
#define MUB_SEED_ARITH_HPP
#include <array>
#include <vector>

namespace mub {
namespace seedc {

using V = std::array<double, 2>;   // a complex number, re/im
using ar = std::array<int, 5>;     // five bins; ascending where the caller
                                   // guarantees it (seed.cpp:19)

// seed.cpp:12.  The binary64 value of pi, written as a hex literal so that no
// decimal-to-binary conversion is involved.  (interfaces.md section 4, last row.)
inline constexpr double pi = 0x1.921fb54442d18p+1;

// seed.cpp:13-16.  Must run before any arithmetic; asserts binary64 and
// round-to-nearest, aborts otherwise.
void environment();

// seed.cpp:21-31.  exp(2*pi*i*x) by reduction to [-1/8,1/8] plus two degree-19
// Taylor tails; returns {NAN,NAN} outside |x| <= 16.
V expair(double x);

// seed.cpp:32.  Modulus.  Not hypot(): the published form sqrt(x*x+y*y) is what
// the error bounds were computed with, and hypot() is a different (more
// accurate) function, so it must not be substituted.
double hp(double x, double y);

// seed.cpp:33.  One seed: bins, the index of the widest bin (the "free"
// coordinate s), the gap g, and the cached centre c computed by sumok.
struct XY {
  ar b{};
  int s = 0;
  double g = 0.;
  double c[2] = {0., 0.};
};

// seed.cpp:34.  n, w = 1/n, and tab[i] = expair((i+.5)/n), i < n.
struct Table {
  int n = 0;
  double w = 0.;
  std::vector<V> tab;
  void build(int nn);
};

// seed.cpp:35-51.  Fills p.c[0..1] and returns whether the box for p is
// accepted.  The error bound is err = pi*(w*w/4)*5.  p.c is written even when
// the answer is false.
bool sumok(XY& p, const Table& t);

}  // namespace seedc
}  // namespace mub
#endif
