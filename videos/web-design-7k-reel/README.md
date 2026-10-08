# $7,000 web design project: Instagram Reel

A 64-second vertical reel (1080x1920, 30fps) built with HyperFrames. It is motion design over the creator's voice-over,
in the style of the three reference reels: graphics panel on top, word-group captions on the seam, the B-roll card at
the bottom with the head breaking out of it, and full-screen cutaways on the emotional beats.

- Final render: `renders/web-design-7k-reel.mp4`
- Plan and design truth: `BRIEF.md`, `DESIGN.md`, `STORYBOARD.md` (13 scenes, timed to the voice-over)

## Edit and re-render

```bash
npm run dev       # Studio preview: click anything to edit, scrub the timeline
npm run check     # lint, layout, motion and contrast gates
npm run render    # MP4 into renders/
```

- Scenes live in `compositions/f01-…f13-*.html`. Each one keeps its timing in global voice-over seconds via `at(t)`.
- Captions, scene slots, the footage strip and SFX are generated: edit the tables in `tools/assemble.py`, then
  `python3 tools/assemble.py`.
- Music bed: `tools/make_bed.py` (needs numpy + scipy) writes `assets/audio/bed.wav`. It is carved under the voice
  with `node .claude/skills/hyperframes-audio/scripts/carve.mjs --comp index.html --bed music-bed --voice vo`.
- Voice: `assets/audio/voiceover.mp3` is the original. `voiceover-master.wav` is the same take, high-passed, gently
  compressed and normalised to -16 LUFS for Reels.
- `assets/video/broll-cutout.webm` is the B-roll with its background removed
  (`npx hyperframes remove-background`). It powers the head pop-out above the footage card.
