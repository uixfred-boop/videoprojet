#!/usr/bin/env python3
"""Trial edit B ("makeover"): assemble index.html: scene slots, footage strip + head pop-out clips, one-word captions, SFX.

Timing source: transcript.json (word-aligned voice-over) + tools/spoken.txt (display text). Re-run after edits:
    python3 tools/assemble.py
No music: the user adds their own track.
"""
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORDS = json.loads((ROOT / "transcript.json").read_text())
SPOKEN = (ROOT / "tools/spoken.txt").read_text()
DURATION = 37.2

# (id, start, end, kind)  kind: panel | cut
SCENES = [
    ("b01-hook", 0.00, 3.53, "panel"),
    ("b02-cut-trap", 3.53, 6.15, "cut"),
    ("b03-anatomy", 6.15, 11.50, "panel"),
    ("b04-spoke-01", 11.50, 13.53, "panel"),
    ("b05-anatomy-02", 13.53, 15.80, "panel"),
    ("b06-spoke-02", 15.80, 18.12, "panel"),
    ("b07-cut-misses", 18.12, 20.42, "cut"),
    ("b08-anatomy-03", 20.42, 22.10, "panel"),
    ("b09-spoke-03", 22.10, 26.45, "panel"),
    ("b10-gallery", 26.45, 28.85, "panel"),
    ("b11-makeover", 28.85, 33.55, "panel"),
    ("b12-cut-comment", 33.55, 34.90, "cut"),
    ("b13-cta", 34.90, DURATION, "panel"),
]

# Two framings of assets/video/desk.mp4 (frontal shot at the laptop, 13.9s) in FRAME pixels. The head top sits
# 100–236px down the source (median 160) and the head centre near x 600, so both put the head top ~60–110px above the
# card edge (y 1408) with the face inside the card. Both play at 0.8x.
SHOTS = {
    "W": {"w": 972, "h": 1728, "left": 36, "top": 1176},     # 0.9x
    "T": {"w": 1242, "h": 2208, "left": -150, "top": 1136},  # 1.15x
}
STRIP_RATE = 0.8
CARD = (72, 1408)
# (start, end, framing, media start): chosen per line, and different from reel 5's cut where a line allows it.
# Reading for the explanations, hands over the face for "no client is writing to you" and "the client closes".
STRIP = [
    (0.00, 1.52, "T", 6.20),
    (1.52, 3.53, "W", 9.55),
    (6.15, 11.50, "T", 4.60),
    (11.50, 13.53, "W", 0.20),
    (13.53, 15.80, "T", 7.00),
    (15.80, 18.12, "W", 2.20),
    (20.42, 22.10, "T", 5.00),
    (22.10, 24.30, "W", 6.40),
    (24.30, 26.45, "T", 9.50),
    (26.45, 28.85, "W", 7.20),
    (28.85, 33.55, "T", 2.00),
    (34.90, DURATION, "W", 2.10),
]


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
    strip, pop = [], []
    for k, (a, b, shot, m) in enumerate(STRIP):
        g = SHOTS[shot]
        assert m + (b - a) * STRIP_RATE <= 13.85, f"strip clip {k} runs past the footage"
        style_card = f"left:{f(g['left'] - CARD[0])}px;top:{f(g['top'] - CARD[1])}px;width:{f(g['w'])}px;height:{f(g['h'])}px"
        style_frame = f"left:{f(g['left'])}px;top:{f(g['top'])}px;width:{f(g['w'])}px;height:{f(g['h'])}px"
        strip.append(
            f'<video id="strip-{k:02d}" class="clip" src="assets/video/desk.mp4" data-start="{f(a)}" data-duration="{f(b - a)}" '
            f'data-media-start="{f(m)}" data-playback-rate="{STRIP_RATE}" data-track-index="3" muted playsinline style="{style_card}"></video>'
        )
        pop.append(
            f'<video id="pop-{k:02d}" class="clip" src="assets/video/desk-cutout.webm" data-start="{f(a)}" data-duration="{f(b - a)}" '
            f'data-media-start="{f(m)}" data-playback-rate="{STRIP_RATE}" data-track-index="4" muted playsinline style="{style_frame}"></video>'
        )
    return strip, pop


# ---------------- captions: one word at a time (the reference's median is 0.33s), hard swaps ----------------
# Display tokens are the spoken words with the script's punctuation. A few pairs read as one unit, as in the
# reference ("6 ways", "the hook"): number + noun, and a short function word glued to the next word when they run
# together. The coined term and the CTA keyword get their own serif italic caption.
SHORT = {"a", "the", "to", "is", "no", "my", "it", "i", "of", "in", "not", "you", "and", "it's", "what"}
NUMBERS = {"three": "3", "ten": "10"}
TERM = ("the", "gallery", "portfolio", "trap")         # "the gallery-portfolio trap."
CTA = ("comment", "portfolio")                           # Comment "PORTFOLIO",


