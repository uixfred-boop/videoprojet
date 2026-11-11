"""Join all shots + mastered voice into the final 4K export (two-pass H.264, 45 Mbps, BT.709).
Every shot is brought to its exact frame count first, so picture and voice stay locked for the whole video."""
import json, os, subprocess, sys
E, OUT = sys.argv[1], sys.argv[2]
FPS = 30
S = json.load(open(f"{E}/shots.json"))["shots"]
probe = lambda p: int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                                      "stream=nb_read_frames", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip())
BT709 = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
os.makedirs(f"{E}/shots/fixed", exist_ok=True)
files = []
for i, s in enumerate(S):
    n = round((s["t1"] - s["t0"]) * FPS); src = f"{E}/shots/s{i:03d}.mp4"; dst = f"{E}/shots/fixed/s{i:03d}.mp4"
    got = probe(src)
    if abs(got - n) > 2: print(f"shot {i}: {got} frames, expected {n}", flush=True)
    if got == n: files.append(src); continue
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src,
                    "-vf", f"tpad=stop_mode=clone:stop=5,trim=end_frame={n},setpts=N/({FPS}*TB)",
                    "-frames:v", str(n), "-r", str(FPS), "-c:v", "libx264", "-preset", "fast", "-crf", "12",
                    "-pix_fmt", "yuv420p", *BT709, dst], check=True)
    files.append(dst)
lst = f"{E}/final_list.txt"
with open(lst, "w") as f:
    for p in files: f.write(f"file '{p}'\n")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{E}/video_only.mp4"], check=True)
print("video frames", probe(f"{E}/video_only.mp4"), "expected", sum(round((s["t1"] - s["t0"]) * FPS) for s in S), flush=True)
v = ["-c:v", "libx264", "-preset", "slow", "-b:v", "45M", "-maxrate", "60M", "-bufsize", "90M", "-pix_fmt", "yuv420p",
     "-profile:v", "high", "-level", "5.2", *BT709, "-passlogfile", f"{E}/x264final"]
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{E}/video_only.mp4", *v, "-pass", "1", "-an", "-f", "null", "/dev/null"], check=True)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{E}/video_only.mp4", "-i", f"{E}/vo_master.wav", "-map", "0:v", "-map", "1:a",
                *v, "-pass", "2", "-tag:v", "avc1", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2",
                "-movflags", "+faststart", OUT], check=True)
print("done", OUT)
