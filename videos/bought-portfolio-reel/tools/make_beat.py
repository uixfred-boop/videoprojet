#!/usr/bin/env python3
"""Synthesize the instrumental beat (assets/audio/beat.wav): a dark trap groove in C minor, ~140 BPM half-time.

Deterministic (seeded noise), no samples. Its drops, stops and builds are pinned to the story, so the grid bends
slightly (139-142 BPM) between these anchor downbeats:
     5.80  drop 1 on "I cheated" (the hook before it runs the same groove muffled)
    50.54  drums back on "said yes" (after the stop on "nothing")
    79.02  breakdown on "so yes, I was a freelancer, just not a good one"
    88.78  second half ("so I wanted to get out of this situation"): new chords, half-time
    97.23  drop 2 on "so I locked in"
   113.12  final hit after "what worked for me"
and it cuts to silence for "nothing" (46.24-47.10) and "subscribe" (110.09-110.94).

Run with a Python that has numpy + scipy:  python tools/make_beat.py
"""
import pathlib
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt, sosfilt_zi

SR = 48000
DUR = 114.2
N = int(round(SR * DUR))
rng = np.random.default_rng(1008)
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets/audio/beat.wav"


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def lowpass(x, hz, order=2):
    return sosfilt(butter(order, hz, "low", fs=SR, output="sos"), x)


def highpass(x, hz, order=2):
    return sosfilt(butter(order, hz, "high", fs=SR, output="sos"), x)


