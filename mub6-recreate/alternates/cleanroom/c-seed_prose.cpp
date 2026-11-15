// c-seed_prose.cpp -- CLEAN-ROOM re-derivation of the 112-bin seed enumeration
// from the manuscript alone.  I have not opened seed.cpp or covout.cpp.
//
// Preprint: "The maximum number of mutually unbiased bases in dimension six"
// (OpenAI, 24 Sep 2026).  Section numbers below are its section numbers.
// Every rule is cited; every choice the prose leaves open is marked OPEN-k and
// is measured in C-NOTES.md against the recorded artefact.
//
// Section 2.3, p.10: "The enumeration in seeds::build now has an explicit
// interpretation.  It visits every weakly increasing five-bin X tuple and
// applies (2.7), the first inequality in (2.8), and sumok.  Separately, for
// every possible first bin it visits all weakly increasing four-bin Y tails
// and applies sumok."
//
// build mode (default): enumerate X tuples, call mk, list xs.
// --ytails=h1,h2,...  : enumerate the Y tails for each given first bin.
//
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <vector>

static int n = 112;              // (2.6) N = 112
static double w = 1.0 / 112.0;   // (2.6) w = 1/N
static const double PI = 0x1.921fb54442d18p+1;   // binary64 pi, spec S4

// ---- OPEN choices, measured in C-NOTES.md ---------------------------------
static int    OPT_dirs      = 3;    // OPEN-1 1=residual only 2=perps only 3=both
static double OPT_slack     = 1e-8; // A.3 comparison addition in chk
static double OPT_gapslack  = 1e-8; // A.3 "Their slack is 1e-8"
static int    OPT_oneminus  = 1;    // OPEN-2 the fixed phase 0 contributes 1
static int    OPT_forward   = 0;    // OPEN-3 1 = lexicographic (a,b,c,d,l) nesting
static int    OPT_res_unnorm= 0;    // OPEN-4 residual direction normalised or not
// ---------------------------------------------------------------------------

struct P2 { double x, y; };

// e(t) = exp(2*pi*i*t), t in cycles (Section 2 preamble)
static P2 ecyc(double t) {
    double a = 2.0 * PI * t;
    return P2{std::cos(a), std::sin(a)};
}

// Lemma 2.7 / (2.11):  |v.c| <= (5*pi*w^2/4)||v|| + (w/2) sum_j |v.J_j|
// "The function sumok tests (2.11) in the residual direction and in directions
//  perpendicular to the five unit-exponential columns."  A.3: "Its remainder
//  coefficient approximates 5 pi/(4 n^2) within 1e-15.  The actual 1e-8
//  comparison addition therefore preserves every feasible list."
// OPEN-1: a perpendicular direction to column J_t is read as v_t = (-J_t.y,
//   J_t.x), of unit norm ("its norm is less than 1.1", A.3).
// OPEN-2: the leading phase 0 is fixed and contributes the "1" of
//   1 + sum_j e(u_j).
static bool sumok(const double* u) {
    P2 J[5];
    double p = OPT_oneminus ? 1.0 : 0.0, q = 0.0;
    for (int j = 0; j < 5; ++j) {
        J[j] = ecyc(u[j]);
        p += J[j].x;
        q += J[j].y;
    }
    P2 c{q / (2.0 * PI), -p / (2.0 * PI)};    // (1+sum e(u_j)) / (2 pi i), (2.9)
    const double E = 5.0 * PI * w * w / 4.0;  // (2.10) remainder coefficient
    P2 v[6]; double vn[6];
    double cn = std::sqrt(c.x * c.x + c.y * c.y);
    if (OPT_res_unnorm) { v[0] = c; vn[0] = cn; }
    else                { v[0] = P2{c.x / cn, c.y / cn}; vn[0] = 1.0; }
    for (int t = 0; t < 5; ++t) { v[1 + t] = P2{-J[t].y, J[t].x}; vn[1 + t] = 1.0; }
    int i0 = (OPT_dirs == 2 ? 1 : 0), i1 = (OPT_dirs == 1 ? 1 : 6);
    for (int i = i0; i < i1; ++i) {
        double vc = v[i].x * c.x + v[i].y * c.y;
        if (vc < 0) vc = -vc;
        double s = 0.0;
        for (int j = 0; j < 5; ++j) {
            double d = v[i].x * J[j].x + v[i].y * J[j].y;
            if (d < 0) d = -d;
            s += d;
        }
        if (vc > E * vn[i] + (w / 2.0) * s + OPT_slack) return false;
    }
    return true;
}

// Section 2.2, after Lemma 2.6: "For sorted midpoint bin indices q0,...,q4, the
// gap used by mk is max{(q0+1/2)/N, (q1-q0)/N, (q2-q1)/N, (q3-q2)/N,
// (q4-q3)/N, 1-(q4+1/2)/N}".  The term (q0+1/2)/N is the gap from the fixed
// leading phase 0; a repeated point contributes a zero gap.
static double midgap(const int* q, int m) {
    double g = ((double)q[0] + 0.5) * w;
    for (int i = 1; i < m; ++i) {
        double t = (double)(q[i] - q[i - 1]) * w;
        if (t > g) g = t;
    }
    double t = 1.0 - ((double)q[m - 1] + 0.5) * w;
    if (t > g) g = t;
    return g;
}

