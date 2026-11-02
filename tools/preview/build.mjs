// Local preview renderer for the Day Up Shopify theme.
// Renders the theme's Liquid with liquidjs + Shopify-like shims and the real
// Day Up product catalog snapshot (data/products.json), writing static HTML
// files to tools/preview/out/. Not used by Shopify.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Liquid, Drop } from 'liquidjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const THEME = path.resolve(__dirname, '../..');
const OUT = path.join(__dirname, 'out');
const CDN = 'https://cdn.shopify.com/s/files/1/0936/4606/1895/files/';

const read = (p) => fs.readFileSync(path.join(THEME, p), 'utf8');
const readJSON = (p) => JSON.parse(read(p));
const locale = readJSON('locales/fr.default.json');

// ---------------------------------------------------------------- drops
class ColorDrop extends Drop {
  constructor(hex) {
    super();
    this.hex = hex || '#000000';
    const h = this.hex.replace('#', '');
    this.red = parseInt(h.slice(0, 2), 16);
    this.green = parseInt(h.slice(2, 4), 16);
    this.blue = parseInt(h.slice(4, 6), 16);
  }
  valueOf() { return this.hex; }
  toString() { return this.hex; }
}
const img = (src, width = 1200, height = 1200, alt = '') => ({ src, url: src, width, height, alt, aspect_ratio: width / height, id: src });

// ---------------------------------------------------------------- data
const raw = JSON.parse(fs.readFileSync(path.join(__dirname, 'data/products.json'), 'utf8')).products;
function toProduct(p) {
  const images = p.images.map((i) => img(i.src, i.width, i.height, p.title));
  const variants = p.variants.map((v) => ({
    id: v.id, title: v.title, option1: v.option1, available: v.available,
    price: Math.round(parseFloat(v.price) * 100),
    compare_at_price: v.compare_at_price ? Math.round(parseFloat(v.compare_at_price) * 100) : null,
    featured_media: null, metafields: {}, sku: v.sku, url: `/products/${p.handle}?variant=${v.id}`
  }));
  const prices = variants.map((v) => v.price);
  return {
    id: p.id, title: p.title, handle: p.handle, url: `/products/${p.handle}`, vendor: p.vendor,
    description: p.body_html, content: p.body_html, available: true, tags: p.tags,
    images, featured_image: images[0],
    media: images.map((im, i) => ({ id: 1000 + i, media_type: 'image', preview_image: im, alt: p.title })),
    variants, first_available_variant: variants[0], selected_or_first_available_variant: variants[0], selected_variant: null,
    has_only_default_variant: variants.length === 1 && variants[0].title === 'Default Title',
    price: Math.min(...prices), price_min: Math.min(...prices), price_max: Math.max(...prices),
    compare_at_price_max: Math.max(...variants.map((v) => v.compare_at_price || 0)),
    options: p.options.map((o) => o.name), metafields: { reviews: {}, judgeme: {}, custom: {} }
  };
}
const products = Object.fromEntries(raw.map((p) => [p.handle, toProduct(p)]));
const mainProduct = products['dayup-daily-energy'];

const linklists = {
  'main-menu': { title: 'Menu principal', links: [
    { title: 'Accueil', url: '/', links: [] }, { title: 'Produit', url: '/products/dayup-daily-energy', links: [] },
    { title: 'FAQ', url: '/pages/faq', links: [] }, { title: 'Challenge', url: '/pages/challenge', links: [] },
    { title: 'À propos', url: '/pages/a-propos', links: [] }, { title: 'Contact', url: '/pages/contact', links: [] }] },
  footer: { title: 'Aide', links: [
    { title: 'Contact', url: '/pages/contact', links: [] }, { title: 'Livraison', url: '/policies/shipping-policy', links: [] },
    { title: 'Retours & remboursements', url: '/policies/refund-policy', links: [] }, { title: 'CGV', url: '/policies/terms-of-service', links: [] },
    { title: 'Mentions légales', url: '/policies/legal-notice', links: [] }] }
};

