import cv2, numpy as np, sys, json
path,reft,outp=sys.argv[1],float(sys.argv[2]),sys.argv[3]
cap=cv2.VideoCapture(path)
orb=cv2.ORB_create(1500); bf=cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
def prep(f):
    g=cv2.cvtColor(cv2.resize(f,(360,640)),cv2.COLOR_BGR2GRAY)
    m=np.full(g.shape,255,np.uint8); m[200:640,80:280]=0; m[:110]=0  # drop body + top text band
    return g,m
cap.set(cv2.CAP_PROP_POS_MSEC,reft*1000); ok,f=cap.read(); g,m=prep(f); rk,rd=orb.detectAndCompute(g,m)
cap.set(cv2.CAP_PROP_POS_FRAMES,0); out=[]; i=0
while True:
    ok,f=cap.read()
    if not ok: break
    g,m=prep(f); kp,des=orb.detectAndCompute(g,None)
    s=None;cx=cy=None;n=0
    if des is not None:
        mt=bf.match(rd,des)
        if len(mt)>15:
            p0=np.float32([rk[x.queryIdx].pt for x in mt]); p1=np.float32([kp[x.trainIdx].pt for x in mt])
            M,inl=cv2.estimateAffinePartial2D(p0,p1,ransacReprojThreshold=3)
            if M is not None and inl.sum()>20:
                s=float(np.hypot(M[0,0],M[1,0])); n=int(inl.sum())
                # zoom anchor: fixed point of transform x=sx+t -> x=t/(1-s)
                if abs(1-s)>0.02: cx=float(M[0,2]/(1-s)); cy=float(M[1,2]/(1-s))
    out.append({'t':i/30,'s':s,'n':n,'cx':cx,'cy':cy}); i+=1
json.dump(out,open(outp,'w'))
