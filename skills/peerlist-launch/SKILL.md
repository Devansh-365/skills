---
name: peerlist-launch
description: Prepare a complete Peerlist Launchpad launch for a product, especially an Apify Actor. Writes every Add Project form field to Peerlist's limits (name, tagline, categories from the real Peerlist list, built with, description); builds the bold-style logo (500x500) and 4 cover images (1200x630) with a "Runs on Apify" badge from real output data; renders a silent HyperFrames demo video; writes the maker comment and launch-day steps; and saves everything to docs/launch/peerlist/<slug>/. Use this whenever the user wants to launch, list, post or submit something on Peerlist, mentions Peerlist Launchpad, Add Project, a Peerlist cover image, tagline or category, or says "launch this actor" or "let's do a launch like the exhibitor one", even if they only ask for one piece, such as the tagline or categories.
---

# Peerlist launch

Turns a product (usually an Apify Actor) into a ready-to-paste Peerlist Launchpad submission: form copy, media,
demo video and launch-day plan. It was first used for Exhibitor List Scraper
(https://apify.com/getascraper/exhibitor-list-scraper) on 2026-10-28. That launch is the worked example, and its
cover and video files are this skill's templates in `assets/`.

Why the workflow looks like this: it was built for a solo builder with no marketing team. A launch has to be cheap to
repeat, honest (the audience is technical and spots fake numbers), and visually consistent with the Apify Store
page people land on. So the skill reuses one proven style and real data instead of inventing a new look each time.

## The Peerlist form (what has to be filled)

| Field | Limit | Notes |
|---|---|---|
| Autofill with AI | | Skip it. It pulls messy Store text. |
| Project name * | 45 chars | The product name, nothing else (e.g. "Exhibitor List Scraper") |
| Project URL | | The public Store URL `https://apify.com/<user>/<actor>` |
| Tagline * | 60 chars | Outcome in plain words. Count the characters with a script. |
| Category(ies) | up to 3 | Only from `references/categories.md`. There is no Sales or Lead Generation category. |
| Built with | up to 10 | Real stack only (Apify, TypeScript, Node.js, Crawlee...). Never the suggested Cursor/OpenAI unless used. |
| Collaborators | | Empty |
| Open source | checkbox | Unticked unless the code is really public |
| Description | 5000 chars, H / bold / italic / lists / links | Pasted as rich text from an HTML file (see step 2) |
| Logo | 500x500, max 15 MB | |
| Cover image(s) | 1200x630, up to 4, max 15 MB each | The first one is the one most people see |
| Demo video | max 100 MB | Silent MP4, 30 to 40 s |

## Workflow

If they are installed, invoke the `copywriting` skill before writing the tagline, description and maker comment,
and `launch-strategy` for the launch-day plan. The images are HTML frames exported with `scripts/export.mjs`
(Playwright); a `launch-assets` skill, if you have one, works too. The video uses HyperFrames
(`npx hyperframes`, with the `product-launch-video` skill if installed). The look is the "bold" listing style
(a flat brand-colour field, huge headlines, real UI on white cards, yellow tags), first designed for a monday.com
marketplace listing.

Read `references/lessons.md` once before building anything. It lists the traps the first launch hit.

### 1. Gather true facts (no copy yet)

- Live listing: `GET https://api.apify.com/v2/acts/<id>` with your Apify token (for example from
  `~/.apify/auth.json`; read it only inside one-shot commands, never print it). Take `title`, `description`, `categories` and `pictureUrl` from there,
  not from local `actor.json`.
- README: `actors/<name>/.actor/README.md` for capabilities, personas and wording already approved.
- Real output: a recent successful Cloud run's dataset (`/v2/acts/<id>/runs?desc=1&limit=25`, then
  `/v2/datasets/<id>/items?clean=1`). These rows become the images. Don't start a new Cloud run just for the
  launch unless no usable dataset exists, and if one is needed, keep it to one small run.
- Store icon: download `pictureUrl` (it becomes the logo and the brand tile).
- Product marketing context: `.agents/product-marketing-context.md` if present (its claims rule applies).

Every number in the copy and images must trace to one of these sources. If a claim needs a fact you don't have,
drop the claim.

### 2. Write the listing copy

Rules (defaults that worked; keep them unless the user says otherwise): plain language, outcome first, no em dashes, no price numbers, no technical
words (no "API", "proxy", "scraper engine"), no invented stats, no hype, no exclamation marks. Never claim complete
coverage ("any fair") when the product supports a list.

- **Tagline:** write 3 options of 60 characters or fewer, count them with `python3 -c "print(len('...'))"`,
  recommend one and say why.
- **Categories:** pick 3 from `references/categories.md` with its "How to choose" table. Explain each pick in one
  line, and say which tempting categories were skipped and why.
