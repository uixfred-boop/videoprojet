# YouTube episode: "This portfolio got me a $7,000 client"

The edit follows the reference breakdown in `editing-style/YOUTUBE_REFERENCE_KALLAWAY.md`.

**Deliverable:** `ep3_7000-portfolio_youtube_4K.mp4`.
- **Video:** 3840×2160, 30 fps, 4:58 (8,942 frames), H.264 High@5.2 two-pass at 45 Mbps, BT.709.
- **Audio:** voice only, AAC 320 kbps, −14.5 LUFS, loudness range 2.4 LU.
- **Size:** about 1.5 GB, so it is gitignored and delivered directly.
- **Requested by Fred:** no music and no sound effects.

## Cut (pipeline/edl.json)
- **Source:** one 6:50 4K take, `YOUTUBE.mp4`, cut down to 4:58. All pauses are gone, and for each retake the cleanest complete take was kept.
- **Choosing takes:** speech was split into 123 phrases by silence and each was transcribed on its own (`raw_phrases_transcript.txt`). Mid-sentence cuts use word timings re-measured locally (`localwords.py`). The assembled voice was re-transcribed to check that no word is clipped.
- **Not in the footage:** script section IV ("The trap") and the line "Watch." before the reveal were never recorded.
  - The reveal still happens: 18 s of silent site walkthrough, with no music because Fred asked for none.
- **Wording kept as spoken, not as scripted:**
  - "So I'm Fred, a web designer"
  - "Your result will depend on your work and your outreach. It's not simple or magic", which Fred added himself.

## Picture
- **Background:** every talking-head frame is matted with Robust Video Matting. The alpha is stored at 1080p, and the 4K compositing is done in ffmpeg (`thclip.py`) over the episode-2 room plate (`plate4k.png`, built from `edits/ep2-7000-portfolio/pipeline/plate.webp`).
  - **Edges:** a choke, plus edge darkening (fg·α²) so the old grey wall never rims the hair. Setup A uses a stronger choke because its wall was lighter.
  - **Matte timing:** the matte files store millisecond timestamps, while the camera file uses exact 1/30 s ones. If the compositor pairs frames by timestamp, every third frame gets the previous frame's matte, which shows as a flickering light rim when the head moves. `thclip.py` instead seeks both inputs half a frame before the first wanted frame and re-times them by frame index, so frame N of the picture always gets matte N.
- **Two camera setups matched:** setup B is scaled 0.975 and lowered 8.5 % so the head size and headroom match setup A. The ending take (setup C) is white-balanced on skin to match B.
- **Grade:** per-setup white balance from the wall, then `person.cube` (gentle contrast) and `look.cube` on the whole frame (cool shadows, warm highlights, deep blacks with detail), plus a light vignette.
- **Reframing:** wide 1.0, medium 1.05 and tight 1.10, switched on cuts, with slow push-ins (+4 %) on build-ups. Zooms are anchored high so the head always keeps headroom.

## Graphics (blue glass system, `gfx.py` + `scene.py`)
- **Element types:** chapter cards ("PART 0X", with a 9-step progress bar), numbered lists, check/cross lists, a quote card, the path diagram, the add/remove cards, "less" chips, a persona dots graphic, the outreach flow, the equation (Same designer + Different perception = $7,000), "Takeaway" lower thirds, side-panel lists, a name tag, and screen recordings in browser frames.
- **No URL:** the browser frames show no address, because no real domain was given.
- **Screen recordings** come from Fred's own captures in the raw file (120–198 s, 363–386 s).
- **Layout:** about 42 % face and 58 % graphics/screens. 1 min 40 s of the narration was recorded over screen captures, with no face available, which is why the face share is lower than the reference's 58 %.

## Rebuild
`matte.py` (per setup range) → `build.py <work>` (shot list + elements) → `render_shots.py <work> gfx|face` → `assemble.py <work> <out>`. Shots are rendered frame-exact and padded to their exact length during assembly, which keeps lip-sync locked.
