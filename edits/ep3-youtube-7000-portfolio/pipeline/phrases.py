import json, numpy as np
from scipy.io import wavfile
from faster_whisper import WhisperModel
R=[tuple(map(float,l.split()[:2])) for l in open("/tmp/claude-0/-home-user-videoprojet/6386d7a0-9dfd-599c-825b-733ce7c63b86/scratchpad/ep3/vad_regions.txt") if l.strip()]
M=[]
for a,b in R:
    if M and a-M[-1][1]<0.22: M[-1][1]=b
    else: M.append([a,b])
M=[m for m in M if m[1]-m[0]>0.12]
sr,x=wavfile.read("/tmp/claude-0/-home-user-videoprojet/6386d7a0-9dfd-599c-825b-733ce7c63b86/scratchpad/ep3/raw.wav"); x=x.astype(np.float32)/32768
m=WhisperModel("medium.en",device="cpu",compute_type="int8")
out=[]
for i,(a,b) in enumerate(M):
    seg=x[int(max(0,a-0.08)*sr):int((b+0.12)*sr)]
    seg=np.concatenate([np.zeros(sr//4,np.float32),seg,np.zeros(sr//4,np.float32)])
    t=" ".join(s.text.strip() for s in m.transcribe(seg,beam_size=5,language="en",condition_on_previous_text=False)[0])
    out.append({"i":i,"a":round(a,2),"b":round(b,2),"text":t})
    print(f"{i:3d} {a:7.2f}-{b:7.2f} ({b-a:4.1f}s) {t}",flush=True)
json.dump(out,open("/tmp/claude-0/-home-user-videoprojet/6386d7a0-9dfd-599c-825b-733ce7c63b86/scratchpad/ep3/phrases.json","w"),indent=1)
