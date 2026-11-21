#!/usr/bin/env python3
"""Stage 7 — trailer + 9:16 social cuts, taken from the finished master."""
import json, os, re, subprocess
ROOT="/home/user/judgement-tales/.work"; REPO="/home/user/judgement-tales"
OUT=f"{REPO}/out"; MASTER=f"{OUT}/judgement-tales-s01e01-the-queue.mp4"
C=json.load(open(f"{ROOT}/cuts.json")); LOGO=f"{ROOT}/logo.png"
SRT=f"{ROOT}/judgement-tales-s01e01.en.srt"
os.makedirs(OUT,exist_ok=True)

def parse_srt(p):
    out=[]
    for blk in open(p,encoding="utf-8").read().strip().split("\n\n"):
        L=blk.split("\n")
        if len(L)<3: continue
        a,b=L[1].split(" --> ")
        def s(x):
            h,m,rest=x.split(":"); sec,ms=rest.split(",")
            return int(h)*3600+int(m)*60+int(sec)+int(ms)/1000
        out.append((s(a),s(b),"\n".join(L[2:])))
    return out
CUES=parse_srt(SRT)
def ts(x):
    h=int(x//3600); m=int(x%3600//60); s=int(x%60); ms=int(round((x-int(x))*1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
def shifted_srt(a,b,path,offset=0.0):
    n=0
    with open(path,"w",encoding="utf-8") as f:
        for st,en,tx in CUES:
            if en<=a or st>=b: continue
            n+=1
            f.write(f"{n}\n{ts(max(0,st-a)+offset)} --> {ts(min(b,en)-a+offset)}\n{tx}\n\n")
    return n

STYLE=("FontName=DejaVu Serif,Fontsize=15,PrimaryColour=&H00FFFFFF,OutlineColour=&H00101D33,"
       "BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=26,Bold=1")

def vertical(key, meta):
    a,b=meta["span"]; d=b-a
    sub=f"{ROOT}/tmp_{key}.srt"; shifted_srt(a,b,sub)
    out=f"{OUT}/judgement-tales-s01e01-{key}-vertical.mp4"
    fc=(
      "[0:v]scale=216:384:force_original_aspect_ratio=increase,crop=216:384,"
      "gblur=sigma=7,scale=1080:1920,eq=brightness=-0.16:saturation=0.75[bg];"
      "[0:v]scale=1080:-2[fg];"
      "[bg][fg]overlay=0:(H-h)/2:format=auto[v0];"
      f"[v0]subtitles='{sub}':force_style='{STYLE}'[v1];"
      "[1:v]scale=132:132,format=rgba,rotate=2*PI*t/25:c=none:ow=rotw(iw):oh=roth(ih),"
      "colorchannelmixer=aa=0.70[wm];"
      "[v1][wm]overlay=W-w-34:150:format=auto,setsar=1[v]"
    )
    subprocess.run(["ffmpeg","-y","-v","error","-ss",str(a),"-t",str(d),"-i",MASTER,
      "-loop","1","-i",LOGO,"-filter_complex",fc,"-map","[v]","-map","0:a:0",
      "-c:v","libx264","-preset","veryfast","-crf","23","-maxrate","9M","-bufsize","18M",
      "-pix_fmt","yuv420p","-r","24","-c:a","aac","-b:a","160k","-ar","48000","-ac","2",
      "-t",str(d),"-frames:v",str(int(round(d*24))),"-movflags","+faststart",out],check=True)
    os.remove(sub)
    real=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
          "-of","csv=p=0",out],capture_output=True,text=True).stdout)
    return out, real

def trailer():
    parts=[]; pos=0.0; srtpath=f"{ROOT}/tmp_trailer.srt"; cues=[]
    for i,(a,b) in enumerate(C["trailer"]):
        p=f"{ROOT}/tr_{i}.mp4"
        subprocess.run(["ffmpeg","-y","-v","error","-ss",str(a),"-t",str(b-a),"-i",MASTER,
          "-vf","scale=1920:1080,setsar=1","-c:v","libx264","-preset","veryfast","-crf","19",
          "-pix_fmt","yuv420p","-r","24","-video_track_timescale","12288",
          "-c:a","aac","-b:a","192k","-ar","48000","-ac","2",p],check=True)
        for st,en,tx in CUES:
            if en<=a or st>=b: continue
            cues.append((max(st,a)-a+pos, min(en,b)-a+pos, tx))
        pos+=(b-a); parts.append(p)
    ta,tb=C["trailer_title"]
    p=f"{ROOT}/tr_title.mp4"
    subprocess.run(["ffmpeg","-y","-v","error","-ss",str(ta),"-t",str(tb-ta),"-i",MASTER,
      "-vf","scale=1920:1080,setsar=1","-c:v","libx264","-preset","veryfast","-crf","19",
      "-pix_fmt","yuv420p","-r","24","-video_track_timescale","12288",
      "-c:a","aac","-b:a","192k","-ar","48000","-ac","2",p],check=True)
    parts.append(p)
    with open(srtpath,"w",encoding="utf-8") as f:
        for n,(st,en,tx) in enumerate(cues,1): f.write(f"{n}\n{ts(st)} --> {ts(en)}\n{tx}\n\n")
    lst=f"{ROOT}/trailer_concat.txt"
    open(lst,"w").write("".join(f"file '{p}'\n" for p in parts))
    out=f"{OUT}/judgement-tales-s01e01-trailer.mp4"
    subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",lst,
      "-c","copy",f"{ROOT}/trailer_raw.mp4"],check=True)
    subprocess.run(["ffmpeg","-y","-v","error","-i",f"{ROOT}/trailer_raw.mp4",
      "-i",srtpath,"-map","0:v:0","-map","0:a:0","-map","1:s:0","-c:v","copy","-c:a","copy",
      "-c:s","mov_text","-metadata:s:s:0","language=eng",
      "-metadata","title=JUDGEMENT TALES S01E01 - Trailer",
      "-metadata","artist=WANNATION MEDIA","-movflags","+faststart",out],check=True)
    for p in parts+[f"{ROOT}/trailer_raw.mp4",lst,srtpath]: os.remove(p)
    real=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
          "-of","csv=p=0",out],capture_output=True,text=True).stdout)
    return out, real

res={}
import sys
if "--skip-trailer" in sys.argv:
    tf=f"{OUT}/judgement-tales-s01e01-trailer.mp4"
    d=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",tf],capture_output=True,text=True).stdout)
    res["trailer"]=dict(file=os.path.basename(tf),seconds=round(d,2))
else:
    o,d=trailer(); res["trailer"]=dict(file=os.path.basename(o),seconds=round(d,2))
print(f"trailer           {d:6.2f}s")
for k,m in C["cuts"].items():
    o,d=vertical(k,m); res[k]=dict(file=os.path.basename(o),seconds=round(d,2),
                                   title=m["title"],caption=m["caption"],
                                   span=m["span"],platform=m["platform"])
    print(f"{k:<22}{d:6.2f}s  {o}")
json.dump(res,open(f"{ROOT}/social_built.json","w"),indent=1)
