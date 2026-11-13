"""Beat rap instrumental dynamique (95 BPM, fa mineur), entièrement synthétisé : aucun droit à gérer.

Usage : python3 beat_gen.py <dossier_sortie>   → beat.wav (≈ 41 s, 16 mesures)
"""
import sys, wave
import numpy as np

SR = 48000
BPM = 95
STEP = 60 / BPM / 4            # double croche
BAR = 16 * STEP
BARS = 16
N = int(SR * BAR * BARS) + SR
rng = np.random.default_rng(11)
out = sys.argv[1]

def midi(m): return 440 * 2 ** ((m - 69) / 12)

def fft_filter(x, lo=None, hi=None, order=2):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); H = np.ones_like(f)
    if hi: H *= 1 / np.sqrt(1 + (f / hi) ** (2 * order))
    if lo: H *= 1 - 1 / np.sqrt(1 + (f / lo) ** (2 * order))
    return np.fft.irfft(X * H, len(x))

def add(buf, x, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf): return
    L = min(len(x), len(buf) - i)
    buf[i:i + L] += x[:L] * gain

# ---------- sons ----------
def kick():
    t = np.arange(int(SR * 0.55)) / SR
    f = 46 + 120 * np.exp(-t * 38)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 5.5)
    click = fft_filter(rng.standard_normal(len(t)), lo=2000) * np.exp(-t * 400) * 0.35
    return np.tanh(2.2 * (body + click))

def snare():
    t = np.arange(int(SR * 0.35)) / SR
    tone = np.sin(2 * np.pi * 185 * t) * np.exp(-t * 22) * 0.55
    noise = fft_filter(rng.standard_normal(len(t)), lo=1200, hi=9000) * np.exp(-t * 16)
    clap = np.zeros(len(t))
    for d in (0.0, 0.011, 0.023):
        i = int(d * SR); n = fft_filter(rng.standard_normal(len(t)), lo=900, hi=6000)
        clap[i:] += n[: len(t) - i] * np.exp(-t[: len(t) - i] * 45)
    x = tone + 0.7 * noise + 0.5 * clap
    return np.tanh(1.6 * x)

def hat(open_=False):
    L = 0.32 if open_ else 0.06
    t = np.arange(int(SR * L)) / SR
    n = fft_filter(rng.standard_normal(len(t)), lo=7000, hi=16000)
    return n * np.exp(-t * (10 if open_ else 70))

def bass808(m, dur):
    t = np.arange(int(SR * dur)) / SR
    f = midi(m) * (1 + 0.12 * np.exp(-t * 60))
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.clip(t / 0.004, 0, 1) * np.exp(-t * 1.1) * np.clip((dur - t) / 0.03, 0, 1)
    return np.tanh(2.5 * np.sin(ph)) * env

def keys(notes, dur, bright=1.0):
    t = np.arange(int(SR * dur)) / SR
    x = np.zeros(len(t))
    for m in notes:
        f = midi(m)
        for h, a, d in ((1, 1.0, 3.5), (2, 0.45 * bright, 6), (3, 0.22 * bright, 9), (4, 0.12 * bright, 13)):
            x += a * np.sin(2 * np.pi * f * h * t + rng.uniform(0, 6.28)) * np.exp(-t * d)
    return x * np.clip(t / 0.003, 0, 1) / max(1, len(notes))

def pad(notes, dur):
    t = np.arange(int(SR * dur)) / SR
    x = np.zeros(len(t))
    for m in notes:
        for det in (-0.08, 0.08):
            f = midi(m) * 2 ** (det / 12)
            x += sum(np.sin(2 * np.pi * f * k * t) / k for k in (1, 2, 3, 4, 5))
    env = np.clip(t / 0.25, 0, 1) * np.clip((dur - t) / 0.3, 0, 1)
    return fft_filter(x * env, hi=1600) / len(notes)

# ---------- arrangement ----------
CHORDS = [[53, 56, 60], [49, 53, 56], [56, 60, 63], [51, 55, 58]]   # Fm  Db  Ab  Eb
ROOTS = [41, 37, 44, 39]
MOTIF = [77, 75, 72, 70, 72, 75, 72, 68]   # pentatonique de fa mineur, octave haute

