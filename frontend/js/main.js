fetch('http://localhost:8000/api/videos/')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(videos => {
        const container = document.getElementById('video-list');
        container.innerHTML = ''; // Clear old content if any

        videos.forEach(video => {
            container.innerHTML += `
                <div class="col-md-3 mb-4">
                    <div class="card bg-secondary">
                        <video width="100%" controls>
                            <source src="${video.file}" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>
                        <div class="card-body">
                            <h5 class="card-title">${video.title}</h5>
                            <p class="card-text">${video.description || ''}</p>
                        </div>
                    </div>
                </div>
            `;
        });
    })
    .catch(err => console.error('Error fetching videos:', err));
