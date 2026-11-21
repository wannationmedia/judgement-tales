#!/usr/bin/env python3
"""Stage 2 — lay measured audio on a timeline; expand held beats into real cuts."""
import json, math
from timeline import TL
from shots import SHOTS
ROOT="/home/user/judgement-tales/.work"
VO=json.load(open(f"{ROOT}/vo_durations.json"))
TARGET=600.0; AIR_LINE=1.35; MAXCUT=3.1

# coverage pools per plate, for splitting a held beat into cuts
POOL={
 "P1":["recep_wide","queue_grp","gates","sign_recep","desk_papers","queue_deep",
       "two_pl","sign_good","recep_wide2","peter_mid","lwazi_mid","two_lc","stamp_ins"],
 "P3":["complaints_wide","sign_complaints","brenda_mid","hr_mug","moses_mid","tablet1","tablet2"],
 "P4":["downstairs_wide","sultan_mid","attendants","baklava","elevator"],
 "P6":["accused_wide","sven_mid","moses_door","sven_cu"],
}
def pool_for(shot):
    return POOL.get(SHOTS[shot]["p"], ["recep_wide"]) if shot in SHOTS else POOL["P1"]

def split(shot, d, seed, prev):
    """Break a held beat into 1..n cuts of <=MAXCUT, rotating coverage."""
    if d <= MAXCUT: return [(shot, d)]
    n = math.ceil(d / MAXCUT)
    pl = [s for s in pool_for(shot) if s != shot]
    cuts=[]; last=prev
    for k in range(n):
        s = shot if k == 0 else pl[(seed + k) % len(pl)]
        if s == last and len(pl) > 1:
            s = pl[(seed + k + 3) % len(pl)]
        cuts.append(s); last = s
    # weight the opening cut slightly longer, rest even
    w=[1.25]+[1.0]*(n-1); tot=sum(w)
    return [(cuts[k], d*w[k]/tot) for k in range(n)]

def build(bscale):
    t=0.0; ev=[]; prev=None
    for i,e in enumerate(TL):
        if e["ev"]=="line":
            d=VO[str(i)]["dur"]
            t+=e["pre"]*AIR_LINE
            ev.append(dict(i=i,kind="line",who=e["who"],start=t,dur=d,end=t+d,
                           shot=e["shot"],sub=e["sub"],fx=e["fx"],seg=e["seg"],
                           file=VO[str(i)]["file"],move=e.get("move")))
            if e["shot"]: prev=e["shot"]
            t+=d+e["post"]*AIR_LINE
        elif e["ev"]=="beat":
            total=e["dur"]*bscale
            for j,(s,d) in enumerate(split(e["shot"], total, i, prev)):
                ev.append(dict(i=i,kind="beat",start=t,dur=d,end=t+d,shot=s,
                               sub=e.get("sub") if j==0 else None,
                               fx=e["fx"] if j==0 else [],seg=e["seg"],move=e.get("move")))
                prev=s; t+=d
        else:
            d=e["dur"]
            ev.append(dict(i=i,kind="card",card=e["card"],start=t,dur=d,end=t+d,
                           sub=e.get("sub"),fx=e["fx"],seg=e["seg"]))
            prev=None; t+=d
    return ev,t

lo,hi=0.5,6.0
for _ in range(80):
    mid=(lo+hi)/2; _,tot=build(mid)
    (lo,hi) = (mid,hi) if tot<TARGET else (lo,mid)
bs=(lo+hi)/2; ev,tot=build(bs)
# visual duration: a cut holds until the next cut starts, absorbing dialogue pauses
for i,e in enumerate(ev):
    e["vdur"] = (ev[i+1]["start"] - e["start"]) if i+1 < len(ev) else (tot - e["start"])
cuts=[e for e in ev if e["kind"] in ("line","beat")]
print(f"sum of visual durations {sum(e['vdur'] for e in ev):.2f}s")
print(f"beat scale {bs:.2f}x -> total {tot:.2f}s ({tot/60:.3f} min)")
print(f"cuts: {len(ev)} events | avg shot length {sum(c['vdur'] for c in cuts)/len(cuts):.2f}s")
import collections
segs=collections.OrderedDict()
for e in ev:
    s=segs.setdefault(e["seg"],[1e9,0,0]); s[0]=min(s[0],e["start"]); s[1]=max(s[1],e["end"]); s[2]+=1
for k,(a,b,n) in segs.items():
    print(f"  {k:<8} {int(a//60):02d}:{a%60:05.2f} -> {int(b//60):02d}:{b%60:05.2f}  {b-a:6.1f}s  {n:3d} cuts")
long=[(e['shot'],round(e['dur'],1)) for e in ev if e['kind']=='beat' and e['dur']>MAXCUT+0.1]
print("over-long beats:",long[:5] or "none")
json.dump(dict(beat_scale=bs,air_line=AIR_LINE,total=tot,events=ev),
          open(f"{ROOT}/layout.json","w"), indent=1)