def bandpass(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def place(buf, t, sig, gain=1.0):
    """Mix a mono signal into buf at time t (s); clips at both ends."""
    i = int(round(t * SR))
    if i < 0:
        sig = sig[-i:]
        i = 0
    if i >= len(buf) or len(sig) == 0:
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * gain


def fade_edges(x, a=0.002, r=0.004):
    a_n, r_n = max(1, int(a * SR)), max(1, int(r * SR))
    x[:a_n] *= np.linspace(0, 1, a_n)
    x[-r_n:] *= np.linspace(1, 0, r_n)
    return x


def sweep_filter(x, t0, t1, f0, f1, kind="low", order=2):
    """Time-varying Butterworth filter over [t0, t1] (cutoff moves exponentially f0 -> f1), dry elsewhere.
    Block-wise with the filter state carried across blocks; 10 ms crossfades back to dry at both ends."""
    i0, i1 = max(0, int(t0 * SR)), min(len(x), int(t1 * SR))
    seg = x[i0:i1]
    out = np.empty_like(seg)
    blk = 256
    nb = int(np.ceil(len(seg) / blk))
    zi = None
    for b in range(nb):
        frac = b / max(1, nb - 1)
        fc = f0 * (f1 / f0) ** frac
        sos = butter(order, min(fc, SR * 0.45), kind, fs=SR, output="sos")
        if zi is None:
            zi = sosfilt_zi(sos) * seg[0]
        y, zi = sosfilt(sos, seg[b * blk:(b + 1) * blk], zi=zi)
        out[b * blk:(b + 1) * blk] = y
    xf = int(0.01 * SR)
    w = np.ones(len(seg))
    w[:xf] = np.linspace(0, 1, xf)
    w[-xf:] = np.minimum(w[-xf:], np.linspace(1, 0, xf))
    res = x.copy()
    res[i0:i1] = seg * (1 - w) + out * w
    return res


# --------------------------------------------------------------------------------------------- grid
def build_bars():
    """Bars as dicts: t (start), beat (s), n (beats in the bar), k (global bar index; 0 = drop 1)."""
    segs = [(5.80, 50.54, [4] * 26), (50.54, 79.02, [4] * 16 + [2]), (79.02, 88.78, [4] * 5 + [3]),
            (88.78, 97.23, [4] * 5), (97.23, 113.12, [4] * 8 + [5])]
    bars = []
    b0 = (segs[0][1] - segs[0][0]) / sum(segs[0][2])
    for j in range(4, 0, -1):  # pre-roll for the hook, same tempo as segment 1
        bars.append(dict(t=5.80 - 4 * b0 * j, beat=b0, n=4, k=-j))
    k = 0
    for a, b, sizes in segs:
        beat = (b - a) / sum(sizes)
        t = a
        for n in sizes:
            bars.append(dict(t=t, beat=beat, n=n, k=k))
            t += n * beat
            k += 1
    return bars


BARS = build_bars()
BY_K = {b["k"]: b for b in BARS}


def at_k(k, beats=0.0):
    """Time of bar k's downbeat plus a number of beats."""
    b = BY_K[k]
    return b["t"] + beats * b["beat"]


def step_t(bar, s):
    return bar["t"] + s * bar["beat"] / 4


# section per global bar index
def section(k):
    if k < 0:
        return "intro"
    if k <= 11:
        return "grooveA"
    if k <= 19:
        return "grooveB"
    if k <= 21:
        return "tensionA"
    if k <= 23:
        return "tensionB"
    if k <= 25:
        return "reentry"
    if k <= 33:
        return "grooveA"
    if k <= 41:
        return "grooveB"
    if k == 42:
        return "fill"
    if k <= 45:
        return "breakdown"
    if k <= 48:
        return "build"
    if k <= 52:
        return "part2"
    if k == 53:
        return "build2"
    if k <= 61:
        return "drop2"
    return "outro"


PROG_A = ["Cm", "Ab", "Fm", "G"]
SPECIAL = {43: "Ab", 44: "Fm", 45: "Cm", 46: "Ab", 47: "Bb", 48: "Cm",
           49: "Ab", 50: "Bb", 51: "Cm", 52: "Cm", 53: "G", 62: "Bb"}
PROG_D2 = ["Ab", "Bb", "Eb", "Cm"]


def chord_of(k):
    if k in SPECIAL:
        return SPECIAL[k]
    if 54 <= k <= 61:
        return PROG_D2[(k - 54) % 4]
    if k <= 25:
        return PROG_A[k % 4]
    return PROG_A[(k - 26) % 4]


CHORDS = {  # 808 root (MIDI) and pad voicing
    "Cm": dict(root=36, pad=[55, 60, 63, 67]),
    "Ab": dict(root=32, pad=[56, 60, 63, 68]),
    "Fm": dict(root=29, pad=[56, 60, 65, 68]),
    "G": dict(root=31, pad=[55, 59, 62, 67]),
    "Bb": dict(root=34, pad=[58, 62, 65, 70]),
    "Eb": dict(root=39, pad=[58, 63, 67, 70]),
}
RHY = [0, 3, 6, 8, 10, 13]  # 3-3-2-2-3-3 syncopation
BELL_A = {"Cm": [79, 75, 72, 74, 75, 79], "Ab": [80, 75, 72, 70, 72, 75],
          "Fm": [77, 75, 72, 68, 72, 77], "G": [71, 74, 79, 77, 75, 74]}
BELL_B = {"Ab": [75, 80, 84, 82, 80, 75], "Bb": [74, 77, 82, 80, 77, 74],
          "Eb": [75, 79, 82, 84, 82, 79], "Cm": [72, 75, 79, 82, 79, 75], "G": [71, 74, 79, 77, 75, 74]}
BELL_LONG = {"Ab": [72, 75], "Bb": [74, 77], "Cm": [75, 79], "G": [74, 71], "Fm": [72, 77], "Eb": [75, 79]}

KICK_A = [[0, 10], [0, 7, 10]]
KICK_B = [[0, 6, 10], [0, 3, 10, 13]]
QUARTERS = [0, 4, 8, 12, 16]
HAT8_V = [1.0, 0.55, 0.8, 0.55, 0.95, 0.55, 0.8, 0.6]
HAT16_V = [1, .35, .6, .35, .9, .35, .6, .4, 1, .35, .6, .35, .9, .35, .6, .45]

FINAL = 113.12
GAPS = [
    (at_k(0, -0.5), at_k(0)),      # an eighth of silence before drop 1 ("I cheated")
    (at_k(23, 2), at_k(24)),       # the stop under "but after that… nothing"
    (at_k(48, 2.5), at_k(49)),     # an eighth before the second half
    (at_k(61, 2), at_k(62)),       # "subscribe" in the clear
]


# --------------------------------------------------------------------------------------------- voices
def make_kick():
    L = int(0.5 * SR)
    t = np.arange(L) / SR
    f = 47 + 150 * np.exp(-t * 40) + 18 * np.exp(-t * 7)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.0)
    body = np.tanh(2.2 * body) / np.tanh(2.2)
    click = highpass(rng.standard_normal(L) * np.exp(-t * 450), 2500) * 0.22
    return fade_edges(body + click, 0.0008, 0.02)


