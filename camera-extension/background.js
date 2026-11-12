// Opens (or focuses) the floating camera window when the popup asks for it.
let camWindowId = null;

async function openCamWindow() {
  if (camWindowId !== null) {
    try {
      await chrome.windows.update(camWindowId, { focused: true });
      return;
    } catch {
      camWindowId = null; // window was closed
    }
  }
  const win = await chrome.windows.create({
    url: chrome.runtime.getURL("camera.html"),
    type: "popup",
    width: 320,
    height: 350
  });
  camWindowId = win.id;
}

chrome.runtime.onMessage.addListener((msg) => {
  if (msg?.type === "openCamWindow") openCamWindow();
});

chrome.windows.onRemoved.addListener((id) => {
  if (id === camWindowId) camWindowId = null;
});
