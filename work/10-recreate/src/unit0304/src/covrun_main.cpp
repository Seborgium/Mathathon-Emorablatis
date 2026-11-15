// covrun_main.cpp -- the frozen `covrun <out>` program (interfaces.md §2).
// argv contract: argc == 2, else abort(). environment() runs first, as upstream covout.cpp:139.
#include "../include/cover.hpp"
#include <cstdlib>
int main(int argc,char**argv){
  environment();
  if(argc!=2) abort();
  return covrun_main(argv[1],112);
}
