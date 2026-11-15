"""Restricted class: U_1=I and U_2,U_3,U_4 exactly Hadamard (|entries|=1/sqrt6).
Optimise max_{a<b} dev over the 3x36 phases."""
import numpy as np
from scipy.optimize import minimize

d=6
def Hmats(th):
    # th: (3,6,6) phases -> 4 matrices, first = I
    U=[np.eye(d,dtype=complex)]
    for a in range(3):
        U.append(np.exp(1j*th[a])/np.sqrt(d))
    return U
def devmax(th, beta=0.0):
    U=Hmats(th.reshape(3,d,d)); m=0.0; vals=[]
    for a in range(4):
        for b in range(a+1,4):
            P=np.abs(U[a].conj().T@U[b])**2
            vals.append(np.abs(P-1.0/d).ravel())
    v=np.concatenate(vals)
    if beta<=0: return v.max()
    return v.max()+np.log(np.exp(beta*(v-v.max())).sum())/beta-np.log(len(v))/beta
def obj(x,beta): return devmax(x,beta)

rng=np.random.default_rng(0)
best=(9,None)
seeds=[]
# seed 1: E2 point's hadamards (phases)
E=list(np.load('e2best.npy'))
seeds.append(np.concatenate([np.angle(E[a]) for a in range(1,4)]).ravel())
# seed 2: tetrahedral construction phases (C^2 x MUB_3 is not Hadamard in d=6? |entries| = 1/sqrt2*1/sqrt3 ok)
T=list(np.load('tetra_u.npy'))
seeds.append(np.concatenate([np.angle(T[a]) for a in range(1,4)]).ravel())
for k in range(6): seeds.append(rng.uniform(0,2*np.pi,3*d*d))
for s,x0 in enumerate(seeds):
    x=x0.copy()
    for beta in (30.,300.,3000.):
        r=minimize(obj,x,args=(beta,),method='L-BFGS-B',options={'maxiter':2000,'maxfun':400000,'eps':1e-7})
        x=r.x
    val=obj(x,0.0)
    if val<best[0]: best=(val,x.copy()); print("seed",s,"devmax",f"{val:.10f}",flush=True)
print("BEST Hadamard-class max dev:",best[0])
np.save('hadbest.npy',best[1].reshape(3,d,d))
