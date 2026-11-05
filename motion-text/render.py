#!/usr/bin/env python3
"""Render motion text in the house style (CLAUDE.md, motion-text/style.json).

Usage:
    python3 motion-text/render.py TIMELINE.json OUT.mp4 [--beat]

TIMELINE.json:
    {
      "size": [1920, 1080], "fps": 30, "bpm": 155,
      "audio": "optional/path/to/music.mp3",
      "shots": [
        {"text": "Hi", "move": "punch", "beats": 1},
        {"text": "How are you?", "move": "build", "beats": 3, "exit": "wipe"},
        {"text": "typography", "move": "invert", "variant": "skew", "beats": 1.5}
      ]
    }

Each shot lasts "beats" (at "bpm") or "sec" seconds. Moves: punch, cut,
build, karaoke, letters, wipe, invert (variant: track | skew).
Exits: cut (default), slide, wipe. Optional per shot: "scale" (size
multiplier), "y" (vertical offset as a fraction of frame height),
"invert": true (put any move on the white card), and for build:
"wordAt" (beat at which each word appears, e.g. [0, 2]) and
"shiftSeconds" (how long the line takes to slide over for a new word).
Timeline option "pad": "invert" makes the lead-in and tail white.
--beat adds a simple kick/hat track at the timeline's bpm so the sync
can be judged when there is no music yet.
"""
import argparse
import json
import math
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
STYLE = json.loads((ROOT / "motion-text" / "style.json").read_text())
FONT_FILE = str(ROOT / STYLE["font"]["file"])
C = STYLE["colors"]
M = STYLE["motion"]
L = STYLE["layout"]


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_rgb(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(round(lerp(x, y, t)) for x, y in zip(a, b))


def clamp01(x):
    return max(0.0, min(1.0, x))


def ease_out(x):
    return 1 - (1 - clamp01(x)) ** 3


def ease_in(x):
    return clamp01(x) ** 2


_fonts = {}


def font(size):
    key = round(size * 2) / 2
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FONT_FILE, key)
    return _fonts[key]


CAP_RATIO = 0.6455  # Grandstander cap height / em


def layout(text, size, tracking_em=0.0):
    """Return glyph list [(char, x, word_index)] and total width."""
    f = font(size)
    glyphs, word = [], 0
    track = tracking_em * size
    for i, ch in enumerate(text):
        if ch == " ":
            word += 1
            continue
        x = f.getlength(text[:i]) + i * track
        glyphs.append((ch, x, word))
    width = f.getlength(text) + max(0, len(text) - 1) * track
    return glyphs, width


def draw_glyph(layer, ch, x, baseline, size, color, alpha=255, skew=0.0):
    f = font(size)
    if abs(skew) < 1e-3:
        ImageDraw.Draw(layer).text((x, baseline), ch, font=f, fill=color + (alpha,), anchor="ls")
        return
    # Draw on a tile, shear around the baseline, paste.
    asc, desc = f.getmetrics()
    w = int(f.getlength(ch) + abs(skew) * asc + size * 0.2) + 4
    h = asc + desc + 4
    tile = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(tile).text((2, asc + 2), ch, font=f, fill=color + (alpha,), anchor="ls")
    by = asc + 2
    tile = tile.transform(tile.size, Image.AFFINE, (1, skew, -skew * by, 0, 1, 0), resample=Image.BICUBIC)
    layer.alpha_composite(tile, (int(round(x)) - 2, int(round(baseline)) - by))


def clip_x(layer, x0, x1):
    """Keep only the columns between x0 and x1 of the layer."""
    a = layer.getchannel("A")
    d = ImageDraw.Draw(a)
    W, H = layer.size
    if x0 > 0:
        d.rectangle([0, 0, int(x0), H], fill=0)
    if x1 < W:
        d.rectangle([int(x1), 0, W, H], fill=0)
    layer.putalpha(a)


def shot_duration(shot, bpm):
    if "sec" in shot:
        return float(shot["sec"])
    return float(shot.get("beats", 1)) * 60.0 / bpm


