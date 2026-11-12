"""Build the YouTube thumbnail.

Takes the reference thumbnail (blue/black gradient, "AWWWARDS" headline,
dark device frame) and replaces the website shown inside the frame with
our own site. Also removes the "6:13" duration badge, cleans the white
rounded corners left over from the YouTube UI screenshot, and exports a
16:9 image at 1920x1080.

Usage:  python3 miniature/build_thumbnail.py
"""

from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REF_PATH = HERE / "sources" / "reference.webp"
SITE_PATH = HERE / "sources" / "site.webp"
OUT_PNG = HERE / "miniature-youtube.png"
OUT_JPG = HERE / "miniature-youtube.jpg"

OUT_SIZE = (1920, 1080)
SS = 8  # supersampling factor for the anti-aliased screen mask


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def lum(a):
    return a[..., :3].mean(axis=2)


def dilate(mask, r):
    """Binary dilation with a disc of radius r (no wrap-around at edges)."""
    h, w = mask.shape
    p = np.pad(mask, r)
    out = np.zeros_like(mask)
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dy * dy + dx * dx > r * r:
                continue
            out |= p[r + dy:r + dy + h, r + dx:r + dx + w]
    return out


def harmonic_fill(img, mask, iters=4000):
    """Fill masked pixels by solving Laplace's equation (smooth inpainting).

    Works well for smooth backgrounds (gradients, flat colours)."""
    ys, xs = np.where(mask)
    if len(ys) == 0:
        return img
    h, w = mask.shape
    y0, y1 = max(ys.min() - 3, 0), min(ys.max() + 4, h)
    x0, x1 = max(xs.min() - 3, 0), min(xs.max() + 4, w)
    sub = img[y0:y1, x0:x1].copy()
    m = mask[y0:y1, x0:x1]
    ring = dilate(m, 1) & ~m
    sub[m] = sub[ring].mean(axis=0)
    for _ in range(iters):
        p = np.pad(sub, ((1, 1), (1, 1), (0, 0)), mode="edge")
        avg = (p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:]) / 4.0
        sub[m] = avg[m]
    img[y0:y1, x0:x1] = sub
    return img


def crossing(profile, thr):
    """Sub-pixel index where a 1-D profile first rises above thr."""
    for i in range(1, len(profile)):
        if profile[i] >= thr > profile[i - 1]:
            return (i - 1) + (thr - profile[i - 1]) / (profile[i] - profile[i - 1])
    raise ValueError("no crossing")


def _axis_cov(n, start, lo, hi):
    """Coverage of pixels [start+i, start+i+1) by the interval [lo, hi]."""
    i = start + np.arange(n)
    return np.clip(np.minimum(i + 1, hi) - np.maximum(i, lo), 0, 1)


def _corners(box, r):
    L, T, R, B = box
    return ((L + r, T + r, -1, -1), (R - r, T + r, 1, -1),
            (L + r, B - r, -1, 1), (R - r, B - r, 1, 1))


def _inside(X, Y, box, r):
    L, T, R, B = box
    ins = (X >= L) & (X <= R) & (Y >= T) & (Y <= B)
    for cx, cy, sx, sy in _corners(box, r):
        beyond = (sx * (X - cx) > 0) & (sy * (Y - cy) > 0)
        ins &= ~(beyond & ((X - cx) ** 2 + (Y - cy) ** 2 > r * r))
    return ins


