"""Turns the screencast frames + timestamps into a constant-frame-rate 1080p MP4.
Usage: python3 encode.py <framesDir> <out.mp4>"""
import json, os, subprocess, sys
frames, out = sys.argv[1], sys.argv[2]
st = json.load(open(os.path.join(frames, "stamps.json")))
lines = []
for i, t in enumerate(st):
    d = (st[i + 1] - t) if i + 1 < len(st) else 1.5
    lines.append(f"file '{os.path.abspath(os.path.join(frames, f'{i:06d}.jpg'))}'\nduration {max(d, 0.001):.4f}")
lines.append(f"file '{os.path.abspath(os.path.join(frames, f'{len(st)-1:06d}.jpg'))}'")
lst = os.path.join(frames, "list.txt")
open(lst, "w").write("\n".join(lines) + "\n")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
    "-vf", "scale=1920:1080:flags=lanczos,fps=30,format=yuv420p",
    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-movflags", "+faststart", out], check=True)
print("wrote", out)
