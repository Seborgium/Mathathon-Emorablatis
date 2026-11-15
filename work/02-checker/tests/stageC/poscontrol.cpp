// m1 positive controls for the Stage-C graph search.
// The search code is *upstream's*, not a re-implementation: this TU defines STAGEC_HEADER
// and includes saved-run/compiled-build/source/stageC.cpp verbatim, then drives graph::clique,
// graph::exist and graph::startDuo directly on synthetic `nodes` arrays.  Nothing in the search
// is edited.  Only init()/pairtest() (the geometric edge construction) are bypassed.
#define STAGEC_HEADER
#include "stageC.cpp"
#include <random>
#include <functional>
#include <cstdio>

static int M_ = 0;
static std::vector<std::vector<char>> O_, U_;

static void install(int M, int pO1000, int pU1000, std::mt19937_64 &rng,
                    const std::vector<int> *plantA = nullptr, const std::vector<int> *plantB = nullptr) {
  M_ = M;
  O_.assign(M, std::vector<char>(M, 0));
  U_.assign(M, std::vector<char>(M, 0));
  std::uniform_int_distribution<int> d(0, 999);
  for (int i = 0; i < M; i++)
    for (int j = 0; j < i; j++) {
      if (d(rng) < pO1000) O_[i][j] = O_[j][i] = 1;
      if (d(rng) < pU1000) U_[i][j] = U_[j][i] = 1;
    }
  if (plantA && plantB) {
    for (int a : *plantA) for (int b : *plantA) if (a < b) O_[a][b] = O_[b][a] = 1;
    for (int a : *plantB) for (int b : *plantB) if (a < b) O_[a][b] = O_[b][a] = 1;
    for (int a : *plantA) for (int b : *plantB) U_[a][b] = U_[b][a] = 1;
  }
  words = (M + 63) / 64;
  nodes.assign(M, node{});
  for (int i = 0; i < M; i++)
    for (int j = 0; j < M; j++) {
      if (O_[i][j]) nodes[i].O.set(j);
      if (U_[i][j]) nodes[i].U.set(j);
    }
}

// Definitional brute force, independent of the search: enumerate every 6-subset that is an
// O-clique (as a bitmask), then every pair of disjoint such cliques whose 36 cross pairs all
// lie in U (checked by intersecting U-neighbourhood masks).
// Returns 1 = pattern exists, 0 = not, -1 = gave up (too many cliques).
static int brute(int M, long long budget = 4000000LL) {
  std::vector<uint64_t> Umask(M, 0), cl;
  for (int i = 0; i < M; i++) for (int j = 0; j < M; j++) if (U_[i][j]) Umask[i] |= 1ull << j;
  std::vector<int> cur;
  long long work = 0;
  std::function<void(int)> rec = [&](int start) {
    if (work > budget) return;
    if ((int)cur.size() == 6) {
      uint64_t m = 0; for (int v : cur) m |= 1ull << v; cl.push_back(m); return;
    }
    for (int i = start; i < M; i++) {
      if (++work > budget) return;
      bool ok = true;
      for (int v : cur) if (!O_[i][v]) { ok = false; break; }
      if (!ok) continue;
      cur.push_back(i); rec(i + 1); cur.pop_back();
    }
  };
  rec(0);
  if (work > budget || cl.size() > 4000) return -1;
  for (size_t x = 0; x < cl.size(); x++) {
    uint64_t common = ~0ull;
    for (int i = 0; i < M; i++) if ((cl[x] >> i) & 1) common &= Umask[i];
    for (size_t y = x + 1; y < cl.size(); y++)
      if (!(cl[x] & cl[y]) && (cl[y] & ~common) == 0) return 1;
  }
  return 0;
}

static int runSearch(int M, int mode, uint64_t cap) {
  BS p;
  for (int i = 0; i < M; i++) p.set(i);
  graph::steps = 0; graph::gaveup = false; capSteps = cap; searchMode = mode;
  bool q = (mode >= 2) ? graph::startDuo(p) : graph::exist(p, p, 6);
  return q ? 1 : 0;
}

