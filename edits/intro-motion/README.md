# Intro motion: "I'm Fred, and I'm a web designer…"

**Deliverable:** `fred-intro_voiced.mp4`. It is 1920×1080, 30 fps and 33.0 s. It is your kinetic-typography intro, narrated in your cloned voice, with the text retimed so each word appears as it is spoken.

## Voice clone
- **Model:** [Chatterbox](https://github.com/resemble-ai/chatterbox) (Resemble AI, MIT licence) on CPU. Every clip it generates carries Resemble's inaudible "Perth" watermark, which marks it as AI-generated audio.
- **Reference:** `voice/voice_reference_ep2.wav` is 13.5 s of Fred from the episode 2 take, with pauses removed.
- **Lines:** the narration was generated line by line (`clone_tts.py`, exaggeration 0.5, cfg 0.5), and each line was checked with Whisper.
  - "Likes." on its own came out as "let it go", so it was regenerated in context as "Likes. Comments like…"; 2 of 4 takes were correct and take 0 is used.
- **Assembly:** `assemble_vo.py` trims each line, adds pauses that follow the script's rhythm, applies an EQ that matches the long-term spectrum of the real episode 2 voice (low end never boosted), compresses lightly and normalizes. The result is `voice/narration_cloned.wav`.
- **Speaker similarity** to the episode 2 voice (Resemblyzer):

  | Sample | Similarity |
  |---|---|
  | Clone, after EQ | 0.94 |
  | Clone, raw | 0.84 |
  | Real Fred, episode 1 take | 0.81 |
  | Model default voice | 0.60 |

## Sync
`retime.py` aligns the video to the voice:
1. It detects the source video's 59 text events by frame differencing.
2. It anchors each event on its spoken word (Whisper word timestamps; the first word uses the actual audio onset).
3. It plays each animation at 1x and stretches or squeezes only the hold that follows, so the text lands 50 ms before each word.

Measured result: the mean offset is −0.04 s and the worst is 0.11 s. The text follows the on-screen wording ("design something good, and smart"), not the script's "something like good". Audio is −14.6 LUFS.
