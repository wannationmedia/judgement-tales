#!/usr/bin/env python3
"""Series key art: channel banner, profile mark, feed and story posts."""
import subprocess, os
W="/home/user/judgement-tales"; PL=f"{W}/.work/plates"; PR=f"{W}/.work/props"; OUT=f"{W}/out/social/key-art"
NAVY="#101d33"; GOLD="#f0d070"; GOLD2="#d9b24c"; CREAM="#f3ead6"; INK="#0a0a0f"
SER="Liberation-Serif-Bold"; SERR="Liberation-Serif"
def run(a): subprocess.run(a,check=True)
def halo(x,y,rx,ry,sw=8): return ["-fill","none","-stroke",GOLD,"-strokewidth",str(sw),
                                  "-draw",f"ellipse {x},{y} {rx},{ry} 0,360","-stroke","none"]
def t(s,size,y,fill=GOLD,font=SER,grav="north",stroke=6):
    return ["-font",font,"-pointsize",str(size),"-gravity",grav,"-stroke",INK,"-strokewidth",str(stroke),
            "-fill",INK,"-annotate",f"+0+{y}",s,"-stroke","none","-fill",fill,"-annotate",f"+0+{y}",s]
def band(w,h,y0,y1,a="E0"):
    return ["(","-size",f"{w}x{h}","xc:none","-fill",f"{NAVY}{a}","-draw",f"rectangle 0,{y0} {w},{y1}",
            "-blur","0x30",")","-compose","over","-composite"]

# YouTube channel banner 2560x1440 — everything that matters inside the centred 1546x423 safe area
run(["convert",f"{W}/images/1.jpg","-filter","Lanczos","-resize","2560x1440!","-modulate","70,90",
     *band(2560,1440,470,970),*halo(1280,560,92,24,7),
     *t("JUDGEMENT TALES",150,590),*t("Heaven runs on forms.",56,770,CREAM,SERR,stroke=4),
     *t("an animated comedy  ·  WANNATION MEDIA",36,850,GOLD2,SERR,stroke=3),
     "-quality","90",f"{OUT}/youtube-channel-banner-2560x1440.jpg"])
# profile mark 800x800 (YouTube/TikTok/IG crop it to a circle — the roundel already is one)
run(["convert","-size","800x800",f"xc:{NAVY}","(",f"{W}/.work/logo.png","-resize","720x720",")",
     "-gravity","center","-composite",f"{OUT}/profile-mark-800.png"])
# square feed post 1080x1080 — the core joke
run(["convert",f"{PL}/two_pl.png","-resize","1920x1080!","-gravity","center","-crop","1080x1080+120+0","+repage",
     "-modulate","100,110",*band(1080,1080,700,1080,"F0"),
     "(",f"{PR}/board_046.png","-resize","360x",")","-gravity","northeast","-geometry","+40+40","-composite",
     *t("JUDGEMENT TALES",86,770),*t("Episode 1  ·  The Queue",44,880,CREAM,SERR,stroke=3),
     *t("He's ticket 047. They're serving 046.",38,950,CREAM,SERR,stroke=3),
     "-quality","92",f"{OUT}/post-square-1080.jpg"])
# portrait feed post 1080x1350 — Sven, the series' most clickable face
run(["convert",f"{PL}/sven_cu.png","-resize","2400x1350!","-gravity","west","-crop","1080x1350+60+0","+repage",
     "-modulate","100,110",*band(1080,1350,930,1350,"F0"),
     *t("IN LINE SINCE 862 AD",64,990,CREAM,"Inter-Black",stroke=8),
     *t("JUDGEMENT TALES",80,1100),*t("Episode 1  ·  The Queue",42,1205,CREAM,SERR,stroke=3),
     "-quality","92",f"{OUT}/post-portrait-1080x1350.jpg"])
# story 1080x1920 — launch announcement (no date baked in; add it in the story sticker)
run(["convert","-size","1080x1920",f"xc:{NAVY}",
     "(",f"{PL}/sven_cu.png","-resize","x1080","-gravity","northwest","-crop","1080x1080+0+0","+repage",")",
     "-gravity","north","-geometry","+0+330","-composite",
     *halo(540,1500,70,19,6),*t("JUDGEMENT TALES",96,1530),
     *t("A new animated comedy",46,1660,CREAM,SERR,stroke=3),
     *t("EPISODE 1 · THE QUEUE",42,1730,GOLD2,"Inter-Black",stroke=5),
     *t("NOW ON YOUTUBE",58,200,CREAM,"Inter-Black",stroke=8),
     "-quality","92",f"{OUT}/story-launch-1080x1920.jpg"])
for f in sorted(os.listdir(OUT)): print(f"{f:<44}{os.path.getsize(f'{OUT}/{f}')//1024:>6} KB")
