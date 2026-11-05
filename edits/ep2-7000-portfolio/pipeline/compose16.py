"""Episode 2 (YouTube 16:9): ASS text, PNG asides, synthesized SFX, final mix/render at 4K."""
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

SOFT = r"\bord3\3c&H000000&\3a&HA0&\shad0\blur10"
ass = ["[Script Info]", "ScriptType: v4.00+", "ScaledBorderAndShadow: yes", "PlayResX: 1920", "PlayResY: 1080", "WrapStyle: 2", "",
       "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Title,Instrument Serif,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,-1,0,1,0,0,8,40,40,0,1",
       "Style: Note,Coming Soon,32,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,8,40,40,0,1",
       "Style: Tag,Homemade Apple,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1",
       "Style: Cap,Instrument Serif,50,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1",
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


def note(t0, t1, text, pos, size=32, rot=0):
    ev(t0, t1, "Note", f"{{\\pos({pos[0]},{pos[1]}){SOFT}\\fs{size}\\frz{rot}}}{text}")

# Section titles: right-hand column over the shelves (the face is centred), typewriter, persist per section
CX, TY, NY = 1560, 250, 340
typewriter(0.0, T("k4"), "Title", "The $7,000 portfolio", (CX, TY), cps=28)
ev(1.4, T("k4"), "Tag", f"{{\\pos({CX - 190},{TY - 22}){SOFT}\\frz14}}episode 2")
note(T("k3"), T("k4"), "...then came the call", (CX, NY))
typewriter(T("k4"), T("k7"), "Title", "The question:", (CX, TY))
note(T("k4") + 0.1, T("k6", "no"), "\"have you ever done\\Na project like mine?\"", (CX, NY))
typewriter(T("k7"), T("k10"), "Title", "In this video:", (CX, TY))
note(T("k7", "built"), T("k10"), "how I built this site", (CX, NY))
note(T("k8", "front"), T("k10"), "how it reached the right clients", (CX, NY + 50))
note(T("k9", "said"), T("k10"), "what I said to that question", (CX, NY + 100))
typewriter(T("k10"), TOTAL + 1, "Title", "The answer that\nclosed the deal", (CX, TY - 30), cps=30)

# Word-by-word captions: left of the face at mouth height (face centred at x=960); off unless CAPTIONS=1
for cid in (order if os.environ.get("CAPTIONS") == "1" else []):
    ws = W[cid]["words"]
    for i, (w, tt) in enumerate(ws):
        a = off[cid] + tt; b = off[cid] + ws[i + 1][1] if i + 1 < len(ws) else END(cid)
        ev(a, b, "Cap", f"{{\\pos(150,690){SOFT}}}{w}", layer=1)
# on-screen text (titles, notes, tag) is off unless TEXT=1
if os.environ.get("TEXT") != "1": ass = [l for l in ass if not l.startswith("Dialogue:")]
open(f"{work}/text.ass", "w").write("\n".join(ass) + "\n")

# ---------------------------------------------------------------- PNG overlays
K = 2  # overlays are drawn natively at 4K (2160x3840); layout coordinates stay in 1080x1920 units
k = lambda v: int(round(v * K))
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
    im = Image.new("RGBA", (w + e.width + k(14), int(size * 1.6)))
    ImageDraw.Draw(im).text((0, 0), text, font=f, fill="white"); im.paste(e, (w + k(12), int(size * 0.12)), e)
    return soft_shadow(im, k(6), 110)

def rrect(size, r, fill):
    im = Image.new("RGBA", size); ImageDraw.Draw(im).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=fill); return im

overlays = []  # (png, x, y, t0, t1)
def add(name, im, x, y, t0, t1, anchor="tl"):
    p = f"{work}/ov_{name}.png"; im.save(p)
    x, y = x * K, y * K  # layout units are 1920x1080
    if anchor == "tc": x = x - im.width // 2
    overlays.append((p, int(x), int(y), t0, t1))

# aside on the reveal ("no.")
add("aside1", hand_line("*my honest answer: no.*", "\U0001F605", k(34)), 1560, 330, T("k6", "no"), T("k7"), "tc")

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
cues += [("pop", T(c)) for c in ("k4", "k7", "k10")]
cues += [("ding", t_) for t_ in (T("k6", "no"), T("k7", "built"), T("k8", "front"), T("k9", "said"))]
for cid, c in W.items():
    if c.get("zoom", {}).get("kind") == "snap": cues.append(("swish", off[cid] + c["zoom"]["t"]))
if os.environ.get("SFX") != "1": cues = []  # voice only unless SFX=1
mix = np.zeros((int((TOTAL + 1.5) * SR), 2))
for name, at in cues:
    s = LIB[name]; i = max(0, int((at - PRE[name]) * SR)); mix[i:i + len(s)] += s[:len(mix) - i]
wavfile.write(f"{work}/sfx.wav", SR, mix[:int(TOTAL * SR)].astype(np.float32))
json.dump({"cues": sorted(cues, key=lambda c: c[1]), "overlays": overlays, "total": TOTAL}, open(f"{work}/plan.json", "w"), indent=1)

# ---------------------------------------------------------------- final render
if os.environ.get("TEXT") != "1": overlays = []
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
                "-crf", "17", "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "5.2",
                "-x264-params", "aq-mode=3", "-tag:v", "avc1", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", OUT], check=True)
print("total", round(TOTAL, 2), "overlays", len(overlays), "cues", len(cues))
