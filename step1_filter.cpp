// step1_filter.cpp -- Step 1 (preprint section 2) filters on seed bin pairs.
//
//   ./step1_filter            worked example: one matrix's seed, then four perturbations
//   ./step1_filter survey M   Monte Carlo over M random bin pairs, per-test kill counts
//
// Tests, in the preprint's order and numbering:
//   T1 (2.7)  integral orientation      a <= l - d + 1
//   T2 (2.8)  midpoint gap filters      gx <= 1-(l-1)/N ,  gy >= 1-(l+2)/N
//   T3 (2.11) vanishing-sum dual        |v.c| <= (5 pi w^2/4)|v| + (w/2) sum_j |v.J_j|
//   T4 (2.14) shared-coordinate interval from the x list must meet the one from the y list
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <array>
#include <vector>
#include <algorithm>
#include <random>
#include <string>

static const int N = 112;                 // bins
static const double w = 1.0 / N;          // bin width
static const double E = 5.0 * M_PI / (4.0 * N);   // (2.12) grid-unit margin
using Bins = std::array<int, 5>;
struct V2 { double x, y; };
static V2 operator+(V2 a, V2 b){ return {a.x+b.x, a.y+b.y}; }
static V2 operator*(double s, V2 a){ return {s*a.x, s*a.y}; }
static double dot(V2 a, V2 b){ return a.x*b.x + a.y*b.y; }
static double nrm(V2 a){ return std::hypot(a.x, a.y); }
static V2 unit(double t){ return {std::cos(2*M_PI*t), std::sin(2*M_PI*t)}; }
static double mid(int b){ return (b + 0.5) / N; }        // u_b

// ---- T1 ---- (2.7)
static bool T1(const Bins& x){ return x[0] <= x[4] - x[3] + 1; }

// ---- T2 ---- (2.8): discrete midpoint gaps from bin indices (as used by seeds::mk)
static double gapMid(const int* q, int n){          // q sorted, n = 5
    double g = (q[0] + 0.5);                        // arc from 0 to the first point
    for (int i = 0; i + 1 < n; ++i) g = std::max(g, double(q[i+1] - q[i]));
    g = std::max(g, double(N) - (q[n-1] + 0.5));    // arc from the last point round to 0
    return g / N;
}
static bool T2(const Bins& x, const Bins& y){
    double gx = gapMid(x.data(), 5), gy = gapMid(y.data(), 5);
    return gx <= 1.0 - double(x[4] - 1) / N  &&  gy >= 1.0 - double(x[4] + 2) / N;
}

// ---- T3 ---- (2.9)-(2.11): c and J_j from the five midpoint phases
static void residual(const Bins& b, V2& c, std::array<V2,5>& J){
    V2 s{1.0, 0.0};                                 // the fixed leading 1
    for (int j = 0; j < 5; ++j){ J[j] = unit(mid(b[j])); s = s + J[j]; }
    c = { -s.y / (2*M_PI), s.x / (2*M_PI) };        // c = s / (2 pi i)
}
static double T3ratio(const Bins& b){               // > 1 means excluded
    V2 c; std::array<V2,5> J; residual(b, c, J);
    double best = 0;
    V2 dirs[3] = { nrm(c) > 1e-12 ? (1.0/nrm(c))*c : V2{1,0},
                   J[0], V2{-J[0].y, J[0].x} };
    for (V2 v : dirs){
        if (nrm(v) < 1e-12) continue;
        double lhs = std::fabs(dot(v, c));
        double rhs = (5*M_PI*w*w/4)*nrm(v);
        for (int j = 0; j < 5; ++j) rhs += (w/2)*std::fabs(dot(v, J[j]));
        if (rhs > 0) best = std::max(best, lhs / rhs);
    }
    return best;
}

// ---- T4 ---- (2.13)-(2.14): interval for the shared grid coordinate h_t
static bool interval(const Bins& b, int t, V2 v, double& lo, double& hi){
    V2 c; std::array<V2,5> J; residual(b, c, J);
    double a = dot(v, J[t]);
    if (std::fabs(a) < 1e-9) return false;
    double r = E*nrm(v);
    for (int j = 0; j < 5; ++j) if (j != t) r += 0.5*std::fabs(dot(v, J[j]));
    double mid0 = -N*dot(v, c)/a, half = r/std::fabs(a);
    lo = mid0 - half; hi = mid0 + half;
    return true;
}
static bool T4(const Bins& x, int s, const Bins& y){
    // y holds the five varying entries with the shared one first (index 0)
    V2 dirs[2];
    { V2 c; std::array<V2,5> J; residual(y, c, J); dirs[0] = J[0]; dirs[1] = {-J[0].y, J[0].x}; }
    for (V2 v : dirs){
        double lx, hx, ly, hy;
        if (!interval(x, s, v, lx, hx)) continue;
        if (!interval(y, 0, v, ly, hy)) continue;
        if (std::max(lx, ly) > std::min(hx, hy)) return false;   // disjoint -> excluded
    }
    return true;
}

