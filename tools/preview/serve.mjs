// Tiny static server for the preview: /assets/* from the theme, everything else from out/.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const THEME = path.resolve(__dirname, '../..');
const OUT = path.join(__dirname, 'out');
const PORT = Number(process.env.PORT || 4321);
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.woff2': 'font/woff2', '.svg': 'image/svg+xml', '.png': 'image/png', '.json': 'application/json' };

http.createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  let file;
  if (url.pathname.startsWith('/assets/')) file = path.join(THEME, url.pathname);
  else if (url.pathname === '/' ) file = path.join(OUT, 'index.html');
  else if (url.pathname.startsWith('/products/')) file = path.join(OUT, 'product.html');
  else if (url.pathname === '/pages/faq') file = path.join(OUT, 'faq.html');
  else file = path.join(OUT, url.pathname.replace(/^\//, '') + (path.extname(url.pathname) ? '' : '.html'));
  if (url.pathname === '/cart.js') { res.writeHead(200, { 'Content-Type': 'application/json' }); return res.end('{"item_count":0}'); }
  fs.readFile(file, (err, buf) => {
    if (err) { res.writeHead(404); return res.end('not found'); }
    res.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'application/octet-stream' });
    res.end(buf);
  });
}).listen(PORT, () => console.log(`preview on http://localhost:${PORT}`));
