"""Structural + exact-cheap validator for the seed-cover witness stream.

This checks output integrity, previous-centre identities, self-midpoint coverage,
and exact (2.17)-(2.18) cheap reuse. Dual 2.19 checking is a separate obligation;
this program reports it rather than pretending that a v was validated.
"""
import argparse, math, struct
from fractions import Fraction
from pathlib import Path

def records(path):
    data=Path(path).read_bytes(); assert data[:8]==b'SEEDWIT1'
    N,nx=struct.unpack_from('<II',data,8); off=16
    xs=[]
    for i in range(nx):
        tag=data[off]; assert tag==0
        b=tuple(data[off+1:off+6]); s=data[off+6];off+=7
        xs.append((b,s));off+=0
    events=[]
    while off<len(data):
        tag=data[off:off+1];off+=1
        assert tag==b'P',(off,tag)
        xi=struct.unpack_from('<I',data,off)[0];off+=4
        tail=tuple(data[off:off+4]);off+=4
        kind=data[off:off+1];off+=1
        prior=struct.unpack_from('<I',data,off)[0];off+=4
        ptail=tuple(data[off:off+4]);off+=4
        v=None
        if kind==b'D':
            v=struct.unpack_from('<4d',data,off);off+=32
        events.append((xi,tail,kind,prior,ptail,v))
    return N,xs,events

def centre_key(x,tail):
    b,s=x
    return list(b[:5])+[s]+list(tail)

def check(path,centres=None,xprefix=None):
    N,xs,events=records(path)
    if centres is not None:
        centres={tuple(z) for z in centres}
    emitted=set()
    for xi,tail,kind,prior,ptail,v in events:
        assert 0<=xi<len(xs) and 0<=prior<=xi,(xi,prior)
        if centres is not None:
            assert tuple(centre_key(xs[prior],ptail)) in centres,(prior,ptail,'not a retained centre')
        assert xs[prior][1]==xs[xi][1],('selected-position mismatch',xi,prior)
        if kind==b'R':
            assert (prior,ptail)==(xi,tail)
            emitted.add(tuple(centre_key(xs[xi],tail)))
        elif kind==b'C':
            a,sa=xs[xi];cp,sp=xs[prior]
            assert sa==sp
            s=sa
            # (2.15), selected X entry moved to the start in both k vectors
            k=[a[s]-cp[s]]+[a[j]-cp[j] for j in range(5) if j!=s]+[tail[j]-ptail[j] for j in range(4)]
            lhs=sum(z*z for z in k)+sum(abs(z) for z in k)+Fraction(9,4)
            rn2=(Fraction(N)*Fraction(0.032))**2-Fraction(1,10000)
            assert lhs<rn2,(xi,tail,lhs,rn2,'cheap cover fails')
        elif kind==b'D':
            assert all(math.isfinite(z) and abs(z)<=10000 for z in v)
        else: raise AssertionError(('unknown outcome',kind))
    if centres is not None:
        assert emitted==centres,(len(emitted),len(centres),'fresh midpoint list mismatch')
    out={k:sum(1 for e in events if e[2]==k.encode()) for k in 'RCD'}
    print(dict(N=N,Xtuples=len(xs),pairs=len(events),outcomes=out,
               validated='all structural references + exact cheap covers + fresh midpoint list',
               pending='independent interval evaluation of every dual v'))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('witness');ap.add_argument('--centres');ap.add_argument('--expected-prefix')
    a=ap.parse_args()
    cs=None
    if a.centres:
        cs=[list(map(int,z.split())) for z in Path(a.centres).read_text().splitlines()[1:]]
        if a.expected_prefix:
            n=int(a.expected_prefix);cs=cs[:n]
    check(a.witness,cs)
