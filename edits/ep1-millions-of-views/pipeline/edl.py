# Edit decision list for "Millions of views, zero clients" (Fred, episode 1)
# (id, source, start, end, caption text) — times in source seconds
FPS = 30
CLIPS = [
    ("c1",  "A", 1.18, 2.86,  "Okay, it's a bit crazy, but"),
    ("c2",  "A", 3.02, 4.93,  "I got millions of views and zero clients."),
    ("c3",  "A", 5.90, 8.67,  "If you're new here, hi, I'm Fred. I'm a web designer."),
    ("c4",  "A", 9.52, 13.55, "You may know me from my designer versus developer videos."),
    ("c5",  "A", 14.44, 15.42, "This one got three"),
    ("c6",  "A", 15.88, 17.12, "million views."),
    ("c7",  "A", 17.21, 21.02, "So I thought, okay, this is it. Clients are gonna come to me,"),
    ("c8",  "A", 21.35, 22.00, "naturally."),
    ("c9",  "A", 23.10, 24.65, "It took me a while to get it."),
    ("c10", "A", 24.97, 26.06, "People came for the"),
    ("c11", "A", 26.32, 28.52, "joke, not for my expertise."),
    ("c13", "B", 0.72, 3.50,  "The views felt great, but they don't pay the bills."),
    ("c14", "B", 5.42, 9.13,  "So I stopped, and I started over with one goal:"),
    ("c15", "B", 9.29, 9.95,  "get a"),
    ("c16", "B", 10.25, 11.75, "real client."),
    ("c17", "B", 12.15, 15.25, "And I did. One project for seven thousand dollars."),
    ("c18", "B", 15.33, 16.65, "One single project."),
    ("c19", "B", 18.96, 19.95, "But before that,"),
    ("c20", "B", 20.12, 21.25, "I failed a lot."),
    ("c21", "B", 21.27, 24.45, "So in the next videos, I'll show you what did not work and"),
    ("c22", "B", 24.62, 25.65, "what finally did."),
    ("c23", "B", 25.75, 26.85, "Mistakes included."),
    ("c24", "B", 26.87, 29.93, "If you want to see that, stick around for my next video."),
]
# zooms: clip -> (kind, trigger word index or None, target scale)
ZOOMS = {
    "c2":  ("snap", "zero", 1.15),
    "c9":  ("slow", None, 1.12),
    "c11": ("snap", "not", 1.15),
    "c17": ("snap", "seven", 1.15),
    "c20": ("slow", None, 1.12),
}
# face anchor (fraction of frame) used as zoom centre
ANCHOR = {"A": (0.46, 0.22), "B": (0.50, 0.24)}
SRC = {"A": "rawA.mp4", "B": "rawB.mp4"}
