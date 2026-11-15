#!/usr/bin/env python3
"""Defect F4 (sentinel 100 inside the valid range) and the undiscussed arithmetic
constants: .64 eigenvalue split, K = 1.00001, q_d < 3.8, beta = .45 and .8,
'at most 30' updates, '25 midpoint trials', the 1e-6 divisor skip.

Run: python3 experiments/consts.py
"""
import math


def main():
    print("=== F4: the sentinel 100 of `ell` is inside the legitimate range ===")
    print("   A.8 proves the certified spectral bound satisfies gu <= 100.1, and")
    print("   `ell` returns 100 on scale failure.  So 100 is a value a valid bound")
    print("   can take.  Safety comes from the DOWNSTREAM conversion to cycles and")
    print("   the t < 10 guard of bootstrap (s4.6):")
    print(f"   100 cycles = 100            -> passes t<10? {100 < 10}")
    print(f"   100 radians = 100/(2*pi) = {100 / (2 * math.pi):.4f} cycles "
          f"-> passes t<10? {100 / (2 * math.pi) < 10}")
    print(f"   the sentinel lands at {100 / (2 * math.pi):.4f} cycles, i.e. "
          f"{(100 / (2 * math.pi)) / 10:.4f}x the t<10 threshold:")
    print(f"   rejected by a factor of {(100 / (2 * math.pi)) / 10:.2f}, and by no more.")
    print("   So the guard is 1.59x above the sentinel value and nothing more.  If any")
    print("   threshold in that neighbourhood is retuned (t<20, or a 5 radian")
    print("   sentinel), a failure would be read as a certified tangent bound.")
    print("   Same class: bootstrap's failure sentinel 10, relationB::eval's 10.")
    for val, name in ((10.0, "bootstrap"), (10.0, "relationB::eval")):
        print(f"   {name}: legitimate quantities are radii <= .126 (s5.1) and")
        print(f"   t <= 2 (s5.6), and A.9 bounds every stored distance by .378;")
        print(f"   so {val} is {val / 0.378:.0f}x above every legitimate value.")
    print("   Recommendation: NaN with a checked isnan, or a status flag.")

    print("\n=== K = 1.00001 (s6.1, equation (6.3)) ===")
    f0 = 1e-6
    bound = math.sqrt(1 + math.pi * math.sqrt(2) / 6 * f0)
    print("   (6.3): ||A/sqrt6||_op <= sqrt(1 + (pi*sqrt2/6) f0)")
    print(f"   with f0 < 1e-6: bound = {bound:.12f}, i.e. 1 + {bound - 1:.3e}")
    print(f"   K = 1.00001 = 1 + 1e-5: slack {1.00001 - bound:.3e}, "
          f"ratio {(1.00001 - 1) / (bound - 1):.1f}")
    print(f"   the tightest admissible K is {bound:.9f}; halving to 1.000005 still")
    print(f"   holds ({bound - 1:.2e} < 5e-6).  K enters only through (6.2)'s")
    print("   r_H = sqrt(1+omega) r and the operator bound on Q, so a larger K")
    print("   inflates every single-vector test by (K-1) ~ 1e-5: harmless.")
    print("   Verdict: justified, 27x slack, and the value is 3-digit-round.")

    print("\n=== q_d < 3.8 (Lemma 4.8) ===")
    print("   the proof needs q_d < 4 for (1 - q_d/4)^(-1/2) and arcsin(c/2).")
    for q in (0.5, 1.0, 2.0, 3.0, 3.8, 3.99):
        fac = (1 - q / 4) ** -0.5
        print(f"   q_d={q:5.2f}: (1-q_d/4)^-1/2 = {fac:6.3f}"
              f"   max single chord sqrt(q_d) = {math.sqrt(q):.3f}"
              f"   {'< sqrt2' if q < 2 else '>= sqrt2'}")
    print("   Lemma 4.8's own sentence says 'in particular no individual chord")
    print("   reaches sqrt2', which needs q_d < 2, not q_d < 3.8.  The extra 1.8")
    print("   is unused headroom that makes a stated claim false in the admitted")
    print("   range.  Recommendation: restate as q_d < 2 (safe: the achieved q_d")
    print("   is not reported anywhere), or delete the sentence.")
    print("   cost of lowering to 2: records whose q_d is in [2,3.8) would fail")
    print("   the Candidate path and fall back to subdivision - more work, never")
    print("   less coverage; the run does not report any q_d, so the cost is")
    print("   unknown but bounded by the 22,379 fine records.")

    print("\n=== beta = .45 and .8 (Lemma 4.11) ===")
    print("   G >= (1+beta) r^2 AA* + (1+1/beta) q^2 BB*, for every beta > 0.")
    print("   write u = r^2||A||^2, v = q^2||B||^2; the ellipsoid only cares about")
    print("   the two coefficients.  The best beta balances them:")
    print("   beta   1+beta   1+1/beta   f(beta)= (1+b)u + (1+1/b)v at u=1")
    for b in (0.45, 0.5, 0.8, 1.0, 1.25):
        print(f"   {b:5.2f} {1 + b:8.3f} {1 + 1 / b:10.3f}     "
              f"{1 + b + (1 + 1 / b) * v_ratio(b):.3f}")
    print("   (last column assumes v/u = beta^2, the self-consistent choice)")
    print("   .45 corresponds to v/u = .2025, .8 to v/u = .64: the two choices are")
    print("   the same formula at two assumed ratios of the D-contribution to the")
    print("   seed-contribution.  Neither is justified in the paper, and both are")
    print("   safe for ANY beta > 0 - a wrong beta only inflates the bound.")
    print("   cost: at v/u = 1 the optimal beta is 1 and f = 4u; .45 gives 4.67u")
    print("   (17% larger) and .8 gives 4.05u.  Recommendation: print u, v and the")
    print("   beta used, and pick beta = sqrt(v/u).")

    print("\n=== 'at most 30 bootstrap updates' (s4.6) ===")
    print("   (4.38) replaces s by sqrt(n_P(s)^2 + (1+ort) t0^2) only when that")
    print("   decreases s, so every accepted update strictly shrinks s and the")
    print("   iteration is monotone.  30 is therefore a WORK cap, not a convergence")
    print("   claim: any finite number preserves coverage (Prop 4.13).")
    print("   size of one step: with n_P(s) = n0 + id s + C s^2, C < 20, s <= .126,")
    print(f"   the update moves s to at most sqrt((n_P(s))^2 + 1.00001 t0^2).")
    for s in (0.05, 0.103, 0.125):
        np_ = 1e-6 + 1e-4 * s + 20 * s * s
        print(f"   s={s:.3f}: n_P = {np_:.6f}; a single step can only reduce s to")
        print(f"           sqrt(n_P^2 + t0^2) which for t0 = 0.5s is "
              f"{math.hypot(np_, 0.5 * s):.4f}")
    print("   verdict: 30 is harmless and unjustified; the paper should say what")
    print("   fraction of records needed more than 1 update (not reported).")

    print("\n=== '25 midpoint trials' (s5.6) ===")
    print("   the rho search bisects [0, 1.01a] with a <= .126, accepting a trial m")
    print("   when D(m) < a - 2e-7 (5.18).  Resolution after k trials:")
    for k in (13, 17, 20, 25):
        res = 1.01 * 0.126 / 2 ** k
        print(f"   k={k:3d}: 1.01*.126/2^{k} = {res:.3e}"
              f"   {'>= tolerances' if res > 2e-7 else '< 2e-7 (converged)'}"
              f"   {'< 1e-7' if res < 1e-7 else ''}")
    need = math.log2(1.01 * 0.126 / 2e-7)
    print(f"   the smallest k with resolution below the 2e-7 tolerance is "
          f"{math.ceil(need)}.")
    print(f"   So 25 carries {2 ** (25 - math.ceil(need)):.0f}x slack over the")
    print("   tolerance: justified, and further trials buy nothing.")

    print("\n=== the 1e-6 divisor skip in extend (s2.3) ===")
    print("   'It omits divisors of magnitude below 1e-6, which only removes a")
    print("   constraint.'  Removing a constraint can only ENLARGE the intersection,")
    print("   so soundness is preserved; the cost is retained bins.")
    print(f"   at the accepted divisor |a| > .999e-6, the two quotients are bounded")
    print("   by 1.2e8 (midpoint) and 3e6 (radius), so no overflow follows.")
    for eps in (1e-3, 1e-4, 1e-6, 1e-9):
        print(f"   skip < {eps:g}: endpoint error budget 1e-7/|a| = "
              f"{1e-7 / eps:.3g}")
    print("   verdict: harmless and correctly stated.  The paper should print how")
    print("   many divisors were skipped; if the count is not small the filters are")
    print("   silently weaker than advertised.")

    print("\n=== the .64 eigenvalue split (Prop 4.6) ===")
    print("   'Eigenvalues below .64 propose columns of T; the other columns propose")
    print("   factors HV, LV for M ... more than 10 proposed T columns causes")
    print("   failure.'  Nothing in Appendix A constrains .64: it is a proposal")
    print("   heuristic, and every certificate is a direct check.")
    print("   The only quantitative requirement is on the COUNT of columns kept:")
    print("     <= 10  (Def 4.1, s5.1, s6.1)      hard validation")
    print("     <=  5  (mid pass box cap, see experiments/stage_b_widths.py)")
    print("   so .64 must cut the 25-coordinate horizontal spectrum below 5.  A")
    print("   threshold is admissible exactly when it separates the kernel (the")
    print("   k <= 5 small eigenvalues) from the bulk; the gap is not reported.")
    print("   Recommendation: print the 25 eigenvalues' five smallest and the")
    print("   adjacent gap; then .64 is justified by a number instead of a habit.")
    print("   halving to .32 keeps more columns (risk: >10, failure, more work).")
    print("   doubling to 1.28: on a unit-normalised spectrum it keeps everything")
    print("   (risk: k too large for the box cap).  Both failure modes are")
    print("   'unresolved', never 'negative', so the proof survives either.")


def v_ratio(b):
    return b * b


if __name__ == "__main__":
    main()
