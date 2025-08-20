// frontend/js/signup.js
const AUTH_API = "http://localhost:8000/api/auth/";

document.getElementById("signupForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    username: document.getElementById("username").value,
    email: document.getElementById("email").value,
    full_name: document.getElementById("full_name").value,  // NEW
    password: document.getElementById("password").value
  };

  try {
    const res = await fetch(`${AUTH_API}signup/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await res.json();
    if (res.ok) {
      saveTokens(result.access, result.refresh);
      showToast("Signup successful! Redirecting...", "success");
      setTimeout(() => window.location.href = "index.html", 1200);
    } else {
      alert(result.error || result.detail || "Signup failed");
    }
  } catch (err) {
    console.error("Error during signup:", err);
    alert("Error during signup");
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
