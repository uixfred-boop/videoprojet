# Style: "Lock-In", pure red on a black dot grid

A reading of the reference reel the user sent on 2026-10-14 ("analyze this new reference video perfectly"). It is
84.6s at 720x1280 / 30fps (an Instagram download): a talking head plus motion design about the "Lock-In Zone", the 2–3
sentences after a hook.

It comes from the same creator family as `../listicle-crimson/STYLE.md` and uses the same canvas and layout grid. This
file lists what is the same and what changes. The reference video and its frames are not stored, because this repo is
public; everything below is measured and described in text.

**Status:** analysis plus reusable CSS (`components.css`). Reel 5 (`videos/portfolio-trap-reel/`) is the first edit
in this style and the working example; there are no separate style frames. `listicle-crimson` stays the default style
until the user says otherwise.

All positions are in **1080x1920** px (the reference measured at 720x1280, ×1.5).

## 1. Structure: a numbered-list hub with spokes

The film is one numbered list of 6 items. It keeps returning to the list (the hub), and each item gets one
explanation scene (the spoke) and usually one cutaway.

| #   | Time (s)    | Layout   | Voice (gist)                                         | Picture                                                                                                         |
| --- | ----------- | -------- | ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| 1   | 0.00–1.77   | split    | why your videos don't hold attention                 | Hub title over a "Reel insights" card. The reel thumbnail tints red, a views pill counts up, a red retention curve drops, and a red ping circle lands on the drop. |
| 2   | 1.77–4.47   | cutaway  | …because you're missing *the term*                   | Tight shot. The coined term lands as one serif italic caption ("The Lock-In Zone.").                            |
| 3   | 4.47–9.40   | split    | everyone talks about the hook; the secret is the 2–3 sentences after it | Underline header (the term) plus a "Video Script" document. The red Hook row draws in, then yellow "Lock-in zone" rows draw one by one and glow. |
| 4   | 9.40–11.97  | split    | where you lock in attention                          | Same header. The document slides out left; a phone and a glowing white 3D figure slide in from the right. A red padlock pops in; a red ping lands on the figure's head. |
| 5   | 11.97–13.03 | cutaway  | …and get them to stay                                |                                                                                                                 |
| 6   | 13.03–15.47 | split    | there are 6 ways                                     | List hub: "The 6 Ways To Approach / *term*", with six glass rows 01–06 and their labels blurred.                |
| 7   | 15.47–16.70 | cutaway  | …to capture attention                                |                                                                                                                 |
| 8   | 16.70–18.8  | split    | number 1 is …                                        | List again. Only row 01 keeps its bar; its label sharpens and a white sheen sweeps across it.                   |
| 9   | 18.8–23.37  | split    | item 1 explained                                     | Breadcrumb bar "01 · name", then an "AI Workflow" tag over a reel card. "Stat" and "Result" cards slide in from the sides, flash green twice on "confirms", then a hook label appears with a red ping on "hook". |
| 10  | 23.37–27.6  | split    | number 2 is …                                        | List, row 02. This is a hard cut from the spoke with no cutaway in between.                                     |
| 11  | 27.6–31.0   | split    | before / after the viewer feels                      | Breadcrumb with a 3-line label. "Before" and "After" boxes joined by a red-white dashed connector, and a red avatar badge on "the viewer". |
| 12  | 31.0–32.77  | cutaway  | …once it's delivered                                 |                                                                                                                 |
| 13  | 32.77–35.7  | split    | number 3 is …                                        | List, row 03                                                                                                    |
| 14  | 35.7–40.97  | split    | contrast against the common belief                   | Phone playing the creator's own reel, with a green flash on "this video" and an "If You Rewatch It" pill. The screen switches to the document. "Contrast — Against — Common Belief" tags are linked by thin lines over two label boxes. |
| 15  | 40.97–43.27 | cutaway  | …to clarify the claim                                |                                                                                                                 |
| 16  | 43.27–45.9  | split    | number 4 is …                                        | List, row 04                                                                                                    |
| 17  | 46.0–49.30  | split    | introduce a term, framework or method                | The document slides in on the right. An "Introduce The Name Of A:" box, then big red buttons "Term", "Framework", "Method", one per spoken word. |
| 18  | 49.30–52.43 | cutaway  | …the viewer hasn't heard before                      |                                                                                                                 |
| 19  | 52.43–54.7  | split    | number 5 is …                                        | List, row 05                                                                                                    |
| 20  | 54.7–57.67  | split    | make a bold contrarian claim                         | AI Workflow reel card with a "Bold Contrarian Claim" tag, and a big label with the hook text over it.           |
| 21  | 57.67–61.67 | cutaway  | …then handle the objection                           |                                                                                                                 |
| 22  | 61.67–63.6  | split    | number 6 is …                                        | List, row 06                                                                                                    |
| 23  | 63.6–67.20  | split    | double down on the hook                              | The document's placeholder lines become real text: the hook in red, the lock-in zone typing in yellow.          |
| 24  | 67.20–69.37 | cutaway  | …to intensify the claim                              |                                                                                                                 |
| 25  | 69.37–73.0  | split    | without a plan for *the term*…                       | Title "Your Videos Won't Perform / Without A Plan For *The Lock-In Zone*" (the term in serif italic on the red bar), and a "Without Plan" red button over the document. |
| 26  | 73.0–75.90  | split    | …your videos won't grab attention                    | Slide back to the red "Reel insights" card: a bookend to the hook.                                              |
| 27  | 75.90–77.43 | cutaway  | Comment "Lock"                                       | Two-line caption: "Comment" in sans, then "Lock" in serif italic with quotes.                                   |
| 28  | 77.43–84.5  | split    | the doc breaks down all 6, with examples and tactics | CTA title "Comment *"Lock"* To Get The Doc / Breaking Down All 6 Approaches". Six document pages fan into a 3x2 grid, a lime highlight chases across them on "6 options", then "With Examples" and "Tactics" buttons appear. |

