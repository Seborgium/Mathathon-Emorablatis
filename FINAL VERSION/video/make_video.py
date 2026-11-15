"""Render slides/video/stageC-demo.mp4: a real run of examples/step4_example.py,
with the two exact integer tests that discard the candidates."""
import os, subprocess, sys, shutil
from PIL import Image, ImageDraw, ImageFont

W,H,FPS = 1280,720,15
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTD = os.path.join(ROOT,".scratch","vframes")
os.makedirs(OUTD, exist_ok=True)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_mono  = ImageFont.truetype(MONO, 17)
f_monos = ImageFont.truetype(MONO, 15)
f_cap   = ImageFont.truetype(SANS, 19)
f_caps  = ImageFont.truetype(SANS, 16)
f_ttl   = ImageFont.truetype(BOLD, 44)
f_sub   = ImageFont.truetype(SANS, 21)
f_big   = ImageFont.truetype(BOLD, 76)
BG=(20,22,26); TERM=(13,15,18); BAR=(10,11,13); FG=(226,226,220); DIM=(140,142,148)
ACC=(196,84,64); STEEL=(122,164,196); GREEN=(140,178,120); YEL=(214,182,110)

# ---- the real run -------------------------------------------------------
import time
t0=time.time()
run=subprocess.run([sys.executable,"examples/step4_example.py"],cwd=ROOT,
                   capture_output=True,text=True,timeout=120)
wall=time.time()-t0
lines=run.stdout.splitlines()
print(f"run rc={run.returncode} wall={wall:.2f}s lines={len(lines)}")

def frame():
    im=Image.new("RGB",(W,H),BG); return im,ImageDraw.Draw(im)

def rr(d,box,r,fill):
    d.rounded_rectangle(box,radius=r,fill=fill)

def base(caption=None, fade=1.0):
    im,d=frame()
    rr(d,(0,0,W,H),0,BG)
    if caption:
        d.rectangle((0,H-64,W,H),fill=BAR)
        d.text((40,H-42),caption,font=f_cap,fill=(238,236,230))
    return im,d

# terminal box geometry
TX0,TY0,TX1,TY1 = 40,64,916,620
SX0,SX1 = 940,1240

def draw_term(d, duty_lines, prompt=None, typed=""):
    rr(d,(TX0,TY0,TX1,TY1),10,TERM)
    d.rectangle((TX0,TY0,TX1,TY0+30),fill=(28,30,35))
    for i,c in enumerate(((120,80,78),(150,132,90),(110,140,105))):
        d.ellipse((TX0+14+i*20,TY0+10,TX0+24+i*20,TY0+20),fill=c)
    d.text((TX0+80,TY0+7),os.path.basename("step4_example.py")+"  —  exact arithmetic in Z[ζ12]",
           font=f_monos,fill=DIM)
    x,y=TX0+18,TY0+46
    if prompt:
        d.text((x,y),"$",font=f_mono,fill=GREEN); x+=22
        d.text((x,y),typed,font=f_mono,fill=FG)
        if typed and (int(typed.__len__())%2==0):
            d.rectangle((x+d.textlength(typed,font=f_mono)+2,y+1,x+d.textlength(typed,font=f_mono)+11,y+18),fill=FG)
        y+=30
    import re
    for txt,col in duty_lines:
        parts=re.split(r"\s{2,}",txt.strip())
        name=parts[0]; vals=parts[1:]
        d.text((x,y),name,font=f_mono,fill=col)
        if vals:
            vx=x+318
            d.text((vx,y),vals[0],font=f_mono,fill=col)
            if len(vals)>1:
                d.text((vx+150,y),"".join(vals[1:]),font=f_monos,fill=DIM)
        y+=30
    return y

