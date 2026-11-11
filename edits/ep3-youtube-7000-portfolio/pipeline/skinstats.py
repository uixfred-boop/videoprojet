"""Skin statistics per camera setup, measured on the graded person layer (before compositing).
usage: skinstats.py <work> [extra_lut_A extra_lut_B]  -> prints per-setup skin mean RGB + luma quantiles; saves samples.json"""
import json, subprocess, sys, numpy as np
E = sys.argv[1]
cfgs = json.load(open(f"{E}/setups.json")); C = json.load(open(f"{E}/edl.json"))["clips"]
extra = {"A": sys.argv[2], "B": sys.argv[3]} if len(sys.argv) > 3 else {}
def setup_of(a): return "A" if a < 125 else ("B" if a < 380 else "C")
by = {"A": [], "B": [], "C": []}
for c in C:
    if c.get("silent") or c.get("raw_vis") == "screen": continue     # VO over screen captures: no face in those
    by[setup_of(c["a"])].append((c["a"] + c["b"]) / 2)
def grab(src, t, vf, fmt, shape):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", vf, "-f", "rawvideo", "-pix_fmt", fmt, "-"],
                       capture_output=True).stdout
    return np.frombuffer(r, np.uint8).reshape(shape).astype(float)
res = {}
for st, ts in by.items():
    cfg = cfgs[st]; g = [cfg["gains"][i] / cfgs["A"]["gains"][i] for i in range(3)]
    pick = [ts[int(i)] for i in np.linspace(0, len(ts) - 1, min(8, len(ts)))]
    px = []
    for t in pick:
        vf = (f"unsharp=5:5:0.45:5:5:0,format=gbrpf32le,colorchannelmixer=rr={g[0]}:gg={g[1]}:bb={g[2]},"
              f"lut3d={E}/person_warm.cube:interp=tetrahedral" + (f",lut3d={E}/{extra[st]}:interp=tetrahedral" if st in extra else "") +
              ",scale=1920:1080:flags=area,format=rgb24")
        rgb = grab(f"{E}/raw.mp4", t, vf, "rgb24", (1080, 1920, 3))
        a = grab(f"{E}/matte/{cfg['alpha']}", t - cfg["alpha_offset"], "format=gray", "gray", (1080, 1920))
        R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]; Y = .2126 * R + .7152 * G + .0722 * B
        m = (a > 245) & (R > G + 6) & (G > B) & ((R - B) / np.maximum(R, 1) > 0.22) & (Y > 18) & (Y < 200)
        px.append(rgb[m])
    p = np.concatenate(px); Y = p @ [.2126, .7152, .0722]
    res[st] = {"mean": p.mean(0).round(2).tolist(), "q": np.percentile(Y, [5, 25, 50, 75, 95]).round(2).tolist(), "n": int(len(p))}
    print(st, "skin RGB", p.mean(0).round(1), "R/G %.3f B/G %.3f" % (p[:, 0].mean() / p[:, 1].mean(), p[:, 2].mean() / p[:, 1].mean()),
          "Y q5/25/50/75/95", np.percentile(Y, [5, 25, 50, 75, 95]).round(1), "n", len(p))
json.dump(res, open(f"{E}/qc/match/stats{'_after' if extra else ''}.json", "w"), indent=1)
