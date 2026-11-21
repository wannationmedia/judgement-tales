#!/usr/bin/env python3
"""Sven: clean matte (drop chair, crowned figure, table) + a horned helmet that travels with him."""
import numpy as np, subprocess
from PIL import Image, ImageDraw, ImageFilter
im=Image.open("sven_cut.png").convert("RGBA"); a=np.array(im).astype(np.float32)
H,W=a.shape[:2]; rgb=a[...,:3]/255; al=a[...,3]
# 1) hard-clean the soft ghosts (palm/sky)
al=np.where(al>140,255,0).astype(np.float32)
# 2) key out the saturated blue chair
mx=rgb.max(-1); mn=rgb.min(-1); sat=(mx-mn)/(mx+1e-6)
blue=(rgb[...,2]>rgb[...,0]+0.10)&(rgb[...,2]>rgb[...,1]+0.02)&(sat>0.35)&(mx>0.25)
al[blue]=0
# 3) remove the crowned figure: everything right of a line hugging Sven's cape
yy,xx=np.mgrid[0:H,0:W]
edge=np.interp(yy,[0,190,270,330,470],[330,318,328,365,385])
al[(yy>138)&(yy<178)&(xx>104)&(xx<142)]=0
al[xx>edge]=0
# 4) drop the table and everything below the elbows' baseline
al[yy>428]=0
m=Image.fromarray(al.astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
a[...,3]=np.array(m)
Image.fromarray(a.astype(np.uint8)).crop((0,0,W,430)).save("sven_clean.png")
print("matte cleaned")
