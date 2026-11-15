// c-cover.hpp — team C / m2: re-derivation of the covering machine of upstream
// covout.cpp (struct SI, extend, cent, indexed, coverSeeds), behind an explicit
// interface and with the constant set named.
//
// Arithmetic is faithful: same expressions, same order, same intermediate types, same
// libm entry points. Everything that decides the output is integer or a comparison
// against a fixed tolerance; see NOTES.md for the audit of which comparisons carry
// margin (none of them is closer than 1e-6, so byte-identity does not depend on
// last-bit agreement of the interval endpoints — it does depend on the integer tests).
#ifndef C_COVER_HPP
#define C_COVER_HPP
#include "c-seedcore.hpp"

namespace mub {

#if defined(__GNUC__) || defined(__clang__)
#define MUB_AI __attribute__((always_inline)) inline
#else
#define MUB_AI inline
#endif

// A cell together with the interval it admits for the shared shift, and the 2x5 matrix
// of tab values at its bins.  covout.cpp:8.
struct SI {
  xy p;
  double lo = 0., hi = 0.;
  double J[2][5] = {};
};

// extend: compute [lo,hi] for cell p whose distinguished coordinate sits at index s.
// err = pi*(w/4)*5  (covout.cpp:12).  The argument of `clip` is one half-plane normal
// in the (cos,sin) frame of the shift; the residual sums the *other* four bins' taps at
// half weight.  Tolerances: (r+1e-7)/|a| and +-1e-5.  covout.cpp:9-25.
inline SI extend(const xy& p, int s, const Lattice& L) {
  SI o{}; o.p = p;
  for (int a = 0; a < 2; a++)
    for (int j = 0; j < 5; j++) o.J[a][j] = L.tab[p.b[j]][a];
  double err = pi * (L.w / 4) * 5.;
  o.lo = -.5; o.hi = .5;
  auto clip = [&](double x, double y) {
    double v = (x * p.c[0] + y * p.c[1]) * L.n,
           a = x * o.J[0][s] + y * o.J[1][s];
    if (std::abs(a) < 1e-6) return;
    double r = hp(x, y) * err;
    for (int j = 0; j < 5; j++)
      if (j != s) r += .5 * std::abs(x * o.J[0][j] + y * o.J[1][j]);
    double mid = -v / a;
    r = (r + 1e-7) / std::abs(a);
    o.lo = std::max(o.lo, mid - r - 1e-5);
    o.hi = std::min(o.hi, mid + r + 1e-5);
  };
  clip(o.J[0][s], o.J[1][s]);
  for (int j = 0; j < 5; j++)
    if (j != s) clip(-o.J[1][j], o.J[0][j]);
  return o;
}

// A centre: index of the A cell and the four free bins of the B cell.  covout.cpp:26.
struct cent { int ix; std::array<int, 4> y{}; };

// A B cell packed for the bucket structure: the five A-B bin differences, the free bins,
// and the squared / absolute bin distance.  covout.cpp:28.
struct indexed {
  std::array<int8_t, 5> k{};
  std::array<int, 4> y{};
  int xsq = 0, xab = 0;
};

inline int sq(int x) { return x * x; }

// ---- the covering machine ---------------------------------------------------
// Parameters of the recorded run: run(S, .032, 2)  (covout.cpp:140), giving
//   RN2 = (R*n)^2 - 1e-4 = 12.844956000000002
//   T   = (sqrt(RN2)+1.5)^2 = 25.84691414723998, int(T) = 25
//   K   = max(1, int(R*n+.51)) = 4,  m = ceil(n/K) = 28
// See NOTES.md F1: the frozen spec's "K=3, m=38" is arithmetically inconsistent with
// these expressions; 4 and 28 are what the published code computes.
struct Options {
  double R = .032;      // cover radius in units of the bin spacing (covout.cpp:140)
  int dual = 2;         // number of dual (weighted least squares) iterations
  int K = -1;           // bucket width in bins; -1 = derive as upstream
  int m = -1;           // buckets per axis;     -1 = derive as upstream
  bool cheap_accept = true;    // enable the L2 short-circuit testBucket:82
  bool cheap_prefilter = true; // enable the "s-a > RN2" skip of the LP, testBucket:83
  bool filter_gap = true;      // enable the gap filter of run:122
  bool filter_interval = true; // enable the interval-overlap filter of run:123
};

struct coverSeeds {
  // geometry
  int n = 0;
  double w = 0.;
  // parameters
  int K = 0, m = 0, dual = 0;
  double R = 0., RN2 = 0., T = 0.;
  // data
  std::vector<SI> X;
  std::vector<std::vector<SI>> Y;
  std::vector<std::vector<cent>> byX;
  std::vector<cent> all;
  std::vector<std::vector<indexed>> buckets;
  // counters, in the order covrun prints them (covout.cpp:132)
  uint64_t checked = 0, ncover = 0, ncheap = 0, nlp = 0, nvisit = 0;
  // extra accounting (not printed by covrun; printed on an `extra` line)
  uint64_t nlp_ok = 0, drop_gap = 0, drop_interval = 0;

