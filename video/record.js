// Records the guided demo of the interactive ebook.
// Usage: node record.js <url> <outDir>   (needs Playwright; frames are captured with the CDP screencast)
const fs = require("fs");
const path = require("path");
const { chromium } = require(process.env.PWPATH || "playwright");

const URL = process.argv[2] || "http://127.0.0.1:8123/index.html";
const OUT = process.argv[3] || path.join(__dirname, "frames");
const W = 1440, H = 810, DSF = 4 / 3; // 1920x1080 output

const OVERLAY_CSS = `
#demo-cursor { position: fixed; left: 0; top: 0; width: 26px; height: 26px; z-index: 99999; pointer-events: none; transform: translate(-100px,-100px); transition: none; }
#demo-cursor svg { width: 26px; height: 26px; filter: drop-shadow(0 2px 3px rgba(0,0,0,.25)); transition: transform .12s; transform-origin: 4px 3px; }
#demo-cursor.down svg { transform: scale(.82); }
.demo-ripple { position: fixed; z-index: 99998; width: 44px; height: 44px; margin: -22px 0 0 -22px; border-radius: 50%; border: 2px solid #AE5230; pointer-events: none; animation: demoRip .55s ease-out forwards; }
@keyframes demoRip { from { transform: scale(.2); opacity: .9 } to { transform: scale(1.4); opacity: 0 } }
#demo-cap { position: fixed; right: 28px; bottom: 28px; z-index: 99990; width: 430px; pointer-events: none;
  background: #FBF8F2; border: 1px solid #E3D9C8; border-left: 3px solid #AE5230; border-radius: 4px 12px 12px 4px;
  box-shadow: 0 18px 40px -18px rgba(60,35,20,.45); padding: 18px 22px 20px; display: grid; gap: 6px;
  opacity: 0; transform: translateY(14px); transition: opacity .45s ease, transform .45s ease; }
#demo-cap.on { opacity: 1; transform: none; }
#demo-cap.top { bottom: auto; top: 28px; }
#demo-cap .e { font: 600 11px/1.3 Inter, sans-serif; letter-spacing: .16em; text-transform: uppercase; color: #AE5230; }
#demo-cap .t { font: 400 21px/1.35 Lora, Georgia, serif; color: #1F1A15; }
#demo-card { position: fixed; inset: 0; z-index: 99995; display: grid; align-content: center; padding: 0 160px; gap: 0;
  background-color: #EDE3D2; background-image: linear-gradient(#E5DAC7 1px, transparent 1px), linear-gradient(90deg, #E5DAC7 1px, transparent 1px); background-size: 36px 36px;
  transition: opacity .8s ease; }
#demo-card.out { opacity: 0; }
#demo-card > * { opacity: 0; transform: translateY(18px); animation: demoIn .9s cubic-bezier(.2,.7,.2,1) forwards; }
@keyframes demoIn { to { opacity: 1; transform: none } }
#demo-card .e { font: 600 13px/1 Inter, sans-serif; letter-spacing: .2em; text-transform: uppercase; color: #AE5230; padding-bottom: 18px; border-bottom: 1px solid #C9B699; max-width: 1120px; display: flex; justify-content: space-between; }
#demo-card h1 { font: 500 112px/0.98 Lora, Georgia, serif; color: #1F1A15; margin: 70px 0 0; letter-spacing: -.01em; }
#demo-card h1 em { display: block; color: #AE5230; font-style: italic; }
#demo-card .s { font: 400 24px/1.5 Lora, Georgia, serif; font-style: italic; color: #736C64; margin-top: 40px; }
#demo-card .row { display: flex; gap: 40px; margin-top: 46px; padding-top: 22px; border-top: 1px solid #C9B699; max-width: 1120px; }
#demo-card .row div { font: 600 12px/1.4 Inter, sans-serif; letter-spacing: .14em; text-transform: uppercase; color: #736C64; }
#demo-card .row b { display: block; font: 400 40px/1.1 Lora, Georgia, serif; color: #1F1A15; letter-spacing: 0; text-transform: none; margin-bottom: 6px; }
#demo-card .row div:last-child b { color: #AE5230; }
#demo-card .fin { font: 400 96px/1.05 Lora, Georgia, serif; font-style: italic; color: #1F1A15; margin: 0; }
#demo-card .sig { font: 400 30px/1.3 Lora, Georgia, serif; color: #736C64; margin-top: 18px; }
#demo-card .hdl { font: 600 14px/1 Inter, sans-serif; letter-spacing: .16em; text-transform: uppercase; color: #AE5230; margin-top: 60px; }
#demo-stage { position: fixed; inset: 0; z-index: 99994; display: grid; grid-template-columns: minmax(380px, 1fr) auto; align-items: center; gap: 70px; padding: 0 100px;
  background-color: #EDE3D2; background-image: linear-gradient(#E5DAC7 1px, transparent 1px), linear-gradient(90deg, #E5DAC7 1px, transparent 1px); background-size: 36px 36px;
  opacity: 0; transition: opacity .7s ease; }
#demo-stage.on { opacity: 1; }
#demo-stage .txt { display: grid; gap: 22px; }
#demo-stage .txt .e { font: 600 12px/1 Inter, sans-serif; letter-spacing: .18em; text-transform: uppercase; color: #AE5230; }
#demo-stage .txt h2 { font: 500 50px/1.08 Lora, Georgia, serif; color: #1F1A15; margin: 0; }
#demo-stage .txt h2 em { color: #AE5230; }
#demo-stage .txt p { font: 400 19px/1.55 Inter, sans-serif; color: #2F2822; margin: 0; max-width: 420px; }
#demo-stage .phones { display: flex; gap: 34px; }
#demo-stage .phone { width: 342px; height: 724px; border-radius: 46px; background: #1F1A15; padding: 11px; box-shadow: 0 30px 60px -28px rgba(50,30,15,.6); }
#demo-stage .screen { width: 320px; height: 702px; border-radius: 36px; overflow: hidden; position: relative; background: #F4EDE1; }
#demo-stage iframe { width: 390px; height: 856px; border: 0; transform: scale(.8205); transform-origin: 0 0; position: absolute; left: 0; top: 0; }
#demo-stage .lbl { text-align: center; font: 600 11px/1 Inter, sans-serif; letter-spacing: .16em; text-transform: uppercase; color: #736C64; margin-top: 14px; }
`;

