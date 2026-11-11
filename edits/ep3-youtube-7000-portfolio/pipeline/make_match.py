"""Build match_A.cube / match_B.cube: bring the graded skin of setups A and B onto setup C (the look Fred picked).
Luma: monotone curve through the skin luma quantiles (5/25/50/75/95 %) of the setup onto C's.
Colour: R/G and B/G of the skin moved onto C's, weighted by how warm (skin-like) a colour is, so neutral
whites (teeth, eyes) and the black hoodie are left alone. Brightness after the colour move is pinned to the curve."""
import json, sys, numpy as np
from scipy.interpolate import PchipInterpolator
E = sys.argv[1]
st = json.load(open(f"{E}/qc/match/stats.json"))
N = 33; g = np.linspace(0, 1, N)
lum = lambda c: c @ np.array([0.2126, 0.7152, 0.0722])
tC = st["C"]
for s in ("A", "B"):
    src = st[s]
    xs = [0.0] + src["q"] + [255.0]; ys = [0.0] + tC["q"] + [255.0]
    curve = PchipInterpolator(xs, ys)
    m, mc = np.array(src["mean"]), np.array(tC["mean"])
    gR = (mc[0] / mc[1]) / (m[0] / m[1]); gB = (mc[2] / mc[1]) / (m[2] / m[1])
    L = [f'TITLE "match-{s}-to-C"', f"LUT_3D_SIZE {N}", "DOMAIN_MIN 0 0 0", "DOMAIN_MAX 1 1 1"]
    for b in g:
        for gg in g:
            for r in g:
                c = np.array([r, gg, b]); Y = lum(c) * 255
                Yn = float(curve(Y)) if Y > 0 else 0.0
                c1 = c * (Yn / Y) if Y > 1e-6 else c.copy()
                warm = (c[0] - c[2]) / max(c[0], 1e-6) if c[0] > c[1] >= c[2] else 0.0
                w = np.clip((warm - 0.10) / 0.20, 0, 1)
                c1 = c1 * np.array([1 + w * (gR - 1), 1.0, 1 + w * (gB - 1)])
                y1 = lum(c1) * 255
                if y1 > 1e-6: c1 = c1 * (Yn / y1)
                L.append(" ".join(f"{v:.6f}" for v in np.clip(c1, 0, 1)))
    open(f"{E}/match_{s}.cube", "w").write("\n".join(L) + "\n")
    print(s, "gR %.3f gB %.3f" % (gR, gB), "curve", [round(float(curve(v)), 1) for v in (10, 26, 40, 50, 65, 92, 150, 220)])
