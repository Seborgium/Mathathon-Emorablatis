import numpy as np, sys, time
sys.path.insert(0,'.')
from scipy.optimize import minimize
from hadlib import obj, to_mats, d
rng=np.random.default_rng(int(sys.argv[1]) if len(sys.argv)>1 else 7)
N=int(sys.argv[2]) if len(sys.argv)>2 else 40
best=(9,None); t0=time.time()
try:
    x=np.load('hadbest.npy').ravel(); best=(obj(x,0.0),x.copy()); print("resume from",best[0],flush=True)
except Exception: pass
seeds=[rng.uniform(0,2*np.pi,3*d*d) for _ in range(N)]
T=np.load('tetra_u.npy'); seeds.append(np.concatenate([np.angle(T[a]) for a in range(1,4)]).ravel())
E=np.load('e2best.npy');  seeds.append(np.concatenate([np.angle(E[a]) for a in range(1,4)]).ravel())
for s,x0 in enumerate(seeds):
    x=x0.copy()
    for beta in (30.,300.,3000.,30000.):
        x=minimize(obj,x,args=(float(beta),),method='L-BFGS-B',
                   options={'maxiter':3000,'maxfun':600000,'eps':1e-7}).x
    val=obj(x,0.0)
    if val<best[0]-1e-12:
        best=(val,x.copy()); np.save('hadbest.npy',to_mats(x))
        print("seed",s,"devmax",f"{val:.12f}",f"{time.time()-t0:.0f}s",flush=True)
print("FINAL",best[0],flush=True)
