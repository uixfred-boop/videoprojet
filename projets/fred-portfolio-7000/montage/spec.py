"""Spécification de montage des 6 shorts (plan validé par l'utilisateur).

Chaque scène couvre une suite de blocs de sous-titres (« lockups »).
Balisage d'un lockup :
  {b:..} mot clé Inter Black      {i:..} mot clé serif italique
  {s:..} mot clé serif condensée  {x:..} boîte bleue (serif italique)
  {m:..} surligneur (barre derrière) {g:..} mot clé en retrait (gris)
  préfixe ">" : lockup entre guillemets géants
La scène commence à l'attaque du premier mot de son premier lockup.
"""

FACE = "face"  # params: cx, cy, zoom (recadrage de la carte visage dans le rush 1920x1080)
LEFT = dict(cx=470)          # Fred décalé à gauche (52,5 s → 60,4 s)
PUNCH = dict(zoom=1.22, cy=540)  # punch-in, exclut aussi les encarts incrustés bas-gauche

SHORTS = {
 "short1": dict(
  titre="The $7,000 question", segments=[(0.0, 11.58), (218.28, 234.32)],
  cta=("PORTFOLIO", "and I'll send you the template."),
  scenes=[
   dict(type=FACE, caps=["This portfolio got me {b:$7,000} on one single client."]),
   dict(type=FACE, caps=["But on the call,", "the client asked me {i:one question:}"]),
   dict(type="plate", bg="blue", caps=[">Have you ever done a project {i:like mine?}"]),
   dict(type=FACE, **PUNCH, revealAt=9.08, caps=["And honestly,", "the answer was {b:no.}"]),
   dict(type="plate", bg="navy", caps=["Looking back,"]),
   dict(type=FACE, revealAt=220.05, caps=["this portfolio didn't make me", "a {i:better designer.}"]),
   dict(type="plate", bg="paper", caps=["It didn't teach me {s:a new skill.}"]),
   dict(type=FACE, caps=["I was the exact {b:same} designer."]),
   dict(type="line", variant="thin", caps=["The only thing that changed", "was how a client {i:saw my work.}"]),
   dict(type="plate", bg="blue", caps=["And for me, that difference", "was worth {s:$7,000.}"]),
  ]),
 "short2": dict(
  titre="Millions of views, zero clients", segments=[(25.58, 60.34)],
  cta=("PORTFOLIO", "and I'll send you the template."),
  scenes=[
   dict(type="illustration", caps=["For a long time,", "I made the most classic {s:mistake}", "on the internet:"]),
   dict(type=FACE, revealAt=28.92, caps=["chasing views", "instead of chasing {x:value.}"]),
   dict(type="reels", caps=["I had {b:millions} of views on Instagram."]),
   dict(type="plate", bg="paper", caps=["Likes, comments, but {b:zero clients.}"]),
   dict(type="strike", hide=True, items=[["0 clients", None], ["A system to find them", "No"], ["Real projects", "real"]],
        caps=["No system to find them,", "no real projects."]),
   dict(type=FACE, revealAt=38.0, caps=["So I wanted to {b:prove} something to myself:", "that I could design something good and smart", "to land {x:a real big client.}"]),
   dict(type="plate", bg="blue", caps=["Before designing anything,", "I asked myself {i:one simple question:}"]),
   dict(type="plate", bg="paper", caps=[">What actually makes a client {s:say yes?}"]),
   dict(type=FACE, cxAt=[[0, 940], [52.5, 470]], caps=["It's not the {g:prettiest design.}", "It's not the {g:lowest price.}"]),
   dict(type="plate", bg="blue", caps=["It's the moment they think:", ">This guy gets my {m:business.}"]),
   dict(type=FACE, **LEFT, zoom=1.2, caps=["Without them having", "to {i:explain a thing.}"]),
  ]),
 "short3": dict(
  titre="Why I chose construction", segments=[(63.30, 97.18)],
  cta=("PORTFOLIO", "and I'll send you the template."),
  scenes=[
   dict(type=FACE, caps=["The first decision it forced me to make", "had {b:nothing} to do with design."]),
   dict(type="photo", src="iran_workers.jpg", focus=[0.62, 0.5], caps=["I chose one industry:", "{s:construction.}"]),
   dict(type="plate", bg="navy", num="3", caps=["For three reasons."]),
   dict(type="plate", bg="blue", num="01", caps=["First, {i:real money.}", "A single new project", "can pay for {x:the whole website.}"]),
   dict(type="photo", src="nara_silhouettes.jpg", focus=[0.5, 0.45], num="02", caps=["Second, they don't have time", "for the {b:tech side.}"]),
   dict(type="stack", caps=["And their clients choose them", "based on {i:past projects.}"]),
   dict(type=FACE, caps=["So a website that really shows off their work?", "That's {i:gold.}"]),
   dict(type="plate", bg="paper", num="03", caps=["Three,", "premium work means {s:premium prices.}", "And that choice"]),
   dict(type=FACE, **PUNCH, caps=["changed {i:everything.}", "I wasn't making a portfolio anymore."]),
   dict(type="screen", src="scr_hero.mp4", phone=True, caps=["I was making the portfolio", "a construction business owner", "would actually {x:want to open.}"]),
  ]),
 "short4": dict(
  titre="Don't add. Remove.", segments=[(97.18, 131.28)],
  cta=("PORTFOLIO", "and I'll send you the template."),
  scenes=[
   dict(type="screen", src="scr_grid.mp4", caps=["I studied a lot of portfolios.", "The best ones didn't use {i:fancy effects.}"]),
   dict(type="plate", bg="blue", caps=["They controlled your {s:attention.}"]),
   dict(type="line", variant="thick", caps=["What you look at {i:first,}", "what you look at {i:next,}", "and why you {i:keep scrolling.}"]),
   dict(type="plate", bg="paper", caps=["That's when it hit me.", "I wasn't designing {s:pages.}"]),
   dict(type="line", variant="thick", chips=["What do you do?", "Show me.", "What's in it for me?", "Shall we talk?"],
        caps=["I was designing {i:a path.}", "A path that answers the client's questions", "{i:one by one,}", "before he even asks them."]),
   dict(type="plate", bg="blue", caps=["So instead of asking myself", ">What can I {g:add?}", "I asked", ">What can I {s:remove?}"]),
   dict(type="plate", bg="paper", caps=["{s:Fewer colors.}", "{s:Less decoration.}", "{s:More space.}", "And way more room for {i:the visuals.}", "Because if your work is good,"]),
   dict(type="screen", src="scr_site.mp4", caps=["you don't need to {b:shout.}", "You just need to give it {i:the right stage.}"]),
  ]),
 "short5": dict(
  titre="Details nobody notices", segments=[(131.28, 158.50), (176.90, 182.48)],
  cta=("PORTFOLIO", "and I'll send you the template."),
  scenes=[
   dict(type="screen", src="scr_hero.mp4", morph=True, caps=["Then I designed everything {b:mobile-first,}", "because your future client", "won't open your site on a big screen."]),
   dict(type="photo", src="iran_workers.jpg", focus=[0.3, 0.5], phoneOverlay="scr_mobile.mp4", caps=["He'll open it on his phone,", "{i:between two job sites.}"]),
   dict(type="screen", src="scr_mobile.mp4", phone=True, caps=["I built it in {i:Framer.}", "Transitions that pull you forward.", "{i:Motion} you feel", "without really noticing it."]),
   dict(type="dimension", src="scr_editor.mp4", caps=["I spent hours on things", "nobody will ever see.", "{b:Three pixels} here.", "A transition that's", "a hair too fast there."]),
   dict(type="plate", bg="blue", caps=["But all those little details", "nobody notices one by one", "add up to {m:a feeling}", "everyone notices."]),
   dict(type="converge", caps=["For the first time,", "the strategy and design", "were pulling in the same direction."]),
   dict(type=FACE, caps=["And I was {i:proud} of it."]),
  ]),
 "short6": dict(
  titre="Have a clear persona", segments=[(184.94, 218.28)],
  cta=("SYSTEM", "and I'll send you the system."),
  scenes=[
   # encart incrusté sur la bouche de 185,9 à 189,6 s : pas de visage sur ce passage
   dict(type=FACE, caps=["A portfolio,"]),
   dict(type="screen", src="scr_site.mp4", caps=["no matter how good it looks,"]),
   dict(type="plate", bg="navy", caps=["is {b:worthless}", "{x:until it brings you a client.}"]),
   dict(type="plate", bg="paper", caps=["Since I knew {i:exactly}"]),
   dict(type=FACE, revealAt=191.35, caps=["who I'd built this site for,", "I knew {i:exactly} who to contact."]),
   dict(type="photo", src="nara_silhouettes.jpg", focus=[0.5, 0.4], caps=["{s:Construction companies.}"]),
   dict(type="plate", bg="paper", caps=["{s:Nobody else.}"]),
   dict(type=FACE, **PUNCH, caps=["And this is the most {b:important} advice", "in this whole video:"]),
   dict(type="plate", bg="blue", caps=["have a clear {s:persona.}"]),
   dict(type="dots", label="Construction business owner", caps=["If you talk to {i:everyone,}", "nobody feels like", "you're talking to them."]),
   dict(type="steps", nodes=[["Outreach", "reached"], ["1 reply", "replied."], ["Discovery call", "discovery"]],
        caps=["So that's who I reached out to.", "And one of them replied.", "He wanted a discovery call."]),
   dict(type="plate", bg="blue", caps=["My system {s:worked.}", "And by the way,"]),
   # encart incrusté + visage décalé vers 216-218 s : fin sur fond clair
   dict(type="plate", bg="paper", caps=["you'll find this system", "in the {i:first comment.}"]),
  ]),
}
