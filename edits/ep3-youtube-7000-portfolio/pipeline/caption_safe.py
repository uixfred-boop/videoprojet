"""Keep the bottom band (y >= SAFE px at 4K) free for subtitles: lift lower-third cards and shrink tall browser frames.
Writes shots.json in place (backup: shots_v2.json) and prints the shots that must be re-rendered."""
import json, math, sys
from PIL import Image
sys.path.insert(0, sys.argv[1])
E = sys.argv[1]; K = 2; SAFE = 1790
from gfx import browser_frame, save
S = json.load(open(f"{E}/shots.json"))["shots"] if "shots" in json.load(open(f"{E}/shots.json")) else None
doc = json.load(open(f"{E}/shots.json"))
def bottom(it):
    w, h = Image.open(it["png"]).size; pad = it.get("pad", 0)
    return it["y"] * K + h - 2 * pad
NEWBOX = {"frame_1400x788.png": (360, 60, 1200, 675), "frame_1560x878.png": (330, 40, 1260, 709)}
changed = []
for i, s in enumerate(doc["shots"]):
    items = s["items"]; touched = False
    fr = [it for it in items if it["png"].split("/")[-1] in NEWBOX]
    if fr:
        x, y, w, h = NEWBOX[fr[0]["png"].split("/")[-1]]
        path = f"{E}/g/frame_{w}x{h}.png"
        bf, p, vp = browser_frame(w, h); save((bf, p), path)
        fr[0].update({"png": path, "pad": p, "x": x, "y": y})
        for it in items:
            if "video" in it: it["video"].update({"x": x + 1, "y": y + 46, "w": w - 2, "h": h - 2})
        touched = True
    low = [it for it in items if "video" not in it and not it["png"].endswith("empty.png") and bottom(it) > SAFE]
    if low:
        dy = math.ceil((max(bottom(it) for it in low) - SAFE) / K)
        for it in low: it["y"] -= dy
        touched = True
    if touched: changed.append(i)
json.dump(doc, open(f"{E}/shots.json", "w"), indent=1)
print("re-render:", " ".join(map(str, changed)))
for i in changed:
    print(i, doc["shots"][i]["kind"], [(it["png"].split("/")[-1], it["x"], it["y"], bottom(it)) for it in doc["shots"][i]["items"] if "video" not in it])
