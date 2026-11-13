"""Musique de fond ambient et bruitages discrets, synthétisés (aucun droit à gérer).

Usage : python3 audio_gen.py <dossier_sortie>
"""
import sys, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(7)
out = sys.argv[1]

def write(name, x):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1: x = np.stack([x, x], 1)
    peak = np.max(np.abs(x)) + 1e-9
    x = x / peak * 0.89
    with wave.open(f"{out}/{name}", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())

def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x):
        s = (1 - a) * v + a * s; y[i] = s
    return y

def lp_fast(x, fc, order=2):
    # filtre passe-bas par FFT (rapide pour de longs signaux)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    H = 1 / np.sqrt(1 + (f / fc) ** (2 * order))
    return np.fft.irfft(X * H, len(x))

def bp_fast(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    H = 1 / np.sqrt(1 + (f / hi) ** 4) * (1 - 1 / np.sqrt(1 + (f / lo) ** 4))
    return np.fft.irfft(X * H, len(x))

def reverb(x, t60=3.2, mix=0.45):
    n = int(SR * t60)
    t = np.arange(n) / SR
    irL = rng.standard_normal(n) * np.exp(-6.9 * t / t60)
    irR = rng.standard_normal(n) * np.exp(-6.9 * t / t60)
    irL = lp_fast(irL, 5000); irR = lp_fast(irR, 5000)
    N = len(x) + n
    def conv(sig, ir):
        return np.fft.irfft(np.fft.rfft(sig, N) * np.fft.rfft(ir, N), N)[:len(x)]
    wetL, wetR = conv(x, irL), conv(x, irR)
    wetL /= np.max(np.abs(wetL)) + 1e-9; wetR /= np.max(np.abs(wetR)) + 1e-9
    d = x / (np.max(np.abs(x)) + 1e-9)
    return np.stack([(1 - mix) * d + mix * wetL, (1 - mix) * d + mix * wetR], 1)

midi = lambda m: 440 * 2 ** ((m - 69) / 12)

# ---------- musique ----------
DUR = 46.0
BPM = 72; beat = 60 / BPM; bar = 4 * beat
n = int(SR * DUR); t = np.arange(n) / SR
# Dmaj9 – Bm7(add11) – Gmaj7(#11) – A6sus : posé, lumineux, un peu mélancolique
chords = [[50, 57, 61, 64, 66], [47, 54, 57, 62, 64], [43, 50, 54, 59, 61], [45, 52, 57, 59, 62]]
chord_len = 2 * bar
pad = np.zeros(n)
for ci in range(int(DUR / chord_len) + 1):
    notes = chords[ci % 4]
    t0 = ci * chord_len
    seg = (t >= t0 - 1.5) & (t < t0 + chord_len + 2.0)
    tt = t[seg] - t0
    env = np.clip((tt + 1.5) / 2.0, 0, 1) * np.clip((chord_len + 2.0 - tt) / 2.0, 0, 1)
    env = env ** 1.5
    s = np.zeros(seg.sum())
    for m in notes:
        for det in (-0.06, 0.0, 0.07):
            f = midi(m + 12) * 2 ** (det / 12)
            ph = rng.uniform(0, 2 * np.pi)
            s += (np.sin(2 * np.pi * f * tt + ph) + 0.35 * np.sin(4 * np.pi * f * tt + ph) + 0.12 * np.sin(6 * np.pi * f * tt)) / 3
    pad[seg] += s * env
pad = lp_fast(pad, 1400)
# basse douce
sub = np.zeros(n)
for ci in range(int(DUR / chord_len) + 1):
    root = chords[ci % 4][0] - 12
    seg = (t >= ci * chord_len) & (t < (ci + 1) * chord_len)
    tt = t[seg] - ci * chord_len
    sub[seg] = np.sin(2 * np.pi * midi(root) * tt) * np.clip(tt / 0.8, 0, 1) * np.clip((chord_len - tt) / 0.6, 0, 1)
# notes de piano feutré, croches lentes
bell = np.zeros(n)
for k in range(int(DUR / (beat / 2))):
    st = k * beat / 2
    ci = int(st / chord_len) % 4
    if rng.random() < 0.45: continue
    m = chords[ci][rng.integers(1, 5)] + 24
    i0 = int(st * SR); L = int(SR * 1.6)
    tt = np.arange(min(L, n - i0)) / SR
    env = np.exp(-tt * 2.8) * np.clip(tt / 0.008, 0, 1)
    f = midi(m)
    bell[i0:i0 + len(tt)] += (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2.01 * f * tt) * np.exp(-tt * 6)) * env * rng.uniform(0.5, 1)
bell = lp_fast(bell, 3200)
air = lp_fast(rng.standard_normal(n), 900) * 0.04
mix = pad / np.max(np.abs(pad)) * 0.55 + sub / np.max(np.abs(sub)) * 0.22 + bell / np.max(np.abs(bell)) * 0.18 + air
music = reverb(mix, t60=3.5, mix=0.5)
fade = np.clip(t / 1.2, 0, 1)[:, None]
write("music.wav", music * fade)

# ---------- bruitages ----------
def env_ar(L, a, r):
    tt = np.arange(L) / SR
    return np.clip(tt / a, 0, 1) * np.exp(-np.clip(tt - a, 0, None) / r)

# souffle doux : bruit filtré dont la bande monte puis redescend
L = int(SR * 0.7); noise = rng.standard_normal(L)
seg = np.zeros(L); hop = 1024
for i in range(0, L - hop, hop):
    p = i / L
    lo = 250 + 1500 * np.sin(np.pi * p); hi = lo * 2.2
    blk = bp_fast(noise[i:i + 4 * hop] if i + 4 * hop < L else noise[i:], lo, hi)[:hop]
    seg[i:i + hop] = blk
tt = np.arange(L) / L
whoosh = seg * np.sin(np.pi * tt) ** 1.6
pan = np.stack([whoosh * (1 - 0.4 * tt), whoosh * (0.6 + 0.4 * tt)], 1)
write("whoosh.wav", reverb(pan[:, 0] + pan[:, 1], t60=1.2, mix=0.3))

# micro-clic
L = int(SR * 0.08); tt = np.arange(L) / SR
click = (np.sin(2 * np.pi * 2100 * tt) * 0.6 + bp_fast(rng.standard_normal(L), 1500, 6000) * 0.5) * np.exp(-tt / 0.012)
write("click.wav", click)

# pop doux (photos qui s'empilent)
L = int(SR * 0.15); tt = np.arange(L) / SR
pop = np.sin(2 * np.pi * (520 - 900 * tt) * tt) * np.exp(-tt / 0.035)
write("pop.wav", pop)

# montée légère vers le CTA
L = int(SR * 1.6); tt = np.arange(L) / SR
rise = bp_fast(rng.standard_normal(L), 400, 5000) * (tt / tt[-1]) ** 2.2
tone = np.sin(2 * np.pi * midi(74) * tt) * (tt / tt[-1]) ** 3 * 0.3
write("riser.wav", reverb(rise + tone, t60=1.5, mix=0.35))
print("ok")
