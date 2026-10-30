"""Graphics + sound layer for the cut: ASS text, PNG overlays, synthesized SFX, final mix/render."""
import json, subprocess, sys, os
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
from PIL import Image, ImageDraw, ImageFont, ImageFilter

work, fonts = sys.argv[1], sys.argv[2]
OUT = sys.argv[3]
W = json.load(open(f"{work}/words.json"))
order = list(W.keys())
off, t = {}, 0.0
for cid in order:
    off[cid] = t; t += W[cid]["dur"]
TOTAL = t


def T(cid, word=None, k=0):
    """Output time of clip start, or of the k-th occurrence of a word inside the clip."""
    if word is None: return off[cid]
    hits = [tt for w, tt in W[cid]["words"] if w.lower().strip(",.:") == word]
    return off[cid] + hits[k]

def END(cid): return off[cid] + W[cid]["dur"]

# ---------------------------------------------------------------- ASS text
def ts(x):
    x = max(0, x); h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"

SOFT = r"\bord2\3c&H000000&\3a&HD0&\shad0\blur6"
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 2", "",
       "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Title,Instrument Serif,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,-1,0,1,0,0,8,40,40,0,1",
       "Style: Note,Coming Soon,42,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,8,40,40,0,1",
       "Style: Tag,Homemade Apple,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1",
       "Style: Cap,Instrument Serif,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1",
       "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
typing = []  # times of typewriter keystrokes (for tick SFX)

def ev(t0, t1, style, text, layer=0):
    ass.append(f"Dialogue: {layer},{ts(t0)},{ts(t1)},{style},,0,0,0,,{text}")

def typewriter(t0, t1, style, text, pos, cps=26, extra=""):
    """Letter-by-letter reveal; hidden remainder keeps the final (centred) layout fixed."""
    stops = [i for i in range(1, len(text) + 1) if not text[i - 1].isspace()]
    starts = [t0 + k / cps for k in range(len(stops))]
    for k, i in enumerate(stops):
        a = starts[k]; b = starts[k + 1] if k + 1 < len(stops) else t1
        shown = text[:i].replace("\n", r"\N"); hidden = text[i:].replace("\n", r"\N")
        txt = f"{{\\pos({pos[0]},{pos[1]}){SOFT}{extra}}}{shown}" + (f"{{\\alpha&HFF&}}{hidden}" if hidden else "")
        ev(a, b, style, txt)
        typing.append(a)


def note(t0, t1, text, pos, size=42, rot=0):
    ev(t0, t1, "Note", f"{{\\pos({pos[0]},{pos[1]}){SOFT}\\fs{size}\\frz{rot}}}{text}")

# Section titles (top centre, typewriter, persist for the section)
TITLE_Y = 62
typewriter(0.0, T("c4"), "Title", "Millions of views.\nZero clients.", (540, 52), cps=30, extra=r"\fs76")
ev(1.6, T("c4"), "Tag", f"{{\\pos(235,44){SOFT}\\frz16}}episode 1")
typewriter(T("c4"), T("c9"), "Title", "Designer vs Developer", (540, TITLE_Y))
note(T("c4", "designer") + 0.2, T("c7"), "the videos you might know me from", (540, 146))
note(T("c7") + 0.25, T("c9"), "so I thought... this is it. clients will come.", (540, 146))
typewriter(T("c10"), T("c13"), "Title", "The problem:", (540, TITLE_Y))
note(T("c11", "not"), T("c13"), "they came for the joke... not for the designer", (540, 146))
typewriter(T("c13"), T("c19"), "Title", "Views ≠ bills", (540, TITLE_Y))
note(T("c16", "real"), T("c19"), "goal: get 1 real client", (540, 146))
note(T("c17", "dollars"), T("c19"), "1 project = $7,000", (540, 200))
typewriter(T("c19"), T("c21"), "Title", "But first...", (540, TITLE_Y))
typewriter(T("c21"), T("c24"), "Title", "Coming soon:", (540, TITLE_Y))
note(T("c21", "did"), T("c24"), "what didn't work", (540, 146))
note(T("c22", "what"), T("c24"), "what finally did", (540, 200))
note(T("c23"), T("c24"), "mistakes included", (230, 232), size=40, rot=14)

