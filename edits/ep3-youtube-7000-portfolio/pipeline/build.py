"""Episode 3 edit: shot list -> 4K talking-head pieces + blue-glass graphics + screen recordings -> one video.
usage: build.py <work> [only_shot_index ...]"""
import json, os, subprocess, sys
sys.path.insert(0, sys.argv[1])
from gfx import *

E = sys.argv[1]; ONLY = set(int(x) for x in sys.argv[2:])
RAW = f"{E}/raw.mp4"; G = f"{E}/g"; SH = f"{E}/shots"; os.makedirs(G, exist_ok=True); os.makedirs(SH, exist_ok=True)
FPS = 30
clips = json.load(open(f"{E}/edl.json"))["clips"]
t = 0.0
for c in clips:
    c["d"] = c.get("silent") or round((c["b"] - c["a"]) * FPS) / FPS; c["t"] = round(t, 4); t += c["d"]
TOTAL = round(t, 4)
T = {c["id"]: c["t"] for c in clips}

def setup_of(a):
    return "A" if a < 125 else ("B" if a < 380 else "C")

# ------------------------------------------------------------------ element helpers (cached PNGs)
_n = [0]
def png(item, name=None):
    _n[0] += 1; path = f"{G}/{name or 'e%03d' % _n[0]}.png"; info = save(item, path); return info
def el(info, x, y, t, anim="up", out=None, d=0.4):
    return {"png": info["path"], "pad": info["pad"], "x": x, "y": y, "t": round(t, 3), "anim": anim, "out": out, "d": d}
EMPTY = f"{G}/empty.png"; Image.new("RGBA", (4, 4)).save(EMPTY)
BG = f"{G}/bg.png"
if not os.path.exists(BG): background(0).save(BG)

CHAPTERS = ["The mistake", "The click", "The choice", "The build", "The details", "The pivot", "The outreach", "The lesson", "The offer"]
def progress(idx):
    w, h = k(900), k(40); im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im)
    n = len(CHAPTERS); xs = [int(k(20) + i * (w - k(40)) / (n - 1)) for i in range(n)]; y = h // 2
    d.line([(xs[0], y), (xs[-1], y)], fill=(160, 190, 255, 70), width=k(2))
    d.line([(xs[0], y), (xs[idx], y)], fill=BLUE + (255,), width=k(3))
    for i, x in enumerate(xs):
        r = k(9) if i == idx else k(6)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(BLUE + (255,)) if i <= idx else (40, 60, 100, 255), outline=(200, 220, 255, 200), width=k(1.5))
    return glow(im, 10, 0.6)
def chapter(idx, dur, extra=()):
    lab = png(text_img([f"PART {idx + 1:02d}"], size=22, fnt=FS, color=(170, 195, 255)))
    tit = png(text_img([CHAPTERS[idx]], size=96, glow_strength=0.55))
    pr = png(progress(idx))
    tw = (tit["w"] - 2 * tit["pad"]) / K
    items = [el(lab, 960 - (lab["w"] / K) / 2, 395, 0.0), el(tit, 960 - tw / 2, 430, 0.08, d=0.45), el(pr, 510, 610, 0.25, "fade")]
    return {"kind": "gfx", "dur": dur, "items": items + list(extra)}

def title(text, size=60, x=160, y=120, t0=0.0, hl=None):
    i = png(text_img([text], size=size, glow_strength=0.5, hl=hl)); return el(i, x, y, t0)
def lower_third(label, text, t0, out=None, w=1100):
    return el(png(card(label, [text], w=w, size=30)), 120, 840, t0, "up", out)
def name_tag(name, sub, t0, out=None):
    i = png(card(None, [name], w=430, size=30, icon=None))
    s2 = png(text_img([sub], size=20, fnt=FR, color=(200, 212, 240)))
    return [el(i, 120, 880, t0, "left", out), el(s2, 140, 950, t0 + 0.15, "left", out)]

