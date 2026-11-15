// c-harness.cpp — experiment driver (not the program contract). Adds a seed cache,
// prefix sweeps and parameter ablations so that the invariance of the centre count can
// be tested without a second full run. Every ablation is off by default; the default
// configuration is byte-for-byte the faithful one.
#include "c-cover.hpp"
#include <chrono>
#include <string>
#include <cinttypes>

using namespace mub;

static const char* CMAGIC = "CSEED1";

static bool saveSeeds(const Seeds& S, const char* path) {
  FILE* f = fopen(path, "wb"); if (!f) return false;
  fwrite(CMAGIC, 1, 6, f);
  int32_t nn = S.L.n; fwrite(&nn, 4, 1, f);
  int64_t nx = (int64_t)S.xs.size(); fwrite(&nx, 8, 1, f);
  auto wr = [&](const xy& p) {
    int32_t b[5] = {p.b[0], p.b[1], p.b[2], p.b[3], p.b[4]};
    int32_t s = p.s; fwrite(b, 4, 5, f); fwrite(&s, 4, 1, f);
    fwrite(&p.g, 8, 1, f); fwrite(&p.c[0], 8, 1, f); fwrite(&p.c[1], 8, 1, f);
  };
  for (const auto& p : S.xs) wr(p);
  for (int a = 0; a < S.L.n; a++) { int64_t c = (int64_t)S.ys[a].size(); fwrite(&c, 8, 1, f); }
  for (int a = 0; a < S.L.n; a++) for (const auto& p : S.ys[a]) wr(p);
  bool ok = !ferror(f) && fclose(f) == 0;
  return ok;
}

static bool loadSeeds(Seeds& S, const char* path) {
  FILE* f = fopen(path, "rb"); if (!f) return false;
  char mg[6]; if (fread(mg, 1, 6, f) != 6 || memcmp(mg, CMAGIC, 6)) return false;
  int32_t nn; if (fread(&nn, 4, 1, f) != 1) return false;
  S.L.init(nn);
  int64_t nx; if (fread(&nx, 8, 1, f) != 1) return false;
  auto rd = [&](xy& p) {
    int32_t b[5], s;
    if (fread(b, 4, 5, f) != 5) return false;
    if (fread(&s, 4, 1, f) != 1) return false;
    for (int j = 0; j < 5; j++) p.b[j] = b[j];
    p.s = s;
    if (fread(&p.g, 8, 1, f) != 1) return false;
    if (fread(&p.c[0], 8, 1, f) != 1) return false;
    if (fread(&p.c[1], 8, 1, f) != 1) return false;
    return true;
  };
  S.xs.resize(nx);
  for (int64_t i = 0; i < nx; i++) if (!rd(S.xs[i])) return false;
  std::vector<int64_t> cnt(nn);
  for (int a = 0; a < nn; a++) if (fread(&cnt[a], 8, 1, f) != 1) return false;
  S.ys.resize(nn);
  for (int a = 0; a < nn; a++) {
    S.ys[a].resize(cnt[a]);
    for (int64_t i = 0; i < cnt[a]; i++) if (!rd(S.ys[a][i])) return false;
  }
  bool ok = !ferror(f) && fclose(f) == 0;
  return ok;
}

int main(int argc, char** argv) {
  environment();
  std::string cache, out, stats;
  long tmax = -1;
  Options opt;
  bool dump = false, seeded = false;
  for (int i = 1; i < argc; i++) {
    std::string a = argv[i];
    if (a == "--dump-seeds") { dump = true; cache = argv[++i]; }
    else if (a == "--load") { seeded = true; cache = argv[++i]; }
    else if (a == "--out") out = argv[++i];
    else if (a == "--stats") stats = argv[++i];
    else if (a == "--tmax") tmax = atol(argv[++i]);
    else if (a == "--K") opt.K = atoi(argv[++i]);
    else if (a == "--m") opt.m = atoi(argv[++i]);
    else if (a == "--dual") opt.dual = atoi(argv[++i]);
    else if (a == "--R") opt.R = atof(argv[++i]);
    else if (a == "--no-cheap") opt.cheap_accept = false;
    else if (a == "--no-prefilter") opt.cheap_prefilter = false;
    else if (a == "--no-gap") opt.filter_gap = false;
    else if (a == "--no-iv") opt.filter_interval = false;
    else { fprintf(stderr, "unknown option %s\n", a.c_str()); return 2; }
  }
  auto st = std::chrono::steady_clock::now();
  Seeds S;
  if (seeded) { if (!loadSeeds(S, cache.c_str())) { fprintf(stderr, "load failed\n"); return 3; } }
  else { S.build(112); if (dump && !saveSeeds(S, cache.c_str())) { fprintf(stderr, "dump failed\n"); return 3; } }
  double tb = std::chrono::duration<double>(std::chrono::steady_clock::now() - st).count();
  size_t ny = 0; for (auto& v : S.ys) ny += v.size();
  printf("seeds xs%zu ys%zu build%.2f\n", S.xs.size(), ny, tb);
  coverSeeds C;
  C.run(S, opt, tmax);
  if (!out.empty() && !C.writeCenters(out.c_str())) return 4;
  printf("N%d r%.4f dual%d K%d m%d checked%lu centers%zu visit%lu near%lu cheap%lu lp%lu\n",
         C.n, C.R, C.dual, C.K, C.m, (unsigned long)C.checked, C.all.size(),
         (unsigned long)C.nvisit, (unsigned long)C.ncover, (unsigned long)C.ncheap,
         (unsigned long)C.nlp);
  printf("extra lpok%lu dropgap%lu dropiv%lu covered%lu\n",
         (unsigned long)C.nlp_ok, (unsigned long)C.drop_gap,
         (unsigned long)C.drop_interval,
         (unsigned long)(C.checked - C.all.size()));
  printf("time %.2f\n", std::chrono::duration<double>(std::chrono::steady_clock::now() - st).count());
  if (!stats.empty()) {
    FILE* f = fopen(stats.c_str(), "w"); if (!f) return 5;
    fprintf(f, "{\"xs\":%zu,\"ys\":%zu,\"tmax\":%ld,\"K\":%d,\"m\":%d,\"dual\":%d,"
               "\"checked\":%" PRIu64 ",\"centers\":%zu,\"visit\":%" PRIu64 ",\"near\":%" PRIu64
               ",\"cheap\":%" PRIu64 ",\"lp\":%" PRIu64 ",\"lpok\":%" PRIu64 ","
               "\"dropgap\":%" PRIu64 ",\"dropiv\":%" PRIu64 "}\n",
            S.xs.size(), ny, tmax, C.K, C.m, C.dual, C.checked, C.all.size(), C.nvisit,
            C.ncover, C.ncheap, C.nlp, C.nlp_ok, C.drop_gap, C.drop_interval);
    if (ferror(f) || fclose(f) != 0) return 5;
  }
  return 0;
}
