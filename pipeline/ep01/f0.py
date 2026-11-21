import sys, wave, numpy as np
def f0(path):
    w=wave.open(path,'rb'); sr=w.getframerate()
    a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)
    if w.getnchannels()==2: a=a.reshape(-1,2).mean(1)
    a/= (np.abs(a).max()+1e-9)
    # frame-wise autocorrelation pitch
    fl=int(0.04*sr); hop=int(0.02*sr); vals=[]
    lo,hi=int(sr/300),int(sr/70)   # 70-300 Hz
    for i in range(0,len(a)-fl,hop):
        fr=a[i:i+fl]
        if np.sqrt((fr**2).mean())<0.05: continue
        fr=fr-fr.mean()
        ac=np.correlate(fr,fr,'full')[fl-1:]
        if ac[0]<=0: continue
        seg=ac[lo:hi]
        if len(seg)==0: continue
        k=int(np.argmax(seg))+lo
        if ac[k]/ac[0] > 0.3: vals.append(sr/k)
    return (float(np.median(vals)) if vals else 0.0), len(vals)
for p in sys.argv[1:]:
    m,n=f0(p)
    print(f"{p.split('/')[-1][:-4]:<14} medianF0={m:6.1f} Hz  voiced_frames={n}")
