import cv2,numpy as np,sys
cap=cv2.VideoCapture(sys.argv[1]); end=float(sys.argv[2]) if len(sys.argv)>2 else 1e9
D=[];prev=None;i=0
while True:
    ok,f=cap.read()
    if not ok or i/30>end: break
    g=cv2.cvtColor(cv2.resize(f,(90,160)),cv2.COLOR_BGR2GRAY).astype(np.int16)
    r=g[40:110,20:70]  # person/face region below title band
    hist=cv2.calcHist([g.astype(np.uint8)[45:]],[0],None,[32],[0,256]).ravel()
    if prev is not None: D.append(np.abs(r-prev[0]).mean())
    else: D.append(0)
    prev=(r,hist); i+=1
D=np.array(D); cuts=[]
for k in range(2,len(D)-2):
    loc=np.concatenate([D[max(0,k-12):k-1],D[k+2:k+13]]); med=np.median(loc)
    if D[k]>max(2.0*med,med+3) and D[k]==D[k-2:k+3].max(): cuts.append(k/30)
segs=np.diff([0]+cuts+[len(D)/30])
print(len(cuts),"cuts; shots/min %.1f; mean %.2fs median %.2fs p10 %.2fs p90 %.2fs"%(len(cuts)/(len(D)/30)*60,segs.mean(),np.median(segs),np.percentile(segs,10),np.percentile(segs,90)))
print(" ".join(f"{c:.2f}" for c in cuts))