def display_tokens():
    raw = re.findall(r"\S+", SPOKEN)
    toks = []
    for w in raw:
        n = len(re.findall(r"[a-z']+", w.lower()))
        toks.append((w, n))
    return toks


def clean(w):
    return re.sub(r"[^a-z']", "", w.lower())


def build_caps():
    toks = display_tokens()
    total = sum(n for _, n in toks)
    assert total == len(WORDS), f"display tokens cover {total} words, transcript has {len(WORDS)}"
    items, wi = [], 0
    for disp, n in toks:
        items.append({"t": disp, "s": WORDS[wi]["start"], "e": WORDS[wi + n - 1]["end"], "w": [WORDS[j]["text"] for j in range(wi, wi + n)]})
        wi += n
    groups, i = [], 0
    while i < len(items):
        it = items[i]
        words = [x for g in items[i:i + 3] for x in g["w"]]
        if tuple(words[:4]) == TERM:
            groups.append({"items": items[i:i + 3], "style": "term"})   # "the" "gallery-portfolio" "trap."
            i += 3
            continue
        if tuple(x for g in items[i:i + 2] for x in g["w"]) == CTA:
            groups.append({"items": items[i:i + 2], "style": "cta"})
            i += 2
            continue
        g = [it]
        if it["t"].startswith('"') and not re.search(r'"[.,:!?…]*$', it["t"]):   # a quoted phrase stays one caption
            j = i + 1
            while j < len(items) and not re.search(r'"[.,:!?…]*$', items[j - 1]["t"]):
                g.append(items[j])
                j += 1
            groups.append({"items": g, "style": "s"})
            i += len(g)
            continue
        nxt = items[i + 1] if i + 1 < len(items) else None
        starts_special = nxt is not None and (
            tuple(x for gg in items[i + 1:i + 4] for x in gg["w"])[:4] == TERM
            or tuple(x for gg in items[i + 1:i + 3] for x in gg["w"]) == CTA)
        if nxt and not starts_special and not re.search(r"[.,:!?…]$", it["t"]) and nxt["s"] - it["e"] < 0.1:
            num = clean(it["t"]) in NUMBERS
            short = clean(it["t"]) in SHORT and len(clean(nxt["t"])) <= 12 and nxt["e"] - it["s"] < 0.75
            if num or short:
                g.append(nxt)
        groups.append({"items": g, "style": "s"})
        i += len(g)
    # a caption on screen for less than ~0.15s only flickers: fold it into the next one ("which I corrected",
    # "they don't know"); a word right before the coined term just starts the term's caption earlier
    merged = []
    for k, gr in enumerate(groups):
        nxt = groups[k + 1] if k + 1 < len(groups) else None
        dur = (nxt["items"][0]["s"] - gr["items"][0]["s"]) if nxt else 1.0
        if merged and merged[-1].get("carry"):
            gr = {"items": merged[-1]["items"] + gr["items"], "style": gr["style"], "drop": merged[-1].get("drop_text")}
            merged.pop()
        if nxt and dur < 0.15 and gr["style"] == "s":
            if nxt["style"] == "s":
                if sum(len(x["w"]) for x in gr["items"] + nxt["items"]) <= 3:
                    gr = dict(gr, carry=True)
            else:
                gr = dict(gr, carry=True, drop_text=True)
        merged.append(gr)
    groups = [g for g in merged if not g.get("carry")]
    out = []
    starts = [max(gr["items"][0]["s"] - 0.04, 0.0) for gr in groups]
    for k, gr in enumerate(groups):
        g = gr["items"]
        sc = scene_at(g[0]["s"] + 0.06)
        a = max(starts[k], sc[1]) if sc[3] == "cut" else starts[k]
        last_end = g[-1]["e"]
        if k + 1 < len(groups):
            nxt = starts[k + 1]
            b = nxt if nxt - last_end < 0.7 else last_end + 0.3
            if scene_at(groups[k + 1]["items"][0]["s"] + 0.06)[3] != sc[3]:
                b = min(b, sc[2])
        else:
            b = DURATION
        words = []
        for j, x in enumerate(g):
            t = x["t"]
            key = clean(t)
            if key in NUMBERS and j == 0 and len(g) == 2:    # "3 mistakes", "10 projects", "3 points"
                t = NUMBERS[key] + re.sub(r"^[A-Za-z']+", "", t)
            t = re.sub(r'^"', "“", t)
            t = re.sub(r'"([.,:!?…]*)$', r"”\1", t)
            words.append(t)
        pos = "center" if sc[3] == "cut" else "seam"
        if gr["style"] == "term":
            html = '<span class="t">The Gallery-Portfolio Trap.</span>'
        elif gr["style"] == "cta":
            html = '<span class="t">Comment</span><span class="t k">“Portfolio”</span>'
        else:
            html = f'<span class="t">{" ".join(words)}</span>'
        out.append(f'<div id="cap-{k:03d}" class="cap clip {pos} {gr["style"]}" data-start="{f(a)}" data-duration="{f(b - a)}" '
                   f'data-track-index="0">{html}</div>')
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
      <div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="{f(DURATION)}">
{body}
      </div>
      <script>
        (function () {{
          // the reference swaps caption words with no entrance animation: the timeline only exists to be registered
          const tl = gsap.timeline({{ paused: true }});
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


CAP_CSS = """
        #root { position: absolute; inset: 0; pointer-events: none; }
        .cap { position: absolute; left: 40px; width: 1000px; height: 120px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .cap.seam { top: 1225px; }
        .cap.center { top: 1225px; }
        .cap .t { display: block; white-space: nowrap; font-family: "Inter Tight", Arial, sans-serif; font-weight: 800;
          font-size: 53px; letter-spacing: -0.03em; line-height: 1; color: #fbfbfb;
          text-shadow: 0 3px 14px rgba(0,0,0,0.7), 0 1px 3px rgba(0,0,0,0.6); }
        .cap.center .t { font-size: 68px; }
        .cap.term .t { font-family: "Instrument Serif", Georgia, serif; font-style: italic; font-weight: 400; font-size: 90px; letter-spacing: -0.01em; }
        .cap.cta { top: 1190px; height: 190px; }
        .cap.cta .t { font-size: 68px; }
        .cap.cta .t.k { margin-top: 6px; font-family: "Instrument Serif", Georgia, serif; font-style: italic; font-weight: 400; font-size: 92px; letter-spacing: -0.01em; }"""


# ---------------- SFX (the reference: a low whoosh ~0.2s before each graphic change; soft pops on tags) ----------------
# (time, file in assets/sfx, volume). Every volume is scaled by SFX_GAIN, the quieter level the user asked for on
# reel 3 (about 20 dB under the voice).
SFX_GAIN = 0.45
SWOOSH = [s[1] - 0.2 for s in SCENES if s[3] == "panel" and s[1] > 0.5]
SFX = [
    *[(t, "whoosh-low", 0.22) for t in SWOOSH],
    # b01: likes, the inbox slides in, the 0 badge and its ping
    (0.76, "pop", 0.1), (1.95, "whoosh-low", 0.12), (2.45, "pop", 0.18), (2.95, "whoosh-low", 0.1),
    # b03: the list builds, row 01 lights
    (6.30, "click-soft", 0.25), (8.95, "click-soft", 0.3),
    # b04: the client, the question, the missing results, the ping
    (11.60, "pop", 0.14), (11.87, "click-soft", 0.25), (12.79, "pop", 0.14), (13.05, "whoosh-low", 0.1),
    # b05 / b08: hub returns light a row
    (13.56, "click-soft", 0.3), (20.45, "click-soft", 0.3),
    # b06: bio boxed, clients, strike, the ping
    (15.91, "click-soft", 0.22), (16.30, "pop", 0.12), (17.04, "click", 0.3), (17.72, "whoosh-low", 0.1),
    # b09: scroll, ten projects, zero buttons, the swipe, the question, the ping
    (22.20, "whoosh-low", 0.1), (22.37, "pop", 0.16), (23.10, "pop", 0.16), (24.44, "whoosh-low", 0.16), (25.22, "click-soft", 0.25), (25.78, "whoosh-low", 0.1),
    # b10: the rope, the exhibit light
    (26.85, "click-soft", 0.18), (28.03, "ping", 0.1),
    # b11: the three fixes, the green flash, step-by-step, the new message
    (29.75, "click-soft", 0.22), (29.95, "click-soft", 0.22), (30.12, "pop", 0.18), (30.34, "ping", 0.08), (31.06, "pop", 0.18), (32.30, "ping", 0.14), (32.66, "whoosh-low", 0.1),
    # b13: the comment is posted, the waitlist button
    (35.29, "click-soft", 0.25), (35.43, "pop", 0.22),
]
SFX_LEN = {}


def sfx_len(name):
    if name not in SFX_LEN:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                              str(ROOT / f"assets/sfx/{name}.mp3")], capture_output=True, text=True, check=True).stdout
        SFX_LEN[name] = round(float(out), 2)
    return SFX_LEN[name]


def build_audio():
    out, lanes_end = [], []
    for k, (t, name, vol) in enumerate(sorted(SFX)):
        length = min(sfx_len(name), DURATION - t)
        lane = next((i for i, end in enumerate(lanes_end) if end <= t + 1e-6), None)
        if lane is None:
            lanes_end.append(0.0)
            lane = len(lanes_end) - 1
        lanes_end[lane] = t + length
        out.append(f'<audio id="sfx-{k:03d}-{name}" src="assets/sfx/{name}.mp3" data-start="{f(t)}" data-duration="{f(length)}" '
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
