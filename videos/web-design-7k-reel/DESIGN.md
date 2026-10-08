# DESIGN.md: house style taken from the three reference reels

Brand truth for every composition in this project. The values come from frames of the user's references, which all
share one creator's house style.

## Canvas and grid

- 1080x1920, 30fps, Instagram Reels safe area: keep text inside x 60–1020. The top 120px and the strip below the
  B-roll card are UI-safe only for decoration.
- Split layout for "panel" scenes:
  - **Headline zone**: y 150–400, centred.
  - **Graphic zone**: y 420–1180.
  - **Caption seam**: one line centred on y ≈ 1268.
  - **B-roll card**: x 72–1008, top y 1408, runs off the bottom edge, radius 34px. The subject's head breaks out above
    the card's top edge (cutout layer).
- Cutaway scenes: full-bleed footage punched in on the face, with the caption on the chest at y ≈ 1150.

## Palette

| Token                | Value                      | Use                                             |
| -------------------- | -------------------------- | ----------------------------------------------- |
| `--bg-dark`          | `#030303`                  | dark scenes (most of the film)                  |
| `--grid-dark`        | `rgba(255,255,255,0.055)`  | 40px grid lines on dark                         |
| `--bg-light`         | `#E2E2DF`                  | light "realisation" scenes                      |
| `--grid-light`       | `rgba(0,0,0,0.07)`         | 40px grid lines on light                        |
| `--card`             | `#2A292A → #171717` (grad) | dark glass cards and list items                 |
| `--card-border`      | `rgba(255,255,255,0.12)`   | 2px card border                                 |
| `--red`              | `#C00304`                  | THE accent: tabs, highlight bars, lines, glows  |
| `--red-bright`       | `#E3191F`                  | glows, chart stroke, active states              |
| `--green`            | `#27C964`                  | success states only (checks, "signed")          |
| `--ink`              | `#F4F3F1`                  | text on dark                                    |
| `--ink-dark`         | `#111111`                  | text on light                                   |
| `--muted`            | `#8E8C8A`                  | secondary labels                                |

One accent (red). Green appears only as the "it worked" signal.

## Type

- **Inter Tight** 700/800 (embedded woff2): headlines, captions, UI. Tracking -0.035em on display sizes. Headlines are
  Title Case, 76–96px, line-height 0.98.
- **Instrument Serif Italic** (embedded woff2): the emphasis word inside a headline ("Not *Much*") and key-phrase
  captions. Set ~1.12x the sans size, tracking -0.01em.
- Captions: Inter Tight 700, 64px, one line of 1–3 words, white with a soft dark shadow on dark scenes and `#111` on
  light scenes. Key phrases switch to Instrument Serif Italic at 76px.
- Red highlight bar: white Inter Tight 800 on a `--red` block with 10px horizontal padding (as in "From 0 To $100K In
  3 Months").

## Components

- **Glass card**: `--card` gradient, 2px `--card-border`, radius 22px, shadow `0 40px 90px rgba(0,0,0,.65)`, 1px inner
  top highlight.
- **List row**: dark row, 108px tall, red 30px tab on the left edge, mono-ish numeral "01" then the label. Inactive
  rows are blurred (6px) and dimmed; the active row is sharp and slightly scaled up (ref3 "Content Production system").
- **Chart card**: label, big number (count-up), red polyline with a glowing end dot, three pill labels under it.
- **Click ripple**: translucent red circle, scale 0→1.4, opacity .45→0 (ref1 cursor click).

## Motion

- Entrances: blur-in (blur 18→0 + y 30→0 + opacity), 0.45–0.6s, `power3.out` / `expo.out`. Pops use `back.out(1.6)`.
- Headlines reveal word by word, timed to the voice-over words that say them.
- Rack focus: inactive items blur (depth-of-field-blur) as the voice moves on.
- Every scene has slow ambient motion (glow breathe, card float, grid drift). No static frames.
- Scene changes: hard cut on the word, with a 0.25s blur/scale settle on the incoming graphic and a whoosh.

## Don'ts

- No invented statistics. Use only figures from the script; any other number is blurred placeholder text.
- No gradient text, no neon, no purple. Red is the only hue besides the green "success" state.
