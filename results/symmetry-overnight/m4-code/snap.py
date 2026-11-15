import numpy as np, itertools
def snap(M, Ns=(3,4,6,8,12,24), tol=1e-8):
    """Return (exponent matrix mod N, N) if every entry is a root of unity of order in Ns."""
    M=np.asarray(M,dtype=complex)
    for N in Ns:
        E=np.zeros(M.shape,dtype=np.int64); ok=True
        for idx in np.ndindex(M.shape):
            z=M[idx]
            k=None
            for kk in range(N):
                if abs(np.exp(2j*np.pi*kk/N)-z)<tol: k=kk; break
            if k is None: ok=False; break
            E[idx]=k
        if ok: return E,N
    return None,None

def exact_mub_check(mats, ring):
    """mats: list of (E,N) columns-orthonormal flat unitaries (all flat, d x d).
    Verify: each column-orthonormal, and |X^*Y| = 1/sqrt(d) exactly."""
    def conjexp(E,N): return (-E)%N
    out=[]
    d=mats[0][0].shape[0]
    for (E,N) in mats:
        # <col p, col q> = sum_i z^{E_ip - E_iq} ; need d if p==q else 0
        for p in range(d):
            for q in range(d):
                v=ring.sumexp(list(E[:,p]-E[:,q]))
                if p==q:
                    exp=np.zeros(ring.deg,dtype=np.int64); exp[0]=d
                    good=np.array_equal(v,exp)
                else:
                    good=ring.iszero(v)
                if not good: return False,("orth",p,q,np.nonzero(v)[0][:3])
    for (E,N),(F,Nf) in itertools.combinations(mats,2):
        assert N==Nf
        # (E^* F)_{pq} = sum_i z^{F_iq - E_ip}; need modulus 1/sqrt(d):
        # equivalent: s * conj(s) = 1  where s = sum_i z^{...}  (since |.|^2 = s * bar s ; scaling 1/d)
        for p in range(d):
            for q in range(d):
                v=ring.sumexp(list(F[:,q]-E[:,p]))
                w=ring.sumexp(list(E[:,p]-F[:,q]))
                prod=polymul(v,w,ring)
                exp=np.zeros(ring.deg,dtype=np.int64); exp[0]=1
                if not np.array_equal(prod,exp): return False,("flat",p,q)
    return True,None

def polymul(a,b,ring):
    """multiply two elements of Z[zeta_N] given in the power basis of degree deg=phi(N)."""
    N=ring.N; deg=ring.deg
    # build polynomial product degree <= 2deg-2, then reduce x^k for k up to 2deg-2
    c=np.zeros(2*deg-1,dtype=np.int64)
    for i in range(deg):
        if a[i]==0: continue
        for j in range(deg):
            if b[j]==0: continue
            c[i+j]+=a[i]*b[j]
    out=np.zeros(deg,dtype=np.int64)
    for k in range(2*deg-1):
        if c[k]: out+= c[k]*ring.pows[k % N] if k%N==k else c[k]*ring.reduce(k)
    return out
