#!/usr/bin/env python3
"""Stage 3 — place dialogue, lay the score, duck under speech, write the episode audio master."""
import json, wave, numpy as np, subprocess, os
import synth
SR=synth.SR; ROOT="/home/user/judgement-tales/.work"
L=json.load(open(f"{ROOT}/layout.json")); EV=L["events"]; TOT=L["total"]
N=int(TOT*SR)+SR
dlg=np.zeros(N); mus=np.zeros(N); fx=np.zeros(N)

def rd(p):
    w=wave.open(p,'rb'); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
    if w.getnchannels()==2: a=a.reshape(-1,2).mean(1)
    if w.getframerate()!=SR:
        a=np.interp(np.linspace(0,len(a),int(len(a)*SR/w.getframerate())),np.arange(len(a)),a)
    return a
def put(buf,x,at,g=1.0):
    s=int(at*SR); e=min(len(buf),s+len(x))
    if s<len(buf): buf[s:e]+=x[:e-s]*g

# ---- dialogue -----------------------------------------------------------
for e in EV:
    if e["kind"]=="line": put(dlg, rd(e["file"]), e["start"], 1.0)

# ---- segment windows ----------------------------------------------------
seg={}
for e in EV:
    s=seg.setdefault(e["seg"],[1e9,0]); s[0]=min(s[0],e["start"]); s[1]=max(s[1],e["end"])
thunder=next((e["start"] for e in EV if "thunder" in e["fx"]), None)
skitC  =seg["C"][0]
print(f"thunder cut at {thunder:.1f}s · muzak returns at {skitC:.1f}s")

# ---- score --------------------------------------------------------------
put(mus, synth.sfx("taxi", seg["cold"][1]-seg["cold"][0]), seg["cold"][0], 0.30)
put(mus, synth.harp_theme(6.5), seg["titles"][0]+0.2, 0.95)          # celestial…
put(mus, synth.muzak(seg["titles"][1]-seg["titles"][0]-3.0), seg["titles"][0]+3.0, 0.85)  # …curdles
beds=[(seg["A"][0], thunder), (skitC, seg["credits"][1])]            # muzak dies on the thunder
for a,b in beds:
    if b and b>a: put(mus, synth.muzak(b-a+2.0), a, 0.55)
# ---- spot effects -------------------------------------------------------
for e in EV:
    for name in e["fx"]:
        if name in ("muzak_in","muzak_up","theme"): continue
        put(fx, synth.sfx(name, max(1.0, e["dur"])), e["start"], 1.0)

# ---- duck the score under speech ---------------------------------------
w=int(0.12*SR); envd=np.convolve(np.abs(dlg), np.ones(w)/w, mode="same")
duck=1.0-0.78*np.clip(envd/0.07,0,1)
k=int(0.35*SR); duck=np.convolve(duck,np.ones(k)/k,mode="same")
mus*=duck; fx*=(0.45+0.55*duck)

mix=dlg*1.0+mus*0.55+fx*0.50
mix=np.tanh(mix*0.92)*0.97
mix=np.clip(mix,-1,1)

raw=f"{ROOT}/episode_audio_raw.wav"
with wave.open(raw,'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix*32767).astype(np.int16).tobytes())
out=f"{ROOT}/episode_audio.wav"
subprocess.run(["ffmpeg","-y","-v","error","-i",raw,
  "-af","aresample=48000,highpass=f=55,loudnorm=I=-16:TP=-1.5:LRA=11,alimiter=limit=0.95",
  "-ac","2","-ar","48000",out],check=True)
os.remove(raw)
d=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out],
                 capture_output=True,text=True).stdout.strip()
print(f"wrote {out}  duration {float(d):.2f}s")
