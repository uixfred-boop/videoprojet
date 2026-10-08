#!/usr/bin/env python3
"""Force-align a known script to a voice-over and write word timings (HyperFrames transcript.json shape).

Whisper can't download its model in the cloud sandbox, but PocketSphinx ships its English model inside the wheel:
    python3 -m venv .venv && .venv/bin/pip install pocketsphinx
    .venv/bin/python tools/align_vo.py voiceover.mp3 script.txt transcript.json

script.txt must contain the words as SPOKEN (write "7000$" as "seven thousand dollars"). Words missing from the
dictionary need a pronunciation in EXTRA below (ARPAbet), or the alignment fails.
"""
import json
import os
import re
import subprocess
import sys

from pocketsphinx import Decoder, get_model_path

EXTRA = {
    "fiverr": "F AY V ER",
    "upwork": "AH P W ER K",
    "dms": "D IY EH M Z",
    "shopify": "SH AA P IH F AY",
    "monetize": "M AA N AH T AY Z",
    "spamming": "S P AE M IH NG",
    "instagram": "IH N S T AH G R AE M",
    "unfiltered": "AH N F IH L T ER D",
}


def main(audio, script, out):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", audio, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
        capture_output=True, check=True,
    ).stdout
    words = re.findall(r"[a-z']+", open(script).read().lower())
    dict_path = os.path.join(get_model_path(), "en-us", "cmudict-en-us.dict")
    known = {line.split()[0] for line in open(dict_path)}
    d = Decoder(samprate=16000, bestpath=False, beam=1e-80, wbeam=1e-60, pbeam=1e-80)
    for w in sorted(set(words) - known):
        if w not in EXTRA:
            sys.exit(f"no pronunciation for '{w}': add it to EXTRA")
        d.add_word(w, EXTRA[w], update=True)
    d.set_align_text(" ".join(words))
    d.start_utt()
    d.process_raw(raw, full_utt=True)
    d.end_utt()
    result = [
        {"text": re.sub(r"\(\d\)$", "", s.word), "start": round(s.start_frame / 100, 3), "end": round((s.end_frame + 1) / 100, 3)}
        for s in d.seg()
        if s.word not in ("<sil>", "<s>", "</s>")
    ]
    json.dump(result, open(out, "w"), indent=1)
    print(f"{len(result)} words → {out} (first {result[0]}, last {result[-1]})")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
