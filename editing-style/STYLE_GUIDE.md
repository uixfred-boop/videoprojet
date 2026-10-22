# Reference Editing Style — "Cozy Editorial Yap"

This is the house editing style for future videos. It was derived from frame-by-frame,
audio and motion analysis of two reference reels:

| Ref | Topic | Length | Format |
|-----|-------|--------|--------|
| `ref1` | "Starting from scratch: SAHM + content creator — tools you need + tips for filming yaps" (episode 6) | 2:46 | 720×1280, 30 fps, H.264 / AAC 44.1 kHz |
| `ref2` | "How I edit my yapping reels — as a non-techy SAHM to 3 boys" (episode 2) | 1:59 | 720×1280, 30 fps, H.264 / AAC 44.1 kHz |

Both are from the same creator and share one consistent system. Machine-readable values
live in [`style.json`](./style.json).

---

## 1. Overall feel

- **Genre:** solo talking-head "yap" reel, educational/tips, a series ("episode N").
- **Vibe:** calm, warm, editorial, *quiet luxury*. It's minimal: small, elegant text,
  no loud colors, no bouncing captions. The energy comes from the speaker and the
  pacing, not from heavy effects.
- **Aspect:** 9:16 vertical. The safe area is respected: all text sits between ~5% and
  ~60% of frame height, never in the bottom UI zone.

## 2. Shooting look (so new footage matches)

- **Framing:** medium close-up, chest-up, subject centered; head top at ~25–30% of
  frame height. Static tripod; the camera does not move in the A-roll.
- **Front camera, not mirrored back:** text on clothing reads reversed. This is
  normal; don't flip it.
- **Mic in shot:** she holds a small fluffy lav/wireless mic (deadcat) at the chin the
  whole time. It's part of the aesthetic.
- **Set:** cozy, neutral home interior with real depth behind her. A door, framed art,
  a plant, a warm lamp glow and dark furniture sit a few meters back.
- **Light:** soft natural window light facing the subject, plus warm practical
  lamps in the background.
- **Color grade:** warm and creamy, slightly lifted blacks, low-to-medium contrast,
  gently desaturated greens, skin warm/peachy. No LUT "look" is visible; it reads
  as natural iPhone footage nudged warm and soft.

## 3. Cutting & pacing

- **Dead air removed:** silence detection (−40 dB, ≥0.25 s) finds **zero to two**
  gaps in the whole video. Every breath and pause between thoughts is cut.
- **Jump cuts:** visible jump cuts between takes about **every 2 s on average**
  (median ≈ 1.7–2.0 s, shortest ≈ 0.2–0.4 s, longest ≈ 5–9 s on a strong run).
  - ref1: ~23 cuts/min · ref2: ~29 cuts/min.
- **Jump cuts are left raw:** no crossfades or morph cuts. The small head-position
  jump is accepted as part of the style.
- **Cuts land on new sentences or ideas,** often just before the first word, so
  speech starts on frame 1 of each clip.
- **Hook:** speech starts at 0.0 s. There's no intro card and no logo; the title
  text animates in over the first spoken words.
- **Ending:** a soft CTA ("follow along / comment X"). The handle card pops in for the
  last ~3 s, then the video ends on her last word. There's no outro or end screen.

## 4. Zoom / keyframe language

There are exactly two zoom moves. ref2 is literally a tutorial on them.

| Move | What | Measured | When to use |
|------|------|----------|-------------|
| **Slow zoom** (push-in) | Keyframe scale 100% → ~115%, centered on the face, over ~1.0–1.5 s, then **snap back to 100% on the next cut** | 1.53→1.77 over ~1.4 s (≈ +15%) | Building to a point, a confession, a "get this…" moment |
| **Quick snap zoom** | Instant scale jump 100% → ~115–120% in 2–5 frames (0.07–0.17 s), held 0.3–0.6 s, snap back | +16–19% in ≤0.2 s | Punchline, emphasis word, a reaction beat. Paired with a **whoosh SFX** |

- Zooms are used **sparingly**: roughly 3–6 per minute of talking, not on every cut.
  ref1 has almost none; the variety there comes from jump cuts and B-roll.
- Zoom anchor = the face (eyes at the upper third), never the frame center.
- After any zoom, the next clip returns to the **base framing**. There are no
  lingering zoom-outs.

## 5. Typography system

Text is white everywhere, with a very soft shadow and no stroke. It's always small and
editorial. There are four layers:

