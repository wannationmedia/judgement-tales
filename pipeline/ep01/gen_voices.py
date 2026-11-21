#!/usr/bin/env python3
"""Stage 1 — synthesize every spoken line, treat it, and measure its real duration."""
import json, os, subprocess, sys, concurrent.futures as cf
from cast import CAST
from timeline import TL

ROOT = "/home/user/judgement-tales/.work"
VOICES = f"{ROOT}/voices"; OUT = f"{ROOT}/vo"; os.makedirs(OUT, exist_ok=True)
SR = 48000

def dur(p):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                        "-of","csv=p=0",p],capture_output=True,text=True)
    return float(r.stdout.strip() or 0)

def synth(i, who, txt):
    c = CAST[who]
    raw = f"{OUT}/{i:03d}_{who}.raw.wav"; fin = f"{OUT}/{i:03d}_{who}.wav"
    cmd = ["python3","-m","piper","-m",f"{VOICES}/{c['model']}.onnx",
           "--length-scale",str(c["len"]),"--noise-scale","0.60","--noise-w-scale","0.75",
           "--sentence-silence","0.12","-f",raw]
    if c["spk"] is not None: cmd += ["-s",str(c["spk"])]
    subprocess.run(cmd, input=txt, text=True, capture_output=True, check=True)
    p = c["pitch"]
    ch = [f"asetrate={SR}*{p}", f"aresample={SR}", f"atempo={1/p:.6f}"] if abs(p-1)>1e-4 else [f"aresample={SR}"]
    ch.append(c["eq"])
    # marble-hall air on in-scene dialogue; narration and PA stay dry/close
    if who not in ("LWAZI_VO","TANNOY"): ch.append("aecho=0.8:0.85:28:0.11")
    ch += ["dynaudnorm=f=180:g=9:p=0.72", "alimiter=limit=0.94", "afade=t=in:st=0:d=0.02"]
    subprocess.run(["ffmpeg","-y","-v","error","-i",raw,"-af",",".join(ch),
                    "-ar",str(SR),"-ac","1",fin], check=True)
    os.remove(raw)
    return i, fin, dur(fin)

jobs = [(i,e["who"],e["txt"]) for i,e in enumerate(TL) if e["ev"]=="line"]
res = {}
with cf.ThreadPoolExecutor(max_workers=4) as ex:
    for i,f,d in ex.map(lambda a: synth(*a), jobs):
        res[i] = dict(file=f, dur=d)
        print(f"  {i:03d} {os.path.basename(f):<26} {d:5.2f}s", flush=True)
json.dump(res, open(f"{ROOT}/vo_durations.json","w"), indent=1)
tot = sum(v["dur"] for v in res.values())
print(f"\n{len(res)} lines · total spoken audio {tot:.1f}s ({tot/60:.1f} min)")
