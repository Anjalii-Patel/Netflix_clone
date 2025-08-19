// console.log("video.js loaded");

const API_BASE = "http://localhost:8000/api/videos/";

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
        const res = await fetch(`${API_BASE}${videoId}/`);
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }

        const video = await res.json();
        console.log("Video data:", video);

        // Update title + description
        document.getElementById("videoTitle").innerText = video.title;
        document.getElementById("videoDescription").innerText = video.description;

        // Initialize player and set HLS stream
        const player = videojs("videoPlayer");
        player.src({
            src: video.playback_url,   // e.g. http://localhost:8000/media/hls/1/master.m3u8
            type: "application/x-mpegURL"
        });

    } catch (err) {
        console.error("Error loading video:", err);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadVideo();
});
