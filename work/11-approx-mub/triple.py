"""Does a genuine MUB triple exist in C^6?  Then: best 4th basis given the triple."""
import numpy as np, sys, time
sys.path.insert(0,'.')
from mubopt import expm, maxdev
np.random.seed(0)
d=6
def randU(rng):
    A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)); Q,R=np.linalg.qr(A)
    return Q*np.exp(-1j*np.angle(np.diag(R)))
def pairwise(Us):
    return [np.abs(np.abs(Us[a].conj().T@Us[b])**2-1.0/d).ravel() for a in range(len(Us)) for b in range(a+1,len(Us))]
def G_of(Us, gfun):
    n=len(Us); G=[np.zeros((d,d),dtype=complex) for _ in range(n)]
    vals=[];mats=[]
    for a in range(n):
        for b in range(a+1,n):
            X=Us[a].conj().T@Us[b]; mats.append((a,b,X)); vals.append((np.abs(X)**2-1.0/d).ravel())
    v=np.concatenate(vals); g=gfun(v)
    off=0
    for (a,b,X) in mats:
        M=(g[off:off+d*d]*np.conj(X).ravel()).reshape(d,d); off+=d*d
        G[a]+=Us[b]@M.T; G[b]+=Us[a]@np.conj(M)
    out=[]
    for a in range(n):
        H=Us[a].conj().T@G[a]; out.append(H-(H+H.conj().T)/2)
    return out, np.abs(v).max()
def descend(Us,beta,iters=4000):
    def gfun(v):
        av=np.abs(v); m=av.max(); w=np.exp(beta*(av-m)); w/=w.sum(); return w*np.sign(v)
    def f(Us):
        v=np.abs(np.concatenate(pairwise(Us))); m=v.max()
        return m+np.log(np.exp(beta*(v-m)).sum())/beta
    cur=f(Us)
    for it in range(iters):
        G,_=G_of(Us,gfun); step=1.0
        while step>1e-13:
            cand=[Us[0]]+[Us[a+1]@expm(-step*G[a+1]) for a in range(len(Us)-1)]
            fc=f(cand)
            if fc<cur-1e-16: break
            step*=0.5
        else: break
        Us,cur=cand,fc
    return Us
rng=np.random.default_rng(1)
best=(9,None)
for s in range(10):
    Us=[np.eye(d,dtype=complex)]+[randU(rng) for _ in range(2)]
    for beta in (30.,300.,3000.,3e4,3e5):
        Us=descend(Us,beta)
    md=max(abs(x).max() for x in pairwise(Us))
    print("3-basis start",s,"maxdev",f"{md:.10f}",flush=True)
    if md<best[0]: best=(md,Us)
print("TRIPLE: best maxdev",best[0],flush=True)
np.save('triple3.npy',np.array(best[1]))
if best[0]<1e-6:
    print("MUB triple found; now best 4th basis",flush=True)
    T=list(np.load('triple3.npy')); best4=(9,None)
    for s in range(15):
        Us=T+[randU(rng)]
        for beta in (30.,300.,3000.,3e4,3e5):
            Us=descend(Us,beta)
        md=maxdev(Us)
        if md<best4[0]: best4=(md,Us); np.save('triple_plus1.npy',np.array(Us)); print("  4th basis dev",f"{md:.10f}",flush=True)
    print("BEST triple completion:",best4[0],flush=True)
