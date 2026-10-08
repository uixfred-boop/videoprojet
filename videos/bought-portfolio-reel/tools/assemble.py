#!/usr/bin/env python3
"""Assemble index.html: scene slots, footage strip + head pop-out clips, captions sub-composition, SFX.

Timing source: transcript.json (word-aligned voice-over) + tools/spoken.txt (display text). Re-run after edits:
    python3 tools/assemble.py
"""
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORDS = json.loads((ROOT / "transcript.json").read_text())
SPOKEN = (ROOT / "tools/spoken.txt").read_text()
DURATION = 114.2

# (id, start, end, kind)  kind: panel | cut
SCENES = [
    ("s01-hub-hook", 0.00, 5.80, "panel"),
    ("s02-hero-01", 5.80, 9.92, "panel"),
    ("s03-views-bank", 9.92, 15.00, "panel"),
    ("s04-cut-obsessed", 15.00, 20.15, "cut"),
    ("s05-no-portfolio", 20.15, 23.42, "panel"),
    ("s06-hub-02", 23.42, 28.05, "panel"),
    ("s07-outreach", 28.05, 32.72, "panel"),
    ("s08-spam", 32.72, 35.95, "panel"),
    ("s09-result", 35.95, 39.40, "panel"),
    ("s10-opened", 39.40, 44.38, "panel"),
    ("s11-cut-nothing", 44.38, 46.97, "cut"),
    ("s12-hub-03", 46.97, 49.36, "panel"),
    ("s13-one-of-500", 49.36, 53.35, "panel"),
    ("s14-shopify", 53.35, 61.75, "panel"),
    ("s15-cut-happy", 61.75, 64.40, "cut"),
    ("s16-demand", 64.40, 69.05, "panel"),
    ("s17-template", 69.05, 74.35, "panel"),
    ("s18-price", 74.35, 79.02, "panel"),
    ("s19-cut-freelancer", 79.02, 83.25, "cut"),
    ("s20-copied", 83.25, 88.78, "panel"),
    ("s21-hub-04", 88.78, 92.33, "panel"),
    ("s22-good-portfolio", 92.33, 97.23, "panel"),
    ("s23-locked", 97.23, 101.50, "panel"),
    ("s24-studied", 101.50, 106.62, "panel"),
    ("s25-cta", 106.62, DURATION, "panel"),
]

# Footage shots in assets/video/people.mp4 (usable source range) and their card geometry in FRAME pixels:
# scale, left, top chosen so the head top sits ~78px above the card edge (y 1408) and roughly centred.
SHOTS = {
    "B": {"src": (7.5, 12.3), "w": 1080, "h": 1920, "left": 72, "top": 960},
    "C": {"src": (14.6, 20.6), "w": 1080, "h": 1920, "left": -72, "top": 890},
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
            f'data-start="{f(a)}" data-duration="{f(b - a)}" data-track-index="1" data-width="1080" data-height="1920"></div>'
        )
    return out


def build_strip():
    """Footage for every panel scene, alternating shots B/C at scene cuts. A scene longer than a shot is split
    into even parts (no tiny fragments); a shot whose remaining source is too short wraps to its start."""
    clips = []
    cursor = {k: v["src"][0] for k, v in SHOTS.items()}
    order = ["B", "C"]
    n = 0
    for sid, a, b, kind in SCENES:
        if kind != "panel":
            continue
        L = b - a
        maxlen = min(v["src"][1] - v["src"][0] for v in SHOTS.values())
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
            f'<video id="strip-{k:02d}" class="clip" src="assets/video/people.mp4" data-start="{f(t)}" data-duration="{f(d)}" '
            f'data-media-start="{f(m)}" data-track-index="3" muted playsinline style="{style_card}"></video>'
        )
        pop.append(
            f'<video id="pop-{k:02d}" class="clip" src="assets/video/people-cutout.webm" data-start="{f(t)}" data-duration="{f(d)}" '
            f'data-media-start="{f(m)}" data-track-index="4" muted playsinline style="{style_frame}"></video>'
        )
    return strip, pop


# ---------------- captions ----------------
NUMBER_MERGES = [
    (["one", "thousand", "five", "hundred", "dollars"], "$1,500"),
    (["three", "hundred", "fifty", "dollars"], "$350"),
    (["five", "hundred"], "500"),
]
EMPH = {"cheated", "transparency", "spam", "nothing", "amateur", "demand", "solution", "lucrative", "strategy", "freelancer",
        "proves", "monetize", "locked", "expertise", "ready-made", "portfolio", "template"}
HEAVY = {"$350", "$1,500", "500", "subscribe,", "yes."}


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
        n = len(re.findall(r"[a-z']+", w.lower()))  # "ready-made" counts as 2 aligned words
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
    # attach timings
    items = []
    wi = 0
    for disp, n in toks:
        items.append({"t": disp, "s": WORDS[wi]["start"], "e": WORDS[wi + n - 1]["end"]})
        wi += n
    groups, cur = [], []
    for k, it in enumerate(items):
        if cur:
            prev = cur[-1]
            text_len = len(" ".join(x["t"] for x in cur + [it]))
            if (
                re.search(r"[.?!:,…]$|\.\.\.$", prev["t"])
                or it["s"] - prev["e"] > 0.25
                or len(cur) >= 3
                or text_len > 19
                or it["t"] in HEAVY
                or prev["t"] in HEAVY
            ):
                groups.append(cur)
                cur = []
        cur.append(it)
    if cur:
        groups.append(cur)
    out = []
    starts = [max(g[0]["s"] - 0.05, 0.0) for g in groups]
    for k, g in enumerate(groups):
        a = starts[k]
        sc = scene_at(g[0]["s"])
        last_end = g[-1]["e"]
        if k + 1 < len(groups):
            nxt = starts[k + 1]
            b = nxt if nxt - last_end < 0.8 else last_end + 0.35
            if scene_at(groups[k + 1][0]["s"])[3] != sc[3]:
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