def make_clap():
    L = int(0.55 * SR)
    t = np.arange(L) / SR
    env = np.zeros(L)
    for d, g in ((0.0, 0.7), (0.009, 0.8), (0.019, 0.9), (0.028, 1.0)):
        i = int(d * SR)
        env[i:] += np.exp(-(t[i:] - d) * 230) * g
    env += np.where(t > 0.028, np.exp(-(t - 0.028) * 15) * 0.38, 0)
    x = bandpass(rng.standard_normal(L) * env, 850, 7500)
    body = np.sin(2 * np.pi * 205 * t) * np.exp(-t * 38) * 0.22
    return fade_edges(x + body, 0.0005, 0.03)


def make_snare():
    L = int(0.22 * SR)
    t = np.arange(L) / SR
    x = bandpass(rng.standard_normal(L) * np.exp(-t * 30), 1100, 9000)
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 42) * 0.5
    return fade_edges(x + body, 0.0005, 0.02)


def make_metal(L_s, decay):
    L = int(L_s * SR)
    t = np.arange(L) / SR
    x = np.zeros(L)
    for f, ph in zip((205.3, 304.4, 369.6, 522.7, 540.0, 800.0), (0.1, 0.7, 1.3, 2.1, 2.9, 4.0)):
        x += np.sign(np.sin(2 * np.pi * f * 1.7 * t + ph))
    x = highpass(x / 6, 7200, 4) * 0.9 + highpass(rng.standard_normal(L), 9000, 2) * 0.35
    return fade_edges(x * np.exp(-t * decay), 0.0005, 0.01)


def make_crash(L_s=3.2):
    L = int(L_s * SR)
    t = np.arange(L) / SR
    env = np.exp(-t * 1.5)
    chans = []
    for _ in range(2):
        nz = highpass(rng.standard_normal(L), 3800, 2) + 0.5 * make_metal(L_s, 0.0)[:L] * 0.6
        chans.append(lowpass(nz, 13000) * env)
    return [fade_edges(c, 0.001, 0.2) for c in chans]


def make_impact():
    L = int(1.6 * SR)
    t = np.arange(L) / SR
    f = 36 + 80 * np.exp(-t * 9)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.6)
    x = np.tanh(1.8 * x) / np.tanh(1.8)
    thump = lowpass(rng.standard_normal(L) * np.exp(-t * 18), 400) * 0.6
    return fade_edges(x + thump, 0.001, 0.3)


def make_riser(dur, f0=350, f1=9000):
    L = int(dur * SR)
    t = np.arange(L) / SR
    nz = rng.standard_normal(L)
    out = np.zeros(L)
    blk = 512
    zi = None
    for b in range(0, L, blk):
        fc = f0 * (f1 / f0) ** (b / L)
        sos = butter(2, [fc / 1.5, min(fc * 1.5, SR * 0.45)], "band", fs=SR, output="sos")
        if zi is None:
            zi = sosfilt_zi(sos) * 0
        y, zi = sosfilt(sos, nz[b:b + blk], zi=zi)
        out[b:b + blk] = y
    tone = np.sin(2 * np.pi * np.cumsum(220 * 4 ** (t / dur)) / SR) * 0.12
    amp = (t / dur) ** 2.2
    return fade_edges((out + tone) * amp, 0.05, 0.004)


def make_downlifter(dur=1.8):
    r = make_riser(dur, 300, 7000)[::-1].copy()
    return fade_edges(r, 0.004, 0.2)


# wavetable saw (band-limited to 24 harmonics) for pads
_TAB_N = 4096
_ph = np.arange(_TAB_N) / _TAB_N
SAW_TAB = sum(np.sin(2 * np.pi * h * _ph) / h for h in range(1, 25)) * (2 / np.pi)


def saw(freq, L, phase0=0.0):
    ph = (phase0 + freq * np.arange(L) / SR) % 1.0
    return SAW_TAB[(ph * _TAB_N).astype(int)]


def bell_note(m, dur=1.3, bright=1.0):
    L = int(dur * SR)
    t = np.arange(L) / SR
    f = midi(m)
    idx = (2.6 * np.exp(-t * 7) + 0.25) * bright
    x = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * 3.5 * t))
    x += 0.55 * np.sin(2 * np.pi * f * t) + 0.12 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 6)
    env = np.exp(-t * 3.4)
    return fade_edges(x * env, 0.002, 0.05)


