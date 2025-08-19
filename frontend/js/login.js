// frontend/js/login.js
const AUTH_API = "http://localhost:8000/api/auth/";

document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    username: document.getElementById("username").value,
    password: document.getElementById("password").value
  };

  try {
    const res = await fetch(`${AUTH_API}login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await res.json();
    if (res.ok) {
      saveTokens(result.access, result.refresh);
      showToast("Login successful! Redirecting...", "success");
      setTimeout(() => window.location.href = "index.html", 1200);
    } else {
      alert(result.detail || result.error || "Login failed");
    }
  } catch (err) {
    console.error("Error during login:", err);
    alert("Error during login");
  }
});

document.addEventListener("DOMContentLoaded", () => {
  redirectIfLoggedIn();
  renderNav();
});

// =========== Toast Notification ===========
function showToast(message, type = "") {
  let toast = document.createElement("div");
  toast.className = `custom-toast ${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.classList.add("show"), 100);
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 400);
  }, 2000);
}
