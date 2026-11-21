#!/usr/bin/env python3
"""Pick trailer + vertical social cuts, snapped to real cut boundaries in the finished master."""
import json
ROOT="/home/user/judgement-tales/.work"
L=json.load(open(f"{ROOT}/layout.json")); EV=L["events"]

def find(frag, kind="line", nth=0):
    hits=[i for i,e in enumerate(EV) if e["kind"]==kind and frag.lower() in (e.get("sub") or "").lower()]
    if not hits: raise SystemExit(f"not found: {frag}")
    return hits[nth]
def t0(i): return EV[i]["start"]
def t1(i): return EV[i]["start"]+EV[i]["vdur"]

def seg(a_frag, b_frag, pre=0.6, post=0.9, nth_a=0, nth_b=0):
    a=find(a_frag,nth=nth_a); b=find(b_frag,nth=nth_b)
    return round(max(0,t0(a)-pre),2), round(min(600,t1(b)+post),2)

CUTS={
 "take-a-ticket": dict(
   platform=["TikTok","Reels","Shorts"],
   title="Take a ticket. For heaven.",
   span=seg("Take a ticket.","It has been forty-six for four hundred years"),
   caption="Heaven runs on forms. #JudgementTales #animation #comedy #afterlife"),
 "eleven-hundred-years": dict(
   platform=["TikTok","Reels","Shorts"],
   title="He's been in the queue since 862 AD",
   span=seg("Do not. Skip. The queue.","Home Affairs has a franchise up here"),
   caption="Queue Member of the Century. Four times. #JudgementTales #animatedseries #comedy"),
 "the-fast-track": dict(
   platform=["TikTok","Reels","Shorts"],
   title="The fast-track to the Complaints Department",
   span=seg("So it works?","I have heard this one before"),
   caption="You skip the queue to reach the department that processes complaints about the queue. #JudgementTales"),
}
# trailer: the strongest beats, in order, plus the title card
TRAILER=[
  seg("Take a ticket.","A ticket. For heaven.", pre=0.4, post=0.5),
  seg("It has been forty-six for four hundred years","It has been forty-six for four hundred years", pre=0.3, post=0.8),
  seg("I have held this position since","It was a good day", pre=0.3, post=0.6),
  seg("You want me to rob a Viking","You want me to rob a Viking", pre=0.4, post=0.7),
  seg("It fast-tracks you straight to the","It fast-tracks you straight to the", pre=0.4, post=1.0),
  seg("I died to escape admin","better signage", pre=0.4, post=0.9),
]
TITLE=(round(t0(find("JUDGEMENT TALES",kind="card")),2),
       round(t0(find("JUDGEMENT TALES",kind="card"))+6.0,2))

segs={}
for e in EV:
    s=segs.setdefault(e["seg"],[1e9,0]); s[0]=min(s[0],e["start"]); s[1]=max(s[1],e["start"]+e["vdur"])
out=dict(running_order={k:[round(v[0],2),round(v[1],2)] for k,v in segs.items()},
         cuts=CUTS, trailer=TRAILER, trailer_title=TITLE, total=L["total"])
json.dump(out, open(f"{ROOT}/cuts.json","w"), indent=1)
def tc(x): return f"{int(x//60):02d}:{x%60:05.2f}"
print("VERIFIED RUNNING ORDER (from the render)")
for k,(a,b) in out["running_order"].items(): print(f"  {k:<8} {tc(a)} -> {tc(b)}   {b-a:6.1f}s")
print("\nSOCIAL CUTS")
for k,v in CUTS.items():
    a,b=v["span"]; print(f"  {k:<22} {tc(a)} -> {tc(b)}   {b-a:5.1f}s   {v['title']}")
print("\nTRAILER SEGMENTS")
tot=sum(b-a for a,b in TRAILER)+ (TITLE[1]-TITLE[0])
for a,b in TRAILER: print(f"  {tc(a)} -> {tc(b)}  ({b-a:.1f}s)")
print(f"  + title card {TITLE[1]-TITLE[0]:.1f}s   => trailer ≈ {tot:.1f}s")
