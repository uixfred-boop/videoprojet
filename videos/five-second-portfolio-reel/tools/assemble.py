#!/usr/bin/env python3
"""Assemble index.html: scene slots, footage strip + head pop-out clips, captions sub-composition, SFX.

Timing source: transcript.json (word-aligned voice-over) + tools/spoken.txt (display text). Re-run after edits:
    python3 tools/assemble.py
No music: the user adds their own track.
"""
import json
import pathlib
import re
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SFX_LIB = ROOT.parent.parent / ".claude/skills/media-use/audio/assets/sfx"
WORDS = json.loads((ROOT / "transcript.json").read_text())
SPOKEN = (ROOT / "tools/spoken.txt").read_text()
DURATION = 38.0

# (id, start, end, kind)  kind: panel | cut
SCENES = [
    ("s01-hub-hook", 0.00, 3.08, "panel"),
    ("s02-five-seconds", 3.08, 7.21, "panel"),
    ("s03-cut-reality", 7.21, 9.02, "cut"),
    ("s04-hub-01", 9.02, 11.27, "panel"),
    ("s05-too-much", 11.27, 14.25, "panel"),
    ("s06-hub-02", 14.25, 17.23, "panel"),
    ("s07-different", 17.23, 20.37, "panel"),
    ("s08-who-what", 20.37, 23.70, "panel"),
    ("s09-cut-clicked", 23.70, 25.62, "cut"),
    ("s10-not-wow", 25.62, 27.48, "panel"),
    ("s11-understood", 27.48, 29.40, "panel"),
    ("s12-hub-03", 29.40, 31.45, "panel"),
    ("s13-logic", 31.45, 32.84, "panel"),
    ("s14-cta", 32.84, DURATION, "panel"),
]

# Two framings of assets/video/desk.mp4 (one camera angle) in FRAME pixels. The head top sits ~250–345px down the
# source frame, so these put it ~60–100px above the card edge (y 1408) with the whole face inside the card. Each framing cycles through its own source range;
# the cutaways' moments (9.0–10.8s, 17.75–19.7s) are left out.
SHOTS = {
    "W": {"src": (0.3, 8.9), "w": 972, "h": 1728, "left": 54, "top": 1060},     # 0.9x, head centred
    "T": {"src": (11.0, 17.6), "w": 1242, "h": 2208, "left": -124, "top": 985},  # 1.15x, head a little left
}
CARD = (72, 1408)


