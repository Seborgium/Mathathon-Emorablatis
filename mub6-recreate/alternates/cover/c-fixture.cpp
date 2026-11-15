// c-fixture.cpp — bit-level fixture. Compiles the *published* sources into this
// translation unit (upstream main renamed away) and compares them, field by field and
// bit by bit, against the re-derived module c-cover.hpp / c-seedcore.hpp.
//
// This is the unit-level acceptance test of the cover direction: it proves that the
// re-derived module agrees with the published implementation on
//   (a) the whole seed family set (every xs cell, every ys[a] cell, in order),
//   (b) the extend() interval endpoints and J matrices on samples,
//   (c) the parameter expressions RN2, T, K, m and int(T),
//   (d) supdual() on sample bin-difference vectors,
// before the expensive whole-file comparison is attempted.
//
// The published include is read-only; nothing under .scratch/gh/upstream is modified.
#define main upstream_covout_main
#include "../../../.scratch/gh/upstream/covout.cpp"
#undef main
#include "c-cover.hpp"
#include <cstring>

static int fails = 0, checks = 0;

static void ck(bool ok, const char* what, long long a = 0, long long b = 0) {
  checks++;
  if (!ok) { fails++; printf("FAIL %s  %lld vs %lld\n", what, a, b); }
}
static void ckd(bool ok, const char* what, double a, double b) {
  checks++;
  if (!ok) { fails++; printf("FAIL %s  %.17g vs %.17g\n", what, a, b); }
}
static bool bits(double a, double b) { return std::memcmp(&a, &b, sizeof(double)) == 0; }

