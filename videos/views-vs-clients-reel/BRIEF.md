---
workflow: general-video
flow: automation
storyboard: no
message: "Views aren't clients: content has to serve your business objectives."
destination: instagram-reels
aspect: 1080x1920
language: en
audience: web designers who want to land real client contracts
length: 29.6s
angle: narrative
---

## Intent

Fourth reel in the series. Millions of views and hundreds of thousands of likes, yet the bank account showed zero:
beautiful work that built neither trust nor an image of expertise. People liked, then left. The lesson: content
has to serve your business objectives. CTA: "if you're a web designer, follow me".

The user's words: "Okay, here is the script, the voice-over and the sequences. Do the editing."

- The style is the repo default, `styles/listicle-crimson/STYLE.md`.
- Sound: no music. On the previous reel the user said they'd add the background music themselves, and they said
  nothing new here.
- Soft UI SFX stay in, at the quieter level they asked for on reel 3 (about 20 dB under the voice).

## Assets

- `assets/audio/voiceover.mp3`: the user's voice-over (MiniMax "fred_voice2", 29.2s, mono).
  - `voiceover-master.wav` is the same take, high-passed, gently compressed and normalised to -16 LUFS.
  - Words are force-aligned in `transcript.json` and snapped to pauses. "So if you're a web designer" was
    corrected by hand from the energy envelope.
- `assets/video/desk.mp4`: the user's footage (rec.mp4, 10.5s, graded; `desk-raw.mp4` is ungraded), one
  high-angle shot at the laptop.
  - 0–4.7s: typing.
  - 5–10.4s: hand over the mouth, thinking.
- `assets/video/desk-cutout.webm`: the same shot with the background removed, for the head pop-out.
- `assets/video/instagram.mp4`: the user's screen recording of their own Instagram profile (IMG_8316.MP4, 384x848,
  muted). It is trimmed to 0–7.45s, before Control Center slides in to stop the recording.
  - 0–1.15s: the profile header.
  - 1.17s on: the reels grid scrolling.

## Customizations

- Hub card: "Views Or Clients?" with two tiles (Views, Clients) and a "vs" ball that becomes ≠.
- The footage is short, so the strip cycles its two halves at 0.8x in two framings (0.9x and 1.15x).
- The footage gets one correction everywhere it appears (strip, pop-out and cutaways). Since feedback round 1 it is:
  - deep blacks, a neutral white balance and a brighter face;
  - a canonical treatment (`tools/grade.json`), compared with `hyperframes grade-compare`;
  - baked by `tools/bake_grade.sh`, because the realtime grade on ~18 videos crashed `hyperframes check` in this
    GPU-less sandbox.

  The ungraded files stay as `desk-raw.mp4` and `desk-cutout-raw.webm`.
- "My work was beautiful" shows the user's own Instagram feed scrolling in a phone. UI fidelity: no grade on it, and
  it is shown at 0.9x so the small recording is never upscaled.

## Feedback round 1 (2026-10-09)

The user's words: "the color of the person seems blurry, yellowish and low quality, look closely at the hair and the
t-shirt, well black. illustrate the "my work was beautiful" part with this video showing my work on my Instagram."

- **The grade was the cause.**
  - The first grade (exposure +0.35, shadows +0.3) lifted the black point. In the render the t-shirt sat at ~18/255
    and the hair at ~33, so they read grey.
  - Its curve also pushed the warm cast further: the wall was beige, red−blue +31.
- **The new grade:**
  - Exposure +0.36 with blacks −0.25 and no shadow lift. The t-shirt is at 0–6/255 and the hair at ~3–7, while the
    face is brighter (forehead luma 52 → 60).
  - Temperature −0.24 and tint +0.02, plus a shadows-only split tone, so the wall is off-white (red−blue +4; the raw
    footage is +20) and the blacks are neutral, not navy.
  - Vibrance +0.05.
- **Sharper:**
  - A light luma unsharp (5x5, 0.8) on both files.
  - Explicit BT.709 conversions and tags. The first bake had lost its colour-matrix tag.
  - The render now extracts source frames as PNG (`--video-frame-format png`) instead of the default JPEG (q:v 7),
    which had smeared the dark footage.
- **Cleaner pop-out:** the cutout's soft matte carried wall colour, which drew a light rim around the hair against
  the dark background. Its alpha is now choked.
- **"My work was beautiful" (s04)** is now the user's Instagram feed (`instagram.mp4`):
  - It scrolls in a phone at 2.4x, tagged "My Instagram", with sparkles on "beautiful".
  - In s05 the same phone shrinks and dims under the struck-out Trust and Expertise rows. It replaces the abstract
    work cards, which no longer echoed anything.

## Notes

- "1M+" and "100K+" are the script's "millions of views" and "hundreds of thousands of likes" as lower bounds. No
  other figures are shown, apart from the view counts visible in the user's own Instagram recording.
