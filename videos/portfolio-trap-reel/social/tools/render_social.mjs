// Screenshot the story and carousel pages (social/pages/*.html) to PNG at their exact Instagram sizes.
// Serves the reel's project root over HTTP so the pages can load /assets/... (fonts need a real origin).
//   node social/tools/render_social.mjs
import { createServer } from "node:http";
import { readFile, mkdir } from "node:fs/promises";
import { extname, join, normalize, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
let playwright;
try {
  playwright = require("playwright");
} catch {
  // the cloud sandbox installs playwright globally
  playwright = require(join(process.execPath, "../../lib/node_modules/playwright"));
}

const ROOT = normalize(join(dirname(fileURLToPath(import.meta.url)), "../.."));
const TYPES = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".woff2": "font/woff2", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml" };
const JOBS = [
  ...[1, 2, 3, 4].map((n) => ({ page: `story-${n}`, w: 1080, h: 1920, out: `social/stories/story-${n}.png` })),
  ...[1, 2, 3, 4].map((n) => ({ page: `carousel-${n}`, w: 1080, h: 1350, out: `social/carousel/carousel-${n}.png` })),
];

const server = createServer(async (req, res) => {
  const path = normalize(join(ROOT, decodeURIComponent(new URL(req.url, "http://x").pathname)));
  if (!path.startsWith(ROOT)) return res.writeHead(403).end();
  try {
    const body = await readFile(path);
    res.writeHead(200, { "content-type": TYPES[extname(path)] || "application/octet-stream" }).end(body);
  } catch {
    res.writeHead(404).end();
  }
});
await new Promise((ok) => server.listen(0, "127.0.0.1", ok));
const base = `http://127.0.0.1:${server.address().port}`;

const browser = await playwright.chromium.launch();
try {
  for (const job of JOBS) {
    const page = await browser.newPage({ viewport: { width: job.w, height: job.h }, deviceScaleFactor: 1 });
    const failed = [];
    page.on("requestfailed", (r) => failed.push(r.url()));
    page.on("response", (r) => r.status() >= 400 && failed.push(`${r.status()} ${r.url()}`));
    await page.goto(`${base}/social/pages/${job.page}.html`, { waitUntil: "networkidle" });
    await page.evaluate(async () => {
      await document.fonts.ready;
      await Promise.all(Array.from(document.images).map((im) => (im.complete ? null : new Promise((r) => (im.onload = im.onerror = r)))));
    });
    const fonts = await page.evaluate(() => Array.from(document.fonts).filter((f) => f.status === "loaded").map((f) => `${f.family} ${f.weight} ${f.style}`));
    await mkdir(join(ROOT, dirname(job.out)), { recursive: true });
    await page.screenshot({ path: join(ROOT, job.out), clip: { x: 0, y: 0, width: job.w, height: job.h } });
    console.log(`${job.out} ${job.w}x${job.h}  fonts: ${fonts.length}${failed.length ? "  FAILED: " + failed.join(", ") : ""}`);
    await page.close();
  }
} finally {
  await browser.close();
  server.close();
}
