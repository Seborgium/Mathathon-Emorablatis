"""Compare instrumented replay outputs with the shipped run, byte for byte.
Run after the probe sweep: python3 src/report/h0_replay_verify.py <probe-all-dir> <saved-exec-dir>
"""
import sys, os, hashlib, json, re
probe, saved = sys.argv[1:3]
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
rows=[]
for i in range(88):
    got=os.path.join(probe,f'batch{i}','bad.bin'); exp=os.path.join(saved,'data','batches',f'bad{i}.bin')
    rows.append((f'batch{i}',os.path.exists(got),os.path.exists(exp),sha(got)==sha(exp) if os.path.exists(got) and os.path.exists(exp) else None))
for p in range(4):
    got=os.path.join(probe,f'final{p}','bad.bin'); exp=os.path.join(saved,'data',f'fb1cbad{p}.bin')
    rows.append((f'final{p}',os.path.exists(got),os.path.exists(exp),sha(got)==sha(exp) if os.path.exists(got) and os.path.exists(exp) else None))
ok=[r for r in rows if r[3] is True]; missing=[r for r in rows if r[3] is None]; bad=[r for r in rows if r[3] is False]
print(json.dumps(dict(identical=len(ok),missing=len(missing),different=[r[0] for r in bad],missing_names=[r[0] for r in missing]),indent=1))
json.dump(rows,open('certdata/runs/h0-replay-byte-compare.json','w'),indent=1)
