// c-cover.hpp -- the covering machine of the published covout.cpp.
//
// Provenance: covout.cpp lines 6-8 (SI), 9-31 (extend), 32-34 (cent/RX), 35-37
// (indexed/sq), 38-40, 41-45 (coverSeeds data), 46-92 (supdual), 93-113
// (testBucket), 114-122 (covered), 123-126 (insert), 127-169 (run).
//
// A seed X is covered if some already-accepted centre (Y side) lies within the
// Euclidean distance R of it, measured on the projected five-torus in the
// coordinates of the common bin X.b[X.s].  The Bucket grid (K bins per side,
// m cells per side) is only an acceleration: the exact decision is
// testBucket -> supdual (a small dual LP with regularisation), and the radius
// tests use RN2 = (R*n)^2 - 1e-4 and T = (sqrt(RN2) + 1.5)^2.
#ifndef C_COVER_HPP
#define C_COVER_HPP

#include <array>
#include <cstdint>
#include <vector>

#include "c-seed.hpp"

namespace cov {

// covout.cpp:6  struct SI{xy p; double lo,hi; double J[2][5];};
//   lo,hi the allowed interval for the shared coordinate s; J[a][j] = tab[b_j][a].
struct SI {
  xy p;
  double lo, hi;
  double J[2][5];
};

// covout.cpp:9-31.  Intersect the coordinate-s interval with what every other bin
// of the cell allows.  err = pi*(w/4)*5 -- note the different rounding from
// sumok's pi*(w*w/4)*5.
SI extend(xy p, int s);

// covout.cpp:32  struct cent{int ix; i4 y;};
using i4 = std::array<int, 4>;
struct cent {
  int ix;
  i4 y;
};
// covout.cpp:33  struct RX{i4 x; int dummy;};  (declared, never used upstream)
struct RX {
  i4 x;
  int dummy;
};
// covout.cpp:35  struct indexed{array<int8_t,5> k; i4 y; int xsq,xab;};
struct indexed {
  std::array<int8_t, 5> k;
  i4 y;
  int xsq, xab;
};

inline int sq(int x) { return x * x; }

struct coverSeeds {
  int K, m, dual;
  double R, RN2, T;
  std::vector<SI> X;                  // the seeds xs, each extended at its own s
  std::vector<std::vector<SI>> Y;     // Y[a] = ys[a], each extended at s = 0
  std::vector<std::vector<cent>> byX; // centres found so far per seed index
  std::vector<cent> all;              // the output, in (t, position in ys) order
  std::vector<std::vector<indexed>> buckets;
  uint64_t checked = 0, ncover = 0, ncheap = 0, nlp = 0, nvisit = 0;

