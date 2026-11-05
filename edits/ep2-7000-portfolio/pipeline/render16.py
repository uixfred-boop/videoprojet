"""16:9 clip renderer: trim the composited 4K take, LUT grade, zoom keyframes, light sharpening.
Audio comes from the original camera file (the composite is video only)."""
import json, subprocess, sys
sys.path.insert(0, sys.argv[1])
from edl import ZOOMS, ANCHOR, FPS

work, lut, comp, raw = sys.argv[2:6]
OW, OH = 3840, 2160
W = json.load(open(f"{work}/words.json"))
out_dir = f"{work}/clips"
subprocess.run(["mkdir", "-p", out_dir], check=True)
names = []
for cid, c in W.items():
    s, e = c["start"], c["end"]; dur = round((e - s) * FPS) / FPS
    ax, ay = ANCHOR[c["src"]]
    z = "1"
    if cid in ZOOMS:
        kind, word, sc = ZOOMS[cid]
        if kind == "snap":
            t0 = max(0.0, next(t for w, t in c["words"] if w.lower().strip(",.:\"") == word) - 0.03)
            z = f"1+{sc-1}*(1-pow(1-clip((t-{t0:.3f})/0.13,0,1),3))"
        else:
            t0 = 0.0; z = f"1+{sc-1}*clip(t/{dur:.3f},0,1)"
        c["zoom"] = {"kind": kind, "t": t0}
    vf = (f"format=gbrpf32le,lut3d={lut}:interp=tetrahedral,format=yuv444p,"
          f"scale=w='trunc({OW}*({z})/2)*2':h='trunc({OH}*({z})/2)*2':eval=frame:flags=lanczos,"
          f"crop={OW}:{OH}:'(iw-{OW})*{ax}':'(ih-{OH})*{ay}',"
          f"unsharp=5:5:0.35:5:5:0.0,fps={FPS},format=yuv420p")
    af = f"afade=t=in:d=0.012,afade=t=out:st={dur-0.015:.3f}:d=0.015"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{s:.3f}", "-i", comp, "-ss", f"{s:.3f}", "-i", raw,
                    "-t", f"{dur:.3f}", "-map", "0:v", "-map", "1:a", "-vf", vf, "-af", af, "-r", str(FPS),
                    "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1",
                    f"{out_dir}/{cid}.mov"], check=True)
    c["dur"] = dur; names.append(cid)
    print(cid, f"{s:.2f}+{dur:.2f}", c.get("zoom", ""))
json.dump(W, open(f"{work}/words.json", "w"), indent=1)
open(f"{out_dir}/list.txt", "w").write("".join(f"file '{n}.mov'\n" for n in names))
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{out_dir}/list.txt",
                "-c", "copy", f"{work}/cut.mov"], check=True)