function mockCart(withItems) {
  if (!withItems) return { item_count: 0, items: [], total_price: 0, cart_level_discount_applications: [], currency: { iso_code: 'EUR' } };
  const p = mainProduct;
  const v = p.variants[0];
  const items = [{ variant_id: v.id, quantity: 1, url: v.url, image: p.images[0], title: p.title, product: p, variant: v,
    final_line_price: v.price, original_line_price: v.price, line_level_discount_allocations: [] }];
  return { item_count: 1, items, total_price: v.price, cart_level_discount_applications: [], currency: { iso_code: 'EUR' } };
}

// ---------------------------------------------------------------- settings resolution
function resolveValue(type, val) {
  if (val === undefined || val === null || val === '') return val;
  switch (type) {
    case 'product': return products[val] || null;
    case 'collection': return null;
    case 'link_list': return linklists[val] || null;
    case 'image_picker': {
      const m = String(val).match(/^shopify:\/\/shop_images\/(.+)$/);
      return m ? img(CDN + m[1], 1200, 1600, '') : null;
    }
    case 'color': return new ColorDrop(val);
    default: return val;
  }
}
function resolveSettings(schemaSettings = [], values = {}) {
  const out = {};
  for (const s of schemaSettings) {
    if (!s.id) continue;
    const v = Object.prototype.hasOwnProperty.call(values, s.id) ? values[s.id] : s.default;
    out[s.id] = resolveValue(s.type, v);
  }
  return out;
}
const themeSchema = readJSON('config/settings_schema.json');
const themeSettingDefs = themeSchema.flatMap((g) => g.settings || []);
const themeData = readJSON('config/settings_data.json').current;
const settings = resolveSettings(themeSettingDefs, themeData);

function sectionSource(type) { return read(`sections/${type}.liquid`); }
function sectionSchema(type) {
  const m = sectionSource(type).match(/\{%-?\s*schema\s*-?%\}([\s\S]*?)\{%-?\s*endschema\s*-?%\}/);
  return m ? JSON.parse(m[1]) : { settings: [] };
}
function buildSection(id, type, data = {}) {
  const schema = sectionSchema(type);
  const blocksDef = Object.fromEntries((schema.blocks || []).map((b) => [b.type, b]));
  const order = data.block_order || Object.keys(data.blocks || {});
  const blocks = order.map((bid) => {
    const b = data.blocks[bid];
    return { id: bid, type: b.type, settings: resolveSettings((blocksDef[b.type] || {}).settings, b.settings || {}), shopify_attributes: '' };
  });
  return { schema, section: { id, type, settings: resolveSettings(schema.settings, data.settings || {}), blocks } };
}

// ---------------------------------------------------------------- engine
const stripSchema = (src) => src
  .replace(/\{%-?\s*schema\s*-?%\}[\s\S]*?\{%-?\s*endschema\s*-?%\}/g, '')
  .replace(/posted_successfully\?/g, 'posted_successfully');

const engine = new Liquid({
  root: [path.join(THEME, 'snippets')],
  extname: '.liquid',
  dynamicPartials: true,
  strictFilters: false,
  strictVariables: false,
  lenientIf: true,
  relativeReference: false,
  fs: {
    readFileSync: (f) => stripSchema(fs.readFileSync(f, 'utf8')),
    readFile: async (f) => stripSchema(fs.readFileSync(f, 'utf8')),
    existsSync: (f) => fs.existsSync(f),
    exists: async (f) => fs.existsSync(f),
    resolve: (root, file, ext) => path.resolve(root, file.endsWith(ext) ? file : file + ext),
    contains: () => true,
    sep: path.sep
  }
});

// keyword args helper: liquidjs passes `key: value` args as [key, value] arrays
function kw(args) {
  const o = {};
  for (const a of args) if (Array.isArray(a) && a.length === 2) o[a[0]] = a[1];
  return o;
}
const money = (c) => {
  const n = Number(c || 0) / 100;
  return '€' + n.toFixed(2).replace('.', ',');
};
function srcOf(v) { return typeof v === 'string' ? v : v && (v.src || v.url) || ''; }
function withWidth(url, w) { if (!url || !w) return url; return url + (url.includes('?') ? '&' : '?') + 'width=' + w; }

