const msg = document.getElementById("msg");

document.getElementById("tab").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  try {
    await chrome.scripting.executeScript({ target: { tabId: tab.id }, files: ["bubble.js"] });
    window.close();
  } catch {
    msg.textContent = "Chrome doesn't allow extensions on this page. Switch to the tab you want to present (like Google Slides) and try again.";
  }
});

document.getElementById("window").addEventListener("click", () => {
  chrome.runtime.sendMessage({ type: "openCamWindow" });
  window.close();
});
