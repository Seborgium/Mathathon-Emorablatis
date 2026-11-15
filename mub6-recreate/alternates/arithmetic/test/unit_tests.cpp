// unit_tests.cpp -- independent checks of arith/seed_arith.*, i.e. checks that
// do NOT take their expected values from our own code and do not compare
// against the oracle.  The oracle comparison is test/compare.py; this file
// tests properties the published code claims (accuracy, the rounding
// environment, the enclosure bound) using long double as the reference, which
// on x86-64 has a 64-bit significand and is therefore ~2000x finer than the
// 3.1e-4 bound it is used to audit.
//
// Exit status 0 iff every check passes.
#include <cfloat>
#include <cfenv>
#include <cstdint>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <vector>

#include "../arith/seed_arith.hpp"

using namespace mub::seedc;

static int fails = 0;
static void ck(bool cond, const char* what) {
  std::printf("%-58s %s\n", what, cond ? "PASS" : "FAIL");
  if (!cond) ++fails;
}
static double ulp_at(double x) {  // spacing of doubles around x
  return std::nextafter(std::fabs(x), INFINITY) - std::fabs(x);
}
// expair's two components are both in [-1,1] and are frequently very close to
// zero, where a relative (ulp-of-the-result) error is meaningless; the error is
// therefore measured in units of 2^-53, the spacing of doubles just below 1.
static double ulp1(double got, double want) { return std::fabs(got - want) / 0x1p-53; }

