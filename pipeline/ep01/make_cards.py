#!/usr/bin/env python3
"""Title, caption and credit cards in the show's own signage palette."""
import os, subprocess
OUT="/home/user/judgement-tales/.work/cards"; os.makedirs(OUT,exist_ok=True)
PL="/home/user/judgement-tales/.work/plates"
W,H=1920,1080
NAVY="#1b3156"; DEEP="#101d33"; GOLD="#d9b24c"; BRIGHT="#f0d070"; CREAM="#f3ead6"; BLACK="#07080c"
SER="Liberation-Serif-Bold"; SERR="Liberation-Serif"; SANS="DejaVu-Sans"

def run(a): subprocess.run(a,check=True)
def halo(x,y,rx,ry,sw=7,col=BRIGHT):
    return ["-fill","none","-stroke",col,"-strokewidth",str(sw),
            "-draw",f"ellipse {x},{y} {rx},{ry} 0,360","-stroke","none"]
def frame(col=GOLD):
    return ["-fill","none","-stroke",col,"-strokewidth","4",
            "-draw",f"rectangle 70,60 {W-70},{H-60}","-strokewidth","1.5",
            "-draw",f"rectangle 88,78 {W-88},{H-78}","-stroke","none"]
def navy_bg(dark=False):
    return ["-size",f"{W}x{H}",f"xc:{DEEP if dark else NAVY}",
            "-attenuate","0.55","+noise","Gaussian","-blur","0x0.6"]

