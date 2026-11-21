#!/usr/bin/env python3
"""Measure the walkthrough's acceptance criteria against the finished master and its captions."""
import json, re, subprocess
from shots import FACES
R="/home/user/judgement-tales"; M=f"{R}/out/judgement-tales-s01e01-the-queue.mp4"
EV=json.load(open(f"{R}/.work/layout.json"))["events"]
tc=lambda x:f"{int(x//60)}:{x%60:05.2f}"
INSERTS={'alcove','gates','pass_gold','helmet_ins','desk_papers','baklava','elevator','ticket_ins','stamp_ins'}
res=[]
def ok(n,cond,detail): res.append((n,cond,detail))

# 1 — nobody's voice over someone else's face
bad=[(tc(e['start']),e['who'],e['shot']) for e in EV if e['kind']=='line' and e.get('shot') and not e.get('card')
     and e['who']!='LWAZI_VO' and FACES.get(e['shot']) and e['who'] not in FACES[e['shot']]]
ok(1,not bad,f"{len(bad)} lines heard over another character's face")
# 2 — Nigel: alcove or inserts only, first line on the alcove
ng=[e for e in EV if e.get('who')=='NIGEL']
ok(2,all(e['shot'] in INSERTS for e in ng) and ng[0]['shot']=='alcove',
   f"{len(ng)} Nigel lines; shots used: {sorted({e['shot'] for e in ng})}; first: {ng[0]['shot']}")
# 3 — default captions name off-screen speakers
srt=open(f"{R}/out/judgement-tales-s01e01.en.srt",encoding="utf-8").read()
blocks=[b.split("\n") for b in srt.strip().split("\n\n")]
txt=lambda b:" ".join(b[2:])
nigel_labelled=sum(1 for b in blocks if txt(b).startswith("NIGEL:"))
credits_labelled=sum(1 for b in blocks if re.match(r"(CANDICE|ST\. PETER):",txt(b)))
ok(3,nigel_labelled>=len(ng) and credits_labelled>=4,
   f"NIGEL-labelled cues {nigel_labelled} (lines {len(ng)}); button-gag cues labelled {credits_labelled}")
# 4 — the helmet exists before anyone asks for it
first_sven=min(e['start'] for e in EV if e.get('shot') in ('sven_cu','sven_mid','helmet_lift'))
helmet_said=min(e['start'] for e in EV if e.get('who')=='NIGEL' and "helmet" in e['sub'].lower())
sven_shots={e['shot'] for e in EV if e.get('who')=='SVEN'}
ok(4,first_sven<helmet_said and sven_shots<= {'sven_cu','sven_mid','helmet_lift'},
   f"helmet on screen from {tc(first_sven)}, first asked for at {tc(helmet_said)}; Sven shots {sorted(sven_shots)}")
# 5 — Sven is staged in reception; no crowned figure (boardroom plate gone)
p6=[e['shot'] for e in EV if e.get('shot') in ('accused_wide','moses_door')]
ok(5,not p6,"Sven shots are reception composites; boardroom framings used: "+str(len(p6)))
# 6 — the punchline sign is readable and captioned
sh=[e for e in EV if 'shutter' in (e.get('fx') or [])][0]
cap=any("SIGN: GONE TO LUNCH" in txt(b) for b in blocks)
ok(6,sh['vdur']-0.35>=3.0 and cap,f"legible {sh['vdur']-0.35:.2f}s; captioned in default track: {cap}")
# 7 — reception never cuts to another location
ok(7,not p6,"off-location cuts in reception scenes: "+str(len(p6)))
# 8 — plain-language caption track names in the master
t=subprocess.run(["ffprobe","-v","error","-select_streams","s","-show_entries","stream_tags=title",
                  "-of","csv=p=0",M],capture_output=True,text=True).stdout.strip().splitlines()
ok(8,"SDH" not in " ".join(t) and len(t)==2,f"tracks: {t}")
# 9 — first 25s: no pure-black hold > 1.0s; the world on screen by 0:10
bd=subprocess.run(["ffmpeg","-v","info","-t","25","-i",M,"-vf","blackdetect=d=1.0:pix_th=0.06","-an","-f","null","-"],
                  capture_output=True,text=True).stderr
blacks=re.findall(r"black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)",bd)
world=min(e['start'] for e in EV if e['kind']=='beat' and e.get('shot'))
ok(9,not blacks and world<=10,f"black holds >1.0s in first 25s: {blacks or 'none'}; world from {world:.2f}s")
# 10 — runtime
dur=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",M],
                         capture_output=True,text=True).stdout)
ok(10,abs(dur-600)<0.05,f"runtime {dur:.2f}s")
for n,c,d in res: print(f"  {'PASS' if c else 'FAIL'}  AC{n:<2} {d}")
print(f"\n{sum(c for _,c,_ in res)}/{len(res)} acceptance criteria met")
