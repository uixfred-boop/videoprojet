"""person.cube: gentle contrast for the talking head. look.cube: Kallaway-style finish (cool shadows, warm highlights)."""
import numpy as np, sys
N = 33; g = np.linspace(0, 1, N)
def write(path, fn, title):
    L = [f'TITLE "{title}"', f"LUT_3D_SIZE {N}", "DOMAIN_MIN 0 0 0", "DOMAIN_MAX 1 1 1"]
    for b in g:
        for gg in g:
            for r in g:
                L.append(" ".join(f"{v:.6f}" for v in np.clip(fn(np.array([r, gg, b])), 0, 1)))
    open(path, "w").write("\n".join(L) + "\n")
lum = lambda c: c @ [0.2126, 0.7152, 0.0722]
def person(c):
    ss = c * c * (3 - 2 * c); c = c + 0.15 * (ss - c)          # depth without crushing skin
    l = lum(c); c = l + (c - l) * 1.04
    return c * 0.97 + 0.004                                     # sit a touch darker into the moody room
def look(c):
    l = lum(c)
    sh = (1 - l) ** 2.2; hi = l ** 2
    c = c + sh * np.array([-0.012, 0.0, 0.022]) + hi * np.array([0.018, 0.004, -0.018])
    ss = c * c * (3 - 2 * c); c = c + 0.12 * (ss - c)
    return 0.012 + c * 0.985                                    # black point lifted 1 %: deep but not clipped
write(sys.argv[1] + "/person.cube", person, "fred-person"); write(sys.argv[1] + "/look.cube", look, "fred-blue-room")