def render_frame(shot, t, d, W, H):
    move = shot.get("move", "punch")
    variant = shot.get("variant")
    exit_kind = shot.get("exit", "cut")
    text = shot["text"].replace("'", "\u2019")  # curly apostrophe, as in the reference
    invert = move == "invert" or bool(shot.get("invert"))

    bg = rgb(C["invertBackground"] if invert else C["background"])
    img = Image.new("RGBA", (W, H), bg + (255,))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    base = L["fontSizePercentOfFrameHeight"] / 100 * H * shot.get("scale", 1.0)
    _, w0 = layout(text, base)
    max_w = L["maxTextWidthPercentOfFrameWidth"] / 100 * W
    if move == "invert" and variant == "track":
        _, w_tracked = layout(text, base, M["trackingEndEm"])
        if w_tracked > max_w:
            base *= max_w / w_tracked
    elif w0 > max_w:
        base *= max_w / w0

    # Scale: punch on entry, slow shrink while held.
    punch = {"punch": M["punchScale"], "cut": M["cutPunchScale"], "build": M["punchScale"],
             "karaoke": 0.15, "invert": M["invertPunchScale"]}.get(move, 0.0)
    scale = 1 + punch * math.exp(-t / M["punchTauSeconds"]) - M["holdShrink"] * clamp01(t / max(d, 1e-6))
    size = base * scale

    tracking = 0.0
    if invert and variant == "track":
        tracking = M["trackingEndEm"] * ease_out(t / max(d, 1e-6))

    glyphs, width = layout(text, size, tracking)
    cx = W / 2
    baseline = H / 2 + size * CAP_RATIO / 2 + shot.get("y", 0) * H
    x_offset = 0.0

    text_col = rgb(C["text"])
    inactive = rgb(C["inactive"])
    if invert:
        text_col = rgb(C["invertText"])

    words = text.split(" ")
    clip = None  # (x0, x1) in frame coordinates
    word_start = [0.0] * len(words)  # when each word appears (build only)

    if move == "build":
        n = len(words)
        word_start = shot.get("_word_times") or [i * d * 0.7 / n for i in range(n)]
        k = max(i for i in range(n) if word_start[i] <= t or i == 0)
        local = t - word_start[k]
        reveal = ease_out(local / shot.get("shiftSeconds", M["buildWipeSeconds"]))
        vis_prev = " ".join(words[:k])
        vis_now = " ".join(words[:k + 1])
        f = font(size)
        w_prev = f.getlength(vis_prev) if k > 0 else 0
        w_now = f.getlength(vis_now)
        w_cur = lerp(w_prev, w_now, reveal)
        left = cx - w_cur / 2
        glyphs = [g for g in glyphs if g[2] <= k]
        clip = (-1, left + w_cur + 1 if reveal < 1 else W + 1)
        x_start = left
    else:
        x_start = cx - width / 2

    if move == "letters":
        x_offset += M["lettersSlideInPercentOfWidth"] / 100 * W * math.exp(-t / 0.06)

    if move == "wipe":
        p = ease_out(t / M["wipeSeconds"])
        clip = (-1, x_start + x_offset + width * p + 1 if p < 1 else W + 1)

    # Exit.
    exit_dur = M["exitSeconds"] if exit_kind == "slide" else M["wipeSeconds"]
    q = clamp01((t - (d - exit_dur)) / exit_dur) if exit_kind in ("slide", "wipe") else 0.0
    dim = 0.0
    if exit_kind == "slide" and q > 0:
        x_offset += M["slideExitPercentOfWidth"] / 100 * W * ease_in(q)
        dim = q
    if exit_kind == "wipe" and q > 0:
        x_left = x_start + x_offset - 2
        hide_to = x_left + (width + 4) * ease_in(q)
        clip = (max(clip[0], hide_to) if clip else hide_to, clip[1] if clip else W + 1)

    n_glyphs = len(glyphs)
    for gi, (ch, gx, wi) in enumerate(glyphs):
        col = text_col
        skew = 0.0
        tw = t - word_start[wi]  # time since this glyph's word appeared
        if invert:
            col = lerp_rgb(rgb(C["invertTextStart"]), rgb(C["invertText"]), ease_out(tw / M["invertFadeSeconds"]))
        if move == "karaoke":
            active = min(len(words) - 1, int(t / (d * 0.85 / len(words))))
            col = text_col if wi == active else inactive
        if move == "letters":
            lt = (t - gi * M["lettersStaggerSeconds"]) / M["lettersFadeSeconds"]
            col = lerp_rgb(inactive, text_col, ease_out(lt))
        if invert and variant == "skew" and (move != "build" or wi == len(words) - 1):
            group = [g for g in glyphs if g[2] == wi] if move == "build" else glyphs
            idx = next(j for j, g in enumerate(group) if g[1] == gx and g[2] == wi)
            delay = (idx - len(group) * 0.5) * M["skewStaggerSeconds"]
            skew = M["skewStart"] * (1 - ease_out((tw - delay) / M["skewSettleSeconds"]))
        if dim > 0:
            col = lerp_rgb(col, rgb(C["exitDim"]) if not invert else rgb(C["invertTextStart"]), dim)
        draw_glyph(layer, ch, x_start + x_offset + gx, baseline, size, col, skew=skew)

    if clip:
        clip_x(layer, clip[0], clip[1])
    img.alpha_composite(layer)
    return img.convert("RGB")


