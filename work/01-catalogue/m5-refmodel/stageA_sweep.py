import numpy as np, sys, json
sys.path.insert(0,'.')
import mubref as M
rs=0.0320001; Rs=2*np.pi*rs
def dephased_hadamard(a,b):
    H=M.fourier_family(a,b); P=M.dephase(H); return M.e(P), P
rng=np.random.default_rng(1)
rows=[]
for trial in range(400):
    a,b=rng.random(2)
    H,P=dephased_hadamard(a,b)
    s=M.seed_of(P)
    v=rng.standard_normal(9); v=v/np.linalg.norm(v)*rs*rng.random()**(1/9)
    p=s+v
    r=M.stageA(p,P)
    q=M.lemma_3_2_q(r,Rs); pol=M.lemma_3_2_polar(r['Y'],q)
    rows.append(dict(q=q,mB=r['mB'],mC=r['mC'],ident=r['ident38'],b39=r['bound39_ok'],
                     psd=r['psd'],pol=pol['ok'],lhs=pol['lhs'],p=pol['p'],
                     disp2=r['e1']**2+r['b1']**2+r['c1']**2))
R=rows; arr=lambda k: np.array([r[k] for r in R])
print("n =",len(R))
print("identity (3.8) max |resid|      : %.3e" % np.abs(arr('ident')).max())
print("6I-Y*Y psd everywhere           :", bool(arr('psd').all()))
print("tr(6I-Y*Y) <= (3.9) bound       :", bool(arr('b39').all()))
print("||Y-sqrt6 V||_F <= p (3.11)     :", bool(arr('pol').all()), " worst lhs/p = %.4f"%(arr('lhs')/arr('p')).max())
print("q  max %.5f  median %.5f  min %.5f"%(arr('q').max(),np.median(arr('q')),arr('q').min()))
print("q<0.32 everywhere               :", bool((arr('q')<0.32).all()), " q<6 everywhere:", bool((arr('q')<6).all()))
print("frames: min mB %.4f min mC %.4f min m %.4f"%(arr('mB').min(),arr('mC').min(),np.minimum(arr('mB'),arr('mC')).min()))
print("(3.3) max (e1^2+b1^2+c1^2)/Rs^2 : %.6f"%((arr('disp2')/Rs**2).max()))
json.dump([{k:(float(v) if not isinstance(v,(bool,np.bool_)) else bool(v)) for k,v in r.items()} for r in R],open('stageA_sweep.json','w'))
