// frontend/js/video.js
const API_VIDEOS = "http://localhost:8000/api/videos/";

function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

async function getPlayUrl(videoId) {
  // POST /api/videos/{id}/play-url/
  const res = await apiFetch(`${API_VIDEOS}${videoId}/play-url/`, {
    method: "POST",
    body: JSON.stringify({})
  });
  if (res.status === 402) {
    // requires subscription
    window.location.href = `subscribe.html?next=video.html?id=${videoId}`;
    return null;
  }
  if (!res.ok) {
    console.error("play-url failed", await res.text());
    alert("Unable to start playback.");
    return null;
  }
  const data = await res.json();
  return data.playback_url;
}

async function loadVideo() {
  checkAuth();
  renderNav();

  const videoId = getQueryParam("id");
  if (!videoId) {
    alert("No video selected.");
    window.location.href = "index.html";
    return;
  }

  // we can still fetch metadata if you want title/desc via GET /videos/{id}/
  try {
    const metaRes = await apiFetch(`${API_VIDEOS}${videoId}/`);
    if (metaRes.ok) {
      const v = await metaRes.json();
      document.getElementById("videoTitle").innerText = v.title || "";
      document.getElementById("videoDescription").innerText = v.description || "";
    }
  } catch (_) {}

  const playbackUrl = await getPlayUrl(videoId);
  if (!playbackUrl) return;

  const player = videojs("videoPlayer");
  player.src({ src: playbackUrl, type: "application/x-mpegURL" });
}

document.addEventListener("DOMContentLoaded", loadVideo);
