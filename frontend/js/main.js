// fetch('http://localhost:8000/api/videos/')
//     .then(response => {
//         if (!response.ok) {
//             throw new Error(`HTTP error! Status: ${response.status}`);
//         }
//         return response.json();
//     })
//     .then(videos => {
//         const container = document.getElementById('video-list');
//         container.innerHTML = ''; // Clear old content if any

//         videos.forEach(video => {
//             container.innerHTML += `
//                 <div class="col-md-3 mb-4">
//                     <div class="card bg-secondary">
//                         <video width="100%" controls>
//                             <source src="${video.file}" type="video/mp4">
//                             Your browser does not support the video tag.
//                         </video>
//                         <div class="card-body">
//                             <h5 class="card-title">${video.title}</h5>
//                             <p class="card-text">${video.description || ''}</p>
//                         </div>
//                     </div>
//                 </div>
//             `;
//         });
//     })
//     .catch(err => console.error('Error fetching videos:', err));

console.log("main.js loaded");

const API_BASE = "http://localhost:8000/api/videos/";

// Fetch all videos from API
async function fetchVideos() {
    try {
        const res = await fetch(API_BASE);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const videos = await res.json();
        return videos;
    } catch (err) {
        console.error("Error fetching videos:", err);
        return [];
    }
}

// Render video cards in a container
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
    const videos = await fetchVideos();
    // Split into trending and recent for demo
    renderVideos(videos.slice(0, 5), "trending-row");
    renderVideos(videos.slice(5), "recent-row");
})();
