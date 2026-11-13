"""Génère les données Remotion de chaque short à partir de spec.py et des mots alignés.

Usage : python3 build.py  → écrit remotion/src/data/<short>.json
"""
import json, re, sys, importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FPS = 30
PAD_IN, PAD_OUT = 0.03, 0.12
CTA_DUR = 2.4

spec_mod = importlib.util.spec_from_file_location("spec", HERE / "spec.py")
spec = importlib.util.module_from_spec(spec_mod); spec_mod.loader.exec_module(spec)
WORDS = json.load(open(HERE.parent / "transcript" / "mots_alignes.json"))["words"]

def norm(s):
    return re.sub(r"[^a-z0-9$]", "", s.lower().replace("’", "'"))

TAG = re.compile(r"\{([bisxmg]):([^}]*)\}")

def parse_lockup(markup):
    quoted = markup.startswith(">")
    if quoted: markup = markup[1:]
    toks = []
    pos = 0
    for m in TAG.finditer(markup):
        for w in markup[pos:m.start()].split():
            toks.append({"text": w, "style": "base"})
        for w in m.group(2).split():
            toks.append({"text": w, "style": m.group(1)})
        pos = m.end()
    for w in markup[pos:].split():
        toks.append({"text": w, "style": "base"})
    return quoted, toks

MIN_PAUSE, KEEP_PAUSE = 0.4, 0.25
_ENV = None
def voice_env():
    """Enveloppe RMS (pas de 20 ms) de la voix isolée par Demucs."""
    global _ENV
    if _ENV is None:
        import wave
        import numpy as np
        w = wave.open(str(ROOT / "remotion" / "public" / "audio" / "voice.wav"))
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).mean(1) / 32768
        hop = int(w.getframerate() * 0.02)
        _ENV = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, "same")[::hop]) + 1e-9)
    return _ENV

def split_pauses(segs):
    import numpy as np
    env = voice_env(); out = []
    for a, b in segs:
        e = env[int(a / 0.02):int(b / 0.02)]; thr = np.median(e) - 22
        cur = a; run = 0
        for k, v in enumerate(list(e < thr) + [False]):
            if v: run += 1; continue
            L = run * 0.02
            if L >= MIN_PAUSE:
                p0 = a + (k - run) * 0.02
                out.append((cur, p0 + KEEP_PAUSE / 2 - PAD_OUT))
                cur = p0 + L - KEEP_PAUSE / 2 + PAD_IN
            run = 0
        out.append((cur, b))
    return out

