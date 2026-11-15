"""For the F_6-chart triple, enumerate the projection-symmetry group (index of the support lattice)
and test, for each element T, whether T actually permutes the rays of each basis, or swaps them,
or neither (which would refute the recovery lemma)."""
import sys; sys.path.insert(0,'scratch')
import numpy as np, itertools
from exact import Ring, proj_support_exact, relation_matrix
from flatops import flat_prod, conjT
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form
ring=Ring(24); N=24; d=6

rays=[]
Fm=np.array([[np.exp(2j*np.pi*((j*k)%6)/6) for k in range(6)] for j in range(6)])/np.sqrt(6)
for tail in itertools.product(range(12),repeat=5):
    th=(0,)+tail
    v=np.array([np.exp(2j*np.pi*k/12) for k in th])/np.sqrt(6)
    if np.abs(np.abs(Fm.conj().T@v)-1/np.sqrt(6)).max()<1e-9: rays.append(th)
rays=sorted(set(rays))
Fexp=np.array([[(4*j*k)%24 for k in range(6)] for j in range(6)])
c=(0,2,5,6,8,11)
Kexp=np.array([[(2*rays[c[r]][i])%24 for r in range(6)] for i in range(6)])

def basis_from(E): return np.exp(2j*np.pi*E/24)/np.sqrt(6)
def quotient_elements(rows):
    """elements theta in R^6 (mod overall shift) with theta.r in Z for all relations r;
    returned as integer exponent vectors mod N via Smith normal form of the relation matrix."""
    M=sp.Matrix([list(r) for r in rows])
    s=smith_normal_form(M,domain=ZZ)
    # solve for the dual: enumerate solutions of M x = 0 mod 1 -> use integer lattice duality
    return M, s

def monolike(M,tol=1e-8):
    """is M monomial (one nonzero of modulus 1 per row and column)?"""
    A=np.abs(M)
    if (A>tol).sum()!=min(M.shape): return False,"count"
    return (np.abs(A.max(1)-1)<tol).all() and (np.abs(A.max(0)-1)<tol).all(),"ok"
def rayperm(M,d=6,tol=1e-8):
    """does M map the standard ray set to itself up to permutation and phases?"""
    A=np.abs(M)
    return ((np.abs(A-1)<tol).sum()==d) and ((A>tol).sum()==d)

def group_of_index(rows, d=6):
    """enumerate the group {theta in R^d/R.1 : theta.r in Z for all relations r}.
    Elements lie in (1/N)Z^d with N = index; enumerate k in (Z/N)^d, theta = k/N."""
    from exact import index_of_lattice
    N=index_of_lattice(rows)
    sols=[]
    for k in itertools.product(range(N),repeat=d):
        if all(sum(t*rr for t,rr in zip(k,r))%N==0 for r in rows): sols.append(k)
    return N,sols

# choose anchor B (basis B=F_6): other two bases in B coordinates
BinvT=conjT(Fexp,N); BC=flat_prod(BinvT,Kexp,ring)
S=proj_support_exact(BinvT,BC,ring); rows=relation_matrix(S)
print("anchor B: support",len(S),"relations",len(rows))
Nidx,sols=group_of_index(rows)
print("index:",Nidx," ; projection-symmetry group order:",len(sols),"modulus",Nidx)
Amat=basis_from(BinvT); Cmat=basis_from(BC)     # the two other bases in B coordinates
Kfull=basis_from(Kexp); Ffull=basis_from(Fexp); I6=np.eye(6)
for th in sols:
    T=np.diag(np.exp(2j*np.pi*np.array(th)/Nidx))
    # does T preserve the ray set of a basis given by matrix X (columns=vectors)?
    def check(X):
        Y=T@X
        # T maps rays of X to rays of X iff there is a monomial M with T X = X M
        M=X.conj().T@Y
        return monolike(M)
    okA,whyA=check(Amat); okC,whyC=check(Cmat)
    print("theta",th,"order",end=" ")
    k=1; v=np.array(th)
    while k<400:
        v=(v+np.array(th))%Nidx
        if not v.any(): break
        k+=1
    print(k," preserves A:",okA," preserves C:",okC)