def rounded_rect_coverage(shape, box, r, origin):
    """Anti-aliased coverage (0..1) of a rounded rectangle.

    box = (L, T, R, B) in continuous image coordinates (pixel i spans [i, i+1)).
    origin = (x0, y0) of the returned array in image coordinates.
    Straight edges are exact (separable); corners are supersampled."""
    h, w = shape
    x0, y0 = origin
    L, T, R, B = box
    cov = np.outer(_axis_cov(h, y0, T, B), _axis_cov(w, x0, L, R))
    for cx, cy, _, _ in _corners(box, r):
        px0 = max(int(np.floor(cx - r - 2)) - x0, 0)
        px1 = min(int(np.ceil(cx + r + 2)) - x0, w)
        py0 = max(int(np.floor(cy - r - 2)) - y0, 0)
        py1 = min(int(np.ceil(cy + r + 2)) - y0, h)
        xs = x0 + px0 + (np.arange((px1 - px0) * SS) + 0.5) / SS
        ys = y0 + py0 + (np.arange((py1 - py0) * SS) + 0.5) / SS
        X, Y = np.meshgrid(xs, ys)
        ins = _inside(X, Y, box, r)
        cov[py0:py1, px0:px1] = ins.reshape(py1 - py0, SS, px1 - px0, SS).mean(axis=(1, 3))
    return cov


# --------------------------------------------------------------------------
# 1. load
# --------------------------------------------------------------------------
ref = np.asarray(Image.open(REF_PATH).convert("RGB")).astype(np.float64)
H, W = ref.shape[:2]
L_ = lum(ref)

site_rgba = Image.open(SITE_PATH).convert("RGBA")
white = Image.new("RGBA", site_rgba.size, (255, 255, 255, 255))
site = Image.alpha_composite(white, site_rgba).convert("RGB")

# --------------------------------------------------------------------------
# 2. measure the screen (light area inside the dark frame) with sub-pixel
#    precision on each side
# --------------------------------------------------------------------------
frame_px = ref[300:900, 269:274].reshape(-1, 3)
frame_color = np.median(frame_px, axis=0)
frame_lum = frame_color.mean()

lefts, rights, tops, bottoms = [], [], [], []
for y in range(300, 950, 10):
    inner = L_[y, 295]
    thr = (frame_lum + inner) / 2
    lefts.append(270 + crossing(L_[y, 270:300], thr) + 0.5)
    inner = L_[y, 1725]
    thr = (frame_lum + inner) / 2
    prof = L_[y, 1752:1720:-1]  # from the frame towards the inside
    rights.append(1752 - crossing(prof, thr) + 0.5)
for x in range(400, 1500, 10):
    inner = L_[212, x]
    thr = (frame_lum + inner) / 2
    tops.append(186 + crossing(L_[186:215, x], thr) + 0.5)
    inner = L_[1045, x]
    thr = (frame_lum + inner) / 2
    prof = L_[1066:1040:-1, x]
    bottoms.append(1066 - crossing(prof, thr) + 0.5)

SL, SR = float(np.median(lefts)), float(np.median(rights))
ST, SB = float(np.median(tops)), float(np.median(bottoms))
box = (SL, ST, SR, SB)

# corner radius: pick the one whose rendered edge best matches the original
bx0, by0 = int(SL) - 3, int(ST) - 3
bx1, by1 = int(np.ceil(SR)) + 3, int(np.ceil(SB)) + 3
best_r, best_err = None, 1e18
corners = [
    (slice(by0 - by0, 30), slice(0, 30)),
    (slice(0, 30), slice(bx1 - bx0 - 30, bx1 - bx0)),
    (slice(by1 - by0 - 30, by1 - by0), slice(0, 30)),
    (slice(by1 - by0 - 30, by1 - by0), slice(bx1 - bx0 - 30, bx1 - bx0)),
]
region_lum = L_[by0:by1, bx0:bx1]
for r in np.arange(8, 22, 0.5):
    cov = rounded_rect_coverage((by1 - by0, bx1 - bx0), box, r, (bx0, by0))
    pred = cov * 246 + (1 - cov) * frame_lum
    err = sum(np.abs(pred[s] - region_lum[s]).sum() for s in corners)
    if err < best_err:
        best_r, best_err = r, err
RADIUS = float(best_r)
print(f"screen box L={SL:.2f} T={ST:.2f} R={SR:.2f} B={SB:.2f}  "
      f"({SR - SL:.1f} x {SB - ST:.1f}), corner radius {RADIUS}")

