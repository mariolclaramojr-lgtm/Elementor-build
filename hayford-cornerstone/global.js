/* ===== HAYFORD REDESIGN START ===== */
/* Favicon + Apple touch icon (Hayford mark, Media Library "hayford-sprout-site-icon.png").
   Prefer WordPress › Appearance › Customize › Site Identity › Site Icon; once that is set this block can be removed. */
(function () {
  if (document.querySelector('link[rel~="icon"][href*="cropped-"]')) return; // WP Site Icon already set
  var src = 'https://rrnewhayford.wpenginepowered.com/wp-content/uploads/2026/11/hayford-sprout-site-icon.png';
  [['icon', 'image/png'], ['apple-touch-icon', '']].forEach(function (r) {
    document.querySelectorAll('link[rel="' + r[0] + '"]').forEach(function (l) { l.remove(); });
    var l = document.createElement('link'); l.rel = r[0]; l.href = src; if (r[1]) l.type = r[1];
    document.head.appendChild(l);
  });
})();
/* ===== HAYFORD REDESIGN END ===== */
