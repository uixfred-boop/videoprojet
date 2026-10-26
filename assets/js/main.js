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
  const isDesktop = () => window.innerWidth >= 1024;

  gsap.registerPlugin(ScrollTrigger);

  /* ------------------------------------------------------------------------
     Helpers
     ------------------------------------------------------------------------ */
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
  const esc = (s) =>
    String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const projectUrl = (p) => `project.html?p=${encodeURIComponent(p.slug)}`;
  const vh = (n) => (window.innerHeight * n) / 100;

  const store = {
    get(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { sessionStorage.setItem(k, v); } catch (e) { /* ignore */ } },
  };

  const icons = {
    arrowDown: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 5v14M5 12l7 7 7-7"/></svg>`,
    arrowRight: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>`,
    menu: `<svg class="i-menu" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>`,
    close: `<svg class="i-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>`,
    muted: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M11 5L6 9H2v6h4l5 4V5zM23 9l-6 6M17 9l6 6"/></svg>`,
    sound: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M11 5L6 9H2v6h4l5 4V5zM15.5 8.5a5 5 0 010 7M19 5a10 10 0 010 14"/></svg>`,
  };

  // Image, vidéo, ou dégradé de remplacement quand `src` est vide.
  function media(item, colors, label) {
    item = item || {};
    const c = item.colors || colors || ["#8a8a8a", "#1c1c1c"];
    let inner;
    if (item.src && item.type === "video") {
      inner = `<video src="${esc(item.src)}" ${item.poster ? `poster="${esc(item.poster)}"` : ""} autoplay muted loop playsinline preload="metadata"></video>`;
    } else if (item.src) {
      inner = `<img src="${esc(item.src)}" alt="${esc(item.alt || label || "")}" loading="lazy">`;
    } else {
      const text = item.label || label;
      inner = `<div class="ph${item.type === "video" ? " ph--video" : ""}" style="--c1:${c[0]};--c2:${c[1]}">${text ? `<span class="ph__label">${esc(text)}</span>` : ""}</div>`;
    }
    return `<div class="media">${inner}</div>`;
  }

  // Texte en double pour l'effet de « roulement » au survol
  const roll = (text) =>
    `<span class="roll"><span class="roll__inner"><span>${esc(text)}</span><span>${esc(text)}</span></span></span>`;

  // Bandeau défilant (texte dupliqué pour une boucle continue)
  function ticker(items) {
    const text = items.map(esc).join(", ") + ",";
    const speed = Math.max(14, text.length * 0.28);
    const p = `<p class="dot-font">${text}</p>`;
    return `<div class="ticker"><div class="ticker__track" style="--ticker-speed:${speed}s">${p}${p}</div></div>`;
  }

  const mask = (html, cls = "") => `<span class="mask ${cls}"><span>${html}</span></span>`;

  /* ------------------------------------------------------------------------
     Layout commun : header, barre du bas, footer
     ------------------------------------------------------------------------ */
  function renderLayout() {
    const cols = SITE.header
      .map((h) => {
        const value = h.url
          ? `<a href="${esc(h.url)}" target="_blank" rel="noopener" class="group muted">${roll(h.value)}</a>`
          : `<span class="muted">${esc(h.value)}</span>`;
        return `<div class="header__col">${mask(esc(h.label))}${mask(value)}</div>`;
      })
      .join("");

    const avatar = typeof SITE.avatar === "string" ? esc(SITE.avatar) : media(SITE.avatar);
    const firstCover = PROJECTS[0] ? media(PROJECTS[0].cover, PROJECTS[0].colors) : "";
    const navLinks = [
      { label: "Home", href: "index.html", thumb: `<span class="dock__thumb-label">${esc(SITE.domain)}</span>` },
      { label: "Work", href: "work.html", thumb: firstCover },
    ];

    document.body.insertAdjacentHTML(
      "afterbegin",
      `<header class="header">${cols}</header>
      <div class="header__cta">
        <a href="mailto:${esc(SITE.email)}" class="cta group" aria-label="M'envoyer un email">
          <span class="cta__emoji" aria-hidden="true">${esc(typeof SITE.avatar === "string" ? SITE.avatar : "✉️")}</span>
          <span class="cta__pill">${roll("Me contacter")}</span>
        </a>
      </div>
      <div class="dock">
        <div class="dock__menu">
          <nav class="dock__nav">
            ${navLinks
              .map(
                (l) => `<a class="dock__link" href="${l.href}">
                  <span class="dock__thumb">${l.thumb}</span>
                  ${roll(l.label)}
                </a>`
              )
              .join("")}
          </nav>
          <div class="dock__line"></div>
        </div>
        <div class="dock__bar">
          <div class="dock__id">
            <div class="dock__avatar">${avatar}</div>
            <div class="dock__text">
              <a class="dock__name" href="index.html">${esc(SITE.name)}</a>
              ${ticker(SITE.roles)}
            </div>
          </div>
          <button class="dock__toggle" aria-label="Ouvrir le menu" aria-expanded="false">${icons.menu}${icons.close}</button>
        </div>
      </div>`
    );

    const tiles = [
      `<a class="tile tile--8" href="work.html">Work</a>`,
      `<a class="tile tile--4" href="mailto:${esc(SITE.email)}">Contact</a>`,
      ...SITE.socials.map(
        (s) => `<a class="tile tile--4 tile--sm" href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.label)}</a>`
      ),
    ];
    const footer = document.createElement("footer");
    footer.className = "footer";
    footer.innerHTML = `<h2 class="footer__big" aria-hidden="true">${esc(SITE.domain)}</h2>${tiles.join("")}`;
    document.body.appendChild(footer);
  }

  function initDock() {
    const dock = $(".dock");
    const menu = $(".dock__menu", dock);
    const btn = $(".dock__toggle", dock);
    let open = false;

    const tl = gsap.timeline({ paused: true })
      .to(menu, { height: "auto", duration: 0.6, ease: "power3.inOut" })
      .fromTo($$(".dock__thumb", dock), { y: 24, scale: 0.9, opacity: 0 }, { y: 0, scale: 1, opacity: 1, duration: 0.5, stagger: 0.06, ease: "power3.out" }, 0.2)
      .fromTo($$(".dock__link .roll__inner", dock), { yPercent: 50 }, { yPercent: 0, duration: 0.5, stagger: 0.06, ease: "power3.out", clearProps: "transform" }, 0.25)
      .fromTo($(".dock__line", dock), { width: "0%" }, { width: "100%", duration: 0.6, ease: "power3.inOut" }, 0.2);

    btn.addEventListener("click", () => {
      open = !open;
      dock.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", open);
      btn.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
      open ? tl.play() : tl.reverse();
    });

    // La barre se cache quand on arrive sur le footer
    ScrollTrigger.create({
      trigger: ".footer",
      start: "top 85%",
      onEnter: () => gsap.to(dock, { y: 160, duration: 0.6, ease: "power3.inOut" }),
      onLeaveBack: () => gsap.to(dock, { y: 0, duration: 0.6, ease: "power3.out" }),
    });
  }

  /* ------------------------------------------------------------------------
     Smooth scroll
     ------------------------------------------------------------------------ */
  function initScroll() {
    if (reduceMotion || typeof window.Lenis === "undefined") return;
    const lenis = new Lenis({ lerp: 0.1 });
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }

  /* ------------------------------------------------------------------------
     Loader (premier chargement uniquement) puis animations d'entrée
     ------------------------------------------------------------------------ */
  function loader(done) {
    if (reduceMotion || store.get("loaded")) return done();
    store.set("loaded", "1");
    document.body.classList.add("is-loading");
    document.body.insertAdjacentHTML("afterbegin", `<div class="loader"><div class="mask"><p>0</p></div></div>`);
    const el = $(".loader");
    const count = { v: 0 };
    gsap.timeline()
      .to(count, {
        v: 100, duration: 1.6, ease: "power2.inOut",
        onUpdate: () => ($("p", el).textContent = Math.round(count.v)),
      })
      .to($("p", el), { yPercent: -110, duration: 0.5, ease: "power3.in" })
      .to(el, {
        opacity: 0, duration: 0.6, ease: "power2.out",
        onStart: done,
        onComplete: () => { el.remove(); document.body.classList.remove("is-loading"); },
      });
  }

  function layoutIn() {
    gsap.from($$(".header .mask > *"), { yPercent: 100, duration: 1, ease: "power4.out", stagger: 0.05 });
    gsap.from(".header__cta", { y: 16, scale: 0.95, opacity: 0, duration: 0.8, ease: "power3.out", delay: 0.2 });
    gsap.from(".dock", { y: 100, scale: 0.95, opacity: 0, duration: 1, ease: "power3.out", delay: 0.3 });
  }

  /* ------------------------------------------------------------------------
     Animations génériques au scroll
     ------------------------------------------------------------------------ */
  // Éléments qui apparaissent (opacité + léger décalage)
  function appear(targets, opts = {}) {
    $$(targets).forEach((el) => {
      gsap.fromTo(el, { opacity: 0, y: opts.y ?? 24, scale: opts.scale ?? 0.98 }, {
        opacity: 1, y: 0, scale: 1, duration: 0.9, ease: "power3.out",
        scrollTrigger: { trigger: el, start: "top 92%", once: true },
      });
    });
  }

  // Étiquettes qui arrivent une par une
  function tagsIn(container) {
    $$(".tags", container).forEach((list) => {
      gsap.fromTo(list.children, { opacity: 0, y: 24, scale: 0.9 }, {
        opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "power3.out", stagger: 0.04,
        scrollTrigger: { trigger: list, start: "top 92%", once: true },
      });
    });
  }

  // Parallaxe verticale d'un élément dans son conteneur
  function parallax(el, amount) {
    gsap.fromTo(el, { y: () => -vh(amount) }, {
      y: () => vh(amount), ease: "none",
      scrollTrigger: { trigger: el.parentElement, start: "top bottom", end: "bottom top", scrub: true, invalidateOnRefresh: true },
    });
  }

  // Ajuste la taille du titre pour remplir toute la largeur
  function fitText(el, words) {
    const fit = () => {
      el.style.fontSize = "100px";
      const width = el.clientWidth;
      const sizes = words.map((w) => w.getBoundingClientRect().width);
      if (isDesktop()) {
        const gap = window.innerWidth * 0.04;
        const total = sizes.reduce((a, b) => a + b, 0);
        el.style.fontSize = `${(100 * (width - gap * (words.length - 1))) / total}px`;
      } else {
        const widest = Math.max(...sizes);
        el.style.fontSize = `${(100 * width) / widest}px`;
      }
    };
    fit();
    if (document.fonts) document.fonts.ready.then(() => { fit(); ScrollTrigger.refresh(); });
    window.addEventListener("resize", fit);
  }

  /* ------------------------------------------------------------------------
     Composants
     ------------------------------------------------------------------------ */
  function projectCard(p) {
    const icon = p.icon
      ? `<span class="card__icon">${media(p.icon, p.colors)}</span>`
      : `<span class="card__icon" style="background:${p.colors[0]}">${esc(p.title.charAt(0))}</span>`;
    return `<a class="card" href="${projectUrl(p)}">
      <div class="card__media">
        <div class="card__blur"></div>
        <div class="card__preview">${media(p.preview, p.colors, "Aperçu vidéo")}</div>
        <div class="card__parallax">${media(p.cover, p.colors)}</div>
      </div>
      <div class="card__info">
        <div class="card__row">
          <div class="card__name">${icon}<p class="card__title">${esc(p.title)}</p></div>
          <div class="card__meta"><p>${esc(p.category)}</p><p>${esc(p.year)}</p></div>
        </div>
        ${ticker(p.tags)}
      </div>
    </a>`;
  }

  function initCards(scope) {
    $$(".card__parallax", scope).forEach((el) => parallax(el, 10));
  }

  /* ------------------------------------------------------------------------
     Pages
     ------------------------------------------------------------------------ */
  const pages = {
    home() {
      const h = SITE.hero;

      // Hero
      const hero = $(".hero");
      hero.innerHTML = `
        <div class="hero__bottom">
          ${mask(`<span class="hero__top">${h.top.map((w) => `<span>${esc(w)}</span>`).join("")}</span>`)}
          <div class="hero__title">${h.title.map((w) => mask(`<span class="hero__word">${esc(w)}</span>`)).join("")}</div>
        </div>
        <div class="hero__scroll hero__scroll--l">${mask(`<span style="display:flex;align-items:center;gap:4px">${icons.arrowDown}${esc(h.scrollLeft)}</span>`)}</div>
        <div class="hero__scroll hero__scroll--r">${mask(`<span style="display:flex;align-items:center;gap:4px">${esc(h.scrollRight)}${icons.arrowDown}</span>`)}</div>`;
      fitText($(".hero__title"), $$(".hero__word"));

      // Showreel
      const frame = $(".intro__frame");
      frame.innerHTML = `${media(SITE.showreel, ["#3fb6c9", "#0b1316"], SITE.showreel.label)}
        <button class="sound-btn" aria-label="Activer le son">${icons.muted}</button>`;
      const video = $("video", frame);
      const soundBtn = $(".sound-btn", frame);
      if (video) {
        frame.addEventListener("click", () => {
          video.muted = !video.muted;
          soundBtn.innerHTML = video.muted ? icons.muted : icons.sound;
          soundBtn.setAttribute("aria-label", video.muted ? "Activer le son" : "Couper le son");
        });
      } else {
        soundBtn.remove();
      }

      // Moi
      const words = SITE.about.text.split(/\s+/);
      $(".about__label").textContent = SITE.about.label;
      $(".about__text").innerHTML = words.map((w) => `<span class="w">${esc(w)}</span>`).join(" ");
      $(".about__media").innerHTML = media(SITE.about.media, ["#ff5a1f", "#2a0d02"]);

      // Work
      $(".work__head").innerHTML = `${mask(esc(SITE.work.title))}${mask(esc(SITE.work.year))}`;
      $(".work__list").innerHTML = PROJECTS.slice(0, 2).map((p) => `<li>${projectCard(p)}</li>`).join("");
      $(".see-all").innerHTML = `<span>${esc(SITE.work.seeAll)}</span>${icons.arrowRight}`;

      // Services
      const s = SITE.services;
      $(".services__intro").innerHTML = `<div><p class="small-label">${esc(s.label)}</p><p>${esc(s.intro)}</p></div>`;
      $(".services__list").innerHTML = s.items
        .map(
          (it, i) => `<li class="service">
            <p class="service__num">${String(i + 1).padStart(2, "0")}</p>
            <h3 class="service__title">${esc(it.title)}</h3>
            <div class="service__body">
              <p class="service__text">${esc(it.text)}</p>
              <ul class="tags">${it.tags.map((t) => `<li class="tag">${esc(t)}</li>`).join("")}</ul>
            </div>
            <div class="service__media"><div class="service__media-inner">${media(it.media, null)}</div></div>
          </li>`
        )
        .join("");

      // Tech stack
      const st = SITE.stack;
      $(".letters").innerHTML = st.title
        .map((line) => {
          const chars = [...line.toUpperCase()];
          return `<li>${chars
            .map((ch, i) =>
              ch === " "
                ? ""
                : `<span class="letter${chars[i + 1] === " " ? " is-space" : ""}"><span>${esc(ch)}</span><span aria-hidden="true">${esc(ch)}</span></span>`
            )
            .join("")}</li>`;
        })
        .join("");
      $(".stack__label").textContent = st.label;
      const cell = (t) =>
        `<a class="logo-cell" href="${esc(t.url)}" target="_blank" rel="noopener" aria-label="${esc(t.name)}"><img src="assets/icons/${esc(t.icon)}.svg" alt="${esc(t.name)}"></a>`;
      $(".logos").innerHTML = `
        <div class="logos__row logos__row--top">${st.top.map(cell).join("")}</div>
        <div class="logos__row logos__row--bottom">${st.bottom.map(cell).join("")}</div>
        <div class="logos__highlight"></div>`;

      return () => {
        // Entrée du hero
        gsap.from($$(".hero .mask > *"), { yPercent: 100, duration: 1.2, ease: "power4.out", stagger: 0.08 });
        gsap.fromTo(frame, { clipPath: "inset(0 0 100% 0)" }, { clipPath: "inset(0 0 0% 0)", duration: 1.4, ease: "power4.inOut", delay: 0.2 });

        initShowreel(frame);
        initAboutWords();
        initCards($(".work"));
        appear(".work__list > li");
        gsap.from($$(".work__head .mask > *"), {
          yPercent: 100, duration: 1.1, ease: "power4.out", stagger: 0.08,
          scrollTrigger: { trigger: ".work__head", start: "top 85%", once: true },
        });
        tagsIn($(".services"));
        $$(".service__media-inner").forEach((el) => {
          gsap.to(el, {
            clipPath: "polygon(0 0, 100% 0, 100% 100%, 0 100%)", duration: 1.4, ease: "power4.inOut",
            scrollTrigger: { trigger: el.parentElement, start: "top 85%", once: true },
          });
          parallax(el, 3);
        });
        initLetters();
        initLogos();
      };
    },

    work() {
      $(".page-head__years").innerHTML = mask(esc(SITE.workPage.years));
      $(".page-head h1").innerHTML = mask(esc(SITE.workPage.title));
      $(".work-grid").innerHTML = PROJECTS.map((p) => `<div class="work-grid__item">${projectCard(p)}</div>`).join("");
      document.title = `Work — ${SITE.name}`;
      return () => {
        gsap.from($$(".page-head .mask > *"), { yPercent: 100, duration: 1.2, ease: "power4.out", stagger: 0.08 });
        gsap.from(".work-grid", { opacity: 0, y: 24, scale: 0.95, duration: 1, ease: "power3.out", delay: 0.2 });
        appear(".work-grid__item");
        initCards($(".work-grid"));
      };
    },

    project() {
      const slug = new URLSearchParams(location.search).get("p");
      const p = PROJECTS.find((x) => x.slug === slug) || PROJECTS[0];
      document.title = `${p.title} — ${SITE.name}`;

      $(".project__title").innerHTML = mask(esc(p.title));
      $(".project__meta").innerHTML = `
        <div class="meta-year">${mask('<p class="small-label">Année</p>')}${mask(`<p class="meta-value">${esc(p.year)}</p>`)}</div>
        <div class="meta-services">${mask('<p class="small-label">Services</p>')}<ul class="tags">${p.services.map((t) => `<li class="tag">${esc(t)}</li>`).join("")}</ul></div>
        <div class="meta-summary">${mask('<p class="small-label">Résumé</p>')}${mask(`<p class="meta-value">${esc(p.summary)}</p>`)}</div>`;
      $(".project__gallery").innerHTML = (p.gallery || [])
        .map((g) =>
          Array.isArray(g)
            ? `<div class="shot-pair">${g.map((x) => `<div class="shot">${media(x, p.colors)}</div>`).join("")}</div>`
            : `<div class="shot">${media(g, p.colors)}</div>`
        )
        .join("");

      return () => {
        gsap.from(".project__box", { opacity: 0, y: 24, scale: 0.95, duration: 1, ease: "power3.out" });
        gsap.from($$(".project .mask > *"), { yPercent: 100, duration: 1.2, ease: "power4.out", stagger: 0.06, delay: 0.2 });
        tagsIn($(".project"));
        appear(".project__gallery > *", { y: 32 });
      };
    },
  };

  /* ------------------------------------------------------------------------
     Animations spécifiques à l'accueil
     ------------------------------------------------------------------------ */

  // La vidéo part petite en haut du hero (et suit la souris), puis grandit
  // jusqu'à occuper toute la largeur au scroll.
  function initShowreel(frame) {
    const mm = gsap.matchMedia();
    mm.add("(min-width: 1024px)", () => {
      const intro = $(".intro");
      const startScale = 0.35;
      let progress = 0;
      let mouse = 0; // -1 (gauche) → 1 (droite)

      const xTo = gsap.quickTo(frame, "x", { duration: 1, ease: "power3" });
      const followMouse = () => {
        const free = (intro.clientWidth - frame.offsetWidth * startScale) / 2 - 16;
        xTo(mouse * free * (1 - progress));
      };
      const onMove = (e) => { mouse = (e.clientX / window.innerWidth - 0.5) * 2; followMouse(); };
      window.addEventListener("mousemove", onMove);

      gsap.fromTo(frame, { y: () => -(intro.offsetTop - 90), scale: startScale }, {
        y: 0, scale: 1, ease: "none",
        scrollTrigger: {
          trigger: intro, start: "top bottom", end: "top 50px", scrub: true, invalidateOnRefresh: true,
          onUpdate: (self) => { progress = self.progress; followMouse(); },
        },
      });
      return () => window.removeEventListener("mousemove", onMove);
    });
  }

  // Les mots du paragraphe « Moi » sont décalés au hasard puis se recalent au scroll
  function initAboutWords() {
    const words = $$(".about__text .w");
    gsap.fromTo(words, { marginLeft: () => (Math.random() < 0.35 ? 0 : gsap.utils.random(0, 9) + "vw") }, {
      marginLeft: 0, ease: "none",
      scrollTrigger: { trigger: ".about", start: "top 70%", end: "bottom 60%", scrub: true },
    });
  }

  // Chaque lettre « roule » vers le bas pour laisser place à sa copie
  function initLetters() {
    gsap.to($$(".letter"), {
      yPercent: 100, ease: "none",
      stagger: { each: 0.08, from: "random" },
      scrollTrigger: { trigger: ".letters", start: "top 75%", end: "center 45%", scrub: true },
    });
  }

  // Un carré sombre suit la case de logo survolée
  function initLogos() {
    const wrap = $(".logos");
    const hl = $(".logos__highlight", wrap);
    const cells = $$(".logo-cell", wrap);
    const moveTo = (cell) => {
      const a = wrap.getBoundingClientRect();
      const b = cell.getBoundingClientRect();
      Object.assign(hl.style, { left: `${b.left - a.left}px`, top: `${b.top - a.top}px`, width: `${b.width}px`, height: `${b.height}px` });
      cells.forEach((c) => c.classList.toggle("is-active", c === cell));
    };
    cells.forEach((c) => c.addEventListener("mouseenter", () => moveTo(c)));
    wrap.addEventListener("mouseleave", () => moveTo(cells[0]));
    window.addEventListener("resize", () => moveTo($(".logo-cell.is-active", wrap) || cells[0]));
    moveTo(cells[0]);
  }

  function initFooter() {
    gsap.fromTo(".footer__big", { y: () => -vh(10) }, {
      y: () => vh(10), ease: "none",
      scrollTrigger: { trigger: ".footer", start: "top bottom", end: "bottom bottom", scrub: true, invalidateOnRefresh: true },
    });
  }

  /* ------------------------------------------------------------------------
     Boot
     ------------------------------------------------------------------------ */
  renderLayout();
  const start = pages[page] ? pages[page]() : null;
  initScroll();
  initDock();
  initFooter();

  loader(() => {
    if (reduceMotion) return start && start();
    layoutIn();
    if (start) start();
    ScrollTrigger.refresh();
  });
})();
