import numpy as np
d=6; w=np.exp(2j*np.pi/3)
def pdev(U,V): return np.abs(np.abs(U.conj().T@V)**2-1.0/d).max()
F3=np.exp(2j*np.pi*np.outer(np.arange(3),np.arange(3))/3)/np.sqrt(3)
B=[F3, np.diag([1,w,w])@F3, np.diag([1,w**2,w**2])@F3, np.eye(3,dtype=complex)]
print("C3 4 MUBs pairwise dev:", max(pdev(B[i],B[j]) for i in range(4) for j in range(i+1,4)))
F2=np.array([[1,1],[1,-1]])/np.sqrt(2)
A=[np.eye(2,dtype=complex),F2]
print("C2 pair dev:", pdev(A[0],A[1]))
Us=[np.kron(A[i],B[j]) for (i,j) in [(0,0),(0,1),(1,0),(1,1)]]
print("K4  pairwise dev:")
for a in range(4): print([round(float(pdev(Us[a],Us[b])),12) for b in range(4)])
print("K4 maxdev", max(pdev(Us[a],Us[b]) for a in range(4) for b in range(a+1,4)))
