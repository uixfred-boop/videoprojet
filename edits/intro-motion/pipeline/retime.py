"""Retime a kinetic-typography video to a narration: each text event lands on its spoken word.
Each event's animation plays at 1x (squeezed only if there's no room); the static hold after it absorbs the difference.
usage: retime.py src.mp4 narration.wav events.json out.mp4"""
import json, re, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

src, vo, ev_p, out = sys.argv[1:5]
FPS, LEAD, TAIL = 30, 0.05, 1.4   # text appears 50 ms before the word; hold the last word 1.4 s after speech
E = json.load(open(ev_p))         # [{"t0":start,"t1":end,"word":str|None}], last one = outro
norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower().replace("’", "'"))

raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", vo, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                     capture_output=True, check=True).stdout
m = WhisperModel("medium.en", device="cpu", compute_type="int8")
segs, _ = m.transcribe(np.frombuffer(raw, np.float32), word_timestamps=True, beam_size=5, language="en",
                       condition_on_previous_text=False)
words = [(w.start, w.end, norm(w.word)) for s in segs for w in s.words]
# whisper tends to put the first word at 0.0: use the real audio onset instead
x = np.frombuffer(raw, np.float32); h = 160; n = len(x) // h
db = 20 * np.log10(np.sqrt((x[:n * h].reshape(n, h) ** 2).mean(1)) + 1e-9)
onset = np.argmax(db > db.max() - 35) * h / 16000
words[0] = (max(words[0][0], onset), words[0][1], words[0][2])
speech_end = words[-1][1]

# anchor each worded event on the next matching spoken word, in order
j, anchors = 0, []
for e in E:
    if e["word"] is None: anchors.append(None); continue
    k = next(i for i in range(j, len(words)) if words[i][2] == norm(e["word"]))
    anchors.append(words[k][0] - LEAD); j = k + 1
for i, a in enumerate(anchors):        # unanchored events keep their original offset from the previous event
    if a is None:
        anchors[i] = anchors[i - 1] + (E[i]["t0"] - E[i - 1]["t0"]) if i else E[i]["t0"]
outro = speech_end + TAIL
anchors[-1] = max(anchors[-1], outro)

# segments: [0, first event) + each event up to the next one; build trim/setpts chains
cuts = [0.0] + [e["t0"] for e in E]
targets = [0.0] + anchors
dur_src = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                               capture_output=True, text=True).stdout)
cuts.append(dur_src); targets.append(anchors[-1] + (dur_src - E[-1]["t0"]))
fc, labels, plan = [], [], []
for i in range(len(cuts) - 1):
    a, b = cuts[i], cuts[i + 1]; new = targets[i + 1] - targets[i]
    anim_end = min(E[i - 1]["t1"] + 0.1, b) if i else a
    anim = anim_end - a; hold = b - anim_end
    if new < anim + 1 / FPS:                       # no room: squeeze the whole segment
        pieces = [(a, b, new / (b - a))]
    else:
        pieces = [(a, anim_end, 1.0)] if anim > 0 else []
        pieces.append((anim_end, b, (new - anim) / hold if hold > 0 else 1.0))
    for (x, y, k) in pieces:
        if y - x <= 1e-3: continue
        lab = f"s{len(labels)}"
        fc.append(f"[0:v]trim=start={x:.4f}:end={y:.4f},setpts=(PTS-STARTPTS)*{k:.5f}[{lab}]"); labels.append(lab)
    plan.append((round(a, 2), round(b, 2), round(targets[i], 2), round(new, 2)))
fc.append("".join(f"[{l}]" for l in labels) + f"concat=n={len(labels)}:v=1:a=0,fps={FPS},format=yuv420p[v]")
total = targets[-1]
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-i", vo, "-filter_complex", ";".join(fc)
                + f";[1:a]volume=2dB,alimiter=limit=0.89:level=false,apad,atrim=0:{total:.3f}[a]",
                "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
json.dump({"words": [(round(a, 2), w) for a, _, w in words], "plan": plan, "total": total},
          open(out.replace(".mp4", "_plan.json"), "w"), indent=1)
print("spoken words", len(words), "| events", len(E), "| new length", round(total, 2), "s")
