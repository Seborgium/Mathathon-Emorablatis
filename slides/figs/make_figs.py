import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle, Wedge
from matplotlib.collections import LineCollection

INK="#1d1d20"; ACC="#b03a2e"; STEEL="#33566e"; GREY="#c9c4bb"; PAPER="#ffffff"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"axes.linewidth":0,
    "xtick.major.size":0,"ytick.major.size":0,"savefig.transparent":False})

def clean(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)

# ---------- 1. the phase matrix: 36 entries, 25 genuine
def fig_phases(path, dephase=True):
    fig, axes = plt.subplots(1,2,figsize=(7.2,3.4))
    for ax, dep in zip(axes,(False,True)):
        for j in range(6):
            for k in range(6):
                a = (2*j*k + j + k*k) % 12
                if dep and (j==0 or k==0):   # gauge-fixed entries
                    col, lw = GREY, 0.8
                else:
                    col, lw = (ACC if (2*j*k+j+k*k)%12 in (0,6) else STEEL), 1.0
                ax.add_patch(Circle((k,5-j), 0.30, fc="none", ec=col, lw=lw, alpha=.55))
                ang = 2*np.pi*a/12
                ax.plot(k+0.30*np.cos(ang), 5-j+0.30*np.sin(ang), "o", ms=2.6,
                        color=col if not (dep and (j==0 or k==0)) else GREY)
        ax.set_xlim(-.55,5.55); ax.set_ylim(-.55,5.55); ax.set_aspect("equal"); clean(ax)
    axes[0].set_title("36 phases", fontsize=10, color=INK, pad=6)
    axes[1].set_title("11 fixed by gauge, 25 left", fontsize=10, color=INK, pad=6)
    fig.tight_layout(pad=0.2); fig.savefig(path); plt.close(fig)

# ---------- 2. the seed cover: circle of 112 bins, one ball of radius 0.032
def fig_cover(path):
    fig, ax = plt.subplots(figsize=(3.6,3.6))
    N=112
    for i in range(N):
        a=2*np.pi*i/N
        ax.plot([np.cos(a)*1.0],[np.sin(a)*1.0],"|",ms=4,color=GREY,mec=GREY,
                transform=ax.transData) if False else None
    # ticks drawn as radial dashes
    segs=[[(np.cos(2*np.pi*i/N)*0.97,np.sin(2*np.pi*i/N)*0.97),
           (np.cos(2*np.pi*i/N)*1.03,np.sin(2*np.pi*i/N)*1.03)] for i in range(N)]
    ax.add_collection(LineCollection(segs,colors=GREY,lw=1.0))
    # a highlighted bin and its ball
    i0=17; a0=2*np.pi*i0/N
    ax.add_patch(Wedge((0,0),1.0,np.degrees(a0),np.degrees(a0+2*np.pi/N),width=0.06,
                       fc=ACC,ec="none",alpha=.9))
    r=0.34  # exaggerated: true radius is 0.032 cycles
    ax.add_patch(Circle((np.cos(a0),np.sin(a0)),r,fc=STEEL,ec="none",alpha=.10))
    ax.plot(np.cos(a0),np.sin(a0),"o",ms=3.2,color=STEEL)
    ax.annotate("", xy=(0.28,0.24), xytext=(np.cos(a0)-0.02,np.sin(a0)+0.06),
                arrowprops=dict(arrowstyle="-",color=STEEL,lw=0.6))
    ax.set_xlim(-1.45,1.75); ax.set_ylim(-1.35,1.35); ax.set_aspect("equal"); clean(ax)
    fig.tight_layout(pad=0.05); fig.savefig(path); plt.close(fig)

# ---------- 3. the U(2) chart: a square cut into cells, one cell holding the completion
def fig_chart(path):
    fig, ax = plt.subplots(figsize=(3.4,2.5))
    n=8
    for i in range(n+1):
        ax.plot([i/n,i/n],[0,1],color=GREY,lw=.7)
        ax.plot([0,1],[i/n,i/n],color=GREY,lw=.7)
    ax.add_patch(Rectangle((3/n,4/n),1/n,1/n,fc=ACC,ec="none",alpha=.35))
    ax.plot(3.5/n,4.5/n,"o",ms=3.4,color=INK)
    ax.set_xlim(-.02,1.02); ax.set_ylim(-.02,1.02); ax.set_aspect("equal"); clean(ax)
    fig.tight_layout(pad=.05); fig.savefig(path); plt.close(fig)

