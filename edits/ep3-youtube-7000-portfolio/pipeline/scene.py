"""Render an animated graphic scene at 4K with ffmpeg overlays.
Scene JSON: {"dur": s, "base": {"type": "bg"|"video"|"color", "path":..., "ss":..}, "items": [
   {"png": path, "x": pt, "y": pt, "pad": px, "t": in_s, "out": out_s|null, "anim": "up"|"left"|"right"|"fade"|"pop", "video": {...}} ]}
Positions are in 1920x1080 points (top-left of the visible element, padding/glow excluded).
A "video" item plays a clip (screen recording) scaled into a box: {"src","ss","w","h"} placed under its frame png."""
import json, subprocess, sys
W, H, K, FPS = 3840, 2160, 2, 30
TO709 = "scale=out_color_matrix=bt709:out_range=tv"   # RGB graphics -> YUV with the matrix the file is tagged with
spec = json.load(open(sys.argv[1])); out = sys.argv[2]
dur = spec["dur"]
inputs, fc = [], []
base = spec["base"]
if base["type"] == "bg":
    inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.3f}", "-i", base["path"]]
    fc.append(f"[0:v]{TO709},format=yuv444p,setpts=PTS-STARTPTS[b0]")
elif base["type"] == "video":
    inputs += ["-ss", f"{base['ss']:.3f}", "-t", f"{dur:.3f}", "-i", base["path"]]
    fc.append(f"[0:v]setpts=PTS-STARTPTS,fps={FPS},scale={W}:{H},format=yuv444p[b0]")
cur, n = "b0", 1
EASE = "(1-pow(1-min(max((t-{t0})/{d},0),1),3))"
for i, it in enumerate(spec["items"]):
    t0 = it["t"]; t1 = it.get("out") or dur; d = it.get("d", 0.4)
    e = EASE.format(t0=t0, d=d)
    x, y = it["x"] * K - it.get("pad", 0), it["y"] * K - it.get("pad", 0)
    dx, dy = {"up": (0, 40), "left": (-60, 0), "right": (60, 0)}.get(it.get("anim", "up"), (0, 0))
    xe = f"{x}+{dx * K}*(1-{e})" if dx else f"{x}"
    ye = f"{y}+{dy * K}*(1-{e})" if dy else f"{y}"
    if "video" in it:                       # screen recording inside a frame: scale + slide like the frame
        v = it["video"]
        inputs += ["-ss", f"{v['ss']:.3f}", "-t", f"{t1 - t0 + 0.1:.3f}", "-i", v["src"]]
        vx, vy = v["x"] * K, v["y"] * K
        fc.append(f"[{n}:v]setpts=PTS-STARTPTS+{t0}/TB,fps={FPS},scale={v['w'] * K}:{v['h'] * K}:flags=lanczos,format=yuva444p,"
                  f"fade=t=in:st={t0}:d={d}:alpha=1[v{i}]")
        fc.append(f"[{cur}][v{i}]overlay=x='{vx}+{dx * K}*(1-{e})':y='{vy}+{dy * K}*(1-{e})':eval=frame:"
                  f"enable='between(t,{t0},{t1})':eof_action=pass[c{i}v]")
        cur = f"c{i}v"; n += 1
    inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.3f}", "-i", it["png"]]
    fade = f"fade=t=in:st={t0}:d={d * 0.8:.3f}:alpha=1"
    if it.get("out"):
        fade += f",fade=t=out:st={t1 - 0.25:.3f}:d=0.25:alpha=1"
    fc.append(f"[{n}:v]{TO709},format=yuva444p,{fade}[p{i}]")
    fc.append(f"[{cur}][p{i}]overlay=x='{xe}':y='{ye}':eval=frame:enable='between(t,{t0},{t1})'[c{i}]")
    cur = f"c{i}"; n += 1
fc.append(f"[{cur}]fps={FPS},format=yuv420p[v]")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[v]",
                "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-x264-params", "keyint=30",
                "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-an", out], check=True)
print("scene", out, f"{dur:.2f}s", len(spec["items"]), "items")
