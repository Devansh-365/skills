# Peerlist launch: Exhibitor List Scraper

Prepared 2026-10-28. Store page: https://apify.com/getascraper/exhibitor-list-scraper

## Form fields

| Field | Value |
|---|---|
| Project name | Exhibitor List Scraper |
| Project URL | https://apify.com/getascraper/exhibitor-list-scraper |
| Tagline (54/60) | Turn trade show exhibitor lists into clean lead sheets |
| Categories | Marketing, Productivity, SaaS (Peerlist has no Sales or Lead Generation category) |
| Built with | Apify, TypeScript, Node.js, Crawlee |
| Open source | Unticked |
| Description | Open `description.html` in a browser, select all, copy, paste (keeps headings, bold and links) |

Other taglines: "Exhibitors from 148 trade shows, in one clean spreadsheet" (57), "Trade show exhibitor lists to clean leads, with emails" (54).

## Media

| Slot | File |
|---|---|
| Logo (500x500) | `logo.png` |
| Cover 1, first (1200x630) | `cover-1-sheet.png` |
| Cover 2 | `cover-2-shows.png` |
| Cover 3 | `cover-3-email.png` |
| Cover 4 | `cover-4-facts.png` |
| Demo video (1920x1080, 37 s, silent) | `demo-video.mp4` |

Style: mondaystack `monday-listing-assets` "bold" direction, recoloured to the README orange (#c2410c), with a
"Runs on Apify" badge using the official wordmark. All rows, show names and the email example are real output
(Cloud run NW7CR9Wi8MPcYgL9s, `dist/shows.js`); the one personal email is masked. No prices, user counts or ratings.

## Maker comment

> Hi Peerlist 👋 I built Exhibitor List Scraper because every trade show publishes its exhibitor list differently,
> and teams still copy rows by hand before a show. Pick from 148 named fairs or paste a list link, and you get one
> clean spreadsheet: company, website, email, phone, stand and contact persons. When the fair has no email, it
> checks the exhibitor's own website for a named person's email, never a guessed one. If your trade show isn't
> supported yet, drop the link in the comments and I'll add it.

## Launch day

1. Save the project, then submit it to Launchpad for the next launch week.
2. Post the maker comment right away.
3. Reply to every comment that day.
4. Share the launch once on your Peerlist feed.

## Rebuilding the assets

- Images: `src/concepts/*.html` on `src/assets/bold.css`, exported at exact size with the `launch-assets` skill's
  `capture.mjs` (`src/*@2x.png` are the retina masters).
- Video: `src/video/` is a HyperFrames project (`npx --yes hyperframes@0.8.151 render --quality high`). Fonts are
  not saved; download Cabinet Grotesk 700/800 and Satoshi 500/700/900 from Fontshare into `src/video/assets/fonts/`.
