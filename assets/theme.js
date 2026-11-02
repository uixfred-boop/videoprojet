/* Day Up theme — vanilla JS, no dependencies */
(() => {
  'use strict';

  const DU = window.DayUp || { routes: {}, strings: {} };
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const routes = Object.assign({ root: '/', cart: '/cart', cartAdd: '/cart/add', cartChange: '/cart/change' }, DU.routes);

  /* ---------- Toast ---------- */
  const toastEl = $('[data-toast]');
  let toastTimer;
  function toast(msg) {
    if (!toastEl || !msg) return;
    toastEl.textContent = msg;
    toastEl.hidden = false;
    requestAnimationFrame(() => toastEl.classList.add('is-visible'));
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toastEl.classList.remove('is-visible');
      setTimeout(() => { toastEl.hidden = true; }, 300);
    }, 2600);
  }

  /* ---------- Drawers (cart + menu) ---------- */
  // The menu drawer lives in the header section, which is sticky (own stacking context).
  // Move it to <body> so it can sit above the page overlay.
  const menuDrawer = document.getElementById('MenuDrawer');
  if (menuDrawer && menuDrawer.parentElement !== document.body) document.body.appendChild(menuDrawer);
  const overlay = $('[data-overlay]');
  let openDrawer = null;
  let lastFocus = null;

  function showDrawer(name) {
    const drawer = $(`[data-drawer="${name}"]`);
    if (!drawer) return false;
    if (openDrawer && openDrawer !== drawer) hideDrawer(true);
    lastFocus = document.activeElement;
    drawer.classList.add('is-open');
    drawer.setAttribute('aria-hidden', 'false');
    if (overlay) { overlay.hidden = false; requestAnimationFrame(() => overlay.classList.add('is-visible')); }
    document.body.classList.add('is-locked');
    $$('[data-menu-open]').forEach((b) => b.setAttribute('aria-expanded', name === 'menu' ? 'true' : 'false'));
    openDrawer = drawer;
    setTimeout(() => { (drawer.querySelector('[data-drawer-close]') || drawer).focus({ preventScroll: true }); }, 50);
    return true;
  }
  function hideDrawer(keepOverlay) {
    if (!openDrawer) return;
    openDrawer.classList.remove('is-open');
    openDrawer.setAttribute('aria-hidden', 'true');
    $$('[data-menu-open]').forEach((b) => b.setAttribute('aria-expanded', 'false'));
    openDrawer = null;
    if (!keepOverlay) {
      document.body.classList.remove('is-locked');
      if (overlay) { overlay.classList.remove('is-visible'); setTimeout(() => { if (!openDrawer) overlay.hidden = true; }, 300); }
      if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    }
  }

  document.addEventListener('click', (e) => {
    const cartBtn = e.target.closest('[data-cart-open]');
    if (cartBtn) { if (showDrawer('cart')) e.preventDefault(); return; }
    if (e.target.closest('[data-menu-open]')) { showDrawer('menu'); return; }
    if (e.target.closest('[data-drawer-close]') || e.target === overlay) { hideDrawer(); return; }
    const menuLink = e.target.closest('.drawer--menu a[href^="#"]');
    if (menuLink) hideDrawer();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && openDrawer) hideDrawer();
    if (e.key === 'Tab' && openDrawer) {
      const f = $$('a[href], button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])', openDrawer).filter((el) => el.offsetParent !== null);
      if (!f.length) return;
      const first = f[0];
      const last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { last.focus(); e.preventDefault(); }
      else if (!e.shiftKey && document.activeElement === last) { first.focus(); e.preventDefault(); }
    }
  });

  /* ---------- Cart (AJAX + Section Rendering API) ---------- */
  const CART_SECTION = 'cart-drawer';

  function renderCart(sections) {
    if (!sections || !sections[CART_SECTION]) return;
    const doc = new DOMParser().parseFromString(sections[CART_SECTION], 'text/html');
    const fresh = doc.querySelector('[data-cart-root]');
    const current = $('[data-cart-root]');
    if (fresh && current) current.innerHTML = fresh.innerHTML;
  }
  function updateCount(count) {
    $$('[data-cart-count]').forEach((el) => { el.textContent = count; el.hidden = count === 0; });
  }
  async function refreshCount() {
    try {
      const res = await fetch(`${routes.cart}.js`, { headers: { Accept: 'application/json' } });
      const cart = await res.json();
      updateCount(cart.item_count);
    } catch (e) { /* ignore */ }
  }

  async function addToCart(form, button) {
    const body = new FormData(form);
    body.append('sections', CART_SECTION);
    body.append('sections_url', window.location.pathname);
    if (button) button.classList.add('is-loading');
    try {
      const res = await fetch(`${routes.cartAdd}.js`, { method: 'POST', body, headers: { Accept: 'application/json', 'X-Requested-With': 'XMLHttpRequest' } });
      const data = await res.json();
      if (!res.ok || data.status) throw new Error(data.description || data.message || DU.strings.error);
      renderCart(data.sections);
      await refreshCount();
      if (!showDrawer('cart')) toast(DU.strings.added);
    } catch (err) {
      toast(err.message || DU.strings.error);
    } finally {
      if (button) button.classList.remove('is-loading');
    }
  }

  async function changeLine(line, quantity) {
    const root = $('[data-cart-root]');
    if (root) root.style.opacity = '.6';
    try {
      const res = await fetch(`${routes.cartChange}.js`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ line, quantity, sections: [CART_SECTION], sections_url: window.location.pathname })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.description || DU.strings.error);
      renderCart(data.sections);
      updateCount(data.item_count);
    } catch (err) {
      toast(err.message || DU.strings.error);
    } finally {
      const r = $('[data-cart-root]');
      if (r) r.style.opacity = '';
    }
  }

  document.addEventListener('submit', (e) => {
    const form = e.target.closest('form[data-add-to-cart]');
    if (!form) return;
    e.preventDefault();
    const btn = e.submitter || form.querySelector('[type="submit"]');
    addToCart(form, btn);
  });
  // Buttons outside the form (sticky bar) with form="..." also trigger submit events on the form above.

  document.addEventListener('click', (e) => {
    const q = e.target.closest('.qty [data-qty]');
    if (q) { changeLine(Number(q.closest('[data-line]').dataset.line), Number(q.dataset.qty)); return; }
    const rm = e.target.closest('[data-qty-remove]');
    if (rm) changeLine(Number(rm.dataset.line), 0);
  });

  /* ---------- Announcement rotator ---------- */
  function initRotators(scope) {
    $$('[data-rotator]', scope).forEach((root) => {
      const items = $$('[data-rotator-item]', root);
      if (items.length < 2 || reduceMotion || root.dataset.ready) return;
      root.dataset.ready = '1';
      let i = 0;
      const timer = setInterval(() => {
        if (!root.isConnected) { clearInterval(timer); return; }
        items[i].classList.remove('is-active');
        i = (i + 1) % items.length;
        items[i].classList.add('is-active');
      }, Number(root.dataset.interval) || 5000);
    });
  }

  /* ---------- Header state ---------- */
  const onHeaderScroll = () => { const h = $('[data-header]'); if (h) h.classList.toggle('is-scrolled', window.scrollY > 40); };
  onHeaderScroll();
  window.addEventListener('scroll', onHeaderScroll, { passive: true });

  /* ---------- Buy box: variant cards, price, gallery ---------- */
  function initBuyboxes(scope) {
  $$('[data-buybox]', scope).forEach((box) => {
    if (box.dataset.ready) return;
    box.dataset.ready = '1';
    const section = box.closest('.shopify-section') || document;
    const input = $('[data-variant-input]', box);
    const submit = $('[data-submit]', box);
    const priceEl = $('[data-submit-price]', box);
    const labelEl = $('[data-submit-label]', box);
    const stickyPrice = $('[data-sticky-price]', section);
    const track = $('[data-gallery-track]', box);
    const thumbs = $$('[data-thumb]', box);
    const dots = $$('.gallery__dot', box);

    function goTo(index, smooth = true) {
      if (!track) return;
      const slide = track.children[index];
      if (!slide) return;
      track.scrollTo({ left: slide.offsetLeft, behavior: smooth && !reduceMotion ? 'smooth' : 'auto' });
      setActive(index);
    }
    function setActive(index) {
      thumbs.forEach((t, i) => t.classList.toggle('is-active', i === index));
      dots.forEach((d, i) => d.classList.toggle('is-active', i === index));
    }
    thumbs.forEach((t) => t.addEventListener('click', () => goTo(Number(t.dataset.thumb))));
    if (track) {
      let raf;
      track.addEventListener('scroll', () => {
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(() => setActive(Math.round(track.scrollLeft / track.clientWidth)));
      }, { passive: true });
    }

    $$('[data-variant]', box).forEach((radio) => {
      radio.addEventListener('change', () => {
        if (!radio.checked) return;
        if (input) input.value = radio.value;
        if (priceEl) priceEl.textContent = `· ${radio.dataset.price}`;
        if (stickyPrice) stickyPrice.textContent = radio.dataset.price;
        if (submit) submit.disabled = radio.disabled;
        if (labelEl && labelEl.dataset.label) labelEl.textContent = labelEl.dataset.label;
        if (radio.dataset.mediaId && track) {
          const idx = Array.from(track.children).findIndex((s) => s.dataset.mediaId === radio.dataset.mediaId);
          if (idx > -1) goTo(idx);
        }
        if (box.closest('.product-section--main')) {
          const url = new URL(window.location.href);
          url.searchParams.set('variant', radio.value);
          window.history.replaceState({}, '', url.toString());
        }
      });
    });

    // Sticky add-to-cart bar: visible once the main button has scrolled out of view.
    const sticky = $('[data-sticky-atc]', section);
    if (sticky && submit && 'IntersectionObserver' in window) {
      sticky.hidden = false;
      let boxVisible = false;
      let btnVisible = true;
      const update = () => sticky.classList.toggle('is-visible', boxVisible && !btnVisible);
      new IntersectionObserver(([en]) => { btnVisible = en.isIntersecting || en.boundingClientRect.top > window.innerHeight; update(); }).observe(submit);
      new IntersectionObserver(([en]) => { boxVisible = en.isIntersecting; update(); }, { rootMargin: '0px 0px 200px 0px' }).observe(section);
    }
  });
  }

  /* ---------- Dialogs ---------- */
  document.addEventListener('click', (e) => {
    const opener = e.target.closest('[data-dialog-open]');
    if (opener) {
      const d = document.getElementById(opener.dataset.dialogOpen);
      if (d && d.showModal) d.showModal();
      return;
    }
    if (e.target.closest('[data-dialog-close]')) { e.target.closest('dialog').close(); return; }
    if (e.target.tagName === 'DIALOG') e.target.close();
  });

  /* ---------- Autoplay videos only when visible ---------- */
  const videoIO = 'IntersectionObserver' in window ? new IntersectionObserver((entries) => {
      entries.forEach(({ target, isIntersecting }) => {
        if (isIntersecting && !reduceMotion) {
          if (target.preload === 'none') target.preload = 'auto';
          const p = target.play();
          if (p && p.catch) p.catch(() => {});
        } else {
          target.pause();
        }
      });
    }, { rootMargin: '120px 0px' }) : null;
  function initVideos(scope) {
    if (!videoIO) return;
    $$('video[data-autoplay]', scope).forEach((v) => videoIO.observe(v));
  }

  /* ---------- UGC videos: tap to play with sound ---------- */
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-ugc-play]');
    const vid = btn ? btn.parentElement.querySelector('video') : e.target.closest('[data-ugc-video]');
    if (!vid) return;
    const card = vid.closest('.ugc__card');
    $$('[data-ugc-video]').forEach((other) => {
      if (other !== vid) { other.pause(); other.closest('.ugc__card').classList.remove('is-playing'); }
    });
    if (vid.paused) {
      vid.muted = false;
      vid.controls = true;
      const p = vid.play();
      if (p && p.catch) p.catch(() => {});
      card.classList.add('is-playing');
    } else {
      vid.pause();
      card.classList.remove('is-playing');
    }
  });

  /* ---------- Scroll story (sticky scene) ---------- */
  {
    const tick = () => {
      $$('[data-story]').forEach((story) => {
        const rect = story.getBoundingClientRect();
        const total = story.offsetHeight - window.innerHeight;
        const p = reduceMotion ? 1 : Math.min(1, Math.max(0, -rect.top / Math.max(total, 1)));
        story.style.setProperty('--p', p.toFixed(4));
        const pop = Math.min(1, Math.max(0, (p - 0.72) / 0.2));
        story.style.setProperty('--pop', pop.toFixed(3));
        const lines = $$('.story__line', story);
        const n = lines.length;
        lines.forEach((line, i) => {
          const threshold = 0.06 + (i / Math.max(n, 1)) * 0.62;
          line.classList.toggle('is-in', p >= threshold);
        });
      });
    };
    let ticking = false;
    const onScroll = () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => { tick(); ticking = false; });
    };
    tick();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
  }

  /* ---------- Reveal on scroll ---------- */
  const REVEAL = '.offer-card, .value-card, .trust__tile, .ugc__card, .steps__item, .compare__table, .cta__card, .splitcard__card, .faq__list .accordion';
  const revealIO = 'IntersectionObserver' in window && !reduceMotion && !(window.Shopify && window.Shopify.designMode)
    ? new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) { en.target.classList.add('is-in'); revealIO.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' }) : null;
  function initReveal(scope) {
    if (!revealIO) return;
    $$(REVEAL, scope).forEach((el, i) => {
      el.setAttribute('data-reveal', '');
      el.style.transitionDelay = `${(i % 4) * 70}ms`;
      revealIO.observe(el);
    });
  }

  /* ---------- Smooth anchor scroll for in-page CTAs (#buy) ---------- */
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a || a.getAttribute('href').length < 2) return;
    const target = document.getElementById(a.getAttribute('href').slice(1));
    if (!target) return;
    e.preventDefault();
    target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
  });

  /* ---------- Init + theme editor support ---------- */
  function init(scope = document) {
    initRotators(scope);
    initBuyboxes(scope);
    initVideos(scope);
    initReveal(scope);
  }
  init();
  document.addEventListener('shopify:section:load', (e) => {
    init(e.target);
    const md = e.target.querySelector('#MenuDrawer');
    if (md) { const old = document.body.querySelector(':scope > #MenuDrawer'); if (old && old !== md) old.remove(); document.body.appendChild(md); }
    window.dispatchEvent(new Event('scroll'));
  });
  document.addEventListener('shopify:block:select', (e) => {
    const slide = e.target.closest('.gallery__slide');
    if (slide) slide.scrollIntoView({ block: 'nearest', inline: 'start' });
  });
})();