### 5.1 Series tag
- Handwritten script (thin monoline brush/marker), e.g. *"episode 6"*.
- Tilted **about −20°**, tucked above the top-left of the main title.
- Small: about 3–4% of frame height. It appears 1–3 s after the title.

### 5.2 Main / section titles
- **Font:** a tightly tracked, high-contrast **editorial display serif**
  (Instrument Serif / Playfair Display / CapCut "Elegance"-style). Close-
  fitting, slightly condensed.
- **Opening title** can be ALL-CAPS (`STARTING FROM SCRATCH:` /
  `SAHM + CONTENT CREATOR`) or sentence case, 2 lines (`How I edit my` /
  `yapping reels`).
- **Section headers** use sentence case with a numeral: `1. Natural light`,
  `2. Depth + cozy background`, `4. Do multiple takes`, `Teleprompter tips...`,
  `Coming soon:`, `Today: keyframes`, `5 tips for filming...`.
- Centered horizontally at **~8–12% from the top**. Size: cap height ≈ 4–5% of
  width (titles span 40–70% of frame width).
- **Animation:** typewriter reveal, letter by letter (`STARTI…` →
  `STARTING FROM SCRATCH:`), over ~0.5–1 s.
- **Persistence:** a section header **stays on screen for the entire section**
  (often 10–40 s) and is swapped the moment the next section starts.
- Trailing ellipsis (`...`) is used for "list incoming" headers.

### 5.3 Sub-notes / annotations
- **Font:** rounded, casual **hand-printed font** (Google "Coming Soon" /
  CapCut handwriting-style), mixed case, white.
- Sits directly under the title, centered, 1–3 short lines, ~45–55% of title size.
- **It appears 1–3 s after its title,** once she starts explaining the point. The
  note summarizes the advice in one casual line, e.g. *"sit facing a window or in your
  car"*, *"you don't get brownie points for less reps + the reps build confidence and
  skill"*, *"there is no shame, even the pros use it"*.
- **List build:** items appear one at a time, in sync with speech. Extra items can
  sit tilted at the sides for playfulness (*"Sound effects"* rotated ≈ −15° at left,
  *"...etc"* rotated ≈ +15° at right). Each item has its own **ding**.
- Standalone asides use the same font with asterisks or emoji: `*viewer beware* 😅`,
  `Get this... 😂`, `...like I said 😂`, `If I can do this, so can you!`,
  `Quick disclaimer...`.

### 5.4 Spoken captions (word by word)
- **One word at a time,** synced to speech, swapping on every word.
- **Small white serif,** the same family as the titles but tiny: about 2.5–3% of
  frame height, a fraction of what typical reels use.
- **Position:** fixed, **left of the face at chin/mouth height** (x ≈ 15–30%,
  y ≈ 48–50%). It isn't centered and isn't low. It reads like a whisper next to her.
- No highlight color, no box, no pop animation, no emoji in captions. Punctuation
  is kept (`obviously,` `videos.` `Third,`).
- Captions keep running over B-roll, GIFs and screen recordings.

### 5.5 Callout pills
- **White rounded rectangle** (≈ 12 px radius at 720 w), black text, no shadow.
- CTA pill in typewriter/mono font: `comment TOOLS for the links` (typed in).
- Chapter label pill in the serif: `First: the slow zoom`,
  `Second: the quick snap zoom`.
- Placed top-center (~12–15% from top).

## 6. Overlays, GIFs & graphics

- **Reaction GIFs / meme clips** (pop culture) are inserted for comedic beats.
  - Examples: "I AM TRYING MY BEST!", Michael/Dwight (The Office), "GOLD STAR FOR
    YOU!", "WASSUP PEOPLES!", "DO IT! DO IT! DO IT!" (Wolf of Wall Street), and
    Miranda Priestly "MOTHER, BOSS, QUEEN".
  - **Size:** small, ~30–45% of frame width. They sit **top-center/top-left above her
    head** so her face stays visible. One "big moment" GIF can go to ~65% width and
    cover the body, but never the full frame.
  - **Duration:** 1.5–3 s. They appear with a **hard cut-in** (no animation) and leave
    with a hard cut.
  - Frequency: about one every 20–40 s.
- **Proof screenshots** (her own reel thumbnail, Instagram follower-growth card) appear
  as **floating cards lower-left/center,** like she's holding them up. Several can
  stack. Each one gets a **pop** sound. An emoji (🤯) can be stuck on the card corner.
