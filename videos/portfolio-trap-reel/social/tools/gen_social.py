#!/usr/bin/env python3
"""Story and carousel stills for the gallery-portfolio-trap reel, in its lockin-red style (styles/lockin-red/STYLE.md).

Each still is a static HTML page built from the reels' pieces, and tools/render_social.mjs screenshots it:
- 4 stories at 1080x1920. Key content stays inside y 250-1650, clear of Instagram's profile bar and reply field.
- 4 carousel slides at 1080x1350 (4:5).

Copy follows the script (tools/spoken.txt). The pages load /assets/... from the reel's project root, which the
render script serves.
    python3 social/tools/gen_social.py && node social/tools/render_social.mjs
"""
import pathlib

SOCIAL = pathlib.Path(__file__).resolve().parent.parent
PAGES = SOCIAL / "pages"

FONTS = """
      @font-face { font-family: "Inter Tight"; src: url("/assets/fonts/inter-tight-latin-700-normal.woff2") format("woff2"); font-weight: 700; font-style: normal; }
      @font-face { font-family: "Inter Tight"; src: url("/assets/fonts/inter-tight-latin-800-normal.woff2") format("woff2"); font-weight: 800; font-style: normal; }
      @font-face { font-family: "Inter Tight"; src: url("/assets/fonts/inter-tight-latin-900-normal.woff2") format("woff2"); font-weight: 900; font-style: normal; }
      @font-face { font-family: "Instrument Serif"; src: url("/assets/fonts/instrument-serif-latin-400-italic.woff2") format("woff2"); font-weight: 400; font-style: italic; }"""

BASE_CSS = """
      html, body { margin: 0; padding: 0; background: #000; }
      #root { position: relative; overflow: hidden; background: #000; }
      .tt { position: absolute; left: 30px; right: 30px; display: flex; flex-direction: column; align-items: center; font-family: "Inter Tight", Arial, sans-serif;
        font-weight: 800; letter-spacing: -0.03em; line-height: 1.06; color: #fbfbfb; text-shadow: 0 2px 10px rgba(0,0,0,0.6); white-space: nowrap; }
      .tt .l2 { position: relative; padding: 0 16px; margin-top: 2px; }
      .tt .l2 .bar { position: absolute; left: 0; right: 0; top: 7%; bottom: 0; background: #b80000; }
      .tt .l2 .tx { position: relative; }
      .it { font-family: "Instrument Serif", Georgia, serif; font-style: italic; font-weight: 400; letter-spacing: -0.01em; }
      .big { font-family: "Inter Tight", Arial, sans-serif; font-weight: 900; letter-spacing: -0.04em; line-height: 0.9; color: #fbfbfb; white-space: nowrap; }
      .body { position: absolute; left: 80px; right: 80px; text-align: center; font-family: "Inter Tight", Arial, sans-serif; font-weight: 700;
        letter-spacing: -0.015em; line-height: 1.25; color: #e6e6e6; }
      .cx { position: absolute; left: 0; right: 0; display: flex; justify-content: center; align-items: center; gap: 26px; }
      .cx > * { position: relative; }
      .chk { width: 76px; height: 76px; border-radius: 50%; background: #18de3a; box-shadow: 0 0 20px rgba(24,222,58,0.6); flex: none; }
      .chk svg { width: 100%; height: 100%; display: block; }
      .cl { width: 116px; height: 116px; border-radius: 50%; flex: none; background: radial-gradient(circle at 35% 30%, #ff4a3a 0%, #c00000 45%, #6a0000 100%);
        box-shadow: 0 0 0 4px rgba(255,255,255,0.85), 0 0 28px rgba(220,0,0,0.6), 0 16px 30px rgba(0,0,0,0.6); }
      .cl svg { position: absolute; left: 18%; top: 16%; width: 64%; height: 64%; }
      .strike { position: absolute; height: 16px; border-radius: 8px; background: #e0324f; box-shadow: 0 0 18px rgba(224,50,79,0.7); }
      .swipe { position: absolute; right: 64px; display: flex; align-items: center; gap: 14px; font: 800 36px/1 "Inter Tight", Arial, sans-serif; color: #fbfbfb; letter-spacing: -0.01em; }
      .swipe svg { width: 54px; height: 30px; }
      .crumb { left: 110px; width: 860px; height: 136px; }
      .crumb .num { font-size: 58px; width: 130px; }
      .crumb .lbl { font-size: 40px; }"""

