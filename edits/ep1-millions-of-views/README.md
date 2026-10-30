# Episode 1: "Millions of views. Zero clients."

Final edit: `ep1_millions-of-views_zero-clients.mp4`. It is 1080×1920, 30 fps, 45.5 s, −14.5 LUFS, edited in the house style from `editing-style/STYLE_GUIDE.md`.

The sources were two raw takes: take A (10291) is the first half of the script and take B (10293) is the second half.

## Pipeline (`pipeline/`)
1. `edl.py` lists the clips (source, in, out, caption text) and the zoom keyframes.
2. `align.py` uses Whisper word timestamps, prompted with the script, to time the captions word by word.
3. `render_clips.py` trims each clip, scales it to 1080×1920, matches white balance per clip (the raw takes drift from warm to blue), applies the warm grade and the slow/snap zooms.
4. `compose.py` builds the typewriter titles, handwritten notes, word captions (ASS), PNG cards, the synthesized SFX palette (boom / pop / ding / swish / ticks) and the final mix and render.

## Placeholders to replace
- The "designer vs developer" card and the "≈ 3,000,000 views" badge stand in for the real clips and the real view count (`[montre des extraits]` / `[montre la vidéo]`).
- The end profile card shows "Fred · web designer" and has no @handle.
