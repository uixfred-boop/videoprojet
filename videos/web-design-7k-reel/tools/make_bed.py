#!/usr/bin/env python3
"""Synthesize the music bed (assets/audio/bed.wav) — a quiet minor-key lo-fi pulse that follows the story.

Deterministic (seeded noise). Arrangement follows the scene table in tools/assemble.py:
  0–12.06    hook + doubt: pad, arp, light kick/hats
  12.06–14.68 "But for me?" cutaway: drums drop, pad swells
  14.68–32.2  struggle: full groove
  32.2–34.3   "nothing but silence": everything fades to true silence
  34.3–40.66  questioning / rebuilding: pad + sub only
  40.66–42.44 "it hit me": pad, then hard stop on the hit (SFX carries it)
  42.44–47.1  realisation: half-time kick, pad
  47.1–58.52  lesson + promise: full groove, brighter arp
  58.52–64    CTA: full groove, final ring-out
Run with a Python that has numpy + scipy:  python tools/make_bed.py
"""
import pathlib
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
DUR = 64.0
BPM = 90.0
BEAT = 60.0 / BPM
BAR = 4 * BEAT
N = int(SR * DUR)
t_all = np.arange(N) / SR
rng = np.random.default_rng(7)

# A minor: i – VI – III – VII  (Am – F – C – G), one chord per bar
CHORDS = [
    {"bass": 55.00, "pad": [220.00, 261.63, 329.63, 440.00], "arp": [440.00, 523.25, 659.25, 523.25]},
    {"bass": 43.65, "pad": [174.61, 220.00, 261.63, 349.23], "arp": [349.23, 440.00, 523.25, 440.00]},
    {"bass": 65.41, "pad": [196.00, 261.63, 329.63, 392.00], "arp": [392.00, 523.25, 659.25, 523.25]},
    {"bass": 49.00, "pad": [196.00, 246.94, 293.66, 392.00], "arp": [392.00, 493.88, 587.33, 493.88]},
]


def env_points(points):
    """Piecewise-linear gain curve over the whole bed from [(t, gain), ...]."""
    ts = np.array([p[0] for p in points])
    gs = np.array([p[1] for p in points])
    return np.interp(t_all, ts, gs)


def lowpass(x, hz, order=2):
    return sosfilt(butter(order, hz, "low", fs=SR, output="sos"), x)


def highpass(x, hz, order=2):
    return sosfilt(butter(order, hz, "high", fs=SR, output="sos"), x)


def adsr(n, a, d, s, r_len, total):
    """Envelope of length `total` samples: attack a, decay d to sustain s, release over the last r_len."""
    e = np.full(total, s, dtype=float)
    a_n, d_n, r_n = int(a * SR), int(d * SR), int(r_len * SR)
    a_n = max(1, min(a_n, total))
    e[:a_n] = np.linspace(0, 1, a_n)
    d_end = min(total, a_n + d_n)
    if d_end > a_n:
        e[a_n:d_end] = np.linspace(1, s, d_end - a_n)
    if r_n > 0 and r_n < total:
        e[-r_n:] *= np.linspace(1, 0, r_n)
    return e


def add(buf, start_s, sig):
    i = int(start_s * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i]


pad = np.zeros(N)
arp = np.zeros(N)
bass = np.zeros(N)
kick = np.zeros(N)
snare = np.zeros(N)
hats = np.zeros(N)

