// Viewport Sizer — service worker.
// All sizing work happens here so it keeps running if the popup closes
// when the window moves or resizes.

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const CDP_VERSION = '1.3';

// ---------- session state (survives service-worker restarts) ----------

async function getState() {
  const { state } = await chrome.storage.session.get('state');
  return state || { emulated: {}, originalBounds: {} };
}
async function setState(state) {
  await chrome.storage.session.set({ state });
}

// ---------- helpers ----------

async function activeTab() {
  const [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
  if (!tab) throw new Error('No active tab found.');
  return tab;
}

// The size of the page's viewport in CSS pixels (what media queries see).
async function viewportOf(tabId) {
  const tab = await chrome.tabs.get(tabId);
  let zoom = 1;
  try { zoom = await chrome.tabs.getZoom(tabId); } catch (_) {}
  return {
    width: Math.round(tab.width / zoom),
    height: Math.round(tab.height / zoom),
    zoom,
  };
}

function isRestrictedUrl(url = '') {
  return /^(chrome|edge|about|chrome-extension|devtools|view-source):/i.test(url) ||
    url.startsWith('https://chrome.google.com/webstore') ||
    url.startsWith('https://chromewebstore.google.com');
}

// ---------- mode 1 & 3: size a real window so the viewport matches ----------

async function fitWindowToViewport(windowId, tabId, width, height) {
  let win = await chrome.windows.get(windowId);
  if (win.state !== 'normal') {
    await chrome.windows.update(windowId, { state: 'normal' });
    await sleep(250);
  }

  // Window and tab sizes are in device-independent pixels; the page sees
  // CSS pixels, which differ when the page is zoomed.
  let zoom = 1;
  try { zoom = await chrome.tabs.getZoom(tabId); } catch (_) {}
  const targetW = Math.round(width * zoom);
  const targetH = height ? Math.round(height * zoom) : null;

  // Browser chrome (toolbar, borders, docked DevTools…) varies, so measure
  // the difference and correct a few times until the viewport lands exactly.
  for (let i = 0; i < 5; i++) {
    win = await chrome.windows.get(windowId);
    const tab = await chrome.tabs.get(tabId);
    const okW = tab.width === targetW;
    const okH = targetH == null || tab.height === targetH;
    if (okW && okH) break;

    const update = {};
    if (!okW) update.width = Math.max(1, win.width + (targetW - tab.width));
    if (!okH) update.height = Math.max(1, win.height + (targetH - tab.height));
    try {
      await chrome.windows.update(windowId, update);
    } catch (e) {
      // Chrome refuses bounds that push the window mostly off-screen:
      // move it to the top-left corner and try again.
      try {
        await chrome.windows.update(windowId, { ...update, left: 0, top: 0 });
      } catch (_) {
        break; // larger than the screen allows — report what we got
      }
    }
    await sleep(120 + i * 80);
  }

  const result = await viewportOf(tabId);
  result.exact = result.width === width && (!height || result.height === height);
  return result;
}

async function resizeCurrentWindow(tab, opts) {
  const state = await getState();
  const key = String(tab.windowId);
  if (!state.originalBounds[key]) {
    const win = await chrome.windows.get(tab.windowId);
    state.originalBounds[key] = {
      left: win.left, top: win.top, width: win.width, height: win.height, state: win.state,
    };
    await setState(state);
  }
  // Emulation would mask the real viewport, so drop it first.
  if (state.emulated[tab.id]) await stopEmulation(tab.id);
  return fitWindowToViewport(tab.windowId, tab.id, opts.width, opts.height);
}

async function openInNewWindow(tab, opts) {
  const url = opts.url || tab.url;
  const win = await chrome.windows.create({
    url,
    type: 'popup',
    width: opts.width + 16,
    height: (opts.height || 800) + 90,
    focused: true,
  });
  const newTab = win.tabs && win.tabs[0];
  if (!newTab) throw new Error('Could not open the new window.');
  await sleep(300);
  return fitWindowToViewport(win.id, newTab.id, opts.width, opts.height);
}

// ---------- mode 2: device emulation through the DevTools protocol ----------

function mobileUserAgent() {
  const m = navigator.userAgent.match(/Chrome\/([\d.]+)/);
  const v = m ? m[1].split('.')[0] + '.0.0.0' : '130.0.0.0';
  return `Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${v} Mobile Safari/537.36`;
}

function send(tabId, method, params = {}) {
  return chrome.debugger.sendCommand({ tabId }, method, params);
}

async function emulate(tab, opts) {
  if (isRestrictedUrl(tab.url)) {
    throw new Error('Chrome does not allow emulation on this page. Try a normal website.');
  }
  const state = await getState();
  if (!state.emulated[tab.id]) {
    try {
      await chrome.debugger.attach({ tabId: tab.id }, CDP_VERSION);
    } catch (e) {
      if (!/already attached/i.test(e.message)) {
        throw new Error('Could not attach: ' + e.message + ' (close DevTools on this tab and try again).');
      }
    }
    // The "is debugging this browser" bar shrinks the tab; let it settle.
    await sleep(250);
  }

  const width = opts.width;
  const height = opts.height || (await viewportOf(tab.id)).height;
  const dpr = Number(opts.dpr) || 0; // 0 = keep the screen's real ratio
  const mobile = !!opts.mobile;

  // Scale the page down if the emulated viewport is bigger than the tab.
  const t = await chrome.tabs.get(tab.id);
  const scale = opts.fit === false ? 1 : Math.min(1, t.width / width, t.height / height);

  await send(tab.id, 'Emulation.setDeviceMetricsOverride', {
    width, height, deviceScaleFactor: dpr, mobile,
    scale: Math.max(0.1, Math.floor(scale * 1000) / 1000),
    screenWidth: width, screenHeight: height,
    screenOrientation: width > height
      ? { type: 'landscapePrimary', angle: 90 }
      : { type: 'portraitPrimary', angle: 0 },
  });
  await send(tab.id, 'Emulation.setTouchEmulationEnabled', { enabled: mobile, maxTouchPoints: mobile ? 5 : 1 });
  await send(tab.id, 'Emulation.setEmitTouchEventsForMouse', { enabled: mobile, configuration: 'mobile' }).catch(() => {});
  await send(tab.id, 'Emulation.setUserAgentOverride', { userAgent: mobile ? mobileUserAgent() : '' });

  state.emulated[tab.id] = { width, height, dpr, mobile };
  await setState(state);

  if (opts.reload) await chrome.tabs.reload(tab.id);
  return { width, height, zoom: 1, exact: true, emulated: true, scale };
}

async function stopEmulation(tabId) {
  try {
    await send(tabId, 'Emulation.clearDeviceMetricsOverride');
    await send(tabId, 'Emulation.setTouchEmulationEnabled', { enabled: false });
    await send(tabId, 'Emulation.setUserAgentOverride', { userAgent: '' });
  } catch (_) {}
  try { await chrome.debugger.detach({ tabId }); } catch (_) {}
  const state = await getState();
  delete state.emulated[tabId];
  await setState(state);
}

chrome.debugger.onDetach.addListener(async ({ tabId }) => {
  // User clicked "Cancel" on the debugging bar, or the tab closed.
  const state = await getState();
  if (tabId != null && state.emulated[tabId]) {
    delete state.emulated[tabId];
    await setState(state);
  }
});

chrome.tabs.onRemoved.addListener(async (tabId) => {
  const state = await getState();
  if (state.emulated[tabId]) { delete state.emulated[tabId]; await setState(state); }
});

chrome.windows.onRemoved.addListener(async (windowId) => {
  const state = await getState();
  if (state.originalBounds[windowId]) { delete state.originalBounds[windowId]; await setState(state); }
});

// ---------- actions ----------

async function apply(opts) {
  const width = Math.round(Number(opts.width));
  const height = opts.height ? Math.round(Number(opts.height)) : null;
  if (!width || width < 1 || width > 10000) throw new Error('Enter a width between 1 and 10000.');
  if (height != null && (height < 1 || height > 10000)) throw new Error('Enter a height between 1 and 10000.');
  const o = { ...opts, width, height };

  const tab = await activeTab();
  await chrome.storage.local.set({ lastApplied: o });

  if (o.mode === 'emulate') return emulate(tab, o);
  if (o.mode === 'window') return openInNewWindow(tab, o);
  return resizeCurrentWindow(tab, o);
}

async function reset() {
  const tab = await activeTab();
  const state = await getState();
  let did = false;
  if (state.emulated[tab.id]) { await stopEmulation(tab.id); did = true; }
  const b = state.originalBounds[tab.windowId];
  if (b) {
    await chrome.windows.update(tab.windowId, { left: b.left, top: b.top, width: b.width, height: b.height });
    if (b.state && b.state !== 'normal') await chrome.windows.update(tab.windowId, { state: b.state });
    const s2 = await getState();
    delete s2.originalBounds[tab.windowId];
    await setState(s2);
    did = true;
  }
  await sleep(150);
  return { ...(await viewportOf(tab.id)), didReset: did };
}

async function status() {
  const tab = await activeTab();
  const state = await getState();
  const vp = await viewportOf(tab.id);
  return {
    ...vp,
    url: tab.url,
    restricted: isRestrictedUrl(tab.url),
    emulation: state.emulated[tab.id] || null,
    canRestore: !!state.originalBounds[tab.windowId],
  };
}

chrome.runtime.onMessage.addListener((msg, _sender, reply) => {
  const run = { apply: () => apply(msg.options), reset, status }[msg.type];
  if (!run) return false;
  run().then((data) => reply({ ok: true, data }), (e) => reply({ ok: false, error: e.message }));
  return true; // async reply
});

chrome.commands.onCommand.addListener(async (command) => {
  try {
    if (command === 'reset') return await reset();
    if (command === 'reapply-last') {
      const { lastApplied } = await chrome.storage.local.get('lastApplied');
      if (lastApplied) await apply({ ...lastApplied, mode: lastApplied.mode === 'window' ? 'resize' : lastApplied.mode });
    }
  } catch (e) {
    console.warn('Viewport Sizer:', e.message);
  }
});
