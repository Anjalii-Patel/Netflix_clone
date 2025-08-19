// frontend/js/video.js
const VIDEO_API = "http://localhost:8000/api/videos/";

function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

async function loadVideo() {
    const videoId = getQueryParam("id");
    if (!videoId) {
        alert("No video selected.");
        window.location.href = "index.html";
        return;
    }

    try {
        const res = await apiFetch(`${VIDEO_API}${videoId}/`);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

        const video = await res.json();
        console.log("Video data:", video);

        document.getElementById("videoTitle").innerText = video.title;
        document.getElementById("videoDescription").innerText = video.description;

        const player = videojs("videoPlayer");
        player.src({
            src: video.playback_url,
            type: "application/x-mpegURL"
        });

    } catch (err) {
        console.error("Error loading video:", err);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    checkAuth();
    renderNav();
    loadVideo();
});
