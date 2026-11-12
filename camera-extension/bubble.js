// Injected into the tab you want to present. Adds a draggable, resizable
// round camera bubble. Running it again removes the bubble.
(() => {
  const existing = document.getElementById("presenter-cam-bubble");
  if (existing) {
    existing.__presenterCamStop?.();
    return;
  }

  const host = document.createElement("div");
  host.id = "presenter-cam-bubble";
  Object.assign(host.style, {
    position: "fixed", right: "24px", bottom: "24px", width: "200px", height: "200px",
    zIndex: "2147483647", borderRadius: "50%", cursor: "grab", touchAction: "none"
  });
  const root = host.attachShadow({ mode: "open" });
  root.innerHTML = `
    <style>
      :host { all: initial; }
      .wrap { position: relative; width: 100%; height: 100%; border-radius: 50%; overflow: hidden;
        background: #000; box-shadow: 0 4px 16px rgba(0,0,0,.35); }
      video { width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); display: block; pointer-events: none; }
      .msg { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; padding: 20px;
        text-align: center; color: #fff; font: 12px system-ui, sans-serif; }
      .msg:empty { display: none; }
      button { position: absolute; width: 26px; height: 26px; border-radius: 50%; border: none; cursor: pointer;
        background: rgba(0,0,0,.65); color: #fff; font: 14px/26px system-ui, sans-serif; padding: 0;
        opacity: 0; transition: opacity .15s; }
      :host(:hover) button { opacity: 1; }
      .close { top: 12%; right: 12%; }
      .flip { top: 12%; left: 12%; }
      .resize { bottom: 8%; right: 8%; cursor: nwse-resize; }
    </style>
    <div class="wrap">
      <video autoplay playsinline muted></video>
      <div class="msg">Starting camera…</div>
    </div>
    <button class="flip" title="Mirror on/off">⇋</button>
    <button class="close" title="Remove camera">✕</button>
    <button class="resize" title="Drag to resize">⤡</button>`;

  const video = root.querySelector("video");
  const msgEl = root.querySelector(".msg");
  let stream = null;
  let mirrored = true;

  function stop() {
    stream?.getTracks().forEach((t) => t.stop());
    document.removeEventListener("fullscreenchange", placeHost);
    host.remove();
  }
  host.__presenterCamStop = stop;

  root.querySelector(".close").addEventListener("click", stop);
  root.querySelector(".flip").addEventListener("click", () => {
    mirrored = !mirrored;
    video.style.transform = mirrored ? "scaleX(-1)" : "none";
  });

  // Drag to move; drag the corner button to resize.
  let mode = null, startX, startY, startRect;
  host.addEventListener("pointerdown", (e) => {
    const path = e.composedPath();
    if (path.some((el) => el.classList?.contains("close") || el.classList?.contains("flip"))) return;
    mode = path.some((el) => el.classList?.contains("resize")) ? "resize" : "move";
    startX = e.clientX; startY = e.clientY;
    startRect = host.getBoundingClientRect();
    host.setPointerCapture(e.pointerId);
    host.style.cursor = "grabbing";
    e.preventDefault();
  });
  host.addEventListener("pointermove", (e) => {
    if (!mode) return;
    const dx = e.clientX - startX, dy = e.clientY - startY;
    if (mode === "move") {
      const left = Math.min(Math.max(0, startRect.left + dx), innerWidth - startRect.width);
      const top = Math.min(Math.max(0, startRect.top + dy), innerHeight - startRect.height);
      Object.assign(host.style, { left: left + "px", top: top + "px", right: "auto", bottom: "auto" });
    } else {
      const size = Math.max(80, Math.min(600, startRect.width + Math.max(dx, dy)));
      Object.assign(host.style, {
        left: startRect.left + "px", top: startRect.top + "px", right: "auto", bottom: "auto",
        width: size + "px", height: size + "px"
      });
    }
  });
  const endDrag = () => { mode = null; host.style.cursor = "grab"; };
  host.addEventListener("pointerup", endDrag);
  host.addEventListener("pointercancel", endDrag);

  // When the page goes fullscreen (e.g. Slides "Present"), only the fullscreen
  // element is visible, so move the bubble inside it.
  function placeHost() {
    const target = document.fullscreenElement || document.documentElement;
    if (host.parentNode !== target) target.appendChild(host);
    video.play().catch(() => {});
  }
  document.addEventListener("fullscreenchange", placeHost);
  placeHost();

  navigator.mediaDevices.getUserMedia({ video: { width: { ideal: 1280 }, height: { ideal: 720 } }, audio: false })
    .then((s) => {
      if (!host.isConnected) { s.getTracks().forEach((t) => t.stop()); return; }
      stream = s;
      video.srcObject = s;
      msgEl.textContent = "";
    })
    .catch((err) => {
      msgEl.textContent = err.name === "NotAllowedError"
        ? "Camera blocked. Allow it with the camera icon in the address bar, then try again."
        : "Camera error: " + err.message;
    });
})();
