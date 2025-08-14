// console.log("video.js loaded");

const API_BASE = "http://localhost:8000/api/videos/";

function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

async function loadVideo() {
    const videoId = getQueryParam("id");
    // console.log("Video ID from URL:", videoId);

    if (!videoId) {
        alert("No video selected.");
        window.location.href = "index.html";
        return;
    }

    try {
        // console.log("Fetching:", `${API_BASE}${videoId}/`);
        const res = await fetch(`${API_BASE}${videoId}/`);
        // console.log("Response status:", res.status);

        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }

        const video = await res.json();
        console.log("Video data:", video);

        // Now update the DOM **inside this function**
        document.getElementById("videoTitle").innerText = video.title;
        document.getElementById("videoDescription").innerText = video.description;
        const player = document.getElementById("videoPlayer");
        const source = document.getElementById("videoSource");
        source.src = video.file;
        // console.log("Video src set to:", video.file);
        player.load();

    } catch (err) {
        console.error("Error loading video:", err);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadVideo();
});