def pluck_note(m, dur=0.32):
    L = int(dur * SR)
    t = np.arange(L) / SR
    f = midi(m)
    x = sum(np.sin(2 * np.pi * f * h * t) / h * np.exp(-t * (7 + 5 * h)) for h in range(1, 9))
    return fade_edges(x, 0.002, 0.03)


def pad_chord(notes, L, detune=(-0.09, 0.0, 0.08)):
    """Returns (left, right) of a detuned saw chord, unenveloped."""
    left = np.zeros(L)
    right = np.zeros(L)
    for i, m in enumerate(notes):
        for j, d in enumerate(detune):
            v = saw(midi(m + d), L, phase0=(i * 0.37 + j * 0.21) % 1)
            if j == 0:
                left += v
            elif j == 2:
                right += v
            else:
                left += 0.6 * v
                right += 0.6 * v
    return left, right


# --------------------------------------------------------------------------------------------- score
kick = np.zeros(N)
bass = np.zeros(N)
clap = np.zeros(N)
snare = np.zeros(N)
hat = np.zeros(N)
ohat = np.zeros(N)
bell = np.zeros(N)
pluck = np.zeros(N)
padL = np.zeros(N)
padR = np.zeros(N)
cymL = np.zeros(N)  # crashes + reverse crashes
cymR = np.zeros(N)
rise = np.zeros(N)  # risers
boom = np.zeros(N)  # impacts + downlifter
keep = np.zeros(N)  # cymbal audible inside a stop (reverse crash into the beat's return)
kick_times = []

KICK = make_kick()
CLAP = make_clap()
SNARE = make_snare()
HAT = make_metal(0.09, 75)
OHAT = make_metal(0.5, 8.5)
CRASH = make_crash()
IMPACT = make_impact()

bass_notes = []  # (t_on, midi, glide_from, velocity)


def add_kick(t, v=1.0, with_bass=None, glide=None):
    if t < 0:
        return
    place(kick, t, KICK, v)
    kick_times.append(t)
    if with_bass is not None:
        bass_notes.append((t, with_bass, glide, 1.0))


def hats8(bar, v=1.0, upto=16):
    for i, s in enumerate(range(0, min(16, upto), 2)):
        place(hat, step_t(bar, s) + rng.normal(0, 0.002), HAT, v * HAT8_V[i] * rng.uniform(0.92, 1.05))


def hats16(bar, v=1.0, roll=None, upto=16):
    for s in range(min(16, upto)):
        if roll and s >= 12:
            continue
        place(hat, step_t(bar, s) + rng.normal(0, 0.0015), HAT, v * HAT16_V[s] * rng.uniform(0.92, 1.05))
    if roll:
        hat_roll(bar, roll, v)


def hat_roll(bar, kind="trip", v=1.0):
    sub = 8 if kind == "32" else 6
    q = bar["beat"] / sub
    t0 = step_t(bar, 12)
    for i in range(sub):
        place(hat, t0 + i * q, HAT, v * (0.45 + 0.5 * i / sub))


def snare_roll(t0, t1, sub_per_beat, beat, v0, v1):
    q = beat / sub_per_beat
    n = int(round((t1 - t0) / q))
    for i in range(n):
        place(snare, t0 + i * q, SNARE, v0 + (v1 - v0) * i / max(1, n - 1))


def bells(bar, melody, v=1.0, octave=0, bright=1.0):
    for s, m in zip(RHY, melody):
        if s < bar["n"] * 4:
            place(bell, step_t(bar, s), bell_note(m + octave, bright=bright), v * (1.0 if s in (0, 8) else 0.82))


def arp(bar, notes, v=1.0):
    seq = [0, 1, 2, 3, 2, 1, 2, 3]
    for s in range(0, min(16, bar["n"] * 4)):
        m = notes[seq[s % 8]] + 12
        place(pluck, step_t(bar, s), pluck_note(m), v * (1.0 if s % 2 == 0 else 0.6))


def pad(bar, ch, v=1.0, attack=0.25, length=None):
    L = int(((length or bar["n"] * bar["beat"]) + 0.6) * SR)
    l, r = pad_chord(CHORDS[ch]["pad"], L)
    t = np.arange(L) / SR
    env = np.minimum(1, t / attack) * np.where(t > L / SR - 0.6, np.clip((L / SR - t) / 0.6, 0, 1), 1)
    place(padL, bar["t"], l * env, v)
    place(padR, bar["t"], r * env, v)


def crash(t, v=1.0):
    place(cymL, t, CRASH[0], v)
    place(cymR, t, CRASH[1], v)