engine.registerFilter('asset_url', (n) => `/assets/${n}`);
engine.registerFilter('shopify_asset_url', (n) => `/assets/${n}`);
engine.registerFilter('preload_tag', (u, ...args) => { const o = kw(args); return `<link rel="preload" href="${u}"${Object.entries(o).map(([k, v]) => ` ${k}="${v}"`).join('')}>`; });
engine.registerFilter('stylesheet_tag', (u) => `<link rel="stylesheet" href="${u}">`);
engine.registerFilter('script_tag', (u) => `<script src="${u}" defer></script>`);
engine.registerFilter('image_url', (v, ...args) => {
  const o = kw(args);
  const base = srcOf(v);
  if (!base) return '';
  const u = withWidth(base, o.width);
  return { __img: true, url: u, base, width: o.width, alt: v && v.alt, toString() { return u; }, valueOf() { return u; } };
});
engine.registerFilter('img_url', (v) => srcOf(v));
engine.registerFilter('image_tag', (v, ...args) => {
  const o = kw(args);
  const base = v && v.base ? v.base : srcOf(v);
  const src = v && v.url ? v.url : base;
  const widths = String(o.widths || '').split(',').map((s) => s.trim()).filter(Boolean);
  const srcset = widths.length ? ` srcset="${widths.map((w) => `${withWidth(base, w)} ${w}w`).join(', ')}"` : '';
  const attrs = ['class', 'loading', 'sizes', 'style'].filter((k) => o[k]).map((k) => ` ${k}="${o[k]}"`).join('');
  return `<img src="${src}"${srcset}${attrs} alt="${(o.alt ?? (v && v.alt) ?? '').toString().replace(/"/g, '&quot;')}">`;
});
engine.registerFilter('money', money);
engine.registerFilter('money_with_currency', (c) => money(c) + ' EUR');
engine.registerFilter('money_without_currency', (c) => (Number(c || 0) / 100).toFixed(2).replace('.', ','));
engine.registerFilter('money_without_trailing_zeros', (c) => money(c).replace(/,00$/, ''));
engine.registerFilter('t', (key, ...args) => {
  const o = kw(args);
  let s = String(key).split('.').reduce((acc, k) => (acc ? acc[k] : undefined), locale);
  if (s === undefined) return `translation missing: ${key}`;
  return s.replace(/\{\{\s*(\w+)\s*\}\}/g, (_, k) => (o[k] ?? ''));
});
engine.registerFilter('handleize', (s) => String(s ?? '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''));
engine.registerFilter('handle', (s) => String(s ?? '').toLowerCase().replace(/[^a-z0-9]+/g, '-'));
function adjustColor(hex, amt) {
  const h = String(hex).replace('#', '');
  let r = parseInt(h.slice(0, 2), 16) / 255, g = parseInt(h.slice(2, 4), 16) / 255, b = parseInt(h.slice(4, 6), 16) / 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  let hh = 0, s = 0, l = (max + min) / 2;
  if (max !== min) {
    const d = max - min; s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    hh = max === r ? (g - b) / d + (g < b ? 6 : 0) : max === g ? (b - r) / d + 2 : (r - g) / d + 4; hh /= 6;
  }
  l = Math.min(1, Math.max(0, l + amt / 100));
  const f = (p, q, t) => { if (t < 0) t += 1; if (t > 1) t -= 1; if (t < 1 / 6) return p + (q - p) * 6 * t; if (t < 1 / 2) return q; if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6; return p; };
  let rr, gg, bb;
  if (s === 0) { rr = gg = bb = l; } else { const q = l < 0.5 ? l * (1 + s) : l + s - l * s; const p = 2 * l - q; rr = f(p, q, hh + 1 / 3); gg = f(p, q, hh); bb = f(p, q, hh - 1 / 3); }
  return '#' + [rr, gg, bb].map((x) => Math.round(x * 255).toString(16).padStart(2, '0')).join('');
}
engine.registerFilter('color_lighten', (c, a) => adjustColor(String(c), Number(a)));
engine.registerFilter('color_darken', (c, a) => adjustColor(String(c), -Number(a)));
for (const f of ['structured_data', 'default_pagination', 'default_errors', 'video_tag', 'external_video_tag', 'placeholder_svg_tag', 'format_address', 'payment_type_svg_tag'])
  engine.registerFilter(f, () => '');
engine.registerFilter('format_code', (s) => s);
engine.registerFilter('link_to', (t, u) => `<a href="${u}">${t}</a>`);

// ----- tags
const ignoreBlock = (name) => ({
  parse(token, remain) {
    this.tpls = [];
    const stream = this.liquid.parser.parseStream(remain);
    stream.on(`tag:end${name}`, () => stream.stop()).on('template', () => {}).on('end', () => { throw new Error(`${name} not closed`); });
    stream.start();
  },
  * render() {}
});
engine.registerTag('stylesheet', ignoreBlock('stylesheet'));
engine.registerTag('javascript', ignoreBlock('javascript'));
engine.registerTag('layout', { parse() {}, * render() {} });

function splitArgs(str) {
  const out = []; let cur = ''; let q = null;
  for (const ch of str) {
    if (q) { cur += ch; if (ch === q) q = null; continue; }
    if (ch === '"' || ch === "'") { q = ch; cur += ch; continue; }
    if (ch === ',') { out.push(cur.trim()); cur = ''; continue; }
    cur += ch;
  }
  if (cur.trim()) out.push(cur.trim());
  return out;
}
engine.registerTag('form', {
  parse(token, remain) {
    this.args = token.args;
    this.tpls = [];
    const stream = this.liquid.parser.parseStream(remain);
    stream.on('tag:endform', () => stream.stop()).on('template', (t) => this.tpls.push(t)).on('end', () => { throw new Error('form not closed'); });
    stream.start();
  },
  * render(ctx, emitter) {
    const parts = splitArgs(this.args);
    const type = parts.shift().replace(/['"]/g, '');
    const attrs = {};
    for (const p of parts) {
      const m = p.match(/^([\w-]+)\s*:\s*(.+)$/);
      if (m) attrs[m[1]] = this.liquid.evalValueSync(m[2], ctx);
    }
    const actions = { product: '/cart/add', customer: '/contact#newsletter', contact: '/contact' };
    ctx.push({ form: { posted_successfully: false, errors: null } });
    const html = yield this.liquid.renderer.renderTemplates(this.tpls, ctx);
    ctx.pop();
    const attrStr = Object.entries(attrs).map(([k, v]) => ` ${k}="${v}"`).join('');
    emitter.write(`<form method="post" action="${actions[type] || '/'}" accept-charset="UTF-8"${attrStr}><input type="hidden" name="form_type" value="${type}">${html}</form>`);
  }
});
engine.registerTag('paginate', {
  parse(token, remain) {
    this.tpls = [];
    const stream = this.liquid.parser.parseStream(remain);
    stream.on('tag:endpaginate', () => stream.stop()).on('template', (t) => this.tpls.push(t)).on('end', () => { throw new Error('paginate not closed'); });
    stream.start();
  },
  * render(ctx, emitter) {
    ctx.push({ paginate: { pages: 1 } });
    emitter.write(yield this.liquid.renderer.renderTemplates(this.tpls, ctx));
    ctx.pop();
  }
});

let GLOBALS = {};
async function renderSectionHTML(id, type, data, wrapperId, extraClass = '') {
  const { schema, section } = buildSection(id, type, data);
  const html = await engine.parseAndRender(stripSchema(sectionSource(type)), { ...GLOBALS, section });
  return `<div id="${wrapperId}" class="shopify-section ${extraClass} ${schema.class || ''}">${html}</div>`;
}
engine.registerTag('section', {
  parse(token) { this.name = token.args.replace(/['"]/g, '').trim(); },
  * render(ctx, emitter) {
    const data = (themeData.sections || {})[this.name] || { settings: {} };
    emitter.write(yield renderSectionHTML(this.name, this.name, data, `shopify-section-${this.name}`));
  }
});
engine.registerTag('sections', {
  parse(token) { this.name = token.args.replace(/['"]/g, '').trim(); },
  * render(ctx, emitter) {
    const group = readJSON(`sections/${this.name}.json`);
    let out = '';
    for (const key of group.order) {
      const s = group.sections[key];
      out += yield renderSectionHTML(`sections--${this.name}__${key}`, s.type, s, `shopify-section-sections--${this.name}__${key}`, `shopify-section-group-${this.name}`);
    }
    emitter.write(out);
  }
});

// ---------------------------------------------------------------- pages
async function renderPage({ template, out, product = null, cartItems = false, pageType = 'index', title = 'DayUp', inject = '' }) {
  const tpl = readJSON(`templates/${template}.json`);
  const templateName = template.split('.')[0];
  GLOBALS = {
    settings, shop: { name: 'DayUp', url: 'https://dayup-shop.com', money_format: '€{{amount_with_comma_separator}}', description: '',
      policies: [{ title: 'Politique de remboursement', url: '/policies/refund-policy' }, { title: 'Politique de confidentialité', url: '/policies/privacy-policy' },
        { title: "Conditions d'utilisation", url: '/policies/terms-of-service' }, { title: "Politique d'expédition", url: '/policies/shipping-policy' }],
      enabled_payment_types: [] },
    routes: { root_url: '/', cart_url: '/cart', cart_add_url: '/cart/add', cart_change_url: '/cart/change', cart_update_url: '/cart/update', all_products_collection_url: '/collections/all', search_url: '/search', account_url: '/account' },
    request: { locale: { iso_code: 'fr' }, page_type: pageType, design_mode: false, origin: 'https://dayup-shop.com' },
    template: { name: templateName, suffix: template.includes('.') ? template.split('.')[1] : null },
    product, cart: mockCart(cartItems), linklists, all_products: products,
    page_title: title, canonical_url: 'https://dayup-shop.com/', content_for_header: '', current_page: 1
  };
  engine.options.globals = GLOBALS; // Shopify globals are visible inside {% render %} snippets
  let content = '';
  for (const key of tpl.order) {
    const s = tpl.sections[key];
    if (s.disabled) continue;
    content += await renderSectionHTML(`template--${template}__${key}`, s.type, s, `shopify-section-template--${template}__${key}`);
  }
  const layout = stripSchema(read('layout/theme.liquid'));
  let html = await engine.parseAndRender(layout, { ...GLOBALS, content_for_layout: content });
  if (inject) html = html.replace('</body>', inject + '</body>');
  fs.writeFileSync(path.join(OUT, out), html);
  return html;
}

fs.mkdirSync(OUT, { recursive: true });
const t0 = Date.now();
await renderPage({ template: 'index', out: 'index.html', title: 'DayUp – Ton énergie du matin en 2 gummies' });
await renderPage({ template: 'product', out: 'product.html', product: mainProduct, pageType: 'product', title: mainProduct.title });
await renderPage({ template: 'page.faq', out: 'faq.html', pageType: 'page', title: 'FAQ' });
await renderPage({ template: 'index', out: 'cart.html', cartItems: true, inject: '<script>addEventListener("load",()=>setTimeout(()=>document.querySelector("[data-cart-open]").click(),300))</script>' });
await renderPage({ template: 'index', out: 'cart-empty.html', inject: '<script>addEventListener("load",()=>setTimeout(()=>document.querySelector("[data-cart-open]").click(),300))</script>' });
await renderPage({ template: 'index', out: 'menu.html', inject: '<script>addEventListener("load",()=>setTimeout(()=>document.querySelector("[data-menu-open]").click(),300))</script>' });
await renderPage({ template: '404', out: '404.html', pageType: '404', title: '404' });
console.log(`preview built in ${Date.now() - t0}ms → ${OUT}`);