int main(int argc, char** argv) {
  int nn = argc > 1 ? atoi(argv[1]) : 112;
  printf("building published seed set n=%d ...\n", nn); fflush(stdout);
  seeds S; S.build(nn);
  printf("building re-derived seed set ...\n"); fflush(stdout);
  mub::Seeds T; T.build(nn);

  ck(S.xs.size() == T.xs.size(), "xs.size", (long long)S.xs.size(), (long long)T.xs.size());
  ck(n == T.L.n, "n", n, T.L.n);
  ckd(bits(w, T.L.w), "w", w, T.L.w);
  ck(tab.size() == T.L.tab.size(), "tab.size", (long long)tab.size(), (long long)T.L.tab.size());
  for (size_t i = 0; i < tab.size() && i < T.L.tab.size(); i++) {
    ckd(bits(tab[i][0], T.L.tab[i][0]), "tab.cos", tab[i][0], T.L.tab[i][0]);
    ckd(bits(tab[i][1], T.L.tab[i][1]), "tab.sin", tab[i][1], T.L.tab[i][1]);
  }

  // (a) every xs cell
  for (size_t i = 0; i < S.xs.size() && i < T.xs.size(); i++) {
    const xy& p = S.xs[i]; const mub::xy& q = T.xs[i];
    for (int j = 0; j < 5; j++) ck(p.b[j] == q.b[j], "xs.b", p.b[j], q.b[j]);
    ck(p.s == q.s, "xs.s", p.s, q.s);
    ckd(bits(p.g, q.g), "xs.g", p.g, q.g);
    ckd(bits(p.c[0], q.c[0]), "xs.c0", p.c[0], q.c[0]);
    ckd(bits(p.c[1], q.c[1]), "xs.c1", p.c[1], q.c[1]);
  }
  // every ys[a] cell, and the per-bin counts (which fix the centre order)
  ck((int)S.ys.size() == (int)T.ys.size(), "ys.size", (long long)S.ys.size(), (long long)T.ys.size());
  size_t ytot = 0, ytot2 = 0;
  for (int a = 0; a < nn; a++) {
    ck(S.ys[a].size() == T.ys[a].size(), "ys.count", (long long)S.ys[a].size(), (long long)T.ys[a].size());
    for (size_t i = 0; i < S.ys[a].size() && i < T.ys[a].size(); i++) {
      const xy& p = S.ys[a][i]; const mub::xy& q = T.ys[a][i];
      for (int j = 0; j < 5; j++) ck(p.b[j] == q.b[j], "ys.b", p.b[j], q.b[j]);
      ck(p.s == q.s, "ys.s", p.s, q.s);
      ckd(bits(p.g, q.g), "ys.g", p.g, q.g);
      ckd(bits(p.c[0], q.c[0]), "ys.c0", p.c[0], q.c[0]);
      ckd(bits(p.c[1], q.c[1]), "ys.c1", p.c[1], q.c[1]);
    }
    ytot += S.ys[a].size(); ytot2 += T.ys[a].size();
  }
  ck(ytot == ytot2, "ys.total", (long long)ytot, (long long)ytot2);

  // (b) extend() on samples: xs with their own s, ys with s=0
  int ns = int(S.xs.size());
  int idx[8] = {0, 1, 2, ns / 2, ns - 3, ns - 2, ns - 1, 12345 % ns};
  for (int k = 0; k < 8; k++) {
    int i = idx[k];
    SI A = extend(S.xs[i], S.xs[i].s);
    mub::SI B = mub::extend(T.xs[i], T.xs[i].s, T.L);
    ckd(bits(A.lo, B.lo), "extend.lo", A.lo, B.lo);
    ckd(bits(A.hi, B.hi), "extend.hi", A.hi, B.hi);
    for (int a2 = 0; a2 < 2; a2++) for (int j = 0; j < 5; j++)
      ckd(bits(A.J[a2][j], B.J[a2][j]), "extend.J", A.J[a2][j], B.J[a2][j]);
  }
  for (int a = 0; a < nn; a += 13) {
    if (S.ys[a].empty()) continue;
    SI A = extend(S.ys[a][0], 0);
    mub::SI B = mub::extend(T.ys[a][0], 0, T.L);
    ckd(bits(A.lo, B.lo), "extendY.lo", A.lo, B.lo);
    ckd(bits(A.hi, B.hi), "extendY.hi", A.hi, B.hi);
  }

  // (c) parameter expressions, spelled exactly as the published lines
  {
    double R = .032;
    double rn2 = sq(1) * pow(R * n, 2) - .0001;
    double TT = pow(sqrt(rn2) + 1.5, 2);
    int K = int(R * n + .51); K = K > 1 ? K : 1;
    int m = (n + K - 1) / K;
    mub::Options opt;
    mub::coverSeeds C;
    C.n = T.L.n; C.w = T.L.w; C.R = opt.R; C.dual = opt.dual;
    C.RN2 = mub::square_pow(C.R * C.n) - .0001;
    C.T = mub::square_pow(std::sqrt(C.RN2) + 1.5);
    C.K = std::max(1, int(C.R * C.n + .51));
    C.m = (C.n + C.K - 1) / C.K;
    ckd(bits(rn2, C.RN2), "RN2", rn2, C.RN2);
    ckd(bits(TT, C.T), "T", TT, C.T);
    ck(K == C.K, "K", K, C.K);
    ck(m == C.m, "m", m, C.m);
    ck(int(TT) == int(C.T), "int(T)", int(TT), int(C.T));
    // F2: libm pow(x,2) vs a single multiply at the two published arguments
    ckd(bits(pow(R * n, 2), mub::square_mul(R * n)), "pow-fold R*n",
        pow(R * n, 2), mub::square_mul(R * n));
    ckd(bits(pow(sqrt(rn2) + 1.5, 2), mub::square_mul(sqrt(rn2) + 1.5)), "pow-fold sqrt",
        pow(sqrt(rn2) + 1.5, 2), mub::square_mul(sqrt(rn2) + 1.5));
    printf("params RN2=%.17g T=%.17g intT=%d K=%d m=%d\n", rn2, TT, int(TT), K, m);
  }

  // (d) supdual on sample (A,B,k): A from xs, B from Y[A.b[A.s]], k from a real diff
  {
    unsigned long long seed = 12345;
    auto rnd = [&]() { seed = seed * 6364136223846793005ULL + 1442695040888963407ULL; return seed >> 33; };
    int tested = 0;
    for (int rep = 0; rep < 400 && rep < ns; rep++) {
      int t = int(rnd() % ns), h = int(rnd() % ns);
      int bin = S.xs[t].b[S.xs[t].s];
      if (S.ys[bin].empty()) continue;
      int yi = int(rnd() % S.ys[bin].size());
      SI A = extend(S.xs[t], S.xs[t].s), Bs = extend(S.ys[bin][yi], 0);
      mub::SI A2 = mub::extend(T.xs[t], T.xs[t].s, T.L);
      mub::SI B2 = mub::extend(T.ys[bin][yi], 0, T.L);
      std::array<int, 9> k{};
      for (int j = 0; j < 5; j++) k[j] = S.xs[t].b[j] - S.xs[h].b[j];
      for (int j = 0; j < 4; j++) k[5 + j] = S.ys[bin][yi].b[j + 1] - (int)(rnd() % 112);
      double u1 = coverSeeds::supdual(k, A, Bs, 2);
      double u2 = mub::coverSeeds::supdual(k, A2, B2, 2, n, w);
      ckd(bits(u1, u2), "supdual", u1, u2);
      double u3 = coverSeeds::supdual(k, A, Bs, 1), u4 = mub::coverSeeds::supdual(k, A2, B2, 1, n, w);
      ckd(bits(u3, u4), "supdual1", u3, u4);
      double u5 = coverSeeds::supdual(k, A, Bs, 0), u6 = mub::coverSeeds::supdual(k, A2, B2, 0, n, w);
      ckd(bits(u5, u6), "supdual0", u5, u6);
      tested++;
    }
    printf("supdual samples %d\n", tested);
  }

  printf("%s checks=%d fails=%d\n", fails ? "FIXTURE-FAIL" : "FIXTURE-OK", checks, fails);
  return fails ? 1 : 0;
}
