#!/usr/bin/env python3
"""Animated practical props: the NOW SERVING board, the lunch sign, the golden pass."""
import os, subprocess
W="/home/user/judgement-tales/.work"; OUT=f"{W}/props"; os.makedirs(OUT,exist_ok=True)
NAVY="#16294a"; GOLD="#d9b24c"; CREAM="#f3ead6"; DARK="#0b1322"
SER="Liberation-Serif-Bold"; SANS="DejaVu-Sans-Bold"

def board(num, fname):
    subprocess.run(["convert","-size","560x300","xc:none",
      "-fill",NAVY,"-draw","roundrectangle 0,0 559,299 18,18",
      "-fill","none","-stroke",GOLD,"-strokewidth","6","-draw","roundrectangle 8,8 551,291 14,14",
      "-stroke","none","-font",SANS,"-pointsize","40","-fill",GOLD,
      "-gravity","north","-annotate","+0+30","NOW SERVING",
      "-fill",DARK,"-draw","roundrectangle 110,100 450,265 10,10",
      "-font",SER,"-pointsize","150","-fill",CREAM,"-gravity","north","-annotate","+0+108",num,
      # split-flap hinge line
      "-fill","#000000AA","-draw","rectangle 110,181 450,187",
      f"{OUT}/{fname}"],check=True)
board("046","board_046.png"); board("047","board_047.png")
# mid-flap frame (blurred, for the flip)
subprocess.run(["convert",f"{OUT}/board_047.png","-blur","0x9","-modulate","78",
                f"{OUT}/board_flip.png"],check=True)

# ---- GONE TO LUNCH shutter sign -----------------------------------------
subprocess.run(["convert","-size","900x320","xc:none",
  "-fill","#7d2b22","-draw","roundrectangle 0,0 899,319 14,14",
  "-fill","none","-stroke",CREAM,"-strokewidth","6","-draw","roundrectangle 14,14 885,305 10,10",
  "-stroke","none","-font",SER,"-pointsize","78","-fill",CREAM,
  "-gravity","north","-annotate","+0+56","GONE TO LUNCH",
  "-font",SER,"-pointsize","52","-fill","#f0d070","-annotate","+0+168","BACK IN ETERNITY",
  f"{OUT}/lunch_sign.png"],check=True)

# ---- the golden Fast-Track Pass (re-grade of the ticket insert) ----------
subprocess.run(["convert",f"{W}/plates/ticket_ins.png",
  "-modulate","108,138,96","-fill","#d9a62c","-colorize","26",
  "(","+clone","-fill","black","-colorize","100","-fill","white",
    "-draw","ellipse 1180,900 620,420 0,360","-blur","0x180",")",
  "-compose","screen","-composite","-modulate","96,120,100",
  f"{W}/plates/pass_gold.png"],check=True)
print("props:",sorted(os.listdir(OUT)))
