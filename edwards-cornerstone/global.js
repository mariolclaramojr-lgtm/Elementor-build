/* ===== EDWARDS REDESIGN START ===== */
/* Edwards — global helpers (Cornerstone › Global JS). Editors type plain text; this does the rest.
   1. H1/H2 accent: 1 word = plain, 2–5 words = last word, 6+ words = last two words (span.ed-accent).
      A heading that already contains <em> is left as typed. Opt out with data-ed-no-accent.
   2. Photo viewer: images with the class "ed-lightbox" open full-size (arrows / keyboard / Esc).
   3. Next-service countdown: the "Next Service" item (.ed-next-service / .ed-next-value) counts down
      to Sunday 10am / Wednesday 7pm and shows "Happening Now" during a service. */
(function () {
  var SKIP = '.gform_wrapper, .x-off-canvas, .x-modal, .ed-lb, article .entry-title, .smpro-item, .wpfc-sermon, .mec-wrap, [data-ed-no-accent]';

  function accent(h) {
    if (h.querySelector('.ed-accent, em') || h.closest(SKIP)) return;
    var words = h.textContent.trim().split(/\s+/).length;
    if (words < 2) return;
    var w = document.createTreeWalker(h, NodeFilter.SHOW_TEXT, null), n, last = null;
    while ((n = w.nextNode())) if (/\S/.test(n.nodeValue)) last = n;
    if (!last) return;
    var m = (words > 5 && last.nodeValue.match(/^([\s\S]*?)(\S+\s+\S+)(\s*)$/)) || last.nodeValue.match(/^([\s\S]*?)(\S+)(\s*)$/);
    if (!m) return;
    var span = document.createElement('span'); span.className = 'ed-accent'; span.textContent = m[2];
    var f = document.createDocumentFragment();
    if (m[1]) f.appendChild(document.createTextNode(m[1]));
    f.appendChild(span);
    if (m[3]) f.appendChild(document.createTextNode(m[3]));
    last.parentNode.replaceChild(f, last);
  }
  function run(root) { (root || document).querySelectorAll('h1, h2').forEach(accent); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { run(); }); else run();
  var t; new MutationObserver(function () { clearTimeout(t); t = setTimeout(run, 150); }).observe(document.documentElement, { childList: true, subtree: true });

  /* ---- Photo viewer ---- */
  function lightbox() {
    var links = Array.prototype.slice.call(document.querySelectorAll('a.ed-lightbox, .ed-lightbox a'));
    if (!links.length) return;
    var lb = document.createElement('div');
    lb.className = 'ed-lb'; lb.hidden = true; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', 'Photo viewer');
    var X = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">';
    lb.innerHTML = '<button type="button" class="ed-lb-close" aria-label="Close">' + X + '<path d="M6 6l12 12M18 6L6 18"/></svg></button>' +
      '<button type="button" class="ed-lb-prev" aria-label="Previous photo">' + X + '<path d="M15 5l-7 7 7 7"/></svg></button>' +
      '<figure><img src="" alt=""><figcaption></figcaption></figure>' +
      '<button type="button" class="ed-lb-next" aria-label="Next photo">' + X + '<path d="M9 5l7 7-7 7"/></svg></button>';
    document.body.appendChild(lb);
    var img = lb.querySelector('img'), cap = lb.querySelector('figcaption'), cur = 0, back;
    function show(i) { cur = (i + links.length) % links.length; var a = links[cur], im = a.querySelector('img'); img.src = a.href; img.alt = im ? im.alt : ''; cap.textContent = (cur + 1) + ' / ' + links.length; }
    function open(i) { back = document.activeElement; show(i); lb.hidden = false; requestAnimationFrame(function () { lb.classList.add('is-open'); }); document.body.style.overflow = 'hidden'; lb.querySelector('.ed-lb-close').focus(); }
    function close() { lb.classList.remove('is-open'); setTimeout(function () { lb.hidden = true; }, 300); document.body.style.overflow = ''; if (back) back.focus(); }
    links.forEach(function (a, i) { a.addEventListener('click', function (e) { e.preventDefault(); open(i); }); });
    lb.querySelector('.ed-lb-close').addEventListener('click', close);
    lb.querySelector('.ed-lb-prev').addEventListener('click', function () { show(cur - 1); });
    lb.querySelector('.ed-lb-next').addEventListener('click', function () { show(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) { if (lb.hidden) return; if (e.key === 'Escape') close(); if (e.key === 'ArrowLeft') show(cur - 1); if (e.key === 'ArrowRight') show(cur + 1); });
  }

  /* ---- Next-service countdown ---- */
  function countdown() {
    var box = document.querySelector('.ed-next-service'); if (!box) return;
    var valEl = box.querySelector('.ed-next-value .x-text-content-text-primary') || box.querySelector('.ed-next-value');
    var labs = box.querySelectorAll('.x-text-content-text-primary'), labEl = labs.length > 1 ? labs[0] : null;
    var S = [{ day: 0, h: 10, len: 90, name: 'Sunday 10am' }, { day: 3, h: 19, len: 90, name: 'Wednesday 7pm' }];
    function tick() {
      var now = new Date(), best = null;
      S.forEach(function (s) { for (var a = 0; a <= 7; a++) { var d = new Date(now); d.setDate(now.getDate() + a); d.setHours(s.h, 0, 0, 0);
        if (d.getDay() !== s.day) continue; var end = new Date(d.getTime() + s.len * 60000); if (end > now && (!best || d < best.start)) best = { start: d, s: s }; } });
      if (!best || !valEl) return;
      if (now >= best.start) { box.classList.add('is-live'); if (labEl) labEl.textContent = 'Happening Now'; valEl.textContent = best.s.name + ' · Watch live'; return; }
      box.classList.remove('is-live'); if (labEl) labEl.textContent = 'Next Service';
      var m = Math.round((best.start - now) / 60000), dd = Math.floor(m / 1440), hh = Math.floor(m % 1440 / 60), mm = m % 60;
      valEl.textContent = (best.s.name + ' · in ' + (dd ? dd + 'd ' : '') + (dd || hh ? hh + 'h ' : '') + (dd ? '' : mm + 'm')).trim();
    }
    tick(); setInterval(tick, 30000);
  }

  /* ---- Favicon (until a WordPress Site Icon is set) ---- */
  if (!document.querySelector('link[rel~="icon"]')) {
    var fav = document.createElement('link'); fav.rel = 'icon'; fav.type = 'image/png';
    fav.href = '/wp-content/uploads/2026/11/site-icon.png'; document.head.appendChild(fav);
    var ati = document.createElement('link'); ati.rel = 'apple-touch-icon'; ati.href = fav.href; document.head.appendChild(ati);
  }

  function init() { lightbox(); countdown(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
/* ===== EDWARDS REDESIGN END ===== */
