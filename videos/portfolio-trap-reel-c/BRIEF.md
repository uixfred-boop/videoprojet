---
workflow: general-video
flow: automation
storyboard: no
message: "A beautiful portfolio that brings no clients is a gallery: show results, say what you sell, give a next step."
destination: instagram-reels (trial reel)
aspect: 1080x1920
language: en
audience: web designers whose portfolio gets compliments but no client messages
length: 34.0s
angle: listicle
---

## Intent

Trial edit C of reel 5 (`../portfolio-trap-reel/`). The user's words (2026-10-14): "Okay, now I want two other
versions of this one that I could use as trial reels, so two other different edits but with the same reference."

- **Same:**
  - the script and the voice;
  - the footage;
  - the lockin-red style (`../../styles/lockin-red/STYLE.md`);
  - the one-word captions;
  - no music, and quiet SFX.
- **Different:** this is the "fast cut".
  - **Pace:** the voice-over's pauses are tightened, from 36.7s to 33.6s. Every breath and word is kept; only the quiet
    stretches between words are shortened, to about 0.18s. That is about 3.5 words/s, the reference's density (reel 5
    runs at 3.2).
  - **Hook:** face first. The headline "Beautiful Portfolio, / So Why No Clients?" sits over a big footage card of the
    lean-in, then cuts to a giant red "0" on "no client".
  - **Five face shots** land on the payoff lines, as in the reference (about a quarter of the runtime): the trap, "what
    it brings them", "almost everyone misses it", and "the client closes", besides the hook.
  - **Typographic statements** instead of illustrations:
    - a giant outline number on One / Two / Three;
    - "Projects" struck out, then "Results";
    - a jumble of services collapsing into "Versatile Creative", stamped "Speaks To No One";
    - 10 / 0 counters;
    - "Portfolio − Next Step = Gallery";
    - three stacked template buttons;
    - a comment bubble typing "Portfolio";
    - a waitlist that gets your name.
- **Edit B** (`../portfolio-trap-reel-b/`) is the other version: the "makeover" of a phone portfolio, at the original
  pace.

## Assets

- `assets/audio/voiceover-tight.wav` is the tightened voice-over, made by `tools/tighten_vo.py` from reel 5's master
  (`voiceover-master.wav`, kept here as its source).
  - It is -15.8 LUFS integrated, -1.5 dBFS peak.
  - The cut list is in `tools/vo_cuts.json`.
  - `transcript.json` is the remapped word timing; `tools/transcript-untrimmed.json` is reel 5's.
- `assets/video/desk.mp4` and `desk-cutout.webm`: the graded footage and its cutout, as in reel 5.

## Notes

- No invented numbers. "Ten projects" and "zero clear button" are the script's words. The services in the jumble are
  generic examples of what a "versatile creative" lists.
- The waitlist rows are blurred placeholder lines; the only readable name is "You".
