#!/usr/bin/env python3
"""Paste-ready YouTube metadata, generated from the real timeline so chapters are exact."""
import json
ROOT="/home/user/judgement-tales"; OUT=f"{ROOT}/out/youtube"
EV=json.load(open(f"{ROOT}/.work/layout.json"))["events"]
seg={}
for e in EV:
    s=seg.setdefault(e["seg"],[1e9,0]); s[0]=min(s[0],e["start"]); s[1]=max(s[1],e["start"]+e["vdur"])
def mmss(x): x=int(x); return f"{x//60:02d}:{x%60:02d}"
CH=[(0,"Cold open — The Last Tuesday"),(seg["titles"][0],"Main titles"),
    (seg["A"][0],"Skit A — Now Serving: 047"),(seg["B"][0],"Skit B — The Fast-Track"),
    (seg["C"][0],"Skit C — Processing Error"),(seg["credits"][0],"Credits (and one last form)")]
assert CH[0][0]==0 and all(CH[i+1][0]-CH[i][0]>=10 for i in range(len(CH)-1)), "chapter rules"

TITLE="JUDGEMENT TALES — Ep 1: The Queue | Animated Afterlife Comedy"
TITLE_ALT=["Heaven Has a Queue. He's Ticket 047. | JUDGEMENT TALES Ep 1",
           "Heaven Is Run Like Home Affairs | JUDGEMENT TALES Ep 1 \"The Queue\""]
DESC=f"""Lwazi dies on an ordinary Tuesday and wakes up at Heaven's reception — where eternity is run like Home Affairs. He's ticket 047. They're serving 046. They have been for four hundred years.

Episode 1 of JUDGEMENT TALES, an adult animated comedy about the afterlife's paperwork. A Viking who has queued since 862 AD. A black-market Fast-Track Pass. A Sultan who would like a hat. And Brenda. We don't say Brenda's name in the queue.

CHAPTERS
""" + "\n".join(f"{mmss(t)} {n}" for t,n in CH) + """

CAST (characters)
Lwazi "Lucky" Nkosi · St. Peter · Sven · Nigel "The Blagger" · The Sultan · Brenda · Candice · Moses

A WANNATION MEDIA PRODUCTION
WANNATION MEDIA — a division of WANNATION HOLDINGS (PTY) LTD · Reg No: 2026/463724/07

This is a work of fiction and satire. The target is bureaucracy, power and individual characters — never a faith, a people or a nation. Casting choices are creative interpretations, not historical or factual claims about any population, and not a statement about anyone's faith.

Animated from original scene art. Voices are synthesized. Original score and sound design.

Subscribe for Episode 2: "Orientation Day".

#JudgementTales #AnimatedComedy #Afterlife"""
TAGS=["Judgement Tales","animated comedy","adult animation","afterlife comedy","heaven comedy",
      "satire","bureaucracy","South African comedy","Home Affairs","queue","animated series",
      "pilot episode","cartoon comedy","WANNATION MEDIA","St Peter","Viking","sketch comedy"]
tags_len=sum(len(t)+ (2 if " " in t else 0) for t in TAGS)+len(TAGS)-1
checks={"title ≤100":len(TITLE)<=100,"alt titles ≤100":all(len(t)<=100 for t in TITLE_ALT),
        "description ≤5000":len(DESC)<=5000,"tags ≤500 chars":tags_len<=500,
        "no < or > in description":("<" not in DESC and ">" not in DESC),"≥3 chapters from 00:00":len(CH)>=3}
for k,v in checks.items(): print(f"  {'OK ' if v else 'FAIL'} {k}")
assert all(checks.values())
open(f"{OUT}/title.txt","w").write(TITLE+"\n\n# alternatives for title testing:\n"+"\n".join(TITLE_ALT)+"\n")
open(f"{OUT}/description.txt","w").write(DESC+"\n")
open(f"{OUT}/tags.txt","w").write(", ".join(TAGS)+"\n")
json.dump({"chapters":[{"t":mmss(t),"title":n} for t,n in CH]},open(f"{OUT}/chapters.json","w"),indent=1)
print(f"title {len(TITLE)} chars · description {len(DESC)} chars · tags {tags_len} chars")
print("\n".join(f"  {mmss(t)} {n}" for t,n in CH))