drums = np.zeros(N); bass = np.zeros(N); mel = np.zeros(N); pads = np.zeros(N)
K, S = kick(), snare()
H, OH = hat(), hat(True)
kick_times = []
for b in range(BARS):
    t0 = b * BAR
    ci = b % 4
    k_steps = [0, 7, 10] if b % 2 == 0 else [0, 3, 8, 10, 14]
    for s in k_steps:
        add(drums, K, t0 + s * STEP, 0.8 if s in (0, 8) else 0.68); kick_times.append(t0 + s * STEP)
    for s in (4, 12):
        add(drums, S, t0 + s * STEP, 0.95)
    # charleston : doubles croches avec accents, roulement en triolets de triples croches toutes les 2 mesures
    for s in range(16):
        if b % 2 == 1 and s >= 14:
            continue
        vel = 0.5 if s % 4 == 0 else 0.36 if s % 2 == 0 else 0.24
        add(drums, H, t0 + s * STEP, vel * rng.uniform(0.85, 1.1))
    if b % 2 == 1:
        for r in range(6):
            add(drums, H, t0 + 14 * STEP + r * (2 * STEP / 6), 0.12 + 0.03 * r)
    if b % 4 == 3:
        add(drums, OH, t0 + 14 * STEP, 0.18)
    if b == 7:  # roulement de caisse claire avant la relance
        for r in range(8):
            add(drums, S, t0 + 12 * STEP + r * STEP / 2, 0.18 + 0.05 * r)
    # 808 sur les kicks, glissés vers la fondamentale de l'accord
    for j, s in enumerate(k_steps):
        nxt = k_steps[j + 1] if j + 1 < len(k_steps) else 16
        add(bass, bass808(ROOTS[ci], (nxt - s) * STEP), t0 + s * STEP, 0.9 if s == 0 else 0.7)
    # accords plaqués syncopés + motif mélodique (à partir de la mesure 3)
    for s in (0, 6, 10):
        add(mel, keys([m + 12 for m in CHORDS[ci]], 0.6, 0.9), t0 + s * STEP, 0.55 if s == 0 else 0.4)
    if b >= 2:
        for k_, m in enumerate(MOTIF):
            if (b + k_) % 3 == 0:
                continue
            add(mel, keys([m], 0.45, 1.2), t0 + (k_ * 2 + 1) * STEP, 0.35)
    add(pads, pad(CHORDS[ci], BAR + 0.2), t0, 1.0)

# compression latérale (la nappe se tasse sur chaque kick)
t = np.arange(N) / SR
duck = np.ones(N)
for kt in kick_times:
    i = int(kt * SR); L = int(SR * 0.28)
    seg = 1 - 0.65 * np.exp(-np.arange(min(L, N - i)) / SR * 14)
    duck[i:i + len(seg)] = np.minimum(duck[i:i + len(seg)], seg)
pads *= duck

def norm(x): return x / (np.max(np.abs(x)) + 1e-9)
mix = 1.0 * norm(drums) + 0.42 * norm(bass) * duck ** 0.3 + 0.62 * norm(mel) + 0.3 * norm(pads)
mix = fft_filter(mix, lo=28)
mix = np.tanh(1.3 * mix) / np.tanh(1.3)
# léger élargissement stéréo : mélodie et nappe décalées de quelques ms
side = np.roll(0.62 * norm(mel) + 0.3 * norm(pads), int(SR * 0.012))
L_ = mix + 0.15 * side; R_ = mix - 0.15 * side
st = np.stack([L_, R_], 1)
st = st / np.max(np.abs(st)) * 0.93
end = int(SR * BAR * BARS)
st = st[:end]
st[-int(SR * 0.05):] *= np.linspace(1, 0, int(SR * 0.05))[:, None]
with wave.open(f"{out}/beat.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
print(f"beat.wav : {end / SR:.1f} s, {BPM} BPM")
