import json,sys,numpy as np
from scipy.ndimage import median_filter
d=json.load(open(sys.argv[1]))
t=np.array([r['t'] for r in d]); s=np.array([r['s'] if r['s'] else np.nan for r in d])
ok=~np.isnan(s); si=np.interp(t,t[ok],s[ok]); z=median_filter(si,11); z=z/np.percentile(z,3)
print("zoom (median-filtered) every 1s:")
print(" ".join(f"{int(t[i])}:{z[i]:.2f}{'' if ok[i] else '?'}" for i in range(0,len(d),30)))
# events: change >2.5% within 6 frames = snap; within 6-60 frames ramp
ev=[];i=0
while i<len(z)-6:
    dz=z[i+5]-z[i]
    if abs(dz)>0.03:
        j=i+5
        while j<len(z)-1 and abs(z[j+1]-z[j])>0.002: j+=1
        ev.append(f"{t[i]:.2f}-{t[j]:.2f} {z[i]:.2f}->{z[j]:.2f} ({'SNAP' if j-i<=8 else 'RAMP'} {(j-i)/30:.2f}s)"); i=j+1
    else: i+=1
print("\n".join(ev))
