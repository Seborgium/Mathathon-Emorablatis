"""Exact (symbolic) verification of the tetrahedral construction: max deviation exactly 1/18."""
import sympy as sp

I=sp.I; R=sp.Rational; s2=sp.sqrt(2); s3=sp.sqrt(3); s6=sp.sqrt(6)
w=sp.exp(2*sp.pi*I/3)
w=sp.simplify(sp.expand_complex(w))       # -1/2 + i sqrt3/2

# --- C^3: the four MUBs
F3=sp.Matrix(3,3,lambda k,l: sp.exp(2*sp.pi*I*k*l/3)/s3)
D1=sp.diag(1,w,w); D2=sp.diag(1,w**2,w**2)
B=[sp.simplify(F3), sp.simplify(D1*F3), sp.simplify(D2*F3), sp.eye(3)]

# --- C^2: four bases whose Bloch vectors are the regular tetrahedron
n=[sp.Matrix([1,1,1])/s3, sp.Matrix([1,-1,-1])/s3, sp.Matrix([-1,1,-1])/s3, sp.Matrix([-1,-1,1])/s3]
def basis(nvec):
    c=sp.sqrt((1+nvec[2])/2); s=sp.sqrt((1-nvec[2])/2)
    eip=(nvec[0]+I*nvec[1])/sp.sqrt(nvec[0]**2+nvec[1]**2)
    return sp.Matrix([[c, -sp.conjugate(eip)*s],[eip*s, c]])
A=[basis(v) for v in n]
print("A_a^*A_a - I  simplified to zero:", [sp.simplify(sp.expand_complex(a.H*a-sp.eye(2)).applyfunc(lambda e: sp.radsimp(sp.simplify(e)))) == sp.zeros(2,2) for a in A])

def kron(X,Y):
    m,n=X.shape; p,q=Y.shape
    M=sp.zeros(m*p,n*q)
    for i in range(m):
        for j in range(n):
            for k in range(p):
                for l in range(q):
                    M[i*p+k,j*q+l]=sp.expand(X[i,j]*Y[k,l])
    return M
U=[kron(A[a],B[a]) for a in range(4)]
def pmat(P,Q):
    X=sp.expand_complex(P.H*Q)
    return sp.Matrix(6,6,lambda i,j: sp.simplify(sp.expand(sp.expand_complex(X[i,j]*sp.conjugate(X[i,j])))))
vals=set()
for a in range(4):
    for b in range(a+1,4):
        M=pmat(U[a],U[b])
        for i in range(6):
            for j in range(6):
                vals.add(sp.nsimplify(sp.N(M[i,j],30)))
print("distinct values of |<u,v>|^2 over all cross pairs:", vals)
print("max |v - 1/6| =", max(abs(v-R(1,6)) for v in vals))
