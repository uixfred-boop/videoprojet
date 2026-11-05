# Edit decision list, episode 2 (YouTube 16:9): "This portfolio got me a $7,000 client"
# (id, source, start, end, caption text) — times in source seconds; pauses removed
FPS = 30
CLIPS = [
    ("k1",  "A", 0.09, 3.02,  "This portfolio got me $7,000 from one single client."),
    ("k2",  "A", 3.10, 3.71,  "But"),
    ("k3",  "A", 3.99, 6.62,  "on the call, the client asked me one question:"),
    ("k4",  "A", 7.12, 8.35,  "\"Have you"),
    ("k5",  "A", 9.20, 11.74, "ever done a project like mine?\""),
    ("k6",  "A", 12.07, 15.40, "And honestly, the answer was... no."),
    ("k7",  "A", 15.76, 20.38, "In this video, I'll show you how I built this site, how I got it"),
    ("k8",  "A", 21.28, 22.47, "in front of the right clients..."),
    ("k9",  "A", 22.54, 26.33, "and what I said to that question. Because that answer"),
    ("k10", "A", 26.58, 27.26, "is what"),
    ("k11", "A", 27.42, 28.36, "closed the deal."),
]
ZOOMS = {
    "k1":  ("snap", "$7,000", 1.12),
    "k6":  ("slow", None, 1.10),
    "k11": ("snap", "closed", 1.15),
}
ANCHOR = {"A": (0.50, 0.38)}
SRC = {"A": "comp.mp4"}