  // supdual: a two-step weighted least-squares solve of the dual of the 4-variable
  // interval LP, returning a certified upper bound on the largest squared distance
  // reachable by the pair (A,B) with bin-difference vector k.  Rows 0..4 carry A's
  // five bins in the (cos,sin) columns 0,1; row s additionally carries B's bin 0 in
  // columns 2,3 (the shared bin); rows 5..8 carry B's bins 1..4.  err = 1.251*pi*w
  // (covout.cpp:47) is the per-bin phase error.  covout.cpp:40-72.
  // MUB_AI: force inlining. Semantic no-op (no reassociation, no contraction); it makes
  // the hot loop match the published build's code shape. The published covrun has no
  // out-of-line supdual symbol at all; leaving this out costs 2.0x wall clock.
  static MUB_AI double supdual(const std::array<int, 9>& k, const SI& A, const SI& B,
                               int iters, int n_, double w_) {
    int s = A.p.s;
    double rows[9][4] = {};
    for (int j = 0; j < 5; j++) { rows[j][0] = A.J[0][j]; rows[j][1] = A.J[1][j]; }
    for (int j = 0; j < 5; j++) {
      int h = j ? 4 + j : s;
      rows[h][2] = B.J[0][j]; rows[h][3] = B.J[1][j];
    }
    double rhs[4] = {-n_ * A.p.c[0], -n_ * A.p.c[1], -n_ * B.p.c[0], -n_ * B.p.c[1]};
    double err = 1.251 * pi * w_;
    double y[4] = {}, reg[2] = {.2, .2}, ww[9] = {1., 1., 1., 1., 1., 1., 1., 1., 1.};
    double best = 1e10;
    for (int loop = 0; loop < iters; loop++) {
      double M[4][4] = {}, v[4] = {};
      for (int j = 0; j < 9; j++)
        for (int a = 0; a < 4; a++) {
          double p = rows[j][a] * ww[j];
          v[a] += p * k[j];
          for (int b = 0; b < a + 1; b++) M[a][b] += p * rows[j][b];
        }
      for (int a = 0; a < 4; a++) { M[a][a] += reg[a / 2]; v[a] -= 2 * rhs[a]; }
      double D[4];
      for (int i = 0; i < 4; i++) {
        D[i] = 1. / M[i][i];
        for (int j = i + 1; j < 4; j++) {
          double l = M[j][i] * D[i];
          for (int b = j; b < 4; b++) M[b][j] -= l * M[b][i];
          v[j] -= l * v[i];
        }
        v[i] *= D[i];
      }
      for (int j = 3; j > 0; j--)
        for (int i = 0; i < j; i++) v[i] -= M[j][i] * D[i] * v[j];
      bool usable = true;
      for (int a = 0; a < 4; a++) if (!(std::abs(v[a]) <= 1e4)) usable = false;
      if (!usable) break;
      double u = 0;
      for (int a = 0; a < 4; a++) u += 2 * v[a] * rhs[a];
      for (int e = 0; e < 2; e++) {
        double q = hp(v[2 * e], v[2 * e + 1]);
        u += 2 * err * q;
        reg[e] = 2 * err / std::max(.02, q);
      }
      for (int j = 0; j < 9; j++) {
        double z = k[j];
        for (int a = 0; a < 4; a++) z -= rows[j][a] * v[a];
        u += std::abs(z);
        ww[j] = 1. / std::max(std::abs(z), .03);
      }
      best = std::min(best, u);
    }
    return best + .01;
  }

  // testBucket: scan one bucket pool for a stored centre that certifies (A,B) covered.
  //   s = |k_A|^2 + |k_y|^2 must be <= int(T)                       (covout.cpp:78-79)
  //   a = |k_A|_1 + |k_y|_1
  //   cheap: s + a + 2.25 < RN2  => covered                          (covout.cpp:82)
  //   LP:    s - a > RN2         => cannot be covered, skip          (covout.cpp:83)
  //          s + 2.25 + supdual(...) < RN2 => covered                (covout.cpp:85)
  bool testBucket(const std::vector<indexed>& pool, const SI& A, const SI& B,
                  const Options& opt) {
    const ar& y = B.p.b;
    nvisit += pool.size();
    for (const auto& e : pool) {
      std::array<int, 9> k = {e.k[0], e.k[1], e.k[2], e.k[3], e.k[4],
                              y[1] - e.y[0], y[2] - e.y[1], y[3] - e.y[2], y[4] - e.y[3]};
      int s = e.xsq + sq(k[5]) + sq(k[6]) + sq(k[7]) + sq(k[8]);
      if (s > int(T)) continue;
      ncover++;
      int a = e.xab + std::abs(k[5]) + std::abs(k[6]) + std::abs(k[7]) + std::abs(k[8]);
      if (opt.cheap_accept && s + a + 2.25 < RN2) { ncheap++; return true; }
      if (!dual || (opt.cheap_prefilter && s - a > RN2)) continue;
      nlp++;
      if (s + 2.25 + supdual(k, A, B, dual, n, w) < RN2) { nlp_ok++; return true; }
    }
    return false;
  }