CHECK = '<svg viewBox="0 0 40 40"><path d="M11 21 L18 28 L30 13" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PERSON = '<svg viewBox="0 0 60 60"><circle cx="30" cy="22" r="11" fill="#ffffff"/><path d="M10 54 C 12 40, 48 40, 50 54 Z" fill="#ffffff"/></svg>'
MAIL = '<svg width="44" height="34" viewBox="0 0 34 26"><rect x="2" y="2" width="30" height="22" rx="3" fill="none" stroke="#fff" stroke-width="3"/><path d="M3 4 L17 15 L31 4" fill="none" stroke="#fff" stroke-width="3"/></svg>'
ARROW = '<svg viewBox="0 0 54 30"><path d="M2 15 H48 M36 3 L50 15 L36 27" fill="none" stroke="#fbfbfb" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SWIPE = f'<div class="swipe" style="bottom: 56px">Swipe {ARROW}</div>'

THUMBS = [
    ("linear-gradient(140deg, #e8dcc8 0%, #b89a76 100%)", "radial-gradient(circle at 70% 35%, #2b2b2b 0 18%, transparent 19%)"),
    ("linear-gradient(160deg, #18323f 0%, #4f8796 100%)", "linear-gradient(0deg, rgba(255,255,255,0.85) 0 12%, transparent 12%)"),
    ("linear-gradient(135deg, #2a2a2e 0%, #5d5d66 100%)", "radial-gradient(circle at 35% 60%, #e2b64e 0 22%, transparent 23%)"),
    ("linear-gradient(150deg, #f1ece4 0%, #d6cbbb 100%)", "linear-gradient(90deg, transparent 0 55%, #b2472f 55% 75%, transparent 75%)"),
]


def title(l1, l2, top, size):
    return (f'<div class="tt" style="top: {top}px; font-size: {size}px"><span>{l1}</span>'
            f'<span class="l2"><span class="bar"></span><span class="tx">{l2}</span></span></div>')


def crumb(n, label, top=70):
    return (f'<div class="lr-crumb crumb" style="top: {top}px"><span class="edge"></span>'
            f'<span class="num">{n}</span><span class="lbl">{label}</span></div>')


def page(name, w, h, css, body):
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <!-- Generated by social/tools/gen_social.py: edit the generator, not this file. -->
    <link rel="stylesheet" href="/assets/css/lockin.css" />
    <style>{FONTS}{BASE_CSS}
      html, body, #root {{ width: {w}px; height: {h}px; }}
{css}
    </style>
  </head>
  <body>
    <div id="root">
      <div class="lr-bg"></div>
{body}
    </div>
  </body>
