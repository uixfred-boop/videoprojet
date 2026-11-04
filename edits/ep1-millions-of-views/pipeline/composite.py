"""Replace the background behind the matted person, frame by frame.

person: white-balanced to take A (per-frame wall reading, smoothed), pulled toward the plate's
        colour (partial Lab transfer), RVM de-spilled foreground used on soft edges
plate : cropped/scaled to 9:16, slightly blurred, film grain to match phone noise
blend : alpha composite + light wrap (plate light bleeding onto the silhouette edge)
"""
import json, subprocess, sys
import numpy as np, cv2

src, pha_p, fgr_p, plate_p, cfg_p, out = sys.argv[1:7]
limit = int(sys.argv[7]) if len(sys.argv) > 7 else 10 ** 9
cfg = json.load(open(cfg_p))
W, H = 1080, 1920
rng = np.random.default_rng(3)


def reader(path, fmt, ch):
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", path, "-vf", f"scale={W}:{H}:flags=lanczos",
                          "-f", "rawvideo", "-pix_fmt", fmt, "-"], stdout=subprocess.PIPE)
    def nxt():
        b = p.stdout.read(W * H * ch)
        return None if len(b) < W * H * ch else np.frombuffer(b, np.uint8).reshape(H, W, ch)
    return nxt


# ---- background plate
img = cv2.cvtColor(cv2.imread(plate_p), cv2.COLOR_BGR2RGB)
x0, y0, cw, ch = cfg["crop"]
plate = cv2.resize(img[y0:y0 + ch, x0:x0 + cw], (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32) / 255
plate = cv2.GaussianBlur(plate, (0, 0), cfg["blur"])
plate = np.clip(plate * cfg.get("exposure", 1.0), 0, 1)
wrap_src = cv2.GaussianBlur(plate, (0, 0), 30)
lab_p = cv2.cvtColor(plate, cv2.COLOR_RGB2LAB)
p_ab = lab_p[..., 1:].reshape(-1, 2).mean(0)

# ---- white balance reference: take A's wall as shot
REF = np.array(cfg["wall_ref"], np.float32); TARGET = REF / REF.mean()

rs, rp, rf = reader(src, "rgb24", 3), reader(pha_p, "gray", 1), reader(fgr_p, "rgb24", 3)
enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                        "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "8",
                        "-pix_fmt", "yuv444p", out], stdin=subprocess.PIPE)
gains = None; n = 0
while n < limit:
    s, a, f = rs(), rp(), rf()
    if s is None or a is None: break
    s = s.astype(np.float32) / 255; f = f.astype(np.float32) / 255; a = a[..., 0].astype(np.float32) / 255
    # per-frame WB from the original wall (top-left), smoothed so it never pumps
    wall = s[int(H * .03):int(H * .12), int(W * .02):int(W * .18)].reshape(-1, 3).mean(0)
    g = TARGET / (wall / wall.mean()); g /= g.mean()
    gains = g if gains is None else 0.9 * gains + 0.1 * g
    # solid interior from the camera image, soft edges from RVM's de-spilled foreground
    core = np.clip((a - 0.9) / 0.1, 0, 1)[..., None]
    fg = np.clip((s * core + f * (1 - core)) * gains, 0, 1)
    # pull the person's chroma toward the plate (partial), keep his exposure
    lab = cv2.cvtColor(fg, cv2.COLOR_RGB2LAB)
    m = a > 0.5
    if m.any():
        f_ab = lab[..., 1:][m].mean(0)
        lab[..., 1:] += cfg["match"] * (p_ab - f_ab)
    lab[..., 0] *= cfg.get("fg_exposure", 1.0)
    fg = np.clip(cv2.cvtColor(lab, cv2.COLOR_LAB2RGB), 0, 1)
    # motivated light: warm falloff from the side the practical light sits on
    if cfg.get("rim"):
        side, amt, col = cfg["rim"]["side"], cfg["rim"]["amount"], np.array(cfg["rim"]["color"], np.float32)
        ramp = np.linspace(0, 1, W, dtype=np.float32) if side == "right" else np.linspace(1, 0, W, dtype=np.float32)
        fg = fg * (1 + amt * (ramp[None, :, None] ** 2) * (col - 1))
    # light wrap: plate light spilling over the silhouette edge
    edge = np.clip(cv2.GaussianBlur(1 - a, (0, 0), 12) * a, 0, 1)[..., None]
    fg = fg + cfg["wrap"] * edge * wrap_src * (1 - fg)
    # matching grain on the clean plate
    bg = plate + rng.normal(0, cfg["grain"] / 255, (H, W, 1)).astype(np.float32)
    A = a[..., None]
    o = fg * A + bg * (1 - A)
    enc.stdin.write((np.clip(o, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
    n += 1
    if n % 150 == 0: print(n, flush=True)
enc.stdin.close(); enc.wait()
print("frames", n)
