"""Word-by-word subtitles in Fred's reference style -> captions.ass (+ captions.json for checks).

Text comes from the cut list (edl.json, the corrected spoken text); timing comes from a word-level transcription of the
final voice track (words_forced.json: the cut list's text force-aligned clip by clip). Style: white Inter Medium, one keyword per line in blue
Instrument Serif Italic, soft dark glow. Each word rises in (~28 px, 0.22 s) and fades in exactly when it is spoken; the
line clears at the end of the phrase. Lines sit in the bottom band, which the final pass darkens with a gradient."""
import difflib, json, re, sys
E = sys.argv[1]
FPS = 30
W, H = 3840, 2160
X, Y = W // 2, 1985                 # \an2: bottom-centre of the line box
FS, FS_EM = 116, 136                # Inter Medium cap ~70 px; serif sized to the same x-height
WHITE, BLUE = "&H00FFFFFF&", "&H00EFB25A&"   # blue = #5AB2EF (BGR in ASS)
RISE, T_IN, T_OUT = 28, 140, 110

clips = json.load(open(f"{E}/edl.json"))["clips"]
t = 0.0
for c in clips:
    c["d"] = c.get("silent") or round((c["b"] - c["a"]) * FPS) / FPS; c["t"] = t; t += c["d"]
WW = json.load(open(f"{E}/words_forced.json"))     # script text force-aligned onto the final voice track (words_forced.py)
norm = lambda s: re.sub(r"[^a-z0-9$]", "", s.lower().replace("’", "'").replace(",", ""))

# ---- 1. timed tokens: EDL text aligned onto the transcription, clip by clip
tokens = []
for c in clips:
    if c.get("silent"): continue
    a, b = c["t"], c["t"] + c["d"]
    ws = [w for w in WW if w["clip"] == c["id"]]
    toks = [x for x in c["text"].replace("...", " ").replace("—", " ").split() if norm(x)]
    sm = difflib.SequenceMatcher(None, [norm(x) for x in toks], [norm(w["w"]) for w in ws], autojunk=False)
    tm = [None] * len(toks)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1): tm[i1 + k] = (ws[j1 + k]["s"], ws[j1 + k]["e"])
        elif op == "replace" and j2 > j1:          # different counts: spread the tokens over those words' span
            s0, e0 = ws[j1]["s"], ws[j2 - 1]["e"]; n = i2 - i1; L = sum(len(toks[i]) for i in range(i1, i2)); acc = 0
            for i in range(i1, i2):
                ts = s0 + (e0 - s0) * acc / L; acc += len(toks[i]); tm[i] = (ts, s0 + (e0 - s0) * acc / L)
    # tokens still untimed (inserted in the text, nothing heard): interpolate between neighbours / clip edges
    i = 0
    while i < len(toks):
        if tm[i] is None:
            j = i
            while j < len(toks) and tm[j] is None: j += 1
            s0 = tm[i - 1][1] if i > 0 else max(a, (ws[0]["s"] - 0.3) if ws else a)
            e0 = tm[j][0] if j < len(toks) else min(b, (ws[-1]["e"] + 0.3) if ws else b)
            if e0 <= s0: e0 = s0 + 0.12 * (j - i)
            L = sum(len(toks[k]) for k in range(i, j)); acc = 0
            for k in range(i, j):
                ts = s0 + (e0 - s0) * acc / L; acc += len(toks[k]); tm[k] = (ts, s0 + (e0 - s0) * acc / L)
            i = j
        else: i += 1
    for tok, (s, e) in zip(toks, tm):
        tokens.append({"w": tok, "s": max(a, min(s, b - 0.05)), "e": max(a, min(e, b)), "clip": c["id"]})
# keep time order strictly increasing
for i in range(1, len(tokens)):
    tokens[i]["s"] = max(tokens[i]["s"], tokens[i - 1]["s"] + 0.04)

# ---- 2. lines (chunks)
def shown(w):                       # displayed form: no trailing , . : ; (cleaner lines); keep ? ! quotes $ '
    w = w.strip()
    w = re.sub(r"[,.:;]+(\"?)$", r"\1", w)
    return w
# phrases: cut at sentence/clause punctuation, at pauses, and between clips that are not spoken back to back
phrases, cur = [], []
for tk in tokens:
    if cur:
        prev = cur[-1]; gap = tk["s"] - prev["e"]
        endp = prev["w"].rstrip("\"”").endswith((".", "?", "!", ":", ",", ";"))
        if gap > 0.45 or endp or (prev["clip"] != tk["clip"] and gap > 0.25):
            phrases.append(cur); cur = []
    cur.append(tk)
