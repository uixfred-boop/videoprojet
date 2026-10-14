#!/usr/bin/env python3
"""Trial edit C: tighten the voice-over's pauses, keeping every breath, and remap the word timings.

Inside each gap between two words longer than TARGET, only the quiet stretches (10 ms RMS below QUIET dBFS) are
removed, MARGIN in from their edges and never within GUARD of a word, until the gap is TARGET long or nothing quiet is
left. Breaths are louder than QUIET, so they stay. Joints get a short linear crossfade; both sides are quiet.
Run from a venv with numpy + scipy:
    python tools/tighten_vo.py
Reads  assets/audio/voiceover-master.wav (reel 5's master) and tools/transcript-untrimmed.json.
Writes assets/audio/voiceover-tight.wav, transcript.json and tools/vo_cuts.json (cut intervals in original seconds).
"""
import json
import pathlib

import numpy as np
from scipy.io import wavfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = 0.18     # s of pause to keep between words
QUIET = -46.0     # dBFS, 10 ms RMS
MARGIN = 0.03     # s kept at each edge of a quiet stretch
GUARD = 0.04      # s never cut next to a word
LEAD = 0.06       # s kept before the first word
XF = 0.010        # s crossfade at each joint
STEP = 0.01

fs, x = wavfile.read(ROOT / "assets/audio/voiceover-master.wav")
assert x.dtype == np.int16 and x.ndim == 1, (x.dtype, x.shape)
sig = x.astype(np.float64) / 32768.0
words = json.loads((ROOT / "tools/transcript-untrimmed.json").read_text())


def quiet_runs(a, b):
    """Quiet stretches inside [a, b], as (start, end) seconds."""
    runs, t, start = [], a, None
    while t + STEP <= b + 1e-9:
        seg = sig[int(t * fs):int((t + STEP) * fs)]
        db = 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-12)
        if db < QUIET and start is None:
            start = t
        elif db >= QUIET and start is not None:
            runs.append((start, t))
            start = None
        t += STEP
    if start is not None:
        runs.append((start, t))
    return runs


cuts = []
first = words[0]["start"]
if first > LEAD + 0.02:
    cuts.append((0.0, round(first - LEAD, 3)))
for w0, w1 in zip(words, words[1:]):
    a, b = w0["end"], w1["start"]
    need = (b - a) - TARGET
    if need <= 0.02:
        continue
    cand = []
    for s, e in quiet_runs(a + GUARD, b - GUARD):
        s, e = s + MARGIN, e - MARGIN
        if e - s > 0.02:
            cand.append((s, e))
    cand.sort(key=lambda r: r[1] - r[0], reverse=True)
    for s, e in cand:
        if need <= 0.02:
            break
        take = min(need, e - s)
        mid = (s + e) / 2
        cuts.append((round(mid - take / 2, 3), round(mid + take / 2, 3)))
        need -= take
cuts.sort()

# rebuild the audio: keep everything outside the cuts, crossfading each joint
keep, t = [], 0.0
for s, e in cuts:
    keep.append((t, s))
    t = e
keep.append((t, len(sig) / fs))
keep = [(s, e) for s, e in keep if e - s > 2 * XF]
xf = int(XF * fs)
out = sig[int(keep[0][0] * fs):int(keep[0][1] * fs)].copy()
for s, e in keep[1:]:
    seg = sig[int(s * fs):int(e * fs)]
    ramp = np.linspace(0, 1, xf)
    out[-xf:] = out[-xf:] * (1 - ramp) + seg[:xf] * ramp
    out = np.concatenate([out, seg[xf:]])
removed = len(sig) / fs - len(out) / fs


def remap(t):
    """Original seconds -> tightened seconds (a time inside a cut lands on its joint)."""
    shift = 0.0
    for k, (s, e) in enumerate(cuts):
        if t >= e:
            shift += (e - s) + (XF if s > 0 else 0.0)
        elif t > s:
            return round(s - shift - XF * 0.5, 3)
    return round(t - shift, 3)


new_words = [dict(w, start=remap(w["start"]), end=remap(w["end"])) for w in words]
wavfile.write(ROOT / "assets/audio/voiceover-tight.wav", fs, np.clip(np.round(out * 32768.0), -32768, 32767).astype(np.int16))
(ROOT / "transcript.json").write_text(json.dumps(new_words, indent=1) + "\n")
(ROOT / "tools/vo_cuts.json").write_text(json.dumps({"target": TARGET, "quiet_dbfs": QUIET, "cuts": cuts}, indent=1) + "\n")
print(f"cuts: {len(cuts)}, removed {removed:.2f}s; {len(sig) / fs:.2f}s -> {len(out) / fs:.2f}s; "
      f"last word ends {new_words[-1]['end']:.2f}s (was {words[-1]['end']:.2f}s)")