const CURSOR_SVG = `<svg viewBox="0 0 24 24"><path d="M4 2.5 L4 19.5 L8.6 15.2 L11.6 21.6 L14.6 20.2 L11.7 13.9 L18 13.6 Z" fill="#1F1A15" stroke="#FBF8F2" stroke-width="1.4" stroke-linejoin="round"/></svg>`;

(async () => {
  fs.rmSync(OUT, { recursive: true, force: true });
  fs.mkdirSync(OUT, { recursive: true });

  const browser = await chromium.launch();
  const context = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: DSF, colorScheme: "light" });
  // Controllable clock so the 25-minute call timer can be shown quickly.
  await context.addInitScript(() => {
    const realNow = Date.now.bind(Date);
    let last = realNow(), virt = last, speed = 1;
    Date.now = () => { const r = realNow(); virt += (r - last) * speed; last = r; return Math.floor(virt); };
    window.__setSpeed = (s) => { Date.now(); speed = s; };
  });
  const page = await context.newPage();
  await page.goto(URL);
  await page.evaluate(() => document.fonts.ready);

  await page.addStyleTag({ content: OVERLAY_CSS });
  await page.evaluate((svg) => {
    const c = document.createElement("div"); c.id = "demo-cursor"; c.innerHTML = svg; document.body.appendChild(c);
    document.addEventListener("mousemove", (e) => { c.style.transform = `translate(${e.clientX - 4}px, ${e.clientY - 3}px)`; }, true);
    const cap = document.createElement("div"); cap.id = "demo-cap"; cap.innerHTML = '<span class="e"></span><span class="t"></span>'; document.body.appendChild(cap);
    window.__scroll = (to, ms) => new Promise((res) => {
      const from = window.scrollY, d = to - from, t0 = performance.now();
      const ease = (t) => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      (function step(now) {
        const t = Math.min(1, (now - t0) / ms);
        window.scrollTo({ top: from + d * ease(t), behavior: "instant" });
        t < 1 ? requestAnimationFrame(step) : res();
      })(t0);
    });
  }, CURSOR_SVG);

  // ---------- capture ----------
  const cdp = await context.newCDPSession(page);
  let n = 0; const stamps = [];
  cdp.on("Page.screencastFrame", async (f) => {
    const file = path.join(OUT, String(n).padStart(6, "0") + ".jpg");
    fs.writeFileSync(file, Buffer.from(f.data, "base64"));
    stamps.push(f.metadata.timestamp); n++;
    try { await cdp.send("Page.screencastFrameAck", { sessionId: f.sessionId }); } catch (e) {}
  });

  // ---------- helpers ----------
  const wait = (ms) => page.waitForTimeout(ms);
  let mx = W / 2, my = H / 2;
  async function moveTo(x, y, ms = 650) {
    const steps = Math.max(8, Math.round(ms / 16)), sx = mx, sy = my;
    for (let i = 1; i <= steps; i++) {
      const t = i / steps, e = t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
      await page.mouse.move(sx + (x - sx) * e, sy + (y - sy) * e);
      await wait(16);
    }
    mx = x; my = y;
  }
  async function box(sel) {
    const l = typeof sel === "string" ? page.locator(sel).first() : sel;
    await l.scrollIntoViewIfNeeded();
    return l.boundingBox();
  }
  async function hover(sel, ms) { const b = await box(sel); await moveTo(b.x + b.width / 2, b.y + b.height / 2, ms); }
  async function click(sel, ms) {
    const l = typeof sel === "string" ? page.locator(sel).first() : sel;
    await hover(l, ms); await wait(120);
    await page.evaluate(([x, y]) => {
      document.getElementById("demo-cursor").classList.add("down");
      const r = document.createElement("div"); r.className = "demo-ripple"; r.style.left = x + "px"; r.style.top = y + "px";
      document.body.appendChild(r); setTimeout(() => r.remove(), 700);
    }, [mx, my]);
    await l.click();
    await wait(110);
    await page.evaluate(() => document.getElementById("demo-cursor").classList.remove("down"));
  }
  async function type(sel, text, delay = 55) {
    const l = page.locator(sel).first();
    await click(l);
    await l.fill("");
    await l.pressSequentially(text, { delay });
  }
  async function pick(sel, label) { const l = page.locator(sel).first(); await click(l); await wait(200); await l.selectOption(label); }
  async function scrollEl(sel, offset = 90, ms = 1300) {
    const y = await page.evaluate(([s, o]) => { const el = document.querySelector(s); return el.getBoundingClientRect().top + window.scrollY - o; }, [sel, offset]);
    await page.evaluate(([y, ms]) => window.__scroll(y, ms), [y, ms]); await wait(100);
  }
  async function scrollBy(dy, ms = 1500) { await page.evaluate(([dy, ms]) => window.__scroll(window.scrollY + dy, ms), [dy, ms]); }
  async function cap(e, t, top = false) {
    await page.evaluate(([e, t, top]) => {
      const c = document.getElementById("demo-cap");
      const show = () => { c.classList.toggle("top", top); c.querySelector(".e").textContent = e; c.querySelector(".t").textContent = t; c.classList.add("on"); };
      if (c.classList.contains("on")) { c.classList.remove("on"); setTimeout(show, 380); } else show();
    }, [e, t, top]);
    await wait(450);
  }
  async function capOff() { await page.evaluate(() => document.getElementById("demo-cap").classList.remove("on")); await wait(400); }
  async function card(html, hold) {
    await page.evaluate((html) => {
      const c = document.createElement("div"); c.id = "demo-card"; c.innerHTML = html; document.body.appendChild(c);
      [...c.children].forEach((el, i) => { el.style.animationDelay = (0.25 + i * 0.22) + "s"; });
    }, html);
    await wait(hold);
  }
  async function cardOut() { await page.evaluate(() => { const c = document.getElementById("demo-card"); c.classList.add("out"); setTimeout(() => c.remove(), 900); }); await wait(900); }

  await cdp.send("Page.startScreencast", { format: "jpeg", quality: 92, maxWidth: 1920, maxHeight: 1080, everyNthFrame: 1 });

  // ================= 0. Title card =================
  await card(`
    <div class="e"><span>Introducing</span><span>Interactive edition</span></div>
    <h1>First Client <em>Playbook</em></h1>
    <p class="s">The guide that reads like a book, and works like an app.</p>
    <div class="row"><div><b>8</b>steps</div><div><b>6</b>live templates</div><div><b>0</b>setup &middot; saves as you go</div></div>`, 5200);
  await page.mouse.move(mx, my);
  await cardOut();

  // ================= 1. Cover =================
  await cap("Interactive edition", "The 27-page PDF, rebuilt as a living ebook. Same fonts, same colors, same feel.", true);
  await moveTo(700, 300, 900); await wait(900);
  await hover("#startBtn", 900); await wait(1600);
  await click("#startBtn"); await wait(1400);

  // ================= 2. Intro + progress =================
  await cap("Read at your pace", "Every chapter of the guide, in one calm reading column.");
  await moveTo(1180, 420, 700);
  await scrollBy(700, 3200); await wait(800);
  await scrollEl('[data-done-for="intro"]', 420, 1800);
  await cap("Track your progress", "Mark each chapter as done. The contents rail keeps score.");
  await click('[data-toggle-done="intro"]', 900); await wait(700);
  await hover('#toc a[data-id="intro"]', 900); await wait(900);
  await hover("#progressTxt", 700); await wait(1200);

  // ================= 3. Method =================
  await click('#toc a[data-id="method"]', 700); await wait(1500);
  await cap("Click to navigate", "The method map links straight to every step.");
  await scrollEl("#method .flow", 140, 1000);
  for (const s of ['#method .flow-row:first-of-type .flow-box:nth-child(1)', '#method .flow-row:first-of-type .flow-box:nth-child(2)', '#method .flow-row:first-of-type .flow-box:nth-child(4)']) { await hover(s, 550); await wait(500); }
  await hover(page.locator("#method .flow-row").nth(1).locator(".flow-box").nth(2), 550); await wait(600);
  await scrollEl("#stepsGrid", 160, 1000);
  await hover('.step-card[data-id="step2"]', 500); await wait(400);
  await hover('.step-card[data-id="step4"]', 500); await wait(400);
  await click('.step-card[data-id="step1"]', 500); await wait(1500);

  // ================= 4. Niche scorer =================
  await scrollEl("#nicheTbl", 220, 1500);
  await cap("Step 01 · Niche scorer", "Score your options on the 4 tests. The best total is picked for you.");
  await wait(600);
  const last = '#nicheTbl tbody tr:last-child';
  await type(`${last} input[data-f="name"]`, "Roofing companies", 60);
  const scores = ["5", "5", "4", "4"];
  for (let i = 0; i < 4; i++) { await pick(`${last} select[data-f="s${i}"]`, scores[i]); await wait(380); }
  await moveTo(mx + 60, my + 30, 400);
  await wait(1800);
  await scrollEl('#step1 [data-k="niche"]', 300, 1200);
  await cap("Fill it once", "Your niche flows into the emails, scripts and quote later on.");
  await type('#step1 [data-k="niche"]', "roofing companies");
  await type('#step1 [data-k="country"]', "Germany");
  await wait(900);

  // ================= 5. Find prospects =================
  await scrollEl('#step3 .tool', 110, 1800);
  await cap("Step 03 · Find prospects", "Build Google Maps searches for every target city in one go.");
  await type('#step3 [data-k="searchTerm"]', "Dachdecker", 70);
  await type('#step3 [data-k="searchCities"]', "München, Berlin, Hamburg, Köln", 45);
  await wait(500);
  await hover("#searchLinks li:nth-child(2) a", 600); await wait(1200);
  await scrollEl('#step3 .checks', 240, 1400);
  await cap("Qualify each site", "Tick the signs of a weak website. The verdict updates live.");
  for (const k of ["weak1", "weak3", "weak4"]) { await click(`#step3 label:has([data-k="${k}"])`, 450); await wait(500); }
  await hover("#weakVerdict", 500); await wait(1500);

  // ================= 6. Price =================
  await click('#toc a[data-id="step6"]', 700); await wait(1400);
  await scrollEl("#step6 .tool", 70, 1500);
  await cap("Step 06 · Price calculator", "Price on value: 10 to 15% of what one new client is worth.");
  await type('#step6 [data-k="clientValue"]', "40000", 110); await wait(900);
  await type('#step6 [data-k="price"]', "2500", 120); await wait(1600);
  await hover("#pVerdict", 500); await wait(1400);
  await type('#step6 [data-k="price"]', "5000", 120); await wait(600);
  await hover("#gDot", 600); await wait(1800);
  await scrollEl('#step6 [data-out="range"]', 330, 1600);
  await cap("Connected", "Your price range is written into the call scripts automatically.");
  await hover('#step6 [data-out="range"]', 700); await wait(2000);

  // ================= 7. Payment plan =================
  await scrollEl('#step7 .fields', 230, 1600);
  await cap("Step 07 · Payment plan", "Set your deposit. The plan and the balance follow.");
  await type('#step7 [data-k="deposit"]', "1000", 120); await wait(700);
  await hover('#step7 [data-out="balanceFmt"]', 700); await wait(1400);
  await scrollEl('#step7 .checks', 240, 1400);
  for (const k of ["c1", "c2", "c3"]) { await click(`#step7 label:has([data-k="${k}"])`, 400); await wait(300); }
  await wait(800);

  // ================= 8. Plan =================
  await click('#toc a[data-id="plan"]', 700); await wait(1400);
  await scrollEl("#plan .progress", 120, 900);
  await cap("30-day action plan", "One small task a day, ticked off as you go.");
  for (let d = 1; d <= 5; d++) { await click(`#planWeeks label:has([data-k="d${d}"])`, 380); await wait(260); }
  await hover("#planTxt", 600); await wait(1500);

  // ================= 9. Troubleshoot =================
  await click('#toc a[data-id="trouble"]', 600); await wait(1300);
  await cap("If it does not work yet", "Answers to the common objections, one click away.");
  await click("#trouble details:nth-child(3) summary", 600); await wait(1500);
  await click("#trouble details:nth-child(4) summary", 500); await wait(1600);

  // ================= 10. Email builder =================
  await click('#toc a[data-id="t1"]', 700); await wait(1400);
  await scrollEl("#t1 .tool", 90, 900);
  await cap("Template 1 · Cold email builder", "Type your details once. Every [bracket] fills itself in.");
  await type('#t1 [data-k="yourName"]', "Fred");
  await type('#t1 [data-k="portfolio"]', "fred.design", 45);
  await type('#t1 [data-k="caseLink"]', "fred.design/roofing", 40);
  await scrollEl("#t1 .tool:nth-of-type(2)", 90, 1200);
  await cap("Linked to your tracker", "Pick a company from the tracker. Its name, city and problem drop in.");
  await pick("#fromTracker", "Musterbau GmbH"); await wait(1300);
  await type('#t1 [data-k="lastName"]', "Mr. Mustermann");
  await type('#t1 [data-k="work"]', "family homes");
  await scrollEl("#subjects", 160, 1500);
  await cap("Ready to send", "Choose a subject line, then copy the whole email in one click.");
  await click('#subjects label:nth-child(5)', 600); await wait(800);
  await scrollBy(300, 1300); await wait(1500);
  await click('[data-copy="email1"]', 700); await wait(1800);

  // ================= 11. Call timer =================
  await click('#toc a[data-id="t2"]', 700); await wait(1400);
  await scrollEl("#t2 .tool", 80, 900);
  await cap("Template 2 · Call timer", "A 25-minute call script. The part you are on lights up.");
  await click("#tStart", 700);
  await page.evaluate(() => window.__setSpeed(50));
  await wait(1800);
  await scrollEl("#script", 230, 2600); await wait(2600);
  await scrollBy(260, 3000); await wait(3500);
  await scrollBy(300, 3000); await wait(4500);
  await page.evaluate(() => window.__setSpeed(1));
  await scrollEl("#t2 .tool", 80, 1200);
  await click("#tStart", 600); await wait(1200);

  // ================= 12. Quote =================
  await click('#toc a[data-id="t3"]', 700); await wait(1400);
  await scrollEl("#t3 .tool", 80, 900);
  await cap("Template 3 · Quote generator", "Fill in the client. A clean quote builds itself, with your price.");
  await type('#t3 [data-k="qCompany"]', "Musterbau GmbH");
  await type('#t3 [data-k="qContact"]', "Max Mustermann");
  await type('#t3 [data-k="qAddress"]', "Musterstraße 1, 80331 München", 40);
  await scrollEl("#quoteDoc", 40, 2000); await wait(1500);
  await moveTo(1000, 520, 800); await wait(600);
  await scrollBy(420, 2600); await wait(1500);
  await click('[data-copy="quoteDoc"]', 700); await wait(1600);

  // ================= 13. Tracker =================
  await click('#toc a[data-id="t4"]', 700); await wait(1400);
  await scrollEl("#kpis", 110, 900);
  await cap("Template 4 · Prospect tracker", "Your pipeline at a glance: sent, replies, calls, signed.");
  await wait(1200);
  await click("#addProspect", 700); await wait(500);
  const row = "#trackTbl tbody tr:last-child";
  await type(`${row} [data-f="company"]`, "Dach Weber", 60);
  await type(`${row} [data-f="city"]`, "Berlin", 60);
  await type(`${row} [data-f="problem"]`, "No project photos", 45);
  await type(`${row} [data-f="email"]`, "info@dachweber.de", 40);
  await cap("Automatic follow-ups", "Set the sent date: the follow-up date fills itself in, 2 days later.");
  const today = await page.evaluate(() => { const d = new Date(); return new Date(d - d.getTimezoneOffset() * 6e4).toISOString().slice(0, 10); });
  await click(`${row} [data-f="sent"]`, 500); await page.locator(`${row} [data-f="sent"]`).fill(today); await page.locator(`${row} [data-f="sent"]`).dispatchEvent("change"); await wait(500);
  await hover(`${row} [data-f="follow"]`, 600); await wait(1500);
  await hover("#kpis", 700); await wait(1000);
  await pick(`${row} [data-f="status"]`, "Replied"); await wait(1200);
  await pick(`${row} [data-f="status"]`, "Call booked"); await wait(900);
  await hover("#kpis > div:nth-child(4)", 700); await wait(1500);
  await cap("Take it anywhere", "Copy the whole table straight into Google Sheets.");
  await click("#copyTsv", 700); await wait(1800);

  // ================= 14. Portfolio checklist =================
  await click('#toc a[data-id="t5"]', 700); await wait(1400);
  await scrollEl("#t5 .progress", 120, 900);
  await cap("Template 5 · Portfolio checklist", "Check your portfolio before you publish it.");
  for (let i = 1; i <= 10; i++) { await click(`#pfChecks label:has([data-k="pf${i}"])`, 260); await wait(120); }
  await hover("#pfTxt", 600); await wait(1500);

  // ================= 15. Testimonial =================
  await click('#toc a[data-id="t6"]', 700); await wait(1400);
  await cap("Template 6 · Testimonial request", "One month after launch, ask for results in two clicks.");
  await type('#t6 [data-k="clientName"]', "Max", 90); await wait(500);
  await hover('[data-copy="email3"]', 700); await wait(1700);

  // ================= 16. Progress recap =================
  for (const id of ["method", "step1", "step3", "step6", "step7", "t1", "t2", "t3", "t4", "t5"]) await page.evaluate((id) => document.querySelector(`[data-toggle-done="${id}"]`).click(), id);
  await cap("Saves as you go", "Close the tab, come back tomorrow. Everything is where you left it.");
  await hover("#progressTxt", 900); await wait(800);
  await moveTo(140, 470, 1200); await wait(1600);
  await capOff();

  // ================= 17. Phones =================
  await page.evaluate(() => {
    const s = document.createElement("div"); s.id = "demo-stage";
    s.innerHTML = `<div class="txt"><span class="e">Any screen, any theme</span><h2>Reads like a book.<br><em>Works like an app.</em></h2><p>On a laptop or on a phone, in light or dark mode. No download, no login.</p></div>
      <div class="phones"><div><div class="phone"><div class="screen"><iframe src="index.html#t1"></iframe></div></div><div class="lbl">Light</div></div>
      <div><div class="phone"><div class="screen"><iframe src="index.html#t1"></iframe></div></div><div class="lbl">Dark</div></div></div>`;
    document.body.appendChild(s);
  });
  await page.waitForFunction(() => [...document.querySelectorAll("#demo-stage iframe")].every((f) => f.contentDocument && f.contentDocument.readyState === "complete" && f.contentDocument.querySelector("#email1 p")));
  await page.evaluate(() => {
    const fr = [...document.querySelectorAll("#demo-stage iframe")];
    fr[0].contentDocument.documentElement.dataset.theme = "light";
    fr[1].contentDocument.documentElement.dataset.theme = "dark";
    fr.forEach((f) => { f.contentDocument.documentElement.style.scrollBehavior = "auto"; const y = f.contentDocument.getElementById("cover").offsetTop; f.contentWindow.scrollTo(0, y); });
  });
  await wait(300);
  await page.evaluate(() => document.getElementById("demo-stage").classList.add("on"));
  await page.evaluate(() => { document.getElementById("demo-cursor").style.visibility = "hidden"; });
  await wait(1800);
  const phoneScroll = (sel, ms) => page.evaluate(([sel, ms]) => Promise.all([...document.querySelectorAll("#demo-stage iframe")].map((f) => new Promise((res) => {
    const w = f.contentWindow, d = f.contentDocument, el = d.querySelector(sel);
    const to = el.getBoundingClientRect().top + w.scrollY - 60, from = w.scrollY, t0 = performance.now();
    (function step(now) { const t = Math.min(1, (now - t0) / ms), e = t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; w.scrollTo(0, from + (to - from) * e); t < 1 ? requestAnimationFrame(step) : res(); })(t0);
  }))), [sel, ms]);
  await phoneScroll("#method .flow", 2200); await wait(1200);
  await phoneScroll("#step6 .tool", 2400); await wait(1400);
  await phoneScroll("#t4 .kpis", 2400); await wait(1400);
  await page.evaluate(() => [...document.querySelectorAll("#demo-stage iframe")].forEach((f) => f.contentDocument.getElementById("navToggle").click()));
  await wait(2400);

  // ================= 18. Outro =================
  await card(`
    <div class="e"><span>First Client Playbook</span><span>Interactive edition</span></div>
    <p class="fin" style="margin-top:70px">Go get your<br>first client.</p>
    <p class="sig">Fred</p>
    <p class="hdl">@ui_fred_designer</p>`, 5500);

  await cdp.send("Page.stopScreencast");
  await wait(300);
  fs.writeFileSync(path.join(OUT, "stamps.json"), JSON.stringify(stamps));
  console.log("frames:", n, "duration:", (stamps[stamps.length - 1] - stamps[0]).toFixed(1) + "s");
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