n_bars = int(np.ceil(DUR / BAR)) + 1
for b in range(n_bars):
    bt = b * BAR
    ch = CHORDS[b % 4]
    # pad: detuned saw-ish stack, slow attack, overlaps into next bar
    L = int((BAR + 0.9) * SR)
    tt = np.arange(L) / SR
    e = adsr(L, 0.6, 0.8, 0.8, 0.9, L)
    voice = np.zeros(L)
    for f in ch["pad"]:
        for det in (-0.6, 0.0, 0.7):
            ph = 2 * np.pi * (f + det) * tt
            voice += (np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.18 * np.sin(3 * ph)) / 3
    add(pad, bt, voice * e * 0.12)
    # sub bass: root on beats 1 and 3, soft
    for k in (0, 2):
        Lb = int(BEAT * 1.9 * SR)
        tb = np.arange(Lb) / SR
        eb = adsr(Lb, 0.02, 0.3, 0.6, 0.25, Lb)
        add(bass, bt + k * BEAT, np.sin(2 * np.pi * ch["bass"] * 2 * tb) * eb * 0.5)
    # arp: 8th-note plucks
    for k in range(8):
        f = ch["arp"][k % 4] * (2 if k in (3, 7) else 1)
        Lp = int(0.45 * SR)
        tp = np.arange(Lp) / SR
        ep = np.exp(-tp * 9.0)
        ep[: int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
        ph = 2 * np.pi * f * tp
        add(arp, bt + k * BEAT / 2, (np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.08 * np.sin(4 * ph)) * ep * 0.16)
    # drums
    for k in range(4):
        st = bt + k * BEAT
        if k in (0, 2):
            Lk = int(0.32 * SR)
            tk = np.arange(Lk) / SR
            f_sweep = 45 + 85 * np.exp(-tk * 30)
            phase = 2 * np.pi * np.cumsum(f_sweep) / SR
            add(kick, st, np.sin(phase) * np.exp(-tk * 11) * 0.9)
        if k in (1, 3):
            Ls = int(0.22 * SR)
            ts_ = np.arange(Ls) / SR
            nz = rng.standard_normal(Ls)
            body = np.sin(2 * np.pi * 185 * ts_) * np.exp(-ts_ * 25) * 0.4
            add(snare, st, (nz * np.exp(-ts_ * 18) * 0.5 + body) * 0.55)
    for k in range(8):
        Lh = int(0.06 * SR)
        th = np.arange(Lh) / SR
        nz = rng.standard_normal(Lh)
        add(hats, bt + k * BEAT / 2, nz * np.exp(-th * 70) * (0.35 if k % 2 else 0.22))

hats = highpass(hats, 7000)
snare = highpass(lowpass(snare, 6000), 180)
pad = lowpass(pad, 1700)
arp = lowpass(arp, 4200)
bass = lowpass(bass, 220)

# section automation (seconds, gain)
g_pad = env_points([(0, 0.0), (0.5, 0.75), (12.0, 0.75), (12.3, 1.0), (14.5, 1.0), (14.7, 0.8), (32.2, 0.8),
                    (33.0, 0.0), (34.3, 0.0), (35.0, 0.85), (41.75, 0.85), (41.8, 0.0), (42.3, 0.0), (42.9, 0.8),
                    (63.0, 0.8), (64.0, 0.0)])
g_arp = env_points([(0, 0.0), (0.4, 0.7), (12.0, 0.7), (12.2, 0.25), (14.6, 0.25), (14.8, 0.8), (32.0, 0.8),
                    (32.8, 0.0), (47.0, 0.0), (47.6, 1.0), (62.4, 1.0), (63.8, 0.0)])
g_bass = env_points([(0, 0.0), (0.3, 0.8), (12.0, 0.8), (12.2, 0.5), (32.0, 0.9), (32.9, 0.0), (34.3, 0.0),
                     (35.5, 0.6), (41.75, 0.6), (41.8, 0.0), (42.4, 0.0), (42.6, 0.8), (63.2, 0.8), (64.0, 0.0)])
g_kick = env_points([(0, 0.7), (12.0, 0.7), (12.06, 0.0), (14.6, 0.0), (14.68, 0.9), (32.1, 0.9), (32.3, 0.0),
                     (42.44, 0.0), (42.5, 0.55), (47.0, 0.55), (47.1, 0.95), (63.0, 0.95), (63.3, 0.0)])
g_snare = env_points([(0, 0.0), (14.6, 0.0), (14.68, 0.8), (32.1, 0.8), (32.3, 0.0), (47.0, 0.0), (47.1, 0.85),
                      (63.0, 0.85), (63.3, 0.0)])
g_hats = env_points([(0, 0.45), (12.0, 0.45), (12.06, 0.0), (14.6, 0.0), (14.68, 0.8), (32.1, 0.8), (32.3, 0.0),
                     (47.0, 0.0), (47.1, 0.9), (63.0, 0.9), (63.3, 0.0)])
# half-time feel in 42.44–47.1: keep only beat-1 kicks by gating beat 3
beat_idx = np.floor(t_all / BEAT).astype(int) % 4
halftime = (t_all >= 42.44) & (t_all < 47.1) & (beat_idx == 2)
g_kick[halftime] = 0.0

dry = (pad * g_pad + arp * g_arp + bass * g_bass + kick * g_kick + snare * g_snare + hats * g_hats)

# simple stereo: arp/hats slightly wide via short delays
def delay(x, ms):
    d = int(SR * ms / 1000)
    return np.concatenate([np.zeros(d), x[:-d]])

wide = arp * g_arp + hats * g_hats * 0.6
left = dry + 0.25 * delay(wide, 11)
right = dry + 0.25 * delay(wide, 17)

# room reverb (deterministic noise IR)
ir_len = int(1.6 * SR)
ir_t = np.arange(ir_len) / SR
ir = rng.standard_normal(ir_len) * np.exp(-ir_t * 3.2)
ir = lowpass(ir, 5000)
ir /= np.sqrt(np.sum(ir ** 2))
send = lowpass(pad * g_pad + arp * g_arp + snare * g_snare, 6000)
rev = fftconvolve(send, ir)[:N]
left += rev * 0.32
right += np.roll(rev, int(0.013 * SR)) * 0.32

# vinyl texture: sparse seeded crackle + faint hiss
crackle = np.zeros(N)
pos = rng.integers(0, N - 200, size=int(DUR * 9))
for p in pos:
    crackle[p : p + 40] += rng.standard_normal(40) * np.exp(-np.arange(40) / 6) * rng.uniform(0.05, 0.25)
hiss = highpass(rng.standard_normal(N), 3000) * 0.004
tex = highpass(crackle, 1500) * 0.35 + hiss
g_tex = env_points([(0, 1.0), (32.3, 1.0), (33.0, 0.0), (34.3, 0.0), (35.0, 1.0), (63.5, 1.0), (64.0, 0.0)])
left += tex * g_tex
right += tex * g_tex

stereo = np.stack([left, right], axis=1)
stereo = highpass(stereo.T, 30).T
peak = np.max(np.abs(stereo))
stereo = stereo / peak * 0.5  # leave headroom; the mix sets the final level

out = pathlib.Path(__file__).resolve().parent.parent / "assets/audio/bed.wav"
with wave.open(str(out), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((np.clip(stereo, -1, 1) * 32767).astype("<i2").tobytes())
print("wrote", out)