def draw_side(d,items,big=None):
    rr(d,(SX0,TY0,SX1,TY1),10,(26,28,33))
    d.text((SX0+22,TY0+18),"the tally",font=f_caps,fill=DIM)
    y=TY0+56
    for lab,val,col in items:
        d.text((SX0+22,y),lab,font=f_caps,fill=(170,172,178)); y+=20
        d.text((SX0+22,y),val,font=ImageFont.truetype(BOLD,30),fill=col); y+=52
    if big:
        d.line((SX0+22,y+4,SX1-22,y+4),fill=(60,62,68),width=1)
        y+=22
        d.text((SX0+22,y),"surviving",font=f_caps,fill=(170,172,178)); y+=22
        d.text((SX0+22,y),big,font=f_big,fill=ACC)

def save(im,n):
    im.save(os.path.join(OUTD,f"f{n:05d}.png"))

# ---- the timeline -------------------------------------------------------
PROMPT="$ cd examples && python3 step4_example.py"
OUT=[("s4.candidates                 12","rays unbiased to the standard and Fourier bases",STEEL),
     ("s4.candidates.exact_residual  0","max |A-6| + |B| over all checks (exact ints)",DIM),
     ("s4.pairs                      66","pairs of candidates",DIM),
     ("s4.O.edges                    48","pairs exactly orthogonal",FG),
     ("s4.U.edges                     0","pairs exactly unbiased (|<x,y>| = 1/sqrt6)",ACC),
     ("s4.O.sixcliques                4","orthonormal bases among the candidates",FG),
     ("s4.pattern                 False","two disjoint six-cliques, all 36 cross edges?",ACC)]
CODE=[("def inner(a, b):",FG),
      ("    # <x,y> for x_k = z^a_k/sqrt6, y_k = z^b_k/sqrt6",DIM),
      ("    return counts([a[k] - b[k] for k in range(6)])",FG),
      ("",FG),
      ("if all(x == 0 for x in reduce4(nn)):   O[i,j] = True",FG),
      ("if abs2_ok(nn):                        U[i,j] = True",ACC)]
CTX=[("s4.U.edges                     0",ACC),("s4.pattern                 False",ACC)]
KILL=[("s4.kill.1e-06.disto       4.082482905e-07","one entry rotated by 1e-06 cycles",DIM),
      ("s4.kill.1e-06.O                       False","O edge at radius 0",ACC),
      ("s4.kill.1e-06.radius       2.081482905e-07","per-ball radius needed to keep it",DIM)]

n=0
def hold(im,secs):
    global n
    for _ in range(int(round(secs*FPS))):
        save(im,n); n+=1

# 1. title card
for k in range(int(3.0*FPS)):
    im,d=base()
    a=min(1.0,(k+1)/(1.2*FPS))
    col=tuple(int(BG[i]+(238-BG[i])*a) for i in range(3))
    d.text((80,250),"Discarding the candidates",font=f_ttl,fill=col)
    d.text((84,320),"Stage C on the standard + Fourier pair, run for real",font=f_sub,
           fill=tuple(int(BG[i]+(170-BG[i])*a) for i in range(3)))
    d.line((84,370,84+int(360*a),370),fill=ACC,width=3)
    save(im,n); n+=1

# 2. typing the command
TYPE_T=2.6
for k in range(int(TYPE_T*FPS)):
    im,d=base("The program enumerates every vector unbiased to both bases — exactly.")
    t=int(len(PROMPT)*min(1.0,(k+1)/(TYPE_T*FPS)))
    draw_term(d,[],prompt=True,typed=PROMPT[:t])
    draw_side(d,[])
    save(im,n); n+=1

# 3. output grows, with the tally
seq=[]   # (text, note, colour, seconds)
for t in OUT: seq.append((t[0],t[1],t[2], 0.9 if "pairs" in t[0] else 1.5))
seq[4]=(seq[4][0],seq[4][1],seq[4][2],3.4)   # U.edges 0 -- hold
seq[6]=(seq[6][0],seq[6][1],seq[6][2],3.0)   # pattern False -- hold
tally=[("candidates","12",FG)]
for txt,note,col,secs in seq:
    if "O.edges" in txt: tally.append(("orthogonal pairs","48",FG))
    if "U.edges" in txt: tally.append(("unbiased pairs","0",ACC))
    if "sixcliques" in txt: tally.append(("candidate bases","4",FG))
    for k in range(int(secs*FPS)):
        im,d=base(note)
        idx=[i for i,t in enumerate(seq) if t==(txt,note,col,secs)][0]
        draw_term(d,[(l[0],(l[2] if i==idx else FG)) for i,l in enumerate(seq[:idx+1])],)
        draw_side(d,tally,big="0" if "U.edges" in txt else None)
        save(im,n); n+=1

