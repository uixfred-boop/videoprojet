"""Voice-cloned narration with Chatterbox (MIT). One wav per sentence, cloned from a reference clip.
usage: clone_tts.py ref.wav out_dir [exaggeration] [cfg_weight] [only_index]"""
import sys, os, time, json
import torch, torchaudio
from chatterbox.tts import ChatterboxTTS

ref, out = sys.argv[1], sys.argv[2]
EXAG = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
CFG = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
ONLY = int(sys.argv[5]) if len(sys.argv) > 5 else None
LINES = [
    "I'm Fred, and I'm a web designer.",
    "For a long time, I made the most classic mistake on the internet: chasing views instead of chasing value.",
    "I had millions of views on Instagram.",
    "Likes.",
    "Comments like, \"Your work is so beautiful.\"",
    "And zero clients.",
    "No real projects.",
    "No system to find them.",
    "On top of that, online agencies kept rejecting me.",
    "So I wanted to prove something to myself:",
    "that I could design something good, and smart, to land a real, big client.",
]
os.makedirs(out, exist_ok=True)
torch.manual_seed(7)
model = ChatterboxTTS.from_pretrained(device="cpu")
model.prepare_conditionals(ref, exaggeration=EXAG)
meta = []
for i, text in enumerate(LINES):
    if ONLY is not None and i != ONLY: continue
    t0 = time.time()
    torch.manual_seed(100 + i)
    wav = model.generate(text, exaggeration=EXAG, cfg_weight=CFG)
    path = f"{out}/line{i:02d}.wav"
    torchaudio.save(path, wav, model.sr)
    meta.append({"i": i, "text": text, "path": path, "dur": wav.shape[-1] / model.sr})
    print(i, f"{wav.shape[-1] / model.sr:.2f}s audio in {time.time() - t0:.1f}s", flush=True)
json.dump(meta, open(f"{out}/lines.json", "w"), indent=1)