def reverse_crash(t_end, dur, v=1.0, through_stop=False):
    L = int(dur * SR)
    for buf, c in ((cymL, CRASH[0]), (cymR, CRASH[1])):
        r = c[:L][::-1].copy()
        r = fade_edges(r, 0.02, 0.003)
        place(buf, t_end - dur, r, v)
    if through_stop:
        place(keep, t_end - dur, np.ones(L))


for bar in BARS:
    k, sec, ch = bar["k"], section(bar["k"]), chord_of(bar["k"])
    root = CHORDS[ch]["root"]
    steps = bar["n"] * 4
    phrase_end = (k % 4 == 3)

    if sec in ("intro", "grooveA", "grooveB", "drop2"):
        busy = sec in ("grooveB", "drop2")
        pat = (KICK_B if busy else KICK_A)[k % 2]
        for s in pat:
            add_kick(step_t(bar, s), 1.0, root)
        if busy and phrase_end:  # classic 808 slide up the octave at the end of the phrase
            bass_notes.append((step_t(bar, 14), root + 12, root, 0.9))
        place(clap, step_t(bar, 8), CLAP, 1.0)
        if phrase_end:
            place(clap, step_t(bar, 15), CLAP, 0.35)
        if busy:
            hats16(bar, 1.0, roll=("32" if k % 4 == 3 else "trip") if k % 2 else None)
            if k % 2 == 0:
                place(ohat, step_t(bar, 14), OHAT, 0.8)
        elif sec != "intro":
            hats8(bar, 1.0, upto=12 if phrase_end else 16)
            if phrase_end:
                hat_roll(bar, "trip", 0.85)
        if sec == "drop2":
            bells(bar, BELL_B[ch], 1.0)
            arp(bar, CHORDS[ch]["pad"], 0.8)
        else:
            happy = 32 <= k <= 33  # "of course I was happy in the moment": lift the bell an octave
            bells(bar, BELL_A[ch], 0.9 if not happy else 0.75, octave=12 if happy else 0)
            if busy:
                arp(bar, CHORDS[ch]["pad"], 0.7)
        pad(bar, ch, 0.8 if busy else 0.7)
        if sec == "drop2" and k == 61:  # the "subscribe" stop: snare pickup into the gap
            snare_roll(step_t(bar, 4), step_t(bar, 8), 4, bar["beat"], 0.3, 0.6)

    elif sec == "tensionA":
        place(clap, step_t(bar, 8), CLAP, 0.9)
        hats8(bar, 1.0)
        bells(bar, BELL_A[ch], 0.85)
        pad(bar, ch, 0.8)
        bass_notes.append((bar["t"], root, None, 0.6))

    elif sec == "tensionB":
        cut = 8 if k == 23 else 16  # stop on beat 3 of bar 23 (46.24), just before "nothing"
        for s in QUARTERS:
            if s < cut:
                add_kick(step_t(bar, s), 0.85, root if s == 0 else None)
        hats16(bar, 0.9, upto=cut)
        if k == 22:
            snare_roll(bar["t"], step_t(bar, 16), 2, bar["beat"], 0.25, 0.55)
        else:
            snare_roll(bar["t"], step_t(bar, 4), 4, bar["beat"], 0.55, 0.8)
            snare_roll(step_t(bar, 4), step_t(bar, 8), 8, bar["beat"], 0.8, 1.0)
        bells(bar, BELL_A[ch], 0.75)
        pad(bar, ch, 0.85, length=(cut / 4) * bar["beat"])

    elif sec == "reentry":
        bells(bar, BELL_A[ch], 0.9)
        pad(bar, ch, 0.9, attack=0.6)
        if k == 25:
            hats8(bar, 0.55)
            reverse_crash(bar["t"] + 4 * bar["beat"], bar["beat"] * 2, 0.9)

    elif sec == "fill":  # 2-beat bar before the breakdown
        add_kick(bar["t"], 1.0, root)
        snare_roll(bar["t"], step_t(bar, 8), 4, bar["beat"], 0.45, 0.9)
        hats8(bar, 0.8, upto=8)
        pad(bar, ch, 0.7)

    elif sec == "breakdown":
        bass_notes.append((bar["t"], root, None, 0.9))
        pad(bar, ch, 1.0, attack=0.35)
        place(bell, bar["t"], bell_note(BELL_LONG[ch][0], dur=2.2, bright=0.7), 0.8)
        place(bell, step_t(bar, 8), bell_note(BELL_LONG[ch][1], dur=2.0, bright=0.7), 0.6)
        if k == 45:  # "and that's when I understood something": hats creep back in from beat 2
            for s in range(4, 16, 2):
                place(hat, step_t(bar, s), HAT, 0.55)

    elif sec == "build":
        upto = bar["n"] * 4
        cut = 10 if k == 48 else upto  # short gap before the second half
        for s in QUARTERS:
            if s < cut:
                add_kick(step_t(bar, s), 0.85, root if s == 0 else None)
        if k == 46:
            hats8(bar, 0.8)
            snare_roll(bar["t"], step_t(bar, 16), 2, bar["beat"], 0.25, 0.5)
        elif k == 47:
            hats16(bar, 0.85)
            snare_roll(bar["t"], step_t(bar, 16), 4, bar["beat"], 0.5, 0.75)
        else:
            hats16(bar, 0.9, upto=cut)
            snare_roll(bar["t"], step_t(bar, cut), 8, bar["beat"], 0.75, 1.0)
        bells(bar, BELL_A.get(ch, BELL_B[ch]), 0.7)
        pad(bar, ch, 0.9, length=(cut / 4) * bar["beat"])

    elif sec == "part2":
        add_kick(bar["t"], 1.0, root)
        if k % 2:
            add_kick(step_t(bar, 10), 0.9, root)
        place(clap, step_t(bar, 8), CLAP, 0.95)
        hats8(bar, 0.75)
        if k % 2:
            place(ohat, step_t(bar, 14), OHAT, 0.7)
        for s, m in zip((0, 8), BELL_LONG[ch]):
            place(bell, step_t(bar, s), bell_note(m + 12, dur=1.6, bright=0.8), 0.75)
        arp(bar, CHORDS[ch]["pad"], 0.45)
        pad(bar, ch, 0.95, attack=0.3)

    elif sec == "build2":
        for s in QUARTERS[:4]:
            add_kick(step_t(bar, s), 0.85, root if s == 0 else None)
        hats16(bar, 0.9)
        snare_roll(bar["t"], step_t(bar, 8), 4, bar["beat"], 0.4, 0.7)
        snare_roll(step_t(bar, 8), step_t(bar, 16), 8, bar["beat"], 0.7, 1.0)
        bells(bar, BELL_B[ch], 0.7)
        pad(bar, ch, 0.9)
        reverse_crash(bar["t"] + 4 * bar["beat"], 2 * bar["beat"], 1.0)

    elif sec == "outro":  # 5-beat bar, then the final hit
        for s in (0, 6, 10, 16):
            add_kick(step_t(bar, s), 1.0, root)
        place(clap, step_t(bar, 8), CLAP, 1.0)
        hats16(bar, 1.0)
        snare_roll(step_t(bar, 16), step_t(bar, 20), 4, bar["beat"], 0.5, 1.0)
        bells(bar, BELL_B[ch], 1.0)
        arp(bar, CHORDS[ch]["pad"], 0.8)
        pad(bar, ch, 0.8)