**Pacing:**
- **Beats:** 28 beats. The 19 graphic beats average 3.4s.
- **Cutaways:** 9, totalling 19.9s (24% of the runtime), each 1.1–4.0s. Each one lands on the *payoff clause* of an
  item's sentence, so the face says the punchline.
- **Hubs:** each hub return lasts 2.0–4.2s, its spoke 3.0–5.3s.
- **Speech:** about 300 words in 84.5s, roughly 3.6 words/s (≈ 215 wpm).
- **Bookends:** the hook's retention card comes back just before the CTA.

## 2. Canvas and layout

This is the house grid, unchanged: the same as `listicle-crimson` and `videos/web-design-7k-reel/DESIGN.md`.

| Zone                     | Position (1080x1920)                                                                    |
| ------------------------ | --------------------------------------------------------------------------------------- |
| Hub title (2 lines)      | centred. Line 1 cap-top y ≈ 128; line 2 on the red bar at y ≈ 174–225                   |
| Single-line header       | centred. Cap-top y ≈ 113, red underline at y ≈ 174–183                                  |
| Breadcrumb bar           | x 225–855, y 105–228 (630x123)                                                          |
| List rows                | x 279–801 (522 wide), 103 tall, 134 pitch, first row at y ≈ 339                         |
| Graphic zone             | y ≈ 260–1180, panels centred                                                            |
| Captions                 | one word centred on y ≈ 1285                                                            |
| Footage card             | x 72–1008, top 1408, runs off the bottom, radius ≈ 36, faint light top edge             |
| Pop-out                  | person cutout above the card edge: the cap, and the hands when raised                   |
| Cutaway                  | full-bleed tight shot, caption at the same y ≈ 1285 but bigger                          |

Graphics pass **behind** the footage card (the document slides under it), and the caption sits in the dark seam.

## 3. Palette (sampled)