def frame_scene(dur, vids, label=None, extras=(), box=(260, 110, 1400, 788)):
    """Screen recording(s) in a browser frame on the blue background. vids: [(src_ss, t0, t1)]"""
    x, y, w, h = box
    bf, p, vp = browser_frame(w, h)
    fr = save((bf, p), f"{G}/frame_{w}x{h}.png")
    items = []
    for ss, t0, t1 in vids:
        items.append({"png": EMPTY, "pad": 0, "x": 0, "y": 0, "t": t0, "out": t1, "anim": "fade", "d": 0.2,
                      "video": {"src": RAW, "ss": ss, "x": x + 1, "y": y + 46, "w": w - 2, "h": h - 2}})
    items.append(el(fr, x, y, 0.0, "fade", d=0.25))
    if label: items.append(label)
    return {"kind": "gfx", "dur": dur, "items": items + list(extras)}

# ------------------------------------------------------------------ shot list (output timeline)
S = []
def face(t0, t1, zoom=1.0, push=0, shift=None, items=()):
    S.append({"kind": "face", "t0": t0, "t1": t1, "zoom": zoom, "push": push, "shift": shift, "items": list(items)})
def gfx(t0, t1, scene):
    scene.update({"t0": t0, "t1": t1}); S.append(scene)

# HOOK
badge = png(card(None, ["$7,000", ], w=300, size=46, num=None))
badge_l = png(text_img(["from 1 client"], size=22, fnt=FR, color=(200, 212, 240)))
face(0.0, 5.80, 1.0, 1, items=[el(badge, 150, 330, 1.05, "left"), el(badge_l, 172, 445, 1.25, "left")])
q_l = png(text_img(["On the call, the client asked:"], size=26, fnt=FR, color=(190, 205, 240)))
q = png(card(None, ["\"Have you ever done", "a project like mine?\""], w=1000, size=58, italic=True))
gfx(5.80, 8.93, {"kind": "gfx", "dur": 3.13, "items": [el(q_l, 470, 330, 0.0), el(q, 460, 390, 0.15, d=0.5)]})
face(8.93, 11.87, 1.10)
r1 = png(card(None, ["How I built this site"], w=1300, size=40, num=1))
r2 = png(card(None, ["How I got it in front of the right clients"], w=1300, size=40, num=2))
r3 = png(card(None, ["What I said to that question"], w=1300, size=40, num=3, hl={"question"}))
gfx(11.87, 20.60, {"kind": "gfx", "dur": 8.73, "items": [title("In this video:", 64, 300, 180), el(r1, 300, 330, 0.7, "left"),
                                                          el(r2, 300, 490, 3.13, "left"), el(r3, 300, 650, 6.05, "left")]})
face(20.60, 23.33, 1.05)
# 01 MISTAKE
face(23.33, 25.70, 1.0, items=name_tag("Fred", "Web designer", 0.15))
gfx(25.70, 28.67, chapter(0, 2.97))
v1 = png(card(None, ["Views"], w=280, size=40, icon=False)); v2 = png(card(None, ["Value"], w=280, size=40, icon=True, hl={"value"}))
face(28.67, 31.53, 1.05, items=[el(v1, 170, 420, 0.25, "left"), el(v2, 1470, 420, 1.55, "right")])
had = [png(card(None, [x], w=640, size=38, icon=True)) for x in ["Millions of views", "Likes", "Comments"]]
nad = [png(card(None, [x], w=640, size=38, icon=False)) for x in ["0 clients", "No system to find them", "No real projects"]]
gfx(31.53, 37.80, {"kind": "gfx", "dur": 6.27, "items": [
    title("What I had", 48, 230, 210), el(had[0], 230, 320, 0.1, "left"), el(had[1], 230, 460, 1.65, "left"), el(had[2], 230, 600, 2.15, "left"),
    title("What I didn't", 48, 1050, 210, 2.6), el(nad[0], 1050, 320, 3.25, "right"), el(nad[1], 1050, 460, 4.2, "right"), el(nad[2], 1050, 600, 5.3, "right")]})
face(37.80, 40.07, 1.0)
face(40.07, 46.20, 1.05, 1)
# 02 CLICK
gfx(46.20, 48.40, chapter(1, 2.20))
face(48.40, 49.80, 1.0)
face(49.80, 52.47, 1.10)
x1 = png(card(None, ["The prettiest design"], w=700, size=36, icon=False))
x2 = png(card(None, ["The lowest price"], w=700, size=36, icon=False))
x3 = png(card(None, ["\"This guy gets my business.\""], w=700, size=36, icon=True, hl={"business"}))
x4 = png(text_img(["Without them having to explain a thing."], size=24, fnt=FR, color=(200, 212, 240)))
face(52.47, 60.53, 1.0, shift=-0.2, items=[title("What makes a client say yes?", 40, 1060, 250), el(x1, 1060, 350, 0.1, "right"),
     el(x2, 1060, 480, 1.45, "right"), el(x3, 1060, 610, 3.6, "right", d=0.5), el(x4, 1080, 730, 6.0, "fade")])
