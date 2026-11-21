#!/usr/bin/env python3
"""Stage 4a — cut each framing out of its approved plate and upscale for camera headroom."""
import os, subprocess
from shots import SHOTS, P
REPO="/home/user/judgement-tales"; OUT=f"{REPO}/.work/plates"; os.makedirs(OUT,exist_ok=True)
W,H=2880,1620
# Nigel is never seen: his alcove is treated as a silhouette.
TREAT={"alcove":["-modulate","52,64,106","-blur","0x2.5","-brightness-contrast","-6x10"]}
for name,s in SHOTS.items():
    x,y,w,h=s["crop"]; src=f"{REPO}/{P[s['p']]}"; dst=f"{OUT}/{name}.png"
    cmd=["convert",src,"-crop",f"{w}x{h}+{x}+{y}","+repage"]
    cmd+=TREAT.get(name,[])
    cmd+=["-filter","Lanczos","-resize",f"{W}x{H}!","-quality","97",dst]
    subprocess.run(cmd,check=True)
print(f"prepared {len(SHOTS)} framings at {W}x{H}")
