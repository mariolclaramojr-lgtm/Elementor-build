const video = document.getElementById("video");
const statusEl = document.getElementById("status");
const deviceSelect = document.getElementById("device");
const mirrorBox = document.getElementById("mirror");
const circleBox = document.getElementById("circle");
const pipBtn = document.getElementById("pip");

let stream = null;

const saved = JSON.parse(localStorage.getItem("presenterCam") || "{}");
mirrorBox.checked = saved.mirror ?? true;
circleBox.checked = saved.circle ?? false;

function save() {
  localStorage.setItem("presenterCam", JSON.stringify({
    deviceId: deviceSelect.value,
    mirror: mirrorBox.checked,
    circle: circleBox.checked
  }));
}

function applyStyles() {
  video.classList.toggle("mirror", mirrorBox.checked);
  video.classList.toggle("circle", circleBox.checked);
}

async function startCamera(deviceId) {
  if (stream) stream.getTracks().forEach((t) => t.stop());
  statusEl.textContent = "Starting camera…";
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: {
        deviceId: deviceId ? { exact: deviceId } : undefined,
        width: { ideal: 1280 },
        height: { ideal: 720 }
      },
      audio: false
    });
    video.srcObject = stream;
    statusEl.textContent = "";
  } catch (err) {
    statusEl.textContent =
      err.name === "NotAllowedError"
        ? "Camera access was blocked. Click the camera icon in the address bar (or check chrome://settings/content/camera) and allow it, then reopen this window."
        : `Could not start camera: ${err.message}`;
  }
}

async function listCameras(selectedId) {
  const devices = await navigator.mediaDevices.enumerateDevices();
  const cams = devices.filter((d) => d.kind === "videoinput");
  deviceSelect.innerHTML = "";
  cams.forEach((cam, i) => {
    const opt = document.createElement("option");
    opt.value = cam.deviceId;
    opt.textContent = cam.label || `Camera ${i + 1}`;
    deviceSelect.appendChild(opt);
  });
  if (selectedId && cams.some((c) => c.deviceId === selectedId)) {
    deviceSelect.value = selectedId;
  }
}

deviceSelect.addEventListener("change", () => { save(); startCamera(deviceSelect.value); });
mirrorBox.addEventListener("change", () => { applyStyles(); save(); });
circleBox.addEventListener("change", () => { applyStyles(); save(); });
navigator.mediaDevices.addEventListener("devicechange", () => listCameras(deviceSelect.value));

// Picture-in-Picture: a small always-on-top window that stays visible over
// Slides, other apps, and anything you share in Meet.
pipBtn.addEventListener("click", async () => {
  try {
    if (document.pictureInPictureElement) {
      await document.exitPictureInPicture();
    } else {
      await video.requestPictureInPicture();
    }
  } catch (err) {
    statusEl.textContent = `Pop out failed: ${err.message}`;
  }
});
video.addEventListener("enterpictureinpicture", () => { pipBtn.textContent = "Pop in"; });
video.addEventListener("leavepictureinpicture", () => { pipBtn.textContent = "Pop out"; });

window.addEventListener("beforeunload", () => {
  if (stream) stream.getTracks().forEach((t) => t.stop());
});

(async () => {
  applyStyles();
  await startCamera(saved.deviceId);
  // Labels are only available after permission is granted.
  await listCameras(stream?.getVideoTracks()[0]?.getSettings().deviceId || saved.deviceId);
})();
