const { chromium } = require('playwright');
const B = 'https://rrnewlewisthem.wpenginepowered.com';
const pages = ['/thank-you/','/get-connected/','/','/about/','/connect/','/plan-your-visit/','/watch-live/','/give/','/messages/','/events-calendar/','/get-connected/','/thank-you/','/sermons/pretty-simple/','/events/sunday-worship/','/sermons/','/series/second-series/'];
const widths = [390, 768, 1440];
(async () => {
  const b = await chromium.launch();
  const links = new Set(); const report = [];
  for (const w of widths) {
    const ctx = await b.newContext({ viewport: { width: w, height: 900 } });
    for (const path of pages) {
      const p = await ctx.newPage(); const errs = [];
      p.on('console', m => { if (m.type() === 'error') errs.push(m.text().slice(0, 140)); });
      p.on('pageerror', e => errs.push('JS: ' + e.message.slice(0, 140)));
      const bad = [];
      p.on('response', r => { if (r.status() >= 400 && r.url().startsWith(B)) bad.push(r.status() + ' ' + r.url().replace(B, '')); });
      await p.goto(B + path, { waitUntil: 'networkidle', timeout: 90000 });
      for (let y = 0; y < 12000; y += 700) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(60); }
      await p.waitForTimeout(800);
      const r = await p.evaluate(() => {
        const vw = document.documentElement.clientWidth;
        const over = [...document.querySelectorAll('body *')].filter(e => { const b = e.getBoundingClientRect(); const cs = getComputedStyle(e);
          return b.width > 0 && (b.right > vw + 2) && cs.position !== 'fixed' && !e.closest('.x-off-canvas,.x-modal,.tooltip_templates,.mec-tooltip-event-title,iframe') ; })
          .filter(e => { let a = e.parentElement; while (a) { const o = getComputedStyle(a).overflowX; if (o === 'hidden' || o === 'clip' || o === 'auto' || o === 'scroll') return false; a = a.parentElement; } return true; })
          .slice(0, 5).map(e => (e.className && e.className.baseVal === undefined ? e.className : e.tagName).toString().slice(0, 60) + ' r=' + Math.round(e.getBoundingClientRect().right));
        const imgs = [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.src && !i.src.startsWith('data:')).map(i => i.src.slice(-60));
        const ls = [...document.querySelectorAll('a[href]')].map(a => a.href).filter(h => h.startsWith(location.origin) && !h.includes('#') && !h.includes('/wp-admin'));
        return { scrollW: document.documentElement.scrollWidth, vw, over, imgs, ls };
      });
      r.ls.forEach(l => links.add(l.split('?')[0]));
      report.push({ w, path, overflow: r.scrollW > r.vw ? `scrollW ${r.scrollW} > ${r.vw}` : '', overEls: r.over, brokenImgs: r.imgs, consoleErrs: [...new Set(errs)].slice(0, 4), http: [...new Set(bad)].slice(0, 4) });
      await p.close();
    }
    await ctx.close();
  }
  // link check
  const ctx = await b.newContext(); const linkBad = [];
  for (const l of links) { try { const r = await ctx.request.get(l, { timeout: 60000 }); if (r.status() >= 400) linkBad.push(r.status() + ' ' + l); } catch (e) { linkBad.push('ERR ' + l); } }
  console.log(JSON.stringify({ report: report.filter(x => x.overflow || x.overEls.length || x.brokenImgs.length || x.consoleErrs.length || x.http.length), checked: report.length, links: links.size, linkBad }, null, 1));
  await b.close();
})();