  // covered: 27 buckets around B's (b1,b2,b3), restricted to the sorted upper triangle
  // because B's free bins are ascending.  covout.cpp:89-95.
  bool covered(const SI& A, const SI& B, const Options& opt) {
    int a = B.p.b[1] / K, b = B.p.b[2] / K, c = B.p.b[3] / K;
    for (int i = std::max(0, a - 1); i <= std::min(m - 1, a + 1); i++)
      for (int j = std::max(i, b - 1); j <= std::min(m - 1, b + 1); j++)
        for (int l = std::max(j, c - 1); l <= std::min(m - 1, c + 1); l++)
          if (testBucket(buckets[(i * m + j) * m + l], A, B, opt)) return true;
    return false;
  }

  // insert: file a packed centre under the bucket of its (y0,y1,y2).  covout.cpp:96-98.
  void insert(const indexed& u) {
    int i = u.y[0] / K, j = u.y[1] / K, k = u.y[2] / K;
    buckets[(i * m + j) * m + k].push_back(u);
  }

  // run: fix the parameters, extend every seed, then sweep t ascending; each surviving
  // cell is appended to `all` and to byX[t] and immediately becomes a covering centre.
  // covout.cpp:99-133.  tmax >= 0 stops the sweep early (harness option for prefix
  // runs; the published run uses tmax < 0, i.e. the whole sweep).
  void run(const Seeds& S, const Options& opt, long tmax = -1, bool reset = true) {
    n = S.L.n; w = S.L.w;
    R = opt.R; dual = opt.dual;
    RN2 = square_pow(R * n) - .0001;                 // covout.cpp:100
    T = square_pow(std::sqrt(RN2) + 1.5);            // covout.cpp:101
    K = opt.K >= 0 ? opt.K : std::max(1, int(R * n + .51));
    m = opt.m >= 0 ? opt.m : (n + K - 1) / K;        // covout.cpp:102-103
    buckets.assign(size_t(m) * m * m, {});
    if (reset) { X.clear(); Y.clear(); byX.clear(); all.clear(); }
    X.reserve(S.xs.size());
    for (const auto& p : S.xs) X.push_back(extend(p, p.s, S.L));
    Y.resize(n);
    for (int i = 0; i < n; i++)
      for (const auto& p : S.ys[i]) Y[i].push_back(extend(p, 0, S.L));
    byX.resize(X.size());
    size_t tstop = tmax < 0 ? X.size() : std::min<size_t>(X.size(), size_t(tmax));
    for (size_t t = 0; t < tstop; t++) {
      const SI& A = X[t];
      for (auto& L : buckets) L.clear();
      for (size_t h = 0; h < t; h++) {
        const xy& p = X[h].p;
        if (p.s != A.p.s) continue;
        indexed u{};
        int s = 0, ab = 0;
        for (int j = 0; j < 5; j++) {
          int k = A.p.b[j] - p.b[j];
          u.k[j] = int8_t(k); s += sq(k); ab += std::abs(k);
        }
        u.xsq = s; u.xab = ab;
        if (s > int(T) || s - ab > RN2) continue;    // covout.cpp:118
        for (const auto& c : byX[h]) { u.y = c.y; insert(u); }
      }
      for (const auto& B : Y[A.p.b[A.p.s]]) {
        if (opt.filter_gap && B.p.g + 1e-8 < 1. - (A.p.b[4] + 2) * w) { drop_gap++; continue; }
        if (opt.filter_interval && (B.hi < A.lo || B.lo > A.hi)) { drop_interval++; continue; }
        checked++;
        if (covered(A, B, opt)) continue;
        cent c{int(t), {B.p.b[1], B.p.b[2], B.p.b[3], B.p.b[4]}};
        all.push_back(c); byX[t].push_back(c);
        indexed u{}; u.y = c.y; insert(u);
      }
    }
  }

  // writeCenters: the exact recorded format.  covout.cpp:141.
  //   "%d %d %d %d %d %d %d %d %d %d \n" per centre, header "%d %zu\n".
  bool writeCenters(const char* path) const {
    FILE* f = fopen(path, "w");
    if (!f) return false;
    fprintf(f, "%d %zu\n", n, all.size());
    for (const auto& u : all) {
      const auto& p = X[u.ix].p;
      for (int b : p.b) fprintf(f, "%d ", b);
      fprintf(f, "%d ", p.s);
      for (int b : u.y) fprintf(f, "%d ", b);
      fprintf(f, "\n");
    }
    if (ferror(f) || fclose(f) != 0) return false;
    return true;
  }
};

}  // namespace mub
#endif
