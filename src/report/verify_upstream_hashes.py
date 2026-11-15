"""Verify fetched mathematical source files against upstream code/extraction.json."""
import hashlib,json,os,sys
root=sys.argv[1] if len(sys.argv)>1 else '.scratch/h0/dl/verification'
ex=json.load(open(os.path.join(root,'code/extraction.json')))
rows=[]
for e in ex['files']:
 p=os.path.join(root,'saved-run/compiled-build/source',e['file'])
 data=open(p,'rb').read()
 rows.append(dict(file=e['file'],bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),
                  expected_bytes=e['bytes'],hash_matches=hashlib.sha256(data).hexdigest()==e['sha256'],
                  bytes_match=len(data)==e['bytes']))
out=dict(all_match=all(r['hash_matches'] and r['bytes_match'] for r in rows),files=rows)
json.dump(out,open('certdata/runs/h1-source-hash-check.json','w'),indent=2)
print(json.dumps(out,indent=2))
if not out['all_match']: sys.exit(1)