# Word-by-word captions: left of the face at mouth height
for cid in order:
    ws = W[cid]["words"]
    for i, (w, tt) in enumerate(ws):
        a = off[cid] + tt; b = off[cid] + ws[i + 1][1] if i + 1 < len(ws) else END(cid)
        ev(a, b, "Cap", f"{{\\pos(150,690){SOFT}}}{w}", layer=1)
open(f"{work}/text.ass", "w").write("\n".join(ass) + "\n")

# ---------------------------------------------------------------- PNG overlays
F = lambda name, size: ImageFont.truetype(name, size)
SERIF = f"{fonts}/InstrumentSerif-Regular.ttf"; HAND = f"{fonts}/ComingSoon-Regular.ttf"
def find_font(stem):
    out = subprocess.run(["fc-match", "-f", "%{file}", stem], capture_output=True, text=True).stdout
    return out
INTER = find_font("Inter:style=SemiBold"); INTER_R = find_font("Inter:style=Regular")
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

def emoji(ch, h):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (160, 160)); ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox()); return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)

def soft_shadow(im, r=8, a=90):
    sh = Image.new("RGBA", (im.width + 4 * r, im.height + 4 * r))
    alpha = Image.new("L", sh.size); alpha.paste(im.getchannel("A").point(lambda v: v * a // 255), (2 * r, 2 * r + 3))
    sh.putalpha(alpha.filter(ImageFilter.GaussianBlur(r))); sh.paste(im, (2 * r, 2 * r), im); return sh

def hand_line(text, emo, size=40):
    f = F(HAND, size); w = int(f.getlength(text)); e = emoji(emo, int(size * 1.0))
    im = Image.new("RGBA", (w + e.width + 14, int(size * 1.6)))
    ImageDraw.Draw(im).text((0, 0), text, font=f, fill="white"); im.paste(e, (w + 12, int(size * 0.12)), e)
    return soft_shadow(im, 6, 110)

def rrect(size, r, fill):
    im = Image.new("RGBA", size); ImageDraw.Draw(im).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=fill); return im

overlays = []  # (png, x, y, t0, t1)
def add(name, im, x, y, t0, t1, anchor="tl"):
    p = f"{work}/ov_{name}.png"; im.save(p)
    if anchor == "tc": x = x - im.width // 2
    overlays.append((p, int(x), int(y), t0, t1))

# aside: "they didn't. not one." (line from the script that wasn't filmed)
add("aside1", hand_line("*they didn't. not one.*", "\U0001F605", 42), 540, 60, T("c9"), T("c10"), "tc")
add("aside2", hand_line("I failed. a lot.", "\U0001F605", 36), 540, 132, T("c20", "failed"), T("c21"), "tc")

# proof card (placeholder for the real designer-vs-developer reel)
card = rrect((330, 470), 22, (250, 248, 244, 255)); d = ImageDraw.Draw(card)
thumb = Image.new("RGBA", (306, 360)); td = ImageDraw.Draw(thumb)
for yy in range(360):
    c = int(28 + 30 * yy / 360); td.line([(0, yy), (306, yy)], fill=(c + 8, c + 4, c, 255))
mask = rrect((306, 360), 16, (0, 0, 0, 255)).getchannel("A"); card.paste(thumb, (12, 12), mask)
d.text((165, 120), "designer", font=F(SERIF, 54), fill="white", anchor="mm")
d.text((165, 178), "vs", font=F(HAND, 30), fill=(230, 220, 205), anchor="mm")
d.text((165, 236), "developer", font=F(SERIF, 54), fill="white", anchor="mm")
d.polygon([(30, 336), (30, 356), (47, 346)], fill="white")
d.text((54, 346), "Reel", font=F(INTER, 20), fill="white", anchor="lm")
d.text((24, 400), "designer vs developer", font=F(INTER, 22), fill=(25, 25, 25), anchor="lm")
d.text((24, 432), "Fred · web designer", font=F(INTER_R, 18), fill=(120, 120, 120), anchor="lm")
add("card", soft_shadow(card.rotate(-3, expand=True, resample=Image.BICUBIC), 12, 120), 40, 1080,
    T("c4", "designer"), T("c7") + 0.6)

badge = rrect((300, 96), 20, (250, 248, 244, 255)); bd = ImageDraw.Draw(badge)
bd.text((24, 30), "views", font=F(INTER_R, 20), fill=(120, 120, 120), anchor="lm")
bd.text((24, 64), "≈ 3,000,000", font=F(INTER, 30), fill=(20, 20, 20), anchor="lm")
b2 = Image.new("RGBA", (360, 150)); b2.paste(badge, (0, 40), badge); e = emoji("\U0001F92F", 64); b2.paste(e, (262, 0), e)
add("badge", soft_shadow(b2, 10, 110), 300, 1500, T("c6", "million"), T("c7") + 0.6)

# end profile card (avatar from his own footage)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "3", "-i", f"{work}/rawB.mp4", "-frames:v", "1",
                "-vf", "crop=300:300:210:180,scale=120:120", f"{work}/avatar.png"], check=True)
