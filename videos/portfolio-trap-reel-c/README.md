# "The gallery-portfolio trap", trial edit C ("fast cut"): Instagram Reel

A 34.0-second vertical reel (1080x1920, 30fps) built with HyperFrames in the lockin-red style
(`styles/lockin-red/STYLE.md`). It is a third edit of reel 5 (`videos/portfolio-trap-reel/`), made to post as a trial
reel. It has the same script, voice and footage, at a faster pace.

- **Pace:** the voice-over's pauses are tightened (36.7s → 33.6s). Breaths and words are untouched.
- **Hook:** face first. The headline "Beautiful Portfolio, / So Why No Clients?" sits over a big footage card, then a
  giant red "0".
- **Five face shots** land on the payoff lines, about a quarter of the runtime, as in the reference.
- **Graphics** are bold typographic statements:
  - "Projects" struck for "Results";
  - a jumble of services collapsing into "Versatile Creative";
  - 10 / 0 counters;
  - "Portfolio − Next Step = Gallery";
  - stacked template buttons;
  - a comment bubble and a waitlist.

**There is no music, on purpose:** the user adds their own track. Soft sound effects are part of the edit, about
27 dB under the voice.

- Render: `renders/portfolio-trap-reel-c.mp4`.
- Plan: `BRIEF.md` and `STORYBOARD.md`. The look is described in `../portfolio-trap-reel/DESIGN.md`.
- The other version is `../portfolio-trap-reel-b/` (the "makeover" of a phone portfolio, at the original pace).

## Edit and re-render

```bash
npm run dev       # Studio preview
npm run render    # MP4 into renders/ (delivery quality, 30fps, PNG frame extraction)
```

On the cloud sandbox's CPU, the whole check runs past the CLI's fixed 120s limit. Run it in three ranges instead:
`npx hyperframes@0.8.157 check --json --range 0,11.33 --samples 3`, then `11.33,22.67` and `22.67,34`.

- **Voice-over:** `python tools/tighten_vo.py` (from a venv with numpy + scipy) rebuilds the tightened voice-over
  from `assets/audio/voiceover-master.wav` and `tools/transcript-untrimmed.json`.
  - It writes `assets/audio/voiceover-tight.wav`, `transcript.json` and the cut list `tools/vo_cuts.json`.
  - `TARGET` sets the pause to keep (0.18s).
  - Inside a gap, only stretches quieter than `QUIET` (-46 dBFS) are cut, so breaths stay.
  - After changing it, retime the scenes: their times are written against this transcript.
- `python3 tools/gen_scenes.py` writes every scene (`compositions/c01-…c16-*.html`). Each keeps its timing in global
  voice-over seconds via `at(t)`.
  - The hook is its own big footage card. In `assemble.py` it is a "cut" scene, so it sits above the strip.
  - The main timeline raises the strip at 1.28s.
- `python3 tools/assemble.py` writes the scene slots, the footage strip (`STRIP`, with an optional per-clip rate), the
  captions and the SFX into `index.html`.
