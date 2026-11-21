#!/usr/bin/env python3
"""Stage 5 — English subtitles timed to the measured dialogue audio.
Writes a clean dialogue track and an SDH track (speaker labels + sound cues)."""
import json, re, os
from shots import FACES
ROOT="/home/user/judgement-tales/.work"
L=json.load(open(f"{ROOT}/layout.json")); EV=L["events"]
MAXLINE=42; MAXCUE=84; TAIL=0.35; MINCUE=0.9

NAME={"LWAZI":"LWAZI","LWAZI_VO":"LWAZI (V.O.)","PETER":"ST. PETER","SVEN":"SVEN",
      "NIGEL":"NIGEL","SULTAN":"THE SULTAN","BRENDA":"BRENDA","CANDICE":"CANDICE",
      "MOSES":"MOSES","TANNOY":"TANNOY"}

def clean(s, keep_paren):
    s=s.replace("**","").replace("*","")
    s=re.sub(r"[\U0001F300-\U0001FAFF☀-➿]","",s)
    if not keep_paren: s=re.sub(r"\((?!V\.O\.)[^)]*\)","",s)
    return re.sub(r"\s+"," ",s).strip(" -—")

def wrap(s):
    w=s.split(); out=[]; cur=""
    for x in w:
        if len(cur)+len(x)+1<=MAXLINE: cur=(cur+" "+x).strip()
        else: out.append(cur); cur=x
    if cur: out.append(cur)
    return "\n".join(out[:2]) if len(out)<=2 else "\n".join(out)

def split_cue(text, st, en):
    """Break an over-long line into sequential cues weighted by character count."""
    if len(text)<=MAXCUE: return [(st,en,text)]
    words=text.split(); parts=[]; cur=""
    for x in words:
        if len(cur)+len(x)+1<=MAXCUE: cur=(cur+" "+x).strip()
        else: parts.append(cur); cur=x
    if cur: parts.append(cur)
    tot=sum(len(p) for p in parts); out=[]; t=st
    for p in parts:
        d=(en-st)*len(p)/tot; out.append((t,t+d,p)); t+=d
    return out

def ts(x):
    if x<0: x=0
    h=int(x//3600); m=int(x%3600//60); s=int(x%60); ms=int(round((x-int(x))*1000))
    if ms==1000: s+=1; ms=0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def build(sdh):
    cues=[]
    for i,e in enumerate(EV):
        if e["kind"]=="line":
            txt=clean(e["sub"], keep_paren=sdh)
            if not txt: continue
            who=e['who'].replace('_VO','')
            onscreen = (not e.get('card')) and who in FACES.get(e.get('shot') or '', set())
            # SDH names everyone; the default track names a speaker whenever their face isn't on screen
            if sdh or not onscreen: txt=f"{NAME.get(e['who'],e['who'])}: {txt}"
            nxt=next((x["start"] for x in EV[i+1:] if x["kind"]=="line"), 1e9)
            en=min(e["end"]+TAIL, nxt-0.08)
            en=max(en, e["start"]+MINCUE if e["start"]+MINCUE<nxt-0.08 else e["end"])
            cues+=split_cue(txt, e["start"], en)
        elif e.get("ontext") and e["kind"]=="beat":
            # words printed on screen that carry a joke are captioned in both tracks
            cues.append((e["start"]+0.35, e["start"]+e.get("vdur",e["dur"])-0.1, f"SIGN: {e['ontext']}"))
        elif sdh and e.get("sub") and e["kind"] in ("beat","card"):
            txt=clean(e["sub"], keep_paren=True)
            if not txt: continue
            if not txt.startswith("["): txt=f"[{txt}]" if txt.isupper() is False and "—" not in txt else txt
            en=min(e["end"], e["start"]+4.0)
            if en-e["start"]>=0.7: cues.append((e["start"],en,txt))
    cues.sort(key=lambda c:c[0])
    # de-overlap
    fixed=[]
    for st,en,tx in cues:
        if fixed and st < fixed[-1][1]: st=fixed[-1][1]+0.04
        if en-st<0.5: en=st+0.5
        fixed.append((st,en,tx))
    return fixed

for sdh,fn in ((False,"judgement-tales-s01e01.en.srt"),(True,"judgement-tales-s01e01.en-sdh.srt")):
    cues=build(sdh); p=f"{ROOT}/{fn}"
    with open(p,"w",encoding="utf-8") as f:
        for n,(st,en,tx) in enumerate(cues,1):
            f.write(f"{n}\n{ts(st)} --> {ts(en)}\n{wrap(tx)}\n\n")
    print(f"{fn}: {len(cues)} cues, last out {ts(cues[-1][1])}")
    # WebVTT twin for the site player
    v=p.replace(".srt",".vtt")
    with open(v,"w",encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for n,(st,en,tx) in enumerate(cues,1):
            f.write(f"{n}\n{ts(st).replace(',','.')} --> {ts(en).replace(',','.')}\n{wrap(tx)}\n\n")
