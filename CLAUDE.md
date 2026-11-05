# videoprojet: standing rules for motion text

These rules apply to **every** motion text, caption, title, lower third and
on-screen word in this project unless the user says otherwise for one shot.

## 1. Typeface (mandatory)

- **Font: Grandstander Medium (weight 500), for all text.** No other family,
  no other weight.
- Font file: `assets/fonts/Grandstander-Medium.ttf` (fixed-weight file, which
  works in After Effects, Premiere, DaVinci Resolve, CapCut and ffmpeg).
- Web / Remotion / HTML: import `motion-text/grandstander.css` and use
  `font-family: "Grandstander"; font-weight: 500;`.
- ffmpeg `drawtext`: `fontfile=assets/fonts/Grandstander-Medium.ttf`.
- Show emphasis with scale, color or motion, never with a different weight
  or font.
- Design tokens (sizes, spacing, timing) are in `motion-text/style.json`.

## 2. Read the text first, then pick the motion

Before animating, read the line and decide what it **means** and how it
**feels**. The motion should express that meaning, not just decorate it.
Use the table below as the default mapping (details and timings are in
`motion-text/style.json` → `moods`).

| What the text expresses              | Motion                                                        |
|--------------------------------------|---------------------------------------------------------------|
| Energy, excitement, a punchline      | Pop / overshoot scale-in, word by word, small bounce          |
| Calm, emotion, reflection            | Slow fade + gentle rise, letter spacing opening slightly      |
| Information, a fact, an instruction  | Clean slide-in, line by line, no bounce                       |
| A number, a price, a statistic       | Count-up or a quick scale punch on the number only            |
| A question                           | Words arrive one by one, short hold, small tilt on the "?"    |
| Urgency, warning, "stop"             | Fast snap-in, short shake, high contrast color                |
| Humor, irony                         | Playful wobble or squash & stretch, slightly off-beat timing  |
| A list or steps                      | Staggered entry, one item per beat                            |
| Call to action (subscribe, link…)    | Scale punch + a gentle looping pulse while it stays on screen |

Rules:
- **Find the key word** of each line (the word that carries the meaning) and
  give it the emphasis: larger scale, accent color, or its own beat. Only one
  key word per line, two at most.
- **Pace follows the voice/music**: words should land on the spoken syllable
  or on the beat. Keep text on screen long enough to read (about 3 words per
  second at minimum).
- **Exit is softer than entry**: exits should be quicker and less flashy.
- If a line mixes moods, follow the mood of the key word.
- If the meaning is unclear, ask the user rather than guess.

## 3. Reference style

The user said they would share a reference for the motion text style. It has
not been received yet. When it arrives, put it in `references/` and update
this file and `motion-text/style.json` to match it (colors, stroke/shadow,
casing, timing). The reference then takes priority over the defaults above.
