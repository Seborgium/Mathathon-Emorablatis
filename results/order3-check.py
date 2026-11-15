"""Verification for results/order3-stratum.md.

Checks, from the definitions only:
  (1) the model flat T-covariant bases are unitary, flat and T-covariant;
  (2) Theorem B (criterion (E)+(B)) is exact: on the explicit Fourier triple the residual is ~1e-16,
      every zero of the criterion is a genuinely unbiased pair, and criterion == unbiasedness;
  (3) the quartet gap: max|overlap^2 - 1/6| over T-covariant quadruples, minimised from many starts;
  (4) the minimiser's squared overlaps take three values (the "three-value law").
Runtime: ~1-3 min on 4 cores.  Usage:  python3 results/order3-check.py
"""
import numpy as np
from scipy.optimize import least_squares, minimize

w = np.exp(2j*np.pi/3)
Z = np.diag([1, w, w**2]); T = np.kron(np.eye(2), Z)          # order 3, eigenvalues 1,w,w^2 twice
Tp = [np.linalg.matrix_power(T, k) for k in range(3)]
P3 = np.zeros((3,3))
for _k in range(3): P3[(_k+1)%3,_k] = 1.0        # column k of a T-orbit maps to column k+1
PI = np.block([[P3, np.zeros((3,3))],[np.zeros((3,3)), P3]])

def F3(n=3):
    j,k = np.meshgrid(np.arange(n), np.arange(n), indexing='ij'); return np.exp(2j*np.pi*j*k/n)/np.sqrt(n)
F2 = np.array([[1,1],[1,-1]])/np.sqrt(2)

def gen(ph):
    """nine phases -> orbit data (v[t,a], u[t,a]) ; index of coordinate (a,t) is a*3+t"""
    a=np.exp(1j*ph[0:3]); b=np.exp(1j*ph[3:6]); l=np.exp(1j*ph[6:9])
    v=np.zeros((3,2),complex); u=np.zeros((3,2),complex)
    for t in range(3):
        v[t]=[a[t]/np.sqrt(6), b[t]/np.sqrt(6)]
        u[t]=[l[t]*np.conj(b[t])/np.sqrt(6), -l[t]*np.conj(a[t])/np.sqrt(6)]
    return v,u

def basis(ph):
    v,u=gen(ph); V=np.zeros(6,complex); W=np.zeros(6,complex)
    for t in range(3):
        V[0*3+t]=v[t,0]; V[1*3+t]=v[t,1]; W[0*3+t]=u[t,0]; W[1*3+t]=u[t,1]
    return np.array([Tp[k]@z for z in (V,W) for k in range(3)]).T

def crit(ph):
    """(E),(B) for the four orbit pairs of two bases given by ph[0:9], ph[9:18]"""
    xA=gen(ph[0:9]); xB=gen(ph[9:18]); r=[]
    for x in xA:
        for y in xB:
            c=np.array([np.vdot(x[t],y[t]) for t in range(3)])
            r.append(np.sum(np.abs(c)**2)-1/6)
            P=np.sum(c*np.conj(np.roll(c,1))); r+=[P.real,P.imag]
    return np.array(r)

def defect_pair(ph):
    A,B=basis(ph[0:9]),basis(ph[9:18]); return np.abs(np.abs(A.conj().T@B)**2-1/6).max()

def overlaps4(ph):
    A,B,C=basis(ph[0:9]),basis(ph[9:18]),basis(ph[18:27]); out=[]
    for X,Y in ((A,B),(A,C),(B,C)): out.append((np.abs(X.conj().T@Y)**2).ravel())
    return np.concatenate(out)

rng=np.random.default_rng(2026)

# ---------- (1) sanity of the model ----------
print("(1) model bases")
for _ in range(3):
    C=basis(rng.uniform(0,2*np.pi,9))
    print("    unitarity %.1e   flatness %.1e   T-covariance %.1e" % (
        np.abs(C.conj().T@C-np.eye(6)).max(), np.abs(np.abs(C)-1/np.sqrt(6)).max(), np.abs(T@C-C@PI).max()))

# ---------- (2) Theorem B ----------
print("(2) Theorem B")
U2=np.kron(F2,F3()); U3=np.kron(np.diag([1,1j])@F2, np.diag([1,w**2,w**2])@F3())
def phases_of(A):
    v=np.array([[A[0*3+t,0],A[1*3+t,0]] for t in range(3)])*np.sqrt(6)
    u=np.array([[A[0*3+t,3],A[1*3+t,3]] for t in range(3)])*np.sqrt(6)
    return np.concatenate([np.angle(v[:,0]),np.angle(v[:,1]),np.angle(u[:,0]/np.conj(v[:,1]))])
ph=np.concatenate([phases_of(U2),phases_of(U3)])
print("    explicit triple  : true defect %.1e   criterion residual %.1e" % (defect_pair(ph), np.abs(crit(ph)).max()))
bad=0; zeros=0
for _ in range(40):
    s=least_squares(crit,rng.uniform(0,2*np.pi,18),xtol=1e-15,ftol=1e-15,gtol=1e-15,max_nfev=3000)
    if np.abs(s.fun).max()<1e-9:
        zeros+=1
        if defect_pair(s.x)>1e-8: bad+=1
print("    criterion zeros  : %d found, %d of them not unbiased" % (zeros,bad))

# ---------- (3) quartet gap ----------
print("(3) T-covariant quadruples, 60 restarts (raise the count for more confidence)")
best=(9.0,None)
for _ in range(60):
    s=minimize(lambda p: np.sum((overlaps4(p)-1/6)**2), rng.uniform(0,2*np.pi,27),
               method='L-BFGS-B', options={'maxiter':20000,'ftol':1e-18,'gtol':1e-14})
    v=np.abs(overlaps4(s.x)-1/6).max()
    if v<best[0]: best=(v,s.x.copy())
print("    min over starts of max|overlap^2-1/6| = %.10f" % best[0])

# ---------- (4) three-value law ----------
vals=np.sort(overlaps4(best[1])); u=np.unique(np.round(vals,7))
print("(4) squared overlaps of the minimiser: %d distinct values" % len(u))
for x in u: print("      %.10f   multiplicity %d" % (x, int(np.sum(np.round(vals,7)==x))))
