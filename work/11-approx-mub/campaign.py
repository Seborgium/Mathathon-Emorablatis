import numpy as np, sys, time, json
sys.path.insert(0,'.')
from mubopt import *

def randU(rng):
    A=rng.normal(size=(6,6))+1j*rng.normal(size=(6,6)); Q,R=np.linalg.qr(A)
    return Q*np.exp(-1j*np.angle(np.diag(R)))
def hard(Us,betas=(1e2,1e3,1e4,1e5,1e6,1e7),iters=6000):
    best=Us
    for b in betas:
        Us,_=descend(Us,b,iters=iters)
        if maxdev(Us)<maxdev(best): best=Us
    return best
def pert(U,rng,s):
    G=rng.normal(size=(6,6))+1j*rng.normal(size=(6,6)); G=(G+G.conj().T)/2
    return U@expm(1j*s*G/np.abs(G).max())

rng=np.random.default_rng(2024)
seed=list(np.load('best2.npy'))
best=(maxdev(seed),list(seed)); t0=time.time(); recs=[]
for k in range(60):                      # hops around current best
    s=[0.005,0.02,0.05,0.15,0.4][k%5]
    Us=hard([seed[0]]+[pert(seed[a],rng,s) for a in range(1,4)])
    md=maxdev(Us); recs.append(md)
    if md<best[0]-1e-12:
        best=(md,Us); np.save('best3.npy',np.array(Us)); print("hop new best",k,s,f"{md:.12f}",f"{time.time()-t0:.0f}s",flush=True)
print("after hops",best[0],flush=True)
for k in range(150):                     # fresh random starts
    Us=hard([np.eye(6,dtype=complex)]+[randU(rng) for _ in range(3)])
    md=maxdev(Us); recs.append(md)
    if md<best[0]-1e-12:
        best=(md,Us); np.save('best3.npy',np.array(Us)); print("rand new best",k,f"{md:.12f}",f"{time.time()-t0:.0f}s",flush=True)
print("FINAL",best[0],"n",len(recs),"lowest 10",sorted(recs)[:10],flush=True)
json.dump([float(x) for x in recs],open('campaign.json','w'))
np.save('best3.npy',np.array(best[1]))
