// c-writer.hpp -- the exact byte form of centers.txt.
//
// Provenance: covout.cpp:172, the single line
//   fprintf(f,"%d %zu\n",n,C.all.size());
//   for(auto u:C.all){auto &p=C.X[u.ix].p;for(int b:p.b)fprintf(f,"%d ",b);
//                     fprintf(f,"%d ",p.s);for(int b:u.y)fprintf(f,"%d ",b);fprintf(f,"\n");}
// Ten decimal integers per line, EACH FOLLOWED BY ONE SPACE, then "\n" -- the
// space before the newline is part of the format and appears in the recorded file.
#ifndef C_WRITER_HPP
#define C_WRITER_HPP

#include <vector>

#include "c-cover.hpp"

namespace cov {

// Writes the file at `path`; aborts on any I/O error (as the published code does,
// via ferror||fclose).  `nn` is the bin count to put in the header (112).
void writeCenters(const char* path, int nn, const std::vector<SI>& X, const std::vector<cent>& all);

}  // namespace cov
#endif