// ---- the canonical tuple of an exact seed (given phase bins) ----
static const char* verdict(bool ok){ return ok ? "pass" : "EXCLUDED"; }

static void report(const char* name, const Bins& x, const Bins& y, int s){
    double gx = gapMid(x.data(),5), gy = gapMid(y.data(),5);
    double rx = T3ratio(x), ry = T3ratio(y);
    std::printf("%-26s x=(%d,%d,%d,%d,%d) y=(%d,%d,%d,%d,%d) s=%d\n", name,
        x[0],x[1],x[2],x[3],x[4], y[0],y[1],y[2],y[3],y[4], s);
    std::printf("   T1 a<=l-d+1 : %d <= %d          %s\n", x[0], x[4]-x[3]+1, verdict(T1(x)));
    std::printf("   T2 gaps     : gx=%.4f <= %.4f ? %s | gy=%.4f >= %.4f ? %s\n",
        gx, 1.0-(x[4]-1.0)/N, gx <= 1.0-(x[4]-1.0)/N ? "y":"n",
        gy, 1.0-(x[4]+2.0)/N, gy >= 1.0-(x[4]+2.0)/N ? "y":"n");
    std::printf("   T3 sum      : max ratio %.3f (x) %.3f (y)   %s\n", rx, ry,
        (rx<=1 && ry<=1) ? "pass" : "EXCLUDED");
    std::printf("   T4 shared   : %s\n\n", verdict(T4(x, s, y)));
}

