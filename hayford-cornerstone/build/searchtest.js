const {chromium} = require('playwright');
const BASE = 'https://rrnewhayford.wpenginepowered.com/';
const CASES = [
  ['worship', ['Worship Night']], ['sermon', ['Messages']], ['love', ['Rooted in Love']], ['fear', ['When Fear Knocks']],
  ['David', ['A Heart After God']], ['prodigal', ['Come As You Are']], ['kids', ['Connect']], ['students', ['Connect']],
  ['women', ['Connect']], ['men', ['Connect']], ['prayer', ['Night of Prayer']], ['Thanksgiving', ['Thanksgiving Community Dinner']],
  ['give', ['Give']], ['beliefs', ['About']], ['Holy Spirit', null], ['visit', ['Plan Your Visit']],
  ['coffee', ['Plan Your Visit']], ['live', ['Watch Live']], ['connection card', ['Get Connected']],
  ['Lombardi', []], ['zzqxnomatch', null], ['<script>alert(1)</script>', null], ['', []],
];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: 1440, height: 900}});
  const errs = []; p.on('pageerror', e => errs.push(e.message.slice(0, 60)));
  p.on('dialog', d => { errs.push('DIALOG ' + d.message()); d.dismiss(); });
  let pass = 0, fail = 0;
  const allLinks = new Set();
  for (const [q, expect] of CASES) {
    await p.goto(BASE + '?s=' + encodeURIComponent(q), {waitUntil: 'domcontentloaded', timeout: 60000});
    await p.waitForTimeout(600);
    const r = await p.evaluate(() => ({
      h1: (document.querySelector('h1') || {}).innerText || '',
      titles: [...document.querySelectorAll('.x-cell h2')].map(e => e.innerText.trim()),
      links: [...document.querySelectorAll('a.x-cell')].map(a => a.href),
      none: document.body.innerText.includes("We couldn't find a match"),
      count: ((document.body.innerText.match(/(\d+) results for/i) || [])[1]) || null,
    }));
    r.links.forEach(l => allLinks.add(l));
    let ok;
    if (q.includes('<script>')) ok = r.h1.includes('403');
    else if (expect === null) ok = r.none && r.titles.length === 0;
    else ok = !r.none && expect.every(t => r.titles.includes(t)) && (r.count === null || +r.count >= r.titles.length);
    if (new Set(r.titles).size !== r.titles.length) ok = false;
    ok ? pass++ : fail++;
    console.log((ok ? 'PASS' : 'FAIL'), JSON.stringify(q).padEnd(30), '|', r.count ?? '-', 'results |', r.titles.slice(0, 6).join(', ') || (r.none ? '(no-results panel)' : '(none)'));
  }
  // every result link opens
  let bad = 0;
  for (const l of allLinks) {
    const res = await p.request.get(l, {maxRedirects: 3});
    if (res.status() !== 200) { bad++; console.log('BROKEN', res.status(), l); }
  }
  console.log(`links checked: ${allLinks.size}, broken: ${bad}`);
  // header search icon -> modal -> submit
  await p.goto(BASE + 'about/', {waitUntil: 'networkidle'});
  const toggle = p.locator('.x-bar:visible .x-anchor-toggle').first();
  await toggle.click(); await p.waitForTimeout(800);
  const input = p.locator('.x-modal.x-active input[type=search], .x-modal input[type=search]:visible').first();
  await input.fill('prayer'); await input.press('Enter');
  await p.waitForLoadState('networkidle');
  const viaHeader = p.url().includes('s=prayer') && (await p.locator('h1').innerText()).includes('prayer');
  console.log((viaHeader ? 'PASS' : 'FAIL'), 'header search icon → modal → results', p.url());
  // search box on the results page
  const box = p.locator('h1 ~ * input[type=search], .x-search input[type=search]').first();
  await box.fill('kids'); await box.press('Enter'); await p.waitForLoadState('networkidle');
  const viaBox = p.url().includes('s=kids');
  console.log((viaBox ? 'PASS' : 'FAIL'), 'results-page search box', p.url());
  await p.screenshot({path: __dirname + '/wpqa/search-kids.png'});
  // mobile
  const m = await b.newPage({viewport: {width: 390, height: 844}});
  await m.goto(BASE + '?s=worship', {waitUntil: 'networkidle'});
  const sw = await m.evaluate(() => document.body.scrollWidth);
  console.log((sw === 390 ? 'PASS' : 'FAIL'), 'mobile results page width', sw);
  const H = await m.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < H; y += 400) { await m.evaluate(y => scrollTo(0, y), y); await m.waitForTimeout(80); }
  await m.screenshot({path: __dirname + '/wpqa/search-mobile.png', fullPage: true});
  console.log(`\nqueries: ${pass} passed, ${fail} failed; page errors: ${errs.length ? errs.join(' | ') : 'none'}`);
  await b.close();
})();