if cur: phrases.append(cur)
MAXC, MAXW = 30, 6
def text_of(ws): return " ".join(shown(x["w"]) for x in ws)
def split_balanced(ph):
    """Split a phrase into the fewest lines that fit, with line lengths as even as possible."""
    if len(text_of(ph)) <= MAXC + 2 and len(ph) <= MAXW: return [ph]
    best = None
    for k in range(2, len(ph) + 1):
        # dynamic programming over cut points: minimise the longest line, lines must fit
        n = len(ph); INF = 10 ** 9
        dp = [[INF] * (k + 1) for _ in range(n + 1)]; cut = [[0] * (k + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        for i in range(1, n + 1):
            for j in range(1, k + 1):
                for m in range(j - 1, i):
                    seg = ph[m:i]; L = len(text_of(seg))
                    if L > MAXC + 2 or len(seg) > MAXW: continue
                    v = max(dp[m][j - 1], L)
                    if v < dp[i][j]: dp[i][j] = v; cut[i][j] = m
        if dp[n][k] < INF:
            out, i, j = [], n, k
            while j > 0: m = cut[i][j]; out.append(ph[m:i]); i, j = m, j - 1
            best = out[::-1]; break
    return best or [ph]
chunks = []
for ph in phrases: chunks += split_balanced(ph)
# fold lone words into a neighbour line. A lone lead-in ("So,", "First:", "Then,") joins the NEXT line; any other lone
# word joins the previous line unless that line ends a sentence. Never across a long pause.
ends_sentence = lambda ws: ws[-1]["w"].rstrip("\"”").endswith((".", "?", "!"))
leads_in = lambda w: w.rstrip("\"”").endswith((",", ":", ";"))
merged, pending = [], None
for ch in chunks:
    if pending is not None:
        if ch[0]["s"] - pending[-1]["e"] < 0.6 and len(text_of(pending + ch)) <= MAXC + 10: ch = pending + ch
        else: merged.append(pending)
        pending = None
    if len(ch) == 1 and leads_in(ch[0]["w"]):
        pending = ch; continue
    if (len(ch) == 1 and merged and not ends_sentence(merged[-1]) and ch[0]["s"] - merged[-1][-1]["e"] < 0.3
            and len(text_of(merged[-1] + ch)) <= MAXC + 4):
        merged[-1] += ch
    else: merged.append(ch)
if pending is not None: merged.append(pending)
chunks = merged

# ---- 3. one emphasised word per line (blue serif italic), not on every line
KEY3 = {"$7,000", "7,000", "zero", "millions", "three", "fifty"}
KEY2 = set("""portfolio client clients question deal classic mistake views value system good smart simple business idea
design industry construction money website time projects gold premium path remove add fewer less space visuals shout stage
mobile-first phone framer motion feel hours details feeling strategy proud enough worthless exactly contact important
persona replied discovery worked comment better skill same changed difference honest guarantee outreach magic packaged
template blank kit land anywhere description subscribe instagram only pick profile attention scrolling pages\nyes no nobody everyone everything""".split())
def score(w):
    n = re.sub(r"[^a-z0-9$,\-]", "", w.lower()).strip(",")
    return 3 if n in KEY3 else (2 if n in KEY2 else 0)
prev_em = False
for ch in chunks:
    best = max(range(len(ch)), key=lambda i: (score(ch[i]["w"]), len(ch[i]["w"])))
    sc = score(ch[best]["w"])
    use = sc >= 3 or (sc == 2 and not prev_em and len(ch) >= 2)
    for i, tk in enumerate(ch): tk["em"] = use and i == best
    prev_em = use

# ---- 4. timing of each line and ASS events
def ts(x):
    x = max(0.0, x); h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"
def piece(tk, visible):
    w = shown(tk["w"]).replace("{", "(").replace("}", ")")
    a = r"\alpha&H00&\3a&H70&" if visible else r"\alpha&HFF&"
    if tk["em"]: return "{" + rf"\fnInstrument Serif\i1\fs{FS_EM}\c{BLUE}{a}" + "}" + w + "{" + rf"\fnInter Medium\i0\fs{FS}\c{WHITE}" + "}"
    return "{" + a + "}" + w
events = []
for n, ch in enumerate(chunks):
    nxt = chunks[n + 1][0]["s"] if n + 1 < len(chunks) else ch[-1]["e"] + 1.0
    end = min(nxt - 0.03, max(ch[-1]["e"] + 0.6, ch[-1]["s"] + 0.35))   # never overlaps the next line
    for k, tk in enumerate(ch):
        start = max(0.0, tk["s"] - 0.04)
        if end - start < 0.08: continue
        text = " ".join(piece(x, x is tk) for x in ch)
        head = "{" + rf"\an2\q2\move({X},{Y + RISE},{X},{Y},0,220)\fad({T_IN},{T_OUT})\blur9" + "}"
        events.append(f"Dialogue: 0,{ts(start)},{ts(end)},Cap,,0,0,0,,{head}{text}")
    ch_info = {"s": round(ch[0]["s"], 3), "e": round(end, 3), "text": " ".join(shown(x["w"]) for x in ch),
               "em": [shown(x["w"]) for x in ch if x["em"]]}
    ch[0]["info"] = ch_info

hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter Medium,{FS},{WHITE},{WHITE},&H00000000&,&H00000000&,0,0,0,0,100,100,0,0,1,6,0,2,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open(f"{E}/captions.ass", "w").write(hdr + "\n".join(events) + "\n")
json.dump([ch[0]["info"] for ch in chunks], open(f"{E}/captions.json", "w"), indent=1)
print(len(tokens), "words,", len(chunks), "lines,", len(events), "events,", sum(1 for ch in chunks if any(x["em"] for x in ch)), "with emphasis")
