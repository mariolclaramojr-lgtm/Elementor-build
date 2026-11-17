/* Edwards Church — shared behaviour for the inner pages
   (menu, sticky header, back-to-top, scroll reveals, forms, video toggles). */
(function () {
  /* Mobile menu */
  var btn = document.querySelector('.menu-toggle'), nav = document.getElementById('site-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) { nav.classList.remove('open'); btn.setAttribute('aria-expanded', false); } });
  }

  /* Header turns solid on scroll; back-to-top appears */
  var header = document.querySelector('.site-header'), toTop = document.querySelector('.to-top');
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('scrolled', y > 60);
    if (toTop) toTop.classList.toggle('show', y > 700);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Scroll reveals */
  var items = document.querySelectorAll('.reveal, .reveal-img');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  } else { items.forEach(function (el) { el.classList.add('in'); }); }

  /* Forms: mockup only — show a thank-you message instead of submitting */
  document.querySelectorAll('form[data-success]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var first = form.querySelector('[name="first"]');
      var name = first && first.value.trim() ? ', ' + first.value.trim() : '';
      var box = document.createElement('div');
      box.className = 'form-success';
      box.setAttribute('role', 'status');
      box.innerHTML = '<span class="tick"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span>' +
        '<h3>Thank you' + name + '!</h3><p>' + form.dataset.success + '</p>';
      form.replaceWith(box);
    });
  });

  /* Accordions: only one open at a time inside a group */
  document.querySelectorAll('.accordion[data-single]').forEach(function (group) {
    group.addEventListener('toggle', function (e) {
      if (!e.target.open) return;
      group.querySelectorAll('details[open]').forEach(function (d) { if (d !== e.target) d.open = false; });
    }, true);
  });

  /* Muted background videos: play / pause button */
  document.querySelectorAll('.video-card').forEach(function (card) {
    var v = card.querySelector('video'), b = card.querySelector('.vc-toggle');
    if (!v || !b) return;
    b.addEventListener('click', function () {
      if (v.paused) { v.play(); b.lastChild.textContent = 'Pause'; } else { v.pause(); b.lastChild.textContent = 'Play'; }
    });
  });
})();