# ---------------- SFX ----------------
# (time, file in assets/sfx, volume[, trimmed length])  — filled in once scenes are built
SFX = [
    # scene changes
    *[(t, "whoosh-short", 0.24) for t in (5.80, 9.92, 20.15, 28.05, 32.72, 35.95, 39.40, 49.36, 53.35, 64.40, 69.05, 74.35,
                                          83.25, 92.33, 97.23, 101.50, 106.62)],
    *[(t, "whoosh", 0.28) for t in (23.42, 46.97, 88.78)],                 # hub returns
    *[(t, "impact-bass-2", 0.05, 1.2) for t in (15.00, 44.38, 61.75, 79.02)],  # cutaways
    # ghost typing under the hub titles
    (0.10, "typing", 0.12), (2.0, "typing", 0.10), (23.45, "typing", 0.10), (88.80, "typing", 0.10),
    (107.45, "typing", 0.10), (110.35, "typing", 0.10),
    # s01-s03
    (0.12, "pop", 0.22), (0.40, "pop", 0.22),
    (5.90, "click", 0.45), (5.90, "impact-bass-1", 0.08, 0.8), (6.30, "whoosh", 0.26),
    (12.00, "pop", 0.24), (12.85, "pop", 0.24), (14.55, "error", 0.22),
    # s05-s10
    (22.74, "pop", 0.34), (24.45, "whoosh", 0.26),
    (29.73, "pop", 0.3), (30.79, "pop", 0.3), (31.35, "whoosh-short", 0.22), (31.40, "sparkle", 0.14),
    (33.21, "typing", 0.14), (35.37, "click", 0.5), (35.37, "impact-bass-1", 0.08, 0.8),
    (36.60, "whoosh-short", 0.18), (38.28, "error", 0.2),
    *[(41.79 + i * 0.12, "click-soft", 0.3) for i in range(4)],
    *[(42.99 + i * 0.14, "click-soft", 0.3) for i in range(4)],
    # s12-s14
    (47.40, "whoosh", 0.26), (49.40, "sparkle", 0.15), (50.54, "ping", 0.34), (50.70, "pop", 0.24),
    (54.78, "typing", 0.13), (56.01, "ping", 0.24), (56.80, "error", 0.18), (60.45, "typing", 0.12), (61.24, "chime", 0.2),
    # s16-s18
    (65.30, "sparkle", 0.15), (66.72, "whoosh-short", 0.2),
    (71.23, "click", 0.5), (71.23, "impact-bass-1", 0.08, 0.8), (73.34, "pop", 0.3),
    (77.36, "typing", 0.13), (78.80, "ping", 0.24),
    # s20-s25
    (83.40, "whoosh-short", 0.18), (83.75, "whoosh-short", 0.18), (84.10, "whoosh-short", 0.18), (87.54, "error", 0.15),
    (89.65, "whoosh", 0.26), (95.10, "whoosh-short", 0.2), (95.74, "pop", 0.34), (96.30, "click-soft", 0.3),
    (97.95, "click", 0.5), (99.16, "key-press", 0.42), (100.74, "key-press", 0.42),
    (102.26, "pop", 0.2), (102.50, "pop", 0.2), (102.74, "pop", 0.2), (104.60, "whoosh", 0.28), (105.90, "pop", 0.3),
    (110.40, "pop", 0.4), (111.00, "click", 0.5), (111.10, "notification", 0.22),
]
SFX_LEN = {
    "sparkle": 1.80, "key-press": 0.43, "typing": 1.54, "whoosh": 0.57, "whoosh-cinematic": 5.54, "chime": 2.54,
    "error": 1.62, "impact-bass-1": 2.12, "notification": 2.46, "click-soft": 0.37, "pop": 0.72, "click": 0.37,
    "impact-bass-2": 2.59, "whoosh-short": 0.57, "ping": 1.32,
}


def trimmed_sfx(name, length):
    out = ROOT / f"assets/sfx/{name}-{length:g}s.mp3"
    if not out.exists():
        fade = min(0.4, length / 3)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ROOT / f"assets/sfx/{name}.mp3"), "-af",
                        f"atrim=0:{length},afade=t=out:st={length - fade:.3f}:d={fade:.3f}", str(out)], check=True)
    return out.name


def build_audio():
    out, lanes_end = [], []
    for k, item in enumerate(sorted(SFX)):
        t, name, vol = item[0], item[1], item[2]
        if len(item) > 3:
            length = min(item[3], DURATION - t)
            src = trimmed_sfx(name, item[3])
        else:
            length = min(SFX_LEN[name], DURATION - t)
            src = f"{name}.mp3"
        lane = next((i for i, end in enumerate(lanes_end) if end <= t + 1e-6), None)
        if lane is None:
            lanes_end.append(0.0)
            lane = len(lanes_end) - 1
        lanes_end[lane] = t + length
        out.append(f'<audio id="sfx-{k:03d}-{name}" src="assets/sfx/{src}" data-start="{f(t)}" data-duration="{f(length)}" '
                   f'data-track-index="{21 + lane}" data-volume="{vol}"></audio>')
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
