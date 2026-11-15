#!/usr/bin/env python3
"""N = 112: every constraint on the seed-cover bin count, and the cost curve.
(member m3, team T5).  Run:  python3 experiments/m3/n112.py
"""
import csv, os
from math import comb, sqrt, ceil, floor

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, os.pardir, os.pardir, "data", "m3"))
R = 0.032
N0 = 112

def pr(*a): print(*a)
def C(N, k=4): return comb(N + k, 5)

pr("=" * 78)
pr("1. The paper's quoted counts (mub6.txt 7.3) -- recomputed")
pr("=" * 78)
pairs0, tails0 = comb(116, 5), comb(115, 4)
pr(f"  C(116,5) = {pairs0:,}   (paper: 160,389,488)   ok={pairs0 == 160389488}")
pr(f"  C(115,4) = {tails0:,}    (paper: 6,913,340)     ok={tails0 == 6913340}")
pr(f"  C(116,5) < 2**31 ? {pairs0 < 2**31};  2**31 = {2**31:,}")

pr(); pr("=" * 78); pr("2. The three constraints on N"); pr("=" * 78)
def N_min_pack(R=R):
    N = 1
    while 1.5 / N >= R: N += 1
    return N
Nlo = N_min_pack()
pr(f"(a) fresh-centre radius  sqrt(9)/(2N) = 1.5/N must be < R = {R}")
pr(f"    1.5/R = {1.5/R:.4f}  ->  N >= {Nlo}   (N={Nlo-1}: 1.5/{Nlo-1} = {1.5/(Nlo-1):.6f} >= R)")
N = 1
while C(N + 1) < 2**31: N += 1
Nhi32 = N
pr(f"(b) C(N+4,5) < 2**31  ->  largest N = {Nhi32}")
pr(f"    C({Nhi32+4},5) = {comb(Nhi32+4,5):,} < 2**31 = {2**31:,}")
pr(f"    C({Nhi32+5},5) = {comb(Nhi32+5,5):,} > 2**31")
pr(f"    at N={N0}: C(116,5) = {pairs0:,} is {pairs0/2**31:.3%} of the limit")
Nhi8 = 128
pr(f"(c) five-coordinate bin difference <= N-1 must fit int8_t (127)  ->  N <= {Nhi8}")
pr(f"    at N={N0}: N-1 = {N0-1}, slack {127-(N0-1)} ({(127-(N0-1))/127:.1%} of the type range)")
pr(f"    at N={Nhi32}: N-1 = {Nhi32-1} > 127  -> int8_t overflow")
pr(f"    (9*(N-1)^2 = {9*(Nhi32-1)**2:,} still fits int32; the int32 sum is not the limit.)")
pr(f"    WINDOW from documented types: [{Nlo}, {Nhi8}]   (paper's reasoning alone: [{Nlo}, {Nhi32}])")
pr("(d) gap filter (2.8): t_x = 1-(l-1)/N , t_y = 1-(l+2)/N")
pr("    t_x - t_y = 3/N = 3w exactly, for every N and l; Lemma 2.5/2.6 perturbation = w.")
pr("    ratio = 3.000 for every N  -> this filter does not pin N (3x slack at every N).")

def reach(N): return sqrt((N * R) ** 2 - 1e-4) - 1.5
def count_offsets(m2):
    if m2 < 0: return 1
    f = [[0] * (m2 + 1) for _ in range(10)]
    f[0][0] = 1
    for j in range(1, 10):
        for s in range(m2 + 1):
            t, x = 0, 0
            while x * x <= s:
                t += (1 if x == 0 else 2) * f[j - 1][s - x * x]
                x += 1
            f[j][s] = t
    return sum(f[9][s] for s in range(m2 + 1))
pr(); pr("(e) reuse reach: the crude test (2.18) certifies a bin at integer offset k = N(u-u')")
pr("    exactly when (|k| + 1.5) <= sqrt((NR)^2 - 1e-4).")
for N in (47, 56, 64, 78, 96, 109, 110, 112, 128, 160, 189, 224):
    rr = reach(N); m2 = int(floor(rr * rr)) if rr > 0 else -1
    pr(f"      N={N:4d}  NR-1.5 = {N*R-1.5:7.4f}  |k|max = {rr:6.3f}  m2={m2:3d}  offsets={count_offsets(m2):8d}")
N_reach2 = min(N for N in range(1, 400) if reach(N) >= 2.0)
pr(f"    smallest N with a two-step offset usable: N = {N_reach2}")
pr(f"    (#{{|k|<=1}} = {count_offsets(1)}, #{{|k|^2<=4}} = {count_offsets(4)}, ratio {count_offsets(4)/count_offsets(1):.0f}x)")

