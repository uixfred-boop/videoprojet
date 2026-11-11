import sys, numpy as np
from scipy.io import wavfile
from faster_whisper import WhisperModel
sr,x=wavfile.read("/tmp/claude-0/-home-user-videoprojet/6386d7a0-9dfd-599c-825b-733ce7c63b86/scratchpad/ep3/raw.wav"); x=x.astype(np.float32)/32768
m=WhisperModel("medium.en",device="cpu",compute_type="int8")
for spec in sys.argv[1:]:
    a,b=map(float,spec.split("-")); seg=x[int(a*sr):int(b*sr)]
    segs,_=m.transcribe(seg,word_timestamps=True,beam_size=5,language="en",condition_on_previous_text=False)
    print(f"== {a}-{b}:", " ".join(f"{w.word.strip()}[{a+w.start:.2f}-{a+w.end:.2f}]" for s in segs for w in s.words), flush=True)
