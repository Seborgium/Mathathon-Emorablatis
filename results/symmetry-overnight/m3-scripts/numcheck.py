import numpy as np
w = np.exp(2j*np.pi/6)
N=6
X = np.zeros((N,N), dtype=complex)
for j in range(N): X[(j+1)%N, j] = 1
Z = np.diag([w**j for j in range(N)])
def W(a,b): return np.linalg.matrix_power(X,a) @ np.linalg.matrix_power(Z,b)
def eb(M):
    vals, vecs = np.linalg.eig(M)
    return vecs
for (a,b) in [(0,1),(1,0),(1,1),(1,2),(2,3)]:
    B = eb(W(a,b))
    print((a,b), "flat:", np.allclose(np.abs(B), 1/np.sqrt(6), atol=1e-9))
Bs = {k: eb(W(*k)) for k in [(0,1),(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(2,3),(3,2)]}
keys=list(Bs)
print("     ", "  ".join(str(k) for k in keys))
for k1 in keys:
    row=[]
    for k2 in keys:
        M = np.abs(Bs[k1].conj().T @ Bs[k2])
        row.append("U " if np.allclose(M, 1/np.sqrt(6), atol=1e-9) else "%.2f"%M.min())
    print(k1, row)