face(60.53, 63.27, 1.05)
face(63.27, 68.57, 1.0, 1)
# 03 CHOICE
con = png(chip("Construction", size=34))
gfx(68.57, 70.93, chapter(2, 2.36, [el(con, 870, 700, 1.0, "up")]))
def reason(n, head, sub, state):
    c = card(None, [head, sub] if state else [" ", " "], w=480, size=32, num=n, hl=None)
    return png(c)
R = [(1, "Real money", "1 project pays for the site"), (2, "No time for tech", "clients judge past projects"), (3, "Premium work", "means premium prices")]
full = [png(card(None, [h, s], w=500, size=32, num=n)) for n, h, s in R]
empty = [png(card(None, [" ", " "], w=500, size=32, num=n)) for n, h, s in R]
gx = [180, 710, 1240]
gfx(70.93, 80.83, {"kind": "gfx", "dur": 9.90, "items": [title("Why construction?", 60, 180, 200)] +
    [el(empty[i], gx[i], 400, 0.0, "fade") for i in range(3)] + [el(full[0], gx[0], 400, 0.15, "up"), el(full[1], gx[1], 400, 4.10, "up")]})
face(80.83, 83.77, 1.10)
gfx(83.77, 86.80, {"kind": "gfx", "dur": 3.03, "items": [title("Why construction?", 60, 180, 200, 0.0)] +
    [el(full[0], gx[0], 400, 0.0, "fade", d=0.01), el(full[1], gx[1], 400, 0.0, "fade", d=0.01), el(empty[2], gx[2], 400, 0.0, "fade", d=0.01),
     el(full[2], gx[2], 400, 0.15, "up")]})
face(86.80, 91.87, 1.0)
face(91.87, 97.57, 1.0, 0, items=[lower_third("Takeaway", "Not \"a portfolio\". The one a construction owner wants to open.", 1.2, w=1250)])
# 04 BUILD (voice-over; raw shows screen recordings)
gfx(97.57, 99.13, chapter(3, 1.56))
gfx(99.13, 106.80, frame_scene(7.67, [(126.6, 0.0, 7.67)]))
nodes = ["What do you do?", "Show me.", "What's in it for me?", "Shall we talk?"]
np_ = [png(chip(n, size=30)) for n in nodes]; arr = png(arrow(70))
path_items = [title("Not pages. A path.", 64, 160, 220, 0.1)]
xs = [160, 560, 900, 1380]
for i, n in enumerate(np_):
    path_items.append(el(n, xs[i], 520, [3.3, 4.7, 6.6, 8.1][i], "up"))
    if i: path_items.append(el(arr, xs[i] - 95, 537, [3.3, 4.7, 6.6, 8.1][i] - 0.15, "left"))
path_items.append(el(png(text_img(["Each section answers the client's next question, before he asks it."], size=26, fnt=FR, color=(200, 212, 240))), 160, 660, 6.0, "fade"))
gfx(106.80, 116.07, {"kind": "gfx", "dur": 9.27, "items": path_items})
add = png(card(None, ["What can I add?"], w=700, size=44, icon=False)); rem = png(card(None, ["What can I remove?"], w=700, size=44, icon=True, hl={"remove?"}))
gfx(116.07, 121.50, {"kind": "gfx", "dur": 5.43, "items": [title("Instead of asking…", 48, 610, 250, 0.1), el(add, 610, 360, 2.4), el(rem, 610, 520, 3.3)]})
less = ["Fewer colors", "Less decoration", "More space", "More room for the visuals"]
lp = [png(chip(x, size=34)) for x in less]
gfx(121.50, 126.50, {"kind": "gfx", "dur": 5.0, "items": [title("Less, but better.", 60, 160, 220)] +
    [el(lp[i], [160, 520, 960, 160][i], [430, 430, 430, 560][i], [0.1, 1.0, 1.9, 2.6][i]) for i in range(4)]})
