# Story and carousel images: "The gallery-portfolio trap"

Still images for posting alongside reel 5 and its trial edits. They use the reels' lockin-red look and graphics, and
the user's own footage (the hand-on-chin frame at 3.95s, graded, plus its background-removed cutout). The copy follows
the script.

## Stories (1080x1920, `stories/`)

Key content stays inside y 250–1650, clear of Instagram's profile bar and reply field.

1. **Hook:** "Your Portfolio Is Beautiful… / But No Client Writes." over the face card, with a red "0 Messages" pill
   and "Tap to see why".
2. **The trap:** "It's Not Your Talent. / It's The *Gallery-Portfolio Trap*". The phone portfolio stands behind a
   museum rope, with "A portfolio without a next step is a *gallery*."
3. **The three mistakes:** "3 Mistakes I Fixed / To Land My First Client". Each row has one line of explanation from
   the script.
4. **CTA:** "My Template" fixes Results, Clear Offer and Next Step. Then "Comment *"Portfolio"*", under the latest
   reel, to join the waitlist.

## Carousel (1080x1350, 4:5, `carousel/`)

1. **Cover:** "The Gallery-Portfolio Trap" tag and "Your Portfolio Is Beautiful. / So Why No Client Writes?". The
   cutout sits next to a red "0: Clients Writing To You".
2. **01 · Projects, Not Results:** "Projects" struck out for "Results", and the client asking "What's In It For Me?".
3. **02 · Nobody Gets What You Sell:** a jumble of services around "Versatile Creative", struck out and stamped "Speaks
   To No One".
4. **03 · No Next Step:** 10 projects and 0 clear buttons; "a portfolio without a next step is a *gallery*". The CTA:
   "My template fixes all 3. Comment *"Portfolio"* to join the waitlist".

## Rebuild

```bash
python3 social/tools/gen_social.py      # writes social/pages/*.html
node social/tools/render_social.mjs     # screenshots them to social/stories/ and social/carousel/
```

Run both from `videos/portfolio-trap-reel/`.
- The render script serves this project over HTTP, so the pages can load `/assets/css/lockin.css` and the fonts.
- It needs Playwright, which the cloud sandbox installs globally.
- `social/img/` holds the two footage stills.
