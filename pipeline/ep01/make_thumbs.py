#!/usr/bin/env python3
"""YouTube thumbnails (1280x720, <2MB). One joke each, readable at phone size.
Text stays top-left/left; bottom-right is where YouTube prints the duration."""
import subprocess, os
W="/home/user/judgement-tales"; PL=f"{W}/.work/plates"; PR=f"{W}/.work/props"; OUT=f"{W}/out/youtube"
NAVY="#101d33"; GOLD="#f0d070"; WHITE="#ffffff"; INK="#0a0a0f"
def run(a): subprocess.run(a,check=True)
def text(x,y,s,size,fill=WHITE,stroke=12):
    return ["-font","Inter-Black","-pointsize",str(size),"-gravity","northwest",
            "-stroke",INK,"-strokewidth",str(stroke),"-fill",INK,"-annotate",f"+{x}+{y}",s,
            "-stroke","none","-fill",fill,"-annotate",f"+{x}+{y}",s]
def brand(): return ["-font","Liberation-Serif-Bold","-pointsize","34","-gravity","northwest",
                     "-stroke",INK,"-strokewidth","5","-fill",INK,"-annotate","+44+652","JUDGEMENT TALES",
                     "-stroke","none","-fill",GOLD,"-annotate","+44+652","JUDGEMENT TALES"]
def leftfade(width):
    return ["(","-size",f"{width}x720","gradient:#101d33F2-#101d3300","-rotate","-90",")",
            "-gravity","west","-compose","over","-composite","-compose","over"]

# A — the core joke: board says 046, he holds 047, it's been that way for 400 years
run(["convert","-size","1280x720",f"xc:{NAVY}",
     "(",f"{PL}/lwazi_cu.png","-resize","1280x720!","-modulate","106,112",")",
     "-geometry","+250+0","-composite",*leftfade(760),
     "(",f"{PR}/board_046.png","-resize","430x",")","-gravity","northwest","-geometry","+44+44","-composite",
     "(",f"{W}/images/1.jpg","-crop","118x124+647+451","+repage","-resize","250x","-bordercolor","white",
         "-border","6","-background","none","-rotate","-9",")","-gravity","northwest","-geometry","+455+380","-composite",
     *text(44,300,"400",150,GOLD), *text(44,455,"YEARS.",104), *brand(),
     "-quality","90",f"{OUT}/thumbnail-a-400-years.jpg"])
# B — the Viking who has queued since 862. Unmirrored (the sign behind him must read the right way);
# Sven holds the left, the headline sits top-right, clear of the bottom-right duration badge.
def rtext(y,s,size,fill=WHITE,stroke=12):
    return ["-font","Inter-Black","-pointsize",str(size),"-gravity","northeast",
            "-stroke",INK,"-strokewidth",str(stroke),"-fill",INK,"-annotate",f"+40+{y}",s,
            "-stroke","none","-fill",fill,"-annotate",f"+40+{y}",s]
run(["convert",f"{PL}/sven_cu.png","-resize","1280x720!","-modulate","104,112",
     "(","-size","700x720","gradient:#101d3300-#101d33F2","-rotate","-90",")",
     "-gravity","east","-compose","over","-composite",
     *rtext(40,"IN LINE",118), *rtext(168,"SINCE",118), *rtext(296,"862 AD",132,GOLD),
     "-font","Liberation-Serif-Bold","-pointsize","34","-gravity","northeast",
     "-stroke",INK,"-strokewidth","5","-fill",INK,"-annotate","+40+470","JUDGEMENT TALES",
     "-stroke","none","-fill",GOLD,"-annotate","+40+470","JUDGEMENT TALES",
     "-quality","90",f"{OUT}/thumbnail-b-since-862.jpg"])
# C — the fast-track leads to the Complaints Department (unmirrored: the tablets must read)
run(["convert","-size","1280x720",f"xc:{NAVY}",
     "(",f"{PL}/moses_mid.png","-resize","1280x720!","-modulate","104,112",")","-geometry","+300+0","-composite",
     *leftfade(720),
     *text(40,48,"THE",96), *text(40,150,"FAST",130,GOLD), *text(40,282,"TRACK",130,GOLD),
     *text(40,430,"(to complaints)",54), *brand(),
     "-quality","90",f"{OUT}/thumbnail-c-fast-track.jpg"])
for f in sorted(os.listdir(OUT)):
    if f.endswith(".jpg"): print(f, os.path.getsize(f"{OUT}/{f}")//1024, "KB")