gfx(126.50, 131.90, frame_scene(5.40, [(146.2, 0.0, 5.40)], box=(360, 60, 1200, 675), extras=[lower_third("Takeaway", "If your work is good, you don't need to shout.", 0.9, w=1000)]))
# 05 DETAILS
gfx(131.90, 133.60, chapter(4, 1.70))
gfx(133.60, 141.40, frame_scene(7.80, [(158.5, 0.0, 7.80)], label=el(png(chip("Mobile-first", size=30)), 260, 30, 0.4, "left")))
gfx(141.40, 147.23, frame_scene(5.83, [(172.0, 0.0, 5.83)], label=el(png(chip("Built in Framer", size=30)), 260, 30, 0.2, "left")))
gfx(147.23, 153.00, frame_scene(5.77, [(186.5, 0.0, 5.77)], extras=[el(png(chip("3 px", size=30)), 260, 30, 2.3, "left"),
                                                                    el(png(chip("a hair too fast", size=30)), 400, 30, 3.8, "left")]))
s1 = png(text_img(["Little details nobody notices…"], size=64, glow_strength=0.4))
s2 = png(text_img(["…add up to a feeling everyone notices."], size=64, glow_strength=0.55, hl={"feeling"}))
gfx(153.00, 159.17, {"kind": "gfx", "dur": 6.17, "items": [el(s1, 220, 380, 0.15), el(s2, 220, 520, 3.65)]})
# REVEAL (silent, site walkthrough cut to rhythm)
rv = [(162.0, 0.0, 2.8), (168.0, 2.8, 5.8), (173.0, 5.8, 8.8), (178.5, 8.8, 11.6), (186.5, 11.6, 14.6), (194.0, 14.6, 18.0)]
gfx(159.17, 177.17, frame_scene(18.0, [(ss + 0.0, a, b) for ss, a, b in rv], box=(180, 70, 1560, 878)))
# 06 PIVOT
gfx(177.17, 178.60, chapter(5, 1.43))
face(178.60, 183.47, 1.0)
face(183.47, 189.97, 1.05, 1, items=[lower_third("Takeaway", "A portfolio is worthless until it brings you a client.", 2.8, w=1100)])
# 07 OUTREACH
gfx(189.97, 191.40, chapter(6, 1.43))
c1 = png(card(None, ["Construction companies"], w=520, size=34, icon=True)); c2 = png(card(None, ["Nobody else."], w=360, size=34, icon=None))
face(191.40, 197.90, 1.0, items=[el(c1, 1300, 380, 4.4, "right"), el(c2, 1300, 520, 5.5, "right")])
face(197.90, 203.30, 1.10, items=[lower_third("The most important advice", "Have a clear persona.", 3.6, w=700)])
# persona graphic
dots = Image.new("RGBA", (k(1100), k(420))); dd = ImageDraw.Draw(dots)
for r_ in range(5):
    for c_ in range(14):
        x_, y_ = k(40 + c_ * 78), k(40 + r_ * 82); dd.ellipse((x_ - k(14), y_ - k(14), x_ + k(14), y_ + k(14)), fill=(70, 95, 150, 255))
dots_p = png(glow(dots, 6, 0.3))
focus = png(card("Your persona", ["Construction business owner"], w=620, size=38, icon=True, hl={"construction"}))
gfx(203.30, 210.80, {"kind": "gfx", "dur": 7.5, "items": [title("Talk to everyone…", 56, 160, 140), el(dots_p, 410, 260, 0.2, "fade"),
    el(png(text_img(["…and nobody feels you're talking to them."], size=34, fnt=FS, color=(210, 220, 245))), 160, 720, 2.0, "fade"),
    el(focus, 650, 380, 4.5, "up", d=0.5)]})
fl = [png(chip(x, size=32)) for x in ["Outreach", "1 reply", "Discovery call"]]; ok = png(card(None, ["My system worked."], w=520, size=36, icon=True))
fx = [200, 680, 1110]
gfx(210.80, 215.10, {"kind": "gfx", "dur": 4.3, "items": [el(fl[0], fx[0], 440, 0.05), el(arr, 410, 457, 0.4, "left"), el(fl[1], fx[1], 440, 0.6),
    el(arr, 870, 457, 1.6, "left"), el(fl[2], fx[2], 440, 1.75), el(ok, 700, 600, 3.4)]})