pc = rrect((620, 132), 34, (18, 18, 18, 205)); pd = ImageDraw.Draw(pc)
av = Image.open(f"{work}/avatar.png").convert("RGBA").resize((88, 88), Image.LANCZOS)
m = Image.new("L", (88, 88)); ImageDraw.Draw(m).ellipse((0, 0, 87, 87), fill=255); pc.paste(av, (22, 22), m)
pd.text((128, 48), "Fred", font=F(INTER, 30), fill="white", anchor="lm")
pd.text((128, 88), "web designer · episode 2 soon", font=F(INTER_R, 21), fill=(200, 200, 200), anchor="lm")
fb = rrect((126, 56), 28, (255, 255, 255, 255)); ImageDraw.Draw(fb).text((63, 28), "Follow", font=F(INTER, 22), fill=(10, 10, 10), anchor="mm")
pc.paste(fb, (474, 38), fb)
add("profile", soft_shadow(pc, 10, 100), 540, 92, T("c24"), TOTAL + 1, "tc")
add("stick", hand_line("stick around...", "✨", 34), 540, 34, T("c24"), TOTAL + 1, "tc")

# ---------------------------------------------------------------- SFX (synthesized to match the reference palette)
SR = 48000
rng = np.random.default_rng(7)
def db(x): return 10 ** (x / 20)
def norm_peak(x, peak_db): return x / (np.abs(x).max() + 1e-9) * db(peak_db)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), x)

def sfx_boom():
    n = int(1.0 * SR); tt = np.arange(n) / SR
    f = 110 * (42 / 110) ** (tt / 1.0); ph = 2 * np.pi * np.cumsum(f) / SR
    hit = np.sin(ph) * np.exp(-tt / 0.32) * np.minimum(1, tt / 0.015)
    out = []
    for ch in range(2):
        nz = rng.standard_normal(n); env = np.exp(-((tt - 0.22) / 0.16) ** 2)
        wh = sum(bp(nz, lo, lo * 2.2) * np.exp(-((tt - c) / 0.12) ** 2) for lo, c in [(400, .10), (900, .2), (1800, .28), (700, .4)])
        out.append(hit * 1.0 + wh * 0.6 * (1 + 0.1 * ch))
    return norm_peak(np.stack(out, 1), -10)

def sfx_pop():
    n = int(0.18 * SR); tt = np.arange(n) / SR
    f = 600 + 120 * np.minimum(1, tt / 0.1); ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.sin(np.pi * np.minimum(tt / 0.2, 1)) ** 2 * np.exp(-np.maximum(0, tt - 0.1) / 0.03)
    x = np.sin(ph) * env + 0.25 * np.sin(2 * ph) * env
    return norm_peak(np.stack([x, x * 0.92], 1), -30)

