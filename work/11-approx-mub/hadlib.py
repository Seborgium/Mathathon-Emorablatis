"""Hadamard-class objective: U_1=I, U_2..U_4 exactly Hadamard (|entries|=1/sqrt6)."""
import numpy as np
d=6
def Hmats(th):
    U=[np.eye(d,dtype=complex)]
    for a in range(3):
        U.append(np.exp(1j*th[a])/np.sqrt(d))
    return U
def devs_h(th):
    U=Hmats(th.reshape(3,d,d))
    return np.concatenate([np.abs(np.abs(U[a].conj().T@U[b])**2-1.0/d).ravel()
                           for a in range(4) for b in range(a+1,4)])
def obj(x,beta=0.0):
    v=np.abs(devs_h(x)); m=v.max()
    if beta<=0: return float(m)
    return float(m+np.log(np.exp(beta*(v-m)).sum())/beta-np.log(len(v))/beta)
def to_mats(th): return np.array(Hmats(th.reshape(3,d,d)))