int main() {
  environment();

  // --- T1: the pi literal is the binary64 value of pi, not a decimal literal.
  {
    double from_acosl = double(acosl(-1.0L));  // correctly rounded to 64 bits, then to 53
    uint64_t bits;
    std::memcpy(&bits, &pi, 8);
    std::printf("pi = %a, bits 0x%016llx, (double)acosl(-1) = %a\n", pi,
                (unsigned long long)bits, from_acosl);
    ck(pi == from_acosl, "T1 pi literal == (double)acosl(-1.0L)");
    ck(bits == 0x400921FB54442D18ULL, "T1 pi bits == 0x400921FB54442D18");
  }
  ck(FLT_EVAL_METHOD == 0, "T1b FLT_EVAL_METHOD == 0");
  ck(std::numeric_limits<double>::digits == 53, "T1b double significand is 53 bits");

  // --- T2: environment() forces round-to-nearest whatever we leave behind.
  {
    bool ok = true;
    for (int m : {FE_UPWARD, FE_DOWNWARD, FE_TOWARDZERO}) {
      std::fesetround(m);
      if (std::fegetround() != m) ok = false;
      environment();
      if (std::fegetround() != FE_TONEAREST) ok = false;
    }
    std::fesetround(FE_TONEAREST);
    ck(ok, "T2 environment() -> FE_TONEAREST from every rounding mode");
    // and prove the mode is observable at all: 1/3 rounds up under FE_UPWARD
    std::fesetround(FE_UPWARD);
    volatile double a = 1., b = 10.;
    double up = a / b;
    std::fesetround(FE_DOWNWARD);
    double dn = a / b;
    std::fesetround(FE_TONEAREST);
    double nn = a / b;
    std::printf("     1/10 upward %a downward %a nearest %a\n", up, dn, nn);
    // A quotient of two exactly-representable doubles is never at a tie, so the
    // nearest value equals one of the directed ones; what the test shows is that
    // the upward and downward results differ, i.e. the mode is observable here.
    ck(up != dn && (nn == up || nn == dn) && up - dn == ulp_at(nn),
       "T2b the rounding mode is observable (1/10 up != down)");
  }

  // --- T3: expair is the exponential, to within a few ulp.
  {
    // (a) fixed points with exact answers
    V e0 = expair(0.), e4 = expair(.25), e2 = expair(.5), e75 = expair(.75);
    ck(e0[0] == 1. && e0[1] == 0., "T3 expair(0) == (1,0) exactly");
    ck(e4[0] == 0. && e4[1] == 1., "T3 expair(1/4) == (0,1) exactly");
    ck(e2[0] == -1. && e2[1] == 0., "T3 expair(1/2) == (-1,0) exactly");
    ck(e75[0] == 0. && e75[1] == -1., "T3 expair(3/4) == (0,-1) exactly");
    // (b) domain guard
    V big = expair(16.0000001), huge = expair(1e300), neg = expair(-16.0000001);
    ck(std::isnan(big[0]) && std::isnan(big[1]), "T3 expair(16.0000001) is NaN,NaN");
    ck(std::isnan(huge[0]) && std::isnan(huge[1]), "T3 expair(1e300) is NaN,NaN");
    ck(std::isnan(neg[0]) && std::isnan(neg[1]), "T3 expair(-16.0000001) is NaN,NaN");
    ck(!std::isnan(expair(16.)[0]), "T3 expair(16) is in range");
    // (c) scan [0,1) against long-double cosl/sinl
    double worst = 0.;
    double wx = 0.;
    for (int i = 0; i < 200000; ++i) {
      double x = i / 200000.;
      long double t = 2.0L * (long double)pi * (long double)x;
      V got = expair(x);
      double erra = ulp1(got[0], double(cosl(t)));
      double errb = ulp1(got[1], double(sinl(t)));
      double e = std::max(erra, errb);
      if (e > worst) { worst = e; wx = x; }
    }
    std::printf("     worst |expair - (cos,sin)(2 pi x)| over 200001 x in [0,1): %.3f x 2^-53 at x=%a\n",
                worst, wx);
    ck(worst <= 8., "T3 expair is within 8 x 2^-53 of the long-double exponential");
    // (d) the 112 grid points the table actually uses
    double tabworst = 0.;
    for (int i = 0; i < 112; ++i) {
      long double t = 2.0L * (long double)pi * (((long double)i + 0.5L) / 112.0L);
      V got = expair((i + .5) / 112);
      tabworst = std::max(tabworst, std::max(ulp1(got[0], double(cosl(t))),
                                             ulp1(got[1], double(sinl(t)))));
    }
    std::printf("     worst tab-grid error: %.3f x 2^-53\n", tabworst);
    ck(tabworst <= 8., "T3b tab grid is within 8 x 2^-53 of cos/sin");
  }

  // --- T4: hp
  {
    ck(hp(3., 4.) == 5., "T4 hp(3,4) == 5 exactly");
    ck(hp(0., 0.) == 0., "T4 hp(0,0) == 0 exactly");
    ck(hp(-3., -4.) == 5., "T4 hp(-3,-4) == 5 exactly");
  }

  // --- T5: the seed error bound has the association the manuscript records,
  // and that association is worth one ulp in binary64.
  {
    Table t;
    t.build(112);
    const double err = pi * (t.w * t.w / 4) * 5.;
    const double err2 = 5 * pi / (4 * 112 * 112);  // same real number, other association
    std::printf("     err = %a   (5*pi/(4*112*112) = %a, delta %d ulp)\n", err, err2,
                int((err2 - err) / ulp_at(err)));
    ck(err == 0x1.4843ae1860576p-12, "T5 err == 0x1.4843ae1860576p-12 (pi*(w*w/4)*5.)");
    ck(std::fabs(err - err2) <= 2 * ulp_at(err), "T5 the two associations differ by <= 2 ulp");
  }

  // --- T6: sumok's c is inside the interval it publishes.
  // For a fixed pseudo-random sample of ascending 5-subsets, recompute
  // c = (sum_b sin, -1/sum... ) / (2 pi) in long double from the exact angles
  // and check |c - c_true| <= err, the bound sumok's callers rely on.
  {
    Table t;
    t.build(112);
    const double err = pi * (t.w * t.w / 4) * 5.;
    long double worst_rel = 0.;
    int nacc = 0, ntot = 0;
    uint64_t s = 123456789;
    for (int trial = 0; trial < 4000; ++trial) {
      ar b{};
      for (int j = 0; j < 5; ++j) {  // 5 distinct bins, ascending
        s = s * 6364136223846793005ULL + 1442695040888963407ULL;
        int v;
        bool dup;
        do {
          s = s * 6364136223846793005ULL + 1442695040888963407ULL;
          v = int((s >> 33) % 112);
          dup = false;
          for (int k = 0; k < j; ++k) dup |= (b[k] == v);
        } while (dup);
        b[j] = v;
        for (int k = j; k > 0 && b[k - 1] > b[k]; --k) std::swap(b[k - 1], b[k]);
      }
      XY p{};
      p.b = b;
      for (int j = 0; j < 5; ++j)
        if (std::abs(b[j] * 2 + 1 - t.n) < std::abs(b[p.s] * 2 + 1 - t.n)) p.s = j;
      sumok(p, t);
      long double c0 = 0., c1 = -1.0L / (2.0L * acosl(-1.0L));
      for (int j = 0; j < 5; ++j) {
        long double th = 2.0L * acosl(-1.0L) * (((long double)b[j] + 0.5L) / 112.0L);
        c0 += sinl(th) / (2.0L * acosl(-1.0L));
        c1 -= cosl(th) / (2.0L * acosl(-1.0L));
      }
      double d = std::max(std::fabs(double(c0) - p.c[0]), std::fabs(double(c1) - p.c[1]));
      double rel = d / err;
      worst_rel = std::max(worst_rel, (long double)rel);
      ++ntot;
      if (rel <= 1.) ++nacc;
    }
    std::printf("     max |c_longdouble - c| / err over %d sampled seeds: %.3Le\n", ntot,
                worst_rel);
    ck(nacc == ntot, "T6 every sampled seed's c lies inside its err ball");
  }

  std::printf("\n%s: %d failure(s)\n", fails ? "FAILED" : "ALL PASSED", fails);
  return fails ? 1 : 0;
}
