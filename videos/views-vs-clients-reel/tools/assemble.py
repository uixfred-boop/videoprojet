#!/usr/bin/env python3
"""Assemble index.html: scene slots, footage strip + head pop-out clips, captions sub-composition, SFX.

Timing source: transcript.json (word-aligned voice-over) + tools/spoken.txt (display text). Re-run after edits:
    python3 tools/assemble.py
No music: the user adds their own track.
"""
import html
import json
import pathlib
import re
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SFX_LIB = ROOT.parent.parent / ".claude/skills/media-use/audio/assets/sfx"
WORDS = json.loads((ROOT / "transcript.json").read_text())
SPOKEN = (ROOT / "tools/spoken.txt").read_text()
DURATION = 29.6

# (id, start, end, kind)  kind: panel | cut
SCENES = [
    ("s01-hub-hook", 0.00, 3.83, "panel"),
    ("s02-millions", 3.83, 7.31, "panel"),
    ("s03-zero", 7.31, 9.37, "panel"),
    ("s04-beautiful", 9.37, 10.92, "panel"),
    ("s05-no-trust", 10.92, 14.86, "panel"),
    ("s06-cut-left", 14.86, 18.48, "cut"),
    ("s07-objectives", 18.48, 22.21, "panel"),
    ("s08-cut-hard-way", 22.21, 23.86, "cut"),
    ("s09-cta", 23.86, DURATION, "panel"),
]

# Two framings of assets/video/desk.mp4 (one high-angle shot, 10.5s) in FRAME pixels. The head top sits 72–132px
# down the source frame (median 108), the face centred near x 485, so both put the head top ~70–110px above the card
# edge (y 1408) with the face inside the card. W cycles the typing half, T the thinking half; both play at 0.8x so
# the short footage stretches over the reel.
SHOTS = {
    "W": {"src": (0.2, 4.7), "w": 972, "h": 1728, "left": 72, "top": 1228},     # 0.9x
    "T": {"src": (5.2, 10.3), "w": 1242, "h": 2208, "left": -18, "top": 1196},  # 1.15x
}
STRIP_RATE = 0.8
# A gentle exposure/shadow lift on the footage (it was shot dark): validated with `hyperframes media-treatment`
# (tools/grade.json is its normalised payload) and applied identically to the strip, the pop-out cutout and the
# cutaways so the head above the card edge matches the face inside it.
GRADE = html.escape(json.dumps(json.loads((ROOT / "tools/grade.json").read_text()), separators=(",", ":")))
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
    maxlen = min(v["src"][1] - v["src"][0] for v in SHOTS.values()) / STRIP_RATE
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
            used = seg * STRIP_RATE
            if cursor[shot] + used > s1 + 1e-6:
                cursor[shot] = s0
            clips.append((t, seg, shot, cursor[shot]))
            cursor[shot] += used
            t += seg
    strip, pop = [], []
    for k, (t, d, shot, m) in enumerate(clips):
        g = SHOTS[shot]
        style_card = f"left:{f(g['left'] - CARD[0])}px;top:{f(g['top'] - CARD[1])}px;width:{f(g['w'])}px;height:{f(g['h'])}px"
        style_frame = f"left:{f(g['left'])}px;top:{f(g['top'])}px;width:{f(g['w'])}px;height:{f(g['h'])}px"
        strip.append(
            f'<video id="strip-{k:02d}" class="clip" data-color-grading="{GRADE}" src="assets/video/desk.mp4" data-start="{f(t)}" data-duration="{f(d)}" '
            f'data-media-start="{f(m)}" data-playback-rate="{STRIP_RATE}" data-track-index="3" muted playsinline style="{style_card}"></video>'
        )
        pop.append(
            f'<video id="pop-{k:02d}" class="clip" data-color-grading="{GRADE}" src="assets/video/desk-cutout.webm" data-start="{f(t)}" data-duration="{f(d)}" '
            f'data-media-start="{f(m)}" data-playback-rate="{STRIP_RATE}" data-track-index="4" muted playsinline style="{style_frame}"></video>'
        )
    return strip, pop


# ---------------- captions ----------------
NUMBER_MERGES = []
EMPH = {"views", "clients", "millions", "beautiful", "trust", "expertise", "left", "prospects", "objectives", "hard",
        "follow"}
HEAVY = {"zero."}
BREAK_BEFORE = set()


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
# sound effects on reel 3 (2026-10-09, "especially on the wow"); this reel starts at that quieter level.
SFX_GAIN = 0.45  # -7 dB
SFX = [
    # cuts and cutaways: short whooshes
    *[(t, "whoosh-short", 0.22) for t in (3.83, 7.31, 9.37, 10.92, 14.86, 18.48, 22.21, 23.86)],
    # ghost typing under headlines and hub lines
    (0.38, "typing", 0.10, 0.5), (1.18, "typing", 0.10, 1.0), (2.78, "typing", 0.10, 0.9), (4.05, "typing", 0.10, 0.9),
    (7.56, "typing", 0.10), (9.37, "typing", 0.10, 1.2), (11.06, "typing", 0.10, 0.9), (18.81, "typing", 0.10, 0.7),
    (24.48, "typing", 0.10, 0.8), (25.63, "typing", 0.10, 0.6), (27.22, "typing", 0.10, 1.2),
    # s01 hook: tiles, ball, "not the same"
    (0.40, "pop", 0.24), (1.18, "pop", 0.22), (1.62, "pop", 0.24), (3.03, "click-soft", 0.3),
    # s02 millions / likes
    (3.88, "pop", 0.2), (4.90, "ping", 0.2), (5.40, "pop", 0.2), *[(5.70 + i * 0.16, "pop", 0.12) for i in range(6)],
    (6.54, "ping", 0.18),
    # s03 zero
    (8.66, "click", 0.25),
    # s04 beautiful work
    (9.42, "pop", 0.16), (9.60, "pop", 0.16), (9.78, "pop", 0.16), (10.00, "sparkle", 0.05),
    # s05 neither trust nor expertise
    (12.10, "click", 0.3), (12.20, "pop", 0.15), (13.95, "click", 0.3), (14.05, "pop", 0.15),
    # s06 liked... then left. No prospects.
    (15.07, "pop", 0.15), (15.25, "pop", 0.15), (16.47, "whoosh-short", 0.15), (17.50, "click", 0.35),
    # s07 content -> business objectives
    (20.06, "whoosh-short", 0.15), (20.58, "pop", 0.3), *[(21.25 + i * 0.12, "click-soft", 0.2) for i in range(3)],
    (21.75, "ping", 0.2),
    # s09 CTA
    (23.95, "pop", 0.3), (25.68, "click", 0.4), (25.78, "notification", 0.18), (26.98, "pop", 0.2), (27.10, "pop", 0.2),
    (28.07, "ping", 0.2),
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
