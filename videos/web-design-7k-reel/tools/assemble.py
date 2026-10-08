#!/usr/bin/env python3
"""Assemble index.html: scene slots, footage strip clips, caption groups and SFX.

Timing source: transcript.json (voice-over aligned word by word). Re-run after editing any table below:
    python3 tools/assemble.py
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORDS = json.loads((ROOT / "transcript.json").read_text())
DURATION = 64.0

# (id, start, end, kind) — kind: dark | light | cut. Each scene starts ~0.1s before its first word.
SCENES = [
    ("f01-hook", 0.00, 5.86, "dark"),
    ("f02-not-much", 5.86, 12.06, "light"),
    ("f03-cut-for-me", 12.06, 14.68, "cut"),
    ("f04-figured-out", 14.68, 18.50, "dark"),
    ("f05-views-bank", 18.50, 24.90, "dark"),
    ("f06-tried-everything", 24.90, 34.30, "dark"),
    ("f07-cut-questioned", 34.30, 37.18, "cut"),
    ("f08-rebuild", 37.18, 40.66, "dark"),
    ("f09-cut-hit", 40.66, 42.44, "cut"),
    ("f10-problem-me", 42.44, 47.10, "light"),
    ("f11-lesson", 47.10, 54.72, "light"),
    ("f12-unfiltered", 54.72, 58.52, "dark"),
    ("f13-cta", 58.52, DURATION, "dark"),
]

# Footage strip windows (panel scenes only) and the B-roll source offset each one plays from.
# The B-roll is 26.77s, so windows reuse its steady section (4.6s onward); the 0–4.5s moves are cutaways.
STRIP = [
    ("a", 0.00, 12.06, 4.60),
    ("b", 14.68, 34.30, 7.00),
    ("c", 37.18, 40.66, 20.00),
    ("d", 42.44, DURATION, 5.00),
]

# Caption groups: (first word idx, last word idx, display text, style). s=sans, i=serif italic,
# n=heavy number/punch, r=red serif.
CAPS = [
    (0, 1, "I made", "s"),
    (2, 4, "$7,000", "n"),
    (5, 7, "on a single", "s"),
    (8, 10, "web design project.", "s"),
    (11, 11, "Now,", "s"),
    (12, 13, "I know...", "s"),
    (14, 17, "for some of you,", "s"),
    (18, 20, "that's not much.", "i"),
    (21, 23, "It might even", "s"),
    (24, 24, "sound", "s"),
    (25, 25, "ridiculous.", "i"),
    (26, 28, "But for me?", "s"),
    (29, 30, "It's what", "s"),
    (31, 32, "changed everything.", "i"),
    (33, 35, "Because before that,", "s"),
    (36, 37, "I thought", "s"),
    (38, 41, "I had it all", "s"),
    (42, 43, "figured out.", "i"),
    (44, 45, "I had", "s"),
    (46, 46, "millions", "i"),
    (47, 48, "of views", "s"),
    (49, 50, "on Instagram...", "s"),
    (51, 52, "and yet,", "s"),
    (53, 55, "my bank account", "s"),
    (56, 57, "still showed", "s"),
    (58, 59, "zero dollars.", "r"),
    (60, 62, "So I tried", "s"),
    (63, 63, "everything.", "i"),
    (64, 64, "Fiverr.", "s"),
    (65, 65, "Upwork.", "s"),
    (66, 68, "Mass cold emails.", "s"),
    (69, 70, "And every", "s"),
    (71, 72, "single time,", "s"),
    (73, 74, "nothing but", "s"),
    (75, 75, "silence.", "i"),
    (76, 78, "At that point,", "s"),
    (79, 80, "I questioned", "s"),
    (81, 81, "everything.", "i"),
    (82, 84, "I even stopped", "s"),
    (85, 85, "posting", "s"),
    (86, 88, "for a while,", "s"),
    (89, 91, "just to rebuild", "s"),
    (92, 93, "from scratch.", "i"),
    (94, 96, "And that's when", "s"),
    (97, 99, "it hit me.", "n"),
    (100, 103, "I had to stop", "s"),
    (104, 105, "looking for", "s"),
    (106, 108, "the fault elsewhere.", "s"),
    (109, 110, "The problem", "s"),
    (111, 112, "was me.", "i"),
    (113, 115, "That's when I", "s"),
    (116, 117, "finally understood", "s"),
    (118, 118, "something:", "s"),
    (119, 121, "design isn't just", "s"),
    (122, 122, "about", "s"),
    (123, 123, "aesthetics.", "i"),
    (124, 127, "It has to be", "s"),
    (128, 128, "effective", "i"),
    (129, 130, "for a", "s"),
    (131, 132, "specific profile.", "i"),
    (133, 134, "So today,", "s"),
    (135, 137, "I'm coming back", "s"),
    (138, 140, "to tell you", "s"),
    (141, 141, "everything,", "s"),
    (142, 142, "unfiltered.", "i"),
    (143, 145, "And if you're", "s"),
    (146, 148, "a web designer", "s"),
    (149, 151, "who wants to", "s"),
    (152, 152, "land", "s"),
    (153, 154, "real contracts", "i"),
    (155, 158, "in the coming weeks...", "s"),
    (159, 159, "subscribe.", "n"),
]

# SFX: (global time, file in assets/sfx, volume, optional clip length)
SFX = [
    (0.18, "whoosh-short", 0.30),
    (1.22, "whoosh", 0.26),
    (1.34, "typing", 0.14),
    (2.90, "ping", 0.30),
    (3.25, "whoosh-short", 0.28),
    (3.88, "pop", 0.32),
    (4.52, "click-soft", 0.32),
    (5.86, "whoosh", 0.30),
    (7.86, "pop", 0.30),
    (8.99, "pop", 0.30),
    (10.14, "pop", 0.30),
    (11.18, "pop", 0.34),
    (12.06, "impact-bass-2", 0.06, 1.4),
    (14.68, "whoosh-short", 0.30),
    (16.28, "click-soft", 0.38),
    (17.34, "click-soft", 0.38),
    (18.00, "click-soft", 0.38),
    (18.50, "whoosh", 0.28),
    (19.27, "typing", 0.14),
    (21.32, "whoosh-short", 0.28),
    (21.62, "pop", 0.30),
    (24.02, "error", 0.30),
    (24.90, "whoosh", 0.28),
    (26.48, "pop", 0.26),
    (27.10, "click", 0.34),
    (28.17, "click", 0.34),
    (29.00, "click", 0.34),
    (30.84, "key-press", 0.45),
    (31.25, "key-press", 0.45),
    (31.65, "key-press", 0.45),
    (32.26, "whoosh-short", 0.16),
    (34.30, "impact-bass-2", 0.05, 1.4),
    (37.18, "whoosh-short", 0.28),
    (37.52, "click", 0.34),
    (39.55, "typing", 0.14),
    (40.62, "whoosh-cinematic", 0.30, 1.9),
    (41.80, "impact-bass-1", 0.18, 1.5),
    (42.44, "whoosh", 0.28),
    (44.02, "click-soft", 0.30),
    (44.17, "click-soft", 0.30),
    (44.32, "click-soft", 0.30),
    (44.47, "click-soft", 0.30),
    (45.05, "whoosh-short", 0.28),
    (46.28, "pop", 0.34),
    (47.10, "whoosh", 0.26),
    (49.29, "pop", 0.28),
    (51.00, "sparkle", 0.20),
    (52.48, "ping", 0.28),
    (53.28, "whoosh-short", 0.24),
    (54.13, "click", 0.34),
    (54.72, "whoosh", 0.28),
    (55.74, "pop", 0.26),
    (57.68, "click", 0.40),
    (57.72, "whoosh-short", 0.28),
    (57.80, "sparkle", 0.18),
    (58.52, "whoosh", 0.28),
    (60.20, "typing", 0.14),
    (61.30, "chime", 0.20),
    (61.52, "click-soft", 0.30),
    (61.85, "click-soft", 0.30),
    (62.12, "click-soft", 0.30),
    (62.50, "pop", 0.40),
    (62.90, "click", 0.45),
    (63.04, "notification", 0.24),
]

SFX_LEN = {}  # filled from ffprobe-free table below (seconds, from the bundled library)
SFX_LEN.update(
    {
        "sparkle": 1.80, "key-press": 0.43, "typing": 1.54, "whoosh": 0.57, "whoosh-cinematic": 5.54,
        "chime": 2.54, "error": 1.62, "glitch-1": 2.64, "impact-bass-1": 2.12, "notification": 2.46,
        "click-soft": 0.37, "pop": 0.72, "click": 0.37, "impact-bass-2": 2.59, "whoosh-short": 0.57,
        "riser": 10.03, "ping": 1.32,
    }
)


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
            f'<div id="el-{sid}" class="{cls}" data-composition-id="{sid}" '
            f'data-composition-src="compositions/{sid}.html" data-start="{f(a)}" '
            f'data-duration="{f(b - a)}" data-track-index="1" data-width="1080" data-height="1920"></div>'
        )
    return out


def build_strip():
    strip, pop = [], []
    for key, a, b, m in STRIP:
        d = b - a
        strip.append(
            f'<video id="strip-{key}" class="clip" src="assets/video/broll.mp4" data-start="{f(a)}" '
            f'data-duration="{f(d)}" data-media-start="{f(m)}" data-track-index="3" muted playsinline></video>'
        )
        pop.append(
            f'<video id="pop-{key}" class="clip" src="assets/video/broll-cutout.webm" data-start="{f(a)}" '
            f'data-duration="{f(d)}" data-media-start="{f(m)}" data-track-index="4" muted playsinline></video>'
        )
    return strip, pop


CAP_CSS = """
        #captions-root {
          position: absolute;
          inset: 0;
          pointer-events: none;
        }
        .cap {
          position: absolute;
          left: 40px;
          width: 1000px;
          height: 120px;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .cap.seam {
          top: 1208px;
        }
        .cap.center {
          top: 1090px;
        }
        .cap .t {
          display: block;
          white-space: nowrap;
          font-family: "Inter Tight", Arial, sans-serif;
          font-weight: 700;
          font-size: 64px;
          letter-spacing: -0.03em;
          line-height: 1;
          color: #f4f3f1;
          text-shadow:
            0 4px 22px rgba(0, 0, 0, 0.6),
            0 1px 3px rgba(0, 0, 0, 0.5);
        }
        .cap.light .t {
          color: #111111;
          text-shadow: 0 2px 14px rgba(255, 255, 255, 0.55);
        }
        .cap.center .t {
          font-size: 74px;
          text-shadow:
            0 6px 30px rgba(0, 0, 0, 0.75),
            0 2px 4px rgba(0, 0, 0, 0.6);
        }
        .cap.i .t {
          font-family: "Instrument Serif", Georgia, serif;
          font-style: italic;
          font-weight: 400;
          font-size: 80px;
          letter-spacing: -0.01em;
        }
        .cap.center.i .t {
          font-size: 92px;
        }
        .cap.n .t {
          font-weight: 900;
          font-size: 80px;
          letter-spacing: -0.04em;
        }
        .cap.center.n .t {
          font-size: 96px;
        }
        .cap.r .t {
          font-family: "Instrument Serif", Georgia, serif;
          font-style: italic;
          font-weight: 400;
          font-size: 84px;
          letter-spacing: -0.01em;
          color: #ff3b3f;
          text-shadow: 0 0 28px rgba(227, 25, 31, 0.55);
        }"""


def build_caps():
    """Write compositions/captions.html: one full-length sub-composition holding every caption group."""
    groups = []
    starts = [max(WORDS[s]["start"] - 0.05, 0.0) for s, *_ in CAPS]
    for k, (s, e, text, style) in enumerate(CAPS):
        a = starts[k]
        sc = scene_at(WORDS[s]["start"])
        last_end = WORDS[e]["end"]
        if k + 1 < len(CAPS):
            nxt = starts[k + 1]
            b = nxt if nxt - last_end < 0.8 else last_end + 0.35
            nsc = scene_at(WORDS[CAPS[k + 1][0]]["start"])
            if nsc[3] != sc[3]:
                b = min(b, sc[2])
        else:
            b = DURATION
        pos = "center" if sc[3] == "cut" else "seam"
        light = " light" if sc[3] == "light" else ""
        groups.append(
            f'<div id="cap-{k:02d}" class="cap clip {pos}{light} {style}" data-start="{f(a)}" '
            f'data-duration="{f(b - a)}" data-track-index="0"><span class="t">{text}</span></div>'
        )
    fonts = (ROOT / "tools/fonts.css.snippet").read_text()
    body = "\n".join(f"          {g}" for g in groups)
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <!-- Generated by tools/assemble.py from transcript.json. Edit CAPS there, not here. -->
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
          // every caption group springs in at its own start (read once from static attributes)
          document.querySelectorAll("#captions-root .cap").forEach((cap) => {{
            const at = parseFloat(cap.getAttribute("data-start"));
            const t = cap.querySelector(".t");
            const big = cap.classList.contains("n");
            tl.fromTo(
              t,
              {{ opacity: 0, y: 16, scale: big ? 0.7 : 0.9, filter: "blur(8px)" }},
              {{
                opacity: 1,
                y: 0,
                scale: 1,
                filter: "blur(0px)",
                duration: big ? 0.24 : 0.16,
                ease: big ? "back.out(2.2)" : "power2.out",
              }},
              at,
            );
          }});
          window.__timelines["captions"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""
    (ROOT / "compositions/captions.html").write_text(html)
    slot = (
        f'<div id="el-captions" class="captions" data-composition-id="captions" '
        f'data-composition-src="compositions/captions.html" data-start="0" data-duration="{f(DURATION)}" '
        f'data-track-index="5" data-track-kind="captions" data-width="1080" data-height="1920"></div>'
    )
    return [slot]


def build_audio():
    out = []
    lanes_end = []  # greedy track assignment so no two SFX overlap on one track
    for k, item in enumerate(SFX):
        t, name, vol = item[0], item[1], item[2]
        length = item[3] if len(item) > 3 else SFX_LEN[name]
        length = min(length, DURATION - t)
        lane = next((i for i, end in enumerate(lanes_end) if end <= t + 1e-6), None)
        if lane is None:
            lanes_end.append(0.0)
            lane = len(lanes_end) - 1
        lanes_end[lane] = t + length
        auto = ""
        if len(item) > 3:  # trimmed clip: fade the tail
            env = {"version": 1, "lanes": [{"target": "volume", "points": [
                {"t": 0, "v": 1}, {"t": round(length - 0.4, 2), "v": 1}, {"t": round(length, 2), "v": 0}]}]}
            auto = f" data-automation='{json.dumps(env, separators=(',', ':'))}'"
        out.append(
            f'<audio id="sfx-{k:02d}-{name}" src="assets/sfx/{name}.mp3" data-start="{f(t)}" '
            f'data-duration="{f(length)}" data-track-index="{21 + lane}" data-volume="{vol}"{auto}></audio>'
        )
    return out


def inject(html, tag, lines, indent):
    pat = re.compile(rf"(<!-- {tag}:BEGIN -->)(.*?)(\n\s*<!-- {tag}:END -->)", re.S)
    body = "".join(f"\n{indent}{line}" for line in lines)
    return pat.sub(lambda m: m.group(1) + body + m.group(3), html)


def main():
    path = ROOT / "index.html"
    html = path.read_text()
    strip, pop = build_strip()
    html = inject(html, "SCENES", build_scenes(), "      ")
    html = inject(html, "STRIP", strip, "          ")
    html = inject(html, "POPOUT", pop, "        ")
    html = inject(html, "CAPSLOT", build_caps(), "      ")
    html = inject(html, "AUDIO", build_audio(), "      ")
    path.write_text(html)
    print(f"scenes={len(SCENES)} strip={len(strip)} captions={len(CAPS)} sfx={len(SFX)}")


if __name__ == "__main__":
    main()
