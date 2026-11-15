# harness/build/portable.mk -- the portable build of spec/interfaces.md §1.
#
#   make -f harness/build/portable.mk                      # gcc, -O2, monolithic TUs
#   make -f harness/build/portable.mk CXX=clang++ OUT=…     # clang
#   make -f harness/build/portable.mk MODE=modular          # team C's module tree
#   make -f harness/build/portable.mk print-config          # exact flags, for the log
#
# What "portable" fixes (spec §1): -O2, no -march=native, gcc and clang, held to
# structural equality and to the checker rather than to byte identity.
#
# Two decisions this file makes, both logged by portable.sh:
#   * -ffp-contract=off is KEPT.  The compile default is -ffp-contract=fast; on a
#     target with FMA that permits a*b+c contraction and would let a build silently
#     change bytes (determinism register item 9).  -march=native is what is dropped.
#   * the ABI/FP probe is a separate `probe` target, not part of `all`: abi-fp-probe.cpp
#     #errors on clang by design (it hard-requires GCC), so a clang `all` must not
#     depend on it.

REPO := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))../../../..)
SRC  ?= $(REPO)/.scratch/gh/upstream
MOD  ?= $(REPO)/work/10-recreate/src
OUT  ?= $(REPO)/work/10-recreate/harness/out/portable
CXX  ?= g++
MODE ?= mono
PROGS := covrun arun brun crun

PORTABLE := -O2 -ffp-contract=off -fno-fast-math
CXX17    := -std=gnu++17
WARN     := -Wall

.PHONY: all probe clean print-config modular-check

ifeq ($(MODE),mono)
TARGETS := $(addprefix $(OUT)/,$(PROGS))
all: $(TARGETS)

$(OUT)/covrun: $(SRC)/covout.cpp $(SRC)/seed.cpp | $(OUT)
	$(CXX) $(PORTABLE) $(WARN) $< -o $@
$(OUT)/arun: $(SRC)/atlas.cpp $(SRC)/patchx.cpp $(SRC)/ub.cpp $(SRC)/seed.cpp | $(OUT)
	$(CXX) $(CXX17) $(PORTABLE) $(WARN) $< -o $@
$(OUT)/brun: $(SRC)/stageB.cpp $(SRC)/atlas.cpp | $(OUT)
	$(CXX) $(CXX17) $(PORTABLE) $(WARN) $< -o $@
$(OUT)/crun: $(SRC)/stageC.cpp $(SRC)/stageB.cpp | $(OUT)
	$(CXX) $(CXX17) $(PORTABLE) $(WARN) $< -o $@
probe: $(OUT)/abi-fp-probe

$(OUT)/abi-fp-probe: $(SRC)/abi-fp-probe.cpp | $(OUT)
	$(CXX) $(PORTABLE) $(WARN) $< -o $@

else ifeq ($(MODE),modular)
# Expects team C's module tree: $(MOD)/include/*.hpp plus one .cpp per module
# (seed ub patchx atlas stageB stageC covout).  It is wired so that the portable
# build can be switched to the recreation sources without touching this file.
MODULES := seed ub patchx atlas stageB stageC covout
MODCPP  := $(addprefix $(MOD)/,$(addsuffix .cpp,$(MODULES)))
$(if $(wildcard $(MOD)/include),,$(error MODE=modular: no $(MOD)/include -- team C's units 03-09 are not in the tree yet; a modular portable build is blocked on them (CR to C). Use MODE=mono to build the published sources portably.))
$(foreach m,$(MODULES),$(if $(wildcard $(MOD)/$(m).cpp),,$(error MODE=modular: missing $(MOD)/$(m).cpp)))
all: $(addprefix $(OUT)/,$(PROGS))

$(OUT)/obj/%.o: $(MOD)/%.cpp | $(OUT)
	@mkdir -p $(OUT)/obj
	$(CXX) $(CXX17) $(PORTABLE) $(WARN) -I$(MOD)/include -c $< -o $@

$(OUT)/covrun: $(OUT)/obj/covout.o $(OUT)/obj/seed.o | $(OUT)
	$(CXX) $(PORTABLE) $^ -o $@
$(OUT)/arun: $(OUT)/obj/atlas.o $(OUT)/obj/patchx.o $(OUT)/obj/ub.o $(OUT)/obj/seed.o | $(OUT)
	$(CXX) $(PORTABLE) $^ -o $@
$(OUT)/brun: $(OUT)/obj/stageB.o $(OUT)/obj/atlas.o $(OUT)/obj/patchx.o $(OUT)/obj/ub.o $(OUT)/obj/seed.o | $(OUT)
	$(CXX) $(PORTABLE) $^ -o $@
$(OUT)/crun: $(OUT)/obj/stageC.o $(OUT)/obj/stageB.o $(OUT)/obj/atlas.o $(OUT)/obj/patchx.o $(OUT)/obj/ub.o $(OUT)/obj/seed.o | $(OUT)
	$(CXX) $(PORTABLE) $^ -o $@
else
$(error MODE must be mono or modular, not '$(MODE)')
endif

$(OUT):
	mkdir -p $@

print-config:
	@printf 'mode=%s\n' '$(MODE)'
	@printf 'cxx=%s\n' '$(CXX)'
	@printf 'src=%s\n' '$(SRC)'
	@printf 'out=%s\n' '$(OUT)'
	@printf 'flags=%s\n' '$(PORTABLE)'
	@printf 'cxx17=%s\n' '$(CXX17)'
	@printf 'march_native=no\n'

clean:
	rm -rf -- '$(OUT)'