# ---------- 4. four candidate bases, zero unbiased cross pairs
def fig_sextuples(path):
    fig, ax = plt.subplots(figsize=(3.5,3.3))
    n=4
    for i in range(n):
        for j in range(n):
            if i==j:
                fc, ec, t = INK, "none", ""
                ax.add_patch(Rectangle((j, n-1-i), .92,.92, fc=fc, ec=ec, alpha=.85))
            else:
                ax.add_patch(Rectangle((j, n-1-i), .92,.92, fc="none", ec=GREY, lw=.8))
                ax.text(j+.46, n-1-i+.46, "0", ha="center", va="center",
                        color=ACC, fontsize=9, fontweight="bold")
    ax.set_xlim(-.06,3.98); ax.set_ylim(-.06,3.98); ax.set_aspect("equal"); clean(ax)
    fig.tight_layout(pad=.05); fig.savefig(path); plt.close(fig)

# ---------- 5. the 12-ray graph of the Fourier pair, 4 hexagons
def fig_graph(path, edges, cliques, n=12):
    ang=np.linspace(np.pi/2, np.pi/2-2*np.pi, n, endpoint=False)
    P=np.c_[np.cos(ang),np.sin(ang)]
    fig, ax=plt.subplots(figsize=(3.6,3.5))
    cols=[ACC,"#7a8b3c","#8a6d3b",STEEL]
    for ci,cq in enumerate(cliques):
        segs=[[P[a],P[b]] for i,a in enumerate(cq) for b in cq[i+1:]]
        ax.add_collection(LineCollection(segs,colors=cols[ci%len(cols)],lw=1.0,alpha=.55,
                                         zorder=1+ci))
    ax.plot(P[:,0],P[:,1],"o",ms=4.5,color=INK,zorder=9)
    ax.set_xlim(-1.18,1.18); ax.set_ylim(-1.18,1.18); ax.set_aspect("equal"); clean(ax)
    fig.tight_layout(pad=.02); fig.savefig(path); plt.close(fig)

# ---------- 6. ledger: 23 506 records, 163 of them at the cap
def fig_ledger(path):
    fig, ax = plt.subplots(figsize=(6.2,1.0))
    tot=23506; cap=163
    ax.add_patch(Rectangle((0,0),1,1,fc="#dfe4e8",ec="none"))
    ax.add_patch(Rectangle((1-cap/tot,0),cap/tot,1,fc=ACC,ec="none"))
    ax.set_xlim(0,1); ax.set_ylim(0,1); clean(ax)
    fig.tight_layout(pad=.02); fig.savefig(path); plt.close(fig)

if __name__=="__main__":
    import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
    fig_phases("fig_phases.pdf")
    fig_cover("fig_cover.pdf")
    fig_chart("fig_chart.pdf")
    fig_sextuples("fig_sextuples.pdf")
    fig_ledger("fig_ledger.pdf")
    cliques=[(1,2,4,6,9,11),(0,2,5,6,8,11),(1,3,4,7,9,10),(0,3,5,7,8,10)]
    # O edges: pairs with |<x,y>|=0 exactly -- rebuilt from the 8-regular structure
    T=[[0,1,0,9,4,9],[0,1,4,9,4,1],[0,3,4,3,0,7],[0,3,8,3,0,11],[0,5,0,9,8,9],
       [0,5,8,9,8,5],[0,7,0,3,4,3],[0,7,4,3,4,7],[0,9,4,9,0,1],[0,9,8,9,0,5],
       [0,11,0,3,8,3],[0,11,8,3,8,11]]
    z=np.exp(1j*np.pi/6)
    E=[]
    for i in range(12):
        for j in range(i+1,12):
            ssum=sum(z**((T[i][k]-T[j][k])%12) for k in range(6))
            if abs(ssum)<1e-9: E.append((i,j))
    fig_graph("fig_graph.pdf", E, cliques)
    print("O edges:",len(E))
    print("ok")
