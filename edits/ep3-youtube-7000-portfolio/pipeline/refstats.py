"""Compare the person's tones in the episode-2 reference with episode 3 (graded person layer, before compositing).
Classes inside the matte: skin (warm), darks (Y<40: hair, top/hoodie), whole person luma quantiles."""
import json, subprocess, sys, numpy as np
E = sys.argv[1]; REF = sys.argv[2]; extra = dict(a.split("=") for a in sys.argv[3:])   # e.g. A=lutA.cube
W, H = 960, 540
def grab(src, t, vf, fmt, ch):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", vf, "-f", "rawvideo", "-pix_fmt", fmt, "-"], capture_output=True).stdout
    a = np.frombuffer(r, np.uint8).astype(float); return a.reshape(H, W, ch) if ch > 1 else a.reshape(H, W)
def classes(rgb, a):
    R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]; Y = .2126 * R + .7152 * G + .0722 * B
    inside = a > 245
    skin = inside & (R > G + 6) & (G > B) & ((R - B) / np.maximum(R, 1) > 0.22) & (Y > 18) & (Y < 200)
    dark = inside & (Y < 40) & ~skin
    return skin, dark, inside, Y
def summary(name, P):
    out = {}
    for k in ("skin", "dark"):
        p = np.concatenate(P[k]); Y = p @ [.2126, .7152, .0722]
        out[k] = {"mean": p.mean(0).round(2).tolist(), "q": np.percentile(Y, [5, 25, 50, 75, 95]).round(2).tolist()}
    y = np.concatenate(P["Y"]); out["person_q"] = np.percentile(y, [2, 10, 25, 50, 75, 90, 98]).round(2).tolist()
    print(f"{name:4s} skin {np.round(out['skin']['mean'],1)} Yq {out['skin']['q']} | dark {np.round(out['dark']['mean'],1)} Yq {out['dark']['q']} | person Yq {out['person_q']}")
    return out
res = {}
# reference: every ~1.5 s
P = {"skin": [], "dark": [], "Y": []}
for t in np.arange(0.5, 24.0, 1.5):
    rgb = grab(REF, t, f"scale={W}:{H}:flags=area,format=rgb24", "rgb24", 3); a = grab(f"{E}/qc/ref2/ref_pha.mkv", t, "format=gray", "gray", 1)
    s, d, i, Y = classes(rgb, a); P["skin"].append(rgb[s]); P["dark"].append(rgb[d]); P["Y"].append(Y[i])
res["REF"] = summary("REF", P)
# episode 3: graded person layer per setup
cfgs = json.load(open(f"{E}/setups.json")); C = json.load(open(f"{E}/edl.json"))["clips"]
so = lambda a: "A" if a < 125 else ("B" if a < 380 else "C")
by = {"A": [], "B": [], "C": []}
for c in C:
    if not c.get("silent") and c.get("raw_vis") != "screen": by[so(c["a"])].append((c["a"] + c["b"]) / 2)
for st, ts in by.items():
    cfg = cfgs[st]; g = [cfg["gains"][i] / cfgs["A"]["gains"][i] for i in range(3)]
    chain = [f"unsharp=5:5:0.45:5:5:0,format=gbrpf32le,colorchannelmixer=rr={g[0]}:gg={g[1]}:bb={g[2]}", f"lut3d={E}/person_warm.cube:interp=tetrahedral"]
    if st in ("A", "B"): chain.append(f"lut3d={E}/match_{st}.cube:interp=tetrahedral")
    if st in extra: chain.append(f"lut3d={E}/{extra[st]}:interp=tetrahedral")
    vf = ",".join(chain) + f",scale={W}:{H}:flags=area,format=rgb24"
    P = {"skin": [], "dark": [], "Y": []}
    for t in [ts[int(i)] for i in np.linspace(0, len(ts) - 1, min(8, len(ts)))]:
        rgb = grab(f"{E}/raw.mp4", t, vf, "rgb24", 3); a = grab(f"{E}/matte/{cfg['alpha']}", t - cfg["alpha_offset"], f"scale={W}:{H},format=gray", "gray", 1)
        s, d, i, Y = classes(rgb, a); P["skin"].append(rgb[s]); P["dark"].append(rgb[d]); P["Y"].append(Y[i])
    res[st] = summary(st, P)
json.dump(res, open(f"{E}/qc/ref2/refstats{'_after' if extra else ''}.json", "w"), indent=1)
