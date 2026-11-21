# JUDGEMENT TALES — Ep1 shot/framing library.
# Each framing = a 16:9 window onto an approved 1536x864 scene plate.
# crop = (x, y, w, h) in plate pixels. move = default camera move.
P = {
 "P1": "images/1.jpg",  # Heavenly Reception  (St Peter, Lwazi, Candice, queue, gates)
 "P2": "images/2.jpg",  # Orientation Day
 "P3": "images/3.jpg",  # Complaints Department (Brenda, Moses, tablets)
 "P4": "images/4.jpg",  # Downstairs Neighbours (Sultan, attendants, elevator, baklava)
 "P5": "images/5.jpg",  # Boardroom / the numbers
 "P6": "images/6.jpg",  # Boardroom of the accused (Sven stand-in, Moses at door)
}

SHOTS = {
 # ---- Heavenly Reception (P1) -------------------------------------------
 "recep_wide":  dict(p="P1", crop=(0,0,1536,864),      move="push_slow"),
 "recep_wide2": dict(p="P1", crop=(0,0,1536,864),      move="pull_slow"),
 "peter_cu":    dict(p="P1", crop=(160,150,460,259),   move="push_micro"),
 "peter_mid":   dict(p="P1", crop=(40,60,800,450),     move="drift_r"),
 "stamp_ins":   dict(p="P1", crop=(160,470,400,225),   move="push_micro"),
 "desk_papers": dict(p="P1", crop=(0,520,560,315),     move="drift_l"),
 "lwazi_cu":    dict(p="P1", crop=(645,175,370,208),   move="push_micro"),
 "lwazi_mid":   dict(p="P1", crop=(590,120,560,315),   move="drift_l"),
 "lwazi_wide":  dict(p="P1", crop=(520,60,760,428),    move="push_slow"),
 "ticket_ins":  dict(p="P1", crop=(545,410,330,186),   move="push_micro"),
 "pass_gold":   dict(p="P1", crop=(545,410,330,186),   move="push_micro"),
 "candice_cu":  dict(p="P1", crop=(915,195,340,191),   move="push_micro"),
 "queue_grp":   dict(p="P1", crop=(960,120,576,324),   move="drift_r"),
 "queue_deep":  dict(p="P1", crop=(1100,150,436,245),  move="push_slow"),
 "gates":       dict(p="P1", crop=(470,0,480,270),     move="push_slow"),
 "sign_recep":  dict(p="P1", crop=(0,0,370,208),       move="drift_r"),
 "sign_good":   dict(p="P1", crop=(1130,0,406,228),    move="push_micro"),
 "two_pl":      dict(p="P1", crop=(170,90,880,495),    move="push_slow"),
 "two_lc":      dict(p="P1", crop=(620,130,700,394),   move="drift_r"),
 # ---- Complaints Department (P3) ----------------------------------------
 "complaints_wide": dict(p="P3", crop=(0,0,1536,864),  move="push_slow"),
 "sign_complaints": dict(p="P3", crop=(40,0,500,281),  move="drift_r"),
 "brenda_cu":   dict(p="P3", crop=(310,280,400,225),   move="push_micro"),
 "brenda_mid":  dict(p="P3", crop=(140,200,680,383),   move="push_slow"),   # stops short of Moses' tablet
 "hr_mug":      dict(p="P3", crop=(150,610,340,191),   move="drift_r"),
 "moses_cu":    dict(p="P3", crop=(900,50,420,236),    move="push_micro"),
 "moses_mid":   dict(p="P3", crop=(800,30,620,349),    move="pull_slow"),
 "tablet1":     dict(p="P3", crop=(820,280,340,191),   move="push_micro"),
 "tablet2":     dict(p="P3", crop=(1180,290,330,186),  move="push_micro"),
 # ---- Downstairs Neighbours (P4) ----------------------------------------
 "downstairs_wide": dict(p="P4", crop=(0,0,1536,864),  move="push_slow"),
 "sultan_cu":   dict(p="P4", crop=(455,140,400,225),   move="push_micro"),
 "sultan_mid":  dict(p="P4", crop=(370,60,680,383),    move="push_slow"),
 "attendants":  dict(p="P4", crop=(0,180,470,264),     move="drift_r"),
 "baklava":     dict(p="P4", crop=(1030,639,400,225),  move="push_micro"),
 "elevator":    dict(p="P4", crop=(760,30,480,270),    move="push_slow"),
 "alcove":      dict(p="P1", crop=(0,470,520,293),      move="drift_l"),
 # ---- Boardroom of the accused (P6) -------------------------------------
 # Sven is cut out of plate 6, given his horned helmet, and staged in the reception queue
 # (.work/cutout/stage_sven.py). These four are pre-built plates, not crops.
 "sven_cu":     dict(p="PRE", crop=None, scene="P1", move="push_micro"),
 "helmet_ins":  dict(p="PRE", crop=None, scene="P1", move="push_micro"),
 "helmet_lift": dict(p="PRE", crop=None, scene="P1", move="static"),
 "sven_mid":    dict(p="PRE", crop=None, scene="P1", move="push_slow"),
 "accused_wide":dict(p="P6", crop=(0,0,1536,864),      move="push_slow"),
 "moses_door":  dict(p="P6", crop=(1180,40,356,200),   move="push_micro"),
}

def norm(c):
    """Force exact 16:9 inside plate bounds."""
    x,y,w,h = c
    h2 = round(w*9/16)
    if h2 != h:
        y = max(0, y - (h2-h)//2); h = h2
    if y+h > 864: y = 864-h
    if x+w > 1536: x = 1536-w
    return (max(0,x), max(0,y), w, h)

for k,v in SHOTS.items():
    if v["crop"]: v["crop"] = norm(v["crop"])
    v.setdefault("scene", v["p"])

# Whose face can be read in each framing. Drives the off-screen speaker labels in the default
# caption track and the voice-to-face check. With no lip-sync anywhere, the face on screen is
# the viewer's only cue for who is talking — so any line heard over a face that is not the
# speaker's gets a name in the captions, and the cut list is checked for it.
FACES={
 'lwazi_cu':{'LWAZI'},'lwazi_mid':{'LWAZI','CANDICE'},'lwazi_wide':{'LWAZI','CANDICE'},
 'peter_cu':{'PETER'},'peter_mid':{'PETER','LWAZI'},'two_pl':{'PETER','LWAZI'},'two_lc':{'LWAZI','CANDICE'},
 'candice_cu':{'CANDICE'},'queue_grp':{'CANDICE'},
 'recep_wide':{'PETER','LWAZI','CANDICE'},'recep_wide2':{'PETER','LWAZI','CANDICE'},
 'sven_cu':{'SVEN'},'sven_mid':{'LWAZI','SVEN'},'helmet_lift':{'SVEN'},
 'brenda_cu':{'BRENDA'},'brenda_mid':{'BRENDA'},'moses_cu':{'MOSES'},'moses_mid':{'MOSES'},
 'complaints_wide':{'BRENDA','MOSES'},
 'sultan_cu':{'SULTAN'},'sultan_mid':{'SULTAN'},'downstairs_wide':{'SULTAN','CANDICE'},'attendants':{'SULTAN'},
}
