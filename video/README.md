# Demo video

`First-Client-Playbook-Interactive-Demo.mp4`: 1920×1080, 30 fps, about 5 minutes, silent with on-screen captions.

To re-record after changing the ebook:

```sh
python3 -m http.server 8123 --bind 127.0.0.1   # from the repo root
node video/record.js http://127.0.0.1:8123/index.html /tmp/frames
python3 video/encode.py /tmp/frames video/First-Client-Playbook-Interactive-Demo.mp4
```

`record.js` drives the page with Playwright (cursor, typing, captions, title and outro cards) and captures frames with Chrome's screencast; `encode.py` turns them into an H.264 MP4 with ffmpeg.
