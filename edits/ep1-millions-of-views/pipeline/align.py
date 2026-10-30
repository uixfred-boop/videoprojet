"""Word-level caption timing per clip: whisper (prompted with the script text) + difflib alignment."""
import json, re, sys, difflib
import numpy as np
from scipy.io import wavfile
from faster_whisper import WhisperModel
sys.path.insert(0, sys.argv[1])
from edl import CLIPS, FPS

work = sys.argv[2]
q = lambda t: round(t * FPS) / FPS
norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower())
m = WhisperModel("medium.en", device="cpu", compute_type="int8")
audio = {}
for s in ("A", "B"):
    sr, a = wavfile.read(f"{work}/raw{s}.wav"); audio[s] = a.astype(np.float32) / 32768

out = {}
for cid, src, s, e, text in CLIPS:
    s, e = q(s), q(e); dur = e - s
    seg = audio[src][int(s * 16000):int(e * 16000)]
    segs, _ = m.transcribe(seg, word_timestamps=True, beam_size=5, language="en",
                           initial_prompt=text, condition_on_previous_text=False)
    ww = [(w.start, w.end, w.word.strip()) for sg in segs for w in sg.words]
    cap = text.split()
    sm = difflib.SequenceMatcher(None, [norm(x) for x in cap], [norm(w[2]) for w in ww])
    st = [None] * len(cap)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            st[blk.a + k] = ww[blk.b + k][0]
    # interpolate unmatched by character length
    known = [(i, t) for i, t in enumerate(st) if t is not None]
    anchors = [(-1, 0.0)] + known + [(len(cap), dur)]
    for (i0, t0), (i1, t1) in zip(anchors, anchors[1:]):
        if i1 - i0 > 1:
            for k in range(i0 + 1, i1):
                st[k] = t0 + (t1 - t0) * (k - i0) / (i1 - i0)
    st[0] = min(st[0], 0.05)
    st = [min(max(t, 0.0), dur - 0.05) for t in st]
    for k in range(1, len(st)):
        st[k] = max(st[k], st[k - 1] + 0.06)
    out[cid] = {"src": src, "start": s, "end": e, "words": [[w, round(t, 3)] for w, t in zip(cap, st)],
                "heard": " ".join(w[2] for w in ww), "matched": sum(1 for b in sm.get_matching_blocks() for _ in range(b.size))}
    print(cid, f"{out[cid]['matched']}/{len(cap)}", "|", out[cid]["heard"], "|", [(w[0],round(w[1],2)) for w in out[cid]["words"]][:4], [(round(a,2),t) for a,b,t in ww][:3])
json.dump(out, open(f"{work}/words.json", "w"), indent=1)
