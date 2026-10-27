# Lessons from the first launch (Exhibitor List Scraper, 2026-10-28)

Each point cost one round of fixes. Read this before building assets.

## Facts and honesty

- Read the live Store title, description and categories from the Apify API, not from local `actor.json`. The
  live description is the source for numbers such as "30 fair platforms" and "148 named shows".
- Don't show Store stats (users, ratings, bookmarks) when they are low. Showing 3 users and 0 reviews hurts more
  than it helps. Crop them out of any Store screenshot too.
- Use real rows from a recent Cloud run of the actor (`GET /v2/acts/{id}/runs?desc=1`, then the run's dataset
  items). Pick rows that look clean: avoid rows a later fix changed, such as rows the email classifier got wrong in
  an older run.
- A role inbox (info@, sales@) is published business contact data and can be shown. A named person's email must be
  partly hidden: `j•••.j•••••••@domain.de`.
- Missing values stay missing ("not listed"). Never fill a cell to make a table look complete.
- No price numbers, no em dashes, no technical words in any public text.

## Layout traps

- **Headline collides with the card.** Keep the headline column at most about 500px wide at 64 to 76px on a
  1200px cover, and start the card at least 40px to its right. Check line wraps after every copy change.
- **Big gap between headline and subline.** Place the subline about 30px under the headline's last line, not at a
  fixed low position.
- **Cut through words.** A card may bleed off the edge, but never cut a word or an email in half. Put the payoff
  column (email) before less important columns, or narrow the table until it fits.
- **Tags run off the stage.** Measure the tag's right edge (left + text width) against the stage width; shorten
  the text ("Or paste a list link") rather than shrinking it.
- **Badge touching a card.** When the brand row gains a badge, move cards down so they clear the brand row (top
  of about 100px or more on a cover).
- The fixed `top:` values in the templates assume the template copy. New copy means re-checking every position.

## Rendering

- Fontshare fonts load via `@import` for the covers, one `@import` per family: a combined request served only
  Cabinet Grotesk, and the body text silently fell back to Helvetica. Satoshi loading makes text a little taller,
  so re-check the positions of anything placed under a table. For the video, download the woff2 files locally
  (HyperFrames render needs a local `@font-face`), again one request per family.
- On the Store page, `waitUntil: 'networkidle'` times out. Use `'load'` plus a 6 second wait, and click "Dismiss"
  on the cookie banner before capturing.
- The Apify wordmark is at `https://apify.com/img/apify-logo/wordmark.svg` (dark text, for light backgrounds) and
  `wordmark-white.svg`. Other names 404. Download it at build time; it isn't bundled because it is Apify's brand
  asset.
- HyperFrames `check` flags low contrast: grey `#a8a29e` text on white fails, so use `#78716c`. Its
  `nested_structure_needs_subcomposition` warnings are expected for a hand-written single-file video and can be
  ignored, just as they were for Waypost.
- A highlight overlay with extra glyphs ("✓ MEDICA") overflows its chip. Highlight with colour alone.

## Working with the user

- When the user asks to "show me", open the preview right away (`open out/contact.png`, or the MP4). Render with
  your own headless browser; don't take over the user's browser.
- Render the video once checks pass and say plainly that it can be re-rendered. Rendering takes about 30 seconds.
- Save the final files to the repo, but commit only after the user asks.
