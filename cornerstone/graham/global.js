/* ===== GRAHAM REDESIGN START ===== */
/* Graham — global helpers (Theme Options › JS). Editors type plain text; this does the formatting.
   Heading accent for H1/H2 inside Graham sections (.gc-section):
     1 word      -> nothing
     2 words     -> last word
     3+ words    -> the second half (rounded up), e.g. "A Church | For the City."
   The accent goes on its own line in italic gold (see global CSS). A heading that already
   contains <em> is left as typed. Add data-gc-no-accent to opt an element out. */
(function () {
  var SKIP = '.x-masthead, .x-colophon, .gform_wrapper, .mec-wrap, .smpro-items, .wpfc-sermon, .tooltipster-box, [data-gc-no-accent]';

  function lum(rgb) {
    var p = (rgb || '').match(/[\d.]+/g);
    if (!p || p.length < 3) return null;
    return (0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2]) / 255;
  }

  function accent(h) {
    if (h.querySelector('.gc-accent, em') || h.closest(SKIP)) return;
    var text = h.textContent.replace(/\s+/g, ' ').trim();
    var words = text.split(' ');
    if (words.length < 2) return;
    var n = words.length === 2 ? 1 : Math.ceil(words.length / 2);
    var target = h.querySelector('.x-text-content-text-primary') || h;
    if (target.children.length) return; // unexpected markup: leave it alone
    var span = document.createElement('span');
    span.className = 'gc-accent';
    span.textContent = words.slice(-n).join(' ');
    var l = lum(getComputedStyle(h).color);
    if (l !== null && l > 0.6) span.classList.add('is-on-dark');
    target.textContent = words.slice(0, words.length - n).join(' ') + ' ';
    target.appendChild(span);
  }

  function run() { document.querySelectorAll('.gc-section h1, .gc-section h2').forEach(accent); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
})();
/* ===== GRAHAM REDESIGN END ===== */
