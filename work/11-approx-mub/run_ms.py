import numpy as np, json, sys, time
sys.path.insert(0,'.')
from mubopt import *

def randU(rng):
    A=rng.normal(size=(6,6))+1j*rng.normal(size=(6,6)); Q,R=np.linalg.qr(A)
    return Q*np.exp(-1j*np.angle(np.diag(R)))

def gradcheck(seed=5):
    rng=np.random.default_rng(seed)
    Us=[np.eye(6,dtype=complex)]+[randU(rng) for _ in range(3)]
    beta=300.0; Bs=tangent_basis(); G,_=grad_lse(Us,beta); eps=1e-6; worst=0
    for a in range(NB):
        for k in range(36):
            Up=list(Us); Up[a+1]=Us[a+1]@expm(eps*Bs[k]); Um=list(Us); Um[a+1]=Us[a+1]@expm(-eps*Bs[k])
            fd=(lse(Up,beta)-lse(Um,beta))/(2*eps)
            an=2*np.real(np.trace(G[a+1].conj().T@Bs[k]))
            worst=max(worst,abs(fd-an))
    return worst

if __name__ == "__main__":
    print("grad check (body coords):", gradcheck(), flush=True)
    rng=np.random.default_rng(int(sys.argv[1]) if len(sys.argv)>1 else 0)
    N=int(sys.argv[2]) if len(sys.argv)>2 else 200
    tag=sys.argv[1] if len(sys.argv)>1 else "0"
    best=None; recs=[]; t0=time.time()
    for s in range(N):
        Us=[np.eye(6,dtype=complex)]+[randU(rng) for _ in range(3)]
        Us=polish(Us)
        md=maxdev(Us); recs.append(float(md))
        if best is None or md<best[0]:
            best=(md,Us); np.save(f'best_{tag}.npy', np.array(Us))
            print(f"restart {s}: maxdev {md:.12f} E2 {e2(Us):.10f}  t={time.time()-t0:.1f}s", flush=True)
    print("summary: n",N,"min",min(recs),"median",float(np.median(recs)),"max",max(recs), flush=True)
    json.dump({"n":N,"devs":recs}, open(f'ms_{tag}.json','w'))