// seeds::mk on an X tuple: (2.7) a <= l-d+1 (integral), then the first
// inequality of (2.8) gx,mid <= 1-(l-1)/N, then sumok.  Returns s or -1.
// "choose s in {0..4} as the first minimizer of |2 bX_s + 1 - N|"  (2.7)
static int mk(int a, int b, int c, int d, int l, long* cnt) {
    if (a > l - d + 1) return -1;
    cnt[0]++;
    int q[5] = {a, b, c, d, l};
    if (!(midgap(q, 5) <= 1.0 - (double)(l - 1) * w + OPT_gapslack)) return -1;
    cnt[1]++;
    double u[5];
    for (int j = 0; j < 5; ++j) u[j] = ((double)q[j] + 0.5) * w;
    if (!sumok(u)) return -1;
    cnt[2]++;
    int s = 0;
    double best = std::fabs(2.0 * (double)q[0] + 1.0 - (double)n);
    for (int i = 1; i < 5; ++i) {
        double t = std::fabs(2.0 * (double)q[i] + 1.0 - (double)n);
        if (t < best) { best = t; s = i; }
    }
    return s;
}

int main(int argc, char** argv) {
    int dump = 0;
    const char* yh = nullptr;
    for (int i = 1; i < argc; ++i) {
        if (!strcmp(argv[i], "--dump")) dump = 1;
        if (!strncmp(argv[i], "--ytails=", 9)) yh = argv[i] + 9;
        if (!strncmp(argv[i], "--dirs=", 7)) OPT_dirs = atoi(argv[i] + 7);
        if (!strncmp(argv[i], "--slack=", 8)) OPT_slack = atof(argv[i] + 8);
        if (!strncmp(argv[i], "--gapslack=", 11)) OPT_gapslack = atof(argv[i] + 11);
        if (!strcmp(argv[i], "--no-oneminus")) OPT_oneminus = 0;
        if (!strcmp(argv[i], "--residual-unnormalised")) OPT_res_unnorm = 1;
        if (!strcmp(argv[i], "--order=forward")) OPT_forward = 1;
    }

    if (yh) {   // Y tail enumeration for the listed first bins
        int hs[256]; int nh = 0;
        const char* p = yh;
        while (*p) { hs[nh++] = atoi(p); while (*p && *p != ',') ++p; if (*p == ',') ++p; }
        long tot = 0, nacc = 0;
        for (int i = 0; i < nh; ++i) {
            int h = hs[i];
            // OPEN-3': nesting direction of the four tail loops.  Ascending with
            // the LAST coordinate outermost is the only choice the recorded file
            // leaves consistent (see C-NOTES.md).
            for (int y4 = 0; y4 < n; ++y4)
            for (int y3 = 0; y3 <= y4; ++y3)
            for (int y2 = 0; y2 <= y3; ++y2)
            for (int y1 = 0; y1 <= y2; ++y1) {
                ++tot;
                double u[5] = {((double)h + 0.5) * w, ((double)y1 + 0.5) * w,
                               ((double)y2 + 0.5) * w, ((double)y3 + 0.5) * w,
                               ((double)y4 + 0.5) * w};
                if (sumok(u)) { ++nacc; printf("%d %d %d %d %d\n", h, y1, y2, y3, y4); }
            }
        }
        fprintf(stderr, "y-tails: first bins %d, tuples visited %ld, accepted %ld\n",
                nh, tot, nacc);
        return 0;
    }

    long cnt[3] = {0, 0, 0};
    std::vector<int> xs;
    if (OPT_forward) {
        for (int a = 0; a < n; ++a)
        for (int b = a; b < n; ++b)
        for (int c = b; c < n; ++c)
        for (int d = c; d < n; ++d)
        for (int l = d; l < n; ++l) {
            int s = mk(a, b, c, d, l, cnt);
            if (s >= 0) { xs.push_back(a); xs.push_back(b); xs.push_back(c);
                          xs.push_back(d); xs.push_back(l); xs.push_back(s); }
        }
    } else {
        for (int l = 0; l < n; ++l)
        for (int d = 0; d <= l; ++d)
        for (int c = 0; c <= d; ++c)
        for (int b = 0; b <= c; ++b)
        for (int a = 0; a <= b; ++a) {
            int s = mk(a, b, c, d, l, cnt);
            if (s >= 0) { xs.push_back(a); xs.push_back(b); xs.push_back(c);
                          xs.push_back(d); xs.push_back(l); xs.push_back(s); }
        }
    }
    printf("n %d order=%s dirs=%d slack=%g gapslack=%g oneminus=%d residual=%s"
           " | (2.7) %ld +(2.8a) %ld +sumok %ld xs %zu\n",
           n, OPT_forward ? "forward" : "reversed", OPT_dirs, OPT_slack,
           OPT_gapslack, OPT_oneminus, OPT_res_unnorm ? "unnorm" : "unit",
           cnt[0], cnt[1], cnt[2], xs.size() / 6);
    if (dump)
        for (size_t i = 0; i < xs.size(); i += 6)
            printf("%d %d %d %d %d %d\n", xs[i], xs[i+1], xs[i+2], xs[i+3],
                   xs[i+4], xs[i+5]);
    return 0;
}