  // covout.cpp:46-92.  Upper bound on the minimum of
  //   |k_1..4 - A.v|_1 + |k_5..8 - (B.v - A.v)|_1 + 1.251*pi*w*(|A.v| + |B.v|)
  // over v in R^4, by `iters` rounds of an IRLS/dual-LP iteration with
  // regularisation reg = (0.2, 0.2) -> 2*err/max(.02, |v_e|).  The +.01 is slack.
  static double supdual(std::array<int, 9> k, const SI& A, const SI& B, int iters) {
    int s = A.p.s;
    double rows[9][4]{};
    F(j, 5) {
      rows[j][0] = A.J[0][j];
      rows[j][1] = A.J[1][j];
    }
    F(j, 5) {
      int h = j ? 4 + j : s;
      rows[h][2] = B.J[0][j];
      rows[h][3] = B.J[1][j];
    }
    double rhs[4] = {-n * A.p.c[0], -n * A.p.c[1], -n * B.p.c[0], -n * B.p.c[1]};
    double err = 1.251 * pi * w;
    double y[4]{}, reg[2] = {.2, .2}, ww[9] = {1., 1., 1., 1., 1., 1., 1., 1., 1.};
    (void)y;
    double best = 1e10;
    F(loop, iters) {
      double M[4][4]{}, v[4]{};
      F(j, 9) F(a, 4) {
        double p = rows[j][a] * ww[j];
        v[a] += p * k[j];
        F(b, a + 1) M[a][b] += p * rows[j][b];
      }
      F(a, 4) {
        M[a][a] += reg[a / 2];
        v[a] -= 2 * rhs[a];
      }
      double D[4];
      F(i, 4) {
        D[i] = 1. / M[i][i];
        for (int j = i + 1; j < 4; j++) {
          double l = M[j][i] * D[i];
          for (int b = j; b < 4; b++) M[b][j] -= l * M[b][i];
          v[j] -= l * v[i];
        }
        v[i] *= D[i];
      }
      for (int j = 3; j > 0; j--) F(i, j) v[i] -= M[j][i] * D[i] * v[j];
      bool usable = true;
      F(a, 4) if (!(std::abs(v[a]) <= 1e4)) usable = false;
      if (!usable) break;
      double u = 0;
      F(a, 4) u += 2 * v[a] * rhs[a];
      F(e, 2) {
        double q = hp(v[2 * e], v[2 * e + 1]);
        u += 2 * err * q;
        reg[e] = 2 * err / std::max(.02, q);
      }
      F(j, 9) {
        double z = k[j];
        F(a, 4) z -= rows[j][a] * v[a];
        u += std::abs(z);
        ww[j] = 1. / std::max(std::abs(z), .03);
      }
      best = std::min(best, u);
    }
    return best + .01;
  }

  // covout.cpp:93-113.  For every already-accepted centre in the bucket, in stored
  // order: cheap l1 test, then the borderline test, then the dual bound.
  bool testBucket(const std::vector<indexed>& pool, const SI& A, const SI& B) {
    const ar& y = B.p.b;
    nvisit += pool.size();
    for (auto& e : pool) {
      std::array<int, 9> k = {e.k[0], e.k[1], e.k[2], e.k[3], e.k[4], y[1] - e.y[0], y[2] - e.y[1],
                              y[3] - e.y[2], y[4] - e.y[3]};
      int s = e.xsq + sq(k[5]) + sq(k[6]) + sq(k[7]) + sq(k[8]);
      if (s > int(T)) continue;
      ncover++;
      int a = e.xab + std::abs(k[5]) + std::abs(k[6]) + std::abs(k[7]) + std::abs(k[8]);
      if (s + a + 2.25 < RN2) {
        ncheap++;
        return true;
      }
      if (!dual || s - a > RN2) continue;
      nlp++;
      if (s + 2.25 + supdual(k, A, B, dual) < RN2) return true;
    }
    return false;
  }

  // covout.cpp:114-122.  The 27 neighbouring cells of B's bin triple.
  bool covered(const SI& A, const SI& B) {
    int a = B.p.b[1] / K, b = B.p.b[2] / K, c = B.p.b[3] / K;
    for (int i = std::max(0, a - 1); i <= std::min(m - 1, a + 1); i++)
      for (int j = std::max(i, b - 1); j <= std::min(m - 1, b + 1); j++)
        for (int l = std::max(j, c - 1); l <= std::min(m - 1, c + 1); l++)
          if (testBucket(buckets[(i * m + j) * m + l], A, B)) return true;
    return false;
  }

  // covout.cpp:123-126.
  void insert(indexed u) {
    int i = u.y[0] / K, j = u.y[1] / K, k = u.y[2] / K;
    buckets[(i * m + j) * m + k].push_back(u);
  }

  // covout.cpp:127-169.  R = .032, dual = 2 for the recorded run.
  // stopAfter limits the t loop; it exists only so that a development run can be
  // checked against a prefix of centers.txt.  The recorded build always passes the
  // default and is unaffected (see NOTES.md, deviation D-1).
  void run(seeds& S, double r, int d, size_t stopAfter = size_t(-1));
};

}  // namespace cov
#endif
