const $ = (s) => document.querySelector(s);
const MODE_HINTS = {
  resize: 'Resizes this window so the page viewport is exactly the size you set. Windows can’t go narrower than ~500px — use Emulate for phones.',
  emulate: 'Emulates the viewport inside this tab at any size, with pixel ratio, touch and mobile user agent. Chrome shows a “debugging” bar while active.',
  window: 'Opens the page (or the URL below) in a new window with this exact viewport.',
};

let mode = 'resize';
let custom = [];

function send(type, extra = {}) {
  return chrome.runtime.sendMessage({ type, ...extra }).then((res) => {
    if (!res || !res.ok) throw new Error(res ? res.error : 'No response from the extension.');
    return res.data;
  });
}

function setMsg(text, kind = '') {
  const el = $('#msg');
  el.textContent = text;
  el.className = 'msg ' + kind;
}

function setMode(m) {
  mode = m;
  document.querySelectorAll('.seg button').forEach((b) => {
    const on = b.dataset.mode === m;
    b.classList.toggle('on', on);
    b.setAttribute('aria-selected', on);
  });
  document.body.dataset.mode = m;
  $('#mode-hint').textContent = MODE_HINTS[m];
  chrome.storage.local.set({ mode: m });
}

async function refreshStatus() {
  try {
    const s = await send('status');
    $('#cur-size').textContent = `${s.width} × ${s.height}` + (s.zoom !== 1 ? ` @ ${Math.round(s.zoom * 100)}%` : '');
    const badge = $('#cur-badge');
    if (s.emulation) {
      badge.hidden = false;
      badge.textContent = `Emulating ${s.emulation.width} × ${s.emulation.height}`;
    } else if (s.canRestore) {
      badge.hidden = false;
      badge.textContent = 'Resized';
    } else {
      badge.hidden = true;
    }
    return s;
  } catch (e) {
    $('#cur-size').textContent = '—';
  }
}

function readForm() {
  return {
    mode,
    width: Number($('#w').value),
    height: $('#h').value ? Number($('#h').value) : null,
    dpr: Number($('#dpr').value),
    mobile: $('#mobile').checked,
    reload: $('#reload').checked,
    url: $('#url').value.trim() || null,
  };
}

function fillForm(p) {
  $('#w').value = p.width ?? '';
  $('#h').value = p.height ?? '';
  if (p.dpr != null) {
    const v = String(p.dpr);
    if (![...$('#dpr').options].some((o) => o.value === v)) $('#dpr').add(new Option(v + '×', v));
    $('#dpr').value = v;
  } else {
    $('#dpr').value = '0';
  }
  $('#mobile').checked = !!p.mobile;
}

async function apply(opts) {
  if (opts.url && !/^[a-z][\w+.-]*:/i.test(opts.url)) opts.url = 'https://' + opts.url;
  setMsg('Applying…');
  try {
    const r = await send('apply', { options: opts });
    chrome.storage.local.set({ form: opts });
    if (r.emulated) {
      const pct = Math.round(r.scale * 100);
      setMsg(`Emulating ${r.width} × ${r.height}` + (pct < 100 ? ` (shown at ${pct}% to fit)` : '') + '.', 'ok');
    } else if (r.exact) {
      setMsg(`Viewport is now ${r.width} × ${r.height}.`, 'ok');
    } else {
      setMsg(`Got ${r.width} × ${r.height} — the window hit a size limit (screen or OS minimum). Try Emulate for an exact size.`, 'warn');
    }
    if (mode !== 'window') refreshStatus();
  } catch (e) {
    setMsg(e.message, 'err');
  }
}

function chip(p, onRemove) {
  const b = document.createElement('button');
  b.type = 'button';
  b.className = 'chip';
  const dims = p.height ? `${p.width}×${p.height}` : `${p.width}w`;
  b.innerHTML = `<span class="lbl"></span><span class="dim"></span>`;
  b.querySelector('.lbl').textContent = p.label;
  b.querySelector('.dim').textContent = !p.label.includes(String(p.width)) ? dims
    : (p.height && !p.label.includes(String(p.height)) ? `×${p.height}` : '');
  b.title = `${dims}${p.dpr ? ` · ${p.dpr}×` : ''}${p.mobile ? ' · mobile' : ''}\nClick to apply${onRemove ? ' · right-click to delete' : ''}`;
  b.addEventListener('click', () => {
    fillForm(p);
    apply({ ...readForm(), ...p, mode });
  });
  if (onRemove) {
    b.addEventListener('contextmenu', (e) => { e.preventDefault(); onRemove(); });
  }
  return b;
}

function renderPresets() {
  const root = $('#presets');
  root.textContent = '';
  const groups = [...PRESET_GROUPS];
  if (custom.length) groups.unshift({ name: 'Saved', items: custom, removable: true });
  for (const g of groups) {
    const h = document.createElement('h2');
    h.textContent = g.name;
    const wrap = document.createElement('div');
    wrap.className = 'chips';
    g.items.forEach((p, i) => {
      wrap.append(chip(p, g.removable ? async () => {
        custom.splice(i, 1);
        await chrome.storage.sync.set({ custom });
        renderPresets();
      } : null));
    });
    root.append(h, wrap);
  }
}

async function init() {
  const { mode: savedMode, form } = await chrome.storage.local.get(['mode', 'form']);
  ({ custom = [] } = await chrome.storage.sync.get('custom'));
  setMode(savedMode || 'resize');
  renderPresets();

  const s = await refreshStatus();
  if (form) {
    fillForm(form);
    $('#reload').checked = !!form.reload;
  } else if (s) {
    fillForm({ width: s.width, height: s.height });
  }

  document.querySelectorAll('.seg button').forEach((b) => b.addEventListener('click', () => setMode(b.dataset.mode)));

  $('#form').addEventListener('submit', (e) => {
    e.preventDefault();
    apply(readForm());
  });

  $('#rotate').addEventListener('click', () => {
    const w = $('#w').value, h = $('#h').value;
    if (!h) return;
    $('#w').value = h;
    $('#h').value = w;
  });

  $('#save').addEventListener('click', async () => {
    const f = readForm();
    if (!f.width) return setMsg('Enter a width first.', 'err');
    const label = (f.height ? `${f.width} × ${f.height}` : `${f.width}w`) + (f.mobile ? ' mobile' : '');
    const p = { label, width: f.width };
    if (f.height) p.height = f.height;
    if (f.dpr) p.dpr = f.dpr;
    if (f.mobile) p.mobile = true;
    custom.push(p);
    await chrome.storage.sync.set({ custom });
    renderPresets();
    setMsg(`Saved “${label}”. Right-click a saved preset to delete it.`, 'ok');
  });

  $('#reset').addEventListener('click', async () => {
    try {
      const r = await send('reset');
      setMsg(r.didReset ? `Reset — viewport is ${r.width} × ${r.height}.` : 'Nothing to reset on this tab.', r.didReset ? 'ok' : '');
      refreshStatus();
    } catch (e) {
      setMsg(e.message, 'err');
    }
  });
}

init();
