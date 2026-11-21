#!/usr/bin/env python3
"""Stage 6 — concat the cuts, grade to the retro broadcast look, spin the watermark, mux audio + subs."""
import json, os, subprocess, sys
ROOT="/home/user/judgement-tales/.work"; REPO="/home/user/judgement-tales"
OUT=f"{REPO}/out"; os.makedirs(OUT,exist_ok=True)
W,H,FPS=1920,1080,24
SCAN=f"{ROOT}/scanlines.png"; LOGO=f"{ROOT}/logo.png"

# scanline field (2px dark line every 4px, low alpha)
if not os.path.exists(SCAN):
    subprocess.run(["convert","-size",f"{W}x4","xc:none","-fill","#00000030",
                    "-draw",f"rectangle 0,0 {W},1","-write","mpr:row","+delete",
                    "-size",f"{W}x{H}","tile:mpr:row",SCAN],check=True)

stitched=f"{ROOT}/stitched.mp4"
if not os.path.exists(stitched) or "--restitch" in sys.argv:
    subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0",
                    "-i",f"{ROOT}/concat.txt","-c","copy",stitched],check=True)
    print("stitched ok")

graded=f"{ROOT}/graded.mp4"
fc=(
 "[0:v]eq=contrast=1.06:saturation=1.05:gamma=0.99,"
 "vignette=PI/4.6,"
 "noise=alls=7:allf=t+u[g];"
 "[1:v]format=rgba[sc];[g][sc]overlay=0:0:format=auto[s];"
 f"[2:v]scale=150:150,format=rgba,rotate=2*PI*t/25:c=none:ow=rotw(iw):oh=roth(ih),"
 "colorchannelmixer=aa=0.66[wm];"
 "[s][wm]overlay=W-w-56:56:format=auto,setsar=1[v]"
)
subprocess.run(["ffmpeg","-y","-v","error","-i",stitched,
  "-loop","1","-i",SCAN,"-loop","1","-i",LOGO,
  "-filter_complex",fc,"-map","[v]","-frames:v",str(int(600*FPS)),
  # YouTube's recommended upload settings for 1080p24 SDR: H.264 High, progressive, 4:2:0,
  # closed GOP of half the frame rate, 2 B-frames, ~8 Mbps or better, moov atom at the front.
  "-c:v","libx264","-preset","medium","-crf","17","-maxrate","14M","-bufsize","28M",
  "-profile:v","high","-g","12","-bf","2","-flags","+cgop","-pix_fmt","yuv420p",
  "-r",str(FPS),"-movflags","+faststart","-an",graded],check=True)
print("graded ok")

master=f"{OUT}/judgement-tales-s01e01-the-queue.mp4"
subprocess.run(["ffmpeg","-y","-v","error","-i",graded,"-i",f"{ROOT}/episode_audio.wav",
  "-i",f"{ROOT}/judgement-tales-s01e01.en.srt","-i",f"{ROOT}/judgement-tales-s01e01.en-sdh.srt",
  "-map","0:v:0","-map","1:a:0","-map","2:s:0","-map","3:s:0",
  "-c:v","copy","-af","volume=-0.9dB","-c:a","aac","-b:a","384k","-ar","48000","-ac","2","-c:s","mov_text",
  "-metadata:s:s:0","language=eng","-metadata:s:s:0","title=English",
  "-metadata:s:s:1","language=eng","-metadata:s:s:1","title=English — speaker names & sounds",
  # MP4 drops `title` on subtitle streams; players show handler_name instead
  "-metadata:s:s:0","handler_name=English","-metadata:s:s:1","handler_name=English — speaker names & sounds",
  "-metadata","title=JUDGEMENT TALES S01E01 - The Queue",
  "-metadata","artist=WANNATION MEDIA",
  "-metadata","copyright=WANNATION MEDIA - a division of WANNATION HOLDINGS (PTY) LTD - Reg No: 2026/463724/07",
  "-t","600","-movflags","+faststart",master],check=True)
for f in ("judgement-tales-s01e01.en.srt","judgement-tales-s01e01.en-sdh.srt",
          "judgement-tales-s01e01.en.vtt","judgement-tales-s01e01.en-sdh.vtt"):
    subprocess.run(["cp",f"{ROOT}/{f}",f"{OUT}/{f}"],check=True)
print("master:",master)
