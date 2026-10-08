#!/usr/bin/env python3
"""Simulate a HyperFrames composition's audio mix offline, before rendering.

Sums every <audio> element of index.html at its data-start / data-duration / data-volume, applies a carved bed's
data-fx-chain (peaking and gain nodes) with its data-automation lanes, and reports the loudness and true peak.
The renderer lowers the whole mix when the true peak goes over -1 dBTP, so check that here first.

    python tools/simulate_mix.py videos/<name> [--voice vo] [--bed music-bed] [--bed-volume 0.5]
                                               [--mute music-bed] [--out mix.wav]

Needs numpy + scipy and ffmpeg on PATH. Notes on the renderer it mirrors:
  * a data-automation lane on `volume` replaces data-volume (it does not scale it);
  * fx lanes give the node parameter directly (dB for gain), linearly interpolated, held before the first point.
"""
import argparse
import html
import json
import pathlib
import re
import subprocess
import wave

import numpy as np
from scipy.signal import lfilter, resample_poly

SR = 48000


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).astype(np.float64)


def lane_values(points, n, t0=0.0):
    ts = np.array([p["t"] for p in points], dtype=float)
    vs = np.array([p["v"] for p in points], dtype=float)
    return np.interp(t0 + np.arange(n) / SR, ts, vs)


def peaking_coefs(f0, gain_db, q):
    a = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * f0 / SR
    alpha = np.sin(w0) / (2 * q)
    b = np.array([1 + alpha * a, -2 * np.cos(w0), 1 - alpha * a])
    den = np.array([1 + alpha / a, -2 * np.cos(w0), 1 - alpha / a])
    return b / den[0], den / den[0]


def apply_chain(x, chain, lanes):
    """x: (n, 2). Peaking nodes are processed in 10 ms blocks so their gain can follow a lane."""
    by_target = {ln["target"]: ln["points"] for ln in lanes}
    n = len(x)
    for node in chain.get("nodes", []):
        if node.get("enabled") is False:
            continue
        kind, nid, params = node["type"], node["id"], node.get("params", {})
        lane = by_target.get(f"fx.{nid}.gain")
        g = lane_values(lane, n) if lane else np.full(n, float(params.get("gain", 0)))
        if kind == "gain":
            x = x * (10 ** (g / 20))[:, None]
        elif kind == "peaking":
            blk = SR // 100
            out = np.empty_like(x)
            zi = np.zeros((2, 2))
            for i in range(0, n, blk):
                b, a = peaking_coefs(float(params["frequency"]), float(g[min(n - 1, i + blk // 2)]), float(params["q"]))
                for c in range(2):
                    out[i:i + blk, c], zi[c] = lfilter(b, a, x[i:i + blk, c], zi=zi[c])
            x = out
        else:
            print(f"  (fx node type {kind!r} not simulated)")
    return x


def k_weighted(x):
    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1, -1.99004745483398, 0.99007225036621]
    return lfilter(b2, a2, lfilter(b1, a1, x, axis=0), axis=0)


def block_loudness(x, win=0.4, hop=0.1):
    z = k_weighted(x) ** 2
    w, h = int(win * SR), int(hop * SR)
    cs = np.concatenate([np.zeros((1, 2)), np.cumsum(z, axis=0)])
    starts = np.arange(0, max(1, len(x) - w + 1), h)
    ms = (cs[starts + w] - cs[starts]) / w
    return starts / SR, -0.691 + 10 * np.log10(ms.sum(axis=1) + 1e-15)


def integrated(x):
    _, l = block_loudness(x)
    l = l[l > -70]
    if len(l) == 0:
        return -np.inf
    rel = 10 * np.log10(np.mean(10 ** (l / 10))) - 10
    l = l[l > rel]
    return 10 * np.log10(np.mean(10 ** (l / 10)))


def true_peak_db(x):
    up = resample_poly(x, 4, 1, axis=0)
    return 20 * np.log10(np.max(np.abs(up)) + 1e-12)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--voice", default="vo")
    ap.add_argument("--bed", default="music-bed")
    ap.add_argument("--bed-volume", type=float, default=None, help="override the bed's data-volume")
    ap.add_argument("--mute", action="append", default=[], help="element id to leave out (repeatable)")
    ap.add_argument("--out", default=None, help="write the simulated mix to this WAV")
    args = ap.parse_args()

    proj = pathlib.Path(args.project)
    src = (proj / "index.html").read_text()
    root_dur = float(re.search(r'data-composition-id="[^"]+"[^>]*?data-duration="([\d.]+)"', src).group(1))
    n = int(round(root_dur * SR))
    mix = np.zeros((n, 2))
    stems = {}
    cache = {}
    for m in re.finditer(r"<audio\s+([^>]*)>", src, flags=re.S):
        attrs = {k: html.unescape(v) for k, v in re.findall(r'([\w-]+)="([^"]*)"', m.group(1))}
        eid = attrs.get("id", "?")
        if eid in args.mute:
            continue
        path = proj / attrs["src"]
        if path not in cache:
            cache[path] = decode(path)
        st = float(attrs.get("data-start", 0))
        du = float(attrs.get("data-duration", root_dur - st))
        ms = float(attrs.get("data-media-start", 0))
        x = cache[path][int(ms * SR):int((ms + du) * SR)].copy()
        lanes = json.loads(attrs["data-automation"])["lanes"] if "data-automation" in attrs else []
        if "data-fx-chain" in attrs:
            x = apply_chain(x, json.loads(attrs["data-fx-chain"]), lanes)
        vol_lane = next((ln["points"] for ln in lanes if ln["target"] == "volume"), None)
        if vol_lane:
            x = x * lane_values(vol_lane, len(x))[:, None]
        else:
            vol = float(attrs.get("data-volume", 1))
            if eid == args.bed and args.bed_volume is not None:
                vol = args.bed_volume
            x = x * vol
        i = int(round(st * SR))
        j = min(n, i + len(x))
        if j <= i:
            continue
        mix[i:j] += x[: j - i]
        if eid in (args.voice, args.bed):
            stems[eid] = np.zeros((n, 2))
            stems[eid][i:j] += x[: j - i]

    print(f"mix     integrated {integrated(mix):6.1f} LUFS   true peak {true_peak_db(mix):5.1f} dBTP")
    if args.voice in stems and args.bed in stems:
        tv, lv = block_loudness(stems[args.voice], 3.0, 0.5)
        _, lb = block_loudness(stems[args.bed], 3.0, 0.5)
        speech = lv > -40
        diff = lv[speech] - lb[speech]
        print(f"voice   integrated {integrated(stems[args.voice]):6.1f} LUFS")
        print(f"bed     integrated {integrated(stems[args.bed]):6.1f} LUFS")
        print(f"bed under speech (3 s short-term): median {np.median(diff):4.1f} dB below the voice "
              f"(10th pct {np.percentile(diff, 10):4.1f}, 90th pct {np.percentile(diff, 90):4.1f})")
    if args.out:
        y = np.clip(mix, -1, 1)
        with wave.open(args.out, "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((y * 32767).astype("<i2").tobytes())
        print("wrote", args.out)


if __name__ == "__main__":
    main()
