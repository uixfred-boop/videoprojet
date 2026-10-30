"""Render each EDL clip: trim, white-balance match to take A, LUT grade, 4K upscale + sharpen, zoom keyframes."""
import json, subprocess, sys
import numpy as np, cv2
sys.path.insert(0, sys.argv[1])
from edl import ZOOMS, ANCHOR, SRC, FPS

work = sys.argv[2]
W = json.load(open(f"{work}/words.json"))
OW, OH = 2160, 3840
LUT = sys.argv[3]
WARM = np.array([1.015, 1.0, 0.975])  # tiny warm bias on top of take A's balance


def wall_rgb(path, t):
    cap = cv2.VideoCapture(path); cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, f = cap.read(); h, w = f.shape[:2]
    r = f[int(h * .03):int(h * .12), int(w * .02):int(w * .18)].reshape(-1, 3).mean(0)[::-1]  # BGR->RGB
    return r


REF = wall_rgb(f"{work}/{SRC['A']}", 5.0); TARGET = REF / REF.mean() * WARM  # take A as shot = the look
manifest = []
for cid, c in W.items():
    src, s, e = c["src"], c["start"], c["end"]; dur = round((e - s) * FPS) / FPS
    path = f"{work}/{SRC[src]}"
    rgb = wall_rgb(path, s + dur / 2)
    gains = TARGET / (rgb / rgb.mean()); gains /= gains.mean()
    ax, ay = ANCHOR[src]
    z = "1"
    if cid in ZOOMS:
        kind, word, sc = ZOOMS[cid]
        if kind == "snap":
            t0 = next(t for w, t in c["words"] if w.lower().strip(",.") == word)
            t0 = max(0.0, t0 - 0.03)
            # ease-out over 4 frames (0.13s)
            z = f"1+{sc-1}*(1-pow(1-clip((t-{t0:.3f})/0.13,0,1),3))"
        else:
            z = f"1+{sc-1}*clip(t/{dur:.3f},0,1)"
        c["zoom"] = {"kind": kind, "t": (t0 if kind == "snap" else 0.0)}
    # 720p take B gets a light denoise before the 3x upscale so noise isn't magnified
    pre = "hqdn3d=1.5:1.5:3:3," if src == "B" else "hqdn3d=1:1:2:2,"
    sharp = "unsharp=7:7:0.9:5:5:0.0" if src == "B" else "unsharp=5:5:0.6:5:5:0.0"
    vf = (f"{pre}format=gbrpf32le,"
          f"colorchannelmixer=rr={gains[0]:.3f}:gg={gains[1]:.3f}:bb={gains[2]:.3f},"
          f"lut3d={LUT}:interp=tetrahedral,format=yuv444p,"
          f"scale={OW}:{OH}:flags=lanczos+accurate_rnd+full_chroma_int,setsar=1,"
          f"scale=w='trunc({OW}*({z})/2)*2':h='trunc({OH}*({z})/2)*2':eval=frame:flags=lanczos,"
          f"crop={OW}:{OH}:'(iw-{OW})*{ax}':'(ih-{OH})*{ay}',"
          f"{sharp},fps={FPS},format=yuv420p")
    af = f"afade=t=in:d=0.012,afade=t=out:st={dur-0.015:.3f}:d=0.015"
    out = f"{work}/clips4k/{cid}.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{s:.3f}", "-i", path, "-t", f"{dur:.3f}",
                    "-vf", vf, "-af", af, "-r", str(FPS), "-c:v", "libx264", "-preset", "fast", "-crf", "12",
                    "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1", out.replace(".mp4", ".mov")], check=True)
    c["dur"] = dur
    manifest.append(cid)
    print(cid, src, f"{s:.2f}+{dur:.2f}", "gains", gains.round(3), c.get("zoom", ""))
json.dump(W, open(f"{work}/words.json", "w"), indent=1)
with open(f"{work}/clips4k/list.txt", "w") as f:
    for cid in manifest: f.write(f"file '{cid}.mov'\n")
