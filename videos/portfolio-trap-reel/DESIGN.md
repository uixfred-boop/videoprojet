# Design

The design truth is `../../styles/lockin-red/STYLE.md`. Palette, type, components and motion all come from there. The
reusable CSS is `assets/css/lockin.css`, copied to `../../styles/lockin-red/components.css` as the canonical file.

The layout is the house split layout of `../web-design-7k-reel/DESIGN.md`, the same grid as the reference:

- graphics in y ≈ 100–1180;
- one-word captions on the seam, centred on y ≈ 1285;
- the footage card at x 72–1008 from y 1408, with the head popping out above its top edge;
- full-screen cutaways, with bigger one-word captions at the same height.

## Look

- Pure black `#000` with a dot grid (2px dots every 17px, `#2A2A2A`). No aura, no vignette.
- **Pure red `#B80000`:**
  - title bars, the underline, row and breadcrumb edges, bullets and ping circles;
  - deep red `#96050F` for small tags;
  - a red gradient (`#C40000` → `#7A0000`) for big buttons.
- **Other colours:**
  - Yellow `#ECE512`: highlight lines in the template document.
  - Green `#18DE3A`: the "result" confirm flash only.
- **Type:** Inter Tight 800 (the reference's heavy grotesk) and Instrument Serif Italic (the coined term, the CTA
  keyword, document headings).

## What this reel uses from the reference

- **Hub title:** line 1 white, line 2 white on a red bar that grows with the typing. Typing is fast (≈ 0.55s per title)
  and re-runs after every cut.
- **Numbered list:** three glass rows with a red edge.
  - The labels stay blurred until their item is spoken.
  - The active row keeps its bar and gets a white sheen; the others drop their bars.
- **Breadcrumb bar:** a wide glass bar with a red edge, a big number and the item name. It heads each explanation.
- **Portfolio card:** a `--panel` card with a beautiful mock site (the hook, and mistake 3).
  - On the pain word it tints red and a red "0 messages" pill appears, then a ping lands.
- **Project vs Result cards:** white screenshot-style cards with a red glow border and medium tags, sliding in from the
  sides. The result card carries an up-trend with no figures.
- **Label boxes:** the client's voice ("What's In It For Me?", "What Do I Do Now?") and the bio "Versatile Creative".
- **Template document:** like the reference's "Video Script".
  - A serif italic heading and three bullet rows (Results / Clear Offer / Next Step).
  - They draw in red, yellow and red on "solves these three points".
- **Big red buttons:** "Step-By-Step", "Join The Waitlist". A dashed empty button outline stands for "zero clear button".
- **Ping circle:** a translucent red disc that grows and fades on the focal word.
- **CTA page grid:** template pages in a 3x2 grid with a slow push-in.

## Rules kept from the reference

- Dark from start to finish. Red is the only accent; yellow and green are used once each.
- Captions are one word at a time with hard swaps and no animation. Only the coined term and the CTA keyword switch to
  serif italic.
- Hard cuts on the word, and slow push-ins on the focal panel.
- **SFX:**
  - a low whoosh starting about 0.2s before each graphic scene change;
  - soft pops on tags and buttons;
  - no typing ticks;
  - all about 20 dB under the voice.
- **No music:** the user adds their own.
