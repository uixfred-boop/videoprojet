/* Shared, seek-safe animation helpers for the lockin-red look (../../styles/lockin-red/STYLE.md). Loaded once by
   index.html; every sub-composition calls them with its own paused timeline. All tweens are fromTo / absolute values. */
(function () {
  const INK = "#f5f5f5";
  const GHOST = "#9e9e9e"; // lockin-red ghost letters are lighter than listicle-crimson's #6b6b6b
  const all = (sel) => (typeof sel === "string" ? Array.from(document.querySelectorAll(sel)) : [].concat(sel));

  // split an element's text into letter spans (once)
  function split(el) {
    if (el.dataset.split === "1") return Array.from(el.querySelectorAll(".ch"));
    const out = [];
    const walk = (node) => {
      Array.from(node.childNodes).forEach((child) => {
        if (child.nodeType === 3) {
          const frag = document.createDocumentFragment();
          child.textContent.split(/(\s+)/).forEach((part) => {
            if (!part) return;
            if (/^\s+$/.test(part)) {
              frag.appendChild(document.createTextNode(part));
              return;
            }
            const word = document.createElement("span");
            word.className = "wd";
            word.style.display = "inline-block";
            word.style.whiteSpace = "nowrap";
            for (const c of part) {
              const s = document.createElement("span");
              s.className = "ch";
              s.textContent = c;
              word.appendChild(s);
              out.push(s);
            }
            frag.appendChild(word);
          });
          child.replaceWith(frag);
        } else if (child.nodeType === 1 && !child.classList.contains("ch")) {
          walk(child);
        }
      });
    };
    walk(el);
    el.dataset.split = "1";
    return out;
  }

  window.fx = {
    INK,
    GHOST,
    /** Ghost typing (STYLE.md signature): letters show grey + soft, then fill white in order. */
    type(tl, sel, start, per = 0.035, opts = {}) {
      const chars = [];
      all(sel).forEach((el) => chars.push(...split(el)));
      tl.fromTo(
        chars,
        { color: GHOST, opacity: opts.hidden ? 0 : 0.55, filter: "blur(3px)" },
        { color: opts.color || INK, opacity: 1, filter: "blur(0px)", duration: 0.07, ease: "none", stagger: per },
        start,
      );
      return start + chars.length * per;
    },
    /** Type a span of text across a word-timed window (letters spread evenly between t0 and t1). */
    typeSpan(tl, sel, t0, t1, opts = {}) {
      const chars = [];
      all(sel).forEach((el) => chars.push(...split(el)));
      const per = Math.max(0.012, (t1 - t0) / Math.max(1, chars.length));
      return this.type(tl, chars, t0, per, opts);
    },
    blurIn(tl, sel, t, o = {}) {
      tl.fromTo(
        sel,
        { opacity: 0, y: o.y ?? 40, scale: o.scale ?? 0.96, filter: `blur(${o.blur ?? 16}px)` },
        { opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: o.dur ?? 0.5, ease: o.ease || "expo.out", stagger: o.stagger || 0 },
        t,
      );
    },
    pop(tl, sel, t, o = {}) {
      tl.fromTo(
        sel,
        { opacity: 0, scale: o.from ?? 0.4, rotation: o.rot0 ?? 0 },
        { opacity: 1, scale: 1, rotation: o.rot ?? 0, duration: o.dur ?? 0.4, ease: o.ease || "back.out(2)", stagger: o.stagger || 0 },
        t,
      );
    },
    stamp(tl, sel, t, rot = -6) {
      tl.fromTo(sel, { opacity: 0, scale: 2.3, rotation: rot - 10 }, { opacity: 1, scale: 1, rotation: rot, duration: 0.22, ease: "power4.in" }, t);
    },
    /** Paths need pathLength="1" stroke-dasharray="1" stroke-dashoffset="1". */
    draw(tl, sel, t, dur = 0.6, stagger = 0) {
      tl.fromTo(sel, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: dur, ease: "power2.inOut", stagger }, t);
    },
    count(tl, el, from, to, t, dur, fmt) {
      const node = typeof el === "string" ? document.querySelector(el) : el;
      const p = { v: from };
      node.textContent = fmt(from);
      tl.fromTo(p, { v: from }, { v: to, duration: dur, ease: "power2.out", onUpdate: () => (node.textContent = fmt(p.v)) }, t);
    },
    float(tl, sel, t, dur, dy = -14) {
      tl.to(sel, { y: dy, duration: dur / 2, ease: "sine.inOut", yoyo: true, repeat: 1 }, t);
    },
    shake(tl, sel, t, amp = 10) {
      [amp, -amp * 0.9, amp * 0.7, -amp * 0.5, amp * 0.3, 0].forEach((x, i) => tl.to(sel, { x, duration: 0.045, ease: "none" }, t + i * 0.045));
    },
    /** A red title bar or underline growing with the typing (scaleX from its left edge, linear like the letters). */
    grow(tl, sel, t0, t1) {
      tl.fromTo(sel, { scaleX: 0 }, { scaleX: 1, duration: Math.max(0.05, t1 - t0), ease: "none" }, t0);
    },
    /** Ping circle: grows on the focal word, holds a beat, fades. Both tweens wait for their time (immediateRender:
        false), so before the ping the circle keeps its CSS opacity 0 instead of showing as a small dot. */
    ping(tl, sel, t) {
      tl.fromTo(sel, { opacity: 0.95, scale: 0.05 }, { opacity: 0.95, scale: 1, duration: 0.22, ease: "power2.out", immediateRender: false }, t);
      tl.fromTo(sel, { opacity: 0.95, scale: 1 }, { opacity: 0, scale: 1.12, duration: 0.32, ease: "power1.in", immediateRender: false }, t + 0.3);
    },
    /** White sheen sweeping across an active bar. */
    sheen(tl, sel, t, dist = 900) {
      tl.fromTo(sel, { x: -260 }, { x: dist, duration: 0.45, ease: "power2.inOut" }, t);
    },
    /** Slow push-in on the focal panel (never stops in the reference). */
    push(tl, sel, t, dur, to = 1.06) {
      tl.fromTo(sel, { scale: 1 }, { scale: to, duration: dur, ease: "none" }, t);
    },
    /** Green "confirm" flash: two quick pulses of an overlay. */
    flash(tl, sel, t) {
      tl.fromTo(sel, { opacity: 0 }, { opacity: 0.85, duration: 0.06, ease: "none", immediateRender: false }, t);
      tl.to(sel, { opacity: 0.2, duration: 0.1, ease: "none" }, t + 0.08);
      tl.to(sel, { opacity: 0.85, duration: 0.06, ease: "none" }, t + 0.2);
      tl.to(sel, { opacity: 0, duration: 0.18, ease: "none" }, t + 0.3);
    },
    /** Ambient drift for the shared background layer of a scene. */
    ambient(tl, root, dur) {
      const grid = root.querySelector(".lc-grid");
      const aura = root.querySelector(".lc-aura");
      if (grid) tl.fromTo(grid, { y: 0 }, { y: 40, duration: dur, ease: "none" }, 0);
      if (aura) tl.fromTo(aura, { scale: 0.88, opacity: 0.7 }, { scale: 1.08, opacity: 1, duration: dur, ease: "sine.inOut" }, 0);
    },
  };
})();
