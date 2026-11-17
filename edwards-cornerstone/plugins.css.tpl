/* ---------- Checklist (Text elements with class ed-checklist) ---------- */
.ed-checklist ul { list-style: none; margin: 0; padding: 0; display: grid; gap: .8rem; }
.ed-checklist li { display: grid; grid-template-columns: 30px minmax(0,1fr); gap: .8rem; align-items: center; font-weight: 500; color: {slate}; margin: 0; }
.ed-checklist li::before { content: ""; width: 30px; height: 30px; border-radius: 50%;
  background: {accent} url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 12.5l4.5 4.5L19 7.5'/%3E%3C/svg%3E") center / 16px no-repeat; }

/* ---------- Gravity Forms (all forms) ---------- */
.gform_wrapper.gform_wrapper { font-family: {font}; margin: 0; }
.gform_wrapper .gform_fields { display: grid; gap: 1.15rem; }
.gform_wrapper ul.gform_fields li.gfield { margin: 0 !important; padding: 0 !important; }
.gform_wrapper .gfield_label { font-size: .72rem !important; font-weight: 700 !important; letter-spacing: .16em; text-transform: uppercase; color: {slate} !important; margin-bottom: .45rem !important; }
.gform_wrapper .gfield_required { color: {accent} !important; }
.gform_wrapper .ginput_complex label, .gform_wrapper .gfield_description, .gform_wrapper .ginput_complex .name_first label, .gform_wrapper .ginput_complex .name_last label { font-size: .78rem !important; color: {text-soft} !important; letter-spacing: 0; padding-top: .35rem; }
.gform_wrapper input:not([type=submit]):not([type=button]):not([type=checkbox]):not([type=radio]):not([type=file]),
.gform_wrapper textarea, .gform_wrapper select {
  width: 100% !important; font-family: {font} !important; font-size: 1rem !important; color: {text} !important;
  background: {mist} !important; border: 1px solid transparent !important; border-radius: 8px !important;
  padding: .85rem 1rem !important; box-shadow: none !important; transition: border-color .25s, background-color .25s, box-shadow .25s; }
.gform_wrapper textarea { min-height: 130px; }
.gform_wrapper input:focus, .gform_wrapper textarea:focus, .gform_wrapper select:focus { outline: none !important; background: #fff !important; border-color: {accent} !important; box-shadow: 0 0 0 4px {accent-18} !important; }
.gform_wrapper .ginput_container_date { display: flex; align-items: center; gap: .5rem; }
.gform_wrapper .gform-datepicker-toggle { color: {slate}; }
.gform_wrapper .gform_footer { margin: 1.4rem 0 0 !important; padding: 0 !important; }
.gform_wrapper .gform_footer input[type=submit], .gform_wrapper .gform_footer button, .gform_wrapper .gform_button {
  font-family: {font} !important; font-size: .8rem !important; font-weight: 600 !important; letter-spacing: .16em !important; text-transform: uppercase !important;
  color: #fff !important; background: {slate} !important; border: 0 !important; border-radius: 8px !important; padding: 1.15em 1.9em !important;
  cursor: pointer; transition: background-color .4s ease, transform .3s ease; }
.gform_wrapper .gform_footer input[type=submit]:hover, .gform_wrapper .gform_button:hover { background: {accent} !important; transform: translateY(-2px); }
.gform_wrapper .validation_message, .gform_wrapper .gform_validation_errors, .gform_wrapper div.validation_error { color: #b3261e !important; border-radius: 8px; font-size: .85rem; }
.gform_confirmation_message { font-family: {font}; font-size: 1.1rem; color: {slate}; background: {mist}; border-left: 3px solid {accent}; padding: 1.4rem 1.6rem; border-radius: 0 12px 12px 0; }

/* ---------- Sermon Manager Pro ([smpro_archive]) ---------- */
.smpro-items, .smpro-items * { font-family: {font} !important; }
.smpro-items .sm-filtering { margin-bottom: 2.5rem !important; }
.smpro-items .sm-filtering select { appearance: none; -webkit-appearance: none; min-width: 180px; font-size: .95rem; color: {slate};
  background: #fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%232F3E4C' stroke-width='2' stroke-linecap='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E") no-repeat right .8rem center / 16px;
  border: 1px solid {rule}; border-radius: 8px; padding: 0 2.4rem 0 1rem; height: 48px !important; line-height: 46px !important; cursor: pointer; transition: border-color .25s; }
.smpro-items .sm-filtering select:hover, .smpro-items .sm-filtering select:focus { border-color: {accent}; outline: none; }
.smpro-item { background: #fff !important; border: 1px solid {rule} !important; border-radius: 18px !important; overflow: hidden; transition: transform .5s cubic-bezier(.22,.61,.36,1), box-shadow .5s; }
.smpro-item:hover { transform: translateY(-6px); box-shadow: 0 30px 60px -30px {slate-deep-45}; }
.smpro-image { overflow: hidden; }
.smpro-image__background { transition: transform 1s cubic-bezier(.22,.61,.36,1); }
.smpro-item:hover .smpro-image__background { transform: scale(1.06); }
.smpro-item__main { padding: 1.6rem 1.6rem 1.4rem !important; }
.smpro-meta-item_type_date .smpro-meta-item__text { font-size: .7rem; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; color: {accent}; }
.smpro-meta-item_type_series .smpro-meta-item__text { font-size: .72rem; font-weight: 600; color: {slate} !important; background: {mist}; padding: .3rem .7rem; border-radius: 999px; }
.smpro-title { margin: .7rem 0 .5rem !important; }
.smpro-title__text, .smpro-title__text.smpro-title__text { font-size: 1.45rem !important; font-weight: 700 !important; letter-spacing: -.02em; line-height: 1.2; color: {slate} !important; text-decoration: none !important; }
.smpro-title__text:hover { color: {accent} !important; }
.smpro-meta-item__prefix { font-weight: 700; color: {slate}; font-style: normal !important; }
.smpro-meta-item__text_linked, .smpro-items a.rtBibleRef { color: {accent} !important; text-decoration: none !important; }
.smpro-meta-item__text_linked:hover { color: {slate} !important; }
.smpro-description { color: {text-soft} !important; line-height: 1.7; }
.smpro-meta-item_type_bible-passage { font-style: normal !important; color: {text-soft}; }
.smpro-items .libronixLinkImage, .smpro-items .rtLibronix { display: none !important; }
.smpro-item__footer { border-top: 1px solid {rule} !important; }
.smpro-item__meta .smpro-meta-item__text { font-size: .74rem; background: {mist}; color: {slate} !important; padding: .3rem .7rem; border-radius: 999px; }
.smpro-item__meta .smpro-meta-item__text:hover { background: {accent}; color: #fff !important; }
.smpro-item__meta .smpro-meta-item::after, .smpro-item__meta .smpro-meta-item + .smpro-meta-item::before { display: none !important; }
.smpro-share .a2a_svg { background-color: {slate} !important; border-radius: 50% !important; transition: background-color .3s; }
.smpro-share a:hover .a2a_svg { background-color: {accent} !important; }

/* ---------- Modern Events Calendar ([MEC id="52"]) ---------- */
.mec-wrap, .mec-wrap *:not(i):not([class*="mec-sl-"]):not([class*="mec-fa-"]) { font-family: {font} !important; }
.mec-wrap .mec-totalcal-box { background: #fff; border: 1px solid {rule}; border-radius: 18px; padding: 1.2rem; box-shadow: 0 20px 40px -34px {slate-deep-45}; }
.mec-wrap .mec-totalcal-box input, .mec-wrap .mec-totalcal-box select { border-radius: 8px !important; border-color: {rule} !important; color: {slate} !important; }
.mec-wrap .mec-totalcal-box i { color: {accent} !important; }
.mec-wrap .mec-totalcal-box .mec-totalcal-view span { border-color: {rule} !important; color: {text-soft} !important; font-weight: 700; letter-spacing: .08em; transition: all .3s; }
.mec-wrap .mec-totalcal-box .mec-totalcal-view span:first-child { border-radius: 999px 0 0 999px; }
.mec-wrap .mec-totalcal-box .mec-totalcal-view span:last-child { border-radius: 0 999px 999px 0; }
.mec-wrap .mec-totalcal-box .mec-totalcal-view span:hover { color: {accent} !important; }
.mec-wrap .mec-totalcal-box .mec-totalcal-view span.mec-totalcalview-selected { background: {slate} !important; border-color: {slate} !important; color: #fff !important; }
.mec-wrap .mec-month-divider h2, .mec-wrap .mec-month-divider span { color: {slate} !important; font-weight: 700 !important; letter-spacing: -.01em; text-transform: none !important; }
.mec-wrap .mec-month-divider i { color: {accent} !important; }
.mec-wrap .mec-event-list-standard .mec-event-article { border: 1px solid {rule} !important; border-radius: 18px !important; overflow: hidden; box-shadow: none !important; transition: transform .45s cubic-bezier(.22,.61,.36,1), box-shadow .45s; }
.mec-wrap .mec-event-list-standard .mec-event-article:hover { transform: translateY(-4px); box-shadow: 0 30px 60px -30px {slate-deep-45} !important; }
.mec-wrap .mec-event-image { overflow: hidden; }
.mec-wrap .mec-event-image img { transition: transform 1s cubic-bezier(.22,.61,.36,1); }
.mec-wrap .mec-event-article:hover .mec-event-image img { transform: scale(1.06); }
.mec-wrap .mec-event-title, .mec-wrap .mec-event-title a { color: {slate} !important; font-weight: 700 !important; letter-spacing: -.01em; }
.mec-wrap .mec-event-title a:hover, .mec-wrap .mec-color-hover:hover { color: {accent} !important; }
.mec-wrap .mec-repeating-label { background: {accent} !important; border-radius: 999px; }
.mec-wrap .mec-event-description { color: {text-soft} !important; }
.mec-wrap .mec-event-meta i, .mec-wrap .mec-event-meta svg, .mec-wrap .mec-color, .mec-wrap .mec-color-before :before, .mec-wrap .mec-event-sharing-wrap i { color: {accent} !important; fill: {accent} !important; }
.mec-wrap .mec-event-meta .mec-date-details, .mec-wrap .mec-event-meta .mec-time-details { color: {slate}; font-weight: 600; }
.mec-wrap .mec-event-footer { background: {mist} !important; border-top: 1px solid {rule} !important; }
.mec-wrap .mec-booking-button { border-radius: 8px !important; border-color: {slate} !important; color: {slate} !important; background: transparent !important; font-weight: 600 !important; letter-spacing: .14em !important; transition: all .35s !important; }
.mec-wrap .mec-booking-button:hover { background: {slate} !important; color: #fff !important; }
.mec-wrap .mec-calendar .mec-calendar-events-sec, .mec-wrap .mec-calendar { border-radius: 18px; }
.mec-wrap .mec-calendar .mec-selected-day, .mec-wrap .mec-calendar .mec-has-event:after { background: {accent} !important; }
.mec-wrap .mec-calendar .mec-calendar-row dt.mec-has-event:hover, .mec-wrap .mec-calendar .mec-calendar-side .mec-next-month:hover, .mec-wrap .mec-calendar .mec-calendar-side .mec-previous-month:hover { color: {accent} !important; }
.mec-wrap .mec-event-tile-view article.mec-tile-item { border-radius: 18px; overflow: hidden; }
