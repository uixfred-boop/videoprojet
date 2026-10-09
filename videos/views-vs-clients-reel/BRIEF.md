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
- `assets/video/desk.mp4`: the user's footage (rec.mp4, 10.5s), one high-angle shot at the laptop.
  - 0–4.7s: typing.
  - 5–10.4s: hand over the mouth, thinking.
- `assets/video/desk-cutout.webm`: the same shot with the background removed, for the head pop-out.

## Customizations

- Hub card: "Views Or Clients?" with two tiles (Views, Clients) and a "vs" ball that becomes ≠.
- The footage is short, so the strip cycles its two halves at 0.8x in two framings (0.9x and 1.15x).
- The footage was shot dark, so it gets a gentle canonical correction everywhere it appears: strip, pop-out and
  cutaways. That's exposure +0.35 and shadows +0.3, validated with `hyperframes media-treatment` and stored in
  `tools/grade.json`. The analyzer saw no technical imbalance: the shot is low-key. The lift only makes the face
  read in the small card. Delete `tools/grade.json`'s use in the generators to return to the original look.

## Notes

- "1M+" and "100K+" are the script's "millions of views" and "hundreds of thousands of likes" as lower bounds. No
  other figures are shown.