| Token          | Value                                     | Use                                                                         |
| -------------- | ----------------------------------------- | --------------------------------------------------------------------------- |
| `--bg`         | `#000000`                                 | everywhere. No aura blobs, no vignette.                                     |
| `--dots`       | `#2A2A2A`, ~2px dots on a ~17px grid      | the whole background, uniform                                               |
| `--red`        | `#B80000`                                 | THE accent: title bars, underline, row and breadcrumb edge, Hook bullet and line, ping circle |
| `--red-deep`   | `#96050F`                                 | small tags (AI Workflow, Stat, Result, Contrast, Before, After)             |
| `--red-btn`    | vertical gradient `#C40000` → `#7A0000`   | big buttons (Term, Framework, With Examples, Tactics, Without Plan)         |
| `--red-glow`   | 2px `#E0625B` edge + dark red outer glow  | border of white screenshot cards                                            |
| `--yellow`     | `#ECE512` with a yellow glow              | lock-in zone bullet, highlight lines, yellow text in the document           |
| `--green`      | `#18DE3A` (flash), `#8DEE08` (lime chase) | "confirm" highlight only                                                    |
| `--ink`        | `#FBFBFB`                                 | text                                                                        |
| `--ghost`      | `#9E9E9E`                                 | not-yet-typed letters (lighter than crimson's `#6B6B6B`)                    |
| `--glass`      | horizontal gradient `#121212` → `#2C2C2C`, 1px light top edge | list rows, breadcrumb bar                               |
| `--panel`      | `#0B0B0B` fill, 2px white border, ~12px white outer glow, soft inner glow | document, insights card                     |
| `--doc-line`   | `#6E6E70`                                 | placeholder lines in the document                                           |
| `--label`      | `#141414` fill, 2–3px white border, radius ≈ 4 | label boxes                                                            |

Pure red here has **no blue in it**: R 184, G 0–5, B 2–9. Logos and screenshots keep their own colours.

## 4. Type

- **Sans:** a heavy grotesk, with the look of SF Pro Display Bold/Heavy; our stand-in is Inter Tight 800.
  - Tracking is about -0.03em, white, with a faint dark shadow.
  - Graphics text is in Title Case.
- **Serif italic:** a condensed modern serif; our stand-in is Instrument Serif Italic. It is used for:
  - the "Video Script" heading;
  - the coined term, both in captions and inside titles, where it sits on the red bar;
  - the quoted CTA keyword.
- **Sizes** (px at 1080):

  | Text                                          | Size                             |
  | --------------------------------------------- | -------------------------------- |
  | Hub title (both lines)                        | 54                               |
  | Single-line header                            | 74                               |
  | Breadcrumb: number / label                    | 47 / 29 (26 when 3 lines)        |
  | List row: number / label                      | 42 / 27                          |
  | Caption: split / cutaway / serif term         | 53 / 68 / 90                     |
  | Big red buttons                               | ≈ 60                             |
  | Medium tags / small tags                      | ≈ 32 / ≈ 26                      |
  | Label boxes                                   | 24–36, bold, centred, 1–2 lines  |
  | "Video Script"                                | ≈ 48 serif italic                |

- **Line spacing:** the 2-line title is tight (pitch ≈ 56px for 54px type). The red bar hugs line 2 with about 10px
  horizontal padding, 9px above and 4px below.

## 5. Components

- **Hub title:**
  - Line 1 is white. Line 2 is white on a pure-red bar that grows with the typing.
  - It sits over the panel: on the hook, the title overlaps the zooming card.
- **Single-line header (underline variant):**
  - White 74px text with a 9px red underline about 7px under the baseline, overhanging the text by 24px each side.
  - The underline grows with the typing.
  - The header persists while the content under it slides.
- **Numbered list:**
  - Six glass rows (`--glass`, radius ≈ 10) with a 21px red left edge, a bold number and a centred label.
  - Inactive labels are Gaussian-blurred (≈ 6–8px) so they can't be read yet.
  - In item mode only the active row keeps its bar and sharp label. The other rows lose their bars and keep a number
    and a blurred label.
- **Breadcrumb bar:**
  - A wide glass bar (630x123, radius ≈ 12) with a 24px red left edge.
  - A big number on the left, and the item name centred in the rest (up to 3 lines).
  - It replaces the hub title during a spoke.
- **"Video Script" document:**
  - A `--panel` card (≈ 610x754 at rest) with a centred "Video Script" heading in serif italic.
  - Row 1: a red square bullet, bold "Hook", and a red line.
  - Row 2: a yellow square bullet, bold "Lock-in zone", and 4 yellow highlight lines with glow.
  - Then about 20 grey placeholder lines.
  - Later the lines become real text: the hook in red, the zone in yellow.
- **"Reel insights" card:**
  - A `--panel` card mocking Instagram's insights: a reel thumbnail, a "Retention" axis with 100% / 50% grid lines,
    and a "skip rate" legend.
  - For the beat, the thumbnail gets a red tint, a red pill with an eye icon counts the views up, and a ≈ 5px red curve
    with glow drops from 100% to about 15%.
- **Tags:**
  - Small and medium tags are `--red-deep` rectangles (radius ≈ 3) with bold white text, set half over the top edge of
    the card they label.
  - Big buttons are `--red-btn` gradient rectangles (radius ≈ 6) with ≈ 60px white text and a subtle top highlight.
- **White screenshot cards:** app screenshots on white, with the `--red-glow` border and a medium tag ("Stat",
  "Result") on the top-left edge. Under each is a label box with a one-line caption.
- **Label boxes:** `--label`, used for hook texts, Before/After statements and "Introduce The Name Of A:".
- **Connectors:**
  - Thin white lines link tag to tag ("Contrast — Against — Common Belief").
  - A red-white dashed bar runs between the Before and After boxes.
- **Ping circle:** a translucent red disc (`--red` at ~55%) with a lighter rim. It marks the focal point on "attention",
  "hook" and "feel".
- **Avatar badge:** a red sphere with a white user glyph and a light ring, for "the viewer".
- **Phone:** a black iPhone with a notch, showing a real reel with the Instagram UI, or the document.
- **3D figure:** a glowing white, matte 3D person looking at a phone, with a red ping circle on the head. It is a
  rendered asset.
- **CTA page grid:** 6 white document pages with blurred text in a 3x2 grid (≈ 200px wide each). Big red buttons are
  stacked in the middle of the grid.

## 6. Motion (measured at 30fps)

- **Ghost typing (fast):**
  - Letters appear `--ghost` grey, then turn white. A 2-line title finishes in about 0.55s, which is 30–80 characters/s,
    2–3x faster than listicle-crimson.
  - The title bar and the underline grow with the text.
  - Every title re-types from nothing after each cut, including hub returns.
- **Build from black:**
  - The first frame of a split scene after a cutaway is empty. Elements fade and blur in within 0.3–0.6s.
  - List rows drop in staggered by 2 frames (0.067s each) and settle by about 0.7s.
- **Slow push-in on the focal panel:** it never stops.
  - The document grows ~10%/s while it is explained.
  - The insights card goes from 1.0 to 1.4 over 1.4s.
  - The CTA grid grows ~7%/s.
  - Cutaways drift in about +5% per shot.
- **Slide within a chapter:**
  - Old content exits left and new content enters from the right in about 0.4s.
  - A white horizontal light streak trails the seam.
  - The header stays put.
- **Hub → spoke:** the list blurs out in about 0.1s. The breadcrumb slides in from +50px with an ease-out (≈ 0.4s), and
  the new panel brightens in from a washed-out, blurred state.
- **Active row:** a white sheen sweeps the active bar left to right in about 0.3s, as its label unblurs.
- **Draw-ons:**
  - The Hook line and the yellow highlight lines draw left to right, about 0.25s each, staggered by about 0.15s.
  - A glow pulse (about 0.3s) marks the emphasis word.
- **Pops:** the padlock, tags and buttons appear in 0.1–0.2s (scale from 0, or fade plus blur), one per spoken word.
- **Ping:** it grows from a dot to about 180px in 0.2s, then fades over 0.3s.
- **Confirm flash:**
  - A green overlay pulses twice within 0.4s on "confirms".
  - The lime chase runs across the pages about 0.13s apart on "6 options".
- **Side cards:**
  - They slide in from the left and right (about 0.3s).
  - Meanwhile the central card dims, and the stack shrinks about 12% and moves up to make room for a label.
- **Cuts:** split ↔ cutaway changes are hard cuts on the word. There are no wipes.

## 7. Footage

- **Two framings of one take, cut on speech:**
  - The card shows a medium-wide desk shot: a framed photo, warm practical lamps and teal LED shelves.
  - The cutaways are a tight medium close-up.
- **Grade:** dark and contrasty with **true blacks**: the black hoodie and cap stay black. Teal and cyan practicals,
  warm highlights, natural skin.
- **Pop-out:** the person cutout breaks the card's top edge, the cap and any raised hand, with no visible fringe.

## 8. Captions

- **Pacing:** one word at a time (a few short pairs or triples), back-to-back with no gaps. There are 229 captions,
  median 0.33s, longest 1.53s.
- **No animation:** words hard-swap; no pop, no scale, no colour.
- **Style:** white bold sans, about 53px in split scenes and about 68px in cutaways, centred on y ≈ 1285.
  - Lowercase as spoken, with punctuation.
  - The coined term and the CTA keyword switch to serif italic and get bigger (about 90px).

## 9. Sound

- **Mix:**
  - -14.1 LUFS integrated, true peak -0.4 dBFS.
  - LRA 3.1 LU: heavily compressed.
  - The voice is essentially mono.
- **Music:** a dark, drumless ambient pad whose energy is almost all sub-bass.
  - It holds sustained notes F1–G1–A♭1 (44–52 Hz), each for 2.5–5s.
  - It sits about 12 dB under the voice in the low end and is nearly absent above 250 Hz, so it reads as warmth, not a
    tune.
  - It drops out for about 3s at the concept reveal (5–8s), comes back softly, and plays at full level from about 18s to
    the end.
- **Main SFX:** a short, low stereo whoosh (about 0.35s, sub-heavy). It starts about 0.2s **before** every graphic
  scene change, so the cut lands on its peak:
  - slides;
  - list builds;
  - hub → spoke;
  - wrap-up;
  - CTA;
  - and under the ping circles.
- **Softer swipes:** about 0.8s long and about 8 dB quieter, on Before/After and on the Term/Framework/Method pops.
- **What's absent:** no typing ticks under the ghost typing, no sounds on captions, and no booming impacts.

## 10. What changes from `listicle-crimson`

|                   | listicle-crimson                                     | this reference                                                                  |
| ----------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------- |
| Accent            | crimson `#99122B` (+ `#B8193A` glow)                 | pure red `#B80000`; deep red `#96050F` tags; red gradient buttons               |
| Background        | `#0B0B0B`, 40px line grid, crimson aura              | `#000`, dot grid, no aura                                                       |
| Hub               | title + cloud of glass tiles around a badge ball     | title + vertical numbered list with red-edged glass rows and blurred labels     |
| Breadcrumb        | eyebrow + name inside 4 corner brackets              | glass bar: red edge, big number, label                                          |
| Header variant    | —                                                    | single-line header with a red underline                                         |
| Ghost typing      | `#6B6B6B`, paced to the voice                        | `#9E9E9E`, 2–3x faster, re-typed after every cut                                |
| Captions          | 1–3 word groups                                      | single words (median 0.33s), hard swaps                                         |
| Signature objects | tiles, badge ball, wires, value pill                 | script document with red Hook + yellow highlights, red tags, ping circle, green confirm flash, big red buttons |
| Music             | quiet bed 15–18 dB under the voice                   | drumless sub-bass pad, ~12 dB under in the lows only, dropped for the reveal    |
| SFX               | pops, clicks, whoosh, typing ticks                   | low whoosh just before each scene change; no typing ticks                       |

**The same in both:**
- the layout grid: the card, the seam captions, the pop-out, the cutaways;
- heavy sans paired with serif italic, and Title Case graphics;
- hard cuts to cutaways on the word;
- the "Comment "x" To Get The Doc" CTA over document pages.

## 11. Building it in HyperFrames (when asked)

**Start from reel 5** (`videos/portfolio-trap-reel/`). It has:
- `components.css` as `assets/css/lockin.css`;
- `tools/gen_scenes.py` helpers: `title()` (the title bar grows with the typing), `rows()` and `hub_return()` (the
  list hub and its re-type), `crumb()` (breadcrumb) and `cut()` (cutaway with a slow push);
- `assets/js/fx.js` with `grow`, `ping`, `sheen`, `push` and `flash` added;
- `tools/assemble.py` with one-word captions (the term and the CTA keyword in serif italic) and a low whoosh 0.2s
  before each graphic scene (`assets/sfx/whoosh-low.mp3`: `whoosh-short` pitched down and low-passed).

The notes below are the original plan for the first build.

- **Reuse unchanged:** the house layout in `index.html` (strip, pop-out, captions) and the assembler pattern.
  - From `fx.js`, `type`/`typeSpan` with `GHOST = "#9E9E9E"` and a faster pace, plus `blurIn`, `pop`, `draw` and
    `count`.
- **New CSS components:**
  - dot background;
  - list rows (blurred label state, active sheen);
  - breadcrumb bar;
  - underline header;
  - script document;
  - insights card with an SVG retention curve;
  - small, medium and big red tags;
  - label boxes;
  - ping circle;
  - flash overlay;
  - page grid.
- **Captions:** in `assemble.py`, group one word per caption (a short pair at most), at 53px / 68px on y ≈ 1285, with
  no entrance tween. Use serif italic for the coined term.
- **SFX:** from our library, take `whoosh-short` / `whoosh-cinematic`, low-passed or pitched down, placed 0.2s before
  each cut. Add `pop` for the buttons; drop the typing ticks.
- **Music:** synthesise a drumless pad with a sustained sub-bass progression (numpy, like
  `videos/web-design-7k-reel/tools/make_bed.py`), about 12 dB under the voice in the lows. Mute it for the concept
  reveal.
- **The 3D figure** is a rendered asset we don't have. Use a glowing white SVG silhouette, or the user's own footage.

## 12. Don'ts

- No crimson or blue-ish reds, no aura blobs, no line grid, no light scenes.
- Don't animate captions or put typing ticks under titles.
- Don't invent statistics. Counters and screenshots show the creator's real data; placeholder text stays blurred
  lines.
