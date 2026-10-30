"""Gentle 'warm natural' look: neutral shadows, slight S-curve, warm highlights, +5% saturation."""
import numpy as np, sys
N = 33
g = np.linspace(0, 1, N)
lines = [f'TITLE "fred-warm-natural"', f"LUT_3D_SIZE {N}", "DOMAIN_MIN 0 0 0", "DOMAIN_MAX 1 1 1"]
for b in g:
    for gg in g:
        for r in g:
            c = np.array([r, gg, b])
            ss = c * c * (3 - 2 * c)                      # smoothstep S-curve
            c = c + 0.18 * (ss - c)                       # 18% of it: more depth, no crush
            l = c @ [0.2126, 0.7152, 0.0722]
            c = l + (c - l) * 1.05                        # +5% saturation
            w = np.clip((l - 0.35) / 0.65, 0, 1)          # warm only mids/highlights
            c = c * [1 + 0.035 * w, 1 + 0.005 * w, 1 - 0.04 * w]
            lines.append(" ".join(f"{v:.6f}" for v in np.clip(c, 0, 1)))
open(sys.argv[1], "w").write("\n".join(lines) + "\n")
