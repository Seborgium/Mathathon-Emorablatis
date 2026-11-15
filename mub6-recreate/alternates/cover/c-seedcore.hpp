// c-seedcore.hpp — team C / m2: re-derivation of the arithmetic + enumeration core of
// upstream seed.cpp, as a module with an explicit interface.
//
// Faithful arithmetic: every expression below is evaluated in the same order, with the
// same intermediate types, as the published source. Where the published code relies on
// <cmath> semantics (nearbyint, sqrt, pow) we call the same libm entry points. The one
// deliberate deviation is `square_pow`/`square_mul`: upstream writes pow(x,2) in
// coverSeeds::run and gcc -O3 does NOT fold it (see NOTES.md, finding F2); both
// spellings are exposed and asserted bit-equal in the unit tests.
#ifndef C_SEEDCORE_HPP
#define C_SEEDCORE_HPP
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <array>
#include <algorithm>
#include <random>
#include <cfenv>
#include <limits>
#include <cstdint>
#include <cstring>
#pragma STDC FENV_ACCESS ON

namespace mub {

// ---- ABI / environment contract (upstream seed.cpp:12-16) -------------------
constexpr double pi = 0x1.921fb54442d18p+1;   // seed.cpp:12

inline void environment() {
  static_assert(std::numeric_limits<double>::is_iec559 &&
                std::numeric_limits<double>::digits == 53, "binary64 required");
  if (fesetround(FE_TONEAREST) != 0 || fegetround() != FE_TONEAREST) std::abort();
}

using ar = std::array<int, 5>;      // five bin indices of a basis
using V  = std::array<double, 2>;   // (cos, sin) of a tab entry

inline double square_pow(double x) { return std::pow(x, 2.0); }  // upstream spelling
inline double square_mul(double x) { return x * x; }             // folded spelling

// expair: exp(2*pi*i*x) by 9-term Taylor on y = (x - k/4)*2*pi, k = nearbyint(4x);
// k mod 4 selects a quarter turn.  seed.cpp:21-31.
inline V expair(double x) {
  if (!(std::abs(x) <= 16.)) return {NAN, NAN};
  int k = int(std::nearbyint(4 * x));
  double y = (x - .25 * k) * (2 * pi), yy = -y * y;
  double a = 1., b = y, ta = 1., tb = y;
  for (int j = 1; j <= 9; j++) {
    ta = (ta * yy) / ((2 * j - 1.) * (2 * j));
    tb = (tb * yy) / ((2 * j) * (2 * j + 1.));
    a += ta; b += tb;
  }
  switch ((k % 4 + 4) % 4) {
    case 0: return {a, b};
    case 1: return {-b, a};
    case 2: return {-a, -b};
    default: return {b, -a};
  }
}

inline double hp(double x, double y) { return std::sqrt(x * x + y * y); }  // seed.cpp:32

// ---- the lattice: n bins, spacing w = 1/n, the table tab --------------------
struct Lattice {
  int n = 0;
  double w = 0.;
  std::vector<V> tab;
  void init(int nn) {
    n = nn; w = 1. / n; tab.clear(); tab.reserve(nn);
    for (int i = 0; i < n; i++) tab.push_back(expair((i + .5) / n));
  }
};

// A cell: five bins, a distinguished index s, a gap g and the centre c[2].
// seed.cpp:33.
struct xy {
  ar b{};
  int s = 0;
  double g = 0., c[2] = {0., 0.};
};

// sumok: is the cell's centre c[2] consistent with all five bins under the interval
// arithmetic?  err = pi*(w*w/4)*5  (seed.cpp:41); tolerance 1e-8 per half-plane test.
inline bool sumok(xy& p, const Lattice& L) {
  double c[2] = {0., -1. / (2 * pi)};
  for (auto b : p.b) {
    c[0] += L.tab[b][1] / (2 * pi);
    c[1] -= L.tab[b][0] / (2 * pi);
  }
  p.c[0] = c[0]; p.c[1] = c[1];
  double err = pi * (L.w * L.w / 4) * 5.;
  auto chk = [&](double x, double y) {
    double l = std::abs(x * c[0] + y * c[1]), r = hp(x, y) * err;
    for (auto b : p.b) r += (L.w / 2) * std::abs(x * L.tab[b][0] + y * L.tab[b][1]);
    return !(l > r + 1e-8);
  };
  if (!chk(c[0], c[1])) return false;
  for (auto b : p.b)
    if (!chk(-L.tab[b][1], L.tab[b][0])) return false;
  return true;
}

// mk: build a cell from five bins. s = argmin |2b+1-n| with strict < over a scan of the
// unpassed order (p.s starts at 0); g = minimal gap of the bin set including both
// boundary gaps, in units of bins, scaled by w.  seed.cpp:74-82.
inline xy mk(ar b, bool sorted, const Lattice& L) {
  xy p{}; p.b = b;
  for (int j = 0; j < 5; j++)
    if (std::abs(b[j] * 2 + 1 - L.n) < std::abs(b[p.s] * 2 + 1 - L.n)) p.s = j;
  if (!sorted) std::sort(b.begin(), b.end());
  p.g = .5 * std::max(2 * b[0] + 1, 2 * L.n - (2 * b[4] + 1));
  for (int j = 0; j < 4; j++) p.g = std::max(p.g, double(b[j + 1] - b[j]));
  p.g *= L.w;
  return p;
}

// The two seed families. xs = "A" cells (bins ascending, s = middle index);
// ys[a] = "B" cells (a = free first bin, bins 1..4 ascending), in enumeration order.
// That order is what fixes the centre index t; see NOTES.md (D1..D4).
struct Seeds {
  Lattice L;
  std::vector<xy> xs;
  std::vector<std::vector<xy>> ys;
  void build(int nn) {
    L.init(nn);
    // xs: e ascending, then d<e, c<d, b<c, a<b  (seed.cpp:85-90)
    for (int e = 0; e < L.n; e++)
      for (int d = 0; d < e + 1; d++)
        for (int c = 0; c < d + 1; c++)
          for (int b = 0; b < c + 1; b++)
            for (int a = 0; a < b + 1; a++) {
              if (a > e - d + 1) continue;                    // seed.cpp:86
              xy p = mk({a, b, c, d, e}, true, L);
              if (p.g > 1. - (e - 1) * L.w + 1e-8) continue;  // seed.cpp:88
              if (sumok(p, L)) xs.push_back(p);
            }
    // ys: a free, then e ascending, d<e, c<d, b<c  (seed.cpp:92-95)
    ys.resize(L.n);
    for (int a = 0; a < L.n; a++)
      for (int e = 0; e < L.n; e++)
        for (int d = 0; d < e + 1; d++)
          for (int c = 0; c < d + 1; c++)
            for (int b = 0; b < c + 1; b++) {
              xy p = mk({a, b, c, d, e}, false, L);
              if (sumok(p, L)) ys[a].push_back(p);
            }
  }
};

}  // namespace mub
#endif
