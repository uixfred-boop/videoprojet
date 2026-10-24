"""Composite the guide cover onto the hands-holding-book reference photo.

Usage: python3 make_hands_poster.py <reference.jpg> <out.png> <bg_hex>
Maps the cover onto the front face and a rendered spine onto the spine, keeps
the photo's own lighting and the hands on top, and recolors the wall.
"""
import sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

SCALE = 3  # work at 3x the reference so the cover stays crisp
FRONT = [(80, 273), (466, 145), (723, 683), (317, 840)]
SPINE = [(57, 300), (80, 273), (317, 842), (288, 857)]
TERRACOTTA = (180, 83, 47)
CREAM = (243, 233, 218)
HERE = __file__.rsplit("/", 1)[0]


def quad_mask(shape, quad):
    m = np.zeros(shape[:2], np.uint8)
    cv2.fillPoly(m, [np.array(quad, np.int32)], 255)
    return m


def warp(src, quad, shape):
    h, w = src.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32([(0, 0), (w, 0), (w, h), (0, h)]), np.float32(quad))
    return cv2.warpPerspective(src, M, (shape[1], shape[0]), flags=cv2.INTER_LANCZOS4)


def spine_texture(h=2400, w=150):
    img = Image.new("RGB", (h, w), TERRACOTTA)  # drawn sideways, rotated below
    d = ImageDraw.Draw(img)
    sans = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 58)
    text = "5  M I S T A K E S   ·   F I R S T   C L I E N T   ·   F R E D"
    tw = d.textlength(text, font=sans)
    d.text(((h - tw) / 2, w / 2), text, font=sans, fill=CREAM, anchor="lm")
    return np.array(img.rotate(-90, expand=True))


def main(ref_path, out_path, bg_hex):
    ref = cv2.cvtColor(cv2.imread(ref_path), cv2.COLOR_BGR2RGB)
    ref = cv2.resize(ref, None, fx=SCALE, fy=SCALE, interpolation=cv2.INTER_LANCZOS4)
    front_q = [(x * SCALE, y * SCALE) for x, y in FRONT]
    spine_q = [(x * SCALE, y * SCALE) for x, y in SPINE]
    f = ref.astype(np.float32)
    R, G, B = f[..., 0], f[..., 1], f[..., 2]

    # Skin = warm, saturated pixels; everything else inside the book is cover.
    skin = ((R - B > 28) & (R > G)).astype(np.uint8) * 255
    skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    # Lighting map: luminance of the white cover with its printed design removed.
    ink = ((B - R > 18) | (f.mean(-1) < 90)).astype(np.uint8) * 255
    ink = cv2.dilate(ink, np.ones((15, 15), np.uint8))
    lum = cv2.cvtColor(ref, cv2.COLOR_RGB2GRAY)
    lum = cv2.inpaint(lum, ink, 9, cv2.INPAINT_TELEA).astype(np.float32)
    lum = cv2.GaussianBlur(lum, (0, 0), 4)

    book_f = quad_mask(ref.shape, front_q)
    book_s = quad_mask(ref.shape, spine_q)
    white = np.percentile(lum[book_f > 0], 96)
    shade_f = np.clip(lum / white, 0, 1.05)
    lum_s = cv2.GaussianBlur(lum, (0, 0), 30)  # spine: smooth away the old lettering
    s_vals = lum_s[book_s > 0]
    shade_s = np.clip(0.55 + 0.5 * (lum_s - s_vals.min()) / (np.percentile(s_vals, 95) - s_vals.min()), 0, 1.05)

    cover = cv2.cvtColor(cv2.imread(f"{HERE}/assets/cover.png"), cv2.COLOR_BGR2RGB)
    cov_w = warp(cover, front_q, ref.shape).astype(np.float32) * shade_f[..., None]
    spi_w = warp(spine_texture(), spine_q, ref.shape).astype(np.float32) * shade_s[..., None]

    # --- recolor the wall: keep its light and shadow, change the hue ---
    from rembg import remove, new_session
    fg = np.maximum.reduce([
        np.array(remove(Image.fromarray(ref), session=new_session(n), only_mask=True), np.float32) / 255
        for n in ("u2net", "u2net_human_seg")])
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    fg = np.clip((fg - 0.35) / 0.4, 0, 1)  # tighten soft edges so no old wall halo remains
    fg = np.maximum(fg, (book_f | book_s) / 255.0)
    tgt = np.array([int(bg_hex[i:i + 2], 16) for i in (1, 3, 5)], np.float32)
    wall_L = lum / np.percentile(lum[fg < 0.1], 90)
    wall = np.clip(tgt[None, None] * (0.25 + 0.85 * wall_L[..., None]), 0, 255)
    out = f * fg[..., None] + wall * (1 - fg[..., None])

    def paste(img, mask):
        m = cv2.GaussianBlur(mask.astype(np.float32) / 255, (0, 0), 1.2)[..., None]
        return img * m + out * (1 - m)

    not_skin = cv2.bitwise_not(skin)
    out = paste(spi_w, cv2.erode(book_s, np.ones((3, 3), np.uint8)) & not_skin)
    out = paste(cov_w, cv2.erode(book_f, np.ones((3, 3), np.uint8)) & not_skin)

    # Crop to 4:5 and export at Instagram size.
    H, W = out.shape[:2]
    ch = int(W * 5 / 4)
    top = 50 * SCALE
    out = out[top:top + ch]
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).resize((1080, 1350), Image.LANCZOS).save(out_path)


if __name__ == "__main__":
    main(*sys.argv[1:4])