def beat_track(path, bpm, seconds, sr=44100):
    import array
    n = int(seconds * sr)
    out = array.array("h", [0] * n)
    beat = 60.0 / bpm
    b = 0
    while b * beat < seconds:
        start = int(b * beat * sr)
        for i in range(int(0.18 * sr)):
            if start + i >= n:
                break
            tt = i / sr
            f = 50 + 90 * math.exp(-tt / 0.03)
            v = math.sin(2 * math.pi * f * tt) * math.exp(-tt / 0.07) * 0.7
            out[start + i] = max(-32767, min(32767, out[start + i] + int(v * 32767)))
        hs = int((b + 0.5) * beat * sr)
        seed = 12345
        for i in range(int(0.04 * sr)):
            if hs + i >= n:
                break
            seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
            v = ((seed / 0x7FFFFFFF) * 2 - 1) * math.exp(-i / sr / 0.008) * 0.15
            out[hs + i] = max(-32767, min(32767, out[hs + i] + int(v * 32767)))
        b += 1
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(out.tobytes())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("timeline")
    ap.add_argument("out")
    ap.add_argument("--beat", action="store_true", help="add a simple beat track at the timeline bpm")
    args = ap.parse_args()

    tl = json.loads(Path(args.timeline).read_text())
    W, H = tl.get("size", [1920, 1080])
    fps = tl.get("fps", 30)
    bpm = tl.get("bpm", STYLE["rhythm"]["referenceBpm"])
    shots = tl["shots"]
    lead_in = tl.get("leadInSeconds", 0.5)
    tail = tl.get("tailSeconds", 0.5)

    # Snap shot boundaries to whole frames so cuts land exactly.
    for s in shots:
        if "wordAt" in s:
            s["_word_times"] = [b * 60.0 / bpm for b in s["wordAt"]]
    spans, cur = [], lead_in
    for s in shots:
        d = shot_duration(s, bpm)
        spans.append((cur, cur + d))
        cur += d
    total = cur + tail
    nframes = int(round(total * fps))

    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(fps), "-i", "-"]
    tmp = None
    audio = tl.get("audio")
    if args.beat and not audio:
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        beat_track(tmp.name, bpm, total)
        audio = tmp.name
    if audio:
        cmd += ["-i", str(audio), "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-preset", "medium", args.out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    pad = C["invertBackground"] if tl.get("pad") == "invert" else C["background"]
    empty = Image.new("RGB", (W, H), rgb(pad)).tobytes()
    si = 0
    for fi in range(nframes):
        t = fi / fps
        while si < len(spans) and t >= spans[si][1]:
            si += 1
        if si < len(spans) and t >= spans[si][0]:
            a, b = spans[si]
            frame = render_frame(shots[si], t - a, b - a, W, H).tobytes()
        else:
            frame = empty
        proc.stdin.write(frame)
    proc.stdin.close()
    proc.wait()
    if tmp:
        Path(tmp.name).unlink(missing_ok=True)
    if proc.returncode:
        sys.exit(proc.returncode)
    print(f"wrote {args.out} ({total:.2f}s, {nframes} frames, {W}x{H}@{fps})")


if __name__ == "__main__":
    main()