pr(); pr("=" * 78); pr("3. Cost curve, calibrated on the recorded run (Table 1)"); pr("=" * 78)
PAIRS_OBS, CENTRES_OBS = 151744086, 249878
T_COVER, T_A = 621.59, 2020.32
c_pair, c_seed = T_COVER / PAIRS_OBS, T_A / CENTRES_OBS
pr(f"  recorded: {PAIRS_OBS:,} pairs -> {CENTRES_OBS:,} centres  (retention {CENTRES_OBS/PAIRS_OBS:.4%})")
pr(f"  unit costs from 7.5: {c_pair*1e6:.3f} us/pair (cover), {c_seed*1e3:.3f} ms/seed (Stage A)")
m2_112 = int(floor(reach(112) ** 2)); n112 = count_offsets(m2_112)
kappa = (PAIRS_OBS / CENTRES_OBS - 1) / n112
pr(f"  reuse model  centres = pairs/(1+n(N)kappa),  kappa = {kappa:.4f} (calibrated at N=112)")
rows = []
for N in (47, 48, 56, 64, 80, 96, 109, 110, 112, 120, 128, 160, 189, 224):
    P = C(N); pairs = PAIRS_OBS * P / pairs0
    rr = reach(N); m2 = int(floor(rr * rr)) if rr > 0 else -1
    n = count_offsets(m2)
    cen_mid = pairs / (1 + n * kappa)
    cover = T_COVER * pairs / PAIRS_OBS
    rows.append(dict(N=N, C_N4_5=P, pairs_model=round(pairs), reach=round(rr, 4), offsets=n,
                     centres_no_reuse=round(pairs), centres_model=round(cen_mid),
                     centres_saturated=round(CENTRES_OBS), cover_s=round(cover, 1),
                     A_s_model=round(T_A * cen_mid / CENTRES_OBS, 1),
                     A_s_no_reuse=round(T_A * pairs / CENTRES_OBS, 1),
                     total_s_model=round(cover + T_A * cen_mid / CENTRES_OBS, 1)))
hdr = f"{'N':>4} {'C(N+4,5)':>13} {'pairs':>13} {'offsets':>8} {'cen(model)':>11} {'cover_s':>9} {'A_s(model)':>11} {'total_s':>10}"
pr(); pr(hdr); pr("-" * len(hdr))
for r in rows:
    pr(f"{r['N']:>4} {r['C_N4_5']:>13,} {r['pairs_model']:>13,} {r['offsets']:>8} "
       f"{r['centres_model']:>11,} {r['cover_s']:>9.1f} {r['A_s_model']:>11.1f} {r['total_s_model']:>10.1f}")
pr()
pr("  Regime I (N <= 78): no reuse possible -> centres = pairs, A cost scales with pairs.")
pr("  Regime II (N >= 110): two-step offsets reachable -> centres saturate.")
for N in (56, 112, 224):
    r = [x for x in rows if x['N'] == N][0]
    pr(f"  N={N}: pairs {r['pairs_model']:,}, cover {r['cover_s']/60:.1f} min, "
       f"A(no reuse) {r['A_s_no_reuse']/3600:.1f} h, int8 diff {N-1}, "
       f"pairs/4 shards = {r['pairs_model']/4:,.0f} ({r['pairs_model']/4/2e6:.1%} of the atlas cap), "
       f"centre ratio vs 112 = {r['pairs_model']/249878:.1f}x")
best = min(rows, key=lambda x: x['total_s_model'])
r112 = [x for x in rows if x['N'] == 112][0]
pr(f"  model minimum over the table: N={best['N']} ({best['total_s_model']} s); "
   f"N=112 is {r112['total_s_model']/best['total_s_model']-1:.1%} above it and "
   f"{r112['total_s_model']/[x for x in rows if x['N']==110][0]['total_s_model']-1:.1%} above N=110")

pr(); pr("=" * 78)
pr("4. N and R are a matched pair: N >= 3.5/R for guaranteed reuse at |k|=2")
pr("=" * 78)
pr("  Necessary for the crude reuse test: |k| + 1.5 <= NR, so a two-step offset")
pr("  (|k| = 2) is guaranteed usable only when R >= 3.5/N, i.e. N >= 3.5/R.")
for Rt in (0.03125, 0.032, 0.0323):
    nmin = 3.5 / Rt
    pr(f"    R = {Rt:.5f}: 3.5/R = {nmin:8.3f}  -> smallest multiple of 16 = {16*ceil(nmin/16)}")
pr("  So for every R in the admissible window [.03125, .032308) the rule")
pr("        N = 16 * ceil(3.5/(16 R))")
pr("  returns N = 112.  112 is stable in R, not an isolated pick.")

with open(os.path.join(DATA, "n112_window.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["quantity", "value", "note"])
    for row in [("pairs_witness", pairs0, "C(116,5)"), ("tails_witness", tails0, "C(115,4)"),
                ("N_min_packing", Nlo, "1.5/N < R"), ("N_max_int32", Nhi32, "C(N+4,5)<2^31"),
                ("N_max_int8", Nhi8, "N-1 <= 127"), ("N_two_step_reach", N_reach2, "NR-1.5 >= 2"),
                ("gap_filter_ratio", 3, "3w/w, N-free"), ("retention_obs", round(CENTRES_OBS/PAIRS_OBS, 8), "Table 1"),
                ("c_pair_us", round(c_pair*1e6, 4), "cover seconds per pair"),
                ("c_seed_ms", round(c_seed*1e3, 4), "A seconds per seed"), ("kappa", round(kappa, 5), "reuse model calibration")]:
        w.writerow(row)
with open(os.path.join(DATA, "n112_cost.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
pr(); pr(f"  wrote {DATA}/n112_window.csv and n112_cost.csv")
