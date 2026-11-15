// c-fp.hpp -- binary64 arithmetic core of the published seed.cpp, re-derived.
//
// Provenance: transcribed from the published seed.cpp (cached at
// .scratch/gh/upstream/seed.cpp, 119 lines, md5 c26dc3e9c5a6903e600275b07c6281ac).
// Every expression below has the same operand order and the same association as
// the published line quoted in the comment above it; -ffp-contract=off and the
// absence of -ffast-math make the result bit-identical.  Do not "tidy" these
// expressions: (w*w/4)*pi and (w/4)*pi are different roundings.
#pragma STDC FENV_ACCESS ON
#ifndef C_FP_HPP
#define C_FP_HPP
#include <cfenv>
#include <cmath>
#include <cstdlib>
#include <limits>

#ifndef F
#define F(i, n) for (int i = 0; i < int(n); ++i)
#endif

namespace cov {

// seed.cpp:11  const double pi=0x1.921fb54442d18p+1;
// The binary64 value of pi, written as a hex literal so that the compiler does
// not have to round a decimal spelling.
const double pi = 0x1.921fb54442d18p+1;

// seed.cpp:12-16  environment(): assert round-to-nearest, or abort.
inline void environment() {
  static_assert(std::numeric_limits<double>::is_iec559 && std::numeric_limits<double>::digits == 53,
                "binary64 required");
  if (fesetround(FE_TONEAREST) != 0 || fegetround() != FE_TONEAREST) abort();
}

using V = std::array<double, 2>;

// seed.cpp:22-34  expair: e^{i*x} by a 9-term Taylor pair after range reduction
// to |y| <= pi/8, with the quadrant restored by k = nearbyint(4x).
inline V expair(double x) {
  if (!(std::abs(x) <= 16.)) return {NAN, NAN};
  int k = int(std::nearbyint(4 * x));
  double y = (x - .25 * k) * (2 * pi), yy = -y * y;
  double a = 1., b = y, ta = 1., tb = y;
  for (int j = 1; j <= 9; j++) {
    ta = (ta * yy) / ((2 * j - 1.) * (2 * j));
    tb = (tb * yy) / ((2 * j) * (2 * j + 1.));
    a += ta;
    b += tb;
  }
  switch ((k % 4 + 4) % 4) {
    case 0: return {a, b};
    case 1: return {-b, a};
    case 2: return {-a, -b};
    default: return {b, -a};
  }
}

// seed.cpp:35  hp: the Euclidean norm of the pair used as a test direction.
inline double hp(double x, double y) { return std::sqrt(x * x + y * y); }

}  // namespace cov
#endif