# section accents (times from the grid)
for k in (0, 12, 26, 34, 49, 54):  # drop 1, groove B, "yes", "proof there was demand", second half, drop 2
    crash(at_k(k), 0.9)
for k, v in ((49, 0.55), (54, 0.7)):
    place(boom, at_k(k), IMPACT, v)
place(boom, at_k(43), make_downlifter(), 0.5)
reverse_crash(GAPS[0][0], 1.0, 0.8)
reverse_crash(at_k(62), at_k(62) - at_k(61, 3), 0.7, through_stop=True)
for t0, t1, v in ((at_k(-2), GAPS[0][0], 0.8), (at_k(20), GAPS[1][0], 0.9), (at_k(25), at_k(26), 0.6),
                  (at_k(46), GAPS[2][0], 0.9), (at_k(53), at_k(54), 0.8)):
    place(rise, t0, make_riser(t1 - t0), v)

# final hit after "what worked for me"
add_kick(FINAL, 1.0, 36)
crash(FINAL, 1.0)
place(boom, FINAL, IMPACT, 0.75)
fin = dict(t=FINAL, beat=0.43, n=4, k=99)
pad(fin, "Cm", 1.0, attack=0.01, length=0.6)
for m, v in ((72, 1.0), (79, 0.7), (84, 0.5)):
    place(bell, FINAL, bell_note(m, dur=1.1), v)

