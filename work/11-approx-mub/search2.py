import numpy as np, json, sys, time
sys.path.insert(0,'.')
from mubopt import *

def randU(rng):
    A=rng.normal(size=(6,6))+1j*rng.normal(size=(6,6)); Q,R=np.linalg.qr(A)
    return Q*np.exp(-1j*np.angle(np.diag(R)))
def pert(U,rng,s):
    G=rng.normal(size=(6,6))+1j*rng.normal(size=(6,6)); G=(G+G.conj().T)/2
    return U@expm(1j*s*G/np.abs(G).max())

def polish(Us,betas=(3e1,3e2,3e3,3e4,3e5,3e6)):
    best=Us
    for b in betas:
        Us,_=descend(Us,b,iters=4000)
        if maxdev(Us)<maxdev(best): best=Us
    return best

seed=np.load('best_hard.npy')
rng=np.random.default_rng(11)
best=(maxdev(list(seed)),list(seed)); t0=time.time(); out=[]
# 1) basin hopping around best
for k in range(120):
    s=[0.003,0.01,0.03,0.1,0.3][k%5]
    Us=[seed[0]]+[pert(seed[a],rng,s) for a in range(1,4)]
    Us=polish(Us); md=maxdev(Us); out.append(("hop",s,md))
    if md<best[0]: best=(md,Us); np.save('best2.npy',np.array(Us)); print("new best hop",k,s,f"{md:.12f}",f"t={time.time()-t0:.0f}s",flush=True)
print("hop phase best",best[0],flush=True)
# 2) structured seeds: tetrahedral product, 3 MUBs + random
T=list(np.load('tetra_u.npy'))
for k in range(40):
    s=[0.02,0.05,0.1,0.2,0.4][k%5]
    Us=[T[0]]+[pert(T[a],rng,s) for a in range(1,4)]
    Us=polish(Us); md=maxdev(Us); out.append(("tetra",s,md))
    if md<best[0]: best=(md,Us); np.save('best2.npy',np.array(Us)); print("new best tetra",k,s,f"{md:.12f}",flush=True)
print("tetra phase best",best[0],flush=True)
# 3) random
for k in range(80):
    Us=[np.eye(6,dtype=complex)]+[randU(rng) for _ in range(3)]
    Us=polish(Us); md=maxdev(Us); out.append(("rand",0,md))
    if md<best[0]: best=(md,Us); np.save('best2.npy',np.array(Us)); print("new best rand",k,f"{md:.12f}",flush=True)
print("FINAL",best[0],"n",len(out),"sorted tail",sorted(x[2] for x in out)[:8],flush=True)
json.dump([[a,float(b),float(c)] for a,b,c in out],open('search2.json','w'))
np.save('best2.npy',np.array(best[1]))