face(215.10, 218.77, 1.05, items=[lower_third("Outreach system", "Find it in the first pinned comment", 0.8, w=800)])
# 08 LESSON
gfx(218.77, 220.20, chapter(7, 1.43))
face(220.20, 225.77, 1.0, 1)
face(225.77, 227.17, 1.10, items=[el(png(chip("Same designer.", size=34)), 1380, 420, 0.1, "right")])
e1 = png(card(None, ["Same designer"], w=420, size=40)); e2 = png(card(None, ["Different perception"], w=520, size=40, hl={"perception"}))
pl = png(text_img(["+"], size=70)); eq = png(text_img(["="], size=70)); money = png(text_img(["$7,000"], size=110, glow_strength=0.7))
gfx(227.17, 234.63, {"kind": "gfx", "dur": 7.46, "items": [el(e1, 140, 470, 0.1), el(pl, 600, 455, 2.0, "fade"), el(e2, 680, 470, 2.3),
    el(eq, 1240, 455, 5.9, "fade"), el(money, 1330, 430, 6.1, "up", d=0.5)]})
# 09 OFFER
gfx(234.63, 236.00, chapter(8, 1.37))
face(236.00, 244.10, 1.0)
w1 = png(card(None, ["Your work"], w=560, size=36, icon=True)); w2 = png(card(None, ["Your outreach"], w=560, size=36, icon=True))
w3 = png(card(None, ["Not simple. Not magic."], w=560, size=36, icon=False))
gfx(244.10, 252.13, {"kind": "gfx", "dur": 8.03, "items": [title("Your result depends on:", 60, 680, 220), el(w1, 680, 360, 0.9, "left"),
     el(w2, 680, 490, 2.0, "left"), el(w3, 680, 640, 5.2, "left")]})
face(252.13, 257.47, 1.05, 1)
gfx(257.47, 265.17, frame_scene(7.70, [(363.3, 0.0, 7.70)], label=el(png(card(None, ["Framer portfolio template"], w=560, size=32, num=1)), 360, 840, 0.3, "up"), box=(360, 60, 1200, 675)))
gfx(265.17, 270.27, frame_scene(5.10, [(371.9, 0.0, 5.10)], label=el(png(card(None, ["First Client Kit"], w=440, size=32, num=2)), 360, 840, 0.1, "up"), box=(360, 60, 1200, 675)))
gfx(270.27, 276.13, frame_scene(5.86, [(375.5, 0.0, 5.86)], box=(360, 60, 1200, 675), extras=[lower_third("Takeaway", "The portfolio alone wouldn't have been enough.", 1.0, w=980)]))
pin = png(card(None, ["Everything is in the first pinned comment", "and in the description."], w=1100, size=44))
gfx(276.13, 278.50, {"kind": "gfx", "dur": 2.37, "items": [el(pin, 410, 420, 0.1)]})
# END
face(278.50, 288.63, 1.0, items=[el(png(chip("New channel · Subscribe", size=30)), 1350, 300, 4.0, "right", out=9.9)])
qq = png(card("Tell me in the comments", ["Which industry would you pick?"], w=640, size=36))
face(288.63, 293.20, 1.05, items=[el(qq, 1180, 380, 0.15, "right")])
face(293.20, TOTAL, 1.0, items=name_tag("Fred", "Instagram · link in my profile", 0.3))

# sanity: contiguous cover
S.sort(key=lambda s: s["t0"])
for a_, b_ in zip(S, S[1:]):
    assert abs(a_["t1"] - b_["t0"]) < 1e-6, (a_["t0"], a_["t1"], b_["t0"])
assert abs(S[-1]["t1"] - TOTAL) < 1e-6, (S[-1]["t1"], TOTAL)
json.dump({"total": TOTAL, "shots": S}, open(f"{E}/shots.json", "w"), indent=1)
face_s = sum(s["t1"] - s["t0"] for s in S if s["kind"] == "face")
print(f"shots {len(S)} | total {TOTAL:.2f}s | face {face_s / TOTAL * 100:.0f}% | graphics/screens {(1 - face_s / TOTAL) * 100:.0f}%")
