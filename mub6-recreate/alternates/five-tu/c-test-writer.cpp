// c-test-writer.cpp -- fixture test of the byte-exact writer.
//   c-test-writer <fixture> <out>
// <fixture> holds the header line plus the first 10 centre lines of the recorded
// centers.txt verbatim.  The test parses them into the module's data structures,
// writes them back with writeCenters, and requires the result to be byte-identical
// to "112 10\n" followed by those 10 lines -- i.e. header "%d %zu\n", ten integers
// each followed by ONE space, then "\n".
//
// A second check exercises the "no locale dependence" claim: with C_TEST_SETLOCALE
// defined the program calls setlocale(LC_ALL, "") first (which is the only way a
// process could acquire a non-C LC_NUMERIC), and the bytes must not change.
#include <cerrno>
#include <clocale>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>

#include "c-writer.hpp"

int main(int argc, char** argv) {
  if (argc != 3) { fprintf(stderr, "usage: %s <fixture> <out>\n", argv[0]); return 2; }
#ifdef C_TEST_SETLOCALE
  setlocale(LC_ALL, "");
  fprintf(stderr, "setlocale(LC_ALL,\"\") -> LC_NUMERIC=%s\n", setlocale(LC_NUMERIC, nullptr));
#endif
  FILE* f = fopen(argv[1], "rb");
  if (!f) { perror("fixture"); return 2; }
  char line[512];
  if (!fgets(line, sizeof line, f)) return 2;
  int nn = 0;
  size_t cnt = 0;
  size_t rec = 0;  // the recorded file's total; the fixture holds only 10 lines of it
  if (sscanf(line, "%d %zu", &nn, &rec) != 2) { fprintf(stderr, "bad header\n"); return 2; }
  cnt = 10;
  std::vector<cov::SI> X;
  std::vector<cov::cent> all;
  for (size_t i = 0; i < cnt; ++i) {
    if (!fgets(line, sizeof line, f)) { fprintf(stderr, "short fixture\n"); return 2; }
    int v[10];
    char tail[8] = {0};
    // ten integers, each followed by exactly one space, then a newline
    if (sscanf(line, "%d %d %d %d %d %d %d %d %d %d %1s", &v[0], &v[1], &v[2], &v[3], &v[4], &v[5], &v[6], &v[7],
               &v[8], &v[9], tail) != 10) {
      fprintf(stderr, "line %zu not in the recorded format\n", i);
      return 2;
    }
    size_t L = strlen(line);
    if (L < 2 || line[L - 2] != ' ' || line[L - 1] != '\n') { fprintf(stderr, "line %zu misses its trailing space\n", i); return 2; }
    cov::SI s{};
    for (int j = 0; j < 5; ++j) s.p.b[j] = v[j];
    s.p.s = v[5];
    X.push_back(s);
    all.push_back(cov::cent{int(i), {v[6], v[7], v[8], v[9]}});
  }
  fclose(f);
  cov::writeCenters(argv[2], nn, X, all);
  // rebuild the expected bytes from the fixture itself
  char hdr[64];
  snprintf(hdr, sizeof hdr, "%d %zu\n", nn, cnt);
  std::string exp = hdr;
  f = fopen(argv[1], "rb");
  if (!fgets(line, sizeof line, f)) return 2;
  for (size_t i = 0; i < cnt; ++i) {
    if (!fgets(line, sizeof line, f)) return 2;
    exp += line;
  }
  fclose(f);
  f = fopen(argv[2], "rb");
  if (!f) { perror("out"); return 2; }
  std::string got;
  int c;
  while ((c = fgetc(f)) != EOF) got.push_back(char(c));
  fclose(f);
  if (got != exp) {
    size_t d = 0;
    while (d < got.size() && d < exp.size() && got[d] == exp[d]) ++d;
    fprintf(stderr, "FAIL: first differing byte %zu (got %d, want %d)\n", d,
            d < got.size() ? (int)(unsigned char)got[d] : -1, d < exp.size() ? (int)(unsigned char)exp[d] : -1);
    return 1;
  }
  printf("PASS: %zu centre lines byte-identical, sha256 of the 11-line file follows\n", cnt);
  printf("lines %zu bytes\n", got.size());
  return 0;
}
