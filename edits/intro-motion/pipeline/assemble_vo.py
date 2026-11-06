"""Assemble cloned-voice lines into one narration: trim, pause, EQ-match to the real voice, loudness.
usage: assemble_vo.py lines_dir real_voice.mp4 out.wav"""
import sys, subprocess, json
import numpy as np
from scipy.signal import firwin2, fftconvolve, welch

d, real, out = sys.argv[1:4]
SR = 48000
# (file, pause after in s) — pauses follow the rhythm of the script and the text's punch moments
SEQ = [("line00.wav", 0.45), ("line01.wav", 0.55), ("line02.wav", 0.30), ("likes_0.wav", 0.50),
       ("line05.wav", 0.45), ("line06.wav", 0.25), ("line07.wav", 0.50), ("line08.wav", 0.50),
       ("line09.wav", 0.20), ("line10.wav", 0.0)]
LEAD = 0.40  # silence before the first word (matches the original first-word time)

def load(path, sr=SR):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()

def trim(x, thr_db=-45, pad=0.04):
    h = int(SR * 0.01); n = len(x) // h
    db = 20 * np.log10(np.sqrt((x[:n * h].reshape(n, h) ** 2).mean(1)) + 1e-9)
    on = np.where(db > db.max() + thr_db)[0]
    s = max(0, on[0] * h - int(pad * SR)); e = min(len(x), (on[-1] + 1) * h + int(pad * SR))
    y = x[s:e].copy(); f = int(0.01 * SR); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
    return y

parts, marks, t = [np.zeros(int(LEAD * SR), np.float32)], [], LEAD
for f, pause in SEQ:
    y = trim(load(f"{d}/{f}"))
    marks.append({"file": f, "start": round(t, 3), "dur": round(len(y) / SR, 3)})
    parts += [y, np.zeros(int(pause * SR), np.float32)]; t += len(y) / SR + pause
vo = np.concatenate(parts)

# EQ match: long-term spectrum of the clone -> long-term spectrum of the real recording (1/3-octave smooth, ±8 dB)
ref = load(real)
f1, p_ref = welch(ref[np.abs(ref) > 1e-3], SR, nperseg=8192)
_, p_vo = welch(vo[np.abs(vo) > 1e-3], SR, nperseg=8192)
gain_db = 10 * np.log10((p_ref + 1e-15) / (p_vo + 1e-15))
fc = np.geomspace(60, 16000, 40); g = []
for c in fc:
    m = (f1 > c / 2 ** (1 / 6)) & (f1 < c * 2 ** (1 / 6)); g.append(np.median(gain_db[m]) if m.any() else 0)
g = np.clip(np.array(g) - np.median(g), -8, 8)
g[fc < 150] = np.minimum(g[fc < 150], 0)  # never boost room rumble
freqs = np.concatenate([[0], fc, [SR / 2]]) / (SR / 2); gains = 10 ** (np.concatenate([[g[0]], g, [g[-1]]]) / 20)
fir = firwin2(4097, freqs, gains)
vo = fftconvolve(vo, fir, mode="same").astype(np.float32)
np.save(out.replace(".wav", "_eq.npy"), np.stack([fc, g]))

tmp = out.replace(".wav", "_pre.wav")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", tmp],
               input=vo.tobytes(), check=True)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-af",
                "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80,loudnorm=I=-14:TP=-1.5:LRA=11:linear=true,alimiter=limit=0.84:level=false",
                "-ar", str(SR), "-ac", "1", out], check=True)
json.dump({"marks": marks, "total": round(len(vo) / SR, 3)}, open(out.replace(".wav", ".json"), "w"), indent=1)
print("narration", round(len(vo) / SR, 2), "s;", "EQ dB:", " ".join(f"{int(c)}:{v:+.1f}" for c, v in zip(fc[::4], g[::4])))