</html>
"""
    (PAGES / f"{name}.html").write_text(html)


# ---------------------------------------------------------------- the phone portfolio (from trial edit B)
PHONE_CSS = """
      .ph { position: absolute; width: 430px; height: 880px; border-radius: 66px; background: #070707; border: 2px solid rgba(255,255,255,0.62);
        box-shadow: 0 0 0 8px #141416, 0 0 0 10px rgba(255,255,255,0.16), 0 0 46px rgba(255,255,255,0.13), 0 40px 90px rgba(0,0,0,0.75); }
      .ph .scr { position: absolute; left: 14px; top: 14px; width: 402px; height: 852px; border-radius: 54px; overflow: hidden; background: #f4f4f2; }
      .ph .isl { position: absolute; left: 156px; top: 26px; width: 118px; height: 34px; border-radius: 17px; background: #050505; display: block; }
      .pg i, .pg b { display: block; position: absolute; }
      .pg .tm { position: absolute; left: 44px; top: 18px; font: 700 21px/1 "Inter Tight", Arial, sans-serif; color: #111; }
      .pg .bat { right: 38px; top: 19px; width: 34px; height: 16px; border-radius: 5px; border: 2px solid #111; }
      .pg .av { left: 24px; top: 62px; width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(140deg, #4f8796, #18323f); }
      .pg .nm { left: 76px; top: 75px; width: 130px; height: 14px; border-radius: 7px; background: #cfcdc8; }
      .pg .h { position: absolute; left: 24px; top: 116px; font: 800 26px/1 "Inter Tight", Arial, sans-serif; letter-spacing: -0.02em; color: #111; }
      .pg .th { border-radius: 10px; width: 171px; height: 124px; }
      .pg .k { position: absolute; left: 24px; font: 700 15px/1 "Inter Tight", Arial, sans-serif; letter-spacing: 0.12em; text-transform: uppercase; color: #6b6b6b; }
      .pg .bio { position: absolute; left: 24px; font: 800 32px/1 "Inter Tight", Arial, sans-serif; letter-spacing: -0.02em; color: #111; white-space: nowrap; }
      .pg .ln { left: 24px; height: 11px; border-radius: 6px; background: #d6d4cf; }"""


def phone(left, top):
    th = "".join(f'<i class="th" style="left: {24 + (i % 2) * 183}px; top: {156 + (i // 2) * 136}px; background: {m}, {b}"></i>'
                 for i, (b, m) in enumerate(THUMBS))
    pg = (f'<div class="pg"><span class="tm">9:41</span><i class="bat"></i><i class="av"></i><i class="nm"></i>'
          f'<div class="h">Selected Work</div>{th}'
          '<div class="k" style="top: 446px">About</div><div class="bio" style="top: 474px">Versatile Creative</div>'
          '<i class="ln" style="top: 522px; width: 300px"></i><i class="ln" style="top: 542px; width: 230px"></i>'
          '<div class="k" style="top: 596px">Contact</div>'
          '<i class="ln" style="top: 756px; width: 190px"></i><i class="ln" style="top: 776px; width: 140px"></i></div>')
    return f'<div class="ph" style="left: {left}px; top: {top}px"><div class="scr">{pg}</div><i class="isl"></i></div>'


def main():
    PAGES.mkdir(exist_ok=True)

    # ================================================================ STORIES (1080x1920)
    # S1: the hook, on the face
    page("story-1", 1080, 1920, """
      .card { position: absolute; left: 90px; top: 470px; width: 900px; height: 1010px; border-radius: 36px; overflow: hidden; background: #141414;
        box-shadow: 0 -18px 70px rgba(0,0,0,0.55), 0 0 30px rgba(255,255,255,0.06); }
      .card img { position: absolute; left: 0; top: 0; width: 900px; height: 1010px; object-fit: cover; }
      .card .edge { position: absolute; inset: 0; border-radius: 36px; box-shadow: inset 0 2px 0 rgba(255,255,255,0.22), inset 0 0 0 2px rgba(255,255,255,0.1); }
      .card .shade { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0) 62%, rgba(0,0,0,0.45) 100%); }
      .pill { display: flex; align-items: center; gap: 16px; padding: 16px 34px 18px; border-radius: 48px; background: #b80000;
        box-shadow: 0 0 34px rgba(184,0,0,0.6), 0 14px 30px rgba(0,0,0,0.6); font: 800 50px/1 "Inter Tight", Arial, sans-serif; letter-spacing: -0.02em; color: #fff; }
      .tap { gap: 16px; font: 700 46px/1 "Inter Tight", Arial, sans-serif; letter-spacing: -0.015em; color: #e6e6e6; }
      .tap svg { width: 54px; height: 30px; }""", f"""
      {title("Your Portfolio Is Beautiful…", "But No Client Writes.", 250, 66)}
      <div class="card"><img src="/social/img/face-chin.jpg" alt="" /><div class="shade"></div><div class="edge"></div></div>
      <div class="cx" style="top: 1432px"><div class="pill">{MAIL}<span>0 Messages</span></div></div>
      <div class="cx tap" style="top: 1588px">Tap to see why {ARROW}</div>""")

    # S2: the gallery-portfolio trap: the phone on show behind a museum rope
    page("story-2", 1080, 1920, PHONE_CSS + """
      .post { position: absolute; top: 1135px; width: 24px; height: 300px; border-radius: 6px; background: linear-gradient(90deg, #5e4a1c 0%, #e3c46a 45%, #8a6a22 100%); }
      .foot { position: absolute; top: 1422px; width: 100px; height: 18px; border-radius: 9px; background: linear-gradient(180deg, #d9b95e, #6b5420); }
      .knob { position: absolute; top: 1108px; width: 44px; height: 44px; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #fff1b8 0%, #c9a646 50%, #6b5420 100%); }
      .rope { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
      .plq { position: absolute; left: 810px; top: 820px; width: 160px; height: 90px; border-radius: 3px; background: #e9e6e0; padding: 18px 16px; box-sizing: border-box; box-shadow: 0 10px 22px rgba(0,0,0,0.55); }
      .plq i { display: block; height: 8px; border-radius: 3px; background: #9a9a9a; margin-bottom: 10px; filter: blur(0.8px); }
      .spot { position: absolute; left: 100px; top: 420px; width: 880px; height: 1100px; background: radial-gradient(ellipse 44% 52% at 50% 38%, rgba(255,250,235,0.34) 0%, rgba(255,250,235,0) 70%); }""", f"""
      <div class="spot"></div>
      {phone(325, 520)}
      <div class="plq"><i style="width: 118px"></i><i style="width: 84px"></i><i style="width: 100px"></i></div>
      <i class="post" style="left: 203px"></i><i class="post" style="left: 853px"></i>
      <i class="foot" style="left: 165px"></i><i class="foot" style="left: 815px"></i>
      <i class="knob" style="left: 193px"></i><i class="knob" style="left: 843px"></i>
      <svg class="rope" viewBox="0 0 1080 1920"><path d="M215 1132 C 370 1250, 710 1250, 865 1132" stroke="#8e0b14" stroke-width="22" fill="none" stroke-linecap="round"/>
        <path d="M215 1125 C 370 1241, 710 1241, 865 1125" stroke="#d2323c" stroke-width="6" fill="none" stroke-linecap="round" opacity="0.8"/></svg>
      {title("It’s Not Your Talent.", 'It’s The <span class="it">Gallery-Portfolio Trap</span>', 250, 64)}
      <div class="body" style="top: 1500px; font-size: 48px">A portfolio without a next step<br />is a <span class="it" style="font-size: 62px">gallery</span>.</div>""")

    # S3: the three mistakes, spelled out
    rows = []
    subs = ["The client wants to know what it brings them.", "“Versatile creative” speaks to no one.", "10 projects. 0 clear button."]
    for i, ((n, label), sub) in enumerate(zip((("01", "Projects, Not Results"), ("02", "Nobody Gets What You Sell"), ("03", "No Next Step")), subs)):
        top = 550 + i * 330
        rows.append(f'<div class="lr-row row" style="top: {top}px"><span class="bar"><span class="edge"></span></span>'
                    f'<span class="num">{n}</span><span class="lbl">{label}</span></div>'
                    f'<div class="body sub" style="top: {top + 160}px">{sub}</div>')
    page("story-3", 1080, 1920, """
      .row { left: 100px; width: 880px; height: 136px; }
      .row .num { margin-left: 70px; width: 130px; font-size: 60px; }
      .row .lbl { font-size: 44px; filter: none; padding-right: 40px; }
      .row .edge { width: 28px; }
      .sub { font-size: 38px; color: #cfcfcf; font-weight: 700; }""", f"""
      {title("3 Mistakes I Fixed", "To Land My First Client", 250, 66)}
      {"".join(rows)}""")

    # S4: the template fixes all three; comment PORTFOLIO
    btns = "".join(f'<div class="cx" style="top: {470 + k * 160}px"><div class="lr-btn sb">{n}</div><div class="chk">{CHECK}</div></div>'
                   for k, n in enumerate(("Results", "Clear Offer", "Next Step")))
    page("story-4", 1080, 1920, """
      .hd { top: 250px; font-size: 88px; }
      .hd .ul { bottom: -20px; height: 11px; }
      .sb { width: 620px; text-align: center; font-size: 66px; padding: 18px 0 24px; }
      .lbx { font-size: 42px; line-height: 1.2; padding: 18px 40px 22px; }
      .cm { font: 800 72px/1 "Inter Tight", Arial, sans-serif; letter-spacing: -0.03em; color: #fbfbfb; }
      .kw { font-size: 150px; line-height: 1; color: #fff; }
      .tag2 { font-size: 40px; padding: 8px 28px 12px; }""", f"""
      <div class="lr-head hd"><span class="w"><span>My Template</span><span class="ul"></span></span></div>
      {btns}
      <div class="cx" style="top: 990px"><div class="lr-label lbx">Step-By-Step Strategy<br />From My First Client</div></div>
      <div class="cx" style="top: 1225px"><div class="cm">Comment</div></div>
      <div class="cx" style="top: 1300px"><div class="it kw">“Portfolio”</div></div>
      <div class="cx" style="top: 1500px"><div class="lr-tag md tag2">Under My Latest Reel, To Join The Waitlist</div></div>""")

    # ================================================================ CAROUSEL (1080x1350)
    # C1: cover: the hook, the face, the empty inbox
    page("carousel-1", 1080, 1350, """
      .kick { font-size: 40px; padding: 8px 28px 12px; }
      /* the cutout is cropped at the shoulders: fade it out at the bottom and on the right so no straight edge shows */
      .who { position: absolute; left: -80px; top: 420px; width: 760px;
        -webkit-mask-image: linear-gradient(180deg, #000 0px, #000 640px, rgba(0,0,0,0) 760px), linear-gradient(90deg, #000 0px, #000 540px, rgba(0,0,0,0) 720px);
        -webkit-mask-composite: source-in;
        mask-image: linear-gradient(180deg, #000 0px, #000 640px, rgba(0,0,0,0) 760px), linear-gradient(90deg, #000 0px, #000 540px, rgba(0,0,0,0) 720px);
        mask-composite: intersect; }
      .who img { display: block; width: 760px; height: auto; }
      .zero { position: absolute; left: 590px; top: 538px; width: 400px; text-align: center; font-size: 330px; color: #b80000;
        text-shadow: 0 0 60px rgba(184,0,0,0.55), 0 0 140px rgba(184,0,0,0.25); }
      .ring { position: absolute; left: 640px; top: 548px; width: 300px; height: 300px; border-radius: 50%; border: 4px solid rgba(255,120,120,0.85);
        box-shadow: 0 0 34px rgba(220,0,0,0.5); }
      .zl { position: absolute; left: 590px; top: 900px; width: 400px; display: flex; justify-content: center; }
      .zl .lr-label { position: relative; font-size: 36px; }""", f"""
      <div class="cx" style="top: 64px"><div class="lr-tag md kick">The Gallery-Portfolio Trap</div></div>
      {title("Your Portfolio Is Beautiful.", "So Why No Client Writes?", 150, 64)}
      <div class="who"><img src="/social/img/cutout-chin.png" alt="" /></div>
      <div class="ring"></div>
      <div class="big zero">0</div>
      <div class="zl"><div class="lr-label">Clients Writing To You</div></div>
      {SWIPE}""")

    # C2: mistake 01: projects, not results
    page("carousel-2", 1080, 1350, """
      .proj { font-size: 190px; opacity: 0.42; }
      .res { font-size: 150px; padding: 22px 70px 34px; border-radius: 16px; }
      .q { font-size: 50px; }
      .b2 { font-size: 42px; color: #d6d6d6; }""", f"""
      {crumb("01", "Projects, Not Results")}
      <div class="cx" style="top: 300px"><div class="big proj">Projects</div></div>
      <div class="strike" style="left: 150px; top: 380px; width: 780px"></div>
      <div class="cx" style="top: 560px"><div class="lr-btn res">Results</div></div>
      <div class="cx" style="top: 880px"><div class="cl">{PERSON}</div><div class="lr-label q">What’s In It For Me?</div></div>
      <div class="body b2" style="top: 1060px">The client wants to know<br />what it brings them.</div>
      {SWIPE}""")

    # C3: mistake 02: nobody gets what you sell
    services = [("Logos", 120, 270, -8), ("Websites", 660, 262, 5), ("Video", 330, 340, 3), ("Branding", 760, 380, -4),
                ("Photo", 90, 430, 6), ("Motion", 800, 720, 4), ("3D", 140, 760, -3), ("Illustration", 560, 800, 7),
                ("Social Media", 260, 850, -5), ("UI/UX", 690, 880, -6), ("Print", 70, 620, -7), ("Copywriting", 430, 412, 4)]
    tags = "".join(f'<div class="lr-tag md jt" style="left: {x}px; top: {y}px; transform: rotate({r}deg)">{n}</div>' for n, x, y, r in services)
    page("carousel-3", 1080, 1350, """
      .jt { font-size: 34px; opacity: 0.5; }
      .vc { font-size: 70px; padding: 20px 44px 26px; }
      .no { left: 330px; top: 660px; font-size: 52px; padding: 8px 32px 14px; transform: rotate(-4deg); }
      .b3 { font-size: 42px; color: #d6d6d6; }""", f"""
      {tags}
      {crumb("02", "Nobody Gets What You Sell")}
      <div class="cx" style="top: 500px"><div class="lr-label vc">“Versatile Creative”</div></div>
      <div class="strike" style="left: 170px; top: 560px; width: 740px; height: 13px"></div>
      <div class="lr-tag md no">Speaks To No One</div>
      <div class="body b3" style="top: 1000px">No one understands what you sell.<br />“Versatile creative” doesn’t speak to anyone.</div>
      {SWIPE}""")

    # C4: mistake 03: no next step, a gallery; the CTA
    page("carousel-4", 1080, 1350, """
      .slot { width: 520px; height: 100px; border-radius: 50px; border: 5px dashed rgba(255,255,255,0.8); color: rgba(255,255,255,0.85);
        font: 800 48px/90px "Inter Tight", Arial, sans-serif; letter-spacing: -0.02em; text-align: center; box-sizing: border-box; }
      .n { position: absolute; top: 380px; width: 420px; text-align: center; font-size: 230px; }
      .nl { position: absolute; top: 600px; width: 420px; display: flex; justify-content: center; }
      .nl .lr-label { position: relative; font-size: 38px; }
      .gl { position: absolute; left: 0; right: 0; top: 720px; text-align: center; font: 800 46px/1.2 "Inter Tight", Arial, sans-serif; letter-spacing: -0.02em; color: #fbfbfb; }
      .gw { position: relative; display: inline-block; padding: 0 22px; margin-top: 8px; }
      .gw .bar { position: absolute; left: 0; right: 0; top: 14%; bottom: 4%; background: #b80000; }
      .gw .it { position: relative; font-size: 100px; line-height: 1; color: #fff; }
      .cta { left: 90px; top: 1000px; width: 900px; height: 280px; }
      .cta .c1 { position: absolute; left: 0; right: 0; top: 28px; text-align: center; font: 800 42px/1 "Inter Tight", Arial, sans-serif; color: #fbfbfb; letter-spacing: -0.02em; }
      .cta .c2 { position: absolute; left: 0; right: 0; top: 92px; display: flex; justify-content: center; }
      .cta .c2 .lr-btn { position: relative; font-size: 58px; }
      .cta .c3 { position: absolute; left: 0; right: 0; top: 206px; text-align: center; font: 700 36px/1 "Inter Tight", Arial, sans-serif; color: #cfcfcf; }""", f"""
      {crumb("03", "No Next Step")}
      <div class="cx" style="top: 250px"><div class="slot">Next Step?</div></div>
      <div class="big n" style="left: 90px">10</div>
      <div class="big n" style="left: 570px; color: #b80000; text-shadow: 0 0 60px rgba(184,0,0,0.55)">0</div>
      <div class="nl" style="left: 90px"><div class="lr-label">Projects</div></div>
      <div class="nl" style="left: 570px"><div class="lr-label">Clear Buttons</div></div>
      <div class="gl">A portfolio without a next step is a<br /><span class="gw"><span class="bar"></span><span class="it">Gallery.</span></span></div>
      <div class="lr-panel cta"><div class="c1">My template fixes all 3.</div>
        <div class="c2"><div class="lr-btn">Comment <span class="it">“Portfolio”</span></div></div>
        <div class="c3">to join the waitlist</div></div>""")

    print("pages written:", ", ".join(sorted(p.stem for p in PAGES.glob("*.html"))))


if __name__ == "__main__":
    main()
