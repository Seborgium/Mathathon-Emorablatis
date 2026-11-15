"""Fidelity specification: one row per in-scope declaration.

This is the hand-written half of `reports/statements.md`.  The other half — the *elaborated type*
and the *axiom footprint* of each declaration — is produced mechanically by `audit/audit.py`
from the Lean sources, so that no row of the fidelity table can drift from what Lean actually
checked.

Field meanings
--------------
decl      fully qualified Lean name (provisional, marked `~`, for a declaration owned by a
          sibling direction and not present in this tree)
module    Lean module that must contain it ("PENDING" = not in this tree yet)
paper     paper locator
tag       status tag from `results/proof-claims.md` (M / M? / S / C / E, combinations)
quote     the paper's statement, verbatim (line breaks flattened)
binders   binder-by-binder audit: quantifier order, carriers, shared witnesses, endpoints,
          and the strength of the conclusion
changes   deliberate strengthening or weakening relative to `quote`, with the reason
code_dep  how a code-dependence was turned into a hypothesis (or "none")
owner     direction / member that states it (for rows not in this tree)
"""

SCOPE_A = "scope A (cheap deterministic core)"
SCOPE_B = "scope B (assembly implications, highest value)"

ROWS = [
# ---------------------------------------------------------------- infrastructure (this tree)
dict(
    decl="Mub6.CircDistLE", module="Mub6.Gap", paper="§2.2 (definition, Lemma 2.5)",
    tag="M", owner="m1",
    quote="[not a paper definition; the paper writes `matched to a point of another at circular "
          "distance at most delta`.  Circular distance on R/Z is the distance of a class to 0.]",
    binders="`CircDistLE x y d : Prop := exists m : Z, |x - y - m| <= d`.  Carrier: points are real "
            "representatives of classes mod 1, so no quotient and no choice of lift is needed.  "
            "Quantifier: the integer is an existential *inside* the hypothesis, one per pair.",
    changes="none (fixed reading of the paper's undefined term)",
    code_dep="none",
    note="infrastructure"),
dict(
    decl="Mub6.IsEmptyArc", module="Mub6.Gap", paper="§2.2 (definition of the gap)",
    tag="M", owner="m1",
    quote="The gap of a finite circular multiset is its largest circular gap. Equivalently, it is "
          "the greatest length of an open arc containing no point of the multiset.",
    binders="`IsEmptyArc A a L : Prop := forall x in A, forall m : Z, not (a < x - m and x - m < "
            "a + L)`.  The arc is *open* on both sides, as in the paper; a point on the boundary "
            "does not count as inside.",
    changes="carrier: `Finset R` (a finite set of classes) instead of a multiset.  The paper counts "
            "points with multiplicity, but an empty arc is empty regardless of multiplicity, and "
            "the gap, its stability and Lemma 2.6's use refer only to the underlying set of "
            "classes.  NO loss for this lemma.",
    code_dep="none",
    note="infrastructure"),
dict(
    decl="Mub6.NearMap", module="Mub6.Gap", paper="§2.2, Lemma 2.5 (hypothesis)",
    tag="M", owner="m1",
    quote="If each point of one circular multiset is matched to a point of another at circular "
          "distance at most delta, ...",
    binders="`NearMap A B d : Prop := forall y in B, exists x in A, CircDistLE x y d`.  Note the "
            "argument order: `NearMap A B d` says *B* is matched into *A*.  Only one direction of "
            "the matching is recorded; the difference form takes both directions.",
    changes="the paper speaks of a pointwise matching (a bijection of multisets); we keep only the "
            "direction actually used, which makes `isEmptyArc_transfer` stronger.  `circGap_stability` "
            "carries both directions, so it is exactly the paper's hypothesis.",
    code_dep="none",
    note="infrastructure"),
dict(
    decl="Mub6.GapLE", module="Mub6.Gap", paper="§2.2 (definition of the gap)",
    tag="M", owner="m1",
    quote="... it is the greatest length of an open arc containing no point of the multiset.",
    binders="`GapLE A t := forall a L, IsEmptyArc A a L -> L <= t`: `t` is an upper bound for the "
            "gap.  This is the form in which the gap is *used* downstream (Lemma 2.6 needs an upper "
            "bound on g_{y,mid} from a bound on g_x), so it avoids all attainment plumbing.",
    changes="predicate form of `gap A <= t`; equivalent given `circGap` (see `le_circGap`, "
            "`circGap_le`).",
    code_dep="none", note="infrastructure"),
dict(
    decl="Mub6.circGap", module="Mub6.Gap", paper="§2.2 (definition of the gap)",
    tag="M", owner="m1",
    quote="The gap of a finite circular multiset is its largest circular gap.",
    binders="`circGap A := sSup {L | exists a, IsEmptyArc A a L}`.  `sSup` of a set bounded above by "
            "1 for nonempty A; the nonempty case is the only one the paper uses (a phase multiset "
            "of a row of a Hadamard matrix has six points).",
    changes="sup over empty arcs rather than max over sorted consecutive differences.  Equivalent "
            "for finite sets (both are attained); the arc form is what the paper's proof of "
            "Lemma 2.5 manipulates.",
    code_dep="none", note="infrastructure"),
dict(
    decl="Mub6.isEmptyArc_transfer", module="Mub6.Gap", paper="§2.2, Lemma 2.5, proof",
    tag="M", owner="m1",
    quote="Take an empty open arc of length L in the first multiset. If L > 2 delta, trim delta "
          "from each end. ... Hence the second gap is at least L - 2 delta.",
    binders="`NearMap A B d -> IsEmptyArc A a L -> IsEmptyArc B (a + d) (L - 2 * d)`.  The trimmed "
            "arc is `(a + delta, a + L - delta)`, i.e. both endpoints move; the conclusion is "
            "`IsEmptyArc`, so no comparison of gaps is needed and no `L > 2 delta` case split is "
            "needed (a negative-length arc is empty vacuously).",
    changes="STRENGTHENING: the paper's step is embedded in a proof with a pointwise matching; here "
            "only `NearMap A B d` is assumed.  The paper's `L > 2 delta` case split disappears "
            "because `IsEmptyArc` is vacuous for `L <= 0` — the paper's 'nonnegativity' remark.",
    code_dep="none", note="proved"),
dict(
    decl="Mub6.gapLE_transfer", module="Mub6.Gap", paper="§2.2, Lemma 2.5 (one-sided use)",
    tag="M", owner="m1",
    quote="Lemma 2.5 bounds each gap change by w.   [Lemma 2.6, proof]",
    binders="`NearMap B A d -> GapLE A t -> GapLE B (t + 2 * d)`.  Direction check: a gap bound for "
            "`A` becomes one for `B` when `B`'s points are matched into `A`; this is the direction "
            "Lemma 2.6 uses (bound g_x, conclude about g_{y,mid}).",
    changes="none (restatement of Lemma 2.5 in upper-bound form)",
    code_dep="none", note="proved"),
dict(
    decl="Mub6.circGap_stability", module="Mub6.Gap", paper="§2.2, Lemma 2.5",
    tag="M", owner="m1",
    quote="Lemma 2.5 (Stability of circular gaps). If each point of one circular multiset is "
          "matched to a point of another at circular distance at most delta, their gaps differ by "
          "at most 2 delta.",
    binders="`A.Nonempty -> B.Nonempty -> NearMap A B d -> NearMap B A d -> |circGap A - circGap B| "
            "<= 2 * d`.  Both directions of the matching are hypotheses, matching the paper's "
            "'then interchange the two multisets'.  Nonemptiness of both is needed for `sSup` "
            "bookkeeping only (it holds for every phase multiset of a Hadamard matrix: six points).",
    changes="none.  See `isEmptyArc_transfer` for the strictly stronger one-sided form.",
    code_dep="none", note="proved"),
dict(
    decl="Mub6.IsEmptyArc.le_one", module="Mub6.Gap", paper="§2.2 (no explicit statement)",
    tag="M", owner="m1",
    quote="[implicit: a gap is a length of an arc, hence at most 1 for a nonempty multiset]",
    binders="`A.Nonempty -> IsEmptyArc A a L -> L <= 1`.  Needed only to bound the `sSup` in "
            "`circGap`.",
    changes="added infrastructure, no paper statement is affected",
    code_dep="none", note="proved"),
dict(
    decl="Mub6.circGap_le_one", module="Mub6.Gap", paper="§2.2 (no explicit statement)",
    tag="M", owner="m1",
    quote="[implicit: 0 <= gap <= 1]",
    binders="`A.Nonempty -> circGap A <= 1`.",
    changes="added infrastructure", code_dep="none", note="proved"),
# ---------------------------------------------------------------- A: owned by sibling directions
dict(
    decl="Mub6.three_mub_exists", module="Mub6.ThreeMUB", paper="Lemma 1.2", tag="M",
    owner="d3 (m2)", note=SCOPE_A,
    quote="Lemma 1.2 (Three mutually unbiased bases in dimension six). There exist three pairwise "
          "mutually unbiased orthonormal bases in C6.",
    binders="Existential over a triple of orthonormal bases of `EuclideanSpace C (Fin 6)`, no "
            "hypotheses.  'Mutually unbiased' must be stated as: for every pair r != s and all "
            "b in basis r, c in basis s, |<b,c>|^2 = 1/6 (the paper's normalisation: entries of "
            "U_r have modulus 1/sqrt 6).  Conclusion is existence of a *pairwise* unbiased triple; "
            "it does NOT assert maximality (that is Theorem 1.1's job).  The tensor decomposition "
            "C^6 = C^2 (x) C^3 is construction, not hypothesis, and the Gauss-sum computation "
            "(F* D F)_jk with values 1+2w, 2+w^2 of modulus^2 3 is the only non-immediate step.",
    changes="—",
    code_dep="none (a genuine proof; no code dependence)"),
dict(
    decl="Mub6.extendible_iff_all", module="Mub6.Hadamard", paper="Lemma 2.2", tag="M",
    owner="d3 (m2)", note=SCOPE_A,
    quote="Lemma 2.2 (Equivalences). Extendibility is invariant under row or column permutations, "
          "multiplication of rows or columns by unit scalars, complex conjugation, and "
          "transposition.",
    binders="For all H with the entries of H of modulus 1 and H H* = 6 I (Definition 2.1), and each "
            "of the five operations op, `Extendible H <-> Extendible (op H)`.  'Invariant' is an "
            "iff, not an implication: the paper's transposition proof argues reversibility "
            "explicitly.  Carrier: H must be an *exact* Hadamard matrix; the paper warns that the "
            "transposition argument does not apply to an approximate centre, so no ball/cell "
            "version may be stated here.  Row operations act on H alone (a common unitary on all "
            "four bases), so no family is a binder.",
    changes="—",
    code_dep="none"),
dict(
    decl="Mub6.expMat_Pi_rephasing", module="Mub6.Hadamard", paper="Lemma 2.3", tag="M",
    owner="d3 (m2)", note=SCOPE_A,
    quote="Lemma 2.3 (Horizontal phase representatives). The map Pi is the orthogonal projection "
          "onto the horizontal subspace. In particular, ||Pi z||_F <= ||z||_F. If two phase "
          "representatives have difference z, the second is equivalent under row and column "
          "rephasings to the first plus Pi z. This statement remains valid after arbitrary "
          "entrywise integer changes of phase representatives.",
    binders="Carrier: real 6x6 matrices with the Frobenius inner product; the horizontal subspace is "
            "{z : row sums and column sums of z are zero}.  Four conjuncts, all needed downstream: "
            "(i) range(Pi) = horizontal; (ii) Pi is idempotent and self-adjoint (together with (i) "
            "this *is* 'is the orthogonal projection'); (iii) ||Pi z||_F <= ||z||_F; (iv) for phase "
            "lifts P, Q with Q = P + z, `P + Pi z` differs from `Q` by a matrix constant on rows plus "
            "one constant on columns, i.e. by a row/column rephasing followed by an entrywise "
            "integer shift.  Conclusion (iv) is an existence of the rephasing, not an equality of "
            "matrices.",
    changes="—",
    code_dep="none"),
dict(
    decl="Mub6.frameMat_sq_singular_pair", module="Mub6.Frames", paper="Lemma 3.1", tag="M",
    owner="d2 (m4)", note=SCOPE_A,
    quote="Lemma 3.1 (Fixed frames). Let p in C^4 have unit-modulus entries, let S = sum_j p_j, and "
          "set M = (1 p). The squared singular values of M are 4 +- |S|. If |S| < 4, then "
          "M (M* M)^{-1} = (16 - |S|^2)^{-1} (4 1 - p conj S, 4 p - 1 S). Under the same condition "
          "|S| < 4, there is an orthonormal 4-by-2 matrix K with range ker M*.",
    binders="Hypothesis: |p_j| = 1 for j : Fin 4 (unit modulus, matching the phase-matrix setting). "
            "M is 4x2 with first column the all-ones vector and second column p.  'Squared singular "
            "values' are the eigenvalues of M* M, i.e. `T.singularValues i ^ 2` for the linear map of "
            "M; the conclusion is that the multiset is exactly {4 + |S|, 4 - |S|}.  The strict "
            "endpoint |S| < 4 is needed for invertibility of M* M in (3.4) and is kept as printed.",
    changes="(a) The paper's clause 'It may be constructed by completing 1/2 and the normalized "
            "residual of p by projected coordinate vectors' is a *construction*; a Lean existence "
            "statement drops it.  Recorded as a weakening of the proof-relevant content, not of the "
            "proposition.  (b) The existence of K does not actually need |S| < 4 (at |S| = 4, "
            "ker M* is 3-dimensional), but the paper's hypothesis is retained as printed rather "
            "than weakened, since (3.5) uses both facts under one condition.",
    code_dep="none"),
dict(
    decl="Mub6.norm_exclusion", module="Mub6.Exclusion", paper="Lemma 3.8", tag="M",
    owner="d2 (m4)", note=SCOPE_A,
    quote="Lemma 3.8 (Norm exclusion). A feasible completion associated to a cell must satisfy "
          "sum_{i,j=0}^{3} (|D_ij| - 1)^2 <= z^2.",
    binders="Carriers: a cell (centre, frames, the linear model D of (3.16)-(3.18)) and a feasible "
            "completion D' with Z = D' - D and ||Z||_F <= z.  'Associated to a cell' bundles the "
            "hypothesis ||D' - D||_F <= z (Lemma 3.5/(3.19)); in Lean that bound must be an explicit "
            "hypothesis, not part of a black-box predicate, or the lemma becomes vacuous.  The sum "
            "runs over the 4x4 complex block, i.e. 16 terms.  Conclusion is necessary: it excludes a "
            "completion, it does not assert one exists.",
    changes="—",
    code_dep="none (the numerical margins of the *negation* of this test live in Section A; the "
             "Lean statement is over exact arithmetic)"),
dict(
    decl="Mub6.directional_exclusion", module="Mub6.Exclusion", paper="Lemma 3.9", tag="M",
    owner="d2 (m4)", note=SCOPE_A,
    quote="Lemma 3.9 (Directional exclusion). Let y in R^20 be arbitrary, split as two pairs "
          "y_X, y_Y in R^2 and a flat part y_D in R^16, and write g = J_all^* y = (g_s, g_theta) "
          "in R^9 x R^4. Every feasible completion associated to the cell satisfies "
          "y . c_all <= R_s ||g_s|| + h ||g_theta||_1 + E_r ||D o y_D||_F + (1/2) z^2 max(0, "
          "max_{ij}(-y_{D,ij})) + (1/2) R_s^2 (||y_X|| + ||y_Y||).",
    binders="THE quantifier-order trap of §3: `y` is universally quantified FIRST and is not "
            "normalised, and the conclusion is the *necessary* inequality (3.29).  The licence for "
            "Cor. 3.10 is (a) `forall y` (not `exists y`) and (b) positive homogeneity in y.  "
            "Splitting R^20 = R^2 x R^2 x R^16 and the realification convention (complex scalar "
            "= its real and imaginary parts, in that order) are part of the carrier.  The "
            "`max(0, max_{ij}(-y_{D,ij}))` term is where the sign of the quadratic term enters.",
    changes="—",
    code_dep="`trial::certificate` (`S`): only `Asearch::testA` supplies exclusions, after the "
             "checks listed in `CodeClaims.stageA_certificate_is_necessary_test`."),
dict(
    decl="Mub6.ellipsoid_containment", module="Mub6.Ellipsoid", paper="Lemma 4.11", tag="M",
    owner="d2 (m4)", note=SCOPE_A,
    quote="Lemma 4.11 (Ellipsoid containment). For real linear maps A, B, vectors ||s|| <= r, "
          "||v|| <= q, and beta > 0, the sum A s + B v belongs to the ellipsoid "
          "{G^{1/2} w : ||w|| <= 1} whenever G >= (1+beta) r^2 A A* + (1 + 1/beta) q^2 B B*.",
    binders="Order: A, B, r, q, beta, G fixed; then FOR ALL s, v with ||s|| <= r, ||v|| <= q.  "
            "r, q are bounds, not norms.  G must be symmetric positive SEMIdefinite for G^{1/2} to "
            "exist ('holds for singular G'); the hypothesis G >= (1+beta) r^2 A A* + ... already "
            "forces G >= 0, but PSD must be a binder for `CFC.sqrt` to typecheck.  Conclusion is "
            "membership, i.e. an existential over a single w: `exists w, ||w|| <= 1 and G^{1/2} w = "
            "A s + B v`.  Stating it as a quadratic-form inequality instead would be a different "
            "(equivalent for nonsingular G, not for singular G) statement.",
    changes="—",
    code_dep="none"),
dict(
    decl="Mub6.offset_ellipsoid_bound", module="Mub6.Ellipsoid", paper="Lemma 4.12", tag="M",
    owner="d2 (m4)", note=SCOPE_A,
    quote="Lemma 4.12 (Offset ellipsoid norm bound). Let G >= 0 and U in R^k. For every "
          "gamma > lambda_max(G) and ||w|| <= 1, ||U + G^{1/2} w||^2 <= gamma (1 + U* (gamma I - "
          "G)^{-1} U). The simpler upper bound ||U|| + sqrt(lambda_max(G)) for the norm is also "
          "valid. If offsets range over a convex hull of finitely many U_sigma, it suffices to take "
          "the largest of the bounds at those offsets.",
    binders="Three separate conclusions, each needing its own declaration: (i) the squared-norm "
            "bound (4.34) for every gamma STRICTLY greater than lambda_max(G) and every w in the "
            "CLOSED unit ball; (ii) the simpler norm bound ||U|| + sqrt(lambda_max G); (iii) the "
            "convex-hull max-at-vertices statement (a max over a finite index set, not a sup).  "
            "Endpoint discipline: `gamma > lambda_max(G)` strict is exactly what makes "
            "gamma I - G invertible; gamma = lambda_max is excluded.  Conclusion (i) bounds the "
            "SQUARED norm — restating it as a bound on the norm is weaker and must be recorded.",
    changes="—",
    code_dep="none"),
dict(
    decl="~Mub6.operator_bounds", module="PENDING", paper="Lemma 5.1", tag="M",
    owner="d1 (m3); Mub6/Refine.lean is a STUB in the merged tree, so 5.1 is not yet formalised",
    note=SCOPE_A,
    quote="Lemma 5.1. Put A = I - T T*. For every x in R^36, with zeta = T* x, ||T|| <= sqrt(1 + "
          "o_P), ||A|| <= 1 + o_P, ||x||^2 <= (1 + o_P) ||zeta||^2 + ||A x||^2. These statements do "
          "not require x or the columns of T to be horizontal.",
    binders="T is the Root's tangent frame (R^{36 x k}, 0 <= k <= 10); o_P is the Root's `ort`.  "
            "The governing hypothesis is (4.4), ||T*T - I|| <= ort, which is a TWO-SIDED Gram bound: "
            "it gives both ||T||^2 <= 1 + o_P (Remark 4.2, a consequence) and T*T >= (1 - o_P) I.  "
            "Expanding, ||A x||^2 = ||x||^2 - 2||zeta||^2 + ||T zeta||^2, so the third inequality is "
            "exactly ||T zeta||^2 >= (1 - o_P)||zeta||^2, which the lower half of the Gram bound "
            "supplies.  The formal statement therefore takes hT : ||T*T - I|| <= o_P as its binder "
            "(or T*T = I, which is what the code's orthonormal eigendecomposition gives) and must "
            "add NO horizontality hypothesis on x or on the columns of T — '(4.4) has no radius or "
            "horizontality restriction', and the lemma's last sentence makes the point explicitly.",
    changes="none.  (An earlier draft of this table claimed the lemma needed an extra hypothesis "
            "T*T >= (1-o)I not present in Definition 4.1; that was WRONG — (4.4) is two-sided and "
            "the bound is part of the Root certificate.  Retracted; see reports/statements.md.)",
    code_dep="none beyond the Root certificate itself: (4.4) is a certified numerical fact about the "
             "stored frame, which enters as the binder hT."),
dict(
    decl="Mub6.StageC.distinct_labels", module="Mub6.Exclude", paper="Lemma 6.5", tag="M",
    owner="d1 (m3)", note=SCOPE_A,
    quote="Lemma 6.5 (Distinct labels). Two vectors in the same ball B_vec(v, s) with s < .1 are "
          "neither orthogonal nor mutually unbiased. Hence the twelve vectors in two further "
          "mutually unbiased orthonormal bases must occupy twelve distinct retained balls.",
    binders="Carrier trap: 'vectors' are PHASE CLASSES modulo global phase (the proof 'removes "
            "global phases' before summing e(z_j)), so the ball B_vec(v,s) must be a ball in the "
            "phase space R^6/2 pi Z, not in C^6 with global phase forgotten silently.  Hypotheses: "
            "s < 1/10, both points in the closed ball.  Conclusion: <p,q> != 0 AND |<p,q>|^2 != 1/6 "
            "(two separate negations), the paper's quantitative form being |sum_j e(z_j)| >= 6 - "
            "2 pi sqrt 6 ||z|| > 6 - 0.4 pi sqrt 6 > sqrt 6 for ||z|| <= 2s < 0.2.  The 'hence "
            "twelve distinct balls' clause is a pigeonhole corollary over a 12-element index set, "
            "not part of the analysis.",
    changes="—",
    code_dep="none"),
# ---------------------------------------------------------------- B: owned by sibling directions
dict(
    decl="Mub6.AssemblyCover.prop_2_10", module="Mub6.AssemblyCover", paper="Proposition 2.10", tag="M + S + C",
    owner="d1 (m3)", note=SCOPE_B,
    quote="Proposition 2.10 (Exhaustive seed cover). For a completed execution of the specified "
          "covout traversal under the arithmetic conditions of Section A, the written rational "
          "midpoint centers, each with its recorded selected position, cover the seed coordinates "
          "of every exact complex Hadamard matrix up to the equivalences of Lemma 2.2, by closed "
          "Euclidean balls of radius 0.032. After the indicated column ordering and conversion of "
          "the centers to binary phase values, radius 0.0320001 is sufficient.",
    binders="Quantifier order is the whole content: FOR EVERY exact Hadamard H THERE EXIST (an "
            "equivalence Phi from Lemma 2.2, a retained centre c WITH its recorded selected "
            "position s) such that ||seed(Phi H) - c|| <= 0.032, the ball CLOSED and Euclidean in "
            "the nine seed coordinates, and the seed extraction using the same selected position s "
            "as the centre records.  `exists Phi forall H` is false-as-stated and is the classic "
            "mis-transcription.  Second conclusion: radius 0.0320001 after binary conversion (a "
            "separate inequality, a *larger* radius, so a weaker statement that must not replace "
            "the first).  'Completed execution' is a C-hypothesis; 'the tuple is present in the "
            "stated enumeration' is an S-hypothesis (`CodeClaims.covout_visits_all_tuples`).",
    changes="—",
    code_dep="`covout_visits_all_tuples`, `seeds_mk_selection_rule`, `sumok_restricted_directions_"
             "sound`, `extend_dropping_sound`, `supdual_margins_sound` (all `S`), plus the C-event "
             "`TerminalConditions`."),
dict(
    decl="Mub6.AssemblyCover.prop_3_11", module="Mub6.AssemblyCover", paper="Proposition 3.11", tag="M + S + C",
    owner="d1 (m3)", note=SCOPE_B,
    quote="Proposition 3.11 (Completion coverage conditional on successful termination). Fix a seed "
          "ball for which the frame and bound constructions are certified. Suppose that every final "
          "unitary cell is either excluded by a certified necessary-condition test or covered by a "
          "certified phase ball as in Section 4. Then those phase balls cover all feasible Hadamard "
          "completions of the seed ball, with the equivalences specified by the phase-ball "
          "certificates.",
    binders="Hypothesis is a universally quantified disjunction over the FINAL cells of a finite "
            "tree, not over a set of points; the conclusion quantifies over feasible completions "
            "and produces a covering ball that depends on the completion.  Two hypotheses that the "
            "prose leaves implicit and Lean must state: (a) every cell's closed children cover it "
            "(this is what makes the tree induction valid), (b) the exclusions are by NECESSARY "
            "tests.  'With the equivalences specified by the phase-ball certificates' is a relation "
            "supplied per ball; a Lean statement must fix that relation explicitly (global phase "
            "only, in the paper's usage) rather than leave it as a black box.",
    changes="—",
    code_dep="`stageA_system_matches_equations`, `stageA_certificate_is_necessary_test`, "
             "`stageA_terminates_fully_resolved` (`S` + C)."),
dict(
    decl="Mub6.AssemblyCover.prop_4_16", module="Mub6.AssemblyCover", paper="Proposition 4.16", tag="M + S + C",
    owner="d1 (m3)", note=SCOPE_B,
    quote="Proposition 4.16 (Output meaning of a successful A stage). Suppose the initial seed cover "
          "is valid and the completion search processes all its seeds with no failed or unresolved "
          "seed. Then the A-stage Records cover, up to extendibility-preserving equivalence, every "
          "exact second-basis Hadamard matrix required for the four-basis problem.",
    binders="Conclusion quantifies over EXTENDIBLE exact Hadamard matrices ('required for the "
            "four-basis problem'), not over all exact H: stating it for all H is a strengthening "
            "that must be recorded.  'Up to extendibility-preserving equivalence' is the group of "
            "Lemma 4.7 (signed row/column permutation, optional transpose, global sign) acting on "
            "H; the Lean statement needs that group as data, and needs the transport lemma 4.7 to "
            "keep extendibility inside the group action.  'Cover' means: the equivalence class "
            "meets the solution set {e(P+delta) : delta horizontal, ||delta|| <= r, F(P+delta)=0} of "
            "some Record.",
    changes="—",
    code_dep="`patch_certifies_root_data` (`S + C`), `completion_search_processes_all_seeds` "
             "(`S + C`)."),
dict(
    decl="Mub6.AssemblyCover.prop_5_7", module="Mub6.AssemblyCover", paper="Proposition 5.7", tag="M + S + C",
    owner="d1 (m3)", note=SCOPE_B,
    quote="Proposition 5.7. Suppose Stage B is run on a finite list of records with valid Root "
          "certificates, under the arithmetic assumptions and error bounds of Section A. On a "
          "completed run, let A be its final atlas of children and let B be the list of input "
          "parents whose refinement failed. Then the union over input (P,R) of S(P,R) is contained "
          "in the union over (Q,r) in A of S(Q,r) union the union over (P,R) in B of S(P,R).",
    binders="Two traps. (1) The B-list appears on the right with the INPUT radius R, not with the "
            "refined radius tau: 'union_{(P,R) in B} S(P,R)'.  Writing S(P,tau) there (or dropping "
            "the B term) changes the proposition. (2) 'blocker is only ever an already completed "
            "parent' — the induction is on the order of COMPLETED parents, so the Lean statement "
            "needs the insertion order as data and the invariant 'every successful parent sphere is "
            "covered by the current atlas' as the induction hypothesis.  A is the final atlas of "
            "children, so its radii are already bounded by tau.",
    changes="—",
    code_dep="`stageB_threshold_protocol` (`S`), `stageB_no_bad_parents` (`S + C` for the "
             "corollary), `TerminalConditions`."),
dict(
    decl="Mub6.AssemblyCover.prop_6_9", module="Mub6.AssemblyCover", paper="Proposition 6.9", tag="M + S + C",
    owner="d1 (m3)", note=SCOPE_B,
    quote="Proposition 6.9 (Local exclusion certificate). Assume the root certificate (6.1)-(6.2) "
          "and the arithmetic guarantees of Section A. If Stage C returns a negative result for the "
          "Record, then no exact Hadamard e(P + delta) in its closed horizontal radius-r ball can be "
          "extended, together with the coordinate basis, by two further mutually unbiased "
          "orthonormal bases.",
    binders="Carrier: the Record's solution set is {e(P+delta) : delta HORIZONTAL (Pi delta = "
            "delta), ||delta|| <= r (closed), F(P+delta) = 0 (exact)}.  Conclusion is a negative "
            "existence statement: there are no two further orthonormal bases each unbiased to the "
            "standard basis and to e(P+delta)/sqrt 6, and mutually unbiased to each other.  "
            "'Returns a negative result' must be an explicit outcome constructor "
            "(negEmptyBin | negGraphSearch), NOT a Boolean: an unresolved/failed outcome is not a "
            "negative result, and a Bool formalisation would silently equate the two.  Strictness: "
            "the ball is closed (||delta|| <= r), so boundary points are included.",
    changes="—",
    code_dep="`graph_search_false_is_a_certificate`, `stageC_clustering_complete`, "
             "`stageC_negative_paths_only` (`S`)."),
dict(
    decl="Mub6.AssemblyCover.theorem_7_1", module="Mub6.AssemblyCover", paper="Theorem 7.1", tag="C",
    owner="d1 (m3)", note=SCOPE_B,
    quote="Theorem 7.1 (Finite-execution certificate). Use the seven specified source files and the "
          "arithmetic conditions of Appendix A. Suppose the invocations in Section 7.2 meet all of "
          "its terminal conditions, with the record provenance and batch checks stated there. Then "
          "four mutually unbiased orthonormal bases in C6 do not exist.",
    binders="Three hypotheses of three different kinds, all of which must be binders and none of "
            "which may be a proof obligation discharged internally: (1) the seven source files ARE "
            "the programs described — usable content only through the `CodeClaims` fields, since "
            "the files are not in the packet; (2) the arithmetic contract of Appendix A (the "
            "binary64 error model), which is an assumption about a computation, not a theorem about "
            "reals; (3) the terminal conditions of §7.2 — bookkeeping about a run's output, typed "
            "here as `TerminalConditions r`.  Conclusion: no four pairwise MUBs in C^6, i.e. a "
            "negative existence statement.  NOTE: Theorem 7.1 does not give N(6) = 3 on its own; "
            "the lower bound is Lemma 1.2.",
    changes="—",
    code_dep="all `CodeClaims` fields plus `TerminalConditions`; the Appendix-A arithmetic contract "
             "is a further binder (`arith`), status S."),
# ---------------------------------------------------------------- hypothesis equipment (this tree)
dict(
    decl="Mub6.RunReport", module="Mub6.Hypotheses", paper="§7.2, §7.5", tag="S + E",
    owner="m1", note="hypothesis equipment for scope B",
    quote="[§7.2 terminal conditions, as reported by the programs; §7.5 Table 1]",
    binders="A record of the run's bookkeeping: exit statuses, bad-list sizes, initial-C record "
            "count, graph-cap failures, fallback input size, final-C shard counts, unresolved count, "
            "and the two Boolean checks (provenance, fallback-coverage).  Field types are the "
            "weakest that carry the checks: integers and naturals, no floats (the arithmetic model "
            "is a separate binder).",
    changes="added: the paper's prose conditions become data.  Which records were processed is NOT "
            "represented (that needs record identities, an `S` claim).",
    code_dep="n/a — this is the type of the C-hypothesis"),
dict(
    decl="Mub6.TerminalConditions", module="Mub6.Hypotheses", paper="§7.2 (five terminal conditions)",
    tag="C", owner="m1", note="hypothesis equipment for scope B",
    quote="[§7.2: normal builds and a complete centre file; four A exits 0 with empty bad files; two "
          "B exits 0 with zero-count bad files; each initial C batch processed once with consistent "
          "counts; fallback covers every initial failure and the four final C shards partition the "
          "fallback records]",
    binders="A conjunction, in the paper's order, of decidable conditions on a `RunReport`.  The "
            "partition identity is `sum_i finalC i = fallbackInput`; coverage of the failures is the "
            "Boolean flag, since the record identities are not modelled.  Consumed as the C-binder "
            "of Theorem 7.1.",
    changes="the 'processed once with consistent counts' condition is weakened to the counting "
            "content + `driver_bookkeeping_identifies_records`; the identity content is an S-claim "
            "and is carried there.  Recorded in reports/statements.md.",
    code_dep="n/a — this is the C-hypothesis itself"),
dict(
    decl="Mub6.table1_consistent", module="Mub6.Hypotheses", paper="§7.5, Table 1", tag="E",
    owner="m1", note="hypothesis equipment for scope B",
    quote="[Table 1: 62,470 + 62,470 + 62,469 + 62,469 = 249,878; 764 + 774 + 757 + 788 = 3,083; "
          "88 batches = 87*256 + 107 = 22,379; 282 + 282 + 282 + 281 = 1,127]",
    binders="Four closed arithmetic identities, no hypotheses.  They check the bookkeeping of the "
            "reported run, not the run.",
    changes="added (an accuracy check, not a paper claim)",
    code_dep="n/a — E-status data, checked arithmetically"),
dict(
    decl="Mub6.table1_has_terminal_shape", module="Mub6.Hypotheses", paper="§7.5, Table 1; §7.2",
    tag="E", owner="m1", note="hypothesis equipment for scope B",
    quote="[the Table 1 counts, fed through TerminalConditions]",
    binders="`TerminalConditions` holds for the published counts with all exit statuses 0, empty "
            "bad lists and both flags true.  This is a SHAPE check: it shows the §7.2 contract is "
            "satisfiable by the published arithmetic.  It does not and cannot show that the run "
            "satisfied it — the provenance flags and bad-list sizes are inputs here, not outputs.",
    changes="added (consistency check of the hypothesis, not of the run)",
    code_dep="n/a — the C-hypothesis is assumed, not derived"),
dict(
    decl="Mub6.CodeClaims", module="Mub6.Hypotheses", paper="§§2–6, §7.2 (the `S` claims)",
    tag="S", owner="m1", note="hypothesis equipment for scope B",
    quote="[the `S`-tagged claims of results/proof-claims.md: what a named routine does, evidence "
          "the (unavailable) source]",
    binders="18 named `Prop`-valued fields, one per code-behaviour claim, each with its locator and "
            "the proposition that consumes it.  Carrying them as an explicit structure means no "
            "theorem can use a code claim without naming it in its binders.  The fields are `Prop` "
            "by design: typing them concretely would require the record identities and data formats "
            "of the authors' programs, which are not in the packet — typing them would be inventing "
            "a specification, which is exactly what the project forbids.",
    changes="added: the S-claims become binders.  This is the mechanism required by the brief "
            "('code-dependent statements must be represented as explicit hypotheses, never as proved "
            "facts').",
    code_dep="n/a — this IS the code-dependence ledger"),

# ---------------------------------------------------------------- interface conformance (merged tree)
dict(
    decl="Mub6.Cover.Cert.covered", module="Mub6.Interface", paper="Props 2.10, 3.11, 5.7 (inner part), 6.9",
    tag="M", owner="d1 (m3)", note="interface conformance",
    quote="[the paper's four coverage propositions share one induction: a certified finite "
          "decomposition of a region whose leaves are either excluded (disjoint from the target "
          "set) or contained in one ball covers the region]",
    binders="`Cert mem Ball T S` is an inductive with four constructors: empty, excl (Disjoint T S), "
            "ball (S contained in one member of the family), union (a finite exhaustive "
            "decomposition, with the children's covering of the parent as a HYPOTHESIS of the "
            "constructor).  `Cert.covered` concludes Covered mem Ball (T inter S).  This is exactly "
            "where the paper's 'children's closed intervals cover the parent' and 'the exclusion is "
            "by a necessary test' belong: they are constructor arguments, never proof obligations of "
            "the assembly.",
    changes="—",
    code_dep="none: the S + C half of each proposition is the existence of a `Cert`, supplied per "
             "instance (see the `CodeClaims` rows for the corresponding claims)."),
dict(
    decl="Mub6.Cover.accumulate_covered", module="Mub6.Interface", paper="Proposition 5.7",
    tag="M", owner="d1 (m3)", note="interface conformance",
    quote="[Prop 5.7: the blocker induction — a blocker is only ever an already completed parent]",
    binders="Parents as a `List P` in program order; `atlas l` is the atlas after the prefix `l`; "
            "hypotheses are append-only growth (`hatlas_mono`) and the step `hstep` (a non-failed "
            "parent is covered at the atlas current when its processing completes).  The conclusion "
            "is (5.26) restricted to the non-failed parents.  The 'no circularity' remark of the "
            "paper is the shape of `hstep`; the failed list is handled by `failed` and the "
            "one-sided growth assumption.",
    changes="—",
    code_dep="stageB_no_bad_parents (`S + C`) when the failed list is assumed empty (Cor. 5.8)."),
dict(
    decl="Mub6.AssemblyCover.seed_radius", module="Mub6.AssemblyCover", paper="Proposition 2.10 (proof), §2.2",
    tag="M", owner="d1 (m3)", note="interface conformance",
    quote="Its distance from any point of its full nine-dimensional bin is at most sqrt9/(2N) = "
          "3/224 < 0.032.",
    binders="A closed arithmetic identity and one strict inequality: sqrt 9 / (2*112) = 3/224 and "
            "3/224 < 0.032.  This is the ONLY numerical constant in the seed cover, and it is the "
            "one the paper compares with 0.032; the formal check confirms the strict inequality.",
    changes="—",
    code_dep="none"),
dict(
    decl="Mub6.gap_stability", module="Mub6.Seed", paper="Lemma 2.5 (list form)",
    tag="M", owner="d3 (m2)", note="interface conformance",
    quote="Lemma 2.5 (Stability of circular gaps), in the sorted-list carrier of §2.2: x, y "
          "nondecreasing representatives with x_0 = y_0 = 0, all entries < 1, a permutation sigma "
          "with circularDist (x i) (y (sigma i)) <= delta.",
    binders="Six hypotheses (Monotone, first entry 0, entries < 1, a permutation, and the pointwise "
            "circular-distance matching) plus |seedGap x - seedGap y| <= 2 delta, where seedGap is "
            "the max of the six consecutive arcs including the wrap arc 1 - x_5.  It is a "
            "restatement of `Mub6.circGap_stability` in a sorted-list carrier.",
    changes="see `Mub6.circGap_stability`: the arc form needs NO sortedness, NO first-entry "
            "normalisation and no permutation (the paper's own remark: 'No preservation of the "
            "sorted order is used').  The sorted-list form is a specialisation.",
    code_dep="none"),
dict(
    decl="Mub6.AssemblyCover.theorem_1_1", module="Mub6.AssemblyCover", paper="Theorem 1.1 (upper bound half)",
    tag="C", owner="d1 (m3)", note="interface conformance",
    quote="Theorem 7.1 ... Then four mutually unbiased orthonormal bases in C6 do not exist.",
    binders="The composition: seven `Cov` links (seed cover, A, B mid, B fine, initial C, fallback, "
            "final C) along an equivalence `emb` that preserves extendibility, plus the negative "
            "conclusion at every final record, imply no extendible point of H.  `theorem_1_1` adds "
            "the four-basis witness `exists x in H, ext x` and concludes False.  Note what is NOT "
            "here: the §7.2 bookkeeping (record identity, digests, counts).  It is absorbed into the "
            "hypothesis that the seven sets are linked by `Cov`; the bookkeeping premise that makes "
            "those links true is `CodeClaims.driver_bookkeeping_identifies_records`.",
    changes="—",
    code_dep="all `CodeClaims` fields; `TerminalConditions` is the typed form of §7.2's bookkeeping "
             "half and is designed to be the concrete witness for the `Cov` links."),
]
