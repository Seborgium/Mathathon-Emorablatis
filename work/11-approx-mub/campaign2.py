import numpy as np, sys, time, json
sys.path.insert(0,'.')
from mubopt import *
from scipy.optimize import minimize
from hadlib import obj as hobj, to_mats, d as dh

BUDGET=float(sys.argv[1]) if len(sys.argv)>1 else 5400.0
def randU(rng):
    A=rng.normal(size=(6,6))+1j*rng.normal(size=(6,6)); Q,R=np.linalg.qr(A)
    return Q*np.exp(-1j*np.angle(np.diag(R)))
def pert(U,rng,s):
    G=rng.normal(size=(6,6))+1j*rng.normal(size=(6,6)); G=(G+G.conj().T)/2
    return U@expm(1j*s*G/np.abs(G).max())
def polish(Us,betas=(1e4,1e5,1e6,1e7),iters=6000):
    best=list(Us)
    for b in betas:
        Us,_=descend(Us,b,iters=iters)
        if maxdev(Us)<maxdev(best): best=list(Us)
    return best

t0=time.time(); rng=np.random.default_rng(99)
seed=list(np.load('best5.npy')); best=(maxdev(seed),list(seed)); recs=[]
print("start",best[0],flush=True)
while time.time()-t0<BUDGET:
    for s in (1e-4,3e-4,1e-3,3e-3,1e-2,3e-2,1e-1):
        if time.time()-t0>BUDGET: break
        Us=polish([seed[0]]+[pert(seed[a],rng,s) for a in range(1,4)])
        md=maxdev(Us); recs.append(md)
        if md<best[0]-1e-13:
            best=(md,Us); np.save('best6.npy',np.array(Us)); print("hop",s,f"{md:.15f}",f"{time.time()-t0:.0f}s",flush=True)
        if md<best[0]+1e-6: print("  near",s,f"{md:.12f}",flush=True)
    # Hadamard-class start then unconstrained
    if time.time()-t0<BUDGET:
        x=rng.uniform(0,2*np.pi,3*dh*dh)
        for beta in (30.,300.,3000.):
            x=minimize(hobj,x,args=(float(beta),),method='L-BFGS-B',
                       options={'maxiter':800,'maxfun':200000,'eps':1e-7}).x
        hv=hobj(x,0.0)
        Us=polish(list(to_mats(x)))
        md=maxdev(Us); recs.append(md)
        print("hadamard start",f"{hv:.6f} -> {md:.12f}",f"{time.time()-t0:.0f}s",flush=True)
        if md<best[0]-1e-13:
            best=(md,Us); np.save('best6.npy',np.array(Us)); print("NEW BEST",f"{md:.15f}",flush=True)
print("FINAL",best[0],"n",len(recs),"lowest",sorted(recs)[:8],flush=True)
np.save('best6.npy',np.array(best[1]))
json.dump([float(v) for v in recs],open('campaign2.json','w'))
