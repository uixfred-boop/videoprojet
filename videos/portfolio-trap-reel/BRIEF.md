---
workflow: general-video
flow: automation
storyboard: no
message: "A beautiful portfolio that brings no clients is a gallery: show results, say what you sell, give a next step."
destination: instagram-reels
aspect: 1080x1920
language: en
audience: web designers whose portfolio gets compliments but no client messages
length: 37.2s
angle: listicle
---

## Intent

Fifth reel in the series. The portfolio is beautiful, but no client writes: it's not talent, it's the "gallery-portfolio
trap". There are three mistakes the creator fixed to land his first client:

1. Projects shown, not results.
2. Nobody understands what you sell.
3. No next step to take.

A portfolio without a next step is a gallery. His template fixes all three. CTA: comment "PORTFOLIO" and join the
waitlist.

The user's words (2026-10-14): "Okay, here is my script, my voice-over, and my reference video. Do my video editing."

- **Style:** `styles/lockin-red/STYLE.md`, the reference the user had me analyse just before. The script has the same
  shape as that reference: a coined term, a numbered list, and a Comment CTA over a document. The house layout is
  unchanged (footage card, seam captions, pop-out, cutaways).
- **Sound:** no music. Since reel 3 the user adds their own; the reference's dark sub-bass pad can be added on request.
  - Soft SFX follow the reference: a low whoosh just before each scene change, and soft pops on tags.
  - They stay at the quieter level the user asked for on reel 3, about 20 dB under the voice.

## Assets

- **Voice:** `assets/audio/voiceover.mp3` is the user's voice-over (MiniMax "fred_voice2", 36.7s, mono, -37.5 LUFS).
  - `voiceover-master.wav` is the same take, high-passed, gently compressed and normalised to -16 LUFS.
  - Words are force-aligned in `transcript.json` (spoken text: `tools/spoken.txt`) and kept out of the detected pauses.
- **Footage:** `assets/video/desk-raw.mp4` is the user's clip (1008_18.mp4, 13.9s, one take, muted: its sound is
  silent).
  - It is a frontal shot at the laptop, white wall, black t-shirt.
  - 0–9.4s: reading and typing, with a hand on the chin at 3.5–4.6s.
  - 9.6–11.6s: hands over the face.
  - 11.8–13.9s: hands joined in front of the mouth, looking ahead.
- **Graded footage:** `assets/video/desk.mp4` and `desk-cutout.webm` (background removed, for the head pop-out). The
  correction is gentle and baked by `tools/bake_grade.sh`:
  - the blacks are anchored and the navy taken out of the t-shirt;
  - light sharpening;
  - no white-balance shift (the analyzer saw no imbalance).

## Notes

- Nothing quotes numbers that the script doesn't say. "Ten projects" and "zero clear button" are the script's own
  words. The result card shows an up-trend shape with no figures.
- The VO ends on "because…", as in the script. The CTA scene holds about 0.7s after it.
