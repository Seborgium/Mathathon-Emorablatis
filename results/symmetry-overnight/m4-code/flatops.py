import numpy as np, itertools
from exact import Ring

def sqrt_exps(d, ring):
    """exponent vectors of sqrt(d) as element of Z[zeta_N], for d=6 and N=24 (also d=2,3,4)."""
    # brute force: search small sums of roots of unity
    N=ring.N
    for k in range(1,4):
        for combo in itertools.combinations(range(N),k):
            pass
    return None

def sqrt6(ring, N=24):
    v=ring.sumexp([1,23,5,19])
    w=ring.sumexp([m for m in []])
    return v

def flat_prod(X,Y,ring,SQRT=None):
    """X,Y: (d x d) exponent matrices mod N with entries (1/sqrt d) z^E. Return exponent matrix of X@Y.
    Requires the result to be flat with (1/sqrt d) times an N-th root of unity."""
    d=X.shape[0]; N=ring.N
    if SQRT is None: SQRT=sqrt6(ring)
    out=np.zeros((d,d),dtype=np.int64)
    for i in range(d):
        for j in range(d):
            v=ring.sumexp(list(X[i]+Y[:,j]))
            found=False
            for m in range(N):
                cand=ring.sumexp([m+1,m-1,m+5,m-5])
                if np.array_equal(v,cand): out[i,j]=m; found=True; break
            if not found: raise RuntimeError(f"not flat at {i},{j}: {np.nonzero(v)[0]}")
    return out

def conjT(E,N):
    return ((-E).T)%N

def kron_add(A,B,N):
    """exponent matrix of the Kronecker product of flat matrices (exponents add)."""
    ra,rb=A.shape[0],B.shape[0]
    out=np.zeros((ra*rb,ra*rb),dtype=np.int64)
    for i in range(ra):
        for j in range(ra):
            for a in range(rb):
                for b in range(rb):
                    out[i*rb+a, j*rb+b]=(A[i,j]+B[a,b])%N
    return out