# ------------------------------------------------------------------------------------------- 808 render
bass_notes.sort(key=lambda x: x[0])
for i, (t_on, m, gl, vel) in enumerate(bass_notes):
    t_next = bass_notes[i + 1][0] if i + 1 < len(bass_notes) else t_on + 1.1
    dur = min(1.6, max(0.12, t_next - t_on))
    L = int((dur + 0.03) * SR)
    t = np.arange(L) / SR
    f_t = midi(m)
    if gl is not None:
        f = f_t + (midi(gl) - f_t) * np.exp(-t / 0.05)
    else:
        f = f_t * (1 + 0.6 * np.exp(-t * 70))
    env = (0.4 + 0.6 * np.exp(-t * 2.4)) * np.minimum(1, t / 0.003)
    env *= np.clip((dur + 0.03 - t) / 0.03, 0, 1)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env
    x = np.tanh(2.6 * x) / np.tanh(2.6)
    place(bass, t_on, x, vel)
bass = lowpass(bass, 1100)

# ------------------------------------------------------------------------------------------- mix
def k_weight(x):
    s1 = ([1.53512485958697, -2.69169618940638, 1.19839281085285], [1, -1.69065929318241, 0.73248077421585])
    s2 = ([1.0, -2.0, 1.0], [1, -1.99004745483398, 0.99007225036621])
    from scipy.signal import lfilter
    return lfilter(*s2, lfilter(*s1, x))


def lufs(chans, t0=97.23, t1=110.0):
    i0, i1 = int(t0 * SR), int(t1 * SR)
    p = sum(np.mean(k_weight(c[i0:i1]) ** 2) for c in chans)
    return -0.691 + 10 * np.log10(p + 1e-12)


# sidechain pump: melodic parts dip under each kick
pump = np.ones(N)
for t in kick_times:
    i = int(t * SR)
    L = min(N - i, int(0.35 * SR))
    if L <= 0:
        continue
    tt = np.arange(L) / SR
    pump[i:i + L] = np.minimum(pump[i:i + L], 1 - 0.45 * np.exp(-tt / 0.11))

hat = highpass(hat, 6000)
ohat = highpass(ohat, 5000)
pluck = lowpass(pluck, 3500)
bell = lowpass(bell, 6500)
padL, padR = lowpass(padL, 2000), lowpass(padR, 2000)

# target loudness per stem in the drop-2 window (LUFS, before the master gain)
TARGET = {"kick": -15.0, "bass": -15.5, "clap": -20.0, "snare": -26.0, "hat": -25.0, "ohat": -30.0,
          "bell": -21.0, "pluck": -28.0, "pad": -25.0}
stems = {"kick": [kick], "bass": [bass], "clap": [clap], "snare": [snare], "hat": [hat], "ohat": [ohat],
         "bell": [bell], "pluck": [pluck], "pad": [padL, padR]}
gains = {}
for name, chans in stems.items():
    win = (at_k(46), GAPS[2][0]) if name == "snare" else (at_k(54), at_k(61))
    lv = lufs(chans * 2 if len(chans) == 1 else chans, *win)
    gains[name] = 10 ** ((TARGET[name] - lv) / 20)
    print(f"{name:6s} {lv:6.1f} LUFS -> gain {20 * np.log10(gains[name]):+5.1f} dB")

kick *= gains["kick"]
bass *= gains["bass"]
clap *= gains["clap"]
snare *= gains["snare"]
hat *= gains["hat"]
ohat *= gains["ohat"]
bell *= gains["bell"]
pluck *= gains["pluck"]
padL *= gains["pad"]
padR *= gains["pad"]

bell_p = bell * (1 - 0.5 * (1 - pump))
pluck_p = pluck * pump
padL, padR = padL * pump, padR * pump


def delay(x, s):
    d = int(SR * s)
    return np.concatenate([np.zeros(d), x[:-d]])


# ping-pong delay on the bell (dotted eighth), low-passed repeats
d8 = 0.75 * 0.43
echoL = lowpass(0.30 * delay(bell_p, d8) + 0.12 * delay(bell_p, 3 * d8), 3500)
echoR = lowpass(0.22 * delay(bell_p, 2 * d8) + 0.08 * delay(bell_p, 4 * d8), 3500)

