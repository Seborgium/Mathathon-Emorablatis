#!/usr/bin/env bash
# checkerfmt.sh - does the shipped checker accept the stdout the published sources print?
# Works on a copy: results/ is copied, data/ is symlinked, the recorded tree is untouched.
set -u
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO=$(CDPATH= cd -- "$HERE/../../../../.." && pwd)
SRC=${1:-$REPO/work/10-recreate/crew/m3/saved-run/execution}
cd "$HERE" || exit 1
rm -rf results pristine; cp -r "$SRC/results" results; cp -r results pristine
cp -f "$SRC/commands.json" .; cp -f "$SRC/check_records.py" .
[ -e data ] || ln -s "$SRC/data" data
restore(){ rm -rf results; cp -r pristine results; }
run(){ python3 check_records.py . 2>&1 | python3 -c 'import sys,json
s=sys.stdin.read()
try:
  d=json.loads(s); print("   verdict:",d.get("result"),"|",d.get("error"))
except Exception: print("   raw:",s.strip()[:300])'; }
echo "T0 recorded results verbatim"
restore; run
echo "T1 covrun.txt in the published printf format (covout.cpp:139,130,132,142)"
restore
printf 'xs22829 build19.30\n t0/22829 cells42 centers5\n t10000/22829 cells37490183 centers72679\n t20000/22829 cells119874659 centers205716\nN112 r0.0320 dual2 checked151744086 centers249878 visit29769262282 near3341641851 cheap45648766 lp3134060273\ntime 401.82\n' > results/covrun.txt
run
echo "T2 N-line counters kept, other covrun lines as recorded"
restore
printf 'xs 22829\nN112 r0.0320 dual2 checked151744086 centers249878 visit29769262282 near3341641851 cheap45648766 lp3134060273\ncompleted_write\n' > results/covrun.txt
run
echo "T2b 'xs' without the space"
restore
printf 'xs22829\nN112 r0.0320 dual2 checked151744086 centers249878\ncompleted_write\n' > results/covrun.txt
run
echo "T3 A0.txt in the published format (atlas.cpp:233,237)"
restore
python3 - <<'EOF'
p='results/A0.txt'; L=open(p).read().splitlines()
open(p,'w').write('\n'.join([l+' coverFailures0+0' for l in L[:-1]]+['total done62470 candidates1 patches1 global764 failedBalls0 time 3.21'])+'\n')
EOF
run
echo "T4 C.batch0.txt in the published format (stageC.cpp:553,561)"
restore
python3 - <<'EOF'
p='results/C.batch0.txt'; L=open(p).read().splitlines()
open(p,'w').write('\n'.join([l+' avg bins123 balls456 time 1.0' for l in L[:-1]]+[L[-1]+' time 1.2'])+'\n')
EOF
run
echo "T5 Bfine.txt with the published time field (stageB.cpp:324)"
restore
python3 - <<'EOF'
p='results/Bfine.txt'; L=open(p).read().splitlines()
out=[]
for l in L:
    h,r=l.split(' parent',1); out.append(h+' time 0.1 parent'+r)
open(p,'w').write('\n'.join(out)+'\n')
EOF
run
echo "T6 restored"
restore; run
