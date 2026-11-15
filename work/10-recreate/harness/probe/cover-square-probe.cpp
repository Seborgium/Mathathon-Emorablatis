// harness/probe/cover-square-probe.cpp -- executable form of determinism register
// item 9 (spec/interfaces.md §5).
//
// The register says "pow(x,2) must be a single multiply (inspect the disassembly of
// covrun)".  The published covrun does not do that: it imports pow@GLIBC_2.29 and
// calls pow@plt twice from coverSeeds::run, at exactly the two sites that compute
//     RN2 = pow(R*n, 2) - .0001            r = .032, n = 112
//     T   = pow(sqrt(RN2) + 1.5, 2)
// (.scratch/gh/build/covrun.disassembly.txt, offsets 0x53fa and 0x543f).  GCC 15.2.0
// folds both to a multiply; GCC 16.2.0 and the recorded GCC 14.3.1 keep the call.
//
// So the property byte-identity actually needs is
//     bits(libm pow(v,2)) == bits(v*v)   at the two arguments the cover uses,
// and this probe decides it.  It also measures how far the identity extends, because
// that is what a reimplementation replacing pow(x,2) by x*x is betting on.
//
// Expected result on glibc 2.43 (and 2.39): equal at both cover arguments; NOT equal
// everywhere -- about 4.5e-4 of random doubles differ by exactly 1 ulp, because glibc
// pow is <0.52 ulp, not correctly rounded.  Hence the pass criterion is the cover
// arguments alone, and the sweep is reported as a statistic.
//
// exit 0 = the two cover arguments agree bit for bit; 3 = they do not; 2 = no FE_TONEAREST.
#include <cfloat>
#include <cfenv>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <limits>

static std::uint64_t bits(double x) {
    std::uint64_t u = 0;
    std::memcpy(&u, &x, sizeof u);
    return u;
}

static bool same(double a, double b) {
    if (std::isnan(a) || std::isnan(b)) return std::isnan(a) && std::isnan(b);
    return bits(a) == bits(b);
}

// ulp distance for finite, same-sign results; 0 when not comparable
static std::uint64_t ulp_gap(double a, double b) {
    if (!std::isfinite(a) || !std::isfinite(b)) return 0;
    const std::uint64_t ia = bits(a), ib = bits(b);
    if ((ia >> 63) != (ib >> 63)) return 0;
    return ia > ib ? ia - ib : ib - ia;
}

// volatile so the compiler cannot constant-propagate the callee away
static double (*volatile libm_pow)(double, double) = std::pow;

int main() {
    if (std::fesetround(FE_TONEAREST) != 0) return 2;

    volatile double R = .032;          // covout.cpp main: run(S, .032, 2)
    volatile double n = 112.;          // covout.cpp main: S.build(112)
    volatile double v1 = R * n;
    volatile double rn2_libm = libm_pow(v1, 2.0) - .0001;
    volatile double rn2_mul = v1 * v1 - .0001;
    volatile double v2_libm = std::sqrt(rn2_libm) + 1.5;
    volatile double v2_mul = std::sqrt(rn2_mul) + 1.5;
    volatile double T_libm = libm_pow(v2_libm, 2.0);
    volatile double T_mul = v2_mul * v2_mul;
    const bool rn2_ok = same(rn2_libm, rn2_mul);
    const bool t_ok = same(T_libm, T_mul);

    // hostile single arguments, then a deterministic pseudo-random sweep
    static const double edge[] = {
        0.0, -0.0, 1.0, -1.0, .5, 2.0, 3.584, DBL_MIN,
        std::numeric_limits<double>::denorm_min(), -DBL_MIN, DBL_MAX, 1e-160, 1e-170,
        1.5e-154, 1e153, 1e154, 1e155, 1.34e154, std::sqrt(DBL_MAX),
        std::nextafter(std::sqrt(DBL_MAX), 0.), -std::sqrt(DBL_MAX),
        std::numeric_limits<double>::infinity(), -std::numeric_limits<double>::infinity(),
        std::numeric_limits<double>::quiet_NaN(), 4.5e-308, 6.25e-2,
    };
    std::uint64_t checked = 0, bad = 0, max_gap = 0;
    double worst = 0.;
    int edge_bad = 0;
    for (double x : edge) {
        const double a = libm_pow(x, 2.0), b = x * x;
        ++checked;
        if (!same(a, b)) {
            ++bad; ++edge_bad;
            std::printf("mismatch source=edge bits=%016llx gap=%llu\n",
                        (unsigned long long)bits(x), (unsigned long long)ulp_gap(a, b));
        }
    }
    std::uint64_t state = 0x9e3779b97f4a7c15ull;
    const long samples = 8000000;
    for (long i = 0; i < samples; ++i) {
        state ^= state << 13; state ^= state >> 7; state ^= state << 17;   // xorshift64
        double x;
        std::memcpy(&x, &state, sizeof x);
        const double a = libm_pow(x, 2.0), b = x * x;
        ++checked;
        if (!same(a, b)) {
            ++bad;
            const std::uint64_t gap = ulp_gap(a, b);
            if (gap > max_gap) { max_gap = gap; worst = x; }
            if (bad - edge_bad <= 5)
                std::printf("mismatch source=sweep bits=%016llx gap=%llu\n",
                            (unsigned long long)bits(x), (unsigned long long)gap);
        }
    }
    std::printf("cover-square rn2_libm=%a rn2_mul=%a T_libm=%a T_mul=%a\n",
                (double)rn2_libm, (double)rn2_mul, (double)T_libm, (double)T_mul);
    std::printf("sweep checked=%llu mismatches=%llu max_ulp_gap=%llu rate=%.6e\n",
                (unsigned long long)checked, (unsigned long long)bad,
                (unsigned long long)max_gap, (double)bad / (double)checked);
    std::printf("worst_arg bits=%016llx\n", (unsigned long long)bits(worst));
    const bool ok = rn2_ok && t_ok;
    std::printf("pow-equals-multiply at_cover_arguments=%s universally=%s\n",
                ok ? "yes" : "no", bad == 0 ? "yes" : "no");
    std::printf("RESULT cover-square pass=%s\n", ok ? "yes" : "no");
    return ok ? 0 : 3;
}
