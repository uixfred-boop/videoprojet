"""Blue-glass UI elements (Kallaway-style), drawn at 4K as RGBA PNGs.
Layout units are 1920x1080 ("pt"); everything is drawn at K=2 for 3840x2160."""
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

K = 2
W, H = 1920 * K, 1080 * K
k = lambda v: int(round(v * K))

def font(style="SemiBold", italic=False):
    q = f"Inter:style={style}{' Italic' if italic else ''}"
    return subprocess.run(["fc-match", "-f", "%{file}", q], capture_output=True, text=True).stdout
FB, FS, FR, FI = font("Bold"), font("SemiBold"), font("Regular"), font("Medium", True)
F = lambda path, size: ImageFont.truetype(path, k(size))

WHITE = (255, 255, 255)
DIM = (255, 255, 255, 150)
BLUE = (61, 123, 255)
LINE = (207, 224, 255)

def background(seed=0):
    """Full-screen navy background: vertical gradient + radial blue glow + fine grain."""
    y = np.linspace(0, 1, H)[:, None]; x = np.linspace(0, 1, W)[None, :]
    top, bot = np.array([11, 18, 32]), np.array([18, 48, 94])
    img = top * (1 - y[..., None] ** 1.4) + bot * (y[..., None] ** 1.4)
    g = np.exp(-(((x - 0.5) / 0.55) ** 2 + ((y - 1.05) / 0.45) ** 2))[..., None]
    img = img + g * np.array([47, 107, 255]) * 0.35
    img = img + np.random.default_rng(seed).normal(0, 2.2, (H, W, 1))
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")

def glow(im, radius=18, strength=0.55, color=(80, 140, 255)):
    """Add an outer glow around the alpha of an RGBA element (returns a bigger canvas, offset = pad)."""
    pad = k(radius) * 3
    big = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad))
    a = Image.new("L", big.size); a.paste(im.getchannel("A"), (pad, pad))
    a = a.filter(ImageFilter.GaussianBlur(k(radius))).point(lambda v: int(v * strength))
    halo = Image.new("RGBA", big.size, color + (0,)); halo.putalpha(a)
    big = Image.alpha_composite(big, halo); big.alpha_composite(im, (pad, pad))
    return big, pad

def glass(w, h, r=14, fill=(16, 32, 64), alpha=200, border=(170, 200, 255, 150)):
    """Rounded glass card: navy fill, top light gradient, thin light border, outer glow."""
    w, h = k(w), k(h); R = k(r)
    im = Image.new("RGBA", (w, h)); m = Image.new("L", (w, h))
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), R, fill=255)
    grad = np.linspace(1.0, 0.0, h)[:, None] ** 1.6
    base = np.zeros((h, w, 4), np.float32); base[..., :3] = fill; base[..., :3] += grad[..., None] * 38
    base[..., 3] = alpha
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGBA"); im.putalpha(Image.fromarray((np.array(m) * alpha / 255).astype(np.uint8)))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), R, outline=border, width=max(2, k(1.2)))
    return glow(im, 16, 0.45)

def text_img(lines, size=40, fnt=None, color=WHITE, spacing=1.25, align="left", hl=None, glow_strength=0.0):
    """Multi-line text; `hl` = set of words drawn on a blue pill highlight."""
    fnt = F(fnt or FB, size); asc, desc = fnt.getmetrics(); lh = int((asc + desc) * spacing)
    widths = [int(fnt.getlength(l)) for l in lines]; w = max(widths) + k(24); h = lh * len(lines) + k(10)
    im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        x = k(12) if align == "left" else (w - widths[i]) // 2
        y = i * lh
        if hl:
            cx = x
            for word in l.split(" "):
                ww = fnt.getlength(word + " ")
                if word.strip(".,:!?\"").lower() in hl:
                    d.rounded_rectangle((cx - k(6), y + k(2), cx + fnt.getlength(word) + k(6), y + asc + desc - k(2)), k(8), fill=BLUE + (255,))
                cx += ww
        d.text((x, y), l, font=fnt, fill=color)
    if glow_strength:
        return glow(im, 14, glow_strength, (110, 160, 255))
    return im, 0

def icon_check(size=34, ok=True):
    s = k(size); im = Image.new("RGBA", (s, s)); d = ImageDraw.Draw(im)
    col = (80, 220, 160, 255) if ok else (255, 95, 110, 255)
    d.ellipse((0, 0, s - 1, s - 1), outline=col, width=k(2.5))
    if ok: d.line([(s * .28, s * .52), (s * .44, s * .68), (s * .73, s * .34)], fill=col, width=k(3.2), joint="curve")
    else:
        d.line([(s * .32, s * .32), (s * .68, s * .68)], fill=col, width=k(3.2)); d.line([(s * .68, s * .32), (s * .32, s * .68)], fill=col, width=k(3.2))
    return im

