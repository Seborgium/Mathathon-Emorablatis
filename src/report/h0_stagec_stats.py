"""Aggregate H0 Stage-C evidence into JSON (saved logs + instrumented replay probe logs).

Usage: python3 src/report/h0_stagec_stats.py <probe-all-dir> <saved-execution-dir> <out.json>
Sources are logs only; no judgement is encoded here beyond the category names emitted by the
output-only probe build. A category of 'nopattern' is an exclusion produced by a completed graph
search; 'emptylayer' is an exclusion before graph construction; 'cap' is unresolved, not negative.
"""
import json, re, sys, glob, os, statistics

probe_dir, saved_dir, out_path = sys.argv[1:4]
rec_re = re.compile(r'REC (\d+) (\w+) bins(\d+) balls(\d+) O(\d+) U(\d+) steps(\d+)')
res_re = re.compile(r'result done(\d+) bad(\d+) \(graph(\d+) cap(\d+) over(\d+) cluster(\d+)\) time ([\d.]+)')

records = []
per_cmd = []
for d in sorted(glob.glob(os.path.join(probe_dir, '*'))):
    if not os.path.isdir(d): continue
    tag = os.path.basename(d)
    try:
        out = open(os.path.join(d, 'stdout.log')).read()
        err = open(os.path.join(d, 'stderr.log')).read()
    except FileNotFoundError:
        continue
    m = res_re.search(out)
    cats = {}
    for line in err.splitlines():
        r = rec_re.match(line)
        if not r: continue
        idx, cat, bins, balls, o, u, steps = r.groups()
        rec = dict(command=tag, index=int(idx), category=cat, bins=int(bins), balls=int(balls),
                   O=int(o), U=int(u), steps=int(steps))
        records.append(rec); cats[cat] = cats.get(cat, 0)+1
    per_cmd.append(dict(command=tag, result=list(map(float, m.groups())) if m else None,
                        categories=cats, rec_lines=sum(cats.values())))

def dist(vals):
    if not vals: return None
    vals = sorted(vals)
    return dict(n=len(vals), min=vals[0], median=statistics.median(vals), mean=round(statistics.mean(vals),2),
                p95=vals[int(.95*(len(vals)-1))], max=vals[-1], total=sum(vals))

graph_recs = [r for r in records if r['category'] in ('nopattern','cap','positive')]
def totals(rs):
    return dict(records=len(rs),
                pairs=sum(r['balls']*(r['balls']-1)//2 for r in rs),
                O_plus_U=sum(r['O']+r['U'] for r in rs),
                nonedge_reason_slots=sum(r['balls']*(r['balls']-1)//2-r['O']-r['U'] for r in rs),
                adjacency_bytes=sum(2*r['balls']*((r['balls']+63)//64)*8 for r in rs),
                steps=sum(r['steps'] for r in rs))
groups = dict(
    all=totals(records),
    initial=totals([r for r in records if r['command'].startswith('batch')]),
    final=totals([r for r in records if r['command'].startswith('final')]),
    completed_negatives=totals([r for r in records if r['category']=='nopattern']),
    capped=totals([r for r in records if r['category']=='cap']),
)
summary = dict(
    commands=len(per_cmd), records=len(records),
    groups=groups,
    categories={c: sum(1 for r in records if r['category']==c) for c in sorted({r['category'] for r in records})},
    graph_records=len(graph_recs),
    balls=dist([r['balls'] for r in graph_recs]),
    O_edges=dist([r['O'] for r in graph_recs]),
    U_edges=dist([r['U'] for r in graph_recs]),
    steps_nopattern=dist([r['steps'] for r in records if r['category']=='nopattern']),
    steps_cap=dist([r['steps'] for r in records if r['category']=='cap']),
    bins_final_layer=dist([r['bins'] for r in graph_recs]),
    stdout_wall_seconds_total=round(sum(c['result'][-1] for c in per_cmd if c['result']),2),
)
saved_totals = {}
for f in sorted(glob.glob(os.path.join(saved_dir, 'results', 'C.*.txt'))):
    txt=open(f).read()
    m=re.search(r'result done(\d+) bad(\d+) \(graph(\d+) cap(\d+) over(\d+) cluster(\d+)\)',txt)
    if not m: continue
    vals=list(map(int,m.groups()))
    for k,v in zip(('done','bad','graph','cap','over','cluster'),vals): saved_totals[k]=saved_totals.get(k,0)+v
report = dict(summary=summary, saved_log_totals=saved_totals, per_command=per_cmd, records=records)
json.dump(report, open(out_path,'w'), indent=1)
print(json.dumps(dict(summary=summary, saved_log_totals=saved_totals), indent=1))
