import sys; sys.path.insert(0,'scratch')
import numpy as np, time
from exact import *
from flatops import *
ring=Ring(24)
q2 = [None, np.array([[0,0],[0,2]]), np.array([[0,0],[3,1]])]
q3 = [None, np.array([[1,2,0],[0,0,0],[2,1,0]]), np.array([[2,1,2],[0,0,2],[2,0,0]]), np.array([[2,1,1],[0,0,1],[0,1,0]])]
def lift(E,f,N): return (E.astype(np.int64)*(N//f))%N
Bexp = kron_add(lift(q2[1],4,24), lift(q3[1],3,24),24)
Cexp = kron_add(lift(q2[2],4,24), lift(q3[2],3,24),24)
Aexp = None  # anchor identity: matrix of I_6 in I_6 coords is identity (not flat) -> use B,C directly
pairs = {
 'A': (Bexp, Cexp),
 'B': (conjT(Bexp,24), flat_prod(conjT(Bexp,24), Cexp, ring)),
 'C': (conjT(Cexp,24), flat_prod(conjT(Cexp,24), Bexp, ring)),
}
for name,(P,Q) in pairs.items():
    t=time.time(); r=delta_anchor(P,Q,ring)
    print(name, r, f"{time.time()-t:.2f}s")
