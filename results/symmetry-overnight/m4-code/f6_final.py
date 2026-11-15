"""Exact analysis of the F_6 chart: triples {I_6, F_6, K} whose entries are 24th roots of unity.
(1) Delta_X via the support lattice of the projection  (2) the diagonal symmetry groups computed
directly from the bases, independently of the projection."""
import sys; sys.path.insert(0,'scratch')
import numpy as np, itertools
from exact import Ring, delta_anchor, proj_support_exact, relation_matrix
from flatops import flat_prod, conjT
from symgroup import monitors, diag_sym_group, order_of
ring=Ring(24); N=24; d=6

# ---- 12 root-of-unity rays unbiased wrt I_6 and F_6 ----
rays=[]
for tail in itertools.product(range(12),repeat=5):
    th=(0,)+tail
    v=np.array([np.exp(2j*np.pi*k/12) for k in th])/np.sqrt(6)
    Fm=np.array([[np.exp(2j*np.pi*((j*k)%6)/6) for k in range(6)] for j in range(6)])/np.sqrt(6)
    if np.abs(np.abs(Fm.conj().T@v)-1/np.sqrt(6)).max()<1e-9: rays.append(th)
rays=sorted(set(rays)); print("#root-of-unity rays over {I,F_6}:",len(rays))
V=np.array([[np.exp(2j*np.pi*k/12) for k in th] for th in rays])/np.sqrt(6)
O=np.abs(V@V.conj().T)**2; ort=O<1e-9; np.fill_diagonal(ort,False)
sext=[c for c in itertools.combinations(range(len(rays)),6) if all(ort[i,j] for i,j in itertools.combinations(c,2))]
print("#orthonormal sextuples:",len(sext))

Fexp=np.array([[(4*j*k)%24 for k in range(6)] for j in range(6)])   # columns = F_6 vectors
def Kexp_of(c):
    return np.array([[(2*rays[c[r]][i])%24 for r in range(6)] for i in range(6)])

def mmax(X,Y): return np.abs(np.abs(X.conj().T@Y)-1/np.sqrt(6)).max()
for c in sext:
    C=Kexp_of(c)
    Bm=np.exp(2j*np.pi*Fexp/24)/np.sqrt(6); Cm=np.exp(2j*np.pi*C/24)/np.sqrt(6)
    print("="*70); print("sextuple",c)
    print("  numeric MUB devs: I-F %.1e  I-K %.1e  F-K %.1e ; orthonormal K %.1e"
          %(mmax(np.eye(6),Bm),mmax(np.eye(6),Cm),mmax(Bm,Cm),np.abs(Cm.conj().T@Cm-np.eye(6)).max()))
    # Delta via projection lattice
    BinvT=conjT(Fexp,24); BC=flat_prod(BinvT,C,ring); CinvT=conjT(C,24); CB=flat_prod(CinvT,Fexp,ring)
    for anchor,(Pp,Qq) in (('A=I',(Fexp,C)),('B=F',(BinvT,BC)),('C=K',(CinvT,CB))):
        r=delta_anchor(Pp,Qq,ring); print("   Delta_%s: index=%d  rank_F3=%d  supp=%d"%(anchor,r['index'],r['f3'],r['nsupp']))
    # direct symmetry groups (u with u_0=0, T=diag(zeta^u))
    GA=diag_sym_group((Fexp,C),24); GB=diag_sym_group((BinvT,BC),24); GC=diag_sym_group((CinvT,CB),24)
    for lbl,G in (('A=I',GA),('B=F',GB),('C=K',GC)):
        print("   |G_%s| = %d   element orders %s"%(lbl,len(G),sorted(order_of(u,24) for u in G)))
    T=[u for u in GC if order_of(u,24)==2]
    if T: print("   order-2 symmetry at C: u =",T[0])
