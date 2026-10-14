# videoprojet: notes for Claude

This repo holds the user's Instagram Reel edits: motion design over their voice-over and B-roll, built with
HyperFrames (`.claude/skills/`, entry point `/hyperframes`). There is also a Remotion "Hello World" scaffold at the
root (`src/`); it isn't used for the reels.

## Default style for new edits

**Follow `styles/listicle-crimson/STYLE.md`.** The user named it the reference for their next edits. It is a
listicle hub card, numbered glass tiles, breadcrumb headers, ghost typing, crimson wires and a "Comment 'x'" CTA, on
a dark grid with crimson `#99122B`. Reusable CSS is in `styles/listicle-crimson/components.css`. Style frames are in
`styles/listicle-crimson/frames/`.

The split layout (graphics on top, seam captions, B-roll card with head pop-out, full-screen cutaways) comes from the
earlier references and is documented in `videos/web-design-7k-reel/DESIGN.md`.

A second reference from the same creator family is analysed in `styles/lockin-red/STYLE.md` (2026-10-14). It has:
- pure red `#B80000` on a black dot grid;
- a numbered-list hub with blurred labels;
- a "Video Script" document with yellow highlights;
- one-word captions.

Reusable CSS is in `styles/lockin-red/components.css`, and reel 5 (`videos/portfolio-trap-reel/`) uses it.
It is not the default: use it when the user asks for that look or sends that reference with a script.

The repo is **public**. Don't commit third-party reference videos or their frames; describe them in text.

## Pipeline that works in the cloud sandbox

Finished examples (README in each): `videos/web-design-7k-reel/` (split layout), `videos/bought-portfolio-reel/`
(listicle-crimson, with generated scenes and a synthesised beat) and `videos/portfolio-trap-reel/` (lockin-red).

- **New project:** `npx hyperframes init "videos/<name>" --non-interactive --example=blank --skill=general-video`.
  - The CDN is blocked. Ship GSAP locally (`npm pack gsap@3.14.2` → `assets/vendor/gsap.min.js`) and fonts from
    `@fontsource/*`.
  - Asset paths must be root-relative (`assets/...`), even inside `compositions/`.
  - Each file needs its own `@font-face` block.
  - Wrap every sub-composition script in an IIFE.
  - From CLI 0.8.157, lint fails on a sub-composition root styled by class. Give the root `id="root"`, style it as
    `#root`, and find it in the script with `[data-composition-id="…"]`. Lint also warns on a negative `z-index` (use
    DOM order) and on `tl.set` hides at 0 (use inline styles).
  - A `fromTo` draws its from-state as soon as the timeline is built. An element that must stay invisible until its
    tween needs `immediateRender: false` or an opacity-0 from-state. Reel 5's first render showed every ping circle
    as a small red dot before it fired.
- **Trial-reel versions of one reel:** copy the project folder (`videos/portfolio-trap-reel-b/`, `-c/`). Git stores
  identical media once, so the copies cost no repo space. Change the hook, the scene ideas and the footage moments. The
  "fast cut" version also trims the voice-over's pauses with `videos/portfolio-trap-reel-c/tools/tighten_vo.py`.
- **Word timings:**
  - `hyperframes transcribe` can't download Whisper here (huggingface.co is blocked).
  - Force-align the script with PocketSphinx instead: `tools/align_vo.py` (run it from a venv with
    `pip install pocketsphinx`). Example output: `videos/web-design-7k-reel/transcript.json`.
- **Head pop-out:** `npx hyperframes remove-background broll.mp4 -o broll-cutout.webm` works offline (~5 min for
  27s). Overlay it above the footage card, clipped to the strip just above the card's top edge.
