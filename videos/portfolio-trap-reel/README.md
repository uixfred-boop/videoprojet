# "The gallery-portfolio trap": Instagram Reel

A 37.2-second vertical reel (1080x1920, 30fps) built with HyperFrames, in the lockin-red style
(`styles/lockin-red/STYLE.md`), the look of the reference the user sent on 2026-10-14. It is the fifth reel of the
series and the first in this style.

It is motion design over the creator's voice-over:

- a "3 Mistakes I Fixed / To Land My First Client" list hub with blurred labels, which comes back before each mistake;
- one explanation per mistake:
  - a Project card next to a Result card;
  - a "Versatile Creative" bio that gets struck out;
  - a page of ten projects with no button, which the client closes;
- "A Portfolio Without A Next Step / Is A Gallery" with the projects in picture frames, then the template document;
- one-word captions, the footage card with the head popping out, three cutaways and a "Comment “Portfolio”" CTA.

**There is no music, on purpose:** the user adds their own track. Low whooshes and soft pops are part of the edit,
about 26 dB under the voice, as in reel 4.

- Render: `renders/portfolio-trap-reel.mp4`.
- Story and carousel images: `social/` (4 stories at 1080x1920 and 4 carousel slides at 1080x1350).
- Plan: `BRIEF.md`, `DESIGN.md` and `STORYBOARD.md`.

## Edit and re-render

```bash
npm run dev       # Studio preview
npm run check     # lint, layout, motion and contrast gates
npm run render    # MP4 into renders/ (delivery quality, 30fps, PNG frame extraction)
```

On the cloud sandbox's CPU, the whole check runs past the CLI's fixed 120s limit. Run it in three ranges instead:
`npx hyperframes@0.8.157 check --json --range 0,12.4 --samples 3`, then `12.4,24.8` and `24.8,37.2`.

- `python3 tools/gen_scenes.py` writes every scene (`compositions/s01-…s13-*.html`). Each keeps its timing in
  global voice-over seconds via `at(t)`.
  - The style's pieces are helpers: `title()` (hub title on the red bar), `rows()` and `hub_return()` (the list
    hub), `crumb()` (breadcrumb bar) and `cut()` (full-screen cutaway).
- `python3 tools/assemble.py` writes the scene slots, the footage strip, the captions and the SFX into
  `index.html`.
  - The strip's footage moment is chosen per line (`STRIP`).
  - Captions are one word at a time. The term "The Gallery-Portfolio Trap." and the CTA keyword "Portfolio" are serif
    italic.
- The footage grade is baked into `desk.mp4` and `desk-cutout.webm` by `tools/bake_grade.sh`, from the `*-raw`
  files: true blacks, a neutral white balance, a slightly brighter face and light sharpening.
  - The look is a canonical treatment (`tools/grade.json`), built into a 3D LUT with
    `hyperframes media-use resolve --type lut --params`.
  - For the original look, copy the raw files over the graded ones.
- `assets/css/lockin.css` is a copy of `styles/lockin-red/components.css`.
- Word timings are in `transcript.json`, force-aligned from `tools/spoken.txt` with the repo's `tools/align_vo.py`.
