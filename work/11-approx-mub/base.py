import numpy as np, itertools, time
from scipy.linalg import expm
from scipy.optimize import minimize

d = 6
J = np.ones((d,d))/d

def devs(Us):
    out=[]
    for a in range(4):
        for b in range(a+1,4):
            P = np.abs(Us[a].conj().T @ Us[b])**2
            out.append((P-1.0/d).ravel())
    return np.concatenate(out)

def maxdev(Us):
    return np.abs(devs(Us)).max()

def e2(Us):
    return (devs(Us)**2).sum()

def herm(v):
    A=np.zeros((6,6),dtype=complex); k=0
    for i in range(6):
        A[i,i]=v[k]; k+=1
    for i in range(6):
        for j in range(i+1,6):
            A[i,j]=v[k]+1j*v[k+1]; A[j,i]=v[k]-1j*v[k+1]; k+=2
    return A

def unit(v):
    return [np.eye(6,dtype=complex)]+[expm(1j*herm(v[36*a:36*(a+1)])) for a in range(3)]

def obj(v,beta):
    x=devs(unit(v)); m=np.abs(x).max()
    return m + np.log(np.exp(beta*(np.abs(x)-m)).sum())/beta - np.log(len(x))/beta

# --- K4 product construction: C^6 = C^2 x C^3
F3=np.exp(2j*np.pi*np.outer(np.arange(3),np.arange(3))/3)/np.sqrt(3)
D3=np.diag([1,np.exp(2j*np.pi/3),np.exp(4j*np.pi/3)])
B=[F3,D3@F3,D3@D3@F3,np.diag([1,np.exp(2j*np.pi/3),np.exp(2j*np.pi/3)])@F3]
F2=np.array([[1,1],[1,-1]])/np.sqrt(2)
A=[np.eye(2,dtype=complex),F2]
def kron(A,B): return np.kron(A,B)
Us=[kron(A[0],B[0]),kron(A[0],B[1]),kron(A[1],B[0]),kron(A[1],B[1])]
for M in Us: assert np.allclose(M.conj().T@M,np.eye(6))
print("K4 dev matrix:"); 
for a in range(4):
    print([round(maxdev([Us[a],Us[b]]),12) for b in range(4)])
print("K4 maxdev", maxdev(Us), "E2", e2(Us))
# is a 4th canonical: check it is 3-MUB-extendable? print pairwise
t=time.time(); v=np.zeros(108); obj(v,50.0); print("one obj eval", time.time()-t)
