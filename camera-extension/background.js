// Clicking the toolbar icon opens (or focuses) a small camera window.
let camWindowId = null;

chrome.action.onClicked.addListener(async () => {
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
});

chrome.windows.onRemoved.addListener((id) => {
  if (id === camWindowId) camWindowId = null;
});
