import sys; sys.path.insert(0,'scratch')
import numpy as np, itertools
from exact import Ring, proj_support_exact, relation_matrix
from flatops import flat_prod, conjT
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form
ring=Ring(24)
Fm=np.array([[np.exp(2j*np.pi*((j*k)%6)/6) for k in range(6)] for j in range(6)])/np.sqrt(6)
rays=[]
for tail in itertools.product(range(12),repeat=5):
    th=(0,)+tail
    v=np.array([np.exp(2j*np.pi*k/12) for k in th])/np.sqrt(6)
    if np.abs(np.abs(Fm.conj().T@v)-1/np.sqrt(6)).max()<1e-9: rays.append(th)
rays=sorted(set(rays))
V=np.array([[np.exp(2j*np.pi*k/12) for k in th] for th in rays])/np.sqrt(6)
O=np.abs(V@V.conj().T)**2; ort=O<1e-9; np.fill_diagonal(ort,False)
sext=[c for c in itertools.combinations(range(len(rays)),6) if all(ort[i,j] for i,j in itertools.combinations(c,2))]
Fexp=np.array([[(4*j*k)%24 for k in range(6)] for j in range(6)])
def smith_rows(P,Q):
    S=proj_support_exact(P,Q,ring); rows=relation_matrix(S)
    M=Matrix([list(r) for r in rows]); s=smith_normal_form(M,domain=ZZ)
    dg=[abs(int(s[i,i])) for i in range(5)]
    return len(S),len(rows),dg
print("F_6 chart: triples {I_6, F_6, K} with all entries in mu_24")
for c in sext:
    Kexp=np.array([[(2*rays[c[r]][i])%24 for r in range(6)] for i in range(6)])
    BinvT=conjT(Fexp,24); BC=flat_prod(BinvT,Kexp,ring); CinvT=conjT(Kexp,24); CB=flat_prod(CinvT,Fexp,ring)
    out=[]
    for lbl,(P,Q) in (('I',(Fexp,Kexp)),('F',(BinvT,BC)),('K',(CinvT,CB))):
        n,k,dg=smith_rows(P,Q); out.append(f"{lbl}: supp={n} rel={k} Smith={dg}")
    print(" sextuple",c); print("    "+"\n    ".join(out))
# tensor triple
q2 = [None, np.array([[0,0],[0,2]]), np.array([[0,0],[3,1]])]
q3 = [None, np.array([[1,2,0],[0,0,0],[2,1,0]]), np.array([[2,1,2],[0,0,2],[2,0,0]]), np.array([[2,1,1],[0,0,1],[0,1,0]])]
def lift(E,f,N): return (E.astype(np.int64)*(N//f))%N
def kron_add(A,B,N):
    ra,rb=A.shape[0],B.shape[0]; out=np.zeros((ra*rb,ra*rb),dtype=np.int64)
    for i in range(ra):
        for j in range(ra):
            for a in range(rb):
                for b in range(rb): out[i*rb+a,j*rb+b]=(A[i,j]+B[a,b])%N
    return out
Bexp=kron_add(lift(q2[1],4,24),lift(q3[1],3,24),24); Cexp=kron_add(lift(q2[2],4,24),lift(q3[2],3,24),24)
print("tensor triple {I, F_2 (x) F_3, q2' (x) q3'}")
BinvT=conjT(Bexp,24); BC=flat_prod(BinvT,Cexp,ring); CinvT=conjT(Cexp,24); CB=flat_prod(CinvT,Bexp,ring)
for lbl,(P,Q) in (('I',(Bexp,Cexp)),('B',(BinvT,BC)),('C',(CinvT,CB))):
    n,k,dg=smith_rows(P,Q); print(f"   {lbl}: supp={n} rel={k} Smith={dg}")
