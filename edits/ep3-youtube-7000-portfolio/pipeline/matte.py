"""Frame-by-frame person matting with Robust Video Matting (recurrent, so edges stay temporally stable).
Writes alpha (gray) and RVM's de-spilled foreground (rgb) as lossless FFV1 at 1080x1920."""
import subprocess, sys, time
import numpy as np, onnxruntime as ort

model, src, out_pha, out_fgr = sys.argv[1:5]
limit = int(sys.argv[5]) if len(sys.argv) > 5 else 10 ** 9
W, H, DS = (int(sys.argv[6]), int(sys.argv[7]), float(sys.argv[8])) if len(sys.argv) > 8 else (1080, 1920, 0.3)

so = ort.SessionOptions(); so.intra_op_num_threads = 4
sess = ort.InferenceSession(model, so, providers=["CPUExecutionProvider"])
SS, TT = (float(sys.argv[9]), float(sys.argv[10])) if len(sys.argv) > 10 else (0.0, 1e6)
dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", f"{SS:.3f}", "-t", f"{TT:.3f}", "-i", src, "-vf", f"scale={W}:{H}:flags=lanczos",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = lambda fmt, path: subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", fmt,
                                          "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-c:v", "ffv1", path], stdin=subprocess.PIPE)
ep = enc("gray", out_pha); ef = enc("rgb24", out_fgr) if out_fgr != "none" else None
rec = [np.zeros((1, 1, 1, 1), np.float32)] * 4
ds = np.array([DS], np.float32)
n = 0; t0 = time.time()
while n < limit:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    x = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32).transpose(2, 0, 1)[None] / 255
    fgr, pha, *rec = sess.run(None, {"src": x, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3], "downsample_ratio": ds})
    ep.stdin.write((pha[0, 0] * 255 + 0.5).clip(0, 255).astype(np.uint8).tobytes())
    if ef: ef.stdin.write((fgr[0].transpose(1, 2, 0) * 255 + 0.5).clip(0, 255).astype(np.uint8).tobytes())
    n += 1
    if n % 100 == 0: print(n, f"{(time.time() - t0) / n:.2f}s/frame", flush=True)
for e in (ep, ef):
    if e: e.stdin.close(); e.wait()
dec.kill()
print("frames", n, f"{(time.time() - t0) / max(n, 1):.2f}s/frame")
