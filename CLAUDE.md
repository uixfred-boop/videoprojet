# videoprojet: standing rules for motion text

These rules apply to **every** motion text, caption, title and on-screen word
in this project unless the user says otherwise for one shot. The style comes
from `references/motion-style-reference.mp4` (notes in `references/README.md`).
Exact values are in `motion-text/style.json`.

## 1. Typeface (mandatory)

- **Grandstander Medium (weight 500) for all text.** No other family, no other
  weight. File: `assets/fonts/Grandstander-Medium.ttf`.
- Emphasis comes from motion, scale or the inverted card, never from another
  font or weight. A lean/italic look is a shear applied to the letters.
- Web / Remotion: `motion-text/grandstander.css`. ffmpeg: `fontfile=assets/fonts/Grandstander-Medium.ttf`.
- Use curly apostrophes (it’s, don’t).

## 2. Look

- Black and white only: background `#0A0A0A`, text `#FFFFFF`, words not yet
  said `#535353`. Inverted card: white background, text `#282828`.
- No accent color, no outline, no shadow, no box.
- Centered, one line, 1 to 3 words on screen at a time. Font size about 17% of
  frame height, shrunk to fit 82% of the frame width.
- Keep the casing as written (mostly lowercase).

## 3. Rhythm

- Hard cuts between shots, no crossfades. Every cut lands on the beat
  (reference: about 155 BPM).
- Normal pace: one shot every 1 to 2 beats. Climax: one word every half beat
  (about 0.2 s). Speed up toward the end.
- Ask for the music or its BPM; without one, use 155 BPM.

## 4. Read the text, then choose the move

Before animating, split the text the way it is spoken, find the **key word of
each sentence** (the word the sentence is really about) and decide what each
part is doing. Then pick the move:

| What the words are doing                                   | Move                                   | Reference example                |
|------------------------------------------------------------|----------------------------------------|----------------------------------|
| Opening, greeting, first word of a new idea                | `punch` (scale from 165% to 100%)      | Hi, This, rhythmic               |
| A question or phrase that builds as it is said             | `build` (words wiped in one by one)    | How are you?                     |
| **Key word / punchline** of a sentence                     | `invert` (white card, dark text)       | typography, perfect, important   |
|  · a name, product or "proud" word                         | `invert` + `track` (spacing opens up)  | promos                           |
|  · an exclamation, strong feeling, a short punchy word     | `invert` + `skew` (end leans, straightens) | yeah!, short, important      |
|  · the suspense payoff, a question to the viewer           | `invert` (plain fade to dark)          | ready?                           |
| A list of qualities, "X and Y", "X with Y"                 | `karaoke` (gray phrase, said word white) | Simple and powerful            |
| Build-up, suspense, words leading to a reveal              | `letters` (gray→white, left to right)  | it’s getting hot… faster…        |
| Small linking words between two ideas                      | `wipe` or `cut`                        | tool, for                        |
| Fast imperative or motivational run                        | `cut`, half a beat each                | Dream big and work hard          |

Exits: `cut` by default. Use `slide` (speeds off to the right while dimming)
on the shot just before an inverted card or at the end of a section. Use
`wipe` to close a phrase that was built up.

Rules of thumb:
- At most **one inverted card per sentence**, about 1 shot in 7. That is what
  keeps it hitting hard.
- Function words ("the", "and", "to") never get the invert or a big punch.
- If the meaning or the key word is unclear, ask rather than guess.

## 5. Chapter titles (user's choice)

A chapter title is **one single shot on the white card, no black** (no black
lead-in or tail either: `"pad": "invert"`). The chapter number appears alone
in the center, then slides left while the chapter name appears beside it. The
name leans and straightens as it lands, then the whole title is wiped out.
Keep the user's wording and casing (e.g. "I. MISTAKES").
Template: `motion-text/timelines/chapter-1-mistakes.json` (`build` +
`"invert": true` + `"variant": "skew"`, `"wordAt": [0, 2]`, `"shiftSeconds": 0.25`).

## 6. How to deliver

1. Write the shot list as a timeline in `motion-text/timelines/<name>.json`
   (format documented at the top of `motion-text/render.py`;
   example: `motion-text/examples/demo.json`).
2. Render it: `python3 motion-text/render.py <timeline>.json out.mp4`
   (add `--beat` for a guide beat when there is no music; set `"audio"` in the
   timeline to use the real track, `"size": [1080, 1920]` for vertical).
3. Check a contact sheet of the render before handing it over.
4. If the user edits in another tool (After Effects, Premiere, CapCut…), give
   the same shot list with moves, timings and values from `style.json`.
