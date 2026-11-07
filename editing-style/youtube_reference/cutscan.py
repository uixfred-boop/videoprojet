import cv2, numpy as np, sys, json
cap=cv2.VideoCapture(sys.argv[1]); fps=cap.get(cv2.CAP_PROP_FPS); step=2  # analyse at 30 fps
prev=None; i=0; rows=[]
while True:
    ok=cap.grab()
    if not ok: break
    if i%step==0:
        ok,f=cap.retrieve(); g=cv2.cvtColor(cv2.resize(f,(160,90)),cv2.COLOR_BGR2GRAY).astype(np.float32)
        hsv=cv2.cvtColor(cv2.resize(f,(160,90)),cv2.COLOR_BGR2HSV)
        # "talking head" signature: mean of right-edge cyan LED column region
        cyan=float(((hsv[...,0]>80)&(hsv[...,0]<105)&(hsv[...,1]>120)&(hsv[...,2]>120))[:,140:].mean())
        d=float(np.abs(g-prev).mean()) if prev is not None else 0
        rows.append((round(i/fps,3),round(d,2),round(cyan,3),round(float(g.mean()),1)))
        prev=g
    i+=1
json.dump(rows,open(sys.argv[2],"w"))
print(len(rows))
