#!/usr/bin/env python3
"""JUDGEMENT TALES — original score + SFX, synthesized from scratch. No sampled/licensed material."""
import numpy as np
SR=48000
def t(n): return np.arange(int(n*SR))/SR
def env(x, a=0.01, d=0.1, s=0.7, r=0.2):
    n=len(x); A=int(a*SR); D=int(d*SR); R=int(r*SR); S=max(0,n-A-D-R)
    e=np.concatenate([np.linspace(0,1,A), np.linspace(1,s,D), np.full(S,s), np.linspace(s,0,R)])
    return x*e[:n] if len(e)>=n else x*np.pad(e,(0,n-len(e)))

def pluck(f, dur, damp=0.996, bright=0.5):
    """Karplus-Strong plucked string — the harp."""
    N=int(SR/f); buf=np.random.uniform(-1,1,N)
    buf=buf*bright + np.linspace(1,-1,N)*(1-bright)
    out=np.zeros(int(dur*SR))
    for i in range(len(out)):
        out[i]=buf[i%N]
        buf[i%N]=damp*0.5*(buf[i%N]+buf[(i+1)%N])
    return out

def ep(f, dur, detune=1.004):
    """Lounge electric-piano-ish tone: sine stack + tremolo."""
    x=t(dur)
    y=(np.sin(2*np.pi*f*x)+0.5*np.sin(2*np.pi*f*detune*x)
       +0.28*np.sin(2*np.pi*2*f*x)+0.12*np.sin(2*np.pi*3*f*x))
    y*= (1+0.10*np.sin(2*np.pi*5.2*x))           # tremolo
    return env(y, 0.008, 0.25, 0.45, max(0.08,dur*0.4))

def noise(dur): return np.random.uniform(-1,1,int(dur*SR))

def lp(x, cut):
    """one-pole lowpass"""
    a=np.exp(-2*np.pi*cut/SR); y=np.zeros_like(x); p=0.0
    for i in range(len(x)): p=(1-a)*x[i]+a*p; y[i]=p
    return y
def hp(x, cut): return x-lp(x,cut)

def warble(x, depth=0.0016, rate=0.7):
    """tape wow & flutter — the public-access signature"""
    n=len(x); idx=np.arange(n)
    off=depth*SR*np.sin(2*np.pi*rate*idx/SR)+depth*0.4*SR*np.sin(2*np.pi*rate*5.7*idx/SR)
    src=np.clip(idx+off,0,n-1)
    return np.interp(src, idx, x)

NOTE={'C3':130.81,'D3':146.83,'E3':164.81,'F3':174.61,'G3':196.00,'A3':220.00,'B3':246.94,
      'C4':261.63,'D4':293.66,'E4':329.63,'F4':349.23,'G4':392.00,'A4':440.00,'B4':493.88,
      'C5':523.25,'D5':587.33,'E5':659.25,'G5':783.99,'A5':880.00}

def muzak(dur, gain=1.0, bpm=84):
    """Endless, affable, faintly despairing hold music. ii-V-I-vi in C."""
    out=np.zeros(int(dur*SR)); beat=60/bpm; bar=beat*4
    chords=[['D4','F4','A4','C5'],['G3','B3','D4','F4'],['C4','E4','G4','B4'],['A3','C4','E4','G4']]
    bass =['D3','G3','C3','A3']
    i=0; pos=0.0
    while pos<dur:
        ch=chords[i%4]
        for k,nn in enumerate(ch):
            s=int((pos+k*beat*0.06)*SR); seg=ep(NOTE[nn], min(bar*0.95, dur-pos))*0.16
            if s<len(out): out[s:s+len(seg)]+=seg[:max(0,len(out)-s)]
        s=int(pos*SR); b=ep(NOTE[bass[i%4]]*0.5 if False else NOTE[bass[i%4]], min(bar*0.9,dur-pos))*0.20
        if s<len(out): out[s:s+len(b)]+=b[:max(0,len(out)-s)]
        for k in range(4):   # brush pulse
            s=int((pos+k*beat)*SR); h=lp(noise(0.06),6000)*np.linspace(1,0,int(0.06*SR))*0.035
            if s<len(out): out[s:s+len(h)]+=h[:max(0,len(out)-s)]
        pos+=bar; i+=1
    return warble(lp(out,5200))*gain