def card(title=None, lines=(), w=520, size=30, icon=None, num=None, italic=False, hl=None, pad=26):
    """Glass card with optional small label/title, body lines, leading icon or number badge."""
    fb = F(FI if italic else FS, size); asc, desc = fb.getmetrics(); lh = int((asc + desc) * 1.3)
    tf = F(FR, 20)
    head = k(34) if title else 0
    lead = k(64) if (icon is not None or num is not None) else 0
    h = (head + lh * max(1, len(lines)) + k(pad) * 2) / K
    g, p = glass(w, h)
    d = ImageDraw.Draw(g)
    x0 = p + k(pad); y0 = p + k(pad)
    if title:
        d.text((x0, y0 - k(4)), title, font=tf, fill=(200, 215, 255, 190))
        d.line([(x0, y0 + k(26)), (p + k(w) - k(pad), y0 + k(26))], fill=(170, 200, 255, 70), width=k(1))
    if num is not None:
        nb = F(FB, 30); d.ellipse((x0, y0 + head, x0 + k(46), y0 + head + k(46)), fill=BLUE + (255,))
        d.text((x0 + k(23), y0 + head + k(23)), str(num), font=nb, fill=WHITE, anchor="mm")
    if icon is not None:
        g.alpha_composite(icon_check(40, icon), (x0, y0 + head + k(3)))
    cx = x0 + lead
    for i, l in enumerate(lines):
        y = y0 + head + i * lh
        if hl:
            xx = cx
            for word in l.split(" "):
                if word.strip(".,:!?\"").lower() in hl:
                    d.rounded_rectangle((xx - k(5), y + k(2), xx + fb.getlength(word) + k(5), y + asc + desc - k(1)), k(7), fill=BLUE + (255,))
                xx += fb.getlength(word + " ")
        d.text((cx, y), l, font=fb, fill=WHITE)
    return g, p

def chip(text, size=26, w=None):
    f = F(FS, size); tw = f.getlength(text)
    g, p = glass((w or (tw / K + 48)), size * 1.9, r=size * 0.95)
    ImageDraw.Draw(g).text((g.width // 2, g.height // 2), text, font=f, fill=WHITE, anchor="mm")
    return g, p

def arrow(length=90, vertical=False):
    L = k(length); t = k(3)
    im = Image.new("RGBA", (L, k(24)) if not vertical else (k(24), L)); d = ImageDraw.Draw(im)
    if not vertical:
        d.line([(0, k(12)), (L - k(12), k(12))], fill=LINE + (230,), width=t); d.polygon([(L, k(12)), (L - k(16), k(3)), (L - k(16), k(21))], fill=LINE + (230,))
    else:
        d.line([(k(12), 0), (k(12), L - k(12))], fill=LINE + (230,), width=t); d.polygon([(k(12), L), (k(3), L - k(16)), (k(21), L - k(16))], fill=LINE + (230,))
    return glow(im, 8, 0.6)

def browser_frame(w, h, url=""):
    """Rounded browser window frame with a transparent viewport; returns (img, pad, viewport box)."""
    bar = 46
    g, p = glass(w, h + bar, r=16, fill=(14, 20, 34), alpha=255)
    d = ImageDraw.Draw(g)
    for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        cx = p + k(26 + i * 22); d.ellipse((cx - k(6), p + k(17), cx + k(6), p + k(29)), fill=c + (255,))
    d.rounded_rectangle((p + k(w / 2 - 170), p + k(10), p + k(w / 2 + 170), p + k(36)), k(10), fill=(30, 40, 62, 255))
    if url: d.text((p + k(w / 2), p + k(23)), url, font=F(FR, 16), fill=(190, 200, 225, 255), anchor="mm")
    vp = (p + k(2), p + k(bar), p + k(w) - k(2), p + k(bar + h) - k(2))
    a = np.array(g); a[vp[1]:vp[3], vp[0]:vp[2], 3] = 0   # transparent viewport
    return Image.fromarray(a), p, vp

def save(item, path):
    im, pad = item if isinstance(item, tuple) else (item, 0)
    im.save(path); return {"path": path, "w": im.width, "h": im.height, "pad": pad}
