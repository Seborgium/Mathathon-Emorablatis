"""Cap-policy audit: what the 5e6 search cap costs the certificate, and what raising it buys.

  python3 src/cap_policy.py <repo-root> <out.json>

Inputs, all measured:
  * certdata/runs/h0-stagec-probe.json  -- 23,506 records: M, |O|, |U|, steps, bins, category
  * m1's raised-cap run, .ultramath/smwguhf32/m1/runs/probe_hard{,_2}.txt -- all 163 cap-hit
    records re-run at cap 2e8, per-record steps and total wall time
  * the composition block sizes from runs/composition.json (this directory)
  * m2's fallback re-run wall time for the Stage-B re-refinement (4.93 s)
No new execution: this is arithmetic on those measurements.
"""
import sys, os, json, re

repo, outp = sys.argv[1:3]
probe = json.load(open(os.path.join(repo, 'certdata/runs/h0-stagec-probe.json')))
recs = probe['records']
CAP = 5_000_000
caps = [r for r in recs if r['category'] == 'cap']
done = [r for r in recs if r['category'] == 'nopattern']
final = [r for r in recs if r['command'].startswith('final')]
init = [r for r in recs if r['command'].startswith('batch')]
assert len(caps) == 163 and len(final) == 1127 and len(init) == 22379

def pairs(M): return M * (M - 1) // 2

# m1's raised-cap measurements
steps_hard = []
for f in ('probe_hard.txt', 'probe_hard2.txt'):
    p = os.path.join(repo, '.ultramath/smwguhf32/m1/runs', f)
    for line in open(p):
        m = re.search(r'steps(\d+)', line)
        if m:
            steps_hard.append(int(m.group(1)))
assert len(steps_hard) == 163
mx, tot = max(steps_hard), sum(steps_hard)

def cost(rs):
    P = sum(pairs(r['balls']) for r in rs)
    O = sum(r['O'] for r in rs); U = sum(r['U'] for r in rs)
    M = sum(r['balls'] for r in rs)
    return dict(records=len(rs), pairs=P, O=O, U=U, balls=M,
                entries=2 * P - O - U,
                bytes_stageB=1508 * len(rs),          # every one of these has k=4 (fine.bin histogram)
                bytes_balls=56 * M,
                bytes_excl=(2 * P + 7) // 8 + (4 * (2 * P - O - U) + 7) // 8,
                steps=sum(r['steps'] for r in rs))

A_cap = cost(caps); A_fin = cost(final); A_done = cost(done)
done_init = [r for r in done if r['command'].startswith('batch')]
assert len(done_init) == 22216
A_done_init = cost(done_init)
base = dict(# today's certificate: 23,343 records (22,216 completed initial + 1,127 fallback)
            records=len(done),
            bytes=A_done['bytes_stageB'] + A_done['bytes_balls'] + A_done['bytes_excl'],
            composition=28 + 32 * 163 + 4 * 1127 + 4 * 11838,
            fallback_cover='11,838 incidences over 515,243 inside cells; 5.49 CPU-s to re-derive (m2)',
            upstream_cover_cells=321_519_798 - 515_243,
            passes=2)
# policy: cap >= max measured -> all 22,379 initial records complete, no fallback pass
raised = dict(records=len(done_init) + len(caps),
              bytes=A_done_init['bytes_stageB'] + A_done_init['bytes_balls'] + A_done_init['bytes_excl']
                    + A_cap['bytes_stageB'] + A_cap['bytes_balls'] + A_cap['bytes_excl'],
              composition=0,
              fallback_cover='none (no fallback layer)',
              upstream_cover_cells=321_519_798 - 515_243,
              passes=1)
# producer arithmetic
extra_steps = tot - 815_000_163           # census total at the 5e6 cap for the same 163 records
rate = 68.2 / tot                          # m1: 1.925e9 steps in 68.2 s single-threaded
extra_s = extra_steps * rate
fallback_s = len(final) * 0.112            # measured Stage-C per-record rate (this directory)
stageb_s = 4.93                            # m2's fallback re-refinement wall time
headroom = {c: (c - mx) for c in (40_000_000, 100_000_000, 200_000_000)}
res = dict(cap=CAP, max_measured_steps=mx, total_measured_steps=tot,
           headroom=headroom,
           per_record_max_over_cap=mx / CAP,
           certificate_today=base, certificate_raised=raised,
           delta_bytes=raised['bytes'] + raised['composition'] - base['bytes'] - base['composition'],
           delta_records=raised['records'] - base['records'],
           producer=dict(extra_steps=extra_steps, step_rate_ns=rate * 1e9,
                         extra_seconds=round(extra_s, 1),
                         fallback_pass_seconds=round(fallback_s, 1),
                         stageb_refine_seconds=stageb_s,
                         net_seconds_saved=round(fallback_s + stageb_s - extra_s, 1)),
           checker=dict(pairs_today=A_done['pairs'],
                        pairs_raised=A_done_init['pairs'] + A_cap['pairs'],
                        entries_today=A_done['entries'],
                        entries_raised=A_done_init['entries'] + A_cap['entries'],
                        records_today=base['records'], records_raised=raised['records']))
json.dump(res, open(outp, 'w'), indent=1, sort_keys=True)

print('cap hits            %d of %d initial records' % (len(caps), len(init)))
print('at cap 2e8 (m1):    max %d steps, total %d, 68.2 s single-threaded' % (mx, tot))
print('headroom:           cap 4e7 -> %d steps spare; 1e8 -> %d; 2e8 -> %d'
      % (headroom[40_000_000], headroom[100_000_000], headroom[200_000_000]))
print('today:  %d records, 2 passes, %d B + composition %d B; fallback cover %s'
      % (base['records'], base['bytes'], base['composition'], base['fallback_cover']))
print('upstream Stage-B cover (unchanged in both policies): %d inside cells; m2\'s 35-55 CPU-min is'
      ' for the whole 321,519,798-cell layer (Bmid+Bfine+fallback), not for the fallback layer'
      % base['upstream_cover_cells'])
print('raised: %d records, 1 pass,  %d B, no composition, fallback cover %s'
      % (raised['records'], raised['bytes'], raised['fallback_cover']))
print('delta:  %+d records, %+d B' % (res['delta_records'], res['delta_bytes']))
print('producer: +%d steps = +%.1f s, saves fallback pass %.1f s + Stage-B refine %.2f s -> net %+.1f s'
      % (extra_steps, extra_s, fallback_s, stageb_s, res['producer']['net_seconds_saved']))
print('checker: pairs %d -> %d ; evidence entries %d -> %d'
      % (res['checker']['pairs_today'], res['checker']['pairs_raised'],
         res['checker']['entries_today'], res['checker']['entries_raised']))
print('wrote', outp)