left = kick + bass + clap + snare + 0.85 * hat + 1.1 * ohat + bell_p + 0.8 * pluck_p + padL
right = kick + bass + clap + snare + 1.1 * hat + 0.85 * ohat + bell_p + 1.2 * pluck_p + padR
left += echoL
right += echoR

# stereo room reverb (deterministic noise IR, 1.7 s)
ir_len = int(1.7 * SR)
ir_t = np.arange(ir_len) / SR
irs = []
for _ in range(2):
    ir = lowpass(rng.standard_normal(ir_len) * np.exp(-ir_t * 4.0), 5500)
    ir[: int(0.012 * SR)] = 0
    irs.append(ir / np.sqrt(np.sum(ir ** 2)))
send = 0.35 * clap + 0.25 * snare + 0.45 * bell_p + 0.3 * (padL + padR) + 0.2 * pluck_p
revL = fftconvolve(send, irs[0])[:N] * pump
revR = fftconvolve(send, irs[1])[:N] * pump
left += 0.28 * revL
right += 0.28 * revR

# filter moves on the music (risers and cymbals stay out of them)
# muffled hook: the groove runs through a low-pass that opens as the hook builds, then drops wide open at 5.80
left = sweep_filter(left, 0.0, at_k(0), 320, 1500)
right = sweep_filter(right, 0.0, at_k(0), 320, 1500)
# "but after that…": a high-pass rises under the roll into the stop
left = sweep_filter(left, at_k(22), GAPS[1][0], 30, 650, kind="high")
right = sweep_filter(right, at_k(22), GAPS[1][0], 30, 650, kind="high")
# breakdown under water, opening through the build into the second half
left = sweep_filter(left, at_k(43), GAPS[2][0], 550, 16000)
right = sweep_filter(right, at_k(43), GAPS[2][0], 550, 16000)

FX_TARGET = {"cym": (-25.0, at_k(54), at_k(55)), "rise": (-24.0, at_k(53, 2), at_k(54)),
             "boom": (-21.0, at_k(54), at_k(55))}
fx_gain = {}
for name, chans in (("cym", [cymL, cymR]), ("rise", [rise, rise]), ("boom", [boom, boom])):
    tgt, t0, t1 = FX_TARGET[name]
    fx_gain[name] = 10 ** ((tgt - lufs(chans, t0, t1)) / 20)
    print(f"{name:6s} gain {20 * np.log10(fx_gain[name]):+5.1f} dB")
cymL, cymR = cymL * fx_gain["cym"], cymR * fx_gain["cym"]
rise *= fx_gain["rise"]
boom *= fx_gain["boom"]
left += cymL + rise + boom
right += cymR + rise + boom

# hard stops (8 ms fades); a reverse crash marked through_stop stays audible inside its stop
gate = np.ones(N)
for a, b in GAPS:
    i, j = int(a * SR), int(b * SR)
    f = int(0.008 * SR)
    gate[i:j] = 0
    gate[i - f:i] = np.minimum(gate[i - f:i], np.linspace(1, 0, f))
    gate[j:j + f] = np.minimum(gate[j:j + f], np.linspace(0, 1, f))
left = left * gate + cymL * keep * (1 - gate)
right = right * gate + cymR * keep * (1 - gate)

# ring-out after the final hit, silent at the very end
tail = np.ones(N)
i0, i1 = int((FINAL + 0.35) * SR), N - int(0.05 * SR)
tail[i0:i1] = np.linspace(1, 0, i1 - i0) ** 1.6
tail[i1:] = 0
left *= tail
right *= tail
f = int(0.01 * SR)
left[:f] *= np.linspace(0, 1, f)
right[:f] *= np.linspace(0, 1, f)

stereo = np.stack([highpass(left, 28), highpass(right, 28)], axis=1)
# gentle glue: soft-clip the peaks, then set the bed to -14 LUFS (drop 2) with a -1 dBFS ceiling
lv = lufs([stereo[:, 0], stereo[:, 1]])
stereo *= 10 ** ((-14.0 - lv) / 20)
stereo = np.tanh(stereo * 1.15) / 1.15
peak = np.max(np.abs(stereo))
if peak > 0.89:
    stereo *= 0.89 / peak
print(f"bed: drop-2 {lufs([stereo[:, 0], stereo[:, 1]]):.1f} LUFS, peak {20 * np.log10(np.max(np.abs(stereo))):.1f} dBFS")

with wave.open(str(OUT), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((np.clip(stereo, -1, 1) * 32767).astype("<i2").tobytes())
print("wrote", OUT)
