"""Render shots from shots.json. usage: render_shots.py <work> gfx|face|all [index ...]"""
import json, os, subprocess, sys
E, mode = sys.argv[1], sys.argv[2]; only = set(int(x) for x in sys.argv[3:])
FPS = 30
SH = json.load(open(f"{E}/shots.json"))["shots"]
clips = json.load(open(f"{E}/edl.json"))["clips"]
t = 0.0
for c in clips:
    c["d"] = c.get("silent") or round((c["b"] - c["a"]) * FPS) / FPS; c["t"] = t; t += c["d"]
os.makedirs(f"{E}/shots", exist_ok=True)

def setup_of(a):
    return "A" if a < 125 else ("B" if a < 380 else "C")

for i, s in enumerate(SH):
    if only and i not in only: continue
    out = f"{E}/shots/s{i:03d}.mp4"
    if os.path.exists(out): continue
    dur = round((s["t1"] - s["t0"]) * FPS) / FPS
    if s["kind"] == "gfx" and mode in ("gfx", "all"):
        spec = {"dur": dur, "base": {"type": "bg", "path": f"{E}/g/bg.png"}, "items": s["items"]}
        json.dump(spec, open(f"{E}/shots/s{i:03d}.json", "w"))
        subprocess.run(["python3", "-I", f"{E}/scene.py", f"{E}/shots/s{i:03d}.json", out], check=True)
    elif s["kind"] == "face" and mode in ("face", "all"):
        pieces = []
        for c in clips:
            if c.get("silent"): continue
            a0, b0 = max(s["t0"], c["t"]), min(s["t1"], c["t"] + c["d"])
            if b0 - a0 < 1 / FPS / 2: continue
            src_a = c["a"] + (a0 - c["t"]); src_b = src_a + (b0 - a0)
            p = f"{E}/shots/s{i:03d}_p{len(pieces)}.mov"
            args = ["python3", "-I", f"{E}/thclip.py", E, f"{E}/raw.mp4", f"{src_a:.4f}", f"{src_b:.4f}", setup_of(c["a"]),
                    str(s["zoom"]), str(s["push"]), p]
            if s.get("shift") is not None: args.append(str(s["shift"]))
            subprocess.run(args, check=True); pieces.append(p)
        lst = f"{E}/shots/s{i:03d}_list.txt"; open(lst, "w").write("".join(f"file '{p}'\n" for p in pieces))
        base = f"{E}/shots/s{i:03d}_base.mov"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-an", "-c", "copy", base], check=True)
        if s["items"]:
            spec = {"dur": dur, "base": {"type": "video", "path": base, "ss": 0.0}, "items": s["items"]}
            json.dump(spec, open(f"{E}/shots/s{i:03d}.json", "w"))
            subprocess.run(["python3", "-I", f"{E}/scene.py", f"{E}/shots/s{i:03d}.json", out], check=True)
        else:
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", base, "-c", "copy", out], check=True)
        for p in pieces: os.remove(p)
        os.remove(base)
    else:
        continue
    print(i, s["kind"], f"{s['t0']:.2f}-{s['t1']:.2f}", flush=True)
