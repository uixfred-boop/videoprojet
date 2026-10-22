import numpy as np, subprocess, sys
v=sys.argv[1]
raw=subprocess.run(["ffmpeg","-loglevel","error","-i",v,"-f","f32le","-ac","2","-ar","44100","-"],capture_output=True).stdout
a=np.frombuffer(raw,np.float32).reshape(-1,2); side=(a[:,0]-a[:,1])/2
hop=441; n=len(side)//hop; e=np.sqrt((side[:n*hop].reshape(n,hop)**2).mean(1)); db=20*np.log10(e+1e-9)
act=db>-60; ev=[];i=0
while i<n:
    if act[i]:
        j=i
        while j<n and (act[j:j+5].any()): j+=1
        seg=side[i*hop:j*hop]
        sp=np.abs(np.fft.rfft(seg*np.hanning(len(seg)))); f=np.fft.rfftfreq(len(seg),1/44100)
        cen=(sp*f).sum()/sp.sum(); pk=f[sp.argmax()]
        env=db[i:j]; ap=np.argmax(env)
        ev.append(f"{i/100:.2f}s dur={(j-i)/100:.2f}s peak={env.max():.0f}dBFS attack@{ap/100:.2f}s centroid={cen:.0f}Hz peakHz={pk:.0f}")
        i=j
    else: i+=1
print("\n".join(ev))
