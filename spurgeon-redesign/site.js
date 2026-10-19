/* Spurgeon Church redesign — shared script.
   Only what Cornerstone does natively (sticky header, mobile menu, accordion,
   scroll fade) plus small helpers that move into the live site as-is
   (form thank-you, ministry pre-select, sermon filters, events view toggle). */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");

  /* Header: transparent over the hero, cream + hairline after 40px */
  var header = document.querySelector(".site-header");
  function onScroll() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 40);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* Mobile menu (Navigation Modal on the live site) */
  var toggle = document.querySelector(".menu-toggle");
  function setMenu(open) {
    header.classList.toggle("menu-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  }
  if (toggle && header) {
    toggle.addEventListener("click", function () { setMenu(!header.classList.contains("menu-open")); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && header.classList.contains("menu-open")) { setMenu(false); toggle.focus(); }
    });
    header.querySelectorAll(".nav a").forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
  }

  /* Accordion */
  document.querySelectorAll(".acc-trigger").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!open));
      btn.closest(".acc-item").classList.toggle("is-open", !open);
    });
  });

  /* Fade up on enter */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-visible"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* Forms: required-field validation, then a thank-you message */
  document.querySelectorAll("form[data-form]").forEach(function (form) {
    form.setAttribute("novalidate", "");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var firstBad = null;
      form.querySelectorAll("[required]").forEach(function (input) {
        var field = input.closest(".field");
        var err = field && field.querySelector(".field-error");
        var ok = input.checkValidity() && input.value.trim() !== "";
        if (field) field.classList.toggle("has-error", !ok);
        input.setAttribute("aria-invalid", String(!ok));
        if (err) {
          err.textContent = ok ? "" : (input.type === "email" && input.value ? "Please enter a valid email." : "This field is required.");
        }
        if (!ok && !firstBad) firstBad = input;
      });
      if (firstBad) { firstBad.focus(); return; }
      var thanks = document.getElementById(form.getAttribute("data-form"));
      form.hidden = true;
      if (thanks) { thanks.hidden = false; thanks.setAttribute("tabindex", "-1"); thanks.focus(); }
    });
  });

  /* Get Connected: pre-select the ministry in the sign-up form */
  var ministrySelect = document.getElementById("signup-ministry");
  function preselect(value) {
    if (!ministrySelect || !value) return;
    Array.prototype.forEach.call(ministrySelect.options, function (o) {
      if (o.value.toLowerCase() === value.toLowerCase()) ministrySelect.value = o.value;
    });
  }
  if (ministrySelect) {
    preselect(new URLSearchParams(location.search).get("ministry"));
    document.querySelectorAll("[data-ministry]").forEach(function (a) {
      a.addEventListener("click", function () { preselect(a.getAttribute("data-ministry")); });
    });
  }

  /* Messages: filter by speaker / series / topic / book (?speaker=…&series=…) */
  var filterForm = document.getElementById("sermon-filters");
  if (filterForm) {
    var params = new URLSearchParams(location.search);
    var cards = document.querySelectorAll(".sermon-card");
    var empty = document.getElementById("sermon-empty");
    ["speaker", "series", "topic", "book"].forEach(function (k) {
      var sel = filterForm.elements[k];
      if (sel && params.get(k)) sel.value = params.get(k);
    });
    var apply = function () {
      var shown = 0;
      cards.forEach(function (card) {
        var match = ["speaker", "series", "topic", "book"].every(function (k) {
          var v = filterForm.elements[k].value;
          return !v || (card.getAttribute("data-" + k) || "").split(" ").indexOf(v) > -1;
        });
        card.hidden = !match;
        if (match) shown++;
      });
      if (empty) empty.hidden = shown > 0;
    };
    apply();
    filterForm.addEventListener("change", apply);
    filterForm.addEventListener("reset", function () { setTimeout(apply, 0); });
    filterForm.addEventListener("submit", function (e) { e.preventDefault(); apply(); });
  }

  /* Events: month grid from the Select Month / Select Year menus */
  var calForm = document.getElementById("event-filters");
  if (calForm) {
    var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    var now = new Date();
    var mSel = calForm.elements.month, ySel = calForm.elements.year;
    mSel.value = String(now.getMonth());
    if (ySel.querySelector('option[value="' + now.getFullYear() + '"]')) ySel.value = String(now.getFullYear());
    var grid = document.getElementById("cal-days");
    var label = document.getElementById("cal-label");
    var render = function () {
      var m = +mSel.value, y = +ySel.value;
      var first = new Date(y, m, 1).getDay();
      var days = new Date(y, m + 1, 0).getDate();
      var prevDays = new Date(y, m, 0).getDate();
      var html = "";
      var cells = Math.ceil((first + days) / 7) * 7;
      for (var i = 0; i < cells; i++) {
        var d = i - first + 1, cls = "", n = d;
        if (d < 1) { n = prevDays + d; cls = "muted"; }
        else if (d > days) { n = d - days; cls = "muted"; }
        else if (y === now.getFullYear() && m === now.getMonth() && d === now.getDate()) cls = "today";
        html += '<div class="' + cls + '">' + n + "</div>";
      }
      grid.innerHTML = html;
      label.textContent = months[m] + " " + y;
    };
    render();
    calForm.addEventListener("change", render);
  }

  /* Events: Monthly / List / Tile views */
  document.querySelectorAll(".view-toggle button").forEach(function (btn) {
    btn.addEventListener("click", function () {
      btn.parentElement.querySelectorAll("button").forEach(function (b) { b.setAttribute("aria-pressed", String(b === btn)); });
      document.querySelectorAll(".cal-view").forEach(function (v) { v.hidden = v.id !== btn.getAttribute("aria-controls"); });
    });
  });
})();
