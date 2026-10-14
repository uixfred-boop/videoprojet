---
workflow: general-video
flow: automation
storyboard: no
message: "A beautiful portfolio that brings no clients is a gallery: show results, say what you sell, give a next step."
destination: instagram-reels (trial reel)
aspect: 1080x1920
language: en
audience: web designers whose portfolio gets compliments but no client messages
length: 37.2s
angle: listicle
---

## Intent

Trial edit B of reel 5 (`../portfolio-trap-reel/`). The user's words (2026-10-14): "Okay, now I want two other
versions of this one that I could use as trial reels, so two other different edits but with the same reference."

- **Same:**
  - the voice-over and its timing;
  - the script;
  - the footage;
  - the lockin-red style (`../../styles/lockin-red/STYLE.md`);
  - the one-word captions;
  - no music, and quiet SFX.
- **Different:** the hook, the visual idea of every scene and the footage moments.
  - One object carries the whole film: "your" portfolio on a phone. This is the "makeover" edit.
  - **Hook:** "Beautiful Portfolio, / Empty Inbox". Likes float up from the work, then the inbox is empty.
  - **Hub:** the phone, annotated with the three mistakes (connector lines to numbered glass rows), titled "3 Mistakes
    That Kept / My Inbox Empty".
  - **Spokes:** each one zooms into its part of the page while the client (the reference's red avatar badge) reacts.
  - **"Gallery":** the phone stands behind a museum rope.
  - **"My template":** fixes the three parts of the page live, and a new message arrives as a bookend to the empty
    inbox.
  - **CTA:** "PORTFOLIO" is typed into a comment and posted.
- **Edit C** (`../portfolio-trap-reel-c/`) is the third version: a faster cut with a face-first hook.

## Assets

The same files as reel 5, copied; git stores identical files once.

- `assets/audio/voiceover-master.wav`: the -16 LUFS master, word-aligned in `transcript.json`.
- `assets/video/desk.mp4` and `desk-cutout.webm`: the graded footage and its background-removed cutout. The `*-raw`
  files are the originals, and `tools/bake_grade.sh` and `tools/grade.json` rebuild the grade.

## Notes

- No invented numbers. "Ten projects" and "zero clear button" are the script's words.
- The phone's thumbnails are abstract placeholders. The bio "Versatile Creative" is the script's example, and the
  fixed bio is yellow highlight lines rather than an invented offer.
