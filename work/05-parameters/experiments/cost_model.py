#!/usr/bin/env python3
"""Cost curve and recommendation for the bin count N.

Inputs
  * measured pair counts P(N) for N = 48..128      (experiments/n_sweep.py)
  * the recorded run at N = 112                    (paper section 7.5, Table 1)
        151,744,086 pairs reported, 22,829 X lists, 249,878 centres,
        wall times 621.59 s (cover), 2020.32 s (A), 1823.56 s (B+C), 4470.33 s total
  * the hard windows  47 <= N <= 189                (experiments/n_window.py)

Model
  cover time        t_cov(N) = 621.59 * P(N)/P(112)        [pairs are the cover's unit of work]
  everything else   t_rest(N) = 3843.9 * K(N)/K(112)       [K = retained centres]
  centre count      K(N) = 249,878 * (P(N)/P(112)) / (N/112)**d
     d is the dimension of the pair set, fitted from the measured P(N); a ball of radius R
     in the 9-dim phase space holds (N R)^d pairs once N is fine enough, so K is the
     covering number of the pair set by R-balls and is N-independent to leading order.

Run: python3 experiments/cost_model.py
"""
import csv
import math

import numpy as np

DATA = "work/05-parameters/data"
MEAS = {48: 3_460_356, 56: 6_192_348, 64: 10_631_466, 80: 26_567_283,
        96: 57_772_973, 112: 112_160_350, 128: 200_620_232}
K112 = 249_878
P112 = MEAS[112]
T_COVER112 = 621.59
T_A112 = 2020.32
# A, B and C all scale with the centre count; the recorded total is 4470.33 s
T_REST112 = 4470.33 - T_COVER112


def fit_dim():
    ns = np.array(sorted(MEAS))
    ps = np.array([MEAS[n] for n in ns], dtype=float)
    d, b = np.polyfit(np.log(ns), np.log(ps), 1)
    return d, math.exp(b)


def main():
    d, A = fit_dim()
    print(f"measured pair counts P(N): " + ", ".join(f"{n}:{MEAS[n]:,}" for n in sorted(MEAS)))
    print(f"power-law fit: P(N) = {A:.4g} * N^{d:.3f}")
    print(f"  check at N=112: fit {A * 112 ** d:,.0f} vs measured {P112:,}")
    print()
    print(f"recorded run at N=112: {P112:,} pairs (ours), 249,878 centres -> {P112 / K112:.1f} pairs/centre")
    print(f"  (N R)^d at N=112, d={d:.2f}: {(112 * 0.032) ** d:.1f}")
    print(f"  t_rest (A + B + C) at N=112: {T_REST112:.2f} s; per centre {T_REST112 / K112 * 1e3:.2f} ms")
    print(f"  cover: {T_COVER112 / P112 * 1e6:.3f} us per pair")
    print()
    rows = []
    print(f"{'N':>4s} {'pairs P(N)':>15s} {'src':>5s} {'3/(2N)/R':>9s} {'centres K(N)':>13s}"
          f" {'t_cover s':>10s} {'t_rest s':>9s} {'total s':>9s} {'vs 112':>8s}")
    for N in (47, 48, 56, 64, 80, 96, 112, 128, 160, 189, 224):
        if N in MEAS:
            P, src = MEAS[N], "meas"
        else:
            P, src = A * N ** d, "fit"
        K = K112 * (P / P112) / (N / 112) ** d
        tcov = T_COVER112 * P / P112
        trest = T_REST112 * K / K112
        tot = tcov + trest
        rows.append(dict(N=N, pairs=P, source=src, fresh_ratio=1.5 / N / 0.032,
                         centres=K, t_cover_s=tcov, t_rest_s=trest, total_s=tot,
                         ratio_to_112=tot / (T_COVER112 + T_REST112),
                         tuples=math.comb(N + 4, 5), int32_ok=math.comb(N + 4, 5) < 2 ** 31))
        print(f"{N:4d} {P:15,.0f} {src:>5s} {1.5 / N / 0.032:9.3f} {K:13,.0f}"
              f" {tcov:10.1f} {trest:9.1f} {tot:9.1f} {tot / (T_COVER112 + T_REST112):8.3f}")
    print()
    print("=== what breaks at the requested alternatives ===")
    for N in (56, 224):
        P = MEAS.get(N, A * N ** d)
        K = K112 * (P / P112) / (N / 112) ** d
        print(f"  N={N}: tuples C(N+4,5) = {math.comb(N + 4, 5):,}"
              f" ({math.comb(N + 4, 5) / 2 ** 31:.4f} of 2^31); fresh-centre ratio 3/(2N)/R ="
              f" {1.5 / N / 0.032:.3f}; predicted centres {K:,.0f}; predicted total"
              f" {T_COVER112 * P / P112 + T_REST112 * K / K112:,.0f} s")
    print()
    print("=== the 32-bit window and the fresh-centre window ===")
    nmax = max(n for n in range(2, 400) if math.comb(n + 4, 5) < 2 ** 31)
    print(f"  C(N+4,5) < 2^31 holds up to N = {nmax}; 3/(2N) <= .032 holds from N = 47")
    print(f"  N=112 uses {100 * math.comb(116, 5) / 2 ** 31:.2f}% of the 32-bit allowance and"
          f" {100 * (3 / 224) / 0.032:.1f}% of the fresh-centre allowance")
    with open(f"{DATA}/cost_model.csv", "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wtr.writeheader()
        wtr.writerows(rows)


if __name__ == "__main__":
    main()
