// covrun_capped.cpp -- test-only: same pipeline, but stops after centre index t == argv[2].
// Used by harness/verify_R2.sh --prefixcheck to compare a file prefix cheaply.
#include "../include/cover.hpp"
#include <cstdlib>
int main(int argc,char**argv){
  environment();
  if(argc!=3) abort();
  return covrun_main(argv[1],atoi(argv[2]));
}