def build(sid, sh):
    segs = sh["segments"]
    # mots du short (sélection sur les segments du plan)
    pool = [dict(w) for (a, b) in segs for w in WORDS if w["start"] >= a - 0.05 and w["start"] < b - 0.01]
    # coupe des silences internes (> MIN_PAUSE) détectés sur la voix isolée
    segs = split_pauses(segs)
    for w in pool:
        k = next((k for k, (a, b) in enumerate(segs) if a - 0.05 <= w["start"] < b + PAD_OUT), None)
        if k is None:  # mot dont le début tombe dans un silence retiré : on le cale au segment suivant
            k = next(k for k, (a, b) in enumerate(segs) if a > w["start"])
            w["start"] = segs[k][0]
        w["seg"] = k
    # temps du short
    offs, acc = [], 0.0
    for a, b in segs:
        offs.append(acc); acc += (b + PAD_OUT) - max(0.0, a - PAD_IN)
    voice_end = acc
    def tshort(src, k):
        return offs[k] + (src - max(0.0, segs[k][0] - PAD_IN))
    fr = lambda t: int(round(t * FPS))

    cursor = 0
    scenes, lockups = [], []
    for si, sc in enumerate(sh["scenes"]):
        sc_lockups = []
        for li, mk in enumerate(sc["caps"]):
            quoted, toks = parse_lockup(mk)
            for t in toks:
                if cursor >= len(pool):
                    sys.exit(f"{sid}: plus de mots pour « {t['text']} »")
                w = pool[cursor]
                if norm(w["w"]) != norm(t["text"]):
                    sys.exit(f"{sid} scène {si+1}: attendu « {w['w']} » ({w['start']:.2f}s), trouvé « {t['text']} »")
                t["src"] = w["start"]; t["seg"] = w["seg"]; t["t"] = tshort(w["start"], w["seg"])
                cursor += 1
            sc_lockups.append({"quoted": quoted, "words": toks})
        scenes.append({"spec": sc, "lockups": sc_lockups})
    if cursor != len(pool):
        rest = " ".join(w["w"] for w in pool[cursor:cursor+8])
        sys.exit(f"{sid}: {len(pool)-cursor} mots non couverts : {rest}…")

    out_scenes, out_lockups = [], []
    for i, s in enumerate(scenes):
        first = s["lockups"][0]["words"][0]
        t0 = 0.0 if i == 0 else first["t"]
        t1 = scenes[i+1]["lockups"][0]["words"][0]["t"] if i + 1 < len(scenes) else voice_end
        p = {k: v for k, v in s["spec"].items() if k not in ("caps",)}
        src0 = first["src"] - (first["t"] - t0)  # temps source au début de la scène
        if "revealAt" in p:
            p["revealAt"] = max(0, fr(p["revealAt"] - src0))
        if "cxAt" in p:  # convertir les temps source en images de scène
            p["cxAt"] = [[max(0, fr(ts - src0)) if ts > 0 else 0, cx] for ts, cx in p["cxAt"]]
        # éléments synchronisés sur des mots (listes, étapes)
        flat = [w for L in s["lockups"] for w in L["words"]]
        def word_frame(label):
            for w in flat:
                if norm(w["text"]) == norm(label):
                    return fr(w["t"]) - fr(t0)
            return 0
        if p.get("items"):
            p["items"] = [{"text": txt, "at": (word_frame(trig) if trig else 0)} for txt, trig in p["items"]]
        if p.get("nodes"):
            p["nodes"] = [{"text": txt, "at": word_frame(trig)} for txt, trig in p["nodes"]]
        # morceaux de rush à jouer dans la scène (un par segment après coupe des silences)
        pieces = []
        for k, (a, b) in enumerate(segs):
            s0 = offs[k]; s1 = offs[k + 1] if k + 1 < len(segs) else voice_end
            ps, pe = max(s0, t0), min(s1, t1)
            if pe > ps + 1e-3:
                pieces.append({"from": fr(ps) - fr(t0), "src": round(max(0.0, a - PAD_IN) + (ps - s0), 3)})
        out_scenes.append(dict(p, **{"from": fr(t0), "to": fr(t1), "srcStart": round(src0, 3), "idx": i, "pieces": pieces}))
        for j, L in enumerate(s["lockups"]):
            lt0 = L["words"][0]["t"] if not (i == 0 and j == 0) else 0.0
            nxt = s["lockups"][j+1]["words"][0]["t"] if j + 1 < len(s["lockups"]) else t1
            out_lockups.append({
                "from": fr(lt0), "to": fr(nxt), "scene": i, "quoted": L["quoted"],
                "hidden": bool(p.get("hide")),
                "words": [{"text": w["text"], "style": w["style"], "at": fr(w["t"]) - fr(lt0)} for w in L["words"]],
            })
    total = voice_end + CTA_DUR
    voice = [{"src0": round(max(0.0, a - PAD_IN), 3), "src1": round(b + PAD_OUT, 3), "from": fr(offs[k])} for k, (a, b) in enumerate(segs)]
    data = {
        "id": sid, "titre": sh["titre"], "fps": FPS, "durationInFrames": fr(total),
        "voiceEnd": fr(voice_end), "voice": voice, "scenes": out_scenes, "lockups": out_lockups,
        "cta": {"from": fr(voice_end), "to": fr(total), "word": sh["cta"][0], "line": sh["cta"][1]},
    }
    return data

if __name__ == "__main__":
    outdir = ROOT / "remotion" / "src" / "data"; outdir.mkdir(parents=True, exist_ok=True)
    index = []
    for sid, sh in spec.SHORTS.items():
        d = build(sid, sh)
        json.dump(d, open(outdir / f"{sid}.json", "w"), ensure_ascii=False, indent=1)
        index.append(sid)
        print(f"{sid}: {d['durationInFrames']/FPS:5.1f} s, {len(d['scenes'])} scènes, {len(d['lockups'])} blocs de texte")
