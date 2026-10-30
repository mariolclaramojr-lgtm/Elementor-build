/* ===== BETHEL REBRAND START ===== */
/* Bethel Church — global helpers (Theme Options › JS). Editors type plain text; this does the formatting.
   1. H1/H2: the last word gets the accent colour (span.bc-accent); headings of more than five
      words get the last two words. One-word headings stay plain. A heading that already
      contains <em> is left as typed. Moss on light backgrounds, Sage on Forest/photos.
   2. Gravity Forms: each form is marked bc-gf-light / bc-gf-dark from the background it sits on,
      so a new form picks up the right styling automatically. */
(function () {
  // not: forms, top bar + menu bar, off-canvas menu, search/blog result titles, plugin listing titles
  var SKIP = '.gform_wrapper, .bc-topbar, .bc-nav, .x-off-canvas, article .entry-title, .smpro-item, .smpro-archive, .wpfc-sermon, .mec-wrap, [data-bc-no-accent]';

  function lum(rgb) {
    var p = (rgb || '').match(/[\d.]+/g);
    if (!p || p.length < 3) return null;
    if (p.length > 3 && parseFloat(p[3]) < 0.5) return null; // mostly transparent
    return (0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2]) / 255;
  }

  function accentHeading(h) {
    if (h.querySelector('.bc-accent, em') || h.closest(SKIP)) return;
    var words = h.textContent.trim().split(/\s+/).length;
    if (words < 2) return; // one-word headings stay plain
    var walker = document.createTreeWalker(h, NodeFilter.SHOW_TEXT, null), node, last = null;
    while ((node = walker.nextNode())) if (/\S/.test(node.nodeValue)) last = node;
    if (!last) return;
    // more than five words: colour the last two (when they sit in the same text run), else the last one
    var m = (words > 5 && last.nodeValue.match(/^([\s\S]*?)(\S+\s+\S+)(\s*)$/)) || last.nodeValue.match(/^([\s\S]*?)(\S+)(\s*)$/);
    if (!m) return;
    var span = document.createElement('span');
    span.className = 'bc-accent';
    span.textContent = m[2];
    var l = lum(getComputedStyle(h).color);
    if (l !== null && l > 0.6) span.classList.add('is-on-dark');
    var frag = document.createDocumentFragment();
    if (m[1]) frag.appendChild(document.createTextNode(m[1]));
    frag.appendChild(span);
    if (m[3]) frag.appendChild(document.createTextNode(m[3]));
    last.parentNode.replaceChild(frag, last);
  }

  // Dark if the nearest solid background is dark, or the nearest Cornerstone background
  // layer (photo/video/colour under an overlay) is dark.
  function onDark(el) {
    for (var n = el.parentElement; n && n !== document.documentElement; n = n.parentElement) {
      var bg = n.querySelector(':scope > .x-bg');
      if (bg) {
        if (bg.querySelector('.x-bg-layer-lower-image, .x-bg-layer-lower-video, .x-bg-layer-upper-image, .x-bg-layer-upper-video, video, img')) return true;
        var lyr = bg.querySelectorAll('[class*="x-bg-layer"]');
        for (var i = 0; i < lyr.length; i++) { var lb = lum(getComputedStyle(lyr[i]).backgroundColor); if (lb !== null) return lb < 0.5; }
      }
      var l = lum(getComputedStyle(n).backgroundColor);
      if (l !== null) return l < 0.5;
      if (getComputedStyle(n).backgroundImage !== 'none') return true;
    }
    return false;
  }

  function markForm(w) {
    if (w.classList.contains('bc-gf-dark') || w.classList.contains('bc-gf-light')) return;
    w.classList.add(onDark(w) ? 'bc-gf-dark' : 'bc-gf-light');
  }

  function run(root) {
    (root || document).querySelectorAll('h1, h2').forEach(accentHeading);
    (root || document).querySelectorAll('.gform_wrapper, .gform_confirmation_wrapper').forEach(markForm);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { run(); });
  else run();

  // Content loaded later (calendar month change, form confirmation after AJAX submit)
  var t;
  new MutationObserver(function () { clearTimeout(t); t = setTimeout(run, 120); })
    .observe(document.documentElement, { childList: true, subtree: true });
})();
/* ===== BETHEL REBRAND END ===== */
