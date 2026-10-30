"""Render each EDL clip: trim, 1080x1920, per-clip white-balance match + warm grade, zoom keyframes."""
import json, subprocess, sys
import numpy as np, cv2
sys.path.insert(0, sys.argv[1])
from edl import ZOOMS, ANCHOR, SRC, FPS

work = sys.argv[2]
W = json.load(open(f"{work}/words.json"))
TARGET = np.array([1.08, 1.0, 0.92])  # warm neutral wall (R,G,B relative to G)


def wall_rgb(path, t):
    cap = cv2.VideoCapture(path); cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, f = cap.read(); h, w = f.shape[:2]
    r = f[int(h * .03):int(h * .12), int(w * .02):int(w * .18)].reshape(-1, 3).mean(0)[::-1]  # BGR->RGB
    return r


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
    vf = (f"scale=1080:1920:flags=lanczos,setsar=1,"
          f"colorchannelmixer=rr={gains[0]:.3f}:gg={gains[1]:.3f}:bb={gains[2]:.3f},"
          f"scale=w='trunc(1080*({z})/2)*2':h='trunc(1920*({z})/2)*2':eval=frame:flags=bicubic,"
          f"crop=1080:1920:'(iw-1080)*{ax}':'(ih-1920)*{ay}',"
          f"eq=contrast=0.95:brightness=0.03:saturation=0.95:gamma=1.05,"
          f"curves=all='0/0.035 0.5/0.52 1/0.97',"
          f"fps={FPS},format=yuv420p")
    af = f"afade=t=in:d=0.012,afade=t=out:st={dur-0.015:.3f}:d=0.015"
    out = f"{work}/clips/{cid}.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{s:.3f}", "-i", path, "-t", f"{dur:.3f}",
                    "-vf", vf, "-af", af, "-r", str(FPS), "-c:v", "libx264", "-preset", "fast", "-crf", "16",
                    "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1", out.replace(".mp4", ".mov")], check=True)
    c["dur"] = dur
    manifest.append(cid)
    print(cid, src, f"{s:.2f}+{dur:.2f}", "gains", gains.round(3), c.get("zoom", ""))
json.dump(W, open(f"{work}/words.json", "w"), indent=1)
with open(f"{work}/clips/list.txt", "w") as f:
    for cid in manifest: f.write(f"file '{cid}.mov'\n")
