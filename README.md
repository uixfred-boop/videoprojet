# Portfolio

A static portfolio site (HTML / CSS / JS) that reproduces the structure, copy and animations of [itsjay.us](https://www.itsjay.us/), **without the "Lab" page**.
Animations: GSAP + ScrollTrigger. Smooth scroll: Lenis. Both are bundled in `assets/vendor`, so nothing needs installing.

## Pages

| File | Content |
| --- | --- |
| `index.html` | 0→100 loader, "A seriously good Design Engineer" hero, showreel that follows the mouse and grows on scroll, "Myself", two featured projects, services, "Modern Tech Stack" with logos, footer tiles |
| `work.html` | "Selected Work": every project as a card |
| `project.html#<slug>` | Case study: title, year, services, summary, image / video gallery |

Every page has the info header with the "Get in touch" button, the floating bottom dock (Home / Work menu) and the footer.

## Editing the content

Everything lives in **`assets/js/data.js`**:

- `SITE`: name, domain, email, header info, scrolling roles, hero text, showreel, "Myself", services, tools, socials.
- `PROJECTS`: the list of projects (the first two are featured on the home page).

Each project has a `slug` (used in the URL), `title`, `category`, `year`, `colors` (placeholder gradient), `tags` (text scrolling on the card), `services`, `summary`, `cover` (card image), `preview` (video shown when hovering the card) and `gallery`.

Put media in `assets/media/`, for example:

```js
cover: { type: "image", src: "assets/media/project-one/cover.jpg" },
preview: { type: "video", src: "assets/media/project-one/preview.mp4" },
gallery: [
  { type: "video", src: "assets/media/project-one/film.mp4", poster: "assets/media/project-one/poster.jpg" }, // full width
  [ { type: "image", src: "assets/media/project-one/01.jpg" }, { type: "image", src: "assets/media/project-one/02.jpg" } ], // two columns
],
```

Any media without a `src` shows a gradient in the project's colours instead.

Tool logos are the SVG files in `assets/icons/` (from [simple-icons](https://simpleicons.org), CC0). Video tools are already included (Premiere Pro, After Effects, DaVinci Resolve, Blender, Cinema 4D, Photoshop, Illustrator): add their file name to `SITE.stack` to use them.

## Fonts

The original site uses **Saans** (Displaay Type Foundry) and **LCDDot**.

- **LCDDot** is bundled in `assets/fonts` (CC BY-SA 3.0). Its character table was repaired so browsers accept it.
- **Saans** is a commercial font and is not bundled. Once you have a license, add the four `.woff2` files to `assets/fonts` with the names listed in `assets/fonts/README.md` and the site uses them automatically. Until then it falls back to Inter Tight (Google Fonts).

## Running locally

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```
