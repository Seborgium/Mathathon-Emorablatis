"""Direct computation of the diagonal symmetry groups from the bases themselves.
Entries are exponent matrices mod N (entry = (1/sqrt d) zeta_N^e).
Diagonal T = diag(zeta_N^{u_i}); we work modulo overall scalar (fix u_0 = 0)."""
import numpy as np, itertools

def monitors(E, N, d=6):
    """All u such that T = diag(z^u) preserves the ray set of the vectors (columns) of E,
    E[i,r] = exponent of coordinate i in vector r.  T b_r is proportional to b_{sigma(r)}."""
    out=set()
    for sigma in itertools.permutations(range(d)):
        u=tuple(int((E[i,sigma[0]]-E[i,0])%N) for i in range(d))
        ok=True
        for r in range(d):
            c=(u[0]+E[0,r]-E[0,sigma[r]])%N
            for i in range(1,d):
                if (u[i]+E[i,r]-E[i,sigma[r]])%N != c: ok=False; break
            if not ok: break
        if ok: out.add(tuple((x-u[0])%N for x in u))   # normalise mod global phase: u_0=0
    return out

def order_of(u,N,d=6):
    if all(x%N==0 for x in u): return 1
    k=1; v=tuple(x%N for x in u)
    while True:
        v=tuple((a+b)%N for a,b in zip(v,u)); k+=1
        if all(x%N==0 for x in v): return k
        if k>200: return None
def diag_sym_group(anchors_bases, N, d=6):
    """anchors_bases: list of two exponent matrices (the two OTHER bases, in common coordinates).
    Returns the set of u (u_0=0) that preserve both ray sets."""
    S=[monitors(E,N,d) for E in anchors_bases]
    return S[0]&S[1]


if __name__=="__main__":
    import pickle
    res=pickle.load(open('scratch/f6chart.pkl','rb'))
    for c,ok,d in res:
        print("rays",c)
        for anchor in ('A','B','C'):
            print("   ",anchor,d[anchor])
