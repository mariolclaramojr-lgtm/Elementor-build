const { chromium } = require('playwright');
const B = 'https://rrnewlewisthem.wpenginepowered.com';
(async () => {
  const b = await chromium.launch(); const out = {};
  // 1. hero video source + sermon 403
  let p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto(B + '/', { waitUntil: 'networkidle' });
  out.heroVideo = await p.evaluate(() => [...document.querySelectorAll('video')].map(v => ({ src: v.currentSrc || v.src || [...v.querySelectorAll('source')].map(s => s.src).join(','), canMp4: v.canPlayType('video/mp4'), err: v.error && v.error.code, ready: v.readyState, cls: v.parentElement.className.slice(0,40) })));
  // sticky header
  await p.mouse.wheel(0, 1500); await p.waitForTimeout(1500);
  out.sticky = await p.evaluate(() => { const n = document.querySelector('.lc-nav'); return { fixed: n.classList.contains('x-bar-fixed'), bg: getComputedStyle(n).backgroundColor, top: Math.round(n.getBoundingClientRect().top) }; });
  // card hover expand
  await p.evaluate(() => document.querySelector('.lc-cards').scrollIntoView()); await p.waitForTimeout(500);
  const w0 = await p.evaluate(() => [...document.querySelectorAll('.lc-card')].map(c => Math.round(c.getBoundingClientRect().width)));
  await p.hover('.lc-card:nth-child(3)'); await p.waitForTimeout(1000);
  const w1 = await p.evaluate(() => [...document.querySelectorAll('.lc-card')].map(c => Math.round(c.getBoundingClientRect().width)));
  out.cardsHover = { before: w0, after: w1 };
  await p.close();
  p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  const r403 = []; p.on('response', r => { if (r.status() === 403) r403.push(r.url().slice(0, 120)); });
  await p.goto(B + '/sermons/pretty-simple/', { waitUntil: 'networkidle' }); out.sermon403 = r403; await p.close();
  // 2. About welcome video
  p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto(B + '/about/', { waitUntil: 'networkidle' });
  out.aboutVideo = await p.evaluate(() => [...document.querySelectorAll('video')].map(v => ({ srcs: [...v.querySelectorAll('source')].map(s => s.type + ' ' + s.src.slice(-30)), cur: v.currentSrc.slice(-30), autoplay: v.autoplay, err: v.error && v.error.code })));
  await p.close();
  // 3. mobile menu
  p = await b.newPage({ viewport: { width: 390, height: 844 } });
  await p.goto(B + '/', { waitUntil: 'networkidle' });
  await p.click('.lc-nav .x-anchor-toggle'); await p.waitForTimeout(1000);
  out.mobileMenu = await p.evaluate(() => { const oc = document.querySelector('.x-off-canvas'); return { open: oc && oc.classList.contains('x-active'), links: [...document.querySelectorAll('.x-off-canvas .x-anchor-text-primary')].map(e => e.textContent.trim()) }; });
  await Promise.all([p.waitForNavigation(), p.click('.x-off-canvas a[href*="/about/"]')]); out.mobileMenuNav = p.url();
  await p.close();
  // 4. FAQ accordion
  p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto(B + '/plan-your-visit/', { waitUntil: 'networkidle' });
  const acc = async () => p.evaluate(() => [...document.querySelectorAll('.x-acc-item')].map(i => { const c = i.querySelector('.x-acc-content'); return c ? Math.round(c.getBoundingClientRect().height) : -1; }));
  const a0 = await acc(); await p.click('.x-acc-item:nth-child(2) .x-acc-header'); await p.waitForTimeout(900); const a1 = await acc();
  out.faq = { before: a0, afterClick2: a1 };
  await p.close();
  // 5. Calendar next month
  p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto(B + '/events-calendar/', { waitUntil: 'networkidle' });
  const m0 = await p.textContent('.lc-mec .mec-month-container-selected, .lc-mec .mec-calendar-header h2').catch(() => '');
  await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(500); await p.evaluate(() => { const e = document.querySelector('.lc-mec .mec-next-month'); window.scrollTo(0, e.getBoundingClientRect().top + window.scrollY - 400); }); await p.waitForTimeout(800); await p.click('.lc-mec .mec-next-month'); await p.waitForTimeout(3500);
  out.calendar = { before: (await p.$$eval('.lc-mec .mec-calendar-header h2', e => e.map(x => x.textContent.trim()))) };
  out.calendarVisible = await p.evaluate(() => [...document.querySelectorAll('.lc-mec .mec-month-navigator')].filter(n => n.offsetParent).map(n => n.textContent.replace(/\s+/g,' ').trim()));
  await p.close();
  // 6. Sermon filter
  p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto(B + '/messages/', { waitUntil: 'networkidle' });
  await Promise.all([p.waitForNavigation({ timeout: 60000 }).catch(() => null), p.selectOption('#wpfc_preacher', 'guest-speaker')]);
  await p.waitForLoadState('networkidle');
  out.sermonFilter = { url: p.url(), titles: await p.$$eval('.smpro-title__text', e => e.map(x => x.textContent.trim())), styled: await p.evaluate(() => !!document.querySelector('.lc-sermons, body[class*="tax-wpfc"], .post-type-archive-wpfc_sermon')) };
  await p.screenshot({ path: 'qa/filter.png' });
  await p.close();
  // 7. Watch live embed
  p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto(B + '/watch-live/', { waitUntil: 'networkidle' });
  out.youtube = await p.evaluate(() => [...document.querySelectorAll('iframe')].map(i => ({ src: i.src.slice(0, 60), w: Math.round(i.getBoundingClientRect().width), h: Math.round(i.getBoundingClientRect().height) })));
  await p.close();
  console.log(JSON.stringify(out, null, 1)); await b.close();
})();
