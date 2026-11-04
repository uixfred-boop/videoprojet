# Episode 1: "Millions of views. Zero clients."

Edited in the house style from `editing-style/STYLE_GUIDE.md` (30 fps, 45.5 s, −14.5 LUFS).

- **Master: `ep1_millions-of-views_zero-clients_4K.mp4`.** It is 2160×3840 (4K), H.264 High@5.2 at ~26 Mbps and 151 MB. It is not in git because it is over GitHub's 100 MB file limit; it was sent directly and can be rebuilt with the pipeline.
- `ep1_millions-of-views_zero-clients.mp4` is the first 1080p version, which used the older washed-out grade.

## Grade (v2)
Take A as shot is the reference look: neutral-warm and not blue. Each clip's white balance is matched to take A's wall, then `editing-style/lut/fred-warm-natural.cube` is applied. The LUT adds a gentle S-curve, keeps shadows neutral, warms the highlights slightly and adds 5% saturation, with no lifted blacks.
For 4K, the footage is lightly denoised, upscaled with lanczos and sharpened with unsharp; take B (720p) gets more sharpening. Cards are drawn natively at 4K.
Take A is 1080p and take B is 720p, so the 4K is an upscale. It is sharper and better encoded than before, but it cannot recover detail the phone didn't record. Shooting in 4K gets true 4K.

The sources were two raw takes: take A (10291) is the first half of the script and take B (10293) is the second half.

## Pipeline (`pipeline/`)
1. `edl.py` lists the clips (source, in, out, caption text) and the zoom keyframes.
2. `align.py` uses Whisper word timestamps, prompted with the script, to time the captions word by word.
3. `render_clips.py <dir> <work> <lut.cube>` trims each clip, matches its white balance to take A, applies the LUT, upscales to 2160×3840 with denoise and sharpening, and applies the slow/snap zooms.
4. `compose.py` builds the typewriter titles, handwritten notes, word captions (ASS), PNG cards, the synthesized SFX palette (boom / pop / ding / swish / ticks) and the final mix and render.

## Placeholders to replace
- The "designer vs developer" card and the "≈ 3,000,000 views" badge stand in for the real clips and the real view count (`[montre des extraits]` / `[montre la vidéo]`).
- The end profile card shows "Fred · web designer" and has no @handle.

## Background replacement versions (v3)
These are the same edit and grade with the wall swapped for a reference room, rendered at 4K and gitignored (they're 348/356 MB):
- `ep1_bg-lamp_4K.mp4`: warm lamp corner. The plate is reframed so the lamp sits beside the head with the window on the other side.
- `ep1_bg-living-room_4K.mp4`: living room with cove lighting and lit shelves.

How they're built:
1. `matte.py` runs Robust Video Matting (ResNet-50, ONNX) on every frame of both raw takes. The model is recurrent, so edges stay stable over time. It outputs alpha and a de-spilled foreground.
2. `composite.py <take> <alpha> <fgr> <plate> <plate.json> <out>`:
   - White-balances the person to take A each frame.
   - Pulls his colour toward the plate with a partial Lab transfer.
   - Adds warm side light from the practical's side and a light wrap at the silhouette edge.
   - Uses RVM's de-spilled colour on soft edges, so the old grey wall doesn't halo.
   - Gives the plate a slight blur (σ 4 px at 1080) and grain matched to the phone footage.
3. `render_clips.py … <lut> <variant>` renders from `comp_<take>_<variant>.mp4`; the white balance is already done at this point, so it only applies the LUT, 4K upscale and zooms. `compose.py` then runs with `CUT=` pointing to that cut, with the original cut's audio muxed in.

Per-plate settings (crop, blur, colour match, wrap, grain, side light) are in `pipeline/backgrounds/*.json`.