def f(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")


def scene_at(t):
    for s in SCENES:
        if s[1] <= t < s[2]:
            return s
    return SCENES[-1]


def build_scenes():
    out = []
    for sid, a, b, kind in SCENES:
        cls = "scene cut" if kind == "cut" else "scene"
        out.append(
            f'<div id="el-{sid}" class="{cls}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
            f'data-start="{f(a)}" data-duration="{f(b - a)}" data-track-index="1" data-track-kind="graphics" '
            f'data-width="1080" data-height="1920"></div>'
        )
    return out


def build_strip():
    """Footage for every panel scene, alternating framings W/T at scene cuts. A scene longer than a source range is
    split into even parts; a framing whose remaining source is too short wraps to its start."""
    clips = []
    cursor = {k: v["src"][0] for k, v in SHOTS.items()}
    order = ["W", "T"]
    n = 0
    maxlen = min(v["src"][1] - v["src"][0] for v in SHOTS.values())
    for sid, a, b, kind in SCENES:
        if kind != "panel":
            continue
        L = b - a
        parts = max(1, int(-(-L // maxlen)))
        seg = L / parts
        t = a
        for _ in range(parts):
            shot = order[n % 2]
            n += 1
            s0, s1 = SHOTS[shot]["src"]
            if cursor[shot] + seg > s1 + 1e-6:
                cursor[shot] = s0
            clips.append((t, seg, shot, cursor[shot]))
            cursor[shot] += seg
            t += seg
    strip, pop = [], []
    for k, (t, d, shot, m) in enumerate(clips):
        g = SHOTS[shot]
        style_card = f"left:{f(g['left'] - CARD[0])}px;top:{f(g['top'] - CARD[1])}px;width:{f(g['w'])}px;height:{f(g['h'])}px"
        style_frame = f"left:{f(g['left'])}px;top:{f(g['top'])}px;width:{f(g['w'])}px;height:{f(g['h'])}px"
        strip.append(
            f'<video id="strip-{k:02d}" class="clip" src="assets/video/desk.mp4" data-start="{f(t)}" data-duration="{f(d)}" '
            f'data-media-start="{f(m)}" data-track-index="3" muted playsinline style="{style_card}"></video>'
        )
        pop.append(
            f'<video id="pop-{k:02d}" class="clip" src="assets/video/desk-cutout.webm" data-start="{f(t)}" data-duration="{f(d)}" '
            f'data-media-start="{f(m)}" data-track-index="4" muted playsinline style="{style_frame}"></video>'
        )
    return strip, pop


# ---------------- captions ----------------
NUMBER_MERGES = [
    (["five", "seconds"], "5 seconds"),
]
EMPH = {"animations", "understand", "best", "cofolio", "different", "fluid", "efficient", "clicked", "understood",
        "scratch", "logic", "follow", "much"}
HEAVY = {"5 seconds.", "5 seconds,", "WOW."}
BREAK_BEFORE = {"Cofolio."}  # lands alone, in serif


def display_tokens():
    """Script words with punctuation/casing, aligned 1:1 to transcript words (numbers merged)."""
    raw = re.findall(r"\S+", SPOKEN)
    toks = []  # (display, n_words)
    i = 0
    while i < len(raw):
        merged = False
        for seq, disp in NUMBER_MERGES:
            seg = [re.sub(r"[^a-z']", "", w.lower()) for w in raw[i : i + len(seq)]]
            if seg == seq:
                tail = re.sub(r"^[A-Za-z']+", "", raw[i + len(seq) - 1])  # trailing punctuation
                toks.append((disp + tail, len(seq)))
                i += len(seq)
                merged = True
                break
        if merged:
            continue
        w = raw[i]
        n = len(re.findall(r"[a-z']+", w.lower()))
        toks.append((w, max(1, n)))
        i += 1
    return toks


CAP_CSS = """
        #captions-root { position: absolute; inset: 0; pointer-events: none; }
        .cap { position: absolute; left: 40px; width: 1000px; height: 120px; display: flex; align-items: center; justify-content: center; }
        .cap.seam { top: 1217px; }
        .cap.center { top: 1120px; }
        .cap .t { display: block; white-space: nowrap; font-family: "Inter Tight", Arial, sans-serif; font-weight: 800;
          font-size: 62px; letter-spacing: -0.035em; line-height: 1; color: #f5f5f5;
          text-shadow: 0 4px 22px rgba(0,0,0,0.65), 0 1px 3px rgba(0,0,0,0.5); }
        .cap.center .t { font-size: 74px; text-shadow: 0 6px 30px rgba(0,0,0,0.8), 0 2px 4px rgba(0,0,0,0.6); }
        .cap.i .t { font-family: "Instrument Serif", Georgia, serif; font-style: italic; font-weight: 400; font-size: 80px; letter-spacing: -0.01em; }
        .cap.center.i .t { font-size: 94px; }
        .cap.n .t { font-weight: 900; font-size: 78px; letter-spacing: -0.04em; }
        .cap.center.n .t { font-size: 96px; }"""


def build_caps():
    toks = display_tokens()
    total = sum(n for _, n in toks)
    assert total == len(WORDS), f"display tokens cover {total} words, transcript has {len(WORDS)}"
    items = []
    wi = 0
    for disp, n in toks:
        items.append({"t": disp, "s": WORDS[wi]["start"], "e": WORDS[wi + n - 1]["end"]})
        wi += n
    groups, cur = [], []
    for it in items:
        if cur:
            prev = cur[-1]
            text_len = len(" ".join(x["t"] for x in cur + [it]))
            # a sentence's last word may join a full group when it still fits ("doing way too much.")
            closes = re.search(r"[.?!]$", it["t"]) and text_len <= 19
            if (
                re.search(r"[.?!:,…]$|\.\.\.$", prev["t"])
                or it["s"] - prev["e"] > 0.18
                or (len(cur) >= 3 and not closes)
                or text_len > 19
                or it["t"] in HEAVY
                or prev["t"] in HEAVY
                or it["t"] in BREAK_BEFORE
            ):
                groups.append(cur)
                cur = []
        cur.append(it)
    if cur:
        groups.append(cur)
    out = []
    starts = [max(g[0]["s"] - 0.05, 0.0) for g in groups]
    for k, g in enumerate(groups):
        # a word can be aligned a few ms before the cut it belongs to: give the scene a little slack, and keep a
        # cutaway's caption inside the cutaway
        sc = scene_at(g[0]["s"] + 0.06)
        a = max(starts[k], sc[1]) if sc[3] == "cut" else starts[k]
        last_end = g[-1]["e"]
        if k + 1 < len(groups):
            nxt = starts[k + 1]
            b = nxt if nxt - last_end < 0.8 else last_end + 0.35
            if scene_at(groups[k + 1][0]["s"] + 0.06)[3] != sc[3]:
                b = min(b, sc[2])
        else:
            b = DURATION
        text = " ".join(x["t"] for x in g)
        bare = {re.sub(r"[^a-z\-]", "", x["t"].lower()) for x in g}
        style = "s"
        if any(x["t"] in HEAVY for x in g):
            style = "n"
        elif bare & EMPH and len(g) <= 2:
            style = "i"
        pos = "center" if sc[3] == "cut" else "seam"
        out.append(
            f'<div id="cap-{k:03d}" class="cap clip {pos} {style}" data-start="{f(a)}" data-duration="{f(b - a)}" '
            f'data-track-index="0"><span class="t">{text}</span></div>'
        )
    fonts = (ROOT / "tools/fonts.css.snippet").read_text()
    body = "\n".join(f"          {g}" for g in out)
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <!-- Generated by tools/assemble.py from transcript.json + tools/spoken.txt. Edit there, not here. -->
    <template id="captions-template">
      <style>
{fonts}{CAP_CSS}
      </style>
      <div id="captions-root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="{f(DURATION)}">
{body}
      </div>
      <script>
        (function () {{
          const tl = gsap.timeline({{ paused: true }});
          document.querySelectorAll("#captions-root .cap").forEach((cap) => {{
            const at = parseFloat(cap.getAttribute("data-start"));
            const t = cap.querySelector(".t");
            const big = cap.classList.contains("n");
            tl.fromTo(t, {{ opacity: 0, y: 16, scale: big ? 0.7 : 0.9, filter: "blur(8px)" }},
              {{ opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: big ? 0.24 : 0.16, ease: big ? "back.out(2.2)" : "power2.out" }}, at);
          }});
          window.__timelines["captions"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""
    (ROOT / "compositions/captions.html").write_text(html)
    return [
        f'<div id="el-captions" class="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" '
        f'data-start="0" data-duration="{f(DURATION)}" data-track-index="5" data-track-kind="captions" data-width="1080" data-height="1920"></div>'
    ], len(out)


# ---------------- SFX (soft UI sounds only; no music, no impacts) ----------------
# (time, file in assets/sfx, volume[, trimmed length]). Every volume is scaled by SFX_GAIN: the user asked for quieter
# sound effects (2026-10-09), "especially on the wow", so the table keeps the relative balance and this sets the level.
SFX_GAIN = 0.45  # -7 dB
SFX = [
    # scene changes: whooshes on hub returns, short whooshes on cuts and cutaways
    *[(t, "whoosh", 0.26) for t in (9.02, 14.25, 29.40)],
    *[(t, "whoosh-short", 0.22) for t in (3.08, 7.21, 11.27, 17.23, 20.37, 23.70, 25.62, 27.48, 31.45, 32.84)],
    # ghost typing under headlines and hub labels
    (0.03, "typing", 0.11), (1.62, "typing", 0.10), (5.30, "typing", 0.10), (10.16, "typing", 0.10),
    (15.62, "typing", 0.10, 0.6), (17.62, "typing", 0.10, 0.8), (20.38, "typing", 0.10, 0.8), (25.64, "typing", 0.10, 0.5),
    (27.72, "typing", 0.10), (29.80, "typing", 0.10), (33.40, "typing", 0.10, 0.85), (35.98, "typing", 0.10),
    # s01 hook: the clip gets struck out, then tiles + ball
    (1.08, "click", 0.42), (1.12, "whoosh-short", 0.2), (1.62, "pop", 0.24), (1.70, "pop", 0.22),
    (1.78, "pop", 0.22),
    # s02 five seconds
    (3.14, "pop", 0.2), (5.62, "click-soft", 0.32), (6.42, "click-soft", 0.32), (6.93, "ping", 0.24),
    # s04 hub 01
    (9.40, "whoosh-short", 0.18),
    # s05 too much
    (11.30, "pop", 0.2), (11.42, "pop", 0.2), (11.54, "pop", 0.2), (13.00, "pop", 0.24), (13.12, "pop", 0.24),
    *[(13.05 + i * 0.08, "click-soft", 0.24) for i in range(4)],
    (13.29, "pop", 0.34), (13.64, "error", 0.08),
    # s06 hub 02
    (14.90, "whoosh-short", 0.18), (16.20, "sparkle", 0.06),
    # s07 different
    (18.71, "pop", 0.32), (19.52, "pop", 0.32),
    # s08 who / what
    (20.40, "pop", 0.22), (21.15, "ping", 0.22), (21.88, "click-soft", 0.3), (22.87, "click-soft", 0.3), (23.13, "pop", 0.2),
    # s09 clicked
    (24.14, "chime", 0.16),
    # s10 not wow: kept very soft (no sparkle, no error buzz)
    (26.20, "pop", 0.12), (26.84, "click", 0.2),
    # s11 understood
    (27.95, "click-soft", 0.3), (28.20, "click-soft", 0.3), (28.45, "ping", 0.22),
    # s12 hub 03
    # s13 rebuild
    *[(31.55 + i * 0.1, "click-soft", 0.24) for i in range(6)], (32.21, "ping", 0.22),
    # s14 CTA
    (33.00, "pop", 0.34), (34.60, "click", 0.5), (34.70, "notification", 0.2), (35.62, "pop", 0.22), (35.74, "pop", 0.22),
    (35.86, "pop", 0.22),
]
SFX_LEN = {}


def sfx_len(name):
    if name not in SFX_LEN:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                              str(ROOT / f"assets/sfx/{name}.mp3")], capture_output=True, text=True, check=True).stdout
        SFX_LEN[name] = round(float(out), 2)
    return SFX_LEN[name]


def trimmed_sfx(name, length):
    out = ROOT / f"assets/sfx/{name}-{length:g}s.mp3"
    if not out.exists():
        fade = min(0.4, length / 3)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ROOT / f"assets/sfx/{name}.mp3"), "-af",
                        f"atrim=0:{length},afade=t=out:st={length - fade:.3f}:d={fade:.3f}", str(out)], check=True)
    return out.name


def build_audio():
    for name in sorted({item[1] for item in SFX}):
        dst = ROOT / f"assets/sfx/{name}.mp3"
        if not dst.exists():
            shutil.copy(SFX_LIB / f"{name}.mp3", dst)
    out, lanes_end = [], []
    for k, item in enumerate(sorted(SFX)):
        t, name, vol = item[0], item[1], item[2]
        if len(item) > 3:
            length = min(item[3], DURATION - t)
            src = trimmed_sfx(name, item[3])
        else:
            length = min(sfx_len(name), DURATION - t)
            src = f"{name}.mp3"
        lane = next((i for i, end in enumerate(lanes_end) if end <= t + 1e-6), None)
        if lane is None:
            lanes_end.append(0.0)
            lane = len(lanes_end) - 1
        lanes_end[lane] = t + length
        out.append(f'<audio id="sfx-{k:03d}-{name}" src="assets/sfx/{src}" data-start="{f(t)}" data-duration="{f(length)}" '
                   f'data-track-index="{21 + lane}" data-volume="{round(vol * SFX_GAIN, 3)}"></audio>')
    return out


def inject(html, tag, lines, indent):
    pat = re.compile(rf"(<!-- {tag}:BEGIN -->)(.*?)(\n\s*<!-- {tag}:END -->)", re.S)
    body = "".join(f"\n{indent}{line}" for line in lines)
    return pat.sub(lambda m: m.group(1) + body + m.group(3), html)


def main():
    path = ROOT / "index.html"
    html = path.read_text()
    strip, pop = build_strip()
    caps, ncaps = build_caps()
    html = inject(html, "SCENES", build_scenes(), "      ")
    html = inject(html, "STRIP", strip, "          ")
    html = inject(html, "POPOUT", pop, "        ")
    html = inject(html, "CAPSLOT", caps, "      ")
    html = inject(html, "AUDIO", build_audio(), "      ")
    path.write_text(html)
    print(f"scenes={len(SCENES)} strip={len(strip)} captions={ncaps} sfx={len(SFX)}")


if __name__ == "__main__":
    main()
