"""Forced alignment of the cut list's text onto the final voice track, clip by clip: the known text is given to Whisper
as a decoder prefix, so the words are exactly the script's and only their timing comes from the audio."""
import json, re, subprocess, sys, difflib
import numpy as np
from faster_whisper import WhisperModel
E = sys.argv[1]; FPS = 30
clips = json.load(open(f"{E}/edl.json"))["clips"]
t = 0.0
for c in clips:
    c["d"] = c.get("silent") or round((c["b"] - c["a"]) * FPS) / FPS; c["t"] = t; t += c["d"]
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{E}/vo_master.wav", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
audio = np.frombuffer(pcm, np.float32)
m = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=8)
norm = lambda s: re.sub(r"[^a-z0-9$']", "", s.lower().replace("’", "'").replace(",", ""))
out = []
for c in clips:
    if c.get("silent"): continue
    a = max(0.0, c["t"] - 0.05); b = c["t"] + c["d"] + 0.05
    seg = audio[int(a * 16000):int(b * 16000)]
    segs, _ = m.transcribe(seg, language="en", word_timestamps=True, beam_size=1, prefix=c["text"], condition_on_previous_text=False,
                           without_timestamps=True)
    ws = [w for s in segs for w in s.words]
    toks = [x for x in c["text"].replace("...", " ").replace("—", " ").split() if norm(x)]
    sm = difflib.SequenceMatcher(None, [norm(x) for x in toks], [norm(w.word) for w in ws], autojunk=False)
    got = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op in ("equal", "replace") and i2 - i1 == j2 - j1:
            for k in range(i2 - i1):
                w = ws[j1 + k]; out.append({"w": toks[i1 + k], "s": round(a + w.start, 3), "e": round(a + w.end, 3), "clip": c["id"], "i": i1 + k}); got += 1
    print(c["id"], f"{c['t']:.2f}", f"{got}/{len(toks)}", flush=True)
json.dump(out, open(f"{E}/words_forced.json", "w"), indent=0)
print("aligned words", len(out))
