# Design

The design truth is the repo's default style: `../../styles/listicle-crimson/STYLE.md`. Palette, type,
components and motion all come from there; the shared CSS is `assets/css/components.css` (a copy of the canonical
file) plus `assets/css/house.css`. Layout follows the split layout of `../web-design-7k-reel/DESIGN.md`:

- graphics in y ≈ 160–1180;
- captions on the seam (one line centred on y ≈ 1277);
- the footage card at x 72–1008 from y 1408, with the head popping out above its top edge;
- full-screen cutaways, with the caption on the chest.

## What this reel adds

- **Browser panel with footage:** a glass window with crimson edge and the 3-dot bar (`.gl.crim` + `.bar3`), with
  `screen.mp4` playing inside, cropped 16:9. Used for the clean portfolio and for Perry Wang's hero.
- **Floating window collage:** smaller browser windows (`.bw`) tilting around the hub's crimson ball, each playing a
  different busy site. When the voice says "way too much", more windows pile in, chips swarm, everything shakes.
- **Timer ring:** a crimson SVG ring that draws over the words "in five seconds", with "5s" in serif italic in the
  middle.
- **Who / What callouts:** crimson tags (`.lc-tag`) wired with `.lc-wire` curves to the two lines of the portfolio
  hero that answer them, each ending on the yellow node.
- **Strike:** a crimson bar with glow that wipes across a word or an over-animated mock-up ("WOW", the opening
  clutter).
- **Wireframe rebuild:** dashed outline blocks of a page that fill in one by one (hero, what I do, work, contact).

## Rules kept from the style

- Dark from start to finish, crimson `#99122B` as the only accent, the yellow node used once per scene at most.
- Headlines ghost-type while the voice says them; hard cuts on the word; no wipes between scenes.
- Labels that aren't real data are blurred placeholder bars.
- Soft UI SFX only (pop, click, whoosh, typing ticks), no impacts. No music: the user adds their own.
