#!/bin/sh
# Elaborate Interface.lean and report the axiom footprint of each theorem.
# Usage: sh check.sh   (needs `lean` on PATH; no Mathlib import, ~0.2 s)
set -e
tmp=".axioms.$$.lean"
cat Interface.lean > "$tmp"
cat >> "$tmp" <<'INNER'

#print axioms Mub6Assembly.assembly
#print axioms Mub6Assembly.assembly_fallback
#print axioms Mub6Assembly.refines_trans
#print axioms Mub6Assembly.excludes_of_refines
INNER
lean "$tmp"
rm -f "$tmp"
