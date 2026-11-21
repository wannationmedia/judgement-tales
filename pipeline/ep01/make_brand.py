#!/usr/bin/env python3
"""WANNATION logo mark (transparent) for the spinning watermark."""
import subprocess
NAVY="#16294a"; GOLD="#d9b24c"; BRIGHT="#f0d070"
S=512; c=S//2
out="/home/user/judgement-tales/.work/logo.png"
cmd=["convert","-size",f"{S}x{S}","xc:none",
 "-fill",NAVY,"-draw",f"circle {c},{c} {c},{int(S*0.07)}",
 "-fill","none","-stroke",GOLD,"-strokewidth","14","-draw",f"circle {c},{c} {c},{int(S*0.10)}",
 "-stroke",BRIGHT,"-strokewidth","5","-draw",f"circle {c},{c} {c},{int(S*0.155)}",
 "-stroke","none",
 # halo over the monogram
 "-fill","none","-stroke",BRIGHT,"-strokewidth","9",
 "-draw",f"ellipse {c},{int(S*0.315)} {int(S*0.20)},{int(S*0.052)} 0,360","-stroke","none",
 "-font","Liberation-Serif-Bold","-pointsize","150","-fill",BRIGHT,
 "-gravity","center","-annotate","+0+30","WN",
 "-font","Liberation-Serif-Bold","-pointsize","34","-fill",GOLD,
 "-gravity","center","-annotate","+0+130","WANNATION",
 out]
subprocess.run(cmd,check=True)
subprocess.run(["convert",out,"-resize","200x","/tmp/logo_check.png"],check=True)
print("wrote",out)
