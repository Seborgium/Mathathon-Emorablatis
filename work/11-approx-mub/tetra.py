"""Tetrahedral C^2 x (4 MUBs of C^3) construction; expected max dev exactly 1/18."""
import numpy as np
s3=np.sqrt(3)
dirs=[np.array([1,1,1])/s3, np.array([1,-1,-1])/s3, np.array([-1,1,-1])/s3, np.array([-1,-1,1])/s3]
print("tetrahedron inner products:")
print(np.round(np.array([[float(a@b) for b in dirs] for a in dirs]),12))
def basis_from_bloch(n):
    th=np.arccos(np.clip(n[2],-1,1)); ph=np.arctan2(n[1],n[0])
    c,s=np.cos(th/2),np.sin(th/2)
    return np.array([[c,-np.exp(-1j*ph)*s],[np.exp(1j*ph)*s,c]])
A=[basis_from_bloch(n) for n in dirs]
for M in A: assert np.allclose(M.conj().T@M,np.eye(2),atol=1e-14)
w=np.exp(2j*np.pi/3); F3=np.exp(2j*np.pi*np.outer(np.arange(3),np.arange(3))/3)/np.sqrt(3)
B=[F3, np.diag([1,w,w])@F3, np.diag([1,w**2,w**2])@F3, np.eye(3,dtype=complex)]
def pdev(U,V,d): return np.abs(np.abs(U.conj().T@V)**2-1.0/d).max()
print("C3 pairwise dev (should be 0):", max(pdev(B[i],B[j],3) for i in range(4) for j in range(i+1,4)))
print("C2 pairwise |n.n|/2 (should be 1/6):", [round(float(pdev(A[i],A[j],2)),12) for i in range(4) for j in range(i+1,4)])
U=[np.kron(A[a],B[a]) for a in range(4)]
for M in U: assert np.allclose(M.conj().T@M,np.eye(6),atol=1e-14)
D=[[ (pdev(U[a],U[b],6) if a!=b else 0.0) for b in range(4)] for a in range(4)]
print("C6 pairwise dev (should be 1/18=%.12f):"% (1/18))
print(np.round(np.array(D),13))
print("max dev", max(D[a][b] for a in range(4) for b in range(a+1,4)), " 1/18 =", 1/18)
np.save('tetra_u.npy', np.array(U))