# ---- station slate -------------------------------------------------------
run(["convert"]+navy_bg(True)+frame()+halo(W//2,398,118,34)+
    ["-font",SER,"-pointsize","96","-fill",BRIGHT,"-gravity","north",
     "-annotate","+0+440","WANNATION MEDIA",
     "-font",SERR,"-pointsize","38","-fill",CREAM,
     "-annotate","+0+570","a division of WANNATION HOLDINGS (PTY) LTD",
     "-font",SANS,"-pointsize","28","-fill",GOLD,
     "-annotate","+0+640","Reg No: 2026/463724/07",
     "-font",SANS,"-pointsize","26","-fill",GOLD,"-gravity","south",
     "-annotate","+0+110","TRANSMISSION 01   ·   SERIES 1   ·   EPISODE 1",
     f"{OUT}/slate.png"])
# ---- cold-open caption cards --------------------------------------------
def caption(name, big, small=None, rule=True):
    a=["convert","-size",f"{W}x{H}",f"xc:{BLACK}","-attenuate","0.5","+noise","Gaussian","-blur","0x0.7",
       "-font",SER,"-pointsize","104","-fill",BRIGHT,"-gravity","center","-annotate","+0-30",big]
    if rule: a+=["-fill",GOLD,"-draw",f"rectangle {W//2-170},{H//2+50} {W//2+170},{H//2+54}"]
    if small: a+=["-font",SERR,"-pointsize","40","-fill",CREAM,"-annotate","+0+120",small]
    run(a+[f"{OUT}/{name}.png"])
caption("coldtitle","THE LAST TUESDAY")
caption("card_taxi","JOHANNESBURG","an ordinary Tuesday")
caption("card_rail","THE GRAB RAIL","do not let go")
caption("card_montage","THE FAVOUR ECONOMY","everybody owes somebody")
# ---- whiteout ------------------------------------------------------------
run(["convert","-size",f"{W}x{H}","xc:white","-attenuate","0.35","+noise","Gaussian",f"{OUT}/whiteout.png"])
# ---- void (VO over black) ------------------------------------------------
run(["convert","-size",f"{W}x{H}",f"xc:{BLACK}","-attenuate","0.6","+noise","Gaussian","-blur","0x0.8",
     f"{OUT}/void.png"])
# ---- presents card -------------------------------------------------------
run(["convert"]+navy_bg()+frame()+halo(W//2,430,96,28)+
    ["-font",SERR,"-pointsize","46","-fill",CREAM,"-gravity","north","-annotate","+0+300","WANNATION MEDIA",
     "-font",SERR,"-pointsize","36","-fill",GOLD,"-annotate","+0+372","presents",
     "-font",SER,"-pointsize","62","-fill",BRIGHT,"-annotate","+0+500","AN AFTERLIFE RUN LIKE AN OFFICE",
     "-font",SANS,"-pointsize","27","-fill",CREAM,"-gravity","south","-annotate","+0+120",
     "A fictional satirical comedy.  Casting choices are creative interpretations, not historical claims.",
     f"{OUT}/title_card.png"])
# ---- main title (over the gates) ----------------------------------------
run(["convert",f"{PL}/gates.png","-resize",f"{W}x{H}!","-modulate","62,78,104","-blur","0x1.5",
     "(","-size",f"{W}x{H}","xc:black","-fill","white",
     "-draw",f"ellipse {W//2},{H//2} 820,560 0,360","-blur","0x160",")",
     "-compose","multiply","-composite"]+
    halo(W//2,352,150,42,9)+
    ["-font",SER,"-pointsize","150","-fill",BRIGHT,"-stroke",DEEP,"-strokewidth","3",
     "-gravity","north","-annotate","+0+400","JUDGEMENT TALES","-stroke","none",
     "-font",SERR,"-pointsize","42","-fill",CREAM,"-annotate","+0+600","Series 1   ·   Episode 1",
     "-font",SER,"-pointsize","58","-fill",GOLD,"-annotate","+0+672","THE QUEUE",
     f"{OUT}/title_main.png"])
# ---- skit cards ----------------------------------------------------------
def skit(name,label,title):
    run(["convert"]+navy_bg()+frame()+halo(W//2,408,86,25)+
        ["-font",SANS,"-pointsize","34","-fill",GOLD,"-gravity","north","-annotate","+0+300",label,
         "-font",SER,"-pointsize","108","-fill",BRIGHT,"-annotate","+0+470",title,
         f"{OUT}/{name}.png"])
skit("card_skitB","SKIT B","THE FAST-TRACK")
skit("card_skitC","SKIT C","PROCESSING ERROR")
# ---- credits -------------------------------------------------------------
CH=2400
roll=["convert","-size",f"{W}x{CH}",f"xc:{DEEP}","-attenuate","0.45","+noise","Gaussian","-blur","0x0.6",
      "-font",SER,"-pointsize","72","-fill",BRIGHT,"-gravity","north","-annotate","+0+120",
      "A WANNATION MEDIA PRODUCTION",
      "-font",SERR,"-pointsize","40","-fill",CREAM,"-annotate","+0+250","JUDGEMENT TALES",
      "-font",SER,"-pointsize","46","-fill",GOLD,"-annotate","+0+330",'S01 E01  "THE QUEUE"',
      "-font",SANS,"-pointsize","30","-fill",GOLD,"-annotate","+0+470","CAST",
      "-font",SERR,"-pointsize","36","-fill",CREAM,"-annotate","+0+530",
      "LWAZI \"LUCKY\" NKOSI\nST. PETER\nSVEN\nNIGEL \"THE BLAGGER\"\nTHE SULTAN\nBRENDA\nCANDICE\nMOSES",
      "-font",SANS,"-pointsize","30","-fill",GOLD,"-annotate","+0+1000","PRODUCTION",
      "-font",SERR,"-pointsize","34","-fill",CREAM,"-annotate","+0+1060",
      "Written, scored, animated and assembled\nby WANNATION MEDIA\n\nOriginal score and sound design\nsynthesized for this episode\n\nScene art direction from the\nJUDGEMENT TALES show bible",
      "-font",SER,"-pointsize","40","-fill",BRIGHT,"-annotate","+0+1560",
      "WANNATION MEDIA",
      "-font",SERR,"-pointsize","32","-fill",CREAM,"-annotate","+0+1630",
      "a division of WANNATION HOLDINGS (PTY) LTD",
      "-font",SANS,"-pointsize","30","-fill",GOLD,"-annotate","+0+1690","Reg No: 2026/463724/07",
      "-font",SANS,"-pointsize","26","-fill",CREAM,"-annotate","+0+1800",
      "A work of fiction. Satire is aimed at bureaucracy, power and individual characters.\nCasting choices are creative interpretations, not historical or factual claims\nabout any population, and not a statement about anyone's faith.",
      f"{OUT}/credits_roll.png"]
run(roll)
run(["convert"]+navy_bg(True)+frame()+halo(W//2,330,110,32)+
    ["-font",SER,"-pointsize","78","-fill",BRIGHT,"-gravity","north","-annotate","+0+380","WANNATION MEDIA",
     "-font",SERR,"-pointsize","40","-fill",CREAM,"-annotate","+0+500",
     "a division of WANNATION HOLDINGS (PTY) LTD",
     "-font",SANS,"-pointsize","36","-fill",GOLD,"-annotate","+0+580","Reg No: 2026/463724/07",
     "-font",SANS,"-pointsize","28","-fill",CREAM,"-gravity","south","-annotate","+0+120",
     "© 2026 WANNATION HOLDINGS (PTY) LTD.  All rights reserved.",
     f"{OUT}/credits_legal.png"])
print("cards:",sorted(os.listdir(OUT)))
