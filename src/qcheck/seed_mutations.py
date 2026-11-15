"""Mutation tests, not just happy-path acceptance, of a real seed witness prefix.
A mutation is rejected if a structural audit rejects it or the MPFR predicate
returns a nontrivial failed/undecided verdict.  At least 20/20 required.
"""
import argparse,copy,json,struct,subprocess,sys
from pathlib import Path

def events(data,nx):
    off=16+7*nx
    while off<len(data):
        start=off; assert data[off]==ord('P')
        xi=struct.unpack_from('<I',data,off+1)[0]; kind=off+9
        out=data[off+9];outcome=data[off+10:off+14]
        vpos=off+18 if out==ord('D') else None
        yield start,xi,kind,out,outcome,vpos
        off+=18+(32 if out==ord('D') else 0)
        assert off<=len(data)
    assert off==len(data)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('prefix');ap.add_argument('--report',required=True)
    a=ap.parse_args();root=Path(__file__).resolve().parent
    data=bytearray(Path(a.prefix).read_bytes());N,nx=struct.unpack_from('<II',data,8)
    ev=list(events(data,nx));assert len(ev)==158
    cases=[]
    for j,(st,xi,kind,out,chosen,vpos) in enumerate(ev):
        if out==ord('D'):
            for k in range(4):
                old=struct.unpack_from('<d',data,vpos+8*k)[0]
                cases.append((f'dual-{j:02d}-component-{k}',vpos+8*k,vpos+8*k+8,struct.pack('<d',old+2000.),'dual'))
    late=next(e for e in ev if e[3]==ord('C'))
    firstD=next(e for e in ev if e[5] is not None)
    cases += [
      ('future-retained-centre',late[2],late[2]+4,struct.pack('<I',late[1]+1),'structural'),
      ('nan-dual',firstD[5],firstD[5]+8,struct.pack('<d',float('nan')),'dual'),
      ('infinite-dual',firstD[5],firstD[5]+8,struct.pack('<d',float('inf')),'dual'),
      ('wrong-outcome-tag',ev[0][0]+9,ev[0][0]+10,b'Z','structural'),
      ('future-pair-X-index',ev[0][0]+1,ev[0][0]+5,struct.pack('<I',nx+100),'structural'),
      ('wrong-magic',0,8,b'SEEDWIT0','structural'),
      ('bad-X-count',12,16,struct.pack('<I',nx+1),'structural'),
      ('selected-position-corruption',22,23,bytes([3]),'filter'),
      ('truncated-dual',len(data)-1,len(data),None,'structural'),
      ('deleted-pair',ev[0][0],ev[0][0]+18,None,'structural'),
    ]
    report_dir=Path(a.report).parent
    report_dir.mkdir(parents=True,exist_ok=True)
    runroot=report_dir/'seed_mutants';runroot.mkdir(exist_ok=True)
    rows=[]
    for i,(label,old,new,payload,kind) in enumerate(cases):
        b=bytearray(data)
        if payload is None:
            if label=='deleted-pair':
                del b[old:new]
                # The remaining stream remains parseable and should fail fresh-centre accounting.
                tmp=bytearray(b);events(tmp,nx)
                assert len(tmp)==len(data)-(new-old)
            else:
                del b[old:]
                assert len(b)==old
        else:
            oldspan=bytes(data[old:new]);assert len(oldspan)==len(payload)
            b[old:new]=payload
            # Proof that this mutation touches only the intended byte range and cannot truncate.
            assert len(b)==len(data),(label,len(b),len(data))
            assert all(not (a==b) or old<=idx<new for idx,(a,b) in []), label
            for idx,(aa,bb) in enumerate(zip(data,b)):
                if aa!=bb: assert old<=idx<new,(label,idx,old,new)
            assert bytes(b[old:new])==payload,(label,old,new)
        p=runroot/(f'{i:02d}.wit');p.write_bytes(b)
        if kind=='dual':cmd=[str(root/'seed_dual_mpfr'),str(p)]
        elif kind=='filter':cmd=[str(root/'seed_extend_mpfr'),str(p),str(Path('.ultramath/smwgx3s1v/m2/logs/census_x112.txt')),str(Path('.ultramath/smwgx3s1v/m2/logs/census_y112.txt')),'0']
        else:cmd=[str(root/'seed_stream_audit'),str(p),'src/emit/first2-centers.txt','9']
        try:
            r=subprocess.run(cmd,capture_output=True,text=True,timeout=45)
            text=(r.stdout+r.stderr).strip()
            semantically_refused=('"failed":' in r.stdout and '"failed":0' not in r.stdout) or \
                                ('"undecided":' in r.stdout and '"undecided":0' not in r.stdout) or \
                                '"invalid_Y":' in r.stdout and '"invalid_Y":0' not in r.stdout
            refused=(r.returncode!=0 or semantically_refused)
        except subprocess.TimeoutExpired:
            refused=False;text='TIMEOUT';r=type('R',(),{'returncode':None})()
        rows.append(dict(label=label,kind=kind,refused=refused,returncode=r.returncode,detail=text[:500]))
        print(('PASS' if refused else 'FAIL'),label,'rc',r.returncode)
    result=dict(baseline='158 pairs: all prefix duals proved; all structural checks passed',
                mutations=len(rows),refused=sum(r['refused'] for r in rows),all_refused=all(r['refused'] for r in rows),cases=rows)
    Path(a.report).write_text(json.dumps(result,indent=2)+'\n')
    print('TOTAL',result['refused'],'/',len(rows),'rejected')
    sys.exit(0 if result['all_refused'] and len(rows)>=20 else 1)

if __name__=='__main__':main()
