#!/usr/bin/env python3
"""Stage Sven inside Heavenly Reception: a close-up over the blurred queue, and a two-shot with Lwazi."""
from PIL import Image, ImageFilter, ImageEnhance
W,H=2880,1620
P1=Image.open("/home/user/judgement-tales/images/1.jpg").convert("RGB")
sv=Image.open("sven_helmet.png").convert("RGBA")
OUT="/home/user/judgement-tales/.work/plates"
def bg(box, blur, dim=1.0):
    b=P1.crop(box).resize((W,H),Image.LANCZOS)
    if blur: b=b.filter(ImageFilter.GaussianBlur(blur))
    return ImageEnhance.Brightness(b).enhance(dim)
def place(base, scale, x, y):
    s=sv.resize((round(sv.width*scale),round(sv.height*scale)),Image.LANCZOS)
    # soft contact shadow so he sits in the room rather than on it
    sh=Image.new("RGBA",s.size,(0,0,0,0)); sh.putalpha(s.getchannel("A").point(lambda v:int(v*0.35)))
    sh=sh.filter(ImageFilter.GaussianBlur(28))
    base=base.convert("RGBA"); base.alpha_composite(sh,(x-30,y+24)); base.alpha_composite(s,(x,y))
    return base.convert("RGB")
# close-up: Sven over the blurred queue (gold rope, haloes)
CUX,CUY,CUS=-40,1620-round(430*3.49),3.49
cu=place(bg((980,100,1536,413),16,0.92), CUS, CUX, CUY)
cu.save(f"{OUT}/sven_cu.png")
# same close-up without the helmet: the base for the theft-attempt shot
helm=sv; sv=Image.open("sven_clean.png").convert("RGBA")
place(bg((980,100,1536,413),16,0.92), CUS, CUX, CUY).save(f"{OUT}/helmet_lift.png")
sv=helm
# the helmet alone, at render scale (plate 2880 -> output 1920), for the lift overlay
k=1920/2880
Image.open("helmet.png").resize((round(440*CUS*k),round(430*CUS*k)),Image.LANCZOS).save("/home/user/judgement-tales/.work/props/helmet_layer.png")
open("/home/user/judgement-tales/.work/props/helmet_layer.pos","w").write(f"{round(CUX*k)} {round(CUY*k)}")
# insert: the helmet and horns, no eyes, for "Sven's helmet" / "the horned hat"
Image.open(f"{OUT}/sven_cu.png").crop((140,0,1340,675)).resize((W,H),Image.LANCZOS).save(f"{OUT}/helmet_ins.png")
# two-shot: Lwazi mid-ground, Sven foreground right, the queue behind
two=place(bg((560,100,1380,561),3,0.97), 3.24, 1574, 1620-round(430*3.24))
two.save(f"{OUT}/sven_mid.png")
for n in ("sven_cu","sven_mid","helmet_ins","helmet_lift"):
    Image.open(f"{OUT}/{n}.png").resize((640,360)).save(f"/tmp/{n}_prev.png")
print("staged")
