/-
Mub6/Completion.lean — STUB.  §3, Stage A: completion coverage (Prop. 3.11).

Status: this file intentionally contains **no mathematics** in this window.  It exists so that the
import DAG of `lakefile.lean` is complete and so that the module that must hold Prop. 3.11 has a
fixed position: it may import `Mub6.Basic`, `Mub6.Frames` (m4, Lemma 3.1) and `Mub6.Interface`
(m3, the generic coverage interface), and must not import `Mub6.ThreeMUB`, `Mub6.Seed` or
`Mub6.Exclude`.

What belongs here, per reports/DEPGRAPH.md §2: the paper's cell recursion as an instance of
`Interface.Cert.covered` — every terminal cell either carries a certified necessary-test exclusion
(3.8, 3.9 / Cor. 3.10) or a certified phase ball (3.2–3.7), and the children's closed intervals
cover the parent's.  That instantiation is the step where a mis-stated induction would hide; it is
not done.
-/
import Mub6.Basic

namespace Mub6

end Mub6
