# "Views or clients?": Instagram Reel

A 29.6-second vertical reel (1080x1920, 30fps) built with HyperFrames, in the repo's default style
(`styles/listicle-crimson/STYLE.md`). It is the fourth reel of the series.

It is motion design over the creator's voice-over: a Views ≠ Clients hub, stat cards, a $0 bank card, struck-out
Trust and Expertise, a content → business objectives diagram, seam captions, the footage card with the head
popping out, two cutaways and a Follow CTA.

**There is no music, on purpose:** the user adds their own track. Soft UI sound effects are part of the edit.

- Render: `renders/views-vs-clients-reel.mp4`.
- Plan: `BRIEF.md`, `DESIGN.md` and `STORYBOARD.md`.

## Edit and re-render

```bash
npm run dev       # Studio preview
npm run check     # lint, layout, motion and contrast gates
npm run render    # MP4 into renders/
```

- `python3 tools/gen_scenes.py` writes every scene (`compositions/s01-…s09-*.html`). Each keeps its timing in
  global voice-over seconds via `at(t)`.
- `python3 tools/assemble.py` writes the scene slots, the footage strip, the captions and the SFX into
  `index.html`.
- The footage grade (a gentle exposure/shadow lift) is baked into `desk.mp4` and `desk-cutout.webm` by
  `tools/bake_grade.sh`, from the `*-raw` files. The look itself was validated as a canonical treatment
  (`tools/grade.json`). For the original look, copy the raw files over the graded ones.
