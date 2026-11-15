"""H0 micro-benchmark: cost of exact/rational and high-precision arithmetic for the
seed-stage certify predicates, compared with the recorded binary64 covrun baseline.
Measures throughput only; no certificate logic is implemented or validated here.
"""
import json, time, math, random
from fractions import Fraction
import gmpy2
from gmpy2 import mpq, mpfr
import mpmath as mp

N = 112
PAIRS = 151_744_086           # from the recorded covrun log
COVRUN_SECONDS = 401.82       # measured on this VM, byte-identical centres
rng = random.Random(42)
trials = [(rng.randrange(N), rng.randrange(N), rng.randrange(N), rng.randrange(N)) for _ in range(2000)]

def timeit(fn, n):
    t0 = time.perf_counter(); fn(n); return (time.perf_counter()-t0)/n

def double_gap(n):
    # stand-in for the floating-point midpoint gap arithmetic of (2.6)
    s = 0.0
    for a,b,c,d in trials[:n]:
        x1,x5,x4,y5 = a/N,(b+55)/N,c/N,d/N
        g = 1.0-x5
        if x1 <= x5-x4 and g <= y5: s += g
    return s

def rational_gap(n):
    s = mpq(0)
    for a,b,c,d in trials[:n]:
        x1,x5,x4,y5 = mpq(a,N),mpq(b+55,N),mpq(c,N),mpq(d,N)
        g = 1-x5
        if x1 <= x5-x4 and g <= y5: s += g
    return s

def pyFraction_gap(n):
    s = Fraction(0)
    for a,b,c,d in trials[:n]:
        x1,x5,x4,y5 = Fraction(a,N),Fraction(b+55,N),Fraction(c,N),Fraction(d,N)
        g = 1-x5
        if x1 <= x5-x4 and g <= y5: s += g
    return s

xs = [mpq(i, 1000) for i in range(6)]

def mpfr_expsum(n):
    with gmpy2.context(precision=100) as ctx:
        s = mpfr(0)
        for i in range(n):
            x = xs[i % 6]
            # e(x) = exp(2*pi*i*x); real part via cos at 100 bits
            s += gmpy2.cos(2*gmpy2.const_pi()*x)
    return s

mp.mp.dps = 40

def mpmath_expsum(n):
    s = mp.mpf(0)
    for i in range(n):
        x = mp.mpf(int(xs[i % 6].numerator))/int(xs[i % 6].denominator)
        s += mp.cos(2*mp.pi*x)
    return s

out = {
 'baseline': {'pairs': PAIRS, 'covrun_seconds_this_vm': COVRUN_SECONDS,
              'microseconds_per_pair': 1e6*COVRUN_SECONDS/PAIRS},
 'python_version': __import__('sys').version.split()[0],
 'gmpy2': gmpy2.version(), 'mpmath': mp.__version__,
}
measurements = [
 ('double_gap_per_pair_us', double_gap, 2000, 1.0),
 ('gmpy2_mpq_gap_per_pair_us', rational_gap, 2000, 1.0),
 ('python_Fraction_gap_per_pair_us', pyFraction_gap, 500, 1.0),
 ('gmpy2_mpfr100_cos_per_eval_us', mpfr_expsum, 300, 1.0),
 ('mpmath_dps40_cos_per_eval_us', mpmath_expsum, 300, 1.0),
]
for name, fn, n, _ in measurements:
    us = timeit(fn, n)*1e6
    out[name] = us
    if 'per_pair' in name:
        out[name+'_extrapolated_cpu_hours_for_all_pairs'] = us*PAIRS/1e6/3600
print(json.dumps(out, indent=2))
json.dump(out, open('src/kernel/bench_h0.json','w'), indent=2)