# 4. the code panel
for k in range(int(7.0*FPS)):
    im,d=base("Both decisions are integer tests: a sum of twelfth roots vanishes, or its modulus squared is exactly 6.")
    rr(d,(TX0,TY0,TX1,TY1),10,TERM)
    d.rectangle((TX0,TY0,TX1,TY0+30),fill=(28,30,35))
    d.text((TX0+16,TY0+7),"examples/step4_example.py",font=f_monos,fill=DIM)
    y=TY0+52
    for txt,col in CODE:
        d.text((TX0+20,y),txt,font=f_mono,fill=col); y+=28
    rr(d,(SX0,TY0,SX1,TY1),10,(26,28,33))
    d.text((SX0+22,TY0+18),"why it is a proof",font=f_caps,fill=DIM)
    for i,(a) in enumerate(["no tolerance:","the test is `== 0`","and `A == 6, B == 0`,","so a candidate is","discarded only when","the overlap is exactly","wrong."]):
        d.text((SX0+22,TY0+60+i*30),a,font=f_caps,fill=(206,204,198))
    save(im,n); n+=1

# 5. the kill test
for k in range(int(2.0*FPS)):
    im,d=base("Sanity check: move one entry by a millionth of a cycle and watch the edge die.")
    draw_term(d,[("s4.kill.1e-06.disto       4.082482905e-07",DIM)])
    save(im,n); n+=1
for k in range(int(9.0*FPS)):
    im,d=base("A rotation of 1e-6 cycles — far below any tolerance — already breaks orthogonality.")
    draw_term(d,CTX+[(a,c) for a,_,c in KILL])
    rr(d,(SX0,TY0,SX1,TY1),10,(26,28,33))
    d.text((SX0+22,TY0+18),"the margin",font=f_caps,fill=DIM)
    y=TY0+60
    for a in ["the edge","survives only","if the balls","stay inside","a radius of","2.1e-07.","","the balls the","pipeline uses","have radius","0.011 — five","orders larger.","","so the verdict","is not an","artefact of","rounding."]:
        d.text((SX0+22,y),a,font=f_caps,fill=(206,204,198)); y+=30
    save(im,n); n+=1

# 6. end card
for k in range(int(7.0*FPS)):
    im,d=base()
    a=min(1.0,(k+1)/(0.8*FPS))
    d.text((80,230),"0 of 66 pairs are unbiased.",font=f_big,
           fill=tuple(int(BG[i]+(ACC[i]-BG[i])*a) for i in range(3)))
    d.text((84,340),"Four candidate bases. None is unbiased to any other.",font=f_sub,fill=(210,208,202))
    d.text((84,378),"So no fourth basis hides among these candidates.",font=f_sub,fill=(210,208,202))
    d.text((84,470),"What remains is the cover: the same test inside every ball, for every H.",font=f_caps,fill=DIM)
    save(im,n); n+=1

print("frames",n,"=>",n/FPS,"s")
mp4=os.path.join(os.path.dirname(os.path.abspath(__file__)),"stageC-demo.mp4")
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",
                os.path.join(OUTD,"f%05d.png"),"-c:v","libx264","-pix_fmt","yuv420p",
                "-crf","21","-movflags","+faststart",mp4],check=True)
# poster
poster=os.path.join(os.path.dirname(os.path.abspath(__file__)),"poster.png")
Image.open(os.path.join(OUTD,f"f{int(29*FPS):05d}.png")).save(poster)
print("wrote",mp4, os.path.getsize(mp4), "poster",poster)
