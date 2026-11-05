# Episode 2 (YouTube, 16:9): "This portfolio got me $7,000…"

**Deliverable:** `ep2_7000-portfolio_youtube_4K.mp4`. It is 3840×2160, 30 fps, 24.5 s, H.264 High@5.2 two-pass at 45 Mbps (YouTube's 4K SDR recommendation) and 138 MB. It is gitignored because it is over GitHub's 100 MB limit.

It contains no captions, no titles and no sound effects; this was requested. The audio is voice only, at −13.7 LUFS.

The source is one native-4K take (`1103(1).mp4`, 28.4 s), shared from Google Drive.

## What was done
- **Cut to the script.** Every pause was removed; there are 11 clips and the take goes from 28.4 s to 24.5 s.
  - The opening line is spoken as "This portfolio got me $7,000 from one single client," which differs from the script's "…a $7,000 client".
  - "Have you … ever done" had a 1 s hesitation, which was removed.
- **Background replacement:**
  - Robust Video Matting (ResNet-50) runs on every 4K frame (`matte.py`, downsample 0.2).
  - `composite2.py` re-centres the person: the head moves from 44.8 % to 50 % of the width, a 200 px shift.
  - Edge decontamination makes soft edges take colour from inside the silhouette, so the old grey wall never shows. The alpha gets a 6 % choke.
  - A light wrap (0.12) and a subtle cool rim on the right, motivated by the blue shelf LEDs, tie the light together.
  - The plate (`plate.webp`) is cropped clear of its border and given grain matched to the camera noise.
- **Grade and finish:** `render16.py` applies the shared LUT `editing-style/lut/fred-warm-natural.cube` at native 4K, adds light sharpening and three zooms: a snap on "$7,000", a slow push on "…the answer was no", and a snap on "closed the deal".
- **Optional layers:** `compose16.py` still has the titles, captions and SFX. Run it with `TEXT=1`, `CAPTIONS=1` or `SFX=1` to turn them back on.

## Order
`matte.py` → `composite2.py` (in ≤2 parallel frame chunks; 3 at 4K runs out of memory) → concat into `comp.mp4` → `align.py` → `render16.py` → `compose16.py` → two-pass 45 Mbps encode.

## Background only, black hair (v3, latest)
The latest deliverable is `ep2_background-only_black-hair_4K.mp4`. It is the full uncut take (28.4 s) with the new background, the person re-centred, and no cuts, zooms, text or SFX. It is tagged BT.709 and is 138 MB, so it is gitignored.

`hair.py` builds the hair mask from three things multiplied together, then smooths it over time:
- the MediaPipe hair segmenter, run on a head crop each frame
- the RVM person matte, shifted 200 px like the composite
- a darkness gate, which protects skin at the hairline

Masked pixels lose all colour and are darkened to neutral black; a little texture is kept so the hair doesn't look painted. Measured on a sample frame, the hair goes from RGB (14, 14, 20), a blue-grey, to (9, 9, 9). The rest of the frame is unchanged. MediaPipe needs `libegl1` on Linux.
