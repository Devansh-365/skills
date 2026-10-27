// Export every concepts/*.html frame to out/<slug>.png (exact .stage size) and out/<slug>@2x.png,
// then write out/contact.png, a contact sheet of all frames for a quick review.
// Usage (from the lab folder, with playwright resolvable): node export.mjs [slug-filter ...]
import { chromium } from 'playwright';
import { readdirSync, mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const filters = process.argv.slice(2);
const slugs = readdirSync('concepts')
  .filter((f) => f.endsWith('.html'))
  .map((f) => f.replace(/\.html$/, ''))
  .filter((s) => filters.length === 0 || filters.some((f) => s.includes(f)))
  .sort();
mkdirSync('out', { recursive: true });

const browser = await chromium.launch();
let failed = 0;
for (const slug of slugs) {
  const url = pathToFileURL(resolve('concepts', `${slug}.html`)).href;
  for (const scale of [1, 2]) {
    const page = await browser.newPage({ viewport: { width: 2000, height: 2000 }, deviceScaleFactor: scale });
    const broken = [];
    page.on('requestfailed', (r) => broken.push(r.url()));
    await page.goto(url, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(400);
    const stage = await page.$('.stage');
    if (!stage) { console.log(`✗ ${slug}: no .stage element`); failed++; await page.close(); break; }
    const box = await stage.boundingBox();
    const file = `out/${slug}${scale === 2 ? '@2x' : ''}.png`;
    await stage.screenshot({ path: file });
    if (scale === 1) console.log(`${broken.length ? '!' : '✓'} ${slug} ${Math.round(box.width)}x${Math.round(box.height)}${broken.length ? `  failed to load: ${broken.join(', ')}` : ''}`);
    if (broken.length) failed++;
    await page.close();
  }
}

// Contact sheet: every 1x export in a 2-column grid on a dark ground.
const cells = slugs.map((s) => `<figure><img src="${pathToFileURL(resolve('out', `${s}.png`)).href}"><figcaption>${s}</figcaption></figure>`).join('');
const sheet = `<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#1c1917;font:14px system-ui;color:#d6d3d1}
main{display:grid;grid-template-columns:repeat(2,600px);gap:20px;padding:20px;width:max-content}
figure{margin:0}img{display:block;max-width:600px;max-height:600px}figcaption{padding-top:6px}</style><main>${cells}</main>`;
writeFileSync('out/_contact.html', sheet);
const page = await browser.newPage({ viewport: { width: 1260, height: 800 } });
await page.goto(pathToFileURL(resolve('out/_contact.html')).href, { waitUntil: 'load' });
await page.locator('main').screenshot({ path: 'out/contact.png' });
await browser.close();
console.log(`\n${slugs.length - failed} exported, ${failed} with problems. Review out/contact.png`);
process.exitCode = failed ? 1 : 0;
