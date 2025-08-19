// frontend/js/auth.js
console.log("auth.js loaded");

const API_BASE = "http://localhost:8000/api/auth/";

// ================== TOKEN HELPERS ==================
function getAccess() {
    return localStorage.getItem("access");
}
function getRefresh() {
    return localStorage.getItem("refresh");
}
function saveTokens(access, refresh) {
    if (access) localStorage.setItem("access", access);
    if (refresh) localStorage.setItem("refresh", refresh);
}
function clearTokens() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
}

// ================== AUTH CHECK ==================
function checkAuth() {
    const token = getAccess();
    if (!token) {
        window.location.href = "login.html";
    }
}

function redirectIfLoggedIn() {
    if (getAccess()) {
        window.location.href = "index.html";
    }
}

// ================== LOGOUT ==================
function logout() {
    clearTokens();
    window.location.href = "login.html";
}

// ================== NAV RENDER ==================
function renderNav() {
    const nav = document.getElementById("nav-links");
    if (!nav) return;

    nav.innerHTML = "";

    if (getAccess()) {
        nav.innerHTML = `
            <a href="index.html">Home</a>
            <a href="#" onclick="logout()">Logout</a>
        `;
    } else {
        nav.innerHTML = `
            <a href="index.html">Home</a>
            <a href="login.html">Login</a>
            <a href="signup.html">Signup</a>
        `;
    }
}

// ================== AUTO REFRESH ==================
async function refreshAccessToken() {
    const refresh = getRefresh();
    if (!refresh) return null;

    try {
        const res = await fetch(`${API_BASE}token/refresh/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh })
        });

        if (!res.ok) {
            clearTokens();
            return null;
        }

        const data = await res.json();
        saveTokens(data.access, null); // only access refreshed
        return data.access;
    } catch (err) {
        console.error("Error refreshing token:", err);
        clearTokens();
        return null;
    }
}

// ================== UNIVERSAL FETCH ==================
async function apiFetch(url, options = {}, retry = true) {
    let access = getAccess();

    options.headers = {
        ...(options.headers || {}),
        "Content-Type": "application/json",
        ...(access ? { "Authorization": `Bearer ${access}` } : {})
    };

    const res = await fetch(url, options);

    // If unauthorized, try refresh once
    if (res.status === 401 && retry && getRefresh()) {
        const newAccess = await refreshAccessToken();
        if (newAccess) {
            return apiFetch(url, options, false);
        } else {
            logout();
        }
    }

    return res;
}