int main() {
  std::mt19937_64 rng(20261114);
  int bad = 0, tested = 0, skipped = 0;
  int yes = 0, no = 0;
  // (1) random small instances: exists(mode 0,1,2) against definitional brute force
  for (int trial = 0; trial < 400; trial++) {
    int M = 12 + int(rng() % 4);              // 12..15
    int pO = 150 + int(rng() % 550);          // 0.15..0.70
    int pU = 150 + int(rng() % 850);
    bool plant = (trial % 2) == 0;
    std::vector<int> A, B;
    if (plant) {
      std::vector<int> v(M); for (int i = 0; i < M; i++) v[i] = i;
      std::shuffle(v.begin(), v.end(), rng);
      A.assign(v.begin(), v.begin() + 6); B.assign(v.begin() + 6, v.begin() + 12);
    }
    install(M, pO, pU, rng, plant ? &A : nullptr, plant ? &B : nullptr);
    int bf = brute(M);
    if (bf < 0) { skipped++; continue; }
    int r0 = runSearch(M, 0, 1000000000ull);
    int r1 = runSearch(M, 1, 1000000000ull);
    int r2 = runSearch(M, 2, 1000000000ull);
    tested++; bf ? yes++ : no++;
    if (r0 != bf || r1 != bf || r2 != bf) {
      bad++;
      if (bad <= 10)
        printf("MISMATCH trial%d M%d pO%d pU%d plant%d brute%d mode0=%d mode1=%d mode2=%d\n",
               trial, M, pO, pU, (int)plant, bf, r0, r1, r2);
    }
  }
  fflush(stdout); printf("RANDOM tested%d (pattern %d / no-pattern %d, skipped %d) mismatches %d\n",
         tested, yes, no, skipped, bad);

  // (2) planted patterns at production scale, vertices pushed to the end of the index order
  int pbad = 0, ptot = 0;
  uint64_t worst = 0;
  for (int M : {12, 64, 128, 256, 512, 1024}) {
    for (int rep = 0; rep < 3; rep++) {
      std::vector<int> A, B;
      for (int i = 0; i < 6; i++) { A.push_back(M - 12 + i); B.push_back(M - 6 + i); }
      install(M, 150, 400, rng, &A, &B);   // sparse O, moderate U: pattern is not trivially dense
      for (int mode = 0; mode <= 2; mode++) {
        int r = runSearch(M, mode, 4000000000ull);
        ptot++;
        if (!r) { pbad++; printf("PLANT MISS M%d mode%d\n", M, mode); }
        if (graph::gaveup) printf("PLANT CAP M%d mode%d steps%llu\n", M, mode, (unsigned long long)graph::steps);
      }
      worst = std::max(worst, (uint64_t)graph::steps);
    }
    printf("PLANT M%d ok, last steps%llu\n", M, (unsigned long long)graph::steps);
  }
  fflush(stdout); printf("PLANTED runs%d misses%d worst_steps%llu\n", ptot, pbad, (unsigned long long)worst);

  // (3) the self-loop hypothesis: disjointness is enforced *only* by the absence of U self-loops.
  // Graph: vertices 0..5 form an O-clique and a U-clique among themselves, vertex 5 has a U
  // self-loop; the only "12-label" configuration reuses vertex 5.  Definitional brute force
  // (which requires disjointness) says NO.  If the search says YES, it relies on loop-freeness.
  {
    int M = 12;
    install(M, 0, 0, rng);
    // vertices 0..10: complete in both O and U; vertex 11 isolated.  A genuine pattern needs
    // twelve usable labels and does not exist.  A U self-loop at vertex 5 lets the search reuse
    // label 5 in both bases, which the definition forbids.
    for (int i = 0; i <= 10; i++) for (int j = 0; j <= 10; j++) if (i != j) { O_[i][j] = 1; U_[i][j] = 1; }
    U_[5][5] = 1;
    words = 1; nodes.assign(M, node{});
    for (int i = 0; i < M; i++) for (int j = 0; j < M; j++) { if (O_[i][j]) nodes[i].O.set(j); if (U_[i][j]) nodes[i].U.set(j); }
    int bf = brute(M);
    int r1 = runSearch(M, 1, 1000000000ull);
    printf("SELFLOOP brute%d search_mode1=%d  (search YES + definition NO => the search's disjointness relies on U having no self-loops)\n", bf, r1);
  }

  // (4) cap semantics: a genuinely hard instance at a small cap must set gaveup and never be
  // reported as a completed negative.
  {
    std::vector<int> A, B;
    int M = 512;
    for (int i = 0; i < 6; i++) { A.push_back(M - 12 + i); B.push_back(M - 6 + i); }
    install(M, 300, 450, rng, &A, &B);
    for (uint64_t cap : {200ull, 5000ull, 100000ull}) {
      graph::steps = 0; graph::gaveup = false; capSteps = cap; searchMode = 1;
      BS p; for (int i = 0; i < M; i++) p.set(i);
      bool q = graph::exist(p, p, 6);
      printf("CAP cap%llu returned%d gaveup%d steps%llu -> classification %s\n",
             (unsigned long long)cap, (int)q, (int)graph::gaveup, (unsigned long long)graph::steps,
             graph::gaveup ? "unresolved(cap)" : (q ? "positive" : "negative"));
    }
  }
  return 0;
}
