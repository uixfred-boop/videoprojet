---
workflow: general-video
flow: automation
storyboard: no
message: "Forget the animations: a portfolio that lands real contracts is one people understand in five seconds."
destination: instagram-reels
aspect: 1080x1920
language: en
audience: web designers who want to land real client contracts
length: 38s
angle: narrative
---

## Intent

Third reel in the series, right after "I bought a ready-made portfolio". After the reality check, the creator studies
the best portfolios, finds most of them do way too much, then finds Cofolio: fluid, efficient, and clear about who
and what in five seconds. Lesson: the goal isn't "wow", it's being understood. He rebuilds everything on that logic.
CTA: "if you're a web designer, follow me".

The user's words: "Okay, here is the script, the voice-over and the sequences. Do the editing in reference style.
And for the background sound, leave it, I'll do it myself."

- "Reference style" is `styles/listicle-crimson/STYLE.md`, the repo's default.
- **No music bed.** The user adds their own. Soft UI SFX stay in, as part of the motion design.

## Assets

- `assets/audio/voiceover.mp3`: the user's voice-over (MiniMax TTS, 37.5s, mono).
  - `voiceover-master.wav` is the same take, high-passed, gently compressed and normalised to -16 LUFS.
  - Words are force-aligned in `transcript.json` (spoken text: `tools/spoken.txt`), then snapped to the audio's
    pauses.
- `assets/video/desk.mp4`: 0–21.33s of the upload. One shot of the creator at his laptop, front and slightly above.
  It alternates between looking down at the screen and thinking poses (hand on chin at 3.5–5s and 9–12.5s). He
  leans back and looks up at 18–19.5s.
- `assets/video/desk-cutout.webm`: `desk.mp4` with the background removed, for the head pop-out.
- `assets/video/intro.mp4`: the user's second upload (10092.mp4, 4.4s), cropped to its 16:9 band. It is a fast
  montage of the same animated portfolio sites, used under "Forget the animations".
- `assets/video/screen.mp4`: 21.33–38.9s of the upload, cropped to its 16:9 content (1080x608). Screen recordings
  of portfolio sites, in this order (times in screen.mp4 seconds):

  | Time       | Site                                                                           | Role in the edit            |
  | ---------- | ------------------------------------------------------------------------------ | --------------------------- |
  | 0.0–0.2    | Pastry/food collage                                                            | (too brief)                 |
  | 0.2–1.44   | Getty "Tracing Art": image collage                                             | busy                        |
  | 1.44–2.5   | "Human Thinkers / Digital Makers": column of 3D renders                        | busy                        |
  | 2.5–3.97   | gufram: floating 3D objects (lips sofa, cacti)                                 | busy                        |
  | 3.97–5.27  | palmer: plates, "Coco Pink" product view                                       | busy                        |
  | 5.27–6.37  | Telescope / Hasan Khalid: GQ creative development                              | busy                        |
  | 6.37–7.24  | "Creative that converts": loud colour and type                                 | busy                        |
  | 7.24–11.47 | A clean case-study portfolio (Roblox, SoFi, UniJourney…) with a marquee strip | the clean one ("Cofolio")  |
  | 11.47–end  | Perry Wang, product designer: "I craft products, interactions & stories."      | who and what in 5 seconds   |

## Customizations

- The hub has three chapter tiles: 01 Study The Best, 02 Cofolio, 03 Rebuilt From Scratch. It returns for each
  one, around a crimson "5 Seconds" badge ball.
- The busy portfolio recordings float as a collage of browser windows. The clean ones play in one large browser
  panel.
- Two full-screen cutaways: "After my reality check" and "That's when it clicked".

## Notes

- I don't know which site in the recording is Cofolio, or its logo. The edit names it in text only (tile label and
  breadcrumb) over the clean portfolio footage, and invents no logo or URL.
- The labels on the mock-ups ("Who you are", "What you do", "Work", "Contact") come from the script's own wording.
  Nothing quotes statistics.

## Feedback round 1 (2026-10-09)

The user's words: "use this clip at the beginning of the video to illustrate «forget the animations.» lower the volume
of the sound effects, especially on the wow."

- The hook now plays their clip (`intro.mp4`, 2x) in a crimson browser window instead of the synthetic animation
  clutter. It is struck out as "animations" ends.
- Sound effects are ~7 dB quieter overall (`SFX_GAIN` in `tools/assemble.py`), now about 20 dB under the voice.
- The WOW moment is softer still: no sparkle and no error buzz, 22 dB under the voice (it was 9 dB).