- **Emoji row stickers** (Apple emoji, e.g. 🫠🙈😂 or 👦🏻👦🏼👦🏽) appear small at the top
  center as a reaction.
- **Line-icon stickers** illustrate lists (tripod, ring light, mic icons appear
  one by one under "3 tools I use everyday:").
- **Profile card** (IG handle pill: avatar, handle, verified tick, bio line, dark
  translucent rounded rect) pops in top-center for the CTA at the end.
- **Screen-recording tutorial:** the phone recording is overlaid at ~70% width, centered.
  The talking-head footage keeps playing full-frame behind it, and captions continue.
  There are **hand-drawn red curved arrows** and **pointing-hand cursor icons**
  (white 👆 / yellow 👉) to point at UI buttons.

## 7. B-roll

- **Handheld, selfie-style B-roll** shows the thing being talked about: she picks
  up the phone and walks over to the ring light, tripod, mic. It's close and shaky
  (fine), with natural light and no grading change. Each shot runs ~1–2 s, and a
  short sequence lasts 5–8 s.
- The return to A-roll is a straight cut. Captions keep running over the B-roll.
- B-roll doesn't use slow motion, speed ramps or transitions.

## 8. Sound design

- **Voice:** mono, clean lav sound, **−14.5 to −14.8 LUFS integrated** (Instagram/TikTok
  target), voice-forward. There's **no background music bed**; the stereo channel is
  completely silent except for SFX.
- **The SFX palette is small and consistent.** Every SFX is stereo, which is how it
  was isolated from the mono voice:

| SFX | Character (measured) | Level | Used on |
|-----|----------------------|-------|---------|
| **Intro whoosh-boom** | 0.8–1.0 s, deep low-end hit (~75 Hz) + airy whoosh, attack ~0.15–0.3 s | **−9 to −11 dBFS** (loudest SFX) | Frame 1 of the video, under the title type-on. Also on the **big transition** into the screen-recording section (ref2 @ 1:07) |
| **Soft pop / bubble tick** | 0.15–0.2 s, tonal ~690 Hz, soft swell attack ~0.1 s | **−32 to −36 dBFS** (subtle) | **Every** section title / header change, title pills, proof-screenshot cards, profile card |
| **Ding / sparkle chime** | 0.2–0.35 s, bright tonal ~2.4 kHz (centroid ~4.2 kHz), instant attack | **−19 to −21 dBFS** | Emoji asides (`*viewer beware* 😅`), list items appearing one by one, the 🤯 follower stat, the final profile card in ref2 |
| **Swish / whoosh (short)** | ~0.17 s, airy high-frequency (centroid ~6.7 kHz) | **−24 dBFS** | **Quick snap zoom** |
| **Keyboard/typing ticks** | very short, quiet clicks | **−45 to −60 dBFS** | Under typewriter text reveals |

- SFX are **timed to the frame the visual appears** (attack aligned to the overlay's
  first frame).
- Rule of thumb: **soft pop = structure** (new section), **ding = delight** (emoji,
  surprise, list item), **whoosh = motion** (zoom, big transition). Don't use any
  others.

## 9. Structure template (both refs follow it)

1. **0–3 s, hook + title:** whoosh-boom, typewriter title, series tag, and she's already
   talking.
2. **Context/relatable intro (10–20 s):** an aside text (`*viewer beware* 😅`,
   `Quick disclaimer...`), plus 1–2 reaction GIFs.
3. **Topic header** (`Today: keyframes` / `3 tools I use everyday:`), with icons or a list
   and an optional CTA pill (`comment TOOLS for the links`).
4. **Numbered sections:** each has a header (pop SFX), a sub-note ~2 s later, jump cuts
   every ~2 s, and an occasional snap zoom or GIF.
5. **Tutorial / B-roll block** where relevant (screen recording with arrows, or handheld
   gear shots).
6. **"Coming soon" teaser** for the next episode, built as a list with dings.
7. **CTA + profile card** (pop/ding), ending on her last word.

## 10. Do / Don't

**Do:** cut every pause · keep text small and white · use serif + handwriting pairing ·
hold section headers for the whole section · add one-line hand-written summaries ·
use GIFs small and above the head · keep the three-SFX palette · keep the warm, soft grade.

**Don't:** use big bold centered captions · add colored word highlights · use
transitions/crossfades · add music beds · use flashy zoom on every cut · let GIFs cover
the face · use more than ~3 text layers at once · add outros or end screens.
