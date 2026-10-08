# "I bought a ready-made portfolio": Instagram Reel

A 114-second vertical reel (1080x1920, 30fps) built with HyperFrames, in the repo's default style
(`styles/listicle-crimson/STYLE.md`). It is motion design over the creator's voice-over:

- a listicle hub card that returns for each chapter (01 Ready-Made Portfolio, 02 Mass Outreach, 03 The $350 Client,
  04 Study The Best);
- glass panels, stamps and counters for each beat of the story, and the bought template's screen recording;
- word-group captions on the seam;
- the footage card at the bottom with the head breaking out of it, plus full-screen cutaways;
- a synthesised trap beat whose drops and stops follow the story.

Renders:

- `renders/bought-portfolio-reel.mp4`: the final cut, with the beat.
- `renders/bought-portfolio-reel-no-music.mp4`: the same picture with voice and SFX only, ready for another track.

Plan and design truth: `BRIEF.md`, `DESIGN.md` and `STORYBOARD.md`. Scenes are timed to the voice-over in
`transcript.json`.

## Edit and re-render

```bash
npm run dev       # Studio preview: click anything to edit, scrub the timeline
npm run check     # lint, layout, motion and contrast gates
npm run render    # MP4 into renders/
```

- Scenes live in `compositions/s01-…s25-*.html`. They are generated, so edit the generator, not the HTML:
  - `python3 tools/gen_hubs.py` writes the hub scenes (s01, s02, s06, s12, s21).
  - `python3 tools/gen_scenes.py` writes the other 20.
  - Every scene keeps its timing in global voice-over seconds via `at(t)`.
- Captions, scene slots, the footage strip and SFX are generated too: edit the tables in `tools/assemble.py`, then
  run `python3 tools/assemble.py`.
- Shared motion helpers (ghost typing, pops, stamps, counters, line draws) are in `assets/js/fx.js`.

## Audio

- **Voice:** `assets/audio/voiceover.mp3` is the original. `voiceover-master.wav` is the same take, high-passed,
  gently compressed and normalised to -16 LUFS for Reels.
- **Beat:** `tools/make_beat.py` (needs numpy + scipy) writes `assets/audio/beat.wav`.
  - It is a dark C-minor trap groove at about 140 BPM, with no samples and deterministic output.
  - Its grid bends slightly so that the drops land on "I cheated", "said yes" and "so I locked in".
  - It cuts to silence for "nothing" and for "subscribe", and ends on a hit after the last word.
- **Carve:** the beat is carved under the voice with
  `node ../../.claude/skills/hyperframes-audio/scripts/carve.mjs --comp index.html --bed music-bed --voice vo --strength 0.45`.
  That needs `npm i` here for `@hyperframes/core`.
- **Mix check:** `python ../../tools/simulate_mix.py .` simulates the mix (carve included) and reports loudness and
  true peak before a render. Pass `--mute music-bed --out mix.wav` to get the voice and SFX alone.
- **Your own music:** delete the `music-bed` element from `index.html`, or set its `data-volume="0"`, and re-render.

## Footage

- `assets/video/people.mp4` is the creator's footage. `people-cutout.webm` is the same clip with the background
  removed (`npx hyperframes remove-background`); it powers the head pop-out above the footage card.
- `assets/video/screen.mp4` is the screen recording of the bought template (scene s17).
