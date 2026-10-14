# "The gallery-portfolio trap", trial edit B ("makeover"): Instagram Reel

A 37.2-second vertical reel (1080x1920, 30fps) built with HyperFrames in the lockin-red style
(`styles/lockin-red/STYLE.md`). It is a second edit of reel 5 (`videos/portfolio-trap-reel/`), made to post as a
trial reel. It has the same voice-over, script and footage, but a different hook and different visuals.

One object carries the film: "your" portfolio on a phone.

- **Hook:** "Beautiful Portfolio, / Empty Inbox". Likes float up from the work, then the inbox is empty.
- **The mistakes:**
  - the phone annotated with the three mistakes;
  - a zoom into each part while the client reacts ("Cool. But What Do I Get?", "…Now What?");
  - the page swiped away.
- **"Gallery":** the phone behind a museum rope.
- **"My template":** fixes the grid, the bio and the missing button live, and a new message arrives.
- **CTA:** "PORTFOLIO" typed into a comment, then the waitlist button.

**There is no music, on purpose:** the user adds their own track. Soft sound effects are part of the edit, about
26 dB under the voice.

- Render: `renders/portfolio-trap-reel-b.mp4`.
- Plan: `BRIEF.md` and `STORYBOARD.md`. The look is described in `../portfolio-trap-reel/DESIGN.md`.
- The third version is `../portfolio-trap-reel-c/` (a faster cut with a face-first hook).

## Edit and re-render

```bash
npm run dev       # Studio preview
npm run render    # MP4 into renders/ (delivery quality, 30fps, PNG frame extraction)
```

On the cloud sandbox's CPU, the whole check runs past the CLI's fixed 120s limit. Run it in three ranges instead:
`npx hyperframes@0.8.157 check --json --range 0,12.4 --samples 3`, then `12.4,24.8` and `24.8,37.2`.

- `python3 tools/gen_scenes.py` writes every scene (`compositions/b01-…b13-*.html`). Each keeps its timing in
  global voice-over seconds via `at(t)`.
  - `page()` and `phone()` draw the phone and the portfolio page.
  - `hub_body()` lays out the annotated hub.
  - `zoom_mask()` fades the zoomed phone out above and below the graphic zone.
- `python3 tools/assemble.py` writes the scene slots, the footage strip (`STRIP`), the captions and the SFX into
  `index.html`.
- The media are reel 5's files: the -16 LUFS voice-over master, and the graded footage with its background-removed
  cutout (`tools/bake_grade.sh` rebuilds the grade from the `*-raw` files).