- **Description** (aim for about 2,000 to 3,000 chars): sections "What it does", "Why it exists", "What you get"
  (bullets with bold lead-ins), "Who it's for", "How it works" (3 steps), "Pricing" (in words, e.g. "pay only for
  the results you get, try it on Apify's free plan"), an optional "Missing your X?" request line linking to the
  actor's Issues page, and a final "Try <name> on Apify" link. Write it as HTML from
  `assets/description-template.html` so headings, bold and links survive the paste: open the file, select all,
  copy, paste. Check the plain-text length with a script.
- **Maker comment:** 4 to 5 sentences, first person, the pain, what it does, one honest detail, and an invitation
  ("if your X isn't supported, drop the link and I'll add it").

### 3. Build the logo and 4 covers (bold style)

Set up a lab in a temporary folder (not in the repo):

```
peerlist-lab/
  assets/   bold.css (from this skill), store-icon.png (the product icon),
            apify-wordmark.svg (download: curl -o assets/apify-wordmark.svg https://apify.com/img/apify-logo/wordmark.svg)
  concepts/ logo.html, cover-1..4.html (copied from this skill's assets/covers/, then edited)
  out/      exported PNGs (generated)
  export.mjs                 (from this skill's scripts/)
  node_modules               (needs playwright: npm i playwright && npx playwright install chromium,
                              or symlink a project's node_modules that already has it)
```

The Apify wordmark is Apify's brand asset, so it is downloaded at build time rather than shipped with this skill.

The style, in `assets/bold.css` (edit tokens, not frames):
- a flat saturated field in the product's brand colour (the README accent; exhibitor used orange `#c2410c`) with a
  white dot grid;
- Cabinet Grotesk 800 headlines, very large, with one word in signal yellow `#ffd84a`; Satoshi for body text;
- real output on white cards with a tinted shadow, and yellow tags with a pointer at the payoff;
- a brand row on every cover: Store icon tile + product name + a white **"Runs on [Apify wordmark]"** badge, so
  people see at a glance that it's Apify-native. Use the official wordmark (downloaded as above). For a product
  that isn't on Apify, swap the badge for the platform it runs on, or drop it.

The 4-cover arc (one job per image; adapt the content, keep the jobs):

| # | Job | Exhibitor example |
|---|---|---|
| 1 | Hook: the core result, as a card of real output | "Every fair's exhibitor list. One clean sheet." + 8 real rows from 4 fairs |
| 2 | How you start (input made easy) | "Tick the show. Skip the hunt." + real names grouped as chips, 4 ticked |
| 3 | The differentiator, shown as before/after | "A person, not just info@." + one real exhibitor, the email masked |
| 4 | Trust facts + call to action | "Stop copying rows by hand." + 4 numbered true facts + "Try it on Apify" button |

Logo: the Store icon on a white rounded tile on the brand field (`assets/covers/logo.html`). It keeps the Peerlist
logo identical to what people see on Apify.

Export and review:

```bash
cd peerlist-lab && node export.mjs     # every concept -> out/<slug>.png + @2x, and out/contact.png
node export.mjs cover-1                # re-export only frames whose name contains "cover-1"
```

Look at `out/contact.png` yourself and fix overlaps, cut words, tags off the edge and gaps before showing the
user (see lessons.md). Then open it for them (`open out/contact.png` on macOS).

### 4. Render the demo video (silent, 1920x1080, about 35 s)

Start from `assets/video/index.html`, the exhibitor video. It is one hand-written HyperFrames composition (a GSAP
timeline on HTML scenes) in the same style. Keep its 7-frame arc and swap the content:

1. pain hook in big type (about 3 s);
2. brand row with the Runs on Apify badge + the promise (about 4 s);
3. the input step, animated (chips ticking) (about 6 s);
4. the output card filling row by row (about 7 s);
5. the differentiator before/after (about 7.5 s);
6. the recurring-use frame (about 4 s);
7. close: a real capture of the public Store page header (title + "Try for free", stats cropped out), the
   Apify badge, and "Try it free at apify.com/...".

Setup: a `video/` folder in the lab with `index.html`, `hyperframes.json` and `package.json` from `assets/video/`,
plus a `BRIEF.md` (intent, assets, notes: silent, real data, no prices or counts). Download the fonts locally into
`video/assets/fonts/` (see lessons.md), and capture the Store header with headless Playwright (load + 6 s,
dismiss the cookie banner, clip the header only). Then:

```bash
npx --yes hyperframes@0.8.151 lint      # 0 errors; subcomposition warnings are expected
npx --yes hyperframes@0.8.151 check     # must pass with no contrast or overflow items
npx --yes hyperframes@0.8.151 snapshot --at <end of each frame> --no-end   # read the contact sheet
npx --yes hyperframes@0.8.151 render --quality high --output renders/<slug>-promo.mp4
```

Pull 6 frames from the MP4 with ffmpeg and look at them before reporting. Rendering takes about 30 s, so render
once checks pass, open it for the user, and offer changes.

### 5. Save to the repo

Copy the deliverables to the product repo at `docs/launch/peerlist/<slug>/`:

```
logo.png  cover-1-*.png .. cover-4-*.png  demo-video.mp4  description.html  README.md
src/  concepts/*.html  assets/ (bold.css, icon, wordmark)  *@2x.png  video/ (index.html, BRIEF.md, configs, assets without fonts)
```

`README.md` follows `assets/launch-readme-example.md`: form fields table, other taglines, media table, maker
comment, launch-day steps and rebuild notes. Don't commit on your own; offer a single commit of just that folder
and make it when the user says so.

### 6. Launch day (the minimum, for a solo builder)

1. Save the project, then submit it to Launchpad for the next launch week Peerlist offers.
2. Post the maker comment right away.
3. Reply to every comment that day. This matters most for ranking.
4. Share the launch once on your own Peerlist feed. No other channels needed.

## Reply format

Lead with the outcome ("Your Peerlist listing is ready"), then one table per form section with the exact text to
paste and the file to upload, using full absolute paths. Keep explanations to one line per choice. End with the
single next step (for example "Want me to make the video next?").
