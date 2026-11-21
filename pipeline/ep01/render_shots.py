#!/usr/bin/env python3
"""Stage 4b — render every cut as a 1920x1080/24fps clip with camera motion and practical gags."""
import json, os, subprocess, sys, concurrent.futures as cf
from shots import SHOTS
ROOT="/home/user/judgement-tales/.work"
PL=f"{ROOT}/plates"; CD=f"{ROOT}/cards"; PR=f"{ROOT}/props"; OUT=f"{ROOT}/clips"
os.makedirs(OUT,exist_ok=True)
L=json.load(open(f"{ROOT}/layout.json")); EV=L["events"]
FPS=24; W,H=1920,1080
CRED=[e for e in EV if e["seg"]=="credits"]
CB0=CRED[0]["start"]; CB1=next(e["start"] for e in CRED if e.get("card")=="credits_legal")
BOARDABLE={"recep_wide","recep_wide2","two_pl","peter_mid","queue_grp"}

def move_expr(move, N):
    N=max(N-1,1)
    c=("x='iw/2-(iw/zoom/2)'","y='ih/2-(ih/zoom/2)'")
    if move=="push_slow":  return (f"z='1.00+0.100*on/{N}'",)+c
    if move=="push_micro": return (f"z='1.02+0.055*on/{N}'",)+c
    if move=="pull_slow":  return (f"z='1.13-0.110*on/{N}'",)+c
    if move=="drift_r":    return ("z='1.075'", f"x='(iw-iw/zoom)*(0.08+0.84*on/{N})'", c[1])
    if move=="drift_l":    return ("z='1.075'", f"x='(iw-iw/zoom)*(0.92-0.84*on/{N})'", c[1])
    return (f"z='1.01+0.03*on/{N}'",)+c

def render(k, e):
    d=max(e.get("vdur",e["dur"]),0.12); N=max(int(round(d*FPS)),3); d=N/FPS
    out=f"{OUT}/{k:04d}.mp4"
    ins=[]; vf=[]; fc=None
    if e["kind"]=="card" or (e["kind"]=="line" and not e.get("shot")):
        card = e.get("card") or ("credits_roll" if e["seg"]=="credits" else "void")
        img=f"{CD}/{card}.png"
        ins=["-loop","1","-framerate",str(FPS),"-t",f"{d}","-i",img]
        if card=="credits_roll":
            a=(e["start"]-CB0)/max(CB1-CB0,0.1); b=(e["end"]-CB0)/max(CB1-CB0,0.1)
            ih=subprocess.run(["identify","-format","%h",img],capture_output=True,text=True).stdout
            span=max(int(ih)-H,1)
            vf=[f"crop={W}:{H}:0:'{a*span:.1f}+({(b-a)*span:.1f})*t/{d:.3f}'"]
        elif card=="whiteout":
            vf=[f"scale={W}:{H}","noise=alls=14:allf=t"]
        else:
            z,x,y=move_expr("card",N)
            vf=[f"zoompan={z}:{x}:{y}:d=1:s={W}x{H}:fps={FPS}"]
    else:
        shot=e["shot"]; img=f"{PL}/{shot}.png"
        mv=e.get("move") or SHOTS.get(shot,{}).get("move","push_slow")
        z,x,y=move_expr(mv,N)
        ins=["-loop","1","-framerate",str(FPS),"-t",f"{d}","-i",img]
        vf=[f"zoompan={z}:{x}:{y}:d=1:s={W}x{H}:fps={FPS}"]
        fxs=e.get("fx") or []
        # --- practical gag overlays ---
        if ("flip_none" in fxs or "flip_047" in fxs) and shot in BOARDABLE:
            if "flip_047" in fxs:
                ins+=["-loop","1","-framerate",str(FPS),"-t",f"{d}","-i",f"{PR}/board_046.png",
                      "-loop","1","-framerate",str(FPS),"-t",f"{d}","-i",f"{PR}/board_flip.png",
                      "-loop","1","-framerate",str(FPS),"-t",f"{d}","-i",f"{PR}/board_047.png"]
                t1,t2=d*0.46,d*0.60
                fc=(f"[0:v]{','.join(vf)}[bg];"
                    f"[bg][1:v]overlay=660:44:enable='lt(t,{t1:.2f})'[a];"
                    f"[a][2:v]overlay=660:44:enable='between(t,{t1:.2f},{t2:.2f})'[b];"
                    f"[b][3:v]overlay=660:44:enable='gt(t,{t2:.2f})',setsar=1[v]")
            else:
                ins+=["-loop","1","-framerate",str(FPS),"-t",f"{d}","-i",f"{PR}/board_046.png"]
                fc=(f"[0:v]{','.join(vf)}[bg];"
                    f"[bg][1:v]overlay=660:44:format=auto,setsar=1[v]")
        elif "shutter" in fxs:
            ins+=["-loop","1","-framerate",str(FPS),"-t",f"{d}","-i",f"{PR}/lunch_sign.png"]
            fc=(f"[0:v]{','.join(vf)}[bg];"
                f"[bg][1:v]overlay=510:'-340+min(640,640*(t/{d*0.45:.2f}))':format=auto,setsar=1[v]")
    cmd=["ffmpeg","-y","-v","error"]+ins
    if fc: cmd+=["-filter_complex",fc,"-map","[v]"]
    else:  cmd+=["-vf",",".join(vf)+",setsar=1"]
    cmd+=["-frames:v",str(N),"-c:v","libx264","-preset","veryfast","-crf","18",
          "-pix_fmt","yuv420p","-r",str(FPS),"-video_track_timescale","12288","-an",out]
    subprocess.run(cmd,check=True,capture_output=True)
    return k,out,N

jobs=list(enumerate(EV))
done=0
with cf.ThreadPoolExecutor(max_workers=4) as ex:
    futs=[ex.submit(render,k,e) for k,e in jobs]
    for f in cf.as_completed(futs):
        k,o,n=f.result(); done+=1
        if done%40==0: print(f"  {done}/{len(jobs)} clips",flush=True)
with open(f"{ROOT}/concat.txt","w") as f:
    for k,_ in jobs: f.write(f"file '{OUT}/{k:04d}.mp4'\n")
print(f"rendered {done} clips")
