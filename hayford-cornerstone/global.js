/* ===== HAYFORD REDESIGN START ===== */
/* Hayford — global helpers (Theme Options › JS). Editors type plain headings; this adds the accent.
   H1/H2: one word stays plain, 2–5 words → last word, 6+ words → last two words get span.hf-accent
   (Instrument Serif italic, accent colour; lighter accent when the heading text is light/on dark).
   A heading that already contains <em> or .hf-accent is left alone. Add data-hf-no-accent to opt out. */
(function () {
  var SKIP = '.gform_wrapper, .x-off-canvas, .x-modal, article .entry-title, .smpro-item, .wpfc-sermon, .mec-wrap, .mec-container, [data-hf-no-accent]';
  function lum(rgb) {
    var p = (rgb || '').match(/[\d.]+/g);
    if (!p || p.length < 3) return null;
    return (0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2]) / 255;
  }
  function accent(h) {
    if (h.querySelector('.hf-accent, em') || h.closest(SKIP)) return;
    var words = h.textContent.trim().split(/\s+/).length;
    if (words < 2) return;
    var walker = document.createTreeWalker(h, NodeFilter.SHOW_TEXT, null), node, last = null;
    while ((node = walker.nextNode())) if (/\S/.test(node.nodeValue)) last = node;
    if (!last) return;
    var m = (words > 5 && last.nodeValue.match(/^([\s\S]*?)(\S+\s+\S+)(\s*)$/)) || last.nodeValue.match(/^([\s\S]*?)(\S+)(\s*)$/);
    if (!m) return;
    var span = document.createElement('span');
    span.className = 'hf-accent';
    span.textContent = m[2];
    var l = lum(getComputedStyle(h).color);
    if (l !== null && l > 0.6) span.classList.add('is-on-dark');
    var frag = document.createDocumentFragment();
    if (m[1]) frag.appendChild(document.createTextNode(m[1]));
    frag.appendChild(span);
    if (m[3]) frag.appendChild(document.createTextNode(m[3]));
    last.parentNode.replaceChild(frag, last);
  }
  function run() { document.querySelectorAll('h1, h2').forEach(accent); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
/* ===== HAYFORD REDESIGN END ===== */
