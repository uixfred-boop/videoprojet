# "Forget the animations": Instagram Reel

A 38-second vertical reel (1080x1920, 30fps) built with HyperFrames, in the repo's default style
(`styles/listicle-crimson/STYLE.md`). It is the third reel of the series, after `../bought-portfolio-reel/`.

It is motion design over the creator's voice-over:

- a listicle hub card that returns for each chapter (01 Study The Best, 02 Cofolio, 03 Rebuilt From Scratch);
- the portfolio screen recordings as a floating collage, then in one large browser panel;
- "Who / What" callouts drawn on a real portfolio hero;
- word-group captions on the seam;
- the footage card at the bottom with the head breaking out of it, plus two full-screen cutaways.

**There is no music, on purpose:** the user adds their own track. Soft UI sound effects are part of the edit.

- Render: `renders/five-second-portfolio-reel.mp4`.
- Plan and design truth: `BRIEF.md`, `DESIGN.md` and `STORYBOARD.md`. Scenes are timed to the voice-over in
  `transcript.json`.

## Edit and re-render

```bash
npm run dev       # Studio preview: click anything to edit, scrub the timeline
npm run check     # lint, layout, motion and contrast gates
npm run render    # MP4 into renders/
```

- Scenes live in `compositions/s01-…s14-*.html`. They are generated, so edit the generator, not the HTML:
  - `python3 tools/gen_hubs.py` writes the hub scenes (s01, s04, s06, s12).
  - `python3 tools/gen_scenes.py` writes the others.
  - Every scene keeps its timing in global voice-over seconds via `at(t)`.
- Captions, scene slots, the footage strip and SFX are generated too: edit the tables in `tools/assemble.py`, then
  run `python3 tools/assemble.py`.
- To add music in HyperFrames rather than in another editor:
  - add an `<audio id="music-bed">` after `<!-- AUDIO:END -->` in `index.html`;
  - carve it under the voice, as in `../bought-portfolio-reel/README.md`.

## Media

- **Voice:** `assets/audio/voiceover.mp3` is the original (MiniMax, mono). `voiceover-master.wav` is the same take,
  high-passed, gently compressed and normalised to -16 LUFS.
- **Footage:** `assets/video/desk.mp4` is the desk shot (0–21.33s of the upload).
  - `desk-cutout.webm` is the same shot with the background removed (`npx hyperframes remove-background`). It
    powers the head pop-out.
  - The strip alternates two framings of it, 0.9x and 1.15x.
- **Screen recording:** `assets/video/screen.mp4` is the rest of the upload, cropped to its 16:9 content. The table
  in `BRIEF.md` lists which site plays when.