- **Instagram is blocked.** Ask the user to upload reference reels as files.
- **Audio:**
  - Master the voice-over to about -16 LUFS (`acompressor` + two-pass `loudnorm`).
    - A **mono** master plays on both channels at full level in the render, so -16 LUFS mono is -13 LUFS in the
      mix.
    - After the renderer's true-peak trim, the reels land around -14 LUFS, which suits Instagram.
  - There is no music library offline, so music is synthesised with numpy + scipy:
    - `videos/web-design-7k-reel/tools/make_bed.py` is a quiet lo-fi bed;
    - `videos/bought-portfolio-reel/tools/make_beat.py` is a dynamic trap beat. Its tempo grid bends between anchor
      downbeats so the drops and stops land on chosen words.
  - Carve the music under the voice with `.claude/skills/hyperframes-audio/scripts/carve.mjs` (needs
    `npm i -D @hyperframes/core@<cli version>` in the project). Strength 0.45 keeps a beat about 10 dB under the
    voice, and about 15 dB under it in the speech band.
  - When the user may add their own music, also deliver a no-music version: remux the rendered picture with
    `tools/simulate_mix.py --mute music-bed --out …` instead of rendering twice. Null-test that simulation against the
    render's audio first.
  - SFX come from `.claude/skills/media-use/audio/assets/sfx/`. The `impact-bass-*` files are mastered at full
    scale: keep them at ≤0.06–0.2 volume and trimmed.
  - A `data-automation` volume lane **replaces** `data-volume` instead of scaling it. Bake trims and fades into the
    files.
  - Simulate the mix before rendering with `python tools/simulate_mix.py videos/<name>` (from a venv with numpy +
    scipy). It applies carve chains and lanes and prints loudness and true peak. The renderer lowers the whole mix if
    the true peak exceeds -1 dBTP.
- **Dark footage:**
  - Choose and validate a correction with `npx hyperframes media-treatment --analyze` / `--grading`.
  - Don't lift the shadows. The `shadows` control also raises the black point, and on reel 4 the user saw black
    hair and a black t-shirt turn grey and "yellowish".
    - Brighten with `exposure` and hold the floor with negative `blacks`.
    - Check the white balance: warm indoor light reads yellow.
    - Measure hair, clothes, face and wall before and after.
  - Compare candidates with `npx hyperframes grade-compare --for frame.png --grades grades.json`. Re-save ffmpeg's
    PNGs with PIL first: their cICP/gAMA chunks make Chrome darken the shadows in every cell.
  - Don't ship it as realtime `data-color-grading` on many `<video>`s: with no WebGL here, it crashed
    `hyperframes check` ("Target closed").
  - Bake it into the files instead:
    - build the treatment's `adjust` values into a LUT with `npx hyperframes media-use resolve --type lut --params`;
    - apply it with ffmpeg `lut3d`, with explicit BT.709 conversions and tags.

    See `videos/views-vs-clients-reel/tools/bake_grade.sh`.
  - Grade the background-removed cutout the same way so the pop-out matches. Choke its alpha, or its soft matte
    draws a wall-coloured rim around the hair.
- **Check:** `npx hyperframes check` takes about 8 min for a 114s reel. Its terminal output is long, so run it with
  `--json > file` to keep the findings. Ghost-typing letters show up as contrast warnings by design.
  - From CLI 0.8.157 the check stops after a fixed 120s ("Check did not finish within its deadline", with
    `browserSkipped: true`), and a whole reel runs past that on this CPU. `--timeout` doesn't change it. Check in
    ranges instead, e.g. `--range 0,12.4 --samples 3`, which takes about 1 min each.
- **Render:** `npx hyperframes render -q delivery --fps 30 --video-frame-format png` takes about 7 min for 64s at
  1080x1920 on this CPU.
  - Keep `--video-frame-format png` whenever footage or screen recordings are in the reel. The default extracts
    video frames as JPEG (q:v 7), which smears dark footage and small UI text.
  - Chat uploads are capped at 30 MB, so keep the master in the repo and send a 2-pass preview copy.
  - Use ~3.3 Mbps for a 60s reel. For longer reels, scale the bitrate down or encode at 720x1280 to stay under the cap.