int main(int argc, char** argv){
    if (argc > 1 && std::string(argv[1]) == "survey"){                 // ---------- survey
        long long M = argc > 2 ? atoll(argv[2]) : 1000000;
        std::mt19937_64 g(20261114);
        std::uniform_int_distribution<int> U(0, N-1);
        long long pass1=0, pass2=0, pass3x=0, pass3=0, pass4=0;
        for (long long it = 0; it < M; ++it){
            Bins x{ U(g),U(g),U(g),U(g),U(g) }; std::sort(x.begin(), x.end());
            int tail[4] = { U(g),U(g),U(g),U(g) }; std::sort(tail, tail+4);
            int s = 0; double best = 1e18;
            for (int i = 0; i < 5; ++i){ double d = std::fabs(2.0*x[i] + 1 - N); if (d < best){ best = d; s = i; } }
            Bins y{ x[s], tail[0], tail[1], tail[2], tail[3] }; std::sort(y.begin(), y.end());
            if (!T1(x)) continue; ++pass1;
            if (!T2(x, y)) continue; ++pass2;
            if (T3ratio(x) > 1) continue; ++pass3x;
            if (T3ratio(y) > 1) continue; ++pass3;
            if (!T4(x, s, y)) continue; ++pass4;
        }
        std::printf("Monte Carlo over %lld random bin pairs (N=%d)\n", M, N);
        std::printf("  survive T1 (orientation)        %12lld  %8.4f%%\n", pass1, 100.0*pass1/M);
        std::printf("  survive T1+T2 (gaps)            %12lld  %8.4f%%\n", pass2, 100.0*pass2/M);
        std::printf("  survive T1+T2+T3(x)             %12lld  %8.4f%%\n", pass3x, 100.0*pass3x/M);
        std::printf("  survive T1+T2+T3(x)+T3(y)       %12lld  %8.4f%%\n", pass3, 100.0*pass3/M);
        std::printf("  survive all four (T4 too)       %12lld  %8.6f%%\n", pass4, 100.0*pass4/M);
        std::printf("  killed by T1 alone              %8.4f%%\n", 100.0*(M-pass1)/M);
        std::printf("  killed by T2 among T1 survivors %8.4f%%\n", 100.0*(pass1-pass2)/std::max(1LL,pass1));
        std::printf("  killed by T3 among T2 survivors %8.4f%%\n", 100.0*(pass2-pass3)/std::max(1LL,pass2));
        std::printf("  killed by T4 among T3 survivors %8.4f%%\n", 100.0*(pass3-pass4)/std::max(1LL,pass3));
        // x-side only: what a seed cover costs before any y tuple is touched
        long long sa=0, sb=0, sc=0;
        for (long long it = 0; it < M; ++it){
            Bins x{ U(g),U(g),U(g),U(g),U(g) }; std::sort(x.begin(), x.end());
            if (!T1(x)) continue; ++sa;
            if (!(gapMid(x.data(),5) <= 1.0 - double(x[4]-1)/N)) continue; ++sb;
            if (T3ratio(x) > 1) continue; ++sc;
        }
        std::printf("  x side only: T1 %8.4f%%  +gx %8.4f%%  +sum %8.4f%%\n",
            100.0*sa/M, 100.0*sb/M, 100.0*sc/M);
        return 0;
    }

    // ---------------------------------------------------- worked example
    // the dephased Fourier matrix of mub-step1-example.pdf:  x_i = i/6,  xi = 1/2
    Bins x0{18,37,56,74,93};
    Bins y0{56, 0, 0, 56, 56};               // shared bin 56 (xi=1/2), tails 0,0,1/2,1/2
    int s0 = 2;
    std::puts("Base case: the matrix of mub-step1-example.pdf (all four tests must pass)\n");
    report("base", x0, y0, s0);
    { V2 c; std::array<V2,5> J; residual(x0,c,J);
      double lo,hi; interval(x0,2,J[2],lo,hi);
      std::printf("   T4 detail: x list gives h_t in [%.3f, %.3f] (grid units)\n", lo, hi);
      residual(y0,c,J); double lo2,hi2; interval(y0,0,J[0],lo2,hi2);
      std::printf("              y list gives h_t in [%.3f, %.3f]  -> overlap\n\n", lo2, hi2); }

    std::puts("Now the nearest neighbours of that box that are killed by each test in turn:\n"
              "each search walks small perturbations of the base box and reports the first box\n"
              "that passes every earlier test and fails the stated one.\n");
    Bins xr=x0, yr=y0;
    auto search = [&](int stage, int rad){
        for (int i0=-rad;i0<=rad;++i0) for (int i1=-rad;i1<=rad;++i1) for (int i2=-rad;i2<=rad;++i2)
        for (int i3=-rad;i3<=rad;++i3) for (int i4=-rad;i4<=rad;++i4)
        for (int j1=-rad;j1<=rad;++j1) for (int j2=-rad;j2<=rad;++j2) for (int j3=-rad;j3<=rad;++j3) for (int j4=-rad;j4<=rad;++j4){
            Bins x{ x0[0]+i0, x0[1]+i1, x0[2]+i2, x0[3]+i3, x0[4]+i4 };
            int tl[4] = { 0+j1, 0+j2, 0+j3, 0+j4 };
            for (int k=0;k<5;++k) if (x[k]<0||x[k]>=N) goto next;
            for (int k=0;k<4;++k) if (tl[k]<0||tl[k]>=N) goto next;
            {
                std::sort(x.begin(), x.end()); std::sort(tl, tl+4);
                int s=0; double best=1e18;
                for (int k=0;k<5;++k){ double d=std::fabs(2.0*x[k]+1-N); if(d<best){best=d;s=k;} }
                Bins y{ x[s], tl[0], tl[1], tl[2], tl[3] }; std::sort(y.begin(), y.end());
                bool t1=T1(x), t2=T2(x,y), t3=(T3ratio(x)<=1 && T3ratio(y)<=1), t4=T4(x,s,y);
                bool ok = (stage==1? !t1 : stage==2? (t1&&!t2) : stage==3? (t1&&t2&&!t3) : (t1&&t2&&t3&&!t4));
                if (ok){ xr=x; yr=y; return true; }
            }
            next:;
        }
        return false;
    };
    const char* names[5] = {"","P1: killed by T1","P2: killed by T2","P3: killed by T3","P4: killed by T4"};
    for (int st=1; st<=4; ++st){
        int s=0; double best=1e18;
        for (int k=0;k<5;++k){ double d=std::fabs(2.0*x0[k]+1-N); if(d<best){best=d;s=k;} }
        if (search(st, 4)) { /* s recomputed in report */ }
        else { std::printf("%s : none within radius 4\n\n", names[st]); continue; }
        int sr=0; double bb=1e18;
        for (int k=0;k<5;++k){ double d=std::fabs(2.0*xr[k]+1-N); if(d<bb){bb=d;sr=k;} }
        report(names[st], xr, yr, sr);
    }
    std::printf("P5: reuse.  The base box's centre and the box with x5 in bin 94:\n");
    { Bins x5=x0; x5[4]=94; double r=0;
      for (int i=0;i<5;++i){ double d=(x5[i]-x0[i])/double(N); r+=d*d; }
      std::printf("   centre distance %.5f, box circumradius 3w/2 = %.5f, sum %.5f <= R_s = 0.032 : %s\n\n",
        std::sqrt(r), 1.5*w, std::sqrt(r)+1.5*w, (std::sqrt(r)+1.5*w<=0.032)?"absorbed (no new centre)":"kept"); }
    return 0;
}
