# videoprojet

## Motion text standard

- **Typeface:** Grandstander Medium (500), used for all text:
  `assets/fonts/Grandstander-Medium.ttf` (SIL Open Font License, see
  `assets/fonts/OFL.txt`). Install it on your machine to use it in your
  editing software.
- **Style:** black and white kinetic typography cut to the beat, from
  `references/motion-style-reference.mp4`. The move for each word depends on
  what the text means. Rules: `CLAUDE.md`. Values: `motion-text/style.json`.
- **Renderer:** `python3 motion-text/render.py motion-text/examples/demo.json out.mp4 --beat`
  (needs Python 3 with Pillow, and ffmpeg).
- **Web / Remotion:** `motion-text/grandstander.css`.