# --------------------------------------------------------------------------
# 3. clean-up of the reference: YouTube UI corners + "6:13" badge
# --------------------------------------------------------------------------
out = ref.copy()

# top-left / bottom-left corners sit on a dark background -> bright = UI
tl = np.zeros((H, W), bool)
tl[:60, :60] = L_[:60, :60] > 50
bl = np.zeros((H, W), bool)
bl[H - 30:, :30] = L_[H - 30:, :30] > 30
# top-right corner sits on light blue (R ~105) -> R channel high = UI white
tr = np.zeros((H, W), bool)
tr[:25, W - 40:] = ref[:25, W - 40:, 0] > 115
for m in (tl, bl, tr):
    out = harmonic_fill(out, dilate(m, 2), iters=3000)

# "6:13" duration (white text on near-black background)
dur = np.zeros((H, W), bool)
dur[1030:1100, 1850:1995] = L_[1030:1100, 1850:1995] > 10
out = harmonic_fill(out, dilate(dur, 4), iters=6000)

# --------------------------------------------------------------------------
# 4. new screen content: our site, centred, lanyard hanging from the top
# --------------------------------------------------------------------------
site_np = np.asarray(site).astype(np.float64)
nonwhite = site_np.min(axis=2) < 245
ys, xs = np.where(nonwhite)
c_top, c_bot = ys.min(), ys.max()
c_cx = (xs.min() + xs.max()) / 2

top_y = ST - 3  # let the lanyard start under the frame edge
bottom_margin = 30  # white space under the client logos
scale = (SB - bottom_margin - top_y) / (c_bot - 0)
new_w = round(site.width * scale)
new_h = round(site.height * scale)
site_small = site.resize((new_w, new_h), Image.LANCZOS)

reg_w, reg_h = bx1 - bx0, by1 - by0
screen = Image.new("RGB", (reg_w, reg_h), (255, 255, 255))
paste_x = round((SL + SR) / 2 - c_cx * scale) - bx0
paste_y = round(top_y) - by0
screen.paste(site_small, (paste_x, paste_y))
screen_np = np.asarray(screen).astype(np.float64)
print(f"site scale {scale:.4f} -> {new_w}x{new_h}, pasted at "
      f"({paste_x + bx0}, {paste_y + by0})")

cov = rounded_rect_coverage((reg_h, reg_w), box, RADIUS, (bx0, by0))[..., None]
region = out[by0:by1, bx0:bx1]
blended = cov * screen_np + (1 - cov) * frame_color
region = np.where(cov > 0, blended, region)
out[by0:by1, bx0:bx1] = region

# --------------------------------------------------------------------------
# 5. crop the white UI border, extend to 16:9, resize to 1920x1080
# --------------------------------------------------------------------------
CROP_L, CROP_T = 8, 10
out = out[CROP_T:, CROP_L:]
h, w = out.shape[:2]
target_h = round(w * 9 / 16)
extra = target_h - h
if extra > 0:
    # stretch the smooth gradient strip below the frame
    s0 = 1078 - CROP_T
    strip = Image.fromarray(np.clip(out[s0:], 0, 255).astype(np.uint8))
    strip = strip.resize((w, strip.height + extra), Image.BICUBIC)
    out = np.concatenate([out[:s0], np.asarray(strip).astype(np.float64)], axis=0)
elif extra < 0:
    out = out[:target_h]

final = Image.fromarray(np.clip(np.rint(out), 0, 255).astype(np.uint8))
final = final.resize(OUT_SIZE, Image.LANCZOS)
final.save(OUT_PNG, optimize=True)
final.save(OUT_JPG, quality=95, subsampling=0, optimize=True)
print("saved", OUT_PNG, OUT_PNG.stat().st_size // 1024, "KB")
print("saved", OUT_JPG, OUT_JPG.stat().st_size // 1024, "KB")
