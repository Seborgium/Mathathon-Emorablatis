/-
Mub6/Assembly.lean — STUB.  §7: the finite-execution certificate (Thm. 7.1).

Status: no mathematics in this window.  Position in the DAG: the last module on the spine; it may
import everything before it, and nothing imports it.

What belongs here: the composition of Lemma 1.2 with the five coverage implications
(2.10, 3.11, 4.16, 5.7, 6.9) into Thm. 7.1, with the checker's acceptance an **explicit
hypothesis** — "the invocation list of §7.2 met its terminal conditions, with provenance and batch
checks, under the arithmetic of Appendix A" — never a proved fact.  This is the design requirement
for group (B): the paper's specific constructions instantiate a parametric interface; the
composition is proved once.  Neither the instantiation nor the composition is done here.
-/
import Mub6.Basic
import Mub6.Interface

namespace Mub6

end Mub6

/- NOTE (m3, direction d1): the parametric composition of Props 2.10, 3.11, 4.16, 5.7, 6.9 into
   Theorem 7.1 --- proved, with every S/C premise an explicit binder --- is implemented in
   `Mub6/AssemblyCover.lean`, because this file was claimed by the scaffold owner. -/
