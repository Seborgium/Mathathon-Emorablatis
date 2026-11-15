// dump_common.h -- the one text format both dumps use.  It reads only the four
// members every seed type has (b, s, g, c) and prints them in hex-float form,
// so a byte comparison of the two files is a bit comparison of every double.
#ifndef MUB_DUMP_COMMON_H
#define MUB_DUMP_COMMON_H
#include <cstdio>

template <class P>
inline void dump_seed(const P& p) {
  std::printf("%d %d %d %d %d %d %a %a %a\n", p.b[0], p.b[1], p.b[2], p.b[3],
              p.b[4], p.s, p.g, p.c[0], p.c[1]);
}
#endif
