"""ref_A/B/C.cube: bring episode 3's graded person onto the episode-2 reference Fred chose.
Skin-like colours follow a curve through the skin luma quantiles and get the reference skin R/G, B/G.
Neutral colours (hoodie, hair, shadows) follow a curve through the dark-tone quantiles (black like the reference) and get
the reference's dark tint. The two are blended by how warm (skin-like) each colour is, so one LUT handles both."""
import json, sys, numpy as np
from scipy.interpolate import PchipInterpolator
E = sys.argv[1]
st = json.load(open(f"{E}/qc/ref2/refstats.json")); R = st["REF"]
N = 33; g = np.linspace(0, 1, N); lumw = np.array([0.2126, 0.7152, 0.0722])
def ratios(m): return m[0] / m[1], m[2] / m[1]
for s in ("A", "B", "C"):
    X = st[s]
    cs = PchipInterpolator([0] + X["skin"]["q"] + [255], [0] + R["skin"]["q"] + [255])
    joinx = 60.0
    cd = PchipInterpolator([0] + X["dark"]["q"] + [joinx, 255], [0] + R["dark"]["q"] + [float(cs(joinx)), 255])
    sr, sb = [a / b for a, b in zip(ratios(R["skin"]["mean"]), ratios(X["skin"]["mean"]))]
    dr, db = [a / b for a, b in zip(ratios(R["dark"]["mean"]), ratios(X["dark"]["mean"]))]
    L = [f'TITLE "ep3-{s}-to-ep2-reference"', f"LUT_3D_SIZE {N}", "DOMAIN_MIN 0 0 0", "DOMAIN_MAX 1 1 1"]
    for b in g:
        for gg in g:
            for r in g:
                c = np.array([r, gg, b]); Y = float(c @ lumw) * 255
                warm = (c[0] - c[2]) / max(c[0], 1e-6) if c[0] > c[1] >= c[2] else 0.0
                ws = float(np.clip((warm - 0.10) / 0.20, 0, 1))
                Yn = ws * float(cs(Y)) + (1 - ws) * float(cd(Y)) if Y > 0 else 0.0
                c1 = c * (Yn / Y) if Y > 1e-6 else c.copy()
                wd = (1 - ws) * float(np.clip((60 - Y) / 30, 0, 1))          # tint only the deep neutral tones
                c1 = c1 * np.array([1 + ws * (sr - 1) + wd * (dr - 1), 1.0, 1 + ws * (sb - 1) + wd * (db - 1)])
                y1 = float(c1 @ lumw) * 255
                if y1 > 1e-6: c1 = c1 * (Yn / y1)
                L.append(" ".join(f"{v:.6f}" for v in np.clip(c1, 0, 1)))
    open(f"{E}/ref_{s}.cube", "w").write("\n".join(L) + "\n")
    print(s, "skin gains R %.3f B %.3f | dark gains R %.3f B %.3f" % (sr, sb, dr, db),
          "| skin curve", [round(float(cs(v)), 1) for v in (25, 47, 65, 96)], "dark curve", [round(float(cd(v)), 1) for v in (9, 13, 18, 23, 30, 45)])