def sfx_ding():
    n = int(0.4 * SR); tt = np.arange(n) / SR; f0 = 2400
    x = sum(a * np.sin(2 * np.pi * f0 * r * tt) * np.exp(-tt / d) for r, a, d in [(1, 1, .14), (2.0, .3, .08), (2.76, .2, .06), (5.4, .07, .03)])
    x *= np.minimum(1, tt / 0.002)
    return norm_peak(np.stack([x, np.roll(x, 24)], 1), -21)

def sfx_swish():
    n = int(0.2 * SR); tt = np.arange(n) / SR; env = np.sin(np.pi * tt / 0.2) ** 2
    nz = rng.standard_normal(n); x = bp(nz, 2500, 11000) * env; pan = tt / 0.2
    return norm_peak(np.stack([x * (1 - 0.6 * pan), x * (0.4 + 0.6 * pan)], 1), -24)

def sfx_tick():
    n = int(0.012 * SR); tt = np.arange(n) / SR; x = bp(rng.standard_normal(n), 2000, 9000) * np.exp(-tt / 0.002)
    return norm_peak(np.stack([x, x], 1), -50)

LIB = {"boom": sfx_boom(), "pop": sfx_pop(), "ding": sfx_ding(), "swish": sfx_swish(), "tick": sfx_tick()}
PRE = {"pop": 0.09, "ding": 0.0, "swish": 0.05, "boom": 0.0, "tick": 0.0}  # align peak to the visual frame
cues = [("boom", 0.0)]
cues += [("tick", x) for x in typing]
cues += [("pop", T(c)) for c in ("c4", "c10", "c13", "c19", "c21")]
cues += [("pop", T("c4", "designer")), ("pop", T("c24"))]
cues += [("ding", t_) for t_ in (T("c6", "million"), T("c9"), T("c20", "failed"), T("c16", "real"),
                                  T("c17", "dollars"), T("c21", "did"), T("c22", "what"), T("c23"))]
for cid, c in W.items():
    if c.get("zoom", {}).get("kind") == "snap": cues.append(("swish", off[cid] + c["zoom"]["t"]))
mix = np.zeros((int((TOTAL + 1.5) * SR), 2))
for name, at in cues:
    s = LIB[name]; i = max(0, int((at - PRE[name]) * SR)); mix[i:i + len(s)] += s[:len(mix) - i]
wavfile.write(f"{work}/sfx.wav", SR, mix[:int(TOTAL * SR)].astype(np.float32))
json.dump({"cues": sorted(cues, key=lambda c: c[1]), "overlays": overlays, "total": TOTAL}, open(f"{work}/plan.json", "w"), indent=1)

# ---------------------------------------------------------------- final render
inputs = ["-i", f"{work}/cut.mov", "-i", f"{work}/sfx.wav"]
for p, *_ in overlays: inputs += ["-loop", "1", "-i", p]
chain = "[0:v]"; fc = []
for k, (p, x, y, a, b) in enumerate(overlays):
    lbl = f"[v{k}]"; fc.append(f"{chain}[{k+2}:v]overlay={x}:{y}:enable='between(t,{a:.3f},{b:.3f})':shortest=1{lbl}"); chain = lbl
fc.append(f"{chain}ass={work}/text.ass:fontsdir={fonts}[vout]")
fc.append("[0:a]highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,"
          "loudnorm=I=-14.5:TP=-1.5:LRA=7,aresample=48000,pan=stereo|c0=c0|c1=c0[voice]")
fc.append("[voice][1:a]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89:level=false[aout]")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc),
                "-map", "[vout]", "-map", "[aout]", "-t", f"{TOTAL:.3f}", "-c:v", "libx264", "-preset", "slow",
                "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", OUT], check=True)
print("total", round(TOTAL, 2), "overlays", len(overlays), "cues", len(cues))