def harp_theme(dur):
    """Celestial harp run that curdles into hold music."""
    out=np.zeros(int(dur*SR))
    run=['C4','E4','G4','C5','E5','G5','A5','G5','E5','C5']
    for k,nn in enumerate(run):
        s=int(k*0.135*SR); y=pluck(NOTE[nn],1.9)*0.32*np.exp(-np.linspace(0,2.2,int(1.9*SR)))
        if s<len(out): out[s:s+len(y)]+=y[:max(0,len(out)-s)]
    for k,nn in enumerate(['C4','G4','C5','E5']):
        s=int((1.55+k*0.1)*SR); y=pluck(NOTE[nn],2.6)*0.30*np.exp(-np.linspace(0,1.6,int(2.6*SR)))
        if s<len(out): out[s:s+len(y)]+=y[:max(0,len(out)-s)]
    return out

def sfx(name, dur=1.0):
    if name=="static":   return hp(noise(dur),1800)*0.16*np.linspace(1,0.3,int(dur*SR))
    if name=="tick":
        o=np.zeros(int(dur*SR))
        for k in range(int(dur/0.5)):
            s=int(k*0.5*SR); c=lp(noise(0.02),4000)*np.linspace(1,0,int(0.02*SR))*0.5
            o[s:s+len(c)]+=c[:max(0,len(o)-s)]
        return o
    if name=="taxi":
        x=t(dur); rumble=lp(noise(dur),120)*0.45*(1+0.2*np.sin(2*np.pi*3.1*x))
        return rumble+lp(noise(dur),900)*0.05
    if name=="boop":
        x=t(0.26); y=np.sin(2*np.pi*880*x)*np.exp(-np.linspace(0,9,len(x)))*0.5
        return np.pad(y,(0,max(0,int(dur*SR)-len(y))))
    if name in ("sting","sting_end"):
        o=np.zeros(int(dur*SR))
        for k,nn in enumerate(['C5','G4','E4'] if name=="sting" else ['C4','E4','G4','C5']):
            s=int(k*0.09*SR); y=pluck(NOTE[nn],1.6)*0.34
            o[s:s+len(y)]+=y[:max(0,len(o)-s)]
        return o
    if name=="rip":
        y=hp(noise(0.42),2500)*np.linspace(1,0,int(0.42*SR))**0.5*0.42
        return np.pad(y,(0,max(0,int(dur*SR)-len(y))))
    if name in ("ting","shimmer"):
        x=t(1.5); y=(np.sin(2*np.pi*2100*x)+0.6*np.sin(2*np.pi*3180*x))*np.exp(-np.linspace(0,7,len(x)))*0.22
        return np.pad(y,(0,max(0,int(dur*SR)-len(y))))
    if name=="thud":
        y=lp(noise(0.35),180)*np.exp(-np.linspace(0,7,int(0.35*SR)))*0.75
        return np.pad(y,(0,max(0,int(dur*SR)-len(y))))
    if name=="thunder":
        y=lp(noise(2.6),320)*0.85
        y*=np.concatenate([np.linspace(0,1,600),np.exp(-np.linspace(0,3.4,len(y)-600))])
        return np.pad(y,(0,max(0,int(dur*SR)-len(y))))
    if name=="clap":
        y=hp(noise(0.16),1400)*np.exp(-np.linspace(0,14,int(0.16*SR)))*0.55
        return np.pad(y,(0,max(0,int(dur*SR)-len(y))))
    if name=="creak":
        x=t(1.4); f=np.linspace(260,140,len(x))
        y=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-np.linspace(0,2.4,len(x)))*0.20
        return np.pad(y,(0,max(0,int(dur*SR)-len(y))))
    if name=="shutter":
        x=t(0.9); y=hp(noise(0.9),900)*np.linspace(0.6,0,len(x))*0.5
        f=np.linspace(300,90,len(x)); y+=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-np.linspace(0,3,len(x)))*0.18
        return np.pad(y,(0,max(0,int(dur*SR)-len(y))))
    if name=="stone":
        y=lp(noise(0.5),700)*np.exp(-np.linspace(0,8,int(0.5*SR)))*0.5
        return np.pad(y,(0,max(0,int(dur*SR)-len(y))))
    if name=="heels":
        o=np.zeros(int(dur*SR))
        for k in range(int(dur/0.42)):
            s=int(k*0.42*SR); c=hp(noise(0.05),2600)*np.exp(-np.linspace(0,16,int(0.05*SR)))*0.40
            o[s:s+len(c)]+=c[:max(0,len(o)-s)]
        return o
    if name=="steps":
        o=np.zeros(int(dur*SR))
        for k in range(int(dur/0.55)):
            s=int(k*0.55*SR); c=lp(noise(0.08),900)*np.exp(-np.linspace(0,11,int(0.08*SR)))*0.30
            o[s:s+len(c)]+=c[:max(0,len(o)-s)]
        return o
    if name in ("flip_none","flip_047"):
        o=np.zeros(int(dur*SR))
        for k in range(3 if name=="flip_047" else 1):
            s=int((0.25+k*0.16)*SR); c=hp(noise(0.045),1200)*np.exp(-np.linspace(0,13,int(0.045*SR)))*0.42
            o[s:s+len(c)]+=c[:max(0,len(o)-s)]
        if name=="flip_047":
            x=t(0.8); b=np.sin(2*np.pi*1320*x)*np.exp(-np.linspace(0,6,len(x)))*0.18
            s=int(0.75*SR); o[s:s+len(b)]+=b[:max(0,len(o)-s)]
        return o
    if name=="psst":
        y=hp(noise(0.5),3500)*np.exp(-np.linspace(0,5,int(0.5*SR)))*0.28
        return np.pad(y,(0,max(0,int(dur*SR)-len(y))))
    if name=="shudder":
        x=t(1.0); y=lp(noise(1.0),200)*np.exp(-np.linspace(0,3,len(x)))*0.5
        return np.pad(y,(0,max(0,int(dur*SR)-len(y))))
    if name=="wilt":
        x=t(0.8); f=np.linspace(420,110,len(x))
        y=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-np.linspace(0,3.6,len(x)))*0.22
        return np.pad(y,(0,max(0,int(dur*SR)-len(y))))
    if name=="fanfare":
        o=np.zeros(int(dur*SR))
        for k,nn in enumerate(['C4','E4','G4','C5']):
            s=int(k*0.13*SR); y=ep(NOTE[nn],1.4)*0.30
            o[s:s+len(y)]+=y[:max(0,len(o)-s)]
        return o
    if name=="hum":
        x=t(dur); return (np.sin(2*np.pi*70*x)*0.16+lp(noise(dur),260)*0.10)*np.linspace(1,0.2,len(x))
    if name=="glide":
        x=t(1.2); f=np.linspace(700,1500,len(x))
        y=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-np.linspace(0,4,len(x)))*0.12
        return np.pad(y,(0,max(0,int(dur*SR)-len(y))))
    if name=="wifi":
        o=np.zeros(int(dur*SR))
        for k in range(3):
            s=int((0.2+k*0.26)*SR); x=t(0.2)
            y=np.sin(2*np.pi*(1500+k*350)*x)*np.exp(-np.linspace(0,9,len(x)))*0.17
            o[s:s+len(y)]+=y[:max(0,len(o)-s)]
        return o
    return np.zeros(int(dur*SR))
