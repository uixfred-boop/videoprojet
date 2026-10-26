/* ==========================================================================
   Portfolio — scripts partagés par toutes les pages
   Dépendances : GSAP + ScrollTrigger + Lenis (assets/vendor)
   ========================================================================== */
(function () {
  "use strict";

  const SITE = window.SITE;
  const PROJECTS = window.PROJECTS;
  const page = document.body.dataset.page;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const hasGsap = typeof window.gsap !== "undefined";

  if (hasGsap && window.ScrollTrigger) gsap.registerPlugin(ScrollTrigger);

  /* ------------------------------------------------------------------------
     Helpers
     ------------------------------------------------------------------------ */
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
  const pad = (n) => String(n).padStart(2, "0");
  const esc = (s) =>
    String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

  const projectUrl = (p) => `project.html?p=${encodeURIComponent(p.slug)}`;

  const store = {
    get(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { sessionStorage.setItem(k, v); } catch (e) { /* ignore */ } },
  };

  // Renders an image, a video, or a gradient placeholder when no src is set.
  function media(item, project, label) {
    item = item || {};
    const colors = (project && project.colors) || ["#444", "#111"];
    if (item.src && item.type === "video") {
      return `<video src="${esc(item.src)}" ${item.poster ? `poster="${esc(item.poster)}"` : ""} autoplay muted loop playsinline preload="metadata"></video>`;
    }
    if (item.src) {
      return `<img src="${esc(item.src)}" alt="${esc(item.alt || (project && project.title) || "")}" loading="lazy">`;
    }
    const isVideo = item.type === "video";
    return `<div class="ph${isVideo ? " ph--video" : ""}" style="--c1:${colors[0]};--c2:${colors[1]}">
      ${label ? `<span class="ph__label mono">${esc(label)}</span>` : ""}
    </div>`;
  }

  const arrow = `<svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true"><path d="M1 9h15M10 3l6 6-6 6" stroke="currentColor" stroke-width="1.4"/></svg>`;

  function splitChars(el) {
    const text = el.textContent;
    el.setAttribute("aria-label", text);
    el.innerHTML = [...text]
      .map((c) => `<span class="char" aria-hidden="true">${c === " " ? "&nbsp;" : esc(c)}</span>`)
      .join("");
    return $$(".char", el);
  }

  function splitWords(el) {
    const words = el.textContent.trim().split(/\s+/);
    el.innerHTML = words.map((w) => `<span class="word">${esc(w)}</span>`).join(" ");
    return $$(".word", el);
  }

  // Wraps each [data-lines] element's content in a mask for a slide-up reveal.
  function maskLines(el) {
    el.innerHTML = `<span class="line-mask"><span>${el.innerHTML}</span></span>`;
    return $(".line-mask > span", el);
  }

  /* ------------------------------------------------------------------------
     Layout : header, menu mobile, footer, curseur, transitions
     ------------------------------------------------------------------------ */
  const NAV = [
    { id: "work", label: "Work", href: "work.html" },
    { id: "about", label: "About", href: "about.html" },
    { id: "contact", label: "Contact", href: "#contact" },
  ];

  function renderLayout() {
    const activeId = page === "project" ? "work" : page;
    const navLinks = NAV.map(
      (n) => `<a href="${n.href}" class="u-link${n.id === activeId ? " is-active" : ""}">${n.label}</a>`
    ).join("");

    document.body.insertAdjacentHTML(
      "afterbegin",
      `<div class="transition" aria-hidden="true"></div>
      <div class="cursor" aria-hidden="true"><span class="cursor__label"></span></div>
      <header class="header">
        <a href="index.html" class="header__logo">${esc(SITE.name)}<sup class="mono">©</sup></a>
        <div class="header__status mono"><span class="dot"></span>${esc(SITE.availability)}</div>
        <div class="header__time mono"><span>${esc(SITE.location)}</span> <span data-clock></span></div>
        <nav class="header__nav">${navLinks}</nav>
        <button class="menu-btn" aria-expanded="false">Menu</button>
      </header>
      <div class="mobile-menu">
        <nav>${NAV.map((n) => `<a href="${n.href}">${n.label}</a>`).join("")}</nav>
        <div class="mono muted">${esc(SITE.location)} — <span data-clock></span></div>
      </div>`
    );

    const footer = document.createElement("footer");
    footer.className = "footer";
    footer.id = "contact";
    footer.innerHTML = `
      <div class="footer__top">
        <div class="footer__cta">
          <p class="mono muted">Un projet en tête ?</p>
          <h2 data-lines>Travaillons<br>ensemble.</h2>
          <button class="footer__email u-link" data-copy="${esc(SITE.email)}">
            ${esc(SITE.email)} <span class="copied mono">Copié !</span>
          </button>
        </div>
        <div class="footer__links">
          <div class="footer__col">
            <span class="mono muted">Menu</span>
            <a href="index.html" class="u-link">Home</a>
            ${NAV.filter((n) => n.id !== "contact").map((n) => `<a href="${n.href}" class="u-link">${n.label}</a>`).join("")}
          </div>
          <div class="footer__col">
            <span class="mono muted">Réseaux</span>
            ${SITE.socials.map((s) => `<a href="${esc(s.url)}" target="_blank" rel="noopener" class="u-link">${esc(s.label)}</a>`).join("")}
          </div>
        </div>
      </div>
      <div class="footer__bottom mono muted">
        <span>© ${new Date().getFullYear()} ${esc(SITE.name)}</span>
        <span>${esc(SITE.role)}</span>
        <span>${esc(SITE.location)} — <span data-clock></span></span>
        <button class="u-link" data-top>Retour en haut ↑</button>
      </div>
      <div class="footer__giant" aria-hidden="true">${esc(SITE.name)}</div>`;
    document.body.appendChild(footer);
  }

  function initClock() {
    const fmt = new Intl.DateTimeFormat("fr-FR", {
      hour: "2-digit", minute: "2-digit", second: "2-digit", timeZone: SITE.timezone,
    });
    const tick = () => $$("[data-clock]").forEach((el) => (el.textContent = fmt.format(new Date())));
    tick();
    setInterval(tick, 1000);
  }

  function initMenu() {
    const btn = $(".menu-btn");
    const menu = $(".mobile-menu");
    btn.addEventListener("click", () => {
      const open = menu.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", open);
      btn.textContent = open ? "Fermer" : "Menu";
    });
    $$("a", menu).forEach((a) => a.addEventListener("click", () => {
      menu.classList.remove("is-open");
      btn.textContent = "Menu";
    }));
  }

  function initCopy() {
    $$("[data-copy]").forEach((btn) =>
      btn.addEventListener("click", () => {
        const value = btn.dataset.copy;
        const done = () => {
          btn.classList.add("is-copied");
          setTimeout(() => btn.classList.remove("is-copied"), 1600);
        };
        if (navigator.clipboard) navigator.clipboard.writeText(value).then(done, () => (location.href = `mailto:${value}`));
        else location.href = `mailto:${value}`;
      })
    );
  }

  function initCursor() {
    const cursor = $(".cursor");
    if (!hasGsap || window.matchMedia("(hover: none)").matches) return;
    const label = $(".cursor__label", cursor);
    const x = gsap.quickTo(cursor, "x", { duration: 0.5, ease: "power3" });
    const y = gsap.quickTo(cursor, "y", { duration: 0.5, ease: "power3" });
    window.addEventListener("mousemove", (e) => { x(e.clientX); y(e.clientY); });

    document.addEventListener("mouseover", (e) => {
      const target = e.target.closest("a, button, [data-cursor]");
      cursor.classList.toggle("is-hover", !!target && !target.dataset.cursor);
      cursor.classList.toggle("has-label", !!(target && target.dataset.cursor));
      if (target && target.dataset.cursor) label.textContent = target.dataset.cursor;
    });
  }

  /* Smooth scroll */
  let lenis = null;
  function initScroll() {
    if (reduceMotion || typeof window.Lenis === "undefined") return;
    lenis = new Lenis({ lerp: 0.1 });
    if (hasGsap) {
      lenis.on("scroll", ScrollTrigger.update);
      gsap.ticker.add((t) => lenis.raf(t * 1000));
      gsap.ticker.lagSmoothing(0);
    } else {
      const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }
  }

  function scrollToTarget(target) {
    if (lenis) lenis.scrollTo(target, { duration: 1.6 });
    else (typeof target === "number" ? window.scrollTo({ top: target, behavior: "smooth" }) : target.scrollIntoView({ behavior: "smooth" }));
  }

  function initAnchors() {
    $$("[data-top]").forEach((b) => b.addEventListener("click", () => scrollToTarget(0)));
    document.addEventListener("click", (e) => {
      const a = e.target.closest('a[href^="#"]');
      if (!a) return;
      const target = document.querySelector(a.getAttribute("href"));
      if (target) { e.preventDefault(); scrollToTarget(target); }
    });
  }

  /* Page transitions : rideau qui monte avant de changer de page */
  function initTransitions() {
    const curtain = $(".transition");
    if (!hasGsap || reduceMotion) return;

    document.addEventListener("click", (e) => {
      const a = e.target.closest("a");
      if (!a || a.target === "_blank" || e.metaKey || e.ctrlKey || e.shiftKey) return;
      const href = a.getAttribute("href");
      if (!href || href.startsWith("#") || href.startsWith("mailto:") || /^https?:/.test(href)) return;
      e.preventDefault();
      store.set("transition", "1");
      gsap.fromTo(curtain, { yPercent: 100, visibility: "visible" }, {
        yPercent: 0, duration: 0.8, ease: "power4.inOut",
        onComplete: () => (location.href = href),
      });
    });

    // Back/forward cache : on retire le rideau si la page est restaurée
    window.addEventListener("pageshow", (e) => { if (e.persisted) gsap.set(curtain, { yPercent: 100, visibility: "hidden" }); });
  }

  /* ------------------------------------------------------------------------
     Intro : preloader au premier chargement, rideau sinon
     ------------------------------------------------------------------------ */
  function intro(onDone) {
    const curtain = $(".transition");
    if (!hasGsap || reduceMotion) return onDone();

    if (store.get("transition")) {
      store.set("transition", "");
      gsap.set(curtain, { yPercent: 0, visibility: "visible" });
      gsap.to(curtain, {
        yPercent: -100, duration: 0.9, ease: "power4.inOut", delay: 0.05,
        onComplete: () => gsap.set(curtain, { visibility: "hidden" }),
      });
      return setTimeout(onDone, 350);
    }

    if (store.get("visited") || page !== "home") return onDone();
    store.set("visited", "1");

    document.body.classList.add("is-loading");
    document.body.insertAdjacentHTML(
      "afterbegin",
      `<div class="preloader"><span class="preloader__count">0</span><span class="preloader__name mono">${esc(SITE.name)} — ${esc(SITE.role)}</span></div>`
    );
    const pre = $(".preloader");
    const count = { v: 0 };
    gsap.timeline({
      onComplete: () => { pre.remove(); document.body.classList.remove("is-loading"); },
    })
      .to(count, {
        v: 100, duration: 1.8, ease: "power3.inOut",
        onUpdate: () => ($(".preloader__count", pre).textContent = Math.round(count.v)),
      })
      .to(pre, { yPercent: -100, duration: 1, ease: "power4.inOut" })
      .add(onDone, "-=0.6");
  }

  /* ------------------------------------------------------------------------
     Animations génériques
     ------------------------------------------------------------------------ */
  function initReveals() {
    if (!hasGsap || reduceMotion) return;

    $$("[data-lines]").forEach((el) => {
      const inner = maskLines(el);
      gsap.from(inner, {
        yPercent: 110, duration: 1.2, ease: "power4.out",
        scrollTrigger: { trigger: el, start: "top 90%" },
      });
    });

    $$("[data-fade]").forEach((el) => {
      gsap.from(el, {
        y: 40, opacity: 0, duration: 1.2, ease: "power3.out",
        scrollTrigger: { trigger: el, start: "top 92%" },
      });
    });

    $$("[data-stagger]").forEach((list) => {
      gsap.from(list.children, {
        y: 40, opacity: 0, duration: 1, ease: "power3.out", stagger: 0.08,
        scrollTrigger: { trigger: list, start: "top 88%" },
      });
    });

    $$("[data-parallax]").forEach((el) => {
      gsap.fromTo(el, { yPercent: -8, scale: 1.15 }, {
        yPercent: 8, ease: "none",
        scrollTrigger: { trigger: el.parentElement, start: "top bottom", end: "bottom top", scrub: true },
      });
    });

    $$("[data-words]").forEach((el) => {
      const words = splitWords(el);
      gsap.to(words, {
        opacity: 1, stagger: 0.1, ease: "none",
        scrollTrigger: { trigger: el, start: "top 80%", end: "bottom 45%", scrub: true },
      });
    });

    const giant = $(".footer__giant");
    if (giant) {
      gsap.from(giant, {
        yPercent: 60, ease: "none",
        scrollTrigger: { trigger: ".footer", start: "top bottom", end: "bottom bottom", scrub: true },
      });
    }
  }

  // Hero : lettres qui montent une à une
  function heroIn(selector) {
    const title = $(selector);
    if (!title) return;
    const chars = splitChars(title);
    if (!hasGsap || reduceMotion) return;
    gsap.set(title, { overflow: "hidden" });
    gsap.from(chars, { yPercent: 110, duration: 1.4, ease: "power4.out", stagger: 0.04 });
    gsap.from("[data-hero-fade]", { y: 20, opacity: 0, duration: 1, ease: "power3.out", stagger: 0.1, delay: 0.4 });
  }

  /* ------------------------------------------------------------------------
     Liste de projets + aperçu flottant
     ------------------------------------------------------------------------ */
  function workRows(list) {
    return list
      .map(
        (p, i) => `<li>
          <a class="work-row" href="${projectUrl(p)}" data-index="${i}" data-cursor="Voir">
            <span class="work-row__num mono muted">${pad(i + 1)}</span>
            <span class="work-row__title">${esc(p.title)}</span>
            <span class="work-row__cat mono">${esc(p.category)}</span>
            <span class="work-row__year mono">${esc(p.year)}</span>
            <span class="work-row__arrow">${arrow}</span>
          </a>
        </li>`
      )
      .join("");
  }

  function initPreview(listEl, list) {
    if (!hasGsap || window.matchMedia("(hover: none)").matches) return;
    let preview = $(".preview");
    if (!preview) {
      preview = document.createElement("div");
      preview.className = "preview";
      preview.innerHTML = `<div class="preview__track"></div>`;
      document.body.appendChild(preview);
    }
    const track = $(".preview__track", preview);
    track.innerHTML = list
      .map((p, i) => `<div class="preview__item" style="top:${i * 100}%">${media(p.cover, p, p.category)}</div>`)
      .join("");

    const x = gsap.quickTo(preview, "x", { duration: 0.6, ease: "power3" });
    const y = gsap.quickTo(preview, "y", { duration: 0.6, ease: "power3" });
    window.addEventListener("mousemove", (e) => { x(e.clientX); y(e.clientY); });

    listEl.addEventListener("mouseover", (e) => {
      const row = e.target.closest(".work-row");
      if (!row) return;
      track.style.transform = `translateY(${-row.dataset.index * 100}%)`;
      gsap.to(preview, { scale: 1, duration: 0.5, ease: "power3.out", overwrite: "auto" });
    });
    listEl.addEventListener("mouseleave", () =>
      gsap.to(preview, { scale: 0, duration: 0.4, ease: "power3.in", overwrite: "auto" })
    );
  }

  /* ------------------------------------------------------------------------
     Pages
     ------------------------------------------------------------------------ */
  const pages = {
    home() {
      $("[data-site-role]").textContent = SITE.role;
      $("[data-site-intro]").textContent = SITE.intro;
      $("[data-hero-title]").textContent = SITE.name;
      $("[data-statement]").textContent = SITE.statement;

      // Showreel
      const reel = $(".reel__frame");
      reel.insertAdjacentHTML("afterbegin", media(SITE.showreel, { colors: ["#ff5a1f", "#151515"] }));
      $(".reel__label").textContent = SITE.showreel.label || "Showreel";
      const video = $("video", reel);
      if (video) {
        reel.dataset.cursor = "Son";
        reel.addEventListener("click", () => {
          video.muted = !video.muted;
          reel.dataset.cursor = video.muted ? "Son" : "Muet";
          $(".cursor__label").textContent = reel.dataset.cursor;
        });
      }
      if (hasGsap && !reduceMotion) {
        gsap.fromTo(reel, { scale: 0.55, borderRadius: 16 }, {
          scale: 1, borderRadius: 6, ease: "none",
          scrollTrigger: { trigger: ".reel", start: "top bottom", end: "top 10%", scrub: true },
        });
      }

      // Projets
      const list = $("[data-work-list]");
      list.innerHTML = workRows(PROJECTS);
      $("[data-work-count]").textContent = pad(PROJECTS.length);
      initPreview(list, PROJECTS);

      // Services
      $("[data-services]").innerHTML = SITE.services
        .map(
          (s, i) => `<li class="service">
            <span class="mono muted">${pad(i + 1)}</span>
            <h3 class="service__title">${esc(s.title)}</h3>
            <div class="service__body">
              <p class="service__text">${esc(s.text)}</p>
              <div class="service__tags">${s.tags.map((t) => `<span class="tag mono">${esc(t)}</span>`).join("")}</div>
            </div>
          </li>`
        )
        .join("");

      // Marquee clients (dupliqué pour une boucle continue)
      const items = SITE.about.clients.map((c) => `<span class="marquee__item">${esc(c)}<i></i></span>`).join("");
      $(".marquee__track").innerHTML = items + items;

      return () => heroIn("[data-hero-title]");
    },

    work() {
      const listEl = $("[data-work-list]");
      const gridEl = $("[data-work-grid]");
      const categories = ["Tous", ...new Set(PROJECTS.map((p) => p.category))];
      let current = "Tous";

      $("[data-work-count]").textContent = pad(PROJECTS.length);
      $("[data-filters]").innerHTML = categories
        .map((c) => {
          const n = c === "Tous" ? PROJECTS.length : PROJECTS.filter((p) => p.category === c).length;
          return `<button class="filter${c === current ? " is-active" : ""}" data-filter="${esc(c)}">${esc(c)}<sup>${pad(n)}</sup></button>`;
        })
        .join("");

      function render() {
        const list = current === "Tous" ? PROJECTS : PROJECTS.filter((p) => p.category === current);
        listEl.innerHTML = workRows(list);
        gridEl.innerHTML = list
          .map(
            (p) => `<a class="work-card" href="${projectUrl(p)}" data-cursor="Voir">
              <div class="work-card__media">${media(p.cover, p, p.category)}</div>
              <div class="work-card__info">
                <span class="work-card__title">${esc(p.title)}</span>
                <span class="mono muted">${esc(p.category)} — ${esc(p.year)}</span>
              </div>
            </a>`
          )
          .join("");
        initPreview(listEl, list);
        if (hasGsap && !reduceMotion) {
          gsap.from([...listEl.children, ...gridEl.children], { y: 30, opacity: 0, duration: 0.8, ease: "power3.out", stagger: 0.05 });
        }
        if (window.ScrollTrigger) ScrollTrigger.refresh();
      }

      $("[data-filters]").addEventListener("click", (e) => {
        const btn = e.target.closest("[data-filter]");
        if (!btn) return;
        current = btn.dataset.filter;
        $$(".filter").forEach((b) => b.classList.toggle("is-active", b === btn));
        render();
      });

      $(".view-toggle").addEventListener("click", (e) => {
        const btn = e.target.closest("[data-view]");
        if (!btn) return;
        const grid = btn.dataset.view === "grid";
        $$(".view-toggle button").forEach((b) => b.classList.toggle("is-active", b === btn));
        listEl.hidden = grid;
        gridEl.hidden = !grid;
        if (window.ScrollTrigger) ScrollTrigger.refresh();
      });

      render();
      return () => heroIn("[data-hero-title]");
    },

    about() {
      const a = SITE.about;
      $("[data-about-intro]").textContent = SITE.intro;
      $(".about-portrait").innerHTML = `<div data-parallax style="height:100%">${media(a.portrait, { colors: ["#ff5a1f", "#1a1a1a"] }, "Portrait")}</div>`;
      $("[data-about-bio]").innerHTML = a.bio.map((p) => `<p>${esc(p)}</p>`).join("");
      $("[data-experience]").innerHTML = a.experience
        .map((x) => `<li><span>${esc(x.company)}</span><span class="muted">${esc(x.role)}</span><span class="mono">${esc(x.period)}</span></li>`)
        .join("");
      $("[data-recognitions]").innerHTML = a.recognitions
        .map((r) => `<li><span>${esc(r.name)}</span><span class="mono">${esc(r.year)}</span></li>`)
        .join("");
      $("[data-clients]").innerHTML = a.clients.map((c) => `<li>${esc(c)}</li>`).join("");
      $("[data-services-list]").innerHTML = SITE.services
        .map((s, i) => `<li><span>${esc(s.title)}</span><span class="muted">${esc(s.tags.join(", "))}</span><span class="mono">${pad(i + 1)}</span></li>`)
        .join("");
      return () => heroIn("[data-hero-title]");
    },

    project() {
      const slug = new URLSearchParams(location.search).get("p");
      const index = Math.max(0, PROJECTS.findIndex((p) => p.slug === slug));
      const p = PROJECTS[index];
      const next = PROJECTS[(index + 1) % PROJECTS.length];

      document.title = `${p.title} — ${SITE.name}`;
      $("[data-hero-title]").textContent = p.title;
      $("[data-project-summary]").textContent = p.summary;
      $("[data-project-meta]").innerHTML = [
        ["Client", p.client],
        ["Rôle", p.role],
        ["Services", p.services.join(", ")],
        ["Année", p.year],
      ]
        .map(([k, v]) => `<div><span class="mono muted">${k}</span><span>${esc(v)}</span></div>`)
        .join("");
      $(".project-cover__inner").innerHTML = `<div data-parallax style="height:100%">${media(p.cover, p, p.category)}</div>`;
      $("[data-project-text]").innerHTML = p.description.map((d) => `<p>${esc(d)}</p>`).join("");
      const link = $("[data-project-link]");
      if (p.url) link.innerHTML = `<a class="pill" href="${esc(p.url)}" target="_blank" rel="noopener">Voir le site ${arrow}</a>`;
      $("[data-gallery]").innerHTML = (p.gallery || [])
        .map((g, i) => `<div class="gallery__item" data-fade>${media(g, p, `${pad(i + 1)} / ${pad(p.gallery.length)}`)}</div>`)
        .join("");
      const nextLink = $(".next-project");
      nextLink.href = projectUrl(next);
      $(".next-project__title").textContent = next.title;
      return () => heroIn("[data-hero-title]");
    },
  };

  /* ------------------------------------------------------------------------
     Boot
     ------------------------------------------------------------------------ */
  renderLayout();
  const start = pages[page] ? pages[page]() : null;
  initClock();
  initMenu();
  initCopy();
  initCursor();
  initScroll();
  initAnchors();
  initTransitions();
  initReveals();
  intro(() => start && start());
})();
