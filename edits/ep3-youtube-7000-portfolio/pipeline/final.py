"""Final export: shots -> frame-exact concat -> darkened bottom + word-by-word subtitles -> two-pass H.264 with the voice.
usage: final.py <work> <out.mp4> <kbps> [--reuse]   (45000 = master, 9600 = copy under 400 MB)
--reuse keeps an existing video_capt.mp4 (picture with subtitles) and only re-encodes."""
import json, os, subprocess, sys
E, OUT, KBPS = sys.argv[1], sys.argv[2], int(sys.argv[3]); REUSE = "--reuse" in sys.argv
FPS = 30
S = json.load(open(f"{E}/shots.json"))["shots"]
BT709 = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
probe = lambda p: int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                                      "stream=nb_read_frames", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip())
expected = sum(round((s["t1"] - s["t0"]) * FPS) for s in S)
cap = f"{E}/video_capt.mp4"
if not (REUSE and os.path.exists(cap)):
    os.makedirs(f"{E}/shots/fixed", exist_ok=True)
    files = []
    for i, s in enumerate(S):                       # every shot to its exact frame count (keeps lip-sync locked)
        n = round((s["t1"] - s["t0"]) * FPS); src = f"{E}/shots/s{i:03d}.mp4"; dst = f"{E}/shots/fixed/s{i:03d}.mp4"
        got = probe(src)
        if abs(got - n) > 2: print(f"shot {i}: {got} frames, expected {n}", flush=True)
        if got == n: files.append(src); continue
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-vf", f"tpad=stop_mode=clone:stop=5,trim=end_frame={n},setpts=N/({FPS}*TB)",
                        "-frames:v", str(n), "-r", str(FPS), "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-pix_fmt", "yuv420p", *BT709, dst], check=True)
        files.append(dst)
    lst = f"{E}/final_list.txt"; open(lst, "w").write("".join(f"file '{p}'\n" for p in files))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{E}/video_only.mp4"], check=True)
    print("video_only frames", probe(f"{E}/video_only.mp4"), "expected", expected, flush=True)
    # darkened bottom (so the subtitles read cleanly) + subtitles, rendered once into a near-lossless intermediate
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{E}/video_only.mp4", "-loop", "1", "-i", f"{E}/bottom_grad.png",
                    "-filter_complex", f"[0:v][1:v]overlay=0:0:format=auto:shortest=1,subtitles={E}/captions.ass:fontsdir={E}/capfonts,format=yuv420p[v]",
                    "-map", "[v]", "-frames:v", str(expected), "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-x264-params", "keyint=60",
                    *BT709, cap], check=True)
    print("captioned frames", probe(cap), flush=True)
hi = KBPS > 20000
v = ["-c:v", "libx264", "-preset", "slow", "-b:v", f"{KBPS}k", "-maxrate", f"{int(KBPS * (1.33 if hi else 1.67))}k", "-bufsize", f"{KBPS * 2}k",
     "-x264-params", "aq-mode=3", "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "5.2" if hi else "5.1", *BT709,
     "-passlogfile", f"{E}/x264fin{KBPS}"]
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", cap, *v, "-pass", "1", "-an", "-f", "null", "/dev/null"], check=True)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", cap, "-i", f"{E}/vo_master.wav", "-map", "0:v", "-map", "1:a", *v, "-pass", "2",
                "-tag:v", "avc1", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", OUT], check=True)
print("done", OUT, "frames", probe(OUT), flush=True)
