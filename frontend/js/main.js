// frontend/js/main.js
console.log("main.js loaded");

const VIDEO_API = "http://localhost:8000/api/videos/";

// Fetch all videos
async function fetchVideos() {
    try {
        const res = await apiFetch(VIDEO_API);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return await res.json();
    } catch (err) {
        console.error("Error fetching videos:", err);
        return [];
    }
}

// Render video cards
function renderVideos(videos, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = "";

    videos.forEach(video => {
        const card = document.createElement("div");
        card.className = "video-card";
        card.innerHTML = `
            <img src="${video.thumbnails || 'https://via.placeholder.com/200x120'}" alt="${video.title}">
            <p>${video.title}</p>
        `;
        card.onclick = () => {
            window.location.href = `video.html?id=${video.id}`;
        };
        container.appendChild(card);
    });
}

// Initialize homepage
(async function init() {
    checkAuth();
    renderNav();

    const videos = await fetchVideos();
    renderVideos(videos.slice(0, 5), "trending-row");
    renderVideos(videos.slice(5), "recent-row");
})();
