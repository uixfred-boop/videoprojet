# Style: "Listicle hub, crimson glass"

**This is the default reference for new edits in this repo** (the user's instruction on 2026-10-08: "new reference
for the next editing videos").

It comes from a reel the user sent: "4 Lead Magnets For Short-Form Videos" (89s, 9:16, talking head plus motion
design). It is the same creator family as the reels behind `videos/web-design-7k-reel/DESIGN.md`. Everything there
still applies (split layout, seam captions, footage card with head pop-out, full-screen cutaways); this file adds
what is new and overrides the palette. The reference video itself is not stored: this repo is public.

Style frames I made from this reading: `frames/style-frames.jpg`, rendered from `demo/` (HyperFrames, 8s,
4 scenes: hub, spoke, synthesis, CTA). The demo copy is placeholder ("3 Client Magnets"). Reusable CSS:
`components.css` is canonical; `demo/assets/css/components.css` is a copy.

## 1. Structure: a hub-and-spoke listicle

The film is a numbered list that keeps returning to a **hub card**:

1. **Hook / hub (0–5s):** hub title types in, and a cloud of N numbered glass tiles floats around a crimson badge
   ball. Then one tile flies to the centre and grows ("01"), and its label types in.
2. **Spoke N:** a breadcrumb header (`Lead Magnet 01` / `Claude Skill Or Workflow`) sits at the top. Below it, one
   or two explanation scenes: hero icon plus filename, UI mock-ups, a timer, diagrams. A full-screen cutaway of the
   speaker (2–7s) carries the commentary in the middle of most spokes.
3. **Back to the hub** for the next item. Same title, next tile, about 2–3s. This is the rhythm marker.
4. **Synthesis:** all N tiles in a row, crimson wires converging into one pill ("Value"), which branches into 2
   chips.
5. **CTA:** `Comment "keyword"` on a crimson bar / `To Get The Doc`, over a glass panel where document pages
   fan in.

Pacing: the graphic changes every 2–4s, captions every 1–3 words, a cutaway every ~10–15s. Each new headline types
on while the voice says it.

## 2. Canvas and layout (1080x1920)

Same split as before, with numbers taken from the reference:

| Zone                 | Position (px @1080x1920)                                   |
| -------------------- | --------------------------------------------------------- |
| Hub title            | centred, line 1 top ≈ 160, ~800px wide                    |
| Breadcrumb header    | centred, box ≈ 440x120 at y ≈ 195                          |
| Section headline     | centred, y ≈ 130–200 (when no breadcrumb is shown)         |
| Graphic zone         | y ≈ 330–1180                                               |
| Caption seam         | one line centred on y ≈ 1277                               |
| Footage card         | x 72–1008, top 1410, runs off the bottom, radius ≈ 34      |
| Cutaway caption      | full-bleed footage, caption on the chest at y ≈ 1150–1250  |

## 3. Palette (sampled)

| Token           | Value                     | Use                                                          |
| --------------- | ------------------------- | ------------------------------------------------------------ |
| `--bg`          | `#0B0B0B`                 | everywhere; light scenes are not used in this reference      |
| `--grid`        | `rgba(255,255,255,0.04)`  | 40px grid, very faint                                        |
| `--crimson`     | `#99122B`                 | THE accent: title bars, pills, badge ball, wires, brackets   |
| `--crimson-hi`  | `#B8193A`                 | glow and highlight edge of crimson elements                  |
| `--node`        | `#F5C518`                 | rare: one junction dot on a wire, the last progress segment  |
| `--glass-top`   | `#232325`                 | tile and panel gradient, top                                 |
| `--glass-bot`   | `#111113`                 | tile and panel gradient, bottom                              |
| `--glass-edge`  | `rgba(255,255,255,0.16)`  | 2px border plus a soft white outer glow                      |
| `--ink`         | `#F5F5F5`                 | text                                                         |
| `--ghost`       | `#6B6B6B`                 | not-yet-typed letters of a headline                          |

Third-party logos keep their own colours (e.g. the blue of an app logo). Nothing else is blue, purple or green.

## 4. Type

- **Sans:** heavy grotesk (SF Pro Display / Inter Tight 800), tracking -0.035em.
  - Hub title line 1: ~100px, white on a crimson bar (padding ≈ 4px 16px).
  - Hub title line 2: ~66px white, no bar.
  - Section headlines: ~56–60px white.
- **Serif italic** (Instrument Serif Italic) for the emphasis word: `From *Lead Magnets*`, `Comment "*magnet*"`,
  the badge-ball label, and some key-phrase captions.
- **Breadcrumb:** small line ~28px regular, then the name ~36px bold, inside 4 crimson corner brackets (arm ≈ 26px,
  stroke 3px).
- **Captions:** as before: white bold ~60px, 1–3 words, serif italic for key terms.

## 5. Components (CSS in `components.css`)

- **Glass tile:** rounded square (r ≈ 22), dark gradient, 2px light edge and soft white glow.
  - Contents: app-style icon at the top, a hairline divider, the number `01` (small), and a 2-line bold label.
  - Sizes: cloud tile ≈ 190x168; hero tile ≈ 378x335.
  - Labels not yet revealed are blurred grey bars.
- **Badge ball:** crimson sphere (radial highlight top-left, darker rim) with a serif italic white label, and a soft
  crimson aura behind it.
- **Hub title bar:** white text on a crimson block. It grows with the typing.
- **Breadcrumb:** eyebrow plus name, framed by 4 crimson corner brackets.
- **Hero icon plus filename:** big icon with a mono-ish filename under it. A hand-drawn crimson arrow (curved SVG
  stroke) draws in toward it.
- **Wires:** 3px crimson SVG curves with glow, drawn with `stroke-dashoffset`. Twin wires use crimson plus white
  dashed. One yellow node dot travels or sits at the junction. Dashed white elbows branch down to small logo tiles.
- **Value pill:** crimson bar with white bold text ~52px. Branch chips are dark glass with a thin crimson border.
- **Tag pill on a panel:** small crimson label (`Database`, `Examples`) over a bold white subtitle and a row of
  thumbnails.
- **Phone card plus progress bar:** vertical card with a crimson 2px edge, holding a clip or document. Under it, a
  segmented `Hook | Body | CTA` bar: white segments, last one `--node` yellow.
- **Network circle:** thin white circle with many small crimson person icons and an app logo in the centre (for
  "audience / demand" beats).
- **CTA panel:** glass panel where 3 white document pages fan in.

## 6. Motion

- **Ghost typing (signature):** a headline appears letter by letter. Untyped letters show as `--ghost` grey and
  slightly blurred, then snap to white. Use it on every hub title and section headline, paced to the voice.
- **Tile cloud:** tiles float with slow 3D drift (rotateX/Y ±8°, y ±12px). The hero tile flies from its cloud spot
  to the centre (scale 0.5→1, 0.6s, `expo.out`) while the others blur away.
- **Blur-in** for every panel (blur 16→0, y 40→0, 0.5s). Crimson glow pulses behind the focal object on emphasis
  words.
- **Wires draw** in 0.5–0.8s. Pills pop with `back.out(2)`. Chips follow 0.1s apart.
- **Floating screenshot collage:** 5–6 UI cards tilt and drift around the badge ball, each at its own depth and
  blur.
- Hard cuts between scenes, on the word. No wipes.

## 7. Sound

Same as the earlier refs: a quiet music bed about 15–18 dB under the voice, plus soft UI SFX (pop on tiles, click
on pills, whoosh on hub returns, typing ticks under ghost typing). No booming impacts.

## 8. Don'ts

- No light-grey scenes (that was the earlier refs). This reference is dark from start to finish.
- No pure red `#FF0000` or `#C00304`. Use the crimson `#99122B`.
- Don't invent statistics. Labels that aren't real are blurred placeholder bars, as in the reference.
