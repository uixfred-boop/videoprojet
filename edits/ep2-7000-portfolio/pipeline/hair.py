"""Recolour hair to pure (neutral) black, frame by frame.
mask = MediaPipe hair segmenter on a head crop
       x person alpha (RVM matte, shifted like the composite) x darkness gate (protects skin at the hairline),
       lightly smoothed over time so it never flickers.
Hair pixels lose all chroma and are darkened, keeping a little luminance texture so it doesn't look painted."""
import subprocess, sys
import numpy as np, cv2, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision

src, pha_p, model, out = sys.argv[1:5]
DX = int(sys.argv[5]) if len(sys.argv) > 5 else 0      # same horizontal shift the composite used
W, H = 3840, 2160
X0, X1, Y0, Y1 = int(W * .25), int(W * .75), 0, int(H * .62)  # head search area
DARKEN, KEEP = 0.55, 0.35   # luminance scale for hair, and how much original texture survives

seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=mpt.BaseOptions(model_asset_path=model), running_mode=vision.RunningMode.VIDEO,
    output_confidence_masks=True))

def reader(path, fmt, ch):
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", fmt, "-"],
                         stdout=subprocess.PIPE)
    def nxt():
        b = p.stdout.read(W * H * ch)
        return None if len(b) < W * H * ch else np.frombuffer(b, np.uint8).reshape(H, W, ch)
    return nxt

rs, rp = reader(src, "rgb24", 3), reader(pha_p, "gray", 1)
enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                        "-r", "30", "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "10", "-pix_fmt", "yuv444p",
                        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                        out], stdin=subprocess.PIPE)
prev = None; n = 0
while True:
    f, a = rs(), rp()
    if f is None or a is None: break
    crop = np.ascontiguousarray(f[Y0:Y1, X0:X1])
    r = seg.segment_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=crop), int(n * 1000 / 30))
    m = cv2.resize(r.confidence_masks[-1].numpy_view().astype(np.float32), (X1 - X0, Y1 - Y0))
    m = prev * 0.3 + m * 0.7 if prev is not None else m
    prev = m
    alpha = a[..., 0].astype(np.float32) / 255
    if DX: alpha = np.roll(alpha, DX, axis=1); alpha[:, :DX] = 0
    c = crop.astype(np.float32) / 255
    lum = c @ np.float32([0.2126, 0.7152, 0.0722])
    gate = np.clip((0.32 - lum) / 0.12, 0, 1)          # dark pixels only: hair yes, skin no
    w = np.clip(m, 0, 1) * alpha[Y0:Y1, X0:X1] * gate
    black = (lum * DARKEN)[..., None]
    target = black * (1 - KEEP) + (c.mean(2, keepdims=True) * DARKEN) * KEEP  # neutral, faint texture
    c = c * (1 - w[..., None]) + target * w[..., None]
    o = f.copy(); o[Y0:Y1, X0:X1] = (np.clip(c, 0, 1) * 255 + 0.5).astype(np.uint8)
    enc.stdin.write(o.tobytes()); n += 1
    if n % 100 == 0: print(n, flush=True)
enc.stdin.close(); enc.wait()
print("frames", n)
