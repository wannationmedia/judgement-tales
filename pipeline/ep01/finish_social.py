#!/usr/bin/env python3
"""Build the vertical trailer and (re)write social_built.json from the files on disk."""
import json, os, subprocess
src=open("make_social.py").read(); exec(src[:src.index("res={}")])   # definitions only
def dur(f): return round(float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                 "-of","csv=p=0",f],capture_output=True,text=True).stdout),2)
res={}
tr=f"{OUT}/judgement-tales-s01e01-trailer.mp4"
res["trailer"]=dict(file=os.path.basename(tr),seconds=dur(tr))
for k,m in C["cuts"].items():
    f=f"{OUT}/judgement-tales-s01e01-{k}-vertical.mp4"
    res[k]=dict(file=os.path.basename(f),seconds=dur(f),title=m["title"],caption=m["caption"],
                span=m["span"],platform=m["platform"],headline=m["headline"])
o,d=vertical("trailer",dict(span=[0,res["trailer"]["seconds"]],headline="A NEW ANIMATED\nCOMEDY"),
             src=tr,srt=f"{TMP}/trailer.srt")
res["trailer-vertical"]=dict(file=os.path.basename(o),seconds=round(d,2))
json.dump(res,open(f"{ROOT}/social_built.json","w"),indent=1)
for k,v in res.items(): print(f"{k:<22}{v['seconds']:6.2f}s  {v['file']}")
